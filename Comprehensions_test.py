"""Executes the Python extracted from Comprehensions.lean and asserts that
list/set comprehension emission stays correct — both semantically (the code
computes the right answers) and structurally (lambdas actually inline into
comprehensions, complex bodies fall back to a `def`, and dedup produces a set
comprehension).

Usage:
    lake env lean Comprehensions.lean > Comprehensions_out.py
    python3 Comprehensions_test.py
"""
import re
import sys

SRC = open("Comprehensions_out.py").read()

ns: dict = {}
exec(SRC, ns)

failures = []


def check(label, got, want):
    if got != want:
        failures.append(f"{label}: got {got!r}, want {want!r}")


def check_shape(label, pattern, *, should_match=True):
    """Assert the emitted source of one function matches (or doesn't) a regex."""
    present = re.search(pattern, SRC) is not None
    if present != should_match:
        verb = "expected" if should_match else "did NOT expect"
        failures.append(f"{label}: {verb} /{pattern}/ in generated source")


# ---------------------------------------------------------------------------
# Semantics
# ---------------------------------------------------------------------------
check("add_one", ns["add_one"]([1, 2, 3]), [2, 3, 4])
check("squares", ns["squares"]([2, 3, 4]), [4, 9, 16])
check("evens", ns["evens"]([1, 2, 3, 4, 5, 6]), [2, 4, 6])
check("any_big true", ns["any_big"]([1, 2, 200]), True)
check("any_big false", ns["any_big"]([1, 2, 3]), False)
check("all_pos true", ns["all_pos"]([1, 2, 3]), True)
check("all_pos false", ns["all_pos"]([1, 0, 3]), False)
check("first_even", ns["first_even"]([1, 3, 4, 5, 6]), 4)
check("first_even none", ns["first_even"]([1, 3, 5]), None)
check("pos_doubled", ns["pos_doubled"]([-2, 0, 1, 3]), [2, 6])
check("succ_all", ns["succ_all"]([1, 2, 3]), [2, 3, 4])
check("map_with", ns["map_with"]([1, 2, 3], lambda z: z * 100), [100, 200, 300])
check("keep_double_pos", ns["keep_double_pos"]([-1, 2, 0, 3]), [4, 6])
check("via_let", ns["via_let"]([1, 2, 3]), [11, 12, 13])

# eraseDups / toSet model set semantics -> Python set
check("dedup", ns["dedup"]([1, 1, 2, 3, 3, 3]), {1, 2, 3})
check("uniq_squares", ns["uniq_squares"]([1, -1, 2, -2]), {1, 4})
check("uniq_big", ns["uniq_big"]([6, 6, 7, 2, 8]), {6, 7, 8})


# ---------------------------------------------------------------------------
# Structure — the whole point of this change is idiomatic output, so assert it.
# ---------------------------------------------------------------------------
# Variable names carry a deterministic numeric suffix (e.g. `x_3`); the regexes
# below use `\w+` for binders so they stay robust across toolchain bumps while
# still pinning the essential structure. The point is to catch regression back
# to the non-inlined `[_f(x) for x in xs]` form.

# map/filter inline the lambda body (arithmetic/comparison), not `_f(x)`.
check_shape("add_one inlines body", r"\[\(\w+ \+ 1\) for \w+ in xs\]")
check_shape("evens inlines predicate", r"\[(\w+) for \1 in \w+ if \(\(\1 % 2\) == 0\)\]")
check_shape("any_big inlines predicate", r"any\(\(100 < \w+\) for \w+ in \w+\)")

# Named / caller-supplied function argument stays `f(x)`.
check_shape("map_with keeps f(x)", r"\[f\(x\) for x in xs_\d+\]")

# Complex (if/else) lambda body falls back to a real def — and never inlines
# into a call to an undefined helper name (the walrus form calls the real def).
check_shape("keep_double_pos keeps def", r"def _f_\d+\(\w+: int\):")
check_shape("keep_double_pos uses filterMap walrus", r"if \(_y := _f_\d+\(x\)\) is not None")

# Deferred lambda used as a value is materialized as a Python lambda.
check_shape("via_let materializes lambda", r"\w+ = \(lambda \w+: \(\w+ \+ 10\)\)")

# Dedup / toSet produce set comprehensions, fusing upstream map/filter.
check_shape("dedup is a set comprehension", r"\{_v for _v in xs_\d+\}")
check_shape("uniq_squares fuses into set comp", r"\{\(\w+ \* \w+\) for \w+ in xs_\d+\}")
check_shape("uniq_big fuses filter into set comp", r"\{(\w+) for \1 in xs_\d+ if \(5 < \1\)\}")

# No stale list(dict.fromkeys(...)) form should remain for dedup.
check_shape("no dict.fromkeys", r"dict\.fromkeys", should_match=False)


if failures:
    print("FAIL:")
    for f in failures:
        print("  " + f)
    sys.exit(1)
print("OK: all comprehension checks pass (inlining, fallback, set comprehensions)")
