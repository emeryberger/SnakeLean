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

Usage:
  python3 fuzz/fuzz.py [--seeds N] [--start S] [--defs D] [--inputs I]
"""
import argparse
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "roundtrip"))
import run_oracle  # noqa: E402  (reuse load/normalize/call)
import gen  # noqa: E402


def lean_run(lean_src, tmp_path):
    with open(tmp_path, "w") as f:
        f.write(lean_src)
    env = dict(os.environ)
    env["PATH"] = os.path.expanduser("~/.elan/bin") + ":" + env.get("PATH", "")
    proc = subprocess.run(
        ["lake", "env", "lean", tmp_path],
        cwd=ROOT, capture_output=True, text=True, env=env,
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


def run_seed(seed, ndefs, ninputs, tmp_path, coverage=None):
    # Each file is coverage-guided *internally* (its own Gen prefers uncovered
    # productions), so a file depends only on its seed — reproducibility the
    # shrinker relies on.  We do NOT steer across seeds (that would make a file
    # depend on sweep history); instead we just aggregate which productions were
    # exercised, into `coverage`, to report grammar coverage over the whole run.
    src = gen.emit_lean_file(seed, ndefs, ninputs)
    if coverage is not None:
        coverage["offered"] |= gen.emit_lean_file.last_gen.all_prods
        coverage["hit"] |= gen.emit_lean_file.last_gen.covered
    _rc, out, err = lean_run(src, tmp_path)
    # `lake env lean` prints elaboration errors to stdout (interleaved with the
    # `#eval` output) as well as stderr, so scan both.  A Lean error means the
    # GENERATOR produced ill-typed code (not a transpiler bug); skip such seeds.
    errs = real_errors(err) + real_errors(out)
    if errs:
        raise Failure("lean-error", "\n".join(errs[:3]))
    check_output(out)


def minimize(seed, ndefs, ninputs, tmp_path):
    """Shrink to the smallest (defs, inputs) that still fails for this seed."""
    best = (ndefs, ninputs)
    for d in range(1, ndefs + 1):
        for i in range(1, ninputs + 1):
            try:
                run_seed(seed, d, i, tmp_path)
            except Failure as f:
                if f.kind != "lean-error":
                    return (d, i), f
    return best, None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, default=200)
    ap.add_argument("--start", type=int, default=0)
    ap.add_argument("--defs", type=int, default=8)
    ap.add_argument("--inputs", type=int, default=6)
    args = ap.parse_args()

    tmp = "/tmp/fuzz_run.lean"
    lean_errors = 0
    checked = 0
    coverage = {"offered": set(), "hit": set()}
    for seed in range(args.start, args.start + args.seeds):
        try:
            run_seed(seed, args.defs, args.inputs, tmp, coverage=coverage)
            checked += 1
        except Failure as f:
            if f.kind == "lean-error":
                lean_errors += 1
                continue  # generator produced ill-typed code; not our bug
            # A real transpiler bug.
            print(f"\n*** TRANSPILER BUG — seed {seed} — kind={f.kind} ***")
            print(f"  {f.detail}")
            (md, mi), mf = minimize(seed, args.defs, args.inputs, tmp)
            os.makedirs(os.path.join(HERE, "repro"), exist_ok=True)
            repro_lean = os.path.join(HERE, "repro", f"seed{seed}.lean")
            with open(repro_lean, "w") as fh:
                fh.write(gen.emit_lean_file(seed, md, mi))
            print(f"  minimized to defs={md} inputs={mi}; saved {repro_lean}")
            if mf:
                print(f"  minimal failure: {mf.kind}: {mf.detail}")
            sys.exit(1)
        if (seed - args.start + 1) % 25 == 0:
            print(f"  ... {seed - args.start + 1} seeds ({checked} checked, "
                  f"{lean_errors} skipped as ill-typed)")
    print(f"\nNo transpiler bugs found in {args.seeds} seeds "
          f"({checked} checked, {lean_errors} skipped as ill-typed).")
    # Grammar production coverage over the whole sweep.
    universe = gen.ALL_PRODUCTIONS
    hit = coverage["hit"] & universe
    print(f"\nGrammar production coverage: {len(hit)}/{len(universe)} "
          f"({100 * len(hit) // max(len(universe), 1)}%)")
    missed = sorted(universe - hit)
    if missed:
        print(f"  never exercised: {', '.join(missed)}")


if __name__ == "__main__":
    main()
