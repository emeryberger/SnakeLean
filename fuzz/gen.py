#!/usr/bin/env python3
"""Grammar-based generator of well-typed, terminating Lean functions.

Emits a self-contained Lean file containing:
  - N random function definitions over a small typed grammar
    (Nat / Bool / List Nat / Nat x Nat), and
  - a driver `#eval` that transpiles them to Python (### PYTHON banner) and
    prints Lean-computed oracle rows for random inputs (### ORACLE banner).

`fuzz.py` runs the file through Lean, execs the transpiled Python, and diffs
against the oracle. The grammar is designed to hit the transpiler's tricky
lowerings: if/match (Nat/List/Option), let, tuples, list combinators
(map/filter/foldl/reverse/append), DecidableEq comparisons, and fuel-bounded
self-recursion.

Determinism: seeded PRNG, so a failing seed reproduces exactly.

Coverage-guided generation (Havrikov & Zeller, "Systematically Covering Input
Structure", ASE 2019): every grammatical choice is a *labeled production*, and
the generator prefers productions it has not yet covered.  This is scoped to a
single generated file (one `Gen` instance) so a seed still fully determines its
output — the reproducibility a differential fuzzer needs.  `Gen.all_prods` /
`Gen.covered` let `fuzz.py` aggregate which productions were exercised across a
whole sweep, so "did we test construct X?" becomes a measurement instead of a
matter of chance.
"""
import random
import sys

# Types in the grammar.
NAT, BOOL, LISTNAT, PAIR, INT, OPTNAT = (
    "Nat", "Bool", "List Nat", "Nat × Nat", "Int", "Option Nat")
# Phase 1 types: exercise the transpiler's barely-tested String/Char/Array
# handlers (the qsort bug F13 lived in Array; CLAUDE.md flags Max/Xor).
STRING, CHAR, ARRAYNAT = ("String", "Char", "Array Nat")
# Phase 2 types: list element-type variety — exercise the list combinators
# (map/filter/foldr/append/reverse) over non-Nat elements and one nesting level.
LISTINT, LISTBOOL, LISTLISTNAT = ("List Int", "List Bool", "List (List Nat)")
LEAN_TYPES = [NAT, BOOL, LISTNAT, PAIR, INT, OPTNAT, STRING, CHAR, ARRAYNAT,
              LISTINT, LISTBOOL, LISTLISTNAT]

# Every production label the grammar can emit — the coverage universe.  Kept in
# sync with the `choose(...)` labels below; `fuzz.py` reports coverage against
# this set.
ALL_PRODUCTIONS = frozenset({
    "nat.lit", "nat.var", "nat.proj1", "nat.proj2", "nat.length", "nat.headD",
    "nat.foldl", "nat.add", "nat.mul", "nat.sub", "nat.div", "nat.mod",
    "nat.if", "nat.match", "nat.let", "nat.toNat", "nat.natAbs",
    "bool.const", "bool.var", "bool.lt", "bool.le", "bool.gt", "bool.ge",
    "bool.eq", "bool.ne", "bool.and", "bool.or", "bool.not",
    "bool.ilt", "bool.ieq", "bool.isEmpty", "bool.elem",
    "list.nil", "list.var", "list.lit", "list.map", "list.filter",
    "list.reverse", "list.append", "list.cons", "list.match",
    "list.take", "list.drop", "list.foldr",
    "pair.mk",
    # Int
    "int.lit", "int.var", "int.ofNat", "int.neg", "int.add", "int.sub",
    "int.mul", "int.div", "int.mod", "int.if",
    # Option Nat
    "opt.none", "opt.some", "opt.var", "opt.getD", "opt.if", "opt.match",
    # String
    "str.lit", "str.var", "str.append", "str.push", "str.mk", "str.if",
    "str.let",
    # Char
    "char.lit", "char.var", "char.toUpper", "char.toLower", "char.if",
    # Array Nat
    "arr.lit", "arr.var", "arr.mk", "arr.push", "arr.append", "arr.if",
    # String/Char/Array observations returning Nat/Bool (added to those gens)
    "nat.strlen", "nat.arrsize", "nat.charToNat",
    "bool.strEmpty", "bool.charEq", "bool.charIsDigit", "bool.charIsAlpha",
    # List Int / List Bool / nested lists (element-type variety)
    "listint.lit", "listint.var", "listint.map", "listint.append",
    "listint.cons", "listint.reverse",
    "listbool.lit", "listbool.var", "listbool.map", "listbool.append",
    "listbool.cons", "listbool.reverse",
    "listlist.lit", "listlist.var", "listlist.map", "listlist.append",
    "listlist.cons", "listlist.reverse",
    "nat.listlistlen",  # observe a nested list's length back into Nat
})


