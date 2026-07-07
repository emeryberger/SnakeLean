/-
Rust standard-library string functions, ported from the
`model-checking/rust-lean-models` project (Copyright Kani Contributors),
which models Rust's `core`/`std` string API in Lean.

Source: https://github.com/model-checking/rust-lean-models
Original files: RustLeanModels/RustString.lean, RustLeanModels/Basic.lean

Dual-licensed under Apache-2.0 OR MIT (SPDX-License-Identifier: Apache-2.0 OR MIT),
matching the upstream project. See Corpus/RustModels_NOTICE.md for attribution.

Only the computable `def`s are ported (proofs/lemmas/specifications dropped).
Ported to Lean 4.31 for use as a SnakeLean transpiler-fuzzing corpus.
Strings are modelled as `Str = List Char`, as in the upstream project.
-/

namespace Corpus.RustModels

open List Nat Char

abbrev Str := List Char

-- Helper from RustLeanModels.Basic (needed by the substring index functions)
def list_nat_zero_to_aux (m : Nat) (i : Nat) : List Nat := match m with
  | 0 => []
  | Nat.succ t => i :: list_nat_zero_to_aux t (i + 1)

def list_nat_zero_to (m : Nat) : List Nat := list_nat_zero_to_aux m 0

-- Helper from RustLeanModels.Iterator (needed by the `splitn_*_def` functions)
def flatten (s : List (List Char)) : List Char := List.foldl List.append [] s

def is_ascii_whitespace (c : Char) : Bool := c.isWhitespace || (c == '\x0C')

def is_whitespace (c : Char) : Bool :=
  [9, 10, 11, 12, 13, 32, 133, 160, 5760,
   8192, 8193, 8194, 8195, 8196, 8197, 8198, 8199, 8200, 8201, 8202,
   8232, 8233, 8239, 8287, 12288].contains c.val

def Char_is_ascii (c : Char) : Bool := decide (c.val ≤ 127)

def sum_list_Nat (l : List Nat) := List.foldl Nat.add 0 l

def byteSize (s : List Char) : Nat := match s with
  | [] => 0
  | h::t => Char.utf8Size h + byteSize t

def byteSize_aux (s : Str) (k : Nat)  : Nat := match s with
  | [] => k
  | h::t => byteSize_aux t (k + Char.utf8Size h)

def ListCharPos_aux (s: Str) (i: Nat):= match s with
  | [] => []
  | h::t => match t with
            | [] => [i]
            | _::_ => i:: ListCharPos_aux t (i+ Char.utf8Size h)

def ListCharPos (s: Str) := ListCharPos_aux s 0

def CharBoundPos_aux (l: Str) (s: Nat): List Nat := match l with
  | [] => [s]
  | h::t => s :: CharBoundPos_aux t (s + Char.utf8Size h)

def CharBoundPos (s: Str) : List Nat := CharBoundPos_aux s 0

def is_char_boundary (s: Str) (i: Nat) := match s with
  | [] => i == 0
  | h::t => if i = 0 then true else
      if i < Char.utf8Size h then false else is_char_boundary t (i - Char.utf8Size h)

def char_indices_aux (s : Str) (i : Nat): List (Nat × Char) := match s with
  | [] => []
  | h::t => (i, h) :: char_indices_aux t (i + Char.utf8Size h)

def char_indices s := char_indices_aux s 0

def split_at_aux (s: Str) (i: Nat) (ks: Str): Option (List Char × List Char)  := match s with
  | [] => if i = 0 then some (ks, []) else none
  | h::t => if i = 0 then some (ks, h::t) else if i < Char.utf8Size h then none
            else split_at_aux t (i - Char.utf8Size h) (ks++[h])

def split_at (s: Str) (i: Nat) := split_at_aux s i []

def string_slice (s: Str) (p1 p2: Nat):= if p2 < p1 then none else do let (_,s2) ← split_at s p1
                                                                      let (s21, _) ← (split_at s2 (p2-p1))
                                                                      some s21

def PrefixFromPos_safe_r (s: Str) (i: Nat): Str := match s with
  | [] => []
  | h::t => if i = 0 then [] else h::PrefixFromPos_safe_r t (i - Char.utf8Size h)

def PrefixFromPos (s: Str) (i: Nat): Option Str :=
      if is_char_boundary s i then some (PrefixFromPos_safe_r s i) else none

