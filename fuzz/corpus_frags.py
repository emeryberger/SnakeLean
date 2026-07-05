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
import subprocess

import gen

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CORPUS_DIR = os.path.join(ROOT, "Corpus")


# ---------------------------------------------------------------------------
# Phase 3: custom inductive / structure types.
#
# A Lean-side dump (`fuzz/TypeInfo.lean`) reports each corpus type's
# constructors and their field types (robust to source formatting / Lean
# version, unlike a regex over source).  From it we compute which types are
# *constructible* from the fuzzer's value universe (all fields base-harvestable
# or themselves constructible user types), so we can generate values, emit them
# as Lean literals, and compare a transpiled dataclass instance against the Lean
# oracle.  We deliberately start with the tractable slice — enums (nullary
# constructors) and non-recursive structs over constructible fields — leaving
# recursive types (Expr/Trie/JsonValue) and Float-bearing ones out (recursion
# needs depth bounds; Float isn't in the value universe).
# ---------------------------------------------------------------------------

# type name -> list of (ctor_full_name, [field_type_str, ...]); loaded lazily.
_TYPE_INFO = None
# type name -> True/False constructibility (memoized during analysis).
_CONSTRUCTIBLE = {}


def _load_type_info():
    """Run `fuzz/TypeInfo.lean` and parse its `### TYPE` lines into `_TYPE_INFO`
    ({type: [(ctor, [fieldtypes])]}).  Cached after first call."""
    global _TYPE_INFO
    if _TYPE_INFO is not None:
        return _TYPE_INFO
    info = {}
    env = dict(os.environ)
    env["PATH"] = os.path.expanduser("~/.elan/bin") + ":" + env.get("PATH", "")
    lp = env.get("FUZZ_LEAN_PATH")
    if lp is None:
        out = subprocess.run(["lake", "env", "printenv", "LEAN_PATH"], cwd=ROOT,
                             capture_output=True, text=True, env=env)
        lp = out.stdout.strip()
    env["LEAN_PATH"] = lp
    proc = subprocess.run(["lean", os.path.join(HERE, "TypeInfo.lean")], cwd=ROOT,
                          capture_output=True, text=True, env=env)
    for line in proc.stdout.splitlines():
        if not line.startswith("### TYPE\t"):
            continue
        _, tyname, ctors_str = line.split("\t", 2)
        ctors = []
        for cpart in ctors_str.split(" | "):
            cname, _, fields_str = cpart.partition(";")
            fields = [f for f in fields_str.split(",") if f]
            ctors.append((cname, fields))
        info[tyname] = ctors
    _TYPE_INFO = info
    return info


_SHORT_TO_QUAL = None


def _ns_prefixes(ns, defname):
    """Namespace prefixes to try when resolving a short type name in a def's
    signature: every suffix of the `namespace` stack, plus (for a dotted def name
    like `Card.value`) the def's own leading component joined onto each."""
    joined = ".".join(ns)
    prefixes = []
    if joined:
        prefixes.append(joined)
    # a dotted def name (`Card.value`) — the `Card` part is likely a type in scope
    if "." in defname:
        head = defname.rsplit(".", 1)[0]
        prefixes.append(f"{joined}.{head}" if joined else head)
        prefixes.append(head)
    return tuple(prefixes)


def _resolve_type(ty, ns_prefixes=()):
    """Resolve a type name as written in a signature to a fully-qualified corpus
    type name if it is one.  Signatures use either the qualified name
    (`Corpus.Games.RPS`) or the short name (`RPS`) when in-namespace; try the
    given namespace prefixes then a unique short-name match.  Returns `ty`
    unchanged if it's not a (unique) corpus type."""
    global _SHORT_TO_QUAL
    info = _load_type_info()
    if ty in info:
        return ty
    for p in ns_prefixes:
        if f"{p}.{ty}" in info:
            return f"{p}.{ty}"
    if _SHORT_TO_QUAL is None:
        short = {}
        for q in info:
            short.setdefault(q.rsplit(".", 1)[-1], []).append(q)
        _SHORT_TO_QUAL = {s: qs[0] for s, qs in short.items() if len(qs) == 1}
    return _SHORT_TO_QUAL.get(ty, ty)


