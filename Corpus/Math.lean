/-
Mathematical functions for testing Python extraction.
-/

namespace Corpus.Math

-- Basic arithmetic

def abs (x : Int) : Int := if x < 0 then -x else x

def sign (x : Int) : Int :=
  if x < 0 then -1
  else if x > 0 then 1
  else 0

def min (a b : Nat) : Nat := if a <= b then a else b

def max (a b : Nat) : Nat := if a >= b then a else b

def clamp (lo hi x : Nat) : Nat := min hi (max lo x)

-- Division and modulo

def divMod (a b : Nat) : Nat × Nat := (a / b, a % b)

def quotRem (a b : Int) : Int × Int := (a / b, a % b)

-- Exponentiation

def pow (base exp : Nat) : Nat :=
  match exp with
  | 0 => 1
  | n + 1 => base * pow base n

partial def fastPow (base exp : Nat) : Nat :=
  let rec go (b e acc : Nat) : Nat :=
    match e with
    | 0 => acc
    | _ =>
      if e % 2 == 0 then go (b * b) (e / 2) acc
      else go (b * b) (e / 2) (acc * b)
  go base exp 1

partial def modPow (base exp m : Nat) : Nat :=
  let rec go (b e acc : Nat) : Nat :=
    match e with
    | 0 => acc % m
    | _ =>
      if e % 2 == 0 then go ((b * b) % m) (e / 2) acc
      else go ((b * b) % m) (e / 2) ((acc * b) % m)
  go (base % m) exp 1

-- Number theory

partial def gcd (a b : Nat) : Nat :=
  if b == 0 then a else gcd b (a % b)

def lcm (a b : Nat) : Nat :=
  if a == 0 || b == 0 then 0 else (a / gcd a b) * b

def coprime (a b : Nat) : Bool := gcd a b == 1

def extendedGcd (a b : Nat) : Int × Int × Nat :=
  let rec go (r0 r1 s0 s1 t0 t1 : Int) (fuel : Nat) : Int × Int × Nat :=
    match fuel with
    | 0 => (s0, t0, r0.toNat)
    | fuel' + 1 =>
      if r1 == 0 then (s0, t0, r0.toNat)
      else
        let q := r0 / r1
        go r1 (r0 - q * r1) s1 (s0 - q * s1) t1 (t0 - q * t1) fuel'
  go a b 1 0 0 1 (a + b)

def modInverse (a m : Nat) : Option Nat :=
  let (x, _, g) := extendedGcd a m
  if g == 1 then
    let x' := ((x % m) + m) % m
    some x'.toNat
  else none

-- Primes

def isPrime (n : Nat) : Bool :=
  if n < 2 then false
  else
    let rec check (d : Nat) (fuel : Nat) : Bool :=
      match fuel with
      | 0 => true
      | fuel' + 1 =>
        if d * d > n then true
        else if n % d == 0 then false
        else check (d + 1) fuel'
    check 2 n

def nextPrime (n : Nat) : Nat :=
  let rec go (k : Nat) (fuel : Nat) : Nat :=
    match fuel with
    | 0 => k
    | fuel' + 1 =>
      if isPrime k then k else go (k + 1) fuel'
  go (if n < 2 then 2 else n) 1000

def nthPrime (n : Nat) : Nat :=
  let rec go (k count : Nat) (fuel : Nat) : Nat :=
    match fuel with
    | 0 => k
    | fuel' + 1 =>
      if count == n then k
      else if isPrime (k + 1) then go (k + 1) (count + 1) fuel'
      else go (k + 1) count fuel'
  if n == 0 then 2 else go 1 0 (n * 20)

partial def sieveOfEratosthenes (limit : Nat) : List Nat :=
  let rec mark (sieve : List (Nat × Bool)) (p : Nat) : List (Nat × Bool) :=
    sieve.map fun (n, isPrime) =>
      if n > p && n % p == 0 then (n, false) else (n, isPrime)
  let rec sieve (xs : List (Nat × Bool)) (acc : List Nat) : List Nat :=
    match xs with
    | [] => acc.reverse
    | (n, false) :: rest => sieve rest acc
    | (n, true) :: rest => sieve (mark rest n) (n :: acc)
  let initial := (List.range limit).drop 2 |>.map (fun n => (n, true))
  sieve initial []

def primeFactors (n : Nat) : List Nat :=
  let rec go (n d : Nat) (acc : List Nat) (fuel : Nat) : List Nat :=
    match fuel with
    | 0 => acc.reverse
    | fuel' + 1 =>
      if n <= 1 then acc.reverse
      else if d * d > n then (n :: acc).reverse
      else if n % d == 0 then go (n / d) d (d :: acc) fuel'
      else go n (d + 1) acc fuel'
  go n 2 [] n

partial def divisors (n : Nat) : List Nat :=
  let rec go (d : Nat) (acc : List Nat) : List Nat :=
    if d * d > n then acc
    else if n % d == 0 then
      if d * d == n then go (d + 1) (d :: acc)
      else go (d + 1) (d :: n / d :: acc)
    else go (d + 1) acc
  (go 1 []).reverse

