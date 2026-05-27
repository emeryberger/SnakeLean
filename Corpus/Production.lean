/-
Production-quality algorithms - more complex implementations
suitable for real-world use cases.
-/

namespace Corpus.Production

-- ============================================================================
-- Red-Black Tree
-- ============================================================================

inductive Color where
  | red
  | black
deriving Repr, BEq

inductive RBTree (α : Type) where
  | empty : RBTree α
  | node : Color → RBTree α → α → RBTree α → RBTree α
deriving Repr

namespace RBTree

def singleton (x : α) : RBTree α := .node .red .empty x .empty

def member [Ord α] (x : α) : RBTree α → Bool
  | .empty => false
  | .node _ l y r =>
    match compare x y with
    | .lt => member x l
    | .eq => true
    | .gt => member x r

def balance : Color → RBTree α → α → RBTree α → RBTree α
  | .black, .node .red (.node .red a x b) y c, z, d =>
    .node .red (.node .black a x b) y (.node .black c z d)
  | .black, .node .red a x (.node .red b y c), z, d =>
    .node .red (.node .black a x b) y (.node .black c z d)
  | .black, a, x, .node .red (.node .red b y c) z d =>
    .node .red (.node .black a x b) y (.node .black c z d)
  | .black, a, x, .node .red b y (.node .red c z d) =>
    .node .red (.node .black a x b) y (.node .black c z d)
  | c, l, x, r => .node c l x r

partial def insertAux [Ord α] (x : α) : RBTree α → RBTree α
  | .empty => .node .red .empty x .empty
  | .node c l y r =>
    match compare x y with
    | .lt => balance c (insertAux x l) y r
    | .eq => .node c l y r
    | .gt => balance c l y (insertAux x r)

def makeBlack : RBTree α → RBTree α
  | .node _ l x r => .node .black l x r
  | t => t

def insert [Ord α] (x : α) (t : RBTree α) : RBTree α :=
  makeBlack (insertAux x t)

partial def toList : RBTree α → List α
  | .empty => []
  | .node _ l x r => toList l ++ [x] ++ toList r

def fromList [Ord α] (xs : List α) : RBTree α :=
  xs.foldl (fun t x => insert x t) .empty

def size : RBTree α → Nat
  | .empty => 0
  | .node _ l _ r => 1 + size l + size r

def height : RBTree α → Nat
  | .empty => 0
  | .node _ l _ r => 1 + max (height l) (height r)

def blackHeight : RBTree α → Nat
  | .empty => 1
  | .node c l _ _ =>
    (if c == .black then 1 else 0) + blackHeight l

end RBTree

-- ============================================================================
-- Union-Find with Path Compression and Union by Rank
-- ============================================================================

structure UFNode where
  parent : Nat
  rank : Nat
deriving Repr

structure UnionFind where
  nodes : Array UFNode
deriving Repr

namespace UnionFind

def empty : UnionFind := ⟨#[]⟩

def size (uf : UnionFind) : Nat := uf.nodes.size

def push (uf : UnionFind) : UnionFind :=
  ⟨uf.nodes.push ⟨uf.nodes.size, 0⟩⟩

partial def findWithPath (nodes : Array UFNode) (x : Nat) : Nat :=
  if h : x < nodes.size then
    let p := nodes[x].parent
    if p == x then x
    else findWithPath nodes p
  else x

def findRoot (uf : UnionFind) (x : Nat) : Nat := findWithPath uf.nodes x

def connected (uf : UnionFind) (x y : Nat) : Bool :=
  findRoot uf x == findRoot uf y

partial def union (uf : UnionFind) (x y : Nat) : UnionFind :=
  let rx := findRoot uf x
  let ry := findRoot uf y
  if rx == ry then uf
  else if h1 : rx < uf.nodes.size then
    if h2 : ry < uf.nodes.size then
      let rankX := uf.nodes[rx].rank
      let rankY := uf.nodes[ry].rank
      if rankX < rankY then
        ⟨uf.nodes.set! rx ⟨ry, rankX⟩⟩
      else if rankX > rankY then
        ⟨uf.nodes.set! ry ⟨rx, rankY⟩⟩
      else
        let nodes' := uf.nodes.set! ry ⟨rx, rankY⟩
        ⟨nodes'.set! rx ⟨rx, rankX + 1⟩⟩
    else uf
  else uf

def numComponents (uf : UnionFind) : Nat :=
  let roots := (List.range uf.nodes.size).filter fun i =>
    if h : i < uf.nodes.size then uf.nodes[i].parent == i else false
  roots.length

partial def ofSize (n : Nat) : UnionFind :=
  let rec build (i : Nat) (nodes : Array UFNode) : Array UFNode :=
    if i >= n then nodes
    else build (i + 1) (nodes.push ⟨i, 0⟩)
  ⟨build 0 #[]⟩

