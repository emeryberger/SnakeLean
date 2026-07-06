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
import json
import os
import random
import re
import subprocess

import gen

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CORPUS_DIR = os.path.join(ROOT, "Corpus")

# On-disk cache of the `TypeInfo.lean` dump.  Loading type info requires a full
# Lean spawn (~5-8 s with the `import Corpus` olean load); with a large worker
# pool that is 100+ concurrent Lean spawns just to bootstrap.  We cache the parse
# to JSON, keyed by corpus freshness, so the parent computes it once and every
# worker reads the file instead of re-spawning Lean.  (See `_load_type_info`.)
_TYPEINFO_CACHE = os.path.join(HERE, ".typeinfo.json")


# ---------------------------------------------------------------------------
# Phase 3: custom inductive / structure types.
#
# A Lean-side dump (`fuzz/TypeInfo.lean`) reports each corpus type's
# constructors and their field types (robust to source formatting / Lean
# version, unlike a regex over source).  From it we compute which types are
# *constructible* from the fuzzer's value universe (all fields base-harvestable
# or themselves constructible user types), so we can generate values, emit them
# as Lean literals, and compare a transpiled dataclass instance against the Lean
# oracle.  This now covers enums, structs, container types over user elements,
# depth-bounded recursive types (Expr/Trie/JsonValue), AND Float-bearing types
# (Geometry's Point2D/3D) — Float is in the value universe (`gen.VALUE_TYPES`),
# serialized by exact IEEE-754 bits for the strict-equality oracle.
# ---------------------------------------------------------------------------

# type name -> list of (ctor_full_name, [field_type_str, ...]); loaded lazily.
_TYPE_INFO = None
# type name -> True/False constructibility (memoized during analysis).
_CONSTRUCTIBLE = {}


def _typeinfo_sources_mtime():
    """Newest mtime among the inputs that determine the type dump: every
    `Corpus/*.lean` plus `TypeInfo.lean` itself.  The cache is stale iff it
    predates this."""
    newest = os.path.getmtime(os.path.join(HERE, "TypeInfo.lean"))
    for fname in os.listdir(CORPUS_DIR):
        if fname.endswith(".lean"):
            newest = max(newest, os.path.getmtime(os.path.join(CORPUS_DIR, fname)))
    return newest


def _parse_type_info(stdout):
    """Parse `### TYPE` lines from a TypeInfo.lean run into
    {type: [(ctor, [fieldtypes])]}."""
    info = {}
    for line in stdout.splitlines():
        if not line.startswith("### TYPE\t"):
            continue
        _, tyname, ctors_str = line.split("\t", 2)
        ctors = []
        for cpart in ctors_str.split(" | "):
            cname, _, fields_str = cpart.partition(";")
            fields = [f for f in fields_str.split(",") if f]
            ctors.append((cname, fields))
        info[tyname] = ctors
    return info


def _run_type_info():
    """Spawn `lean fuzz/TypeInfo.lean` and parse its output.  This is the
    expensive path (a full Lean process + `import Corpus`); callers should prefer
    the cached `_load_type_info`."""
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
    return _parse_type_info(proc.stdout)


def build_type_info_cache():
    """Compute the type dump (spawning Lean once) and write it to
    `_TYPEINFO_CACHE`.  Call this ONCE in the parent before fanning out workers,
    so each worker reads the JSON instead of re-spawning Lean.  Returns the info
    dict (also priming this process's in-memory `_TYPE_INFO`)."""
    global _TYPE_INFO
    info = _run_type_info()
    tmp = _TYPEINFO_CACHE + ".tmp"
    with open(tmp, "w") as fh:
        json.dump({"mtime": _typeinfo_sources_mtime(), "info": info}, fh)
    os.replace(tmp, _TYPEINFO_CACHE)  # atomic; workers never see a half-written file
    _TYPE_INFO = info
    return info


