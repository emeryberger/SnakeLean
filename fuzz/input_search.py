#!/usr/bin/env python3
"""Coverage-guided oracle-input search for a single transpiled function.

PLAN.md task-5 follow-up: `--pycov` showed that random oracle inputs leave many
transpiled functions' branches unexercised (e.g. `yahtzee_score` at 7% under 40
random seeds — random 5-element lists almost never form a Yahtzee/straight).  A
transpiler bug in such an unreached branch is invisible to differential testing.

Hand-seeding inputs per function doesn't scale to 78 functions.  Instead this is
a small AFL-style greybox loop that runs entirely on the *transpiled Python*
(fast, in-process, no Lean): start from a seed corpus, keep any input that hits a
new line, and prefer mutating covering inputs.  The result is a compact input set
that maximizes branch coverage of the transpiled body.  `fuzz.py --pycov-search`
then emits a Lean oracle file over exactly those inputs, so any divergence a
newly-reached branch exposes is still caught by the oracle.

The search never trusts the transpiled output for correctness — it only uses it
to *choose* inputs.  Correctness is always decided by the Lean oracle downstream.
"""
import random

import gen
import pycov

# Type-directed mutators.  Each takes (rng, value) and returns a nearby value of
# the same Lean type.  Kept deliberately diverse (boundaries, duplicates, sign
# flips) because branch conditions in real corpus code key on exactly those.
_NAT_INTERESTING = [0, 1, 2, 3, 5, 8, 12]
_INT_INTERESTING = [0, 1, -1, 2, -2, 7, -7, 12, -12]


def _mut_nat(rng, v):
    choice = rng.randint(0, 3)
    if choice == 0:
        return rng.choice(_NAT_INTERESTING)
    if choice == 1:
        return max(0, v + rng.choice([-2, -1, 1, 2]))
    if choice == 2:
        return rng.randint(0, 12)
    return v * 2 % 13


def _mut_int(rng, v):
    choice = rng.randint(0, 3)
    if choice == 0:
        return rng.choice(_INT_INTERESTING)
    if choice == 1:
        return v + rng.choice([-2, -1, 1, 2])
    if choice == 2:
        return -v
    return rng.randint(-12, 12)


def _mut_list(rng, v):
    xs = list(v)
    op = rng.randint(0, 6)
    if op == 0 and xs:            # drop an element
        xs.pop(rng.randrange(len(xs)))
    elif op == 1:                 # insert an element
        xs.insert(rng.randint(0, len(xs)), rng.randint(0, 9))
    elif op == 2 and xs:          # tweak an element
        i = rng.randrange(len(xs))
        xs[i] = max(0, xs[i] + rng.choice([-1, 1]))
    elif op == 3:                 # duplicate all (equal-elements branches)
        xs = xs + xs
    elif op == 4:                 # sort (ordered-list branches)
        xs = sorted(xs)
    elif op == 5 and xs:          # make all elements equal (Yahtzee-like)
        xs = [xs[0]] * len(xs)
    else:                         # make consecutive (straight-like)
        n = len(xs) if xs else rng.randint(1, 5)
        base = rng.randint(0, 5)
        xs = [base + i for i in range(n)]
    return xs[:8]                 # bound length so the oracle stays fast


def _mut_pair(rng, v):
    a, b = v
    if rng.random() < 0.5:
        return [_mut_nat(rng, a), b]
    return [a, _mut_nat(rng, b)]


def _mut_opt(rng, v):
    if rng.random() < 0.3:
        return None
    return rng.randint(0, 12) if v is None else _mut_nat(rng, v)


_MUTATORS = {
    gen.NAT: _mut_nat, gen.INT: _mut_int, gen.LISTNAT: _mut_list,
    gen.PAIR: _mut_pair, gen.OPTNAT: _mut_opt, gen.BOOL: lambda rng, v: not v,
}


def _rand(rng, ty):
    """A fresh random value of Lean type `ty` (reuses gen.py's value ranges)."""
    g = gen.Gen.__new__(gen.Gen)
    g.rng = rng
    return g.rand_value(ty)


def _interesting(rng, ty):
    """A structurally-interesting value of Lean type `ty` — the shapes real
    branch conditions key on (all-equal / consecutive / empty lists, boundary
    ints).  Used to bootstrap the search so it doesn't rely on mutation alone to
    stumble onto rare structural branches (Yahtzee, full-house, straight, …)."""
    if ty == gen.LISTNAT:
        n = rng.randint(1, 5)
        kind = rng.randint(0, 3)
        if kind == 0:                       # all equal (e.g. Yahtzee)
            return [rng.randint(0, 6)] * n
        if kind == 1:                       # consecutive (straight)
            base = rng.randint(0, 5)
            return [base + i for i in range(n)]
        if kind == 2:                       # two-of-a-kind blocks (full house)
            a, b = rng.randint(0, 6), rng.randint(0, 6)
            return [a, a, a, b, b][:n] or [a]
        return []                           # empty
    if ty == gen.NAT:
        return rng.choice(_NAT_INTERESTING)
    if ty == gen.INT:
        return rng.choice(_INT_INTERESTING)
    if ty == gen.PAIR:
        return [rng.choice(_NAT_INTERESTING), rng.choice(_NAT_INTERESTING)]
    if ty == gen.OPTNAT:
        return rng.choice([None, 0, 1])
    return _rand(rng, ty)


def _mutate(rng, ptypes, args):
    """Mutate one randomly-chosen argument of `args` in place (typed)."""
    out = list(args)
    i = rng.randrange(len(ptypes))
    out[i] = _MUTATORS[ptypes[i]](rng, out[i])
    return out


def search(fn, ptypes, body, seed=0, budget=400):
    """Greybox-search inputs for transpiled `fn` (a callable) with parameter Lean
    types `ptypes` and executable body-line set `body`.

    Returns (covering_inputs, hit_lines): `covering_inputs` is a small list of
    argument lists that together cover `hit_lines` — each was kept because it hit
    a body line no earlier input did.  Deterministic in `seed`.

    Pure-Python and Lean-free: it traces the transpiled body only to steer input
    selection; correctness is decided later by the Lean oracle.  The loop
    interleaves mutation of covering inputs (exploit) with fresh random draws
    (explore), so it never does worse than the random baseline given equal
    budget."""
    rng = random.Random(seed)
    covered = set()
    corpus = []          # covering inputs — the seeds worth mutating
    covering = []        # the argument lists we return

    def consider(args):
        nonlocal covered
        hit = pycov.trace_call(fn, args) & body
        new = hit - covered
        if new:
            covered |= new
            corpus.append(args)
            covering.append(list(args))
            return True
        return False

    # Bootstrap with structurally-interesting inputs so rare branches (all-equal
    # lists, straights, boundary ints) get an early shot before the mutation loop.
    boot = min(budget // 4, 40)
    for _ in range(boot):
        if covered >= body:
            return covering, covered
        consider([_interesting(rng, t) for t in ptypes])

    for _ in range(boot, budget):
        if covered >= body:
            break
        # ~40% explore (fresh random / interesting), ~60% exploit (mutate).
        if not corpus or rng.random() < 0.4:
            gen_one = _interesting if rng.random() < 0.5 else _rand
            consider([gen_one(rng, t) for t in ptypes])
        else:
            base = corpus[rng.randrange(len(corpus))]
            # Stack 1–3 mutations for a bigger jump toward rare branches.
            args = base
            for _ in range(rng.randint(1, 3)):
                args = _mutate(rng, ptypes, args)
            consider(args)
    return covering, covered
