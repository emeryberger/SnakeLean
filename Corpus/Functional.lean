/-
Functional programming patterns for testing Python extraction.
-/

namespace Corpus.Functional

-- Identity and composition

def id (x : α) : α := x

def const (x : α) (y : β) : α := x

def flip (f : α → β → γ) (y : β) (x : α) : γ := f x y

def compose (f : β → γ) (g : α → β) (x : α) : γ := f (g x)

def pipe (x : α) (f : α → β) : β := f x

def apply (f : α → β) (x : α) : β := f x

-- Currying

def curry (f : α × β → γ) (x : α) (y : β) : γ := f (x, y)

def uncurry (f : α → β → γ) (p : α × β) : γ := f p.1 p.2

-- Option operations

def Option.map (f : α → β) : Option α → Option β
  | none => none
  | some x => some (f x)

def Option.bind (x : Option α) (f : α → Option β) : Option β :=
  match x with
  | none => none
  | some a => f a

def Option.filter (p : α → Bool) : Option α → Option α
  | none => none
  | some x => if p x then some x else none

def Option.getOrElse (x : Option α) (default : α) : α :=
  match x with
  | none => default
  | some a => a

def Option.orElse (x y : Option α) : Option α :=
  match x with
  | some a => some a
  | none => y

def Option.zip (x : Option α) (y : Option β) : Option (α × β) :=
  match x, y with
  | some a, some b => some (a, b)
  | _, _ => none

def Option.traverse (f : α → Option β) (xs : List α) : Option (List β) :=
  match xs with
  | [] => some []
  | x :: xs' =>
    match f x with
    | none => none
    | some y =>
      match Option.traverse f xs' with
      | none => none
      | some ys => some (y :: ys)

def Option.sequence (xs : List (Option α)) : Option (List α) :=
  Option.traverse id xs

-- List operations

def List.head? (xs : List α) : Option α :=
  match xs with
  | [] => none
  | x :: _ => some x

def List.tail? (xs : List α) : Option (List α) :=
  match xs with
  | [] => none
  | _ :: xs' => some xs'

def List.last? (xs : List α) : Option α :=
  match xs with
  | [] => none
  | [x] => some x
  | _ :: xs' => List.last? xs'

def List.init? (xs : List α) : Option (List α) :=
  match xs with
  | [] => none
  | [_] => some []
  | x :: xs' =>
    match List.init? xs' with
    | none => none
    | some ys => some (x :: ys)

def List.nth (xs : List α) (n : Nat) : Option α :=
  match xs, n with
  | [], _ => none
  | x :: _, 0 => some x
  | _ :: xs', n' + 1 => List.nth xs' n'

def List.updateAt (xs : List α) (n : Nat) (f : α → α) : List α :=
  match xs, n with
  | [], _ => []
  | x :: xs', 0 => f x :: xs'
  | x :: xs', n' + 1 => x :: List.updateAt xs' n' f

def List.insertAt (xs : List α) (n : Nat) (x : α) : List α :=
  match xs, n with
  | xs, 0 => x :: xs
  | [], _ => [x]
  | y :: ys, n' + 1 => y :: List.insertAt ys n' x

def List.removeAt (xs : List α) (n : Nat) : List α :=
  match xs, n with
  | [], _ => []
  | _ :: xs', 0 => xs'
  | x :: xs', n' + 1 => x :: List.removeAt xs' n'

def List.splitAt (n : Nat) (xs : List α) : List α × List α :=
  match n, xs with
  | 0, xs => ([], xs)
  | _, [] => ([], [])
  | n' + 1, x :: xs' =>
    let (l, r) := List.splitAt n' xs'
    (x :: l, r)

def List.takeWhile (p : α → Bool) (xs : List α) : List α :=
  match xs with
  | [] => []
  | x :: xs' => if p x then x :: List.takeWhile p xs' else []

def List.dropWhile (p : α → Bool) (xs : List α) : List α :=
  match xs with
  | [] => []
  | x :: xs' => if p x then List.dropWhile p xs' else x :: xs'

def List.span (p : α → Bool) (xs : List α) : List α × List α :=
  (List.takeWhile p xs, List.dropWhile p xs)

def List.break_ (p : α → Bool) (xs : List α) : List α × List α :=
  List.span (fun x => !p x) xs

def List.replicate (n : Nat) (x : α) : List α :=
  match n with
  | 0 => []
  | n' + 1 => x :: List.replicate n' x

def List.iterate (f : α → α) (x : α) (n : Nat) : List α :=
  match n with
  | 0 => []
  | n' + 1 => x :: List.iterate f (f x) n'

def List.scanl (f : β → α → β) (init : β) (xs : List α) : List β :=
  init :: match xs with
  | [] => []
  | x :: xs' => List.scanl f (f init x) xs'

def List.scanr (f : α → β → β) (init : β) (xs : List α) : List β :=
  match xs with
  | [] => [init]
  | x :: xs' =>
    match List.scanr f init xs' with
    | [] => [init]
    | ys@(y :: _) => f x y :: ys

