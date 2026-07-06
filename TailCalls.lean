/-
  Regression cases for tail-call elimination in SnakeLean.lean.

  Lean performs TCO; Python does not. A Lean function whose self-recursive
  calls are all in tail position runs in constant stack, but a naive Python
  translation recurses and overflows the stack (`RecursionError`) on deep
  inputs. SnakeLean detects such functions and rewrites the body into a
  `while True:` loop (parallel parameter rebind + `continue`).

  These cover the structural shapes the rewrite must handle:

  1. Nat match with accumulator (`| 0 => acc | k+1 => f k (g acc)`).
  2. `if`/`Decidable` condition with a direct tail self-call.
  3. List match `.go` loop helper (tail call inside a cons arm).
  4. Multiple tail-call sites (both branches recurse).
  5. Non-tail recursion (factorial) must be LEFT recursive — Lean overflows it
     too, so matching Lean means not pretending to optimize it.

  `TailCalls_test.py` executes the extracted Python at depths far beyond
  Python's default recursion limit (1000) and asserts no RecursionError plus
  correct results, and checks the loop structure was emitted.

    lake env lean TailCalls.lean > TailCalls_out.py
-/
import SnakeLean
open Lean SnakeLean

namespace TailCalls

/-- (1) Nat match with accumulator — classic tail recursion. -/
def sumTo : Nat → Nat → Nat
  | 0, acc => acc
  | n+1, acc => sumTo n (acc + (n+1))

/-- (2) `if` condition, direct tail self-call (Euclid's gcd). -/
partial def gcd (a b : Nat) : Nat :=
  if b == 0 then a else gcd b (a % b)

/-- (2) countdown — single tail call, trivial base case. -/
partial def countdown (n : Nat) : Nat :=
  if n == 0 then 0 else countdown (n - 1)

/-- (3) List `.go` loop helper: sum a list with an accumulator. -/
def sumList (xs : List Nat) : Nat :=
  let rec go (acc : Nat) : List Nat → Nat
    | [] => acc
    | x :: rest => go (acc + x) rest
  go 0 xs

/-- (4) Two tail-call sites: both branches recurse (parity via countdown). -/
partial def evenIsh (n : Nat) (flag : Bool) : Bool :=
  if n == 0 then flag else evenIsh (n - 1) (!flag)

/-- (5) NON-tail recursion — must stay recursive (Lean overflows this too). -/
def fact : Nat → Nat
  | 0 => 1
  | n+1 => (n+1) * fact n

end TailCalls

#eval show CoreM Unit from do
  let code ← emitPythonForNames `TailCalls
    [ ``TailCalls.sumTo,
      ``TailCalls.gcd,
      ``TailCalls.countdown,
      ``TailCalls.sumList,
      ``TailCalls.evenIsh,
      ``TailCalls.fact ]
  IO.println code
