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
LEAN_TYPES = [NAT, BOOL, LISTNAT, PAIR, INT, OPTNAT]

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
})


class Gen:
    def __init__(self, seed, max_depth=4, covered=None, emi=0.0):
        self.rng = random.Random(seed)
        self.max_depth = max_depth
        # Production labels offered / chosen so far (this file).  `covered` may
        # be shared in to seed the preference, but generation stays keyed on the
        # rng, so the output is a pure function of the seed.
        self.all_prods = set()
        self.covered = set(covered) if covered else set()
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

    def choose(self, alts):
        """Pick among labeled alternatives, preferring not-yet-covered ones.

        `alts` is a list of `(label, thunk)`.  We record every offered label,
        prefer the subset whose labels are uncovered (systematic coverage), and
        break ties with the seeded rng so the choice stays reproducible.
        """
        for (label, _) in alts:
            self.all_prods.add(label)
        uncovered = [(l, t) for (l, t) in alts if l not in self.covered]
        pool = uncovered if uncovered else alts
        label, thunk = self.rng.choice(pool)
        self.covered.add(label)
        return thunk()

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
    def gen_def(self, idx):
        nparams = self.rng.randint(1, 3)
        params = []
        for i in range(nparams):
            pty = self.pick(LEAN_TYPES)
            params.append((f"p{idx}_{i}", pty))
        ret = self.pick(LEAN_TYPES)
        env = list(params)
        body = self.gen(ret, env, self.max_depth)
        name = f"gen{idx}"
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
        raise ValueError(ty)


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
    raise ValueError(ty)


PRELUDE = r"""import LeanToPython
open Lean LeanToPython

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
"""


def emit_lean_file(seed, ndefs, ninputs, covered=None, emi=0.0):  # noqa: E302
    """Emit the Lean file for `seed`.

    `covered` optionally seeds the coverage-preference (labels already exercised
    by earlier files in the sweep), steering this file toward fresh productions.
    `emi` (0..1) is the per-subterm EMI envelope probability.  Generation is
    still a pure function of `(seed, emi)`, so `fuzz.py` reproduces/shrinks a
    failure by re-passing the same values.  The Gen's `all_prods` / `covered`
    are exposed via `emit_lean_file.last_gen` for the caller to aggregate
    coverage.
    """
    g = Gen(seed, covered=covered, emi=emi)
    setattr(emit_lean_file, "last_gen", g)
    defs = [g.gen_def(i) for i in range(ndefs)]
    parts = [PRELUDE, ""]
    for _, _, _, src in defs:
        parts.append(src)
    parts.append("")
    # driver
    names = ", ".join("`" + name for (name, _, _, _) in defs)
    parts.append("#eval show CoreM Unit from do")
    parts.append(f"  IO.println \"### PYTHON\"")
    parts.append(f"  IO.println (← emitPythonForNames `Fuzz [{names}])")
    parts.append(f"  IO.println \"### ORACLE\"")
    for (name, params, ret, _) in defs:
        for _ in range(ninputs):
            vals = [g.rand_value(t) for (_, t) in params]
            lean_args = " ".join(f"({lean_lit(t, v)})" for ((_, t), v) in zip(params, vals))
            json_args = "[" + ",".join(json_lit(t, v) for ((_, t), v) in zip(params, vals)) + "]"
            call = f"{name} {lean_args}" if params else name
            ser = serializer_call(ret, call)
            # row: python-name TAB json-args TAB json-result
            row = f'"ORACLE\\t{name}\\t{json_args}\\t" ++ {ser}'
            parts.append(f"  IO.println ({row})")
    return "\n".join(parts) + "\n"


def main():
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    ndefs = int(sys.argv[2]) if len(sys.argv) > 2 else 8
    ninputs = int(sys.argv[3]) if len(sys.argv) > 3 else 5
    emi = float(sys.argv[4]) if len(sys.argv) > 4 else 0.0
    sys.stdout.write(emit_lean_file(seed, ndefs, ninputs, emi=emi))


if __name__ == "__main__":
    main()
