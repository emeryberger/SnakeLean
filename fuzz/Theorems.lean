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
    -- Body must be `@Eq α lhs rhs`.
    let body ← whnf body
    unless body.isAppOfArity ``Eq 3 do return none
    let args := body.getAppArgs
    -- ETA-EXPAND a function-typed equation.  Many library theorems are stated
    -- POINT-FREE (`Bool.and' = and`, `Option.toList = …`), i.e. `α` is itself a
    -- function type.  Taken literally, each side is then a bare function VALUE with
    -- no value parameters, and the driver — which calls the emitted def with
    -- arguments — reported spurious arity errors.  Applying both sides to fresh
    -- binders turns a point-free identity into an ordinary testable one; the equation
    -- stays valid by funext.  (For a non-function `α`, `ys` is empty and this is a
    -- no-op.)
    forallTelescope (← whnf args[0]!) fun ys cod => do
      -- Every binder — from the theorem AND from eta-expansion — must be a value
      -- parameter of a type the driver can generate.
      let binders := xs ++ ys
      let mut ptys := #[]
      for b in binders do
        let bty ← inferType b
        if ← Meta.isProp bty then return none
        let some t := tyName? (← whnf bty) | return none
        ptys := ptys.push t
      let some ret := tyName? (← whnf cod) | return none
      let lhs ← mkLambdaFVars binders (mkAppN args[1]! ys)
      let rhs ← mkLambdaFVars binders (mkAppN args[2]! ys)
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
  -- PRIORITY SOURCE: Lean's own `@[csimp]` table.  Each entry is a PROVED `f = g`
  -- between a reference implementation and the efficient one the compiler actually
  -- substitutes — i.e. a curated database of program-equivalence pairs sitting in the
  -- compiler's attribute table, exactly the corpus this technique wants.  (Isabelle's
  -- `code_test` runs proved lemmas through the code generator; this is the analogous
  -- source, harvested rather than hand-written.)  These bypass the namespace filter:
  -- a csimp pair is a program pair by construction, whatever it is named.
  let csimpThms := (Lean.Compiler.CSimp.ext.getState env).thmNames.toList
  let names : List Name :=
    csimpThms ++ (env.constants.toList.filterMap fun (n, ci) =>
      if ci.isTheorem && !n.isInternal && inScope n
         && ci.type.getForallBody.isAppOf ``Eq then some n else none)
  let mut i := 0
  let mut found := 0
  for n in names do
    if found ≥ maxCands then break
    let some ci := env.find? n | continue
    unless ci.isTheorem do continue
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

-- How many identities to harvest.  `EMP_MAX=0` means "the whole pool" (the environment
-- holds ~19.5k equations at computable types; the in-scope, unconditional, definable
-- subset is far smaller).  The driver sets this.
#eval show CoreM Unit from do
  let n := (← IO.getEnv "EMP_MAX").bind (·.toNat?) |>.getD 40
  EMP.run (if n == 0 then 1000000 else n) |>.run'
