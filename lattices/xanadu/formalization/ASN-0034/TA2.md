### Subtraction for width computation

Let `⊖` denote tumbler subtraction: given two positions, compute the displacement between them.

**TA2 (WellDefinedSubtraction).** For tumblers `a, w ∈ T` where `a ≥ w`, `a ⊖ w` is a well-defined tumbler in `T`.

*Proof.* By TumblerSub, subtraction zero-pads both operands to length `L`, where `L = #a` if `#a ≥ #w` and `L = #w` otherwise (by NAT-order trichotomy on `(#a, #w)`), then scans for the first position at which the padded sequences disagree.

*Case 1: no divergence.* The padded sequences of `a` and `w` agree at every position. TumblerSub produces `[0, ..., 0]` of length `L`. Since `#a ≥ 1` and `#w ≥ 1` by T0, `L ≥ 1`. Each component is `0 ∈ ℕ` by NAT-zero. Hence the result is in T.

*Case 2: divergence at position `k`.* TumblerSub defines `r = a ⊖ w` componentwise: `rᵢ = 0` for `i < k`, `rₖ = aₖ - wₖ`, `rᵢ = aᵢ` for `i > k` (zero-padded values throughout), with `#r = L`.

*Pre-divergence* (`i < k`): `rᵢ = 0 ∈ ℕ` by NAT-zero.

*Divergence point* (`i = k`): The padded sequences differ, so by T3 `a ≠ w`; combined with `a ≥ w` this gives `a > w` under T1.

- *Sub-case (i): T1 component divergence.* There exists a first position `j` with `j ≤ #a ∧ j ≤ #w`, `aⱼ > wⱼ`, and `aᵢ = wᵢ` for all `i < j`. By ZPD's minimality, `k = j`. At `k`, `aₖ > wₖ`, so `aₖ ≥ wₖ` by NAT-order, and NAT-sub yields `rₖ = aₖ - wₖ ∈ ℕ`.

- *Sub-case (ii): T1 prefix relationship.* `w` is a proper prefix of `a`: `#w < #a` and `aᵢ = wᵢ` for `i ≤ #w`. Padding extends `w` with zeros (NAT-zero) at positions `#w + 1` through `L = #a`. Some position `i > #w` has `aᵢ ≠ 0`, else the padded sequences would agree. By ZPD's minimality, `k = min{i : #w < i ≤ L ∧ aᵢ ≠ 0}`. At `k`, `aₖ ≠ 0 = wₖ`. From NAT-zero's `0 ≤ aₖ` and NAT-order's `m ≤ n ⟺ m < n ∨ m = n`, the `aₖ = 0` disjunct is excluded, yielding `aₖ > 0 = wₖ`. Then `aₖ ≥ wₖ` by NAT-order, and NAT-sub yields `rₖ = aₖ - 0 ∈ ℕ`.

*Tail* (`i > k`): `rᵢ = aᵢ` (zero-padded). If `i ≤ #a`, `aᵢ ∈ ℕ` by T0. If `i > #a`, `aᵢ = 0 ∈ ℕ` by NAT-zero.

The result has length `L ≥ 1` (since `#a ≥ 1` and `#w ≥ 1` by T0) with every component in ℕ, hence in T. ∎

*Formal Contract:*
- *Preconditions:* a ∈ T, w ∈ T, a ≥ w
- *Depends:*
  - TumblerSub (TumblerSub) — piecewise construction of `a ⊖ w`: zero-padding, divergence-based case split, componentwise definition, and result length `L`.
  - T0 (CarrierSetDefinition) — minimum-length `≥ 1`, component-typing in ℕ, and carrier-set membership criterion.
  - T1 (LexicographicOrder) — derives `a > w` from `a ≥ w ∧ a ≠ w`; supplies component-divergence and prefix cases at the divergence point.
  - T3 (CanonicalRepresentation) — `a = w` iff same length and components; used to conclude `a ≠ w` from the existence of a padded divergence.
  - ZPD (ZeroPaddedDivergence) — minimality property identifying `k = zpd(a, w)` in both sub-cases.
  - NAT-sub (NatPartialSubtraction) — conditional-closure clause discharging `rₖ ∈ ℕ` once `aₖ ≥ wₖ`.
  - NAT-zero (NatZeroMinimum) — supplies `0 ∈ ℕ` for literal zeros (pre-divergence components, tail padding past `#a`, prefix padding of `w`, and the zero tumbler of Case 1); lower bound `0 ≤ aₖ` for the `≠ 0 ⟹ > 0` step.
  - NAT-order (NatStrictTotalOrder) — trichotomy on `(#a, #w)` naming `L`; defining clause `m ≤ n ⟺ m < n ∨ m = n` used to convert strict inequalities into weak form for NAT-sub and to unfold `0 ≤ aₖ` in sub-case (ii).
- *Postconditions:* a ⊖ w ∈ T, #(a ⊖ w) = L where `L = #a` if `#a ≥ #w`, else `L = #w`.
