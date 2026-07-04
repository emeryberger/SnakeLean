/-
Parser combinator implementations for testing Python extraction.
-/

namespace Corpus.Parsers

-- Simple parser type

structure ParseResult (α : Type) where
  value : Option α
  remaining : String
  deriving Repr

structure Parser (α : Type) where
  run : String → ParseResult α

instance : Inhabited (Parser α) where
  default := ⟨fun s => { value := none, remaining := s }⟩

-- Basic parsers

def pure (x : α) : Parser α :=
  ⟨fun s => { value := some x, remaining := s }⟩

def fail : Parser α :=
  ⟨fun s => { value := none, remaining := s }⟩

def anyChar : Parser Char :=
  ⟨fun s =>
    match s.toList with
    | [] => { value := none, remaining := s }
    | c :: cs => { value := some c, remaining := String.mk cs }⟩

def satisfy (p : Char → Bool) : Parser Char :=
  ⟨fun s =>
    match s.toList with
    | [] => { value := none, remaining := s }
    | c :: cs =>
      if p c then { value := some c, remaining := String.mk cs }
      else { value := none, remaining := s }⟩

def char (c : Char) : Parser Char :=
  satisfy (· == c)

def string (target : String) : Parser String :=
  ⟨fun s =>
    if s.startsWith target then
      { value := some target, remaining := (s.drop target.length).toString }
    else
      { value := none, remaining := s }⟩

def digit : Parser Char := satisfy Char.isDigit

def letter : Parser Char := satisfy Char.isAlpha

def alphaNum : Parser Char := satisfy fun c => c.isAlpha || c.isDigit

def space : Parser Char := satisfy (· == ' ')

def whitespace : Parser Char := satisfy fun c => c == ' ' || c == '\n' || c == '\t'

-- Combinators

def map (f : α → β) (p : Parser α) : Parser β :=
  ⟨fun s =>
    let result := p.run s
    { value := result.value.map f, remaining := result.remaining }⟩

def bind (p : Parser α) (f : α → Parser β) : Parser β :=
  ⟨fun s =>
    let result := p.run s
    match result.value with
    | none => { value := none, remaining := result.remaining }
    | some a => (f a).run result.remaining⟩

def seq (p1 : Parser α) (p2 : Parser β) : Parser β :=
  bind p1 (fun _ => p2)

def seqLeft (p1 : Parser α) (p2 : Parser β) : Parser α :=
  bind p1 (fun a => map (fun _ => a) p2)

def or (p1 p2 : Parser α) : Parser α :=
  ⟨fun s =>
    let result := p1.run s
    match result.value with
    | some _ => result
    | none => p2.run s⟩

def option (default : α) (p : Parser α) : Parser α :=
  or p (pure default)

def optional (p : Parser α) : Parser (Option α) :=
  or (map some p) (pure none)

def many (p : Parser α) : Parser (List α) :=
  ⟨fun s =>
    let rec go (s : String) (acc : List α) (fuel : Nat) : ParseResult (List α) :=
      match fuel with
      | 0 => { value := some acc.reverse, remaining := s }
      | fuel' + 1 =>
        let result := p.run s
        match result.value with
        | none => { value := some acc.reverse, remaining := s }
        | some a => go result.remaining (a :: acc) fuel'
    go s [] 10000⟩

def many1 (p : Parser α) : Parser (List α) :=
  bind p (fun x => map (x :: ·) (many p))

def sepBy (p : Parser α) (sep : Parser β) : Parser (List α) :=
  or (sepBy1 p sep) (pure [])
where
  sepBy1 (p : Parser α) (sep : Parser β) : Parser (List α) :=
    bind p (fun x => map (x :: ·) (many (seq sep p)))

def between (open_ : Parser β) (close : Parser γ) (p : Parser α) : Parser α :=
  seqLeft (seq open_ p) close

def chainl1 (p : Parser α) (op : Parser (α → α → α)) : Parser α :=
  ⟨fun s =>
    let rec go (acc : α) (s : String) (fuel : Nat) : ParseResult α :=
      match fuel with
      | 0 => { value := some acc, remaining := s }
      | fuel' + 1 =>
        let opResult := op.run s
        match opResult.value with
        | none => { value := some acc, remaining := s }
        | some f =>
          let argResult := p.run opResult.remaining
          match argResult.value with
          | none => { value := some acc, remaining := s }
          | some b => go (f acc b) argResult.remaining fuel'
    let first := p.run s
    match first.value with
    | none => { value := none, remaining := s }
    | some a => go a first.remaining 10000⟩

