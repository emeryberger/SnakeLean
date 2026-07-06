/-
  Exhaustive Lean-oracle check (round-trip Option B).

  Where `Oracle.lean` samples inputs, this enumerates the ENTIRE bounded input
  domain for a set of functions and emits a Lean-computed oracle row for every
  point.  `run_oracle.py` then checks the transpiled Python agrees on all of
  them.  Exhaustive agreement over the bounded domain is a stronger faithfulness
  statement than sampling: there is no untested input in range.
-/
import SnakeLean
import Corpus.Algorithms
import Corpus.Math
import Corpus.NumberTheory

open Lean SnakeLean

namespace RoundtripExhaustive

def jNat (n : Nat) : String := toString n
def jBool (b : Bool) : String := if b then "true" else "false"
def jListNat (xs : List Nat) : String :=
  "[" ++ String.intercalate "," (xs.map toString) ++ "]"

def row (leanName argsJson resJson : String) : String :=
  "ORACLE\t" ++ leanName ++ "\t" ++ argsJson ++ "\t" ++ resJson

-- Bounds for the exhaustive domains.
def N1 : Nat := 60   -- unary Nat functions: all n in [0, N1]
def N2 : Nat := 25   -- binary Nat functions: all (x,y) in [0, N2]^2

def range (n : Nat) : List Nat := (List.range (n + 1))

open Corpus.Algorithms in open Corpus.Math in open Corpus.NumberTheory in
def oracleLines : List String := Id.run do
  let mut out : List String := []
  -- Unary Nat -> Nat / Bool / List Nat over [0, N1]
  for n in range N1 do
    let a1 := "[" ++ toString n ++ "]"
    out := out ++ [row "Corpus.Algorithms.fibonacci" a1 (jNat (Corpus.Algorithms.fibonacci n))]
    out := out ++ [row "Corpus.Algorithms.isPrime" a1 (jBool (Corpus.Algorithms.isPrime n))]
    out := out ++ [row "Corpus.NumberTheory.isPrime" a1 (jBool (Corpus.NumberTheory.isPrime n))]
    out := out ++ [row "Corpus.Algorithms.primeFactors" a1 (jListNat (Corpus.Algorithms.primeFactors n))]
    out := out ++ [row "Corpus.Math.numDivisors" a1 (jNat (Corpus.Math.numDivisors n))]
    out := out ++ [row "Corpus.Math.euler_phi" a1 (jNat (Corpus.Math.euler_phi n))]
    out := out ++ [row "Corpus.Math.nextPrime" a1 (jNat (Corpus.Math.nextPrime n))]
  -- Binary Nat -> Nat / Bool over [0, N2]^2
  for x in range N2 do
    for y in range N2 do
      let a2 := "[" ++ toString x ++ "," ++ toString y ++ "]"
      out := out ++ [row "Corpus.Algorithms.gcd" a2 (jNat (Corpus.Algorithms.gcd x y))]
      out := out ++ [row "Corpus.Algorithms.lcm" a2 (jNat (Corpus.Algorithms.lcm x y))]
      out := out ++ [row "Corpus.Math.min" a2 (jNat (Corpus.Math.min x y))]
      out := out ++ [row "Corpus.Math.max" a2 (jNat (Corpus.Math.max x y))]
      out := out ++ [row "Corpus.NumberTheory.coprime" a2 (jBool (Corpus.NumberTheory.coprime x y))]
  return out

def transpileNames : List Name :=
  [`Corpus.Algorithms.fibonacci, `Corpus.Algorithms.isPrime, `Corpus.NumberTheory.isPrime,
   `Corpus.Algorithms.primeFactors, `Corpus.Math.numDivisors, `Corpus.Math.euler_phi,
   `Corpus.Math.nextPrime, `Corpus.Algorithms.gcd, `Corpus.Algorithms.lcm,
   `Corpus.Math.min, `Corpus.Math.max, `Corpus.NumberTheory.coprime]

#eval show CoreM Unit from do
  IO.println "### PYTHON"
  IO.println (← emitPythonForNames `Corpus transpileNames)
  IO.println "### ORACLE"
  for l in oracleLines do
    IO.println l

end RoundtripExhaustive
