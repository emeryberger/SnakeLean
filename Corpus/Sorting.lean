/-
Sorting and searching algorithms for the Lean to Python corpus.
Contains various classic sorting algorithms.
-/
namespace Corpus.Sorting

-- Bubble sort
partial def bubbleSort (xs : List Nat) : List Nat :=
  let n := xs.length
  let arr := xs.toArray
  let rec outer (i : Nat) (arr : Array Nat) : Array Nat :=
    if i >= n then arr
    else
      let rec inner (j : Nat) (arr : Array Nat) : Array Nat :=
        if j >= n - i - 1 then arr
        else
          let arr := if arr[j]! > arr[j + 1]! then arr.swap! j (j + 1) else arr
          inner (j + 1) arr
      outer (i + 1) (inner 0 arr)
  (outer 0 arr).toList

-- Selection sort
partial def selectionSort (xs : List Nat) : List Nat :=
  let n := xs.length
  let arr := xs.toArray
  let rec go (i : Nat) (arr : Array Nat) : Array Nat :=
    if i >= n then arr
    else
      let rec findMin (j minIdx : Nat) : Nat :=
        if j >= n then minIdx
        else findMin (j + 1) (if arr[j]! < arr[minIdx]! then j else minIdx)
      let minIdx := findMin i i
      go (i + 1) (arr.swap! i minIdx)
  (go 0 arr).toList

-- Insertion sort
def insertionSort (xs : List Nat) : List Nat :=
  let rec insert (x : Nat) (sorted : List Nat) : List Nat :=
    match sorted with
    | [] => [x]
    | y :: ys => if x <= y then x :: y :: ys else y :: insert x ys
  xs.foldl (fun sorted x => insert x sorted) []

-- Counting sort (for small range of values)
partial def countingSort (xs : List Nat) (maxVal : Nat) : List Nat :=
  let counts := xs.foldl (fun arr x =>
    arr.set! x (arr.getD x 0 + 1)) (Array.mkArray (maxVal + 1) 0)
  let rec expand (i : Nat) (acc : List Nat) : List Nat :=
    if i > maxVal then acc
    else expand (i + 1) (acc ++ List.replicate (counts.getD i 0) i)
  expand 0 []

-- Radix sort (LSD, base 10)
partial def radixSort (xs : List Nat) : List Nat :=
  let maxVal := xs.foldl max 0
  let rec go (exp : Nat) (xs : List Nat) : List Nat :=
    if exp > maxVal then xs
    else
      let buckets := xs.foldl (fun arr x =>
        let digit := (x / exp) % 10
        arr.modify digit (x :: ·)) (Array.mkArray 10 [])
      let sorted := buckets.foldl (fun acc bucket => acc ++ bucket.reverse) []
      go (exp * 10) sorted
  go 1 xs

-- Gnome sort
partial def gnomeSort (xs : List Nat) : List Nat :=
  let n := xs.length
  let arr := xs.toArray
  let rec go (pos : Nat) (arr : Array Nat) : Array Nat :=
    if pos >= n then arr
    else if pos == 0 || arr[pos]! >= arr[pos - 1]! then go (pos + 1) arr
    else go (pos - 1) (arr.swap! pos (pos - 1))
  (go 0 arr).toList

-- Is sorted check
def isSorted (xs : List Nat) : Bool :=
  match xs with
  | [] => true
  | [_] => true
  | x :: y :: rest => x <= y && isSorted (y :: rest)

-- Is sorted descending
def isSortedDesc (xs : List Nat) : Bool :=
  match xs with
  | [] => true
  | [_] => true
  | x :: y :: rest => x >= y && isSortedDesc (y :: rest)

-- Find minimum
def findMin (xs : List Nat) : Option Nat :=
  xs.foldl (fun acc x => some (match acc with | none => x | some m => min m x)) none

-- Find maximum
def findMax (xs : List Nat) : Option Nat :=
  xs.foldl (fun acc x => some (match acc with | none => x | some m => max m x)) none

-- Find kth smallest (quickselect idea, simplified)
def kthSmallest (xs : List Nat) (k : Nat) : Option Nat :=
  let sorted := insertionSort xs
  sorted.get? k

-- Find kth largest
def kthLargest (xs : List Nat) (k : Nat) : Option Nat :=
  let sorted := insertionSort xs
  if k >= sorted.length then none
  else sorted.get? (sorted.length - 1 - k)

-- Median
def median (xs : List Nat) : Option Nat :=
  if xs.isEmpty then none
  else
    let sorted := insertionSort xs
    let n := sorted.length
    sorted.get? (n / 2)

-- Mode (most frequent element)
def mode (xs : List Nat) : Option Nat :=
  let rec count (x : Nat) (xs : List Nat) : Nat :=
    xs.foldl (fun acc y => if y == x then acc + 1 else acc) 0
  let rec go (xs : List Nat) (best : Option Nat) (bestCount : Nat) : Option Nat :=
    match xs with
    | [] => best
    | x :: rest =>
      let c := count x xs
      if c > bestCount then go rest (some x) c else go rest best bestCount
  go xs none 0

-- Unique elements only
def unique (xs : List Nat) : List Nat :=
  let rec go (xs : List Nat) (seen : List Nat) : List Nat :=
    match xs with
    | [] => seen.reverse
    | x :: rest => if seen.contains x then go rest seen else go rest (x :: seen)
  go xs []

-- Remove duplicates from sorted list
def removeDupsSorted (xs : List Nat) : List Nat :=
  match xs with
  | [] => []
  | [x] => [x]
  | x :: y :: rest =>
    if x == y then removeDupsSorted (y :: rest)
    else x :: removeDupsSorted (y :: rest)

-- Reverse a list
def reverseList (xs : List Nat) : List Nat :=
  let rec go (xs acc : List Nat) : List Nat :=
    match xs with
    | [] => acc
    | x :: rest => go rest (x :: acc)
  go xs []

-- Rotate list left by n positions
def rotateLeft (xs : List Nat) (n : Nat) : List Nat :=
  let len := xs.length
  if len == 0 then []
  else
    let n := n % len
    xs.drop n ++ xs.take n

-- Rotate list right by n positions
def rotateRight (xs : List Nat) (n : Nat) : List Nat :=
  let len := xs.length
  if len == 0 then []
  else
    let n := n % len
    xs.drop (len - n) ++ xs.take (len - n)

-- Interleave two lists
def interleave (xs ys : List Nat) : List Nat :=
  match xs, ys with
  | [], _ => ys
  | _, [] => xs
  | x :: xs', y :: ys' => x :: y :: interleave xs' ys'

-- Run-length encode
def runLengthEncode (xs : List Nat) : List (Nat × Nat) :=
  let rec go (xs : List Nat) (curr : Option Nat) (count : Nat) (acc : List (Nat × Nat)) : List (Nat × Nat) :=
    match xs, curr with
    | [], none => acc.reverse
    | [], some c => ((c, count) :: acc).reverse
    | x :: rest, none => go rest (some x) 1 acc
    | x :: rest, some c =>
      if x == c then go rest (some c) (count + 1) acc
      else go rest (some x) 1 ((c, count) :: acc)
  go xs none 0 []

-- Run-length decode
def runLengthDecode (encoded : List (Nat × Nat)) : List Nat :=
  encoded.foldl (fun acc (val, count) => acc ++ List.replicate count val) []

end Corpus.Sorting
