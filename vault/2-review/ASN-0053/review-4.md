# Review of ASN-0053

## REVISE

### Issue 1: S9 proof Case 2 sub-case 2b overclaims coverage

**ASN-0053, S9 (NormalizationUniqueness)**: "Sub-case 2b: p ≥ start(αᵢ₊₁). Then the gap [reach(αᵢ), start(αᵢ₊₁)) is non-empty ... and every position in this gap lies in ⟦βᵢ⟧ ⊆ S but not in ⟦Σ̂₁⟧."

**Problem**: The claim "every position in this gap lies in ⟦βᵢ⟧" requires reach(βᵢ) ≥ start(αᵢ₊₁), which is not established. We know reach(βᵢ) > reach(αᵢ) (Case 2 assumption) and start(αᵢ₊₁) > reach(αᵢ) (N2 on Σ̂₁), but the relationship between reach(βᵢ) and start(αᵢ₊₁) is undetermined. If reach(βᵢ) < start(αᵢ₊₁), positions in [reach(βᵢ), start(αᵢ₊₁)) are not in ⟦βᵢ⟧, and the universal claim fails.

The contradiction still holds — but from a specific witness, not the universal claim. Moreover, the entire sub-case split is unnecessary. Setting p = reach(αᵢ) from the start of Case 2 gives a direct proof:

- p ∈ ⟦βᵢ⟧: start(βᵢ) = start(αᵢ) < reach(αᵢ) = p and p < reach(βᵢ). ✓
- p ∉ ⟦αᵢ⟧: p = reach(αᵢ) is the exclusive upper bound. ✓
- p ∉ ⟦αⱼ⟧ for j < i: p ≥ reach(αᵢ) > reach(αⱼ) by chaining N2. ✓
- p ∉ ⟦αⱼ⟧ for j > i: p = reach(αᵢ) < start(αᵢ₊₁) ≤ start(αⱼ) by N2 and N1. ✓

Contradiction: p ∈ S but p ∉ ⟦Σ̂₁⟧ = S. No sub-cases required.

**Required**: Either (a) choose p = reach(αᵢ) at the start of Case 2, eliminating sub-cases entirely, or (b) in sub-case 2b, replace "every position in this gap lies in ⟦βᵢ⟧" with "the position reach(αᵢ) lies in this gap (since reach(αᵢ) < start(αᵢ₊₁) by N2) and in ⟦βᵢ⟧ (since start(βᵢ) < reach(αᵢ) < reach(βᵢ))."

## OUT_OF_SCOPE

None. The ASN is well-scoped. The open questions identify the natural extensions (cross-level operations, normalization stability under allocation, subspace boundaries) appropriately.

VERDICT: REVISE
