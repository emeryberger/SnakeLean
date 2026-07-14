import SnakeLean
open Lean Meta SnakeLean

/-!
# EMP: Equivalence Modulo Proofs — the harvester

Lean's environment contains tens of thousands of **machine-checked equations**
(`theorem foo : lhs = rhs`).  Each one is a proof that *two different programs are
the same program*.  This file harvests the ones whose two sides are runnable, turns
each side into a real definition, and transpiles both.

The resulting oracle: **the two Python programs must agree on every input** — and the
*proof*, not Lean's evaluator, is what says so.  So unlike `fuzz/gen.py`'s oracle,
no Lean evaluation is needed at test time.

Why this only works here: EMI (PLDI'14) must *invent* semantics-preserving mutations
from a handful of hand-written envelopes, because C has no ground truth.  We *harvest
thousands of proven ones* from the library, and the supply grows for free with the
imports.  No C/Go/Rust fuzzer has a database of machine-checked program equations.

What makes an identity USEFUL (as opposed to merely true) is that its two sides
exercise *different translation rules* — `Nat.zero_sub : 0 - n = 0` catches truncated
`Nat` subtraction emitted as plain `-`, while `Nat.div_eq_sub_mod_div` cannot (its
subtraction never goes negative).  We therefore emit each side SEPARATELY with its
own `HANDLERS_FIRED` tag list, so the driver can keep the identities whose sides
differ and rank them by which rules they distinguish.

Run:  lake env lean fuzz/Theorems.lean
-/

namespace EMP

/-- Types the differential driver can generate values for (mirrors `gen.py`). -/
def tyName? (e : Expr) : Option String :=
  match e with
  | .const ``Nat _ => some "Nat"
  | .const ``Int _ => some "Int"
  | .const ``Bool _ => some "Bool"
  | .const ``String _ => some "String"
  | .const ``Char _ => some "Char"
  | .app (.const ``List _) a =>
    match a with
    | .const ``Nat _ => some "List Nat"
    | .const ``Int _ => some "List Int"
    | .const ``Bool _ => some "List Bool"
    | _ => none
  | .app (.const ``Array _) a =>
    match a with
    | .const ``Nat _ => some "Array Nat"
    | _ => none
  | .app (.const ``Option _) a =>
    match a with
    | .const ``Nat _ => some "Option Nat"
    | _ => none
  | _ => none

/-- A harvested identity: the value parameters, and both sides as closed lambdas. -/
structure Cand where
  thm    : Name
  params : Array String
  ret    : String
  lhs    : Expr
  rhs    : Expr

/-- Peel `∀ {α} [inst] …` prefixes: instantiate every TYPE binder at `Nat` (which
    monomorphizes polymorphic identities like `List.length_append`, hugely raising
    yield) and synthesize every instance binder.  A `Prop` binder means the identity
    is *conditional* (`n ≤ m → …`); we reject those — an unconditional equation is
    valid on ALL inputs, including the edge cases (`n = 0`) we would never think to
    special-case. -/
partial def monomorphize (ty : Expr) : MetaM (Option Expr) := do
  match ← whnf ty with
  | .forallE _ d b _ =>
    if ← Meta.isProp d then
      return none                                   -- hypothesis ⇒ conditional
    else if d.isSort then
      monomorphize (b.instantiate1 (mkConst ``Nat)) -- ∀ {α} ⇒ α := Nat
    else if (← isClass? d).isSome then
      match ← trySynthInstance d with
      | .some inst => monomorphize (b.instantiate1 inst)
      | _ => return none
    else
      return some ty                                -- first value binder: stop
  | e => return some e

/-- Analyze one theorem.  Returns the identity if every value parameter and the
    equation's own type are types we can generate values for. -/
def analyze (thm : Name) (ty : Expr) : MetaM (Option Cand) := do
  let some mono ← monomorphize ty | return none
  forallTelescope mono fun xs body => do
    -- Every remaining binder must be a value parameter of a supported type.
    let mut ptys := #[]
    for x in xs do
      let xty ← inferType x
      if ← Meta.isProp xty then return none
      let some t := tyName? (← whnf xty) | return none
      ptys := ptys.push t
    -- Body must be `@Eq α lhs rhs` at a supported α.
    let body ← whnf body
    unless body.isAppOfArity ``Eq 3 do return none
    let args := body.getAppArgs
    let some ret := tyName? (← whnf args[0]!) | return none
    let lhs ← mkLambdaFVars xs args[1]!
    let rhs ← mkLambdaFVars xs args[2]!
    -- Reject trivial reflexive identities: both sides the same program.
    if ← withReducible <| isDefEq lhs rhs then return none
    return some { thm, params := ptys, ret, lhs, rhs }

/-- Add a side as a real definition so the transpiler can compile it from LCNF.
    Building the `Expr` directly avoids any pretty-print / re-elaborate round-trip. -/
def addSide (name : Name) (val : Expr) : MetaM Bool := do
  try
    let ty ← inferType val
    -- Universe parameters must be declared, or the KERNEL rejects the definition
    -- ("invalid reference to undefined universe level parameter").  Monomorphizing
    -- `α := Nat` removes most, but not all — a `List (List α)` or `Prod` can still
    -- leave one behind.  Collect whatever survives rather than assuming none.
    let lvls := (collectLevelParams (collectLevelParams {} ty) val).params.toList
    let d : DefinitionVal := {
      name, levelParams := lvls, type := ty, value := val
      hints := .abbrev, safety := .safe }
    -- A side that isn't computable (proof-carrying, `Classical.choice`, …) is
    -- rejected here by the compiler rather than producing bogus Python.
    addDecl (.defnDecl d)
    compileDecl (.defnDecl d)
    return true
  catch _ => return false

/-- Namespaces whose *bodies* we model.  A theorem may have `Nat` parameters yet a
    body over some internal container (`Std.Roc`, `DTreeMap`, `BitVec`) the transpiler
    has no rules for — emitting that yields an undefined-name failure on BOTH sides,
    which is noise rather than a translation bug.  Restrict to the surface we claim
    to support. -/
def inScope (n : Name) : Bool :=
  match n.getRoot with
  | .str _ s => ["Nat", "Int", "Bool", "List", "Array", "Option", "String", "Char",
                 "Prod"].contains s
  | _ => false

/-- Harvest, monomorphize, define, and transpile each side separately (separate
    emissions so each carries its own `HANDLERS_FIRED` set). -/
def run (maxCands : Nat) : MetaM Unit := do
  let env ← getEnv
  let mut i := 0
  let mut found := 0
  for (n, ci) in env.constants.toList do
    if found ≥ maxCands then break
    unless ci.isTheorem && !n.isInternal && inScope n do continue
    -- cheap pre-filter before the expensive analysis
    unless ci.type.getForallBody.isAppOf ``Eq do continue
    let c? ← try analyze n ci.type catch _ => pure none
    let some c := c? | continue
    let lname := Name.mkSimple s!"empL{i}"
    let rname := Name.mkSimple s!"empR{i}"
    unless ← addSide lname c.lhs do continue
    unless ← addSide rname c.rhs do continue
    -- Transpile each side on its own: two independent programs, two rule-tag sets.
    let lpy ← liftM (m := CoreM) (emitPythonForNames `EMP [lname])
    let rpy ← liftM (m := CoreM) (emitPythonForNames `EMP [rname])
    -- Explicit END markers: Lean appends its diagnostics to the same stream, and a
    -- multi-line error landing inside a block would otherwise be `exec`'d as Python
    -- and reported as a transpiler bug — a false positive from the harness itself.
    IO.println s!"### THM\t{i}\t{c.thm}\t{c.ret}\t{String.intercalate "," c.params.toList}"
    IO.println s!"### SIDE\t{i}\tL"
    IO.println lpy
    IO.println s!"### END\t{i}\tL"
    IO.println s!"### SIDE\t{i}\tR"
    IO.println rpy
    IO.println s!"### END\t{i}\tR"
    i := i + 1
    found := found + 1

end EMP

#eval show CoreM Unit from EMP.run 40 |>.run'
