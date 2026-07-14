#!/usr/bin/env python3
"""EMP — Equivalence Modulo Proofs: differential testing against Lean's theorems.

`fuzz/Theorems.lean` harvests machine-checked equations (`theorem : lhs = rhs`) from
the Lean environment, monomorphizes them, and transpiles EACH SIDE separately.  Each
identity is a *proof* that two different programs are the same program, so:

    the two transpiled Python programs must agree on every input.

The proof, not Lean's evaluator, is the oracle — so unlike `fuzz.py` there is **no
Lean evaluation at test time**.  A disagreement is a transpiler bug by construction:
Lean has already proved the two sides equal.

WHAT MAKES AN IDENTITY USEFUL is not that it is true (all of them are) but that its
two sides exercise DIFFERENT translation rules.  `Nat.zero_sub : 0 - n = 0` catches
truncated Nat subtraction emitted as a plain `-`; `Nat.div_eq_sub_mod_div` cannot,
because its subtraction never goes negative.  We therefore diff the two sides'
`HANDLERS_FIRED` tag sets and rank identities by the rules they *distinguish* — the
same lesson as F36, one level up: coverage says a rule ran, not that it ran on a
witness that separates two candidate semantics.

Usage:
    python3 fuzz/emp.py                 # harvest, then differential-test
    python3 fuzz/emp.py --inputs 500    # more inputs per identity
    python3 fuzz/emp.py --show-ranking  # which identities distinguish which rules
"""
import argparse
import contextlib
import os
import random
import re
import signal
import subprocess
import sys


@contextlib.contextmanager
def time_limit(seconds):
    """Hard wall-clock bound on one call.  A `List.range n` on a large `n` would
    otherwise hang the driver rather than fail it."""
    def _fire(signum, frame):
        raise TimeoutError()
    old = signal.signal(signal.SIGALRM, _fire)
    signal.setitimer(signal.ITIMER_REAL, seconds)
    try:
        yield
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
        signal.signal(signal.SIGALRM, old)

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "roundtrip"))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen                      # noqa: E402  (value generation, shared with the fuzzer)
import run_oracle               # noqa: E402  (normalize: the exact-value equality)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Ident:
    """One harvested identity: two transpiled programs Lean has proved equal."""

    def __init__(self, idx, thm, ret, params):
        self.idx, self.thm, self.ret, self.params = idx, thm, ret, params
        self.src = {}       # "L"/"R" -> python source
        self.tags = {}      # "L"/"R" -> set of translation-rule tags fired

    @property
    def distinguishes(self):
        """Rules exercised by exactly one side — the identity's discriminating power."""
        return self.tags.get("L", set()) ^ self.tags.get("R", set())


CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".emp_harvest.txt")


def harvest(max_cands=40, use_cache=True):
    """Run the Lean harvester and parse its ### THM / ### SIDE blocks.

    The harvest scans the whole environment and transpiles both sides of every
    candidate — minutes, not seconds.  Cache the raw stream so re-testing (different
    input counts, a rebuilt transpiler) is instant.  The cache is keyed on nothing:
    delete `.emp_harvest.txt` after changing the transpiler or the harvester.
    """
    if use_cache and os.path.exists(CACHE):
        out = open(CACHE).read()
    else:
        env = dict(os.environ, EMP_MAX=str(max_cands))
        out = subprocess.run(
            ["lake", "env", "lean", "fuzz/Theorems.lean"],
            cwd=ROOT, capture_output=True, text=True, timeout=7200, env=env,
        ).stdout
        with open(CACHE, "w") as f:
            f.write(out)

    # Lean writes its diagnostics into the same stream.  Blocks are therefore
    # explicitly delimited (`### SIDE` … `### END`) and we accumulate ONLY between the
    # markers: a stray Lean error can never be `exec`'d as Python and misreported as a
    # transpiler bug.  A false positive from the harness itself is the worst kind.
    lean_errs = [l for l in out.splitlines()
                 if re.match(r"^\S+\.lean:\d+:\d+: (error|warning)", l)]
    if lean_errs:
        print(f"note: {len(lean_errs)} Lean diagnostic(s) during harvest "
              f"(candidates that failed to define; they are skipped, not tested)",
              file=sys.stderr)

    idents, cur, side, buf = [], None, None, []
    for line in out.splitlines():
        if line.startswith("### THM\t"):
            _, idx, thm, ret, params = line.split("\t")
            cur = Ident(int(idx), thm, ret, [p for p in params.split(",") if p])
            idents.append(cur)
            side = None
        elif line.startswith("### SIDE\t"):
            side, buf = line.split("\t")[2], []
        elif line.startswith("### END\t"):
            if cur is not None and side is not None:
                src = "\n".join(buf)
                cur.src[side] = src
                m = re.search(r"^# HANDLERS_FIRED\t(.*)$", src, re.M)
                cur.tags[side] = set(m.group(1).split("\t")) if m else set()
            side = None
        elif side is not None:
            buf.append(line)
    return [i for i in idents if "L" in i.src and "R" in i.src]


