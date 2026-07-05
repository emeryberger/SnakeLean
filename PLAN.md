# Fuzzing-at-scale plan (working doc)

Goal: run "thousands and thousands" more fuzz tests *productively* on the
Lean→Python transpiler. Volume alone has diminishing returns (we already hit
61/61 grammar-production coverage at 3000 seeds), so the plan increases
throughput AND code-shape diversity, and adds coverage feedback.

## Key measurements (motivate the plan)
- Per-seed cost is ~1s and is **~entirely Lean process startup + olean import**,
  NOT transpilation. => Batching many functions per Lean spawn is the biggest win.
- 120 functions in one file (~1.4s) costs *less* than 8 functions in a file
  (~2.0s). Startup dominates.
- Ill-typed generated seeds ~2.5%. CORRECTION (measured): a type error does NOT
  merely drop one def's rows within a shared `#eval` — it aborts the WHOLE
  `#eval` via the `sorry` axiom (zero output for every seed in that block). So
  batching is safe ONLY if each seed gets its OWN `#eval` block: then a bad seed
  drops just its own block's rows and its siblings still print. `emit_batch_file`
  now emits one seed-tagged block per seed (verified: seeds 12/13/14 with 13
  ill-typed → 24/0/24 rows). A batched seed with no output section is "suspect"
  and re-run alone to tell ill-typed (skip) from a real bug.
- Big `#eval do` blocks overflow the elaborator recursion limit =>
  `set_option maxRecDepth 100000` in the batched file's PRELUDE.

