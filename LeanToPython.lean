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
  nextTmpIdx : Nat := 0

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

/-- Alias one variable to another -/
def aliasVar (from_ to_ : FVarId) : EmitM Unit :=
  modify fun s => { s with varAliases := s.varAliases.insert from_ to_ }

/-- Mark a variable as holding a type class instance -/
def markAsInstance (fvarId : FVarId) (instName : Name) : EmitM Unit :=
  modify fun s => { s with instanceVars := s.instanceVars.insert fvarId instName }

/-- Mark a variable as holding an extracted operation from an instance -/
def markAsExtractedOp (fvarId : FVarId) (instName : Name) (fieldIdx : Nat) : EmitM Unit :=
  modify fun s => { s with extractedOps := s.extractedOps.insert fvarId (instName, fieldIdx) }

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
  | ``Int.div => some "//"
  | ``Int.mod => some "%"
  | ``Int.decLt => some "<"
  | ``Int.decLe => some "<="
  | ``BEq.beq => some "=="
  | _ => none

/-- Builtin functions that wrap their argument -/
def builtinFn? (name : Name) : Option String :=
  match name with
  | ``String.length => some "len"
  | ``List.length => some "len"
  | ``Array.size => some "len"
  | ``Bool.not | ``not => some "not"
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
  | ``List.filter => some "list(filter({}, {}))"  -- special format
  | ``List.map => some "list(map({}, {}))"  -- special format
  | ``List.filterMap => some "[y for x in {} if (y := {}(x)) is not None]"
  | ``List.find? => some "next((x for x in {} if {}(x)), None)"
  | ``List.any => some "any({} for x in {})"  -- special
  | ``List.all => some "all({} for x in {})"  -- special
  | ``List.eraseDups => some "list(dict.fromkeys({}))"
  | ``List.enum => some "list(enumerate({}))"
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
  else none

/-- Check if this is a BEq operation -/
def isBEqOp (name : Name) : Bool :=
  name == ``BEq.beq || name.toString == "beq"

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
  | ``instBEqNat => some "=="
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
  | .natVal n => emit (toString n)
  | .strVal s => emit (quotePyString s)

