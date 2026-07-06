/-
  Regression cases for list/set comprehension emission in SnakeLean.lean.

  These pin down the lambda-inlining + set-comprehension behavior:

  1. `List.map`/`filter`/… inline a simple lambda body directly into the
     comprehension (`[x + 1 for x in xs]`) rather than emitting a helper `def`
     and calling it (`[_f(x) for x in xs]`).
  2. A named-function argument (not a lambda) still falls back to `f(x)`.
  3. A lambda whose body is NOT a simple expression (e.g. has if/else) falls
     back to a real `def` — it must never inline into a call to an undefined
     name.
  4. A deferred lambda used as a plain value is materialized as `(lambda p: e)`.
  5. `List.eraseDups` / `.toSet` / `.toFinset` emit a Python set comprehension,
     fusing an upstream `map`/`filter` comprehension when present.

  Extract this module and run it; `Comprehensions_test.py` asserts the extracted
  Python computes the right answers.

    lake env lean Comprehensions.lean > Comprehensions_out.py
-/
import SnakeLean
open Lean SnakeLean

namespace Comprehensions

/-- (1) map with an inlined arithmetic lambda body. -/
def addOne (xs : List Nat) : List Nat := xs.map (fun x => x + 1)

/-- (1) map with a multiply. -/
def squares (xs : List Nat) : List Nat := xs.map (fun x => x * x)

/-- (1) filter with an inlined comparison body. -/
def evens (xs : List Nat) : List Nat := xs.filter (fun x => x % 2 == 0)

/-- (1) any / all inline their predicate. -/
def anyBig (xs : List Nat) : Bool := xs.any (fun x => 100 < x)
def allPos (xs : List Nat) : Bool := xs.all (fun x => 0 < x)

/-- (1) find? inlines its predicate. -/
def firstEven (xs : List Nat) : Option Nat := xs.find? (fun x => x % 2 == 0)

/-- (1) chained filter-then-map: two fused comprehensions. -/
def posDoubled (xs : List Nat) : List Nat :=
  (xs.filter (fun x => 0 < x)).map (fun x => x * 2)

/-- (2) named function argument (eta-expanded), still correct. -/
def succAll (xs : List Nat) : List Nat := xs.map Nat.succ

/-- (2) a caller-supplied function argument must stay `f(x)`. -/
def mapWith (xs : List Nat) (f : Nat → Nat) : List Nat := xs.map f

/-- (3) lambda body with if/else must fall back to a `def`, not inline. -/
def keepDoublePos (xs : List Nat) : List Nat :=
  xs.filterMap (fun x => if 0 < x then some (x * 2) else none)

/-- (4) a lambda bound to a name then used — materialized as a Python lambda. -/
def viaLet (xs : List Nat) : List Nat :=
  let f := fun x => x + 10
  xs.map f

/-- (5) eraseDups → set comprehension. -/
def dedup (xs : List Nat) : List Nat := xs.eraseDups

/-- (5) map then eraseDups → fused set comprehension. -/
def uniqSquares (xs : List Nat) : List Nat := (xs.map (fun x => x * x)).eraseDups

/-- (5) filter then eraseDups → fused set comprehension. -/
def uniqBig (xs : List Nat) : List Nat := (xs.filter (fun x => 5 < x)).eraseDups

end Comprehensions

#eval show CoreM Unit from do
  let code ← emitPythonForNames `Comprehensions
    [ ``Comprehensions.addOne,
      ``Comprehensions.squares,
      ``Comprehensions.evens,
      ``Comprehensions.anyBig,
      ``Comprehensions.allPos,
      ``Comprehensions.firstEven,
      ``Comprehensions.posDoubled,
      ``Comprehensions.succAll,
      ``Comprehensions.mapWith,
      ``Comprehensions.keepDoublePos,
      ``Comprehensions.viaLet,
      ``Comprehensions.dedup,
      ``Comprehensions.uniqSquares,
      ``Comprehensions.uniqBig ]
  IO.println code
