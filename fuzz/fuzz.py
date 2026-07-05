#!/usr/bin/env python3
"""Grammar-based differential fuzzer for the Lean -> Python transpiler.

For each seed:
  1. `gen.py` emits a self-contained Lean file (random typed functions + an
     oracle driver).
  2. Lean elaborates it, transpiles the functions to Python (### PYTHON), and
     prints Lean-computed results for random inputs (### ORACLE).
  3. We exec the transpiled Python and diff every result against Lean's.

Any of these is a transpilation bug and stops the run with the offending seed:
  - the transpiled Python has a syntax error (can't be parsed/exec'd),
  - a function raises at runtime (undefined name, bad call, ...),
  - Python and Lean disagree on a result.

On failure we minimize: re-generate with the same seed but fewer defs / inputs
to isolate the smallest reproducer, and save the Lean + Python to fuzz/repro/.

Seeds are checked in parallel across CPU cores (each seed's Lean elaboration is
the bottleneck and is independent), so a sweep uses a process pool.

Usage:
  python3 fuzz/fuzz.py [--seeds N] [--start S] [--defs D] [--inputs I]
                       [--emi P] [--jobs J]
"""
import argparse
import os
import subprocess
import sys
import tempfile
from concurrent.futures import ProcessPoolExecutor, as_completed

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "roundtrip"))
import run_oracle  # noqa: E402  (reuse load/normalize/call)
import gen  # noqa: E402
import corpus_frags  # noqa: E402
import pycov  # noqa: E402
import input_search  # noqa: E402


_LEAN_PATH = None  # captured once; avoids per-seed `lake env` overhead


def _lean_env():
    """Environment for invoking bare `lean` directly.  We capture `LEAN_PATH`
    once via `lake env` and reuse it, because spawning `lake env lean` per seed
    serializes on lake's startup and dominates the runtime — the single reason
    the parallel pool wasn't scaling."""
    global _LEAN_PATH
    env = dict(os.environ)
    env["PATH"] = os.path.expanduser("~/.elan/bin") + ":" + env.get("PATH", "")
    if _LEAN_PATH is None:
        # Inherited from the parent (set once in main) if present, else compute.
        _LEAN_PATH = env.get("FUZZ_LEAN_PATH")
    if _LEAN_PATH is None:
        out = subprocess.run(["lake", "env", "printenv", "LEAN_PATH"],
                             cwd=ROOT, capture_output=True, text=True, env=env)
        _LEAN_PATH = out.stdout.strip()
    env["LEAN_PATH"] = _LEAN_PATH
    return env


# A hung oracle `#eval` (e.g. a corpus function that doesn't terminate on a
# fuzzer-constructed input) must not stall the whole pool.  Bound each Lean run;
# a timeout is treated like a Lean error (the seed is skipped), not a hang.
LEAN_TIMEOUT_S = 60
# Extra wall-clock a batched file gets PER extra seed beyond the first.  A
# batch packs N seeds' `#eval` blocks into one Lean process, so its legitimate
# runtime scales with N (each corpus seed is ~3s of transpile+eval); the fixed
# per-seed timeout would kill a healthy batch mid-print.  A genuine hang in one
# block still bounds the whole run at `LEAN_TIMEOUT_S + PER_SEED_TIMEOUT_S*(N-1)`.
PER_SEED_TIMEOUT_S = 10


def _batch_timeout(nseeds):
    return LEAN_TIMEOUT_S + PER_SEED_TIMEOUT_S * max(0, nseeds - 1)


def lean_run(lean_src, tmp_path, timeout=LEAN_TIMEOUT_S):
    with open(tmp_path, "w") as f:
        f.write(lean_src)
    try:
        proc = subprocess.run(
            ["lean", tmp_path],
            cwd=ROOT, capture_output=True, text=True, env=_lean_env(),
            timeout=timeout,
        )
    except subprocess.TimeoutExpired as e:
        # Surface as a Lean 'error' so callers skip the seed; include partial
        # stdout so any oracle rows already printed aren't lost.
        out = e.stdout or ""
        if isinstance(out, bytes):
            out = out.decode("utf-8", "replace")
        return 124, out, "error: lean timed out (possible non-terminating #eval)"
    return proc.returncode, proc.stdout, proc.stderr


def real_errors(stderr):
    bad = []
    for line in stderr.splitlines():
        low = line.lower()
        if "error" in low and "0 errors" not in low:
            bad.append(line)
    return bad


class Failure(Exception):
    def __init__(self, kind, detail):
        self.kind = kind
        self.detail = detail


def parse_handlers(py_src):
    """Extract transpiler self-coverage tags from the `# HANDLERS_FIRED` /
    `# HANDLERS_KNOWN` comment lines the transpiler appends to its Python output.
    Returns (fired, known) as sets of tag strings (empty if absent — e.g. an
    older transpiler build without the instrumentation)."""
    fired, known = set(), set()
    for line in py_src.splitlines():
        if line.startswith("# HANDLERS_FIRED\t"):
            fired |= set(line.split("\t")[1:])
        elif line.startswith("# HANDLERS_KNOWN\t"):
            known |= set(line.split("\t")[1:])
    return fired, known


# Per-process handler tags from the most recent Lean run — mirrors the
# `gen.emit_lean_file.last_gen` pattern so pool workers can return them without
# threading src through every call site.  Set by `_record_handlers`.
_LAST_HANDLERS = (frozenset(), frozenset())


def _record_handlers(lean_stdout):
    """Parse the transpiler's `### PYTHON` output from a Lean run and stash its
    handler tags in `_LAST_HANDLERS` for the calling worker to return."""
    global _LAST_HANDLERS
    fired, known = parse_handlers(lean_stdout)
    _LAST_HANDLERS = (frozenset(fired), frozenset(known))


