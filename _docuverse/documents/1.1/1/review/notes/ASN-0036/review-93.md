# Review of ASN-0036

## REVISE

(none)

## OUT_OF_SCOPE

(none — the ASN's Scope section appropriately delineates deferred topics)

VERDICT: CONVERGED

The ASN establishes the strand model with rigorous proofs throughout. State components `Σ.C` and `Σ.M(d)` are introduced with formal contracts and modeling justifications. Invariants S0–S9 are stated, derived where appropriate, and proven with explicit case analysis and dependency tracking. The structural decomposition machinery (correspondence runs; `ord`/`vpos`/`w_ord`; OrdAddHom, OrdAddS8a, OrdShiftHom) handles boundary cases explicitly (action point at `k = 2` collapses the prefix range; action point at `k = m` collapses the tail range). Subspace-bound contiguity properties (D-CTG, D-MIN, D-CTG-depth, D-SEQ) are properly scoped to the text subspace with link-subspace exemption acknowledged. The worked example exhibits concrete tumblers and verifies S0, S3, S5, S7, S8, D-SEQ across multiple transitions, including a non-singleton correspondence run that exercises the auxiliary lemma's `k ≥ 1` case.

Two observations that do not rise to REVISE:

- **Auxiliary lemma presentation order in S8.** Conclusions are presented (i) → (ii) → (iii), but the formal definition of `subspace_I` via the `E` projection means (i) (subspace identifier preservation) implicitly depends on (ii) (zero-count = 3) and (iii) (element-field depth = δⱼ) for the position of `subspace_I` to coincide between `aⱼ` and `shift(aⱼ, k)`. The proof's content is correct — the integrated argument from prefix-copy plus positive-action-point overwrite establishes all three — but a careful reader must stitch the dependencies together.

- **D-CTG antecedent's S8a-validity of candidate intermediates.** The quantifier ranges over candidates `v` with `subspace(v) = 1` and `#v = #u`, without explicitly requiring S8a. In well-formed states this is harmless (D-CTG-depth restricts attention to candidates that share components 2 through m−1 with V_1(d) members, where positive last components are forced), but the unrestricted antecedent admits hypothetical violations involving non-S8a candidates that simply fail vacuously.
