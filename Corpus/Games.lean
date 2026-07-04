/-
Game logic implementations for testing Python extraction.
-/

namespace Corpus.Games

-- Tic-Tac-Toe

inductive Player where
  | X | O
  deriving Repr, BEq

def Player.other : Player → Player
  | .X => .O
  | .O => .X

structure TicTacToe where
  board : List (Option Player)  -- 9 cells, row-major
  currentPlayer : Player
  deriving Repr

def TicTacToe.empty : TicTacToe :=
  { board := List.replicate 9 none, currentPlayer := .X }

def TicTacToe.get (g : TicTacToe) (row col : Nat) : Option Player :=
  match g.board[row * 3 + col]? with
  | some p => p
  | none => none

def TicTacToe.set (g : TicTacToe) (row col : Nat) : Option TicTacToe :=
  let idx := row * 3 + col
  if idx >= 9 then none
  else match g.board[idx]? with
    | some none =>
      some {
        board := g.board.set idx (some g.currentPlayer)
        currentPlayer := g.currentPlayer.other
      }
    | _ => none

def TicTacToe.checkLine (g : TicTacToe) (i1 i2 i3 : Nat) : Option Player :=
  match g.board[i1]?, g.board[i2]?, g.board[i3]? with
  | some (some p1), some (some p2), some (some p3) =>
    if p1 == p2 && p2 == p3 then some p1 else none
  | _, _, _ => none

def TicTacToe.winner (g : TicTacToe) : Option Player :=
  let lines := [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),  -- rows
    (0, 3, 6), (1, 4, 7), (2, 5, 8),  -- cols
    (0, 4, 8), (2, 4, 6)              -- diags
  ]
  lines.findSome? fun (i1, i2, i3) => g.checkLine i1 i2 i3

def TicTacToe.isDraw (g : TicTacToe) : Bool :=
  g.winner.isNone && g.board.all Option.isSome

def TicTacToe.isOver (g : TicTacToe) : Bool :=
  g.winner.isSome || g.isDraw

def TicTacToe.validMoves (g : TicTacToe) : List (Nat × Nat) :=
  if g.isOver then []
  else (List.range 9).filterMap fun i =>
    match g.board[i]? with
    | some none => some (i / 3, i % 3)
    | _ => none

-- Connect Four (simplified)

structure ConnectFour where
  board : List (List (Option Player))  -- 6 rows × 7 columns
  currentPlayer : Player
  deriving Repr

def ConnectFour.empty : ConnectFour :=
  { board := List.replicate 6 (List.replicate 7 none), currentPlayer := .X }

def ConnectFour.columnHeight (g : ConnectFour) (col : Nat) : Nat :=
  let column := g.board.filterMap (·[col]?)
  column.filter Option.isSome |>.length

def ConnectFour.drop (g : ConnectFour) (col : Nat) : Option ConnectFour :=
  if col >= 7 then none
  else
    let height := g.columnHeight col
    if height >= 6 then none
    else
      let row := 5 - height
      let newBoard := g.board.zipIdx.map fun (rowData, r) =>
        if r == row then rowData.set col (some g.currentPlayer)
        else rowData
      some {
        board := newBoard
        currentPlayer := g.currentPlayer.other
      }

def ConnectFour.checkWin (g : ConnectFour) (p : Player) : Bool :=
  -- Check horizontal
  let horizontal := g.board.any fun row =>
    (List.range 4).any fun c =>
      (List.range 4).all fun i =>
        match row[c + i]? with
        | some (some q) => q == p
        | _ => false
  -- Check vertical
  let vertical := (List.range 7).any fun c =>
    (List.range 3).any fun r =>
      (List.range 4).all fun i =>
        match g.board[r + i]? with
        | some row =>
          match row[c]? with
          | some (some q) => q == p
          | _ => false
        | none => false
  horizontal || vertical

-- Nim

structure Nim where
  piles : List Nat
  deriving Repr

def Nim.create (sizes : List Nat) : Nim := { piles := sizes }

def Nim.take (g : Nim) (pile count : Nat) : Option Nim :=
  match g.piles[pile]? with
  | some n =>
    if count > 0 && count <= n then
      some { piles := g.piles.set pile (n - count) }
    else none
  | none => none

def Nim.isOver (g : Nim) : Bool :=
  g.piles.all (· == 0)

def Nim.nimSum (g : Nim) : Nat :=
  g.piles.foldl Nat.xor 0

def Nim.isWinningPosition (g : Nim) : Bool :=
  g.nimSum != 0

-- Blackjack (simplified)

inductive Suit where
  | hearts | diamonds | clubs | spades
  deriving Repr, BEq

