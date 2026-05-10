**TA1 (OrderPreservationUnderAddition).** `(A a, b, w : a < b ∧ Pos(w) ∧ actionPoint(w) ≤ #a ∧ actionPoint(w) ≤ #b : a ⊕ w ≤ b ⊕ w)`.

TA1 guarantees weak order preservation: positions in order before advancement remain in non-reversed order after.

*Proof.* Let `k = actionPoint(w)`. By TumblerAdd, for any `t ∈ T` with `k ≤ #t`, the result `t ⊕ w` is built in three regions: `(t ⊕ w)ᵢ = tᵢ` for `i < k`, `(t ⊕ w)ₖ = tₖ + wₖ`, and `(t ⊕ w)ᵢ = wᵢ` for `i > k`. By TA0, both `a ⊕ w` and `b ⊕ w` are well-defined members of `T` with length `#w`.

By T1, `a < b` gives two cases: (i) there exists `j` with `j ≤ #a ∧ j ≤ #b` and `aⱼ < bⱼ` and `aᵢ = bᵢ` for `i < j`, or (ii) `#a < #b` and `aᵢ = bᵢ` for `1 ≤ i ≤ #a`.

*Case (ii).* The precondition gives `k ≤ #a` directly. For `i < k`: `(a ⊕ w)ᵢ = aᵢ = bᵢ = (b ⊕ w)ᵢ`. At `i = k`: `aₖ = bₖ` gives `(a ⊕ w)ₖ = aₖ + wₖ = bₖ + wₖ = (b ⊕ w)ₖ`. For `i > k`: `(a ⊕ w)ᵢ = wᵢ = (b ⊕ w)ᵢ`. Lengths agree by TA0, so `a ⊕ w = b ⊕ w` by T3.

*Case (i).* Three sub-cases on `j` vs `k`.

*Sub-case `j < k`.* For `i < j`: `(a ⊕ w)ᵢ = aᵢ = bᵢ = (b ⊕ w)ᵢ`. At `j`: `(a ⊕ w)ⱼ = aⱼ < bⱼ = (b ⊕ w)ⱼ`. Position `j` witnesses T1 case (i): `a ⊕ w < b ⊕ w`.

*Sub-case `j = k`.* For `i < k`: `(a ⊕ w)ᵢ = aᵢ = bᵢ = (b ⊕ w)ᵢ`. At `k`: we must derive `aₖ + wₖ < bₖ + wₖ` from `aₖ < bₖ`. By NAT-order, `aₖ < bₖ` yields `aₖ ≤ bₖ`. By NAT-addcompat right order-compatibility with `m = wₖ`, `aₖ + wₖ ≤ bₖ + wₖ`. If `aₖ + wₖ = bₖ + wₖ`, then NAT-cancel right cancellation yields `aₖ = bₖ`, contradicting `aₖ < bₖ` by NAT-order irreflexivity. Hence `aₖ + wₖ < bₖ + wₖ` by NAT-order. Position `k` witnesses T1 case (i): `a ⊕ w < b ⊕ w`.

*Sub-case `j > k`.* Since `k < j`, `aₖ = bₖ`. For `i < k`: `(a ⊕ w)ᵢ = aᵢ = bᵢ = (b ⊕ w)ᵢ`. At `k`: `(a ⊕ w)ₖ = aₖ + wₖ = bₖ + wₖ = (b ⊕ w)ₖ`. For `i > k`: `(a ⊕ w)ᵢ = wᵢ = (b ⊕ w)ᵢ`. Lengths agree by TA0, so `a ⊕ w = b ⊕ w` by T3.

In every case, `a ⊕ w ≤ b ⊕ w`. ∎

*Formal Contract:*
- *Preconditions:* a ∈ T, b ∈ T, w ∈ T, a < b, Pos(w), actionPoint(w) ≤ #a, actionPoint(w) ≤ #b
- *Depends:*
  - T0 (CarrierSetDefinition) — carrier `T`, length `#·`, component projection `·ᵢ`.
  - T1 (LexicographicOrder) — case analysis on `a < b`; case (i) concludes strict ordering of results.
  - T3 (CanonicalRepresentation) — component-wise agreement with equal length yields equality.
  - TA0 (WellDefinedAddition) — `a ⊕ w`, `b ⊕ w ∈ T` with length `#w`.
  - TumblerAdd (TumblerAdd) — three-region piecewise structure of `⊕`.
  - TA-Pos (PositiveTumbler, this ASN) — supplies `Pos(w)`.
  - ActionPoint (ActionPoint, this ASN) — defines `actionPoint(·)` and yields `1 ≤ k ≤ #w`.
  - NAT-order (NatStrictTotalOrder) — weakening `<` to `≤`, irreflexivity, and reconstructing strict `<` from `≤` plus non-equality.
  - NAT-addcompat (NatAdditionOrderAndSuccessor) — right order-compatibility lifts `aₖ ≤ bₖ` to `aₖ + wₖ ≤ bₖ + wₖ`.
  - NAT-cancel (NatAdditionCancellation) — right cancellation rules out `aₖ + wₖ = bₖ + wₖ`.
- *Postconditions:* a ⊕ w ≤ b ⊕ w

Strict order preservation holds under a tighter condition. We first need a precise notion of where two tumblers first differ.
