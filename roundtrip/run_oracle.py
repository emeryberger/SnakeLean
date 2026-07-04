#!/usr/bin/env python3
"""Differential round-trip check: Lean is the oracle.

Reads the combined output of `roundtrip/Oracle.lean` (a `### PYTHON` section
holding the transpiled code, then a `### ORACLE` section of tab-separated
`ORACLE <pyfn> <json-args> <json-result>` rows).  It execs the Python, calls
each function on the oracle's inputs, and asserts the Python result equals the
Lean result.

Agreement across the battery is the evidence that the Lean->Python
transpilation is faithful: the generated Python computes exactly what the
original Lean definition computes, with Lean itself (not hand-written expected
values) as ground truth.

Usage:
    lake env lean roundtrip/Oracle.lean > roundtrip/gen.txt
    python3 roundtrip/run_oracle.py roundtrip/gen.txt
"""
import inspect
import json
import re
import sys


def load(path):
    text = open(path).read()
    # Split into the two banners.
    py_start = text.index("### PYTHON") + len("### PYTHON")
    or_start = text.index("### ORACLE")
    py_src = text[py_start:or_start].strip("\n")
    oracle_block = text[or_start + len("### ORACLE"):]
    # Build the fully-qualified-Lean-name -> Python-name map from the
    # `# Lean: <fqname>` comment that precedes each `def`.  This decouples the
    # oracle from the transpiler's snake_case / module-prefix heuristics.
    lean_to_py = {}
    lines = py_src.splitlines()
    for i, line in enumerate(lines):
        m = re.match(r"# Lean: (\S+)", line)
        if m and i + 1 < len(lines):
            d = re.match(r"def (\w+)\(", lines[i + 1])
            if d:
                lean_to_py[m.group(1)] = d.group(1)
    rows = []
    for line in oracle_block.splitlines():
        if not line.startswith("ORACLE\t"):
            continue
        _, fn, args_json, res_json = line.split("\t")
        rows.append((fn, json.loads(args_json), json.loads(res_json)))
    return py_src, lean_to_py, rows


def normalize(v):
    # Lean `List Nat` <-> Python list; Bool <-> bool; Option Nat: None or int.
    # JSON already gives us list/bool/int/None, so compare structurally, but
    # coerce Python tuples (from Prod) to lists.
    if isinstance(v, tuple):
        return [normalize(x) for x in v]
    if isinstance(v, list):
        return [normalize(x) for x in v]
    return v


def call(fn, args):
    """Call a transpiled function, padding leading erased type parameters.

    A polymorphic Lean function (e.g. `reverse {α} (xs : List α)`) keeps its
    type parameter as a leading runtime argument (`__k: Any`).  We detect the
    arity gap and prepend `None` placeholders for those erased type args, which
    the transpiled body never inspects.
    """
    try:
        nparams = len(inspect.signature(fn).parameters)
    except (ValueError, TypeError):
        nparams = len(args)
    pad = max(0, nparams - len(args))
    return fn(*([None] * pad), *args)


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "roundtrip/gen.txt"
    py_src, lean_to_py, rows = load(path)

    ns = {}
    exec(compile(py_src, "<transpiled>", "exec"), ns)

    passed = failed = 0
    failures = []
    fns_seen = set()
    for lean_fn, args, expected in rows:
        fns_seen.add(lean_fn)
        py_fn = lean_to_py.get(lean_fn)
        if py_fn is None or py_fn not in ns:
            failed += 1
            failures.append((lean_fn, args, "<no python fn>", expected))
            continue
        try:
            got = normalize(call(ns[py_fn], args))
        except Exception as e:  # noqa: BLE001
            failed += 1
            failures.append((lean_fn, args, f"<raised {type(e).__name__}: {e}>", expected))
            continue
        if got == normalize(expected):
            passed += 1
        else:
            failed += 1
            failures.append((lean_fn, args, got, expected))

    total = passed + failed
    print(f"Round-trip differential (Lean oracle vs transpiled Python)")
    print(f"  functions covered: {len(fns_seen)}")
    print(f"  cases: {passed}/{total} agree")
    if failures:
        print(f"\n  {len(failures)} MISMATCH(es):")
        for fn, args, got, exp in failures[:30]:
            print(f"    {fn}{tuple(args)}: python={got!r}  lean={exp!r}")
        sys.exit(1)
    print("  ALL AGREE — transpilation is faithful on this battery")
    sys.exit(0)


if __name__ == "__main__":
    main()
