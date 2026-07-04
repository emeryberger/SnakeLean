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


def lean_run(lean_src, tmp_path):
    with open(tmp_path, "w") as f:
        f.write(lean_src)
    proc = subprocess.run(
        ["lean", tmp_path],
        cwd=ROOT, capture_output=True, text=True, env=_lean_env(),
    )
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


def check_output(stdout):
    """Parse the ### PYTHON / ### ORACLE output and diff. Raise Failure on any
    disagreement, syntax error, or runtime exception."""
    if "### PYTHON" not in stdout or "### ORACLE" not in stdout:
        raise Failure("no-output", stdout[:400])
    # Reuse the round-trip loader/compare.
    py_start = stdout.index("### PYTHON") + len("### PYTHON")
    or_start = stdout.index("### ORACLE")
    py_src = stdout[py_start:or_start].strip("\n")
    oracle_block = stdout[or_start + len("### ORACLE"):]
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
        _, fn, args_json, res_json = line.split("\t")
        args = json.loads(args_json)
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
    errs = real_errors(err) + real_errors(out)
    if errs:
        raise Failure("lean-error", "\n".join(errs[:3]))
    check_output(out)


def check_seed(args):
    """Pool worker: check one seed. Returns a picklable result tuple
    (seed, status, detail, offered_prods, hit_prods).  `status` is
    'ok' | 'lean-error' | a transpiler-bug kind."""
    seed, ndefs, ninputs, emi = args
    try:
        run_seed(seed, ndefs, ninputs, emi=emi)
        g = gen.emit_lean_file.last_gen
        return (seed, "ok", "", frozenset(g.all_prods), frozenset(g.covered))
    except Failure as f:
        g = gen.emit_lean_file.last_gen
        return (seed, f.kind, f.detail, frozenset(g.all_prods), frozenset(g.covered))


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


def report_bug(seed, kind, detail, ndefs, ninputs, emi):
    """Minimize a failing seed, save the reproducer, and exit(1)."""
    print(f"\n*** TRANSPILER BUG — seed {seed} — kind={kind} ***")
    print(f"  {detail}")
    (md, mi), mf = minimize(seed, ndefs, ninputs, emi=emi)
    os.makedirs(os.path.join(HERE, "repro"), exist_ok=True)
    repro_lean = os.path.join(HERE, "repro", f"seed{seed}.lean")
    with open(repro_lean, "w") as fh:
        fh.write(gen.emit_lean_file(seed, md, mi, emi=emi))
    print(f"  minimized to defs={md} inputs={mi}; saved {repro_lean}")
    if mf:
        print(f"  minimal failure: {mf.kind}: {mf.detail}")
    sys.exit(1)


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
    args = ap.parse_args()

    # Capture LEAN_PATH once and export it so every worker inherits it instead
    # of each spawning its own (serializing) `lake env`.
    os.environ["FUZZ_LEAN_PATH"] = _lean_env()["LEAN_PATH"]

    seeds = list(range(args.start, args.start + args.seeds))
    lean_errors = checked = done = 0
    bugs = []  # (seed, kind, detail)
    offered, hit = set(), set()

    # Check seeds in parallel; each worker elaborates one Lean file (the
    # bottleneck) independently.  We drain results as they complete, aggregate
    # coverage, collect any bugs, then report the LOWEST-seed bug so the run's
    # verdict is deterministic regardless of completion order.
    with ProcessPoolExecutor(max_workers=args.jobs) as ex:
        futures = {ex.submit(check_seed, (s, args.defs, args.inputs, args.emi)): s
                   for s in seeds}
        for fut in as_completed(futures):
            seed, status, detail, off, ht = fut.result()
            offered |= off
            hit |= ht
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


if __name__ == "__main__":
    main()
