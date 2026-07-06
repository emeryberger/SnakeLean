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

## THE efficiency problem (items 1 & 2 DONE; verify at scale on cloudnew)
A 3000-seed `--corpus` sweep at 14 fns/file **did not finish** on 150 cores.
Root causes, in priority order:

1. ✅ **`--corpus` now batches** (`corpus-batching-efficiency` branch). `--corpus
   --batch B` packs B seeds into ONE Lean file, each seed in its OWN `#eval` block
   (banners `### PYTHON {seed}` / `### ORACLE {seed}`, split by the existing
   `_split_batch_output`); user-type JSON serializers are emitted once as the
   union over the batch. A `suspect`/failing seed is re-run alone to classify +
   isolate (`check_corpus_batch`, mirroring grammar `check_batch`). Verified:
   every seed's block is byte-identical to its standalone file, and batched vs
   unbatched give identical verdict + coverage (incl. uneven batches / `--start`
   offsets). Measured ~2x even on the mac at 20 seeds; the win compounds at scale.
2. ✅ **`TypeInfo.lean` cached** (`corpus_frags.build_type_info_cache`). The parent
   spawns Lean once, writes `fuzz/.typeinfo.json` (keyed by newest `Corpus/*.lean`
   + `TypeInfo.lean` mtime; atomic replace); workers `_load_type_info()` from the
   JSON with no Lean spawn. Stale/missing/corrupt cache falls back to a live spawn.
   `harvest()` also runs once in the parent and the (picklable) function list is
   passed to workers. Eliminates the ~150 concurrent bootstrap Lean spawns.
3. ✅ **Batch timeout scaled with size** (`_batch_timeout`). The fixed per-seed
   60 s killed a healthy 25-seed batch mid-print (each corpus seed is ~3 s of
   transpile+eval, so a batch is ~75 s of legitimate work). Now
   `LEAN_TIMEOUT_S + PER_SEED_TIMEOUT_S*(N-1)` (60 + 10*(N-1)); a genuine hang in
   one block still bounds the whole run. This also exposed a latent robustness
   bug (BOTH batch modes): a process killed mid-print leaves a truncated final
   ORACLE row, and `_check_py_oracle`'s `line.split("\t")` raised a bare
   `ValueError` that escaped `Failure` handling and killed the whole pool — now
   raised as `Failure("truncated")` so the seed is re-run alone.

**VERIFIED AT SCALE (2026-07-05, cloudnew, 180 jobs):** the 3000-seed
`--corpus --batch 25 --defs 14 --inputs 6` sweep that previously DID NOT FINISH
now completes: **3000/3000 checked, 0 transpiler bugs, 139/139 corpus functions
exercised, 65/118 handlers fired.** Per-seed blocks byte-identical to standalone;
batched vs unbatched give identical verdict+coverage.

## New bug-finding directions (after efficiency; ~ by expected yield)
1. **Invariant-respecting user-value generation.** Phase 3 excluded `UnionFind`
   (`_UNSAFE_TO_CONSTRUCT`) because a random parent array cycles → `find` loops.
   Generate values that RESPECT the invariant (e.g. `UnionFind.ofSize n` then a
   sequence of `union` ops) instead of raw `.mk`. Unlocks path-compression code —
   a classic source of compiler/transpiler bugs. Same idea for any struct with a
   well-formedness precondition.
2. ✅ **DONE — Recursive & container user types** (`recursive-container-types`
   branch). A recursive type-string interpreter (in `corpus_frags.py`) shared by
   value-gen / Lean-literal / JSON / serializer emission unlocked BOTH container
   types over user elements (`List Card`, `Option (List Nat)`, `List (Char ×
   Trie)`) AND depth-bounded recursive types (`Expr`, `JsonValue`, `Trie`) via
   minimal-term-depth analysis (always cappable with a base case → terminates).
   Harvest **139 → 178** functions. Found & fixed **9 transpiler bugs**: loop-mode
   `find?` predicate → `_uniq_NNN`; `Option.isSome/isNone` point-free; `Option.map`;
   `List.setTR`; point-free USER fn emitted `fn()` not `fn`; applied `List.head?/
   getLast?/…` over erased type arg; `List.zip`; nullary user value point-free
   must be CALLED not referenced (`Trie.empty`); transitive loop-recursion
   detection (`splitOn` → `_uniq_NNN`). Regression cases (6)-(10) in
   `RegressionFixes.lean/_test.py`. VERIFIED AT SCALE (2026-07-06, cloudnew): a
   2000-seed `--corpus --batch 25` sweep = **0 bugs, 177/177 functions, 74/119
   handlers fired** (up from 65/118 — recursive types reach new handlers).
   REMAINING: nested `Option` (`(xs : List (Option α))[i]?` matching `some none`)
   collapses to Python `None` — `TicTacToe.validMoves` excluded via
   `_KNOWN_OPEN_FNS`; a faithful fix needs a sentinel Option representation.
3. ✅ **DONE — Float support** (`float-support` branch). Float added to the
   fuzzer VALUE universe (`gen.VALUE_TYPES`, distinct from the grammar's
   `LEAN_TYPES`), serialized by EXACT IEEE-754 bits (`jFloat`/`Float.ofBits`/
   `struct`) so the oracle uses **strict equality** (decision: transcendentals go
   through libm on both sides and are bit-identical, so no tolerance needed; NaN
   canonicalized to `NaN==NaN`). Harvest **178 → 209** (+31 Geometry). Fixed 4
   transpiler bugs: Float literal (`OfScientific` via instance projection) was a
   call to an undefined var; Float `/` emitted integer `//` (silent wrong value)
   → `floatdiv` arithKind with IEEE `x/0` guard; `Float.sqrt/sin/cos/…` → `math.*`
   (+ always `import math`); `Float.decLt/decLe/decEq` → `</<=/==`. Regression
   case (11). VERIFIED AT SCALE (2026-07-06, cloudnew): 2000-seed sweep = **0
   bugs, 209/209 functions**. (Grammar-side Float generation still not done — the
   grammar doesn't invent Float functions; corpus fragments cover them.)
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
  (`TypeInfo.lean` loader w/ `build_type_info_cache` JSON cache, `_is_constructible`,
  `_UNSAFE_TO_CONSTRUCT`, `_emit_user_serializers`). Batching: `_corpus_block`
  (shared per-seed block) + `emit_corpus_batch_file`.
- `fuzz/fuzz.py` — CLI/modes (`--batch`, `--corpus`, `--pycov`, `--pycov-search`),
  `lean_run` (has the timeout), pool workers, self-coverage report.
- `fuzz/pycov.py` — coverage backends (SlipCover / settrace / sys.monitoring
  paths); `Harness`. `fuzz/input_search.py` — greybox search (base types only).
- `fuzz/TypeInfo.lean` — Lean-side type dump. `roundtrip/run_oracle.py` —
  `normalize`/`materialize` for dataclass round-trip.

## Faithfulness caveat (keep stating)
Differential testing vs the Lean oracle finds bugs; it does not prove absence.
It is exhaustive only within stated input bounds.
