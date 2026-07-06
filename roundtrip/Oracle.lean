/-
  Round-trip / faithfulness oracle driver (Option A: Lean-as-oracle differential).

  For a curated set of monomorphic corpus functions this file:
    1. Emits the transpiled Python (via `emitPythonForNames`) to stdout under a
       `### PYTHON` banner, so the Python runner can `exec` it.
    2. Emits an ORACLE table: for each (function, input) it prints the *Lean*
       `#eval` result, serialized as JSON.  Lean is the ground truth.

  The companion `run_oracle.py` runs the generated Python on the SAME inputs and
  asserts equality against the Lean oracle.  Agreement across the battery is the
  evidence that the Lean->Python transpilation is faithful (it computes what the
  original Lean definition computes).
-/
import SnakeLean
import Corpus.Algorithms
import Corpus.Math
import Corpus.NumberTheory
import Corpus.Sequences

open Lean SnakeLean

namespace Roundtrip

-- ── JSON serializers for the result types in the battery ─────────────────────
def jNat (n : Nat) : String := toString n
def jBool (b : Bool) : String := if b then "true" else "false"
def jListNat (xs : List Nat) : String :=
  "[" ++ String.intercalate "," (xs.map toString) ++ "]"
def jOptNat : Option Nat → String
  | none => "null"
  | some n => toString n
def jProdNat : Nat × Nat → String
  | (a, b) => "[" ++ toString a ++ "," ++ toString b ++ "]"