def _load_type_info():
    """Return the corpus type dump ({type: [(ctor, [fieldtypes])]}), preferring
    the on-disk cache written by `build_type_info_cache` and falling back to a
    live Lean spawn if the cache is missing or stale.  Cached in-process after
    the first call."""
    global _TYPE_INFO
    if _TYPE_INFO is not None:
        return _TYPE_INFO
    try:
        with open(_TYPEINFO_CACHE) as fh:
            cached = json.load(fh)
        if cached.get("mtime", -1) >= _typeinfo_sources_mtime():
            # JSON turns field lists into lists; restore the (ctor, [fields])
            # tuple shape callers expect.
            _TYPE_INFO = {ty: [(c, list(f)) for (c, f) in ctors]
                          for ty, ctors in cached["info"].items()}
            return _TYPE_INFO
    except (OSError, ValueError, KeyError):
        pass  # missing / corrupt / stale → recompute
    _TYPE_INFO = _run_type_info()
    return _TYPE_INFO


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


# Types with internal INVARIANTS that arbitrary field-filling would violate,
# causing their functions to loop forever (e.g. UnionFind's parent array must be
# acyclic — a random `List Nat` can form a cycle, so `find` never terminates).
# The fuzzer can't safely construct these, so treat them as non-constructible.
# (A future improvement could generate only invariant-respecting values.)
_UNSAFE_TO_CONSTRUCT = ("UnionFind",)


# ---------------------------------------------------------------------------
# Type-string structure.  A field / signature type is one of: a base type in
# `gen.VALUE_TYPES` (drives gen.py's value/serializer machinery directly); a
# container `List T` / `Array T` / `Option T`; a binary product `T₁ × T₂`; or a
# (fully-qualified, in `_TYPE_INFO`) user type.  These small parsers decompose a
# type string so the value generator, Lean-literal emitter, JSON emitter, and
# serializer emitter can all recurse over the SAME structure — the single reason
# containers-over-user-types (`List Card`) and recursive types (`Expr`, `Trie`,
# `JsonValue`) become constructible.
# ---------------------------------------------------------------------------

def _strip_outer_parens(s):
    """Remove one fully-enclosing paren pair from `s` (e.g. `(Nat × Nat)` ->
    `Nat × Nat`); leave `s` alone if the leading `(` doesn't match the trailing
    `)` (e.g. `(Nat × Nat) × Bool`)."""
    s = s.strip()
    if not (s.startswith("(") and s.endswith(")")):
        return s
    depth = 0
    for i, c in enumerate(s):
        if c == "(":
            depth += 1
        elif c == ")":
            depth -= 1
            if depth == 0:
                return s[1:-1].strip() if i == len(s) - 1 else s
    return s


def _split_top_pair(s):
    """Index of the FIRST top-level `×` in `s` (outside any parens/brackets), or
    -1.  `×` is the lowest-precedence type operator, so a top-level `×` means the
    whole type is a product — checked BEFORE `List`/`Array`/`Option` prefixes so
    `List Nat × List Nat` parses as a product, not a `List (Nat × List Nat)`."""
    depth = 0
    for i, c in enumerate(s):
        if c in "([":
            depth += 1
        elif c in ")]":
            depth -= 1
        elif c == "×" and depth == 0:
            return i
    return -1


def _pair(s):
    """If `s` is a top-level binary product `T₁ × T₂`, return (T₁, T₂) (parens
    stripped); else None.  Splits at the first top-level `×` (products in the
    corpus are binary)."""
    s = _strip_outer_parens(s)
    i = _split_top_pair(s)
    if i < 0:
        return None
    return _strip_outer_parens(s[:i]), _strip_outer_parens(s[i + 1:])


def _container(s):
    """If `s` is `List T` / `Array T` / `Option T`, return (`List`/`Array`/
    `Option`, T); else None.  `T` is returned with any enclosing parens stripped
    so callers can recurse on it directly.  A top-level product (`… × …`) is NOT a
    container even when it starts with `List` (`List Nat × Bool`)."""
    s = _strip_outer_parens(s)
    if _split_top_pair(s) >= 0:
        return None
    for pfx in ("List", "Array", "Option"):
        if s.startswith(pfx + " "):
            return pfx, _strip_outer_parens(s[len(pfx) + 1:])
    return None


