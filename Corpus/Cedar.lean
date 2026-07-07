/-
Cedar authorization-engine data operations, ported from the
`cedar-policy/cedar-spec` project (Copyright Cedar Contributors), which is the
Lean formalization of the Cedar policy language (`cedar-lean/`).

Source: https://github.com/cedar-policy/cedar-spec/tree/main/cedar-lean
Original files: cedar-lean/Cedar/Data/Int64.lean, cedar-lean/Cedar/Data/Set.lean

Licensed under the Apache License, Version 2.0 (SPDX-License-Identifier:
Apache-2.0), matching the upstream project.  See Corpus/Cedar_NOTICE.md for
attribution.

Only the computable value-level `def`s are ported (proofs/lemmas/typeclass
instances dropped), adapted to plain monomorphic Lean 4.31 for use as a SnakeLean
transpiler-fuzzing corpus:
  * Cedar's `Int64` (Rust-`i64`-style checked arithmetic) is modelled here as a
    range-checked `Int` — `MIN`/`MAX` are the real i64 bounds and the checked
    ops return `none` on overflow, exactly as upstream.  (Upstream wraps Lean's
    machine `Int64`; the observable checked-arithmetic behavior is identical.)
  * Cedar's `Set α` (a canonical sorted, duplicate-free list) is modelled over
    `Int` (`List Int`) so the fuzzer's monomorphic value universe can drive it;
    membership/subset/intersection semantics match upstream.
-/

namespace Corpus.Cedar

/-! ## Int64 — checked 64-bit signed integer arithmetic (Cedar.Data.Int64) -/

/-- Signed 64-bit lower bound (`i64::MIN`). -/
def i64Min : Int := -9223372036854775808
/-- Signed 64-bit upper bound (`i64::MAX`). -/
def i64Max : Int :=  9223372036854775807

/-- Is `i` representable as a signed 64-bit integer? -/
def inRange (i : Int) : Bool := i64Min ≤ i && i ≤ i64Max

/-- `Int64.ofInt?`: `some i` if `i` fits in an `i64`, else `none`. -/
def ofInt? (i : Int) : Option Int := if inRange i then some i else none

/-- `Int64.add?`: checked addition (overflow → `none`). -/
def add? (a b : Int) : Option Int := ofInt? (a + b)

/-- `Int64.sub?`: checked subtraction. -/
def sub? (a b : Int) : Option Int := ofInt? (a - b)

/-- `Int64.mul?`: checked multiplication. -/
def mul? (a b : Int) : Option Int := ofInt? (a * b)

/-- `Int64.neg?`: checked negation (`neg? i64Min = none`). -/
def neg? (a : Int) : Option Int := ofInt? (-a)

/-- `Int64.natAbs`. -/
def natAbs (a : Int) : Nat := a.natAbs

/-- `Int64.smod`: a modulo whose result is always in `[0, b)` for `b > 0`
    (Cedar uses BitVec.smod; over `Int` this is the Euclidean/floor mod). -/
def smod (a b : Int) : Int := a.emod b

/-! ## Set over Int — canonical sorted, duplicate-free list (Cedar.Data.Set) -/

/-- `Set.make`: canonicalize a list into a sorted, duplicate-free representation
    (Cedar's canonical `Set` form). -/
def setMake (elts : List Int) : List Int := (elts.eraseDups).mergeSort (· ≤ ·)

/-- `Set.contains`. -/
def setContains (s : List Int) (elt : Int) : Bool := s.contains elt

/-- `Set.isEmpty`. -/
def setIsEmpty (s : List Int) : Bool := s.isEmpty

/-- `Set.size`. -/
def setSize (s : List Int) : Nat := s.length

/-- `Set.subset`: is every element of `s₁` in `s₂`? -/
def setSubset (s₁ s₂ : List Int) : Bool := s₁.all s₂.contains

/-- `Set.intersects`: do the two sets share any element? -/
def setIntersects (s₁ s₂ : List Int) : Bool := s₁.any s₂.contains

/-- `Set.intersect`: elements present in both. -/
def setIntersect (s₁ s₂ : List Int) : List Int := s₁.filter s₂.contains

/-- `Set.difference`: elements of `s₁` not in `s₂`. -/
def setDifference (s₁ s₂ : List Int) : List Int := s₁.filter (fun x => !s₂.contains x)

/-- `Set.all`. -/
def setAll (f : Int → Bool) (s : List Int) : Bool := s.all f

/-- `Set.any`. -/
def setAny (f : Int → Bool) (s : List Int) : Bool := s.any f

/-- `Set.filter`. -/
def setFilter (f : Int → Bool) (s : List Int) : List Int := s.filter f

/-- `Set.singleton`. -/
def setSingleton (a : Int) : List Int := [a]

/-- `Set.wellFormed`: does the set equal its own canonical form? -/
def setWellFormed (s : List Int) : Bool := s == setMake s

end Corpus.Cedar