class Gen:
    # k-path coverage (Havrikov & Zeller, ASE 2019, §"context-sensitive
    # coverage"): a single-production metric can't tell `map` inside a `match`
    # from `map` at top level.  We additionally track *paths* of up to KMAX
    # nested productions (e.g. `nat.match → list.map → nat.let`), so "did we test
    # a filter inside a foldr inside an if?" becomes measurable — and steer
    # generation toward not-yet-covered paths.
    KMAX = 3

    def __init__(self, seed, max_depth=4, covered=None, emi=0.0, kcovered=None):
        self.rng = random.Random(seed)
        self.max_depth = max_depth
        # Production labels offered / chosen so far (this file).  `covered` may
        # be shared in to seed the preference, but generation stays keyed on the
        # rng, so the output is a pure function of the seed.
        self.all_prods = set()
        self.covered = set(covered) if covered else set()
        # Context-sensitive coverage: `ctx` is the stack of production labels
        # from the root of the current subterm down to the node being generated;
        # `all_kpaths`/`kpaths` mirror `all_prods`/`covered` but for tuples of 2..
        # KMAX consecutive labels along that path.  Like `covered`, `kcovered`
        # may be seeded in to bias the preference, but choice stays rng-keyed.
        self.ctx = []
        self.all_kpaths = set()
        self.kpaths = set(kcovered) if kcovered else set()
        # EMI (equivalence modulo inputs, Le/Afshari/Su PLDI'14) + guided
        # stochastic mutation (Le/Sun/Su OOPSLA'15): `emi` is the per-subterm
        # probability of wrapping a just-generated expression in a
        # semantics-PRESERVING identity envelope (e.g. `x` -> `(x + 0)`).  The
        # result computes the same value, so the Lean oracle is unchanged, but
        # the transpiler sees a different — often deeper — term.  The *count* of
        # envelopes is stochastic (each subterm flips a coin) and *which*
        # envelope is chosen is coverage-guided via `choose`, so mutation steers
        # toward not-yet-covered productions rather than sampling blindly.
        self.emi = emi

    def pick(self, xs):
        return self.rng.choice(xs)

    def _kpaths_ending_with(self, label):
        """The 2..KMAX-length production paths that end at `label` given the
        current context stack (`self.ctx` holds the ancestor labels)."""
        paths = []
        for k in range(2, self.KMAX + 1):
            if len(self.ctx) >= k - 1:
                paths.append(tuple(self.ctx[-(k - 1):]) + (label,))
        return paths

    def choose(self, alts):
        """Pick among labeled alternatives, preferring not-yet-covered ones.

        `alts` is a list of `(label, thunk)`.  We record every offered label and
        prefer the subset whose labels are uncovered (systematic single-production
        coverage).  Among that pool we then prefer alternatives that would open a
        not-yet-covered *k-path* (a novel chain of nested productions), and break
        remaining ties with the seeded rng so the choice stays reproducible.
        """
        for (label, _) in alts:
            self.all_prods.add(label)
            for p in self._kpaths_ending_with(label):
                self.all_kpaths.add(p)
        uncovered = [(lbl, t) for (lbl, t) in alts if lbl not in self.covered]
        pool = uncovered if uncovered else alts
        # Secondary steer: within `pool`, favour labels that create a fresh
        # k-path in the current context.  Falls back to the whole pool when none
        # would (or when there's no context yet), so this never narrows below the
        # single-production preference.
        fresh = [(lbl, t) for (lbl, t) in pool
                 if any(p not in self.kpaths for p in self._kpaths_ending_with(lbl))]
        label, thunk = self.rng.choice(fresh if fresh else pool)
        self.covered.add(label)
        for p in self._kpaths_ending_with(label):
            self.kpaths.add(p)
        # Recurse with `label` pushed so children's k-paths see it as an ancestor.
        self.ctx.append(label)
        try:
            return thunk()
        finally:
            self.ctx.pop()

    # ---- expression generators, indexed by result type -------------------
    def gen(self, ty, env, depth):
        """env: list of (name, type) in scope. Returns a Lean expression str."""
        if ty == NAT:
            e = self.gen_nat(env, depth)
        elif ty == BOOL:
            e = self.gen_bool(env, depth)
        elif ty == LISTNAT:
            e = self.gen_list(env, depth)
        elif ty == PAIR:
            e = self.gen_pair(env, depth)
        elif ty == INT:
            e = self.gen_int(env, depth)
        elif ty == OPTNAT:
            e = self.gen_opt(env, depth)
        elif ty == STRING:
            e = self.gen_string(env, depth)
        elif ty == CHAR:
            e = self.gen_char(env, depth)
        elif ty == ARRAYNAT:
            e = self.gen_array(env, depth)
        elif ty == LISTINT:
            e = self.gen_list_elem(env, depth, LISTINT, INT, "listint")
        elif ty == LISTBOOL:
            e = self.gen_list_elem(env, depth, LISTBOOL, BOOL, "listbool")
        elif ty == LISTLISTNAT:
            e = self.gen_list_elem(env, depth, LISTLISTNAT, LISTNAT, "listlist")
        else:
            raise ValueError(ty)
        return self.maybe_envelope(ty, e)

    # EMI identity envelopes per type: each maps `x` to an expression that
    # provably computes the same value, so wrapping never changes the oracle.
    EMI_ENVELOPES = {
        NAT: [("emi.nat.add0", "({x} + 0)"), ("emi.nat.mul1", "({x} * 1)"),
              ("emi.nat.ite", "(if true then {x} else 0)"),
              ("emi.nat.projpair", "(({x}, 0).1)")],
        INT: [("emi.int.add0", "({x} + (0 : Int))"), ("emi.int.negneg", "(-(-({x})))"),
              ("emi.int.ite", "(if true then {x} else (0 : Int))")],
        BOOL: [("emi.bool.and", "({x} && true)"), ("emi.bool.notnot", "(!(!({x})))"),
               ("emi.bool.or", "(false || {x})")],
        LISTNAT: [("emi.list.appnil", "({x} ++ [])"), ("emi.list.nilapp", "([] ++ {x})"),
                  ("emi.list.revrev", "(({x} : List Nat).reverse.reverse)"),
                  ("emi.list.mapid", "(({x} : List Nat).map (fun z => z))")],
        OPTNAT: [("emi.opt.ite", "(if true then {x} else (none : Option Nat))")],
        PAIR: [("emi.pair.ite", "(if true then {x} else (0, 0))")],
        STRING: [("emi.str.appempty", '(({x} : String) ++ "")'),
                 ("emi.str.ite", '(if true then {x} else "")')],
        CHAR: [("emi.char.ite", "(if true then {x} else 'a')")],
        ARRAYNAT: [("emi.arr.ite", "(if true then {x} else (#[] : Array Nat))")],
    }

    def maybe_envelope(self, ty, expr):
        """With probability `self.emi`, wrap `expr` in a semantics-preserving
        identity envelope (EMI).  Envelope choice is coverage-guided."""
        if self.emi <= 0.0 or self.rng.random() >= self.emi:
            return expr
        alts = [(label, (lambda tpl=tpl: tpl.format(x=expr)))
                for (label, tpl) in self.EMI_ENVELOPES.get(ty, [])]
        if not alts:
            return expr
        return self.choose(alts)

    def vars_of(self, env, ty):
        return [n for (n, t) in env if t == ty]

    def gen_nat(self, env, depth):
        vs = self.vars_of(env, NAT)
        # Leaf productions (always available).
        alts = [("nat.lit", lambda: str(self.rng.randint(0, 9)))]
        for v in vs:
            alts.append(("nat.var", (lambda v=v: v)))
        for (n, t) in env:
            if t == PAIR:
                alts.append(("nat.proj1", (lambda n=n: f"{n}.1")))
                alts.append(("nat.proj2", (lambda n=n: f"{n}.2")))
            if t == LISTNAT:
                alts.append(("nat.length", (lambda n=n: f"{n}.length")))
                alts.append(("nat.headD", (lambda n=n: f"({n}.headD 0)")))
                alts.append(("nat.foldl", (lambda n=n: f"({n}.foldl (· + ·) 0)")))
            if t == STRING:
                alts.append(("nat.strlen", (lambda n=n: f"{n}.length")))
            if t == ARRAYNAT:
                alts.append(("nat.arrsize", (lambda n=n: f"{n}.size")))
            if t == CHAR:
                alts.append(("nat.charToNat", (lambda n=n: f"{n}.toNat")))
            if t == LISTINT or t == LISTBOOL or t == LISTLISTNAT:
                alts.append(("nat.listlistlen", (lambda n=n: f"{n}.length")))
        # Recursive productions (only while we have depth budget).
        if depth > 0 and self.rng.random() >= 0.35:
            def binop(op):
                a = self.gen(NAT, env, depth - 1)
                b = self.gen(NAT, env, depth - 1)
                if op in ("/", "%"):  # guard div/mod by zero
                    return f"({a} {op} ({b} + 1))"
                return f"({a} {op} {b})"
            alts += [
                ("nat.add", lambda: binop("+")), ("nat.mul", lambda: binop("*")),
                ("nat.sub", lambda: binop("-")), ("nat.div", lambda: binop("/")),
                ("nat.mod", lambda: binop("%")),
            ]

            def nat_if():
                c = self.gen(BOOL, env, depth - 1)
                a = self.gen(NAT, env, depth - 1)
                b = self.gen(NAT, env, depth - 1)
                return f"(if {c} then {a} else {b})"
            alts.append(("nat.if", nat_if))

            def nat_let():
                fresh = self.fresh(env)
                val = self.gen(NAT, env, depth - 1)
                body = self.gen(NAT, env + [(fresh, NAT)], depth - 1)
                return f"(let {fresh} := {val}; {body})"
            alts.append(("nat.let", nat_let))

            if vs:
                def nat_match():
                    n = self.pick(vs)
                    z = self.gen(NAT, env, depth - 1)
                    fresh = self.fresh(env)
                    s = self.gen(NAT, env + [(fresh, NAT)], depth - 1)
                    return f"(match {n} with | 0 => {z} | {fresh} + 1 => {s})"
                alts.append(("nat.match", nat_match))
            # Nat from Int: absolute value / clamp-to-Nat.
            alts.append(("nat.natAbs", lambda: f"({self.gen(INT, env, depth-1)}).natAbs"))
            alts.append(("nat.toNat", lambda: f"({self.gen(INT, env, depth-1)}).toNat"))
            # Nat from an Option Nat via getD (default).
            alts.append(("opt.getD",
                         lambda: f"(({self.gen(OPTNAT, env, depth-1)}).getD {self.gen(NAT, env, depth-1)})"))
        return self.choose(alts)

    def gen_bool(self, env, depth):
        vs = self.vars_of(env, BOOL)
        alts = [("bool.const", lambda: self.rng.choice(["true", "false"]))]
        for v in vs:
            alts.append(("bool.var", (lambda v=v: v)))
        if depth > 0 and self.rng.random() >= 0.35:
            def cmp(op, label):
                return (label, lambda: f"({self.gen(NAT, env, depth-1)} {op} {self.gen(NAT, env, depth-1)})")
            alts += [cmp("<", "bool.lt"), cmp("<=", "bool.le"), cmp(">", "bool.gt"),
                     cmp(">=", "bool.ge"), cmp("==", "bool.eq"), cmp("!=", "bool.ne")]

            def logic(op, label):
                return (label, lambda: f"({self.gen(BOOL, env, depth-1)} {op} {self.gen(BOOL, env, depth-1)})")
            alts += [logic("&&", "bool.and"), logic("||", "bool.or")]
            alts.append(("bool.not", lambda: f"(!{self.gen(BOOL, env, depth-1)})"))
            # Int comparisons and list predicates.
            alts.append(("bool.ilt",
                         lambda: f"(decide ({self.gen(INT, env, depth-1)} < {self.gen(INT, env, depth-1)}))"))
            alts.append(("bool.ieq",
                         lambda: f"(decide ({self.gen(INT, env, depth-1)} == {self.gen(INT, env, depth-1)}))"))
            # Annotate the list operand: a bare `[]` receiver is ambiguous for
            # `.isEmpty`/`.contains`, so pin it to `List Nat`.
            alts.append(("bool.isEmpty",
                         lambda: f"(({self.gen(LISTNAT, env, depth-1)} : List Nat)).isEmpty"))
            alts.append(("bool.elem",
                         lambda: f"(({self.gen(LISTNAT, env, depth-1)} : List Nat)).contains {self.gen(NAT, env, depth-1)}"))
            # String / Char predicates — exercise String.isEmpty and the Char
            # classification handlers (Char.isDigit/isAlpha) that are never hit by
            # numeric code.  These are prime spots for Lean-vs-Python semantic
            # divergence, so make them reachable.
            alts.append(("bool.strEmpty",
                         lambda: f"({self.gen(STRING, env, depth-1)}).isEmpty"))
            alts.append(("bool.charEq",
                         lambda: f"({self.gen(CHAR, env, depth-1)} == {self.gen(CHAR, env, depth-1)})"))
            alts.append(("bool.charIsDigit",
                         lambda: f"({self.gen(CHAR, env, depth-1)}).isDigit"))
            alts.append(("bool.charIsAlpha",
                         lambda: f"({self.gen(CHAR, env, depth-1)}).isAlpha"))
        return self.choose(alts)

    def gen_list(self, env, depth):
        vs = self.vars_of(env, LISTNAT)
        alts = [
            ("list.nil", lambda: "[]"),
            ("list.lit", lambda: "[" + ", ".join(
                str(self.rng.randint(0, 9)) for _ in range(self.rng.randint(0, 3))) + "]"),
        ]
        for v in vs:
            alts.append(("list.var", (lambda v=v: v)))
        if depth > 0 and self.rng.random() >= 0.35:
            if vs:
                def list_map():
                    n = self.pick(vs)
                    fresh = self.fresh(env)
                    return f"({n}.map (fun {fresh} => {self.gen(NAT, env + [(fresh, NAT)], depth-1)}))"
                alts.append(("list.map", list_map))

                def list_filter():
                    n = self.pick(vs)
                    fresh = self.fresh(env)
                    return f"({n}.filter (fun {fresh} => {self.gen(BOOL, env + [(fresh, NAT)], depth-1)}))"
                alts.append(("list.filter", list_filter))
                alts.append(("list.reverse", (lambda: f"({self.pick(vs)}.reverse)")))

                def list_match():
                    n = self.pick(vs)
                    nil = self.gen(LISTNAT, env, depth - 1)
                    hd, tl = self.fresh(env), self.fresh(env, offset=1)
                    cons = self.gen(LISTNAT, env + [(hd, NAT), (tl, LISTNAT)], depth - 1)
                    return f"(match {n} with | [] => {nil} | {hd} :: {tl} => {cons})"
                alts.append(("list.match", list_match))
            alts.append(("list.append",
                         lambda: f"({self.gen(LISTNAT, env, depth-1)} ++ {self.gen(LISTNAT, env, depth-1)})"))
            alts.append(("list.cons",
                         lambda: f"({self.gen(NAT, env, depth-1)} :: {self.gen(LISTNAT, env, depth-1)})"))
            if vs:
                alts.append(("list.take",
                             lambda: f"({self.pick(vs)}.take {self.gen(NAT, env, depth-1)})"))
                alts.append(("list.drop",
                             lambda: f"({self.pick(vs)}.drop {self.gen(NAT, env, depth-1)})"))

                def list_foldr():
                    # foldr prepending mapped elements: builds a list.
                    n = self.pick(vs)
                    fresh = self.fresh(env)
                    acc = self.fresh(env, offset=1)
                    init = self.gen(LISTNAT, env, depth - 1)
                    body = self.gen(NAT, env + [(fresh, NAT), (acc, LISTNAT)], depth - 1)
                    return f"({n}.foldr (fun {fresh} {acc} => {body} :: {acc}) {init})"
                alts.append(("list.foldr", list_foldr))
        return self.choose(alts)

    def gen_pair(self, env, depth):
        def mk():
            a = self.gen(NAT, env, max(depth - 1, 0))
            b = self.gen(NAT, env, max(depth - 1, 0))
            return f"({a}, {b})"
        return self.choose([("pair.mk", mk)])

    def gen_int(self, env, depth):
        vs = self.vars_of(env, INT)
        alts = [("int.lit", lambda: f"({self.rng.randint(-9, 9)} : Int)")]
        for v in vs:
            alts.append(("int.var", (lambda v=v: v)))
        # Int from a Nat (coercion).
        alts.append(("int.ofNat", lambda: f"(({self.gen(NAT, env, max(depth-1, 0))} : Nat) : Int)"))
        if depth > 0 and self.rng.random() >= 0.35:
            def ibin(op):
                a = self.gen(INT, env, depth - 1)
                b = self.gen(INT, env, depth - 1)
                if op in ("/", "%"):  # guard div/mod by zero: nonzero divisor
                    return f"({a} {op} (if {b} == 0 then 1 else {b}))"
                return f"({a} {op} {b})"
            alts += [
                ("int.add", lambda: ibin("+")), ("int.sub", lambda: ibin("-")),
                ("int.mul", lambda: ibin("*")), ("int.div", lambda: ibin("/")),
                ("int.mod", lambda: ibin("%")),
            ]
            alts.append(("int.neg", lambda: f"(-{self.gen(INT, env, depth-1)})"))

            def int_if():
                c = self.gen(BOOL, env, depth - 1)
                a = self.gen(INT, env, depth - 1)
                b = self.gen(INT, env, depth - 1)
                return f"(if {c} then {a} else {b})"
            alts.append(("int.if", int_if))
        return self.choose(alts)

    def gen_opt(self, env, depth):
        vs = self.vars_of(env, OPTNAT)
        alts = [
            ("opt.none", lambda: "(none : Option Nat)"),
            ("opt.some", lambda: f"(some {self.gen(NAT, env, max(depth-1, 0))})"),
        ]
        for v in vs:
            alts.append(("opt.var", (lambda v=v: v)))
        if depth > 0 and self.rng.random() >= 0.35:
            def opt_if():
                c = self.gen(BOOL, env, depth - 1)
                a = self.gen(OPTNAT, env, depth - 1)
                b = self.gen(OPTNAT, env, depth - 1)
                return f"(if {c} then {a} else {b})"
            alts.append(("opt.if", opt_if))
            if vs:
                def opt_match():
                    n = self.pick(vs)
                    none_e = self.gen(OPTNAT, env, depth - 1)
                    fresh = self.fresh(env)
                    some_e = self.gen(OPTNAT, env + [(fresh, NAT)], depth - 1)
                    return f"(match {n} with | none => {none_e} | some {fresh} => {some_e})"
                alts.append(("opt.match", opt_match))
        return self.choose(alts)

    # A small ASCII alphabet for string/char literals — kept to letters+digits so
    # generated Lean string/char literals never need escaping (no `"`, `\`,
    # newline) and Char predicate semantics stay on well-defined ASCII.  (Widening
    # to punctuation/Unicode later is exactly how to surface Char.isAlpha-style
    # Lean-vs-Python divergences.)
    _ALPHABET = "abcXYZ019"

    def _str_lit(self):
        n = self.rng.randint(0, 4)
        return "".join(self.rng.choice(self._ALPHABET) for _ in range(n))

    def gen_string(self, env, depth):
        vs = self.vars_of(env, STRING)
        alts = [("str.lit", lambda: f'"{self._str_lit()}"')]
        for v in vs:
            alts.append(("str.var", (lambda v=v: v)))
        if depth > 0 and self.rng.random() >= 0.35:
            alts.append(("str.append",
                         lambda: f"({self.gen(STRING, env, depth-1)} ++ {self.gen(STRING, env, depth-1)})"))
            alts.append(("str.push",
                         lambda: f"({self.gen(STRING, env, depth-1)}.push {self.gen(CHAR, env, depth-1)})"))
            # String.mk from a List Char isn't easily generated (no List Char
            # type), so build a singleton via toString of a char instead.
            alts.append(("str.mk",
                         lambda: f"(String.mk [{self.gen(CHAR, env, depth-1)}])"))

            def str_if():
                c = self.gen(BOOL, env, depth - 1)
                a = self.gen(STRING, env, depth - 1)
                b = self.gen(STRING, env, depth - 1)
                return f"(if {c} then {a} else {b})"
            alts.append(("str.if", str_if))

            def str_let():
                fresh = self.fresh(env)
                val = self.gen(STRING, env, depth - 1)
                body = self.gen(STRING, env + [(fresh, STRING)], depth - 1)
                return f"(let {fresh} := {val}; {body})"
            alts.append(("str.let", str_let))
        return self.choose(alts)

    def gen_char(self, env, depth):
        vs = self.vars_of(env, CHAR)
        alts = [("char.lit", lambda: f"'{self.rng.choice(self._ALPHABET)}'")]
        for v in vs:
            alts.append(("char.var", (lambda v=v: v)))
        if depth > 0 and self.rng.random() >= 0.35:
            alts.append(("char.toUpper", lambda: f"({self.gen(CHAR, env, depth-1)}).toUpper"))
            alts.append(("char.toLower", lambda: f"({self.gen(CHAR, env, depth-1)}).toLower"))

            def char_if():
                c = self.gen(BOOL, env, depth - 1)
                a = self.gen(CHAR, env, depth - 1)
                b = self.gen(CHAR, env, depth - 1)
                return f"(if {c} then {a} else {b})"
            alts.append(("char.if", char_if))
        return self.choose(alts)

    def gen_array(self, env, depth):
        vs = self.vars_of(env, ARRAYNAT)
        alts = [
            ("arr.lit", lambda: "#[" + ", ".join(
                str(self.rng.randint(0, 9)) for _ in range(self.rng.randint(0, 3))) + "]"),
            # `#[]` alone is ambiguous; annotate an empty literal.
            ("arr.mk", lambda: "(#[] : Array Nat)"),
        ]
        for v in vs:
            alts.append(("arr.var", (lambda v=v: v)))
        if depth > 0 and self.rng.random() >= 0.35:
            alts.append(("arr.push",
                         lambda: f"({self.gen(ARRAYNAT, env, depth-1)}.push {self.gen(NAT, env, depth-1)})"))
            alts.append(("arr.append",
                         lambda: f"({self.gen(ARRAYNAT, env, depth-1)} ++ {self.gen(ARRAYNAT, env, depth-1)})"))

            def arr_if():
                c = self.gen(BOOL, env, depth - 1)
                a = self.gen(ARRAYNAT, env, depth - 1)
                b = self.gen(ARRAYNAT, env, depth - 1)
                return f"(if {c} then {a} else {b})"
            alts.append(("arr.if", arr_if))
        return self.choose(alts)

    def gen_list_elem(self, env, depth, listty, elemty, tag):
        """Generate a `List <elemty>` expression.  Parameterized over the element
        type so `List Int`/`List Bool`/`List (List Nat)` reuse one generator and
        exercise the list combinators (map/append/cons/reverse) over non-Nat
        elements.  A typed empty literal (`([] : listty)`) keeps Lean from
        defaulting `[]` to `List Nat`."""
        vs = self.vars_of(env, listty)
        alts = [(f"{tag}.lit", lambda: self._list_elem_lit(listty, elemty))]
        for v in vs:
            alts.append((f"{tag}.var", (lambda v=v: v)))
        if depth > 0 and self.rng.random() >= 0.35:
            if vs:
                def lmap():
                    n = self.pick(vs)
                    fresh = self.fresh(env)
                    # map each element to a fresh element of the same type.
                    body = self.gen(elemty, env + [(fresh, elemty)], depth - 1)
                    return f"({n}.map (fun {fresh} => {body}))"
                alts.append((f"{tag}.map", lmap))
                alts.append((f"{tag}.reverse", (lambda: f"({self.pick(vs)}.reverse)")))
            alts.append((f"{tag}.append",
                         lambda: f"({self.gen(listty, env, depth-1)} ++ {self.gen(listty, env, depth-1)})"))
            alts.append((f"{tag}.cons",
                         lambda: f"({self.gen(elemty, env, depth-1)} :: {self.gen(listty, env, depth-1)})"))
        return self.choose(alts)

    def _list_elem_lit(self, listty, elemty):
        """A typed list literal, e.g. `([(-1 : Int), 2])` or `([] : List Bool)`."""
        n = self.rng.randint(0, 3)
        if n == 0:
            return f"(([] : {listty}))"
        elems = ", ".join(self._elem_lit(elemty) for _ in range(n))
        return f"[{elems}]"

    def _elem_lit(self, elemty):
        if elemty == INT:
            return f"({self.rng.randint(-9, 9)} : Int)"
        if elemty == BOOL:
            return self.rng.choice(["true", "false"])
        if elemty == LISTNAT:
            return "[" + ", ".join(str(self.rng.randint(0, 9))
                                   for _ in range(self.rng.randint(0, 3))) + "]"
        return str(self.rng.randint(0, 9))

    _counter = 0

    def fresh(self, env, offset=0):
        # produce a name not shadowing existing binders
        while True:
            self._counter += 1
            name = f"v{self._counter}"
            if name not in [n for (n, _) in env]:
                if offset == 0:
                    return name
                offset -= 1

    # ---- whole function definitions --------------------------------------
    def gen_def(self, idx, prefix=""):
        # `prefix` namespaces the function/param names so many seeds can be
        # packed into one Lean file (batching) without name clashes; empty for
        # the single-seed case.
        nparams = self.rng.randint(1, 3)
        params = []
        for i in range(nparams):
            pty = self.pick(LEAN_TYPES)
            params.append((f"{prefix}p{idx}_{i}", pty))
        ret = self.pick(LEAN_TYPES)
        env = list(params)
        body = self.gen(ret, env, self.max_depth)
        name = f"{prefix}gen{idx}"
        sig = " ".join(f"({n} : {t})" for (n, t) in params)
        src = f"def {name} {sig} : {ret} :=\n  {body}"
        return name, params, ret, src

    # ---- oracle input generation -----------------------------------------
    def rand_value(self, ty):
        if ty == NAT:
            return self.rng.randint(0, 12)
        if ty == BOOL:
            return self.rng.choice([True, False])
        if ty == LISTNAT:
            return [self.rng.randint(0, 9) for _ in range(self.rng.randint(0, 5))]
        if ty == PAIR:
            return [self.rng.randint(0, 12), self.rng.randint(0, 12)]
        if ty == INT:
            # deliberately include negatives — that's where Int div/mod bites
            return self.rng.randint(-12, 12)
        if ty == OPTNAT:
            return None if self.rng.random() < 0.3 else self.rng.randint(0, 12)
        if ty == STRING:
            return "".join(self.rng.choice(self._ALPHABET)
                           for _ in range(self.rng.randint(0, 5)))
        if ty == CHAR:
            return self.rng.choice(self._ALPHABET)
        if ty == ARRAYNAT:
            return [self.rng.randint(0, 9) for _ in range(self.rng.randint(0, 5))]
        if ty == LISTINT:
            return [self.rng.randint(-9, 9) for _ in range(self.rng.randint(0, 5))]
        if ty == LISTBOOL:
            return [self.rng.choice([True, False]) for _ in range(self.rng.randint(0, 5))]
        if ty == LISTLISTNAT:
            return [[self.rng.randint(0, 9) for _ in range(self.rng.randint(0, 3))]
                    for _ in range(self.rng.randint(0, 3))]
        raise ValueError(ty)


