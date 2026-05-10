### Subtraction for width computation

Let `⊖` denote tumbler subtraction: given two positions, compute the displacement between them.

**TA2 (WellDefinedSubtraction).** For tumblers `a, w ∈ T` where `a ≥ w`, `a ⊖ w` is a well-defined tumbler in `T`.

*Proof.* By TumblerSub, subtraction zero-pads both operands to length `L`, where `L = #a` if `#a ≥ #w` and `L = #w` otherwise (by NAT-order trichotomy on `(#a, #w)`), then scans for the first position at which the padded sequences disagree.

*Case 1: no divergence.* The padded sequences of `a` and `w` agree at every position. TumblerSub produces `[0, ..., 0]` of length `L`. Since `#a ≥ 1` and `#w ≥ 1` by T0, `L ≥ 1`. Each component is `0 ∈ ℕ` by NAT-zero. Hence the result is in T.

*Case 2: divergence at position `k`.* TumblerSub defines `r = a ⊖ w` componentwise on ZPD's padded projections `â`, `ŵ`: `rᵢ = 0` for `i < k`, `rₖ = âₖ - ŵₖ`, `rᵢ = âᵢ` for `i > k`, with `#r = L`.

*Pre-divergence* (`i < k`): `rᵢ = 0 ∈ ℕ` by NAT-zero.

*Divergence point* (`i = k`): We must establish `a ≠ w` before T1 can fire, and T3 speaks of native components and lengths only — a padded disagreement at `k` does not invoke T3 directly. We argue by reductio. Suppose `a = w`. T3, instantiated at `(a, w)`, then yields `#a = #w` and `aᵢ = wᵢ` for `1 ≤ i ≤ #a`. NAT-order's trichotomy on `(#a, #w)` selects the equality case, so `L = #a = #w` and the padded domain `[1, L]` coincides with both native domains. By ZPD's padded-projection definition, for every `i` with `1 ≤ i ≤ L`, `âᵢ = aᵢ` (since `i ≤ #a`) and `ŵᵢ = wᵢ` (since `i ≤ #w`); hence `âᵢ = aᵢ = wᵢ = ŵᵢ`, so the padded sequences agree everywhere on `[1, L]`, contradicting Case 2's hypothesis that ZPD identifies a padded divergence at some `k ≤ L`. Therefore `a ≠ w`, and combined with `a ≥ w` this gives `a > w` under T1.

- *Sub-case (i): T1 component divergence.* There exists a first position `j` with `j ≤ #a ∧ j ≤ #w`, `aⱼ > wⱼ`, and `aᵢ = wᵢ` for all `i < j` (native projections, well-defined on the shared native domain). By ZPD's minimality, `k = j`. At `k`, `aₖ > wₖ`; since `k ≤ #a ∧ k ≤ #w` the padded projections coincide with native (`âₖ = aₖ`, `ŵₖ = wₖ`), giving `âₖ > ŵₖ`, so `âₖ ≥ ŵₖ` by NAT-order, and NAT-sub yields `rₖ = âₖ - ŵₖ ∈ ℕ`.

- *Sub-case (ii): T1 prefix relationship.* `w` is a proper prefix of `a`: `#w < #a` and `aᵢ = wᵢ` for `i ≤ #w` (native). ZPD's padded projection `ŵ` extends `w` with zeros (NAT-zero) at positions `#w + 1` through `L = #a`. Some position `i > #w` has `âᵢ ≠ 0` (with `âᵢ = aᵢ` from `i ≤ #a`), else the padded sequences would agree. By ZPD's minimality, `k = min{i : #w < i ≤ L ∧ âᵢ ≠ 0}`. At `k`, `âₖ ≠ 0 = ŵₖ`. From NAT-zero's `0 ≤ âₖ` and NAT-order's `m ≤ n ⟺ m < n ∨ m = n`, the `âₖ = 0` disjunct is excluded, yielding `âₖ > 0 = ŵₖ`. Then `âₖ ≥ ŵₖ` by NAT-order, and NAT-sub yields `rₖ = âₖ - ŵₖ ∈ ℕ`.

*Tail* (`i > k`): `rᵢ = âᵢ`. If `i ≤ #a`, `âᵢ = aᵢ ∈ ℕ` by T0. If `i > #a`, `âᵢ = 0 ∈ ℕ` by NAT-zero.

The result has length `L ≥ 1` (since `#a ≥ 1` and `#w ≥ 1` by T0) with every component in ℕ, hence in T. ∎

*Formal Contract:*
- *Preconditions:* a ∈ T, w ∈ T, a ≥ w
- *Depends:*
  - TumblerSub (TumblerSub) — piecewise construction of `a ⊖ w`: zero-padding, divergence-based case split, componentwise definition, and result length `L`.
  - T0 (CarrierSetDefinition) — minimum-length `≥ 1`, component-typing in ℕ, and carrier-set membership criterion.
  - T1 (LexicographicOrder) — derives `a > w` from `a ≥ w ∧ a ≠ w`; supplies component-divergence and prefix cases at the divergence point.
  - T3 (CanonicalRepresentation) — `a = w` iff same length and components; used in a reductio at the divergence point: assuming `a = w` propagates equal lengths and native component equality, which under NAT-order's equality case on `(#a, #w)` extends via ZPD's padded-projection definition to padded equality on `[1, L]`, contradicting Case 2's padded divergence at `k`.
  - ZPD (ZeroPaddedDivergence) — minimality property identifying `k = zpd(a, w)` in both sub-cases.
  - NAT-sub (NatPartialSubtraction) — conditional-closure clause discharging `rₖ ∈ ℕ` once `âₖ ≥ ŵₖ` (instantiated on ZPD's padded projections so the operands are well-defined when `k > #w`).
  - NAT-zero (NatZeroMinimum) — supplies `0 ∈ ℕ` for literal zeros (pre-divergence components, ZPD's padded extension of `a` past `#a`, ZPD's padded extension of `w` past `#w`, and the zero tumbler of Case 1); lower bound `0 ≤ âₖ` for the `≠ 0 ⟹ > 0` step.
  - NAT-order (NatStrictTotalOrder) — trichotomy on `(#a, #w)` naming `L`; defining clause `m ≤ n ⟺ m < n ∨ m = n` used to convert strict inequalities into weak form for NAT-sub and to unfold `0 ≤ âₖ` in sub-case (ii).
- *Postconditions:* a ⊖ w ∈ T, #(a ⊖ w) = L where `L = #a` if `#a ≥ #w`, else `L = #w`.
