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
