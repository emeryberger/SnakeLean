/-
Number Theory functions for the Lean to Python corpus.
Contains primality testing, factorization, modular arithmetic, etc.
-/
namespace Corpus.NumberTheory

-- Extended Euclidean algorithm
partial def extGcd (a b : Nat) : Int × Int × Nat :=
  if b == 0 then (1, 0, a)
  else
    let (x, y, g) := extGcd b (a % b)
    (y, x - (a / b : Int) * y, g)

-- Modular inverse (if it exists)
def modInverse (a m : Nat) : Option Nat :=
  let (x, _, g) := extGcd a m
  if g == 1 then some ((x % (m : Int) + (m : Int)) % (m : Int)).toNat
  else none

-- Euler's totient function (simplified)
partial def totient (n : Nat) : Nat :=
  if n <= 1 then n
  else
    let rec count (i : Nat) (acc : Nat) : Nat :=
      if i == n then acc
      else if gcd i n == 1 then count (i + 1) (acc + 1)
           else count (i + 1) acc
    count 1 0
where
  gcd (a b : Nat) : Nat := if b == 0 then a else gcd b (a % b)

-- Check if n is a perfect number
def isPerfect (n : Nat) : Bool :=
  if n < 2 then false
  else
    let divisorSum := (List.range n).foldl (fun acc i =>
      if i > 0 && n % i == 0 then acc + i else acc) 0
    divisorSum == n

-- Check if n is abundant
def isAbundant (n : Nat) : Bool :=
  if n < 2 then false
  else
    let divisorSum := (List.range n).foldl (fun acc i =>
      if i > 0 && n % i == 0 then acc + i else acc) 0
    divisorSum > n

-- Check if n is deficient
def isDeficient (n : Nat) : Bool :=
  if n < 1 then false
  else
    let divisorSum := (List.range n).foldl (fun acc i =>
      if i > 0 && n % i == 0 then acc + i else acc) 0
    divisorSum < n

-- Collatz sequence length
partial def collatzLength (n : Nat) : Nat :=
  if n <= 1 then 0
  else 1 + collatzLength (if n % 2 == 0 then n / 2 else 3 * n + 1)

-- Integer square root
def isqrt (n : Nat) : Nat :=
  if n == 0 then 0
  else
    let rec go (x : Nat) (fuel : Nat) : Nat :=
      match fuel with
      | 0 => x
      | fuel' + 1 =>
        let next := (x + n / x) / 2
        if next >= x then x else go next fuel'
    go n n

-- Check if n is a perfect square
def isPerfectSquare (n : Nat) : Bool :=
  let s := isqrt n
  s * s == n

-- Digital root (repeated digit sum until single digit)
partial def digitalRoot (n : Nat) : Nat :=
  if n < 10 then n
  else digitalRoot (digitSum n)
where
  digitSum (n : Nat) : Nat :=
    if n == 0 then 0
    else (n % 10) + digitSum (n / 10)

-- Harshad (Niven) number check
partial def isHarshad (n : Nat) : Bool :=
  if n == 0 then false
  else
    let ds := digitSum n
    ds > 0 && n % ds == 0
where
  digitSum (n : Nat) : Nat :=
    if n == 0 then 0
    else (n % 10) + digitSum (n / 10)

-- Hamming weight (population count)
partial def hammingWeight (n : Nat) : Nat :=
  if n == 0 then 0
  else (n % 2) + hammingWeight (n / 2)

-- Josephus problem
partial def josephus (n k : Nat) : Nat :=
  if n == 1 then 0
  else (josephus (n - 1) k + k) % n

-- Modular exponentiation
partial def modPow (base exp m : Nat) : Nat :=
  if exp == 0 then 1 % m
  else if exp % 2 == 0 then
    let half := modPow base (exp / 2) m
    (half * half) % m
  else (base * modPow base (exp - 1) m) % m

-- Sum of divisors
def sumDivisors (n : Nat) : Nat :=
  if n == 0 then 0
  else (List.range (n + 1)).foldl (fun acc i =>
    if i > 0 && n % i == 0 then acc + i else acc) 0

-- Number of divisors
def numDivisors (n : Nat) : Nat :=
  if n == 0 then 0
  else (List.range (n + 1)).foldl (fun acc i =>
    if i > 0 && n % i == 0 then acc + 1 else acc) 0

-- GCD using Euclidean algorithm
partial def gcd (a b : Nat) : Nat :=
  if b == 0 then a else gcd b (a % b)

-- LCM
def lcm (a b : Nat) : Nat :=
  if a == 0 || b == 0 then 0 else (a / gcd a b) * b

-- Check if coprime
def coprime (a b : Nat) : Bool :=
  gcd a b == 1

-- Simple primality test
partial def isPrime (n : Nat) : Bool :=
  if n < 2 then false
  else
    let rec check (d : Nat) : Bool :=
      if d * d > n then true
      else if n % d == 0 then false
      else check (d + 1)
    check 2

-- Prime factors
partial def primeFactors (n : Nat) : List Nat :=
  if n <= 1 then []
  else
    let rec go (n d : Nat) (acc : List Nat) : List Nat :=
      if d * d > n then
        if n > 1 then (n :: acc).reverse else acc.reverse
      else if n % d == 0 then go (n / d) d (d :: acc)
      else go n (d + 1) acc
    go n 2 []

-- Divisors of n
def divisors (n : Nat) : List Nat :=
  if n == 0 then []
  else (List.range (n + 1)).filter (fun i => i > 0 && n % i == 0)

-- Sum of digits
partial def digitSum (n : Nat) : Nat :=
  if n == 0 then 0
  else (n % 10) + digitSum (n / 10)

-- Number of digits
partial def numDigits (n : Nat) : Nat :=
  if n == 0 then 1
  else
    let rec go (n acc : Nat) : Nat :=
      if n == 0 then acc else go (n / 10) (acc + 1)
    go n 0

-- Reverse digits
partial def reverseDigits (n : Nat) : Nat :=
  let rec go (n acc : Nat) : Nat :=
    if n == 0 then acc else go (n / 10) (acc * 10 + n % 10)
  go n 0

-- Is palindrome number
def isPalindromeNum (n : Nat) : Bool :=
  n == reverseDigits n

end Corpus.NumberTheory