def floor_char_boundary_aux (s: Str) (i: Nat) (k: Nat): Nat := match s with
  | [] => k
  | h::t => if i < Char.utf8Size h then k else floor_char_boundary_aux t (i - Char.utf8Size h) (k + Char.utf8Size h)

def floor_char_boundary (s: Str) (i: Nat) := floor_char_boundary_aux s i 0

def ceiling_char_boundary_aux (s: Str) (i: Nat) (k: Nat): Nat := match s with
  | [] => k
  | h::t =>
      if i = 0 then k else
      if i < Char.utf8Size h then k + Char.utf8Size h else ceiling_char_boundary_aux t (i - Char.utf8Size h) (k + Char.utf8Size h)

def ceiling_char_boundary (s: Str) (i: Nat) := ceiling_char_boundary_aux s i 0

inductive Pattern: Type
  | SingleChar (c: Char)
  | ListChar (l: Str)
  | FilterFunction (f: Char → Bool)
  | WholeString (s: Str)

def contains_substring (s: Str) (ss: Str)  := match s, ss with
  | _ , [] => true
  | [], _ => false
  | _::ts, _ => if List.isPrefixOf ss s then true else contains_substring ts ss

def contains_char_filter  (s: Str) (f: Char → Bool) := match s with
  | [] => false
  | h::t => if f h then true else contains_char_filter t f

def contains (s: Str) (P: Pattern) : Bool := match P with
  | Pattern.SingleChar c => contains_char_filter s (fun x => x == c)
  | Pattern.ListChar l => contains_char_filter s (fun x => l.contains x)
  | Pattern.FilterFunction f => contains_char_filter s f
  | Pattern.WholeString ss => contains_substring s ss

def find_substring_aux (s: Str) (ss: Str) (i: Nat): Option Nat:= match s, ss with
  | _ , [] => some i
  | [], _ => none
  | hs::ts, _ => if List.isPrefixOf ss s then i else find_substring_aux ts ss (i + Char.utf8Size hs)

def find_substring (s: Str) (ss: Str) := find_substring_aux s ss 0

def find_char_filter_aux (s: Str) (f: Char → Bool) (i: Nat) : Option Nat:= match s with
  | [] => none
  | h::t => if f h then some i else find_char_filter_aux t f (i + Char.utf8Size h)

def find_char_filter (s: Str) (f: Char → Bool)  := find_char_filter_aux s f 0

def find (s: Str) (P: Pattern) : Option Nat := match P with
  | Pattern.SingleChar c => find_char_filter s (fun x => x == c)
  | Pattern.ListChar l => find_char_filter s (fun x => l.contains x)
  | Pattern.FilterFunction f => find_char_filter s f
  | Pattern.WholeString ss => find_substring s ss

def rfind_substring (s: Str) (ss: Str) := match find_substring (List.reverse s) (List.reverse ss) with
  | none => none
  | some i => some (byteSize s - byteSize ss -i)

def find_char_filter_next_aux (s: Str) (f: Char → Bool) (i: Nat) : Option Nat:= match s with
  | [] => none
  | h::t => if f h then some (i + Char.utf8Size h) else find_char_filter_next_aux t f (i + Char.utf8Size h)

def find_char_filter_next (s: Str) (f: Char → Bool)  := find_char_filter_next_aux s f 0

def rfind_char_filter (s: Str) (f: Char → Bool)  := match find_char_filter_next (List.reverse s) f with
  | none => none
  | some i => some (byteSize s - i)

def rfind (s: Str) (P: Pattern) : Option Nat := match P with
  | Pattern.SingleChar c => rfind_char_filter s (fun x => x == c)
  | Pattern.ListChar l => rfind_char_filter s (fun x => l.contains x)
  | Pattern.FilterFunction f => rfind_char_filter s f
  | Pattern.WholeString ss => rfind_substring s ss

def charIndex_to_pos (s: Str) (i: Nat)  :=
  if i = 0 then 0 else match s with
  | [] => 0
  | h::t => (Char.utf8Size h) + charIndex_to_pos t (i-1)

def charIndex_to_pos_def (s: Str) (i: Nat)  := byteSize (s.take i)

def substring_charIndex_aux (s: Str) (ss: Str) (i: Nat): Option Nat:= match s, ss with
  | _ , [] => some i
  | [], _ => none
  | _::ts, _ => if List.isPrefixOf ss s then i else substring_charIndex_aux ts ss (i + 1)

