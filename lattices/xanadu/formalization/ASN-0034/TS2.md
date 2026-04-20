**TS2 (ShiftInjectivity).**

`(A v₁, v₂ ∈ T, n ∈ ℕ : n ≥ 1 ∧ #v₁ = #v₂ : shift(v₁, n) = shift(v₂, n) ⟹ v₁ = v₂)`

*Proof.* Fix v₁, v₂ ∈ T with #v₁ = #v₂, and fix n ≥ 1. Let m = #v₁ = #v₂. Assume shift(v₁, n) = shift(v₂, n). By T0, m ≥ 1.

Applying OrdinalShift at v = v₁ and at v = v₂ (preconditions `v ∈ T, n ∈ ℕ, n ≥ 1` transfer from hypothesis), the assumption rewrites as

v₁ ⊕ δ(n, m) = v₂ ⊕ δ(n, m).

Applying OrdinalDisplacement at (n, m): `n ∈ ℕ` and `n ≥ 1` transfer from hypothesis; `m ∈ ℕ` and `m ≥ 1` from T0's length typing and length axiom at v₁ ∈ T. Its postconditions give `δ(n, m) ∈ T`, `Pos(δ(n, m))`, and `actionPoint(δ(n, m)) = m`.

Apply TA-MTO with w = δ(n, m), a = v₁, b = v₂. Verifying its six preconditions:

(i) δ(n, m) ∈ T — OrdinalDisplacement.

(ii) Pos(δ(n, m)) — OrdinalDisplacement.

(iii) v₁ ∈ T — hypothesis.

(iv) v₂ ∈ T — hypothesis.

(v) #v₁ ≥ actionPoint(δ(n, m)) — reduces to m ≥ m via `actionPoint(δ(n, m)) = m` and `#v₁ = m`.

(vi) #v₂ ≥ actionPoint(δ(n, m)) — reduces to m ≥ m via `actionPoint(δ(n, m)) = m` and `#v₂ = m`.

TA-MTO's converse yields v₁ᵢ = v₂ᵢ for all 1 ≤ i ≤ m. Since #v₁ = #v₂ = m and all m components agree, T3 gives v₁ = v₂. ∎

*Formal Contract:*
- *Preconditions:* v₁ ∈ T, v₂ ∈ T, n ∈ ℕ, n ≥ 1, #v₁ = #v₂
- *Depends:*
  - T0 (CarrierSetDefinition) — length typing `#·: T → ℕ` and length axiom `#a ≥ 1 for a ∈ T`.
  - OrdinalShift (OrdinalShift) — rewrites `shift(v, n) = v ⊕ δ(n, m)`.
  - OrdinalDisplacement (OrdinalDisplacement) — exports `δ(n, m) ∈ T`, `Pos(δ(n, m))`, `actionPoint(δ(n, m)) = m`.
  - TA-Pos (PositiveTumbler) — defines the predicate `Pos(·)`.
  - ActionPoint (ActionPoint) — defines the operator `actionPoint(·)`.
  - TA-MTO (ManyToOne) — load-bearing lemma; converse yields component-wise agreement.
  - T3 (CanonicalRepresentation) — component-wise plus length agreement implies equality.
- *Postconditions:* shift(v₁, n) = shift(v₂, n) ⟹ v₁ = v₂
