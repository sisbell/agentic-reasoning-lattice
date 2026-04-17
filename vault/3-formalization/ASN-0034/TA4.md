**TA4 (PartialInverse).** `(A a, w : Pos(w) ∧ k = #a ∧ #w = k ∧ (A i : 1 ≤ i < k : aᵢ = 0) : (a ⊕ w) ⊖ w = a)`, where `k` is the action point of `w`.

The precondition has three parts. First, `k = #a` — the action point falls at the last component of `a`. This is necessary because addition replaces `a`'s trailing structure below the action point with `w`'s trailing structure (tail replacement, defined below). When `k < #a`, components `aₖ₊₁, ..., a_{#a}` are discarded by addition and cannot be recovered by subtraction. Concretely: `[1, 5] ⊕ [1, 3] = [2, 3]` (action point 1, position 2 replaced by `w`'s trailing `3`), then `[2, 3] ⊖ [1, 3] = [1, 3] ≠ [1, 5]`.

Second, `#w = k` — the displacement has no trailing components beyond the action point. When `#w > k`, the result acquires trailing components from `w` that were not present in `a`. The trailing `7` from `w` persists through subtraction: `[0, 5] ⊕ [0, 3, 7] = [0, 8, 7]`, then `[0, 8, 7] ⊖ [0, 3, 7]` yields `[0, 5, 7] ≠ [0, 5]`.

Third, `(A i : 1 ≤ i < k : aᵢ = 0)` — all components of `a` before the action point are zero. This ensures the subtraction's divergence-discovery mechanism finds the action point at the right position. If `a` has a nonzero component at some position `j < k`, then the result of addition has `rⱼ = aⱼ ≠ 0`, and the subtraction's divergence falls at `j`, not at `k`. Concretely: `[5, 3] ⊕ [0, 7] = [5, 10]`, then `[5, 10] ⊖ [0, 7]`: divergence at position 1, producing `[5, 10] ≠ [5, 3]`.

When all three conditions hold, recovery is exact. The restriction is not a deficiency but a precise statement of when the operations are inverses.

The precondition `Pos(w)` (TA-Pos) guarantees that the action point `k` exists; by TA-Pos, this excludes every all-zero displacement regardless of length.

*Proof.* We show that under the stated preconditions, the round-trip `(a ⊕ w) ⊖ w` recovers `a` exactly. Throughout, `k` denotes the action point of `w` — the least position `i` with `wᵢ > 0` — so by definition `wᵢ = 0` for all `i < k` and `wₖ > 0`.

**Step 1: the structure of `r = a ⊕ w`.** By TumblerAdd (applicable since `k = #a` gives `k ≤ #a`, satisfying TA0's precondition), the result `r` is built in three regions relative to the action point: `rᵢ = aᵢ` for `i < k` (prefix copy), `rₖ = aₖ + wₖ` (single-component advance), and `rᵢ = wᵢ` for `i > k` (tail copy from displacement). We determine each region under the preconditions.

For `i < k`: the precondition `(A i : 1 ≤ i < k : aᵢ = 0)` gives `rᵢ = aᵢ = 0`.

At `i = k`: `rₖ = aₖ + wₖ`, and since `wₖ > 0` (definition of action point), `rₖ ≥ wₖ > 0`.

For `i > k`: by the result-length identity (TA0), `#r = #w`. The precondition `#w = k` gives `#r = k`, so there are no positions beyond `k` — the tail-copy region is empty. The precondition `k = #a` ensures that no components of `a` beyond position `k` are discarded by tail replacement.

Therefore `r = [0, ..., 0, aₖ + wₖ]` — a tumbler of length `k` with zeros at all positions before `k`.

**Step 2: computing `s = r ⊖ w`.** TumblerSub requires `r ≥ w` (T1). Since `r = a ⊕ w`, TumblerAdd's dominance postcondition gives `r ≥ w`, discharging this obligation. Subtraction scans `r` and `w` for the first divergence, zero-padding the shorter to the length of the longer. Since `#r = k = #w`, no padding is needed. At each position `i < k`, both `rᵢ = 0` (established above) and `wᵢ = 0` (definition of action point), so `rᵢ = wᵢ` and no divergence occurs before position `k`.

Two cases arise at position `k`, exhausting all possibilities for `aₖ ∈ ℕ`.

*Case 1: `aₖ > 0`.* Then `rₖ = aₖ + wₖ > wₖ` (since `aₖ > 0`), so `rₖ ≠ wₖ` and the first divergence is at position `k`. Since `rₖ > wₖ`, TumblerSub's precondition `rₖ ≥ wₖ` at the divergence point is satisfied. TumblerSub produces: `sᵢ = 0` for `i < k` (zeroing pre-divergence positions), `sₖ = rₖ - wₖ = (aₖ + wₖ) - wₖ = aₖ` (reversing the advance), and `sᵢ = rᵢ` for `i > k` (tail copy). Since `#r = k`, there are no positions beyond `k`, so the tail-copy region contributes nothing. The result length is `max(#r, #w) = k`, giving `s = [0, ..., 0, aₖ]` of length `k`. By the precondition, `aᵢ = 0` for all `i < k` and `#a = k`, so `s = a`.

*Case 2: `aₖ = 0`.* Every component of `a` is zero: `aᵢ = 0` for `i < k` by precondition, and `aₖ = 0` by the case hypothesis, so `a` is the zero tumbler of length `k`. The addition gives `rₖ = 0 + wₖ = wₖ`. Combined with `rᵢ = 0 = wᵢ` for `i < k` and `#r = k = #w`, this yields `r = w`. Now `s = r ⊖ w = w ⊖ w`: the sequences agree at every position, so no divergence exists and TumblerSub yields the zero tumbler of length `max(#w, #w) = k`. This zero tumbler of length `k` is exactly `a`.

In both cases, `(a ⊕ w) ⊖ w = a`. ∎

*Formal Contract:*
- *Preconditions:* `a ∈ T`, `w ∈ T`, `Pos(w)`, `k = #a`, `#w = k`, `(A i : 1 ≤ i < k : aᵢ = 0)`, where `k` is the action point of `w`
- *Depends:* TA-Pos (PositiveTumbler) — invoked through the precondition `Pos(w)` and consumed by the action-point existence remark ("The precondition `Pos(w)` (TA-Pos) guarantees that the action point `k` exists; by TA-Pos, this excludes every all-zero displacement regardless of length"). ActionPoint (ActionPoint) — invoked at the opening of the proof to fix `k` as "the least position `i` with `wᵢ > 0`" and to license the standing fact `wᵢ = 0` for `i < k` and `wₖ > 0`, both of which are unfolded against TumblerAdd's three regions and TumblerSub's pre-divergence-zero phase. TumblerAdd (TumblerAdd) — invoked at Step 1 to compute `r = a ⊕ w` ("By TumblerAdd (applicable since `k = #a` gives `k ≤ #a`, satisfying TA0's precondition), the result `r` is built in three regions relative to the action point: `rᵢ = aᵢ` for `i < k` (prefix copy), `rₖ = aₖ + wₖ` (single-component advance), and `rᵢ = wᵢ` for `i > k` (tail copy from displacement)"), and again at Step 2 for the dominance postcondition `r ≥ w` ("Since `r = a ⊕ w`, TumblerAdd's dominance postcondition gives `r ≥ w`, discharging this obligation"). TA0 (WellDefinedAddition) — invoked twice: at Step 1 to license TumblerAdd's applicability ("satisfying TA0's precondition") and to supply the result-length identity ("by the result-length identity (TA0), `#r = #w`"); the precondition `#w = k` then collapses the tail-copy region. T1 (LexicographicOrder) — invoked at Step 2's discharge of TumblerSub's input precondition ("TumblerSub requires `r ≥ w` (T1)"); T1 supplies the comparison `≥` against which the dominance fact `r ≥ w` is read. TumblerSub (TumblerSub) — invoked at Step 2 to compute `s = r ⊖ w` via the scan-for-divergence rule ("TumblerSub scans `r` and `w` for the first divergence, zero-padding the shorter to the length of the longer"), and at Cases 1 and 2 for the three-region production rule (`sᵢ = 0` for `i < k`, `sₖ = rₖ - wₖ`, tail copy beyond) used to conclude `s = a`. T3 (CanonicalRepresentation) — invoked implicitly at the closing of both cases when component-by-component agreement and length agreement are converted into tumbler equality ("By the precondition, `aᵢ = 0` for all `i < k` and `#a = k`, so `s = a`" in Case 1; "this yields `r = w`" and "This zero tumbler of length `k` is exactly `a`" in Case 2); T3 supplies the principle that tumblers agreeing in length and at every component are equal.
- *Postconditions:* `(a ⊕ w) ⊖ w = a`

Gregory's analysis confirms that `⊕` and `⊖` are NOT inverses in general. The implementation's `absadd` is asymmetric: the first argument supplies the high-level prefix, the second supplies the low-level suffix. When `d = a ⊖ b` strips a common prefix (reducing the exponent), `b ⊕ d` puts the difference in the wrong operand position — `absadd`'s else branch discards the first argument entirely and returns the second. The operand-order asymmetry causes total information loss even before any digit overflow.

The reverse direction is equally necessary:
