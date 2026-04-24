**TA7a.2 (SubspaceDivergenceResidue).** When the action point is at position 1 and the leading components coincide with a strict disagreement later, the subspace-closure guarantee of TA7a fails and the residue acquires a leading zero, placing it in `T \ S`.

  `(A o ∈ S, w ∈ T : Pos(w) ∧ o ≥ w ∧ #w ≤ #o ∧ actionPoint(w) = 1 ∧ o₁ = w₁ ∧ o ≠ w ⟹ o ⊖ w ∈ T \ S)`

*Proof.* Let `o ∈ S`, `w ∈ T` with `Pos(w)`, `o ≥ w`, `#w ≤ #o`, `k := actionPoint(w) = 1`, `o₁ = w₁`, and `o ≠ w`. By TA2, `r := o ⊖ w ∈ T`. NAT-order's trichotomy on `(#o, #w)` with `#w ≤ #o` selects sub-case (α) `#o = #w` with `L = #o` or sub-case (γ) `#w < #o` with `L = #o`; in either `L = #o`.

Since `o ≠ w`, the zero-padded sequences disagree at some position, so `zpd(o, w)` is defined; write `d = zpd(o, w)`. The disagreement cannot be at position 1 because `o₁ = w₁`; by ZPD's minimality `d > 1`. By TumblerSub's componentwise formula, `rᵢ = 0` for `1 ≤ i < d`. In particular `r₁ = 0`.

The index `1` lies in `[1, #r]` (since `#r = L = #o ≥ 1` by T0), and `r₁ = 0` violates the universal positivity clause of **S**; hence `r ∉ S`. Combined with `r ∈ T` from TA2, `r ∈ T \ S`. ∎

Example: `[5, 3] ⊖ [5, 1] = [0, 2]` — `k = 1`, `o₁ = w₁ = 5`, divergence at `d = 2` (`3 ≠ 1`), giving `r₁ = 0` (pre-divergence zero), `r₂ = 3 − 1 = 2` (divergence point). `r = [0, 2] ∈ T \ S`, consistent with the predicted residue.

*Formal Contract:*
- *Preconditions:* `o ∈ S`, `w ∈ T`, `Pos(w)`, `o ≥ w`, `#w ≤ #o`, `actionPoint(w) = 1`, `o₁ = w₁`, `o ≠ w`.
- *Depends:*
  - TA7a (SubspaceClosure) — parent claim defining **S** and establishing the complementary in-S branch whose precondition `o₁ > w₁` this sub-claim negates under `o ≠ w`.
  - T0 (CarrierSetDefinition) — carrier `T`, length `#`, `#r ≥ 1`.
  - TA-Pos (PositiveTumbler) — `Pos(w)` precondition; **S** definition whose universal positivity clause is violated at index 1.
  - ActionPoint (ActionPoint) — defines `k = actionPoint(w)`; the precondition `k = 1` is consumed only to characterise the scenario, not inside the proof (the divergence location `d > 1` follows from `o₁ = w₁ ∧ o ≠ w` without invoking `k`).
  - TA2 (WellDefinedSubtraction) — delivers `o ⊖ w ∈ T`.
  - TumblerSub (TumblerSub) — zero-padding under NAT-order trichotomy, ZPD-based dispatch, and the pre-divergence-zero clause `rᵢ = 0` for `i < d` which places `r₁ = 0`.
  - ZPD (ZeroPaddedDivergence) — minimality of `zpd(o, w)` places `d > 1` given agreement at position 1 and disagreement from `o ≠ w`.
  - NAT-order (NatStrictTotalOrder) — trichotomy on `(#o, #w)` with `#w ≤ #o` places `L = #o`.
  - NAT-zero (NatZeroMinimum) — supplies `0 ∈ ℕ` for `r₁ = 0`.
- *Postcondition:* `o ⊖ w ∈ T \ S`, with `r₁ = 0` witnessing the escape from **S**.
