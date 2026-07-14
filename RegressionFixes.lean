/-
  Regression cases for three extraction bugs fixed in SnakeLean.lean:

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
import SnakeLean
open Lean SnakeLean

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

-- (6) Loop-mode `find?` with a tuple-destructuring predicate lambda.  Pre-fix,
-- the tail-loop transform diverted the (non-recursive) predicate lambda to the
-- inline-thunk set, so the comprehension referenced an unemitted `_uniq_NNN`.
-- Mirrors `Corpus.DataStructures.Trie.contains`.
def lookLoop (xs : List (Nat × Nat)) (k : Nat) : Bool :=
  match xs with
  | [] => false
  | _ :: rest =>
    match xs.find? (fun (p, _) => p == k) with
    | some _ => true
    | none => lookLoop rest k

-- (7) Option predicate / user function passed POINT-FREE to a combinator.  Both
-- must become a function *reference*, not `is_some(...)` / `is_ace(...)` calls
-- with a spurious arg.  Mirrors `ConnectFour.columnHeight` / `BlackjackHand.numAces`.
def isBig (n : Nat) : Bool := n > 3
def countSome (xs : List (Option Nat)) : Nat := (xs.filter Option.isSome).length
def countBig (xs : List Nat) : Nat := (xs.filter isBig).length

-- (8) Option.map, List.zip, List.set (setTR) — previously undefined names.
def bump (o : Option Nat) : Option Nat := o.map (· + 1)
def pairUp (xs ys : List Nat) : List (Nat × Nat) := xs.zip ys
def setAt (xs : List Nat) (i v : Nat) : List Nat := xs.set i v

-- (9) List.head?/getLast? applied (must apply over the value arg only, not the
-- erased type arg).  Mirrors `Corpus.Strings.head`/`last`.
def firstOf (xs : List Nat) : Option Nat := xs.head?
def lastOf (xs : List Nat) : Option Nat := xs.getLast?

-- (10) Nullary user value referenced point-free must be CALLED, not bound as the
-- function object.  Here `base` (a nullary def) is used inside a recursive call;
-- pre-fix `base` bound the function, corrupting the result.  Mirrors
-- `Corpus.DataStructures.Trie.insert`'s use of `Trie.empty`.
def base : List Nat := [0]
def prependBase (n : Nat) : List Nat := n :: base

-- (11) Float support: literal (`OfScientific`), real division `/` (NOT integer
-- `//`), `Float.sqrt` → `math.sqrt`, and Float comparison (`Float.decLt`).
-- Pre-fix: the literal became a call to an undefined var, `/` emitted `//`,
-- sqrt emitted an undefined `sqrt`, and `<` emitted an undefined `dec_lt`.
-- Mirrors `Corpus.Geometry.circleArea`/`midpoint2D`/`dist2D`/`orientation`.
def circAreaF (r : Float) : Float := 3.14159265358979 * r * r
def halfF (x : Float) : Float := x / 2.0
def hypotF (a b : Float) : Float := Float.sqrt (a * a + b * b)
def signF (x : Float) : Nat := if x < 0.0 then 2 else if x == 0.0 then 0 else 1

-- (12) rust-lean-models corpus bugs.
--   (a) A Nat/Int binary op passed POINT-FREE to a combinator (`List.foldl
--       Nat.add …`) emitted a bare snake name (`add`) — an undefined name.
--       Now a 2-arg lambda.  Mirrors `RustModels.sum_list_Nat`.
--   (b) `Char.utf8Size c` had no handler and emitted `utf8size(c)` — undefined.
--       Now `len(c.encode('utf-8'))`.  Mirrors `RustModels.byteSize`.
def sumFold (l : List Nat) : Nat := List.foldl Nat.add 0 l
def utf8Len (c : Char) : Nat := c.utf8Size
def byteSizeR (s : List Char) : Nat := s.foldl (fun acc c => acc + c.utf8Size) 0

