# Review of ASN-0084

## REVISE

### Issue 1: Wrong foundation citation in CanonicalBlockDecomposition uniqueness proof
**ASN-0084, Canonical block decomposition, step (b)**: "v₁ + k₁ = v₁ + k₂ gives k₁ = k₂ (by TS2 when both ≥ 1; when one is 0, TS4 forces the other to be 0)"
**Problem**: TS2 (ShiftInjectivity) establishes `shift(v₁, n) = shift(v₂, n) ⟹ v₁ = v₂` — injectivity in the *start position* given the same shift amount. The step here needs injectivity in the *shift amount* given the same start position: `shift(v, k₁) = shift(v, k₂) ⟹ k₁ = k₂`. TS2 does not give this.
**Required**: Cite TS5 (ShiftAmountMonotonicity): if `k₁ < k₂` (both ≥ 1), then `shift(v₁, k₁) < shift(v₁, k₂)`, contradicting equality. Alternatively, cite TA-LC (LeftCancellation): `v₁ ⊕ δ(k₁, m) = v₁ ⊕ δ(k₂, m)` implies `δ(k₁, m) = δ(k₂, m)`, hence `k₁ = k₂`. Note: the second TS2 citation in the same proof — for the a₁ = a₂ step where `shift(a₁, k₁) = shift(a₂, k₁)` with `#a₁ = #a₂` — is correctly applied.

## OUT_OF_SCOPE

### Topic 1: Formal generalization from depth-2 to arbitrary V-position depth
**Why out of scope**: The ASN acknowledges the restriction and claims generalization is structurally identical via D-CTG-depth (ASN-0036). The depth-2 case carries all the essential structure. Formalizing the general case is a separate piece of work, not an error in this ASN.

VERDICT: REVISE
