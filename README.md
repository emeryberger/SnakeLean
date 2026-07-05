# LeanToPython

A Lean 4 to Python transpiler that extracts idiomatic Python code from Lean's LCNF (Lean Compiler Normal Form).

## Overview

LeanToPython converts Lean 4 functions into readable Python code by working directly from the compiler's intermediate representation. Unlike runtime-based approaches, this produces standalone Python that:

- Reads like hand-written Python
- Uses native Python data structures (lists, dicts, tuples, dataclasses)
- Requires no special runtime library
- Can be understood and modified by Python developers

## Correctness

Faithful transpilation is checked at four complementary layers, from
hand-written unit tests up to a differential oracle where **Lean itself is the
ground truth**. Each layer catches a different class of bug; together they are
the regression gate for changes to the transpiler.

See [`VERIFICATION.md`](VERIFICATION.md) for the full bug ledger — every
transpilation bug the differential harness and the fuzzer have caught and
fixed, with root cause, minimal reproducer, and fix.

### 1. Unit test suite — `evaluate_correctness.py`

Runs the transpiled Python for 27 representative functions against
hand-written expected values (132 input/output cases). LCNF extraction passes
**132/132 (100%)**. This is the quick end-to-end smoke test.

| Category | Functions |
|----------|-----------|
| Numeric algorithms | gcd, factorial, fibonacci, is_prime, prime_factors, lcm, coprime |
| Sorting | insertion_sort, merge_sort |
| Searching | binary_search, linear_search |
| Math | pow, abs, binomial, fast_pow, mod_pow, digit_sum, num_digits, is_palindrome_num |
| Strings | reverse_str, to_upper, to_lower |
| Heap operations | left_child, right_child, parent |
| Predicates | is_even, is_odd |

```bash
python3 evaluate_correctness.py
```

### 2. Structural regression tests — `*_test.py`

`Comprehensions_test.py`, `TailCalls_test.py`, and `RegressionFixes_test.py`
each `exec` the Python extracted from a paired `.lean` module and assert both
*semantic* results and *structural* properties the semantics alone would not
catch — e.g. that a lambda actually inlines into a comprehension, that a
self-tail-recursive function becomes a `while True:` loop (constant stack), and
that `Decidable`-cases branch order is not swapped. Each pins a specific
transpiler behavior so a regression fails loudly.

```bash
lake env lean Comprehensions.lean > Comprehensions_out.py && python3 Comprehensions_test.py
lake env lean TailCalls.lean      > TailCalls_out.py      && python3 TailCalls_test.py
lake env lean RegressionFixes.lean > RegressionFixes_out.py && python3 RegressionFixes_test.py
```

### 3. Round-trip differential harness — `roundtrip/` (Lean as oracle)

The strongest layer: rather than trusting hand-written expected values, it uses
**Lean itself as the oracle**. Lean `#eval`s each corpus function on a battery
of inputs and emits the result; the runner execs the transpiled Python on the
same inputs and asserts equality. Two modes:

- **Sampled** (`Oracle.lean`): a curated battery across 21 monomorphic corpus
  functions — **112/112 agree**.
- **Exhaustive** (`Exhaustive.lean`): the *entire* bounded input domain for 12
  functions — all `n ∈ [0,60]` (unary) and all `(x,y) ∈ [0,25]²` (binary),
  **3807/3807 agree** — so there is no untested input in range.

```bash
./roundtrip/run.sh
```

See [`roundtrip/README.md`](roundtrip/README.md) for how the oracle stays
decoupled from the transpiler's naming and how polymorphic arguments are
handled. This is empirical differential testing against an oracle (exhaustive
*within the stated bounds*), not a proof of transpiler correctness — but it is
exactly the kind of evidence that catches real bugs. Several were found and
fixed this way: a dropped `default` arm in list/option matches, un-collected
transitive callees, an unmapped `List.lengthTR`, and `Eq.ndrec`/`cast`
proof-term leakage.

### 4. Full-corpus extraction as a smoke test

Transpiling the entire corpus (~550 functions) and parsing the result with
Python's `ast` catches structural regressions — dropped match arms, malformed
blocks, undefined names — across a much wider surface than the curated suites.

```bash
lake build Corpus
lake env lean Corpus/CorpusTestCombined.lean > /tmp/corpus.py
python3 -c "import ast, sys; ast.parse(open('/tmp/corpus.py').read()); print('syntax OK')"
```

### 5. Grammar-based differential fuzzing — `fuzz/`

`fuzz/gen.py` generates random **well-typed, terminating** Lean function
definitions from a small typed grammar (over `Nat` / `Bool` / `List Nat` /
`Nat × Nat`, exercising `if`/`match`, `let`, tuples, arithmetic incl. truncated
`Nat` subtraction, list combinators, `DecidableEq`, and fuel-bounded recursion).
Generation is **coverage-guided** (it prefers grammar productions not yet
exercised — see [5] below). Each generated program is run through the same
**Lean-as-oracle** pipeline as layer 3; any parse error, runtime exception, or
Python/Lean value mismatch is a transpilation bug. Failures are automatically
**shrunk** to a minimal reproducer saved under `fuzz/repro/`, and seeds are
deterministic so a failure reproduces exactly.

Seeds are checked **in parallel** across CPU cores (each seed's Lean
elaboration is independent and is the bottleneck), so a sweep scales with
`--jobs` (default: cores − 1). Because per-seed cost is dominated by Lean's
~1s process startup rather than transpilation, `--batch B` packs `B` seeds'
functions into a single Lean spawn (each seed in its own `#eval` block, so one
ill-typed seed can't abort the others), amortizing that startup across many
functions — ~5x faster in practice. A seed that fails or whose block aborts is
automatically re-run on its own to isolate it (ill-typed seeds are skipped; a
real bug is shrunk as usual), so batching changes throughput, not the verdict.

```bash
python3 fuzz/fuzz.py --seeds 200             # broad sweep (EMI on by default)
python3 fuzz/fuzz.py --seeds 1 --start 18    # reproduce a specific seed
python3 fuzz/fuzz.py --seeds 200 --emi 0     # disable EMI mutation
python3 fuzz/fuzz.py --seeds 2000 --batch 25 --jobs 190  # big batched sweep
```

This layer found **thirteen** bugs the curated corpus missed — including several
*silent wrong-value* bugs (Lean's truncated `Nat` subtraction emitted as Python
`-`; Euclidean `Int` division/modulo emitted as Python's flooring `//`/`%`; an
`OfNat` literal collision) that no crash-based check would catch. The two most
recent (F12 `Nat`/`Int` division/modulo by zero — Lean's division is *total*
(`n/0=0`, `n%0=n`) while Python's `//`/`%` raise; F13 `Array.qsort` argument
mis-indexing) were surfaced by **fragment-reuse fuzzing** over the real corpus
(`--corpus`), which exercises constructs the generative grammar can't invent
(the grammar always guards its divisors and never sorts). All are documented in
[`VERIFICATION.md`](VERIFICATION.md).

Beyond the default generative sweep, three additional modes deepen coverage:

```bash
python3 fuzz/fuzz.py --corpus --seeds 3000    # fragment-reuse: fuzz REAL Corpus/*.lean defs
python3 fuzz/fuzz.py --pycov  --seeds 1000    # input-adequacy: line coverage of transpiled Python
python3 fuzz/fuzz.py --seeds 5000 --batch 25 --jobs 180   # batched sweep, reports k-path coverage
```

The design draws on the grammar-fuzzing literature:

- Generating inputs from a **grammar** to reach deep structural states goes back
  to Purdom's sentence generator for testing parsers [1] and underlies modern
  grammar/whitebox fuzzers such as Godefroid et al. [2].
- Using an **independent oracle for differential testing** — comparing two
  executions that should agree, rather than checking hand-written expected
  values — is the methodology behind Csmith's discovery of C-compiler bugs [3];
  here Lean's `#eval` is the oracle and the transpiled Python the system under
  test.
- **Automatic reduction** of a failing input to a minimal reproducer is delta
  debugging [4]; `fuzz.py` uses a simple size-shrinking form.
- **Grammar production coverage** [5] — every grammatical choice is a labeled
  production, and the generator *prefers not-yet-covered productions* within
  each file rather than sampling uniformly. `fuzz.py` aggregates which
  productions were exercised across the sweep and prints a coverage line (e.g.
  `61/61 (100%)`), so "did we actually exercise construct X?" is a measurement,
  not a matter of chance. Coverage guidance is scoped per file (per seed) so
  generation stays a pure function of the seed — the reproducibility the
  shrinker depends on.
- **Grammar expansion** — the surest way to find *more* bugs is to widen the
  input domain, since bugs hide in constructs the grammar never generates.
  Growing the grammar from `Nat`/`Bool`/`List Nat` to also cover `Int` and
  `Option Nat` immediately surfaced five further bugs (F7–F11 in
  [`VERIFICATION.md`](VERIFICATION.md)), including two silent wrong-value bugs:
  Lean's Euclidean `Int` division/modulo emitted as Python's flooring `//`/`%`,
  and an `Int`-literal `OfNat` collision.
- **Equivalence Modulo Inputs (EMI) [6] + guided stochastic mutation [7]** —
  after generating a subterm, the generator stochastically wraps it in a
  *semantics-preserving identity envelope* (`x` → `(x + 0)`, `b` → `!!b`,
  `xs` → `xs.reverse.reverse`, …). Because the envelope computes the same value,
  the Lean oracle is unchanged, but the transpiler sees a different, deeper term
  — so each seed becomes many differential tests over shapes the base grammar
  wouldn't reach. The *number* of envelopes is stochastic (guided mutation) and
  *which* envelope is chosen is coverage-guided. Controlled by `--emi P`
  (default 0.3; `--emi 0` disables). Envelopes are provably identities, so a
  disagreement is unambiguously a transpiler bug.

- **Fragment-reuse grammars [8]** — `--corpus` harvests every `Corpus/*.lean`
  definition whose signature is in the fuzzer's value universe (78 functions)
  and fuzzes *them* on random inputs (`emitPythonForNames` auto-pulls transitive
  dependencies, so a one-line fragment drags in its `let rec` helpers). Real code
  exercises constructs the generative grammar never invents — this immediately
  found bugs F12/F13.
- **Context-sensitive (k-path) coverage [5]** — beyond single-production
  coverage, the generator records every chain of up to 3 nested productions
  (e.g. `match → map → let`) and reports it. Single-production coverage
  saturates near 100% while k-path coverage sits far lower (~40–50% of offered
  paths), exposing the untested *combinations* flat coverage hides.
- **Structural (HDD/C-Reduce-style) reduction [9,10]** — after the count-based
  minimizer isolates a single failing def, a term-level shrinker replaces
  balanced-paren subterms with type-agnostic leaves, keeping any rewrite that
  still elaborates *and* still reproduces the bug (Lean re-type-checks and the
  oracle recomputes, so kept rewrites are sound). Reduces sprawling generated
  terms to a few characters.
- **Input-adequacy coverage of the transpiled Python** — `--pycov` traces which
  lines of each *transpiled* function the oracle inputs actually execute (via
  `sys.settrace`, portable to 3.11). A branch no input reaches is where a
  transpiler bug hides undiff'd; the mode flags under-exercised functions.

Techniques we considered but have **not** adopted — the
`Float`-vs-exact-`Fraction` question and formal-verification / e-graph
approaches — are written up with citations in
[`RELATED_WORK.md`](RELATED_WORK.md).

## References

1. P. Purdom. *A sentence generator for testing parsers.* BIT Numerical
   Mathematics, 12(3):366–375, 1972. <https://doi.org/10.1007/BF01932308>
2. P. Godefroid, A. Kiezun, M. Y. Levin. *Grammar-based whitebox fuzzing.*
   PLDI 2008. <https://doi.org/10.1145/1375581.1375607>
3. X. Yang, Y. Chen, E. Eide, J. Regehr. *Finding and understanding bugs in C
   compilers.* PLDI 2011. (Csmith) <https://doi.org/10.1145/1993498.1993532>
4. A. Zeller, R. Hildebrandt. *Simplifying and isolating failure-inducing
   input.* IEEE Transactions on Software Engineering, 28(2):183–200, 2002. <https://doi.org/10.1109/32.988498>
5. N. Havrikov, A. Zeller. *Systematically covering input structure.* ASE 2019. <https://doi.org/10.1109/ASE.2019.00027>
6. V. Le, M. Afshari, Z. Su. *Compiler validation via equivalence modulo
   inputs.* PLDI 2014. (EMI) <https://doi.org/10.1145/2594291.2594334>
7. V. Le, C. Sun, Z. Su. *Finding deep compiler bugs via guided stochastic
   program mutation.* OOPSLA 2015. <https://doi.org/10.1145/2814270.2814319>
8. C. Holler, K. Herzig, A. Zeller. *Fuzzing with code fragments.* USENIX
   Security 2012. (LangFuzz) <https://www.usenix.org/conference/usenixsecurity12/technical-sessions/presentation/holler>
9. G. Misherghi, Z. Su. *HDD: Hierarchical delta debugging.* ICSE 2006. <https://doi.org/10.1145/1134285.1134307>
10. J. Regehr, Y. Chen, P. Cuoq, E. Eide, C. Ellison, X. Yang. *Test-case
    reduction for C compiler bugs.* PLDI 2012. (C-Reduce) <https://doi.org/10.1145/2254064.2254104>

## Corpus

The extraction corpus includes **536 functions** (12,400+ lines) covering:

- **Algorithms** - Sorting, searching, numeric algorithms
- **Math** - Arithmetic, number theory, combinatorics
- **Data Structures** - Stack, Queue, BinaryTree, Graph, Trie, Heap, UnionFind
- **Functional** - Higher-order functions, Option/Either combinators
- **Strings** - String manipulation and processing
- **Games** - TicTacToe, Nim, Blackjack, Sudoku validators
- **Number Theory** - GCD, LCM, primality, totient, Collatz
- **Geometry** - 2D/3D points, distances, areas, intersections
- **Combinatorics** - Permutations, combinations, Stirling numbers
- **Sequences** - Fibonacci variants, figurate numbers
- **Production** - Red-Black Trees, Union-Find with path compression, Dynamic Programming (LCS, Edit Distance, Knapsack, Coin Change, Matrix Chain, LIS)

## Usage

### Building

```bash
lake build
```

### Extracting Python

```bash
lake env lean Corpus/CorpusTestCombined.lean > extracted/lcnf_corpus.py
```

### Running Tests

See [Correctness](#correctness) for the full four-layer testing story. The
quickest check:

```bash
python3 evaluate_correctness.py        # unit suite (132 cases)
./roundtrip/run.sh                     # Lean-as-oracle differential
```

## Quick Start

```lean
import LeanToPython

open Lean LeanToPython

def factorial (n : Nat) : Nat :=
  match n with
  | 0 => 1
  | k + 1 => (k + 1) * factorial k

#eval show CoreM Unit from do
  let code ← emitPythonForNames `MyModule [`factorial]
  IO.println code
```

Run with:
```bash
lake env lean MyFile.lean > output.py
python3 output.py
```

## Example Output

**Lean input:**
```lean
def max (x y : Nat) : Nat := if x > y then x else y

def greet (name : String) : String := "Hello, " ++ name ++ "!"

def safeDiv (x y : Nat) : Option Nat :=
  if y == 0 then none else some (x / y)
```

**Python output:**
```python
def max(x: int, y: int) -> int:
    _x = y < x
    if _x:
        return x
    else:
        return y

def greet(name: str) -> str:
    _x = "Hello, " + name
    return _x + "!"

def safe_div(x: int, y: int) -> int | None:
    _x = y == 0
    if _x:
        return None
    else:
        return x // y
```

## Project Structure

```
LeanToPython/
├── LeanToPython.lean      # Main extraction logic
├── Corpus/                # Lean source corpus (14 modules)
│   ├── Algorithms.lean
│   ├── Math.lean
│   ├── DataStructures.lean
│   ├── Functional.lean
│   ├── Strings.lean
│   ├── Games.lean
│   ├── NumberTheory.lean
│   ├── Geometry.lean
│   ├── Combinatorics.lean
│   ├── Sequences.lean
│   ├── Sorting.lean
│   ├── Advanced.lean
│   ├── Parsers.lean
│   ├── Production.lean    # Red-Black Trees, Union-Find, DP
│   └── CorpusTestCombined.lean
├── extracted/             # Generated Python output
│   ├── lcnf_corpus.py     # ~11,900 lines of transpiled Python
│   └── llm_corpus.py
├── evaluate_correctness.py
└── CORRECTNESS_REPORT.md
```

## Type Mappings

| Lean | Python |
|------|--------|
| `Nat`, `Int` | `int` |
| `Float` | `float` |
| `Bool` | `bool` |
| `String` | `str` |
| `List α` | `list[T]` |
| `Array α` | `list[T]` |
| `Option α` | `T \| None` |
| `α × β` | `tuple[A, B]` |
| `α → β` | `Callable[[A], B]` |
| `+`, `-`, `*`, `/`, `%` | `+`, `-`, `*`, `//`, `%` |
| `<`, `<=`, `>`, `>=`, `==` | `<`, `<=`, `>`, `>=`, `==` |
| `&&`, `\|\|`, `!` | `and`, `or`, `not` |
| `match` on `Nat` | `if n == 0: ... else: ...` |
| `match` on `Bool` | `if x: ... else: ...` |
| `match` on `Option` | `if x is None: ... else: ...` |
| `match` on `List` | `if len(xs) == 0: ... else: ...` |
| Custom inductives | `@dataclass` classes |

## How It Works

LeanToPython operates on LCNF (Lean Compiler Normal Form), an intermediate representation used by the Lean compiler. Key transformations:

1. **Type class inlining**: Operations like `x + y` go through `HAdd.hAdd` in LCNF. We recognize these patterns and emit `x + y` directly.

2. **Comparison handling**: Decidable propositions (`Nat.decLt`, etc.) are converted to Python comparison operators.

3. **Pattern matching**: Nat patterns become `if n == 0` checks. Bool/Option/List patterns use appropriate Python idioms.

4. **Custom types**: Inductive types are emitted as Python dataclasses with union type aliases.

## Requirements

- Lean 4.12.0+
- Python 3.10+ (for `match` statements and union types)

## License

MIT
