#!/usr/bin/env python3
"""Input-adequacy coverage of the TRANSPILED Python during oracle execution.

The transpiler is written in Lean, so Python coverage tools can't measure *it*.
The useful target (per PLAN.md task 5) is coverage of the *transpiled code* while
the oracle rows drive it: if some branch of a transpiled function never executes
under any oracle input, a transpiler bug in that branch is invisible to
differential testing.  This module measures which lines of each transpiled
function the oracle inputs actually exercised, so "are these inputs adequate?"
becomes a number.

Two coverage backends, selected at runtime:

- **SlipCover** (preferred, when importable) — instruments the compiled code
  object directly (`Slipcover.instrument(compile(...))`), so it works on the
  `exec`'d transpiled string without an imported file.  It counts executable
  lines at the bytecode level, so it correctly excludes non-tracing header lines
  like a bare `else:` (no manual heuristic needed), and on Python 3.12+ (with the
  `slipcover.branch.preinstrument` AST pass) it additionally records real
  **branch** coverage — a stronger adequacy signal than lines alone.
- **`sys.settrace`** (fallback) — a zero-dependency line tracer scoped to the
  `<transpiled>` filename.  Used when SlipCover isn't installed (e.g. cloudnew's
  Python 3.11 environment) so the fuzzer always runs.  Line coverage only; a
  small heuristic drops bare `else:`/`try:`/`finally:` headers that never fire a
  line event, matching SlipCover's line denominator.
"""
import sys

try:
    import slipcover as _slipcover
    import ast as _ast
    _HAVE_SLIPCOVER = True
except ImportError:  # cloudnew py3.11 has no slipcover — fall back to settrace
    _slipcover = None
    _HAVE_SLIPCOVER = False


def have_slipcover():
    """Whether the SlipCover backend is available in this interpreter."""
    return _HAVE_SLIPCOVER


def executable_lines(py_src, func_lines):
    """Best-effort set of *executable* line numbers inside each function body,
    keyed by the Python function name.  `func_lines` maps func name -> (start,
    end) 1-based line span.  We count any non-blank, non-comment, non-`def`
    header line as executable — an over-approximation that's fine for an
    adequacy ratio (blank/comment lines never trace, so including only real
    statements keeps the denominator meaningful).

    Exception: a *bare* compound-statement header (`else:`, `try:`, `finally:`,
    `elif …:` with nothing after the colon) never produces its own `line` trace
    event — control jumps straight to the first statement in the block — so
    counting it would make 100% coverage unreachable and inflate the denominator.
    We exclude those (their body statements are still counted)."""
    # Openers whose bare header line the tracer skips (no line event fires on it).
    _untraced = ("else:", "try:", "finally:")
    lines = py_src.splitlines()
    out = {}
    for fn, (start, end) in func_lines.items():
        execs = set()
        for ln in range(start, min(end, len(lines)) + 1):
            text = lines[ln - 1].strip()
            if not text or text.startswith("#"):
                continue
            if text in _untraced:
                continue
            execs.add(ln)
        out[fn] = execs
    return out


def function_spans(py_src):
    """Map each top-level `def name(` to its (start, end) 1-based line span (end
    = last line before the next top-level def / EOF)."""
    import re
    lines = py_src.splitlines()
    defs = []
    for i, line in enumerate(lines):
        m = re.match(r"def (\w+)\(", line)
        if m:
            defs.append((m.group(1), i + 1))
    spans = {}
    for j, (name, start) in enumerate(defs):
        end = (defs[j + 1][1] - 1) if j + 1 < len(defs) else len(lines)
        spans[name] = (start, end)
    return spans


class LineTracer:
    """Records the set of line numbers executed under `<transpiled>` while it is
    installed as the trace function.  Scoped to our synthetic filename so it
    ignores the fuzzer's own frames."""

    def __init__(self, filename="<transpiled>"):
        self.filename = filename
        self.hit = set()

    def __call__(self, frame, event, arg):
        if frame.f_code.co_filename != self.filename:
            return None  # don't trace into other files
        if event == "line":
            self.hit.add(frame.f_lineno)
        return self

    def __enter__(self):
        self._prev = sys.gettrace()
        sys.settrace(self)
        return self

    def __exit__(self, *exc):
        sys.settrace(self._prev)
        return False


# Execution-PATH coverage needs the ORDERED sequence of executed lines per call,
# which SlipCover can't give (its callback returns `sys.monitoring.DISABLE`, so a
# line fires at most once ever).  We instead use `sys.monitoring` (PEP 669, 3.12+)
# with a LINE callback that does NOT disable, recording every line event in
# order.  From that sequence we derive bounded k-line subpaths (windows of k
# consecutive executed lines) as the coverage unit — an execution-order analogue
# of the grammar k-path metric (gen.Gen.KMAX).
_HAVE_MONITORING = (sys.version_info[:2] >= (3, 12)
                    and hasattr(sys, "monitoring"))
