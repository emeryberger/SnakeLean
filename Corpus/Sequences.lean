/-
Classic integer sequences for the Lean to Python corpus.
Contains Fibonacci, prime sequences, figurate numbers, etc.
-/
namespace Corpus.Sequences

-- Fibonacci sequence
partial def fibonacci (n : Nat) : Nat :=
  let rec go (n a b : Nat) : Nat :=
    if n == 0 then a
    else go (n - 1) b (a + b)
  go n 0 1

-- Lucas sequence
partial def lucas (n : Nat) : Nat :=
  let rec go (n a b : Nat) : Nat :=
    if n == 0 then a
    else go (n - 1) b (a + b)
  go n 2 1

-- Tribonacci sequence
partial def tribonacci (n : Nat) : Nat :=
  let rec go (n a b c : Nat) : Nat :=
    if n == 0 then a
    else go (n - 1) b c (a + b + c)
  go n 0 0 1

-- Pell numbers
partial def pell (n : Nat) : Nat :=
  let rec go (n a b : Nat) : Nat :=
    if n == 0 then a
    else go (n - 1) b (2 * b + a)
  go n 0 1

-- Padovan sequence
partial def padovan (n : Nat) : Nat :=
  let rec go (n a b c : Nat) : Nat :=
    if n == 0 then a
    else go (n - 1) b c (a + b)
  go n 1 1 1

-- Perrin sequence
partial def perrin (n : Nat) : Nat :=
  let rec go (n a b c : Nat) : Nat :=
    if n == 0 then a
    else go (n - 1) b c (a + b)
  go n 3 0 2

-- Jacobsthal numbers
partial def jacobsthal (n : Nat) : Nat :=
  let rec go (n a b : Nat) : Nat :=
    if n == 0 then a
    else go (n - 1) b (b + 2 * a)
  go n 0 1

-- Motzkin numbers
partial def motzkin (n : Nat) : Nat :=
  if n == 0 then 1
  else if n == 1 then 1
  else
    let rec go (k : Nat) (acc : Nat) : Nat :=
      if k == n + 1 then acc
      else go (k + 1) (acc + motzkin k * motzkin (n - 1 - k))
    motzkin (n - 1) + go 0 0

-- Narayana numbers N(n, k)
partial def narayana (n k : Nat) : Nat :=
  if k == 0 || k > n then 0
  else binomial n k * binomial n (k - 1) / n
where
  binomial (n k : Nat) : Nat :=
    if k > n then 0
    else
      let k := if k > n - k then n - k else k
      let rec go (i acc : Nat) : Nat :=
        if i == k then acc
        else go (i + 1) ((acc * (n - i)) / (i + 1))
      go 0 1

-- Triangular numbers
partial def triangular (n : Nat) : Nat :=
  n * (n + 1) / 2

-- Square numbers
partial def square (n : Nat) : Nat :=
  n * n

-- Pentagonal numbers
partial def pentagonal (n : Nat) : Nat :=
  n * (3 * n - 1) / 2

-- Hexagonal numbers
partial def hexagonal (n : Nat) : Nat :=
  n * (2 * n - 1)

-- Heptagonal numbers
partial def heptagonal (n : Nat) : Nat :=
  n * (5 * n - 3) / 2

-- Octagonal numbers
partial def octagonal (n : Nat) : Nat :=
  n * (3 * n - 2)

-- Generalized k-gonal numbers
partial def kGonal (k n : Nat) : Nat :=
  n * ((k - 2) * n - (k - 4)) / 2

-- Tetrahedral numbers
partial def tetrahedral (n : Nat) : Nat :=
  n * (n + 1) * (n + 2) / 6

-- Pyramidal numbers (square base)
partial def pyramidal (n : Nat) : Nat :=
  n * (n + 1) * (2 * n + 1) / 6

-- Centered triangular numbers
partial def centeredTriangular (n : Nat) : Nat :=
  (3 * n * n + 3 * n + 2) / 2

-- Centered square numbers
partial def centeredSquare (n : Nat) : Nat :=
  n * n + (n + 1) * (n + 1)

-- Centered hexagonal numbers
partial def centeredHexagonal (n : Nat) : Nat :=
  3 * n * (n - 1) + 1