inductive Rank where
  | ace | two | three | four | five | six | seven | eight | nine | ten | jack | queen | king
  deriving Repr, BEq

structure Card where
  rank : Rank
  suit : Suit
  deriving Repr

def Card.value (c : Card) : Nat :=
  match c.rank with
  | .ace => 11
  | .two => 2
  | .three => 3
  | .four => 4
  | .five => 5
  | .six => 6
  | .seven => 7
  | .eight => 8
  | .nine => 9
  | .ten | .jack | .queen | .king => 10

def Card.isAce (c : Card) : Bool := c.rank == .ace

structure BlackjackHand where
  cards : List Card
  deriving Repr

def BlackjackHand.empty : BlackjackHand := { cards := [] }

def BlackjackHand.add (h : BlackjackHand) (c : Card) : BlackjackHand :=
  { cards := c :: h.cards }

def BlackjackHand.hardValue (h : BlackjackHand) : Nat :=
  h.cards.foldl (fun acc c => acc + c.value) 0

def BlackjackHand.numAces (h : BlackjackHand) : Nat :=
  h.cards.filter Card.isAce |>.length

def BlackjackHand.bestValue (h : BlackjackHand) : Nat :=
  let hard := h.hardValue
  let rec adjust (value aces : Nat) : Nat :=
    match aces with
    | 0 => value
    | aces' + 1 =>
      if value <= 21 then value
      else adjust (value - 10) aces'
  adjust hard h.numAces

def BlackjackHand.isBust (h : BlackjackHand) : Bool :=
  h.bestValue > 21

def BlackjackHand.isBlackjack (h : BlackjackHand) : Bool :=
  h.cards.length == 2 && h.bestValue == 21

-- Dice

def roll (sides : Nat) (seed : Nat) : Nat :=
  -- Simple LCG for reproducibility
  ((seed * 1103515245 + 12345) % (2^31)) % sides + 1

def rollDice (numDice sides seed : Nat) : List Nat × Nat :=
  let rec go (n seed : Nat) (acc : List Nat) : List Nat × Nat :=
    match n with
    | 0 => (acc.reverse, seed)
    | n' + 1 =>
      let newSeed := (seed * 1103515245 + 12345) % (2^31)
      let value := newSeed % sides + 1
      go n' newSeed (value :: acc)
  go numDice seed []

def sumDice (dice : List Nat) : Nat :=
  dice.foldl (· + ·) 0

-- Scoring

def yahtzeeScore (dice : List Nat) : Nat :=
  if dice.length != 5 then 0
  else
    let sorted := dice.toArray.qsort (· < ·) |>.toList
    let counts := (List.range 6).map fun n =>
      dice.filter (· == n + 1) |>.length
    let maxCount := counts.foldl max 0
    let sumAll := dice.foldl (· + ·) 0
    -- Check for Yahtzee (all same)
    if maxCount == 5 then 50
    -- Check for large straight
    else if sorted == [1, 2, 3, 4, 5] || sorted == [2, 3, 4, 5, 6] then 40
    -- Check for full house
    else if counts.contains 3 && counts.contains 2 then 25
    -- Otherwise sum
    else sumAll

-- Rock Paper Scissors

inductive RPS where
  | rock | paper | scissors
  deriving Repr, BEq

def RPS.beats : RPS → RPS → Bool
  | .rock, .scissors => true
  | .paper, .rock => true
  | .scissors, .paper => true
  | _, _ => false

def RPS.compare (a b : RPS) : Int :=
  if a == b then 0
  else if a.beats b then 1
  else -1

def RPS.fromNat : Nat → Option RPS
  | 0 => some .rock
  | 1 => some .paper
  | 2 => some .scissors
  | _ => none

-- Sudoku validation (simplified)

def isValidSudokuRow (row : List Nat) : Bool :=
  let nonzero := row.filter (· != 0)
  nonzero.length == nonzero.eraseDups.length

def isValidSudokuGrid (grid : List (List Nat)) : Bool :=
  -- Check rows
  let validRows := grid.all isValidSudokuRow
  -- Check columns
  let cols := (List.range 9).map fun c =>
    grid.filterMap fun row => row[c]?
  let validCols := cols.all isValidSudokuRow
  -- Check 3x3 boxes
  let boxes := (List.range 3).flatMap fun br =>
    (List.range 3).map fun bc =>
      (List.range 3).flatMap fun r =>
        (List.range 3).filterMap fun c =>
          match grid[br * 3 + r]? with
          | some row => row[bc * 3 + c]?
          | none => none
  let validBoxes := boxes.all isValidSudokuRow
  validRows && validCols && validBoxes

end Corpus.Games
