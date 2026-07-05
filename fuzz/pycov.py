#!/usr/bin/env python3
"""Input-adequacy coverage of the TRANSPILED Python during oracle execution.

The transpiler is written in Lean, so Python coverage tools can't measure *it*.
The useful target (per PLAN.md task 5) is coverage of the *transpiled code* while
the oracle rows drive it: if some branch of a transpiled function never executes
under any oracle input, a transpiler bug in that branch is invisible to
differential testing.  This module measures which lines of each transpiled
function the oracle inputs actually exercised, so "are these inputs adequate?"
becomes a number.

Why `sys.settrace` and not SlipCover / `sys.monitoring`: the transpiled code is
`exec`'d from a string (not an imported file), and the fuzzer must run on
cloudnew's Python 3.11, where `sys.monitoring` (PEP 669, 3.12+) is unavailable.
`sys.settrace` line events are portable to every supported version and are
sufficient for line/branch-body adequacy.
"""
import sys


def executable_lines(py_src, func_lines):
    """Best-effort set of *executable* line numbers inside each function body,
    keyed by the Python function name.  `func_lines` maps func name -> (start,
    end) 1-based line span.  We count any non-blank, non-comment, non-`def`
    header line as executable — an over-approximation that's fine for an
    adequacy ratio (blank/comment lines never trace, so including only real
    statements keeps the denominator meaningful)."""
    lines = py_src.splitlines()
    out = {}
    for fn, (start, end) in func_lines.items():
        execs = set()
        for ln in range(start, min(end, len(lines)) + 1):
            text = lines[ln - 1].strip()
            if not text or text.startswith("#"):
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


def measure(py_src, run_calls):
    """Exec `py_src` (compiled as `<transpiled>`), then invoke `run_calls(ns,
    tracer)` with the module namespace under line tracing.  Returns
    {func_name: (hit_lines, executable_lines)} — the per-function line coverage
    the calls achieved.

    `run_calls` should call every transpiled function on every oracle input; it
    is passed the namespace and runs inside the tracer's scope."""
    ns = {}
    code = compile(py_src, "<transpiled>", "exec")
    exec(code, ns)
    tracer = LineTracer("<transpiled>")
    with tracer:
        run_calls(ns)
    spans = function_spans(py_src)
    execs = executable_lines(py_src, spans)
    result = {}
    for fn, ex in execs.items():
        start, end = spans[fn]
        # The `def` header line itself isn't a traced "line" event body; drop it.
        body = {ln for ln in ex if ln != start}
        hit = tracer.hit & body
        result[fn] = (hit, body)
    return result
