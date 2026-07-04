#!/bin/bash
# Round-trip faithfulness harness: use Lean itself as the oracle and check that
# the transpiled Python computes the same results.
#
#   Option A (differential):  a sampled battery across 21 corpus functions.
#   Option C (exhaustive):    the ENTIRE bounded input domain for 12 functions.
#
# Usage: roundtrip/run.sh     (from the repo root)
set -euo pipefail
export PATH="$HOME/.elan/bin:$PATH"

echo "=== Building transpiler + corpus ==="
lake build >/dev/null
lake build Corpus.Algorithms Corpus.Math Corpus.NumberTheory Corpus.Sequences >/dev/null

echo
echo "=== Option A: sampled differential (Lean oracle vs transpiled Python) ==="
lake env lean roundtrip/Oracle.lean > roundtrip/gen.txt 2>/dev/null
python3 roundtrip/run_oracle.py roundtrip/gen.txt

echo
echo "=== Option C: exhaustive over bounded input domains ==="
lake env lean roundtrip/Exhaustive.lean > roundtrip/gen_exhaustive.txt 2>/dev/null
python3 roundtrip/run_oracle.py roundtrip/gen_exhaustive.txt
