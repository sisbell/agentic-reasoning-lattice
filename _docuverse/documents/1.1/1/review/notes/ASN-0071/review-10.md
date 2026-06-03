# Review of ASN-0071

I checked the load-bearing proofs (subspace confinement, the `iaddrs ⊆ dom(C)` subset claim, the `resolve` equality, F-FIN, F-CUR), the worked scenario, and the boundary cases the guidance demands.

## Verified

**Subspace confinement proof.** Airtight. For `t ∈ ⟦σ⟧`, the argument `(u⊕ℓ)₁ = u₁` (prefix-copy, since `1 < actionPoint(ℓ)`) followed by the two trichotomy exclusions (`t₁ < u₁ ⟹ t < u`; `t₁ > (u⊕ℓ)₁ ⟹ t > u⊕ℓ`, both via T1 case (i) at position 1) is complete and holds at every depth, since only position 1 is consulted. The `actionPoint(ℓ) ≥ 2` precondition is genuinely load-bearing and the `u=[1,5], ℓ=[2,0]` counter-example correctly exhibits a straddling span.

**Subset claim `iaddrs(Q)(Σ) ⊆ dom(Σ.C)`.** Confinement gives every consulted `v` subspace `s_C`; S3★ routes the image to `dom(C)`. State-dependence on both sides handled explicitly. Sound.

**`resolve` equality.** The chain through C1a (unique decomposition of `f = M(d_s)|⟦σ⟧`), B1 coverage (`dom(f) = ⟦σ⟧ ∩ dom(M(d_s))`), and B3 consistency is shown step-by-step, with set-flattening dedup correctly reconciled against M14. Not a hand-wave.

**Edge cases.** Empty query (F-EMPTY), unresolvable positions (F-FILT, charitable reading justified as a substantive choice), zero-width spans (excluded by `Pos(ℓ)`), empty source arrangement (vspec relaxation), multi-source queries (source locality), and the home/transcluding distinction are all addressed. The worked scenario verifies F-SHARE, F-DIST, F-PART, F-FILT, F-CUR against a concrete two-document transclusion state.

**F-FIN.** The three-step induction correctly bounds against the *elementary* transition count, handles the multi-K.δ composite, and notes `E₀ = {n₀}` gives `(E₀)_doc = ∅`. Sound.

**F-CUR.** Derivation correct — `find` reads only `E_doc` and `M`; the hypothesis covers `M(d_s)` for query sources since vspecs require `d_s ∈ E_doc`.

I could find no missing case, no proof by "similarly," no unestablished conjunct, and no non-foundation cross-ASN reference (citations are to 0047/0053/0058 and to bare tumbler notation). The operation is a pure query, so the absence of weakest-precondition/state-preservation analysis is appropriate rather than a gap. The `[3,0)` glyph in the counter-example is a compressed but recoverable shorthand for the half-open upper bound; it does not impair the argument.

The ASN is rigorous and complete on its own terms.

VERDICT: CONVERGED