/-- Pure string form of a literal value (for expression-mode rendering). -/
def litValueStr (lit : LitValue) : String :=
  match lit with
  | .natVal n => toString n
  | .strVal s => quotePyString s

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
  | .value lit =>
    -- Record the literal for OfNat pattern
    recordLiteral lit
    return false  -- Don't skip, we'll emit it
  | .const name _ args =>
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
      return true
    return false
  | .proj _ idx fvarId =>
    -- Check if projecting from an instance
    if let some instName := (← get).instanceVars[fvarId]? then
      -- Special case: projecting from OfNat gives us the literal value
      let instStr := instName.toString
      if instName == ``instOfNatNat || instStr.startsWith "instOfNat" || containsSubstr instStr ".instOfNat" then
        if let some lit := (← get).lastLiteral then
          markAsLiteralVar decl.fvarId lit
          return true  -- Skip this, but the var is now a known literal
      -- Check if this is a known arithmetic operator we can inline
      if hOpToPyOp? instName |>.isSome then
        markAsExtractedOp decl.fvarId instName idx
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
      -- Handle unary negation
      if op == "unary-" && args.size == 1 then
        emitIndent
        emit s!"{varName} = -"
        emitArg args[0]!
        emit "\n"
        return true
      -- Handle binary operations
      if args.size == 2 then
        emitIndent
        emit s!"{varName} = "
        emitArg args[0]!
        emit s!" {op} "
        emitArg args[1]!
        emit "\n"
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
  | .value v =>
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
    if let some op := natBinOp? declName then
      if args.size == 2 then
        return some s!"({← renderArg args[0]!} {op} {← renderArg args[1]!})"
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
        if op == "unary-" && args.size == 1 then
          return some s!"(-{← renderArg args[0]!})"
        if args.size == 2 then
          return some s!"({← renderArg args[0]!} {op} {← renderArg args[1]!})"
    -- Call of a (possibly deferred-lambda) function variable.
    if args.size == 0 then
      -- Value alias.
      aliasVar decl.fvarId fnVar
      return some ""
    -- Only inline a call to a locally-known function or a deferred lambda; a
    -- bare unknown fvar call is safe (it maps to a Python name), so allow it.
    return some s!"{← getVarName fnVar}({← renderArgs args})"
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
      return some (← getVarName fvarId)
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
          modify fun s => { s with buf := s.buf.take start, lastListComp := none }
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
  | .value v =>
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
    -- Check for direct Nat/Int binary operations
    if let some op := natBinOp? declName then
      if args.size == 2 then
        emitIndent
        emit s!"{varName} = "
        emitArg args[0]!
        emit s!" {op} "
        emitArg args[1]!
        emit "\n"
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
      emitArgs args
      emit ")\n"
      return
    -- Check for stdlib function mappings
    if let some pyFn := stdlibFnToPython? declName then
      -- Handle simple wrapper functions like len, list, etc.
      if !containsSubstr pyFn "{}" then
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
    -- Special handling for List.map and List.filter - use idiomatic list comprehensions
    if declName == ``List.map then
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
    if declName == ``List.filter then
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
    if declName == ``List.filterMap then
      if args.size >= 2 then
        let (binder, body) ← fnCompParts args[args.size - 2]! "x"
        let xs ← renderArg args[args.size - 1]!
        emitIndent
        emit s!"{varName} = [_y for {binder} in {xs} if (_y := {body}) is not None]\n"
        return
    -- List.bind (flatMap): [y for x in xs for y in f(x)]
    if declName == ``List.bind then
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
    if declName == ``List.foldr then
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
    -- List.get? - safe indexing
    if declName == ``List.get? then
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
    -- List.enum - enumerate with indices
    if declName == ``List.enum then
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
      if args.size >= 2 then
        emitIndent
        emit s!"{varName} = sorted("
        emitArg args[args.size - 2]!  -- array
        emit ", key=functools.cmp_to_key(lambda a, b: -1 if "
        emitArg args[args.size - 1]!  -- comparator (lt function)
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
    -- Char.isDigit
    if declName == ``Char.isDigit then
      if args.size >= 1 then
        emitIndent
        emit s!"{varName} = "
        emitArg args[args.size - 1]!
        emit ".isdigit()\n"
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
      if declName == ``Char.isDigit then
        emitIndent
        emit s!"{varName} = (lambda c: c.isdigit())\n"
        return
      if declName == ``Char.isAlpha then
        emitIndent
        emit s!"{varName} = (lambda c: c.isalpha())\n"
        return
      if declName == ``Nat.xor then
        emitIndent
        emit s!"{varName} = (lambda a, b: a ^ b)\n"
        return
    -- Regular function call
    emitIndent
    emit s!"{varName} = {toPyFnName declName}("
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
        emitIndent
        emit s!"{varName} = (lambda xs, i: xs[i] if 0 <= i < len(xs) else None)\n"
        return
      else if idx == 0 then
        -- Project 0 (valid?) is the validity predicate
        emitIndent
        emit s!"{varName} = (lambda xs, i: 0 <= i < len(xs))\n"
        return
    -- Max instance - project 0 is the max function
    if containsSubstr typeStr "Max" && idx == 0 then
      emitIndent
      emit s!"{varName} = max\n"
      return
    -- Min instance - project 0 is the min function
    if containsSubstr typeStr "Min" && idx == 0 then
      emitIndent
      emit s!"{varName} = min\n"
      return
    emitIndent
    emit s!"{varName} = "
    emit (← getVarName structFvar)
    -- Use tuple indexing for Prod type, otherwise field access
    if typeName == ``Prod then
      emit s!"[{idx}]\n"
    else
      emit s!".{toPyFnName typeName}_{idx}\n"

/-- Check if a type is PUnit or Unit -/
def isUnitType (e : Expr) : Bool :=
  match e with
  | .const ``PUnit _ => true
  | .const ``Unit _ => true
  | _ => false

/-! ## Code Emission -/

mutual

