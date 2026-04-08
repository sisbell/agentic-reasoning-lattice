## Subspace closure

When arithmetic advances a position within one element subspace, the result must remain in that subspace. Text positions must not cross into link space, and vice versa.

An element-local position within subspace `S` has two components: the subspace identifier `N` and the ordinal `x`. A natural first attempt at an element-local displacement is `w = [0, n]` — action point `k = 2`, preserving the subspace identifier and advancing the ordinal. Addition works: `[N, x] ⊕ [0, n] = [N, x + n]`, preserving the subspace. But subtraction exposes a subtlety: `[N, x] ⊖ [0, n]` finds the first divergence at position 1 (where `N ≠ 0`), not at position 2 where the intended action lies. The subtraction produces `[N - 0, x] = [N, x]` — a no-op. The abstract `⊖` cannot shift a position backward by a displacement that disagrees with the position at the subspace identifier.

Gregory's implementation reveals the resolution. The operands passed to the arithmetic during shifts are not full element-local positions; they are *within-subspace ordinals* — the second component alone. The subspace identifier is not an operand to the shift; it is structural context that determines *which* positions are subject to the shift. The arithmetic receives ordinals, not full positions.

**TA7a (SubspaceClosure).** The canonical representation for shift arithmetic is the *ordinal-only* formulation: a position in a subspace with identifier `N` and ordinal `o = [o₁, ..., oₘ]` (where `m ≥ 1`) is represented as the tumbler `o` for arithmetic purposes, with `N` held as structural context. Define **S** = {o ∈ T : #o ≥ 1 ∧ (A i : 1 ≤ i ≤ #o : oᵢ > 0)} — ordinals with all positive components, matching T4's positive-component constraint on element fields. An element-local displacement is a positive tumbler `w` with action point `k` satisfying `1 ≤ k ≤ m`. In this formulation:

  `(A o ∈ S, w > 0 : k ≤ #o ⟹ o ⊕ w ∈ T)`

  `(A o ∈ S, w > 0 : o ≥ w ⟹ o ⊖ w ∈ T)`

Both claims assert closure in T: arithmetic on ordinals, with the subspace identifier held as structural context, produces results that remain in T. The subspace identifier is not an operand — it determines *which* positions are subject to the shift, but never enters the arithmetic. This design ensures that no shift can escape the subspace.

The ordinal-only formulation is not arbitrary. The natural 2-component formulation `[N, x]` fails for subtraction: `[N, x] ⊖ [0, n]` finds the divergence at position 1 (where `N > 0 = 0`), producing `[N, x]` — a no-op rather than a genuine shift. Stripping the subspace identifier from the operands avoids this degeneracy.

*Proof.* We prove each conjunct of TA7a, then analyze the finer question of S-membership.

Let `o = [o₁, ..., oₘ]` with `o ∈ S`, so `m ≥ 1` and every `oᵢ > 0`. Let `w` be a positive displacement with action point `k = min({i : 1 ≤ i ≤ #w ∧ wᵢ ≠ 0})`.

**Conjunct 1** (`⊕`-closure in T). The precondition gives `o ∈ T`, `w ∈ T`, `w > 0`, and `k ≤ #o = m`. These are exactly the preconditions of TA0 (well-defined addition). By TA0, `o ⊕ w ∈ T`, with `#(o ⊕ w) = #w`. The subspace identifier, held as structural context outside the operands, is untouched.

A stronger result holds for S-membership. By TumblerAdd's constructive definition, the result `r = o ⊕ w` has components: `rᵢ = oᵢ > 0` for `1 ≤ i < k` (prefix copied from `o ∈ S`); `rₖ = oₖ + wₖ > 0` (since `oₖ > 0` because `o ∈ S`, and `wₖ > 0` because `k` is the action point of `w`); and `rᵢ = wᵢ` for `k < i ≤ #w` (tail copied from the displacement). Components before and at the action point are positive. The result is in S precisely when every tail component `wᵢ` (for `i > k`) is also positive. For single-component ordinals — the common case — `[x] ⊕ [n] = [x + n]`, which is unconditionally in S since both `x > 0` and `n > 0`.

For example, spanning from ordinal `[1, 3, 2]` to `[1, 5, 7]` requires displacement `[0, 2, 7]` (action point `k = 2`). TumblerAdd produces `[1, 3 + 2, 7] = [1, 5, 7]` — position 1 of the ordinal is copied from the start, preserving the ordinal prefix.

**Conjunct 2** (`⊖`-closure in T). The precondition gives `o ∈ T`, `w ∈ T`, and `o ≥ w`. These are exactly the preconditions of TA2 (well-defined subtraction). By TA2, `o ⊖ w ∈ T`. The subspace identifier is again untouched.

The S-membership question for `⊖` is more delicate. We analyze by action point and divergence position, using TumblerSub's constructive definition: zero-pad to length `max(#o, #w)`, find the divergence position `d` (the first position where the padded sequences differ), then set `rᵢ = 0` for `i < d`, `r_d = o_d - w_d`, and `rᵢ = oᵢ` for `i > d`.

*Preliminary: when `#w > m`.* TumblerSub produces a result of length `max(m, #w) = #w > m`. The zero-padded minuend has zeros at positions `m + 1` through `#w`, so the result inherits trailing zeros at those positions and lies in T \ S. The cases below assume `#w ≤ m`.

*Case `k ≥ 2`:* The displacement has `wᵢ = 0` for all `i < k`, so in particular `w₁ = 0`. Since `o ∈ S`, `o₁ > 0`. Therefore `o₁ ≠ w₁` and the divergence falls at `d = 1`. TumblerSub produces: `r₁ = o₁ - 0 = o₁ > 0`, and `rᵢ = oᵢ > 0` for `1 < i ≤ m` (copied from the minuend since `i > d = 1`). When `#w ≤ m`, the result has length `m` and equals `o` itself — a no-op. The result is trivially in S. This is the vacuous closure: TumblerSub finds the mismatch at the ordinal's first positive component rather than at the displacement's intended action point.

*Case `k = 1`, divergence `d = 1`:* The displacement has `w₁ > 0`, and `o₁ ≠ w₁`. Since `o ≥ w`, the ordering at the first divergence position requires `o₁ > w₁` (T1). TumblerSub produces: `r₁ = o₁ - w₁ > 0` (since `o₁ > w₁ ≥ 1`), and `rᵢ = oᵢ > 0` for `1 < i ≤ m` (copied from the minuend). When `#w ≤ m`, all components are positive and the result is in S.

*Case `k = 1`, divergence `d > 1`:* The displacement has `w₁ > 0`, and `o₁ = w₁` (the operands agree at position 1, with divergence at some later `d > 1`). TumblerSub zeros all positions before `d`: `rᵢ = 0` for `1 ≤ i < d`. In particular `r₁ = 0`, so the result has a zero first component and is not in S. Counterexample: `o = [5, 3]`, `w = [5, 1]` (action point `k = 1`, divergence `d = 2`). TumblerSub yields `r = [0, 3 - 1] = [0, 2]`. We have `[0, 2] ∈ T` (confirming the T-closure claim) but `[0, 2] ∉ S ∪ Z`. This sub-case arises when `o` and `w` share a leading prefix — the subtraction produces a displacement-like tumbler with leading zeros rather than a valid ordinal position.

For single-component ordinals, the `d > 1` sub-case cannot arise (there is only one position), and `⊖` gives closure in S ∪ Z: `[x] ⊖ [n]` is `[x - n] ∈ S` when `x > n`, or `[0] ∈ Z` when `x = n` (a sentinel, TA6).

In every case, the result lies in T. The subspace identifier, held as structural context outside the operands, is never modified by either operation. TA7a holds. ∎

The restriction to element-local displacements is necessary. An unrestricted displacement whose action point falls at the subspace-identifier position could produce an address in a different subspace — TA7a cannot hold for arbitrary `w`.

*Formal Contract:*
- *Preconditions:* For `⊕`: `o ∈ S`, `w ∈ T`, `w > 0`, `actionPoint(w) ≤ #o`. For `⊖`: `o ∈ S`, `w ∈ T`, `w > 0`, `o ≥ w`.
- *Postconditions:* `o ⊕ w ∈ T`, `#(o ⊕ w) = #w`. `o ⊖ w ∈ T`. For `⊕`, the result is in S when all tail components of `w` (after the action point) are positive. For `⊖` with `actionPoint(w) ≥ 2` and `#w ≤ #o`: the divergence falls at position 1, TumblerSub produces `o` itself (a no-op), and the result is in S. For `⊖` with `actionPoint(w) = 1` and divergence at position `d = 1` (i.e., `o₁ ≠ w₁`): `r₁ = o₁ - w₁ > 0` and `rᵢ = oᵢ > 0` for `i > 1`, so the result is in S when `#w ≤ #o`. For `⊖` with `actionPoint(w) = 1` and divergence at position `d > 1` (i.e., `o₁ = w₁`): the result has `r₁ = 0` and lies in `T \ S` (counterexample: `[5, 3] ⊖ [5, 1] = [0, 2]`). For `⊖` when `#w > #o`: the result inherits trailing zeros at positions `#o + 1` through `#w` and lies in `T \ S`. For `⊖` on single-component ordinals (`#o = 1`, `#w = 1`): the result is in `S ∪ Z`: `[x] ⊖ [n] ∈ S` when `x > n`, and `[x] ⊖ [n] ∈ Z` when `x = n`.
- *Frame:* The subspace identifier `N`, held as structural context, is not an operand and is never modified by either operation.
- *Definition:* **S** = {o ∈ T : #o ≥ 1 ∧ (A i : 1 ≤ i ≤ #o : oᵢ > 0)} — ordinals with all positive components, matching T4's positive-component constraint on element fields.