# JSON-escape a Python string for embedding in a Lean string literal (must match
# how `json.dumps` escapes, since the oracle serializer output is compared to the
# JSON of the input value).  Only `"` and `\` occur in our alphabet-restricted
# strings today, but escape the full set so widening the alphabet stays safe.
def _lean_str_escape(s):
    return (s.replace("\\", "\\\\").replace('"', '\\"')
             .replace("\n", "\\n").replace("\t", "\\t"))


def lean_lit(ty, v):
    if ty == NAT:
        return str(v)
    if ty == BOOL:
        return "true" if v else "false"
    if ty == LISTNAT:
        return "[" + ", ".join(str(x) for x in v) + "]"
    if ty == PAIR:
        return f"({v[0]}, {v[1]})"
    if ty == INT:
        return f"({v} : Int)"
    if ty == OPTNAT:
        return "(none : Option Nat)" if v is None else f"(some {v} : Option Nat)"
    if ty == STRING:
        return f'"{_lean_str_escape(v)}"'
    if ty == CHAR:
        return f"'{v}'"
    if ty == ARRAYNAT:
        return "#[" + ", ".join(str(x) for x in v) + "]"
    if ty == LISTINT:
        if not v:
            return "([] : List Int)"
        return "[" + ", ".join(f"({x} : Int)" for x in v) + "]"
    if ty == LISTBOOL:
        if not v:
            return "([] : List Bool)"
        return "[" + ", ".join("true" if x else "false" for x in v) + "]"
    if ty == LISTLISTNAT:
        inner = ", ".join("[" + ", ".join(str(x) for x in row) + "]" for row in v)
        return f"([{inner}] : List (List Nat))"
    raise ValueError(ty)


