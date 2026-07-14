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
      -- Reject NONCOMPUTABLE sides.  `Bool.not'`, `Bool.and'`, and anything routed
      -- through `Classical.choice` cannot be compiled at all, so Lean emits no code and
      -- the transpiler — correctly — emits no function.  The identity is untestable, not
      -- violated; offering it produced a "no emitted def" flag that looked like a bug.
      let env ← getEnv
      let noncomp (e : Expr) : Bool :=
        e.getUsedConstants.any fun c => Lean.isNoncomputable env c
      if noncomp lhs || noncomp rhs then return none
      return some { thm, params := ptys, ret, lhs, rhs }

/-- Rename a lambda spine's binders to `p0, p1, …`.  The theorem's own binder names can
    be inaccessible (`x✝`), which does not round-trip through the pretty-printer.
    Binders are also forced EXPLICIT: a theorem's `{m n : Nat}` would otherwise print as
    `fun {p0 p1} => …`, which does not elaborate against the signature `Nat → Nat → …`. -/
partial def renameBinders (e : Expr) (i : Nat := 0) : Expr :=
  match e with
  | .lam _ t b _ => .lam (Name.mkSimple s!"p{i}") t (renameBinders b (i + 1)) .default
  | e => e

/-- Render one side as Lean SOURCE text.

    This is the whole point of the round-trip.  We previously built each side by
    abstracting the theorem's `Expr` and `addDecl`-ing it directly.  Those definitions
    are well-typed — but their LCNF shape is **not one the elaborator ever produces from
    source**, and several of the transpiler's rules are shape-sensitive pattern matches
    on instance structure.  Source-written `n - m` carries its `instSubNat`, so the
    truncated-subtraction rule fires; the raw `HSub.hSub` in a theorem statement need
    not, and the transpiler then emitted a plain `-` and EMP reported a "bug" that
    cannot occur in real code.

    So we print the term and let the ELABORATOR rebuild it, exactly as `gen.py` and
    `corpus_frags.py` do.  `pp.explicit := false` is essential: implicit and instance
    arguments are re-inferred on the way back in, which is precisely what makes the
    result source-shaped. -/
def sideSource (val : Expr) : MetaM String := do
  let e := renameBinders val
  withOptions (fun o => o
      |>.setBool `pp.fullNames true      -- unambiguous, resolves from any namespace
      |>.setBool `pp.explicit false      -- let the elaborator re-infer implicits/instances
      |>.setBool `pp.universes false
      |>.setBool `pp.notation true
      -- Without these the pretty-printer ELIDES long terms as `⋯`, which cannot be
      -- re-elaborated ("don't know how to synthesize placeholder").  A term we cannot
      -- print faithfully must be dropped, not silently truncated.
      |>.setBool `pp.deepTerms true
      |>.setBool `pp.proofs true
      |>.set `pp.maxSteps (10000000 : Nat)) do
    return (← ppExpr e).pretty (width := 1000000)

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

/-- Harvest and monomorphize, then emit each side as Lean SOURCE.

    PHASE 1 of two.  `fuzz/emp.py` assembles the emitted `def`s into a Lean file and
    runs it, so both sides are RE-ELABORATED from source before the transpiler sees
    them (phase 2).  That round-trip is what makes EMP's findings trustworthy: the
    transpiler is only ever handed terms shaped the way real code is shaped. -/
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
    let lsrc ← try sideSource c.lhs catch _ => continue
    let rsrc ← try sideSource c.rhs catch _ => continue
    -- A pretty-printed term with a metavariable or an inaccessible name will not
    -- re-elaborate; drop it here rather than break the phase-2 file.
    if lsrc.any (· == '✝') || rsrc.any (· == '✝') then continue
    if (lsrc.splitOn "?m").length > 1 || (rsrc.splitOn "?m").length > 1 then continue
    if lsrc.contains '\n' || rsrc.contains '\n' then continue
    -- The signature `T0 → T1 → Ret` matches the lambda `sideSource` printed.
    let sig := String.intercalate " → " (c.params.toList ++ [c.ret])
    IO.println s!"### THM\t{i}\t{c.thm}\t{c.ret}\t{String.intercalate "," c.params.toList}"
    IO.println s!"### DEF\t{i}\tL\tdef empL{i} : {sig} := {lsrc}"
    IO.println s!"### DEF\t{i}\tR\tdef empR{i} : {sig} := {rsrc}"
    i := i + 1
    found := found + 1

end EMP

-- How many identities to harvest.  `EMP_MAX=0` means "the whole pool" (the environment
-- holds ~19.5k equations at computable types; the in-scope, unconditional, definable
-- subset is far smaller).  The driver sets this.
#eval show CoreM Unit from do
  let n := (← IO.getEnv "EMP_MAX").bind (·.toNat?) |>.getD 40
  EMP.run (if n == 0 then 1000000 else n) |>.run'