def report_self_coverage(fired, known):
    """Print the transpiler self-coverage block: which special-cased handlers the
    sweep exercised, which never fired (untested → bug-prone), and any core-
    namespace fallthroughs (a handler a Lean API change may have silently broken).
    Mirrors the grammar-production-coverage report."""
    if not known:
        return  # transpiler build without instrumentation; nothing to report
    hit = fired & known
    print(f"\nTranspiler self-coverage: {len(hit)}/{len(known)} handlers fired "
          f"({100 * len(hit) // max(len(known), 1)}%)")
    missed = sorted(known - hit)
    if missed:
        print(f"  never fired ({len(missed)}): {', '.join(missed)}")
    # Fallthroughs on CORE namespaces = a special handler likely broken by a Lean
    # change (the construct stopped matching and hit the generic call path, which
    # emits an undefined Python name).  User-function fallthroughs are expected
    # and ignored.
    core = ("List.", "Nat.", "Int.", "String.", "Char.", "Array.", "Option.",
            "Prod.", "Bool.", "Decidable.")
    broken = sorted(t[len("fallthrough."):] for t in fired
                    if t.startswith("fallthrough.")
                    and any(t[len("fallthrough."):].startswith(c) for c in core))
    if broken:
        print(f"  ⚠ CORE-NAMESPACE FALLTHROUGHS ({len(broken)}) — a special "
              f"handler may be broken by a Lean API change: {', '.join(broken)}")


def _check_py_oracle(py_src, oracle_block):
    """Exec the transpiled `py_src` and diff every ORACLE row in `oracle_block`
    against it.  Raise Failure on any disagreement, syntax error, or runtime
    exception."""
    # name map from `# Lean:` comments
    import re
    lean_to_py = {}
    lines = py_src.splitlines()
    for i, line in enumerate(lines):
        m = re.match(r"# Lean: (\S+)", line)
        if m and i + 1 < len(lines):
            d = re.match(r"def (\w+)\(", lines[i + 1])
            if d:
                lean_to_py[m.group(1)] = d.group(1)
    ns = {}
    try:
        exec(compile(py_src, "<transpiled>", "exec"), ns)
    except SyntaxError as e:
        raise Failure("syntax", f"{e} (line {e.lineno}): {e.text}")
    except Exception as e:  # noqa: BLE001
        raise Failure("exec", f"{type(e).__name__}: {e}")

    import json
    for line in oracle_block.splitlines():
        if not line.startswith("ORACLE\t"):
            continue
        parts = line.split("\t")
        if len(parts) != 4:
            # A truncated row — the Lean process was killed mid-print (e.g. a
            # batch timed out, or a genuine hang in one `#eval`).  Not a diff we
            # can trust; surface as a Failure so the batch worker re-runs this
            # seed alone (where a real hang times out → skipped, and a healthy
            # seed passes).  Never let a bare ValueError escape and kill the pool.
            raise Failure("truncated", f"malformed ORACLE row: {line[:80]!r}")
        _, fn, args_json, res_json = parts
        # Materialize any custom-inductive args ({"c":..,"f":..}) into the
        # transpiled dataclass instances the function expects.
        args = [run_oracle.materialize(a, ns) for a in json.loads(args_json)]
        expected = run_oracle.normalize(json.loads(res_json))
        py_fn = lean_to_py.get(fn)
        if py_fn is None or py_fn not in ns:
            raise Failure("missing-fn", f"{fn} -> {py_fn!r} not defined")
        try:
            got = run_oracle.normalize(run_oracle.call(ns[py_fn], args))
        except Exception as e:  # noqa: BLE001
            raise Failure("runtime", f"{fn}{tuple(args)}: {type(e).__name__}: {e}")
        if got != expected:
            raise Failure("mismatch", f"{fn}{tuple(args)}: python={got!r} lean={expected!r}")


def _name_map(py_src):
    """Map each Lean qualified name to its transpiled Python def name, via the
    `# Lean:` trace comments."""
    import re
    lean_to_py = {}
    lines = py_src.splitlines()
    for i, line in enumerate(lines):
        m = re.match(r"# Lean: (\S+)", line)
        if m and i + 1 < len(lines):
            d = re.match(r"def (\w+)\(", lines[i + 1])
            if d:
                lean_to_py[m.group(1)] = d.group(1)
    return lean_to_py


def check_output(stdout):
    """Parse a single-seed's ### PYTHON / ### ORACLE output and diff."""
    if "### PYTHON" not in stdout or "### ORACLE" not in stdout:
        raise Failure("no-output", stdout[:400])
    py_start = stdout.index("### PYTHON") + len("### PYTHON")
    or_start = stdout.index("### ORACLE")
    py_src = stdout[py_start:or_start].strip("\n")
    oracle_block = stdout[or_start + len("### ORACLE"):]
    _check_py_oracle(py_src, oracle_block)


def measure_pycov(stdout):
    """Measure input-adequacy coverage of the transpiled Python (task 5): which
    lines of each transpiled function the oracle inputs actually exercised.
    Returns {py_fn: (hit_lines, body_lines)}.  A function with body_lines not
    fully hit has branches no oracle input reached — where a transpiler bug could
    hide.  Parsing mirrors `check_output`."""
    import json
    py_start = stdout.index("### PYTHON") + len("### PYTHON")
    or_start = stdout.index("### ORACLE")
    py_src = stdout[py_start:or_start].strip("\n")
    oracle_block = stdout[or_start + len("### ORACLE"):]
    lean_to_py = _name_map(py_src)
    calls = []
    for line in oracle_block.splitlines():
        if not line.startswith("ORACLE\t"):
            continue
        _, fn, args_json, _ = line.split("\t")
        calls.append((lean_to_py.get(fn), json.loads(args_json)))

    def run_calls(ns):
        for py_fn, args in calls:
            if py_fn and py_fn in ns:
                try:
                    run_oracle.call(ns[py_fn], args)
                except Exception:  # noqa: BLE001
                    pass  # runtime errors are caught by the diff path, not here
    return pycov.measure(py_src, run_calls)


