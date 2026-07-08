# Attribution: Corpus/Mathlib.lean

The Lean definitions in `Corpus/Mathlib.lean` are adapted (re-stated
monomorphically over `Nat` in plain Lean 4.31, reduced to computable `def`s
only) from **Mathlib**, the Lean 4 mathematical library:

- Upstream: https://github.com/leanprover-community/mathlib4
- Copyright: **The Mathlib Community**
- License: **Apache-2.0** (SPDX-License-Identifier: `Apache-2.0`)

Every upstream Mathlib source file carries the header:

```
Copyright (c) <year> <authors>. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
```

## What was ported

Only the **computable, value-level** function definitions were ported, each
re-stated monomorphically over `Nat`:

- `Mathlib/Data/Nat/Factorial/Basic.lean` — `factorial`, `ascFactorial`,
  `descFactorial`
- `Mathlib/Data/Nat/Choose/Basic.lean` — `choose`, `multichoose`, `centralBinom`
- `Mathlib/Data/Nat/Fib/Basic.lean` — `fib`

All theorems, lemmas, `Prop`-valued specifications, `@[simp]` attributes, and
typeclass/instance machinery were dropped. Mathlib's generic definitions (some
stated over algebraic-hierarchy typeclasses) were specialized to `Nat` so the
SnakeLean fuzzer's monomorphic value universe can drive them.

## Why not a build dependency

Mathlib is **not** added as a Lake dependency. Its transitive import graph and
build cost are prohibitive for this fuzzing harness, it would lock the exact
toolchain and slow every fuzzer Lean spawn, and the fragment harvester only
enumerates `Corpus.*`-namespaced defs regardless. This mirrors the hand-port
approach already used for `Corpus/RustModels.lean` and `Corpus/Cedar.lean`.
