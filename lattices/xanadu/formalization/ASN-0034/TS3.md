**TS3 (ShiftComposition).**

`(A v, n₁, n₂, m : v ∈ T ∧ n₁ ∈ ℕ ∧ n₂ ∈ ℕ ∧ n₁ ≥ 1 ∧ n₂ ≥ 1 ∧ #v = m : shift(shift(v, n₁), n₂) = shift(v, n₁ + n₂))`

The binder's `#v = m` fixes `m` as the length of `v`; with `v ∈ T`, T0 gives `m ∈ ℕ` and `m ≥ 1`.

*Proof.* Fix `v ∈ T`, `n₁, n₂ ∈ ℕ` with `n₁, n₂ ≥ 1`, and let `m = #v`.

**Left side.** By OrdinalShift, `shift(v, n₁) = v ⊕ δ(n₁, m)` with `actionPoint(δ(n₁, m)) = m ≤ m = #v`. Let `u = v ⊕ δ(n₁, m)`. By TumblerAdd with `k = m`:

- For `1 ≤ i < m`: `uᵢ = vᵢ`.
- At `i = m`: `uₘ = vₘ + n₁`.
- `#u = #δ(n₁, m) = m` by TA0's length postcondition.

By TA0's carrier postcondition, `u ∈ T`. By OrdinalShift, `shift(u, n₂) = u ⊕ δ(n₂, m)` with `actionPoint(δ(n₂, m)) = m ≤ m = #u`. Let `L = u ⊕ δ(n₂, m)`. By TumblerAdd with `k = m`:

- For `1 ≤ i < m`: `Lᵢ = uᵢ = vᵢ`.
- At `i = m`: `Lₘ = uₘ + n₂ = (vₘ + n₁) + n₂`.
- `#L = m`.

**Right side.** By NAT-closure, `n₁ + n₂ ∈ ℕ`. We derive `n₁ + n₂ ≥ 1` via the chain `n₁ + n₂ ≥ 1 + n₂ ≥ 1 + 1 ≥ 1`: the first step applies NAT-addcompat right order-compatibility to `1 ≤ n₁`; the second applies NAT-addcompat left order-compatibility to `1 ≤ n₂`; the third unfolds NAT-addcompat's strict successor inequality `1 < 1 + 1` through NAT-order's defining clause `m ≤ n ⟺ m < n ∨ m = n`. By OrdinalShift, `shift(v, n₁ + n₂) = v ⊕ δ(n₁ + n₂, m)` with `actionPoint(δ(n₁ + n₂, m)) = m ≤ m = #v`. Let `R = v ⊕ δ(n₁ + n₂, m)`. By TumblerAdd with `k = m`:

- For `1 ≤ i < m`: `Rᵢ = vᵢ`.
- At `i = m`: `Rₘ = vₘ + (n₁ + n₂)`.
- `#R = m`.

**Comparison.** `#L = m = #R`. For `1 ≤ i < m`: `Lᵢ = vᵢ = Rᵢ`. At `i = m`: by T0, `vₘ ∈ ℕ`; by NAT-addassoc at `(vₘ, n₁, n₂)`, `(vₘ + n₁) + n₂ = vₘ + (n₁ + n₂)`, so `Lₘ = Rₘ`. By T3, `L = R`. ∎

*Formal Contract:*
- *Preconditions:* v ∈ T, n₁ ∈ ℕ, n₂ ∈ ℕ, n₁ ≥ 1, n₂ ≥ 1, #v = m
- *Depends:*
  - OrdinalShift (OrdinalShift) — unfolds `shift(·, n) = · ⊕ δ(n, m)` at each of three shift sites.
  - OrdinalDisplacement (OrdinalDisplacement) — fixes `δ(n, m) = [0, ..., 0, n]` with `actionPoint = m`, and exports `Pos(δ(n, m))` and `δ(n, m) ∈ T`.
  - T0 (CarrierSetDefinition) — length operator typing `#·: T → ℕ` and length axiom `#a ≥ 1` supply `m ∈ ℕ` and `m ≥ 1`; carrier characterisation places `vₘ ∈ ℕ`.
  - TA-Pos (PositiveTumbler) — defines `Pos(·)` consumed at TA0's third precondition.
  - ActionPoint (ActionPoint) — defines `actionPoint(·)` consumed at TA0's fourth precondition.
  - NAT-closure (NatArithmeticClosureAndIdentity) — addition-closure supplies `n₁ + n₂ ∈ ℕ`.
  - NAT-addcompat (NatAdditionOrderAndSuccessor) — left/right order compatibility and strict successor inequality supply the chain `n₁ + n₂ ≥ 1 + n₂ ≥ 1 + 1 ≥ 1`.
  - NAT-order (NatStrictTotalOrder) — defining clause `m ≤ n ⟺ m < n ∨ m = n` and transitivity of `<` compose the chain into `n₁ + n₂ ≥ 1`.
  - TA0 (WellDefinedAddition) — discharges each `⊕`'s action-point precondition, supplies result-length `#(a ⊕ w) = #w`, and supplies `u ∈ T` for the second shift.
  - TumblerAdd (TumblerAdd) — three-region rule producing `uᵢ`, `Lᵢ`, `Rᵢ`.
  - NAT-addassoc (NatAdditionAssociative) — `(vₘ + n₁) + n₂ = vₘ + (n₁ + n₂)` at the comparison step.
  - T3 (CanonicalRepresentation) — component-wise and length agreement implies tumbler equality.
- *Postconditions:* shift(shift(v, n₁), n₂) = shift(v, n₁ + n₂)
- *Frame:* #shift(shift(v, n₁), n₂) = #v = m
