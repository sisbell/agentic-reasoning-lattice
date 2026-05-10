**TA7a.2 (SubspaceDivergenceResidue).** When the action point is at position 1 and the leading components coincide with a strict disagreement later, the subspace-closure guarantee of TA7a fails and the residue acquires a leading zero, placing it in `T \ S`.

  `(A o ∈ S, w ∈ T : Pos(w) ∧ o ≥ w ∧ #w ≤ #o ∧ actionPoint(w) = 1 ∧ o₁ = w₁ ∧ o ≠ w ⟹ o ⊖ w ∈ T \ S)`

*Proof.* Let `o ∈ S`, `w ∈ T` with `Pos(w)`, `o ≥ w`, `#w ≤ #o`, `k := actionPoint(w) = 1`, `o₁ = w₁`, and `o ≠ w`. By TA2, `r := o ⊖ w ∈ T`. NAT-order's trichotomy on `(#o, #w)` with `#w ≤ #o` selects sub-case (α) `#o = #w` with `L = #o` or sub-case (γ) `#w < #o` with `L = #o`; in either `L = #o`.

We establish that `zpd(o, w)` is defined by case-splitting on the trichotomy outcome. The bare disagreement `o ≠ w` does not suffice — ZPD's partiality clause is explicit that `o ≠ w` is compatible with `zpd(o, w)` undefined (the documented counterexample `[3, 0]` versus `[3]`). The argument must consume the sub-case structure that the trichotomy already supplied.

*Sub-case (α)* (`#o = #w`, `L = #o`). When the lengths agree there is no padding to traverse: ZPD's defining clauses give `ôᵢ = oᵢ` for `1 ≤ i ≤ #o` and `ŵᵢ = wᵢ` for `1 ≤ i ≤ #w = #o`, so on `[1, L]` the padded projections coincide with the native sequences. Suppose for contradiction that `zpd(o, w)` is undefined; ZPD's partiality clause then forces `(A i : 1 ≤ i ≤ L : ôᵢ = ŵᵢ)`, i.e. `(A i : 1 ≤ i ≤ #o : oᵢ = wᵢ)`. Conjoined with `#o = #w`, T3's forward direction at `(o, w)` yields `o = w`, contradicting the precondition `o ≠ w`. Hence `zpd(o, w)` is defined.

*Sub-case (γ)* (`#w < #o`, `L = #o`). Here the strict inequality leaves at least one position past `#w` within `[1, L]`; pick `i := #o`, which satisfies `#w < i ≤ L = #o`. ZPD's padding clause for `ŵ` gives `ŵᵢ = 0` (the position is past `#w`), and ZPD's native clause for `ô` gives `ôᵢ = oᵢ` (the position is within `#o`). Since `o ∈ S`, the universal positivity clause from **S**'s definition delivers `oᵢ > 0`, so `ôᵢ = oᵢ > 0 = ŵᵢ` and `ôᵢ ≠ ŵᵢ`. The disagreement at this index forecloses ZPD's universal-agreement antecedent, so `zpd(o, w)` is defined.

In either sub-case `zpd(o, w)` is defined; write `d = zpd(o, w)`. The padded projections agree at position 1 — `ô₁ = o₁ = w₁ = ŵ₁` — so the disagreement cannot be at position 1, and by ZPD's minimality `d > 1`. By TumblerSub's componentwise formula, `rᵢ = 0` for `1 ≤ i < d`. In particular `r₁ = 0`.

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
  - T3 (CanonicalRepresentation) — forward direction `(#a = #b ∧ (A i : 1 ≤ i ≤ #a : aᵢ = bᵢ)) ⟹ a = b` instantiated at `(o, w)` in sub-case (α): the contradiction `o = w` against the precondition `o ≠ w` is what forces `zpd(o, w)` defined when the lengths agree.
  - TumblerSub (TumblerSub) — zero-padding under NAT-order trichotomy, ZPD-based dispatch, and the pre-divergence-zero clause `rᵢ = 0` for `i < d` which places `r₁ = 0`.
  - ZPD (ZeroPaddedDivergence) — partiality clause used both ways: in sub-case (α), the universal-agreement antecedent contradicts T3 plus `o ≠ w`; in sub-case (γ), the padding clause `ŵᵢ = 0` for `#w < i ≤ L` against `ôᵢ = oᵢ > 0` (from `o ∈ S`) breaks universal agreement at `i = #o`. Together these establish `zpd(o, w)` defined; minimality then places `d > 1` given agreement at position 1.
  - NAT-order (NatStrictTotalOrder) — trichotomy on `(#o, #w)` with `#w ≤ #o` places `L = #o`.
  - NAT-zero (NatZeroMinimum) — supplies `0 ∈ ℕ` for `r₁ = 0`.
- *Postcondition:* `o ⊖ w ∈ T \ S`, with `r₁ = 0` witnessing the escape from **S**.
