# Review of ASN-0053

## REVISE

### Issue 1: S8's sort step is not "well-defined" by T1 alone
**ASN-0053, S8 (NormalizationExistence)**: "Sort the component spans by start position (T1 makes this well-defined)."
**Problem**: T1 totally orders tumblers, but distinct spans can share a start position (SC case (iv) containment, case (v) equal). The sorted *sequence* is therefore not unique — only the start values are. The phrase "T1 makes this well-defined" conflates the well-definedness of the comparison with uniqueness of the sort. The algorithm's output is in fact independent of how ties are broken (the merge branch fires whenever start(σᵢ) ≤ r), and the result's uniqueness comes from S9 — but the proof does not argue this.
**Required**: Either (a) note explicitly that any sort consistent with non-decreasing starts works, with output uniqueness inherited from S9; or (b) extend the sort to a total order on spans (e.g., break ties by reach) and verify the loop invariant carries through that extension.

### Issue 2: S9 Case 1 collapses an N2 + N1 chain into a single citation
**ASN-0053, S9 (NormalizationUniqueness), Case 1**: "for j < i, reach(βⱼ) = reach(αⱼ) < start(αᵢ) by N2 on Σ̂₁"
**Problem**: N2 on Σ̂₁ gives only reach(αⱼ) < start(αⱼ₊₁), not reach(αⱼ) < start(αᵢ). Reaching start(αᵢ) requires chaining through N1 (start(αⱼ₊₁) < ... < start(αᵢ)). Case 2 of the same proof does spell this out ("by N2 ..., repeated application of N1 (start(αⱼ₊₁) < ... < start(αᵢ)), and non-emptiness"); Case 1 hand-waves the same step. Identical proof obligation, inconsistent treatment.
**Required**: Make the N2 + N1 chain in Case 1 explicit, matching Case 2's rigor. The same compression also affects the j > n sub-case (where i is past βᵢ's end, requiring chaining through the final reach(βₙ)).

### Issue 3: Span-set union Σ₁ ∪ Σ₂ used in S10 without definition
**ASN-0053, S10 (UnionOrderIndependence)**: "normalize(Σ₁ ∪ Σ₂) = normalize(Σ₂ ∪ Σ₁)"
**Problem**: A span-set is defined as a finite *sequence* ⟨σ₁, ..., σₙ⟩, but the operator ∪ between span-sets (concatenation? bag union?) is never defined. The denotation interpretation makes the meaning clear (⟦Σ₁ ∪ Σ₂⟧ = ⟦Σ₁⟧ ∪ ⟦Σ₂⟧), but the operator itself is uncited prior to use.
**Required**: Define Σ₁ ∪ Σ₂ explicitly as either concatenation of sequences or as the span-set whose denotation is ⟦Σ₁⟧ ∪ ⟦Σ₂⟧. Either choice is fine, but it should be stated.

## OUT_OF_SCOPE

None — the ASN respects its scope. The "Implementation observations" section is appropriately framed as observations (not properties), the "Open Questions" appropriately defer concerns about allocation interaction, cross-depth operations, and content-layer distinctions to future ASNs.

VERDICT: REVISE
