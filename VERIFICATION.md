# Verification & Bugs Found

This document records how the SnakeLean transpiler is verified and every
transpilation bug that verification has caught and fixed. It complements the
[Correctness](README.md#correctness) section of the README, which describes the
standing test layers; this file is the historical bug ledger and a description
of the two *bug-finding* techniques (differential round-tripping and
grammar-based fuzzing) that produced most of the fixes.

All bugs below are in `SnakeLean.lean` (the transpiler) unless noted. Each
was reduced to a minimal Lean input, fixed, and covered by a regression check.

## Bug-finding techniques

### Differential round-trip (Lean as oracle) — `roundtrip/`

For a curated and an exhaustive battery of corpus functions, Lean `#eval`s the
function and the transpiled Python is run on the same inputs; any disagreement
is a bug. Lean is the ground truth, so this needs no hand-written expected
values. See [`roundtrip/README.md`](roundtrip/README.md). Exhaustive mode covers
the *entire* bounded input domain (all `n ∈ [0,60]`, all `(x,y) ∈ [0,25]²`).

### Grammar-based fuzzing — `fuzz/`

`fuzz/gen.py` generates random **well-typed, terminating** Lean function
definitions from a small typed grammar (over `Nat` / `Bool` / `List Nat` /
`Nat × Nat`), exercising `if`/`match` (Nat/List/Option), `let`, tuples,
arithmetic (incl. truncated `Nat` subtraction and guarded div/mod), list
combinators, `DecidableEq`, and fuel-bounded recursion. `fuzz/fuzz.py` runs each
generated program through the same Lean-as-oracle pipeline and flags:

- **syntax** — transpiled Python doesn't parse,
- **exec / runtime** — a NameError/TypeError at import or call time,
- **mismatch** — Python and Lean disagree on a value.

Generation is **coverage-guided** (Havrikov & Zeller, ASE 2019): each grammar
choice is a labeled production and the generator prefers productions not yet
covered *within a file*, so a short sweep exercises every construct rather than
relying on uniform sampling. `fuzz.py` reports aggregate production coverage
(e.g. `61/61`). Guidance is per-seed, so output stays a pure function of the
seed.

It also applies **EMI + guided stochastic mutation** (Le/Afshari/Su PLDI 2014;
Le/Sun/Su OOPSLA 2015): each generated subterm is stochastically wrapped in a
semantics-*preserving* identity envelope (`x` → `(x + 0)`, `b` → `!!b`,
`xs` → `xs.reverse.reverse`, …). The envelope computes the same value, so the
Lean oracle is unchanged, but the transpiler sees a different, deeper term —
each seed becomes many differential tests over shapes the base grammar would not
reach. The envelope count is stochastic and the choice is coverage-guided
(`--emi P`, default 0.3).

On failure it **shrinks** to the smallest `(defs, inputs)` that still fails and
saves a reproducer under `fuzz/repro/`. Seeds are deterministic, so a failing
seed reproduces exactly. Run:

```bash
python3 fuzz/fuzz.py --seeds 200            # broad sweep
python3 fuzz/fuzz.py --seeds 1 --start 18   # reproduce one seed
```

The generator only emits well-typed, provably-terminating code, so any Lean
elaboration error means the *generator* produced something out of range (those
seeds are skipped and counted, not reported as transpiler bugs).

## Bugs found by grammar-based fuzzing

These are semantic/soundness bugs the curated corpus never happened to exercise
in the offending shape. The first is the most serious: a **silent wrong
answer**, not a crash.

### F1. `Nat` subtraction emitted as Python `-` (silent wrong value)

- **Seed:** 1 · **Kind:** mismatch (`python=[8, -64]` vs `lean=[8, 0]`)
- **Root cause:** Lean `Nat` subtraction is *truncated* (monus): `8 - 72 = 0`.
  The transpiler emitted plain Python `-`, which goes negative.
- **Fix:** emit `max(0, a - b)` for `Nat` subtraction. `Nat.sub` is
  unambiguously Nat. The generic `HSub.hSub` is polymorphic, so a small
  propagation tags the concrete `instSubNat` instance, follows it through the
  `instHSub` wrapper that carries it, and onto the projected `.hSub` op
  (`natSubVars`); Int subtraction is left as `-`.

### F2. `List.headD` not mapped

- **Seed:** 1 · **Kind:** runtime (`NameError: name 'head_d' is not defined`)
- **Root cause:** `List.headD xs d` (head-or-default) had no Python mapping, so
  it was emitted as a call to an undefined snake-cased name.
- **Fix:** special-case `List.headD` to `(xs[0] if xs else d)`.

### F3. `!=` (`bne`) emitted as a mis-applied lambda

- **Seed:** 1 · **Kind:** runtime (`TypeError: <lambda>() missing 1 required
  positional argument: 'b'`)
- **Root cause:** `bne` only had a first-class-value fallback
  (`(lambda a, b: a != b)`); when applied to two operands split across a join
  point it was emitted as that lambda and then called with one argument.
- **Fix:** recognize `bne`/`Ne` (`isBNeOp`) as an inline binary operator and
  emit `a != b` directly, mirroring the existing `==` (`isBEqOp`) handling.
  The lambda form remains as a fallback for `bne` used as a value.

### F4. `match` on a literal discriminant referenced an unbound variable

- **Seed:** 11 · **Kind:** runtime (`NameError: name '_x_20' is not defined`)
- **Root cause:** `match v with …` where `v` is a `let`-bound literal (via an
  `OfNat` projection whose binding was elided) emitted the discriminant as a
  bare variable name that was never assigned.
- **Fix:** in `emitCases`, resolve the discriminant through aliases and known
  literal vars, emitting the literal value (e.g. `if 4 == 0:`) instead of an
  unbound name.

### F5. `OfNat` literal collision (silent wrong value)

- **Seed:** 18 · **Kind:** mismatch (`python=0` vs `lean=5`; minimal:
  `if p then 6 else …` returned `1`)
- **Root cause:** `OfNat.ofNat` projections recovered their literal from a
  single global "last literal seen" slot. An intervening literal (e.g. the `1`
  in `6 + 1`) clobbered it before the projection for `6` was reached, so `6`
  was mis-read as `1`.
- **Fix:** key each raw literal to its own fvar, capture the literal against the
  specific `instOfNatNat` instance (whose sole argument *is* that literal), and
  have the projection read the instance-specific literal instead of the global
  slot.

### F6. Returning a `let`-bound literal referenced an unbound variable

- **Seed:** 56 · **Kind:** runtime (`NameError: name '_x_99' is not defined`;
  minimal: `let v1 := 8; v1` emitted `return _x_99`)
- **Root cause:** the `return` emitter checked `literalVars`/`boolVars` by the
  raw fvar, but a returned variable is often an *alias* of the literal var whose
  own binding was elided, so the lookup missed and it emitted the unbound name.
- **Fix:** resolve aliases before the literal/bool lookup in the `return`
  emitter.

### Grammar expansion — adding `Int` and `Option Nat`

Widening the grammar beyond `Nat`/`Bool`/`List Nat` (the *grammar expansion*
technique: bugs hide in constructs the grammar never generates) immediately
surfaced five more, two of them silent wrong values.

### F7. `Nat → Int` coercion emitted as a call to undefined `cast`

- **Kind:** runtime (`NameError: name 'cast' is not defined`)
- **Root cause:** the `Nat → Int` coercion (`Nat.cast` via `instNatCastInt`) was
  emitted through the generic const path as `cast(None, inst, x)`.
- **Fix:** treat numeric coercions (`Nat.cast`/`NatCast.natCast`/`Int.ofNat`) as
  identity in Python (both are `int`), aliasing to the coerced value — the
  *last* fvar argument (the earlier fvar is the typeclass instance).

### F8. `Int.toNat` not mapped (would be a silent wrong value)

- **Kind:** runtime (`NameError: name 'to_nat'`)
- **Root cause:** `Int.toNat` was unmapped. It clamps negatives to 0
  (`(-5).toNat = 0`), so even the "obvious" identity mapping would be wrong.
- **Fix:** emit `max(0, x)`.

### F9. `List.take`/`drop` emitted as a mis-applied lambda

- **Kind:** runtime (`NameError: name 'take_tr'`, then a `TypeError`)
- **Root cause:** `List.take` lowers to `List.takeTR` in 4.31 (unmapped); and
  the `stdlibFnToPython?` lambda forms for `take`/`drop`
  (`(lambda n, xs: xs[:n])`) were treated by the generic handler as *bare
  callables* and applied to a single argument. This was a latent bug for every
  lambda-form stdlib entry.
- **Fix:** dedicated `take`/`drop` emission (`xs[:n]` / `xs[n:]`, recognizing the
  `*TR` form), and the generic handler now only treats a `pyFn` as a bare
  callable when it contains no `(`, space, or `{}` — lambda/format forms must be
  special-cased.

### F10. Euclidean `Int` division / modulo emitted as Python `//` / `%` (silent wrong value)

- **Seed:** 11 · **Kind:** mismatch (`python=-7` vs `lean=-9`)
- **Root cause:** Lean's `Int./` and `Int.%` are **Euclidean** (the remainder is
  always non-negative: `(-7) % 3 = 2`, `(-7) / 3 = -3`), whereas Python `//`/`%`
  *floor*. They diverge whenever operands have opposite signs. The transpiler
  emitted the raw Python operators.
