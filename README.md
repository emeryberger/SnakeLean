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