def json_lit(_ty, v):
    import json
    return json.dumps(v)


def serializer_call(ty, expr):
    if ty == NAT:
        return f"jNat ({expr})"
    if ty == BOOL:
        return f"jBool ({expr})"
    if ty == LISTNAT:
        return f"jListNat ({expr})"
    if ty == PAIR:
        return f"jPair ({expr})"
    if ty == INT:
        return f"jInt ({expr})"
    if ty == OPTNAT:
        return f"jOpt ({expr})"
    if ty == STRING:
        return f"jString ({expr})"
    if ty == CHAR:
        return f"jChar ({expr})"
    if ty == ARRAYNAT:
        return f"jArrayNat ({expr})"
    if ty == LISTINT:
        return f"jListInt ({expr})"
    if ty == LISTBOOL:
        return f"jListBool ({expr})"
    if ty == LISTLISTNAT:
        return f"jListListNat ({expr})"
    raise ValueError(ty)


PRELUDE = r"""import LeanToPython
open Lean LeanToPython

-- Batched files pack many functions + hundreds of oracle-row statements into one
-- `#eval do` block, which overflows the default elaborator recursion limit.
set_option maxRecDepth 100000

def jNat (n : Nat) : String := toString n
def jBool (b : Bool) : String := if b then "true" else "false"
def jListNat (xs : List Nat) : String :=
  "[" ++ String.intercalate "," (xs.map toString) ++ "]"
def jPair : Nat × Nat → String
  | (a, b) => "[" ++ toString a ++ "," ++ toString b ++ "]"
def jInt (n : Int) : String := toString n
def jOpt : Option Nat → String
  | none => "null"
  | some n => toString n
-- JSON-escape a string so the oracle row is valid JSON that Python's
-- `json.loads` parses back to the same value, matching `json.dumps`.  Besides
-- quote/backslash/named controls, JSON forbids ALL raw control chars (<0x20) —
-- they must be `\uXXXX`.  Corpus functions like `Strings.fromAsciiCodes`/`chr`
-- readily produce such chars, so escape the whole <0x20 range (else json.loads
-- raises "Invalid control character").
def jHex4 (n : Nat) : String :=
  let d := fun (k : Nat) => "0123456789abcdef".toList[k % 16]!.toString
  "\\u00" ++ d (n / 16) ++ d n
def jStrEscape (s : String) : String :=
  s.foldl (fun acc c =>
    acc ++ (match c with
      | '"'  => "\\\""
      | '\\' => "\\\\"
      | '\n' => "\\n"
      | '\t' => "\\t"
      | '\r' => "\\r"
      | _    => if c.toNat < 0x20 then jHex4 c.toNat else c.toString)) ""
def jString (s : String) : String := "\"" ++ jStrEscape s ++ "\""
def jChar (c : Char) : String := jString c.toString
def jArrayNat (xs : Array Nat) : String :=
  "[" ++ String.intercalate "," (xs.toList.map toString) ++ "]"
def jListInt (xs : List Int) : String :=
  "[" ++ String.intercalate "," (xs.map toString) ++ "]"
def jListBool (xs : List Bool) : String :=
  "[" ++ String.intercalate "," (xs.map (fun b => if b then "true" else "false")) ++ "]"
def jListListNat (xss : List (List Nat)) : String :=
  "[" ++ String.intercalate "," (xss.map jListNat) ++ "]"
"""


