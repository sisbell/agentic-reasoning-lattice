**TS4 (ShiftStrictIncrease).**

`(A v, n, m : v ∈ T ∧ n ∈ ℕ ∧ n ≥ 1 ∧ #v = m : shift(v, n) > v)`

The dummy `m` abbreviates `#v`: the range predicate `#v = m` binds `m` as the length of `v`, with `m ∈ ℕ` from T0's length typing `#·: T → ℕ` and `m ≥ 1` from T0's length axiom.

*Proof.* Fix v ∈ T, n ∈ ℕ with n ≥ 1, and let m = #v. By OrdinalShift, shift(v, n) = v ⊕ δ(n, m); we must show v ⊕ δ(n, m) > v.

Apply TA-strict with a = v and w = δ(n, m). Four preconditions:

*First: v ∈ T.* Directly from TS4's own precondition, under the identity substitution a ↦ v.

*Second: δ(n, m) ∈ T.* From OrdinalDisplacement's exported postcondition `δ(n, m) ∈ T`, under the substitution w ↦ δ(n, m).

*Third: Pos(δ(n, m)).* From OrdinalDisplacement's exported postcondition `Pos(δ(n, m))`.

*Fourth: actionPoint(δ(n, m)) ≤ #v.* From OrdinalDisplacement's exported postcondition `actionPoint(δ(n, m)) = m`. Since #v = m, we have m ≤ m.

By TA-strict: v ⊕ δ(n, m) > v, that is, shift(v, n) > v. ∎

*Formal Contract:*
- *Preconditions:* v ∈ T, n ∈ ℕ, n ≥ 1, #v = m
- *Depends:*
  - OrdinalShift (OrdinalShift) — unfolds `shift(v, n) = v ⊕ δ(n, m)`. Preconditions `v ∈ T`, `n ∈ ℕ`, `n ≥ 1` discharged from TS4's own preconditions under identity substitution.
  - OrdinalDisplacement (OrdinalDisplacement) — supplies exported postconditions `δ(n, m) ∈ T`, `Pos(δ(n, m))`, and `actionPoint(δ(n, m)) = m` at TA-strict's membership, positivity, and action-point precondition checks respectively.
  - TA-strict (StrictIncrease) — the load-bearing lemma: converts `Pos(w)` and `actionPoint(w) ≤ #a` into `a ⊕ w > a`.
  - T0 (CarrierSetDefinition) — length operator typing `#·: T → ℕ` supplies `m ∈ ℕ`; length axiom `#a ≥ 1 for all a ∈ T` supplies `m ≥ 1`. Both feed OrdinalDisplacement's `m ∈ ℕ` and `m ≥ 1` preconditions.
  - TA-Pos (PositiveTumbler) — defines the predicate `Pos(t) ⟺ (E i : 1 ≤ i ≤ #t : tᵢ ≠ 0)` consumed at TA-strict's first precondition.
  - ActionPoint (ActionPoint) — defines `actionPoint(w) = min({i : 1 ≤ i ≤ #w ∧ wᵢ ≠ 0})` consumed at TA-strict's second precondition.
- *Postconditions:* shift(v, n) > v