# Minimal term-depth: the height of the SMALLEST value of a type.  This is what
# makes depth-bounded generation of recursive types (`Expr`, `JsonValue`, `Trie`)
# terminate: with a remaining budget, we prefer constructors we can finish within
# it, but always fall back to a minimal-depth constructor when the budget runs
# out — so the tree can always be capped off with a base case (`Expr.num`,
# `JsonValue.null`, `Trie.node _ []`).  A user type with NO finite value (no base
# case) has infinite min-depth and is therefore not constructible.
#
# Conventions: base types and (force-emptyable) containers/options have depth 0;
# a product is the max of its components; a user constructor is 1 + the max of its
# field depths (nullary → 1); a user type is the min over its constructors.
_MIN_DEPTH = None
_INF = float("inf")


def _md_field(ty, md):
    """Minimal depth to construct a value of field type `ty`, given the per-user-
    type map `md`.  Containers/options are 0 (empty/none); products max their
    components; bare user types read `md` (default ∞ until computed)."""
    ty = ty.strip()
    if ty in gen.VALUE_TYPES or ty in _HARVESTABLE:
        return 0
    if _container(ty):
        return 0               # empty list / `none` — a finite value at any budget
    p = _pair(ty)
    if p:
        return max(_md_field(p[0], md), _md_field(p[1], md))
    return md.get(ty, _INF)


def _md_ctor(fields, md):
    """Minimal depth of a value built with constructor `fields`: 1 + max field
    depth (a nullary constructor is depth 1)."""
    return 1 + (max((_md_field(f, md) for f in fields), default=0))


def _min_depths():
    """Fixpoint map {user_type: minimal term-depth} (∞ if it has no finite value)."""
    global _MIN_DEPTH
    if _MIN_DEPTH is not None:
        return _MIN_DEPTH
    info = _load_type_info()
    md = {ty: _INF for ty in info}
    changed = True
    while changed:
        changed = False
        for ty, ctors in info.items():
            best = min((_md_ctor(fields, md) for (_c, fields) in ctors),
                       default=_INF)
            if best < md[ty]:
                md[ty] = best
                changed = True
    _MIN_DEPTH = md
    return md


def _is_constructible(ty, stack=()):
    """Can the fuzzer build a value of Lean type `ty`?  True for base types,
    containers/products over constructible element types, and user types that
    (a) have a finite value (finite minimal term-depth — a base case) and
    (b) have every constructor field constructible.  A field that refers back to
    a type already on `stack` is allowed — recursion is handled by the depth-
    bounded generator — so recursive types (`Expr`, `Trie`, `JsonValue`) are now
    constructible, unlike before."""
    ty = ty.strip()
    if ty in _HARVESTABLE or ty in gen.VALUE_TYPES:
        return True
    c = _container(ty)
    if c:
        return _is_constructible(c[1], stack)
    p = _pair(ty)
    if p:
        return all(_is_constructible(x, stack) for x in p)
    info = _load_type_info()
    if ty not in info:
        return False           # unknown / Float / function type
    if any(ty.endswith(u) for u in _UNSAFE_TO_CONSTRUCT):
        return False
    if ty in stack:            # recursive back-reference — the depth bound covers it
        return True
    if ty in _CONSTRUCTIBLE:
        return _CONSTRUCTIBLE[ty]
    ok = (_min_depths().get(ty, _INF) != _INF and
          all(all(_is_constructible(f, stack + (ty,)) for f in fields)
              for (_ctor, fields) in info[ty]))
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


def _rand_user_value(rng, ty, depth):
    """A random value of constructible user type `ty` at recursion budget `depth`,
    as a dict `{"__ctor__": full_ctor_name, "fields": [values...]}`.

    Termination: choose only among constructors *affordable* within `depth`
    (minimal term-depth ≤ depth+1); if the budget is too small for any, fall back
    to the minimal-depth constructor(s) so the tree is always capped by a base
    case (`Expr.num`, `JsonValue.null`, `Trie.node _ []`).  Fields recurse with
    `depth-1`, and container fields are forced empty at depth ≤ 0 in
    `_rand_input`, so recursion always bottoms out."""
    md = _min_depths()
    ctors = _load_type_info()[ty]
    affordable = [(c, f) for (c, f) in ctors if _md_ctor(f, md) <= depth + 1]
    if not affordable:
        best = min(_md_ctor(f, md) for (_c, f) in ctors)
        affordable = [(c, f) for (c, f) in ctors if _md_ctor(f, md) == best]
    ctor, fields = rng.choice(affordable)
    return {"__ctor__": ctor,
            "fields": [_rand_input(rng, f, depth - 1) for f in fields]}


