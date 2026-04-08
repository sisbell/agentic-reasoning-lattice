**TS2 (ShiftInjectivity).**

`(A v₁, v₂, n : n ≥ 1 ∧ #v₁ = #v₂ = m : shift(v₁, n) = shift(v₂, n) ⟹ v₁ = v₂)`

*Proof.* We show that the ordinal shift is injective: if two equal-length tumblers produce the same result when shifted by the same amount, they must be equal.

Fix v₁, v₂ ∈ T with #v₁ = #v₂ = m, and fix n ≥ 1. Assume shift(v₁, n) = shift(v₂, n). By OrdinalShift, this assumption is v₁ ⊕ δ(n, m) = v₂ ⊕ δ(n, m).

We apply TA-MTO (ManyToOne) with w = δ(n, m), a = v₁, b = v₂. We first verify its preconditions:

(i) δ(n, m) ∈ T and δ(n, m) > 0 — by OrdinalDisplacement, δ(n, m) = [0, ..., 0, n] with n ≥ 1, so its m-th component is positive.

(ii) #v₁ ≥ actionPoint(δ(n, m)) and #v₂ ≥ actionPoint(δ(n, m)) — the action point of δ(n, m) is m (OrdinalDisplacement), and #v₁ = #v₂ = m, so m ≥ m holds for both.

All preconditions are satisfied. TA-MTO's converse direction states: v₁ ⊕ δ(n, m) = v₂ ⊕ δ(n, m) implies v₁ᵢ = v₂ᵢ for all 1 ≤ i ≤ actionPoint(δ(n, m)) = m. We therefore have v₁ᵢ = v₂ᵢ for all 1 ≤ i ≤ m.

Since #v₁ = #v₂ = m and v₁ᵢ = v₂ᵢ at every position 1 ≤ i ≤ m, T3 (CanonicalRepresentation) gives v₁ = v₂. ∎

*Formal Contract:*
- *Preconditions:* v₁ ∈ T, v₂ ∈ T, n ≥ 1, #v₁ = #v₂ = m
- *Postconditions:* shift(v₁, n) = shift(v₂, n) ⟹ v₁ = v₂
