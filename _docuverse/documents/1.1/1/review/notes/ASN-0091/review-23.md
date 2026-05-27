# Review of ASN-0091

The ASN develops REARRANGE as a Vstream-only operation, with an abstract class (RA-reg, RA-dom, RA-π, RA-frame, RA-adm) and REARRANGE_K as its concrete realisation. It derives a catalog of RE-* consequences spanning content/link store invariance, domain/range invariance, projection transport, cross-document independence, transclusion preservation, and run-decomposition cardinality variations.

I checked each derivation against the foundation. The key arguments hold:

- **S2 derivation at the abstract level** explicitly chains pre-state S2 + RA-dom + RA-π through π's bijectivity. The unique pre-image construction `v = π⁻¹(v')` is well-licensed.
- **RE-proj** establishes both inclusions explicitly (forward via RA-π + coverage state-independence; reverse via π's bijectivity); the bijection-non-uniqueness section concretely verifies that the set image is witness-invariant.
- **Subspace preservation under RA-adm** is argued bidirectionally (content-to-link and link-to-content), each direction routing through S3★ + L14 + RE-C/RE-L.
- **ChainDisjointAdjacency** inline lemma is sound — TA5(c)'s chain-successor identity together with T3's component-wise tumbler equality forces same-chain origin under purported chain-adjacency, contradicting the distinct-chain hypothesis. Parametric across all length cases (including proper-prefix documents).
- **P4a discharge** through SequentialTransitionAxiom's append-only trace + RE-R is sound; past states are committed inputs that future transitions cannot rewrite.

Edge cases covered:
- Empty case (admitted abstractly; REARRANGE_K excludes via R-PRE(iv) + CS2)
- Identity case (admitted abstractly; REARRANGE_K excludes via π ≠ id from K.μ~)
- 3-cut pivot (worked example 1), 4-cut swap (worked example 2 — exercises Δ(μ) = w_β − w_α ≠ 0)
- Interior cuts (worked example 3 — exercises R-EXT pointwise)
- Shared I-addresses (worked example 4 — exhibits two distinct valid bijections π₁ and π₂ for the same Σ → Σ' and verifies RE-proj's set-image uniformity)
- Existential possibility lemmas (RE-frag, RE-coal, RE-eq) each have explicit concrete witnesses

Foundation invariants checked: each worked example traces admissibility through S2, S3★, S3★-aux, S8a, S8-fin, S8-depth, S8★, D-CTG★, D-MIN★, D-SEQ★, CL-OWN, CL-UNIQ, P4★, P4a — each clause discharged from named premises rather than waved through.

Cross-ASN architecture handled: the ASN explicitly notes R-SP's S3 and S8 clauses are not load-bearing in the unified state (they're superseded by S3★ and S8★), and provides separate constructive derivations from REARRANGE_K's structural properties.

Composition section catalogs ★ forms with explicit conditions (e.g., RE-trans★ unconditionally preserves (i)+(ii) but requires no step targets origin(a) for (iii); RE-other★ requires no step targets the named document).

Open Questions appropriately defer harder questions (cross-document transclusion fragmentation semantics, link-subspace REARRANGE, observational equivalence, RE-frag upper bound, REARRANGE_K completeness for the abstract class).

VERDICT: CONVERGED
