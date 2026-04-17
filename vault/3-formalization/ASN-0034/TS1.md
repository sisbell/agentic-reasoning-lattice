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
- *Depends:* OrdinalShift (OrdinalShift) — invoked at the proof opening to unfold shift via addition of the displacement ("By OrdinalShift, shift(v₁, n) = v₁ ⊕ δ(n, m) and shift(v₂, n) = v₂ ⊕ δ(n, m), so we must show v₁ ⊕ δ(n, m) < v₂ ⊕ δ(n, m)"); without OrdinalShift the reduction to TA1-strict could not be performed. OrdinalDisplacement (OrdinalDisplacement) — invoked twice in the precondition checks: at (ii) for the structural form `δ(n, m) = [0, ..., 0, n]` and the positivity of its m-th component ("by OrdinalDisplacement, δ(n, m) = [0, ..., 0, n] with n ≥ 1, so its m-th component is positive"), and at (iii) for the action-point fact ("the action point of δ(n, m) is m (OrdinalDisplacement)"). Divergence (Divergence) — invoked at precondition (iv) to discharge the action-point-at-or-after-divergence requirement by ruling out the prefix-divergence case ("since #v₁ = #v₂ = m, Divergence case (ii) (prefix divergence) is excluded: it requires #v₁ ≠ #v₂") and bounding the remaining case ("case (i) applies: divergence(v₁, v₂) = min({j : 1 ≤ j ≤ m ∧ v₁ⱼ ≠ v₂ⱼ}), which satisfies divergence(v₁, v₂) ≤ m"). TA1-strict (StrictOrderPreservation) — invoked at the proof closing to convert the four discharged preconditions into the strict ordering of the sums ("All four preconditions hold. By TA1-strict: v₁ ⊕ δ(n, m) < v₂ ⊕ δ(n, m)"); TA1-strict is the load-bearing lemma the entire proof reduces to.
- *Postconditions:* shift(v₁, n) < shift(v₂, n)