def _split_batch_output(stdout):
    """Split a batched file's stdout into {seed: (py_src, oracle_block)} using
    the seed-tagged `### PYTHON {seed}` / `### ORACLE {seed}` banners that
    `gen.emit_batch_file` emits.  A seed whose `#eval` block aborted (e.g. an
    ill-typed def → `sorry` axiom) has no banner and is simply absent."""
    import re
    py_re = re.compile(r"^### PYTHON (\d+)\s*$")
    or_re = re.compile(r"^### ORACLE (\d+)\s*$")
    sections = {}
    cur_seed, mode, py_buf, or_buf = None, None, [], []

    def flush():
        if cur_seed is not None:
            sections[cur_seed] = ("\n".join(py_buf), "\n".join(or_buf))

    for line in stdout.splitlines():
        mp = py_re.match(line)
        if mp:
            flush()
            cur_seed, mode, py_buf, or_buf = int(mp.group(1)), "py", [], []
            continue
        if or_re.match(line):
            mode = "or"
            continue
        if mode == "py":
            py_buf.append(line)
        elif mode == "or":
            or_buf.append(line)
    flush()
    return sections


def run_batch(seeds, ndefs, ninputs, emi=0.0, tmp_path=None):
    """Run many seeds in ONE Lean spawn (amortizing Lean's ~1s startup).  Returns
    (results, cov): `results` maps each seed to (status, detail), where status is
    'ok', a transpiler-bug kind, or 'suspect' (block aborted — no output section,
    so it needs a per-seed run to tell an ill-typed seed from a real bug)."""
    src, cov = gen.emit_batch_file(seeds, ndefs, ninputs, emi=emi)
    path = tmp_path
    if path is None:
        fd, path = tempfile.mkstemp(prefix="fuzz_batch_", suffix=".lean")
        os.close(fd)
    try:
        _rc, out, _err = lean_run(src, path, timeout=_batch_timeout(len(seeds)))
    finally:
        if tmp_path is None:
            try:
                os.unlink(path)
            except OSError:
                pass
    _record_handlers(out)  # per-block HANDLERS comments union across the batch
    sections = _split_batch_output(out)
    results = {}
    for seed in seeds:
        if seed not in sections:
            results[seed] = ("suspect", "no output section (block aborted)")
            continue
        py_src, oracle_block = sections[seed]
        try:
            _check_py_oracle(py_src, oracle_block)
            results[seed] = ("ok", "")
        except Failure as f:
            results[seed] = (f.kind, f.detail)
    return results, cov


def run_seed(seed, ndefs, ninputs, tmp_path=None, coverage=None, emi=0.0):
    # Each file is coverage-guided *internally* (its own Gen prefers uncovered
    # productions), so a file depends only on its seed — reproducibility the
    # shrinker relies on.  We do NOT steer across seeds (that would make a file
    # depend on sweep history); instead we just aggregate which productions were
    # exercised, into `coverage`, to report grammar coverage over the whole run.
    src = gen.emit_lean_file(seed, ndefs, ninputs, emi=emi)
    if coverage is not None:
        coverage["offered"] |= gen.emit_lean_file.last_gen.all_prods
        coverage["hit"] |= gen.emit_lean_file.last_gen.covered
    # A unique temp file per call so parallel workers never collide.
    path = tmp_path
    if path is None:
        fd, path = tempfile.mkstemp(prefix=f"fuzz_{seed}_", suffix=".lean")
        os.close(fd)
    try:
        _rc, out, err = lean_run(src, path)
    finally:
        if tmp_path is None:
            try:
                os.unlink(path)
            except OSError:
                pass
    # `lake env lean` prints elaboration errors to stdout (interleaved with the
    # `#eval` output) as well as stderr, so scan both.  A Lean error means the
    # GENERATOR produced ill-typed code (not a transpiler bug); skip such seeds.
    _record_handlers(out)
    errs = real_errors(err) + real_errors(out)
    if errs:
        raise Failure("lean-error", "\n".join(errs[:3]))
    check_output(out)


def _gen_cov(g):
    """The four coverage sets exposed by a Gen: (offered prods, hit prods,
    offered k-paths, hit k-paths)."""
    return (frozenset(g.all_prods), frozenset(g.covered),
            frozenset(g.all_kpaths), frozenset(g.kpaths))


def check_seed(args):
    """Pool worker: check one seed. Returns a picklable result tuple
    (seed, status, detail, offered, hit, koffered, khit, fired, known).  `status`
    is 'ok' | 'lean-error' | a transpiler-bug kind."""
    seed, ndefs, ninputs, emi = args
    try:
        run_seed(seed, ndefs, ninputs, emi=emi)
        return (seed, "ok", "", *_gen_cov(gen.emit_lean_file.last_gen), *_LAST_HANDLERS)
    except Failure as f:
        return (seed, f.kind, f.detail, *_gen_cov(gen.emit_lean_file.last_gen),
                *_LAST_HANDLERS)


def check_batch(args):
    """Pool worker: run a chunk of seeds in one Lean spawn, then resolve any
    anomaly with a per-seed run.  A batched seed can come back 'suspect' (its
    `#eval` block aborted, usually an ill-typed generated def) or with a
    transpiler-bug kind; either way we re-run that seed ALONE — which both tells
    an ill-typed seed (`lean-error`, skipped) from a real bug and yields an
    isolated reproducer the shrinker can work from.  Returns a list of
    (seed, status, detail, offered, hit) tuples, matching `check_seed`."""
    seeds, ndefs, ninputs, emi = args
    results, cov = run_batch(seeds, ndefs, ninputs, emi=emi)
    fired, known = _LAST_HANDLERS  # batch-global handler tags (same file)
    out = []
    for seed in seeds:
        status, detail = results[seed]
        offered, hit, koffered, khit = cov[seed]
        if status != "ok":
            # Re-run alone: isolates the culprit and classifies ill-typed seeds.
            try:
                run_seed(seed, ndefs, ninputs, emi=emi)
                status, detail = "ok", ""
            except Failure as f:
                status, detail = f.kind, f.detail
        out.append((seed, status, detail, offered, hit, koffered, khit, fired, known))
    return out


