# Review of ASN-0058

I worked through every proof carefully, checking foundation citations, edge cases (n=1, k=0, m=2 boundary, empty arrangements), and the interaction between block algebra and ASN-0034/ASN-0036 foundations.

## REVISE

(none)

## OUT_OF_SCOPE

(none)

**Notes on what I verified positively:**

- **M-int** (TumblerIntervalCharacterization): all four sub-arguments (Subspace agreement, Depth equality, Prefix agreement, Component-m reduction) are rigorous. The proof correctly handles the k=0 boundary via T3 and OrdinalShiftBase, with k≥1 via TumblerAdd.
- **M12a/M12b**: the run-disjointness and no-extension lemmas correctly factor the canonical uniqueness proof. The Equal Starts argument's use of M-aux to construct v' = v₁ + (k₂ − 1) and contradict R₂'s left-non-extension is sound.
- **M7-cov** (NonOverlap): the strict v₁ < v₂ premise correctly excludes M-int's k=0 case (which would collapse v₂=v₁), forcing v₂ ∈ V(β₁) and contradicting B2.
- **M16a** (OriginInvarianceUnderShift): the structural argument is detailed — z₃ = #a − #E(a) ≤ #a − 2 places the third separator zero strictly below the action point #a, so TumblerAdd's prefix-copy preserves the entire document prefix and all three zero positions. The conclusion that zeros(a+k)=3 (S7b) combined with positional agreement forces the same zero positions in a+k.
- **C0** (OrdinalDisplacementNecessity): the construction of the wⱼ family at j > uₘ correctly exploits divergence at index k < m to place infinitely many distinct depth-m tumblers in ⟦σ⟧, contradicting S8-fin.
- **C0a** (PrefixConfinement): both case (a) sub-arguments (proper-prefix via T1(ii), divergence via T1(i)) and case (b)'s J-minimality argument are sound; the m=1 note correctly explains why the precondition is sharp.
- **C2** (ResolutionWidthPreservation): the three-step set-equality argument (D_m = E, dom(f) = D_m, |E| = ℓ_m) is rigorous; Step 2 correctly invokes C0a to confine dom(f) to V_{u₁}(d_s) before applying S8-depth.

Cross-ASN references are limited to the named foundation ASNs (0034, 0036, 0053). The Span Algebra Analogy remark correctly explicates the relationship without taking it as an identity.

VERDICT: CONVERGED
