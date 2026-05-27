/-
Algorithmic functions for testing Python extraction.
-/

namespace Corpus.Algorithms

-- Sorting algorithms

def insertionSort (xs : List Nat) : List Nat :=
  let rec insert (x : Nat) (sorted : List Nat) : List Nat :=
    match sorted with
    | [] => [x]
    | y :: ys => if x <= y then x :: y :: ys else y :: insert x ys
  let rec sort (unsorted : List Nat) (acc : List Nat) : List Nat :=
    match unsorted with
    | [] => acc
    | x :: xs => sort xs (insert x acc)
  sort xs []

def merge (xs ys : List Nat) : List Nat :=
  match xs, ys with
  | [], ys => ys
  | xs, [] => xs
  | x :: xs', y :: ys' =>
    if x <= y then x :: merge xs' (y :: ys')
    else y :: merge (x :: xs') ys'

def split (xs : List Nat) : List Nat × List Nat :=
  match xs with
  | [] => ([], [])
  | [x] => ([x], [])
  | x :: y :: rest =>
    let (l, r) := split rest
    (x :: l, y :: r)

partial def mergeSort (xs : List Nat) : List Nat :=
  match xs with
  | [] => []
  | [x] => [x]
  | _ =>
    let (l, r) := split xs
    merge (mergeSort l) (mergeSort r)

-- Searching

def linearSearch (xs : List Nat) (target : Nat) : Option Nat :=
  let rec go (xs : List Nat) (idx : Nat) : Option Nat :=
    match xs with
    | [] => none
    | x :: xs' => if x == target then some idx else go xs' (idx + 1)
  go xs 0

def binarySearch (arr : Array Nat) (target : Nat) : Option Nat :=
  let rec go (lo hi : Nat) (fuel : Nat) : Option Nat :=
    match fuel with
    | 0 => none
    | fuel' + 1 =>
      if lo >= hi then none
      else
        let mid := lo + (hi - lo) / 2
        match arr[mid]? with
        | none => none
        | some v =>
          if v == target then some mid
          else if v < target then go (mid + 1) hi fuel'
          else go lo mid fuel'
  go 0 arr.size arr.size

-- Numeric algorithms

partial def gcd (a b : Nat) : Nat :=
  if b == 0 then a else gcd b (a % b)

def lcm (a b : Nat) : Nat :=
  if a == 0 || b == 0 then 0 else (a / gcd a b) * b

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

def fibonacci (n : Nat) : Nat :=
  let rec go (a b : Nat) (k : Nat) : Nat :=
    match k with
    | 0 => a
    | k' + 1 => go b (a + b) k'
  go 0 1 n

partial def power (base exp : Nat) : Nat :=
  let rec go (b e acc : Nat) : Nat :=
    match e with
    | 0 => acc
    | _ =>
      if e % 2 == 0 then go (b * b) (e / 2) acc
      else go (b * b) (e / 2) (acc * b)
  go base exp 1

-- List algorithms

def reverse (xs : List α) : List α :=
  let rec go (xs acc : List α) : List α :=
    match xs with
    | [] => acc
    | x :: xs' => go xs' (x :: acc)
  go xs []

def take (n : Nat) (xs : List α) : List α :=
  match n, xs with
  | 0, _ => []
  | _, [] => []
  | n' + 1, x :: xs' => x :: take n' xs'

def drop (n : Nat) (xs : List α) : List α :=
  match n, xs with
  | 0, xs => xs
  | _, [] => []
  | n' + 1, _ :: xs' => drop n' xs'

def filter (p : α → Bool) (xs : List α) : List α :=
  match xs with
  | [] => []
  | x :: xs' => if p x then x :: filter p xs' else filter p xs'

def map (f : α → β) (xs : List α) : List β :=
  match xs with
  | [] => []
  | x :: xs' => f x :: map f xs'

def foldl (f : β → α → β) (init : β) (xs : List α) : β :=
  match xs with
  | [] => init
  | x :: xs' => foldl f (f init x) xs'

def foldr (f : α → β → β) (init : β) (xs : List α) : β :=
  match xs with
  | [] => init
  | x :: xs' => f x (foldr f init xs')

def zip (xs : List α) (ys : List β) : List (α × β) :=
  match xs, ys with
  | [], _ => []
  | _, [] => []
  | x :: xs', y :: ys' => (x, y) :: zip xs' ys'

def unzip (xys : List (α × β)) : List α × List β :=
  match xys with
  | [] => ([], [])
  | (x, y) :: rest =>
    let (xs, ys) := unzip rest
    (x :: xs, y :: ys)

def concat (xss : List (List α)) : List α :=
  match xss with
  | [] => []
  | xs :: xss' => xs ++ concat xss'

def intersperse (sep : α) (xs : List α) : List α :=
  match xs with
  | [] => []
  | [x] => [x]
  | x :: xs' => x :: sep :: intersperse sep xs'

def span (p : α → Bool) (xs : List α) : List α × List α :=
  match xs with
  | [] => ([], [])
  | x :: xs' =>
    if p x then
      let (ys, zs) := span p xs'
      (x :: ys, zs)
    else ([], xs)

def partition (p : α → Bool) (xs : List α) : List α × List α :=
  match xs with
  | [] => ([], [])
  | x :: xs' =>
    let (yes, no) := partition p xs'
    if p x then (x :: yes, no) else (yes, x :: no)

partial def groupBy (eq : α → α → Bool) (xs : List α) : List (List α) :=
  match xs with
  | [] => []
  | x :: xs' =>
    let (same, rest) := span (eq x) xs'
    (x :: same) :: groupBy eq rest

-- String algorithms

def isPalindrome (s : String) : Bool :=
  let chars := s.toList
  chars == chars.reverse

def countChar (c : Char) (s : String) : Nat :=
  s.toList.foldl (fun acc x => if x == c then acc + 1 else acc) 0

def replaceChar (old new : Char) (s : String) : String :=
  String.mk (s.toList.map (fun c => if c == old then new else c))

end Corpus.Algorithms
