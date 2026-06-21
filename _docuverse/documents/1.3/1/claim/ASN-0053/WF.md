**WF (WellFormedSpanFromEndpoints).** For s, r ∈ T with s < r and #s = #r, the pair γ = (s, r ⊖ s) is a well-formed level-uniform span (satisfying T12) with reach(γ) = r.

*Proof.* The identity reach(γ) = r is the work of D1, whose preconditions at (a, b) = (s, r) are a ∈ T, b ∈ T, a < b, divergence(a, b) ≤ #a, and #a ≤ #b. Four are immediate: s, r ∈ T and s < r are hypotheses, and #s ≤ #r follows from #s = #r. The fifth — divergence(s, r) ≤ #s — we must establish, and we do so first.

Since s < r, T1's trichotomy disjointness `¬(s < r ∧ s = r)` gives s ≠ r, so divergence(s, r) is defined. T1 witnesses s < r by some k with 1 ≤ k and sᵢ = rᵢ for 1 ≤ i < k, falling in case (i) `k ≤ #s ∧ k ≤ #r ∧ sₖ < rₖ` or case (ii) `k = #s + 1 ≤ #r`. The equal-length hypothesis #s = #r excludes case (ii): it would force #s + 1 ≤ #s, impossible since #s < #s + 1. So case (i) holds — equal length admits only a component mismatch at a shared position, never a proper prefix — giving k ≤ #s and sₖ < rₖ, whence sₖ ≠ rₖ. The conjunction `1 ≤ k ∧ k ≤ #s ∧ k ≤ #r ∧ sₖ ≠ rₖ ∧ (A i : 1 ≤ i < k : sᵢ = rᵢ)` is exactly the qualifier of Divergence's case (i), whose uniqueness clause identifies k = divergence(s, r). Hence divergence(s, r) = k ≤ #s, discharging D1's remaining precondition.

The width r ⊖ s has a positive component at position k (namely rₖ − sₖ > 0, from sₖ < rₖ), so it is positive with action point k ≤ #s; T12 is satisfied. With all five preconditions in hand, D1 applies: reach(γ) = s ⊕ (r ⊖ s) = r. The span is level-uniform: #width(γ) = #(r ⊖ s) = max(#r, #s) = #s = #start(γ).  ∎

*Formal Contract:*

- *Preconditions:* s, r ∈ T with s < r and #s = #r.
- *Definition:* γ = (start(γ), width(γ)) = (s, r ⊖ s).
- *Postconditions:* γ is a well-formed level-uniform span satisfying T12 — its width r ⊖ s is positive with action point k ≤ #s, and #width(γ) = #start(γ); and reach(γ) = s ⊕ (r ⊖ s) = r.

- *Depends:*
  - T12 (SpanWellDefinedness, ASN-0034) — supplies the well-formedness predicate (Pos(ℓ) and actionPoint(ℓ) ≤ #s) that the proof verifies and the claim's conclusion targets
  - D1 (DisplacementRoundTrip, ASN-0034) — supplies the identity a ⊕ (b ⊖ a) = b used in the proof step reach(γ) = s ⊕ (r ⊖ s) = r; its precondition divergence(s, r) ≤ #s is discharged in the proof from T1 and Divergence
  - T1 (LexicographicOrder, ASN-0034) — its definition of s < r supplies the witness k (with sᵢ = rᵢ for 1 ≤ i < k) in case (i) `k ≤ #s ∧ k ≤ #r ∧ sₖ < rₖ` or case (ii) `k = #s + 1 ≤ #r`; #s = #r excludes case (ii), leaving k ≤ #s and sₖ ≠ rₖ; its trichotomy disjointness `¬(s < r ∧ s = r)` yields s ≠ r, well-defining divergence(s, r)
  - Divergence (Divergence, ASN-0034) — its case-(i) uniqueness clause identifies the T1 witness k with divergence(s, r), so k ≤ #s discharges D1's precondition divergence(s, r) ≤ #s