## Branch / PR hygiene (IMPORTANT — recurring failure)
- Stacked PRs (base = another feature branch) have stranded work FOUR times
  (#6, #9). #9 auto-closed as "merged" when its base merged, but its 6 commits
  (fuzzer + transpiler fixes F1–F11) never reached main; re-landed via #11.
- RULE: branch every new PR directly off `main`; merge in order. Current work is
  on branch `fuzz-scale` off main (which now has the fuzzer via #11).

## Tasks (in priority order)
1. [DONE] **Batching** — `--batch B` packs B seeds' functions into one Lean
   spawn. `gen.emit_batch_file(seeds, ndefs, ninputs, emi)` emits one seed-tagged
   `#eval` block per seed (`s{seed}_` name prefixes; `### PYTHON {seed}` /
   `### ORACLE {seed}` banners) so output splits back per seed and one ill-typed
   seed can't poison the batch (see corrected measurement above); returns
   (src, {seed:(all_prods,covered)}). `set_option maxRecDepth 100000` in PRELUDE.
   Wired into fuzz.py: `check_batch` worker runs a chunk in one spawn, then
   re-runs any suspect/failing seed ALONE via `run_seed` — which classifies
   ill-typed seeds (`lean-error`, skipped) and, for a real bug, yields the
   isolated seed that `report_bug`/`minimize` shrink. Verified: batch vs non-
   batch give identical verdict + 61/61 coverage + per-seed coverage bit-for-bit
   (determinism/shrinking preserved). Speedup (local mac, 12 cores): 60 seeds
   jobs=1 72s→17s (4.3x); 200 seeds jobs=6 128s→23.5s (5.4x, CPU util 122%→333%
   as serial Lean-startup stalls shrink). Batching stacks with `--jobs`.
2. [DONE] **Fragment-reuse grammars** (LangFuzz-style, Lean-specific):
   `fuzz/corpus_frags.py` harvests every top-level `Corpus/*.lean` def whose
   params+ret are all in the fuzzer's value universe (78 functions) and fuzzes
   them on random inputs via `fuzz.py --corpus` (`emitPythonForNames` auto-pulls
   transitive deps, so a 1-line fragment drags in its `let rec` helpers). Reports
   distinct-function coverage; corpus-specific minimizer shrinks #funcs then
   #inputs. IMMEDIATELY found TWO real soundness bugs the grammar structurally
   cannot reach (grammar always guards divisors + never sorts):
     - **F12 Nat/Int div/mod by zero**: Lean division is TOTAL (n/0=0, n%0=n for
       Nat and Int, incl. Euclidean variants); transpiler emitted bare Python
       `//`/`%` which raise ZeroDivisionError. Fixed centrally via `guardZeroDiv`
       at all 4 emission sites + the Euclidean `emitArithBinary` forms.
     - **F13 Array.qsort mis-indexing**: recent Lean materializes qsort's two
       trailing optParams (`low:=0`, `high:=as.size-1`), so LCNF args are
       `[…,as,lt,low,high]`; handler grabbed the last two → `sorted(0, key=high)`
       (`TypeError: 'int' not iterable`). Fixed to index as/lt from size-4/size-3
       with a 2-arg fallback for older Lean.
   Validated on cloudnew: 3000 corpus seeds clean, 78/78 functions exercised;
   all 216 pre-fix failures were exactly these two bugs (0 survive both fixes).
3. [DONE] **k-path (context-sensitive) coverage** [5 README]: `Gen` now keeps a
   context stack (`ctx`) and records every 2..KMAX-length chain of nested
   productions (`all_kpaths`/`kpaths`, KMAX=3), e.g. `bool.gt → nat.match`,
   `bool.ge → nat.add → nat.lit`. `fuzz.py` aggregates and reports it. KEY
   FINDING: single-production coverage saturates at ~98–100% while k-path
   coverage sits at ~39% of offered paths — the metric surfaces the untested
   *combinations* that flat coverage hides (the LangFuzz/Havrikov point).
   `choose` also applies a secondary "prefer a fresh k-path" steer, but its
   effect is ~neutral (39.0% vs 38.7% A/B over 40 seeds): each file is
   independently seeded for reproducibility, so per-file steering can't
   coordinate across the sweep, and the small depth budget forces most in-file
   paths anyway. The measurement, not the steer, is the deliverable. Determinism
   preserved (identical k-path totals single vs batch mode).
4. [DONE] **Stronger reduction**: `struct_shrink` (fuzz.py) reduces the failing
   Lean TERM (HDD/C-Reduce style, Misherghi&Su ICSE'06 / Regehr PLDI'12), run
   after the count-based `minimize` isolates a single def. It enumerates
   balanced-paren subterms (longest first) and replaces each with a small set of
   type-agnostic leaves (`0`, `[]`, `true`, `(none : Option Nat)`, a param name),
   keeping a rewrite iff the file still elaborates AND still reproduces the same
   bug class — greedy fixpoint over rounds. Soundness is automatic: Lean
   re-type-checks each candidate (ill-typed rewrites → `lean-error`, rejected)
   and the oracle recomputes the expected value, so a kept rewrite genuinely
   still diverges. Enabler in gen.py: `single_def_body(seed, ninputs)` returns
   `(orig_body, rebuild, params)` with the oracle rows FROZEN once (they consume
   the rng), so `rebuild(body)` only swaps body text; `rebuild(orig_body)` is
   byte-identical to `emit_lean_file(seed,1,ninputs)`. Verified: a 373-char
   nested term shrank to 13 chars (`(0 + (0 / 0))`) still triggering the bug
   under test. `report_bug` now saves the structurally-minimized reproducer.
5. [DONE] **Input-adequacy coverage of the TRANSPILED Python** (`fuzz/pycov.py`
   + `fuzz.py --pycov`). The transpiler is in Lean so Python coverage can't
   measure IT; the target is coverage of the *transpiled code* during oracle
   execution — a bug in a branch no oracle input reaches is invisible to
   differential testing. Coverage backend (`pycov.Harness`): **SlipCover** when
   importable — it instruments the compiled code OBJECT directly
   (`Slipcover.instrument(compile(...))`), so it works fine on the `exec`'d
   transpiled string with no imported file (an earlier note here claiming
   otherwise was WRONG), counts executable lines at the bytecode level (bare
   `else:` correctly excluded), and on Python 3.12+ (with `slipcover.branch.
   preinstrument`) records real **branch** coverage. Falls back to portable
   `sys.settrace` line events when SlipCover is absent. cloudnew now runs
   python3.12 + slipcover (installed 2026-07-05) to get branch coverage.
   `--pycov` runs a corpus sweep, unions hit body-lines per function across all
   seeds/inputs, and flags functions with unexercised lines. KEY FINDING:
   `yahtzee_score` sits at 7% (16/209 lines) — random 5-element lists almost
   never form a Yahtzee/straight/full-house, so its scoring branches are barely
   tested; many number-theory `go` helpers sit at 60–85%. This is the exact
   adequacy gap the task anticipated: a transpiler bug in one of those unreached
   branches would pass every differential test.
5b. [DONE] **Coverage-guided input search** (task-5 follow-up): `fuzz/input_search.py`
   + `fuzz.py --pycov-search`. Rather than hand-seed inputs per function (doesn't
   scale to 78), an AFL-style greybox loop runs entirely on the *transpiled
   Python* (fast, in-process, Lean-free): transpile once → search inputs that hit
   new body lines, mutating covering inputs (typed mutators + structure-aware
   bootstrap: all-equal / consecutive / full-house lists, boundary ints) →
   emit a Lean oracle over the discovered covering inputs and diff, so any
   mis-transpiled branch the search reaches is still caught. When SlipCover branch
   coverage is available (3.12+) the search targets uncovered *branch edges*, not
   just lines — a stronger signal. RESULT: 100% LINE coverage on all 78 functions
   (yahtzee_score 96%→100% with ~6 inputs vs 400 random); 100% BRANCH coverage on
   all 37 functions that have branches; 0 divergences — the transpiler is correct
   on every newly-reached branch. Deterministic (seed 0). Two measurement fixes:
   (a) settrace fallback drops bare `else:`/`try:`/`finally:` headers (never fire
   a line event); (b) branch mode excludes provably-unreachable `match … → EXIT`
   fall-through edges — the transpiler emits `match` only on irrefutable tuple
   patterns, so SlipCover's conservative match-failure edge is dead code that
   would otherwise peg such functions below 100% forever.

## Scaled validation on cloudnew (192 cores, python3.11) — this session
All work synced to cloudnew via patch off origin/main and run on 90–180 cores:
- Grammar (5000 seeds, --batch 25, --emi 0.3): 0 bugs, 61/61 production coverage,
  k-path coverage 89% (vs 39% at 40 seeds — the metric climbs with volume).
- Corpus fragment (3000 seeds): 0 bugs, 78/78 functions (both F12/F13 fixes hold).
- Input-adequacy (--pycov, 1000 seeds): 98% of transpiled body lines exercised
  (26342/26862 across 105 fns); yahtzee_score 7%→86% as inputs accumulate; 63
  fns still have gaps (targets for per-fn input biasing).

## Done this session (already merged or in-flight)
- Round-trip harness (Option A sampled 112/112 + Option B exhaustive 3807/3807).
- Grammar fuzzer + coverage-guided generation + grammar expansion (Int, Option).
- EMI + guided stochastic mutation (`--emi`, default 0.3).
- Parallelism (`--jobs`, ProcessPoolExecutor; bare `lean` + captured LEAN_PATH,
  not `lake env lean`, to avoid serializing). ~1570% CPU on cloudnew.
- 16 transpiler bugs fixed (R1–R4, F1–F11 + upgrade-era); 5 silent wrong-value
  bugs (Nat.sub monus, Euclidean Int div & mod, two OfNat literal collisions).
- 3000-seed parallel EMI campaign on cloudnew (192 cores): clean, 61/61.
- Docs: README (4-layer correctness + fuzzer section + refs), VERIFICATION.md
  (full bug ledger), RELATED_WORK.md (not-adopted techniques), roundtrip/README.
  All references now carry a DOI or URL.

## Environment notes
- cloudnew: 192 cores, Linux, elan+lean installed; repo cloned at
  ~/git/LeanToPython (branch was fuzz-and-bugdoc). Run fuzzer with `python3.11`
  there (transpiled Python needs 3.10+ for PEP 604 unions; cloudnew default is
  3.9). Big runs: `python3.11 fuzz/fuzz.py --seeds N --jobs 180 --emi P`.
- Local mac: python3.12, 12 cores.
- `lake env printenv LEAN_PATH` once, then bare `lean` for speed/parallelism.
- Shell cwd sometimes resets between commands — use absolute paths.

## Faithfulness caveat to keep stating
Differential testing vs an oracle finds bugs; it does not prove absence. It is
exhaustive only within stated input bounds.
