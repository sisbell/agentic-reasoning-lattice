**TS2 (ShiftInjectivity).**

`(A v₁, v₂, n : n ≥ 1 ∧ #v₁ = #v₂ = m : shift(v₁, n) = shift(v₂, n) ⟹ v₁ = v₂)`

*Proof.* Fix v₁, v₂ ∈ T with #v₁ = #v₂ = m, and fix n ≥ 1. Assume shift(v₁, n) = shift(v₂, n). Since v₁, v₂ ∈ T, T0 (CarrierSetDefinition) gives m = #v₁ = #v₂ ≥ 1, so no empty-sequence case arises.

By OrdinalShift, the assumption rewrites as v₁ ⊕ δ(n, m) = v₂ ⊕ δ(n, m). We apply TA-MTO (ManyToOne) with w = δ(n, m), a = v₁, b = v₂, verifying its preconditions:

(i) δ(n, m) ∈ T and δ(n, m) > 0 — by OrdinalDisplacement, δ(n, m) = [0, ..., 0, n] with n ≥ 1 and m ≥ 1, so its m-th component is positive.

(ii) #v₁ ≥ actionPoint(δ(n, m)) and #v₂ ≥ actionPoint(δ(n, m)) — the action point of δ(n, m) is m (OrdinalDisplacement), and #v₁ = #v₂ = m, so m ≥ m holds for both.

All preconditions are satisfied. TA-MTO's converse direction gives v₁ᵢ = v₂ᵢ for all 1 ≤ i ≤ actionPoint(δ(n, m)) = m. Since #v₁ = #v₂ = m and all m components agree, T3 (CanonicalRepresentation) gives v₁ = v₂. ∎

*Formal Contract:*
- *Preconditions:* v₁ ∈ T, v₂ ∈ T, n ≥ 1, #v₁ = #v₂ = m
- *Depends:* T0 (CarrierSetDefinition) — invoked at the proof opening to rule out the empty-sequence degenerate case ("T0 (CarrierSetDefinition) gives m = #v₁ = #v₂ ≥ 1, so no empty-sequence case arises"); without T0 the m ≥ 1 lower bound on length would be unsourced. OrdinalShift (OrdinalShift) — invoked immediately after to rewrite `shift = · ⊕ δ(n, m)` ("By OrdinalShift, the assumption rewrites as v₁ ⊕ δ(n, m) = v₂ ⊕ δ(n, m)"); this is the reduction step that exposes a TA-MTO call. OrdinalDisplacement (OrdinalDisplacement) — invoked twice in the precondition checks: at (i) for the structural form `δ(n, m) = [0, ..., 0, n]` and the positivity of its m-th component, and at (ii) for the action-point fact ("the action point of δ(n, m) is m (OrdinalDisplacement)"). TA-MTO (ManyToOne) — invoked as the load-bearing lemma ("We apply TA-MTO (ManyToOne) with w = δ(n, m), a = v₁, b = v₂") whose converse direction yields the component-wise agreement `v₁ᵢ = v₂ᵢ` for `1 ≤ i ≤ m`. T3 (CanonicalRepresentation) — invoked at the proof closing to convert component-wise plus length agreement into tumbler equality ("Since #v₁ = #v₂ = m and all m components agree, T3 (CanonicalRepresentation) gives v₁ = v₂"); T3 supplies the principle that tumblers agreeing in length and at every component are equal.
- *Postconditions:* shift(v₁, n) = shift(v₂, n) ⟹ v₁ = v₂
