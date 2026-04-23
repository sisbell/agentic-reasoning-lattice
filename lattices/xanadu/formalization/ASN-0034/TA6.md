**TA6 (ZeroTumblers).** No zero tumbler is a valid address, and every zero tumbler is less than every tumbler with a positive component under T1.

  `(A t ∈ T : Zero(t) ⟹ t is not a valid address)`

  `(A s, t ∈ T : Zero(s) ∧ (E j : 1 ≤ j ≤ #t : tⱼ > 0) ⟹ s < t)`

*Proof (from T0, T4, TA-Pos, TA-PosDom, NAT-zero, NAT-order).*

**Conjunct 1** (invalidity): Let `t ∈ T` with `Zero(t)`. Unpacking `Zero(t)` via TA-Pos gives `tᵢ = 0` for all `1 ≤ i ≤ #t`. From T0, `#t ≥ 1`, so `t₁` is defined and equals `0`. This violates T4's requirement `t₁ ≠ 0`, so `t` is not a valid address.

**Conjunct 2** (ordering): Let `s ∈ T` with `Zero(s)` and let `t ∈ T` satisfy `(E j : 1 ≤ j ≤ #t : tⱼ > 0)`. By T0, each `tⱼ ∈ ℕ`; NAT-zero gives `0 ≤ tⱼ`, and combined with NAT-order this yields `tⱼ > 0 ⟺ tⱼ ≠ 0`. The hypothesis is therefore `(E j : 1 ≤ j ≤ #t : tⱼ ≠ 0)`, which is `Pos(t)` by TA-Pos. Apply TA-PosDom's postcondition with `z := s` to conclude `s < t`. ∎

*Formal Contract:*
- *Depends:*
  - T0 (CarrierSetDefinition) — `#t ≥ 1` and components in ℕ.
  - T1 (LexicographicOrder) — strict total order `<` on T under which `s < t` is asserted.
  - T4 (HierarchicalParsing) — boundary clause `t₁ ≠ 0`.
  - TA-Pos (PositiveTumbler) — definitions of `Pos(t)` and `Zero(t)`.
  - TA-PosDom (PositiveDominatesZero) — postcondition `(A t ∈ T, z ∈ T : Pos(t) ∧ Zero(z) :: z < t)` cited directly.
  - NAT-zero (NatZeroMinimum) — lower bound `0 ≤ n` for `n ∈ ℕ`.
  - NAT-order (NatStrictTotalOrder) — `m ≤ n ⟺ m < n ∨ m = n` and irreflexivity of `<`, used to establish `tⱼ > 0 ⟺ tⱼ ≠ 0` on ℕ.
- *Postconditions:*
  (a) `(A t ∈ T : Zero(t) ⟹ t is not a valid address)`.
  (b) `(A s, t ∈ T : Zero(s) ∧ (E j : 1 ≤ j ≤ #t : tⱼ > 0) ⟹ s < t)`.

Zero tumblers serve as *sentinels*: they mark uninitialized values, denote "unbounded" when used as span endpoints, and act as lower bounds.
