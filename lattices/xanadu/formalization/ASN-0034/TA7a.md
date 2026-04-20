## Subspace closure

When arithmetic advances a position within one element subspace, the result must remain in that subspace. Text positions must not cross into link space, and vice versa.

**TA7a (SubspaceClosure).** A position in a subspace with identifier `N` and ordinal `o = [o₁, ..., oₘ]` (where `m ≥ 1`) is represented as the tumbler `o` for arithmetic purposes, with `N` held as structural context. Define **S** = {o ∈ T : #o ≥ 1 ∧ (A i : 1 ≤ i ≤ #o : oᵢ > 0)}. An element-local displacement is a positive tumbler `w` with action point `k` satisfying `1 ≤ k ≤ m`. Then:

  `(A o ∈ S, Pos(w) : k ≤ #o ⟹ o ⊕ w ∈ T)`

  `(A o ∈ S, Pos(w) : o ≥ w ⟹ o ⊖ w ∈ T)`

The subspace identifier is not an operand; it determines which positions are subject to the shift but never enters the arithmetic.

*Proof.* Let `o = [o₁, ..., oₘ]` with `o ∈ S`, and let `w` be positive with action point `k = min({i : 1 ≤ i ≤ #w ∧ wᵢ ≠ 0})`.

**Conjunct 1** (`⊕`-closure in T). From `o ∈ T`, `w ∈ T`, `Pos(w)`, and `k ≤ #o = m`, TA0 gives `o ⊕ w ∈ T` with `#(o ⊕ w) = #w`.

For S-membership: by TumblerAdd, `r = o ⊕ w` has `rᵢ = oᵢ > 0` for `1 ≤ i < k`; `rₖ = oₖ + wₖ`; `rᵢ = wᵢ` for `k < i ≤ #w`. Strict positivity `rₖ > 0` follows from NAT-addcompat's left order-compatibility (at `m = oₖ, n = wₖ, p = 1`) lifting `wₖ ≥ 1` to `oₖ + wₖ ≥ oₖ + 1`, NAT-addcompat's strict successor `oₖ + 1 > oₖ`, and NAT-order's `≤` defining clause plus transitivity of `<` composing these into `oₖ + wₖ > oₖ`, then chained with `oₖ > 0` via transitivity to give `oₖ + wₖ > 0`. Components before and at `k` are positive; the result is in S when every tail `wᵢ` (for `i > k`) is also positive. For single-component ordinals, `[x] ⊕ [n] = [x + n] ∈ S`.

Example: `[1, 3, 2] ⊕ [0, 2, 7] = [1, 5, 7]` (action point `k = 2`).

**Conjunct 2** (`⊖`-closure in T). From `o ∈ T`, `w ∈ T`, `o ≥ w`, TA2 gives `o ⊖ w ∈ T`. S-membership by action point and divergence, using TumblerSub: zero-pad to length `L` (named by NAT-order's trichotomy on `(#o, #w)`: sub-case (α) `#o = #w`, `L = #o`; (β) `#o < #w`, `L = #w`; (γ) `#w < #o`, `L = #o`); find divergence `d`; set `rᵢ = 0` for `i < d`, `r_d = o_d - w_d`, `rᵢ = oᵢ` for `i > d`.

*Preliminary: `#w > m`.* The length pair lies in sub-case (β), `L = #w > m`. The zero-padded minuend has zeros at positions `m + 1` through `#w`, so the result inherits trailing zeros and lies in T \ S. Cases below assume `#w ≤ m`.

*Case `k ≥ 2`:* `w₁ = 0` and `o₁ > 0`, so `d = 1`. By NAT-sub's left-inverse characterisation at `m = o₁, n = 0` (precondition `o₁ ≥ 0` from NAT-zero), `0 + (o₁ − 0) = o₁`; NAT-closure's left identity rewrites to `o₁ − 0 = o₁`. So `r₁ = o₁ > 0` and `rᵢ = oᵢ > 0` for `1 < i ≤ m`. When `#w ≤ m`, the result equals `o` — a no-op, in S.

*Case `k = 1`, divergence `d = 1`:* `w₁ > 0`, `o₁ ≠ w₁`, and `o ≥ w` forces `o₁ > w₁` (T1). TumblerSub gives `r₁ = o₁ − w₁ > 0` by NAT-sub strict positivity; `rᵢ = oᵢ > 0` for `1 < i ≤ m`. When `#w ≤ m`, the result is in S.

*Case `k = 1`, divergence `d > 1`:* `w₁ > 0`, `o₁ = w₁`, divergence at `d > 1`. TumblerSub zeros positions `1 ≤ i < d`, so `r₁ = 0` and the result is not in S. Counterexample: `[5, 3] ⊖ [5, 1] = [0, 2] ∈ T`, `∉ S ∪ Z`.

*Case `k = 1`, no divergence:* `w₁ > 0` and zero-padded sequences agree everywhere. Sub-case (γ) is excluded (`o ∈ S` forces divergence at `#w + 1` against the padded zeros of `w`); so `#o = #w = m`, `L = m`, and `o = w`. TumblerSub yields `[0, ..., 0]` of length `m`; `Zero(o ⊖ w)` by TA-Pos's defining clause, so `o ⊖ w ∈ Z`. Example: `[1, 2] ⊖ [1, 2] = [0, 0] ∈ Z`.

For single-component ordinals, the `d > 1` case cannot arise, and `⊖` gives closure in S ∪ Z: `[x] ⊖ [n] = [x − n] ∈ S` when `x > n`, or `[0] ∈ Z` when `x = n` (a sentinel, TA6).

In every case, the result lies in T. TA7a holds. ∎

The restriction to element-local displacements is necessary: an unrestricted displacement whose action point falls at the subspace-identifier position could produce an address in a different subspace.

*Formal Contract:*
- *Preconditions:* For `⊕`: `o ∈ S`, `w ∈ T`, `Pos(w)`, `actionPoint(w) ≤ #o`. For `⊖`: `o ∈ S`, `w ∈ T`, `Pos(w)`, `o ≥ w`.
- *Depends:*
  - T0 (CarrierSetDefinition) — supplies positivity from ℕ for the **S** definition.
  - T4 (HierarchicalParsing) — anchors the element-field shape underlying **S**.
  - T1 (LexicographicOrder) — converts `o ≥ w` and `o₁ ≠ w₁` to `o₁ > w₁` at divergence.
  - TA-Pos (PositiveTumbler) — licenses action-point existence via `Pos(w)`; defines **Z** = {t ∈ T : Zero(t)} and the `Zero` predicate consumed in the no-divergence branch.
  - ActionPoint (ActionPoint) — defines `k` as least non-zero position; supplies `wₖ ≥ 1` and prefix zeros.
  - TumblerAdd (TumblerAdd) — three-region construction of `r = o ⊕ w`.
  - TumblerSub (TumblerSub) — zero-pad, divergence, and no-divergence branches used throughout Conjunct 2.
  - NAT-addcompat (NatAdditionOrderAndSuccessor) — left order-compatibility and strict successor for the component-level `rₖ > 0` chain.
  - NAT-order (NatStrictTotalOrder) — trichotomy names `L` in TumblerSub dispatch; `≤` defining clause and transitivity of `<` compose the strict-through-addition chain.
  - TA0 (WellDefinedAddition) — T-closure of `⊕`.
  - TA2 (WellDefinedSubtraction) — T-closure of `⊖`.
  - TA6 (ZeroTumblers) — interprets `[0]` as sentinel.
  - NAT-sub (NatPartialSubtraction) — left-inverse for `o₁ − 0 = o₁`; strict positivity for `o₁ − w₁ > 0`; conditional closure for divergence-point subtraction.
  - NAT-closure (NatArithmeticClosureAndIdentity) — left additive identity rewriting `0 + (o₁ − 0)` to `o₁ − 0`.
  - NAT-zero (NatZeroMinimum) — `o₁ ≥ 0` precondition for NAT-sub's left-inverse at `n = 0`.
- *Postconditions:* `o ⊕ w ∈ T`, `#(o ⊕ w) = #w`. `o ⊖ w ∈ T`. For `⊕`: result is in S when all tail components of `w` after `k` are positive. For `⊖` with `actionPoint(w) ≥ 2` and `#w ≤ #o`: result is `o` (no-op), in S. For `⊖` with `actionPoint(w) = 1`, `d = 1`, `#w ≤ #o`: result is in S. For `⊖` with `actionPoint(w) = 1`, `d > 1`: result has `r₁ = 0`, in T \ S (e.g., `[5, 3] ⊖ [5, 1] = [0, 2]`). For `⊖` with `actionPoint(w) = 1`, `#o = #w ≥ 2`, `o = w`: result is `[0, ..., 0] ∈ Z`. For `⊖` when `#w > #o`: result has trailing zeros, in T \ S. For single-component ordinals: `[x] ⊖ [n] ∈ S` when `x > n`, `∈ Z` when `x = n`.
- *Frame:* The subspace identifier `N` is not an operand and is never modified.
- *Definition:* **S** = {o ∈ T : #o ≥ 1 ∧ (A i : 1 ≤ i ≤ #o : oᵢ > 0)}.
