# SnakeLean

A Lean 4 library that generates runnable, idiomatic Python code from Lean definitions.

## Project Structure

```
SnakeLean/
├── SnakeLean.lean   # Main library (~1000 lines)
├── Test.lean           # Basic usage example
├── TestSuite.lean      # Comprehensive test suite (~40 functions)
├── lakefile.toml       # Lake build configuration
├── lean-toolchain      # Lean version (4.12.0)
├── CLAUDE.md           # Development documentation (this file)
└── README.md           # User-facing documentation
```

## Building

```bash
lake build
```

## Testing

```bash
# Run basic test
lake env lean Test.lean

# Run comprehensive test suite
lake env lean TestSuite.lean > test.py
python3 test.py
```

To verify generated Python works:
```bash
lake env lean TestSuite.lean > test.py
python3 -c "
exec(open('test.py').read())
assert factorial(5) == 120
assert fib(10) == 55
print('Tests passed!')
"
```

## Usage

```lean
import SnakeLean

open Lean SnakeLean

def myFunction (x y : Nat) : Nat := x + y

#eval show CoreM Unit from do
  let code ← emitPythonForNames `MyModule [`myFunction]
  IO.println code
```

Output:
```python
def my_function(x: int, y: int) -> int:
    _x_4 = x + y
    return _x_4
```

## Architecture

The library works by:
1. Using `toDecl` to compile Lean definitions to LCNF (Lean Compiler Normal Form)
2. Traversing the LCNF AST and emitting corresponding Python code
3. Recognizing type class instance patterns and inlining operations
4. Converting common operations to Python operators
5. Handling partial application patterns from LCNF
6. Emitting custom inductive types as Python dataclasses

### Key Files

- `SnakeLean.lean` - Main library (~1000 lines)
- `Test.lean` - Example usage with tests
- `TestSuite.lean` - Comprehensive test suite

### Main Entry Points

- `emitPythonForNames` - Compile specific declarations by name and emit Python (recommended)
- `emitPythonForDecls` - Emit Python from pre-compiled LCNF declarations

### Type Class Instance Handling

Type class instances (like `instHAdd`, `instHMul`, `instBEq`) are recognized and their operations are inlined:
- `instHAdd` / `instAddNat` → `+`
- `instHSub` / `instSubNat` → `-`
- `instHMul` / `instMulNat` → `*`
- `instHDiv` → `//` (integer), but **Float `/` → `/`** real division (the concrete
  Float `Div` instance is tagged `floatdiv`; `x/0` yields IEEE `±inf`/`nan` to
  match Lean, not a Python `ZeroDivisionError`)
- `instHMod` → `%`
- `instHPow` → `**`
- `instBEq*` → `==`
- `instNeg*` → `-` (unary)
- `instHAppend*` / `instAppend*` → `+` (string concatenation)

### Float Support

Floats are IEEE-754 float64 on both sides (bit-identical, incl. transcendentals
via libm), so the differential oracle uses **strict equality** (values serialized
by exact bit pattern, not truncating `toString`). Handled:
- **Literals** (`3.14…`): Lean's `OfScientific.ofScientific m sign e` (reached via
  an `instOfScientific` projection) → the exact decimal `<m>e±<e>`.
- **`/`**: real division (see above), NOT integer `//`.
- **Methods** → `math.*`: `Float.sqrt/sin/cos/tan/asin/acos/atan/atan2/exp/log/
  floor/ceil` and `Float.abs` → `abs`. `import math` is always emitted.
- **Comparisons**: `Float.decLt/decLe/decEq` → `< / <= / ==` (IEEE NaN semantics
  match Python).

The pattern recognition:
1. `const instHAdd` → tracked as instance, not emitted
2. `proj HAdd.0` → tracked as extracted op
3. `fvar _extracted_op (x, y)` → emitted as `x + y`

### Comparison Handling

Decidable comparisons are converted to Python operators:
- `Nat.decLt` / `Int.decLt` → `<`
- `Nat.decLe` / `Int.decLe` → `<=`
- `Decidable.decide` → alias to comparison result

### Literal Handling

`instOfNat*` patterns are recognized to properly inline numeric literals:
- `const instOfNatNat` after a literal → tracked
- `proj OfNat.0` from it → the literal value is inlined

### Custom Inductive Types

Custom inductive types are automatically emitted as Python dataclasses:
```lean
inductive Color where
  | red | green | blue
```
becomes:
```python
@dataclass
class red:
    pass

@dataclass
class green:
    pass

@dataclass
class blue:
    pass

Color = red | green | blue
```

### Python Type Mappings

