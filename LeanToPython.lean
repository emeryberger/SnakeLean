/-
Copyright (c) 2026 Lean FRO, LLC. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
-/

import Lean.Compiler.LCNF.CompilerM
import Lean.Compiler.LCNF.PhaseExt
import Lean.Compiler.LCNF.ToDecl
import Lean.Compiler.NameMangling
import Lean.Compiler.ExternAttr

/-!
# LeanToPython: Idiomatic Python Code Generation

This library emits idiomatic, readable Python code from Lean LCNF declarations.
-/

namespace LeanToPython

open Lean Lean.Compiler.LCNF

/-!
Lean 4.31 made the LCNF datatypes (`Decl`, `Code`, `FunDecl`, `LetDecl`,
`LetValue`, `Param`, `Arg`, `Alt`, `Cases`) indexed by a `Purity` parameter.
This transpiler operates entirely on the `.pure` phase (what `toDecl` returns),
so we pin the purity here with shadowing abbreviations.  A local `abbrev`
shadows the `open`ed indexed type, and field projections resolve through it, so
the rest of the file is unchanged.
-/
abbrev Decl     := Lean.Compiler.LCNF.Decl     .pure
abbrev Code     := Lean.Compiler.LCNF.Code     .pure
abbrev FunDecl  := Lean.Compiler.LCNF.FunDecl  .pure
abbrev LetDecl  := Lean.Compiler.LCNF.LetDecl  .pure
abbrev LetValue := Lean.Compiler.LCNF.LetValue .pure
abbrev Param    := Lean.Compiler.LCNF.Param    .pure
abbrev Arg      := Lean.Compiler.LCNF.Arg      .pure
abbrev Alt      := Lean.Compiler.LCNF.Alt      .pure
abbrev Cases    := Lean.Compiler.LCNF.Cases    .pure

/-- Lean 4.31 wraps a declaration's body in `DeclValue` (`.code` | `.extern`);
    previously `Decl.value` was the `Code` directly.  This transpiler only
    handles code bodies, so project the `Code` out (extern decls have no LCNF
    body to translate, so we treat them as an empty/unreachable body). -/
def declCode (d : Decl) : Code :=
  match d.value with
  | .code c => c
  | .extern _ => default

structure Context where
  modName : Name
  indentLevel : Nat := 0

structure State where
  buf : String := ""
  emittedTypes : Lean.NameSet := {}
  /-- Maps FVarId to Python variable name -/
  varNames : Std.HashMap FVarId String := {}
  /-- Tracks which base names have been used to avoid collisions -/
  usedNames : Std.HashSet String := {}
  /-- Track variables that hold type class instances (to inline their operations) -/
  instanceVars : Std.HashMap FVarId Name := {}
  /-- Track variables that hold extracted operations from instances -/
  extractedOps : Std.HashMap FVarId (Name × Nat) := {}
  /-- Instance / op fvars whose arithmetic differs from the naive Python
      operator, tagged by kind:
        "natsub" — truncated `Nat` subtraction (saturates at 0): `max(0, a-b)`
        "intdiv" — Euclidean `Int` division: `(a - a % abs b) // b`
        "intmod" — Euclidean `Int` modulo:   `a % abs b`
      The tag is propagated from the concrete instance (`instSubNat`,
      `Int.instDiv`, `Int.instMod`) through the generic `instH*` wrapper built
      from it, onto the projected `.hSub`/`.hDiv`/`.hMod` op, so the emission can
      wrap it correctly rather than emitting a plain `-`/`//`/`%` that has the
      wrong sign behaviour on `Nat`/negative `Int` operands. -/
  arithKind : Std.HashMap FVarId String := {}
  /-- Track the last literal value seen (for OfNat pattern) -/
  lastLiteral : Option LitValue := none
  /-- Track variables that are just literals (from OfNat projections) -/
  literalVars : Std.HashMap FVarId LitValue := {}
  /-- Track variables that hold Bool values -/
  boolVars : Std.HashMap FVarId Bool := {}
  /-- Track fvars whose LCNF type is `Bool` (params / let-bindings). Used to
      decide Decidable-cases branch order authoritatively rather than by name. -/
  boolTypedVars : Std.HashSet FVarId := {}
  /-- Track variables that are unit values (can be skipped in calls) -/
  unitVars : Std.HashSet FVarId := {}
  /-- Track local function arities (nonUnitParams, totalParams) for partial application detection -/
  localFnArities : Std.HashMap FVarId (Nat × Nat) := {}
  /-- Variable aliases: when one variable is just a copy of another -/
  varAliases : Std.HashMap FVarId FVarId := {}
  /-- Track the last comparison result variable (for decide pattern) -/
  lastCompareVar : Option FVarId := none
  /-- Rendered Python expression strings for let-bound fvars inside a lambda
      body that is being inlined into a comprehension. -/
  exprVars : Std.HashMap FVarId String := {}
  /-- Single-parameter lambdas that were deferred (not emitted as a `def`)
      because their body renders as a simple expression. Maps the lambda's
      fvar to (paramName, bodyExpr). Consumed inline by comprehensions; any
      other use is materialized as a Python `(lambda p: e)`. -/
  deferredLambdas : Std.HashMap FVarId (String × String) := {}
  /-- For a let-fvar bound to a list comprehension we emitted (map/filter/…),
      the comprehension's inner text without the surrounding brackets, e.g.
      "(x + 1) for x in xs". Lets a downstream `toFinset`/`toSet`/`eraseDups`
      fuse into a set comprehension `{...}` instead of wrapping a list. -/
  listCompInner : Std.HashMap FVarId String := {}
  /-- The most recently emitted list-comprehension statement, as
      (fvar, bufStart, bufEnd). If a set-comprehension fuses this exact fvar as
      the immediately following statement (buffer unchanged since), the dead
      intermediate line is truncated away. -/
  lastListComp : Option (FVarId × Nat × Nat) := none
  /-- When emitting a self-tail-recursive function as a `while True:` loop, this
      holds `(declName, pyParamNames)` for the current function. A tail
      self-call to `declName` is then emitted as a parallel rebind of these
      parameters followed by `continue`, instead of a recursive call. `none`
      when not in a tail-loop. -/
  tailLoop : Option (Name × Array String) := none
  /-- Local continuation thunks (`_alt`) that we inline in tail-loop mode:
      maps the thunk's fvar to its FunDecl so a tail-jump/call to it emits the
      body inline (allowing `continue` to reach the enclosing loop) rather than
      calling a nested `def`. -/
  inlineThunks : Std.HashMap FVarId FunDecl := {}
  nextTmpIdx : Nat := 0
  /-- Self-coverage instrumentation: the set of emission-handler tags that fired
      while transpiling. Lets the fuzzer report which of the transpiler's
      special-cased handlers its test corpus actually exercised — an untested
      handler is where a bug hides (both F12 and F13 lived in handlers the
      generative grammar never reached). Populated via `markHandler`; dumped by
      `emitPythonForDecls` as a `### HANDLERS` stderr line. -/
  firedHandlers : Std.HashSet String := {}
  /-- Global de-duplicated Python names for top-level (and helper) declarations,
      keyed by the full Lean `Name`.  `toPyFnName` maps some distinct Lean
      functions to the SAME short Python name (e.g. `Corpus.Sorting.mode.count`
      and `Corpus.Strings.count` both → `count`); when several such functions are
      emitted into one file the later `def` shadows the earlier, and calls
      resolve to the wrong body.  A pre-pass (`assignGlobalFnNames`) fills this
      map, suffixing collisions (`count`, `count_2`, …); `pyFnName` consults it so
      the `def` and every call site agree on the unique name. -/
  globalFnNames : Std.HashMap Name String := {}

abbrev EmitM := ReaderT Context StateRefT State CompilerM

@[inline] def getModName : EmitM Name := return (← read).modName

@[inline] def getIndent : EmitM Nat := return (← read).indentLevel

@[inline] def withIndent (x : EmitM α) : EmitM α :=
  withReader (fun ctx => { ctx with indentLevel := ctx.indentLevel + 1 }) x

def emitIndent : EmitM Unit := do
  let n ← getIndent
  modify fun s => { s with buf := s.buf ++ String.mk (List.replicate (n * 4) ' ') }

@[inline] def emit (str : String) : EmitM Unit :=
  modify fun s => { s with buf := s.buf ++ str }

@[inline] def emitLn (str : String) : EmitM Unit := do
  emitIndent
  emit str
  emit "\n"

/-- Record that emission handler `tag` fired (self-coverage instrumentation).
    Tags are free-form but conventionally `binop.<Name>`, `stdlib.<Name>`,
    `special.<name>`, `cases.<kind>`, `struct.<name>` so the fuzzer can group
    them. See `State.firedHandlers`. -/
@[inline] def markHandler (tag : String) : EmitM Unit :=
  modify fun s => { s with firedHandlers := s.firedHandlers.insert tag }

def emitBlankLine : EmitM Unit := emit "\n"

/-! ## Name Management -/

def isPyKeyword : String → Bool
  | "and" | "as" | "assert" | "async" | "await" | "break" | "class" | "continue"
  | "def" | "del" | "elif" | "else" | "except" | "False" | "finally" | "for"
  | "from" | "global" | "if" | "import" | "in" | "is" | "lambda" | "None"
  | "nonlocal" | "not" | "or" | "pass" | "raise" | "return" | "True" | "try"
  | "while" | "with" | "yield" | "match" | "case" | "type" => true
  | _ => false

def sanitizeName (s : String) : String :=
  let s := s.map fun c => if c.isAlphanum || c == '_' then c else '_'
  if s.isEmpty then "_v"
  else if s.get? 0 |>.map (·.isDigit) |>.getD false then "_" ++ s
  else if isPyKeyword s then s ++ "_"
  else s

def toSnakeCase (s : String) : String := Id.run do
  let mut result := ""
  let mut prevLower := false
  for c in s.toList do
    if c.isUpper && prevLower then
      result := result.push '_'
    result := result.push c.toLower
    prevLower := c.isLower
  return result

/-- Common helper function names that need their parent prefix to be unique -/
def isHelperName : String → Bool
  | "go" | "loop" | "aux" | "iter" | "rec" | "helper"
  | "check" | "sort" | "succ" | "adjust" | "visit" | "process"
  | "inner" | "step" | "work" | "build" | "make" | "run"
  | "insert" | "merge" | "split" | "fold" | "map" | "filter"
  | "f" | "g" | "h" => true
  | _ => false

/-- Function names that commonly collide across modules -/
def needsModulePrefix : String → Bool
  | "reverse" | "gcd" | "lcm" | "fibonacci" | "isPrime" | "primeFactors"
  | "map" | "filter" | "foldl" | "foldr" | "zip" | "take" | "drop"
  | "concat" | "replicate" | "isEmpty" | "contains" | "insert"
  | "id" | "const" | "flip" | "compose" | "apply"
  | "empty" | "size" | "bind" | "isPalindrome" | "isOver" | "countChar"
  | "ord" | "chr" | "abs" | "min" | "max" | "sum" | "all" | "any" | "len" | "range"
  | "get" | "set" | "create" | "push" | "neighbors" | "addVertex" | "addEdge"
  | "Graph" => true  -- Graph module functions need grandparent prefix
  | _ => false

def isParentThatNeedsGrandparent : String → Bool
  | "Graph" | "Matrix" | "Heap" | "UnionFind" => true
  | _ => false

def toPyFnName (name : Name) : String :=
  let base := match name with
    | .str (.str (.str _ grandparent) parent) s =>
      -- For helpers with common parent names (go, check), include grandparent for uniqueness
      -- e.g., Algorithms.fibonacci.go -> algorithms_fibonacci_go
      if isHelperName s && needsModulePrefix parent then
        toSnakeCase grandparent ++ "_" ++ toSnakeCase parent ++ "_" ++ s
      -- For types like Graph that exist in multiple modules, include grandparent
      else if isParentThatNeedsGrandparent parent && needsModulePrefix s then
        toSnakeCase grandparent ++ "_" ++ toSnakeCase parent ++ "_" ++ s
      -- Include parent prefix for common helper names
      else if isHelperName s then toSnakeCase parent ++ "_" ++ s
      -- Include module prefix for commonly colliding function names
      else if needsModulePrefix s then toSnakeCase parent ++ "_" ++ s
      else s
    | .str (.str _ parent) s =>
      -- Include parent prefix for common helper names to avoid collisions
      if isHelperName s then toSnakeCase parent ++ "_" ++ s
      -- Include module prefix for commonly colliding function names
      else if needsModulePrefix s then toSnakeCase parent ++ "_" ++ s
      else s
    | .str _ s => s
    | .num p n => toPyFnName p ++ s!"_{n}"
    | .anonymous => "anon"
  sanitizeName (toSnakeCase base)

/-- Common constructor names that need parent prefix to be unique -/
def isCommonCtorName : String → Bool
  | "mk" | "node" | "empty" | "nil" | "cons" | "some" | "none" => true
  | _ => false

def toPyTypeName (name : Name) : String :=
  match name with
  | .str (.str _ parent) s =>
    -- Include parent prefix for common constructor names to avoid collisions
    if isCommonCtorName s then parent ++ "_" ++ s
    else s
  | .str _ s => s
  | .num p n => toPyTypeName p ++ s!"{n}"
  | .anonymous => "Anon"

/-- Register a variable with a given base name, handling collisions -/
def registerVar (fvarId : FVarId) (baseName : Name) : EmitM String := do
  let base := sanitizeName (toSnakeCase (baseName.toString (escape := false)))
  let st ← get
  if let some name := st.varNames[fvarId]? then
    return name
  let name ← do
    if st.usedNames.contains base then
      -- Find a unique suffix
      let mut idx := st.nextTmpIdx
      while st.usedNames.contains s!"{base}_{idx}" do
        idx := idx + 1
      modify fun s => { s with nextTmpIdx := idx + 1 }
      pure s!"{base}_{idx}"
    else
      pure base
  modify fun s => { s with
    varNames := s.varNames.insert fvarId name
    usedNames := s.usedNames.insert name
  }
  return name

/-- Resolve variable aliases (non-recursive to avoid termination issues) -/
def resolveAlias (fvarId : FVarId) : EmitM FVarId := do
  let mut current := fvarId
  for _ in [0:100] do  -- Limit iterations to prevent infinite loops
    match (← get).varAliases[current]? with
    | some target => current := target
    | none => return current
  return current

/-- Get the Python name for an FVarId, or generate a tmp name if unknown -/
def getVarName (fvarId : FVarId) : EmitM String := do
  let fvarId ← resolveAlias fvarId
  if let some name := (← get).varNames[fvarId]? then
    return name
  -- Fallback: use the fvarId name
  registerVar fvarId fvarId.name

/-- The registered Python name for `fvarId`, or `none` if it was never bound.
    Unlike `getVarName`, this does NOT invent a fallback name from the raw fvar
    (`_uniq_NNN`).  Expression-mode rendering uses it to REFUSE to render a body
    that references an unemitted local function — otherwise the deferred lambda
    would call a name that never gets a `def` (a `NameError` at runtime). -/
def knownVarName? (fvarId : FVarId) : EmitM (Option String) := do
  let fvarId ← resolveAlias fvarId
  return (← get).varNames[fvarId]?

/-- The Python name for a top-level/helper declaration `name`, using the global
    de-duplicated map when present (see `State.globalFnNames`) and falling back
    to the pure `toPyFnName` otherwise.  Both the `def` and every call site route
    through this so a collision-suffixed name (`count_2`) is used consistently. -/
def pyFnName (name : Name) : EmitM String := do
  match (← get).globalFnNames[name]? with
  | some n => return n
  | none => return toPyFnName name

/-- Alias one variable to another -/
def aliasVar (from_ to_ : FVarId) : EmitM Unit :=
  modify fun s => { s with varAliases := s.varAliases.insert from_ to_ }

/-- Mark a variable as holding a type class instance -/
def markAsInstance (fvarId : FVarId) (instName : Name) : EmitM Unit :=
  modify fun s => { s with instanceVars := s.instanceVars.insert fvarId instName }

/-- Mark a variable as holding an extracted operation from an instance -/
def markAsExtractedOp (fvarId : FVarId) (instName : Name) (fieldIdx : Nat) : EmitM Unit :=
  modify fun s => { s with extractedOps := s.extractedOps.insert fvarId (instName, fieldIdx) }

/-- Tag an fvar with an arithmetic kind ("natsub" / "intdiv" / "intmod"). -/
def markArith (fvarId : FVarId) (kind : String) : EmitM Unit :=
  modify fun s => { s with arithKind := s.arithKind.insert fvarId kind }

/-- The arithmetic kind tag for an fvar, if any. -/
def arithOf (fvarId : FVarId) : EmitM (Option String) := do
  return (← get).arithKind[fvarId]?

/-- Check if a variable is an instance or extracted op that should be skipped -/
def isInstanceRelated (fvarId : FVarId) : EmitM Bool := do
  let st ← get
  return st.instanceVars.contains fvarId || st.extractedOps.contains fvarId

/-- Record that an fvar has LCNF type `Bool` (a `Bool`-typed param or let).
    Populated as we walk a decl's params and let-bindings; consulted by
    `emitDecidableCases` to pick branch order authoritatively rather than by
    name. (LCNF `findParam?`/`findLetDecl?` don't see the decl's locals during
    emission, so we track types ourselves.) -/
def markBoolTyped (fvarId : FVarId) (ty : Expr) : EmitM Unit := do
  match ty with
  | .const ``Bool _ => modify fun s => { s with boolTypedVars := s.boolTypedVars.insert fvarId }
  | _ => pure ()

/-- True iff the fvar is known to have type `Bool` (after alias resolution). -/
def fvarIsBool (fvarId : FVarId) : EmitM Bool := do
  let r ← resolveAlias fvarId
  let st ← get
  return st.boolTypedVars.contains fvarId || st.boolTypedVars.contains r

