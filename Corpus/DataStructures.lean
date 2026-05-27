/-
Data structure implementations for testing Python extraction.
-/

namespace Corpus.DataStructures

-- Stack (using List)

structure Stack (α : Type) where
  items : List α
  deriving Repr

def Stack.empty : Stack α := ⟨[]⟩

def Stack.push (s : Stack α) (x : α) : Stack α :=
  ⟨x :: s.items⟩

def Stack.pop (s : Stack α) : Option (α × Stack α) :=
  match s.items with
  | [] => none
  | x :: xs => some (x, ⟨xs⟩)

def Stack.peek (s : Stack α) : Option α :=
  s.items.head?

def Stack.isEmpty (s : Stack α) : Bool :=
  s.items.isEmpty

def Stack.size (s : Stack α) : Nat :=
  s.items.length

-- Queue (using two lists)

structure Queue (α : Type) where
  front : List α
  back : List α
  deriving Repr

def Queue.empty : Queue α := ⟨[], []⟩

def Queue.enqueue (q : Queue α) (x : α) : Queue α :=
  ⟨q.front, x :: q.back⟩

def Queue.dequeue (q : Queue α) : Option (α × Queue α) :=
  match q.front with
  | x :: xs => some (x, ⟨xs, q.back⟩)
  | [] =>
    match q.back.reverse with
    | [] => none
    | x :: xs => some (x, ⟨xs, []⟩)

def Queue.isEmpty (q : Queue α) : Bool :=
  q.front.isEmpty && q.back.isEmpty

def Queue.size (q : Queue α) : Nat :=
  q.front.length + q.back.length

-- Binary Tree

inductive BinaryTree (α : Type) where
  | empty : BinaryTree α
  | node : α → BinaryTree α → BinaryTree α → BinaryTree α
  deriving Repr

def BinaryTree.singleton (x : α) : BinaryTree α :=
  .node x .empty .empty

def BinaryTree.insert [Ord α] (t : BinaryTree α) (x : α) : BinaryTree α :=
  match t with
  | .empty => .singleton x
  | .node v l r =>
    match compare x v with
    | .lt => .node v (l.insert x) r
    | .eq => t
    | .gt => .node v l (r.insert x)

def BinaryTree.contains [Ord α] (t : BinaryTree α) (x : α) : Bool :=
  match t with
  | .empty => false
  | .node v l r =>
    match compare x v with
    | .lt => l.contains x
    | .eq => true
    | .gt => r.contains x

def BinaryTree.size (t : BinaryTree α) : Nat :=
  match t with
  | .empty => 0
  | .node _ l r => 1 + l.size + r.size

def BinaryTree.height (t : BinaryTree α) : Nat :=
  match t with
  | .empty => 0
  | .node _ l r => 1 + max l.height r.height

def BinaryTree.inorder (t : BinaryTree α) : List α :=
  match t with
  | .empty => []
  | .node v l r => l.inorder ++ [v] ++ r.inorder

def BinaryTree.preorder (t : BinaryTree α) : List α :=
  match t with
  | .empty => []
  | .node v l r => [v] ++ l.preorder ++ r.preorder

def BinaryTree.postorder (t : BinaryTree α) : List α :=
  match t with
  | .empty => []
  | .node v l r => l.postorder ++ r.postorder ++ [v]

def BinaryTree.levelOrder (t : BinaryTree α) : List α :=
  let rec go (queue : List (BinaryTree α)) (acc : List α) (fuel : Nat) : List α :=
    match fuel with
    | 0 => acc.reverse
    | fuel' + 1 =>
      match queue with
      | [] => acc.reverse
      | .empty :: rest => go rest acc fuel'
      | .node v l r :: rest => go (rest ++ [l, r]) (v :: acc) fuel'
  go [t] [] 10000

def BinaryTree.mirror (t : BinaryTree α) : BinaryTree α :=
  match t with
  | .empty => .empty
  | .node v l r => .node v r.mirror l.mirror

def BinaryTree.map (f : α → β) (t : BinaryTree α) : BinaryTree β :=
  match t with
  | .empty => .empty
  | .node v l r => .node (f v) (l.map f) (r.map f)

def BinaryTree.fold (f : β → α → β) (init : β) (t : BinaryTree α) : β :=
  match t with
  | .empty => init
  | .node v l r => r.fold f (f (l.fold f init) v)