# Tool id 3 is a free slot (0=debugger, 1=coverage/SlipCover, 2=profiler).
_MON_TOOL_ID = 3
# Bound on subpath length — matches gen.Gen.KMAX so the two k-path metrics align.
PATH_K = 2


class PathTracer:
    """Records the ordered line sequence executed under `<transpiled>` via
    `sys.monitoring`, and exposes the set of k-line subpaths hit.  Each subpath is
    a tuple of `PATH_K` consecutive executed line numbers within one call.  Only
    available on Python 3.12+ (`_HAVE_MONITORING`)."""

    def __init__(self, filename="<transpiled>", k=PATH_K):
        self.filename = filename
        self.k = k
        self._seq = []          # ordered lines of the current call
        self.subpaths = set()   # accumulated k-line subpaths across calls

    def _on_line(self, code, lineno):
        if code.co_filename == self.filename:
            self._seq.append(lineno)
        # deliberately return None (not DISABLE) so every line event fires

    def begin_call(self):
        self._seq = []

    def end_call(self):
        seq = self._seq
        for i in range(len(seq) - self.k + 1):
            self.subpaths.add(tuple(seq[i:i + self.k]))

    def __enter__(self):
        mon = sys.monitoring
        if mon.get_tool(_MON_TOOL_ID) is None:
            mon.use_tool_id(_MON_TOOL_ID, "pathcov")
        self._prev_cb = mon.register_callback(
            _MON_TOOL_ID, mon.events.LINE, self._on_line)
        mon.set_events(_MON_TOOL_ID, mon.events.LINE)
        return self

    def __exit__(self, *exc):
        mon = sys.monitoring
        mon.set_events(_MON_TOOL_ID, 0)
        mon.register_callback(_MON_TOOL_ID, mon.events.LINE, self._prev_cb)
        mon.free_tool_id(_MON_TOOL_ID)
        return False


# SlipCover records real branch coverage only via an AST pre-pass, and its
# branch encoding is 3.12+ only (older Python uses a weaker scheme that yields no
# branch data on an exec'd code object).  So branch mode = SlipCover on 3.12+.
_HAVE_BRANCH = _HAVE_SLIPCOVER and sys.version_info[:2] >= (3, 12)


def have_branch_coverage():
    """Whether real branch coverage is available (SlipCover on Python 3.12+)."""
    return _HAVE_BRANCH


def have_path_coverage():
    """Whether execution-path (k-line-subpath) coverage is available
    (`sys.monitoring`, Python 3.12+)."""
    return _HAVE_MONITORING


