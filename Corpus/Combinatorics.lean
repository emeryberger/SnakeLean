/-
Combinatorics functions for the Lean to Python corpus.
Contains permutations, combinations, partition functions, etc.
-/
namespace Corpus.Combinatorics

-- Factorial with tail recursion
partial def factorial (n : Nat) : Nat :=
  let rec go (n acc : Nat) : Nat :=
    if n == 0 then acc else go (n - 1) (n * acc)
  go n 1

-- Double factorial n!!
partial def doubleFactorial (n : Nat) : Nat :=
  if n <= 1 then 1
  else n * doubleFactorial (n - 2)

-- Rising factorial (Pochhammer symbol)
partial def risingFactorial (x n : Nat) : Nat :=
  let rec go (i acc : Nat) : Nat :=
    if i == n then acc
    else go (i + 1) (acc * (x + i))
  go 0 1

-- Falling factorial
partial def fallingFactorial (x n : Nat) : Nat :=
  let rec go (i acc : Nat) : Nat :=
    if i == n then acc
    else go (i + 1) (acc * (x - i))
  go 0 1

-- Binomial coefficient
partial def binomial (n k : Nat) : Nat :=
  if k > n then 0
  else
    let k := if k > n - k then n - k else k
    let rec go (i acc : Nat) : Nat :=
      if i == k then acc
      else go (i + 1) ((acc * (n - i)) / (i + 1))
    go 0 1

-- Multinomial coefficient
partial def multinomial (n : Nat) (ks : List Nat) : Nat :=
  let sum := ks.foldl (· + ·) 0
  if sum != n then 0
  else
    let num := factorial n
    let den := ks.foldl (fun acc k => acc * factorial k) 1
    num / den

-- Stirling number of the first kind (unsigned)
partial def stirling1 (n k : Nat) : Nat :=
  if k == 0 then if n == 0 then 1 else 0
  else if n == 0 then 0
  else (n - 1) * stirling1 (n - 1) k + stirling1 (n - 1) (k - 1)

-- Stirling number of the second kind
partial def stirling2 (n k : Nat) : Nat :=
  if k == 0 then if n == 0 then 1 else 0
  else if n == 0 then 0
  else k * stirling2 (n - 1) k + stirling2 (n - 1) (k - 1)

-- Bell number (number of partitions of a set)
partial def bell (n : Nat) : Nat :=
  let rec go (i acc : Nat) : Nat :=
    if i == n + 1 then acc
    else go (i + 1) (acc + stirling2 n i)
  go 0 0

-- Catalan number
partial def catalan (n : Nat) : Nat :=
  binomial (2 * n) n / (n + 1)

-- Derangement (subfactorial) - permutations with no fixed points
partial def derangement (n : Nat) : Nat :=
  if n == 0 then 1
  else if n == 1 then 0
  else (n - 1) * (derangement (n - 1) + derangement (n - 2))

-- Number of partitions of n
partial def partitionCount (n : Nat) : Nat :=
  let rec p (n k : Nat) : Nat :=
    if n == 0 then 1
    else if k == 0 then 0
    else if k > n then p n n
    else p (n - k) k + p n (k - 1)
  p n n

-- Generate all permutations
partial def permutations {α : Type} [BEq α] (xs : List α) : List (List α) :=
  match xs with
  | [] => [[]]
  | [x] => [[x]]
  | _ =>
    xs.bind fun x =>
      (permutations (xs.filter (· != x))).map (x :: ·)

-- Generate all combinations of size k
partial def combinations {α : Type} (k : Nat) (xs : List α) : List (List α) :=
  if k == 0 then [[]]
  else match xs with
  | [] => []
  | x :: rest =>
    (combinations (k - 1) rest).map (x :: ·) ++ combinations k rest

-- Generate all subsets (power set)
partial def powerSet {α : Type} (xs : List α) : List (List α) :=
  match xs with
  | [] => [[]]
  | x :: rest =>
    let restSubsets := powerSet rest
    restSubsets ++ restSubsets.map (x :: ·)

-- Count number of inversions in a list
partial def countInversions (xs : List Nat) : Nat :=
  let rec count (xs : List Nat) : Nat :=
    match xs with
    | [] => 0
    | x :: rest =>
      rest.foldl (fun acc y => if x > y then acc + 1 else acc) 0 + count rest
  count xs

-- Check if permutation is even (even number of inversions)
partial def isEvenPermutation (xs : List Nat) : Bool :=
  countInversions xs % 2 == 0

