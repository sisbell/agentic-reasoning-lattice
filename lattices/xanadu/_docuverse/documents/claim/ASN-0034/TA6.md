**TA6 (ZeroTumblers).** No zero tumbler is a valid address.

  `(A t ∈ T : Zero(t) ⟹ t is not a valid address)`

*Proof (from T0, T4, TA-Pos).* Let `t ∈ T` with `Zero(t)`. Unpacking `Zero(t)` via TA-Pos gives `tᵢ = 0` for all `1 ≤ i ≤ #t`. From T0, `#t ≥ 1`, so `t₁` is defined and equals `0`. This violates T4's requirement `t₁ ≠ 0`, so `t` is not a valid address. ∎

*Formal Contract:*
- *Depends:*
  - T0 (CarrierSetDefinition) — `#t ≥ 1` and components in ℕ.
  - T4 (HierarchicalParsing) — boundary clause `t₁ ≠ 0`.
  - TA-Pos (PositiveTumbler) — definition of `Zero(t)`.
- *Forward References:*
  - TA-PosDom (PositiveDominatesZero) — uses zero tumblers as the dominated class in its ordering result; TA6 sentinels are the context for that pairing.
- *Postcondition:* `(A t ∈ T : Zero(t) ⟹ t is not a valid address)`.

Zero tumblers thus exist in `T` but lie outside the address-valid subset; paired with TA-PosDom's ordering result they act as sentinels — uninitialized markers, unbounded span endpoints, and lower bounds.
