**TS1 (ShiftOrderPreservation).**

`(A v₁, v₂ ∈ T, n ∈ ℕ : n ≥ 1 ∧ #v₁ = #v₂ ∧ v₁ < v₂ : shift(v₁, n) < shift(v₂, n))`

*Proof.* Fix v₁, v₂ ∈ T with #v₁ = #v₂, v₁ < v₂, and n ≥ 1, and let m abbreviate #v₁. By OrdinalShift, shift(v₁, n) = v₁ ⊕ δ(n, m) and shift(v₂, n) = v₂ ⊕ δ(n, m), so it suffices to show v₁ ⊕ δ(n, m) < v₂ ⊕ δ(n, m). We discharge TA1-strict's eight preconditions with a = v₁, b = v₂, w = δ(n, m):

(i) v₁ ∈ T — hypothesis.

(ii) v₂ ∈ T — hypothesis.

(iii) δ(n, m) ∈ T — OrdinalDisplacement postcondition.

(iv) v₁ < v₂ — hypothesis.

(v) Pos(δ(n, m)) — OrdinalDisplacement postcondition.

(vi) actionPoint(δ(n, m)) ≤ #v₁ — actionPoint(δ(n, m)) = m (OrdinalDisplacement) and #v₁ = m, so m ≤ m.

(vii) actionPoint(δ(n, m)) ≤ #v₂ — similarly, #v₂ = m by hypothesis #v₁ = #v₂, so m ≤ m.

(viii) actionPoint(δ(n, m)) ≥ divergence(v₁, v₂) — from v₁ < v₂, T1 irreflexivity gives v₁ ≠ v₂. Since #v₁ = #v₂, Divergence case (ii) is excluded and case (i) applies, supplying k with 1 ≤ k ≤ #v₁, k ≤ #v₂, (v₁)ₖ ≠ (v₂)ₖ, and prior-position agreement, with divergence(v₁, v₂) = k. Then divergence(v₁, v₂) = k ≤ #v₁ = m.

By TA1-strict: v₁ ⊕ δ(n, m) < v₂ ⊕ δ(n, m), that is, shift(v₁, n) < shift(v₂, n). ∎

*Formal Contract:*
- *Preconditions:* v₁ ∈ T, v₂ ∈ T, n ∈ ℕ, n ≥ 1, #v₁ = #v₂, v₁ < v₂
- *Depends:*
  - OrdinalShift (OrdinalShift) — unfolds shift(v, n) = v ⊕ δ(n, #v).
  - OrdinalDisplacement (OrdinalDisplacement) — supplies δ(n, m) ∈ T, Pos(δ(n, m)), and actionPoint(δ(n, m)) = m.
  - Divergence (Divergence) — case (i) supplies the index k with 1 ≤ k ≤ #v₁, k ≤ #v₂, and divergence(v₁, v₂) = k; case (ii) is excluded by #v₁ = #v₂.
  - T3 (CanonicalRepresentation) — underwrites Divergence's exhaustiveness (used to rule out the residual configuration at the case-(ii)-exclusion step).
  - TA1-strict (StrictOrderPreservation) — load-bearing lemma: a < b with the eight preconditions yields a ⊕ w < b ⊕ w.
  - T0 (CarrierSetDefinition) — carrier T, length operator #·, component projection ·ᵢ.
  - T1 (LexicographicOrder) — the relation < on T, and irreflexivity used to derive v₁ ≠ v₂ from v₁ < v₂.
  - TA-Pos (PositiveTumbler) — definition of Pos(·).
  - ActionPoint (ActionPoint) — definition of actionPoint(·).
  - NAT-order (NatStrictTotalOrder) — ≤ on ℕ used in the length-bound and divergence-bound comparisons.
  - NAT-wellorder (NatWellOrdering) — least-element principle underwriting Divergence case (i)'s well-defined index k.
- *Postconditions:* shift(v₁, n) < shift(v₂, n)