def _gen_defs_for_seed(seed, ndefs, emi, prefix=""):
    """Generate `ndefs` definitions for one seed. Returns (Gen, defs)."""
    g = Gen(seed, emi=emi)
    defs = [g.gen_def(i, prefix=prefix) for i in range(ndefs)]
    return g, defs


def single_def_body(seed, ninputs, emi=0.0):
    """For the structural shrinker: return `(orig_body, rebuild)` for this seed's
    FIRST def, where `rebuild(body_str)` produces a complete single-def Lean file
    with the def's body replaced by `body_str` (params / return type / oracle
    inputs unchanged).

    The rng is consumed in exactly the same order as `emit_lean_file(seed, 1,
    ninputs)` — `gen_def(0)` then `_oracle_rows` — so `rebuild(orig_body)` is
    byte-identical to that file.  Because the oracle calls the def by name on
    fixed literal args and Lean *recomputes* the expected value at elaboration
    time, ANY body rewrite keeps the differential check valid: a rewrite is kept
    only if the transpiler bug still reproduces (see `struct_shrink`)."""
    g = Gen(seed, emi=emi)
    name, params, ret, src = g.gen_def(0)
    # `gen_def` emits `def NAME SIG : RET :=\n  BODY`; recover BODY.
    marker = ":=\n  "
    orig_body = src[src.index(marker) + len(marker):]
    sig = " ".join(f"({n} : {t})" for (n, t) in params)
    # Freeze the oracle rows ONCE (they consume the rng): every `rebuild` must
    # reuse the SAME input literals, or shrinking would compare against a moving
    # oracle.  Rebuilding just swaps the body text; the def name and call sites
    # are unchanged, so the frozen rows still call it correctly.
    frozen_rows = _oracle_rows(g, [(name, params, ret, src)], ninputs)

    def rebuild(body):
        newdef = (name, params, ret,
                  f"def {name} {sig} : {ret} :=\n  {body}")
        return _assemble([newdef], frozen_rows)

    return orig_body, rebuild, [n for (n, _) in params]