- **Fix:** for `Int` division/modulo (tagged via the concrete `Int.instDiv`/
  `Int.instMod` instance, propagated like `natsub`), emit the Euclidean forms
  `(a - a % abs(b)) // b` and `a % abs(b)`, which match Lean bit-for-bit on all
  sign combinations. `Nat` and `Int` share the generic `instHDiv`/`instHMod`, so
  the per-instance tag is what distinguishes them.

### F11. `OfNat` literal collision on `Int` literals (silent wrong value)

- **Seed:** 36 · **Kind:** runtime (`ZeroDivisionError`, masking a wrong value:
  `0 == 0` emitted as `0 == 8`)
- **Root cause:** the same global-`lastLiteral` collision as F5, but for `Int`
  literals, whose `OfNat` instance is `instOfNat` (not the `instOfNatNat` that
  F5's fix special-cased). A nearby `8` literal clobbered a `0`.
- **Fix:** capture the per-instance literal for *any* `OfNat` instance
  (`instOfNat`/`instOfNatNat`/namespaced), not just `instOfNatNat`.

### F12. `Nat`/`Int` division & modulo by zero (crash on a total operation)

- **Found by:** fragment-reuse fuzzing (`--corpus`), `Corpus.Math.divMod` on
  `(a, 0)` · **Kind:** runtime (`ZeroDivisionError`)
- **Root cause:** Lean's `Nat`/`Int` division and modulo are **total** — `n / 0 =
  0` and `n % 0 = n` (for both `Nat` and the Euclidean `Int` variants) — whereas
  Python's `//` and `%` raise `ZeroDivisionError`. The transpiler emitted the
  bare Python operators. The generative grammar never hit this because it always
  guards its divisors (`b + 1` / `if b == 0 then 1 else b`); only *real* corpus
  code divides by an unguarded parameter.
- **Fix:** a central `guardZeroDiv` wraps every `//` / `%` emission (all four
  sites + the Euclidean `emitArithBinary` forms) as `(expr if b != 0 else <Lean
  value>)` — `0` for division, the dividend for modulo — matching Lean on every
  input including zero divisors.

### F13. `Array.qsort` argument mis-indexing (crash)

- **Found by:** fragment-reuse fuzzing (`--corpus`), `Corpus.Games.yahtzeeScore`
  · **Kind:** runtime (`TypeError: 'int' object is not iterable`)
- **Root cause:** `Array.qsort (as) (lt) (low := 0) (high := as.size - 1)` has two
  trailing `optParam`s that recent Lean **materializes**, so the LCNF value args
  are `[…, as, lt, low, high]`. The handler grabbed the *last two* — `low`/`high`
  — emitting `sorted(0, key=<high>(a, b))` (sorting the integer `0`).
- **Fix:** index the array and comparator from `size-4`/`size-3` when four value
  args are present, with a fallback to the old `size-2`/`size-1` shape for older
  Lean versions that don't materialize the optParams.

### F14. Char/String/Array method calls fell through to undefined Python names

- **Found by:** Phase-1 String/Char/Array fuzzing (grammar + `--corpus`)
  · **Kind:** runtime (`NameError`/`TypeError: name 'to_upper' is not defined`)
- **Root cause:** method-call forms `c.toUpper`, `c.isUpper`, `s.push c`,
  `a.push x` lower to `.const Char.toUpper` / `String.push` / `Array.push` in
  LCNF, but only *some* Char spellings had emission handlers (isDigit) and the
  `stdlibFnToPython?` lambda entries fire only when the op is used as a bare
  function *value*, not called. Uncovered ops fell through to `toPyFnName`, which
  snake-cases the Lean name → a call to an undefined `to_upper`/`is_upper`/
  `string_push`/`array_push`. Exactly the class of bug the self-coverage metric
  predicts (these handlers showed "never fired" pre-Phase-1).
- **Fix:** dedicated handlers for `Char.toUpper`/`toLower` (→ `.upper()`/
  `.lower()`), `Char.isUpper`/`isLower`/`isAlpha`/`isAlphanum`/`isWhitespace`
  (→ `.isupper()`/… ), `String.push s c` (→ `s + c`), and `Array.push a x`
  (→ `a + [x]`, matching Lean's persistent/functional Array), plus the
  bare-function-value forms. All verified equal to Lean on the ASCII range
  (Lean's Char predicates are ASCII-only, matching Python's `str` predicates
  there; a documented Unicode-widening target could surface a real divergence).

### F15. `xs[i]!` panic-indexing referenced elided instances (crash)

Fixed on `main` before this Phase-1 branch (see PR #16); listed here for the
ledger. This is what the `Corpus.Production` `_x_266` failures actually were —
NOT a batched-emission name collision, as first suspected.

- **Found by:** Phase-1 Array fuzzing (`Corpus.Production.quicksort` via
  `lomutoPartition`'s `arr[hi]!`); reproduces on plain `List` too (`xs[i]!`)
  · **Kind:** runtime (`NameError: name '_x_266' is not defined`)
- **Root cause:** `xs[i]!` is `GetElem?.getElem! … <GetElem-inst> <Inhabited-inst>
  xs i`. In LCNF the `getElem!` method is a `.proj` (field 2) of the `GetElem`
  instance, then called with the `Inhabited` instance as a leading argument. Both
  instances are *elided* (the transpiler never emits typeclass instances), but the
  projection emitted `_x_N.field_2` and the call passed `_x_M` — referencing the
  unbound instance names. The `.proj` handler covered `GetElem?` idx 0/1
  (`getElem?`/valid) but not idx 2 (`getElem!`), and `emitArg`/`renderArg` had no
  case for an instance-valued arg.
- **Fix:** (a) handle `.proj` idx 2 on a `GetElem` instance as
  `(lambda _inst, xs, i: xs[i])` — absorbing the leading `Inhabited` arg and
  indexing directly (Lean panics on OOB, Python raises `IndexError` — both errors,
  so the differential oracle stays consistent); (b) `emitArg`/`renderArg` now emit
  `None` for a var known to be a typeclass instance, so any elided instance
  threaded as an argument is a harmless placeholder the callee ignores.

### F16. Missing Lean List/Array/String builtins (undefined-name / crash)

- **Found by:** Phase-1 corpus fuzzing over `Corpus.Strings.*`/`Corpus.Production.*`
  · **Kind:** runtime (`NameError`/`TypeError` on snake-cased undefined names)
- **Root cause:** several common Lean builtins had no handler and fell through to
  `toPyFnName` → undefined `drop_while`/`replicate_tr`/`drop_last_tr`/
  `swap_if_in_bounds`/`starts_with`/`is_prefix_of`.
- **Fix (all verified equal to Lean, incl. empty/OOB edge cases):**
  `List.dropLast`/`dropLastTR` → `xs[:-1]`; `List.replicate`/`replicateTR n x` →
  `[x] * n`; `List.isPrefixOf p xs` → `xs[:len(p)] == p`; `List.dropWhile`/
  `takeWhile` → `itertools.dropwhile`/`takewhile`; `Array.swapIfInBounds a i j` →
  a non-mutating copy-and-swap lambda (identity when out of bounds, matching
  Lean's persistent Array); `String.startsWith`/`endsWith` → `str.startswith`/
  `endswith` (filtering the elided pattern-typeclass instance args).
- **Impact:** un-blocked `Corpus.Production.*` (no longer excluded from harvest);
  corpus harvest 82 → 83.

### F17. Deferred continuation referenced an unemitted helper (`_uniq_NNN`)

- **Found by:** Phase-1 corpus fuzzing over `Corpus.Strings.*` (`splitOn`,
  `replace`, …) · **Kind:** runtime (`NameError: name '_uniq_644' is not defined`)
- **Root cause:** expression-mode rendering (`renderExprCode` /
  `renderLetValueExpr`, used to inline single-param lambdas) resolved a
  referenced fvar via `getVarName`, which *invents* a fallback name from the raw
  fvar (`_uniq_NNN`) when it was never bound. So a match-arm continuation that
  called an **unemitted sibling** local function "rendered" successfully as
  `_uniq_644(...)` — a name that never got a `def`. Deferring the lambda then
  emitted that dangling call.
- **Fix:** added `knownVarName?` (like `getVarName` but no fallback); the
  expression-mode `.return` and fvar-call paths now REFUSE to render a reference
  to an unbound fvar (return `none`), so `emitLocalFun` falls back to emitting a
  real `def` for the continuation. That fallback then exposed a second issue —
  the continuation carries the enclosing tail-loop's `continue`, illegal inside a
  nested `def` — so in tail-loop mode such a continuation is now routed to
  `inlineThunks` (inlined at its tail-call site where `continue` is legal) rather
  than emitted as a `def`.
- **Impact:** cleared the entire `Corpus.Strings.*` namespace (45 functions) for
  *per-function* transpilation — which then exposed F18.

### F18. Cross-function top-level name collision (shadowing → wrong body)

- **Found by:** the **scaled** corpus sweep (3000 seeds on cloudnew — a bug the
  100-seed local run missed): `Corpus.Sorting.mode([0,8,8])` → `TypeError: 'int'
  object is not iterable`, only when `mode` was batched with `Corpus.Strings.*`.
- **Root cause:** `toPyFnName` is a *pure* function with a hand-curated collision
  list, so distinct Lean decls can map to the SAME Python name — e.g.
  `Corpus.Sorting.mode`'s helper `count` and `Corpus.Strings.count` both →
  `count` (and `isqrt`, `coprime`, `divisors`, `insertionSort`, … across
  modules).  When several land in one file the later `def` shadows the earlier,
  and every call resolves — by Python's late binding — to the wrong body.  Only
  manifests when the colliding functions are emitted together (fragment-reuse
  batches them; single-function runs never collide — why smaller sweeps passed).
- **Fix:** a pre-pass in `emitPythonForDecls` assigns each decl a globally-unique
  Python name up front (suffixing collisions: `count`, `count_2`, …) into
  `State.globalFnNames`; `pyFnName` routes the `def` and *every* call site through
  that map, and the assigned names pre-seed `usedNames` so nested/local `def`s
  steer clear too.
- **Impact:** all 128 harvestable corpus functions now transpile and agree with
  the oracle, **batched** as well as alone; `_KNOWN_OPEN_NS` is empty.

### F19. Nat/Int binary op passed point-free emitted an undefined name

- **Found by:** the **rust-lean-models corpus** (`RustLeanModels.RustString.
  sum_list_Nat := List.foldl Nat.add 0 l`); a 6-function feasibility spike.
  · **Kind:** runtime (`NameError: name 'add' is not defined`)
- **Root cause:** a Nat/Int arithmetic op is normally inlined as a Python
  operator when *applied* (`natBinOp?` in the `hop`/`const` paths).  Passed
  **point-free** as a higher-order argument (`List.foldl Nat.add`), it reaches
  the zero-value-args const path, which had a hand-written lambda only for
  `Nat.xor`; every other op fell through to `pyFnName`, snake-casing `Nat.add`
  → a call to an undefined `add`.  (`Nat`/`Int` `add`/`sub`/`mul`/`div`/`mod`/
  `pow`/`beq`/`ble`/`blt`/`decLt`/`decLe` all affected.)
- **Fix:** in the point-free const path, look the op up in `natBinOp?` and emit
  the matching 2-arg lambda (`(lambda a, b: a + b)`), mirroring the existing
  `Nat.xor` case, so the combinator receives a real callable.

### F20. `Char.utf8Size` had no handler and emitted an undefined name

- **Found by:** the **rust-lean-models corpus** (`RustString.byteSize` sums
  `Char.utf8Size` over a `List Char`; the library is built on `Str = List
  Char` and threads UTF-8 byte offsets everywhere).
  · **Kind:** runtime (`NameError: name 'utf8size' is not defined`)
- **Root cause:** no emission handler for `Char.utf8Size` (the UTF-8 encoded
  byte length of a char, 1–4); both applied (`c.utf8Size`) and point-free
  (`xs.map Char.utf8Size`) forms fell through to the snake-cased `utf8size`.
- **Fix:** dedicated handlers — applied → `len(c.encode('utf-8'))`, point-free
  → `(lambda c: len(c.encode('utf-8')))` — and added to `knownHandlerTags`.
  Verified equal to Lean's `Char.utf8Size` across the 1/2/3/4-byte ranges.

### Custom inductive / structure types (Phase 3 fragment-reuse expansion)

The fragment-reuse harvester now handles corpus functions whose parameters or
return type are **custom inductive/structure types** (enums like `RPS`/`Player`/
`Suit`; structs like `Card`/`Nim`/`UnionFind`) — not just the base value
universe.  A Lean-side dump (`fuzz/TypeInfo.lean`) reports each type's
constructors and field types; the harness computes which are *constructible*
(all fields base-typed or themselves constructible; recursive/`Float` types
excluded), generates values by applying constructors, emits per-type JSON
serializers into the oracle, and `run_oracle.normalize` reduces a transpiled
`@dataclass` instance to the same `{"c": ctor, "f": [...]}` shape for comparison.
This exercises the transpiler's inductive-emission + `match`-on-user-type paths
under differential testing for the first time.  *Result:* the transpiler is
correct on this slice — a 1500-seed sweep over 139 harvestable functions
(including 7 user-typed: `Nim`/`Card`/`RPS` methods) found **no transpiler bug**
(its inductive emission was already sound).  The phase's findings were two
*harness* issues, both fixed: (a) a fuzzer-constructed value of a type with an
internal invariant (`UnionFind`'s parent array must be acyclic) makes its
`find` loop forever — such types are now excluded from construction
(`_UNSAFE_TO_CONSTRUCT`), and `lean_run` gained a 60 s timeout so no single hung
`#eval` can stall the pool; (b) dataclass names for common constructors (`mk`,
`node`, …) are parent-prefixed (`Nim.mk` → `Nim_mk`), so the oracle serializer
and `run_oracle.normalize` must match `toPyTypeName` — they now do.

### Known-open

None currently in `corpus_frags._KNOWN_OPEN_NS`.  (`List.get!`/`Array.get!` — the
*named* method, not `[i]!` — still inlines Lean's panic machinery into garbage,
but no corpus function uses it, and the fuzzers never generate it.)

## Bugs found by the round-trip differential harness

Found while building `roundtrip/` (before fuzzing), by running corpus functions
against the Lean oracle.

### R1. Dropped `default` arm in list/option matches (empty block)

- **Kind:** syntax (`IndentationError` — empty `if:`/`else:`)
- **Root cause:** `emitListCases`/`emitOptionCases` handled only the *named*
  constructor arms (`List.nil`/`List.cons`, `Option.none`/`Option.some`). An
  n-way match lowers to *nested* binary `casesOn` whose inner non-nil / non-none
  case is a `default` arm, which was ignored — leaving an empty branch body.
- **Fix:** handle the `default` arm on both branches, with a `pass` safety net
  so a branch body is never empty. (list-cases fixed first; option-cases when
  the full corpus was later extracted.)

### R2. Transitive sibling callees not collected

- **Kind:** runtime (`NameError` for an un-emitted helper, e.g.
  `algorithms_split`, `number_theory_gcd`)
- **Root cause:** `collectHelperNames` pulled in only *same-ancestor* helpers
  (`foo.go`), so a function calling a **sibling** top-level function
  (`mergeSort` → `split`, `coprime` → `gcd`) referenced a name that was never
  emitted — the module wasn't self-contained.
- **Fix:** also collect callees that share the top-level namespace root
  (`isEmittableCallee` + `rootComponent`); stdlib callees have a different root
  and are still handled by the builtin/stdlib special cases.

### R3. `List.lengthTR` not mapped to `len`

- **Kind:** runtime (`NameError: name 'length_tr'`)
- **Root cause:** Lean 4.31 lowers `List.length` to the tail-recursive
  `List.lengthTR` in LCNF; only `List.length` was mapped.
- **Fix:** map `List.lengthTR` to `len` as well (same treatment as
  `map`/`filter`/`filterMap` → their `*TR` forms).

### R4. `Eq.ndrec` / `cast` proof-term leakage

- **Kind:** runtime (`NameError: name 'ndrec_symm'`)
- **Root cause:** proof-level identity casts (`Eq.ndrec`, `Eq.ndrec_symm`,
  `Eq.mpr`, `cast`, …) that leak into LCNF from `partial`/well-founded
  definitions were emitted as calls to undefined names.
- **Fix:** treat them as identity on their carried value — alias to the data
  argument (the fvar after the last type argument) and drop the cast.

## Bugs found earlier (upgrade & prior work)

For completeness, the Lean 4.12 → 4.31 toolchain upgrade and the enum/record
support work fixed a further set, verified against the `SmashCoreConc`
enum/record model (exhaustive 1440/1440) and the corpus:

- **Field-only inductive types never emitted** — a type used only as another
  type's field (never a param/return/matched type) was dropped; fixed by
  transitively collecting constructor-field types.
- **Derived `DecidableEq` comparison skipped** — `p.state = EMPTY` on a user
  enum was elided as "instance machinery" (its instance name contains `.inst`),
  dropping the boolean scrutinee; fixed by recognizing derived `DecidableEq` and
  not eliding an *applied* comparison.
- **Struct field projection name mismatch** — projections emitted
  `.<typename>_<i>` while the dataclass declared `field_<i>`, an `AttributeError`
  at runtime (syntactically valid, so `ast`/lint didn't catch it).
- **`Decidable.isTrue`/`isFalse` and `≠` mishandled** — emitted as opaque
  always-truthy dataclasses with wrong arity, and `instDecidableNot` aliased
  away (collapsing `≠` to `=`); fixed to lower to Python `bool`, emit exactly
  the value fields, and render `not <inner>`.

## Regression coverage

After every fix the full matrix is re-run green:

- `evaluate_correctness.py` — 132/132, 0 wrong
- `Comprehensions` / `TailCalls` / `RegressionFixes` structural suites
- `roundtrip/run.sh` — sampled 112/112 + exhaustive 3807/3807
- full-corpus extraction parses as valid Python
- `fuzz/fuzz.py` — with all fixes in place, a **5000-seed EMI-amplified batched
  parallel sweep** (192-core host, ~180-way) is clean: 4975 checked, 25
  ill-typed seeds skipped, 0 transpiler bugs, 61/61 production coverage, 89%
  k-path coverage. Each seed carries stochastic EMI envelopes, so this is far
  more than 5000 distinct code shapes.
- `fuzz/fuzz.py --corpus` — a **3000-seed fragment-reuse sweep** over real
  `Corpus/*.lean` definitions is clean (78/78 functions exercised) with F12/F13
  fixed; all 216 pre-fix failures were exactly those two bugs.

## Summary

23 transpiler bugs found and fixed across this work — 4 by the round-trip
differential harness (R1–R4), 11 by the grammar-based fuzzer (F1–F11), 7 by
fragment-reuse + Phase-1 type expansion (F12–F18), plus the upgrade-era set
— of which **six were silent wrong-value / total-operation bugs** (truncated
`Nat` subtraction, Euclidean `Int` division and modulo, two `OfNat` literal
collisions, and `Nat`/`Int` division-by-zero) that no crash-based check catches
on its own. The differential oracle (Lean's `#eval`) is what makes those
catchable. After F14–F17, all 128 harvestable corpus functions transpile
correctly (up from 78 before the String/Char/Array expansion).
