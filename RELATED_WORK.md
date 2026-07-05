# Related Work & Techniques Considered (Not Yet Adopted)

This file collects techniques from the compiler-testing and verification
literature that are *relevant but not currently implemented* in this project,
so the [README](README.md#correctness) can stay focused on what the test suite
and fuzzer actually do. Each entry notes how it would apply to validating the
Lean → Python transpiler and why it isn't in yet.

For techniques the fuzzer **does** use (grammar-based generation, differential
oracle, delta-debugging-style shrinking, grammar production coverage, grammar
expansion, **EMI + guided stochastic mutation**, **fragment-reuse grammars**,
**k-path coverage**, and **structural HDD/C-Reduce-style reduction**), see the
README's Correctness section and [`VERIFICATION.md`](VERIFICATION.md).

> Note: several techniques once listed here as *not adopted* are **now
> implemented** and have moved to the README's implemented list:
> - **EMI (Le/Afshari/Su, PLDI 2014) + guided stochastic mutation (Le/Sun/Su,
>   OOPSLA 2015)** — semantics-preserving identity envelopes, a stochastic count,
>   chosen coverage-guided (`--emi`).
> - **k-path (context-sensitive) coverage [3]** — the generator records and
>   reports every chain of ≤3 nested productions; single-production coverage
>   saturates near 100% while k-path coverage reveals the untested combinations
>   (~89% of offered paths at 5000 seeds).
> - **Fragment-reuse grammars / LangFuzz [4]** — `--corpus` harvests real
>   `Corpus/*.lean` definitions and fuzzes them, exercising constructs the
>   grammar can't invent; found bugs F12 (`Nat`/`Int` div/mod by zero) and F13
>   (`Array.qsort` mis-indexing).
> - **Structural reduction / HDD [5], C-Reduce [6]** — `struct_shrink` reduces
>   the failing Lean *term* (not just `(defs, inputs)` counts), keeping any
>   rewrite that still elaborates and still reproduces the bug.
>
> The empirical/formal material below remains *not* adopted.

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

### How existing (unverified) extractors are validated [10, 11, 12, 13]

The closest analogues to LeanToPython are the extraction back-ends of proof
assistants. **How was Coq's extraction validated? Not by fuzzing.** Letouzey's
extraction [10, 11] was validated two ways: (1) a **pen-and-paper correctness
proof** in his 2004 thesis — two theorems (via the untyped intermediate calculus
λ□) relating the erasure relation and typing to Coq's operational semantics; and
(2) **in-practice** validation by extracting large developments (CompCert, etc.)
and running / unit-testing them against reference interpreters. The
*implementation* was part of the trusted code base — never machine-verified —
and drifted from the thesis's theory over time. No random/differential testing
appears in that lineage, which is notable because differential testing is
exactly LeanToPython's approach.

That trust gap is precisely what Forster, Sozeau & Tabareau close in **Verified
Extraction from Coq to OCaml** [12] (PLDI 2024): a new extraction pipeline
implemented *and machine-verified in Coq itself* via MetaCoq (a formalization of
Coq's kernel) with the OCaml side specified through Malfunction. A striking
finding relevant to any extractor: they prove first-order data extracts and
interoperates safely, but **higher-order interoperation with unverified code can
misbehave and even segfault** — a caveat about the limits of "extract and trust."
CertiCoq [13] is a separately *verified* compiler for Gallina. LeanToPython sits
at the empirical/trusted end of this spectrum: differential testing is the
pragmatic validation, exactly as for classic Coq extraction, with the round-trip
harness and fuzzer standing in for "extract and run large developments" — and,
unlike that lineage, adding systematic randomized differential testing on top.

## References

1. V. Le, M. Afshari, Z. Su. *Compiler validation via equivalence modulo
   inputs.* PLDI 2014. <https://doi.org/10.1145/2594291.2594334>
2. V. Le, C. Sun, Z. Su. *Finding deep compiler bugs via guided stochastic
   program mutation.* OOPSLA 2015. <https://doi.org/10.1145/2814270.2814319>
3. N. Havrikov, A. Zeller. *Systematically covering input structure.* ASE 2019. <https://doi.org/10.1109/ASE.2019.00027>
4. C. Holler, K. Herzig, A. Zeller. *Fuzzing with code fragments.* USENIX
   Security 2012. <https://www.usenix.org/conference/usenixsecurity12/technical-sessions/presentation/holler>
5. G. Misherghi, Z. Su. *HDD: Hierarchical delta debugging.* ICSE 2006. <https://doi.org/10.1145/1134285.1134307>
6. J. Regehr, Y. Chen, P. Cuoq, E. Eide, C. Ellison, X. Yang. *Test-case
   reduction for C compiler bugs.* PLDI 2012. <https://doi.org/10.1145/2254064.2254104>
7. M. Willsey, C. Nandi, Y. R. Wang, O. Flatt, Z. Tatlock, P. Panchekha.
   *egg: Fast and extensible equality saturation.* POPL 2021. <https://doi.org/10.1145/3434304>
8. T. Koehler et al. *Guided equality saturation.* POPL 2024. <https://doi.org/10.1145/3632900>
9. M. Rossel. *An Equality Saturation Tactic for Lean.* MSc thesis, TU
   Dresden, 2024. <https://github.com/marcusrossel/lean-egg>
10. P. Letouzey. *A new extraction for Coq.* TYPES 2002. <https://doi.org/10.1007/3-540-39185-1_12>
11. P. Letouzey. *Programmation fonctionnelle certifiée : l'extraction de
    programmes dans l'assistant Coq.* PhD thesis, Université Paris-Sud, 2004.
    <http://www.pps.jussieu.fr/~letouzey/download/these_letouzey.pdf>
12. Y. Forster, M. Sozeau, N. Tabareau. *Verified extraction from Coq to
    OCaml.* PLDI 2024. (MetaCoq/MetaRocq + Malfunction;
    artifact: github.com/MetaRocq/rocq-verified-extraction) <https://doi.org/10.1145/3656379>
13. A. Anand, A. Appel, G. Morrisett, et al. *CertiCoq: A verified compiler for
    Coq.* CoqPL 2017. <https://certicoq.org/>
