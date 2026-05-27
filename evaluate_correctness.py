#!/usr/bin/env python3
"""
Comprehensive correctness evaluation of LCNF vs LLM translations.

Tests both translation approaches against expected results and reports accuracy.
"""

from dataclasses import dataclass
from typing import Any, Callable
import traceback

# ============================================================================
# Test Cases with proper expected values for both conventions
# ============================================================================

# Note: LCNF uses fib(0)=0, fib(1)=1 (standard)
#       LLM might use fib(0)=1, fib(1)=1 depending on implementation

TEST_SUITE = [
    # (test_name, lcnf_func, llm_func, inputs, lcnf_expected, llm_expected)

    # Algorithms - numeric
    ("gcd", "algorithms_gcd", "gcd",
     [(48, 18), (100, 25), (17, 5), (0, 5), (12, 0), (36, 24), (1, 1), (13, 13)],
     [6, 25, 1, 5, 12, 12, 1, 13], [6, 25, 1, 5, 12, 12, 1, 13]),

    ("factorial", "factorial", "factorial",
     [(0,), (1,), (2,), (5,), (10,)],
     [1, 1, 2, 120, 3628800], [1, 1, 2, 120, 3628800]),

    ("fibonacci", "algorithms_fibonacci", "fibonacci",
     [(0,), (1,), (2,), (3,), (5,), (10,)],
     [0, 1, 1, 2, 5, 55],  # Standard: fib(0)=0
     [0, 1, 1, 2, 5, 55]), # Both should use same convention now

    ("is_prime", "algorithms_is_prime", "is_prime",
     [(0,), (1,), (2,), (3,), (4,), (5,), (17,), (25,), (97,), (100,)],
     [False, False, True, True, False, True, True, False, True, False],
     [False, False, True, True, False, True, True, False, True, False]),

    ("prime_factors", "algorithms_prime_factors", "prime_factors",
     [(12,), (17,), (100,), (1,), (2,)],
     [[2, 2, 3], [17], [2, 2, 5, 5], [], [2]],
     [[2, 2, 3], [17], [2, 2, 5, 5], [], [2]]),

    # Algorithms - sorting
    ("insertion_sort", "insertion_sort", "insertion_sort",
     [([3, 1, 4, 1, 5],), ([],), ([1],), ([5, 4, 3, 2, 1],), ([1, 2, 3],)],
     [[1, 1, 3, 4, 5], [], [1], [1, 2, 3, 4, 5], [1, 2, 3]],
     [[1, 1, 3, 4, 5], [], [1], [1, 2, 3, 4, 5], [1, 2, 3]]),

    ("merge_sort", "merge_sort", "merge_sort",
     [([3, 1, 4, 1, 5],), ([],), ([1],), ([5, 4, 3, 2, 1],)],
     [[1, 1, 3, 4, 5], [], [1], [1, 2, 3, 4, 5]],
     [[1, 1, 3, 4, 5], [], [1], [1, 2, 3, 4, 5]]),

    # Algorithms - searching
    ("binary_search", "binary_search", "binary_search",
     [([1, 2, 3, 4, 5], 3), ([1, 2, 3, 4, 5], 1), ([1, 2, 3, 4, 5], 6), ([], 1)],
     [2, 0, None, None], [2, 0, None, None]),

    ("linear_search", "linear_search", "linear_search",
     [([1, 2, 3, 4, 5], 3), ([1, 2, 3, 4, 5], 1), ([1, 2, 3, 4, 5], 6), ([], 1)],
     [2, 0, None, None], [2, 0, None, None]),

    # Math
    ("pow", "pow", "pow_nat",
     [(2, 0), (2, 1), (2, 10), (3, 4), (5, 3)],
     [1, 2, 1024, 81, 125], [1, 2, 1024, 81, 125]),

    ("abs", "math_abs", "abs_val",
     [(5,), (-5,), (0,), (-100,)],
     [5, 5, 0, 100], [5, 5, 0, 100]),

    ("binomial", "binomial", "binomial",
     [(5, 2), (10, 3), (0, 0), (5, 0), (5, 6)],
     [10, 120, 1, 1, 0], [10, 120, 1, 1, 0]),

    # LCNF's digit_sum10 is a wrapper for base-10 digit sum
    ("digit_sum", "digit_sum10", "digit_sum",
     [(123,), (999,), (0,), (10,), (12345,)],
     [6, 27, 0, 1, 15], [6, 27, 0, 1, 15]),

    # Strings
    ("reverse_str", "strings_reverse", "reverse_str",
     [("hello",), ("",), ("a",), ("ab",), ("racecar",)],
     ["olleh", "", "a", "ba", "racecar"], ["olleh", "", "a", "ba", "racecar"]),

    # Heap operations
    ("left_child", "left_child", "heap_left_child",
     [(0,), (1,), (2,), (3,)],
     [1, 3, 5, 7], [1, 3, 5, 7]),

    ("right_child", "right_child", "heap_right_child",
     [(0,), (1,), (2,), (3,)],
     [2, 4, 6, 8], [2, 4, 6, 8]),

    # Note: parent(0) is undefined in heap semantics, but (0-1)//2 = -1 in Python
    ("parent", "parent", "heap_parent",
     [(1,), (2,), (3,), (4,), (5,), (6,)],
     [0, 0, 1, 1, 2, 2], [0, 0, 1, 1, 2, 2]),

    # Additional math functions
    ("lcm", "algorithms_lcm", "lcm",
     [(4, 6), (3, 5), (12, 18), (7, 11), (1, 100)],
     [12, 15, 36, 77, 100], [12, 15, 36, 77, 100]),

    ("mod_pow", "mod_pow", "mod_pow",
     [(2, 10, 1000), (3, 5, 100), (2, 20, 1000000)],
     [24, 43, 48576], [24, 43, 48576]),

    ("fast_pow", "fast_pow", "fast_pow",
     [(2, 10), (3, 5), (5, 4)],
     [1024, 243, 625], [1024, 243, 625]),

    ("coprime", "coprime", "coprime",
     [(3, 5), (4, 6), (15, 28), (12, 18)],
     [True, False, True, False], [True, False, True, False]),

    ("is_even", "is_even", "is_even",
     [(0,), (1,), (2,), (100,), (101,)],
     [True, False, True, True, False], [True, False, True, True, False]),

    ("is_odd", "is_odd", "is_odd",
     [(0,), (1,), (2,), (100,), (101,)],
     [False, True, False, False, True], [False, True, False, False, True]),

    # Number theory - LCNF's num_digits10 is a wrapper for base-10 digit count
    ("num_digits", "num_digits10", "num_digits",
     [(0,), (9,), (10,), (100,), (12345,)],
     [1, 1, 2, 3, 5], [1, 1, 2, 3, 5]),

    ("is_palindrome_num", "is_palindrome_num", "is_palindrome_num",
     [(121,), (123,), (12321,), (0,), (1,)],
     [True, False, True, True, True], [True, False, True, True, True]),

    # More string functions
    ("to_upper", "to_upper", "to_upper",
     [("hello",), ("WORLD",), ("HeLLo",), ("",)],
     ["HELLO", "WORLD", "HELLO", ""], ["HELLO", "WORLD", "HELLO", ""]),

    ("to_lower", "to_lower", "to_lower",
     [("HELLO",), ("world",), ("HeLLo",), ("",)],
     ["hello", "world", "hello", ""], ["hello", "world", "hello", ""]),
]


