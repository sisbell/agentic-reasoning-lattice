**TA3-strict (OrderPreservationUnderSubtractionStrict).** `(A a, b, w : a < b ∧ a ≥ w ∧ b ≥ w ∧ #a = #b : a ⊖ w < b ⊖ w)`.

Subtracting a common lower bound from two equal-length tumblers preserves strict order.

*Proof.* Given `a, b, w ∈ T` with `a < b`, `a ≥ w`, `b ≥ w`, `#a = #b`, show `a ⊖ w < b ⊖ w`.

**The form of `a < b`.** Since `#a = #b`, T1 case (ii) (which requires `#a < #b`) is impossible. So `a < b` holds by case (i): there exists a least `j` with `1 ≤ j ≤ #a` such that `aᵢ = bᵢ` for all `i < j` and `aⱼ < bⱼ`. Fix this `j`.

**Well-formedness.** By TA2, `a ⊖ w, b ⊖ w ∈ T`.

Proceed by case analysis on the divergence structure of `(a, w)` and `(b, w)`.

**Case A: `a` is zero-padded-equal to `w`.** By TumblerSub, `a ⊖ w` is the zero tumbler of length `L_{a,w}`. For `i < j`: `bᵢ = aᵢ = wᵢ`. At position `j`: `wⱼ = aⱼ < bⱼ`, so `(b, w)` diverges at `j` and `(b ⊖ w)_j = bⱼ - wⱼ > 0` by NAT-sub (strict positivity). `(b ⊖ w)_i = 0` for `i < j`. Both results zero before `j`; at `j`, `(a ⊖ w)_j = 0 < bⱼ - wⱼ = (b ⊖ w)_j`. By T1 case (i), `a ⊖ w < b ⊖ w`.

**Setup for remaining cases.** Since `a` is not zero-padded-equal to `w`, `d_a = zpd(a, w)` is well-defined with `a_{d_a} > w_{d_a}` (from `a > w`, via T3's contrapositive giving `a ≠ w`, then T1 trichotomy). If `b` were zero-padded-equal to `w`, then `b_{d_a} = w_{d_a} < a_{d_a}` with agreement before `d_a`, giving `a > b` by T1 — contradiction. So `d_b = zpd(b, w)` is well-defined with `b_{d_b} > w_{d_b}`. By NAT-order trichotomy on `(d_a, d_b) ∈ ℕ × ℕ`, exactly one of `d_a = d_b`, `d_a < d_b`, `d_a > d_b` holds.

**Case 1: `d_a = d_b = d`.** By TumblerSub, `(a ⊖ w)_i = (b ⊖ w)_i = 0` for `i < d`. Since `a, b` agree with `w` before `d`, they agree with each other, so `j ≥ d`.

*Subcase `j = d`:* `(a ⊖ w)_d = a_d - w_d` and `(b ⊖ w)_d = b_d - w_d`, both in ℕ by NAT-sub (conditional closure) under `a_d, b_d ≥ w_d` (via NAT-order's `≤` from `<`). From `a_d < b_d` and NAT-sub strict monotonicity, `a_d - w_d < b_d - w_d`. Results agree before `d`, first disagree at `d`. By T1 case (i), `a ⊖ w < b ⊖ w`.

*Subcase `j > d`:* `a_d = b_d`, so `(a ⊖ w)_d = (b ⊖ w)_d`. For `d < i < j`: tail-copy gives `(a ⊖ w)_i = a_i = b_i = (b ⊖ w)_i`. At `j`: `(a ⊖ w)_j = aⱼ < bⱼ = (b ⊖ w)_j`. By T1 case (i), `a ⊖ w < b ⊖ w`.

**Case 2: `d_a < d_b`.** At `d_a`: `a_{d_a} ≠ w_{d_a}` but `b_{d_a} = w_{d_a}`. `a, b` agree with `w` (hence each other) before `d_a` and disagree at `d_a`, so `j = d_a`. From `a < b` by T1: `a_{d_a} < b_{d_a} = w_{d_a}`. But `a_{d_a} > w_{d_a}` — contradiction. Impossible.

**Case 3: `d_a > d_b`.** At `d_b`: `b_{d_b} ≠ w_{d_b}` but `a_{d_b} = w_{d_b}`. Agreement before `d_b`, disagreement at `d_b`, so `j = d_b`. From `a < b`: `a_{d_b} < b_{d_b}`, i.e., `w_{d_b} < b_{d_b}`.

For `a ⊖ w`: `d_b < d_a` places `d_b` in the pre-divergence zero phase, so `(a ⊖ w)_{d_b} = 0`. For `b ⊖ w`: `(b ⊖ w)_{d_b} = b_{d_b} - w_{d_b} > 0` by NAT-sub strict positivity. Both zero for `i < d_b`. First disagreement at `d_b` with `0 < b_{d_b} - w_{d_b}`. By T1 case (i), `a ⊖ w < b ⊖ w`.

In every case, `a ⊖ w < b ⊖ w`. ∎

*Formal Contract:*
- *Preconditions:* a ∈ T, b ∈ T, w ∈ T, a < b, a ≥ w, b ≥ w, #a = #b
- *Depends:*
  - T0 (CarrierSetDefinition) — carrier-set membership `a, b, w ∈ T`; length operator `#·`; native-domain component projection `·ᵢ ∈ ℕ` on `{1, ..., #·}`.
  - T1 (LexicographicOrder) — definition of `<`; ruling out case (ii) under `#a = #b`; converting first-divergence witnesses into strict ordering on differences; `≥ ∧ ≠ ⟹ >` trichotomy step.
  - T3 (CanonicalRepresentation) — contrapositive transports "not zero-padded-equal" to tumbler inequality at pairs `(a, w)` and `(b, w)`.
  - TumblerSub (TumblerSub) — definition of `x ⊖ w` (zero-padding, divergence discovery, three-region rule); componentwise computations.
  - ZPD (ZPD) — well-definedness of `d_a = zpd(a, w)`, `d_b = zpd(b, w)`; each index in ℕ.
  - TA2 (WellDefinedSubtraction) — `a ⊖ w, b ⊖ w ∈ T`.
  - NAT-sub (NatPartialSubtraction) — conditional closure of `a_d - w_d`, `b_d - w_d` in ℕ; strict positivity `b_j - w_j > 0`; strict monotonicity `a_d - w_d < b_d - w_d` from `a_d < b_d` with both `≥ w_d`.
  - NAT-zero (NatZeroMinimum) — `0 ∈ ℕ` for literal-`0` components of zero tumbler and pre-divergence clause; padded operand values `w_i = 0` at `i > #w`.
  - NAT-order (NatStrictTotalOrder) — trichotomy at length pairs `(#a, #b)`, `(#a, #w)`, `(#b, #w)` naming `L_{a,w}`, `L_{b,w}` without a primitive max operator; trichotomy at index pair `(d_a, d_b)` for the three-way case split; defining clause `m ≤ n ⟺ m < n ∨ m = n` converting `>` to `≥` for NAT-sub preconditions.
- *Postconditions:* a ⊖ w < b ⊖ w
