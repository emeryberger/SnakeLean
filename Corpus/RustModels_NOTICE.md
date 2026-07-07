# Attribution: Corpus/RustModels.lean

The Lean definitions in `Corpus/RustModels.lean` are ported (adapted to Lean
4.31 and reduced to computable `def`s only) from the
**`model-checking/rust-lean-models`** project:

- Upstream: https://github.com/model-checking/rust-lean-models
- Copyright: **Kani Contributors**
- License: **dual-licensed Apache-2.0 OR MIT**
  (SPDX-License-Identifier: `Apache-2.0 OR MIT`)

The upstream project provides Lean models of Rust standard-library string
functions (`core`/`std`). Every original source file in that project carries
the header:

```
-- Copyright Kani Contributors
-- SPDX-License-Identifier: Apache-2.0 OR MIT
```

## What was ported

Only the **computable** function definitions were ported (from
`RustLeanModels/RustString.lean`, plus two small helpers from
`RustLeanModels/Basic.lean` and `RustLeanModels/Iterator.lean`). All theorems,
lemmas, `Prop`-valued specifications, and definitions taking proof arguments
were dropped. Some definitions were adjusted for the Lean 4.31 toolchain and,
where the original relied on separately-proved termination lemmas, marked
`partial def`.

## License texts

The full Apache-2.0 and MIT license texts are available in the upstream
repository (`LICENSE-APACHE`, `LICENSE-MIT`). This port is redistributed under
the same dual license.
