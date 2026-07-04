# Related Work & Techniques Considered (Not Yet Adopted)

This file collects techniques from the compiler-testing and verification
literature that are *relevant but not currently implemented* in this project,
so the [README](README.md#correctness) can stay focused on what the test suite
and fuzzer actually do. Each entry notes how it would apply to validating the
Lean → Python transpiler and why it isn't in yet.

For techniques the fuzzer **does** use (grammar-based generation, differential
oracle, delta-debugging-style shrinking, grammar production coverage, grammar
expansion), see the README's Correctness section and
[`VERIFICATION.md`](VERIFICATION.md).

## Additional fuzzing techniques

### Equivalence Modulo Inputs (EMI) [1], guided stochastic mutation [2]

Beyond checking one program against an oracle, EMI mutates a program's
statements that are *unreachable on a given input* and requires the output to
stay identical — turning one seed into many differential tests without needing
an oracle for the "expected" value. The transpiler analogue: apply
semantics-preserving rewrites to a generated Lean term (prune dead branches,
wrap subterms in `id`, rewrite `x` to `x + 0`) and require the transpiled Python
to agree with the un-mutated original. Guided stochastic program mutation [2]
extends EMI with a search that steers mutations toward bug-revealing regions.
Not adopted yet: our differential oracle already gives a ground-truth value per
input, so EMI is an amplifier rather than a prerequisite; worth adding to
multiply coverage per seed.

### k-path (context-sensitive) grammar coverage [3]

The fuzzer currently tracks and prefers uncovered *productions*. A stronger
target is covering *combinations* of productions along a derivation path (e.g. a
`match` inside a `map` inside a `let`) — k-path coverage. This would push the
generator toward construct interactions, where several of the bugs we found
actually lived (e.g. a literal `match` discriminant nested in a `let`).

### Probabilistic / fragment-reuse grammars [4]

Bias production probabilities toward rare constructs, or reuse real code
fragments (as in LangFuzz [4]) drawn from the corpus, to spend generation budget
where bugs are more likely rather than sampling the grammar uniformly.

### Stronger test-case reduction [5, 6]

The current shrinker only reduces the `(defs, inputs)` counts. A structural
reducer over the Lean term itself — hierarchical delta debugging [5] or a
C-Reduce-style pass [6] that deletes subterms and re-checks the failure — would
yield smaller, more legible minimal reproducers.

## Formal-verification approaches

This project validates the transpiler **empirically** (differential testing
against an oracle): it finds bugs but does not prove their absence. The
complementary **formal** route proves each transformation preserves a
denotational semantics. It is out of scope here because a full Lean → Python
semantics (Python's dynamic typing, exceptions, and mutation) is far harder to
formalize than the bounded DSLs these tools target — but it is the other end of
the same spectrum.

### Verified optimization via equality saturation in Lean [7, 8, 9]

Recent Lean work represents all equivalent forms of a term in an **e-graph** and
applies rewrite rules to a fixed point (*equality saturation*), then extracts
the best form by a cost model. `egg` [7] is the canonical fast e-graph library;
Guided Equality Saturation [8] makes it practical at scale in Lean; Rossel's
`lean-egg` tactic [9] integrates `egg` into Lean for automated equality proofs.
The load-bearing idea for us: each rewrite rule carries a Lean theorem proving
semantic preservation, so the optimizer and its proofs cannot diverge. An
analogous transpiler would prove each translation rule preserves an `eval`
denotation. E-graphs/extraction themselves apply only if the transpiler explored
*multiple* equivalent translations and picked one by cost — which it does not.

### How existing (unverified) extractors are validated [10, 11]

The closest analogues to LeanToPython are the extraction back-ends of proof
assistants. Coq's extraction to OCaml/Haskell [10] is part of the *trusted*
computing base — it is **not** formally verified — and is validated in practice
by extracting and running large developments (CompCert, etc.) and by testing.
CertiCoq [11] is the *verified* compiler for Gallina, proving semantic
preservation end to end. LeanToPython sits at the empirical/trusted end of this
spectrum: differential testing is the pragmatic validation, exactly as for Coq's
extraction, with the round-trip harness and fuzzer standing in for "extract and
run large developments."

## References

1. V. Le, M. Afshari, Z. Su. *Compiler validation via equivalence modulo
   inputs.* PLDI 2014.
2. V. Le, C. Sun, Z. Su. *Finding deep compiler bugs via guided stochastic
   program mutation.* OOPSLA 2015.
3. N. Havrikov, A. Zeller. *Systematically covering input structure.* ASE 2019.
4. C. Holler, K. Herzig, A. Zeller. *Fuzzing with code fragments.* USENIX
   Security 2012.
5. G. Misherghi, Z. Su. *HDD: Hierarchical delta debugging.* ICSE 2006.
6. J. Regehr, Y. Chen, P. Cuoq, E. Eide, C. Ellison, X. Yang. *Test-case
   reduction for C compiler bugs.* PLDI 2012.
7. M. Willsey, C. Nandi, Y. R. Wang, O. Flatt, Z. Tatlock, P. Panchekha.
   *egg: Fast and extensible equality saturation.* POPL 2021.
8. T. Koehler et al. *Guided equality saturation.* POPL 2024.
9. M. Rossel. *An Equality Saturation Tactic for Lean.* MSc thesis, TU
   Dresden, 2024.
10. P. Letouzey. *A new extraction for Coq.* TYPES 2002.
11. A. Anand, A. Appel, G. Morrisett, et al. *CertiCoq: A verified compiler for
    Coq.* CoqPL 2017.
