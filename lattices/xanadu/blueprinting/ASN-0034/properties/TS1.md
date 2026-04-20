**TS1 (ShiftOrderPreservation).**

`(A v₁, v₂, n : n ≥ 1 ∧ #v₁ = #v₂ = m ∧ v₁ < v₂ : shift(v₁, n) < shift(v₂, n))`

*Proof.* We show that shifting two equal-length tumblers by the same amount preserves their strict ordering.

Fix v₁, v₂ ∈ T with #v₁ = #v₂ = m, v₁ < v₂, and n ≥ 1. By OrdinalShift, shift(v₁, n) = v₁ ⊕ δ(n, m) and shift(v₂, n) = v₂ ⊕ δ(n, m), so we must show v₁ ⊕ δ(n, m) < v₂ ⊕ δ(n, m). We verify the four preconditions of TA1-strict with w = δ(n, m):

(i) v₁ < v₂ — given.

(ii) δ(n, m) > 0 — by OrdinalDisplacement, δ(n, m) = [0, ..., 0, n] with n ≥ 1, so its m-th component is positive.

(iii) actionPoint(δ(n, m)) ≤ min(#v₁, #v₂) — the action point of δ(n, m) is m (OrdinalDisplacement), and min(#v₁, #v₂) = min(m, m) = m, so m ≤ m holds.

(iv) actionPoint(δ(n, m)) ≥ divergence(v₁, v₂) — since #v₁ = #v₂ = m, Divergence case (ii) (prefix divergence) is excluded: it requires #v₁ ≠ #v₂. Since v₁ < v₂ implies v₁ ≠ v₂, case (i) applies: divergence(v₁, v₂) = min({j : 1 ≤ j ≤ m ∧ v₁ⱼ ≠ v₂ⱼ}), which satisfies divergence(v₁, v₂) ≤ m. The action point m ≥ divergence(v₁, v₂) follows.

All four preconditions hold. By TA1-strict: v₁ ⊕ δ(n, m) < v₂ ⊕ δ(n, m), that is, shift(v₁, n) < shift(v₂, n). ∎

*Formal Contract:*
- *Preconditions:* v₁ ∈ T, v₂ ∈ T, n ≥ 1, #v₁ = #v₂ = m, v₁ < v₂
- *Postconditions:* shift(v₁, n) < shift(v₂, n)