def _oracle_rows(g, defs, ninputs):
    """Lean `IO.println` lines emitting ORACLE rows for `defs`."""
    rows = []
    for (name, params, ret, _) in defs:
        for _ in range(ninputs):
            vals = [g.rand_value(t) for (_, t) in params]
            lean_args = " ".join(f"({lean_lit(t, v)})" for ((_, t), v) in zip(params, vals))
            json_args = "[" + ",".join(json_lit(t, v) for ((_, t), v) in zip(params, vals)) + "]"
            # `json_args` is embedded inside a Lean string literal, so escape any
            # `"`/`\` it contains (JSON strings for String/Char args have quotes).
            # fuzz.py parses the row by splitting on the literal tab, then
            # json.loads() the field — which un-escapes back to the original.
            json_args_esc = _lean_str_escape(json_args)
            call = f"{name} {lean_args}" if params else name
            ser = serializer_call(ret, call)
            rows.append(f'  IO.println ("ORACLE\\t{name}\\t{json_args_esc}\\t" ++ {ser})')
    return rows


def _eval_block(defs, rows, tag=""):
    """Lines for one `#eval` driver: emit the transpiled Python (### PYTHON) and
    the oracle rows (### ORACLE) for `defs`.  `tag` (a seed id) is appended to
    the banners so a batched file's output can be split back apart per seed.

    Crucially, this is ONE `#eval` per call: a type error in any def here makes
    *this* block abort (Lean evaluates it against the `sorry` axiom), but a
    sibling block in the same file is unaffected.  Batching therefore puts each
    seed in its own block so a single ill-typed seed drops only its own rows
    instead of poisoning the whole file."""
    suffix = f" {tag}" if tag != "" else ""
    names = ", ".join("`" + name for (name, _, _, _) in defs)
    block = [
        "#eval show CoreM Unit from do",
        f'  IO.println "### PYTHON{suffix}"',
        f"  IO.println (← emitPythonForNames `Fuzz [{names}])",
        f'  IO.println "### ORACLE{suffix}"',
    ]
    block += rows
    return block