def _is_constructible(ty, stack=()):
    """Can the fuzzer build a value of Lean type `ty`?  True for base-harvestable
    types and for user types whose every constructor's fields are all
    constructible.  `stack` guards against recursive types (Expr → Expr): a type
    that recurses through itself is treated as NOT constructible (no depth bound
    yet)."""
    if ty in _HARVESTABLE:
        return True
    info = _load_type_info()
    if ty not in info:
        return False
    if ty in stack:            # recursive — bail (would need a depth bound)
        return False
    if ty in _CONSTRUCTIBLE:
        return _CONSTRUCTIBLE[ty]
    ok = all(all(_is_constructible(f, stack + (ty,)) for f in fields)
             for (_ctor, fields) in info[ty])
    _CONSTRUCTIBLE[ty] = ok
    return ok


# Constructor names the transpiler prefixes with their parent to avoid dataclass
# collisions — MUST match `toPyTypeName`/`isCommonCtorName` in LeanToPython.lean.
_COMMON_CTOR_NAMES = {"mk", "node", "empty", "nil", "cons", "some", "none"}


def _lean_ctor_short(ctor_full):
    """The Lean constructor short name for a match arm / application:
    `Corpus.Games.Nim.mk` -> `mk`."""
    return ctor_full.rsplit(".", 1)[-1]


def _py_ctor_name(ctor_full):
    """The Python dataclass name the transpiler emits for constructor
    `ctor_full` — mirrors `toPyTypeName`: bare short name, except a *common* name
    (`mk`, `node`, …) is prefixed with its immediate parent (`Corpus.Games.Nim.mk`
    -> `Nim_mk`) to avoid collisions.  The oracle's JSON `"c"` value and
    `run_oracle.normalize` (which reads `type(v).__name__`) must agree on this."""
    parts = ctor_full.split(".")
    s = parts[-1]
    if s in _COMMON_CTOR_NAMES and len(parts) >= 2:
        return f"{parts[-2]}_{s}"
    return s


def _rand_user_value(rng, ty):
    """A random value of constructible user type `ty`, as a dict
    `{"__ctor__": full_ctor_name, "fields": [values...]}`.  Field values are
    generated recursively (base types via `_rand_input`, user types via this)."""
    ctors = _load_type_info()[ty]
    ctor, fields = rng.choice(ctors)
    return {"__ctor__": ctor,
            "fields": [_rand_input(rng, f) for f in fields]}


def _user_lean_lit(ty, v):
    """Lean literal for a user-type value: `Corpus.Games.Card.mk (rank) (suit)`
    (fully-qualified constructor applied to its field literals)."""
    ctor = v["__ctor__"]
    field_types = dict(_load_type_info()[ty])[ctor]
    args = " ".join(f"({_lean_lit(ft, fv)})"
                    for ft, fv in zip(field_types, v["fields"]))
    return f"({ctor} {args})" if args else f"{ctor}"

# The types the fuzzer can generate values for (must match gen.LEAN_TYPES).  A
# def is harvestable iff every parameter type and the return type is one of these.
_HARVESTABLE = {"Nat", "Bool", "Int", "List Nat", "Option Nat", "Nat × Nat",
                "String", "Char", "Array Nat",
                "List Int", "List Bool", "List (List Nat)"}

# `(a b : T)` binds two params of type T; `(x : T)` binds one.  We only accept
# a param group whose type is harvestable.
_PARAM_RE = re.compile(r"\(([^():]+):\s*([^()]+?)\s*\)")
# Allow dotted def names (`Card.value`, `RPS.beats`) — struct/enum methods.
_DEFNAME_RE = re.compile(r"^def\s+([A-Za-z_][A-Za-z0-9_'.]*)\s")
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


def _harvestable_type(ty, ns_prefixes):
    """Resolve `ty` and return the resolved name if the fuzzer can generate values
    of it (base-harvestable OR a constructible user type), else None."""
    if ty in _HARVESTABLE:
        return ty
    resolved = _resolve_type(ty, ns_prefixes)
    if resolved in _HARVESTABLE or _is_constructible(resolved):
        return resolved
    return None