def substring_charIndex (s: Str) (ss: Str) := substring_charIndex_aux s ss 0

def list_char_filter_charIndex_aux (s: Str) (f: Char → Bool) (curpos : Nat) : List Nat :=  match s with
  | [] => []
  | h::t => if f h then curpos::list_char_filter_charIndex_aux t f (curpos + 1)
            else list_char_filter_charIndex_aux t f (curpos + 1)

def list_char_filter_charIndex (s: Str) (f: Char → Bool) := list_char_filter_charIndex_aux s f 0

partial def list_substring_charIndex_aux (s: Str) (ss: Str) (curpos : Nat) : List Nat :=
  if _h : ss.length > 0 then
    match _t: substring_charIndex s ss with
      | none => []
      | some i => (curpos + i) :: list_substring_charIndex_aux (s.drop (i + ss.length)) ss (curpos + i + ss.length)
  else list_nat_zero_to s.length

def list_substring_charIndex (s: Str) (ss: Str) := list_substring_charIndex_aux s ss 0

def split_at_charIndex (s: Str) (i: Nat): List Char × List Char  := match s with
  | [] => ([], [])
  | h::t => if i = 0 then ([], s) else  let l := split_at_charIndex t (i-1)
            (h::(l.1), l.2)

def split_at_charIndex_def (s: Str) (i: Nat) := (s.take i, s.drop i)

def split_at_charIndex_list_aux (s: Str) (l: List Nat) (curpos: Nat): List Str := match l with
  | [] => [s]
  | h::t => (split_at_charIndex s (h - curpos)).1 :: split_at_charIndex_list_aux (split_at_charIndex s (h - curpos)).2 t h

def length_list_from_list_charIndex_aux (l: List Nat) (curpos: Nat):= match l with
  | [] => []
  | h::t => (h - curpos)::(length_list_from_list_charIndex_aux t h)

def length_list_from_list_charIndex (l: List Nat) (s: Str) := length_list_from_list_charIndex_aux (l++[s.length]) 0

def list_char_filter_pos_aux (s: Str) (f: Char → Bool) (curpos : Nat) : List Nat :=  match s with
  | [] => []
  | h::t => if f h then curpos::list_char_filter_pos_aux t f (curpos + Char.utf8Size h)
            else list_char_filter_pos_aux t f (curpos + Char.utf8Size h)

def list_char_filter_pos (s: Str) (f: Char → Bool) := list_char_filter_pos_aux s f 0

def list_char_filter_pos_def (s: Str) (f: Char → Bool):= List.map (charIndex_to_pos s) (list_char_filter_charIndex s f)

partial def list_substring_pos_aux (s: Str) (ss: Str) (curpos : Nat) : List Nat :=
  if _h : ss.length > 0 then
    match _t: substring_charIndex s ss with
      | none => []
      | some i => (curpos + (charIndex_to_pos s i)) :: list_substring_pos_aux (s.drop (i + ss.length)) ss (curpos + (charIndex_to_pos s i) + (byteSize ss))
  else list_nat_zero_to s.length

def list_substring_pos (s: Str) (ss: Str) := list_substring_pos_aux s ss 0

def list_substring_pos_def (s: Str) (ss: Str):= List.map (charIndex_to_pos s) (list_substring_charIndex s ss)

def split_inclusive_char_filter_aux (s: Str) (f: Char → Bool) (w: Str) := match s with
  | [] => [w]
  | h::t => if f h then (w++[h])::split_inclusive_char_filter_aux t f []
            else split_inclusive_char_filter_aux t f (w++[h])

def split_inclusive_char_filter (s: Str) (f: Char → Bool) := split_inclusive_char_filter_aux s f []

partial def split_inclusive_substring (s: Str) (ss: Str)  : List Str:=
  if h: ss.length > 0 then
    match _t: substring_charIndex s ss with
      | none =>  [s]
      | some i => (s.take (i + ss.length)) :: split_inclusive_substring (s.drop (i + ss.length)) ss
  else [[]] ++ List.map (fun c => [c]) s

def split_char_filter_aux (s: Str) (f: Char → Bool) (w: Str) := match s with
  | [] => [w]
  | h::t => if f h then w::split_char_filter_aux t f []
            else split_char_filter_aux t f (w++[h])