def numDivisors (n : Nat) : Nat := (divisors n).length

def sumDivisors (n : Nat) : Nat := (divisors n).foldl (· + ·) 0

def euler_phi (n : Nat) : Nat :=
  let factors := primeFactors n
  let uniqueFactors := factors.eraseDups
  uniqueFactors.foldl (fun acc p => acc * (p - 1) / p * p) n /
    (if uniqueFactors.isEmpty then 1 else uniqueFactors.foldl (· * ·) 1) *
    uniqueFactors.foldl (fun acc p => acc * (p - 1)) 1

-- Fibonacci and related

def fibonacci (n : Nat) : Nat :=
  let rec go (a b : Nat) (k : Nat) : Nat :=
    match k with
    | 0 => a
    | k' + 1 => go b (a + b) k'
  go 0 1 n

def lucas (n : Nat) : Nat :=
  let rec go (a b : Nat) (k : Nat) : Nat :=
    match k with
    | 0 => a
    | k' + 1 => go b (a + b) k'
  go 2 1 n

def tribonacci (n : Nat) : Nat :=
  let rec go (a b c : Nat) (k : Nat) : Nat :=
    match k with
    | 0 => a
    | k' + 1 => go b c (a + b + c) k'
  go 0 0 1 n

-- Combinatorics

def factorial (n : Nat) : Nat :=
  match n with
  | 0 => 1
  | n' + 1 => (n' + 1) * factorial n'

partial def binomial (n k : Nat) : Nat :=
  if k > n then 0
  else
    let rec go (num den : Nat) (i : Nat) : Nat :=
      if i > k then num / den
      else go (num * (n - i + 1)) (den * i) (i + 1)
    go 1 1 1

def catalan (n : Nat) : Nat :=
  binomial (2 * n) n / (n + 1)

def permutations (n k : Nat) : Nat :=
  if k > n then 0
  else factorial n / factorial (n - k)

partial def stirling2 (n k : Nat) : Nat :=
  if k == 0 then if n == 0 then 1 else 0
  else if k > n then 0
  else
    let rec go (i : Nat) (acc : Int) : Int :=
      if i > k then acc
      else
        let sign : Int := if (k - i) % 2 == 0 then 1 else -1
        let term : Int := sign * (binomial k i : Int) * (pow i n : Int)
        go (i + 1) (acc + term)
    (go 0 0 / (factorial k : Int)).toNat

partial def bell (n : Nat) : Nat :=
  let rec go (k : Nat) (acc : Nat) : Nat :=
    if k > n then acc
    else go (k + 1) (acc + stirling2 n k)
  go 0 0

-- Sequences

def triangularNumber (n : Nat) : Nat := n * (n + 1) / 2

def squareNumber (n : Nat) : Nat := n * n

def pentagonalNumber (n : Nat) : Nat := n * (3 * n - 1) / 2

def hexagonalNumber (n : Nat) : Nat := n * (2 * n - 1)

def isqrt (n : Nat) : Nat :=
  let rec go (x : Nat) (fuel : Nat) : Nat :=
    match fuel with
    | 0 => x
    | fuel' + 1 =>
      let x' := (x + n / x) / 2
      if x' >= x then x else go x' fuel'
  if n == 0 then 0 else go n n

def isTriangular (n : Nat) : Bool :=
  let x := (isqrt (8 * n + 1) - 1) / 2
  x * (x + 1) / 2 == n

def isSquare (n : Nat) : Bool :=
  let x := isqrt n
  x * x == n

-- Digit operations

partial def digits (n : Nat) (base : Nat := 10) : List Nat :=
  if base < 2 then []
  else
    let rec go (n : Nat) (acc : List Nat) : List Nat :=
      if n == 0 then if acc.isEmpty then [0] else acc
      else go (n / base) ((n % base) :: acc)
    go n []

def fromDigits (ds : List Nat) (base : Nat := 10) : Nat :=
  ds.foldl (fun acc d => acc * base + d) 0

def numDigits (n : Nat) (base : Nat := 10) : Nat :=
  (digits n base).length

def digitSum (n : Nat) (base : Nat := 10) : Nat :=
  (digits n base).foldl (· + ·) 0

-- Base-10 wrappers for LCNF extraction compatibility
def numDigits10 (n : Nat) : Nat := numDigits n 10

def digitSum10 (n : Nat) : Nat := digitSum n 10

-- Parity tests
def isEven (n : Nat) : Bool := n % 2 == 0

def isOdd (n : Nat) : Bool := n % 2 == 1

def digitalRoot (n : Nat) : Nat :=
  let rec go (n : Nat) (fuel : Nat) : Nat :=
    match fuel with
    | 0 => n
    | fuel' + 1 =>
      let s := digitSum n
      if s < 10 then s else go s fuel'
  go n 100

def reverseDigits (n : Nat) : Nat :=
  fromDigits (digits n).reverse

def isPalindromeNum (n : Nat) : Bool :=
  n == reverseDigits n

end Corpus.Math
