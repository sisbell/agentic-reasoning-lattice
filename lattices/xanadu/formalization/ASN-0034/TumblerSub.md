## Tumbler subtraction

**TumblerSub (TumblerSub).** Given two tumblers `a` (minuend) and `w` (subtrahend), compute their component-wise difference at the first point of zero-padded divergence. When the operands have different lengths, zero-pad the shorter to the length of the longer: `aᵢ = 0` for `i > #a` and `wᵢ = 0` for `i > #w`. NAT-order's trichotomy on `(#a, #w)` selects exactly one of: (α) `#a = #w` with `L = #a`; (β) `#a < #w` with `L = #w`; (γ) `#w < #a` with `L = #a`. When the zero-padded sequences agree at every position, the result is the zero tumbler of length `L`: `a ⊖ w = [0, ..., 0]`. Otherwise, `zpd(a, w)` is defined (ZPD) — write `k = zpd(a, w)`. The result is:

```
         ⎧ 0             if i < k
rᵢ   =  ⎨ aₖ - wₖ      if i = k
         ⎩ aᵢ           if i > k
```

The result has length `L`.

**Precondition:** `a ≥ w` (T1). We prove that when `zpd(a, w)` is defined, this entails `aₖ > wₖ` at `k = zpd(a, w)`. Since zpd is defined, `a` and `w` are not zero-padded-equal (ZPD), so by T3 (contrapositive) `a ≠ w`; combined with `a ≥ w`, this yields `w < a` (T1). Two Divergence cases arise for the pair `(w, a)` with `w ≠ a`:

  (i) Component divergence at position `k` with `k ≤ #w ∧ k ≤ #a` and `wₖ ≠ aₖ`. ZPD's Relationship-to-Divergence gives `zpd(a, w) = divergence(a, w) = k`. Since `w < a` via T1 case (i), `wₖ < aₖ`, whence `aₖ > wₖ`.

  (ii) Prefix divergence splits via NAT-order's trichotomy on `(#w, #a)` into sub-case (ii-a) `#w < #a` with `wᵢ = aᵢ` for `1 ≤ i ≤ #w`, and sub-case (ii-b) `#a < #w` with `wᵢ = aᵢ` for `1 ≤ i ≤ #a`. Sub-case (ii-b) is eliminated: its prefix hypothesis yields `a < w` via T1 case (ii), contradicting `w < a`. In sub-case (ii-a), `w` is a proper prefix of `a`. The padded extension sets `wᵢ = 0` for `i > #w`. Since zpd is defined, the padded sequences disagree somewhere (ZPD, contrapositive); the prefix agreement rules out positions `1 ≤ i ≤ #w`, so the disagreement lies at some `i > #w`. By ZPD's minimality, `k > #w`, whence `wₖ = 0` by zero-padding and `aₖ ≠ 0`. From NAT-zero's `0 ≤ aₖ` and NAT-order's `m ≤ n ⟺ m < n ∨ m = n`, the divergence `aₖ ≠ 0` leaves `0 < aₖ`; hence `aₖ > 0 = wₖ`.

In both cases `aₖ > wₖ` at `k = zpd(a, w)`. When zpd is undefined, the consequence is vacuous.  ∎

Each component of the result is a natural number: for `i < k`, `rᵢ = 0 ∈ ℕ` by NAT-zero; at the divergence point, `rₖ = aₖ − wₖ ∈ ℕ` by NAT-sub, whose precondition `aₖ ≥ wₖ` follows from `aₖ > wₖ` via NAT-order; for `i > k`, `rᵢ` is the zero-padded value of `a`, either `aᵢ ∈ ℕ` or `0 ∈ ℕ` by NAT-zero. In the no-divergence case every component is `0 ∈ ℕ`. The length `L ≥ 1` since T0 gives `#a ≥ 1` and `#w ≥ 1`, and `L` is named by the trichotomy as one of `#a` or `#w`. Hence **`a ⊖ w ∈ T`** by T0.

When `zpd(a, w)` is defined — write `k = zpd(a, w)` — components before `k` are zero by construction, and `rₖ = aₖ − wₖ ≥ 1` by NAT-sub (strict positivity) from `aₖ > wₖ`. The result is not the zero tumbler, whence **`Pos(a ⊖ w)`** (TA-Pos). By ActionPoint, **`actionPoint(a ⊖ w) = zpd(a, w)`**. When `zpd(a, w)` is undefined, the result is the zero tumbler and neither conclusion holds.

*Formal Contract:*
- *Preconditions:* a ∈ T, w ∈ T, a ≥ w (T1). Consequence: when zpd(a, w) is defined, aₖ > wₖ at k = zpd(a, w).
- *Depends:*
  - T0 (CarrierSetDefinition) — carrier membership `a ⊖ w ∈ T` and per-operand length bounds `#a ≥ 1`, `#w ≥ 1`.
  - T1 (LexicographicOrder) — precondition ordering `a ≥ w`; trichotomy derives `w < a`; case (ii) eliminates sub-case (ii-b).
  - T3 (CanonicalRepresentation) — forward direction: `not-padded-equal ⟹ a ≠ w`; reverse direction: length inequality implies tumbler inequality.
  - Divergence — case analysis on the pair `(w, a)`.
  - ZPD — defines `zpd(a, w)`; Relationship-to-Divergence identifies `zpd = divergence` under case (i); case-split and minimality under case (ii).
  - TA-Pos (PositiveTumbler) — defines `Pos` for the conditional postcondition.
  - ActionPoint — supplies `actionPoint(a ⊖ w) = zpd(a, w)`.
  - TumblerAdd (TumblerAdd) — supplies tumbler addition `⊕` for the round-trip relationship `a ⊕ (b ⊖ a) = b` under `divergence(a, b) ≤ #a` and `#a ≤ #b`.
  - NAT-sub (NatPartialSubtraction) — conditional closure `aₖ − wₖ ∈ ℕ` under `aₖ ≥ wₖ`; strict positivity `aₖ − wₖ ≥ 1` under `aₖ > wₖ`.
  - NAT-zero (NatZeroMinimum) — `0 ∈ ℕ` for zero-padding, `rᵢ = 0` components, and the zero-tumbler branch; lower bound `0 ≤ aₖ`.
  - NAT-order (NatStrictTotalOrder) — trichotomy on `(#a, #w)` naming `L`; defining clause `≤ ⟺ < ∨ =` at `(0, aₖ)`; conversion `>` to `≥` at `(aₖ, wₖ)` for NAT-sub.
  - NAT-addcompat (NatAdditionOrderAndSuccessor) — monotonicity of addition with respect to order on ℕ, supporting the round-trip derivation via TumblerAdd.
- *Definition:* NAT-order's trichotomy on `(#a, #w)` selects exactly one of: (α) `#a = #w`, `L = #a`; (β) `#a < #w`, `L = #w`; (γ) `#w < #a`, `L = #a`. a ⊖ w is computed by case analysis on k = zpd(a, w) (ZPD), all component references using zero-padded values (aᵢ = 0 for i > #a, wᵢ = 0 for i > #w); rᵢ = 0 for i < k, rₖ = aₖ − wₖ, rᵢ = aᵢ (zero-padded) for i > k; when zpd(a, w) is undefined, a ⊖ w = [0, …, 0]; #(a ⊖ w) = L.
- *Postconditions:* a ⊖ w ∈ T, #(a ⊖ w) = L (the longer of `#a` and `#w`, named by NAT-order trichotomy per the Definition); when zpd(a, w) is defined: Pos(a ⊖ w) (TA-Pos), actionPoint(a ⊖ w) = zpd(a, w) (ActionPoint).
