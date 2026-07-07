/-
  Dumps constructor/field-type info for the custom inductive & structure types
  declared in `Corpus/*.lean`, for the fragment-reuse fuzzer (Phase 3, custom
  inductive types).  The fuzzer parses this to decide which user types it can
  construct values of, and how.

  Emitted format (one type per `### TYPE` line, tab-separated):
      ### TYPE <TypeName> <Ctor1>;<fieldty>,<fieldty> | <Ctor2>;...
  where each constructor is `name;` followed by a comma-separated list of its
  field types (empty for a nullary constructor).  A Lean-side dump (vs. Python
  regex over source) uses the real environment, so it is robust to formatting
  and to Lean version changes.

  Type abbreviations (`abbrev Str := List Char`) are dumped as
      ### ABBREV <AbbrevName>	<expansion>
  so the fuzzer can expand a signature's `Str` to its drivable `List Char`
  form (an abbrev is transparent, so a param typed `Str` is really `List Char`).

  Run:  lake env lean fuzz/TypeInfo.lean
-/
import Lean
import Corpus
open Lean Meta

/-- All `Corpus.*` inductive/structure type names in the environment. -/
def corpusTypes : MetaM (Array Name) := do
  let env ← getEnv
  let mut out := #[]
  for (n, info) in env.constants.toList do
    match info with
    | .inductInfo _ =>
      -- Only user types under the `Corpus` namespace, skip internal/aux names.
      if (`Corpus).isPrefixOf n && !n.isInternal then
        out := out.push n
    | _ => pure ()
  return out

/-- The field types of one constructor, as pretty-printed strings. -/
def ctorFieldTypes (c : Name) (numFields : Nat) : MetaM (Array String) := do
  let env ← getEnv
  let some (.ctorInfo ci) := env.find? c | return #[]
  forallTelescopeReducing ci.type fun args _ => do
    let fields := args.extract (args.size - numFields) args.size
    let mut tys := #[]
    for f in fields do
      tys := tys.push (toString (← ppExpr (← inferType f)))
    return tys

/-- All `Corpus.*` type abbreviations (`abbrev Str := List Char`) in the
    environment, as (name, expansion) pairs.  An abbrev is a `def` marked
    `@[reducible]`; we pretty-print its value (the RHS type). -/
def corpusAbbrevs : MetaM (Array (Name × String)) := do
  let env ← getEnv
  let mut out := #[]
  for (n, info) in env.constants.toList do
    match info with
    | .defnInfo di =>
      if (`Corpus).isPrefixOf n && !n.isInternal
          && (← getReducibilityStatus n) == .reducible then
        -- Only nullary abbrevs (no leading params) — a parameterized abbrev
        -- can't be substituted positionally into a signature by the fuzzer.
        if di.type.isSort then
          out := out.push (n, toString (← ppExpr di.value))
    | _ => pure ()
  return out

/-- Is `t` a "value" type — i.e. telescoping it, every nested argument type and
    the final codomain is a value (not a `Sort`/`Prop`)?  Keeps `Char → Bool`
    (codomain `Bool`) but rejects `motive : T → Sort u` and proof types, so the
    signature dump filters out compiler-generated recursors. -/
partial def isValueType (t : Expr) : MetaM Bool :=
  Meta.forallTelescopeReducing t fun bs cod => do
    for b in bs do
      unless (← isValueType (← inferType b)) do return false
    if cod.isSort then return false
    if (← Meta.isProp cod) then return false
    return true

/-- Elaborated signatures of every user-written `Corpus.*` function `def`, as
    (name, param-type strings, return-type string).  Reading the ELABORATED type
    (not the source) means the fuzzer harvester needs no source parsing at all —
    it works for defs that omit type annotations (`def char_indices s := …`, of
    which rust-lean-models has ~100) and is robust to formatting/Lean-version
    changes.  Lean-generated helpers (`.match_1`, `.rec`, `.eq_def`, …) are
    filtered via `isInternalDetail`; we also skip anything whose type lives in
    `Prop`/`Sort` (proofs, recursors, motives), keeping only value functions. -/
def corpusDefSigs : MetaM (Array (Name × Array String × String)) := do
  let env ← getEnv
  let mut out := #[]
  for (n, info) in env.constants.toList do
    match info with
    | .defnInfo di =>
      if !((`Corpus).isPrefixOf n) || n.isInternalDetail then continue
      -- Keep only USER-WRITTEN defs: compiler-generated helpers (`.ctorIdx`,
      -- `.toCtorIdx`, `deriving` output, …) have no source declaration range,
      -- while real functions — including nested helpers like `.go`/`.sort` — do.
      if (← findDeclarationRanges? n).isNone then continue
      -- Skip abbrevs (dumped separately) and any def whose declared type is a
      -- sort — those are type synonyms / not value-returning functions.
      if di.type.isForall then
        -- Reject if it takes a proof/type/motive argument or returns a non-value
        -- (Prop/Sort).  A binder is drivable iff, telescoping its OWN type, every
        -- nested argument and the final codomain is a value (not a Sort/Prop):
        -- this keeps `Char → Bool` (codomain `Bool`) but rejects `motive : T →
        -- Sort u` and proof arguments, filtering out compiler-generated
        -- recursors (`recOn`/`casesOn`/`brecOn`) that `isInternalDetail` misses.
        let ok ← forallTelescopeReducing di.type fun args ret => do
          for a in args do
            unless (← isValueType (← inferType a)) do return false
          if ret.isSort then return false
          if (← Meta.isProp ret) then return false
          return true
        if !ok then continue
        let sig ← forallTelescopeReducing di.type fun args ret => do
          let mut ptys := #[]
          for a in args do
            ptys := ptys.push (toString (← ppExpr (← inferType a)))
          return (ptys, toString (← ppExpr ret))
        out := out.push (n, sig.1, sig.2)
    | _ => pure ()
  return out

#eval show MetaM Unit from do
  let env ← getEnv
  for n in (← corpusTypes) do
    let some (.inductInfo info) := env.find? n | continue
    -- Skip type-parameterized types (e.g. `Stack α`) — the fuzzer's value
    -- universe is monomorphic, so it can't construct their element values.
    if info.numParams > 0 then continue
    let mut parts := #[]
    for c in info.ctors do
      let some (.ctorInfo ci) := env.find? c | continue
      let tys ← ctorFieldTypes c ci.numFields
      parts := parts.push s!"{c};{",".intercalate tys.toList}"
    IO.println s!"### TYPE\t{n}\t{" | ".intercalate parts.toList}"
  for (n, expansion) in (← corpusAbbrevs) do
    IO.println s!"### ABBREV\t{n}\t{expansion}"
  for (n, ptys, ret) in (← corpusDefSigs) do
    IO.println s!"### SIG\t{n}\t{",".intercalate ptys.toList}\t{ret}"
