"""Executes the Python extracted from TailCalls.lean and asserts tail-call
elimination works: tail-recursive functions run in CONSTANT stack (no
RecursionError at depths far beyond Python's default limit of 1000) and compute
correct results, while non-tail recursion is left as a normal recursive def.

Usage:
    lake env lean TailCalls.lean > TailCalls_out.py
    python3 TailCalls_test.py
"""
import re
import sys

SRC = open("TailCalls_out.py").read()

ns: dict = {}
exec(SRC, ns)

failures = []


def check(label, got, want):
    if got != want:
        failures.append(f"{label}: got {got!r}, want {want!r}")


def check_no_overflow(label, thunk):
    try:
        thunk()
    except RecursionError:
        failures.append(f"{label}: RecursionError (tail call NOT eliminated)")


def fn(name):
    return ns[name]


def block(name):
    """Return the source text of one top-level function definition."""
    m = re.search(r"^def " + re.escape(name) + r"\(.*?(?=^def |\Z)", SRC, re.M | re.S)
    return m.group(0) if m else ""


# ---------------------------------------------------------------------------
# Correctness on small inputs
# ---------------------------------------------------------------------------
check("sum_to(100)", fn("sum_to")(100, 0), 5050)
check("tail_calls_gcd(48,18)", fn("tail_calls_gcd")(48, 18), 6)
check("countdown(500)", fn("countdown")(500), 0)
check("sum_list([1..100])", fn("sum_list")(list(range(1, 101))), 5050)
check("even_ish(10, True)", fn("even_ish")(10, True), True)
check("even_ish(7, True)", fn("even_ish")(7, True), False)
check("fact(5)", fn("fact")(5), 120)


# ---------------------------------------------------------------------------
# Constant stack: these depths (100k–1M) are far past Python's default 1000.
# Pre-fix, every one of these raised RecursionError.
# ---------------------------------------------------------------------------
check_no_overflow("sum_to deep", lambda: fn("sum_to")(1_000_000, 0))
check_no_overflow("tail_calls_gcd deep", lambda: fn("tail_calls_gcd")(1_000_000, 1))
check_no_overflow("countdown deep", lambda: fn("countdown")(1_000_000))
check_no_overflow("sum_list deep", lambda: fn("sum_list")(list(range(200_000))))
check_no_overflow("even_ish deep", lambda: fn("even_ish")(1_000_000, True))

# And the deep results are still correct.
check("sum_to(1e6) value", fn("sum_to")(1_000_000, 0), 500000500000)
check("countdown(1e6) value", fn("countdown")(1_000_000), 0)


# ---------------------------------------------------------------------------
# Structure
# ---------------------------------------------------------------------------
# Tail-recursive functions become while-True loops with `continue`, and contain
# no residual self-call.
for name in ("sum_to", "tail_calls_gcd", "countdown", "sum_list_go", "even_ish"):
    b = block(name)
    if "while True:" not in b:
        failures.append(f"{name}: expected a `while True:` loop")
    if "continue" not in b:
        failures.append(f"{name}: expected a `continue` (loop step)")
    if re.search(r"=\s*" + re.escape(name) + r"\(", b):
        failures.append(f"{name}: residual self-call — recursion not eliminated")

# even_ish must rebind BOTH parameters in parallel (order-independent).
if not re.search(r"n_3, flag = .*, .*", block("even_ish")):
    failures.append("even_ish: expected parallel two-parameter rebind")

# Non-tail recursion (fact) must stay a real recursive call, NOT a loop.
fb = block("fact")
if "while True:" in fb:
    failures.append("fact: should NOT be loop-rewritten (non-tail recursion)")
if not re.search(r"=\s*fact\(", fb):
    failures.append("fact: expected a recursive call to remain")


if failures:
    print("FAIL:")
    for f in failures:
        print("  " + f)
    sys.exit(1)
print("OK: all tail-call checks pass (constant stack, correct results, loop structure)")
