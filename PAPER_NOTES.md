# Research claim, evidence, and open work

Written to be argued with. Mechanisms: [README](README.md#correctness). Bug
ledger: [VERIFICATION.md](VERIFICATION.md). Citations: [RELATED_WORK.md](RELATED_WORK.md).

## 1. Claim

> **When the source language has a trusted executable semantics, both test-case
> validity and the test oracle are free. Mutation is then decoupled from semantic
> preservation, and the binding constraint on bug-finding shifts from *reaching* a
> translation rule to *distinguishing* its semantics — where coverage, the field's
> standard adequacy signal, is blind.**

SnakeLean transpiles Lean 4 (total, pure, dependently typed) to idiomatic Python.
Lean ships a kernel and an evaluator, which buys two things.

**Validity, by construction.** A candidate program is elaborated by Lean; ill-typed
candidates fail and are discarded. Fuzzers for ordinary languages must *build* this
— a scope tree, a type map, and repair rules — and still only approximate it.

**An oracle, for any well-typed term.** This is the deeper one. EMI [1], the most
successful compiler-fuzzing idea of the last decade, is organized entirely around
*not* having an oracle: it may only apply mutations it can prove
semantics-*preserving*, since nothing can say what a mutated C program should
print. We are unconstrained. Lean evaluates whatever we generate, so we may mutate
arbitrarily and recompute ground truth. **The mutation operator and the oracle are
independent.**

Valid programs and ground truth are therefore not scarce. Good questions are.

## 2. Result: coverage is the wrong adequacy signal for translation rules

**F36.** The transpiler emitted Lean's truncated `Int` division as Python
`int(a / b)`, and truncated modulo as `int(math.fmod(a, b))` — routing an
*arbitrary-precision* `Int` through IEEE float64. Operands above 2^53 silently
round; past ~1e308 the program raises `OverflowError` instead of computing.

| expression | Lean | transpiled Python |
|---|---|---|
| `Int.tdiv (10^18+1) 3` | `333333333333333333` | `333333333333333312` |
| `Int.tmod (10^18+1) 7` | `2` | `1` |
| `Int.tdiv (10^400) 1` | 401-digit integer | `OverflowError` |

A silent wrong answer on the most-used arithmetic path a transpiler has. It
survived **two 5000-seed differential campaigns**, both reported clean. Meanwhile:

- **Translation-rule coverage** (`HANDLERS_FIRED`: white-box, per-rule, strictly
  stronger than basic-block coverage of the transpiler binary) reported the
  `inttdiv` rule **fired**.
- **Grammar production coverage: 100%.** k-path (k≤3): 86%.
- A hand-written regression case pinned `tdiv`/`tmod` *sign* semantics
  (`-7 tdiv 3`, `7 tdiv -3`, division by zero) — and passed.

Every instrument said "tested". Every instrument was correct, and every instrument
was useless.

**Coverage proves a rule ran. It cannot prove the rule ran on a value that
distinguishes two candidate semantics.** `tdiv(7,3)` and `tdiv(10^18+1,3)` traverse
identical code, fire identical rules, and cover identical productions — but only
one can tell float64 from an integer. Two structurally identical tests differ in
whether they are *capable* of detecting the bug, and no code-coverage metric can
see the difference.

The proposed replacement is a **distinguishing-value criterion**: per translation
rule, one witness for each semantic distinction the rule could get wrong —
precision boundary, sign, zero, overflow, wraparound, empty, NaN. Because the
oracle is free (§1), this is *measurable* rather than merely assertable.

**Evidence it is the right diagnosis.** We added exactly two mutators — boundary
values in the literal and input domains, and named-operator substitution (`.tdiv`
is reachable only by a named call, which the grammar could not previously write) —
and re-ran against the *unfixed* transpiler:

| transpiler | mutators | F36 detection |
|---|---|---|
| buggy | original | **0 detections in 2 × 5000 seeds** |
| buggy | + value domain, + named rules | **15 failing seeds / 300** |
| fixed | + value domain, + named rules | 0 / 300; 100% production coverage |

Neither mutator raises code coverage: production coverage was already 100%. The
gain is entirely in the *value* domain and the *rule-selection* domain — the two
axes coverage does not measure.

## 2b. EMP: Equivalence Modulo Proofs

The oracle in §1 is free but *sequential*: every candidate program pays for a Lean
elaboration. A proof assistant offers a second, stronger oracle that costs nothing at
test time.

Lean's environment contains **19,468 machine-checked equations at computable types**
(plus 311 `@[implemented_by]` pairs Lean's own compiler trusts) — with no Mathlib
imported. Each is a proof that **two different programs are the same program**.
Harvest them, transpile *both sides*, and require the two Python programs to agree.
The **proof**, not Lean's evaluator, is the oracle.

    theorem List.map_map : (xs.map f).map g = xs.map (g ∘ f)
      ⇒  transpile both sides.  Any disagreement is a transpiler bug, by construction.

**Novelty: narrow, not wide.** A prior-art search found no published work harvesting a
proof assistant's equational corpus this way, but the claim must be stated carefully.
Isabelle's **`code_test`** [15] already runs proved lemmas through the code generator
on six backends — the same conceptual family — differing in that its cases are
hand-written closed ground terms, its check is unary ("evaluates to `True`") rather
than a two-program comparison, and it never instantiates quantified theorems. EMI [1],
Hermes, GLFuzz, **PTE** [16] and **EET** [17] all do "two equivalent programs must
agree" with **hand-authored or dynamically-inferred** equivalences; **MR-Scout** [18]
mines relations automatically but from *unit tests* (unsound). The defensible claim is
the **conjunction**: the theorem library as a zero-authoring-cost, sound-by-construction
corpus; *both* sides compiled by the SUT (no reference interpreter in the trusted base);
and *quantified* theorems instantiated with generated inputs. Any writeup needs an
explicit "why this isn't `code_test`" and "why this isn't EMI" paragraph — those are the
two attacks. See [RELATED_WORK.md](RELATED_WORK.md).

Three properties, none available to a C/Go/Rust transpiler fuzzer:

1. **No evaluator in the loop.** Harvest once; each identity is then a reusable,
   Lean-free differential test. This removes the throughput bottleneck of §7.
2. **It pits translation rules against each other.** The Lean-as-oracle harness can
   only catch a rule that disagrees with *Lean*. EMP catches a rule that disagrees
   with *another rule* — `List.map_map` forces the fused-comprehension lowering and
   the two-pass lowering to agree — which is where bugs hide whose two lowerings are
   each individually plausible.
3. **The identities are total.** `Nat.div_eq_sub_mod_div` holds at `n = 0` *because
   it is a theorem*. Edge cases arrive as a consequence of the proof, not of guessing.

This inverts EMI [1]. EMI must *invent* semantics-preserving mutations, from a handful
of hand-written envelopes, precisely because C has no ground truth. We *harvest
thousands of proven ones*, and the supply grows for free with the imports. It also
inverts QuickSpec [19] / Ruler [20], which use *testing to discover equations*; we use
*proved equations to obtain tests*.

**`@[csimp]` is the purest source, and it is untouched.** Lean's checked
compiler-rewrite attribute carries, for each entry, a proof `f = g` swapping a reference
implementation for the efficient one the compiler actually emits — literally a curated
database of proved program-equivalence pairs sitting in the compiler's own attribute
table. The prior-art search found no work using it as a test corpus; we now harvest it
as a priority source. (Its unchecked sibling `@[implemented_by]`, which Lean simply
trusts, is a bug-hunting *target* rather than an oracle.)

**Truth is not enough — the identity must DISCRIMINATE.** `Nat.zero_sub : 0 - n = 0`
instantly catches truncated `Nat` subtraction emitted as a plain `-`.
`Nat.div_eq_sub_mod_div` cannot: its subtraction never goes negative, so both sides
agree under the bug. A proven identity is useless unless its two sides exercise the
rule *differently* — §2's lesson, one level up. That yields an automatic filter we are
uniquely able to compute: **transpile both sides, diff their `HANDLERS_FIRED` tag
sets, keep the identities whose sides fire different rules**, and rank them by which
rules they distinguish. It ranks 19,468 candidates by discriminating power and aims
them at the rules that are never otherwise exercised. In the current run, **34 of 40**
harvested identities are discriminating.

**Result.** On its first run, over 40 harvested identities, EMP found **two real
transpiler bugs** (F37/F38): all three index-update forms shared one emission, and out
of range it silently *appended* (`[1,2].set 5 9` → `[1,2,9]`; Lean gives `[1,2]`),
while `Array.set!` — a function that panics in Lean — quietly returned a value. The
identity that exposed it, `Array.getD_getElem?_setIfInBounds`, *is* the bounds
condition, so it cannot avoid testing the out-of-range case. Every existing check had
only ever set an in-range index.

**Triage is load-bearing.** A `fallthrough.*` tag is the emitter *admitting* it has no
rule for a construct; it then emits an undefined name and the program dies with
`NameError`. That is a transpiler **gap** (the F821 class), not a mistranslation, and
lumping the two together buries the signal — 20 of 40 identities are gaps. The gold is
a mismatch between two sides that *both transpiled cleanly*.

**Scale.** The full pool: **~2,085 identities** harvested, 817 tested, **1,768 (85%)
discriminating**, 1,268 set aside as gaps.

**The source round-trip is what makes it trustworthy.** The harvester first built each
side by abstracting the theorem's `Expr` and `addDecl`-ing it. Those definitions are
well-typed, but their LCNF shape is **not one the elaborator produces from source**, and
several transpiler rules are shape-sensitive pattern matches on instance structure:
`Nat.sub_eq` synthesized to a point-free `HSub.hSub` and emitted a plain `-`, where
source-written `n - m` carries `instSubNat` and correctly emits `max(0, n-m)`. EMP was
reporting bugs that *cannot occur in real code*. Phase 1 now pretty-prints each side as
Lean **source** and phase 2 **re-elaborates** it (`pp.explicit := false` is what does the
work — implicit and instance arguments are re-inferred on the way in), so the elaborator
decides the term shape. Flags fell **25 → 9 → 0**, and mutation testing confirms no loss
of sensitivity: an injected off-by-one in `List.take` is still caught at once, via
`List.take_left`.

**Yield: five distinct emitter defects** — F37/F38 (index update out of range), F40
(`Option.toList`, which surfaced through *ten* proven identities at once), F41
(dependent `xs[i]` returned the bounds-check boolean, in a rule that had **never fired**
in the corpus), and F42 — which is the one worth the paper's space:

> **F42: EMP caught a bug we introduced *while fixing* F37/F38.** Seeing `#eval` print
> `Error: index out of bounds` for `Array.set!`, we concluded it panics and made it
> raise. But `panic!` in Lean prints a message and **returns the default** — it is not an
> exception. Lean proves the point outright:
> `Array.set!_eq_setIfInBounds : xs.set! i v = xs.setIfInBounds i v`.
> Our regression case asserted the wrong behaviour and *passed*. The differential oracle
> could not have found this, because we had misread the oracle. **A proof caught an error
> that a plausible reading of the evaluator's output produced.** The panic message is a
> side effect; the theorem is the semantics.

**Honest limits.**
1. **A flag is a lead, not a finding** — confirm it from a hand-written definition. Every
   bug above was confirmed that way. Four harness defects surfaced along the road (Lean's
   100-error file cap killing the `#eval`; recursion depth on a long `do` block; the
   pretty-printer eliding long terms as `⋯`; a failed elaboration leaving `sorryAx` in
   the environment), each of which manufactured plausible-looking "bugs."
2. **Small values only**: identities call the real stdlib, so a boundary value on a
   *size* parameter makes `List.range n` build a 10^18-element list. Composing EMP with
   §2's value domain needs per-parameter size analysis.
3. **Conditional equations are dropped**, not tested under their hypothesis — that is
   most of the 41,615. Noncomputable identities (`Bool.not'`, anything through
   `Classical.choice`) are filtered: Lean emits no code for them, so they are untestable
   rather than violated.

## 3. Extraction has never been fuzzed

SnakeLean is an **extractor**: it compiles definitions in a dependently typed logic
to runnable code. That lineage has a hole.

- Coq's extraction (Letouzey [10,11]) was validated by pen-and-paper proof plus
  "extract large developments and run them". No randomized testing; the
  implementation sat in the TCB and drifted from the theory.
- Verified extraction to OCaml [12] and CertiCoq [13] close the gap the *other* way
  — by machine-checked proof.
- Fuzzing targets C compilers, C-family transpilers, and JS engines. Never an
  extractor.

To our knowledge **no proof-assistant extraction pipeline has been subjected to
systematic randomized differential testing.** SnakeLean occupies the empty middle:
not a proof, but not extract-and-trust either.

The resulting bug taxonomy is not the C-transpiler one (syntax / type-conversion /
omitted fragments). Across 36 bugs it clusters as:

1. **Semantics of *total* operations.** Lean is total: `Nat` subtraction saturates
   at 0, `n / 0 = 0`, `n % 0 = n`, and `Int` division has both Euclidean *and*
   truncated rounding. Python agrees with none of it. (F12, F36.)
2. **Erasure artifacts.** Type parameters, proof terms, and `Decidable` instances
   are runtime-irrelevant and must vanish — but *exactly* as far as the compiler
   erases them. Erase too little and the signature grows a phantom parameter (F35);
   too much and a call loses an argument. Leaked `Eq.ndrec`/`cast` proof terms (R4)
   have no analogue in the C-transpiler literature.
3. **Idiomatic-target rewriting.** We do not transliterate, we *idiomatize*:
   `List.map` → comprehension, `eraseDups` → fused set comprehension,
   self-tail-recursion → `while True:` (Lean does TCO; Python overflows at ~900
   frames). Each is a semantics-preserving optimization that can be wrong. **The
   transpiler is an optimizing compiler, and that is where the richest bugs live.**
4. **Representation collapse.** The idiomatic target type is lossier than the
   source: `Option α → α | None` is elegant until `Option (Option α)` makes
   `some none` and `none` identical; a whole-number `Float` literal emitted as `0`
   rather than `0.0` is silently wrong (F34).

Categories 2 and 3 appear to be new to transpiler testing. They are what you get
when the source is a proof assistant and the target must be idiomatic.

## 4. The oracle's equality relation is a design surface

A differential harness is only as strong as its notion of equality. Ours compares
exact values, not `toString`:

- `Float` crosses the wire as its **IEEE-754 bit pattern**; comparison is strict
  equality (NaNs canonicalized). Justified: both sides are float64 and route
  transcendentals through libm, so results are bit-identical. This is what makes
  `0` vs `0.0` (F34) detectable at all.
- Nested `Option` crosses as `{"__some__": inner}`, keeping `some none` ≠ `none`.
- User inductives cross as `{"c": ctor, "f": [fields]}`.

A `toString`-level oracle — the obvious implementation — would have missed at least
two shipped bugs. The lazy choice of equality hides real defects.

## 5. Artifact

| | |
|---|---|
| Transpiler | `SnakeLean.lean`, ~3.9k lines, LCNF → Python, **147** named translation rules |
| Corpus | 19 modules, ~5.3k lines of Lean; **~538** functions auto-harvested as drivable (incl. ports of cedar-spec, rust-lean-models) |
| Generator | `fuzz/gen.py`, **123** labeled productions, coverage-guided (production + k-path [3]); invents custom inductive types per file |
| Oracle | Lean. Exact-bit wire format (§4) |
| Mutation | boundary-value + named-rule substitution (§2); EMI envelopes [1,2]; LangFuzz-style corpus fragment reuse [4] |
| Shrinking | grid minimization + HDD/C-Reduce term reduction [5,6] |
| Coverage | grammar production/k-path; per-translation-rule; transpiled-Python line/branch/path |
| EMP | `fuzz/Theorems.lean` + `fuzz/emp.py` — harvest proven equations, transpile both sides, require agreement (§2b) |
| Results | **39 bugs found and fixed**; 3807/3807 exhaustive + 112/112 curated cases agree |

## 6. Related work

**TeTRIS** [14] (ACSAC'25) is the only prior fuzzer aimed at source-to-source
transpilers, and the closest comparison. It mutates a language-agnostic AST with
six construct-level mutators and repairs the resulting scope/type violations — an
effort that lifts test-case validity from AFL++'s 2.3% to 71.6%. That effort is the
part §1 argues away: Lean's elaborator *is* the resolver, exactly, and it is also
the oracle. TeTRIS is coverage-guided (AFL/QEMU basic blocks), which §2 argues is
the wrong signal for this bug class. Two of its mutators — REPLACE-LITERAL and
REPLACE-OPERATOR — name blind spots we demonstrably had, and adapting them produced
the §2 result; it remains ahead of us in mutating *real seed programs*, which we do
not yet do. **CSmith**/**YARPGen** generate valid C but are hardcoded to one
language. **EMI** [1,2] is discussed in §1. **LangFuzz** [4] contributes fragment
reuse, which we use.

## 7. Limits

- **Bounded differential testing, not proof.** We find bugs; we do not show their
  absence. [12,13] are the other end of that spectrum.
- **The free oracle is bought with a restriction**: the source must be total, pure,
  and evaluable. That is why it works for a proof assistant and would not transfer
  to C — and it is why the claim is worth making, since the languages that qualify
  (Lean, Coq/Rocq, Agda, Idris, F*) are important and entirely un-fuzzed.
- **Throughput is poor**: every candidate pays for a Lean elaboration. That is the
  price of free validity.
- **F36 refutes our own coverage story**, and should be presented that way. Our best
  instrument said "tested".

## 8. Open work, in order of expected yield

0. **Scale EMP.** It currently harvests 40 identities as a proof of concept; the pool
   is 19,468, and Mathlib multiplies it. Rank by discriminating power (the tag-set
   diff) and run the whole pool. Also: test *conditional* equations under their
   hypothesis (decidable ones can simply be checked before comparing), which is most
   of the 41,615.
0b. **Per-parameter size analysis**, which unblocks composing EMP with the boundary
   value domain (§2). Today a large value on a size parameter hangs the stdlib call, so
   the two strongest techniques cannot yet be combined.

1. **Coercion insertion** (`Nat→Int→Float`, `Int.toNat`, `UInt8.ofNat` wraparound).
   The grammar has **no `UInt` types at all**, while the emitter carries an explicit
   warning that UInt arithmetic wraps mod 2^n. Same shape as the gap that produced
   F36.
2. **Rule-directed generation.** `HANDLERS_KNOWN` minus `HANDLERS_FIRED` is already a
   machine-readable list of untested translation rules (94 of 146 unfired in the
   §2 run). Generate programs *to hit them* — a better target than block coverage.
3. **Structural mutation of corpus bodies.** We drive harvested definitions
   *verbatim*; nothing perturbs real code. `struct_shrink` already enumerates
   balanced-paren spans and keeps rewrites that still elaborate — **invert it into a
   "grow"** that splices same-typed fragments from a construct dictionary. Lean
   supplies scope/type resolution; the oracle is recomputed, so unlike EMI the
   mutation need not preserve semantics.
4. **Audit the transpiler-crash oracle.** `fuzz.py` classifies a Lean error as
   `lean-error` → "generator's fault, skip the seed". An emitter *panic* inside
   `#eval` looks identical. We may be silently swallowing crashes.
5. **Mathlib** as a fragment source: far larger, far nastier.
