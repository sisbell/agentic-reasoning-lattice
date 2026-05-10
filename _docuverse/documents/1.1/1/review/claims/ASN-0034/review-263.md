# Cone Review — ASN-0034/TS2 (cycle 4)

*2026-04-18 08:38*

### OrdinalDisplacement proof attributes `n ∈ ℕ` to the precondition `n ≥ 1` rather than to its own explicit `n ∈ ℕ` precondition
**Foundation**: OrdinalDisplacement (OrdinalDisplacement) — preconditions `n ∈ ℕ, m ∈ ℕ, n ≥ 1, m ≥ 1`; T0 (CarrierSetDefinition) — requires each component ∈ ℕ for carrier-set membership.
**ASN**: OrdinalDisplacement proof, carrier-set discharge: "T0's 'each component ∈ ℕ' clause is discharged at the m-th position by the precondition `n ≥ 1` placing `n ∈ ℕ`, and at the leading positions 1..m−1 by NAT-zero's axiom …"
**Issue**: The phrase "the precondition `n ≥ 1` placing `n ∈ ℕ`" derives a typing fact (`n ∈ ℕ`) from an order fact (`n ≥ 1`). Order statements do not supply carrier membership on their own — `n ≥ 1` presupposes `n ∈ ℕ` rather than establishing it. OrdinalDisplacement already has `n ∈ ℕ` as a distinct, named precondition (added in cycles 6/7), so the correct one-for-one routing is to cite that precondition directly for the m-th position's component-typing, reserving `n ≥ 1` for the separate `n ≠ 0` promotion and for the TA-Pos witness. Under the per-step discipline the sister site applies at `m ∈ ℕ` (cited explicitly via T0's length operator typing, not derived from `m ≥ 1`), the m-th position should likewise cite `n ∈ ℕ` verbatim.
**What needs resolving**: OrdinalDisplacement's proof must cite its own precondition `n ∈ ℕ` directly for T0's "each component ∈ ℕ" clause at position m, rather than attributing that typing to the precondition `n ≥ 1`. The Depends entry for T0 should also make the `n ∈ ℕ` → component-typing route explicit alongside the NAT-zero route for padding positions.