def split_char_filter (s: Str) (f: Char → Bool) := split_char_filter_aux s f []

def split_char_filter_def (s: Str) (f: Char → Bool) := let si := (split_inclusive_char_filter s f)
                  (List.map (fun x : Str => x.dropLast) si.dropLast) ++ si.drop (si.length - 1)

def split_char_filter_aux_def (s: Str) (f: Char → Bool) (w: Str) := let si := (split_inclusive_char_filter_aux s f w)
                  (List.map (fun x : Str => x.dropLast) si.dropLast) ++ si.drop (si.length - 1)

partial def split_substring (s: Str) (ss: Str)   : List Str:=
  if h: ss.length > 0 then
    match _t: substring_charIndex s ss with
      | none => [s]
      | some i => (s.take i)::split_substring (s.drop (i + ss.length)) ss
  else [[]] ++ List.map (fun c => [c]) s ++ [[]]

def drop_tail (s: Str) (n: Nat) := s.take (s.length - n)

def split_substring_def (s: Str) (ss: Str) :=
  if ss.length > 0 then
    let si := (split_inclusive_substring s ss)
    (List.map (fun x : Str => drop_tail x ss.length) si.dropLast) ++ si.drop (si.length - 1)
  else [[]] ++ List.map (fun c => [c]) s ++ [[]]

def str_concat_pad (l: List Str) (s: Str) := match l with
  | [] => []
  | h::t => match t with | [] => h | _ => h ++ s ++ (str_concat_pad t s)

def split (s: Str) (P: Pattern) := match P with
  | Pattern.SingleChar c => split_char_filter s (fun x => x == c)
  | Pattern.ListChar l => split_char_filter s (fun x => l.contains x)
  | Pattern.FilterFunction f => split_char_filter s f
  | Pattern.WholeString ss => split_substring s ss

def rsplit (s: Str) (P: Pattern) := List.reverse (split s P)

def splitn_char_filter_aux (s: Str) (n: Nat) (f: Char → Bool)  (w: Str)  :=
  if n = 0 then [] else if n = 1 then [w++s] else
    match s with
      | [] => [w]
      | h::t => if f h then w::splitn_char_filter_aux t (n-1) f []
                else splitn_char_filter_aux t n f (w++[h])

def splitn_char_filter (s: Str) (n: Nat) (f: Char → Bool)  := splitn_char_filter_aux s n f []

def splitn_char_filter_def (s: Str) (n: Nat) (f: Char → Bool)  :=
    if n = 0 then [] else
      if (split_char_filter s f).length ≤ n then split_char_filter s f else
      (split_char_filter s f).take (n-1) ++ [flatten ((split_inclusive_char_filter s f).drop (n-1))]

def splitn_char_filter_aux_def (s: Str) (n: Nat) (f: Char → Bool)  (w: Str) :=
      if (split_char_filter_aux s f w).length ≤ n then split_char_filter_aux s f w else
      (split_char_filter_aux s f w).take (n-1) ++ [flatten ((split_inclusive_char_filter_aux s f w).drop (n-1))]

partial def splitn_substring(s: Str) (n: Nat) (ss: Str)   : List Str:=
  if n = 0 then [] else if n=1 then [s] else
        if _h1: ss.length > 0 then
          match _t: substring_charIndex s ss with
            | none => [s]
            | some i => (s.take i)::splitn_substring (s.drop (i + ss.length)) (n-1) ss
        else [[]] ++ List.map (fun c => [c]) (s.take (n-2)) ++ [(s.drop (n-2))]

def splitn_substring_def (s: Str) (n: Nat) (ss: Str)  :=
  if n > 0 then
      if (split_substring s ss).length ≤ n then split_substring s ss else
      (split_substring s ss).take (n-1) ++ [flatten ((split_inclusive_substring s ss).drop (n-1))]
  else []

def splitn (s: Str) (n: Nat) (P: Pattern) := match P with
  | Pattern.SingleChar c => splitn_char_filter s n (fun x => x == c)
  | Pattern.ListChar l => splitn_char_filter s n (fun x => l.contains x)
  | Pattern.FilterFunction f => splitn_char_filter s n f
  | Pattern.WholeString ss => splitn_substring s n ss