def run_corpus_seed(seed, nfuncs, ninputs, funcs=None):
    """Run one corpus-fragment file (harvested real Lean defs) through the same
    Lean→exec→diff pipeline.  A Lean error here is NOT an ill-typed generated
    seed — the corpus type-checks — so it's a real failure (e.g. the transpiler's
    dependency emission broke); surface it as such."""
    src, chosen = corpus_frags.emit_corpus_file(seed, nfuncs, ninputs, funcs=funcs)
    fd, path = tempfile.mkstemp(prefix=f"fuzz_corpus_{seed}_", suffix=".lean")
    os.close(fd)
    try:
        _rc, out, err = lean_run(src, path)
    finally:
        try:
            os.unlink(path)
        except OSError:
            pass
    _record_handlers(out)
    errs = real_errors(err) + real_errors(out)
    if errs:
        raise Failure("lean-error", "\n".join(errs[:3]))
    check_output(out)
    return chosen


def check_corpus_seed(args):
    """Pool worker for corpus mode.  Returns (seed, status, detail, chosen_names,
    fired, known) — `chosen_names` is the corpus functions this seed exercised;
    (fired, known) are the transpiler self-coverage tags for this seed."""
    seed, nfuncs, ninputs, funcs = args
    try:
        chosen = run_corpus_seed(seed, nfuncs, ninputs, funcs=funcs)
        return (seed, "ok", "", frozenset(chosen), *_LAST_HANDLERS)
    except Failure as f:
        # Re-derive the chosen names for reporting even on failure.
        _src, chosen = corpus_frags.emit_corpus_file(seed, nfuncs, ninputs, funcs=funcs)
        return (seed, f.kind, f.detail, frozenset(chosen), *_LAST_HANDLERS)


def run_corpus_batch(seeds, nfuncs, ninputs, funcs=None):
    """Run many corpus seeds in ONE Lean spawn (amortizing Lean startup + the
    `import Corpus` olean load, which dominate — NOT the transpilation).  Returns
    (results, chosen_by_seed): `results` maps each seed to (status, detail), where
    status is 'ok', a transpiler-bug kind, or 'suspect' (block aborted — e.g. a
    non-terminating oracle row — so it needs a per-seed run to classify)."""
    src, chosen_by_seed = corpus_frags.emit_corpus_batch_file(
        seeds, nfuncs, ninputs, funcs=funcs)
    fd, path = tempfile.mkstemp(prefix="fuzz_corpus_batch_", suffix=".lean")
    os.close(fd)
    try:
        _rc, out, _err = lean_run(src, path, timeout=_batch_timeout(len(seeds)))
    finally:
        try:
            os.unlink(path)
        except OSError:
            pass
    _record_handlers(out)  # per-block HANDLERS comments union across the batch
    sections = _split_batch_output(out)
    results = {}
    for seed in seeds:
        if seed not in sections:
            results[seed] = ("suspect", "no output section (block aborted)")
            continue
        py_src, oracle_block = sections[seed]
        try:
            _check_py_oracle(py_src, oracle_block)
            results[seed] = ("ok", "")
        except Failure as f:
            results[seed] = (f.kind, f.detail)
    return results, chosen_by_seed


def check_corpus_batch(args):
    """Pool worker: run a chunk of corpus seeds in one Lean spawn, then resolve any
    anomaly with a per-seed run.  Unlike grammar mode a corpus 'suspect' is NOT an
    ill-typed generated seed (the corpus type-checks) — it's most likely a
    non-terminating oracle `#eval` that timed out; the per-seed re-run isolates it
    and classifies (a corpus Lean error IS a real failure).  Returns a list of
    (seed, status, detail, chosen_names, fired, known) tuples matching
    `check_corpus_seed`."""
    seeds, nfuncs, ninputs, funcs = args
    results, chosen_by_seed = run_corpus_batch(seeds, nfuncs, ninputs, funcs=funcs)
    fired, known = _LAST_HANDLERS  # batch-global handler tags (same file)
    out = []
    for seed in seeds:
        status, detail = results[seed]
        if status != "ok":
            # Re-run alone: isolates the culprit (and a timed-out oracle row will
            # time out again → surfaced as a lean-error, i.e. skipped).
            try:
                run_corpus_seed(seed, nfuncs, ninputs, funcs=funcs)
                status, detail = "ok", ""
            except Failure as f:
                status, detail = f.kind, f.detail
        out.append((seed, status, detail,
                    frozenset(chosen_by_seed[seed]), fired, known))
    return out


def minimize(seed, ndefs, ninputs, emi=0.0):
    """Shrink to the smallest (defs, inputs) that still fails for this seed."""
    best = (ndefs, ninputs)
    for d in range(1, ndefs + 1):
        for i in range(1, ninputs + 1):
            try:
                run_seed(seed, d, i, emi=emi)
            except Failure as f:
                if f.kind != "lean-error":
                    return (d, i), f
    return best, None


def _paren_spans(s):
    """Yield (start, end) index pairs of every balanced-parenthesis span in `s`,
    innermost-last within each nesting.  Used by the structural shrinker to
    enumerate candidate subterms to replace."""
    stack, spans = [], []
    for i, c in enumerate(s):
        if c == "(":
            stack.append(i)
        elif c == ")" and stack:
            start = stack.pop()
            spans.append((start, i + 1))
    return spans


def _lean_src_fails(src, want_kind, tmp_path):
    """Run a candidate Lean file; return True iff it reproduces the SAME class of
    transpiler bug.  A `lean-error` (the rewrite made it ill-typed) or a clean run
    both count as "no longer reproduces"."""
    with open(tmp_path, "w") as fh:
        fh.write(src)
    _rc, out, err = lean_run(src, tmp_path)
    if real_errors(err) + real_errors(out):
        return False  # rewrite broke elaboration → reject
    try:
        check_output(out)
    except Failure as f:
        # A syntax/exec/runtime bug stays "the same bug" if its kind matches;
        # for value mismatches, any surviving mismatch is acceptable (the point
        # is a smaller term that still diverges).
        return f.kind == want_kind or (want_kind == "mismatch" and f.kind == "mismatch")
    return False