def _user_lean_lit(ty, v):
    """Lean literal for a user-type value: `Corpus.Games.Card.mk (rank) (suit)`
    (fully-qualified constructor applied to its field literals)."""
    ctor = v["__ctor__"]
    field_types = dict(_load_type_info()[ty])[ctor]
    args = " ".join(f"({_lean_lit(ft, fv)})"
                    for ft, fv in zip(field_types, v["fields"]))
    return f"({ctor} {args})" if args else f"{ctor}"

# The types the fuzzer can generate values for (must match gen.VALUE_TYPES).  A
# def is harvestable iff every parameter type and the return type is one of these.
_HARVESTABLE = {"Nat", "Bool", "Int", "List Nat", "Option Nat", "Nat × Nat",
                "String", "Char", "Array Nat",
                "List Int", "List Bool", "List (List Nat)", "Float"}

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
# sweep stays a clean regression signal.  Phase-1 gaps are all fixed (F14 method
# fall-throughs, F15 getElem!, F16 missing builtins, F17 helper-scoping/`_uniq`,
# F18 cross-function name collisions), as are the recursive/container-type gaps
# (loop-mode `find?` predicate, Option.isSome/map point-free, List.setTR/zip,
# point-free user fns, nullary-const call, transitive loop recursion).
_KNOWN_OPEN_NS = ()

# Individual functions with a KNOWN, DEFERRED transpiler limitation, excluded by
# exact qualified name (a signature-level exclusion can't reach them — the issue
# is in the body, not the types).
#   * TicTacToe.validMoves indexes a `List (Option Player)` with `[i]?` and
#     matches `some none`.  Python models `Option` as `None`, so the outer
#     `some none` (empty cell) and the out-of-bounds `none` COLLAPSE to the same
#     `None` — the classic nested-Option faithfulness gap.  A faithful fix needs
#     a sentinel-based Option representation (a large redesign); deferred.  See
#     CLAUDE.md "Known Limitations".
_KNOWN_OPEN_FNS = ("Corpus.Games.TicTacToe.validMoves",)


def _is_known_open(qual):
    return (any(qual.startswith(ns) for ns in _KNOWN_OPEN_NS)
            or qual in _KNOWN_OPEN_FNS)


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


# Depth budget for recursive user-type generation (Expr/JsonValue/Trie): the
# maximum constructor nesting.  Small — the transpiler bugs live in the recursive
# `match` structure, which even depth 1-2 exercises, and deep trees blow up the
# oracle `#eval` cost.  Container elements at the top level also draw from this.
_MAX_DEPTH = 3
# Element count for containers OVER USER TYPES (`List Card`, `List JsonValue`).
# Kept tiny so recursive element trees don't explode.
_MAX_USER_LIST = 3


def _rand_input(rng, ty, depth=_MAX_DEPTH):
    ty = ty.strip()
    if ty == gen.NAT:
        return rng.randint(0, _MAX_NAT)
    if ty == gen.PAIR:
        return [rng.randint(0, _MAX_NAT), rng.randint(0, _MAX_NAT)]
    if ty in gen.VALUE_TYPES:
        # Reuse gen.py's generators (a Gen wraps the same rng contract).
        g = gen.Gen.__new__(gen.Gen)
        g.rng = rng
        return g.rand_value(ty)
    # Compound types INVOLVING USER TYPES (base compounds are handled above).
    c = _container(ty)
    if c:
        kind, elem = c
        if kind == "Option":
            return None if rng.random() < 0.3 else _rand_input(rng, elem, depth)
        # List/Array: force empty at depth 0 so recursive elements terminate.
        n = 0 if depth <= 0 else rng.randint(0, _MAX_USER_LIST)
        return [_rand_input(rng, elem, depth - 1) for _ in range(n)]
    p = _pair(ty)
    if p:
        return [_rand_input(rng, p[0], depth), _rand_input(rng, p[1], depth)]
    # User inductive/structure type — build a (depth-bounded) constructor value.
    return _rand_user_value(rng, ty, depth)


