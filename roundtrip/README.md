# Round-trip faithfulness harness

Demonstrates that the Lean → Python transpilation is *faithful*: the generated
Python computes exactly what the original Lean definition computes, with **Lean
itself as the oracle** (not hand-written expected values).

Two complementary checks, both driven by `run.sh`:

- **Option A — sampled differential** (`Oracle.lean` + `run_oracle.py`).
  For a curated set of 21 monomorphic corpus functions, Lean `#eval`s each on a
  battery of inputs and emits the result as JSON; the runner execs the
  transpiled Python on the same inputs and asserts equality.

- **Option C — exhaustive** (`Exhaustive.lean` + `run_oracle.py`).
  For 12 functions with small finite domains, enumerates the *entire* bounded
  input space — all `n ∈ [0,60]` (unary) and all `(x,y) ∈ [0,25]²` (binary),
  3807 points — so there is no untested input in range. This mirrors, for
  ordinary functions, the exhaustive `1440/1440` check used for the
  `SmashCoreConc` enum/record model in `../model/`.

## Running

```bash
./roundtrip/run.sh        # from the repo root
```

Expected tail:

```
=== Option A: sampled differential ... ===
  cases: 112/112 agree
  ALL AGREE — transpilation is faithful on this battery

=== Option C: exhaustive over bounded input domains ===
  cases: 3807/3807 agree
  ALL AGREE — transpilation is faithful on this battery
```

## How the oracle stays honest

- Oracle rows are keyed on the **fully-qualified Lean name**; the runner maps
  each to its emitted Python name via the `# Lean:` comments, so the check does
  not depend on the transpiler's snake_case / module-prefix naming.
- Polymorphic functions keep a leading erased type parameter in the emitted
  Python (`reverse(__k, xs)`); the runner pads such calls with `None`, which the
  body never inspects.
- Results are compared structurally after JSON decoding (Lean `List`/`Bool`/
  `Nat` vs Python `list`/`bool`/`int`; `Prod` ↔ tuple).

## Why this is only a *bounded* soundness statement

This is empirical differential testing against an oracle, not a proof of
transpiler correctness. It certifies agreement on the tested inputs (exhaustive
within the stated bounds), which is exactly the kind of evidence that catches
real transpilation bugs — several were found and fixed while building it:
missing `default` list-match arm, un-collected transitive callees, unmapped
`List.lengthTR`, and `Eq.ndrec`/cast proof-term leakage.