def struct_shrink(seed, ninputs, want_kind, emi=0.0, max_rounds=6):
    """HDD/C-Reduce-style structural reduction of the failing Lean TERM (Misherghi
    & Su, ICSE'06; Regehr et al., PLDI'12 — see RELATED_WORK).  The count-based
    `minimize` only shrinks (#defs, #inputs); this shrinks the def's *body*.

    We repeatedly try replacing each balanced-paren subterm with a small set of
    type-agnostic leaves (`0`, `[]`, `true`, `(none : Option Nat)`, a param name).
    A rewrite is kept iff the file still elaborates AND still reproduces the same
    bug class — so a kept rewrite is guaranteed sound (Lean re-type-checks it and
    the oracle recomputes the expected value).  Greedy fixpoint over rounds.

    Returns the minimized body string (or the original if nothing shrank)."""
    orig_body, rebuild, params = gen.single_def_body(seed, ninputs, emi=emi)
    fd, tmp = tempfile.mkstemp(prefix=f"shrink_{seed}_", suffix=".lean")
    os.close(fd)
    # Confirm the starting point actually reproduces (guards against a mismatch
    # between the count-minimizer's kind and the single-def file).
    if not _lean_src_fails(rebuild(orig_body), want_kind, tmp):
        os.unlink(tmp)
        return orig_body
    leaves = ["0", "[]", "true", "(none : Option Nat)"] + params
    body = orig_body
    try:
        for _ in range(max_rounds):
            changed = False
            # Longest spans first: collapsing a big subterm removes the most.
            for (a, b) in sorted(_paren_spans(body), key=lambda ab: ab[1] - ab[0],
                                 reverse=True):
                sub = body[a:b]
                for leaf in leaves:
                    if leaf == sub or f"({leaf})" == sub:
                        continue
                    cand = body[:a] + leaf + body[b:]
                    if cand == body:
                        continue
                    if _lean_src_fails(rebuild(cand), want_kind, tmp):
                        body = cand
                        changed = True
                        break
                if changed:
                    break
            if not changed:
                break
    finally:
        try:
            os.unlink(tmp)
        except OSError:
            pass
    return body


def report_bug(seed, kind, detail, ndefs, ninputs, emi):
    """Minimize a failing seed, save the reproducer, and exit(1).

    Two-stage reduction: first `minimize` shrinks (#defs, #inputs) to isolate a
    single failing def; then `struct_shrink` reduces that def's *term* (HDD-style)
    so the saved repro is a minimal expression, not a big generated tree."""
    print(f"\n*** TRANSPILER BUG — seed {seed} — kind={kind} ***")
    print(f"  {detail}")
    (md, mi), mf = minimize(seed, ndefs, ninputs, emi=emi)
    os.makedirs(os.path.join(HERE, "repro"), exist_ok=True)
    repro_lean = os.path.join(HERE, "repro", f"seed{seed}.lean")
    print(f"  minimized to defs={md} inputs={mi}")
    # Structural term reduction when the failure isolated to one def.
    shrunk_src = None
    fail_kind = mf.kind if mf else kind
    if md == 1:
        _orig, rebuild, _params = gen.single_def_body(seed, mi, emi=emi)
        shrunk_body = struct_shrink(seed, mi, fail_kind, emi=emi)
        shrunk_src = rebuild(shrunk_body)
        print(f"  structurally shrank body to: {shrunk_body}")
    with open(repro_lean, "w") as fh:
        fh.write(shrunk_src if shrunk_src else gen.emit_lean_file(seed, md, mi, emi=emi))
    print(f"  saved {repro_lean}")
    if mf:
        print(f"  minimal failure: {mf.kind}: {mf.detail}")
    sys.exit(1)


def report_corpus_bug(seed, kind, detail, nfuncs, ninputs):
    """Minimize a failing corpus seed (shrink #functions, then #inputs) and save
    the reproducer."""
    print(f"\n*** TRANSPILER BUG (corpus) — seed {seed} — kind={kind} ***")
    print(f"  {detail}")
    best, mf = (nfuncs, ninputs), None
    funcs = corpus_frags.harvest()
    for nf in range(1, nfuncs + 1):
        for ni in range(1, ninputs + 1):
            try:
                run_corpus_seed(seed, nf, ni, funcs=funcs)
            except Failure as f:
                best, mf = (nf, ni), f
                break
        if mf:
            break
    md, mi = best
    os.makedirs(os.path.join(HERE, "repro"), exist_ok=True)
    repro_lean = os.path.join(HERE, "repro", f"corpus_seed{seed}.lean")
    src, chosen = corpus_frags.emit_corpus_file(seed, md, mi, funcs=funcs)
    with open(repro_lean, "w") as fh:
        fh.write(src)
    print(f"  minimized to funcs={md} inputs={mi} ({chosen}); saved {repro_lean}")
    if mf:
        print(f"  minimal failure: {mf.kind}: {mf.detail}")
    sys.exit(1)


def pycov_seed(args):
    """Pool worker: transpile a corpus seed and measure input-adequacy coverage
    of the transpiled Python.  Returns {py_fn: (frozenset hit, frozenset body)}
    or {} if the seed hit a Lean error (nothing to measure)."""
    seed, nfuncs, ninputs = args
    src, _chosen = corpus_frags.emit_corpus_file(seed, nfuncs, ninputs)
    fd, path = tempfile.mkstemp(prefix=f"pycov_{seed}_", suffix=".lean")
    os.close(fd)
    try:
        _rc, out, err = lean_run(src, path)
    finally:
        try:
            os.unlink(path)
        except OSError:
            pass
    if real_errors(err) + real_errors(out) or "### ORACLE" not in out:
        return {}
    try:
        cov = measure_pycov(out)
    except Exception:  # noqa: BLE001
        return {}
    return {fn: (frozenset(hit), frozenset(body)) for fn, (hit, body) in cov.items()}