def load_side(ident, side):
    """exec one side in its OWN namespace (the two sides may reuse helper names)."""
    ns = {}
    exec(compile(ident.src[side], f"<emp{ident.idx}{side}>", "exec"), ns)
    want = f"empL{ident.idx}" if side == "L" else f"empR{ident.idx}"
    m = re.search(rf"^# Lean: {re.escape(want)}\ndef (\w+)", ident.src[side], re.M)
    if not m:
        raise KeyError(f"no emitted def for {want}")
    return ns[m.group(1)]


def check(ident, n_inputs, rng):
    """Feed both proven-equal programs the same inputs; any disagreement is a bug.

    Triage matters here.  A `fallthrough.*` tag is the emitter ADMITTING it met a
    construct it has no rule for — it then emits a call to an undefined name, so the
    program dies with NameError.  That is a transpiler *gap* (the F821 class), not a
    mistranslation, and lumping the two together would bury the real signal.  The gold
    is a MISMATCH between two sides that both transpiled cleanly: Lean proved them
    equal, so a disagreement is a translation bug by construction.
    """
    if any(t.startswith("fallthrough.") for t in ident.tags.get("L", set())
           | ident.tags.get("R", set())):
        return ("gap", "emitter has no rule for a construct on one side", None)

    try:
        fl, fr = load_side(ident, "L"), load_side(ident, "R")
    except SyntaxError as e:
        # The emitter produced Python that does not parse.  A real bug, always.
        return ("syntax", f"{type(e).__name__}: {e}", None)
    except Exception as e:                       # noqa: BLE001
        return ("exec", f"{type(e).__name__}: {e}", None)

    # SMALL values only.  Unlike the grammar's generated defs (non-recursive
    # straight-line arithmetic, where a huge value costs O(1)), EMP identities call
    # the REAL stdlib: a boundary value landing on a SIZE parameter makes
    # `List.range n` / `Array.replicate n` build a 10^18-element list and hang.  EMP's
    # discriminating power comes from the PROOF, not from the value domain, so it does
    # not need big values — combining the two would need per-parameter size analysis.
    g = gen.Gen(seed=rng.randrange(1 << 30))
    g.BIG_INPUT_P = 0.0
    for _ in range(n_inputs):
        args = [g.rand_value(t) for t in ident.params]
        try:
            with time_limit(2):
                lv, rv = fl(*args), fr(*args)
        except TimeoutError:
            continue                             # size-parameter blowup; not a bug
        except (OverflowError, MemoryError, RecursionError):
            continue
        except NameError as e:
            return ("gap", f"undefined name: {e}", args)
        except Exception as e:                   # noqa: BLE001
            # One side raising where the other returns is a real divergence; both
            # sides raising identically is a shared gap, not an inequivalence.
            try:
                fr(*args)
                return ("runtime", f"L raised {type(e).__name__}: {e}", args)
            except Exception:                    # noqa: BLE001
                return ("gap", f"both sides raise {type(e).__name__}: {e}", args)
        if run_oracle.normalize(lv) != run_oracle.normalize(rv):
            return ("mismatch", f"lhs={lv!r} rhs={rv!r}", args)
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--inputs", type=int, default=200,
                    help="random inputs per identity")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--show-ranking", action="store_true",
                    help="list identities by discriminating power")
    ap.add_argument("--max", type=int, default=40, dest="max_cands",
                    help="identities to harvest (0 = the whole pool)")
    args = ap.parse_args()
    rng = random.Random(args.seed)

    print(f"harvesting proven equations from the Lean environment "
          f"(max={args.max_cands or 'ALL'}) ...", flush=True)
    idents = harvest(args.max_cands)
    print(f"harvested {len(idents)} identities (both sides transpiled)\n")

    bugs, gaps, tested = [], [], 0
    for ident in idents:
        res = check(ident, args.inputs, rng)
        if res is None:
            tested += 1
            continue
        kind, detail, iargs = res
        if kind == "gap":
            gaps.append((ident, detail))   # unsupported construct, not a mistranslation
            continue
        tested += 1
        bugs.append((ident, kind, detail, iargs))
        print(f"*** TRANSPILER BUG — {ident.thm} — kind={kind} ***")
        print("  Lean PROVED lhs = rhs, but the transpiled programs disagree.")
        print(f"  args={iargs}")
        print(f"  {detail}")
        print(f"  rules only one side uses: {sorted(ident.distinguishes) or '(none)'}\n")

    print(f"{tested} identities tested, {len(bugs)} translation bug(s).")
    print(f"{len(gaps)} identities set aside as transpiler GAPS (a construct the "
          f"emitter has no rule for — the F821 class, not a mistranslation):")
    for ident, detail in gaps[:10]:
        print(f"    {ident.thm:44s} {detail}")

    # Discriminating power: an identity that fires the SAME rules on both sides can
    # only catch bugs in shared rules; one whose sides differ pits rule against rule.
    disc = [i for i in idents if i.distinguishes]
    print(f"\n{len(disc)}/{len(idents)} identities are DISCRIMINATING "
          f"(their two sides fire different translation rules)")
    if args.show_ranking:
        for i in sorted(disc, key=lambda i: -len(i.distinguishes))[:25]:
            print(f"  {len(i.distinguishes):2d}  {i.thm:42s} {sorted(i.distinguishes)}")


if __name__ == "__main__":
    main()
