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
drop_until_zero = ns["drop_until_zero"]

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

# (4) tail-recursive deferred-continuation helper: must compile (no `continue`
# inside a nested def) and drop everything up to & including the first 0.
check("drop_until_zero([1,2,0,3])", drop_until_zero([1, 2, 0, 3]), [3])
check("drop_until_zero([1,2,3])", drop_until_zero([1, 2, 3]), [])

# (5) name collision: use_tally calls ModA.tally (sum), which must NOT be
# shadowed by ModB.tally (length). [1,2,3] -> sum 6, not length 3.
use_tally = ns["use_tally"]
check("use_tally([1,2,3])", use_tally([1, 2, 3]), 6)
check("use_tally([4,5])", use_tally([4, 5]), 9)

# (6) loop-mode find? predicate: must compile (no undefined _uniq_NNN) and find
# the pair whose first component equals k.
look_loop = ns["look_loop"]
check("look_loop([(1,9),(2,8)], 2)", look_loop([(1, 9), (2, 8)], 2), True)
check("look_loop([(1,9),(2,8)], 5)", look_loop([(1, 9), (2, 8)], 5), False)

# (7) point-free predicates passed to filter (Option.isSome + a user fn).
count_some = ns["count_some"]
count_big = ns["count_big"]
check("count_some([1,None,3,None])", count_some([1, None, 3, None]), 2)
check("count_big([1,5,2,9])", count_big([1, 5, 2, 9]), 2)

# (8) Option.map / List.zip / List.set (setTR).
bump = ns["bump"]
pair_up = ns["pair_up"]
set_at = ns["set_at"]
check("bump(4)", bump(4), 5)
check("bump(None)", bump(None), None)
check("pair_up([1,2,3],[4,5,6])", pair_up([1, 2, 3], [4, 5, 6]), [(1, 4), (2, 5), (3, 6)])
check("set_at([1,2,3], 1, 9)", set_at([1, 2, 3], 1, 9), [1, 9, 3])

# (9) List.head?/getLast? applied over the value arg only.
first_of = ns["first_of"]
last_of = ns["last_of"]
check("first_of([7,8,9])", first_of([7, 8, 9]), 7)
check("first_of([])", first_of([]), None)
check("last_of([7,8,9])", last_of([7, 8, 9]), 9)

# (10) nullary user value used point-free must be CALLED: prepend_base(5) = [5, 0].
prepend_base = ns["prepend_base"]
check("prepend_base(5)", prepend_base(5), [5, 0])

if failures:
    print("FAIL:")
    for f in failures:
        print("  " + f)
    sys.exit(1)
print("OK: all regression checks pass (Bool-branch order, binary min/max)")