-- Heap (min-heap using list representation)

def Heap.parent (i : Nat) : Nat := (i - 1) / 2
def Heap.leftChild (i : Nat) : Nat := 2 * i + 1
def Heap.rightChild (i : Nat) : Nat := 2 * i + 2

structure MinHeap (α : Type) [Ord α] where
  data : Array α
  deriving Repr

def MinHeap.empty [Ord α] : MinHeap α := ⟨#[]⟩

def MinHeap.size [Ord α] (h : MinHeap α) : Nat := h.data.size

def MinHeap.isEmpty [Ord α] (h : MinHeap α) : Bool := h.data.isEmpty

def MinHeap.peek [Ord α] (h : MinHeap α) : Option α := h.data[0]?

-- Association List (simple key-value store)

def AssocList (κ ν : Type) := List (κ × ν)

def AssocList.empty : AssocList κ ν := []

def AssocList.insert [BEq κ] (m : AssocList κ ν) (k : κ) (v : ν) : AssocList κ ν :=
  (k, v) :: m.filter (fun (k', _) => k' != k)

def AssocList.lookup [BEq κ] (m : AssocList κ ν) (k : κ) : Option ν :=
  match m with
  | [] => none
  | (k', v) :: rest => if k == k' then some v else rest.lookup k

def AssocList.remove [BEq κ] (m : AssocList κ ν) (k : κ) : AssocList κ ν :=
  m.filter (fun (k', _) => k' != k)

def AssocList.keys (m : AssocList κ ν) : List κ :=
  m.map Prod.fst

def AssocList.values (m : AssocList κ ν) : List ν :=
  m.map Prod.snd

def AssocList.size (m : AssocList κ ν) : Nat :=
  m.length

-- Graph (adjacency list representation)

structure Graph (ν : Type) where
  vertices : List ν
  edges : List (ν × ν)
  deriving Repr

def Graph.empty : Graph ν := ⟨[], []⟩

def Graph.addVertex [BEq ν] (g : Graph ν) (v : ν) : Graph ν :=
  if g.vertices.contains v then g
  else ⟨v :: g.vertices, g.edges⟩

def Graph.addEdge [BEq ν] (g : Graph ν) (u v : ν) : Graph ν :=
  let g' := g.addVertex u |>.addVertex v
  ⟨g'.vertices, (u, v) :: g'.edges⟩

def Graph.neighbors [BEq ν] (g : Graph ν) (v : ν) : List ν :=
  g.edges.filterMap fun (u, w) =>
    if u == v then some w
    else if w == v then some u
    else none

def Graph.degree [BEq ν] (g : Graph ν) (v : ν) : Nat :=
  (g.neighbors v).length

def Graph.hasEdge [BEq ν] (g : Graph ν) (u v : ν) : Bool :=
  g.edges.any fun (a, b) => (a == u && b == v) || (a == v && b == u)

-- Trie (for strings)

inductive Trie where
  | node : Bool → List (Char × Trie) → Trie
  deriving Repr

def Trie.empty : Trie := .node false []

def Trie.insert (t : Trie) (s : String) : Trie :=
  let rec go (t : Trie) (chars : List Char) : Trie :=
    match t, chars with
    | .node isEnd children, [] => .node true children
    | .node isEnd children, c :: cs =>
      let newChildren := match children.find? (fun (ch, _) => ch == c) with
        | some (_, child) =>
          children.map fun (ch, t') =>
            if ch == c then (ch, go t' cs) else (ch, t')
        | none =>
          (c, go .empty cs) :: children
      .node isEnd newChildren
  go t s.toList

def Trie.contains (t : Trie) (s : String) : Bool :=
  let rec go (t : Trie) (chars : List Char) : Bool :=
    match t, chars with
    | .node isEnd _, [] => isEnd
    | .node _ children, c :: cs =>
      match children.find? (fun (ch, _) => ch == c) with
      | some (_, child) => go child cs
      | none => false
  go t s.toList

def Trie.hasPrefix (t : Trie) (pfx : String) : Bool :=
  let rec go (t : Trie) (chars : List Char) : Bool :=
    match t, chars with
    | _, [] => true
    | .node _ children, c :: cs =>
      match children.find? (fun (ch, _) => ch == c) with
      | some (_, child) => go child cs
      | none => false
  go t pfx.toList

end Corpus.DataStructures
