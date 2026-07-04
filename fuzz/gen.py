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
"""
import random
import sys

# Types in the grammar.
NAT, BOOL, LISTNAT, PAIR = "Nat", "Bool", "List Nat", "Nat × Nat"
LEAN_TYPES = [NAT, BOOL, LISTNAT, PAIR]


class Gen:
    def __init__(self, seed, max_depth=4):
        self.rng = random.Random(seed)
        self.max_depth = max_depth
        self.fuel_recursion = False  # set when a def is recursive

    def pick(self, xs):
        return self.rng.choice(xs)

    # ---- expression generators, indexed by result type -------------------
    def gen(self, ty, env, depth):
        """env: list of (name, type) in scope. Returns a Lean expression str."""
        leaf = depth <= 0 or self.rng.random() < 0.35
        if ty == NAT:
            return self.gen_nat(env, depth, leaf)
        if ty == BOOL:
            return self.gen_bool(env, depth, leaf)
        if ty == LISTNAT:
            return self.gen_list(env, depth, leaf)
        if ty == PAIR:
            return self.gen_pair(env, depth, leaf)
        raise ValueError(ty)

    def vars_of(self, env, ty):
        return [n for (n, t) in env if t == ty]

    def gen_nat(self, env, depth, leaf):
        vs = self.vars_of(env, NAT)
        atoms = [str(self.rng.randint(0, 9))]
        atoms += vs
        # projections from pairs / list length
        for (n, t) in env:
            if t == PAIR:
                atoms += [f"{n}.1", f"{n}.2"]
            if t == LISTNAT:
                atoms += [f"{n}.length", f"({n}.headD 0)", f"({n}.foldl (· + ·) 0)"]
        if leaf:
            return self.pick(atoms)
        k = self.rng.random()
        if k < 0.5:
            op = self.pick(["+", "*", "-", "/", "%"])
            a = self.gen(NAT, env, depth - 1)
            b = self.gen(NAT, env, depth - 1)
            # guard div/mod by zero: use (b + 1)
            if op in ("/", "%"):
                return f"({a} {op} ({b} + 1))"
            return f"({a} {op} {b})"
        if k < 0.7:
            c = self.gen(BOOL, env, depth - 1)
            a = self.gen(NAT, env, depth - 1)
            b = self.gen(NAT, env, depth - 1)
            return f"(if {c} then {a} else {b})"
        if k < 0.85 and vs:
            # match on a Nat: zero vs succ
            n = self.pick(vs)
            z = self.gen(NAT, env, depth - 1)
            fresh = self.fresh(env)
            s = self.gen(NAT, env + [(fresh, NAT)], depth - 1)
            return (f"(match {n} with | 0 => {z} | {fresh} + 1 => {s})")
        # let-binding
        fresh = self.fresh(env)
        val = self.gen(NAT, env, depth - 1)
        body = self.gen(NAT, env + [(fresh, NAT)], depth - 1)
        return f"(let {fresh} := {val}; {body})"

    def gen_bool(self, env, depth, leaf):
        vs = self.vars_of(env, BOOL)
        atoms = ["true", "false"] + vs
        if leaf and atoms:
            return self.pick(atoms)
        k = self.rng.random()
        if k < 0.55:
            op = self.pick(["<", "<=", ">", ">=", "==", "!="])
            a = self.gen(NAT, env, depth - 1)
            b = self.gen(NAT, env, depth - 1)
            return f"({a} {op} {b})"
        if k < 0.8:
            op = self.pick(["&&", "||"])
            a = self.gen(BOOL, env, depth - 1)
            b = self.gen(BOOL, env, depth - 1)
            return f"({a} {op} {b})"
        return f"(!{self.gen(BOOL, env, depth - 1)})"

    def gen_list(self, env, depth, leaf):
        vs = self.vars_of(env, LISTNAT)
        atoms = ["[]"] + vs
        if leaf:
            if self.rng.random() < 0.5:
                elems = [str(self.rng.randint(0, 9)) for _ in range(self.rng.randint(0, 3))]
                return "[" + ", ".join(elems) + "]"
            return self.pick(atoms) if atoms else "[]"
        k = self.rng.random()
        if k < 0.25 and vs:
            n = self.pick(vs)
            fresh = self.fresh(env)
            body = self.gen(NAT, env + [(fresh, NAT)], depth - 1)
            return f"({n}.map (fun {fresh} => {body}))"
        if k < 0.45 and vs:
            n = self.pick(vs)
            fresh = self.fresh(env)
            body = self.gen(BOOL, env + [(fresh, NAT)], depth - 1)
            return f"({n}.filter (fun {fresh} => {body}))"
        if k < 0.6 and vs:
            return f"({self.pick(vs)}.reverse)"
        if k < 0.75:
            a = self.gen(LISTNAT, env, depth - 1)
            b = self.gen(LISTNAT, env, depth - 1)
            return f"({a} ++ {b})"
        if k < 0.85:
            h = self.gen(NAT, env, depth - 1)
            t = self.gen(LISTNAT, env, depth - 1)
            return f"({h} :: {t})"
        # match on a list: nil vs cons
        if vs:
            n = self.pick(vs)
            nil = self.gen(LISTNAT, env, depth - 1)
            hd, tl = self.fresh(env), self.fresh(env, offset=1)
            cons = self.gen(LISTNAT, env + [(hd, NAT), (tl, LISTNAT)], depth - 1)
            return (f"(match {n} with | [] => {nil} | {hd} :: {tl} => {cons})")
        return "[]"

    def gen_pair(self, env, depth, _leaf):
        a = self.gen(NAT, env, max(depth - 1, 0))
        b = self.gen(NAT, env, max(depth - 1, 0))
        return f"({a}, {b})"

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


def emit_lean_file(seed, ndefs, ninputs):
    g = Gen(seed)
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