def rsplitn_char_filter (s: Str) (f: Char → Bool) (n: Nat) := List.map (fun x: Str => x.reverse) (splitn_char_filter (s.reverse) n f)

def rsplitn_substring (s: Str) (ss: Str) (n: Nat) := List.map (fun x: Str => x.reverse) (splitn_substring (s.reverse) n (ss.reverse))

def rsplitn (s: Str) (P: Pattern) (n: Nat):= match P with
  | Pattern.SingleChar c => rsplitn_char_filter s (fun x => x == c) n
  | Pattern.ListChar l => rsplitn_char_filter s (fun x => l.contains x) n
  | Pattern.FilterFunction f => rsplitn_char_filter s f n
  | Pattern.WholeString ss => rsplitn_substring s ss n

def split_once (s: Str) (P: Pattern)  := splitn s 1 P

def rsplitn_once (s: Str) (P: Pattern)  := rsplitn s P 1

def split_ascii_whitespace_aux (s: Str) (w: Str) (prespace: Bool): List Str := match s with
  | [] => if prespace = false then [w] else []
  | h::t => if is_ascii_whitespace h then
          if prespace = false then w::split_ascii_whitespace_aux t [] true else split_ascii_whitespace_aux t []  true
          else split_ascii_whitespace_aux t (w++[h]) false

def split_ascii_whitespace (s: Str) := split_ascii_whitespace_aux s [] true

def split_ascii_whitespace_def (s: Str) := filter (fun a: Str => a.length > 0) (split_char_filter s is_ascii_whitespace)

def split_whitespace_aux (s: Str) (w: Str) (prespace: Bool): List Str := match s with
  | [] => if prespace = false then [w] else []
  | h::t => if is_whitespace h then
          if prespace = false then w::split_whitespace_aux t [] true else split_whitespace_aux t []  true
          else split_whitespace_aux t (w++[h]) false

def split_whitespace (s: Str) := split_whitespace_aux s [] true

def split_whitespace_def (s: Str) := filter (fun sa: Str => sa.length > 0) (split_char_filter s is_whitespace)

def lines (s: Str) := split s (Pattern.SingleChar '\n')

def matches_char_filter (s: Str) (f: Char → Bool)  := match s with
  | [] => []
  | h::t => if f h then [h]::matches_char_filter t f else matches_char_filter t f

def matches_char_filter_def (s: Str) (f: Char → Bool) := List.map (fun x: Char => [x]) (List.filter f s)

partial def matches_substring (s ss: Str) :=
  if _h: ss = [] then []
  else match _h1: substring_charIndex s ss with
    | none => []
    | some p => ss::(matches_substring (s.drop (p + ss.length)) ss)

def list_Str_repeat (s: Str) (n: Nat) := match n with
  | 0 => []
  | succ m => s:: list_Str_repeat s m

def matches_substring_def (s ss: Str) := list_Str_repeat ss (list_substring_charIndex s ss).length

def rust_matches (s: Str) (P: Pattern) := match P with
  | Pattern.SingleChar c => matches_char_filter s (fun x => x == c)
  | Pattern.ListChar l => matches_char_filter s (fun x => l.contains x)
  | Pattern.FilterFunction f => matches_char_filter s f
  | Pattern.WholeString ss => matches_substring s ss

def rmatches (s: Str) (P: Pattern) := List.reverse (rust_matches s P)

def matches_indices_char_filter_aux (s: Str) (f: Char → Bool) (i: Nat):= match s with
  | [] => []
  | h::t => if f h then (i,[h])::matches_indices_char_filter_aux t f (i + Char.utf8Size h)
                    else  matches_indices_char_filter_aux t f (i + Char.utf8Size h)

def matches_indices_char_filter (s: Str) (f: Char → Bool) := matches_indices_char_filter_aux s f 0

def matches_indices_char_filter_def (s: Str) (f: Char → Bool) := List.zip (list_char_filter_pos s f) (matches_char_filter s f)

partial def matches_indices_substring_aux (s ss: Str) (k: Nat):=
  if _h: ss = [] then []
  else match _h1: substring_charIndex s ss with
    | none => []
    | some i => (k + byteSize (s.take i), ss)::(matches_indices_substring_aux (s.drop (i + ss.length)) ss (k + byteSize (s.take i) + byteSize ss ))

def matches_indices_substring (s ss: Str) := matches_indices_substring_aux s ss 0

