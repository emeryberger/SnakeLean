# LeanToPython fuzzing — forward plan (handoff for a fresh context)

Goal: keep finding transpiler bugs at **massive scale**, and first make the
harness **efficient enough** that a multi-thousand-seed corpus sweep actually
finishes on cloudnew's 192 cores.

## Status (all merged to `main`)
The full bug-hunting roadmap is DONE. **23 transpiler bugs fixed** (F1–F18,
R1–R4, upgrade-era), each with a regression test in `RegressionFixes.lean` /
`VERIFICATION.md`. Shipped, in order, as PRs off `main`:
- Grammar fuzzer + EMI + coverage-guided gen + `--batch` (grammar mode).
- `--corpus` fragment reuse; `--pycov` input-adequacy; `--pycov-search`
  coverage-guided input search; grammar **k-path** coverage.
- **Self-coverage metric** (`# HANDLERS_FIRED` comments; `fuzz.py` reports which
  of ~118 transpiler handlers fired — untested ones are where bugs hide).
- **Phase 1** String/Char/Array (F14); **F15** `xs[i]!` getElem!; **F16** missing
  builtins (dropWhile/replicate/isPrefixOf/swapIfInBounds/startsWith/…); **F17**
  helper-scoping `_uniq_NNN`; **F18** cross-function name collision (found only at
  3000-seed scale). **Phase 2** List Int/Bool/nested. **Phase 4** execution-path
  coverage via `sys.monitoring` (NOT a SlipCover fork — its callback returns
  DISABLE so per-call order is unrecoverable). **Phase 3** custom inductive types
  (enums/structs; harvest 129→139; 0 bugs — inductive emission was sound).

Every harvestable corpus function (139) transpiles and agrees with the oracle,
alone and batched. `corpus_frags._KNOWN_OPEN_NS` is empty.

## THE efficiency problem to fix FIRST (blocks massive scale)
A 3000-seed `--corpus` sweep at 14 fns/file **did not finish** on 150 cores.
Root causes, in priority order:

1. **`--corpus` does not batch.** Grammar mode has `--batch B` (packs B seeds per
   Lean spawn — 5x win, since Lean startup + `import Corpus` olean load dominates,
   NOT transpilation). `--corpus` spawns **one Lean process per seed**, each
   re-importing `Corpus` (~5–8 s each). This is the single biggest lever.
   → Add batching to `emit_corpus_file` / `run_corpus_mode`: pack many seeds'
     function-selections into ONE Lean file, each seed in its OWN `#eval` block
     (per the grammar-mode lesson: a shared `#eval` aborts entirely on one
     ill-typed def via the `sorry` axiom; per-seed blocks isolate). Reuse the
     `### PYTHON {seed}` / `### ORACLE {seed}` banner + `_split_batch_output`
     machinery from `gen.emit_batch_file`. Expect a similar ~5x.