def run_pycov_mode(args):
    """Input-adequacy sweep (task 5): measure how thoroughly the oracle inputs
    exercise each transpiled function's body across the whole sweep, unioning hit
    lines per function.  Flags functions that never reach full coverage — their
    unexercised branches are where a transpiler bug would hide undiff'd."""
    corpus_frags.build_type_info_cache()  # once in parent; workers read the JSON
    all_funcs = corpus_frags.harvest()
    print(f"Input-adequacy (pycov) sweep: {len(all_funcs)} corpus functions, "
          f"{args.seeds} seeds x {args.defs} funcs x {args.inputs} inputs.")
    seeds = list(range(args.start, args.start + args.seeds))
    # Union hit lines per function; body-line set is stable per function.
    agg_hit, agg_body = {}, {}
    done = 0
    with ProcessPoolExecutor(max_workers=args.jobs) as ex:
        futures = [ex.submit(pycov_seed, (s, args.defs, args.inputs)) for s in seeds]
        for fut in as_completed(futures):
            for fn, (hit, body) in fut.result().items():
                agg_hit.setdefault(fn, set()).update(hit)
                agg_body.setdefault(fn, set()).update(body)
            done += 1
            if done % 25 == 0:
                print(f"  ... {done}/{len(seeds)} seeds")

    rows = []
    for fn in sorted(agg_body):
        body = agg_body[fn]
        hit = agg_hit.get(fn, set()) & body
        if body:
            rows.append((len(hit) / len(body), fn, len(hit), len(body)))
    total_hit = sum(len(agg_hit.get(fn, set()) & agg_body[fn]) for fn in agg_body)
    total_body = sum(len(b) for b in agg_body.values())
    print(f"\nTranspiled-Python input adequacy: {total_hit}/{total_body} body "
          f"lines exercised across {len(agg_body)} functions "
          f"({100 * total_hit // max(total_body, 1)}%).")
    under = [r for r in sorted(rows) if r[0] < 1.0]
    if under:
        print(f"\n{len(under)} function(s) with UNEXERCISED lines (a bug in an "
              f"unreached branch would hide):")
        for (frac, fn, h, b) in under[:25]:
            print(f"  {fn:40} {h}/{b} lines ({int(100 * frac)}%)")
    else:
        print("\nEvery transpiled function's body fully exercised by the inputs.")


def pycov_search_fn(args):
    """Coverage-guided input search for ONE transpiled corpus function, then
    differential validation of the discovered covering inputs.

    Steps: (1) transpile the function once via Lean; (2) run `input_search` on
    the transpiled Python to find a small input set maximizing body-line
    coverage; (3) emit a Lean oracle over those inputs and diff — so a
    newly-reached branch that mis-transpiles is caught.  Returns
    (qual, hit, body, status, detail)."""
    qual, ptypes, ret, budget = args
    # Skip user-typed functions here: the coverage-guided search's input
    # mutators/generators only cover the base value universe.  Such functions are
    # still differentially validated by the main `--corpus` sweep (the real
    # bug-finder); `--pycov-search` is an input-adequacy tool for base-typed fns.
    if any(t not in gen.LEAN_TYPES for t in ptypes):
        return (qual, 0, 0, "ok", "")
    # (1) transpile once.
    src = corpus_frags.emit_transpile_only(qual)
    fd, path = tempfile.mkstemp(prefix="pcs_t_", suffix=".lean")
    os.close(fd)
    try:
        _rc, out, err = lean_run(src, path)
    finally:
        try:
            os.unlink(path)
        except OSError:
            pass
    if real_errors(err) + real_errors(out) or "### PYTHON" not in out:
        return (qual, 0, 0, "transpile-error", "\n".join(real_errors(err + out)[:2]))
    py_src = out[out.index("### PYTHON") + len("### PYTHON"):].strip("\n")
    py_fn = _name_map(py_src).get(qual)
    if not py_fn:
        return (qual, 0, 0, "no-fn", f"{qual} not in transpiled output")
    try:
        # Prefer PATH mode (sys.monitoring, 3.12+): the search targets uncovered
        # k-line subpaths — branch *combinations* — the strongest adequacy signal.
        # Falls back to branch mode (SlipCover) then line mode automatically.
        want_paths = pycov.have_path_coverage()
        harness = pycov.Harness(py_src, branch=True, paths=want_paths)
    except Exception as e:  # noqa: BLE001
        return (qual, 0, 0, "exec", f"{type(e).__name__}: {e}")
    body = harness.body_units(py_fn)
    # Path mode is OPEN-ENDED (`body` empty by design): still search.  In the
    # non-path modes an empty `body` genuinely means nothing to cover — skip.
    if not body and not harness.paths:
        return (qual, 0, 0, "ok", "")
    # (2) search inputs in pure Python (no Lean).
    covering, hit = input_search.search(harness, harness.ns[py_fn], ptypes, body,
                                        seed=0, budget=budget)
    # (3) validate the covering inputs through the Lean oracle.
    status, detail = "ok", ""
    if covering:
        osrc = corpus_frags.emit_oracle_over(qual, ptypes, ret, covering)
        fd, opath = tempfile.mkstemp(prefix="pcs_o_", suffix=".lean")
        os.close(fd)
        try:
            _rc, oout, oerr = lean_run(osrc, opath)
        finally:
            try:
                os.unlink(opath)
            except OSError:
                pass
        if real_errors(oerr) + real_errors(oout):
            status, detail = "lean-error", "\n".join(real_errors(oerr + oout)[:2])
        else:
            try:
                check_output(oout)
            except Failure as f:
                status, detail = f.kind, f.detail
    return (qual, len(hit), len(body), status, detail)