-- Lehmer code (factoradic representation)
partial def lehmerCode (perm : List Nat) : List Nat :=
  let rec go (perm : List Nat) (acc : List Nat) : List Nat :=
    match perm with
    | [] => acc.reverse
    | x :: rest =>
      let count := rest.foldl (fun acc y => if y < x then acc + 1 else acc) 0
      go rest (count :: acc)
  go perm []

-- From Lehmer code to permutation
partial def fromLehmerCode (code : List Nat) : List Nat :=
  let n := code.length
  let rec go (code : List Nat) (available : List Nat) (acc : List Nat) : List Nat :=
    match code with
    | [] => acc.reverse
    | c :: rest =>
      let elem := available.getD c 0
      go rest (available.filter (· != elem)) (elem :: acc)
  go code (List.range n) []

-- nth permutation in lexicographic order
partial def nthPermutation (n k : Nat) : List Nat :=
  let rec go (k n : Nat) (available : List Nat) (acc : List Nat) : List Nat :=
    match available with
    | [] => acc.reverse
    | _ =>
      let fact := factorial (available.length - 1)
      let idx := k / fact
      let elem := available.getD idx 0
      go (k % fact) n (available.filter (· != elem)) (elem :: acc)
  go k n (List.range n) []

-- Permutation rank (index in lexicographic order)
partial def permutationRank (perm : List Nat) : Nat :=
  let code := lehmerCode perm
  let n := code.length
  let rec go (code : List Nat) (pos : Nat) (acc : Nat) : Nat :=
    match code with
    | [] => acc
    | c :: rest => go rest (pos + 1) (acc + c * factorial (n - pos - 1))
  go code 0 0

-- Next permutation in lexicographic order
partial def nextPermutation (perm : List Nat) : Option (List Nat) :=
  let arr := perm.toArray
  let n := arr.size
  let rec findI (i : Nat) : Option Nat :=
    if i == 0 then none
    else if arr[i - 1]! < arr[i]! then some (i - 1)
    else findI (i - 1)
  match findI (n - 1) with
  | none => none
  | some i =>
    let rec findJ (j : Nat) : Nat :=
      if j == i + 1 then j
      else if arr[j - 1]! > arr[i]! then j - 1 else findJ (j - 1)
    let j := findJ n
    let arr := arr.swap! i j
    let arr := reverseFrom arr (i + 1)
    some arr.toList
where
  reverseFrom (arr : Array Nat) (start : Nat) : Array Nat :=
    let rec go (arr : Array Nat) (l r : Nat) : Array Nat :=
      if l >= r then arr
      else go (arr.swap! l r) (l + 1) (r - 1)
    go arr start (arr.size - 1)

-- Previous permutation
partial def prevPermutation (perm : List Nat) : Option (List Nat) :=
  let arr := perm.toArray
  let n := arr.size
  let rec findI (i : Nat) : Option Nat :=
    if i == 0 then none
    else if arr[i - 1]! > arr[i]! then some (i - 1)
    else findI (i - 1)
  match findI (n - 1) with
  | none => none
  | some i =>
    let rec findJ (j : Nat) : Nat :=
      if j == i + 1 then j
      else if arr[j - 1]! < arr[i]! then j - 1 else findJ (j - 1)
    let j := findJ n
    let arr := arr.swap! i j
    let arr := reverseFrom arr (i + 1)
    some arr.toList
where
  reverseFrom (arr : Array Nat) (start : Nat) : Array Nat :=
    let rec go (arr : Array Nat) (l r : Nat) : Array Nat :=
      if l >= r then arr
      else go (arr.swap! l r) (l + 1) (r - 1)
    go arr start (arr.size - 1)

-- Generate compositions of n (ordered partitions)
partial def compositions (n : Nat) : List (List Nat) :=
  if n == 0 then [[]]
  else
    let rec go (k : Nat) (acc : List (List Nat)) : List (List Nat) :=
      if k > n then acc
      else go (k + 1) (acc ++ (compositions (n - k)).map (k :: ·))
    go 1 []

-- Integer partitions of n
partial def integerPartitions (n : Nat) : List (List Nat) :=
  let rec go (n max : Nat) : List (List Nat) :=
    if n == 0 then [[]]
    else if max == 0 then []
    else
      let withMax := (go (n - max) max).map (max :: ·)
      let withoutMax := go n (max - 1)
      withMax ++ withoutMax
  go n n

end Corpus.Combinatorics