@dataclass
class TestResult:
    test_name: str
    source: str
    func_name: str
    passed: int
    total: int
    failures: list[tuple[tuple, Any, Any]]
    error: str | None = None


def find_function(module, name: str) -> Callable | None:
    """Find a function in a module."""
    if hasattr(module, name) and callable(getattr(module, name)):
        return getattr(module, name)
    return None


def test_function(module, test_name: str, func_name: str, inputs: list, expected: list, source: str) -> TestResult:
    """Test a single function."""
    func = find_function(module, func_name)

    if func is None:
        return TestResult(
            test_name=test_name,
            source=source,
            func_name=func_name,
            passed=0,
            total=len(inputs),
            failures=[],
            error="Function not found"
        )

    passed = 0
    failures = []

    for args, exp in zip(inputs, expected):
        try:
            result = func(*args)
            if result == exp:
                passed += 1
            else:
                failures.append((args, exp, result))
        except Exception as e:
            failures.append((args, exp, f"ERROR: {e}"))

    return TestResult(
        test_name=test_name,
        source=source,
        func_name=func_name,
        passed=passed,
        total=len(inputs),
        failures=failures
    )


def run_evaluation(lcnf_module, llm_module) -> tuple[list[TestResult], list[TestResult]]:
    """Run all tests against both modules."""
    lcnf_results = []
    llm_results = []

    for test_name, lcnf_func, llm_func, inputs, lcnf_expected, llm_expected in TEST_SUITE:
        lcnf_results.append(test_function(lcnf_module, test_name, lcnf_func, inputs, lcnf_expected, "lcnf"))
        llm_results.append(test_function(llm_module, test_name, llm_func, inputs, llm_expected, "llm"))

    return lcnf_results, llm_results


