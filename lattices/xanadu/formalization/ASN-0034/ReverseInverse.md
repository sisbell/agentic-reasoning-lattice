**ReverseInverse (ReverseInverse).** `(A a, w : a ≥ w ∧ Pos(w) ∧ k = #a ∧ #w = k ∧ (A i : 1 ≤ i < k : aᵢ = 0) : (a ⊖ w) ⊕ w = a)`, where `k` is the action point of `w`.

*Proof.* Let `k` denote the action point of `w`, so `wᵢ = 0` for `i < k`.

**Step 1: structure of `y = a ⊖ w`.** TumblerSub zero-pads operands to common length `L` via NAT-order's trichotomy on `(#a, #w)`. The preconditions `k = #a` and `#w = k` give `#a = #w = k`, placing the pair in the equal-length sub-case with `L = k` and empty padding region. For `i < k`, both `aᵢ = 0` (precondition) and `wᵢ = 0` (action point), so operands agree before position `k`.

NAT-order's trichotomy at `(aₖ, wₖ)` gives three outcomes. If `aₖ < wₖ`, then T1 case (i) at position `k` yields `a < w`, contradicting `a ≥ w`. Two cases remain:

- If `aₖ = wₖ`: `a` and `w` agree everywhere, and TumblerSub's no-divergence branch produces the zero tumbler of length `k`.
- If `aₖ > wₖ`: ZPD's case-split identifies `zpd(a, w)` as defined; pre-`k` agreement together with ZPD's minimality fixes `k = zpd(a, w)`. TumblerSub's three-region rule produces `yᵢ = 0` for `i < k`, `yₖ = aₖ - wₖ > 0` (by NAT-sub's conditional closure and strict-positivity clauses), and no components beyond `k`.

Record:
- (Y1) `#y = k`
- (Y2) `yᵢ = 0` for `1 ≤ i < k`
- (Y3a) equality branch `aₖ = wₖ`: `yₖ = 0`
- (Y3b) divergence branch `aₖ > wₖ`: `yₖ = aₖ - wₖ > 0`

**Step 2: TA4 applies to `y` and `w`.** TA4's six preconditions hold: `y ∈ T` (TumblerSub carrier-membership), `w ∈ T`, `Pos(w)`, `k = #y` (Y1), `#w = k`, and `(A i : 1 ≤ i < k : yᵢ = 0)` (Y2). TA4 yields:

`(y ⊕ w) ⊖ w = y`  — (†)

**Step 3: `y ⊕ w = a` by contradiction via TA3-strict.** Assume `y ⊕ w ≠ a`.

*Carrier membership of `y ⊕ w`.* TumblerAdd's preconditions at `(y, w)`: `y ∈ T` (Step 2), `w ∈ T`, `Pos(w)`, and `actionPoint(w) ≤ #y` (from `actionPoint(w) = k = #y` via NAT-order's defining clause). TumblerAdd yields `y ⊕ w ∈ T`.

*Equal length.* `#(y ⊕ w) = #w = k = #a` by TumblerAdd's result-length identity.

*`y ⊕ w > w`.* By TumblerAdd, for `i < k`: `(y ⊕ w)ᵢ = yᵢ = 0 = wᵢ`. At `k`: `(y ⊕ w)ₖ = yₖ + wₖ`. We show `yₖ > 0`. Suppose `yₖ = 0`. In the divergence branch, Y3b gives `yₖ > 0`, contradicting the hypothetical via NAT-order's irreflexivity at `n = 0`. So we are in the equality branch: `y` is the zero tumbler of length `k`, and `aₖ = wₖ`. With pre-`k` agreement and `#a = #w = k`, T3 gives `a = w`. Then `(y ⊕ w)ₖ = 0 + wₖ = wₖ` (NAT-closure's additive identity), so `y ⊕ w = w = a`, contradicting `y ⊕ w ≠ a`. Hence `yₖ > 0`.

Promote to `yₖ + wₖ > wₖ`: NAT-order's defining clause weakens `yₖ > 0` to `0 ≤ yₖ`; NAT-addcompat's right order-compatibility lifts this to `yₖ + wₖ ≥ 0 + wₖ`; NAT-closure rewrites to `yₖ + wₖ ≥ wₖ`; NAT-cancel's summand absorption rules out the equality disjunct (which would force `yₖ = 0`); NAT-order's defining clause returns `yₖ + wₖ > wₖ`. T1 case (i) at position `k` gives `y ⊕ w > w`.

*Trichotomy contradiction.* By T1, since `y ⊕ w ≠ a`, either `y ⊕ w > a` or `y ⊕ w < a`.

*Case `y ⊕ w > a`:* TA3-strict with `a := a, b := y ⊕ w` yields `a ⊖ w < (y ⊕ w) ⊖ w`. Left side is `y` by definition; right side is `y` by (†). So `y < y`, contradicting T1's irreflexivity.

*Case `y ⊕ w < a`:* TA3-strict with `a := y ⊕ w, b := a` yields `(y ⊕ w) ⊖ w < a ⊖ w`. Left is `y` by (†); right is `y` by definition. Again `y < y`, contradicting irreflexivity.

Both cases impossible, so `y ⊕ w = a`. Therefore `(a ⊖ w) ⊕ w = a`. ∎

*Formal Contract:*
- *Preconditions:* `a ∈ T`, `w ∈ T`, `a ≥ w`, `Pos(w)`, `k = #a`, `#w = k`, `(A i : 1 ≤ i < k : aᵢ = 0)`, where `k` is the action point of `w`
- *Depends:*
  - TumblerSub — piecewise definition for structure of `y = a ⊖ w`; carrier-membership postcondition `a ⊖ w ∈ T`.
  - TumblerAdd — prefix-copy/advance rule for components of `y ⊕ w`; result-length identity `#(a ⊕ w) = #w`; carrier-membership postcondition `a ⊕ w ∈ T`.
  - TA-Pos (PositiveTumbler) — precondition `Pos(w)`.
  - ActionPoint — action-point function; `wᵢ = 0` for `i < actionPoint(w)`.
  - TA4 (PartialInverse) — yields `(y ⊕ w) ⊖ w = y`.
  - T1 (LexicographicOrder) — case (i) at divergence position `k`; trichotomy on `(y ⊕ w, a)`; irreflexivity.
  - T3 (CanonicalRepresentation) — yields `a = w` in the equality branch.
  - ZPD (ZeroPaddedDivergence) — case-split and minimality clauses keying TumblerSub's branches.
  - TA3-strict (OrderPreservationUnderSubtractionStrict) — applied at both trichotomy cases.
  - T0 (CarrierSetDefinition) — carrier `T`, length `#`, component projection with typing `aᵢ ∈ ℕ`.
  - NAT-sub — conditional closure and strict positivity for `aₖ - wₖ`.
  - NAT-addcompat — right order-compatibility for the strict-promotion chain.
  - NAT-closure — additive identity `0 + wₖ = wₖ`.
  - NAT-cancel — summand absorption ruling out `yₖ + wₖ = wₖ`.
  - NAT-zero — `0 ∈ ℕ` for the zero-valued components and inequalities.
  - NAT-order — trichotomy on length and component pairs; defining clause `m ≤ n ⟺ m < n ∨ m = n`; irreflexivity at `n = 0`.
- *Postconditions:* `(a ⊖ w) ⊕ w = a`
