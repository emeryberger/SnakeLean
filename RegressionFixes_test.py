"""Executes the Python extracted from RegressionFixes.lean and asserts the
two fixed extraction bugs stay fixed (Bool-branch order, binary min/max).

Usage:
    lake env lean RegressionFixes.lean > RegressionFixes_out.py
    python3 RegressionFixes_test.py
"""
import sys

ns: dict = {}
exec(open("RegressionFixes_out.py").read(), ns)

signed_if = ns["signed_if"]
pick_if = ns["pick_if"]
min_nat = ns["min_nat"]
max_nat = ns["max_nat"]
clamp_high = ns["clamp_high"]
index_bang = ns["index_bang"]

failures = []


def check(label, got, want):
    if got != want:
        failures.append(f"{label}: got {got!r}, want {want!r}")


# (1) Bool-branch order: signedIf flag x = if flag then x else -x
check("signed_if(True, 5)", signed_if(True, 5), 5)
check("signed_if(False, 5)", signed_if(False, 5), -5)
check("pick_if(True, 1, 2)", pick_if(True, 1, 2), 1)
check("pick_if(False, 1, 2)", pick_if(False, 1, 2), 2)

# (2) Binary min/max: both operands used
check("min_nat(3, 7)", min_nat(3, 7), 3)
check("min_nat(9, 4)", min_nat(9, 4), 4)
check("max_nat(3, 7)", max_nat(3, 7), 7)
check("max_nat(9, 4)", max_nat(9, 4), 9)
check("clamp_high(100, 10)", clamp_high(100, 10), 10)
check("clamp_high(5, 10)", clamp_high(5, 10), 5)

# (3) getElem! panic-indexing: in-bounds returns the element (OOB would raise,
# matching Lean's panic — not asserted here since both sides error).
check("index_bang([10,20,30], 1)", index_bang([10, 20, 30], 1), 20)
check("index_bang([10,20,30], 0)", index_bang([10, 20, 30], 0), 10)

if failures:
    print("FAIL:")
    for f in failures:
        print("  " + f)
    sys.exit(1)
print("OK: all regression checks pass (Bool-branch order, binary min/max)")