-- (13) rust-lean-models corpus bugs, part 2.
--   (a) F21: `Char.val` (projection 0 of the `Char` struct) emitted `c.field_0`
--       (AttributeError — a Char is a Python `str`).  Now `ord(c)`.  Mirrors
--       `RustModels.is_whitespace` (`c.val ≤ 127`).
--   (b) F22: `UInt32.decLe` (from a `Char.val ≤ 127` comparison) fell through to
--       an undefined `dec_le`.  Now `<=`.  Mirrors `RustModels.Char_is_ascii`.
def charCode (c : Char) : Nat := c.val.toNat
def isAsciiC (c : Char) : Bool := c.val ≤ 127
def isDigitC (c : Char) : Bool := c.val ≥ 48 && c.val ≤ 57

-- (14) rust-lean-models corpus bugs, part 3 (found via elaborated-signature
-- harvest + Char→Bool/Pattern value generation).
--   (a) F23b: a USER function PARTIALLY applied and passed to a combinator
--       (`List.map (addTo n) xs`) emitted `add_to(n)` — a call missing the last
--       arg.  Now `(lambda _p0: add_to(n, _p0))`.  Mirrors
--       `RustModels.list_substring_pos_def`'s `List.map (charIndex_to_pos s)`.
--   (b) F24: a dependent `match _h : e with` / `if _h : c` introduces an
--       LCNF-erased proof param.  It was emitted as a spurious `def` param and
--       an extra `None` call arg (arity mismatch), and a nullary `none`-arm thunk
--       was returned uncalled.  Mirrors `RustModels`' Option-returning matchers.
--   (c) missing builtins: `List.isSuffixOf`, `List.getD`, point-free
--       `List.append` in a fold (`flatten`).
def addTo (n x : Nat) : Nat := n + x
def mapAddTo (n : Nat) (xs : List Nat) : List Nat := xs.map (addTo n)
def depOptMatch (o : Option Nat) : Nat :=
  match _h : o with
  | none => 7
  | some x => x * 2
def suffixCheck (p xs : List Nat) : Bool := p.isSuffixOf xs
def getDefault (xs : List Nat) (i : Nat) : Nat := xs.getD i 99
def flattenLists (xss : List (List Nat)) : List Nat := List.foldl List.append [] xss

-- (15) cedar-lean corpus bugs.
--   (a) F25: `Int.emod`/`Int.ediv` (Euclidean) and `Int.tmod`/`Int.tdiv`
--       (truncated) called BY NAME emitted Python's `%`/`//`, which disagree
--       with Lean for negative operands (a SILENT wrong-value bug).  Now the
--       correct total formula each.  Mirrors `Cedar.smod` (`Int.emod`).
--   (b) F26: `List.mergeSort le` (lowered to `mergeSortTR₂`) referenced an
--       undefined name and mis-converted the `≤` comparator.  Now
--       `sorted(xs, key=cmp_to_key(lambda a,b: -1 if le(a,b) else 1))`.
--       Mirrors `Cedar.setMake`.
--   (c) F27: `List.contains` passed POINT-FREE (`s₁.all s₂.contains`) emitted
--       garbage (`elt in None`).  Now a membership lambda.  Mirrors
--       `Cedar.setSubset`/`setIntersects`.
def emodByName (a b : Int) : Int := a.emod b
def tmodByName (a b : Int) : Int := a.tmod b
def ediseByName (a b : Int) : Int := a.ediv b
def tdivByName (a b : Int) : Int := a.tdiv b
def sortLe (xs : List Int) : List Int := xs.mergeSort (· ≤ ·)
def allContains (xs ys : List Int) : Bool := xs.all ys.contains

-- (16) rust-lean-models corpus bugs, part 4 (dependent-if / do-block).
--   (a) F28: a `do`-block over the `Option` monad desugars to `Bind.bind` via
--       `instMonadOption` → `proj Monad.toBind` → `proj Bind.bind`.  The
--       elided-instance projections emitted `_inst.field_1.field_0(opt, f)`
--       (undefined names); now the `Option.bind` None-guard.  Mirrors
--       `RustModels.string_slice`.
--   (b) F29: `if _h : xs = [] then …` (a dependent `if` on `DecidableEq`'s
--       `List.instDecidableEqNil xs`, ONE value operand) dropped the
--       discriminant → `if <undefined>:`.  Now `len(xs) == 0`.  Mirrors
--       `RustModels.matches_substring`.
def optDo (o1 o2 : Option Nat) : Option Nat := do
  let a ← o1
  let b ← o2
  some (a + b)