| Lean Type | Python Type |
|-----------|-------------|
| `Nat`, `Int`, `UInt*` | `int` |
| `String` | `str` |
| `Bool` | `bool` |
| `Float` | `float` |
| `Unit`, `PUnit` | skipped |
| `List α` | `list[T]` |
| `Array α` | `list[T]` |
| `Option α` | `T \| None` |
| `α × β` | `tuple[A, B]` |
| `α → β` | `Callable[[A], B]` |
| Custom inductive | `@dataclass` |

### Special Case Handling

- **Nat pattern matching**: `match n with | 0 => ... | k+1 => ...` becomes `if n == 0: ... else: k = n - 1; ...`
- **Bool pattern matching**: Becomes `if discr: true_case else: false_case`
- **Bool constructors**: `Bool.true` → `True`, `Bool.false` → `False`
- **Unit values**: Skipped entirely (both in params and args)
- **Partial application**: LCNF thunks are translated to Python function references
- **Option matching**: `if opt is None: ... else: val = opt; ...`
- **List matching**: `if len(xs) == 0: ... else: head = xs[0]; tail = xs[1:]; ...`
- **Tuple access**: `p.1` → `p[0]`, `p.2` → `p[1]`
- **Tuple construction**: `(a, b)` → `(a, b)`
- **Lambda inlining into comprehensions**: `xs.map (fun x => x + 1)` → `[x + 1 for x in xs]` rather than a helper `def`. See below.
- **Set comprehensions**: `List.eraseDups` / `.toFinset` / `.toSet` → a Python set comprehension `{x for x in xs}`. If the argument was itself a `map`/`filter` comprehension, the two fuse into one set comprehension (`{f(x) for x in xs}`) and the now-dead intermediate line is removed.
- **Tail-call elimination**: a function whose self-recursive calls are all in tail position is rewritten into a `while True:` loop (parallel parameter rebind + `continue`) so deep recursion does not overflow the Python stack. See below.

### Tail-Call Elimination Architecture

Lean performs TCO; Python does not, so a naively-translated tail-recursive Lean
function overflows the Python stack (`RecursionError`, ~900 deep) where Lean
runs in constant stack. (Non-tail recursion — e.g. `factorial` — is O(n) stack
in *both* Lean and Python, so it is deliberately left recursive; matching Lean
means only self-*tail* recursion is optimized. Mutual recursion is likewise
left as-is.)

Detection (`isSelfTailRecursive`) is pure LCNF analysis and deliberately
**sound** — it only fires when it can prove the rewrite is safe:
1. `scanSelfCalls` walks the `Code` tree tracking a `tailCtx` flag. A self-call
   (`const declName`) counts as tail iff it is in tail context and its result
   fvar is immediately returned. The flag is propagated through tail-calls to
   local continuation thunks (`_alt`) and join-point jumps, resolving zero-arg
   fvar aliases (`_alt := _f`) via `collectFunAliases`. Any self-call reached
   in non-tail context fails the check.
2. `recursionThunksSingleUse` requires every recursion-carrying continuation
   thunk to be called from at most one site (LCNF's usual single-use
   continuation). A multiply-called thunk would have its body duplicated when
   inlined, so such functions fall back to plain recursive emission.

Emission (in `emitDecl` + `emitCode`, gated by `tailLoop` state):
- The body is wrapped in `while True:` and the (non-unit) parameter names are
  recorded in `tailLoop`.
