**TA1-strict (StrictOrderPreservation).** `(A a, b, w ∈ T : a < b ∧ Pos(w) ∧ actionPoint(w) ≤ #a ∧ actionPoint(w) ≤ #b ∧ actionPoint(w) ≥ divergence(a, b) : a ⊕ w < b ⊕ w)`.

Tumbler addition by `w` preserves strict order when the action point of `w` lies at or beyond the first disagreement between `a` and `b`. If the action point falls before divergence, both operands receive the same advance and copy the same tail, collapsing the order to equality (e.g. `a = [1, 3]`, `b = [1, 5]`, `w = [2]` with action point 1 gives `a ⊕ w = [3] = b ⊕ w`).

*Proof.* From `a < b` and T1 irreflexivity, `a ≠ b`, discharging Divergence's precondition. Let `j = divergence(a, b)` and let `k` be the action point of `w`. The preconditions give `k ≥ j`, `k ≤ #a`, `k ≤ #b`.

Rule out Divergence case (ii). NAT-order trichotomy at `(#a, #b)` yields `#a = #b`, `#a < #b`, or `#b < #a`. The first makes case (ii) inapplicable. Under `#a < #b`, case (ii-a) gives `j = #a + 1`, so `k ≥ #a + 1` with `k ≤ #a` gives `#a + 1 ≤ #a`. NAT-order's defining clause unfolds this to `#a + 1 < #a ∨ #a + 1 = #a`. NAT-addcompat gives `#a < #a + 1`; the first disjunct composes to `#a + 1 < #a + 1` by transitivity, the second by substitution. NAT-order irreflexivity refutes both. The `#b < #a` branch is symmetric at `n = #b`. So Divergence case (i) holds: `1 ≤ j`, `j ≤ #a`, `j ≤ #b`, `aⱼ ≠ bⱼ`, and `aᵢ = bᵢ` for all `1 ≤ i < j`.

Align the T1 witness with `j`. Foreclose T1 case (ii) for `a < b`: its agreement requirement at `i = j ≤ #a` would force `aⱼ = bⱼ`, contradicting `aⱼ ≠ bⱼ`. So T1 case (i) supplies some `k'` with `1 ≤ k' ≤ #a, #b`, `aₖ' < bₖ'`, and `aᵢ = bᵢ` for `1 ≤ i < k'`. NAT-order trichotomy at `(k', j)`: in `k' < j`, Divergence agreement at `i = k'` gives `aₖ' = bₖ'`; substituted into `aₖ' < bₖ'` this yields `aₖ' < aₖ'`, refuted by NAT-order irreflexivity. In `k' > j`, T1 agreement at `i = j` gives `aⱼ = bⱼ`, contradicting Divergence. At `k' = j`, T1 case (i) delivers `aⱼ < bⱼ`.

Recall TumblerAdd: for tumbler `x`, positive `w`, action point `k ≤ #x`, `(x ⊕ w)ᵢ = xᵢ` for `i < k`, `(x ⊕ w)ₖ = xₖ + wₖ`, `(x ⊕ w)ᵢ = wᵢ` for `i > k`. By TA0, `a ⊕ w, b ⊕ w ∈ T` and `#(a ⊕ w) = #w = #(b ⊕ w)`.

*Case 1: `k = j`.* For `i < k`, Divergence agreement gives `aᵢ = bᵢ`, so `(a ⊕ w)ᵢ = (b ⊕ w)ᵢ`. At `k = j`, `(a ⊕ w)ₖ = aₖ + wₖ` and `(b ⊕ w)ₖ = bₖ + wₖ`. Promote `aₖ < bₖ` to `aₖ + wₖ < bₖ + wₖ`: NAT-order's defining clause weakens to `aₖ ≤ bₖ`; NAT-addcompat's right order-compatibility lifts to `aₖ + wₖ ≤ bₖ + wₖ`; NAT-cancel refutes `aₖ + wₖ = bₖ + wₖ` (it would force `aₖ = bₖ`, contradicting `aₖ < bₖ` via irreflexivity); the defining clause then yields the strict inequality. ActionPoint gives `k ≤ #w`, so `k ≤ #(a ⊕ w)` and `k ≤ #(b ⊕ w)`. By T1 case (i), `a ⊕ w < b ⊕ w`.

*Case 2: `k > j`.* For `i < j`, Divergence agreement with TumblerAdd's prefix-copy rule gives `(a ⊕ w)ᵢ = aᵢ = bᵢ = (b ⊕ w)ᵢ`. At `j < k`, prefix-copy gives `(a ⊕ w)ⱼ = aⱼ < bⱼ = (b ⊕ w)ⱼ`. The case assumption `k > j` with ActionPoint's `k ≤ #w` gives `j < #w` (transitivity on the strict disjunct, substitution on the equality disjunct); weakened to `j ≤ #w` and rewritten under TA0 to `j ≤ #(a ⊕ w)` and `j ≤ #(b ⊕ w)`. By T1 case (i), `a ⊕ w < b ⊕ w`.

In both cases, `a ⊕ w < b ⊕ w`. ∎

*Formal Contract:*
- *Preconditions:* a ∈ T, b ∈ T, w ∈ T, a < b, Pos(w), actionPoint(w) ≤ #a, actionPoint(w) ≤ #b, actionPoint(w) ≥ divergence(a, b)
- *Depends:*
  - T0 (CarrierSetDefinition) — carrier `T`, length operator `#·`, component projection `·ᵢ` with components in ℕ.
  - T1 (LexicographicOrder) — irreflexivity; case (i) witness and agreement; case (ii) structure.
  - T3 (CanonicalRepresentation) — backs Divergence's exhaustiveness at the case-(ii) rule-out.
  - Divergence — supplies `j`, case (i) agreement and disagreement, case (ii) sub-case length structure.
  - TA-Pos (PositiveTumbler) — `Pos(w)` consumed by ActionPoint and TA0.
  - ActionPoint — fixes `k`; supplies `1 ≤ k ≤ #w`.
  - TA0 (WellDefinedAddition) — `a ⊕ w, b ⊕ w ∈ T`; length identity `#(a ⊕ w) = #w`.
  - TumblerAdd — constructive component-wise definition.
  - NAT-order (NatStrictTotalOrder) — trichotomy; defining clause `m ≤ n ⟺ m < n ∨ m = n`; transitivity of `<`; irreflexivity.
  - NAT-addcompat (NatAdditionOrderAndSuccessor) — strict successor `n < n + 1`; right order-compatibility `p ≤ n ⟹ p + m ≤ n + m`.
  - NAT-cancel (NatAdditionCancellation) — right cancellation `n + m = p + m ⟹ n = p`.
- *Postconditions:* a ⊕ w < b ⊕ w
