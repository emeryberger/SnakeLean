/-
Combinatorics and number-theory definitions adapted from **Mathlib**
(`leanprover-community/mathlib4`), the Lean 4 mathematical library.

Source: https://github.com/leanprover-community/mathlib4
Original files:
  * Mathlib/Data/Nat/Factorial/Basic.lean  (factorial, ascFactorial, descFactorial)
  * Mathlib/Data/Nat/Choose/Basic.lean     (choose, multichoose, centralBinom)
  * Mathlib/Data/Nat/Fib/Basic.lean        (fib)

Licensed under the Apache License, Version 2.0 (SPDX-License-Identifier:
Apache-2.0), matching the upstream project.  See Corpus/Mathlib_NOTICE.md for
attribution.

Only the computable, value-level `def`s are ported (all theorems, lemmas,
`Prop`-valued specifications, `@[simp]`/instance machinery dropped), each
re-stated monomorphically over `Nat` in plain Lean 4.31 so the SnakeLean fuzzer's
value universe can drive them.  Mathlib does NOT ship as a dependency here (its
import graph and build cost are prohibitive, and the harvester only sees
`Corpus.*` defs anyway) — following the same hand-port pattern as
`Corpus/RustModels.lean` and `Corpus/Cedar.lean`.  Every def is `#eval`-verified
against its known values below.

Value: Mathlib's definitional *style* — two-argument structural recursion
(`choose`, `multichoose`), accumulation (`ascFactorial`/`descFactorial`), and
truncated-subtraction guards — exercises transpiler `match`/recursion paths the
existing corpus doesn't reach in the same combination.
-/

namespace Corpus.Mathlib

/-! ## Factorials (Mathlib/Data/Nat/Factorial/Basic.lean) -/

/-- `n !` — the factorial `n * (n-1) * … * 1`, with `0! = 1`. -/
def factorial : Nat → Nat
  | 0 => 1
  | n + 1 => (n + 1) * factorial n

/-- `n.ascFactorial k` — the ascending factorial `n * (n+1) * … * (n+k-1)`
    (`k` rising factors starting at `n`), with the empty product `= 1`. -/
def ascFactorial (n : Nat) : Nat → Nat
  | 0 => 1
  | k + 1 => (n + k) * ascFactorial n k

/-- `n.descFactorial k` — the descending factorial `n * (n-1) * … * (n-k+1)`
    (`k` falling factors starting at `n`); `0` once a factor underflows. -/
def descFactorial (n : Nat) : Nat → Nat
  | 0 => 1
  | k + 1 => (n - k) * descFactorial n k

/-! ## Binomial coefficients (Mathlib/Data/Nat/Choose/Basic.lean) -/

/-- `choose n k` — the binomial coefficient "`n` choose `k`", by Pascal's rule. -/
def choose : Nat → Nat → Nat
  | _,     0     => 1
  | 0,     _ + 1 => 0
  | n + 1, k + 1 => choose n k + choose n (k + 1)

/-- `multichoose n k` — the number of multisets of size `k` from `n` elements
    (`= choose (n + k - 1) k`), by its own Pascal-style recursion. -/
def multichoose : Nat → Nat → Nat
  | _,     0     => 1
  | 0,     _ + 1 => 0
  | n + 1, k + 1 => multichoose n (k + 1) + multichoose (n + 1) k

/-- `centralBinom n` — the central binomial coefficient `choose (2n) n`. -/
def centralBinom (n : Nat) : Nat := choose (2 * n) n

/-! ## Fibonacci (Mathlib/Data/Nat/Fib/Basic.lean) -/

/-- `fib n` — the `n`-th Fibonacci number (`fib 0 = 0`, `fib 1 = 1`). -/
def fib : Nat → Nat
  | 0 => 0
  | 1 => 1
  | n + 2 => fib n + fib (n + 1)

-- Known values (verified by `#eval` during development):
--   factorial 5 = 120   ascFactorial 2 3 = 24   descFactorial 5 3 = 60
--   choose 5 2 = 10      multichoose 3 2 = 6     centralBinom 3 = 20
--   fib 10 = 55

end Corpus.Mathlib