def isNilDep (xs : List Nat) : Nat := if _h : xs = [] then 0 else xs.length

-- (17) Array-mutation + combinator arg-order + builtin-shadow bugs (found via a
-- corpus sweep over the Production DP algorithms).
--   (a) F30: `Array.set!`/`getD`/`modify`/`foldl` emitted undefined snake names
--       (`set_`/`get_d`/`modify`/`array_foldl`).  Now list slice-update / bounds
--       default / modify comprehension / `functools.reduce`.
--   (b) F31: `List.zipIdx` has a trailing `start := 0` optParam that recent Lean
--       materializes; the handler grabbed the last arg (`0`) as the list →
--       `enumerate(0)`.  Now uses the first value arg.  Mirrors `Matrix.set`.
--   (c) F32: `List.flatMap f xs` — Lean's arg order is `(f) (xs)`, but the
--       handler read them swapped and iterated the function (`for x in f`).
--       Mirrors `Games.isValidSudokuGrid`.
--   (d) F33: a binder named after a Python builtin the transpiler emits calls to
--       (`max`, as in `integerPartitions.go`) shadowed it, so an emitted
--       `max(0, …)` (from `Nat.sub`) called the int variable.  Now renamed
--       (`max_`).
def arrSet (xs : Array Nat) (i v : Nat) : Array Nat := xs.set! i v
def arrGetD (xs : Array Nat) (i d : Nat) : Nat := xs.getD i d
-- (23) F37/F38: the three index-update forms differ OUT OF RANGE, and the emitted
-- slice `xs[:i] + [v] + xs[i+1:]` matched none of them — it silently APPENDED.
--   List.set / setIfInBounds : out of range ⇒ unchanged;  Array.set! : ⇒ panics.
def arrSetIf (xs : Array Nat) (i v : Nat) : Array Nat := xs.setIfInBounds i v
-- (24) F39: `Char.ofNat` is TOTAL in Lean (invalid ⇒ '\0').  Python's `chr` raises
-- above 0x10FFFF, and — worse — silently returns a SURROGATE for D800–DFFF, which
-- Lean does not consider a valid Char.
def charOf (n : Nat) : Nat := (Char.ofNat n).toNat
def arrModify (xs : Array Nat) (i : Nat) : Array Nat := xs.modify i (· + 10)
def arrFold (xs : Array Nat) : Nat := xs.foldl (· + ·) 0
def zipIdxList (xs : List Nat) : List (Nat × Nat) := xs.zipIdx
def flatMapRange (n : Nat) : List Nat := (List.range n).flatMap (fun i => [i, i])
def usesMaxParam (max : Nat) : Nat := max - 1     -- binder named `max` shadows builtin

