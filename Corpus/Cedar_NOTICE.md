# Attribution: Corpus/Cedar.lean

The Lean definitions in `Corpus/Cedar.lean` are ported (adapted to plain
monomorphic Lean 4.31 and reduced to computable `def`s only) from the
**`cedar-policy/cedar-spec`** project:

- Upstream: https://github.com/cedar-policy/cedar-spec/tree/main/cedar-lean
- Copyright: **Cedar Contributors**
- License: **Apache-2.0** (SPDX-License-Identifier: `Apache-2.0`)

The upstream project is the Lean formalization of the [Cedar](https://www.cedarpolicy.com/)
policy language — its authorization engine, evaluator, and validator, together
with correctness proofs. Every original source file carries the header:

```
Copyright Cedar Contributors
Licensed under the Apache License, Version 2.0 (the "License");
```

## What was ported

Only the **computable, value-level** function definitions from
`cedar-lean/Cedar/Data/Int64.lean` and `cedar-lean/Cedar/Data/Set.lean` were
ported. All theorems, lemmas, `Prop`-valued specifications, and typeclass
instances were dropped. Two adaptations were made for the SnakeLean fuzzing
corpus, whose value universe is monomorphic and does not model machine words:

- **`Int64`** (Cedar's Rust-`i64`-style checked-arithmetic type, which wraps
  Lean's machine `Int64`) is modelled as a **range-checked `Int`**: `i64Min`/
  `i64Max` are the real `i64` bounds and the checked operations (`add?`, `sub?`,
  `mul?`, `neg?`, `ofInt?`) return `none` on overflow — the same observable
  behavior as upstream.
- **`Set α`** (Cedar's canonical sorted, duplicate-free list) is instantiated
  at `Int` (`List Int`), since the generic, `DecidableLT`-constrained upstream
  definition can't be driven by the monomorphic value universe. The
  membership / subset / intersection / difference semantics match upstream.

## License text

The full Apache-2.0 license text is available in the upstream repository
(`LICENSE`, `NOTICE`). This port is redistributed under the same license.
