**TA0 (WellDefinedAddition).** `(A a, w ∈ T : Pos(w) ∧ actionPoint(w) ≤ #a : a ⊕ w ∈ T ∧ #(a ⊕ w) = #w)`.

TA0 exports TumblerAdd's first two postconditions as a single labelled well-definedness fact. The precondition's bound `actionPoint(w) ≤ #a` carries the non-strict relation `≤` on ℕ, grounded by NAT-order via the definition `m ≤ n ⟺ m < n ∨ m = n`.

*Proof.* Immediate from TumblerAdd's first two postconditions `a ⊕ w ∈ T` and `#(a ⊕ w) = #w` under the preconditions `a, w ∈ T`, `Pos(w)`, `actionPoint(w) ≤ #a`. ∎

*Formal Contract:*
- *Preconditions:* a ∈ T, w ∈ T, Pos(w), actionPoint(w) ≤ #a
- *Depends:*
  - TumblerAdd (TumblerAdd, this ASN) — supplies `a ⊕ w ∈ T` and `#(a ⊕ w) = #w` as postconditions.
  - T0 (CarrierSetDefinition, this ASN) — supplies carrier `T` and length operator `#`.
  - TA-Pos (PositiveTumbler, this ASN) — precondition `Pos(w)` ensures the action point exists.
  - ActionPoint (ActionPoint, this ASN) — defines `actionPoint(w)` used in the bound `actionPoint(w) ≤ #a`.
  - NAT-order (NatStrictTotalOrder) — supplies the non-strict relation `≤` on ℕ appearing in the precondition `actionPoint(w) ≤ #a`.
- *Postconditions:* a ⊕ w ∈ T, #(a ⊕ w) = #w
