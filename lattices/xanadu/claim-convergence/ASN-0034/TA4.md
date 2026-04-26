Tumbler addition is not, in general, invertible by `⊖`. TumblerAdd builds `a ⊕ w` in three regions keyed on the action point `k` of `w`: positions `i < k` retain `aᵢ`, position `k` accumulates `aₖ + wₖ`, and positions `i > k` are supplied by `w`. Whatever content `a` carries past position `k` is overwritten by `w`'s tail and cannot be recovered. Even with `#a = k` ruling out that loss, the recovery `(a ⊕ w) ⊖ w = a` further requires that `a`'s prefix vanish (`aᵢ = 0` for `1 ≤ i < k`), so that the first divergence between `a ⊕ w` and `w` falls at position `k` rather than at some earlier nonzero entry of `a` that would mislead TumblerSub's divergence-keyed dispatch. Together with `Pos(w)` (so the action point exists, by TA-Pos) and `#w = k`, these are the structural conditions under which we can establish a partial inverse.

**TA4 (PartialInverse).** `(A a, w ∈ T : Pos(w) ∧ k = #a ∧ #w = k ∧ (A i : 1 ≤ i < k : aᵢ = 0) : (a ⊕ w) ⊖ w = a)`, where `k` is the action point of `w`.

*Proof.* Let `k` denote the action point of `w` (ActionPoint): the least position `i` with `wᵢ > 0`, so `wᵢ = 0` for `i < k` and `wₖ > 0`. `Pos(w)` guarantees `k` exists (TA-Pos).

**Step 1: structure of `r = a ⊕ w`.** By TumblerAdd (`k = #a` discharges TA0's precondition `k ≤ #a`), `r` is built in three regions: `rᵢ = aᵢ` for `i < k`; `rₖ = aₖ + wₖ`; `rᵢ = wᵢ` for `i > k`. The precondition `(A i : 1 ≤ i < k : aᵢ = 0)` gives `rᵢ = 0` for `i < k`. By TA0's result-length identity `#r = #w` and the precondition `#w = k`, `#r = k`, so positions `i > k` are empty. Hence `r = [0, ..., 0, aₖ + wₖ]` of length `k`.

**Step 2: computing `s = r ⊖ w`.** TumblerSub requires `r ≥ w` (T1); TumblerAdd's dominance postcondition discharges this. TumblerSub is keyed on `zpd(r, w)` (ZPD): the three-region rule (`sᵢ = 0` for `i < k`, `sₖ = rₖ − wₖ`, `sᵢ = rᵢ` for `i > k`) when `zpd` is defined, and the zero tumbler of length `L` when `zpd` is undefined. NAT-order's trichotomy on `(#r, #w)` names `L = max(#r, #w)`; with `#r = #w = k`, `L = k`. At every position `i < k`, `rᵢ = 0` and `wᵢ = 0`, so padded projections agree before position `k`.

Since `aₖ ∈ ℕ` (T0 component typing at `k = #a`), NAT-zero supplies `0 ≤ aₖ`, which NAT-order's defining clause `m ≤ n ⟺ m < n ∨ m = n` at `m = 0, n = aₖ` unfolds to `aₖ > 0 ∨ aₖ = 0`.

*Case 1: `aₖ > 0`.* NAT-addcompat's right order-compatibility (`p ≤ n ⟹ p + m ≤ n + m`, at `p = 0, n = aₖ, m = wₖ`) lifts `0 ≤ aₖ` to `0 + wₖ ≤ aₖ + wₖ`; NAT-closure's additive identity rewrites `0 + wₖ = wₖ`, giving `wₖ ≤ aₖ + wₖ`. NAT-cancel's symmetric summand absorption `n + m = m ⟹ n = 0` rules out the equality disjunct, which would force `aₖ = 0` and contradict `aₖ > 0` by NAT-order's irreflexivity. NAT-order's defining clause at `m = wₖ, n = aₖ + wₖ` then yields `aₖ + wₖ > wₖ`, i.e., `rₖ > wₖ`. Combined with pre-divergence agreement at `i < k`, ZPD's minimality identifies `k = zpd(r, w)`. TumblerSub produces `sᵢ = 0` for `i < k`, `sₖ = (aₖ + wₖ) − wₖ = aₖ` (NAT-sub right-telescoping), and nothing beyond (since `#r = k`). Hence `s = [0, ..., 0, aₖ]` of length `k`, which by T3 and the precondition `aᵢ = 0` for `i < k` equals `a`.

*Case 2: `aₖ = 0`.* Then `rₖ = aₖ + wₖ = 0 + wₖ = wₖ` (NAT-closure). Combined with `rᵢ = 0 = wᵢ` for `i < k` and `#r = k = #w`, T3 gives `r = w`. The padded projections agree throughout `{1, ..., k}`, so `zpd(r, w)` is undefined (ZPD case-split) and TumblerSub's no-divergence branch yields the zero tumbler of length `k`. By the precondition, this is `a`.

In both cases, `(a ⊕ w) ⊖ w = a`. ∎

*Formal Contract:*
- *Preconditions:* `a ∈ T`, `w ∈ T`, `Pos(w)`, `k = #a`, `#w = k`, `(A i : 1 ≤ i < k : aᵢ = 0)`, where `k` is the action point of `w`
- *Depends:*
  - TA-Pos (PositiveTumbler) — guarantees action point exists from `Pos(w)`
  - ActionPoint (ActionPoint) — defines `k` as least position with `wᵢ > 0`; `wᵢ = 0` for `i < k`
  - TumblerAdd (TumblerAdd) — three-region construction of `a ⊕ w`; dominance postcondition `r ≥ w`
  - TA0 (WellDefinedAddition) — applicability precondition `k ≤ #a`; result-length identity `#r = #w`
  - TumblerSub (TumblerSub) — three-region construction of `r ⊖ w`; no-divergence zero-tumbler branch
  - T0 (CarrierSetDefinition) — carrier `T`, length `#`, component typing `aᵢ ∈ ℕ`
  - T1 (LexicographicOrder) — `≥` comparison for TumblerSub's precondition
  - T3 (CanonicalRepresentation) — componentwise and length equality imply tumbler equality
  - ZPD (ZPD) — case-split (undefined when padded projections agree); minimality at first disagreement
  - NAT-closure (NatArithmeticClosureAndIdentity) — additive identity `0 + n = n`
  - NAT-addcompat (NatAdditionOrderAndSuccessor) — right order-compatibility `p ≤ n ⟹ p + m ≤ n + m`
  - NAT-cancel (NatAdditionCancellation) — symmetric summand absorption `n + m = m ⟹ n = 0`
  - NAT-zero (NatZeroMinimum) — lower bound `0 ≤ n` for `n ∈ ℕ`
  - NAT-order (NatStrictTotalOrder) — trichotomy on length pair; defining clause `≤ ⟺ < ∨ =`; irreflexivity
  - NAT-sub (NatPartialSubtraction) — right-telescoping `(m + n) − n = m`
- *Postconditions:* `(a ⊕ w) ⊖ w = a`