-- Useful parsers

def spaces : Parser String :=
  map String.mk (many space)

def spaces1 : Parser String :=
  map String.mk (many1 space)

def token (p : Parser α) : Parser α :=
  seqLeft p spaces

def symbol (s : String) : Parser String :=
  token (string s)

def natural : Parser Nat :=
  map (fun ds => ds.foldl (fun acc d => acc * 10 + (d.toNat - '0'.toNat)) 0) (many1 digit)

def integer : Parser Int :=
  bind (optional (char '-')) fun sign =>
    map (fun n : Nat => if sign.isSome then -(n : Int) else (n : Int)) natural

def identifier : Parser String :=
  bind letter fun c =>
    map (fun cs => String.mk (c :: cs)) (many alphaNum)

def quotedString : Parser String :=
  between (char '"') (char '"') (map String.mk (many (satisfy (· != '"'))))

-- Expression parser example

inductive Expr where
  | num : Int → Expr
  | add : Expr → Expr → Expr
  | sub : Expr → Expr → Expr
  | mul : Expr → Expr → Expr
  | div : Expr → Expr → Expr
  | neg : Expr → Expr
  | var : String → Expr
  deriving Repr

partial def parseExpr : Unit → Parser Expr := fun () =>
  let addOp := or (map (fun _ => Expr.add) (symbol "+"))
                  (map (fun _ => Expr.sub) (symbol "-"))
  let mulOp := or (map (fun _ => Expr.mul) (symbol "*"))
                  (map (fun _ => Expr.div) (symbol "/"))
  let atom := or (map Expr.num (token integer))
                 (or (map Expr.var (token identifier))
                     (between (symbol "(") (symbol ")") (parseExpr ())))
  let factor := or (bind (symbol "-") (fun _ => map Expr.neg atom)) atom
  let term := chainl1 factor mulOp
  chainl1 term addOp

def eval (env : String → Option Int) : Expr → Option Int
  | .num n => some n
  | .add e1 e2 => do
      let v1 ← eval env e1
      let v2 ← eval env e2
      some (v1 + v2)
  | .sub e1 e2 => do
      let v1 ← eval env e1
      let v2 ← eval env e2
      some (v1 - v2)
  | .mul e1 e2 => do
      let v1 ← eval env e1
      let v2 ← eval env e2
      some (v1 * v2)
  | .div e1 e2 => do
      let v1 ← eval env e1
      let v2 ← eval env e2
      if v2 == 0 then none else some (v1 / v2)
  | .neg e => do
      let v ← eval env e
      some (-v)
  | .var x => env x

-- JSON-like parser

inductive JsonValue where
  | null : JsonValue
  | bool : Bool → JsonValue
  | num : Int → JsonValue
  | str : String → JsonValue
  | arr : List JsonValue → JsonValue
  | obj : List (String × JsonValue) → JsonValue
  deriving Repr

partial def parseJson : Unit → Parser JsonValue := fun () =>
  let ws := many whitespace
  let jNull := map (fun _ => JsonValue.null) (string "null")
  let jBool := or (map (fun _ => JsonValue.bool true) (string "true"))
                  (map (fun _ => JsonValue.bool false) (string "false"))
  let jNum := map JsonValue.num integer
  let jStr := map JsonValue.str quotedString
  let jArr := between (seq (char '[') ws) (char ']')
                (sepBy (seq ws (parseJson ())) (seq ws (char ',')))
              |> map JsonValue.arr
  let keyVal := bind quotedString fun k =>
                  bind (seq ws (char ':')) fun _ =>
                    bind ws fun _ =>
                      map (k, ·) (parseJson ())
  let jObj := between (seq (char '{') ws) (char '}')
                (sepBy keyVal (seq ws (char ',')))
              |> map JsonValue.obj
  seq ws (or jNull (or jBool (or jNum (or jStr (or jArr jObj)))))

-- CSV parser

def csvField : Parser String :=
  or quotedString (map String.mk (many (satisfy fun c => c != ',' && c != '\n')))

def csvRow : Parser (List String) :=
  sepBy csvField (char ',')

def csv : Parser (List (List String)) :=
  sepBy csvRow (char '\n')

end Corpus.Parsers