def _parse_sig(header, ns_prefixes=()):
    """Parse the parameter section of a def header into a flat list of (resolved)
    types, or return None if any param group's type isn't
    harvestable/constructible (or params use a shape we don't model, e.g.
    implicit `{α}` or typeclass `[...]`)."""
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
        resolved = _harvestable_type(ty, ns_prefixes)
        if resolved is None:
            return None
        ptypes.extend([resolved] * len(names))
    if header[pos:].strip():
        return None
    return ptypes


# Namespaces with KNOWN-OPEN transpiler bugs, excluded from harvesting so the
# sweep stays a clean regression signal.  Now EMPTY: every Phase-1 gap is fixed
# (F14 method fall-throughs, F15 getElem!, F16 missing builtins, F17
# helper-scoping/`_uniq_NNN`, F18 cross-function name collisions).  Every
# harvestable corpus function transpiles and agrees with the oracle, alone and
# batched.  Add a prefix back here only if a new bug is found and deferred.
_KNOWN_OPEN_NS = ()


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
                        header, ret_raw = parts
                        # Namespace prefixes for resolving short type names: the
                        # current `namespace` stack, plus a dotted def name's own
                        # prefix (e.g. `Card.value` sees the `Card`/`Games` scope).
                        ns_prefixes = _ns_prefixes(ns, name)
                        ret = _harvestable_type(_norm_type(ret_raw), ns_prefixes)
                        ptypes = _parse_sig(header, ns_prefixes) if ret else None
                        if ptypes:  # ≥1 binder param, all types harvestable
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
    if ty in gen.LEAN_TYPES:
        # Reuse gen.py's generators (a Gen wraps the same rng contract).
        g = gen.Gen.__new__(gen.Gen)
        g.rng = rng
        return g.rand_value(ty)
    # User inductive/structure type — build a constructor value.
    return _rand_user_value(rng, ty)


def _lean_lit(ty, v):
    """Lean literal for `v` of type `ty`, dispatching user types to
    `_user_lean_lit` and everything else to `gen.lean_lit`."""
    if ty in gen.LEAN_TYPES:
        return gen.lean_lit(ty, v)
    return _user_lean_lit(ty, v)


def _json(ty, v):
    """JSON string for `v` of type `ty` (the oracle-row `args`/expected value).
    User-type values serialize as `{"c":"<shortctor>","f":[<field json>...]}`,
    matching what the Lean serializer (`_user_serializer_name`) emits and what
    `run_oracle.normalize` reduces a transpiled dataclass instance to."""
    if ty in gen.LEAN_TYPES:
        return gen.json_lit(ty, v)
    import json
    ctor = v["__ctor__"]
    field_types = dict(_load_type_info()[ty])[ctor]
    fields = ",".join(_json(ft, fv) for ft, fv in zip(field_types, v["fields"]))
    return f'{{"c":{json.dumps(_py_ctor_name(ctor))},"f":[{fields}]}}'


def _user_serializer_name(ty):
    """Python-safe name for the Lean JSON serializer of user type `ty`
    (`Corpus.Games.Card` -> `jU_Corpus_Games_Card`)."""
    return "jU_" + ty.replace(".", "_")


def _serializer_call(ty, expr):
    """Lean serializer call for a value of type `ty` (dispatches user types to
    their emitted `jU_*` serializer)."""
    if ty in gen.LEAN_TYPES:
        return gen.serializer_call(ty, expr)
    return f"{_user_serializer_name(ty)} ({expr})"


def _field_serializer(ty):
    """The serializer *function name* to apply to a field of type `ty` inside a
    generated `jU_*` serializer.  Base types reuse gen.py's `jNat`/`jInt`/…;
    user types their own `jU_*`."""
    base = {gen.NAT: "jNat", gen.BOOL: "jBool", gen.INT: "jInt",
            gen.LISTNAT: "jListNat", gen.OPTNAT: "jOpt",
            gen.STRING: "jString", gen.CHAR: "jChar", gen.ARRAYNAT: "jArrayNat",
            gen.LISTINT: "jListInt", gen.LISTBOOL: "jListBool",
            gen.LISTLISTNAT: "jListListNat"}
    if ty in base:
        return base[ty]
    return _user_serializer_name(ty)