- A tail self-call becomes `emitTailStep`: a parallel tuple rebind of the loop
  parameters (`n, acc = <arg1>, <arg2>`) followed by `continue`. Parallel
  assignment is essential — it matches Lean's simultaneous parameter update
  (e.g. `gcd`'s `a, b = b, a % b`).
- LCNF buries most tail calls inside single-use `_alt` continuation thunks
  (nested `def`s), where Python's `continue` would be illegal. Those thunks are
  detected (`codeHasSelfCall`), suppressed at their definition site, and
  inlined at their tail-call site via `emitInlinedThunk` (binding the thunk's
  params to the call args) so the `continue` lands in the enclosing loop.
- Base-case thunks that don't carry recursion stay as ordinary nested `def`s.

### Lambda Inlining Architecture

In LCNF, `xs.map (fun x => x + 1)` lowers the lambda to a local `def _f(x): ...`
(a let-chain ending in `return`) that the combinator references by name — which
naively yields `[_f(x) for x in xs]`. To inline it:

1. `emitLocalFun` detects a single-(non-unit-)parameter lambda and attempts to
   render its body as one Python expression via `renderExprCode` /
   `renderLetValueExpr` (string-returning analogues of `emitLetValue`). On
   success it **defers** the lambda — recording `(paramName, bodyExpr)` in
   `deferredLambdas` and emitting no `def`. On failure it rolls back all
   render-time state mutations (via a `State` snapshot) and emits a normal `def`.
2. Comprehension-producing combinators (`List.map`/`filter`/`filterMap`/`bind`/
   `any`/`all`/`find?`/`findSome?`) call `fnCompParts`, which inlines a deferred
   lambda's body with its own binder, or falls back to `f(x)` for a named
   function argument.
3. A deferred lambda used as a plain value (e.g. a match-arm thunk, or passed to
   an un-inlined function) is materialized back into `(lambda p: body)` at the
   use site (`emitArg` and the `.fvar` call path).

The renderer is deliberately **conservative**: it inlines only arithmetic,
comparison, string append, `Nat.succ`, tuple projection, extracted-instance
operators, `Char.*`-style stdlib callables (`isConstFnSafeToInline`), and calls
to already-known local functions. Anything else (constructors like `List.cons`,
`OfNat`, `bne`, `List.contains`, nested `cases`/`fun`) returns `none` so the
lambda falls back to a correct `def` — never a call to an undefined name.

## Example Output

Input (Lean):
```lean
def factorial (n : Nat) : Nat :=
  match n with
  | 0 => 1
  | k + 1 => (k + 1) * factorial k
```

Output (Python):
```python
def factorial(n: int) -> int:
    def _f_116():
        _x_113 = 1
        return 1
    _alt_117 = _f_116
    def _f_130(k: int):
        _x_127 = k + 1
        _x_128 = factorial(k)
        _x_129 = _x_127 * _x_128
        return _x_129
    _alt_131 = _f_130
    if n == 0:
        _x_133 = _alt_117()
        return _x_133
    else:
        n_134 = n - 1
        _x_135 = _alt_131(n_134)
        return _x_135
```

## Extending

To add support for more builtin operations, modify:
- `natBinOp?` - Direct Nat/Int binary operations
- `hOpToPyOp?` - Operations through type class instances
- `isInstanceCtor` - Instance names to recognize and skip
- `builtinFn?` - Builtin functions like `len`, `not`

## Known Limitations

1. Pattern matching generates verbose code with inner functions (LCNF structure)
2. Some unused intermediate variables may be emitted
3. Variable names have numeric suffixes for uniqueness
4. Generic type parameters are erased to `Any`
5. No IO monad support (pure functions only)
6. Some type class projections (e.g., `Max`, `Xor`) emit incorrect code
7. Only *self*-tail recursion is loop-optimized. Non-tail recursion is left
   recursive (Lean overflows it too, so this matches Lean); mutual tail
   recursion is not yet optimized. Deep cases of these can still overflow the
   Python stack.
8. **Nested `Option`** (`Option (Option α)`, or `(xs : List (Option α))[i]?`)
   is unfaithful: Python models `Option` as `None`, so `some none` and `none`
   collapse to the same `None` and a `match` that distinguishes them diverges
   from Lean (e.g. `TicTacToe.validMoves`, excluded from the fuzz corpus via
   `corpus_frags._KNOWN_OPEN_FNS`). A faithful fix needs a sentinel-based Option
   representation (e.g. a `Nothing`/`Just` wrapper) rather than bare `None`.

## Future Work: Mathlib Integration

Adding Mathlib to the corpus would provide a much larger test suite:

### Steps to Add Mathlib

1. **Update Lean toolchain** - Mathlib requires specific Lean versions
2. **Add Mathlib dependency** to lakefile.toml:
   ```toml
   [[require]]
   name = "mathlib"
   scope = "leanprover-community"
   rev = "master"
   ```
3. **Create Mathlib corpus module** extracting key functions:
   - `Nat.factorial`, `Nat.choose`
   - `List.sum`, `List.prod`
   - `Finset` operations
   - Basic algebra operations

### Expected Challenges

- Mathlib uses heavy type class machinery
- Many definitions are noncomputable
- Universe polymorphism complications
- Large import graph increases compile times

### Recommended Approach

1. Start with Mathlib's `Init` and `Data.List.Basic`
2. Focus on computable definitions first
3. Add special handlers for Mathlib-specific patterns
4. Track extraction quality separately from core corpus

## Development Process for High-Quality Extractors

The SnakeLean extractor is developed using an iterative, feedback-driven process:

### 1. Corpus-Based Development

Build a comprehensive corpus of Lean functions to test extraction quality:

```
Corpus/
├── Algorithms.lean   # Sorting, searching, numeric algorithms
├── DataStructures.lean  # Stack, Queue, Tree, Graph, Trie
├── Math.lean         # Number theory, combinatorics
├── Functional.lean   # Higher-order functions, Option, Either
├── Strings.lean      # String manipulation
├── Games.lean        # Game logic (TicTacToe, Nim, Blackjack)
└── Parsers.lean      # Parser combinators
```

The corpus should include:
- Simple arithmetic and recursion
- Pattern matching on various types (Nat, Bool, Option, List, custom inductives)
- Higher-order functions (map, filter, fold)
- Type class usage (comparison, arithmetic)
- Complex data structures

### 2. Automated Quality Analysis

After each extraction, run automated checks:

```bash
# Generate Python from corpus
lake env lean --run Corpus/CorpusTestCombined.lean 2>/dev/null > corpus.py

# Check for errors with ruff
ruff check corpus.py 2>&1 | grep -E "^F821|^F811|^E731"

# F821 = Undefined name (critical bugs)
# F811 = Redefinition (name collisions)
# E731 = Lambda assignment (style)
```

Track progress by counting errors over time:

| Date | F821 | F811 | E731 | Notes |
|------|------|------|------|-------|
| Start | ~4860 | ? | ? | Initial corpus |
| Session 1 | 188 | 32 | 9 | After basic fixes |
| Current | **12** | **0** | **9** | After namespace fixes |

### 3. Traceability

Every emitted function includes a comment tracing back to Lean:

```python
# Lean: Corpus.Algorithms.fibonacci
def algorithms_fibonacci(n: int) -> int:
    ...
```

This makes it easy to find the source of extraction errors.

### 4. Fix Categories

Address issues in priority order:

**Critical (F821 - Undefined names):**
- Missing type definitions → emit dataclasses
- Missing stdlib functions → add explicit handlers
- Name collisions → add namespace prefixes
- Type class projection failures → improve instance tracking

**Medium (F811 - Redefinitions):**
- Same function name in different modules → module prefix
- Same helper name in different functions → grandparent prefix

**Low Priority (E731 - Style):**
- Lambda assignments → could convert to def
- Verbose thunks → could inline simple cases

### 5. Common Patterns to Handle

Each pattern requires specific handling:

| Pattern | Example | Solution |
|---------|---------|----------|
| List comprehensions | `List.map (fun x => x+1)` | `[x + 1 for x in xs]` (lambda body inlined) |
| Set comprehensions | `List.eraseDups`, `.toFinset`, `.toSet` | `{x for x in xs}` (fuses upstream map/filter) |
| Safe indexing | `GetElem?` | `lambda xs, i: xs[i] if 0 <= i < len(xs) else None` |
| Tuple construction | `Prod.mk a b` | `(a, b)` |
| String from chars | `String.mk cs` | `''.join(cs)` |
| Successor | `Nat.succ n` | `n + 1` |
| Name collisions | Multiple `empty` | Module prefix: `stack_empty`, `queue_empty` |
| Helper collisions | Multiple `fibonacci.go` | Grandparent prefix: `algorithms_fibonacci_go` |

### 6. Verification

After fixes, verify working functions:

```python
# In Python
assert algorithms_fibonacci(10) == 55
assert algorithms_gcd(48, 18) == 6
assert algorithms_is_prime(17) == True
assert insertion_sort([3,1,4,1,5]) == [1, 1, 3, 4, 5]
```

### 7. Documentation

Maintain EXTRACTION_ISSUES.md documenting:
- Current error counts
- Working functions
- Fixed issues
- Remaining issues
- Suggested priorities

## Development Notes

### Adding New Operators

To support a new builtin operation:

1. **Direct operations** (like `Nat.add`): Add to `natBinOp?`
2. **Type class operations** (like `HAdd`): Add to `hOpToPyOp?`
3. **Instance constructors** to skip: Update `isInstanceCtor`
4. **Builtin functions** (like `len`): Add to `builtinFn?`

### Debugging LCNF

To see what LCNF is generated for a function:

```lean
import SnakeLean
open Lean Lean.Compiler.LCNF

def myFn (x : Nat) : Nat := x + 1

partial def dumpCode (c : Code) : CompilerM Unit := do
  match c with
  | .let decl k =>
    IO.println s!"let {decl.binderName} = ..."
    dumpCode k
  | .return fv => IO.println s!"return {fv.name}"
  | _ => pure ()

#eval Lean.Compiler.LCNF.CompilerM.run do
  let decl ← toDecl `myFn
  dumpCode decl.value
```

### Key State Fields

- `instanceVars`: Maps FVarId to instance name (for skipping)
- `extractedOps`: Maps FVarId to (instance, field index) for inlining
- `literalVars`: Maps FVarId to literal value (for OfNat inlining)
- `varAliases`: Maps FVarId to FVarId (for decide patterns)
- `boolVars`: Tracks variables holding True/False
- `unitVars`: Tracks unit values (skipped in calls)
