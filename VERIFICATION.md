# Verification & Bugs Found

This document records how the LeanToPython transpiler is verified and every
transpilation bug that verification has caught and fixed. It complements the
[Correctness](README.md#correctness) section of the README, which describes the
standing test layers; this file is the historical bug ledger and a description
of the two *bug-finding* techniques (differential round-tripping and
grammar-based fuzzing) that produced most of the fixes.

All bugs below are in `LeanToPython.lean` (the transpiler) unless noted. Each
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
(e.g. `36/36`). Guidance is per-seed, so output stays a pure function of the
seed.

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
- `fuzz/fuzz.py` — clean across a broad seed sweep