def run_pycov_search_mode(args):
    """Coverage-guided input generation (task-5 follow-up): for each corpus
    function, greybox-search inputs that maximize coverage of its TRANSPILED body,
    then differentially validate those inputs against the Lean oracle.  Reports
    per-function adequacy and any divergence a newly-reached branch exposes."""
    corpus_frags.build_type_info_cache()  # once in parent; workers read the JSON
    all_funcs = corpus_frags.harvest()
    budget = max(args.inputs * 50, 200)
    paths_mode = pycov.have_path_coverage()
    unit = ("k-line paths" if paths_mode
            else "branches" if pycov.have_branch_coverage() else "lines")
    backend = ("sys.monitoring" if paths_mode
               else "slipcover" if pycov.have_slipcover() else "settrace")
    print(f"Coverage-guided input search: {len(all_funcs)} corpus functions, "
          f"budget {budget} candidate inputs each; coverage unit = {unit} "
          f"(backend: {backend}).")
    bugs, rows, done = [], [], 0
    with ProcessPoolExecutor(max_workers=args.jobs) as ex:
        futures = [ex.submit(pycov_search_fn, (q, pt, r, budget))
                   for (q, pt, r) in all_funcs]
        for fut in as_completed(futures):
            qual, hit, body, status, detail = fut.result()
            # `body` is 0 in path mode (open-ended universe); `hit` is the count
            # of distinct units discovered.
            rows.append((qual, hit, body))
            if status not in ("ok", "transpile-error", "no-fn", "lean-error"):
                bugs.append((qual, status, detail))
            done += 1
            if done % 20 == 0:
                print(f"  ... {done}/{len(all_funcs)} functions "
                      f"({len(bugs)} divergence(s) so far)")

    total_hit = sum(h for (_, h, _) in rows)
    if paths_mode:
        # Open-ended: no denominator; report discovered-subpath totals.  The
        # validation of every covering input against the Lean oracle is the real
        # signal — a search that reaches a mis-transpiled branch combination is
        # caught below.
        print(f"\nGuided path search: {total_hit} distinct k-line subpaths "
              f"discovered across {len(rows)} functions and validated against "
              f"the oracle.")
    else:
        total_body = sum(b for (_, _, b) in rows)
        full = sum(1 for (_, h, b) in rows if b and h >= b)
        print(f"\nGuided input adequacy: {total_hit}/{total_body} {unit} "
              f"({100 * total_hit // max(total_body, 1)}%); "
              f"{full}/{len(rows)} functions fully covered.")
        under = sorted((h / b, q, h, b) for (q, h, b) in rows if b and h < b)
        if under:
            print(f"\n{len(under)} function(s) still under full coverage "
                  f"(genuinely rare/undriveable branches):")
            for (frac, qual, h, b) in under[:20]:
                print(f"  {qual:45} {h}/{b} ({int(100 * frac)}%)")
    if bugs:
        print(f"\n*** {len(bugs)} DIVERGENCE(S) on searched inputs ***")
        for (qual, status, detail) in sorted(bugs):
            print(f"  {qual}: {status}: {detail}")
        sys.exit(1)


def run_corpus_mode(args):
    """Fragment-reuse sweep: each seed transpiles `--defs` harvested corpus
    functions and diffs them against the Lean oracle on random inputs.

    Efficiency: the type dump and harvest are computed ONCE in the parent (a Lean
    spawn each) and the function list is passed to workers, instead of every
    worker re-spawning Lean to reload type info / re-harvesting.  With `--batch B`
    each worker packs B seeds into one Lean file, amortizing Lean startup + the
    `import Corpus` olean load across many functions (~5x, per grammar mode)."""
    corpus_frags.build_type_info_cache()  # once in parent; workers read the JSON
    all_funcs = corpus_frags.harvest()
    print(f"Corpus fragment fuzzing: {len(all_funcs)} harvestable functions, "
          f"{args.seeds} seeds x {args.defs} funcs x {args.inputs} inputs"
          f"{f' (batch {args.batch})' if args.batch > 0 else ''}.")
    seeds = list(range(args.start, args.start + args.seeds))
    checked = lean_errors = done = 0
    bugs = []
    exercised = set()
    fired_all, known_all = set(), set()

    def handle(seed, status, detail, chosen, fired, known):
        nonlocal checked, lean_errors, done
        exercised.update(chosen)
        fired_all.update(fired)
        known_all.update(known)
        done += 1
        if status == "ok":
            checked += 1
        elif status == "lean-error":
            lean_errors += 1
        else:
            bugs.append((seed, status, detail))
        if done % 25 == 0:
            print(f"  ... {done}/{len(seeds)} seeds ({checked} checked, "
                  f"{len(bugs)} bug(s) so far)")

    with ProcessPoolExecutor(max_workers=args.jobs) as ex:
        if args.batch > 0:
            chunks = [seeds[i:i + args.batch]
                      for i in range(0, len(seeds), args.batch)]
            futures = [ex.submit(check_corpus_batch,
                                 (c, args.defs, args.inputs, all_funcs))
                       for c in chunks]
            for fut in as_completed(futures):
                for rec in fut.result():
                    handle(*rec)
        else:
            futures = [ex.submit(check_corpus_seed,
                                 (s, args.defs, args.inputs, all_funcs))
                       for s in seeds]
            for fut in as_completed(futures):
                handle(*fut.result())

    if bugs:
        bugs.sort()
        seed, kind, detail = bugs[0]
        if len(bugs) > 1:
            print(f"\n{len(bugs)} seeds failed; reporting the lowest: "
                  f"{sorted(s for s, _, _ in bugs)}")
        report_corpus_bug(seed, kind, detail, args.defs, args.inputs)

    total = len(all_funcs)
    print(f"\nNo transpiler bugs found in {len(seeds)} corpus seeds "
          f"({checked} checked).")
    print(f"\nCorpus function coverage: {len(exercised)}/{total} distinct "
          f"functions exercised.")
    missed = sorted(q for (q, _, _) in all_funcs if q not in exercised)
    if missed:
        print(f"  never selected: {', '.join(missed)}")
    report_self_coverage(fired_all, known_all)