def _lean_lit(ty, v):
    """Lean literal for `v` of type `ty`, dispatching base types to
    `gen.lean_lit`, compound-with-user types (containers / products) structurally,
    and user types to `_user_lean_lit`."""
    ty = ty.strip()
    if ty in gen.VALUE_TYPES:
        return gen.lean_lit(ty, v)
    c = _container(ty)
    if c:
        kind, elem = c
        if kind == "Option":
            if v is None:
                return f"(none : {ty})"
            return f"(some ({_lean_lit(elem, v)}) : {ty})"
        # List / Array: annotate so an empty (or user-element) literal type-checks.
        open_, close_ = ("#[", "]") if kind == "Array" else ("[", "]")
        items = ", ".join(_lean_lit(elem, x) for x in v)
        return f"({open_}{items}{close_} : {ty})"
    p = _pair(ty)
    if p:
        return f"({_lean_lit(p[0], v[0])}, {_lean_lit(p[1], v[1])})"
    return _user_lean_lit(ty, v)


def _json(ty, v):
    """JSON string for `v` of type `ty` (the oracle-row `args`/expected value).
    Must byte-match what the Lean serializer (`_field_serializer` chain) emits and
    what `run_oracle.materialize`/`normalize` expect: base types as plain JSON,
    containers as JSON arrays (`Option` as value-or-null), products as 2-element
    arrays, user-type values as `{"c":"<pyctor>","f":[<field json>...]}`."""
    ty = ty.strip()
    if ty in gen.VALUE_TYPES:
        return gen.json_lit(ty, v)
    c = _container(ty)
    if c:
        kind, elem = c
        if kind == "Option":
            return "null" if v is None else _json(elem, v)
        return "[" + ",".join(_json(elem, x) for x in v) + "]"
    p = _pair(ty)
    if p:
        return "[" + _json(p[0], v[0]) + "," + _json(p[1], v[1]) + "]"
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
    """Lean serializer call for a RETURN value of type `ty`.  Base types use
    gen.py's serializers; everything else (containers / products / user types,
    incl. compounds like `Option (List Nat)` or `List Card`) reuses the inline
    structural serializer so no per-shape named helper is needed."""
    ty = ty.strip()
    if ty in gen.VALUE_TYPES:
        return gen.serializer_call(ty, expr)
    return _field_serializer_expr(ty, f"({expr})")


_BASE_SERIALIZER = {gen.NAT: "jNat", gen.BOOL: "jBool", gen.INT: "jInt",
                    gen.LISTNAT: "jListNat", gen.OPTNAT: "jOpt",
                    gen.STRING: "jString", gen.CHAR: "jChar",
                    gen.ARRAYNAT: "jArrayNat", gen.LISTINT: "jListInt",
                    gen.LISTBOOL: "jListBool", gen.LISTLISTNAT: "jListListNat",
                    gen.PAIR: "jPair", gen.FLOAT: "jFloat"}