def List.mapAccum (f : σ → α → σ × β) (init : σ) (xs : List α) : σ × List β :=
  match xs with
  | [] => (init, [])
  | x :: xs' =>
    let (s', y) := f init x
    let (s'', ys) := List.mapAccum f s' xs'
    (s'', y :: ys)

def List.interleave (xs ys : List α) : List α :=
  match xs, ys with
  | [], ys => ys
  | xs, [] => xs
  | x :: xs', y :: ys' => x :: y :: List.interleave xs' ys'

partial def List.transpose (xss : List (List α)) : List (List α) :=
  match xss with
  | [] => []
  | [] :: _ => []
  | xss =>
    let heads := xss.filterMap List.head?
    let tails := xss.filterMap List.tail?
    if heads.isEmpty then [] else heads :: List.transpose tails

def List.subsequences (xs : List α) : List (List α) :=
  match xs with
  | [] => [[]]
  | x :: xs' =>
    let subs := List.subsequences xs'
    subs ++ subs.map (x :: ·)

def List.permutations (xs : List α) : List (List α) :=
  match xs with
  | [] => [[]]
  | x :: xs' =>
    let perms := List.permutations xs'
    perms.flatMap fun perm =>
      (List.range (perm.length + 1)).map fun i =>
        let (l, r) := perm.splitAt i
        l ++ [x] ++ r

-- Either type

inductive Either (α β : Type) where
  | left : α → Either α β
  | right : β → Either α β
  deriving Repr

def Either.map (f : β → γ) : Either α β → Either α γ
  | .left a => .left a
  | .right b => .right (f b)

def Either.mapLeft (f : α → γ) : Either α β → Either γ β
  | .left a => .left (f a)
  | .right b => .right b

def Either.bimap (f : α → γ) (g : β → δ) : Either α β → Either γ δ
  | .left a => .left (f a)
  | .right b => .right (g b)

def Either.bind (x : Either α β) (f : β → Either α γ) : Either α γ :=
  match x with
  | .left a => .left a
  | .right b => f b

def Either.isLeft : Either α β → Bool
  | .left _ => true
  | .right _ => false

def Either.isRight : Either α β → Bool
  | .left _ => false
  | .right _ => true

def Either.fromLeft (x : Either α β) (default : α) : α :=
  match x with
  | .left a => a
  | .right _ => default

def Either.fromRight (x : Either α β) (default : β) : β :=
  match x with
  | .left _ => default
  | .right b => b

def Either.lefts (xs : List (Either α β)) : List α :=
  xs.filterMap fun e =>
    match e with
    | .left a => some a
    | .right _ => none

def Either.rights (xs : List (Either α β)) : List β :=
  xs.filterMap fun e =>
    match e with
    | .left _ => none
    | .right b => some b

def Either.partitionEithers (xs : List (Either α β)) : List α × List β :=
  (Either.lefts xs, Either.rights xs)

-- State monad (simple representation)

structure State (σ α : Type) where
  run : σ → α × σ

def State.pure (x : α) : State σ α :=
  ⟨fun s => (x, s)⟩

def State.bind (m : State σ α) (f : α → State σ β) : State σ β :=
  ⟨fun s =>
    let (a, s') := m.run s
    (f a).run s'⟩

def State.get : State σ σ :=
  ⟨fun s => (s, s)⟩

def State.put (s : σ) : State σ Unit :=
  ⟨fun _ => ((), s)⟩

def State.modify (f : σ → σ) : State σ Unit :=
  ⟨fun s => ((), f s)⟩

def State.gets (f : σ → α) : State σ α :=
  ⟨fun s => (f s, s)⟩

def State.eval (m : State σ α) (s : σ) : α :=
  (m.run s).1

def State.exec (m : State σ α) (s : σ) : σ :=
  (m.run s).2

-- Reader monad

structure Reader (ρ α : Type) where
  run : ρ → α

def Reader.pure (x : α) : Reader ρ α :=
  ⟨fun _ => x⟩

def Reader.bind (m : Reader ρ α) (f : α → Reader ρ β) : Reader ρ β :=
  ⟨fun r => (f (m.run r)).run r⟩

def Reader.ask : Reader ρ ρ :=
  ⟨fun r => r⟩

def Reader.asks (f : ρ → α) : Reader ρ α :=
  ⟨fun r => f r⟩

def Reader.local (f : ρ → ρ) (m : Reader ρ α) : Reader ρ α :=
  ⟨fun r => m.run (f r)⟩

-- Writer monad (for List logs)

structure Writer (α : Type) where
  run : α × List String

def Writer.pure (x : α) : Writer α :=
  ⟨(x, [])⟩

def Writer.bind (m : Writer α) (f : α → Writer β) : Writer β :=
  let (a, w1) := m.run
  let (b, w2) := (f a).run
  ⟨(b, w1 ++ w2)⟩

def Writer.tell (msg : String) : Writer Unit :=
  ⟨((), [msg])⟩

def Writer.listen (m : Writer α) : Writer (α × List String) :=
  let (a, w) := m.run
  ⟨((a, w), w)⟩

end Corpus.Functional
