**TA7a.1 (SubspaceLengthResidue).** When the subtrahend is longer than the minuend, the subspace-closure guarantee of TA7a fails and the residue lies in `T \ S` with trailing zeros beyond the minuend's length.

  `(A o ∈ S, w ∈ T : Pos(w) ∧ o ≥ w ∧ #w > #o ⟹ o ⊖ w ∈ T \ S)`

*Proof.* Let `o ∈ S` and `w ∈ T` with `Pos(w)`, `o ≥ w`, and `#w > #o`. By TA2, `r := o ⊖ w ∈ T`. NAT-order's trichotomy on `(#o, #w)` selects sub-case (β) of TumblerSub: `L = #w > #o`, and the minuend is zero-padded so that `oᵢ = 0` for `#o < i ≤ #w`.

We first show that the zero-padded sequences disagree. If they agreed everywhere, then in particular `oᵢ = wᵢ` for `1 ≤ i ≤ #o`, and for `#o < i ≤ #w`, `wᵢ = oᵢ (padded) = 0`. Then by T3 the pair `(o, w)` satisfies `o ≠ w` via the length clause `#o < #w`, and T1's prefix-relationship case (ii) applied to the agreement `oᵢ = wᵢ` for `i ≤ #o` — `o` a proper prefix of `w` — yields `o < w`, contradicting `o ≥ w`. Hence the zero-padded sequences disagree, `zpd(o, w)` is defined; write `d = zpd(o, w)`.

Next we locate `d` within `o`'s positions. Suppose `d > #o`. Then by ZPD's minimality, the padded sequences agree for `1 ≤ i ≤ #o`, i.e., `oᵢ = wᵢ` there; for `#o < i < d`, padded agreement means `0 = wᵢ`, i.e., `wᵢ = 0`; at `i = d`, disagreement means `0 = o_d (padded) ≠ w_d`, so `w_d ≠ 0`. But then `o` is a proper prefix of `w` — `oᵢ = wᵢ` on `[1, #o]` and `#o < #w` — so T1's prefix case (ii) again yields `o < w`, contradicting `o ≥ w`. Therefore `d ≤ #o`.

By TumblerSub's componentwise formula: `rᵢ = 0` for `i < d`; `r_d = o_d − w_d`; `rᵢ = oᵢ` (zero-padded) for `d < i ≤ L = #w`. At position `#w` (which satisfies `d < #w` since `d ≤ #o < #w`), `r_{#w} = o_{#w}` (padded). Since `#w > #o`, the padding gives `o_{#w} = 0`, so `r_{#w} = 0`. The index `#w = #r` lies in `[1, #r]`, and its component is `0`, violating the universal positivity clause of **S**; hence `r ∉ S`. Combined with `r ∈ T` from TA2, `r ∈ T \ S`. ∎

Example: `[5, 3] ⊖ [5, 3, 4]` — padding `o` to `[5, 3, 0]`, divergence at position 3 (`0 ≠ 4`) is excluded by `o ≥ w`; take instead `[5, 4] ⊖ [5, 3, 4]`, padding to `[5, 4, 0]`, divergence at position 2 (`4 > 3`), giving `r = [0, 1, 0]` (since `r_2 = 4 − 3 = 1`, `r_3 = o_3 (padded) = 0`). `#r = 3`, `r_3 = 0`, so `r ∈ T \ S`.

*Formal Contract:*
- *Preconditions:* `o ∈ S`, `w ∈ T`, `Pos(w)`, `o ≥ w`, `#w > #o`.
- *Depends:*
  - TA7a (SubspaceClosure) — parent claim defining **S** and establishing the complementary in-S branch whose precondition `#w ≤ #o` this sub-claim negates.
  - T0 (CarrierSetDefinition) — carrier `T`, length `#`, ℕ-typed components.
  - T1 (LexicographicOrder) — prefix-relationship case (ii) rules out `d > #o` and also the padded-sequences-agree-everywhere case, both by deriving `o < w` against `o ≥ w`.
  - T3 (CanonicalRepresentation) — length clause `#o ≠ #w ⟹ o ≠ w` supports the disagreement argument.
  - TA-Pos (PositiveTumbler) — `Pos(w)` precondition; **S** complement referenced in the postcondition.
  - TA2 (WellDefinedSubtraction) — delivers `o ⊖ w ∈ T`.
  - TumblerSub (TumblerSub) — zero-padding under NAT-order trichotomy, ZPD-based dispatch, and componentwise formula — in particular `rᵢ = oᵢ` (zero-padded) for `i > d` which places `r_{#w} = 0`.
  - ZPD (ZeroPaddedDivergence) — minimality of `zpd(o, w)`.
  - NAT-order (NatStrictTotalOrder) — trichotomy on `(#o, #w)` selects sub-case (β) with `L = #w`.
  - NAT-zero (NatZeroMinimum) — supplies `0 ∈ ℕ` for the padding positions `#o < i ≤ #w`.
- *Postcondition:* `o ⊖ w ∈ T \ S`, with `r_{#w} = 0` witnessing the escape from **S**.
