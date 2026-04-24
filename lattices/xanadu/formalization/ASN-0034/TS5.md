**TS5 (ShiftAmountMonotonicity).**

`(A v, n₁, n₂, m : v ∈ T ∧ n₁ ∈ ℕ ∧ n₂ ∈ ℕ ∧ n₁ ≥ 1 ∧ n₂ > n₁ ∧ #v = m : shift(v, n₁) < shift(v, n₂))`

Shifting a tumbler by a larger amount produces a strictly greater result.

*Proof.* Fix v ∈ T with m = #v, and n₁, n₂ ∈ ℕ with n₁ ≥ 1 and n₂ > n₁.

Define d = n₂ − n₁. By NAT-sub's conditional closure at `m = n₂, n = n₁` (using n₂ ≥ n₁ via NAT-order from n₂ > n₁), d ∈ ℕ. By NAT-sub's strict positivity at the same instantiation, d ≥ 1. By NAT-sub's left-inverse characterisation, n₁ + d = n₂.

Invoke TS3 (ShiftComposition) at u = v, a = n₁, b = d: shift(shift(v, n₁), d) = shift(v, n₁ + d) = shift(v, n₂).

Let u = shift(v, n₁). By OrdinalShift at v, n₁: u ∈ T and #u = m. Invoke TS4 (ShiftStrictIncrease) at u, n = d: shift(u, d) > u.

Substituting: shift(v, n₂) = shift(u, d) > u = shift(v, n₁), that is, shift(v, n₂) > shift(v, n₁). T1 (LexicographicOrder) defines the strict total order `<` on T, and the companion relation `>` on T abbreviates the converse — `a > b ⟺ b < a` — so the conclusion rewrites to shift(v, n₁) < shift(v, n₂). ∎

*Worked example.* Let v = [2, 3, 7] (m = 3), n₁ = 4, n₂ = 7. Then shift(v, 4) = [2, 3, 11] and shift(v, 7) = [2, 3, 14]. By T1's lexicographic ordering, [2, 3, 11] < [2, 3, 14]. ✓

*Formal Contract:*
- *Preconditions:* v ∈ T, n₁ ∈ ℕ, n₂ ∈ ℕ, n₁ ≥ 1, n₂ > n₁, #v = m
- *Depends:*
  - TS3 (ShiftComposition) — rewrites shift(v, n₂) as shift(shift(v, n₁), d).
  - TS4 (ShiftStrictIncrease) — yields shift(u, d) > u for u = shift(v, n₁).
  - OrdinalShift — supplies u ∈ T and #u = m for u = shift(v, n₁).
  - NAT-sub (NatPartialSubtraction) — conditional closure, strict positivity, and left-inverse characterisation applied to d = n₂ − n₁.
  - NAT-order (NatStrictTotalOrder) — converts n₂ > n₁ to n₂ ≥ n₁ for NAT-sub's weak-order preconditions.
  - T0 (CarrierSetDefinition) — length operator typing #·: T → ℕ and length axiom #a ≥ 1, licensing m = #v ∈ ℕ with m ≥ 1.
  - T1 (LexicographicOrder) — establishes the strict total order `<` on T and grounds the companion relation `>` as its converse (`a > b ⟺ b < a`), licensing the rewrite from `shift(v, n₂) > shift(v, n₁)` to `shift(v, n₁) < shift(v, n₂)` at the proof's conclusion and the comparison `[2, 3, 11] < [2, 3, 14]` in the worked example.
- *Postconditions:* shift(v, n₁) < shift(v, n₂)