-- Star numbers
partial def starNumber (n : Nat) : Nat :=
  6 * n * (n - 1) + 1

-- Pronic numbers (oblong numbers)
partial def pronic (n : Nat) : Nat :=
  n * (n + 1)

-- Cullen numbers C_n = n * 2^n + 1
partial def cullen (n : Nat) : Nat :=
  n * (2 ^ n) + 1

-- Woodall numbers W_n = n * 2^n - 1
partial def woodall (n : Nat) : Nat :=
  n * (2 ^ n) - 1

-- Mersenne numbers M_n = 2^n - 1
partial def mersenne (n : Nat) : Nat :=
  (2 ^ n) - 1

-- Fermat numbers F_n = 2^(2^n) + 1
partial def fermat (n : Nat) : Nat :=
  (2 ^ (2 ^ n)) + 1

-- Sophie Germain safe primes related: 2p + 1
partial def safeFromGermain (p : Nat) : Nat :=
  2 * p + 1

-- Repunit R_n (n ones in base 10)
partial def repunit (n : Nat) : Nat :=
  let rec go (n acc : Nat) : Nat :=
    if n == 0 then acc
    else go (n - 1) (acc * 10 + 1)
  go n 0

-- Look-and-say sequence next term
partial def lookAndSayNext (xs : List Nat) : List Nat :=
  let rec go (xs : List Nat) (curr : Nat) (count : Nat) (acc : List Nat) : List Nat :=
    match xs with
    | [] => (acc ++ [count, curr]).reverse
    | x :: rest =>
      if x == curr then go rest curr (count + 1) acc
      else go rest x 1 (curr :: count :: acc)
  match xs with
  | [] => []
  | x :: rest => (go rest x 1 []).reverse

-- Collatz sequence
partial def collatzSequence (n : Nat) : List Nat :=
  if n <= 1 then [n]
  else n :: collatzSequence (if n % 2 == 0 then n / 2 else 3 * n + 1)

-- Recaman sequence
partial def recaman (n : Nat) : List Nat :=
  let rec go (i : Nat) (prev : Nat) (seen : List Nat) (acc : List Nat) : List Nat :=
    if i > n then acc.reverse
    else
      let candidate := prev - i
      let next := if candidate > 0 && !seen.contains candidate then candidate else prev + i
      go (i + 1) next (next :: seen) (next :: acc)
  go 1 0 [0] [0]

-- Sylvester's sequence
partial def sylvester (n : Nat) : Nat :=
  if n == 0 then 2
  else
    let prev := sylvester (n - 1)
    prev * prev - prev + 1

-- Alcuin's sequence (3 jugs problem)
partial def alcuin (n : Nat) : Nat :=
  if n % 12 == 0 then n * n / 12
  else if n % 12 == 3 || n % 12 == 9 then (n * n - 3) / 12
  else if n % 12 == 6 then (n * n - 12) / 12
  else (n * n + 3) / 12

-- A000045: Fibonacci (already defined, but listed for completeness)
-- A000040: Prime numbers (generate first n)
partial def firstNPrimes (n : Nat) : List Nat :=
  let rec go (candidate : Nat) (found : List Nat) : List Nat :=
    if found.length >= n then found.reverse
    else if isPrime candidate then go (candidate + 1) (candidate :: found)
    else go (candidate + 1) found
  go 2 []
where
  isPrime (n : Nat) : Bool :=
    if n < 2 then false
    else
      let rec check (d : Nat) : Bool :=
        if d * d > n then true
        else if n % d == 0 then false
        else check (d + 1)
      check 2

-- Van Eck's sequence
partial def vanEck (n : Nat) : List Nat :=
  let rec go (i : Nat) (prev : Nat) (lastSeen : List (Nat × Nat)) (acc : List Nat) : List Nat :=
    if i > n then acc.reverse
    else
      let next := match lastSeen.find? (fun p => p.1 == prev) with
        | none => 0
        | some (_, idx) => i - 1 - idx
      let newLastSeen := (prev, i - 1) :: lastSeen.filter (fun p => p.1 != prev)
      go (i + 1) next newLastSeen (next :: acc)
  go 1 0 [] [0]

end Corpus.Sequences