/-! ## Type Emission -/

partial def getReturnType (e : Expr) : Expr :=
  match e with
  | .forallE _ _ body _ => getReturnType body
  | _ => e

partial def collectArrowTypes (e : Expr) : List Expr × Expr :=
  match e with
  | .forallE _ dom body _ =>
    if body.hasLooseBVars then
      -- Dependent type - just return result
      ([], e)
    else
      let (args, ret) := collectArrowTypes body
      (dom :: args, ret)
  | _ => ([], e)

partial def toPyTypeHint (e : Expr) : EmitM String := do
  match e with
  | .const ``Nat _ => return "int"
  | .const ``Int _ => return "int"
  | .const ``String _ => return "str"
  | .const ``Char _ => return "str"  -- Python has no char type; single chars are str
  | .const ``Bool _ => return "bool"
  | .const ``Float _ => return "float"
  | .const ``Unit _ => return "None"
  | .const ``UInt8 _ | .const ``UInt16 _ | .const ``UInt32 _
  | .const ``UInt64 _ | .const ``USize _ => return "int"
  | .const name _ =>
    if name == ``lcErased then return "Any"
    else return toPyTypeName name
  | .app (.const ``List _) arg =>
    let argType ← toPyTypeHint arg
    return s!"list[{argType}]"
  | .app (.const ``Array _) arg =>
    let argType ← toPyTypeHint arg
    return s!"list[{argType}]"
  | .app (.const ``Option _) arg =>
    let argType ← toPyTypeHint arg
    return s!"{argType} | None"
  | .app (.app (.const ``Prod _) a) b =>
    let aType ← toPyTypeHint a
    let bType ← toPyTypeHint b
    return s!"tuple[{aType}, {bType}]"
  | .forallE _ dom body _ =>
    if body.hasLooseBVars then
      -- Dependent type - return the result type
      toPyTypeHint (getReturnType body)
    else
      -- Non-dependent arrow type: A → B → C becomes Callable[[A, B], C]
      let (args, ret) := collectArrowTypes e
      let argTypes ← args.mapM toPyTypeHint
      let retType ← toPyTypeHint ret
      return s!"Callable[[{", ".intercalate argTypes}], {retType}]"
  | _ => return "Any"

/-! ## Builtin Operations -/

/-- Check if a string contains a substring -/
def containsSubstr (s sub : String) : Bool :=
  (s.splitOn sub).length > 1

/-- Recognize type class instance constructors -/
def isInstanceCtor (name : Name) : Bool :=
  let s := name.toString
  -- Match both "instFoo" and "Module.instFoo" patterns
  s.startsWith "inst" || s.startsWith "Inst" ||
  containsSubstr s ".inst" || containsSubstr s ".Inst"

/-- Get the Python operator for a Nat/Int binary operation -/
def natBinOp? (name : Name) : Option String :=
  match name with
  | ``Nat.add => some "+"
  | ``Nat.sub => some "-"
  | ``Nat.mul => some "*"
  | ``Nat.div => some "//"
  | ``Nat.mod => some "%"
  | ``Nat.pow => some "**"
  | ``Nat.beq => some "=="
  | ``Nat.ble => some "<="
  | ``Nat.blt => some "<"
  | ``Nat.decLt => some "<"
  | ``Nat.decLe => some "<="
  | ``Int.add => some "+"
  | ``Int.sub => some "-"
  | ``Int.mul => some "*"
  | ``Int.tdiv | ``Int.ediv => some "//"
  | ``Int.tmod | ``Int.emod => some "%"
  | ``Int.decLt => some "<"
  | ``Int.decLe => some "<="
  | ``BEq.beq => some "=="
  | _ => none

/-- Builtin functions that wrap their argument -/
def builtinFn? (name : Name) : Option String :=
  match name with
  | ``String.length => some "len"
  | ``List.length | ``List.lengthTR => some "len"
  | ``Array.size => some "len"
  | ``not => some "not"
  | ``Int.neg | ``Neg.neg => some "-"
  | _ => none

/-- Map Lean standard library functions to Python equivalents -/
def stdlibFnToPython? (name : Name) : Option String :=
  match name with
  -- String operations
  | ``String.toList => some "list"
  | ``String.mk => some "''.join"
  | ``String.push => none  -- handled specially with +=
  | ``List.asString => some "''.join"

  -- Char predicates
  | ``Char.isAlpha => some "str.isalpha"
  | ``Char.isDigit => some "str.isdigit"
  | ``Char.isAlphanum => some "str.isalnum"
  | ``Char.isLower => some "(lambda c: c.islower())"
  | ``Char.isUpper => some "(lambda c: c.isupper())"
  | ``Char.isWhitespace => some "(lambda c: c.isspace())"
  | ``Char.toUpper => some "(lambda c: c.upper())"
  | ``Char.toLower => some "(lambda c: c.lower())"
  | ``Char.toNat => some "ord"
  | ``Char.ofNat => some "chr"

  -- Option operations
  | ``Option.isSome => some "(lambda x: x is not None)"
  | ``Option.isNone => some "(lambda x: x is None)"
  | ``Option.get! => some "(lambda x: x)"  -- Python just uses the value
  | ``Option.getD => some "(lambda x, d: x if x is not None else d)"

  -- List operations
  | ``List.reverse => some "list(reversed({}))"  -- special format
  | ``List.append | ``HAppend.hAppend => none  -- handled as +
  | ``List.head? => some "(lambda xs: xs[0] if xs else None)"
  | ``List.tail? => some "(lambda xs: xs[1:] if xs else None)"
  | ``List.getLast? => some "(lambda xs: xs[-1] if xs else None)"
  | ``List.dropLast => some "(lambda xs: xs[:-1])"
  | ``List.take => some "(lambda n, xs: xs[:n])"
  | ``List.drop => some "(lambda n, xs: xs[n:])"
  | ``List.filter | ``List.filterTR => some "list(filter({}, {}))"  -- special format
  | ``List.map | ``List.mapTR => some "list(map({}, {}))"  -- special format
  | ``List.filterMap | ``List.filterMapTR => some "[y for x in {} if (y := {}(x)) is not None]"
  | ``List.find? => some "next((x for x in {} if {}(x)), None)"
  | ``List.any => some "any({} for x in {})"  -- special
  | ``List.all => some "all({} for x in {})"  -- special
  | ``List.eraseDups => some "list(dict.fromkeys({}))"
  | ``List.zipIdx => some "list(enumerate({}))"
  | ``List.zip => some "list(zip({}, {}))"
  | ``List.unzip => some "(lambda xs: (list(map(lambda x: x[0], xs)), list(map(lambda x: x[1], xs))))"
  | ``List.intersperse => some "(lambda sep, xs: [y for x in xs for y in [x, sep]][:-1] if xs else [])"
  | ``List.intercalate => some "sep.join"
  -- List.foldl and foldr handled specially in emitLetValue for correct argument order
  -- | ``List.foldl => some "functools.reduce"
  -- | ``List.foldr => some "..."

  -- Array to list
  | ``Array.toList => some "list"
  | ``List.toArray => some "list"  -- Python lists are arrays

  -- Nat/Int operations
  | ``Nat.succ => some "(lambda n: n + 1)"
  | ``Nat.pred => some "(lambda n: max(0, n - 1))"
  | ``Nat.min => some "min"
  | ``Nat.max => some "max"
  | ``Int.natAbs => some "abs"

  -- Bool operations
  | ``bne => some "(lambda a, b: a != b)"
  | ``xor => some "(lambda a, b: a != b)"  -- xor for bools

  -- Sorting (using string match below since qsort may be in different namespaces)

  | _ =>
    -- Check by string for namespaced variants
    let s := name.toString
    if s.endsWith ".toList" then some "list"
    else if s.endsWith ".toArray" then some "list"
    else if s.endsWith ".isDigit" then some "str.isdigit"
    else if s.endsWith ".isLower" then some "str.islower"
    else if s.endsWith ".isUpper" then some "str.isupper"
    else if s.endsWith ".isAlpha" then some "str.isalpha"
    else if s.endsWith ".isSome" then some "(lambda x: x is not None)"
    else if s.endsWith ".isNone" then some "(lambda x: x is None)"
    else if s.endsWith ".succ" then some "(lambda n: n + 1)"
    else if s.endsWith ".dropLast" then some "(lambda xs: xs[:-1])"
    else if s.endsWith ".getLast!" || s.endsWith ".getLast?" then some "(lambda xs: xs[-1] if xs else None)"
    else if s.endsWith ".eraseDups" then some "list(dict.fromkeys({}))"
    else if s.endsWith ".filterMap" then some "[y for x in {} if (y := {}(x)) is not None]"
    else if s.endsWith ".find?" || s.endsWith ".find" then some "next((x for x in {} if {}(x)), None)"
    else if s.endsWith ".bne" then some "(lambda a, b: a != b)"
    else none

/-- String append operation -/
def isStringAppend (name : Name) : Bool :=
  name == ``String.append || name == ``HAppend.hAppend || name == ``Append.append

/-- Check if this is a decidable comparison -/
def isDecidableCompare (name : Name) : Option String :=
  let s := name.toString
  if s.startsWith "Nat.decLt" || s.startsWith "Int.decLt" then some "<"
  else if s.startsWith "Nat.decLe" || s.startsWith "Int.decLe" then some "<="
  else if s.startsWith "Nat.decEq" || s.startsWith "Int.decEq" || name == ``instDecidableEqNat then some "=="
  -- Any derived / user `DecidableEq T` decision procedure is an equality test.
  -- `deriving DecidableEq` produces `T.decEq` and the instance `instDecidableEqT`
  -- (also `.decEq` as a trailing component for namespaced types); the LCNF call
  -- site passes the two operands, so we render it as `a == b`.  Without this,
  -- a comparison on a user enum/structure falls through to the generic
  -- `instDecidable*` alias-to-first-arg path, which drops the boolean scrutinee.
  else if s.endsWith ".decEq" || s.startsWith "instDecidableEq"
          || containsSubstr s ".instDecidableEq" then some "=="
  else none

/-- Check if this is a BEq operation -/
def isBEqOp (name : Name) : Bool :=
  name == ``BEq.beq || name.toString == "beq"

/-- `!=` operators (`bne`, and `xor` on Bool coincides with `!=`).  When applied
    to two operands these must render inline as `a != b`; the `stdlibFnToPython?`
    lambda form is only a fallback for `bne` used as a first-class value. -/
def isBNeOp (name : Name) : Bool :=
  name == ``bne || name == ``xor || name.toString == "bne"
  || name.toString.endsWith ".bne"

/-- Proof-level equality casts that are the identity on their carried value at
    runtime.  They leak into LCNF from `partial`/well-founded definitions (the
    motive rewrite around a recursive call).  Erasing them to their data
    argument is semantics-preserving; leaving them emits a call to an undefined
    `eq_ndrec`/`eq_mpr` name.  For all of these the carried value is the first
    non-type/non-proof (i.e. first fvar) argument. -/
def isIdentityCast (name : Name) : Bool :=
  name == ``Eq.ndrec || name == ``Eq.ndrec_symm || name == ``Eq.mpr
  || name == ``Eq.mp || name == ``Eq.rec || name == ``Eq.recOn
  || name == ``cast || name == ``Eq.subst

/-- Numeric coercions that are the identity in Python (Nat and Int are both
    `int`): the `Nat → Int` coercion `Nat.cast` / `NatCast.natCast` and its
    `Int.ofNat` spelling.  Unlike the proof casts above, the carried value is
    the LAST argument (these take `[type?, instance, value]`), so we alias to
    the last fvar rather than the first-after-types. -/
def isNumericCast (name : Name) : Bool :=
  name == ``Nat.cast || name == ``NatCast.natCast || name == ``Int.ofNat
  || name.toString.endsWith ".natCast"

/-- Check if name looks like a decide call -/
def isDecide (name : Name) : Bool :=
  name == ``decide || name == ``Decidable.decide || name.toString.startsWith "decide"

/-- Get the Python operator for operations accessed through HAdd, HMul, etc. -/
def hOpToPyOp? (instName : Name) : Option String :=
  match instName with
  | ``instHAdd | ``instAddNat => some "+"
  | ``instHSub | ``instSubNat => some "-"
  | ``instHMul | ``instMulNat => some "*"
  | ``instHDiv => some "//"
  | ``instHMod => some "%"
  | ``instHPow => some "**"
  | ``instBEqOfDecidableEq => some "=="
  | _ =>
    -- Match by string for variants
    let s := instName.toString
    if s.startsWith "instHAppend" || s.startsWith "instAppend" ||
       containsSubstr s ".instHAppend" || containsSubstr s ".instAppend" then some "+"
    else if s.startsWith "instBEq" || containsSubstr s ".instBEq" then some "=="
    else if s.startsWith "instDecidableLt" || s.startsWith "instLT" ||
            containsSubstr s ".instDecidableLt" || containsSubstr s ".instLT" then some "<"
    else if s.startsWith "instDecidableLe" || s.startsWith "instLE" ||
            containsSubstr s ".instDecidableLe" || containsSubstr s ".instLE" then some "<="
    else if s.startsWith "instNeg" || containsSubstr s ".instNeg" then some "unary-"  -- unary negation marker
    else none

/-! ## String Quoting -/

def hexDigit (n : Nat) : Char :=
  if n < 10 then Char.ofNat (n + '0'.toNat)
  else Char.ofNat (n - 10 + 'a'.toNat)

def quotePyString (s : String) : String :=
  let escaped := s.foldl (fun acc c =>
    acc ++ match c with
      | '\n' => "\\n"
      | '\r' => "\\r"
      | '\t' => "\\t"
      | '\\' => "\\\\"
      | '"' => "\\\""
      | c => if c.toNat < 32 then
               s!"\\x{String.mk [hexDigit (c.toNat / 16), hexDigit (c.toNat % 16)]}"
             else String.singleton c
  ) ""
  "\"" ++ escaped ++ "\""

/-! ## Literal Emission -/

def emitLitValue (lit : LitValue) : EmitM Unit := do
  match lit with
  | .nat n => emit (toString n)
  | .str s => emit (quotePyString s)
  | .uint8 v => emit (toString v.toNat)
  | .uint16 v => emit (toString v.toNat)
  | .uint32 v => emit (toString v.toNat)
  | .uint64 v => emit (toString v.toNat)
  | .usize v => emit (toString v.toNat)

/-- Pure string form of a literal value (for expression-mode rendering). -/
def litValueStr (lit : LitValue) : String :=
  match lit with
  | .nat n => toString n
  | .str s => quotePyString s
  | .uint8 v => toString v.toNat
  | .uint16 v => toString v.toNat
  | .uint32 v => toString v.toNat
  | .uint64 v => toString v.toNat
  | .usize v => toString v.toNat

/-! ## Argument Emission -/

def emitArg (arg : Arg) : EmitM Unit := do
  match arg with
  | .fvar fvarId =>
    let fvarId ← resolveAlias fvarId
    -- Check if this is a known literal
    if let some lit := (← get).literalVars[fvarId]? then
      emitLitValue lit
    else if let some b := (← get).boolVars[fvarId]? then
      emit (if b then "True" else "False")
    else if let some e := (← get).exprVars[fvarId]? then
      emit e
    else if let some (param, body) := (← get).deferredLambdas[fvarId]? then
      -- A deferred lambda used as a plain value: materialize it.
      emit s!"(lambda {param}: {body})"
    else if (← get).instanceVars.contains fvarId then
      -- A typeclass-instance var passed as an argument: its binding was elided
      -- (instances aren't emitted), so emit `None` as a placeholder — the callee
      -- ignores it (e.g. the `Inhabited`/decidability arg threaded into
      -- `getElem!`).  Without this it referenced the unbound instance name.
      emit "None"
    else
      emit (← getVarName fvarId)
  | .erased => emit "None"
  | .type _ => emit "None"

def emitArgs (args : Array Arg) (sep : String := ", ") : EmitM Unit := do
  let mut first := true
  for arg in args do
    -- Skip unit arguments
    if let .fvar fvarId := arg then
      if (← get).unitVars.contains fvarId then
        continue
    if !first then emit sep
    first := false
    emitArg arg

/-- Run an emitting action but capture what it appended to the buffer as a
    string (leaving the buffer unchanged).  Lets statement-mode code obtain the
    rendered form of an argument even though `renderArg` is defined later. -/
def captureEmit (act : EmitM Unit) : EmitM String := do
  let before := (← get).buf
  act
  let after := (← get).buf
  modify fun s => { s with buf := before }
  return (after.drop before.length).toString

/-- Is the rendered operand a syntactically nonzero integer literal (e.g. `2`,
    `-3`, `(4)`)?  Such a divisor can never be zero, so a zero-guard is
    unnecessary — and skipping it keeps the common `x % 2` / `x // 10` case clean
    (a guard there also broke the comprehension regression tests).  Conservative:
    anything not obviously a nonzero int literal returns `false` (→ guard). -/
def isNonzeroLiteral (s : String) : Bool :=
  -- strip enclosing parens/whitespace, e.g. "(2)" → "2".
  let t := (s.trim.dropWhile (· == '(')).takeWhile (· != ')') |>.trim
  let digits := if t.startsWith "-" then t.drop 1 else t
  !digits.isEmpty && digits.all Char.isDigit &&
    digits.any (· != '0')  -- at least one nonzero digit ⇒ value ≠ 0

/-- Guard a Python `//` / `%` against a zero divisor.  Lean's `Nat`/`Int`
    division and modulo are TOTAL — `n / 0 = 0` and `n % 0 = n` — whereas
    Python's `//` / `%` raise `ZeroDivisionError`.  We wrap the (possibly
    Euclidean) division expression in a conditional so a zero divisor yields
    Lean's value instead of crashing.  Non-`//`/`%` ops (and provably-nonzero
    literal divisors) pass through unchanged.  `expr` is the full division
    expression to use when `b != 0`; `a`/`b` are the rendered dividend/divisor.
    (Operands are pure in this IR, so re-evaluating `b` in the guard is
    semantics-preserving.) -/