def _field_serializer_expr(ty, var, depth=0):
    """A Lean expression (a String) that serializes `var : ty` to the SAME JSON
    shape `_json` produces.  Base types call gen.py's `jNat`/`jListNat`/…; bare
    user types their emitted `jU_*`; containers/products serialize inline (a
    `.map` for List/Array, a `match` for Option/product) so a field like
    `List (Char × Trie)` needs no named helper.  `depth` freshens bound names to
    avoid shadowing in nested lambdas/matches.  Bound names use a `fx`/`fp`/`fq`
    prefix so they can never collide with a constructor arm's `a0`,`a1`,… binders
    (the field serializer is spliced into a `| .ctor a0 a1 => …` arm)."""
    ty = ty.strip()
    if ty in _BASE_SERIALIZER:
        return f"({_BASE_SERIALIZER[ty]} {var})"
    c = _container(ty)
    if c:
        kind, elem = c
        x = f"fx{depth}"
        ser_x = _field_serializer_expr(elem, x, depth + 1)
        if kind == "Option":
            return (f'(match {var} with | none => "null" '
                    f"| some {x} => {ser_x})")
        seq = f"({var}).toList" if kind == "Array" else f"({var})"
        return (f'("[" ++ String.intercalate "," '
                f"({seq}.map (fun {x} => {ser_x})) ++ \"]\")")
    p = _pair(ty)
    if p:
        a, b = f"fp{depth}", f"fq{depth}"
        return (f"(match {var} with | ({a}, {b}) => "
                f'"[" ++ {_field_serializer_expr(p[0], a, depth + 1)} ++ "," '
                f"++ {_field_serializer_expr(p[1], b, depth + 1)} ++ \"]\")")
    return f"({_user_serializer_name(ty)} {var})"


def _referenced_user_types(ty, acc):
    """Add to `acc` every user type reachable from type string `ty` (through
    containers and products, not just bare positions)."""
    ty = ty.strip()
    if ty in gen.VALUE_TYPES:
        return
    c = _container(ty)
    if c:
        return _referenced_user_types(c[1], acc)
    p = _pair(ty)
    if p:
        _referenced_user_types(p[0], acc)
        _referenced_user_types(p[1], acc)
        return
    if ty in _load_type_info():
        acc.add(ty)


def _is_recursive_type(ty):
    """Does `ty` reach itself through some constructor field (directly or via a
    container/product)?  Such serializers must be emitted `partial def`."""
    info = _load_type_info()
    seen, work = set(), [ty]
    first = True
    while work:
        t = work.pop()
        if not first and t == ty:
            return True
        first = False
        if t in seen:
            continue
        seen.add(t)
        for (_c, fields) in info.get(t, []):
            for f in fields:
                refs = set()
                _referenced_user_types(f, refs)
                work.extend(refs)
    return False


def _emit_user_serializers(types):
    """Emit Lean `jU_<Type>` JSON serializers for each user type in `types` (and
    their transitive user-type fields, reached through containers/products too),
    topologically so a serializer is defined before one that calls it.  Recursive
    types are emitted as one `mutual … end` block of `partial def`s (order within
    a `mutual` block doesn't matter, sidestepping the self-dependency the topo
    sort can't order).  Each emits `{"c":"<ctor>","f":[...]}`."""
    info = _load_type_info()
    # Transitive closure of referenced user types (through containers/products).
    needed, work = set(), list(types)
    while work:
        t = work.pop()
        if t in needed or t not in info:
            continue
        needed.add(t)
        for (_c, fields) in info[t]:
            for f in fields:
                refs = set()
                _referenced_user_types(f, refs)
                work.extend(refs - needed)

    def serializer_def(t, keyword):
        """The `<keyword> jU_T : T → String` lines for type `t`."""
        out = [f"{keyword} {_user_serializer_name(t)} : {t} → String"]
        for (ctor, fields) in info[t]:
            binders = " ".join(f"a{i}" for i in range(len(fields)))
            lean_c = _lean_ctor_short(ctor)
            py_c = _py_ctor_name(ctor)
            if fields:
                fjson = ' ++ "," ++ '.join(
                    _field_serializer_expr(ft, f"a{i}") for i, ft in enumerate(fields))
                body = f'"{{\\"c\\":\\"{py_c}\\",\\"f\\":[" ++ {fjson} ++ "]}}"'
                out.append(f"  | .{lean_c} {binders} => {body}")
            else:
                out.append(f'  | .{lean_c} => "{{\\"c\\":\\"{py_c}\\",\\"f\\":[]}}"')
        return out

    recursive = {t for t in needed if _is_recursive_type(t)}
    lines = []
    # Non-recursive types first, in dependency order (acyclic by construction).
    nonrec = needed - recursive
    ordered, emitted = [], set()
    for _ in range(len(nonrec) + 1):
        for t in sorted(nonrec):
            if t in emitted:
                continue
            deps = set()
            for (_c, fields) in info[t]:
                for f in fields:
                    _referenced_user_types(f, deps)
            if (deps - {t}) <= emitted:
                ordered.append(t)
                emitted.add(t)
    for t in ordered:
        lines += serializer_def(t, "def")
    # Recursive types together in one `mutual` block of `partial def`s.
    if recursive:
        lines.append("mutual")
        for t in sorted(recursive):
            lines += serializer_def(t, "partial def")
        lines.append("end")
    return "\n".join(lines)


