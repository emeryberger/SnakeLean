/-
  Regression cases for three extraction bugs fixed in LeanToPython.lean:

  1. Bool-typed-parameter branch inversion: `if boolParam then a else b` lowered
     to a Decidable cases whose discriminant the name-heuristic didn't recognize,
     swapping the branches. Fixed by tracking each fvar's LCNF `Bool` type and
     resolving through the alias map.

  2. Binary stdlib operand drop: `Nat.min`/`Nat.max` map to Python `min`/`max`
     but were emitted as unary wrappers (`min(b)`), dropping the first operand.

  Extract this module and run it; `RegressionFixes_test.py` asserts the
  extracted Python computes the right answers.

    lake env lean RegressionFixes.lean > RegressionFixes_out.py
-/
import LeanToPython
open Lean LeanToPython

namespace RegressionFixes

/-- (1) Bool param, with the "interesting" (negating) branch in the `else`.
    Pre-fix this came out as `if flag: -x else: x`. -/
def signedIf (flag : Bool) (x : Int) : Int := if flag then x else -x

/-- (1) Bool param, two distinct value branches. -/
def pickIf (flag : Bool) (a b : Int) : Int := if flag then a else b

/-- (2) Nat.min — must extract to `min(a, b)`, not `min(b)`. -/
def minNat (a b : Nat) : Nat := Nat.min a b

/-- (2) Nat.max — must extract to `max(a, b)`. -/
def maxNat (a b : Nat) : Nat := Nat.max a b

/-- (2) min nested in an expression, to catch arg-order regressions. -/
def clampHigh (v hi : Nat) : Nat := Nat.min v hi

/-- (3) `xs[i]!` panic-indexing (`GetElem?.getElem!`).  Pre-fix this projected
    the elided `GetElem` instance (`_x_N.field_2`) and passed the elided
    `Inhabited` instance as an argument, both referencing unbound names. -/
def indexBang (xs : List Nat) (i : Nat) : Nat := xs[i]!

/-- (4) Tail-recursive helper whose match-arm continuation both carries the
    recursion AND is deferred-lambda-eligible.  Pre-fix, the continuation
    rendered as a call to an unemitted `_uniq_NNN` helper (undefined name); the
    fix that materialized it then exposed a `continue` inside a nested `def`.
    This mirrors `Corpus.Strings.splitOn`'s `go`. -/
def dropUntilZero (xs : List Nat) : List Nat :=
  let rec go (ys : List Nat) : List Nat :=
    match ys with
    | [] => []
    | y :: rest => if y == 0 then rest else go rest
  go xs

-- (5) Name-collision (F18): two functions in different namespaces both map to
-- the Python name `tally`.  Pre-fix, the later `def` shadowed the earlier, so a
-- call to one ran the other's body.  `useTally` calls `A.tally`; if collision
-- de-dup fails it would run `B.tally` (a different function) and give a wrong
-- answer.  Mirrors `Corpus.Sorting.mode.count` vs `Corpus.Strings.count`.
namespace ModA
def tally (xs : List Nat) : Nat := xs.foldl (· + ·) 0   -- sum
end ModA
namespace ModB
def tally (xs : List Nat) : Nat := xs.length            -- count (different!)
end ModB
def useTally (xs : List Nat) : Nat := ModA.tally xs      -- must be the SUM

end RegressionFixes

#eval show CoreM Unit from do
  let code ← emitPythonForNames `RegressionFixes
    [ ``RegressionFixes.signedIf,
      ``RegressionFixes.pickIf,
      ``RegressionFixes.minNat,
      ``RegressionFixes.maxNat,
      ``RegressionFixes.clampHigh,
      ``RegressionFixes.indexBang,
      ``RegressionFixes.dropUntilZero,
      ``RegressionFixes.ModA.tally,
      ``RegressionFixes.ModB.tally,
      ``RegressionFixes.useTally ]
  IO.println code