-- An oracle row keyed on the fully-qualified LEAN name (the Python runner maps
-- it to the emitted Python name via the `# Lean:` comments, so the oracle does
-- not depend on the transpiler's snake_case/prefix heuristics).
def row (leanName : String) (argsJson : String) (resJson : String) : String :=
  "ORACLE\t" ++ leanName ++ "\t" ++ argsJson ++ "\t" ++ resJson

def a1 (x : Nat) : String := "[" ++ toString x ++ "]"
def a2 (x y : Nat) : String := "[" ++ toString x ++ "," ++ toString y ++ "]"
def aL (xs : List Nat) : String := "[" ++ jListNat xs ++ "]"

open Corpus.Algorithms in open Corpus.Math in open Corpus.NumberTheory in
open Corpus.Sequences in
def oracleLines : List String := Id.run do
  let mut out : List String := []
  -- gcd (Algorithms) : Nat -> Nat -> Nat
  for (x, y) in [(48,18),(100,25),(17,5),(0,5),(12,0),(36,24),(1,1),(1071,462)] do
    out := out ++ [row "Corpus.Algorithms.gcd" (a2 x y) (jNat (Corpus.Algorithms.gcd x y))]
  -- lcm (Algorithms)
  for (x, y) in [(4,6),(3,5),(12,8),(7,7),(1,9)] do
    out := out ++ [row "Corpus.Algorithms.lcm" (a2 x y) (jNat (Corpus.Algorithms.lcm x y))]
  -- fibonacci (Algorithms) : Nat -> Nat
  for n in [0,1,2,3,5,10,15,20] do
    out := out ++ [row "Corpus.Algorithms.fibonacci" (a1 n) (jNat (Corpus.Algorithms.fibonacci n))]
  -- isPrime (Algorithms) : Nat -> Bool
  for n in [0,1,2,3,4,5,17,25,97,100,113] do
    out := out ++ [row "Corpus.Algorithms.isPrime" (a1 n) (jBool (Corpus.Algorithms.isPrime n))]
  -- primeFactors (Algorithms) : Nat -> List Nat
  for n in [1,2,12,17,100,360] do
    out := out ++ [row "Corpus.Algorithms.primeFactors" (a1 n) (jListNat (Corpus.Algorithms.primeFactors n))]
  -- power (Algorithms) : Nat -> Nat -> Nat
  for (b, e) in [(2,10),(3,4),(5,0),(7,2),(1,100)] do
    out := out ++ [row "Corpus.Algorithms.power" (a2 b e) (jNat (Corpus.Algorithms.power b e))]
  -- insertionSort (Algorithms) : List Nat -> List Nat
  for xs in [[3,1,4,1,5],([] : List Nat),[1],[5,4,3,2,1],[2,2,2]] do
    out := out ++ [row "Corpus.Algorithms.insertionSort" (aL xs) (jListNat (Corpus.Algorithms.insertionSort xs))]
  -- mergeSort (Algorithms) : List Nat -> List Nat
  for xs in [[3,1,4,1,5,9,2,6],([] : List Nat),[1],[9,8,7,6,5]] do
    out := out ++ [row "Corpus.Algorithms.mergeSort" (aL xs) (jListNat (Corpus.Algorithms.mergeSort xs))]
  -- reverse (Algorithms) : List Nat -> List Nat (monomorphize to Nat)
  for xs in [[1,2,3],([] : List Nat),[7],[1,2,3,4,5]] do
    out := out ++ [row "Corpus.Algorithms.reverse" (aL xs) (jListNat (Corpus.Algorithms.reverse xs))]
  -- Math.factorial : Nat -> Nat
  for n in [0,1,2,5,7,10] do
    out := out ++ [row "Corpus.Math.factorial" (a1 n) (jNat (Corpus.Math.factorial n))]
  -- Math.pow : Nat -> Nat -> Nat
  for (b, e) in [(2,8),(3,3),(10,0),(6,2)] do
    out := out ++ [row "Corpus.Math.pow" (a2 b e) (jNat (Corpus.Math.pow b e))]
  -- Math.fastPow
  for (b, e) in [(2,10),(3,5),(5,0),(7,3)] do
    out := out ++ [row "Corpus.Math.fastPow" (a2 b e) (jNat (Corpus.Math.fastPow b e))]
  -- Math.min / max / clamp
  for (x, y) in [(3,7),(9,2),(5,5)] do
    out := out ++ [row "Corpus.Math.min" (a2 x y) (jNat (Corpus.Math.min x y))]
    out := out ++ [row "Corpus.Math.max" (a2 x y) (jNat (Corpus.Math.max x y))]
  -- NumberTheory.isPrime
  for n in [0,1,2,15,17,91,97] do
    out := out ++ [row "Corpus.NumberTheory.isPrime" (a1 n) (jBool (Corpus.NumberTheory.isPrime n))]
  -- NumberTheory.coprime : Nat -> Nat -> Bool
  for (x, y) in [(8,9),(6,9),(14,21),(1,1)] do
    out := out ++ [row "Corpus.NumberTheory.coprime" (a2 x y) (jBool (Corpus.NumberTheory.coprime x y))]
  -- Math.nextPrime
  for n in [1,2,7,14,20] do
    out := out ++ [row "Corpus.Math.nextPrime" (a1 n) (jNat (Corpus.Math.nextPrime n))]
  -- Math.numDivisors
  for n in [1,6,12,28,97] do
    out := out ++ [row "Corpus.Math.numDivisors" (a1 n) (jNat (Corpus.Math.numDivisors n))]
  -- Math.euler_phi
  for n in [1,6,10,12,36] do
    out := out ++ [row "Corpus.Math.euler_phi" (a1 n) (jNat (Corpus.Math.euler_phi n))]
  -- Sequences.lucas / tribonacci
  for n in [0,1,2,5,8] do
    out := out ++ [row "Corpus.Sequences.lucas" (a1 n) (jNat (Corpus.Sequences.lucas n))]
  for n in [0,1,2,5,8] do
    out := out ++ [row "Corpus.Sequences.tribonacci" (a1 n) (jNat (Corpus.Sequences.tribonacci n))]
  return out

-- The set of function names to transpile (must match the ORACLE rows above).
def transpileNames : List Name :=
  [`Corpus.Algorithms.gcd, `Corpus.Algorithms.lcm, `Corpus.Algorithms.fibonacci,
   `Corpus.Algorithms.isPrime, `Corpus.Algorithms.primeFactors, `Corpus.Algorithms.power,
   `Corpus.Algorithms.insertionSort, `Corpus.Algorithms.mergeSort, `Corpus.Algorithms.reverse,
   `Corpus.Math.factorial, `Corpus.Math.pow, `Corpus.Math.fastPow,
   `Corpus.Math.min, `Corpus.Math.max,
   `Corpus.NumberTheory.isPrime, `Corpus.NumberTheory.coprime,
   `Corpus.Math.nextPrime, `Corpus.Math.numDivisors, `Corpus.Math.euler_phi,
   `Corpus.Sequences.lucas, `Corpus.Sequences.tribonacci]

#eval show CoreM Unit from do
  IO.println "### PYTHON"
  IO.println (← emitPythonForNames `Corpus transpileNames)
  IO.println "### ORACLE"
  for l in oracleLines do
    IO.println l

end Roundtrip