2. **`TypeInfo.lean` re-runs per worker.** `corpus_frags.harvest()` (called in
   every pool worker) shells out to `lean fuzz/TypeInfo.lean` (a full Lean spawn)
   via `_load_type_info()`. With 150 workers that's 150 concurrent Lean spawns
   just to load type info. → Run it ONCE in the parent, cache to a JSON file
   (e.g. `fuzz/.typeinfo.json`, regenerated only when `Corpus/*.lean` is newer),
   and have workers read the cache. Same for `harvest()` — compute once, pass the
   function list to workers (it's picklable) instead of re-harvesting per worker.
3. **`lean_run` per-call timeout is 60 s** (added in Phase 3 after UnionFind
   hangs). Fine for safety, but a batched file that hits one slow `#eval` burns
   60 s. With batching, keep the timeout but consider a smaller per-eval budget.

Verify efficiency the same way as `--batch` was: identical verdict + coverage,
per-seed determinism preserved, and measure wall-clock speedup on cloudnew.

## New bug-finding directions (after efficiency; ~ by expected yield)
1. **Invariant-respecting user-value generation.** Phase 3 excluded `UnionFind`
   (`_UNSAFE_TO_CONSTRUCT`) because a random parent array cycles → `find` loops.
   Generate values that RESPECT the invariant (e.g. `UnionFind.ofSize n` then a
   sequence of `union` ops) instead of raw `.mk`. Unlocks path-compression code —
   a classic source of compiler/transpiler bugs. Same idea for any struct with a
   well-formedness precondition.
2. **Recursive user types with depth bounds** (`Expr`, `Trie`, `JsonValue`,
   `RBTree`). Currently excluded (`_is_constructible` bails on recursion). Add a
   depth-bounded generator. `RBTree.balance` and the parser `Expr` evaluator are
   exactly the tricky recursive-`match` code transpilers mishandle.
3. **Float support** (Geometry: Point2D/3D, distance/normalize). Needs a
   tolerance-based oracle comparison (exact `==` will spuriously fail on
   float rounding). Decide an ULP/relative-tolerance policy first.
4. **Grammar-side custom-type generation** — have `gen.py` *invent* small
   inductives + functions over them, not just harvest corpus ones. Reaches
   shapes the corpus doesn't contain.
5. **Mathlib corpus** (see README "Future Work"): a far larger fragment source.
   Heavy: toolchain bump, noncomputable defs, universe polymorphism, long import
   graph. High potential yield.
6. **Massive campaigns as regression + discovery**: once efficient, run
   5k–20k-seed grammar (`--batch 25 --emi 0.3`) and corpus sweeps on cloudnew
   routinely; the self-coverage `never fired` list + `--pycov`/`--pycov-search`
   gaps are the map of what's still untested.

## Efficiency facts (measured; keep in mind)
- Per-seed cost is ~entirely Lean **startup + olean import**, not transpilation.
  120 fns in one file (~1.4s) < 8 fns in a file (~2.0s). Batching is the win.
- Ill-typed generated seeds ~2.5%. A type error aborts the WHOLE `#eval` (sorry
  axiom) → one `#eval` block PER SEED so a bad seed drops only its own rows; a
  seed with no output section is re-run alone to classify (skip vs real bug).
- `set_option maxRecDepth 100000` in the file PRELUDE (big `#eval do` blocks
  overflow the elaborator default).
- Use bare `lean` with a once-captured `LEAN_PATH` (not `lake env lean`, which
  serializes on lake startup and kills parallelism).
- `--jobs` = ProcessPoolExecutor; each worker spawns one `lean`.

## Branch / PR hygiene (RULE — this bit us 4× early on)
Branch every PR directly off `main`; never stack on another feature branch (a
stacked PR auto-closes as "merged" when its base merges, stranding its commits).
Merge in order; a later same-file branch just needs a trivial rebase. Ship each
bug/feature as its own PR, CI green before merge.

## cloudnew (run massive sweeps HERE, not local mac)
- 192 cores, Linux; repo at `~/git/LeanToPython`; elan+lean installed.
- **Use `python3.12`** (installed 2026-07-05 via `sudo dnf install python3.12
  python3.12-pip`, passwordless sudo). 3.12 enables `sys.monitoring` path
  coverage AND SlipCover branch coverage; `slipcover` installed for it via
  `python3.12 -m pip install --user slipcover`. (Transpiled Python needs 3.10+
  for PEP 604 unions; the mac has 3.12 too.)
- Sync uncommitted work: `git diff origin/main > /tmp/p.patch`, scp, then on
  cloudnew `git reset --hard origin/main && git clean -fd fuzz/ && git apply`.
  Then `lake build && lake build Corpus`. Export
  `FUZZ_LEAN_PATH="$(lake env printenv LEAN_PATH)"` before Python runs.
- Big runs in background (`nohup … &`) and poll the log — a foreground ssh call
  will exceed a 2-min tool timeout. Watch for orphaned `lean` procs after a kill
  (`pkill -9 -f "bin/lean /tmp/fuzz"`).
- Shell cwd can reset between commands — use absolute paths.

## Key files
- `LeanToPython.lean` — transpiler. Handler tables ~390–590; `emitLetValue`
  ~1140 (the big `.const` dispatch); `.proj`/`emitCases` for structural handlers;
  `emitPythonForDecls` ~3055 (global name de-dup pre-pass, `### HANDLERS` dump);
  `knownHandlerTags` (self-coverage universe — add a tag when adding a handler).
- `fuzz/gen.py` — grammar generator; `LEAN_TYPES`, `ALL_PRODUCTIONS`, per-type
  `gen_*`, `rand_value`/`lean_lit`/`serializer_call`/PRELUDE serializers.
- `fuzz/corpus_frags.py` — fragment reuse + Phase-3 custom-type registry
  (`TypeInfo.lean` loader, `_is_constructible`, `_UNSAFE_TO_CONSTRUCT`,
  `_emit_user_serializers`). **Batching lives to be added here.**
- `fuzz/fuzz.py` — CLI/modes (`--batch`, `--corpus`, `--pycov`, `--pycov-search`),
  `lean_run` (has the timeout), pool workers, self-coverage report.
- `fuzz/pycov.py` — coverage backends (SlipCover / settrace / sys.monitoring
  paths); `Harness`. `fuzz/input_search.py` — greybox search (base types only).
- `fuzz/TypeInfo.lean` — Lean-side type dump. `roundtrip/run_oracle.py` —
  `normalize`/`materialize` for dataclass round-trip.

## Faithfulness caveat (keep stating)
Differential testing vs the Lean oracle finds bugs; it does not prove absence.
It is exhaustive only within stated input bounds.
