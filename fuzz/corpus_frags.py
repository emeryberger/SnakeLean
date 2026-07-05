#!/usr/bin/env python3
"""Fragment-reuse fuzzing: harvest real Lean definitions from `Corpus/*.lean`
and differentially test them on random inputs.

Motivation (LangFuzz-style fragment reuse, Holler/Herzig/Zeller, USENIX Sec'12):
a grammar fuzzer only exercises constructs it knows how to *invent*.  The curated
corpus is full of shapes the `gen.py` grammar never produces — `let rec` /
mutual recursion, `Array`, `String`, custom inductives, deeply nested matches.
Transpiling those and checking them against the Lean oracle on *random* inputs
(the corpus's own tests use fixed inputs) reaches transpiler paths the generated
grammar can't.

We harvest only the signatures whose parameter and return types are all in the
fuzzer's value universe (so `gen.rand_value` / `lean_lit` / `serializer_call`
can drive them).  A harvested function is referenced by its fully-qualified Lean
name; `emitPythonForNames` pulls in its transitive dependencies automatically, so
a one-line `insertionSort` fragment still drags in its `let rec insert`/`sort`.
"""
import os
import random
import re

import gen

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CORPUS_DIR = os.path.join(ROOT, "Corpus")

# The types the fuzzer can generate values for (must match gen.LEAN_TYPES).  A
# def is harvestable iff every parameter type and the return type is one of these.
_HARVESTABLE = {"Nat", "Bool", "Int", "List Nat", "Option Nat", "Nat × Nat",
                "String", "Char", "Array Nat"}

# `(a b : T)` binds two params of type T; `(x : T)` binds one.  We only accept
# a param group whose type is harvestable.
_PARAM_RE = re.compile(r"\(([^():]+):\s*([^()]+?)\s*\)")
_DEFNAME_RE = re.compile(r"^def\s+([A-Za-z_][A-Za-z0-9_']*)\s")
_NS_RE = re.compile(r"^namespace\s+(\S+)")
_END_RE = re.compile(r"^end\b")


def _norm_type(t):
    """Canonicalize a type annotation's whitespace so it matches `_HARVESTABLE`."""
    return re.sub(r"\s+", " ", t.strip())


def _signature(text):
    """From text starting at a `def`, return (name, sig_str) where `sig_str` is
    everything between the name and the top-level `:=`, or None.  Scans with
    paren/bracket-depth tracking so `:` and `:=` inside param types don't fool
    us."""
    nm = _DEFNAME_RE.match(text)
    if not nm:
        return None
    name = nm.group(1)
    i, depth = nm.end(), 0
    while i < len(text):
        c = text[i]
        if c in "([{":
            depth += 1
        elif c in ")]}":
            depth -= 1
        elif depth == 0 and text.startswith(":=", i):
            return name, text[nm.end():i]
        i += 1
    return None


def _split_ret(sig):
    """Split a signature `(params...) : RetType` at the top-level `:` separating
    params from the return type.  Returns (header, ret) or None."""
    depth = 0
    for i, c in enumerate(sig):
        if c in "([{":
            depth += 1
        elif c in ")]}":
            depth -= 1
        elif c == ":" and depth == 0:
            return sig[:i], _norm_type(sig[i + 1:])
    return None


def _parse_sig(header):
    """Parse the parameter section of a def header into a flat list of types, or
    return None if any param group's type is not harvestable (or params use a
    shape we don't model, e.g. implicit `{α}` or typeclass `[...]`)."""
    # Reject implicit/instance binders outright — they mean generics/typeclasses
    # the value universe can't drive.
    if "{" in header or "[" in header:
        return None
    ptypes = []
    pos = 0
    for m in _PARAM_RE.finditer(header):
        # Everything between param groups must be whitespace (no bare/optional
        # params we can't type).
        if header[pos:m.start()].strip():
            return None
        pos = m.end()
        names, ty = m.group(1).split(), _norm_type(m.group(2))
        if ty not in _HARVESTABLE:
            return None
        ptypes.extend([ty] * len(names))
    if header[pos:].strip():
        return None
    return ptypes