def guardZeroDiv (op expr a b : String) : String :=
  if isNonzeroLiteral b then expr
  else if op == "//" then s!"({expr} if {b} != 0 else 0)"
  else if op == "%" then s!"({expr} if {b} != 0 else {a})"
  else expr

/-- Python expression for a binary op whose semantics differ from Lean's naive
    operator, given the already-rendered operand strings.  Division/modulo forms
    are zero-guarded (Lean division is total; see `guardZeroDiv`) unless the
    divisor is a provably-nonzero literal. -/
def emitArithBinary (kind a b : String) : String :=
  match kind with
  | "natsub" => s!"max(0, {a} - {b})"          -- truncated Nat subtraction
  | "intmod" =>
    if isNonzeroLiteral b then s!"({a} % abs({b}))"
    else s!"({a} % abs({b}) if {b} != 0 else {a})"           -- Euclidean Int modulo (total)
  | "intdiv" =>
    if isNonzeroLiteral b then s!"(({a} - {a} % abs({b})) // {b})"
    else s!"(({a} - {a} % abs({b})) // {b} if {b} != 0 else 0)"  -- Euclidean Int division (total)
  | _        => s!"({a} - {b})"

/-! ## Expression Emission -/

/-- Record a literal value -/
def recordLiteral (lit : LitValue) : EmitM Unit :=
  modify fun s => { s with lastLiteral := some lit }

/-- Mark a variable as holding a literal value -/
def markAsLiteralVar (fvarId : FVarId) (lit : LitValue) : EmitM Unit :=
  modify fun s => { s with literalVars := s.literalVars.insert fvarId lit }

/-- Check if this is an instance construction we should skip -/
def shouldSkipLetDecl (decl : LetDecl) : EmitM Bool := do
  match decl.value with
  | .lit lit =>
    -- Record the literal for OfNat pattern.  Also key it to this fvar so an
    -- `instOfNatNat` built from this literal can recover the RIGHT value later,
    -- instead of relying on the global `lastLiteral`, which an intervening
    -- literal (e.g. the `1` in `6 + 1`) can clobber before the `OfNat.ofNat`
    -- projection is reached.
    recordLiteral lit
    markAsLiteralVar decl.fvarId lit
    return false  -- Don't skip, we'll emit it
  | .const name _ args =>
    -- A decidable *comparison* (Nat/Int/derived `DecidableEq` on a user enum or
    -- structure) is NOT type-class machinery to elide: it produces the boolean
    -- scrutinee for a downstream `if`.  Emit it (return false) so the const
    -- path renders `a == b`.  Recognizing this first is essential — the derived
    -- instance is named e.g. `MyMod.instDecidableEqPState`, which otherwise
    -- matches `isInstanceCtor` (contains `.inst`) and gets skipped, dropping
    -- the comparison and leaving the `if` referencing an unbound name.
    --
    -- BUT only when the two value operands are actually applied here.  A bare
    -- instance value (`instDecidableEqNat` with no value args, later fed to a
    -- separate `decide`) has no operands to compare and must still be skipped;
    -- emitting it produced a dangling nullary call like `inst_decidable_eq_nat()`.
    let valArgCount := (args.filter (fun a => match a with
      | .fvar _ => true | _ => false)).size
    if (isDecidableCompare name).isSome && valArgCount >= 2 then
      return false
    -- Identity equality casts (`Eq.ndrec`, `Eq.mpr`, …): alias to the carried
    -- value and skip, so the cast disappears at runtime.  These consts take
    -- their type/motive arguments first, then the data value, then (erased)
    -- index/proof arguments.  The data value is therefore the first fvar that
    -- appears AFTER the last `.type` argument — not merely the first fvar,
    -- which would wrongly pick an index like `a` in `motive a`.
    if isIdentityCast name then
      let mut lastType := 0
      for h : i in [0:args.size] do
        if let .type _ := args[i] then lastType := i + 1
      let mut aliased := false
      for h : i in [0:args.size] do
        if i >= lastType && !aliased then
          if let .fvar fv := args[i] then
            aliasVar decl.fvarId fv
            aliased := true
      return true
    -- Numeric coercion (Nat → Int): identity in Python.  Alias to the LAST
    -- fvar argument (the coerced value); the earlier fvar is the typeclass
    -- instance, which must not be picked.
    if isNumericCast name then
      let mut last : Option FVarId := none
      for arg in args do
        if let .fvar fv := arg then last := some fv
      if let some fv := last then
        aliasVar decl.fvarId fv
      return true
    -- `instDecidableNot` is the decision for `¬p` (e.g. the `≠` in `a ≠ b`).
    -- It must NOT be skipped/aliased to its inner decidable — that silently
    -- drops the negation and collapses `≠` to `=`.  Emit it so the const path
    -- can render `not <inner>`.
    if name == ``instDecidableNot then
      return false
    -- Special case: instDecidable* with fvar args should alias to the first fvar
    -- This handles patterns like `if boolExpr then ...`
    let nameStr := name.toString
    if nameStr.startsWith "instDecidable" then
      for arg in args do
        if let .fvar fv := arg then
          aliasVar decl.fvarId fv
          return true
      -- No fvar found, fall through to normal instance handling
    if isInstanceCtor name then
      -- Skip all instance constructors - they are type class machinery
      -- GetElem instances will be inlined at projection site
      markAsInstance decl.fvarId name
      -- An `OfNat` instance carries its literal among its fvar arguments
      -- (`instOfNatNat` for `Nat`; `instOfNat` for `Int` and others, which may
      -- wrap it via a nested OfNat instance).  Capture THAT literal against the
      -- instance fvar, so the later `OfNat.ofNat` projection recovers the
      -- correct value even if another literal was bound in between (which would
      -- clobber the global `lastLiteral`).  Scanning all fvar args covers both
      -- the direct-literal and nested-instance cases.
      if name == ``instOfNatNat || nameStr.startsWith "instOfNat"
         || containsSubstr nameStr ".instOfNat" then
        for arg in args do
          if let .fvar fv := arg then
            if let some lit := (← get).literalVars[fv]? then
              markAsLiteralVar decl.fvarId lit
      -- Track arithmetic whose Python operator differs from Lean's semantics:
      -- Nat truncated subtraction, and Euclidean Int division/modulo.  The
      -- concrete instance (`instSubNat` / `Int.instDiv` / `Int.instMod`) fixes
      -- the kind; the generic `instH*` wrapper built from it carries that fvar
      -- among its args, so propagate the tag through it.
      let concreteKind : Option String :=
        if name == ``instSubNat then some "natsub"
        else if name == ``Int.instDiv then some "intdiv"
        else if name == ``Int.instMod then some "intmod"
        else none
      match concreteKind with
      | some k => markArith decl.fvarId k
      | none =>
        if name == ``instHSub || name == ``instHDiv || name == ``instHMod then
          for arg in args do
            if let .fvar fv := arg then
              if let some k := ← arithOf fv then markArith decl.fvarId k
      return true
    return false
  | .proj _ idx fvarId =>
    -- Check if projecting from an instance
    if let some instName := (← get).instanceVars[fvarId]? then
      -- Special case: projecting from OfNat gives us the literal value
      let instStr := instName.toString
      if instName == ``instOfNatNat || instStr.startsWith "instOfNat" || containsSubstr instStr ".instOfNat" then
        -- Prefer the literal captured against this specific OfNat instance;
        -- fall back to `lastLiteral` only if we didn't capture one.
        if let some lit := (← get).literalVars[fvarId]? then
          markAsLiteralVar decl.fvarId lit
          return true
        if let some lit := (← get).lastLiteral then
          markAsLiteralVar decl.fvarId lit
          return true  -- Skip this, but the var is now a known literal
      -- Check if this is a known arithmetic operator we can inline
      if hOpToPyOp? instName |>.isSome then
        markAsExtractedOp decl.fvarId instName idx
        -- Propagate the arithmetic-kind tag from the instance to the projected op.
        if let some k := ← arithOf fvarId then markArith decl.fvarId k
        return true
      -- For other instance projections (like GetElem?), don't skip
      -- We'll emit them as function calls
      return false
    return false
  | _ => return false

/-- Try to emit as an inlined operation (for calls through extracted instance ops) -/
def tryEmitInlinedOp (varName : String) (fnVar : FVarId) (args : Array Arg) : EmitM Bool := do
  let st ← get
  -- Check if fnVar is an extracted operation
  if let some (instName, _) := st.extractedOps[fnVar]? then
    if let some op := hOpToPyOp? instName then
      -- Self-coverage: typeclass-instance operator path.  Most arithmetic
      -- (`a + b`, `a * b`, …) lowers through here via `instHAdd`/`instHMul`
      -- extraction, NOT through the `const.Nat.add` special case — so this is
      -- where addition/multiplication/etc. actually get measured.  Tag by the
      -- Python operator (the meaningful handler identity).
      markHandler s!"hop.{op}"
      -- Handle unary negation
      if op == "unary-" && args.size == 1 then
        emitIndent
        emit s!"{varName} = -"
        emitArg args[0]!
        emit "\n"
        return true
      -- Handle binary operations
      if args.size == 2 then
        -- Arithmetic whose Python operator differs from Lean's semantics
        -- (Nat truncated subtraction; Euclidean Int division/modulo).
        if let some kind := ← arithOf fnVar then
          let a ← captureEmit (emitArg args[0]!)
          let b ← captureEmit (emitArg args[1]!)
          emitIndent
          emit s!"{varName} = {emitArithBinary kind a b}\n"
          return true
        let a ← captureEmit (emitArg args[0]!)
        let b ← captureEmit (emitArg args[1]!)
        emitIndent
        -- Nat/Int `//` and `%` are total in Lean; guard against zero divisor.
        emit s!"{varName} = {guardZeroDiv op s!"({a} {op} {b})" a b}\n"
        return true
  return false

/-! ## Expression-mode rendering (for inlining lambda bodies into comprehensions)