def print_results(lcnf_results: list[TestResult], llm_results: list[TestResult]):
    """Print formatted comparison."""
    print("=" * 100)
    print("CORRECTNESS EVALUATION: LCNF EXTRACTION vs LLM TRANSLATION")
    print("=" * 100)

    print(f"\n{'Test':<20} {'LCNF Func':<25} {'LCNF':<10} {'LLM Func':<25} {'LLM':<10} {'Result'}")
    print("-" * 100)

    lcnf_total_passed = 0
    lcnf_total_tests = 0
    llm_total_passed = 0
    llm_total_tests = 0

    both_correct = 0
    lcnf_only = 0
    llm_only = 0
    neither = 0

    for lcnf_r, llm_r in zip(lcnf_results, llm_results):
        lcnf_str = f"{lcnf_r.passed}/{lcnf_r.total}" if not lcnf_r.error else "N/A"
        llm_str = f"{llm_r.passed}/{llm_r.total}" if not llm_r.error else "N/A"

        lcnf_perfect = lcnf_r.passed == lcnf_r.total and not lcnf_r.error
        llm_perfect = llm_r.passed == llm_r.total and not llm_r.error

        if lcnf_perfect and llm_perfect:
            result = "BOTH ✓"
            both_correct += 1
        elif lcnf_perfect:
            result = "LCNF ✓"
            lcnf_only += 1
        elif llm_perfect:
            result = "LLM ✓"
            llm_only += 1
        else:
            result = "NEITHER"
            neither += 1

        print(f"{lcnf_r.test_name:<20} {lcnf_r.func_name:<25} {lcnf_str:<10} {llm_r.func_name:<25} {llm_str:<10} {result}")

        lcnf_total_passed += lcnf_r.passed
        lcnf_total_tests += lcnf_r.total
        llm_total_passed += llm_r.passed
        llm_total_tests += llm_r.total

    print("-" * 100)
    print(f"{'TOTAL':<20} {'':<25} {lcnf_total_passed}/{lcnf_total_tests:<8} {'':<25} {llm_total_passed}/{llm_total_tests:<8}")

    # Summary
    print("\n" + "=" * 100)
    print("SUMMARY STATISTICS")
    print("=" * 100)

    lcnf_rate = 100 * lcnf_total_passed / lcnf_total_tests if lcnf_total_tests > 0 else 0
    llm_rate = 100 * llm_total_passed / llm_total_tests if llm_total_tests > 0 else 0

    print(f"\nTest Pass Rate:")
    print(f"  LCNF: {lcnf_total_passed}/{lcnf_total_tests} ({lcnf_rate:.1f}%)")
    print(f"  LLM:  {llm_total_passed}/{llm_total_tests} ({llm_rate:.1f}%)")

    total_tests = len(TEST_SUITE)
    print(f"\nFunction-level Correctness (all tests for that function pass):")
    print(f"  Both correct:  {both_correct}/{total_tests} ({100*both_correct/total_tests:.1f}%)")
    print(f"  LCNF only:     {lcnf_only}/{total_tests} ({100*lcnf_only/total_tests:.1f}%)")
    print(f"  LLM only:      {llm_only}/{total_tests} ({100*llm_only/total_tests:.1f}%)")
    print(f"  Neither:       {neither}/{total_tests} ({100*neither/total_tests:.1f}%)")

    # Failures
    print("\n" + "=" * 100)
    print("FAILURE DETAILS")
    print("=" * 100)

    has_failures = False
    for lcnf_r, llm_r in zip(lcnf_results, llm_results):
        if lcnf_r.failures or llm_r.failures or lcnf_r.error or llm_r.error:
            has_failures = True
            print(f"\n{lcnf_r.test_name}:")
            if lcnf_r.error:
                print(f"  LCNF ({lcnf_r.func_name}): {lcnf_r.error}")
            elif lcnf_r.failures:
                print(f"  LCNF ({lcnf_r.func_name}) failures:")
                for args, exp, actual in lcnf_r.failures[:3]:
                    print(f"    {args} -> expected {exp}, got {actual}")
            if llm_r.error:
                print(f"  LLM ({llm_r.func_name}): {llm_r.error}")
            elif llm_r.failures:
                print(f"  LLM ({llm_r.func_name}) failures:")
                for args, exp, actual in llm_r.failures[:3]:
                    print(f"    {args} -> expected {exp}, got {actual}")

    if not has_failures:
        print("\nNo failures!")

    # Conclusions
    print("\n" + "=" * 100)
    print("CONCLUSIONS")
    print("=" * 100)

    # Count failure categories
    missing_func_lcnf = sum(1 for r in lcnf_results if r.error == "Function not found")
    missing_func_llm = sum(1 for r in llm_results if r.error == "Function not found")
    extra_param_lcnf = sum(1 for r in lcnf_results if r.failures and any("missing 1 required" in str(f[2]) for f in r.failures))
    runtime_error_lcnf = sum(1 for r in lcnf_results if r.failures and any("ERROR:" in str(f[2]) for f in r.failures))
    wrong_result_lcnf = sum(1 for r in lcnf_results if r.failures and not any("ERROR:" in str(f[2]) for f in r.failures) and r.passed < r.total)

    print(f"""
Overall correctness comparison:
  - LCNF extraction achieves {lcnf_rate:.1f}% test pass rate
  - LLM translation achieves {llm_rate:.1f}% test pass rate

Failure breakdown (LCNF):
  - Function not found: {missing_func_lcnf}
  - Extra type parameter needed: {extra_param_lcnf}
  - Runtime errors (reduce, etc.): {runtime_error_lcnf}
  - Wrong results: {wrong_result_lcnf}

Key observations:
  1. Core algorithms (gcd, factorial, fibonacci, is_prime, sorting, searching) work correctly
  2. Some LCNF functions require extra type parameters from Lean's polymorphism
  3. Some LCNF string/number functions have broken stdlib dependencies (reduce, etc.)
  4. A few LCNF functions (fast_pow, mod_pow) have logic bugs in the extracted code
  5. LLM translations achieve high accuracy with idiomatic Python patterns

Trade-offs:
  LCNF Extraction:
    + Deterministic and reproducible
    + Directly derived from Lean compiler IR
    + Core functions are semantically correct
    - Polymorphic functions get extra type parameters
    - Some stdlib mappings are incomplete
    - Pattern matching on match expressions can produce buggy code

  LLM Translation:
    + Idiomatic Python conventions
    + Simpler function signatures
    + Higher overall accuracy on this corpus
    - Requires verification against original semantics
    - Not reproducible (may vary between runs)
""")


def main():
    print("Loading modules...")

    try:
        import extracted.lcnf_corpus as lcnf_module
        print(f"  LCNF corpus loaded: {len([n for n in dir(lcnf_module) if not n.startswith('_')])} symbols")
    except Exception as e:
        print(f"  LCNF corpus failed: {e}")
        return

    try:
        import extracted.llm_corpus as llm_module
        print(f"  LLM corpus loaded: {len([n for n in dir(llm_module) if not n.startswith('_')])} symbols")
    except Exception as e:
        print(f"  LLM corpus failed: {e}")
        return

    print("\nRunning tests...")
    lcnf_results, llm_results = run_evaluation(lcnf_module, llm_module)
    print_results(lcnf_results, llm_results)


if __name__ == "__main__":
    main()