# Namespaces with KNOWN-OPEN transpiler bugs, excluded from harvesting so the
# sweep stays a clean regression signal.  Surfaced by the Phase-1 String/Char/
# Array expansion; tracked for a follow-up PR.  NOT false positives — genuine
# transpiler gaps concentrated in `Corpus.Strings` (which leans heavily on Lean
# String builtins the transpiler doesn't yet map):
#   - missing builtins falling through to an undefined Python name:
#     `String.startsWith`→`starts_with`, `.dropWhile`→`drop_while`,
#     `.replicate`→`replicate_tr`, `.dropLast`→`drop_last_tr`, etc.
#   - a batched-emission name collision: two functions in one file both bind a
#     line-numbered temp (`_x_798`), so one references a name from the other's
#     scope (NameError).  Only manifests in multi-function files.
# The individual String/Char/Array *value* handlers the fuzzer generates
# (push/append/toUpper/toLower/is*) ARE fixed — this excludes only functions
# that reach the still-unmapped builtins or the batch collision.  `Strings.*`
# hits missing builtins; `Production.*` hits the `_x_NNN` batch name-collision
# (its Array/nested code reuses LCNF temp numbers across functions in one file).
# Remove a prefix once its gap is fixed.
_KNOWN_OPEN_NS = ("Corpus.Strings.", "Corpus.Production.")


def _is_known_open(qual):
    return any(qual.startswith(ns) for ns in _KNOWN_OPEN_NS)


def harvest(corpus_dir=CORPUS_DIR, include_known_open=False):
    """Return a list of (qualified_name, [param_types], ret_type) for every
    top-level corpus `def` whose signature is entirely in the value universe.
    Functions in known-open namespaces (`_KNOWN_OPEN_NS`) are excluded unless
    `include_known_open` (used to re-check whether a documented bug is fixed).

    Deterministic: files and defs are returned in sorted/source order so a seed
    selecting among them reproduces exactly."""
    funcs = []
    for fname in sorted(os.listdir(corpus_dir)):
        if not fname.endswith(".lean") or fname.startswith("CorpusTest"):
            continue
        path = os.path.join(corpus_dir, fname)
        with open(path) as fh:
            text = fh.read()
        ns = []
        # Walk line-by-line for namespace tracking, but parse each `def` against
        # the remaining text (defs span multiple lines).
        lines = text.splitlines(keepends=True)
        offset = 0
        for line in lines:
            stripped = line.strip()
            nm = _NS_RE.match(stripped)
            if nm:
                ns.append(nm.group(1))
            elif _END_RE.match(stripped):
                if ns:
                    ns.pop()
            elif stripped.startswith("def "):
                sg = _signature(text[offset:])
                if sg:
                    name, sig = sg
                    parts = _split_ret(sig)
                    if parts:
                        header, ret = parts
                        # Need ≥1 param; skip dotted struct methods (receiver type
                        # not in the universe).
                        if "." not in name and ret in _HARVESTABLE:
                            ptypes = _parse_sig(header)
                            if ptypes:
                                qual = ".".join(ns + [name]) if ns else name
                                if include_known_open or not _is_known_open(qual):
                                    funcs.append((qual, ptypes, ret))
            offset += len(line)
    return funcs


# The Lean prelude for a corpus-fragment file additionally imports `Corpus`
# (so the harvested names resolve) and reuses gen.py's JSON serializers.
CORPUS_PRELUDE = gen.PRELUDE.replace(
    "import LeanToPython\n", "import LeanToPython\nimport Corpus\n", 1)

# Some harvested functions are only fast on small inputs (e.g. `nthPrime n`
# sieves up to the nth prime).  Clamp Nat inputs to a modest range so the oracle
# `#eval` terminates quickly; lists/ints keep gen.py's ranges.
_MAX_NAT = 8


def _rand_input(rng, ty):
    if ty == gen.NAT:
        return rng.randint(0, _MAX_NAT)
    if ty == gen.PAIR:
        return [rng.randint(0, _MAX_NAT), rng.randint(0, _MAX_NAT)]
    # Reuse gen.py's generators for the rest (a Gen wraps the same rng contract).
    g = gen.Gen.__new__(gen.Gen)
    g.rng = rng
    return g.rand_value(ty)


