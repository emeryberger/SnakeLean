/-
String manipulation functions for testing Python extraction.
-/

namespace Corpus.Strings

-- Basic operations

def isEmpty (s : String) : Bool := s.length == 0

def isNotEmpty (s : String) : Bool := s.length > 0

def head (s : String) : Option Char := s.toList.head?

def tail (s : String) : String :=
  match s.toList with
  | [] => ""
  | _ :: cs => String.mk cs

def last (s : String) : Option Char := s.toList.getLast?

def init (s : String) : String :=
  String.mk (s.toList.dropLast)

def take (n : Nat) (s : String) : String :=
  String.mk (s.toList.take n)

def drop (n : Nat) (s : String) : String :=
  String.mk (s.toList.drop n)

def charAt (s : String) (i : Nat) : Option Char :=
  s.toList[i]?

def substring (s : String) (start len : Nat) : String :=
  String.mk (s.toList.drop start |>.take len)

def slice (s : String) (start stop : Nat) : String :=
  substring s start (stop - start)

-- Concatenation

def append (s1 s2 : String) : String := s1 ++ s2

def concat (ss : List String) : String :=
  ss.foldl (· ++ ·) ""

def intercalate (sep : String) (ss : List String) : String :=
  match ss with
  | [] => ""
  | [s] => s
  | s :: rest => s ++ sep ++ intercalate sep rest

def join (ss : List String) : String := concat ss

def replicate (n : Nat) (s : String) : String :=
  let rec go (n : Nat) (acc : String) : String :=
    match n with
    | 0 => acc
    | n' + 1 => go n' (acc ++ s)
  go n ""

-- Transformations

def reverse (s : String) : String :=
  String.mk s.toList.reverse

def toUpper (s : String) : String :=
  String.mk (s.toList.map Char.toUpper)

def toLower (s : String) : String :=
  String.mk (s.toList.map Char.toLower)

def capitalize (s : String) : String :=
  match s.toList with
  | [] => ""
  | c :: cs => String.mk (c.toUpper :: cs)

def title (s : String) : String :=
  let rec go (chars : List Char) (capitalize : Bool) : List Char :=
    match chars with
    | [] => []
    | c :: cs =>
      if c == ' ' then c :: go cs true
      else if capitalize then c.toUpper :: go cs false
      else c :: go cs false
  String.mk (go s.toList true)

def swapCase (s : String) : String :=
  String.mk (s.toList.map fun c =>
    if c.isUpper then c.toLower
    else if c.isLower then c.toUpper
    else c)

-- Trimming

def trimLeft (s : String) : String :=
  String.mk (s.toList.dropWhile (· == ' '))

def trimRight (s : String) : String :=
  String.mk (s.toList.reverse.dropWhile (· == ' ')).reverse

def trim (s : String) : String :=
  trimRight (trimLeft s)

def strip (chars : List Char) (s : String) : String :=
  String.mk (s.toList.filter (fun c => !chars.contains c))

-- Padding

def padLeft (n : Nat) (c : Char) (s : String) : String :=
  if s.length >= n then s
  else String.mk (List.replicate (n - s.length) c) ++ s

def padRight (n : Nat) (c : Char) (s : String) : String :=
  if s.length >= n then s
  else s ++ String.mk (List.replicate (n - s.length) c)

def center (n : Nat) (c : Char) (s : String) : String :=
  if s.length >= n then s
  else
    let padding := n - s.length
    let leftPad := padding / 2
    let rightPad := padding - leftPad
    String.mk (List.replicate leftPad c) ++ s ++ String.mk (List.replicate rightPad c)

-- Searching

def contains (s sub : String) : Bool :=
  let rec go (chars : List Char) : Bool :=
    match chars with
    | [] => sub.length == 0
    | c :: cs =>
      if (String.mk (c :: cs)).startsWith sub then true
      else go cs
  go s.toList

def indexOf (s sub : String) : Option Nat :=
  let rec go (chars : List Char) (idx : Nat) : Option Nat :=
    match chars with
    | [] => if sub.length == 0 then some idx else none
    | c :: cs =>
      if (String.mk (c :: cs)).startsWith sub then some idx
      else go cs (idx + 1)
  go s.toList 0

def lastIndexOf (s sub : String) : Option Nat :=
  let rec go (chars : List Char) (idx : Nat) (last : Option Nat) : Option Nat :=
    match chars with
    | [] => if sub.length == 0 then some idx else last
    | c :: cs =>
      if (String.mk (c :: cs)).startsWith sub then go cs (idx + 1) (some idx)
      else go cs (idx + 1) last
  go s.toList 0 none

def count (s sub : String) : Nat :=
  let rec go (chars : List Char) (cnt : Nat) : Nat :=
    match chars with
    | [] => cnt
    | c :: cs =>
      if (String.mk (c :: cs)).startsWith sub then go cs (cnt + 1)
      else go cs cnt
  go s.toList 0