-- (18) `Int → Bool` predicate parameter (mirrors Cedar's `setFilter`/`setAll`).
-- The fuzzer now generates predicate values for `Int → Bool` too (not just
-- `Char → Bool`); this checks the transpiler emits a callable the combinator can
-- apply.  `countMatching p xs` filters `xs` by predicate `p`.
def countMatching (p : Int → Bool) (xs : List Int) : Nat := (xs.filter p).length

-- (19) F34: a whole-number Float LITERAL (`(0 : Float)`, via `instOfNatFloat` →
-- `proj OfNat.0`) emitted the Python int `0`, so a Float-returning `if … then 0
-- else …` yielded an `int` where Lean has `0.0` — failing the exact-bits Float
-- oracle.  Now emitted as `0.0`.  Mirrors `Geometry.angleBetween` (returns `0`
-- for a zero-magnitude vector).
def floatZeroBranch (x : Float) : Float := if x == 0.0 then 0 else x
def floatLitConst : Float := 5

-- (20) Nested Option (`Option (Option α)`) faithfulness.  Python models a flat
-- `Option α` as `α | None`, which collapses `some none` and `none` to a shared
-- `None`.  With type-directed boxing, a NESTED option's `some` becomes
-- `_Some(...)`, so `some none` (→ `_Some(None)`) stays distinct from `none`
-- (→ `None`).  `classifyNested` returns a different Nat for each of the three
-- shapes `none` / `some none` / `some (some n)` — pre-fix `some none` and `none`
-- were indistinguishable and it returned the wrong tag.
def classifyNested (o : Option (Option Nat)) : Nat :=
  match o with
  | none => 0
  | some none => 1
  | some (some n) => n + 100
-- `nestedIndex xs i` reproduces the TicTacToe.validMoves pattern: indexing a
-- `List (Option α)` with `xs[i]?` yields `Option (Option α)`; a found `none`
-- element (`some none`) must differ from an out-of-bounds miss (`none`).
def nestedIndex (xs : List (Option Nat)) (i : Nat) : Nat :=
  match xs[i]? with
  | none => 0            -- out of bounds
  | some none => 1       -- in bounds, element is `none`
  | some (some n) => n + 100
-- (21) Polymorphic tail-recursive helper: a leading TYPE parameter (`{α}`) must
-- be dropped from the emitted Python signature — the LCNF call arg is a `.type`
-- node the emitter drops, so an emitted `_: Any` param leaves both the wrapper's
-- call AND the tail self-call one argument short (`… missing 1 required
-- positional argument`).  `revAcc` reverses via an accumulator (self-tail-
-- recursive → loop); pre-fix `rev_acc_go(xs_, acc_)` passed 2 args to a 3-param
-- `def rev_acc_go(_, xs, acc)`.
def revAcc.go {α : Type} : List α → List α → List α
  | [], acc => acc
  | x :: xs, acc => revAcc.go xs (x :: acc)
def revAcc {α : Type} (xs : List α) : List α := revAcc.go xs []

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
      ``RegressionFixes.useTally,
      ``RegressionFixes.lookLoop,
      ``RegressionFixes.isBig,
      ``RegressionFixes.countSome,
      ``RegressionFixes.countBig,
      ``RegressionFixes.bump,
      ``RegressionFixes.pairUp,
      ``RegressionFixes.setAt,
      ``RegressionFixes.firstOf,
      ``RegressionFixes.lastOf,
      ``RegressionFixes.base,
      ``RegressionFixes.prependBase,
      ``RegressionFixes.circAreaF,
      ``RegressionFixes.halfF,
      ``RegressionFixes.hypotF,
      ``RegressionFixes.signF,
      ``RegressionFixes.sumFold,
      ``RegressionFixes.utf8Len,
      ``RegressionFixes.byteSizeR,
      ``RegressionFixes.charCode,
      ``RegressionFixes.isAsciiC,
      ``RegressionFixes.isDigitC,
      ``RegressionFixes.addTo,
      ``RegressionFixes.mapAddTo,
      ``RegressionFixes.depOptMatch,
      ``RegressionFixes.suffixCheck,
      ``RegressionFixes.getDefault,
      ``RegressionFixes.flattenLists,
      ``RegressionFixes.emodByName,
      ``RegressionFixes.tmodByName,
      ``RegressionFixes.ediseByName,
      ``RegressionFixes.tdivByName,
      ``RegressionFixes.sortLe,
      ``RegressionFixes.allContains,
      ``RegressionFixes.optDo,
      ``RegressionFixes.isNilDep,
      ``RegressionFixes.arrSet,
      ``RegressionFixes.arrSetIf,
      ``RegressionFixes.charOf,
      ``RegressionFixes.arrGetD,
      ``RegressionFixes.arrModify,
      ``RegressionFixes.arrFold,
      ``RegressionFixes.zipIdxList,
      ``RegressionFixes.flatMapRange,
      ``RegressionFixes.usesMaxParam,
      ``RegressionFixes.countMatching,
      ``RegressionFixes.floatZeroBranch,
      ``RegressionFixes.floatLitConst,
      ``RegressionFixes.classifyNested,
      ``RegressionFixes.nestedIndex,
      ``RegressionFixes.revAcc ]
  IO.println code
