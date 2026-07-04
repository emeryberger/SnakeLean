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
NAT, BOOL, LISTNAT, PAIR = "Nat", "Bool", "List Nat", "Nat × Nat"
LEAN_TYPES = [NAT, BOOL, LISTNAT, PAIR]

# Every production label the grammar can emit — the coverage universe.  Kept in
# sync with the `choose(...)` labels below; `fuzz.py` reports coverage against
# this set.
ALL_PRODUCTIONS = frozenset({
    "nat.lit", "nat.var", "nat.proj1", "nat.proj2", "nat.length", "nat.headD",
    "nat.foldl", "nat.add", "nat.mul", "nat.sub", "nat.div", "nat.mod",
    "nat.if", "nat.match", "nat.let",
    "bool.const", "bool.var", "bool.lt", "bool.le", "bool.gt", "bool.ge",
    "bool.eq", "bool.ne", "bool.and", "bool.or", "bool.not",
    "list.nil", "list.var", "list.lit", "list.map", "list.filter",
    "list.reverse", "list.append", "list.cons", "list.match",
    "pair.mk",
})


class Gen:
    def __init__(self, seed, max_depth=4, covered=None):
        self.rng = random.Random(seed)
        self.max_depth = max_depth
        # Production labels offered / chosen so far (this file).  `covered` may
        # be shared in to seed the preference, but generation stays keyed on the
        # rng, so the output is a pure function of the seed.
        self.all_prods = set()
        self.covered = set(covered) if covered else set()

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
            return self.gen_nat(env, depth)
        if ty == BOOL:
            return self.gen_bool(env, depth)
        if ty == LISTNAT:
            return self.gen_list(env, depth)
        if ty == PAIR:
            return self.gen_pair(env, depth)
        raise ValueError(ty)

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
        return self.choose(alts)

    def gen_pair(self, env, depth):
        def mk():
            a = self.gen(NAT, env, max(depth - 1, 0))
            b = self.gen(NAT, env, max(depth - 1, 0))
            return f"({a}, {b})"
        return self.choose([("pair.mk", mk)])

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
    raise ValueError(ty)


PRELUDE = r"""import LeanToPython
open Lean LeanToPython

def jNat (n : Nat) : String := toString n
def jBool (b : Bool) : String := if b then "true" else "false"
def jListNat (xs : List Nat) : String :=
  "[" ++ String.intercalate "," (xs.map toString) ++ "]"
def jPair : Nat × Nat → String
  | (a, b) => "[" ++ toString a ++ "," ++ toString b ++ "]"
"""


def emit_lean_file(seed, ndefs, ninputs, covered=None):  # noqa: E302
    """Emit the Lean file for `seed`.

    `covered` optionally seeds the coverage-preference (labels already exercised
    by earlier files in the sweep), steering this file toward fresh productions.
    Generation is still a pure function of `seed` given the same `covered`, so
    `fuzz.py` reproduces/shrinks a failure by re-passing the same `covered`.
    The Gen's `all_prods` / `covered` are exposed via `emit_lean_file.last_gen`
    for the caller to aggregate coverage.
    """
    g = Gen(seed, covered=covered)
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
    sys.stdout.write(emit_lean_file(seed, ndefs, ninputs))


if __name__ == "__main__":
    main()