end UnionFind

-- ============================================================================
-- Quicksort (Lomuto partition)
-- ============================================================================

partial def lomutoPartition (arr : Array Nat) (lo hi : Nat) : Array Nat × Nat :=
  if hi <= lo then (arr, lo)
  else
    let pivot := arr[hi]!
    let rec go (arr : Array Nat) (i j : Nat) : Array Nat × Nat :=
      if j >= hi then
        let arr' := arr.swap! (i) hi
        (arr', i)
      else if arr[j]! < pivot then
        let arr' := arr.swap! i j
        go arr' (i + 1) (j + 1)
      else
        go arr i (j + 1)
    go arr lo lo

partial def quicksortAux (arr : Array Nat) (lo hi : Nat) : Array Nat :=
  if lo >= hi then arr
  else
    let (arr', p) := lomutoPartition arr lo hi
    let arr'' := if p > 0 then quicksortAux arr' lo (p - 1) else arr'
    if p + 1 < hi then quicksortAux arr'' (p + 1) hi else arr''

def quicksort (arr : Array Nat) : Array Nat :=
  if arr.size <= 1 then arr
  else quicksortAux arr 0 (arr.size - 1)

-- ============================================================================
-- String Matching: Naive and Z-Algorithm
-- ============================================================================

partial def naiveStringMatch (text pattern : String) : Option Nat :=
  let t := text.toList
  let p := pattern.toList
  let n := t.length
  let m := p.length
  if m == 0 then some 0
  else if m > n then none
  else
    let rec search (i : Nat) : Option Nat :=
      if i > n - m then none
      else if checkMatch t p i 0 then some i
      else search (i + 1)
    search 0
where
  checkMatch (t p : List Char) (i j : Nat) : Bool :=
    if j >= p.length then true
    else if t[i + j]! == p[j]! then checkMatch t p i (j + 1)
    else false

partial def naiveStringMatchAll (text pattern : String) : List Nat :=
  let t := text.toList
  let p := pattern.toList
  let n := t.length
  let m := p.length
  if m == 0 then List.range (n + 1)
  else if m > n then []
  else
    let rec search (i : Nat) (acc : List Nat) : List Nat :=
      if i > n - m then acc.reverse
      else if checkMatch t p i 0 then search (i + 1) (i :: acc)
      else search (i + 1) acc
    search 0 []
where
  checkMatch (t p : List Char) (i j : Nat) : Bool :=
    if j >= p.length then true
    else if t[i + j]! == p[j]! then checkMatch t p i (j + 1)
    else false

-- Z-array computation
partial def computeZArray (s : List Char) : Array Nat :=
  let n := s.length
  if n == 0 then #[]
  else
    let z := Array.mkArray n 0
    let z := z.set! 0 n
    let rec compute (z : Array Nat) (i l r : Nat) : Array Nat :=
      if i >= n then z
      else if i > r then
        let len := matchLength s s i 0
        let z' := z.set! i len
        if len > 0 then compute z' (i + 1) i (i + len - 1)
        else compute z' (i + 1) l r
      else
        let k := i - l
        if z[k]! < r - i + 1 then
          compute (z.set! i z[k]!) (i + 1) l r
        else
          let len := matchLength s s (r + 1) (r - i + 1)
          let z' := z.set! i (r - i + 1 + len)
          compute z' (i + 1) i (r + len)
    compute z 1 0 0
where
  matchLength (s t : List Char) (i j : Nat) : Nat :=
    if i >= s.length || j >= t.length then 0
    else if s[i]! == t[j]! then 1 + matchLength s t (i + 1) (j + 1)
    else 0

-- ============================================================================
-- Longest Common Subsequence (Nat lists for simplicity)
-- ============================================================================

partial def lcsLength (xs ys : List Nat) : Nat :=
  let m := xs.length
  let n := ys.length
  let rec fill (i j : Nat) (memo : Array Nat) : Array Nat :=
    if i > m then memo
    else if j > n then fill (i + 1) 0 memo
    else
      let idx := i * (n + 1) + j
      if i == 0 || j == 0 then
        fill i (j + 1) (memo.set! idx 0)
      else
        let xi := xs[i - 1]!
        let yj := ys[j - 1]!
        let val := if xi == yj then
          memo[(i - 1) * (n + 1) + (j - 1)]! + 1
        else
          max (memo[(i - 1) * (n + 1) + j]!) (memo[i * (n + 1) + (j - 1)]!)
        fill i (j + 1) (memo.set! idx val)
  let memo := Array.mkArray ((m + 1) * (n + 1)) 0
  let memo' := fill 0 0 memo
  memo'[m * (n + 1) + n]!

partial def lcs (xs ys : List Nat) : List Nat :=
  let m := xs.length
  let n := ys.length
  let rec fill (i j : Nat) (memo : Array Nat) : Array Nat :=
    if i > m then memo
    else if j > n then fill (i + 1) 0 memo
    else
      let idx := i * (n + 1) + j
      if i == 0 || j == 0 then
        fill i (j + 1) (memo.set! idx 0)
      else
        let xi := xs[i - 1]!
        let yj := ys[j - 1]!
        let val := if xi == yj then
          memo[(i - 1) * (n + 1) + (j - 1)]! + 1
        else
          max (memo[(i - 1) * (n + 1) + j]!) (memo[i * (n + 1) + (j - 1)]!)
        fill i (j + 1) (memo.set! idx val)
  let memo := Array.mkArray ((m + 1) * (n + 1)) 0
  let memo' := fill 0 0 memo
  let rec backtrack (i j : Nat) (acc : List Nat) : List Nat :=
    if i == 0 || j == 0 then acc
    else
      let xi := xs[i - 1]!
      let yj := ys[j - 1]!
      if xi == yj then backtrack (i - 1) (j - 1) (xi :: acc)
      else if memo'[(i - 1) * (n + 1) + j]! > memo'[i * (n + 1) + (j - 1)]! then
        backtrack (i - 1) j acc
      else backtrack i (j - 1) acc
  backtrack m n []

-- ============================================================================
-- Edit Distance (Levenshtein)
-- ============================================================================

partial def editDistance (xs ys : List Nat) : Nat :=
  let m := xs.length
  let n := ys.length
  let rec fill (i j : Nat) (dp : Array Nat) : Array Nat :=
    if i > m then dp
    else if j > n then fill (i + 1) 0 dp
    else
      let idx := i * (n + 1) + j
      let val := if i == 0 then j
        else if j == 0 then i
        else
          let xi := xs[i - 1]!
          let yj := ys[j - 1]!
          let cost := if xi == yj then 0 else 1
          min (min
            (dp[(i - 1) * (n + 1) + j]! + 1)
            (dp[i * (n + 1) + (j - 1)]! + 1))
            (dp[(i - 1) * (n + 1) + (j - 1)]! + cost)
      fill i (j + 1) (dp.set! idx val)
  let dp := Array.mkArray ((m + 1) * (n + 1)) 0
  let dp' := fill 0 0 dp
  dp'[m * (n + 1) + n]!

-- ============================================================================
-- Interval Scheduling (Greedy)
-- ============================================================================

def intervalScheduling (intervals : List (Nat × Nat)) : List (Nat × Nat) :=
  let sorted := intervals.toArray.qsort (fun a b => a.2 < b.2) |>.toList
  let rec select (remaining : List (Nat × Nat)) (lastEnd : Nat) (acc : List (Nat × Nat)) : List (Nat × Nat) :=
    match remaining with
    | [] => acc.reverse
    | (s, e) :: rest =>
      if s >= lastEnd then select rest e ((s, e) :: acc)
      else select rest lastEnd acc
  select sorted 0 []

-- ============================================================================
-- Knapsack Problem (0/1)
-- ============================================================================

partial def knapsack01 (capacity : Nat) (weights values : List Nat) : Nat :=
  let n := weights.length
  let rec fill (i w : Nat) (dp : Array Nat) : Array Nat :=
    if i > n then dp
    else if w > capacity then fill (i + 1) 0 dp
    else
      let idx := i * (capacity + 1) + w
      let val := if i == 0 then 0
        else
          let wi := weights[i - 1]!
          let vi := values[i - 1]!
          if wi > w then
            dp[(i - 1) * (capacity + 1) + w]!
          else
            max (dp[(i - 1) * (capacity + 1) + w]!)
                (dp[(i - 1) * (capacity + 1) + (w - wi)]! + vi)
      fill i (w + 1) (dp.set! idx val)
  let dp := Array.mkArray ((n + 1) * (capacity + 1)) 0
  let dp' := fill 0 0 dp
  dp'[n * (capacity + 1) + capacity]!

-- ============================================================================
-- Coin Change (Minimum Coins)
-- ============================================================================

partial def coinChange (coins : List Nat) (amount : Nat) : Option Nat :=
  let inf := amount + 1
  let rec fill (a : Nat) (dp : Array Nat) : Array Nat :=
    if a > amount then dp
    else
      let minCoins := coins.foldl (fun acc c =>
        if c <= a && dp[a - c]! < inf then min acc (dp[a - c]! + 1)
        else acc) inf
      fill (a + 1) (dp.set! a minCoins)
  let dp := Array.mkArray (amount + 1) inf
  let dp := dp.set! 0 0
  let dp' := fill 1 dp
  if dp'[amount]! >= inf then none else some dp'[amount]!

-- ============================================================================
-- Matrix Chain Multiplication (Optimal Parenthesization)
-- ============================================================================

partial def matrixChainOrder (dims : List Nat) : Nat :=
  let n := dims.length - 1
  if n <= 1 then 0
  else
    let inf := 1000000000
    let rec fill (len i : Nat) (dp : Array Nat) : Array Nat :=
      if len > n then dp
      else if i + len > n then fill (len + 1) 0 dp
      else
        let j := i + len - 1
        let idx := i * n + j
        if len == 1 then fill len (i + 1) (dp.set! idx 0)
        else
          let minCost := (List.range (len - 1)).foldl (fun acc k' =>
            let k := i + k'
            let cost := dp[i * n + k]! + dp[(k + 1) * n + j]! +
                       dims[i]! * dims[k + 1]! * dims[j + 1]!
            min acc cost) inf
          fill len (i + 1) (dp.set! idx minCost)
    let dp := Array.mkArray (n * n) inf
    let dp' := fill 1 0 dp
    dp'[n - 1]!

-- ============================================================================
-- Longest Increasing Subsequence
-- ============================================================================

partial def lisLength (xs : List Nat) : Nat :=
  let n := xs.length
  if n == 0 then 0
  else
    let rec fill (i : Nat) (dp : Array Nat) : Array Nat :=
      if i >= n then dp
      else
        let xi := xs[i]!
        let maxPrev := (List.range i).foldl (fun acc j =>
          if xs[j]! < xi then max acc (dp[j]! + 1)
          else acc) 1
        fill (i + 1) (dp.set! i maxPrev)
    let dp := Array.mkArray n 1
    let dp' := fill 0 dp
    dp'.foldl max 0

partial def lis (xs : List Nat) : List Nat :=
  let n := xs.length
  if n == 0 then []
  else
    let rec fill (i : Nat) (dp : Array Nat) (parent : Array Nat) : Array Nat × Array Nat :=
      if i >= n then (dp, parent)
      else
        let xi := xs[i]!
        let (maxLen, maxJ) := (List.range i).foldl (fun (acc, pj) j =>
          if xs[j]! < xi && dp[j]! + 1 > acc then (dp[j]! + 1, j)
          else (acc, pj)) (1, n)
        fill (i + 1) (dp.set! i maxLen) (parent.set! i maxJ)
    let dp := Array.mkArray n 1
    let parent := Array.mkArray n n
    let (dp', parent') := fill 0 dp parent
    let (_, maxIdx) := (List.range n).foldl (fun (maxVal, maxI) i =>
      if dp'[i]! > maxVal then (dp'[i]!, i) else (maxVal, maxI)) (0, 0)
    let rec backtrack (i : Nat) (acc : List Nat) : List Nat :=
      if i >= n then acc
      else backtrack (parent'[i]!) (xs[i]! :: acc)
    backtrack maxIdx []

-- ============================================================================
-- Maximum Subarray Sum (Kadane's Algorithm)
-- ============================================================================

def maxSubarraySum (xs : List Int) : Int :=
  let rec kadane (xs : List Int) (currentMax globalMax : Int) : Int :=
    match xs with
    | [] => globalMax
    | x :: rest =>
      let newCurrent := max x (currentMax + x)
      let newGlobal := max globalMax newCurrent
      kadane rest newCurrent newGlobal
  match xs with
  | [] => 0
  | x :: rest => kadane rest x x

-- ============================================================================
-- Count Inversions (using merge sort)
-- ============================================================================

partial def countInversions (xs : List Nat) : Nat :=
  (mergeCount xs).2
where
  mergeCount (xs : List Nat) : List Nat × Nat :=
    if xs.length <= 1 then (xs, 0)
    else
      let mid := xs.length / 2
      let (left, right) := (xs.take mid, xs.drop mid)
      let (sortedL, invL) := mergeCount left
      let (sortedR, invR) := mergeCount right
      let (merged, invMerge) := mergeAndCount sortedL sortedR
      (merged, invL + invR + invMerge)
  mergeAndCount (xs ys : List Nat) : List Nat × Nat :=
    let rec go (xs ys : List Nat) (acc : List Nat) (inv : Nat) : List Nat × Nat :=
      match xs, ys with
      | [], ys => (acc.reverse ++ ys, inv)
      | xs, [] => (acc.reverse ++ xs, inv)
      | x :: xs', y :: ys' =>
        if x <= y then go xs' (y :: ys') (x :: acc) inv
        else go (x :: xs') ys' (y :: acc) (inv + xs.length)
    go xs ys [] 0

end Corpus.Production