`renderExprCode` attempts to render a lambda body — an LCNF let-chain ending in
`return` — as a single Python expression string, e.g. `x + 1` or `x % 2 == 0`.
It returns `none` for anything that is not a simple expression (nested
functions, pattern matches, projections we don't understand), in which case the
caller falls back to emitting a real `def`. It deliberately mirrors the subset
of `emitLetValue` that produces pure expressions. -/

/-- String form of an argument, resolving literals / bools / already-rendered
    expression vars / deferred lambdas / plain variable names. -/
def renderArg (arg : Arg) : EmitM String := do
  match arg with
  | .fvar fvarId =>
    let fvarId ← resolveAlias fvarId
    let st ← get
    if let some lit := st.literalVars[fvarId]? then
      return litValueStr lit
    else if let some b := st.boolVars[fvarId]? then
      return (if b then "True" else "False")
    else if let some e := st.exprVars[fvarId]? then
      return e
    else if let some (param, body) := st.deferredLambdas[fvarId]? then
      return s!"(lambda {param}: {body})"
    else if st.instanceVars.contains fvarId then
      -- Elided instance var passed as an argument (see `emitArg`): `None`.
      return "None"
    else
      return (← getVarName fvarId)
  | .erased => return "None"
  | .type _ => return "None"

/-- Render the (possibly filtered) argument list of a call as `a, b, c`,
    skipping unit fvars, exactly like `emitArgs`. -/
def renderArgs (args : Array Arg) : EmitM String := do
  let mut parts : Array String := #[]
  for arg in args do
    if let .fvar fvarId := arg then
      if (← get).unitVars.contains fvarId then
        continue
    parts := parts.push (← renderArg arg)
  return ", ".intercalate parts.toList

/-- True when a `.const` call can be safely inlined as `pyName(args)` in
    expression position: it maps through `stdlibFnToPython?` to a self-contained
    Python callable (no `{}` format placeholder, no `lambda`/paren wrapper that
    would need special call handling). This deliberately excludes constructors
    and specially-handled ops (`List.cons`, `bne`, `OfNat`, `List.contains`, …)
    so those lambdas fall back to a real `def` instead of an undefined name. -/
def isConstFnSafeToInline (declName : Name) : Bool :=
  match stdlibFnToPython? declName with
  | some py => !(containsSubstr py "{}") && !(containsSubstr py "(") && !(containsSubstr py " ")
  | none => false

/-- Try to render a `let`-bound value as a Python expression string. Returns
    `none` if the value isn't a simple expression we can inline. Mutating
    side-effects (literal/instance/op tracking) mirror `emitLetValue`. -/
partial def renderLetValueExpr (decl : LetDecl) : EmitM (Option String) := do
  match decl.value with
  | .lit v =>
    recordLiteral v
    return some (litValueStr v)
  | .erased => return none
  | .const declName _ args =>
    let constNameStr := declName.toString (escape := false)
    if constNameStr == "Ordering.lt" then return some "-1"
    if constNameStr == "Ordering.eq" then return some "0"
    if constNameStr == "Ordering.gt" then return some "1"
    if declName == ``Nat.succ then
      if args.size >= 1 then
        return some s!"({← renderArg args[args.size - 1]!} + 1)"
    -- `Int.toNat` clamps negatives to 0 (it is monus-like, not identity).
    if declName == ``Int.toNat then
      if args.size >= 1 then
        return some s!"max(0, {← renderArg args[args.size - 1]!})"
    if let some op := natBinOp? declName then
      if args.size == 2 then
        -- `Nat.sub` is truncated subtraction (saturates at 0).
        if declName == ``Nat.sub then
          return some s!"max(0, {← renderArg args[0]!} - {← renderArg args[1]!})"
        let a ← renderArg args[0]!
        let b ← renderArg args[1]!
        -- Nat/Int `//` and `%` are total in Lean (n/0=0, n%0=n); guard them.
        return some (guardZeroDiv op s!"({a} {op} {b})" a b)
    if let some fn := builtinFn? declName then
      if args.size >= 1 then
        let a ← renderArg args[args.size - 1]!
        if fn == "not" then return some s!"(not {a})"
        else if fn == "-" then return some s!"(-{a})"
        else return some s!"{fn}({a})"
    if isStringAppend declName then
      if args.size >= 2 then
        return some s!"({← renderArg args[args.size - 2]!} + {← renderArg args[args.size - 1]!})"
    if isBEqOp declName then
      if args.size >= 2 then
        modify fun s => { s with lastCompareVar := some decl.fvarId }
        return some s!"({← renderArg args[args.size - 2]!} == {← renderArg args[args.size - 1]!})"
    if isBNeOp declName then
      if args.size >= 2 then
        modify fun s => { s with lastCompareVar := some decl.fvarId }
        return some s!"({← renderArg args[args.size - 2]!} != {← renderArg args[args.size - 1]!})"
    if let some op := isDecidableCompare declName then
      if args.size >= 2 then
        modify fun s => { s with lastCompareVar := some decl.fvarId }
        return some s!"({← renderArg args[args.size - 2]!} {op} {← renderArg args[args.size - 1]!})"
    if isDecide declName then
      -- decide wraps its decidable arg; alias to it and expose no new expr.
      for arg in args do
        if let .fvar fv := arg then
          aliasVar decl.fvarId fv
          return some ""  -- sentinel: aliased, nothing to bind
      return none
    -- A user/library function we recognize as a plain Python callable name and
    -- that takes no special-cased argument shape: `stdlibFnToPython?` entries
    -- with no `{}` format string, plus locally-defined declarations. Anything
    -- else (constructors like `List.cons`, `OfNat`, `bne`, `List.contains`, …
    -- which `emitLetValue` handles specially) we conservatively decline, so the
    -- lambda falls back to a proper `def` rather than calling an undefined name.
    if let some py := stdlibFnToPython? declName then
      if isConstFnSafeToInline declName then
        return some s!"{py}({← renderArgs args})"
    return none
  | .fvar fnVar args =>
    -- Extracted instance operation inlined as an operator.
    let st ← get
    if let some (instName, _) := st.extractedOps[fnVar]? then
      if let some op := hOpToPyOp? instName then
        -- Self-coverage: instance-op path in expression mode (inlined lambda
        -- bodies).  Same handler family as `tryEmitInlinedOp`; tag identically.
        markHandler s!"hop.{op}"
        if op == "unary-" && args.size == 1 then
          return some s!"(-{← renderArg args[0]!})"
        if args.size == 2 then
          -- Arithmetic whose Python operator differs from Lean's semantics.
          if let some kind := ← arithOf fnVar then
            return some (emitArithBinary kind (← renderArg args[0]!) (← renderArg args[1]!))
          let a ← renderArg args[0]!
          let b ← renderArg args[1]!
          return some (guardZeroDiv op s!"({a} {op} {b})" a b)
    -- Call of a (possibly deferred-lambda) function variable.
    if args.size == 0 then
      -- Value alias.
      aliasVar decl.fvarId fnVar
      return some ""
    -- A deferred single-param lambda applied here: materialize and apply it.
    if let some (param, body) := st.deferredLambdas[fnVar]? then
      return some s!"(lambda {param}: {body})({← renderArgs args})"
    -- Otherwise only inline a call to an ALREADY-BOUND function.  An unbound
    -- fvar is an unemitted local function (e.g. a match-arm continuation); its
    -- raw name would be `_uniq_NNN` — never defined.  Fail the render so the
    -- enclosing lambda falls back to a real `def` (which emits that function).
    match ← knownVarName? fnVar with
    | some name => return some s!"{name}({← renderArgs args})"
    | none => return none
  | .proj typeName idx structFvar =>
    -- Only tuple projections are safe to inline as expressions.
    if typeName == ``Prod then
      return some s!"{← getVarName structFvar}[{idx}]"
    return none

/-- Render a lambda body (`Code`) as a single Python expression, or `none`. -/
partial def renderExprCode (code : Code) : EmitM (Option String) := do
  match code with
  | .let decl k =>
    let _ ← registerVar decl.fvarId decl.binderName
    markBoolTyped decl.fvarId decl.type
    if ← shouldSkipLetDecl decl then
      return (← renderExprCode k)
    match ← renderLetValueExpr decl with
    | none => return none
    | some e =>
      -- "" is the alias sentinel (decide / value alias): bind nothing.
      if e != "" then
        modify fun s => { s with exprVars := s.exprVars.insert decl.fvarId e }
      renderExprCode k
  | .return fvarId =>
    let fvarId ← resolveAlias fvarId
    let st ← get
    if let some lit := st.literalVars[fvarId]? then
      return some (litValueStr lit)
    else if let some b := st.boolVars[fvarId]? then
      return some (if b then "True" else "False")
    else if let some e := st.exprVars[fvarId]? then
      return some e
    else if let some (param, body) := st.deferredLambdas[fvarId]? then
      return some s!"(lambda {param}: {body})"
    else
      -- Only render a reference to an ALREADY-BOUND variable.  If the fvar names
      -- an unemitted local function (common when a match arm is a call to a
      -- sibling continuation), rendering it would emit `_uniq_NNN(...)` for a
      -- name that never gets defined — so fail the render and let `emitLocalFun`
      -- fall back to a real `def` (which emits that inner function properly).
      match ← knownVarName? fvarId with
      | some name => return some name
      | none => return none
  -- Anything else (nested funs, cases, jumps) is not a simple expression.
  | _ => return none

/-- For a function argument to a comprehension-producing combinator, return the
    `(binder, body)` pair to splice into the comprehension. If the argument is a
    deferred single-param lambda, its body is inlined and its own parameter name
    is used as the binder (`[x + 1 for x in xs]`). Otherwise we fall back to
    applying the function to a fresh binder (`[f(x) for x in xs]`). -/
def fnCompParts (fnArg : Arg) (fallbackBinder : String) : EmitM (String × String) := do
  if let .fvar fv := fnArg then
    let fv ← resolveAlias fv
    if let some (param, body) := (← get).deferredLambdas[fv]? then
      return (param, body)
  let f ← renderArg fnArg
  return (fallbackBinder, s!"{f}({fallbackBinder})")

/-- Render a "dedup / to-set" operation on a list argument as a Python set
    comprehension. If the argument was itself produced by a `map`/`filter`
    comprehension (recorded in `listCompInner`), fuse into a single set
    comprehension `{f(x) for x in xs}`; otherwise emit `{v for v in xs}`. -/
def setCompFromArg (listArg : Arg) : EmitM String := do
  let lbrace := "{"
  let rbrace := "}"
  if let .fvar fv := listArg then
    let fv ← resolveAlias fv
    if let some inner := (← get).listCompInner[fv]? then
      -- If the list comprehension we're fusing was the immediately preceding
      -- statement (buffer untouched since), drop that now-dead line.
      match (← get).lastListComp with
      | some (lastFv, start, stop) =>
        if lastFv == fv && stop == (← get).buf.length then
          modify fun s => { s with buf := (s.buf.take start).toString, lastListComp := none }
      | none => pure ()
      return lbrace ++ inner ++ rbrace
  let xs ← renderArg listArg
  return lbrace ++ s!"_v for _v in {xs}" ++ rbrace

partial def emitLetValue (decl : LetDecl) : EmitM Unit := do
  -- Register the variable with its binder name
  let varName ← registerVar decl.fvarId decl.binderName

  -- Record Bool-typed lets so a condition computed into a let still takes the
  -- correct (non-swapped) Decidable-cases branch order. See markBoolTyped.
  markBoolTyped decl.fvarId decl.type

  -- Skip instance-related bindings
  if ← shouldSkipLetDecl decl then
    return

  match decl.value with
  | .lit v =>
    -- Record the literal - if it's used by OfNat, we'll inline it and not need this var
    recordLiteral v
    -- We'll emit it, but if it turns out to be unused (only via OfNat), it's harmless
    -- For cleaner output, we could track usage but for now just emit
    emitIndent
    emit s!"{varName} = "
    emitLitValue v
    emit "\n"
  | .erased =>
    -- Skip erased values entirely
    return
  | .const declName _ args =>
    -- Self-coverage: tag which handler this const dispatches to.  Every special
    -- handler below is keyed by `declName`, so `const.<declName>` uniquely
    -- identifies it — one robust tag instead of ~60 hand-placed ones at each
    -- `return` (which risks under-reporting on a missed return).  The report
    -- intersects fired tags with a curated watchlist, so user-function callees
    -- (which also land here via the generic fallback) are ignored.
    markHandler s!"const.{declName.toString (escape := false)}"
    -- Handle Ordering constructors FIRST before any other checks
    let constNameStr := declName.toString (escape := false)
    if constNameStr == "Ordering.lt" then
      emitIndent
      emit s!"{varName} = -1\n"
      return
    if constNameStr == "Ordering.eq" then
      emitIndent
      emit s!"{varName} = 0\n"
      return
    if constNameStr == "Ordering.gt" then
      emitIndent
      emit s!"{varName} = 1\n"
      return
    -- Check for Nat.succ (n + 1)
    if declName == ``Nat.succ || declName.toString == "Nat.succ" then
      if args.size >= 1 then
        emitIndent
        emit s!"{varName} = "
        emitArg args[args.size - 1]!
        emit " + 1\n"
        return
    -- `Int.toNat` clamps negatives to 0.
    if declName == ``Int.toNat then
      if args.size >= 1 then
        emitIndent
        emit s!"{varName} = max(0, "
        emitArg args[args.size - 1]!
        emit ")\n"
        return
    -- Check for direct Nat/Int binary operations
    if let some op := natBinOp? declName then
      if args.size == 2 then
        -- `Nat.sub` is truncated subtraction (saturates at 0).
        if declName == ``Nat.sub then
          emitIndent
          emit s!"{varName} = "
          emit "max(0, "
          emitArg args[0]!
          emit " - "
          emitArg args[1]!
          emit ")\n"
          return
        let a ← captureEmit (emitArg args[0]!)
        let b ← captureEmit (emitArg args[1]!)
        emitIndent
        -- Nat/Int `//` and `%` are total in Lean (n/0=0, n%0=n); guard them.
        emit s!"{varName} = {guardZeroDiv op s!"({a} {op} {b})" a b}\n"
        return
    -- Check for builtin functions (len, not, etc.)
    if let some fn := builtinFn? declName then
      if args.size >= 1 then
        emitIndent
        emit s!"{varName} = "
        -- For `not`, don't use parentheses
        if fn == "not" then
          emit s!"not "
          emitArg args[args.size - 1]!
        else if fn == "-" then
          -- Unary minus
          emit "-"
          emitArg args[args.size - 1]!
        else
          emit s!"{fn}("
          emitArg args[args.size - 1]!
          emit ")"
        emit "\n"
        return
    -- Check for string append
    if isStringAppend declName then
      -- String append args: [type, inst, s1, s2] - use last two
      if args.size >= 2 then
        emitIndent
        emit s!"{varName} = "
        emitArg args[args.size - 2]!
        emit " + "
        emitArg args[args.size - 1]!
        emit "\n"
        return
    -- Check for BEq operations (x == y)
    if isBEqOp declName then
      -- BEq.beq args: [type, inst, x, y]
      if args.size >= 2 then
        emitIndent
        emit s!"{varName} = "
        emitArg args[args.size - 2]!
        emit " == "
        emitArg args[args.size - 1]!
        emit "\n"
        modify fun s => { s with lastCompareVar := some decl.fvarId }
        return
    if isBNeOp declName then
      -- bne args: [type, inst, x, y]
      if args.size >= 2 then
        emitIndent
        emit s!"{varName} = "
        emitArg args[args.size - 2]!
        emit " != "
        emitArg args[args.size - 1]!
        emit "\n"
        modify fun s => { s with lastCompareVar := some decl.fvarId }
        return
    -- Check for decidable comparisons
    if let some op := isDecidableCompare declName then
      if args.size >= 2 then
        emitIndent
        emit s!"{varName} = "
        emitArg args[args.size - 2]!
        emit s!" {op} "
        emitArg args[args.size - 1]!
        emit "\n"
        -- Track this as the last comparison variable
        modify fun s => { s with lastCompareVar := some decl.fvarId }
        return
    -- Check for decide wrapper
    if isDecide declName then
      -- decide takes [prop, decidable] - the decidable is the comparison result
      -- Find the fvar argument (skip erased/type args)
      for arg in args do
        if let .fvar fv := arg then
          aliasVar decl.fvarId fv
          return
      -- Fallback: use lastCompareVar
      if let some lastVar := (← get).lastCompareVar then
        aliasVar decl.fvarId lastVar
      return
    -- `instDecidableNot` decides `¬p`: render `not <inner decidable>` so a
    -- comparison like `a ≠ b` (which is `¬(a = b)`) keeps its negation.
    if declName == ``instDecidableNot then
      -- The last fvar arg is the inner decidable (the `a = b` result).
      let mut inner : Option FVarId := none
      for arg in args do
        if let .fvar fv := arg then inner := some fv
      if let some fv := inner then
        let innerName ← getVarName (← resolveAlias fv)
        emitIndent
        emit s!"{varName} = not {innerName}\n"
        modify fun s => { s with boolVars := s.boolVars.insert decl.fvarId true }
        return
    -- Check for instDecidableEqBool(x, true) or instDecidableEqBool(x, false)
    -- This pattern appears in `if boolExpr then ...`
    let declStr := declName.toString
    if declStr.startsWith "instDecidable" && args.size >= 2 then
      -- The first fvar arg is the bool expression
      for arg in args do
        if let .fvar fv := arg then
          -- Alias to the first fvar (the bool expression)
          aliasVar decl.fvarId fv
          return
      return
    -- Special constructors
    if declName == ``Bool.true then
      modify fun s => { s with boolVars := s.boolVars.insert decl.fvarId true }
      emitIndent
      emit s!"{varName} = True\n"
      return
    if declName == ``Bool.false then
      modify fun s => { s with boolVars := s.boolVars.insert decl.fvarId false }
      emitIndent
      emit s!"{varName} = False\n"
      return
    -- `Decidable.isTrue`/`isFalse` carry a proof, but as a *value* a Decidable
    -- is just its boolean verdict.  When such a constructor is built directly
    -- (e.g. a `decide`-style helper returning `isTrue …`) and later used as an
    -- `if` scrutinee, emitting the raw dataclass (`isTrue(None)`) is always
    -- truthy — silently breaking the branch.  Lower to a real Python bool.
    if declName == ``Decidable.isTrue then
      modify fun s => { s with boolVars := s.boolVars.insert decl.fvarId true }
      emitIndent
      emit s!"{varName} = True\n"
      return
    if declName == ``Decidable.isFalse then
      modify fun s => { s with boolVars := s.boolVars.insert decl.fvarId false }
      emitIndent
      emit s!"{varName} = False\n"
      return
    if declName == ``Unit.unit || declName == ``PUnit.unit then
      -- Track unit values so we can skip them in calls
      modify fun s => { s with unitVars := s.unitVars.insert decl.fvarId }
      return
    -- Option constructors
    if declName == ``Option.some then
      if args.size >= 1 then
        emitIndent
        emit s!"{varName} = "
        emitArg args[args.size - 1]!  -- Skip the type argument
        emit "\n"
        return
    if declName == ``Option.none then
      emitIndent
      emit s!"{varName} = None\n"
      return
    -- List constructors
    if declName == ``List.nil then
      emitIndent
      emit s!"{varName} = []\n"
      return
    if declName == ``List.cons then
      -- cons args: [type, head, tail]
      if args.size >= 2 then
        emitIndent
        emit s!"{varName} = ["
        emitArg args[args.size - 2]!
        emit "] + "
        emitArg args[args.size - 1]!
        emit "\n"
        return
    -- List.headD xs d -> first element or default: (xs[0] if xs else d).
    -- args: [type, list, default]
    if declName == ``List.headD then
      if args.size >= 2 then
        emitIndent
        emit s!"{varName} = ("
        emitArg args[args.size - 2]!
        emit "[0] if "
        emitArg args[args.size - 2]!
        emit " else "
        emitArg args[args.size - 1]!
        emit ")\n"
        return
    -- Prod constructor -> Python tuple
    if declName == ``Prod.mk then
      -- mk args: [type1, type2, fst, snd]
      if args.size >= 2 then
        emitIndent
        emit s!"{varName} = ("
        emitArg args[args.size - 2]!
        emit ", "
        emitArg args[args.size - 1]!
        emit ")\n"
        return
    -- String constructor -> join char list
    if declName == ``String.mk then
      -- mk args: [List Char]
      if args.size >= 1 then
        emitIndent
        emit s!"{varName} = ''.join("
        emitArg args[args.size - 1]!
        emit ")\n"
        return
    -- Check if it's a constructor
    let env ← getEnv
    if let some (.ctorInfo ctorInfo) := env.find? declName then
      -- Skip instance constructors
      if isInstanceCtor ctorInfo.induct then
        return
      emitIndent
      emit s!"{varName} = {toPyTypeName declName}("
      -- Emit exactly the constructor's value fields — the trailing
      -- `numFields` args.  Leading args are type/universe parameters (e.g.
      -- `Decidable.isTrue`'s implicit `{p : Prop}`) which the dataclass does
      -- not declare; emitting them produced `isTrue(None, None)` against a
      -- one-field dataclass and failed at runtime with a TypeError.
      let valArgs := if args.size >= ctorInfo.numFields
                     then args.extract (args.size - ctorInfo.numFields) args.size
                     else args
      emitArgs valArgs
      emit ")\n"
      return
    -- Check for stdlib function mappings
    if let some pyFn := stdlibFnToPython? declName then
      -- Handle simple wrapper functions like len, list, etc.  A `pyFn` that is
      -- a `(lambda …)` or paren/space expression is NOT a bare callable — it
      -- must be emitted by a dedicated special-case below (e.g. take/drop/
      -- reverse); treating it as a unary wrapper `fn(lastArg)` mis-applies it
      -- (`(lambda n, xs: xs[n:])(xs)` — one arg for a two-arg lambda).
      let isBareCallable := !(containsSubstr pyFn "{}")
        && !(containsSubstr pyFn "(") && !(containsSubstr pyFn " ")
      if isBareCallable then
        if args.size >= 1 then
          emitIndent
          emit s!"{varName} = {pyFn}("
          if pyFn == "min" || pyFn == "max" then
            -- Binary stdlib functions (Nat.min/Nat.max -> min/max) take ALL
            -- value operands, not just the last. Emitting only args[size-1]
            -- silently dropped the first operand, producing `min(b)` for
            -- `Nat.min a b`. Filter to the value (fvar) args and emit them all.
            let valArgs := args.filter (fun a => match a with
              | .fvar _ => true | _ => false)
            emitArgs valArgs
          else
            -- Simple unary wrapper: fn(lastArg)  (len, list, ord, chr, ...)
            emitArg args[args.size - 1]!
          emit ")\n"
          return
        else
          -- No arguments - just emit the function/lambda as a value
          -- This handles cases like Char.toUpper used as a function reference
          emitIndent
          emit s!"{varName} = {pyFn}\n"
          return
    -- Special handling for List.map and List.filter - use idiomatic list
    -- comprehensions.  Lean 4.31 lowers `List.map`/`filter`/`filterMap` to their
    -- tail-recursive counterparts (`List.mapTR` etc.) in LCNF, with the same
    -- `(…, f, xs)` argument shape, so we recognize both spellings.
    if declName == ``List.map || declName == ``List.mapTR then
      if args.size >= 2 then
        let (binder, body) ← fnCompParts args[args.size - 2]! "x"
        let xs ← renderArg args[args.size - 1]!
        let inner := s!"{body} for {binder} in {xs}"
        let start := (← get).buf.length
        emitIndent
        emit s!"{varName} = [{inner}]\n"
        modify fun s => { s with
          listCompInner := s.listCompInner.insert decl.fvarId inner
          lastListComp := some (decl.fvarId, start, s.buf.length) }
        return
    if declName == ``List.filter || declName == ``List.filterTR then
      if args.size >= 2 then
        let (binder, body) ← fnCompParts args[args.size - 2]! "x"
        let xs ← renderArg args[args.size - 1]!
        let inner := s!"{binder} for {binder} in {xs} if {body}"
        let start := (← get).buf.length
        emitIndent
        emit s!"{varName} = [{inner}]\n"
        modify fun s => { s with
          listCompInner := s.listCompInner.insert decl.fvarId inner
          lastListComp := some (decl.fvarId, start, s.buf.length) }
        return
    -- List.filterMap - filter + map in one: [y for x in xs if (y := f(x)) is not None]
    if declName == ``List.filterMap || declName == ``List.filterMapTR then
      if args.size >= 2 then
        let (binder, body) ← fnCompParts args[args.size - 2]! "x"
        let xs ← renderArg args[args.size - 1]!
        emitIndent
        emit s!"{varName} = [_y for {binder} in {xs} if (_y := {body}) is not None]\n"
        return
    -- List.bind (flatMap): [y for x in xs for y in f(x)]
    if declName == ``List.flatMap then
      if args.size >= 2 then
        -- bind's function returns a sublist; inline it as the inner iterable.
        let (binder, body) ← fnCompParts args[args.size - 1]! "x"
        let xs ← renderArg args[args.size - 2]!
        emitIndent
        emit s!"{varName} = [_y for {binder} in {xs} for _y in {body}]\n"
        return
    -- List.range - generate range of numbers
    if declName == ``List.range then
      if args.size >= 1 then
        emitIndent
        emit s!"{varName} = list(range("
        emitArg args[args.size - 1]!  -- upper bound
        emit "))\n"
        return
    -- List.foldl - needs argument reordering: foldl f init xs -> reduce(f, xs, init)
    if declName == ``List.foldl then
      -- Lean: List.foldl f init xs (with type args before)
      -- Python: functools.reduce(f, xs, init)
      if args.size >= 3 then
        emitIndent
        emit s!"{varName} = functools.reduce("
        emitArg args[args.size - 3]!  -- f
        emit ", "
        emitArg args[args.size - 1]!  -- xs
        emit ", "
        emitArg args[args.size - 2]!  -- init
        emit ")\n"
        return
    -- List.foldr - foldl with reversed list and swapped function args
    -- (Lean 4.31 lowers `foldr` to the tail-recursive `List.foldrTR`.)
    if declName == ``List.foldr || declName == ``List.foldrTR then
      -- Lean: List.foldr f init xs
      -- Python: functools.reduce(lambda a, b: f(b, a), reversed(xs), init)
      if args.size >= 3 then
        emitIndent
        emit s!"{varName} = functools.reduce(lambda acc, x: "
        emitArg args[args.size - 3]!  -- f
        emit "(x, acc), reversed("
        emitArg args[args.size - 1]!  -- xs
        emit "), "
        emitArg args[args.size - 2]!  -- init
        emit ")\n"
        return
    -- List.all / List.any - check if all/any elements satisfy predicate
    if declName == ``List.all then
      if args.size >= 2 then
        let (binder, body) ← fnCompParts args[args.size - 1]! "x"
        let xs ← renderArg args[args.size - 2]!
        emitIndent
        emit s!"{varName} = all({body} for {binder} in {xs})\n"
        return
    if declName == ``List.any then
      if args.size >= 2 then
        let (binder, body) ← fnCompParts args[args.size - 1]! "x"
        let xs ← renderArg args[args.size - 2]!
        emitIndent
        emit s!"{varName} = any({body} for {binder} in {xs})\n"
        return
    -- List.reverse needs the list argument
    if declName == ``List.reverse then
      if args.size >= 1 then
        emitIndent
        emit s!"{varName} = list(reversed("
        emitArg args[args.size - 1]!
        emit "))\n"
        return
    -- List.take n xs -> xs[:n] / List.drop n xs -> xs[n:].  args: [type, n, xs].
    -- (Lean 4.31 lowers `take` to the tail-recursive `List.takeTR`.)
    if declName == ``List.take || declName == ``List.takeTR
       || declName == ``List.drop then
      if args.size >= 2 then
        let sliceLo := declName == ``List.drop
        emitIndent
        emit s!"{varName} = "
        emitArg args[args.size - 1]!  -- list
        emit "["
        if sliceLo then
          emitArg args[args.size - 2]!  -- xs[n:]
          emit ":"
        else
          emit ":"
          emitArg args[args.size - 2]!  -- xs[:n]
        emit "]\n"
        return
    -- List.dropLast / List.dropLastTR xs -> xs[:-1]  (empty-safe: [][:-1] == []).
    -- args: [type, xs].
    if declName == ``List.dropLast || declName == ``List.dropLastTR then
      if args.size >= 1 then
        emitIndent
        emit s!"{varName} = "
        emitArg args[args.size - 1]!
        emit "[:-1]\n"
        return
    -- List.replicate / List.replicateTR n x -> [x] * n.  args: [type, n, x].
    if declName == ``List.replicate || declName == ``List.replicateTR then
      if args.size >= 2 then
        emitIndent
        emit s!"{varName} = ["
        emitArg args[args.size - 1]!  -- x
        emit "] * "
        emitArg args[args.size - 2]!  -- n
        emit "\n"
        return
    -- List.isPrefixOf p xs -> xs[:len(p)] == p.  args: [type, inst, p, xs].
    if declName == ``List.isPrefixOf then
      if args.size >= 2 then
        let p ← renderArg args[args.size - 2]!
        let xs ← renderArg args[args.size - 1]!
        emitIndent
        emit s!"{varName} = ({xs}[:len({p})] == {p})\n"
        return
    -- List.dropWhile p xs / List.takeWhile p xs — a prefix-based slice by the
    -- predicate.  args: [type, pred, xs].  Emit an itertools call (correct for
    -- either spelling; the predicate may be an inlined lambda via fnCompParts).
    if declName == ``List.dropWhile || declName == ``List.takeWhile then
      if args.size >= 2 then
        let (binder, body) ← fnCompParts args[args.size - 2]! "x"
        let xs ← renderArg args[args.size - 1]!
        let fn := if declName == ``List.takeWhile then "takewhile" else "dropwhile"
        emitIndent
        emit s!"{varName} = list(__import__('itertools').{fn}(lambda {binder}: {body}, {xs}))\n"
        return
    -- getElem? (`l[i]?`) - safe indexing (Lean 4.31 removed `List.get?`;
    -- `l[i]?` now lowers through the generic `getElem?`)
    if declName == ``getElem? then
      if args.size >= 2 then
        emitIndent
        emit s!"{varName} = "
        emitArg args[args.size - 2]!  -- list
        emit "["
        emitArg args[args.size - 1]!  -- index
        emit "] if 0 <= "
        emitArg args[args.size - 1]!
        emit " < len("
        emitArg args[args.size - 2]!
        emit ") else None\n"
        return
    -- List.zipIdx (was List.enum) - enumerate with indices
    if declName == ``List.zipIdx then
      if args.size >= 1 then
        emitIndent
        emit s!"{varName} = list(enumerate("
        emitArg args[args.size - 1]!
        emit "))\n"
        return
    -- List.set - update element at index
    if declName == ``List.set then
      if args.size >= 3 then
        emitIndent
        emit s!"{varName} = "
        emitArg args[args.size - 3]!  -- list
        emit "[:"
        emitArg args[args.size - 2]!  -- index
        emit "] + ["
        emitArg args[args.size - 1]!  -- new value
        emit "] + "
        emitArg args[args.size - 3]!
        emit "["
        emitArg args[args.size - 2]!
        emit "+1:]\n"
        return
    -- List.contains / List.elem - check membership
    if declName == ``List.contains || declName == ``List.elem then
      if args.size >= 2 then
        emitIndent
        emit s!"{varName} = "
        emitArg args[args.size - 1]!  -- element
        emit " in "
        emitArg args[args.size - 2]!  -- list
        emit "\n"
        return
    -- List.isEmpty / String.isEmpty
    if declName == ``List.isEmpty then
      if args.size >= 1 then
        emitIndent
        emit s!"{varName} = len("
        emitArg args[args.size - 1]!
        emit ") == 0\n"
        return
    if declName == ``String.isEmpty then
      if args.size >= 1 then
        emitIndent
        emit s!"{varName} = len("
        emitArg args[args.size - 1]!
        emit ") == 0\n"
        return
    -- Option.bind - flatMap for Option (x >>= f)
    if declName == ``Option.bind || declName.toString (escape := false) == "Option.bind" then
      if args.size >= 2 then
        emitIndent
        emit s!"{varName} = (lambda opt, f: None if opt is None else f(opt))("
        emitArg args[args.size - 2]!  -- option
        emit ", "
        emitArg args[args.size - 1]!  -- function
        emit ")\n"
        return
    -- List.find? - find first element matching predicate
    if declName == ``List.find? then
      if args.size >= 2 then
        let (binder, body) ← fnCompParts args[args.size - 2]! "x"
        let xs ← renderArg args[args.size - 1]!
        emitIndent
        emit s!"{varName} = next(({binder} for {binder} in {xs} if {body}), None)\n"
        return
    -- List.findSome? - find first Some result of f
    if declName == ``List.findSome? then
      if args.size >= 2 then
        let (binder, body) ← fnCompParts args[args.size - 2]! "x"
        let xs ← renderArg args[args.size - 1]!
        emitIndent
        emit s!"{varName} = next((_y for {binder} in {xs} if (_y := {body}) is not None), None)\n"
        return
    -- List.eraseDups / List.toFinset / List.toSet - dedup as a Python set
    -- comprehension, fusing an upstream map/filter comprehension when present.
    -- (eraseDups is a List in Lean; per configuration we model it as set
    -- semantics, so the result is an unordered Python set.)
    let declStr := declName.toString (escape := false)
    if declName == ``List.eraseDups ||
       declStr.endsWith ".toFinset" || declStr.endsWith ".toSet" ||
       declStr == "List.toFinset" || declStr == "List.toSet" then
      if args.size >= 1 then
        let setComp ← setCompFromArg args[args.size - 1]!
        emitIndent
        emit s!"{varName} = {setComp}\n"
        return
    -- List.qsort / List.mergeSort / Array.qsort - sort
    if declName == ``List.mergeSort then
      if args.size >= 2 then
        emitIndent
        emit s!"{varName} = sorted("
        emitArg args[args.size - 1]!  -- list
        emit ", key=functools.cmp_to_key("
        emitArg args[args.size - 2]!  -- comparator
        emit "))\n"
        return
    if declName == ``Array.qsort || declName.toString == "Array.qsort" then
      -- `Array.qsort (as) (lt) (low := 0) (high := as.size - 1)`.  Recent Lean
      -- materializes the two trailing optParams, so the value args are
      -- `[…, as, lt, low, high]`: the array and comparator are the 4th/3rd from
      -- the end, NOT the last two (indexing from the end at -2/-1 would grab
      -- `low`/`high` and emit `sorted(0, key=high(a,b))`).  Fall back to the
      -- 2-arg shape for older Lean versions without the optParams.
      let (arrIdx, cmpIdx) :=
        if args.size >= 4 then (args.size - 4, args.size - 3)
        else (args.size - 2, args.size - 1)
      if args.size >= 2 then
        emitIndent
        emit s!"{varName} = sorted("
        emitArg args[arrIdx]!  -- array (`as`)
        emit ", key=functools.cmp_to_key(lambda a, b: -1 if "
        emitArg args[cmpIdx]!  -- comparator (lt function)
        emit "(a, b) else 1))\n"
        return
    -- Integer square root (use string matching since Nat.sqrt may not exist in all Lean versions)
    if declName.toString == "Nat.sqrt" || declName.toString == "Int.sqrt" then
      if args.size >= 1 then
        emitIndent
        emit s!"{varName} = int("
        emitArg args[args.size - 1]!
        emit " ** 0.5)\n"
        return
    -- Nat.xor - bitwise xor
    if declName == ``Nat.xor then
      if args.size >= 2 then
        emitIndent
        emit s!"{varName} = "
        emitArg args[args.size - 2]!
        emit " ^ "
        emitArg args[args.size - 1]!
        emit "\n"
        return
    -- Char predicates in method-call form (`c.isDigit`, `c.isUpper`, …) lower to
    -- `.const Char.isX` here, NOT the stdlibFnToPython lambda entries (which only
    -- fire when used as bare function values); without these they fell through to
    -- undefined `is_upper(...)`/`is_alpha(...)` etc.  All match Python's `str`
    -- predicates on the ASCII range.
    if declName == ``Char.isDigit then
      if args.size >= 1 then
        emitIndent
        emit s!"{varName} = "
        emitArg args[args.size - 1]!
        emit ".isdigit()\n"
        return
    if let some meth :=
        (if declName == ``Char.isUpper then some "isupper"
         else if declName == ``Char.isLower then some "islower"
         else if declName == ``Char.isAlpha then some "isalpha"
         else if declName == ``Char.isAlphanum then some "isalnum"
         else if declName == ``Char.isWhitespace then some "isspace"
         else none) then
      if args.size >= 1 then
        emitIndent
        emit s!"{varName} = "
        emitArg args[args.size - 1]!
        emit s!".{meth}()\n"
        return
    -- Char.toNat
    if declName == ``Char.toNat then
      if args.size >= 1 then
        emitIndent
        emit s!"{varName} = ord("
        emitArg args[args.size - 1]!
        emit ")\n"
        return
    -- Char.ofNat / Nat.chr
    if declName == ``Char.ofNat then
      if args.size >= 1 then
        emitIndent
        emit s!"{varName} = chr("
        emitArg args[args.size - 1]!
        emit ")\n"
        return
    -- Char.toUpper / Char.toLower — method-call form `c.toUpper` lowers to a
    -- `.const Char.toUpper` here (NOT the stdlibFnToPython lambda entry, which
    -- only fires when used as a bare function value), so it needs its own case;
    -- otherwise it fell through to an undefined `to_upper(...)`.  Lean upcases
    -- only ASCII letters, matching Python `str.upper()` on the ASCII range.
    if declName == ``Char.toUpper then
      if args.size >= 1 then
        emitIndent
        emit s!"{varName} = "
        emitArg args[args.size - 1]!
        emit ".upper()\n"
        return
    if declName == ``Char.toLower then
      if args.size >= 1 then
        emitIndent
        emit s!"{varName} = "
        emitArg args[args.size - 1]!
        emit ".lower()\n"
        return
    -- String.startsWith / endsWith s pat -> Python str.startswith/endswith.
    -- Signature is `{ρ} → String → (pat : ρ) → [ForwardPattern ρ] → Bool`, so the
    -- value args are the string and pattern; the type + Pattern-instance args are
    -- elided (emit as None).  Pick the two String operands by filtering to fvar
    -- args that aren't known instances.
    if declName == ``String.startsWith || declName == ``String.endsWith then
      let meth := if declName == ``String.startsWith then "startswith" else "endswith"
      -- Collect non-instance fvar operands in order: [s, pat].
      let mut ops : Array String := #[]
      for arg in args do
        match arg with
        | .fvar fv =>
          if !((← get).instanceVars.contains fv) then
            ops := ops.push (← renderArg arg)
        | _ => pure ()
      if ops.size >= 2 then
        emitIndent
        emit s!"{varName} = {ops[0]!}.{meth}({ops[1]!})\n"
        return
    -- String.push s c -> s + c  (Lean String.push is functional: returns a new
    -- string).  args: [s, c].  (`stdlibFnToPython?` marks it `none`/"handled
    -- specially" but never had a handler — it fell through to `string_push`.)
    if declName == ``String.push then
      if args.size >= 2 then
        emitIndent
        emit s!"{varName} = "
        emitArg args[args.size - 2]!
        emit " + "
        emitArg args[args.size - 1]!
        emit "\n"
        return
    -- Array.push a x -> a + [x]  (Lean Array.push is functional/persistent, so
    -- emit a non-mutating concat rather than list.append).  args: [type, a, x].
    if declName == ``Array.push then
      if args.size >= 2 then
        emitIndent
        emit s!"{varName} = "
        emitArg args[args.size - 2]!
        emit " + ["
        emitArg args[args.size - 1]!
        emit "]\n"
        return
    -- Array.swapIfInBounds a i j -> swap elements i,j if both in bounds, else a
    -- unchanged (Lean is functional/persistent).  args: [type, a, i, j].  Emit a
    -- non-mutating helper lambda that copies then swaps.
    if declName == ``Array.swapIfInBounds then
      if args.size >= 3 then
        let a ← renderArg args[args.size - 3]!
        let i ← renderArg args[args.size - 2]!
        let j ← renderArg args[args.size - 1]!
        emitIndent
        emit s!"{varName} = (lambda a, i, j: (a if not (0 <= i < len(a) and 0 <= j < len(a)) else [a[j] if k == i else a[i] if k == j else a[k] for k in range(len(a))]))({a}, {i}, {j})\n"
        return
    -- Ordering constructors - always emit as int values
    let nameStr := declName.toString (escape := false)
    if nameStr == "Ordering.lt" then
      emitIndent
      emit s!"{varName} = -1  # Ordering.lt\n"
      return
    if nameStr == "Ordering.eq" then
      emitIndent
      emit s!"{varName} = 0  # Ordering.eq\n"
      return
    if nameStr == "Ordering.gt" then
      emitIndent
      emit s!"{varName} = 1  # Ordering.gt\n"
      return
    -- Check for function references (zero args) that have a Python equivalent
    -- This handles cases like `s.toList.map Char.toNat` where Char.toNat is passed as a function
    if args.size == 0 then
      -- For known stdlib functions, emit the Python function reference
      if declName == ``Char.toNat then
        emitIndent
        emit s!"{varName} = ord\n"
        return
      if declName == ``Char.ofNat then
        emitIndent
        emit s!"{varName} = chr\n"
        return
      -- Char method-style predicates/converters passed as bare function values
      -- (e.g. `s.toList.map Char.toUpper`): emit the matching Python lambda.
      -- Without these entries such refs fell through to an undefined snake-cased
      -- name (`to_upper`, `is_upper`, …).
      if let some lam :=
          (if declName == ``Char.isDigit then some "(lambda c: c.isdigit())"
           else if declName == ``Char.isAlpha then some "(lambda c: c.isalpha())"
           else if declName == ``Char.isUpper then some "(lambda c: c.isupper())"
           else if declName == ``Char.isLower then some "(lambda c: c.islower())"
           else if declName == ``Char.isAlphanum then some "(lambda c: c.isalnum())"
           else if declName == ``Char.isWhitespace then some "(lambda c: c.isspace())"
           else if declName == ``Char.toUpper then some "(lambda c: c.upper())"
           else if declName == ``Char.toLower then some "(lambda c: c.lower())"
           else none) then
        emitIndent
        emit s!"{varName} = {lam}\n"
        return
      if declName == ``Nat.xor then
        emitIndent
        emit s!"{varName} = (lambda a, b: a ^ b)\n"
        return
    -- Regular function call — the generic fallback for any const not handled by
    -- a special case above.  Self-coverage: tag it `fallthrough.<declName>`.  A
    -- *core-namespace* construct (List/Nat/Int/String/Char/Array/Option/…) that
    -- lands here is the fingerprint of a Lean API change silently breaking a
    -- special handler (e.g. a `List.map` → `List.mapImpl` rename): the handler
    -- stops matching, we fall through, and emit a call to an undefined Python
    -- name.  The fuzzer's report flags such fallthroughs so an upgrade can't
    -- regress a handler unnoticed.  (A user function legitimately falling through
    -- to a real Python def is fine — the report only alarms on core namespaces.)
    markHandler s!"fallthrough.{declName.toString (escape := false)}"
    emitIndent
    emit s!"{varName} = {← pyFnName declName}("
    emitArgs args
    emit ")\n"
  | .fvar fnVar args =>
    -- Try to inline instance operations
    if ← tryEmitInlinedOp varName fnVar args then
      return
    -- Check if calling an instance-related var
    -- Note: We used to skip these entirely, but that breaks code that uses the result
    -- For now, emit a function call and rely on having the function defined somewhere
    -- if ← isInstanceRelated fnVar then return
    -- Count non-unit args and total args
    let st ← get
    let mut nonUnitArgs := 0
    for arg in args do
      match arg with
      | .fvar fv => if !st.unitVars.contains fv then nonUnitArgs := nonUnitArgs + 1
      | .erased => pure ()
      | .type _ => pure ()
    -- A deferred single-param lambda referenced as a value (not inlined by a
    -- comprehension): materialize it as a Python `lambda`.
    if let some (param, body) := st.deferredLambdas[fnVar]? then
      emitIndent
      emit s!"{varName} = (lambda {param}: {body})"
      if args.size > 0 then
        emit "("
        emitArgs args
        emit ")"
      emit "\n"
      return
    -- Check for partial application or value assignment
    if let some (_, totalParams) := st.localFnArities[fnVar]? then
      -- If calling with fewer args than total params, it's a partial application
      if args.size < totalParams then
        -- Just assign the function reference
        emitIndent
        emit s!"{varName} = "
        emit (← getVarName fnVar)
        emit "\n"
        return
    else
      -- Not a known function - if 0 args, this is likely a value assignment
      if nonUnitArgs == 0 && args.size == 0 then
        -- Just an alias
        aliasVar decl.fvarId fnVar
        return
    -- Regular function variable call
    emitIndent
    emit s!"{varName} = "
    emit (← getVarName fnVar)
    emit "("
    emitArgs args
    emit ")\n"
  | .proj typeName idx structFvar =>
    -- Check for GetElem?/GetElem projections - inline them as Python indexing
    let typeStr := typeName.toString
    if containsSubstr typeStr "GetElem" then
      -- For GetElem?, project 1 (getElem?) should be safe indexing
      -- Emit a lambda that does bounds-checked indexing
      if idx == 1 then
        markHandler "proj.GetElem?"
        emitIndent
        emit s!"{varName} = (lambda xs, i: xs[i] if 0 <= i < len(xs) else None)\n"
        return
      else if idx == 0 then
        -- Project 0 (valid?) is the validity predicate
        markHandler "proj.GetElem.valid"
        emitIndent
        emit s!"{varName} = (lambda xs, i: 0 <= i < len(xs))\n"
        return
      else if idx == 2 then
        -- Project 2 (`getElem!`) is panic-on-out-of-bounds indexing (`xs[i]!`).
        -- It's called as `f(<Inhabited-inst>, xs, i)` — a leading typeclass arg
        -- precedes the collection & index — so absorb that arg and index
        -- directly.  Lean panics on OOB; Python raises IndexError — both are
        -- errors, so the differential oracle stays consistent.  (Without this,
        -- the projection referenced the elided GetElem instance → undefined
        -- name; F14-adjacent.)
        markHandler "proj.GetElem!"
        emitIndent
        emit s!"{varName} = (lambda _inst, xs, i: xs[i])\n"
        return
    -- Max instance - project 0 is the max function
    if containsSubstr typeStr "Max" && idx == 0 then
      markHandler "proj.Max"
      emitIndent
      emit s!"{varName} = max\n"
      return
    -- Min instance - project 0 is the min function
    if containsSubstr typeStr "Min" && idx == 0 then
      markHandler "proj.Min"
      emitIndent
      emit s!"{varName} = min\n"
      return
    emitIndent
    emit s!"{varName} = "
    emit (← getVarName structFvar)
    -- Use tuple indexing for Prod type, otherwise field access.  The field name
    -- MUST match the dataclass declaration in `emitInductiveType`, which names
    -- fields `field_{i}` — not `{typeName}_{i}`.  (A type-name-derived accessor
    -- like `page_0` parses fine but fails at runtime with AttributeError.)
    if typeName == ``Prod then
      markHandler "proj.Prod"
      emit s!"[{idx}]\n"
    else
      markHandler "proj.field"
      emit s!".field_{idx}\n"

/-- Check if a type is PUnit or Unit -/
def isUnitType (e : Expr) : Bool :=
  match e with
  | .const ``PUnit _ => true
  | .const ``Unit _ => true
  | _ => false

/-! ## Tail-call analysis

Lean performs tail-call optimization; Python does not. A Lean function whose
self-recursive calls are all in tail position runs in constant stack, but the
naive Python translation recurses and overflows the stack (`RecursionError`)
on deep inputs. We detect such functions here so `emitDecl` can rewrite them
into a `while True:` loop.

The analysis is *inlining-aware*: LCNF lowers `match` arms into single-use
continuation thunks (local `.fun`s bound to `_alt`) and loops into join points
(`.jp`/`.jmp`), so a genuinely tail self-call often sits inside a thunk that is
itself tail-called. We propagate a `tailCtx` flag through tail-calls to those
local functions/join points, mirroring what the emitter will do by inlining
them. The check is deliberately *sound* (a self-call reached in non-tail
context fails the check) at the cost of missing exotic shapes. -/

/-- Collect every local function / join-point declaration in a `Code` tree,
    keyed by the fvar it is bound to. -/
partial def collectLocalFuns (c : Code) (acc : Std.HashMap FVarId FunDecl) : Std.HashMap FVarId FunDecl :=
  match c with
  | .let _ k => collectLocalFuns k acc
  | .fun d k => collectLocalFuns k (collectLocalFuns d.value (acc.insert d.fvarId d))
  | .jp d k => collectLocalFuns k (collectLocalFuns d.value (acc.insert d.fvarId d))
  | .cases cs => cs.alts.foldl (fun a alt =>
      match alt with
      | .alt _ _ code => collectLocalFuns code a
      | .default code => collectLocalFuns code a) acc
  | _ => acc

/-- Collect zero-argument fvar aliases (`let x := fvar f`) throughout a `Code`
    tree. LCNF binds match-arm continuation thunks as `_alt := _f`, so a later
    call to `_alt` must resolve to `_f` to find its body. -/
partial def collectFunAliases (c : Code) (acc : Std.HashMap FVarId FVarId) : Std.HashMap FVarId FVarId :=
  match c with
  | .let decl k =>
    let acc := match decl.value with
      | .fvar f args => if args.isEmpty then acc.insert decl.fvarId f else acc
      | _ => acc
    collectFunAliases k acc
  | .fun d k => collectFunAliases k (collectFunAliases d.value acc)
  | .jp d k => collectFunAliases k (collectFunAliases d.value acc)
  | .cases cs => cs.alts.foldl (fun a alt =>
      match alt with
      | .alt _ _ code => collectFunAliases code a
      | .default code => collectFunAliases code a) acc
  | _ => acc

/-- Resolve an fvar through the zero-arg alias map (bounded to avoid cycles). -/
partial def resolveFunAlias (aliases : Std.HashMap FVarId FVarId) (f : FVarId) (fuel : Nat) : FVarId :=
  if fuel == 0 then f
  else match aliases[f]? with
    | some g => resolveFunAlias aliases g (fuel - 1)
    | none => f

/-- Is `k` exactly `return fv`? (used to decide whether a call's result is
    immediately returned, i.e. the call is in tail position). -/
def isReturnOf (fv : FVarId) (k : Code) : Bool :=
  match k with
  | .return r => r == fv
  | _ => false

/-- Walk a `Code` tree looking for self-recursive calls to `declName`.
    Returns `(foundNonTailSelfCall, foundAnySelfCall)`. `tailCtx` is true when
    this code is in tail position of the top-level function (propagated through
    tail-calls to local funs / join-point jumps). `visited` breaks cycles among
    local functions. `fuel` bounds recursion defensively. -/
partial def scanSelfCalls (declName : Name) (funs : Std.HashMap FVarId FunDecl)
    (aliases : Std.HashMap FVarId FVarId)
    (visited : Std.HashSet FVarId) (fuel : Nat) (tailCtx : Bool) (c : Code) : Bool × Bool :=
  if fuel == 0 then (true, true)  -- give up conservatively: treat as non-tail
  else
  let fuel := fuel - 1
  let orPair := fun (a b : Bool × Bool) => (a.1 || b.1, a.2 || b.2)
  let recur := scanSelfCalls declName funs aliases
  match c with
  | .return _ | .unreach _ => (false, false)
  | .jmp f args =>
    let _ := args
    -- A jump is a tail jump; inline the join point's body in the same context.
    let f := resolveFunAlias aliases f 1000
    if funs.contains f && !visited.contains f then
      recur (visited.insert f) fuel tailCtx (funs[f]!).value
    else (false, false)
  | .cases cs =>
    cs.alts.foldl (fun acc alt =>
      let code := match alt with | .alt _ _ code => code | .default code => code
      orPair acc (recur visited fuel tailCtx code)) (false, false)
  | .fun _ k | .jp _ k =>
    -- Definition site: its body is analyzed at the (tail-aware) call site.
    recur visited fuel tailCtx k
  | .let decl k =>
    match decl.value with
    | .const n _ _ =>
      if n == declName then
        -- A self-recursive call. It is a tail call iff we're in tail context
        -- and its result is immediately returned.
        let isTail := tailCtx && isReturnOf decl.fvarId k
        orPair (!isTail, true) (recur visited fuel tailCtx k)
      else
        recur visited fuel tailCtx k
    | .fvar f args =>
      -- A zero-argument fvar binding is an *alias* (`_alt := _f`), not a call;
      -- it's already recorded in `aliases`, so don't scan the target's body
      -- here (doing so would visit it in non-tail context and mask a genuine
      -- tail call). Only an application (args > 0) invokes the function.
      if args.isEmpty then
        recur visited fuel tailCtx k
      else
        -- A call to a local function. If it's tail-called, analyze its body in
        -- tail context (the emitter will inline it); otherwise non-tail context.
        let f := resolveFunAlias aliases f 1000
        let calledTail := tailCtx && isReturnOf decl.fvarId k
        let inFun :=
          if funs.contains f && !visited.contains f then
            recur (visited.insert f) fuel calledTail (funs[f]!).value
          else (false, false)
        orPair inFun (recur visited fuel tailCtx k)
    | _ => recur visited fuel tailCtx k

/-- Does this `Code` contain a self-recursive call to `declName` anywhere?
    Used in loop mode to decide whether a local continuation thunk carries the
    recursion (and so must be inlined for `continue` to reach the loop) or is a
    genuine helper that can stay a nested `def`. -/
partial def codeHasSelfCall (declName : Name) (c : Code) : Bool :=
  match c with
  | .let decl k =>
    (match decl.value with | .const n _ _ => n == declName | _ => false)
      || codeHasSelfCall declName k
  | .fun d k | .jp d k => codeHasSelfCall declName d.value || codeHasSelfCall declName k
  | .cases cs => cs.alts.any (fun alt =>
      match alt with | .alt _ _ code => codeHasSelfCall declName code | .default code => codeHasSelfCall declName code)
  | _ => false

/-- Count call sites (`_x := f args` with args, or `jmp f`) targeting each
    local function, resolving through the zero-arg alias map so `_alt := _f`
    chains attribute the call to `_f`. -/
partial def countCallSites (aliases : Std.HashMap FVarId FVarId) (c : Code)
    (acc : Std.HashMap FVarId Nat) : Std.HashMap FVarId Nat :=
  let bump := fun (m : Std.HashMap FVarId Nat) (f : FVarId) =>
    let f := resolveFunAlias aliases f 1000
    m.insert f (m.getD f 0 + 1)
  match c with
  | .let decl k =>
    let acc := match decl.value with
      | .fvar f args => if args.isEmpty then acc else bump acc f
      | _ => acc
    countCallSites aliases k acc
  | .fun d k | .jp d k => countCallSites aliases k (countCallSites aliases d.value acc)
  | .jmp f _ => bump acc f
  | .cases cs => cs.alts.foldl (fun a alt =>
      match alt with
      | .alt _ _ code => countCallSites aliases code a
      | .default code => countCallSites aliases code a) acc
  | _ => acc

/-- True iff every local function that *carries a self-recursive call* is
    called from at most one site. Such thunks are inlined by the emitter; a
    multiply-called one would have its body (and the recursion) duplicated, so
    if any exists we decline the loop rewrite (and fall back to plain, correct
    recursive emission). -/
partial def recursionThunksSingleUse (declName : Name) (aliases : Std.HashMap FVarId FVarId)
    (callSites : Std.HashMap FVarId Nat) (c : Code) : Bool :=
  match c with
  | .let _ k => recursionThunksSingleUse declName aliases callSites k
  | .fun d k | .jp d k =>
    let ok := if codeHasSelfCall declName d.value then callSites.getD d.fvarId 0 ≤ 1 else true
    ok && recursionThunksSingleUse declName aliases callSites d.value
       && recursionThunksSingleUse declName aliases callSites k
  | .cases cs => cs.alts.all (fun alt =>
      match alt with
      | .alt _ _ code => recursionThunksSingleUse declName aliases callSites code
      | .default code => recursionThunksSingleUse declName aliases callSites code)
  | _ => true

/-- True iff `declName`'s body has at least one self-recursive call, every
    self-recursive call is in tail position, and every recursion-carrying
    continuation thunk is single-use (so the emitter can inline it without
    duplicating the body). Such functions are rewritten into a `while True:`
    loop by `emitDecl` to avoid Python stack overflow. -/
def isSelfTailRecursive (declName : Name) (body : Code) : Bool :=
  let funs := collectLocalFuns body {}
  let aliases := collectFunAliases body {}
  let (nonTail, anySelf) := scanSelfCalls declName funs aliases {} 100000 true body
  let callSites := countCallSites aliases body {}
  anySelf && !nonTail && recursionThunksSingleUse declName aliases callSites body

/-! ## Code Emission -/

mutual

partial def emitCode (code : Code) : EmitM Unit := do
  match code with
  | .let decl k =>
    -- Tail-loop rewrites (only when emitting a self-tail-recursive function).
    if let some (declName, params) := (← get).tailLoop then
      match decl.value with
      | .const n _ args =>
        -- A tail self-call: rebind the loop parameters in parallel and
        -- `continue`, instead of recursing. Guarded by isReturnOf so we only
        -- fire in genuine tail position (detection already proved all are).
        if n == declName && isReturnOf decl.fvarId k then
          emitTailStep params args
          return
      | .fvar f args =>
        let f ← resolveAlias f
        if args.isEmpty then
          -- Alias to a local fun. If that fun carries the recursion, propagate
          -- the inline marking to this alias and emit nothing for the binding
          -- itself — but still emit the continuation.
          if let some fd := (← get).inlineThunks[f]? then
            modify fun s => { s with inlineThunks := s.inlineThunks.insert decl.fvarId fd }
            emitCode k
            return
        else
          -- Tail-call to an inlined continuation thunk: bind its params to the
          -- args and emit its body inline, so any `continue` reaches the loop.
          if let some fd := (← get).inlineThunks[f]? then
            if isReturnOf decl.fvarId k then
              emitInlinedThunk fd args
              return
      | _ => pure ()
    emitLetValue decl
    emitCode k
  | .fun decl k =>
    -- In loop mode, defer emitting a `def` for a continuation thunk that
    -- carries the recursion; it will be inlined at its tail-call site.
    if let some (declName, _) := (← get).tailLoop then
      if codeHasSelfCall declName decl.value then
        modify fun s => { s with inlineThunks := s.inlineThunks.insert decl.fvarId decl }
        emitCode k
        return
    emitLocalFun decl
    emitCode k
  | .jp decl k =>
    if let some (declName, _) := (← get).tailLoop then
      if codeHasSelfCall declName decl.value then
        modify fun s => { s with inlineThunks := s.inlineThunks.insert decl.fvarId decl }
        emitCode k
        return
    emitJoinPoint decl
    emitCode k
  | .jmp fvarId args =>
    -- Tail-jump to an inlined join point: emit its body inline.
    if (← get).tailLoop.isSome then
      let f ← resolveAlias fvarId
      if let some fd := (← get).inlineThunks[f]? then
        emitInlinedThunk fd args
        return
    emitIndent
    emit s!"return {← getVarName fvarId}("
    emitArgs args
    emit ")\n"
  | .cases cases =>
    emitCases cases
  | .return fvarId =>
    emitIndent
    -- Resolve aliases first: a returned var is often an alias of a literal/bool
    -- var whose own binding was elided, so a direct lookup would miss it and
    -- emit a reference to an unbound name.
    let rfv ← resolveAlias fvarId
    -- Check if returning a known literal
    if let some lit := (← get).literalVars[rfv]? then
      emit "return "
      emitLitValue lit
      emit "\n"
    else if let some b := (← get).boolVars[rfv]? then
      emit s!"return {if b then "True" else "False"}\n"
    else
      emit s!"return {← getVarName fvarId}\n"
  | .unreach _ =>
    emitIndent
    emit "raise RuntimeError(\"unreachable\")\n"

partial def emitLocalFun (decl : FunDecl) : EmitM Unit := do
  -- In loop mode, a continuation that carries the recursion must be INLINED at
  -- its tail-call site (where `continue` is legal), never emitted as a nested
  -- `def` (a `def` body can't `continue` the enclosing `while`).  `emitCode`'s
  -- `.fun` handler already routes such thunks to `inlineThunks`, but a deferred
  -- single-param lambda whose render fails falls through to this function
  -- directly — so guard here too, or we'd emit a `def` with an illegal
  -- `continue`.  (Surfaced once the helper-scoping fix stopped mis-rendering
  -- such thunks as `_uniq_NNN` calls.)
  if let some (declName, _) := (← get).tailLoop then
    if codeHasSelfCall declName decl.value then
      modify fun s => { s with inlineThunks := s.inlineThunks.insert decl.fvarId decl }
      return
  -- Count non-unit params for arity tracking
  let nonUnitParams := decl.params.foldl (fun acc p => if isUnitType p.type then acc else acc + 1) 0
  let totalParams := decl.params.size
  -- Try to defer a single-parameter lambda whose body is a simple expression,
  -- so a consuming comprehension can inline it (e.g. `[x + 1 for x in xs]`
  -- rather than a helper `def`). We only do this for exactly one non-unit
  -- parameter — the comprehension binder — and require the body to render.
  if nonUnitParams == 1 && totalParams == 1 then
    let param := decl.params[0]!
    if !isUnitType param.type then
      -- Snapshot state so a failed render attempt leaves nothing behind.
      let snapshot ← get
      let paramName ← registerVar param.fvarId param.binderName
      markBoolTyped param.fvarId param.type
      match ← renderExprCode decl.value with
      | some body =>
        modify fun s => { s with
          localFnArities := s.localFnArities.insert decl.fvarId (nonUnitParams, totalParams)
          deferredLambdas := s.deferredLambdas.insert decl.fvarId (paramName, body) }
        return
      | none =>
        -- Roll back render-time mutations.
        set snapshot
        -- In loop mode, a lambda whose body didn't render as a pure expression
        -- may carry a tail `continue` (its body references the loop's recursion,
        -- e.g. a match-arm continuation whose self-call `codeHasSelfCall` can't
        -- see through an alias/jmp).  Emitting it as a nested `def` would put a
        -- `continue` outside its loop.  Route it to `inlineThunks` so it's
        -- inlined at its tail-call site instead.  (Pure non-recursive loop-body
        -- lambdas are inlined harmlessly too — their bodies just have no
        -- `continue`.)
        if (← get).tailLoop.isSome then
          modify fun s => { s with inlineThunks := s.inlineThunks.insert decl.fvarId decl }
          return
  let fnName ← registerVar decl.fvarId decl.binderName
  -- Track both for partial application detection
  modify fun s => { s with localFnArities := s.localFnArities.insert decl.fvarId (nonUnitParams, totalParams) }
  emitIndent
  emit s!"def {fnName}("
  emitFunParams decl.params
  emit "):\n"
  withIndent do
    emitCode decl.value

partial def emitJoinPoint (decl : FunDecl) : EmitM Unit := do
  let jpName ← registerVar decl.fvarId decl.binderName
  emitIndent
  emit s!"def {jpName}("
  emitFunParams decl.params
  emit "):\n"
  withIndent do
    emitCode decl.value

/-- Emit one iteration of a tail-recursive loop: rebind the loop parameters to
    the self-call's arguments (in parallel, via a tuple assignment to avoid
    aliasing hazards) and `continue`. `args` is the full LCNF argument list of
    the self-call; we drop type/erased/unit args so the remaining value args
    align positionally with `params` (the Python parameter names). -/
partial def emitTailStep (params : Array String) (args : Array Arg) : EmitM Unit := do
  -- Keep only value arguments, matching how emitArgs filters for the call.
  let mut valArgs : Array Arg := #[]
  for arg in args do
    match arg with
    | .fvar fv => if !(← get).unitVars.contains fv then valArgs := valArgs.push arg
    | .erased | .type _ => pure ()
  let declName := match (← get).tailLoop with | some (n, _) => n | none => .anonymous
  if valArgs.size != params.size then
    -- Arg/param mismatch (shouldn't happen for a direct self-call): fall back
    -- to a plain recursive call so we never emit wrong code (correct, just not
    -- stack-optimized).
    emitIndent
    emit s!"return {← pyFnName declName}("
    emitArgs args
    emit ")\n"
    return
  -- Render each argument value first (they reference the *current* params).
  let mut rhs : Array String := #[]
  for arg in valArgs do
    rhs := rhs.push (← renderArg arg)
  emitIndent
  if params.size == 1 then
    emit s!"{params[0]!} = {rhs[0]!}\n"
  else
    emit s!"{", ".intercalate params.toList} = {", ".intercalate rhs.toList}\n"
  emitIndent
  emit "continue\n"

/-- Emit an inlined continuation thunk body: bind the thunk's parameters to the
    call arguments, then emit its body inline (so any tail self-call inside it
    can `continue` the enclosing loop). -/
partial def emitInlinedThunk (decl : FunDecl) (args : Array Arg) : EmitM Unit := do
  -- Bind non-unit params positionally to the value args.
  let mut valArgs : Array Arg := #[]
  for arg in args do
    match arg with
    | .fvar fv => if !(← get).unitVars.contains fv then valArgs := valArgs.push arg
    | .erased | .type _ => pure ()
  let mut vi := 0
  for p in decl.params do
    if isUnitType p.type then
      let _ ← registerVar p.fvarId p.binderName
      modify fun s => { s with unitVars := s.unitVars.insert p.fvarId }
    else
      let pname ← registerVar p.fvarId p.binderName
      if vi < valArgs.size then
        let rhs ← renderArg valArgs[vi]!
        -- Avoid a pointless `x = x` self-binding.
        if rhs != pname then
          emitIndent
          emit s!"{pname} = {rhs}\n"
        vi := vi + 1
  emitCode decl.value

partial def emitCases (cases : Cases) : EmitM Unit := do
  -- The discriminant may be a known literal (e.g. `match (4 : Nat) with …` after
  -- an OfNat projection whose binding we elided) — resolve to the literal value
  -- so we don't emit a reference to an unbound variable.
  let dfv ← resolveAlias cases.discr
  let discr ←
    match (← get).literalVars[dfv]? with
    | some lit => pure (litValueStr lit)
    | none => getVarName cases.discr
  if cases.typeName == ``Bool then
    markHandler "cases.Bool"
    emitBoolCases discr cases.alts
  else if cases.typeName == ``Nat then
    markHandler "cases.Nat"
    emitNatCases discr cases.alts
  else if cases.typeName == ``Decidable then
    -- Decidable has isFalse and isTrue constructors
    -- Need to check the discriminant type to determine if it's a "match on Nat" vs "if bool"
    markHandler "cases.Decidable"
    emitDecidableCases discr cases.discr cases.alts
  else if cases.typeName == ``Option then
    markHandler "cases.Option"
    emitOptionCases discr cases.alts
  else if cases.typeName == ``List then
    markHandler "cases.List"
    emitListCases discr cases.alts
  else
    -- Generic structural match (custom inductive / Prod destructuring).  Tag with
    -- the type name so the report shows which user types exercised the fallback.
    markHandler s!"cases.match.{cases.typeName.toString (escape := false)}"
    emitIndent
    emit s!"match {discr}:\n"
    withIndent do
      for alt in cases.alts do
        emitAlt alt

partial def emitDecidableCases (discr : String) (discrFvar : FVarId) (alts : Array Alt) : EmitM Unit := do
  -- Decidable cases arise from:
  -- 1. Pattern matching on Nat/Int with literal 0: `match e with | 0 => ... | _ => ...`
  --    - The discriminant is the Nat/Int value itself
  --    - isTrue = "e = 0" is true (e equals 0)
  --    - isFalse = "e = 0" is false (e doesn't equal 0)
  --    - In Python, `if e:` is True when e≠0, so we need SWAPPED branches
  --
  -- 2. Boolean conditions: `if cond then ... else ...`
  --    - The discriminant is already a Bool (or comparison result)
  --    - isTrue = condition is true
  --    - isFalse = condition is false
  --    - In Python, `if cond:` is True when cond is True, so normal branches
  --
  -- Key insight: check if the discriminant is a computed boolean (from comparison)
  -- vs a raw numeric value (from Nat/Int match)
  --
  -- Heuristic: if the discriminant name starts with "_x", it's likely a computed
  -- intermediate value (like `_x = e == 0`), so treat it as Bool.
  -- If it's a simple name (e, n, k, x), check if it's likely Bool or Nat.
  --
  -- For Bool parameters like `x : Bool`, Python's truthiness matches directly.
  -- For Nat parameters like `e : Nat`, Python's truthiness (non-zero) is OPPOSITE
  -- of the "e = 0" proposition's truth value.
  --
  -- Simple heuristic: names starting with _x are comparison results (Bool-like)
  -- Names starting with _y are join point parameters (often Bool from short-circuit eval)
  -- Other names need more context - for now, assume single-letter names like
  -- x, b, p are Bool, while e, n, k, i, j are Nat.
  -- Authoritative signal: if the discriminant's LCNF type is `Bool`, it is a
  -- genuine boolean condition (normal branch order). This fixes Bool-typed
  -- parameters whose names the heuristic below doesn't recognize (e.g.
  -- `isMalloc`), which previously fell through to the Nat-against-0 path and
  -- got their true/false branches SWAPPED. Fall back to the name heuristic
  -- only when the type can't be resolved.
  -- Resolve through the alias map first: `if isMalloc then …` lowers to a
  -- `cases` on `instDecidableEqBool isMalloc true`, whose discriminant fvar is
  -- aliased to `isMalloc`. We want isMalloc's type (Bool), not the Decidable
  -- node's, so a Bool-typed condition takes the normal (non-swapped) branches.
  let resolvedDiscr ← resolveAlias discrFvar
  let discrIsBoolTyped := (← fvarIsBool discrFvar) || (← fvarIsBool resolvedDiscr)
  let discrLooksLikeBool := discrIsBoolTyped ||
                            discr.startsWith "_x" ||
                            discr.startsWith "_y" ||  -- join point params often carry Bool
                            discr == "x" || discr == "b" || discr == "p" ||
                            discr == "cond" || discr == "condition" ||
                            discr.endsWith "_cond" || discr.endsWith "_bool"

  let mut falseAlt : Option Alt := none
  let mut trueAlt : Option Alt := none
  for alt in alts do
    match alt with
    | .alt ctorName _ _ =>
      if ctorName == ``Decidable.isFalse then falseAlt := some alt
      else if ctorName == ``Decidable.isTrue then trueAlt := some alt
    | .default _ => pure ()
  match trueAlt, falseAlt with
  | some tAlt, some fAlt =>
    emitIndent
    if discrLooksLikeBool then
      -- Discriminant is a boolean comparison result
      -- `if discr:` (True) → isTrue, `else:` (False) → isFalse
      emit s!"if {discr}:\n"
      withIndent do emitAltBody tAlt
      emitIndent
      emit "else:\n"
      withIndent do emitAltBody fAlt
    else
      -- Discriminant is a Nat/Int being matched against 0
      -- `if discr:` (non-zero, truthy) → isFalse (e≠0)
      -- `else:` (zero, falsy) → isTrue (e=0)
      emit s!"if {discr}:\n"
      withIndent do emitAltBody fAlt
      emitIndent
      emit "else:\n"
      withIndent do emitAltBody tAlt
  | _, _ =>
    -- Fallback
    emitIndent
    emit s!"if {discr}:\n"
    withIndent do
      if let some alt := alts[0]? then emitAltBody alt
      else emitLn "pass"
    emitIndent
    emit "else:\n"
    withIndent do
      if let some alt := alts[1]? then emitAltBody alt
      else emitLn "pass"

partial def emitOptionCases (discr : String) (alts : Array Alt) : EmitM Unit := do
  emitIndent
  emit s!"if {discr} is None:\n"
  -- `none` branch: the explicit `Option.none` arm, or a `default` arm if the
  -- match was compiled with one.  Handling `default` is required — otherwise
  -- the branch body is dropped, leaving an empty `if:` block (SyntaxError).
  let mut noneEmitted := false
  for alt in alts do
    match alt with
    | .alt ctorName _ code =>
      if ctorName == ``Option.none && !noneEmitted then
        noneEmitted := true
        withIndent do emitCode code
    | _ => pure ()
  if !noneEmitted then
    for alt in alts do
      match alt with
      | .default code => if !noneEmitted then noneEmitted := true; withIndent do emitCode code
      | _ => pure ()
  if !noneEmitted then withIndent do emitLn "pass"
  emitIndent
  emit "else:\n"
  -- `some` branch: the explicit `Option.some` arm, or a `default` arm.
  let mut someEmitted := false
  for alt in alts do
    match alt with
    | .alt ctorName params code =>
      if ctorName == ``Option.some && !someEmitted then
        someEmitted := true
        withIndent do
          if params.size > 0 then
            let valName ← registerVar params[params.size - 1]!.fvarId params[params.size - 1]!.binderName
            emitLn s!"{valName} = {discr}"
          emitCode code
    | _ => pure ()
  if !someEmitted then
    for alt in alts do
      match alt with
      | .default code => if !someEmitted then someEmitted := true; withIndent do emitCode code
      | _ => pure ()
  if !someEmitted then withIndent do emitLn "pass"

partial def emitListCases (discr : String) (alts : Array Alt) : EmitM Unit := do
  emitIndent
  emit s!"if len({discr}) == 0:\n"
  -- Find nil case
  for alt in alts do
    match alt with
    | .alt ctorName _ code =>
      if ctorName == ``List.nil then
        withIndent do emitCode code
    | _ => pure ()
  emitIndent
  emit "else:\n"
  -- The non-nil branch is either an explicit `List.cons` arm or a `default`
  -- arm.  Lean lowers an n-way list match (e.g. []/[x]/x::y::rest) to *nested*
  -- binary `List.casesOn`, where the inner non-nil case is emitted as a
  -- `default` rather than a named `List.cons` — so we must handle both, or the
  -- `else:` body is dropped (leaving an empty block / SyntaxError).
  let mut emitted := false
  for alt in alts do
    match alt with
    | .alt ctorName params code =>
      if ctorName == ``List.cons && !emitted then
        emitted := true
        withIndent do
          if params.size >= 2 then
            let headName ← registerVar params[params.size - 2]!.fvarId params[params.size - 2]!.binderName
            let tailName ← registerVar params[params.size - 1]!.fvarId params[params.size - 1]!.binderName
            emitLn s!"{headName} = {discr}[0]"
            emitLn s!"{tailName} = {discr}[1:]"
          emitCode code
    | _ => pure ()
  if !emitted then
    for alt in alts do
      match alt with
      | .default code =>
        if !emitted then
          emitted := true
          withIndent do emitCode code
      | _ => pure ()
  -- Safety net: never leave the `else` body empty (keeps output parseable).
  if !emitted then
    withIndent do emitLn "pass"

partial def emitNatCases (discr : String) (alts : Array Alt) : EmitM Unit := do
  for h : i in [0:alts.size] do
    let alt := alts[i]
    match alt with
    | .alt ctorName params code =>
      emitIndent
      if ctorName == ``Nat.zero then
        if i == 0 then
          emit s!"if {discr} == 0:\n"
        else
          emit s!"elif {discr} == 0:\n"
      else if ctorName == ``Nat.succ then
        if i == 0 then
          emit "if True:  # succ case\n"
        else
          emit "else:\n"
        -- Register the predecessor variable
        if params.size > 0 then
          let predName ← registerVar params[0]!.fvarId params[0]!.binderName
          withIndent do
            emitIndent
            emit s!"{predName} = {discr} - 1\n"
            emitCode code
          continue
      else
        emit s!"# unknown Nat constructor: {ctorName}\n"
      withIndent do
        emitCode code
    | .default code =>
      emitIndent
      emit "else:\n"
      withIndent do
        emitCode code

partial def emitBoolCases (discr : String) (alts : Array Alt) : EmitM Unit := do
  -- In LCNF, Bool.false comes first (ctor index 0), Bool.true second (ctor index 1)
  -- So we need to match on false first then true
  -- Find which alt is true and which is false
  let mut falseAlt : Option Alt := none
  let mut trueAlt : Option Alt := none
  for alt in alts do
    match alt with
    | .alt ctorName _ _ =>
      if ctorName == ``Bool.false then falseAlt := some alt
      else if ctorName == ``Bool.true then trueAlt := some alt
    | .default _ => pure ()
  -- Emit as if discr: true_case else: false_case
  match trueAlt, falseAlt with
  | some tAlt, some fAlt =>
    emitIndent
    emit s!"if {discr}:\n"
    withIndent do emitAltBody tAlt
    emitIndent
    emit "else:\n"
    withIndent do emitAltBody fAlt
  | _, _ =>
    -- Fallback: emit in order
    for h : i in [0:alts.size] do
      let alt := alts[i]
      if i == 0 then
        emitIndent
        emit s!"if {discr}:\n"
      else
        emitIndent
        emit "else:\n"
      withIndent do
        emitAltBody alt

partial def emitAlt (alt : Alt) : EmitM Unit := do
  match alt with
  | .alt ctorName params code =>
    emitIndent
    -- Use tuple pattern for Prod.mk
    if ctorName == ``Prod.mk then
      emit "case ("
      for h : i in [0:params.size] do
        if i > 0 then emit ", "
        let name ← registerVar params[i].fvarId params[i].binderName
        emit name
      emit "):\n"
    else
      emit s!"case {toPyTypeName ctorName}("
      for h : i in [0:params.size] do
        if i > 0 then emit ", "
        let name ← registerVar params[i].fvarId params[i].binderName
        emit name
      emit "):\n"
    withIndent do
      emitCode code
  | .default code =>
    emitIndent
    emit "case _:\n"
    withIndent do
      emitCode code

partial def emitAltBody (alt : Alt) : EmitM Unit := do
  match alt with
  | .alt _ _ code => emitCode code
  | .default code => emitCode code

partial def emitFunParams (params : Array Param) : EmitM Unit := do
  let mut first := true
  for p in params do
    -- Skip PUnit/Unit parameters
    if isUnitType p.type then
      -- Still register the var as a unit var so calls skip it
      let _ ← registerVar p.fvarId p.binderName
      modify fun s => { s with unitVars := s.unitVars.insert p.fvarId }
      continue
    if !first then emit ", "
    first := false
    let name ← registerVar p.fvarId p.binderName
    markBoolTyped p.fvarId p.type
    let typeHint ← toPyTypeHint p.type
    emit s!"{name}: {typeHint}"

end

/-! ## Declaration Emission -/

def emitDecl (decl : Decl) : EmitM Unit := do
  let fnName ← pyFnName decl.name
  -- Emit a comment with the full Lean name for traceability
  emitLn s!"# Lean: {decl.name}"
  emitIndent
  emit s!"def {fnName}("
  emitFunParams decl.params
  emit ")"
  -- The decl.type is the *result* type after all parameters are applied
  let retType ← toPyTypeHint (getReturnType decl.type)
  emit s!" -> {retType}:\n"
  -- Lean does TCO; Python does not. If every self-recursive call is a tail
  -- call, rewrite the body into a `while True:` loop so deep recursion does not
  -- overflow the Python stack. Detection is sound (see isSelfTailRecursive).
  if isSelfTailRecursive decl.name (declCode decl) then
    markHandler "struct.tailLoop"
    -- Collect the Python names of the (non-unit) parameters, in order — these
    -- are what a tail self-call rebinds. emitFunParams already registered them.
    let mut pyParams : Array String := #[]
    for p in decl.params do
      if !isUnitType p.type then
        pyParams := pyParams.push (← getVarName p.fvarId)
    withIndent do
      emitLn "while True:"
      -- Save/restore loop state so nested decls don't inherit it.
      let saved := (← get).tailLoop
      let savedThunks := (← get).inlineThunks
      modify fun s => { s with tailLoop := some (decl.name, pyParams), inlineThunks := {} }
      withIndent do
        emitCode (declCode decl)
      modify fun s => { s with tailLoop := saved, inlineThunks := savedThunks }
  else
    withIndent do
      emitCode (declCode decl)
  emitBlankLine

/-! ## File Structure Emission -/

def emitFileHeader : EmitM Unit := do
  let modName ← getModName
  emitLn s!"# Generated from {modName}"
  emitBlankLine
  emitLn "from __future__ import annotations"
  emitLn "from dataclasses import dataclass"
  emitLn "import functools"
  emitLn "from typing import Any, Callable"
  emitBlankLine

def emitInductiveType (name : Name) : EmitM Unit := do
  let env ← getEnv
  let some (.inductInfo info) := env.find? name | return
  if (← get).emittedTypes.contains name then return
  markHandler "struct.inductive"
  modify fun s => { s with emittedTypes := s.emittedTypes.insert name }

  if info.ctors.length == 0 then return

  for ctorName in info.ctors do
    let some (.ctorInfo ctorInfo) := env.find? ctorName | continue
    emitLn "@dataclass"
    emitLn s!"class {toPyTypeName ctorName}:"
    withIndent do
      if ctorInfo.numFields == 0 then
        emitLn "pass"
      else
        for i in [0:ctorInfo.numFields] do
          emitLn s!"field_{i}: Any"
    emitBlankLine

  -- Always emit type alias so the type name is defined
  -- For single-constructor types, this aliases to the constructor
  -- For multi-constructor types, this creates a union type
  let ctorNames := " | ".intercalate (info.ctors.map toPyTypeName)
  emitLn s!"{toPyTypeName name} = {ctorNames}"
  emitBlankLine

/-! ## Main Entry Point -/

/-- Collect custom inductive types referenced in a type expression -/
partial def collectCustomTypes (e : Expr) (acc : Lean.NameSet) : CoreM Lean.NameSet := do
  match e with
  | .const name _ =>
    -- Skip builtin types
    if name == ``Nat || name == ``Int || name == ``String || name == ``Bool ||
       name == ``Float || name == ``Unit || name == ``PUnit || name == ``Char ||
       name == ``List || name == ``Array || name == ``Option || name == ``Prod ||
       name == ``UInt8 || name == ``UInt16 || name == ``UInt32 || name == ``UInt64 || name == ``USize then
      return acc
    -- Check if it's an inductive type
    let env ← getEnv
    if let some (.inductInfo _) := env.find? name then
      return acc.insert name
    return acc
  | .app f arg => do
    let acc ← collectCustomTypes f acc
    collectCustomTypes arg acc
  | .forallE _ dom body _ => do
    let acc ← collectCustomTypes dom acc
    collectCustomTypes body acc
  | _ => return acc

/-- Collect types from pattern matching (Cases) in code body -/
partial def collectTypesFromCode (code : Code) (acc : Lean.NameSet) : CoreM Lean.NameSet := do
  match code with
  | .let _ k => collectTypesFromCode k acc
  | .fun fd k =>
    let acc ← collectTypesFromCode fd.value acc
    collectTypesFromCode k acc
  | .jp fd k =>
    let acc ← collectTypesFromCode fd.value acc
    collectTypesFromCode k acc
  | .cases cs =>
    -- The typeName of Cases tells us what type is being matched
    let acc := acc.insert cs.typeName
    -- Process alternatives
    let mut acc := acc
    for alt in cs.alts do
      match alt with
      | .alt _ _ c | .default c => acc ← collectTypesFromCode c acc
    return acc
  | .return _ | .jmp _ _ | .unreach _ => return acc

/-- Transitively add the constructor-field types of every already-collected
    inductive/structure.  Without this, a type that only ever appears as a
    *field* of another collected type (never as a param, return, or matched
    type) is missed — e.g. an enum used solely inside a record and constructed
    by value.  We iterate to a fixpoint so chains of nested records are closed
    over. -/
partial def closeOverFieldTypes (seed : Lean.NameSet) : CoreM Lean.NameSet := do
  let env ← getEnv
  let mut acc := seed
  let mut worklist := seed.toList
  while !worklist.isEmpty do
    let name := worklist.head!
    worklist := worklist.tail!
    let some (.inductInfo info) := env.find? name | continue
    for ctorName in info.ctors do
      let some (.ctorInfo ctorInfo) := env.find? ctorName | continue
      -- Walk the constructor's type; each field's type is a nested Π-binder.
      let fieldTypes ← collectCustomTypes ctorInfo.type {}
      for ft in fieldTypes do
        unless acc.contains ft do
          acc := acc.insert ft
          worklist := ft :: worklist
  return acc

/-- Collect all custom types from declarations -/
def collectTypesFromDecls (decls : Array Decl) : CoreM Lean.NameSet := do
  let mut types : Lean.NameSet := {}
  for decl in decls do
    -- Check parameter types
    for p in decl.params do
      types ← collectCustomTypes p.type types
    -- Check return type
    types ← collectCustomTypes decl.type types
    -- Check types used in pattern matching within the function body
    types ← collectTypesFromCode (declCode decl) types
  -- Transitively include the field types of every collected record/enum, so a
  -- type used only inside another type's fields is still emitted.
  closeOverFieldTypes types

/-- The curated universe of self-coverage handler tags — the denominator for the
    fuzzer's "transpiler self-coverage" report.  These are the special-cased,
    semantically-tricky handlers whose emission we want to *prove* the test
    corpus exercises (an untested one is where a bug hides).  The generic
    per-`declName` `const.*`/`fallthrough.*`/`cases.match.*` tags are NOT listed
    here — they are open-ended and reported separately (fallthroughs on core
    namespaces are flagged as likely-broken handlers; see `markHandler` sites).

    Kept as data, not derived, so the report has a stable target across Lean
    versions; add a tag here when you add a handler.  The `const.<Name>` form is
    used for name-keyed handlers so the tag is exactly what flows through at
    runtime — no Lean-internal constant is hardcoded in a way an API rename could
    silently invalidate (a rename shows up as the handler dropping to a
    `fallthrough.*`, which the report surfaces). -/
def knownHandlerTags : List String := [
  -- Arithmetic via the typeclass-instance path (`instHAdd`/`instHMul`/… →
  -- extracted op).  MOST arithmetic lowers through here, tagged by Python
  -- operator — NOT through the `const.Nat.add`-style special cases (which only
  -- fire when a raw `Nat.add`/`Int.tdiv` const appears directly, e.g. via a
  -- comparison-decl or an un-inlined reference).  Both are listed so the report
  -- shows which path a construct actually took.
  "hop.+", "hop.-", "hop.*", "hop.//", "hop.%", "hop.**", "hop.==", "hop.<",
  "hop.<=", "hop.unary-",
  -- Nat/Int direct-const handlers + arithmetic-semantics special cases
  "const.Nat.div", "const.Nat.mod", "const.Nat.pow", "const.Nat.beq",
  "const.Nat.ble", "const.Nat.blt", "const.Nat.decLt", "const.Nat.decLe",
  "const.Nat.succ", "const.Nat.pred", "const.Nat.xor", "const.Nat.min",
  "const.Nat.max", "const.Nat.sqrt", "const.Nat.sub",
  "const.Int.tdiv", "const.Int.tmod", "const.Int.neg", "const.Int.toNat",
  "const.Int.natAbs", "const.Int.decLt", "const.Int.decLe",
  -- String / Char (barely tested today — a Phase-1 target)
  "const.String.length", "const.String.mk", "const.String.toList",
  "const.String.push", "const.String.isEmpty", "const.String.append",
  "const.String.startsWith", "const.String.endsWith", "const.List.asString",
  "const.Char.isAlpha", "const.Char.isDigit", "const.Char.isAlphanum",
  "const.Char.isLower", "const.Char.isUpper", "const.Char.isWhitespace",
  "const.Char.toUpper", "const.Char.toLower", "const.Char.toNat", "const.Char.ofNat",
  "const.String.push",
  -- Array (the qsort family — F13 lived here)
  "const.Array.size", "const.Array.toList", "const.Array.qsort",
  "const.Array.push", "const.Array.swapIfInBounds", "const.List.toArray",
  -- List combinators / utilities
  -- Note: Lean 4.31 lowers `List.map`/`filter`/`take`/`length` to their
  -- tail-recursive counterparts (`*TR`) in LCNF, so those are the spellings that
  -- fire; the plain spellings are kept as handled synonyms but rarely fire.
  "const.List.nil", "const.List.cons", "const.List.headD", "const.List.reverse",
  "const.List.append", "const.List.mapTR", "const.List.filterTR",
  "const.List.filterMap", "const.List.filterMapTR", "const.List.flatMap",
  "const.List.foldl", "const.List.foldrTR", "const.List.all",
  "const.List.any", "const.List.takeTR", "const.List.drop", "const.List.range",
  "const.List.find?", "const.List.findSome?", "const.List.eraseDups",
  "const.List.zipIdx", "const.List.set", "const.List.contains", "const.List.elem",
  "const.List.isEmpty", "const.List.mergeSort", "const.List.head?",
  "const.List.tail?", "const.List.getLast?", "const.List.dropLast",
  "const.List.dropLastTR", "const.List.replicateTR", "const.List.isPrefixOf",
  "const.List.dropWhile", "const.List.takeWhile",
  -- Option
  "const.Option.some", "const.Option.none", "const.Option.bind",
  "const.Option.isSome", "const.Option.isNone", "const.Option.getD",
  -- Prod / bool / decide / misc
  "const.Prod.mk", "const.Bool.true", "const.Bool.false", "const.getElem?",
  "const.bne", "const.xor",
  -- Structural (proj / cases / whole-decl) handlers
  "proj.GetElem?", "proj.GetElem.valid", "proj.GetElem!", "proj.Max", "proj.Min",
  "proj.Prod", "proj.field",
  "cases.Bool", "cases.Nat", "cases.Decidable", "cases.Option", "cases.List",
  "struct.inductive", "struct.tailLoop"
]

def emitPythonForDecls (modName : Name) (decls : Array Decl) : CompilerM String := do
  -- First collect custom types
  let customTypes ← collectTypesFromDecls decls
  let ctx : Context := { modName }
  -- Global name de-duplication (F18): distinct top-level decls can map to the
  -- same `toPyFnName` (e.g. `Corpus.Sorting.mode`'s helper `count` vs
  -- `Corpus.Strings.count`), so the later `def` would shadow the earlier and
  -- calls resolve wrong.  Assign each decl a unique Python name up front,
  -- suffixing collisions (`count`, `count_2`, …), and pre-seed `usedNames` so
  -- nested/local `def`s (via `registerVar`) also steer clear of these names.
  let mut fnNames : Std.HashMap Name String := {}
  let mut used : Std.HashSet String := {}
  for decl in decls do
    let base := toPyFnName decl.name
    let mut nm := base
    let mut i := 2
    while used.contains nm do
      nm := s!"{base}_{i}"
      i := i + 1
    used := used.insert nm
    fnNames := fnNames.insert decl.name nm
  let (_, st) ← (do
    emitFileHeader
    -- Emit custom inductive types
    for typeName in customTypes do
      emitInductiveType typeName
    -- Emit function declarations
    for decl in decls do
      emitDecl decl
  ).run ctx |>.run { globalFnNames := fnNames, usedNames := used }
  -- Self-coverage: append which handlers fired as trailing Python COMMENTS.
  -- Comments are inert to `exec`, so they ride safely inside the fuzzer's
  -- `### PYTHON` section (a `#eval`'s `IO.eprintln` gets captured to the same
  -- stream as stdout and would land mid-output, corrupting the parse — hence
  -- comments in the returned buffer rather than stderr).  Two lines: the fired
  -- tags and the full known-tag universe (the report's denominator).  A
  -- `fallthrough.<coreNamespace>` tag among the fired set signals a special
  -- handler a Lean change may have silently broken — the fuzzer flags it.
  let fired := st.firedHandlers.toList
  let firedLine := s!"# HANDLERS_FIRED\t{"\t".intercalate fired}"
  let knownLine := s!"# HANDLERS_KNOWN\t{"\t".intercalate knownHandlerTags}"
  return st.buf ++ "\n" ++ firedLine ++ "\n" ++ knownLine ++ "\n"

def emitPython (modName : Name) : CoreM String := do
  let env ← getEnv
  let mut decls := #[]
  let baseDecls := baseExt.getState env
  for (_, decl) in baseDecls do
    decls := decls.push decl
  CompilerM.run (emitPythonForDecls modName decls)

/-- Check if name has baseName as a prefix ancestor -/
def hasAncestor (name baseName : Name) : Bool := Id.run do
  let mut n := name.getPrefix
  while !n.isAnonymous do
    if n == baseName then return true
    n := n.getPrefix
  return false

/-- The top-level component of a name (`Corpus.Math.gcd` → `Corpus`). -/
partial def rootComponent (n : Name) : Name :=
  let p := n.getPrefix
  if p.isAnonymous then n else rootComponent p

/-- Should a called constant be emitted as its own Python `def`?  We pull in a
    callee when it is an internal helper of the base function (`foo.go`), OR a
    *sibling* user definition sharing the same top-level namespace root (e.g.
    another `Corpus.*` function that this one calls) so the emitted module is
    self-contained.  Stdlib callees (`List.*`, `Nat.*`, …) have a different root
    and are handled by the builtin/stdlib special cases instead. -/
def isEmittableCallee (name baseName : Name) : Bool :=
  hasAncestor name baseName
  || (rootComponent name == rootComponent baseName && rootComponent name != baseName)

partial def collectHelperNames (decl : Decl) : CompilerM (List Name) := do
  let baseName := decl.name
  let helpersRef ← IO.mkRef ([] : List Name)
  let visitedRef ← IO.mkRef ({} : Lean.NameSet)

  let rec visit (code : Code) : CompilerM Unit := do
    match code with
    | .let ld k =>
      -- Check let value for helper calls
      match ld.value with
      | .const name _ _ =>
        if isEmittableCallee name baseName then
          let visited := (← visitedRef.get)
          if !visited.contains name then
            visitedRef.modify (·.insert name)
            helpersRef.modify (name :: ·)
            -- Recursively look for helpers called by this helper
            try
              let helperDecl ← toDecl name
              visit (declCode helperDecl)
            catch _ =>
              pure ()
      | _ => pure ()
      visit k
    | .fun fd k =>
      visit fd.value
      visit k
    | .jp fd k =>
      visit fd.value
      visit k
    | .jmp _ _ => pure ()
    | .cases cs =>
      for alt in cs.alts do
        match alt with
        | .alt _ _ c => visit c
        | .default c => visit c
    | .return _ => pure ()
    | .unreach _ => pure ()

  visit (declCode decl)
  helpersRef.get

def emitPythonForNames (modName : Name) (names : List Name) : CoreM String := do
  let decls ← CompilerM.run do
    let mut allNames : List Name := names
    let mut processed : Lean.NameSet := {}
    let mut decls := #[]
    -- First pass: collect main declarations and their helpers
    for name in names do
      if processed.contains name then continue
      try
        let decl ← toDecl name
        let helpers ← collectHelperNames decl
        allNames := helpers ++ allNames
      catch _ =>
        pure ()
    -- Second pass: compile all declarations (helpers first, then main)
    let orderedNames := allNames.reverse.eraseDups.reverse
    for name in orderedNames do
      if processed.contains name then continue
      processed := processed.insert name
      try
        let decl ← toDecl name
        decls := decls.push decl
      catch _ =>
        pure ()
    return decls
  CompilerM.run (emitPythonForDecls modName decls)

end LeanToPython