def main():
    # The transpiled Python uses PEP 604 unions (`list[int] | None`) in dataclass
    # fields / type aliases, which are evaluated eagerly and require Python 3.10+.
    # Fail fast with a clear message rather than misreporting the resulting
    # TypeError as a transpiler bug (as happens under 3.9).
    if sys.version_info < (3, 10):
        sys.exit(f"fuzz.py needs Python 3.10+ to exec the transpiled code "
                 f"(found {sys.version.split()[0]}); e.g. run with python3.11.")
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, default=200)
    ap.add_argument("--start", type=int, default=0)
    ap.add_argument("--defs", type=int, default=8)
    ap.add_argument("--inputs", type=int, default=6)
    ap.add_argument("--emi", type=float, default=0.3,
                    help="EMI envelope probability per subterm (0 disables)")
    ap.add_argument("--jobs", type=int, default=max(1, (os.cpu_count() or 2) - 1),
                    help="parallel worker processes (default: cores - 1)")
    ap.add_argument("--batch", type=int, default=0,
                    help="seeds packed per Lean spawn (0 = one seed per spawn). "
                         "Amortizes Lean's ~1s startup across many functions; a "
                         "failing/ill-typed seed is re-run alone to isolate it.")
    ap.add_argument("--corpus", action="store_true",
                    help="fragment-reuse mode: fuzz REAL harvested Corpus/*.lean "
                         "defs on random inputs instead of grammar-generated ones "
                         "(--defs = functions/file). Exercises constructs the "
                         "grammar never invents.")
    ap.add_argument("--pycov", action="store_true",
                    help="input-adequacy mode: measure line coverage of the "
                         "TRANSPILED Python during oracle execution and flag "
                         "functions with unexercised branches (where a bug hides).")
    ap.add_argument("--pycov-search", action="store_true", dest="pycov_search",
                    help="coverage-guided input search: for each corpus function, "
                         "greybox-search inputs that maximize coverage of its "
                         "transpiled body, then validate them against the oracle.")
    args = ap.parse_args()

    # Capture LEAN_PATH once and export it so every worker inherits it instead
    # of each spawning its own (serializing) `lake env`.
    os.environ["FUZZ_LEAN_PATH"] = _lean_env()["LEAN_PATH"]

    if args.pycov_search:
        return run_pycov_search_mode(args)
    if args.pycov:
        return run_pycov_mode(args)
    if args.corpus:
        return run_corpus_mode(args)

    seeds = list(range(args.start, args.start + args.seeds))
    lean_errors = checked = done = 0
    bugs = []  # (seed, kind, detail)
    offered, hit = set(), set()
    koffered, khit = set(), set()  # k-path (context-sensitive) coverage
    fired_all, known_all = set(), set()  # transpiler self-coverage

    # Check seeds in parallel.  Each worker elaborates one Lean file (the
    # bottleneck); with `--batch B` that file packs B seeds so Lean's ~1s startup
    # is amortized across B*defs functions.  We drain results as they complete,
    # aggregate coverage, collect any bugs, then report the LOWEST-seed bug so the
    # run's verdict is deterministic regardless of completion order.
    def handle(seed, status, detail, off, ht, koff, kht, fired, known):
        nonlocal checked, lean_errors, done
        offered.update(off)
        hit.update(ht)
        koffered.update(koff)
        khit.update(kht)
        fired_all.update(fired)
        known_all.update(known)
        done += 1
        if status == "ok":
            checked += 1
        elif status == "lean-error":
            lean_errors += 1
        else:
            bugs.append((seed, status, detail))
        if done % 25 == 0:
            print(f"  ... {done}/{len(seeds)} seeds ({checked} checked, "
                  f"{lean_errors} skipped, {len(bugs)} bug(s) so far)")

    with ProcessPoolExecutor(max_workers=args.jobs) as ex:
        if args.batch > 0:
            chunks = [seeds[i:i + args.batch]
                      for i in range(0, len(seeds), args.batch)]
            futures = [ex.submit(check_batch, (c, args.defs, args.inputs, args.emi))
                       for c in chunks]
            for fut in as_completed(futures):
                for rec in fut.result():
                    handle(*rec)
        else:
            futures = [ex.submit(check_seed, (s, args.defs, args.inputs, args.emi))
                       for s in seeds]
            for fut in as_completed(futures):
                handle(*fut.result())

    if bugs:
        bugs.sort()  # lowest seed first — deterministic verdict
        seed, kind, detail = bugs[0]
        if len(bugs) > 1:
            print(f"\n{len(bugs)} seeds failed; reporting the lowest: "
                  f"{sorted(s for s, _, _ in bugs)}")
        report_bug(seed, kind, detail, args.defs, args.inputs, args.emi)

    print(f"\nNo transpiler bugs found in {len(seeds)} seeds "
          f"({checked} checked, {lean_errors} skipped as ill-typed).")
    # Grammar production coverage over the whole sweep.
    universe = gen.ALL_PRODUCTIONS
    hitp = hit & universe
    print(f"\nGrammar production coverage: {len(hitp)}/{len(universe)} "
          f"({100 * len(hitp) // max(len(universe), 1)}%)")
    missed = sorted(universe - hitp)
    if missed:
        print(f"  never exercised: {', '.join(missed)}")
    # Context-sensitive (k-path) coverage: how many of the nested-production
    # chains the grammar *can* form did the sweep actually exercise.  Reported as
    # a fraction of the paths OFFERED across the sweep (the reachable universe is
    # combinatorial and only discovered by generating), so it measures how
    # thoroughly the sweep explored the contexts it encountered.
    if koffered:
        print(f"\nk-path coverage (≤{gen.Gen.KMAX} nested productions): "
              f"{len(khit)}/{len(koffered)} offered paths "
              f"({100 * len(khit) // max(len(koffered), 1)}%)")
    report_self_coverage(fired_all, known_all)


if __name__ == "__main__":
    main()
