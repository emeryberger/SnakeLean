#!/usr/bin/env python3
"""
LLM-translated Python code for the Lean corpus.

This file contains idiomatic Python translations of all functions
in the LeanToPython corpus, as translated by Claude.

Total: ~100 functions covering algorithms, math, strings, data structures, games
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Callable, TypeVar

T = TypeVar('T')


# ============================================================================
# ALGORITHMS MODULE
# ============================================================================

def insertion_sort(xs: list[int]) -> list[int]:
    """Sort a list using insertion sort."""
    result = []
    for x in xs:
        i = 0
        while i < len(result) and result[i] < x:
            i += 1
        result.insert(i, x)
    return result


def merge(xs: list[int], ys: list[int]) -> list[int]:
    """Merge two sorted lists."""
    if not xs:
        return ys
    if not ys:
        return xs
    if xs[0] <= ys[0]:
        return [xs[0]] + merge(xs[1:], ys)
    return [ys[0]] + merge(xs, ys[1:])


def split(xs: list) -> tuple[list, list]:
    """Split a list into two halves."""
    if len(xs) == 0:
        return ([], [])
    if len(xs) == 1:
        return ([xs[0]], [])
    left, right = split(xs[2:])
    return ([xs[0]] + left, [xs[1]] + right)


def merge_sort(xs: list[int]) -> list[int]:
    """Sort using merge sort."""
    if len(xs) <= 1:
        return xs
    left, right = split(xs)
    return merge(merge_sort(left), merge_sort(right))


def linear_search(xs: list[int], target: int) -> int | None:
    """Find index of target in list."""
    for i, x in enumerate(xs):
        if x == target:
            return i
    return None


def binary_search(arr: list[int], target: int) -> int | None:
    """Binary search in sorted array."""
    lo, hi = 0, len(arr)
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid
    return None


def gcd(a: int, b: int) -> int:
    """Greatest common divisor."""
    while b:
        a, b = b, a % b
    return a


def lcm(a: int, b: int) -> int:
    """Least common multiple."""
    if a == 0 or b == 0:
        return 0
    return (a // gcd(a, b)) * b


def is_prime(n: int) -> bool:
    """Check if n is prime."""
    if n < 2:
        return False
    d = 2
    while d * d <= n:
        if n % d == 0:
            return False
        d += 1
    return True


def prime_factors(n: int) -> list[int]:
    """Return prime factorization of n."""
    factors = []
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors.append(d)
            n //= d
        d += 1
    if n > 1:
        factors.append(n)
    return factors


def fibonacci(n: int) -> int:
    """Calculate nth Fibonacci number (0-indexed)."""
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def power(base: int, exp: int) -> int:
    """Fast exponentiation."""
    result = 1
    while exp:
        if exp % 2:
            result *= base
        base *= base
        exp //= 2
    return result


def reverse_list(xs: list) -> list:
    """Reverse a list."""
    return xs[::-1]


def take(n: int, xs: list) -> list:
    """Take first n elements."""
    return xs[:n]


def drop(n: int, xs: list) -> list:
    """Drop first n elements."""
    return xs[n:]


def filter_list(p: Callable, xs: list) -> list:
    """Filter list by predicate."""
    return [x for x in xs if p(x)]


def map_list(f: Callable, xs: list) -> list:
    """Map function over list."""
    return [f(x) for x in xs]


def foldl(f: Callable, init, xs: list):
    """Left fold over list."""
    acc = init
    for x in xs:
        acc = f(acc, x)
    return acc


def foldr(f: Callable, init, xs: list):
    """Right fold over list."""
    for x in reversed(xs):
        init = f(x, init)
    return init


def zip_lists(xs: list, ys: list) -> list[tuple]:
    """Zip two lists."""
    return list(zip(xs, ys))


def unzip_list(xys: list[tuple]) -> tuple[list, list]:
    """Unzip list of pairs."""
    if not xys:
        return ([], [])
    xs, ys = zip(*xys)
    return (list(xs), list(ys))


def concat(xss: list[list]) -> list:
    """Flatten list of lists."""
    return [x for xs in xss for x in xs]


def intersperse(sep, xs: list) -> list:
    """Intersperse separator between elements."""
    if len(xs) <= 1:
        return xs
    result = []
    for i, x in enumerate(xs):
        if i > 0:
            result.append(sep)
        result.append(x)
    return result


def span(p: Callable, xs: list) -> tuple[list, list]:
    """Split list at first element not satisfying predicate."""
    i = 0
    while i < len(xs) and p(xs[i]):
        i += 1
    return (xs[:i], xs[i:])


def partition(p: Callable, xs: list) -> tuple[list, list]:
    """Partition list by predicate."""
    yes, no = [], []
    for x in xs:
        (yes if p(x) else no).append(x)
    return (yes, no)


def group_by(eq: Callable, xs: list) -> list[list]:
    """Group consecutive elements by equivalence."""
    if not xs:
        return []
    groups = [[xs[0]]]
    for x in xs[1:]:
        if eq(groups[-1][0], x):
            groups[-1].append(x)
        else:
            groups.append([x])
    return groups


def is_palindrome_str(s: str) -> bool:
    """Check if string is palindrome."""
    return s == s[::-1]


def count_char(c: str, s: str) -> int:
    """Count occurrences of character."""
    return s.count(c)


def replace_char(old: str, new: str, s: str) -> str:
    """Replace all occurrences of character."""
    return s.replace(old, new)


# ============================================================================
# MATH MODULE
# ============================================================================

def abs_val(x: int) -> int:
    """Absolute value."""
    return -x if x < 0 else x


def sign(x: int) -> int:
    """Sign of number: -1, 0, or 1."""
    if x < 0:
        return -1
    if x > 0:
        return 1
    return 0


def min_val(a: int, b: int) -> int:
    """Minimum of two values."""
    return a if a <= b else b


def max_val(a: int, b: int) -> int:
    """Maximum of two values."""
    return a if a >= b else b


def clamp(lo: int, hi: int, x: int) -> int:
    """Clamp value to range."""
    return max(lo, min(hi, x))


def div_mod(a: int, b: int) -> tuple[int, int]:
    """Quotient and remainder."""
    return (a // b, a % b)


def pow_nat(base: int, exp: int) -> int:
    """Power function (recursive)."""
    if exp == 0:
        return 1
    return base * pow_nat(base, exp - 1)


def fast_pow(base: int, exp: int) -> int:
    """Fast power using repeated squaring."""
    result = 1
    while exp:
        if exp % 2:
            result *= base
        base *= base
        exp //= 2
    return result


def mod_pow(base: int, exp: int, m: int) -> int:
    """Modular exponentiation."""
    result = 1
    base %= m
    while exp:
        if exp % 2:
            result = (result * base) % m
        base = (base * base) % m
        exp //= 2
    return result


def coprime(a: int, b: int) -> bool:
    """Check if numbers are coprime."""
    return gcd(a, b) == 1


def factorial(n: int) -> int:
    """Calculate n factorial."""
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


def binomial(n: int, k: int) -> int:
    """Binomial coefficient C(n, k)."""
    if k > n:
        return 0
    if k == 0 or k == n:
        return 1
    return binomial(n - 1, k - 1) + binomial(n - 1, k)


def catalan(n: int) -> int:
    """Catalan number."""
    if n <= 1:
        return 1
    return binomial(2 * n, n) // (n + 1)


def permutations_count(n: int, k: int) -> int:
    """Count permutations P(n, k)."""
    if k > n:
        return 0
    result = 1
    for i in range(n - k + 1, n + 1):
        result *= i
    return result


def triangular_number(n: int) -> int:
    """nth triangular number."""
    return n * (n + 1) // 2


def square_number(n: int) -> int:
    """nth square number."""
    return n * n


def pentagonal_number(n: int) -> int:
    """nth pentagonal number."""
    return n * (3 * n - 1) // 2


def hexagonal_number(n: int) -> int:
    """nth hexagonal number."""
    return n * (2 * n - 1)


def is_triangular(n: int) -> bool:
    """Check if n is triangular."""
    k = int((2 * n) ** 0.5)
    return k * (k + 1) == 2 * n


def is_square(n: int) -> bool:
    """Check if n is a perfect square."""
    k = int(n ** 0.5)
    return k * k == n


def isqrt(n: int) -> int:
    """Integer square root."""
    if n < 0:
        return 0
    return int(n ** 0.5)


def digits(n: int) -> list[int]:
    """Get digits of number."""
    if n == 0:
        return [0]
    result = []
    while n:
        result.append(n % 10)
        n //= 10
    return result[::-1]


def from_digits(ds: list[int]) -> int:
    """Construct number from digits."""
    result = 0
    for d in ds:
        result = result * 10 + d
    return result


def num_digits(n: int) -> int:
    """Count digits in number."""
    if n == 0:
        return 1
    count = 0
    while n:
        count += 1
        n //= 10
    return count


def digit_sum(n: int) -> int:
    """Sum of digits."""
    total = 0
    while n:
        total += n % 10
        n //= 10
    return total


def digital_root(n: int) -> int:
    """Digital root (repeated digit sum until single digit)."""
    while n >= 10:
        n = digit_sum(n)
    return n


def reverse_digits(n: int) -> int:
    """Reverse digits of number."""
    result = 0
    while n:
        result = result * 10 + n % 10
        n //= 10
    return result


def is_palindrome_num(n: int) -> bool:
    """Check if number is palindrome."""
    return n == reverse_digits(n)


def lucas(n: int) -> int:
    """nth Lucas number."""
    if n == 0:
        return 2
    if n == 1:
        return 1
    a, b = 2, 1
    for _ in range(n - 1):
        a, b = b, a + b
    return b


def tribonacci(n: int) -> int:
    """nth Tribonacci number."""
    if n == 0:
        return 0
    if n <= 2:
        return 1
    a, b, c = 0, 1, 1
    for _ in range(n - 2):
        a, b, c = b, c, a + b + c
    return c


def divisors(n: int) -> list[int]:
    """All divisors of n."""
    result = []
    d = 1
    while d * d <= n:
        if n % d == 0:
            result.append(d)
            if d != n // d:
                result.append(n // d)
        d += 1
    return sorted(result)


def num_divisors(n: int) -> int:
    """Count divisors."""
    return len(divisors(n))


def sum_divisors(n: int) -> int:
    """Sum of divisors."""
    return sum(divisors(n))


# ============================================================================
# STRINGS MODULE
# ============================================================================

def is_empty(s: str) -> bool:
    """Check if string is empty."""
    return len(s) == 0


def is_not_empty(s: str) -> bool:
    """Check if string is not empty."""
    return len(s) > 0


def head_str(s: str) -> str | None:
    """First character of string."""
    return s[0] if s else None


def tail_str(s: str) -> str:
    """String without first character."""
    return s[1:] if s else ""


def last_str(s: str) -> str | None:
    """Last character of string."""
    return s[-1] if s else None


def init_str(s: str) -> str:
    """String without last character."""
    return s[:-1] if s else ""


def take_str(n: int, s: str) -> str:
    """Take first n characters."""
    return s[:n]


def drop_str(n: int, s: str) -> str:
    """Drop first n characters."""
    return s[n:]


def char_at(s: str, i: int) -> str | None:
    """Character at index."""
    return s[i] if 0 <= i < len(s) else None


def substring(s: str, start: int, length: int) -> str:
    """Substring from start with given length."""
    return s[start:start + length]


def slice_str(s: str, start: int, stop: int) -> str:
    """Slice of string."""
    return s[start:stop]


def append_str(s1: str, s2: str) -> str:
    """Append two strings."""
    return s1 + s2


def concat_strs(ss: list[str]) -> str:
    """Concatenate list of strings."""
    return "".join(ss)


def intercalate_str(sep: str, ss: list[str]) -> str:
    """Join strings with separator."""
    return sep.join(ss)


def join_strs(ss: list[str]) -> str:
    """Join strings without separator."""
    return "".join(ss)


def replicate_str(n: int, s: str) -> str:
    """Repeat string n times."""
    return s * n


def reverse_str(s: str) -> str:
    """Reverse string."""
    return s[::-1]


def to_upper(s: str) -> str:
    """Convert to uppercase."""
    return s.upper()


def to_lower(s: str) -> str:
    """Convert to lowercase."""
    return s.lower()


def capitalize_str(s: str) -> str:
    """Capitalize first character."""
    return s[0].upper() + s[1:] if s else ""


def swap_case(s: str) -> str:
    """Swap case of all characters."""
    return s.swapcase()


def trim_left(s: str) -> str:
    """Remove leading whitespace."""
    return s.lstrip()


def trim_right(s: str) -> str:
    """Remove trailing whitespace."""
    return s.rstrip()


def trim_str(s: str) -> str:
    """Remove leading and trailing whitespace."""
    return s.strip()


def pad_left(n: int, c: str, s: str) -> str:
    """Pad string on left to length n."""
    return s.rjust(n, c)


def pad_right(n: int, c: str, s: str) -> str:
    """Pad string on right to length n."""
    return s.ljust(n, c)


def center_str(n: int, c: str, s: str) -> str:
    """Center string to length n."""
    return s.center(n, c)


def contains_str(sub: str, s: str) -> bool:
    """Check if substring is in string."""
    return sub in s


def index_of(sub: str, s: str) -> int | None:
    """Find index of substring."""
    i = s.find(sub)
    return i if i >= 0 else None


def count_substr(sub: str, s: str) -> int:
    """Count occurrences of substring."""
    return s.count(sub)


def starts_with(pre: str, s: str) -> bool:
    """Check if string starts with prefix."""
    return s.startswith(pre)


def ends_with(suf: str, s: str) -> bool:
    """Check if string ends with suffix."""
    return s.endswith(suf)


def is_digits(s: str) -> bool:
    """Check if string is all digits."""
    return s.isdigit() if s else False


def is_alpha(s: str) -> bool:
    """Check if string is all alphabetic."""
    return s.isalpha() if s else False


def split_on(sep: str, s: str) -> list[str]:
    """Split string by separator."""
    return s.split(sep)


def lines(s: str) -> list[str]:
    """Split string into lines."""
    return s.split("\n")


def words(s: str) -> list[str]:
    """Split string into words."""
    return s.split()


def unlines(ss: list[str]) -> str:
    """Join lines with newline."""
    return "\n".join(ss)


def unwords(ss: list[str]) -> str:
    """Join words with space."""
    return " ".join(ss)


def replace_str(old: str, new: str, s: str) -> str:
    """Replace all occurrences."""
    return s.replace(old, new)


def replace_first(old: str, new: str, s: str) -> str:
    """Replace first occurrence."""
    return s.replace(old, new, 1)


def remove_prefix(pre: str, s: str) -> str:
    """Remove prefix if present."""
    return s[len(pre):] if s.startswith(pre) else s


def remove_suffix(suf: str, s: str) -> str:
    """Remove suffix if present."""
    return s[:-len(suf)] if s.endswith(suf) and suf else s


def to_char_list(s: str) -> list[str]:
    """Convert string to character list."""
    return list(s)


def from_char_list(cs: list[str]) -> str:
    """Convert character list to string."""
    return "".join(cs)


def filter_chars(p: Callable, s: str) -> str:
    """Filter string by character predicate."""
    return "".join(c for c in s if p(c))


def map_chars(f: Callable, s: str) -> str:
    """Map function over characters."""
    return "".join(f(c) for c in s)


def ord_char(c: str) -> int:
    """Get ASCII code of character."""
    return ord(c)


def chr_int(n: int) -> str:
    """Get character from ASCII code."""
    return chr(n)


def to_ascii_codes(s: str) -> list[int]:
    """Convert string to ASCII code list."""
    return [ord(c) for c in s]


def from_ascii_codes(ns: list[int]) -> str:
    """Convert ASCII code list to string."""
    return "".join(chr(n) for n in ns)


# ============================================================================
# FUNCTIONAL MODULE
# ============================================================================

def identity(x):
    """Identity function."""
    return x


def const(x, y):
    """Constant function."""
    return x


def flip(f: Callable):
    """Flip arguments of binary function."""
    return lambda x, y: f(y, x)


def compose(f: Callable, g: Callable):
    """Compose two functions."""
    return lambda x: f(g(x))


def pipe(f: Callable, g: Callable):
    """Pipe (reverse compose)."""
    return lambda x: g(f(x))


def apply(f: Callable, x):
    """Apply function to argument."""
    return f(x)


def curry(f: Callable):
    """Curry binary function."""
    return lambda x: lambda y: f(x, y)


def uncurry(f: Callable):
    """Uncurry curried function."""
    return lambda xy: f(xy[0])(xy[1])


def option_map(f: Callable, x):
    """Map over optional value."""
    return f(x) if x is not None else None


def option_bind(f: Callable, x):
    """Bind (flatMap) over optional."""
    return f(x) if x is not None else None


def option_filter(p: Callable, x):
    """Filter optional by predicate."""
    return x if x is not None and p(x) else None


def option_get_or_else(default, x):
    """Get value or default."""
    return x if x is not None else default


def option_or_else(alternative, x):
    """Return x if not None, else alternative."""
    return x if x is not None else alternative


def option_zip(x, y):
    """Zip two optionals."""
    return (x, y) if x is not None and y is not None else None


def list_head(xs: list):
    """First element or None."""
    return xs[0] if xs else None


def list_tail(xs: list):
    """All but first element."""
    return xs[1:] if xs else None


def list_last(xs: list):
    """Last element or None."""
    return xs[-1] if xs else None


def list_nth(xs: list, n: int):
    """Element at index or None."""
    return xs[n] if 0 <= n < len(xs) else None


def list_update_at(xs: list, n: int, x) -> list:
    """Update element at index."""
    result = xs.copy()
    if 0 <= n < len(result):
        result[n] = x
    return result


def list_insert_at(xs: list, n: int, x) -> list:
    """Insert element at index."""
    return xs[:n] + [x] + xs[n:]


def list_remove_at(xs: list, n: int) -> list:
    """Remove element at index."""
    return xs[:n] + xs[n+1:] if 0 <= n < len(xs) else xs


def list_split_at(xs: list, n: int) -> tuple[list, list]:
    """Split list at index."""
    return (xs[:n], xs[n:])


def list_take_while(p: Callable, xs: list) -> list:
    """Take while predicate holds."""
    result = []
    for x in xs:
        if not p(x):
            break
        result.append(x)
    return result


def list_drop_while(p: Callable, xs: list) -> list:
    """Drop while predicate holds."""
    i = 0
    while i < len(xs) and p(xs[i]):
        i += 1
    return xs[i:]


def list_replicate(n: int, x) -> list:
    """Create list of n copies."""
    return [x] * n


def list_scanl(f: Callable, init, xs: list) -> list:
    """Scan left, accumulating results."""
    result = [init]
    acc = init
    for x in xs:
        acc = f(acc, x)
        result.append(acc)
    return result


def list_interleave(xs: list, ys: list) -> list:
    """Interleave two lists."""
    result = []
    i, j = 0, 0
    while i < len(xs) or j < len(ys):
        if i < len(xs):
            result.append(xs[i])
            i += 1
        if j < len(ys):
            result.append(ys[j])
            j += 1
    return result


# ============================================================================
# DATA STRUCTURES MODULE
# ============================================================================

def stack_empty() -> list:
    """Create empty stack."""
    return []


def stack_push(s: list, x) -> list:
    """Push onto stack."""
    return [x] + s


def stack_pop(s: list) -> list:
    """Pop from stack."""
    return s[1:] if s else []


def stack_peek(s: list):
    """Peek top of stack."""
    return s[0] if s else None


def stack_is_empty(s: list) -> bool:
    """Check if stack is empty."""
    return len(s) == 0


def stack_size(s: list) -> int:
    """Get stack size."""
    return len(s)


def queue_empty():
    """Create empty queue."""
    return ([], [])


def queue_enqueue(q, x):
    """Enqueue element."""
    return (q[0], [x] + q[1])


def queue_dequeue(q):
    """Dequeue element."""
    front, back = q
    if front:
        return (front[0], (front[1:], back))
    if back:
        front = back[::-1]
        return (front[0], (front[1:], []))
    return (None, ([], []))


def queue_is_empty(q) -> bool:
    """Check if queue is empty."""
    return len(q[0]) == 0 and len(q[1]) == 0


def queue_size(q) -> int:
    """Get queue size."""
    return len(q[0]) + len(q[1])


@dataclass
class BinaryTree:
    """Binary tree node."""
    value: Any
    left: 'BinaryTree | None' = None
    right: 'BinaryTree | None' = None


def tree_singleton(x) -> BinaryTree:
    """Create single-node tree."""
    return BinaryTree(x)


def tree_size(t: BinaryTree | None) -> int:
    """Count nodes in tree."""
    if t is None:
        return 0
    return 1 + tree_size(t.left) + tree_size(t.right)


def tree_height(t: BinaryTree | None) -> int:
    """Height of tree."""
    if t is None:
        return 0
    return 1 + max(tree_height(t.left), tree_height(t.right))


def tree_inorder(t: BinaryTree | None) -> list:
    """Inorder traversal."""
    if t is None:
        return []
    return tree_inorder(t.left) + [t.value] + tree_inorder(t.right)


def tree_preorder(t: BinaryTree | None) -> list:
    """Preorder traversal."""
    if t is None:
        return []
    return [t.value] + tree_preorder(t.left) + tree_preorder(t.right)


def tree_postorder(t: BinaryTree | None) -> list:
    """Postorder traversal."""
    if t is None:
        return []
    return tree_postorder(t.left) + tree_postorder(t.right) + [t.value]


def tree_mirror(t: BinaryTree | None) -> BinaryTree | None:
    """Mirror tree."""
    if t is None:
        return None
    return BinaryTree(t.value, tree_mirror(t.right), tree_mirror(t.left))


def tree_map(f: Callable, t: BinaryTree | None) -> BinaryTree | None:
    """Map function over tree."""
    if t is None:
        return None
    return BinaryTree(f(t.value), tree_map(f, t.left), tree_map(f, t.right))


def tree_fold(f: Callable, init, t: BinaryTree | None):
    """Fold over tree (inorder)."""
    if t is None:
        return init
    acc = tree_fold(f, init, t.left)
    acc = f(acc, t.value)
    return tree_fold(f, acc, t.right)


# ============================================================================
# ADVANCED MODULE
# ============================================================================

def heap_parent(i: int) -> int:
    """Parent index in heap."""
    return (i - 1) // 2


def heap_left_child(i: int) -> int:
    """Left child index in heap."""
    return 2 * i + 1


def heap_right_child(i: int) -> int:
    """Right child index in heap."""
    return 2 * i + 2


def swap_at(xs: list, i: int, j: int) -> list:
    """Swap elements at indices."""
    result = xs.copy()
    if 0 <= i < len(xs) and 0 <= j < len(xs):
        result[i], result[j] = result[j], result[i]
    return result


def heap_empty() -> list:
    """Create empty heap."""
    return []


def heap_is_empty(h: list) -> bool:
    """Check if heap is empty."""
    return len(h) == 0


def heap_size(h: list) -> int:
    """Get heap size."""
    return len(h)


def heap_min(h: list):
    """Get minimum element."""
    return h[0] if h else None


def union_find_empty():
    """Create empty union-find."""
    return ([], [])


def union_find_size(uf) -> int:
    """Get union-find size."""
    return len(uf[0])


def union_find_push(uf):
    """Add new element to union-find."""
    n = len(uf[0])
    return (uf[0] + [n], uf[1] + [0])


def union_find_of_size(n: int):
    """Create union-find with n elements."""
    return (list(range(n)), [0] * n)


def graph_empty():
    """Create empty graph."""
    return (0, [])


def graph_add_vertex(g):
    """Add vertex to graph."""
    return (g[0] + 1, g[1])


def graph_add_edge(g, u: int, v: int):
    """Add edge to graph."""
    return (g[0], [(u, v)] + g[1])


def graph_neighbors(g, v: int) -> list[int]:
    """Get neighbors of vertex."""
    return [w if u == v else u for u, w in g[1] if u == v or w == v]


def matrix_get(m: list[list], i: int, j: int):
    """Get matrix element."""
    if 0 <= i < len(m) and 0 <= j < len(m[i]):
        return m[i][j]
    return None


def matrix_set(m: list[list], i: int, j: int, v) -> list[list]:
    """Set matrix element."""
    result = [row.copy() for row in m]
    if 0 <= i < len(result) and 0 <= j < len(result[i]):
        result[i][j] = v
    return result


def matrix_create(n: int, fill) -> list[list]:
    """Create n x n matrix filled with value."""
    return [[fill] * n for _ in range(n)]


# ============================================================================
# GAMES MODULE
# ============================================================================

from enum import Enum


class Player(Enum):
    """Tic-tac-toe player."""
    X = 1
    O = 2

    def other(self) -> 'Player':
        """Get other player."""
        return Player.O if self == Player.X else Player.X


class RPS(Enum):
    """Rock-Paper-Scissors move."""
    ROCK = 0
    PAPER = 1
    SCISSORS = 2


def rps_beats(a: RPS, b: RPS) -> bool:
    """Check if a beats b."""
    return (a.value - b.value) % 3 == 1


def rps_from_nat(n: int) -> RPS:
    """Convert number to RPS."""
    return RPS(n % 3)


def tictactoe_empty() -> list[list]:
    """Create empty tic-tac-toe board."""
    return [[None] * 3 for _ in range(3)]


def tictactoe_get(board: list[list], r: int, c: int):
    """Get board cell."""
    if 0 <= r < 3 and 0 <= c < 3:
        return board[r][c]
    return None


def tictactoe_set(board: list[list], r: int, c: int, p) -> list[list]:
    """Set board cell."""
    result = [row.copy() for row in board]
    if 0 <= r < 3 and 0 <= c < 3 and result[r][c] is None:
        result[r][c] = p
    return result


def tictactoe_check_line(board: list[list], cells: list[tuple[int, int]]):
    """Check if line is winning."""
    values = [board[r][c] for r, c in cells]
    if values[0] is not None and all(v == values[0] for v in values):
        return values[0]
    return None


def tictactoe_winner(board: list[list]):
    """Get winner if any."""
    lines = [
        [(0, 0), (0, 1), (0, 2)],
        [(1, 0), (1, 1), (1, 2)],
        [(2, 0), (2, 1), (2, 2)],
        [(0, 0), (1, 0), (2, 0)],
        [(0, 1), (1, 1), (2, 1)],
        [(0, 2), (1, 2), (2, 2)],
        [(0, 0), (1, 1), (2, 2)],
        [(0, 2), (1, 1), (2, 0)],
    ]
    for line in lines:
        w = tictactoe_check_line(board, line)
        if w is not None:
            return w
    return None


def tictactoe_is_draw(board: list[list]) -> bool:
    """Check if game is draw."""
    return tictactoe_winner(board) is None and all(
        board[r][c] is not None for r in range(3) for c in range(3)
    )


def tictactoe_is_over(board: list[list]) -> bool:
    """Check if game is over."""
    return tictactoe_winner(board) is not None or tictactoe_is_draw(board)


def tictactoe_valid_moves(board: list[list]) -> list[tuple[int, int]]:
    """Get valid moves."""
    return [(r, c) for r in range(3) for c in range(3) if board[r][c] is None]


def nim_create(heaps: list[int]):
    """Create Nim game state."""
    return heaps


def nim_take(heaps: list[int], heap_idx: int, count: int) -> list[int]:
    """Take from heap in Nim."""
    result = heaps.copy()
    if 0 <= heap_idx < len(result) and 0 < count <= result[heap_idx]:
        result[heap_idx] -= count
    return result


def nim_is_over(heaps: list[int]) -> bool:
    """Check if Nim game is over."""
    return all(h == 0 for h in heaps)


def nim_xor(heaps: list[int]) -> int:
    """Nim-sum (XOR of heap sizes)."""
    result = 0
    for h in heaps:
        result ^= h
    return result


def nim_is_winning(heaps: list[int]) -> bool:
    """Check if position is winning (nim-sum != 0)."""
    return nim_xor(heaps) != 0


def roll_die(seed: int, sides: int = 6) -> tuple[int, int]:
    """Roll die with seed (returns roll and new seed)."""
    new_seed = (seed * 1103515245 + 12345) % (2**31)
    roll = (new_seed % sides) + 1
    return (roll, new_seed)


def roll_dice(seed: int, n: int, sides: int = 6) -> tuple[list[int], int]:
    """Roll n dice."""
    rolls = []
    for _ in range(n):
        roll, seed = roll_die(seed, sides)
        rolls.append(roll)
    return (rolls, seed)


def dice_sum(rolls: list[int]) -> int:
    """Sum of dice rolls."""
    return sum(rolls)


def is_valid_sudoku_row(row: list[int]) -> bool:
    """Check if Sudoku row is valid."""
    nums = [n for n in row if 1 <= n <= 9]
    return len(nums) == len(set(nums))


# ============================================================================
# TESTS
# ============================================================================

if __name__ == "__main__":
    # Run basic tests
    print("Running tests...")

    # Algorithms
    assert insertion_sort([3, 1, 4, 1, 5]) == [1, 1, 3, 4, 5]
    assert gcd(48, 18) == 6
    assert is_prime(17) == True
    assert is_prime(15) == False
    assert fibonacci(10) == 55
    assert prime_factors(12) == [2, 2, 3]

    # Math
    assert factorial(5) == 120
    assert binomial(5, 2) == 10
    assert digit_sum(123) == 6
    assert is_palindrome_num(12321) == True

    # Strings
    assert is_palindrome_str("racecar") == True
    assert reverse_str("hello") == "olleh"
    assert count_char("l", "hello") == 2

    # Data structures
    s = stack_push(stack_push(stack_empty(), 1), 2)
    assert stack_peek(s) == 2
    assert stack_size(s) == 2

    print("All tests passed!")
    print(f"Total functions: ~150")
