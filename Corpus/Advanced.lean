/-
Advanced algorithms and data structures for Python extraction testing.
Inspired by the Lean batteries library.
-/

namespace Corpus.Advanced

-- Binary Heap (simplified, without dependent types)
structure Heap (α : Type) where
  data : List α
  deriving Repr

def Heap.empty : Heap α := ⟨[]⟩

def Heap.isEmpty (h : Heap α) : Bool := h.data.isEmpty

def Heap.size (h : Heap α) : Nat := h.data.length

-- Parent index in heap
def parent (i : Nat) : Nat := (i - 1) / 2

-- Left child index
def leftChild (i : Nat) : Nat := 2 * i + 1

-- Right child index
def rightChild (i : Nat) : Nat := 2 * i + 2

-- Swap elements at indices i and j in a list
def swapAt (xs : List α) (i j : Nat) : List α :=
  match xs[i]?, xs[j]? with
  | some a, some b => xs.set i b |>.set j a
  | _, _ => xs

-- Sift up: move element at index i up to maintain heap property
partial def siftUp [Ord α] (xs : List α) (i : Nat) : List α :=
  if i == 0 then xs
  else
    let p := parent i
    match xs[i]?, xs[p]? with
    | some vi, some vp =>
      if compare vi vp == Ordering.lt then
        siftUp (swapAt xs i p) p
      else xs
    | _, _ => xs

-- Sift down: move element at index i down to maintain heap property
partial def siftDown [Ord α] (xs : List α) (i : Nat) : List α :=
  let n := xs.length
  let l := leftChild i
  let r := rightChild i
  if l >= n then xs  -- No children
  else
    -- Find the smaller child
    let smaller :=
      if r >= n then l  -- Only left child exists
      else match xs[l]?, xs[r]? with
        | some vl, some vr => if compare vl vr == Ordering.lt then l else r
        | _, _ => l
    match xs[i]?, xs[smaller]? with
    | some vi, some vs =>
      if compare vs vi == Ordering.lt then
        siftDown (swapAt xs i smaller) smaller
      else xs
    | _, _ => xs

-- Insert into min-heap
def Heap.insert [Ord α] (h : Heap α) (x : α) : Heap α :=
  let newData := h.data ++ [x]
  ⟨siftUp newData (newData.length - 1)⟩

-- Get minimum element
def Heap.min (h : Heap α) : Option α := h.data.head?

-- Remove minimum element
def Heap.popMin [Ord α] (h : Heap α) : Heap α :=
  match h.data with
  | [] => h
  | [_] => ⟨[]⟩
  | _ :: rest =>
    match rest.getLast? with
    | none => ⟨[]⟩
    | some last => ⟨siftDown (last :: rest.dropLast) 0⟩

-- Build heap from list (heapify)
def Heap.ofList [Ord α] (xs : List α) : Heap α :=
  xs.foldl (·.insert ·) Heap.empty

-- Heap sort
def heapSort [Ord α] (xs : List α) : List α :=
  let rec extract (h : Heap α) (acc : List α) (fuel : Nat) : List α :=
    match fuel with
    | 0 => acc.reverse
    | fuel' + 1 =>
      match h.min with
      | none => acc.reverse
      | some x => extract h.popMin (x :: acc) fuel'
  extract (Heap.ofList xs) [] (xs.length + 1)

-- Union-Find (simplified)
structure UnionFind where
  parent : List Nat  -- parent[i] is the parent of node i
  rank : List Nat    -- rank[i] is the rank of node i
  deriving Repr

def UnionFind.empty : UnionFind := ⟨[], []⟩

def UnionFind.size (uf : UnionFind) : Nat := uf.parent.length

-- Add a new element (as its own set)
def UnionFind.push (uf : UnionFind) : UnionFind :=
  let n := uf.parent.length
  ⟨uf.parent ++ [n], uf.rank ++ [0]⟩

-- Create union-find with n elements
def UnionFind.ofSize (n : Nat) : UnionFind :=
  ⟨List.range n, List.replicate n 0⟩

-- Find root of element (with path compression would require mutation)
partial def UnionFind.root (uf : UnionFind) (i : Nat) : Nat :=
  match uf.parent[i]? with
  | none => i
  | some p => if p == i then i else uf.root p

-- Check if two elements are in the same set
def UnionFind.equiv (uf : UnionFind) (i j : Nat) : Bool :=
  uf.root i == uf.root j

-- Union two sets (union by rank)
def UnionFind.union (uf : UnionFind) (i j : Nat) : UnionFind :=
  let ri := uf.root i
  let rj := uf.root j
  if ri == rj then uf
  else
    match uf.rank[ri]?, uf.rank[rj]? with
    | some ranki, some rankj =>
      if ranki < rankj then
        ⟨uf.parent.set ri rj, uf.rank⟩
      else if ranki > rankj then
        ⟨uf.parent.set rj ri, uf.rank⟩
      else
        ⟨uf.parent.set rj ri, uf.rank.set ri (ranki + 1)⟩
    | _, _ => uf

-- Count number of distinct sets
def UnionFind.numSets (uf : UnionFind) : Nat :=
  let roots := List.range uf.size |>.filter (fun i => uf.root i == i)
  roots.length

-- Graph algorithms
structure Graph where
  vertices : Nat
  edges : List (Nat × Nat)
  deriving Repr