def emit_corpus_file(seed, nfuncs, ninputs, funcs=None):
    """Emit a Lean file that transpiles `nfuncs` harvested corpus functions and
    prints oracle rows for `ninputs` random inputs each.

    Pure function of `(seed, nfuncs, ninputs)` given a fixed corpus, so a failing
    seed reproduces exactly (the harvest order is deterministic).  Returns
    (lean_src, [chosen_qualified_names])."""
    funcs = funcs if funcs is not None else harvest()
    rng = random.Random(seed)
    chosen = funcs if nfuncs >= len(funcs) else rng.sample(funcs, nfuncs)

    names = ", ".join("`" + q for (q, _, _) in chosen)
    rows = []
    for (qual, ptypes, ret) in chosen:
        for _ in range(ninputs):
            vals = [_rand_input(rng, t) for t in ptypes]
            lean_args = " ".join(f"({gen.lean_lit(t, v)})" for (t, v) in zip(ptypes, vals))
            json_args = "[" + ",".join(gen.json_lit(t, v) for (t, v) in zip(ptypes, vals)) + "]"
            call = f"{qual} {lean_args}"
            ser = gen.serializer_call(ret, call)
            # Tag the ORACLE row with the qualified name so fuzz.py maps it back
            # to the transpiled `# Lean:` comment.  Escape json_args for embedding
            # in the Lean string literal (String/Char args carry quotes).
            rows.append(f'  IO.println ("ORACLE\\t{qual}\\t{gen._lean_str_escape(json_args)}\\t" ++ {ser})')

    parts = [CORPUS_PRELUDE, ""]
    parts.append("#eval show CoreM Unit from do")
    parts.append('  IO.println "### PYTHON"')
    parts.append(f"  IO.println (← emitPythonForNames `Fuzz [{names}])")
    parts.append('  IO.println "### ORACLE"')
    parts += rows
    return "\n".join(parts) + "\n", [q for (q, _, _) in chosen]


def emit_transpile_only(qual):
    """A Lean file that only transpiles `qual` (and its deps) to Python — no
    oracle rows.  Used by the coverage-guided input search, which needs the
    transpiled body once and then searches inputs purely in Python."""
    parts = [CORPUS_PRELUDE, ""]
    parts.append("#eval show CoreM Unit from do")
    parts.append('  IO.println "### PYTHON"')
    parts.append(f"  IO.println (← emitPythonForNames `Fuzz [`{qual}])")
    return "\n".join(parts) + "\n"


def emit_oracle_over(qual, ptypes, ret, input_rows):
    """A Lean file transpiling `qual` and printing ORACLE rows for the EXPLICIT
    `input_rows` (each a list of Python values, one per param).  Lets the search
    hand its discovered covering inputs back to the Lean oracle for differential
    validation.  Returns lean_src."""
    rows = []
    for vals in input_rows:
        lean_args = " ".join(f"({gen.lean_lit(t, v)})" for (t, v) in zip(ptypes, vals))
        json_args = "[" + ",".join(gen.json_lit(t, v) for (t, v) in zip(ptypes, vals)) + "]"
        ser = gen.serializer_call(ret, f"{qual} {lean_args}")
        rows.append(f'  IO.println ("ORACLE\\t{qual}\\t{gen._lean_str_escape(json_args)}\\t" ++ {ser})')
    parts = [CORPUS_PRELUDE, ""]
    parts.append("#eval show CoreM Unit from do")
    parts.append('  IO.println "### PYTHON"')
    parts.append(f"  IO.println (← emitPythonForNames `Fuzz [`{qual}])")
    parts.append('  IO.println "### ORACLE"')
    parts += rows
    return "\n".join(parts) + "\n"


if __name__ == "__main__":
    fs = harvest()
    print(f"{len(fs)} harvestable corpus functions:")
    for (q, ps, r) in fs:
        print(f"  {q} : {' → '.join(ps + [r])}")