def matches_indices_substring_def (s ss: Str) := List.map (fun a => (a, ss)) (list_substring_pos s ss)

def matches_indices (s: Str) (P: Pattern) := match P with
  | Pattern.SingleChar c => matches_indices_char_filter s (fun x => x == c)
  | Pattern.ListChar l => matches_indices_char_filter s (fun x => l.contains x)
  | Pattern.FilterFunction f => matches_indices_char_filter s f
  | Pattern.WholeString ss => matches_indices_substring s ss

def rmatches_indices (s: Str) (P: Pattern) := List.reverse (matches_indices s P)

def starts_with_char_filter (s: Str) (f: Char → Bool) := match s with | [] => false | h::_ => f h

def starts_with (s: Str) (P: Pattern) := match P with
  | Pattern.SingleChar c => starts_with_char_filter s (fun a => a == c)
  | Pattern.ListChar l => starts_with_char_filter s (fun a => l.contains a)
  | Pattern.FilterFunction f => starts_with_char_filter s f
  | Pattern.WholeString ss => List.isPrefixOf ss s

def ends_with_char_filter (s: Str) (f: Char → Bool) := starts_with_char_filter s.reverse f

def ends_with (s: Str) (P: Pattern) := match P with
  | Pattern.SingleChar c => ends_with_char_filter s (fun a => a == c)
  | Pattern.ListChar l => ends_with_char_filter s (fun a => l.contains a)
  | Pattern.FilterFunction f => ends_with_char_filter s f
  | Pattern.WholeString ss => List.isSuffixOf ss s

def split_terminator (s: Str) (P: Pattern) := if ends_with s P then (split s P).dropLast else (split s P)

def rsplit_terminator (s: Str) (P: Pattern) := List.reverse (split_terminator s P)

def rust_repeat (s: Str) (n: Nat) := match n with
  | zero => []
  | succ t => s ++ rust_repeat s t

def trim_start_matches_char_filter (s: Str) (f: Char → Bool):= match s with
  | [] => []
  | h::t => if f h then trim_start_matches_char_filter t f else s

partial def trim_start_matches_substring (s: Str) (ss: Str):=
  if ss.length > 0 then
    if List.isPrefixOf ss s then trim_start_matches_substring (s.drop (ss.length)) ss else s
    else s

def trim_start_matches (s: Str) (P: Pattern) := match P with
  | Pattern.SingleChar c => trim_start_matches_char_filter s (fun a => a == c)
  | Pattern.ListChar l => trim_start_matches_char_filter s (fun a => l.contains a)
  | Pattern.FilterFunction f => trim_start_matches_char_filter s f
  | Pattern.WholeString ss => trim_start_matches_substring s ss

def trim_end_matches_char_filter (s: Str) (f: Char → Bool):= List.reverse (trim_start_matches_char_filter (List.reverse s) f)

def trim_end_matches_substring (s: Str) (ss: Str):= List.reverse (trim_start_matches_substring s.reverse ss.reverse)

def trim_end_matches (s: Str) (P: Pattern) := match P with
  | Pattern.SingleChar c => trim_end_matches_char_filter s (fun a => a == c)
  | Pattern.ListChar l => trim_end_matches_char_filter s (fun a => l.contains a)
  | Pattern.FilterFunction f => trim_end_matches_char_filter s f
  | Pattern.WholeString ss => trim_end_matches_substring s ss

def trim_matches_char_filter (s: Str) (f: Char → Bool):= trim_start_matches_char_filter (trim_end_matches_char_filter s f) f

def trim_matches (s: Str) (P: Pattern) : Option Str := match P with
  | Pattern.SingleChar c => some (trim_matches_char_filter s (fun a => a == c))
  | Pattern.ListChar l => some (trim_matches_char_filter s (fun a => l.contains a))
  | Pattern.FilterFunction f => some (trim_matches_char_filter s f)
  | Pattern.WholeString _ => none

def trim_ascii_start (s: Str) := trim_start_matches_char_filter s is_ascii_whitespace

def trim_ascii_end (s: Str) := trim_end_matches_char_filter s is_ascii_whitespace

def trim_ascii (s: Str) := trim_ascii_start (trim_ascii_end s)

def trim_start (s: Str) := trim_start_matches_char_filter s is_whitespace

def trim_end (s: Str) := trim_end_matches_char_filter s is_whitespace