partial def emitCode (code : Code) : EmitM Unit := do
  match code with
  | .let decl k =>
    emitLetValue decl
    emitCode k
  | .fun decl k =>
    emitLocalFun decl
    emitCode k
  | .jp decl k =>
    emitJoinPoint decl
    emitCode k
  | .jmp fvarId args =>
    emitIndent
    emit s!"return {← getVarName fvarId}("
    emitArgs args
    emit ")\n"
  | .cases cases =>
    emitCases cases
  | .return fvarId =>
    emitIndent
    -- Check if returning a known literal
    if let some lit := (← get).literalVars[fvarId]? then
      emit "return "
      emitLitValue lit
      emit "\n"
    else if let some b := (← get).boolVars[fvarId]? then
      emit s!"return {if b then "True" else "False"}\n"
    else
      emit s!"return {← getVarName fvarId}\n"
  | .unreach _ =>
    emitIndent
    emit "raise RuntimeError(\"unreachable\")\n"

partial def emitLocalFun (decl : FunDecl) : EmitM Unit := do
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
        -- Roll back render-time mutations, then fall through to a real def.
        set snapshot
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

partial def emitCases (cases : Cases) : EmitM Unit := do
  let discr ← getVarName cases.discr
  if cases.typeName == ``Bool then
    emitBoolCases discr cases.alts
  else if cases.typeName == ``Nat then
    emitNatCases discr cases.alts
  else if cases.typeName == ``Decidable then
    -- Decidable has isFalse and isTrue constructors
    -- Need to check the discriminant type to determine if it's a "match on Nat" vs "if bool"
    emitDecidableCases discr cases.discr cases.alts
  else if cases.typeName == ``Option then
    emitOptionCases discr cases.alts
  else if cases.typeName == ``List then
    emitListCases discr cases.alts
  else
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
  -- Find none case
  for alt in alts do
    match alt with
    | .alt ctorName _ code =>
      if ctorName == ``Option.none then
        withIndent do emitCode code
    | _ => pure ()
  emitIndent
  emit "else:\n"
  -- Find some case
  for alt in alts do
    match alt with
    | .alt ctorName params code =>
      if ctorName == ``Option.some then
        withIndent do
          if params.size > 0 then
            let valName ← registerVar params[params.size - 1]!.fvarId params[params.size - 1]!.binderName
            emitLn s!"{valName} = {discr}"
          emitCode code
    | _ => pure ()

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
  -- Find cons case
  for alt in alts do
    match alt with
    | .alt ctorName params code =>
      if ctorName == ``List.cons then
        withIndent do
          if params.size >= 2 then
            let headName ← registerVar params[params.size - 2]!.fvarId params[params.size - 2]!.binderName
            let tailName ← registerVar params[params.size - 1]!.fvarId params[params.size - 1]!.binderName
            emitLn s!"{headName} = {discr}[0]"
            emitLn s!"{tailName} = {discr}[1:]"
          emitCode code
    | _ => pure ()

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
  let fnName := toPyFnName decl.name
  -- Emit a comment with the full Lean name for traceability
  emitLn s!"# Lean: {decl.name}"
  emitIndent
  emit s!"def {fnName}("
  emitFunParams decl.params
  emit ")"
  -- The decl.type is the *result* type after all parameters are applied
  let retType ← toPyTypeHint (getReturnType decl.type)
  emit s!" -> {retType}:\n"
  withIndent do
    emitCode decl.value
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
    types ← collectTypesFromCode decl.value types
  return types

def emitPythonForDecls (modName : Name) (decls : Array Decl) : CompilerM String := do
  -- First collect custom types
  let customTypes ← collectTypesFromDecls decls
  let ctx : Context := { modName }
  let (_, { buf, .. }) ← (do
    emitFileHeader
    -- Emit custom inductive types
    for typeName in customTypes do
      emitInductiveType typeName
    -- Emit function declarations
    for decl in decls do
      emitDecl decl
  ).run ctx |>.run {}
  return buf

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

/-- Collect helper names by walking the code and looking for const calls with matching prefix -/
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
        if hasAncestor name baseName then
          let visited := (← visitedRef.get)
          if !visited.contains name then
            visitedRef.modify (·.insert name)
            helpersRef.modify (name :: ·)
            -- Recursively look for helpers called by this helper
            try
              let helperDecl ← toDecl name
              visit helperDecl.value
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

  visit decl.value
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
