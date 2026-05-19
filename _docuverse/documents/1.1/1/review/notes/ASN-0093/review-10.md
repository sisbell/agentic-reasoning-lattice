# Review of ASN-0093

I performed multiple careful passes over ASN-0093 (Allocation Substrate), checking the chain lemmas, the simultaneous-induction discipline, the C1c/L1c chain exhibitions, the Cross-document disjointness lemma in both Case A and Case B (with sub-cases B.i and B.ii), the discharge matrix, and the worked example.

The ASN is structured as a downward decomposition from a fuller transition model, isolating the allocation substrate (three primitives K.σ, K.α, K.λ on three stores C, L, M) without lifting entity stratification or provenance recording.

Key correctness checks I verified:

1. **Chain lemmas** are derived from the purely structural Definition (FirstElementValidity + SiblingRecurrence) plus foundation claims (TA5a, TA5(a)/(b)/(c), TA5-SigValid, T1, T4, Prefix, NAT-*). They do not require T10a's tree-embedding (T10a.4/T10a.5/T10a.6), so the bootstrap is closed.

2. **ChainPrefixExtension's induction** correctly cites ChainElementT4Validity as a standalone prior fact (not a nested induction), avoiding circularity. The lemma stacking is sound.

3. **Cross-document disjointness** handles Case A (prefix-comparable) by M0's `zeros = 2` constraint forcing a separator-vs-positive divergence at position `#d₁ + 1`. Case B (prefix-incomparable) correctly extracts a position-divergence witness `k ≤ min(#d₁, #d₂)` via length-sub-case analysis, recognizing that one side of the `⋠`-conjunction may be satisfied by length alone in asymmetric-length sub-cases. Both sub-cases B.i and B.ii are exhaustive by NAT-order trichotomy.

4. **Simultaneous induction** is correctly framed. The IH at each step is the conjunction of all transition-indexed properties; C2/L1a at the pre-state are consumed in the cross-document freshness derivations to ensure `origin(a') ∈ dom(M)` for prior store entries (so ChainMembershipForOrigin applies).

5. **C1c/L1c chain exhibitions** correctly construct two- and three-step chains respectively, with `k₁ = 2` and length-monotonicity satisfied. The L1c chain's `inc(b_C(d), 0) = b_L(d)` step depends on `s_L = s_C + 1`, which the ASN correctly identifies as load-bearing for SubspaceConventionAxiom.

6. **L14 derivation** (dom(C) ∩ dom(L) = ∅) via L0 + SC-NEQ + StoreT4Validity + T7 is sound; T7's preconditions are discharged at every reachable state.

7. **Worked example** covers all branches (K.σ, K.α first-emit, K.α subsequent-emit, K.λ first-emit, K.λ subsequent-emit, second-document registration, prefix-incomparable third-document registration) with concrete tumblers, verifying invariants at each successor state.

8. **References** use only foundation ASNs (0034, 0036, 0040, 0043). No invented notation duplicating foundation definitions.

9. **Cross-store freshness for K.σ** is correctly argued from zeros-count distinction (d has zeros = 2, content/link have zeros = 3, anchors have zeros = 3); no explicit clause needed.

10. **K.σ admitting addresses broader than Nelson's hierarchical baptism** is explicitly noted as a deliberate substrate-layer commitment; tightening is deferred to higher-layer document-introduction primitives.

The Open Questions section correctly defers link withdrawal, arrangement extension, concurrency, sub-allocator stratification beyond `s_C`/`s_L`, and the document-address discipline.

VERDICT: CONVERGED