def _assemble(all_defs, all_rows):
    """Build a single-`#eval` Lean file from def source blocks and oracle rows."""
    parts = [PRELUDE, ""]
    parts += [src for (_, _, _, src) in all_defs]
    parts.append("")
    parts += _eval_block(all_defs, all_rows)
    return "\n".join(parts) + "\n"


def emit_lean_file(seed, ndefs, ninputs, covered=None, emi=0.0):  # noqa: E302
    """Emit the Lean file for a single `seed`.

    Generation is a pure function of `(seed, emi)`, so `fuzz.py`
    reproduces/shrinks a failure by re-passing the same values.  The Gen's
    `all_prods` / `covered` are exposed via `emit_lean_file.last_gen` for the
    caller to aggregate coverage.
    """
    g, defs = _gen_defs_for_seed(seed, ndefs, emi)
    setattr(emit_lean_file, "last_gen", g)
    return _assemble(defs, _oracle_rows(g, defs, ninputs))


def emit_batch_file(seeds, ndefs, ninputs, emi=0.0):
    """Pack several seeds' functions into ONE Lean file, amortizing Lean's
    ~1s process-startup cost (which dominates per-file runtime) across many
    functions.  Each seed's names are prefixed `s{seed}_` so a failing function
    identifies its seed, and each seed keeps its own `Gen` (so a single seed is
    still reproducible standalone).

    Each seed gets its OWN `#eval` block (banners tagged with the seed id).  A
    type error in one seed's defs aborts only that seed's block — its siblings
    still elaborate and print — so an ill-typed seed drops just its own rows
    instead of poisoning the whole batch.  (A single shared `#eval` would abort
    entirely on the first bad def via the `sorry` axiom.)

    Returns (lean_src, {seed: (all_prods, covered, all_kpaths, kpaths)})."""
    all_defs, blocks, cov = [], [], {}
    for seed in seeds:
        g, defs = _gen_defs_for_seed(seed, ndefs, emi, prefix=f"s{seed}_")
        all_defs += defs
        rows = _oracle_rows(g, defs, ninputs)
        blocks += _eval_block(defs, rows, tag=str(seed))
        cov[seed] = (frozenset(g.all_prods), frozenset(g.covered),
                     frozenset(g.all_kpaths), frozenset(g.kpaths))
    parts = [PRELUDE, ""]
    parts += [src for (_, _, _, src) in all_defs]
    parts.append("")
    parts += blocks
    return "\n".join(parts) + "\n", cov


def main():
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    ndefs = int(sys.argv[2]) if len(sys.argv) > 2 else 8
    ninputs = int(sys.argv[3]) if len(sys.argv) > 3 else 5
    emi = float(sys.argv[4]) if len(sys.argv) > 4 else 0.0
    sys.stdout.write(emit_lean_file(seed, ndefs, ninputs, emi=emi))


if __name__ == "__main__":
    main()
