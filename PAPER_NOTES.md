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
| Results | **36 bugs found and fixed**; 3807/3807 exhaustive + 112/112 curated cases agree |

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
