## Subspace closure

When arithmetic advances a position within one element subspace, the result must remain in that subspace. We state this as a pair of closure theorems for `⊕` and `⊖` whose preconditions are tight enough to keep every component of the result strictly positive, so that no component collapses to a zero that would either exit the subspace into the zero-padded residue `T \ S` or collapse the whole result to the zero tumbler `Z`. The case-analytic residues — length overflow (TA7a.1), interior divergence (TA7a.2), and self-subtraction to `Z` (TA7a.3) — are relocated to sub-claims whose preconditions are the complementary fragments of the theorem's precondition lattice.

**TA7a (SubspaceClosure).** A position in a subspace with identifier `N` and ordinal `o = [o₁, ..., oₘ]` (where `m ≥ 1`) is represented as the tumbler `o` for arithmetic purposes, with `N` held as structural context. Define **S** = {o ∈ T : #o ≥ 1 ∧ (A i : 1 ≤ i ≤ #o : oᵢ > 0)}. An element-local displacement is a positive tumbler `w` with action point `k = actionPoint(w)` satisfying `1 ≤ k ≤ m`. Then:

  `(A o ∈ S, w ∈ T : Pos(w) ∧ k ≤ #o ∧ (A i : k ≤ i ≤ #w : wᵢ > 0) ⟹ o ⊕ w ∈ S)`

  `(A o ∈ S, w ∈ T : Pos(w) ∧ o ≥ w ∧ k ≤ #o ∧ #w ≤ #o ∧ o₁ > w₁ ⟹ o ⊖ w ∈ S)`

The tail-positivity precondition on `w` in the `⊕`-conjunct keeps the trailing components of the result — which TumblerAdd copies verbatim from `w` at positions `i > k` — strictly positive; dropping it admits a displacement whose interior zero survives into the result and exits `S`. In the `⊖`-conjunct, `k ≤ #o` enforces the element-local restriction on `w` stated above (parallel to the `⊕`-conjunct's bound); `#w ≤ #o` forecloses the length-overflow escape characterised by TA7a.1; and `o₁ > w₁` forces divergence at position 1, keeping `r₁ > 0` (against the leading-zero escape characterised by TA7a.2) and the tail `rᵢ = oᵢ > 0` drawn from `o ∈ S` (against the collapse to `Z` characterised by TA7a.3). When `k ≥ 2`, ActionPoint gives `w₁ = 0`, so `o ∈ S` supplies `o₁ > 0 = w₁` automatically; the `o₁ > w₁` precondition only imposes a genuine restriction at `k = 1`, where it rules out the `o₁ = w₁` cases that TA7a.2 and TA7a.3 address.

The subspace identifier is not an operand; it determines which positions are subject to the shift but never enters the arithmetic.

*Proof.* Let `o = [o₁, ..., oₘ]` with `o ∈ S`, and let `w` be positive with action point `k`.

**Conjunct 1** (`⊕`-closure in `S`). From `o, w ∈ T`, `Pos(w)`, and `k ≤ #o`, TA0 gives `r := o ⊕ w ∈ T` with `#r = #w`. By TumblerAdd's three-region componentwise formula, `rᵢ = oᵢ` for `1 ≤ i < k`; `rₖ = oₖ + wₖ`; `rᵢ = wᵢ` for `k < i ≤ #w`. We show each region is positive.

*Pre-action* (`1 ≤ i < k`): `i < k ≤ #o = m` places `i` in the range of `S`'s universal clause on `o`, giving `rᵢ = oᵢ > 0`.

*Action point* (`i = k`): `rₖ = oₖ + wₖ > 0` by NAT-addcompat's left order-compatibility (at `m := oₖ, n := wₖ, p := 1`) lifting `wₖ ≥ 1` — supplied by ActionPoint's minimum-value clause — to `oₖ + wₖ ≥ oₖ + 1`; NAT-addcompat's strict successor gives `oₖ + 1 > oₖ`; NAT-order's `≤` defining clause together with transitivity of `<` compose these into `oₖ + wₖ > oₖ`; chaining with `oₖ > 0` (from `o ∈ S`) via transitivity yields `oₖ + wₖ > 0`.

*Tail* (`k < i ≤ #w`): `rᵢ = wᵢ > 0` by the tail-positivity precondition `(A i : k ≤ i ≤ #w : wᵢ > 0)` restricted to its upper sub-range.

Every index in `[1, #r] = [1, #w]` carries a positive component; with `#r = #w ≥ 1` from T0, we conclude `r ∈ S`. For single-component ordinals, `[x] ⊕ [n] = [x + n] ∈ S`.

Example: `[1, 3, 2] ⊕ [0, 2, 7] = [1, 5, 7]` (action point `k = 2`, tail positive).

**Conjunct 2** (`⊖`-closure in `S`). From `o, w ∈ T` and `o ≥ w`, TA2 gives `r := o ⊖ w ∈ T`. The length precondition `#w ≤ #o` selects — via NAT-order's trichotomy on `(#o, #w)` — either sub-case (α) `#o = #w` with `L = #o` or sub-case (γ) `#w < #o` with `L = #o`; in either `L = #o = m`. Since `o₁ > w₁` gives `o₁ ≠ w₁`, the zero-padded sequences disagree at position 1, and by ZPD's minimality `zpd(o, w) = 1`. TumblerSub's componentwise formula then gives `r₁ = o₁ − w₁`, `rᵢ = oᵢ` (zero-padded) for `1 < i ≤ L = m`, and `#r = L = m`.

*Divergence point* (`i = 1`): NAT-sub's strict-positivity clause `(A m, n ∈ ℕ : m > n : m − n ≥ 1)` at `(o₁, w₁)` lifts `o₁ > w₁` directly to `r₁ = o₁ − w₁ ≥ 1 > 0`.

*Tail* (`1 < i ≤ m`): the position lies within `1 < i ≤ m = #o`, so no zero-padding applies and `rᵢ = oᵢ`; `oᵢ > 0` by `o ∈ S`.

Every index in `[1, #r] = [1, m]` carries a positive component; with `#r = m ≥ 1`, we conclude `r ∈ S`. For single-component ordinals (`m = 1`, `#w = 1`), `[x] ⊖ [n] = [x − n] ∈ S` when `x > n`. ∎

The restriction to element-local displacements is necessary: an unrestricted displacement whose action point falls at the subspace-identifier position could produce an address in a different subspace.

*Formal Contract:*
- *Preconditions:* For `⊕`: `o ∈ S`, `w ∈ T`, `Pos(w)`, `actionPoint(w) ≤ #o`, `(A i : actionPoint(w) ≤ i ≤ #w : wᵢ > 0)`. For `⊖`: `o ∈ S`, `w ∈ T`, `Pos(w)`, `o ≥ w`, `actionPoint(w) ≤ #o`, `#w ≤ #o`, `o₁ > w₁`.
- *Depends:*
  - T0 (CarrierSetDefinition) — supplies carrier `T`, length operator `#`, ℕ-typed components, and the length-minimum `#t ≥ 1` underlying `#r ≥ 1` in both conjuncts; grounds the **S** definition.
  - T1 (LexicographicOrder) — defines the ordering relation `≥` used in the `⊖`-precondition and consumed by TA2.
  - TA-Pos (PositiveTumbler) — the precondition `Pos(w)` licenses action-point existence; supplies the **Z** definition referenced in the narrative and in the sub-claim TA7a.3.
  - ActionPoint (ActionPoint) — defines `k = actionPoint(w)` as the least non-zero position of `w` and supplies the minimum-value clause `w_k ≥ 1` used in the Conjunct 1 action-point positivity chain; the prefix-zero characterisation justifies the narrative remark that `k ≥ 2 ⟹ w₁ = 0`.
  - TumblerAdd (TumblerAdd) — three-region componentwise construction of `r = o ⊕ w` used in Conjunct 1 (pre-action copy from `o`, action-point sum `oₖ + wₖ`, tail copy from `w`).
  - TumblerSub (TumblerSub) — zero-padding under NAT-order trichotomy, ZPD-based divergence dispatch, and componentwise formula used in Conjunct 2; the divergence-at-1 branch is the one selected by `o₁ > w₁`.
  - ZPD (ZeroPaddedDivergence) — minimality clause `zpd(a, w) = min {k : 1 ≤ k ≤ L ∧ âₖ ≠ ŵₖ}` fixes `zpd(o, w) = 1` in Conjunct 2 from the position-1 disagreement `o₁ ≠ w₁` (itself supplied by `o₁ > w₁`); this divergence index is the dispatch key consumed by TumblerSub's componentwise formula at the divergence point.
  - TA0 (WellDefinedAddition) — delivers `o ⊕ w ∈ T` and `#(o ⊕ w) = #w` from the `⊕`-preconditions; the S-strengthening in Conjunct 1 rests on this T-closure.
  - TA2 (WellDefinedSubtraction) — delivers `o ⊖ w ∈ T` from the `⊖`-preconditions; the S-strengthening in Conjunct 2 rests on this T-closure.
  - NAT-addcompat (NatAdditionOrderAndSuccessor) — left order-compatibility and strict successor jointly establishing `oₖ + wₖ > oₖ` at the action point of `⊕`.
  - NAT-order (NatStrictTotalOrder) — trichotomy on `(#o, #w)` names `L` in the TumblerSub dispatch; the `≤` defining clause and transitivity of `<` compose the strict-through-addition chain in Conjunct 1.
  - NAT-sub (NatPartialSubtraction) — strict-positivity clause `m > n ⟹ m − n ≥ 1` discharges `r₁ > 0` at the divergence point of Conjunct 2.
  - NAT-closure (NatArithmeticClosureAndIdentity) — supplies `1 ∈ ℕ` for the numerals in quantifier bounds and in `wₖ ≥ 1`; additive identity required in scope for the consumed contracts of TumblerAdd, TumblerSub, TA-Pos, and ActionPoint.
  - NAT-zero (NatZeroMinimum) — supplies `0 ∈ ℕ` for the literal `0` in the **S** positivity clause `oᵢ > 0` and for the zero-padding semantics of TumblerSub consumed in Conjunct 2.
- *Forward References:*
  - TA7a.1 (SubspaceLengthResidue) — handles the complementary length-overflow residue case (`#w > #o`) relocated from TA7a's precondition lattice
  - TA7a.2 (SubspaceDivergenceResidue) — handles the complementary leading-zero residue case (`o₁ = w₁`) relocated from TA7a's precondition lattice
  - TA7a.3 (SubspaceZeroResidue) — handles the complementary self-subtraction residue case (collapse to Z) relocated from TA7a's precondition lattice
- *Postconditions:* `o ⊕ w ∈ S` with `#(o ⊕ w) = #w`; `o ⊖ w ∈ S` with `#(o ⊖ w) = #o`.
- *Frame:* The subspace identifier `N` is not an operand and is never modified.
- *Definition:* **S** = {o ∈ T : #o ≥ 1 ∧ (A i : 1 ≤ i ≤ #o : oᵢ > 0)}.