def trim (s: Str) := trim_start (trim_end s)

partial def replace_substring (s ss sr: Str) :=
  if _h: ss.length > 0 then
    match _t: substring_charIndex s ss with
      | none => s
      | some i => (s.take i) ++ sr ++ (replace_substring (s.drop (i + ss.length)) ss sr)
  else s

def replace_substring_def (s ss sr: Str) := str_concat_pad (split_substring s ss) sr

def replace_char_filter (s: Str) (f: Char → Bool) (ss: Str) := match s with
  | [] => []
  | h::t => if f h then ss ++ (replace_char_filter t f ss) else h::(replace_char_filter t f ss)

def replace_char_filter_def (s: Str) (f: Char → Bool) (ss: Str) := str_concat_pad (split_char_filter s f) ss

def replace (s: Str) (i: Pattern) (sr: Str):= match i with
  | Pattern.SingleChar c => replace_char_filter s (fun x => x == c) sr
  | Pattern.ListChar l => replace_char_filter s (fun x => l.contains x) sr
  | Pattern.FilterFunction f => replace_char_filter s f sr
  | Pattern.WholeString ss => replace_substring s ss sr

partial def replacen_substring (s ss sr: Str) (n: Nat):=
  if _h: ss.length > 0 then
    if n > 0 then
      match _t: substring_charIndex s ss with
        | none => s
        | some i => (s.take i) ++ sr ++ (replacen_substring (s.drop (i + ss.length)) ss sr (n-1))
    else s
  else s

def replacen_substring_def (s ss sr: Str) (n:Nat):= str_concat_pad (splitn_substring s (n+1) ss ) sr

def replacen_char_filter (s: Str) (f: Char → Bool) (sr: Str) (n: Nat) :=
  if (n > 0) then
    match s with
      | [] => []
      | h::t => if f h then sr ++ (replacen_char_filter t f sr (n-1)) else h::(replacen_char_filter t f sr n)
  else s

def replacen_char_filter_def (s: Str) (f: Char → Bool) (sr: Str) (n: Nat) := str_concat_pad (splitn_char_filter s (n+1) f) sr

def replacen (s: Str) (P: Pattern) (sr: Str) (n: Nat):= match P with
  | Pattern.SingleChar c => replacen_char_filter s (fun x => x == c) sr n
  | Pattern.ListChar l => replacen_char_filter s (fun x => l.contains x) sr n
  | Pattern.FilterFunction f => replacen_char_filter s f sr n
  | Pattern.WholeString ss => replacen_substring s ss sr n

def strip_prefix_char_filter (s: Str) (f: Char → Bool) := match s with
  | [] => none
  | h::t => if f h then some t else none

def strip_prefix_substring (s: Str) (p: Str) : Option Str := if List.isPrefixOf p s then some (s.drop p.length) else none

def strip_prefix (s: Str) (P: Pattern) := match P with
  | Pattern.SingleChar c => strip_prefix_char_filter s (fun x => x == c)
  | Pattern.ListChar l => strip_prefix_char_filter s (fun x => l.contains x)
  | Pattern.FilterFunction f => strip_prefix_char_filter s f
  | Pattern.WholeString s1 => strip_prefix_substring s s1

def strip_suffix_char_filter (s: Str) (f: Char → Bool) := match strip_prefix_char_filter s.reverse f with
  | none => none
  | some s1 => some (s1.reverse)

def strip_suffix_substring (s: Str) (p: Str) : Option Str := if List.isSuffixOf p s then some (s.take (s.length - p.length)) else none

def strip_suffix (s: Str) (P: Pattern) := match P with
  | Pattern.SingleChar c => strip_suffix_char_filter s (fun x => x == c)
  | Pattern.ListChar l => strip_suffix_char_filter s (fun x => l.contains x)
  | Pattern.FilterFunction f => strip_suffix_char_filter s f
  | Pattern.WholeString ss => strip_suffix_substring s ss

def to_ascii_lowercase (s: Str) := List.map Char.toLower s

def to_ascii_uppercase (s: Str) := List.map Char.toUpper s

def is_ascii (s: Str) := List.all s Char_is_ascii

def eq_ignore_ascii_case (s1 s2: Str):= (to_ascii_lowercase s1 = to_ascii_lowercase s2)

end Corpus.RustModels