def countChar (c : Char) (s : String) : Nat :=
  s.toList.foldl (fun acc x => if x == c then acc + 1 else acc) 0

-- Predicates

def startsWith (s pfx : String) : Bool :=
  s.toList.take pfx.length == pfx.toList

def endsWith (s suffix : String) : Bool :=
  s.toList.reverse.take suffix.length == suffix.toList.reverse

def isPalindrome (s : String) : Bool :=
  let chars := s.toList.filter (fun c => c.isAlpha || c.isDigit) |>.map Char.toLower
  chars == chars.reverse

def isDigits (s : String) : Bool :=
  !s.isEmpty && s.toList.all Char.isDigit

def isAlpha (s : String) : Bool :=
  !s.isEmpty && s.toList.all Char.isAlpha

def isAlphaNum (s : String) : Bool :=
  !s.isEmpty && s.toList.all (fun c => c.isAlpha || c.isDigit)

def isSpace (s : String) : Bool :=
  !s.isEmpty && s.toList.all (· == ' ')

def isUpper (s : String) : Bool :=
  !s.isEmpty && s.toList.all (fun c => !c.isAlpha || c.isUpper)

def isLower (s : String) : Bool :=
  !s.isEmpty && s.toList.all (fun c => !c.isAlpha || c.isLower)

-- Splitting

partial def splitOn (s sep : String) : List String :=
  if sep.isEmpty then [s]
  else
    let rec go (chars : List Char) (current : List Char) (acc : List String) : List String :=
      match chars with
      | [] => (String.mk current.reverse :: acc).reverse
      | cs =>
        if (String.mk cs).startsWith sep then
          go (cs.drop sep.length) [] (String.mk current.reverse :: acc)
        else
          match cs with
          | c :: cs' => go cs' (c :: current) acc
          | [] => acc.reverse
    go s.toList [] []

def lines (s : String) : List String :=
  splitOn s "\n"

def words (s : String) : List String :=
  let rec go (chars : List Char) (current : List Char) (acc : List String) : List String :=
    match chars with
    | [] =>
      if current.isEmpty then acc.reverse
      else (String.mk current.reverse :: acc).reverse
    | c :: cs =>
      if c == ' ' then
        if current.isEmpty then go cs [] acc
        else go cs [] (String.mk current.reverse :: acc)
      else go cs (c :: current) acc
  go s.toList [] []

def unlines (ss : List String) : String :=
  intercalate "\n" ss

def unwords (ss : List String) : String :=
  intercalate " " ss

-- Replacement

def replace (s old new : String) : String :=
  intercalate new (splitOn s old)

def replaceFirst (s old new : String) : String :=
  match indexOf s old with
  | none => s
  | some i =>
    take i s ++ new ++ drop (i + old.length) s

def removePrefix (pfx s : String) : String :=
  if startsWith s pfx then drop pfx.length s else s

def removeSuffix (suffix s : String) : String :=
  if endsWith s suffix then take (s.length - suffix.length) s else s

-- Character operations

def toCharList (s : String) : List Char := s.toList

def fromCharList (cs : List Char) : String := String.mk cs

def filterChars (p : Char → Bool) (s : String) : String :=
  String.mk (s.toList.filter p)

def mapChars (f : Char → Char) (s : String) : String :=
  String.mk (s.toList.map f)

def zipChars (s1 s2 : String) : List (Char × Char) :=
  s1.toList.zip s2.toList

-- Encoding (simple)

def ord (c : Char) : Nat := c.toNat

def chr (n : Nat) : Char := Char.ofNat n

def toAsciiCodes (s : String) : List Nat :=
  s.toList.map Char.toNat

def fromAsciiCodes (ns : List Nat) : String :=
  String.mk (ns.map Char.ofNat)

-- Distance (Levenshtein - simplified using dynamic programming)

def editDistance (s1 s2 : String) : Nat :=
  let chars1 := s1.toList
  let chars2 := s2.toList
  let n := chars1.length
  let m := chars2.length
  if n == 0 then m
  else if m == 0 then n
  else
    -- Simple recursive definition with memoization limit
    let rec dist (i j : Nat) (fuel : Nat) : Nat :=
      match fuel with
      | 0 => i + j
      | fuel' + 1 =>
        if i == 0 then j
        else if j == 0 then i
        else
          let cost := if chars1[i - 1]? == chars2[j - 1]? then 0 else 1
          let d1 := dist (i - 1) j fuel' + 1
          let d2 := dist i (j - 1) fuel' + 1
          let d3 := dist (i - 1) (j - 1) fuel' + cost
          min d1 (min d2 d3)
    dist n m (n + m + 1)

end Corpus.Strings