class Harness:
    """A compiled, coverage-instrumented copy of the transpiled module.  `ns` is
    the exec'd namespace (look up transpiled functions there); `trace_call` runs
    one call and returns the coverage units it hit.

    Coverage unit, by mode (each a stronger adequacy signal than the last):
    - `paths=True` (`sys.monitoring`, 3.12+): k-line SUBPATHS — tuples of
      consecutive executed lines — steering the search toward uncovered branch
      *combinations*, not just individual edges.
    - `branch=True` (SlipCover, 3.12+): branch edges `(from_line, to_line)`.
    - otherwise: executed lines (SlipCover if present, else `sys.settrace`).
    A requested mode silently degrades if unavailable on this interpreter."""

    FILENAME = "<transpiled>"

    def __init__(self, py_src, branch=False, paths=False):
        self.py_src = py_src
        self.ns = {}
        self._sci = None
        self.paths = paths and _HAVE_MONITORING
        # Path mode observes the plain code object via sys.monitoring — no
        # SlipCover instrumentation needed (and mixing the two tool ids is
        # avoided).  Branch/line modes use SlipCover when available.
        self.branch = branch and _HAVE_BRANCH and not self.paths
        if self.paths:
            exec(compile(py_src, self.FILENAME, "exec"), self.ns)
        elif _HAVE_SLIPCOVER:
            self._sci = _slipcover.Slipcover(branch=self.branch)
            tree = _ast.parse(py_src)
            if self.branch:
                # Insert branch-tracking markers before compiling (3.12+ path).
                tree = _slipcover.branch.preinstrument(tree)
            code = self._sci.instrument(compile(tree, self.FILENAME, "exec"))
            exec(code, self.ns)
        else:
            exec(compile(py_src, self.FILENAME, "exec"), self.ns)

    def _slipcover_units(self):
        """Cumulative covered units (branches if `self.branch`, else lines) of
        `<transpiled>` from the SlipCover run so far."""
        cov = self._sci.get_coverage()["files"].get(self.FILENAME, {})
        if self.branch:
            return {tuple(b) for b in cov.get("executed_branches", [])}
        return set(cov.get("executed_lines", []))

    def _materialize(self, v):
        """Turn a custom-inductive dict arg `{"c":cls,"f":[...]}` into the
        transpiled `@dataclass` instance from `self.ns` (the coverage-guided
        search generates user-typed args as such dicts; the function needs the
        real instance).  Mirrors `run_oracle.materialize`."""
        if isinstance(v, dict) and "c" in v and "f" in v:
            cls = self.ns.get(v["c"])
            fields = [self._materialize(f) for f in v["f"]]
            return cls(*fields) if cls is not None else v
        if isinstance(v, list):
            return [self._materialize(x) for x in v]
        return v

    def trace_call(self, fn, args):
        """Run `fn(*args)` and return the frozenset of coverage units it hit
        (k-line subpaths in path mode, branches in branch mode, else lines).
        Swallows exceptions — a crashing input still covered the units it reached
        before raising, which is what a coverage-guided search wants to keep."""
        args = [self._materialize(a) for a in args]
        if self.paths:
            tracer = PathTracer(self.FILENAME)
            with tracer:
                tracer.begin_call()
                try:
                    fn(*args)
                except Exception:  # noqa: BLE001
                    pass
                tracer.end_call()
            return frozenset(tracer.subpaths)
        if self._sci is not None:
            before = self._slipcover_units()
            try:
                fn(*args)
            except Exception:  # noqa: BLE001
                pass
            return frozenset(self._slipcover_units() - before)
        tracer = LineTracer(self.FILENAME)
        with tracer:
            try:
                fn(*args)
            except Exception:  # noqa: BLE001
                pass
        return frozenset(tracer.hit)

    def body_lines(self, fn):
        """Executable body line numbers of transpiled function `fn` (excluding its
        `def` header), or an empty set if `fn` isn't present.  With SlipCover we
        use its bytecode-level executable-line set (intersected with the function
        span); otherwise the source heuristic in `executable_lines`."""
        spans = function_spans(self.py_src)
        if fn not in spans:
            return set()
        start, end = spans[fn]
        if self._sci is not None:
            allexec = _slipcover_executable_lines(self._sci, self.FILENAME)
            return {ln for ln in allexec if start < ln <= end}
        return {ln for ln in executable_lines(self.py_src, spans)[fn] if ln != start}

    def body_units(self, fn):
        """The full set of *reachable* coverage units for transpiled function
        `fn` — its branches `(from_line, to_line)` when in branch mode (executed ∪
        missing, so the denominator is known up front), else its body lines.  This
        is what a coverage-guided search aims to cover completely.

        Excludes provably-unreachable `match … → EXIT` fall-through edges: the
        transpiler emits `match` only on irrefutable tuple patterns (`case (a,
        b):` destructuring a Prod), which can never fail, so SlipCover's
        conservative match-failure edge is dead code the search could never
        cover.  Counting it would peg such functions below 100% forever."""
        # Path mode: the k-line-subpath universe is combinatorial and only
        # discovered by running (like the grammar k-path metric), so there is no
        # up-front denominator — return empty to signal an OPEN-ENDED search.
        if self.paths:
            return set()
        spans = function_spans(self.py_src)
        if fn not in spans:
            return set()
        start, end = spans[fn]
        if self.branch:
            cov = self._sci.get_coverage()["files"].get(self.FILENAME, {})
            allbr = {tuple(b) for b in cov.get("executed_branches", [])} \
                | {tuple(b) for b in cov.get("missing_branches", [])}
            srclines = self.py_src.splitlines()
            def reachable(b):
                frm, to = b
                if not (start < frm <= end):
                    return False
                # match-to-EXIT on an irrefutable tuple pattern is unreachable.
                if to == 0 and srclines[frm - 1].strip().startswith("match "):
                    return False
                return True
            return {b for b in allbr if reachable(b)}
        return self.body_lines(fn)


def _slipcover_executable_lines(sci, filename):
    """All executable line numbers SlipCover identified for `filename` (executed
    ∪ missing) — the honest denominator, computed at the bytecode level (so bare
    `else:`/`try:` headers are already excluded)."""
    cov = sci.get_coverage()["files"].get(filename, {})
    return set(cov.get("executed_lines", [])) | set(cov.get("missing_lines", []))


def measure(py_src, run_calls):
    """Exec `py_src` (instrumented), invoke `run_calls(ns)` to drive it, and
    return {func_name: (hit_lines, executable_lines)} per transpiled function.

    `run_calls` should call every transpiled function on every oracle input."""
    h = Harness(py_src)  # line mode (branch=False): the adequacy report is line-based
    spans = function_spans(py_src)
    if h._sci is not None:
        before = h._slipcover_units()
        run_calls(h.ns)
        hits = h._slipcover_units() - before
        allexec = _slipcover_executable_lines(h._sci, Harness.FILENAME)
        result = {}
        for fn, (start, end) in spans.items():
            body = {ln for ln in allexec if start < ln <= end}
            result[fn] = (hits & body, body)
        return result
    # settrace fallback.
    tracer = LineTracer(Harness.FILENAME)
    with tracer:
        run_calls(h.ns)
    execs = executable_lines(py_src, spans)
    result = {}
    for fn, ex in execs.items():
        start, _end = spans[fn]
        body = {ln for ln in ex if ln != start}
        result[fn] = (tracer.hit & body, body)
    return result