def _emit_user_serializers(types):
    """Emit Lean `jU_<Type>` JSON serializers for each user type in `types` (and
    their transitive user-type fields), topologically so a serializer is defined
    before one that calls it.  Each emits `{"c":"<ctor>","f":[...]}`."""
    info = _load_type_info()
    # Collect the transitive closure of user types referenced.
    needed, work = set(), list(types)
    while work:
        t = work.pop()
        if t in needed or t not in info:
            continue
        needed.add(t)
        for (_c, fields) in info[t]:
            for f in fields:
                if f in info and f not in needed:
                    work.append(f)
    # Order so dependencies come first (bounded passes; non-recursive by
    # construction, since only constructible — hence acyclic — types are used).
    ordered, emitted = [], set()
    for _ in range(len(needed) + 1):
        for t in sorted(needed):
            if t in emitted:
                continue
            deps = {f for (_c, fields) in info[t] for f in fields if f in info}
            if deps <= emitted:
                ordered.append(t)
                emitted.add(t)
    lines = []
    for t in ordered:
        arms = []
        for (ctor, fields) in info[t]:
            binders = " ".join(f"a{i}" for i in range(len(fields)))
            lean_c = _lean_ctor_short(ctor)   # Lean match arm: `.mk`
            py_c = _py_ctor_name(ctor)         # JSON "c" value: `Nim_mk`
            if fields:
                fjson = ' ++ "," ++ '.join(
                    f'{_field_serializer(ft)} a{i}' for i, ft in enumerate(fields))
                body = f'"{{\\"c\\":\\"{py_c}\\",\\"f\\":[" ++ {fjson} ++ "]}}"'
                arms.append(f"  | .{lean_c} {binders} => {body}")
            else:
                arms.append(f'  | .{lean_c} => "{{\\"c\\":\\"{py_c}\\",\\"f\\":[]}}"')
        lines.append(f"def {_user_serializer_name(t)} : {t} → String")
        lines.extend(arms)
    return "\n".join(lines)


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
    rows, used_types = [], set()
    for (qual, ptypes, ret) in chosen:
        for t in ptypes + [ret]:
            if t not in gen.LEAN_TYPES:
                used_types.add(t)
        for _ in range(ninputs):
            vals = [_rand_input(rng, t) for t in ptypes]
            lean_args = " ".join(f"({_lean_lit(t, v)})" for (t, v) in zip(ptypes, vals))
            json_args = "[" + ",".join(_json(t, v) for (t, v) in zip(ptypes, vals)) + "]"
            call = f"{qual} {lean_args}"
            ser = _serializer_call(ret, call)
            # Tag the ORACLE row with the qualified name so fuzz.py maps it back
            # to the transpiled `# Lean:` comment.  Escape json_args for embedding
            # in the Lean string literal (String/Char args carry quotes).
            rows.append(f'  IO.println ("ORACLE\\t{qual}\\t{gen._lean_str_escape(json_args)}\\t" ++ {ser})')

    parts = [CORPUS_PRELUDE, ""]
    if used_types:
        parts.append(_emit_user_serializers(used_types))
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
    used_types = {t for t in ptypes + [ret] if t not in gen.LEAN_TYPES}
    for vals in input_rows:
        lean_args = " ".join(f"({_lean_lit(t, v)})" for (t, v) in zip(ptypes, vals))
        json_args = "[" + ",".join(_json(t, v) for (t, v) in zip(ptypes, vals)) + "]"
        ser = _serializer_call(ret, f"{qual} {lean_args}")
        rows.append(f'  IO.println ("ORACLE\\t{qual}\\t{gen._lean_str_escape(json_args)}\\t" ++ {ser})')
    parts = [CORPUS_PRELUDE, ""]
    if used_types:
        parts.append(_emit_user_serializers(used_types))
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
