# LeanToPython

A Lean 4 to Python transpiler that extracts idiomatic Python code from Lean's LCNF (Lean Compiler Normal Form).

## Overview

LeanToPython converts Lean 4 functions into readable Python code by working directly from the compiler's intermediate representation. Unlike runtime-based approaches, this produces standalone Python that:

- Reads like hand-written Python
- Uses native Python data structures (lists, dicts, tuples, dataclasses)
- Requires no special runtime library
- Can be understood and modified by Python developers

## Correctness

The transpiler achieves **100% accuracy** on a test suite of 27 functions (132 test cases) covering:

| Category | Functions |
|----------|-----------|
| Numeric algorithms | gcd, factorial, fibonacci, is_prime, prime_factors, lcm, coprime |
| Sorting | insertion_sort, merge_sort |
| Searching | binary_search, linear_search |
| Math | pow, abs, binomial, fast_pow, mod_pow, digit_sum, num_digits, is_palindrome_num |
| Strings | reverse_str, to_upper, to_lower |
| Heap operations | left_child, right_child, parent |
| Predicates | is_even, is_odd |

## Corpus

The extraction corpus includes 472 functions (9,400+ lines) covering:

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

```bash
python evaluate_correctness.py
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
├── Corpus/                # Lean source corpus
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
│   └── CorpusTestCombined.lean
├── extracted/             # Generated Python output
│   ├── lcnf_corpus.py
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
