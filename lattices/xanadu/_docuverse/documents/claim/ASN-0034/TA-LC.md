### Cancellation properties of ⊕

TumblerAdd's constructive definition determines each component of the result from exactly one input. This makes the operation left-cancellative.

**TA-LC (LeftCancellation).** If a ⊕ x = a ⊕ y with both sides well-defined (TA0 satisfied for both), then x = y.

*Proof.* Let `k₁` be the action point of `x` and `k₂` the action point of `y`. Both exist because TA0 requires `Pos(x)` and `Pos(y)`, so each has at least one nonzero component. We eliminate both strict orderings.

**Case k₁ < k₂.** Every component of `y` before position `k₂` is zero, so `y_{k₁} = 0`. Position `k₁` falls in the prefix-copy region of `a ⊕ y`: `(a ⊕ y)_{k₁} = a_{k₁}`. In `a ⊕ x`, position `k₁` is the action point: `(a ⊕ x)_{k₁} = a_{k₁} + x_{k₁}`. From `a ⊕ x = a ⊕ y`, `a_{k₁} + x_{k₁} = a_{k₁}`, so by NAT-cancel (summand absorption, `m + n = m ⟹ n = 0`) with `m = a_{k₁}`, `n = x_{k₁}`, we get `x_{k₁} = 0`. But `k₁` is the action point of `x`, so `x_{k₁} > 0` — contradiction.

**Case k₂ < k₁.** Symmetric: `x_{k₂} = 0`, so `(a ⊕ x)_{k₂} = a_{k₂}` while `(a ⊕ y)_{k₂} = a_{k₂} + y_{k₂}`. By NAT-cancel, `y_{k₂} = 0`, contradicting `y_{k₂} > 0`.

By NAT-order's trichotomy, `k₁ = k₂`. Write `k` for this common action point.

**Positions i < k.** `xᵢ = 0 = yᵢ` by definition of action point.

**Position i = k.** `(a ⊕ x)_k = a_k + x_k` and `(a ⊕ y)_k = a_k + y_k`. From `a ⊕ x = a ⊕ y`, `a_k + x_k = a_k + y_k`, so `x_k = y_k` by NAT-cancel (left cancellation, `m + n = m + p ⟹ n = p`).

**Positions i > k.** Tail-copy region: `(a ⊕ x)_i = x_i` and `(a ⊕ y)_i = y_i`. From `a ⊕ x = a ⊕ y`, `x_i = y_i`.

**Length.** By T3, `#(a ⊕ x) = #(a ⊕ y)`. The result-length identity gives `#(a ⊕ w) = #w`, so `#x = #y`.

All components agree and `#x = #y`, so `x = y` by T3.  ∎

*Worked example.* Let a = [2, 5] and suppose a ⊕ x = a ⊕ y = [2, 8]. Suppose k_x = 1: then 2 + x₁ = 2 gives x₁ = 0, contradicting k_x = 1. So k_x = 2, and similarly k_y = 2. At position 2: 5 + x₂ = 8 gives x₂ = 3, and 5 + y₂ = 8 gives y₂ = 3. For i < k: x₁ = 0 = y₁. From `#(a ⊕ x) = #x`, #x = 2 = #y. By T3, x = y = [0, 3].

*Formal Contract:*
- *Preconditions:* a, x, y ∈ T; Pos(x); Pos(y); actionPoint(x) ≤ #a; actionPoint(y) ≤ #a; a ⊕ x = a ⊕ y
- *Depends:*
  - TumblerAdd (TumblerAdd) — prefix-copy, advance, tail-copy rules and result-length identity.
  - TA0 (WellDefinedAddition) — well-definedness of `a ⊕ x` and `a ⊕ y`.
  - TA-Pos (PositiveTumbler) — supplies `Pos(x)` and `Pos(y)` for action-point existence.
  - ActionPoint (ActionPoint) — action point as first nonzero component.
  - NAT-cancel (NatAdditionCancellation) — summand absorption and left cancellation on ℕ.
  - NAT-order (NatStrictTotalOrder) — trichotomy collapsing ruled-out orderings to equality.
  - T3 (CanonicalRepresentation) — component-wise and length agreement imply tumbler equality.
- *Postconditions:* x = y