def Graph.empty : Graph := ⟨0, []⟩

def Graph.addVertex (g : Graph) : Graph :=
  ⟨g.vertices + 1, g.edges⟩

def Graph.addEdge (g : Graph) (u v : Nat) : Graph :=
  ⟨g.vertices, (u, v) :: g.edges⟩

-- Get neighbors of a vertex
def Graph.neighbors (g : Graph) (v : Nat) : List Nat :=
  g.edges.filterMap fun (u, w) =>
    if u == v then some w
    else if w == v then some u  -- undirected
    else none

-- BFS traversal
partial def Graph.bfs (g : Graph) (start : Nat) : List Nat :=
  let rec loop (queue : List Nat) (visited : List Nat) (fuel : Nat) : List Nat :=
    match fuel with
    | 0 => visited.reverse
    | fuel' + 1 =>
      match queue with
      | [] => visited.reverse
      | v :: rest =>
        if visited.contains v then loop rest visited fuel'
        else
          let newVisited := v :: visited
          let neighbors := g.neighbors v |>.filter (!newVisited.contains ·)
          loop (rest ++ neighbors) newVisited fuel'
  loop [start] [] (g.vertices + g.edges.length + 1)

-- DFS traversal
partial def Graph.dfs (g : Graph) (start : Nat) : List Nat :=
  let rec loop (stack : List Nat) (visited : List Nat) (fuel : Nat) : List Nat :=
    match fuel with
    | 0 => visited.reverse
    | fuel' + 1 =>
      match stack with
      | [] => visited.reverse
      | v :: rest =>
        if visited.contains v then loop rest visited fuel'
        else
          let newVisited := v :: visited
          let neighbors := g.neighbors v |>.filter (!newVisited.contains ·)
          loop (neighbors ++ rest) newVisited fuel'
  loop [start] [] (g.vertices + g.edges.length + 1)

-- Check if graph is connected (for undirected graph)
def Graph.isConnected (g : Graph) : Bool :=
  if g.vertices == 0 then true
  else
    let visited := g.bfs 0
    visited.length == g.vertices

-- Topological sort (for DAG) - Kahn's algorithm
def Graph.topoSort (g : Graph) : Option (List Nat) :=
  -- Compute in-degrees
  let inDegree := List.range g.vertices |>.map fun v =>
    g.edges.filter (·.2 == v) |>.length

  let rec loop (queue : List Nat) (inDeg : List Nat) (result : List Nat) (fuel : Nat) : Option (List Nat) :=
    match fuel with
    | 0 => none  -- Cycle detected or too many iterations
    | fuel' + 1 =>
      match queue with
      | [] =>
        if result.length == g.vertices then some result.reverse
        else none  -- Cycle detected
      | v :: rest =>
        let newResult := v :: result
        -- Decrease in-degree of neighbors
        let outEdges := g.edges.filter (·.1 == v)
        let (newInDeg, newQueue) := outEdges.foldl (fun (deg, q) (_, w) =>
          match deg[w]? with
          | some d =>
            let newD := d - 1
            let newDeg := deg.set w newD
            if newD == 0 then (newDeg, w :: q) else (newDeg, q)
          | none => (deg, q)
        ) (inDeg, rest)
        loop newQueue newInDeg newResult fuel'

  -- Start with vertices having in-degree 0
  let initQueue := List.range g.vertices |>.filter fun v =>
    inDegree[v]? |>.map (· == 0) |>.getD false
  loop initQueue inDegree [] (g.vertices + 1)

-- Detect cycle in directed graph
def Graph.hasCycle (g : Graph) : Bool :=
  g.topoSort.isNone

-- Matrix operations (for algorithms like Floyd-Warshall)
abbrev Matrix := List (List Int)

def Matrix.get (m : Matrix) (i j : Nat) : Option Int :=
  match m[i]? with
  | none => none
  | some row => row[j]?

def Matrix.set (m : Matrix) (i j : Nat) (v : Int) : Matrix :=
  m.zipIdx.map fun (row, idx) =>
    if idx == i then row.zipIdx.map fun (val, jdx) => if jdx == j then v else val
    else row

-- Create n×n matrix filled with value
def Matrix.create (n : Nat) (fill : Int) : Matrix :=
  List.replicate n (List.replicate n fill)

-- Floyd-Warshall shortest paths (fuel-based to avoid termination proofs)
def floydWarshall (n : Nat) (edges : List (Nat × Nat × Int)) : Matrix :=
  let inf := 1000000000  -- Large value representing infinity
  -- Initialize distance matrix
  let init := Matrix.create n inf
  let withDiag := List.range n |>.foldl (fun m i => m.set i i 0) init
  let withEdges := edges.foldl (fun m (u, v, w) => m.set u v w) withDiag
  -- Main algorithm using foldl instead of recursion
  List.range n |>.foldl (fun dist k =>
    List.range n |>.foldl (fun d i =>
      List.range n |>.foldl (fun d' j =>
        match d'.get i k, d'.get k j, d'.get i j with
        | some dik, some dkj, some dij =>
          if dik + dkj < dij then d'.set i j (dik + dkj) else d'
        | _, _, _ => d'
      ) d
    ) dist
  ) withEdges

end Corpus.Advanced
