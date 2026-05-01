**OrdinalShift (OrdinalShift).** For a tumbler v ∈ T of length m = #v and natural number n ≥ 1:

`shift(v, n) = v ⊕ δ(n, m) where m = #v`

*Derivation.* Discharge TA0's four preconditions. (i) v ∈ T by assumption. (ii) δ(n, m) ∈ T by OrdinalDisplacement's postcondition. (iii) Pos(δ(n, m)) by OrdinalDisplacement's postcondition. (iv) actionPoint(δ(n, m)) = m = #v by OrdinalDisplacement's postcondition, so actionPoint(δ(n, m)) ≤ #v.

OrdinalDisplacement's own preconditions discharge as: n ∈ ℕ and n ≥ 1 transfer from OrdinalShift's preconditions, with NAT-carrier supplying `ℕ` as the underlying set in which the membership `n ∈ ℕ` is asserted; m ∈ ℕ from T0's length typing `#·: T → ℕ` at v ∈ T, the codomain `ℕ` again grounded by NAT-carrier; m ≥ 1 from T0's length axiom `#a ≥ 1` at a = v.

By TA0, shift(v, n) = v ⊕ δ(n, m) ∈ T. By TumblerAdd: shift(v, n)ᵢ = vᵢ for i < m, and shift(v, n)ₘ = vₘ + n. TA0's postcondition `#(a ⊕ w) = #w` yields `#shift(v, n) = #δ(n, m)`; OrdinalDisplacement's `#δ(n, m) = m` and the binding m = #v complete `#shift(v, n) = #v`.

Component lower bound `shift(v, n)ₘ = vₘ + n ≥ 1`. T0 places vₘ ∈ ℕ. NAT-zero gives `0 ≤ vₘ`. NAT-addcompat right order-compatibility lifts to `vₘ + n ≥ 0 + n`. NAT-closure's additive identity rewrites to `vₘ + n ≥ n`. NAT-order composes `vₘ + n ≥ n` with precondition `n ≥ 1` into `vₘ + n ≥ 1` via its defining clause and transitivity of `<`. ∎

*Formal Contract:*
- *Preconditions:* v ∈ T, n ∈ ℕ, n ≥ 1
- *Definition:* shift(v, n) = v ⊕ δ(n, m) where m = #v
- *Depends:*
  - OrdinalDisplacement (OrdinalDisplacement) — constructs δ(n, m); supplies postconditions `δ(n, m) ∈ T`, `Pos(δ(n, m))`, `actionPoint(δ(n, m)) = m`, `#δ(n, m) = m`.
  - T0 (CarrierSetDefinition) — length operator typing `#·: T → ℕ` and length axiom `#a ≥ 1`; carrier characterisation places vₘ ∈ ℕ.
  - NAT-carrier (NatCarrierSet) — supplies `ℕ` as the underlying set for the Precondition membership clause `n ∈ ℕ`, and as the codomain of T0's length operator `#·: T → ℕ` instantiated at v to type m = #v ∈ ℕ — the depth argument passed to OrdinalDisplacement.
  - TA-Pos (PositiveTumbler) — defines the predicate `Pos(·)` consumed at TA0 precondition (iii).
  - ActionPoint (ActionPoint) — defines `actionPoint(·)` consumed at TA0 precondition (iv).
  - TA0 (WellDefinedAddition) — postconditions `a ⊕ w ∈ T` and `#(a ⊕ w) = #w`.
  - TumblerAdd (TumblerAdd) — piecewise component rule: prefix copy for i < m, advance `vₘ + n` at position m.
  - NAT-zero (NatZeroMinimum) — `(∀ n ∈ ℕ :: 0 ≤ n)` supplies `0 ≤ vₘ`.
  - NAT-addcompat (NatAdditionOrderAndSuccessor) — right order-compatibility lifts `0 ≤ vₘ` to `vₘ + n ≥ 0 + n`.
  - NAT-closure (NatArithmeticClosureAndIdentity) — additive identity `0 + n = n`.
  - NAT-order (NatStrictTotalOrder) — defining clause `m ≤ n ⟺ m < n ∨ m = n` and transitivity of `<` compose `vₘ + n ≥ n` with `n ≥ 1` into `vₘ + n ≥ 1`.
- *Postconditions:* shift(v, n) ∈ T, #shift(v, n) = #v, shift(v, n)ᵢ = vᵢ for i < #v, shift(v, n)_{#v} = v_{#v} + n ≥ 1