def _corpus_block(seed, nfuncs, ninputs, funcs, tag=""):
    """Build one seed's `#eval` block (transpile its chosen functions, then emit
    ORACLE rows over `ninputs` random inputs each).  `tag` (a seed id) is appended
    to the `### PYTHON`/`### ORACLE` banners so a batched file's output splits back
    apart per seed.  Returns (block_lines, chosen_qualified_names, used_types).

    The rng is seeded from `seed` alone and consumed in a fixed order (selection,
    then inputs per function), so a seed's rows are identical whether emitted
    standalone or inside a batch — the property the shrinker relies on."""
    rng = random.Random(seed)
    chosen = funcs if nfuncs >= len(funcs) else rng.sample(funcs, nfuncs)
    names = ", ".join("`" + q for (q, _, _) in chosen)
    rows, used_types = [], set()
    for (qual, ptypes, ret) in chosen:
        for t in ptypes + [ret]:
            if t not in gen.VALUE_TYPES:
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
    suffix = f" {tag}" if tag != "" else ""
    block = ["#eval show CoreM Unit from do",
             f'  IO.println "### PYTHON{suffix}"',
             f"  IO.println (← emitPythonForNames `Fuzz [{names}])",
             f'  IO.println "### ORACLE{suffix}"']
    block += rows
    return block, [q for (q, _, _) in chosen], used_types


def emit_corpus_file(seed, nfuncs, ninputs, funcs=None):
    """Emit a Lean file that transpiles `nfuncs` harvested corpus functions and
    prints oracle rows for `ninputs` random inputs each.

    Pure function of `(seed, nfuncs, ninputs)` given a fixed corpus, so a failing
    seed reproduces exactly (the harvest order is deterministic).  Returns
    (lean_src, [chosen_qualified_names])."""
    funcs = funcs if funcs is not None else harvest()
    block, chosen, used_types = _corpus_block(seed, nfuncs, ninputs, funcs)
    parts = [CORPUS_PRELUDE, ""]
    if used_types:
        parts.append(_emit_user_serializers(used_types))
    parts += block
    return "\n".join(parts) + "\n", chosen


def emit_corpus_batch_file(seeds, nfuncs, ninputs, funcs=None):
    """Pack several corpus seeds into ONE Lean file, amortizing Lean's startup +
    `import Corpus` olean load (which dominate per-seed runtime, NOT the
    transpilation) across many functions — the same ~5x win `--batch` gives
    grammar mode.

    Each seed gets its OWN `#eval` block (banners tagged with the seed id): a
    non-terminating or otherwise failing oracle row aborts only that seed's block,
    and the user-type JSON serializers are emitted ONCE (as the union over all
    seeds' used types) since they are top-level defs shared across blocks.

    Returns (lean_src, {seed: [chosen_qualified_names]})."""
    funcs = funcs if funcs is not None else harvest()
    blocks, chosen_by_seed, used_types = [], {}, set()
    for seed in seeds:
        block, chosen, used = _corpus_block(seed, nfuncs, ninputs, funcs, tag=str(seed))
        blocks += block
        chosen_by_seed[seed] = chosen
        used_types |= used
    parts = [CORPUS_PRELUDE, ""]
    if used_types:
        parts.append(_emit_user_serializers(used_types))
    parts += blocks
    return "\n".join(parts) + "\n", chosen_by_seed


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
    used_types = {t for t in ptypes + [ret] if t not in gen.VALUE_TYPES}
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
