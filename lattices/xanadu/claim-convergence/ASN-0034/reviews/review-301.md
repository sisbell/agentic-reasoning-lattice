# Cone Review — ASN-0034/TA3 (cycle 2)

*2026-04-18 15:45*

### TA6 Conjunct 2's `> 0 ⟺ ≠ 0` bridge uses NAT-order directly, but TA6's Depends characterises NAT-order as "invoked transitively through TA-PosDom"

**Foundation**: N/A — cross-cutting citation discipline established throughout this ASN (TumblerSub precondition-consequence case (ii), TA2 sub-case (ii), ActionPoint's third postcondition) that the `≠ 0 ⟹ > 0` step is discharged by NAT-zero's lower bound together with NAT-order's defining clause `m ≤ n ⟺ m < n ∨ m = n`, with both axioms cited directly at that step.

**ASN**: TA6 Conjunct 2 proof: "with that lower bound, the conditions `tⱼ > 0` and `tⱼ ≠ 0` coincide on ℕ-valued components — the forward direction `tⱼ > 0 ⟹ tⱼ ≠ 0` excludes equality because `0 < tⱼ` is strict, and the converse `tⱼ ≠ 0 ⟹ tⱼ > 0` combines `0 ≤ tⱼ` with `tⱼ ≠ 0` to yield `0 < tⱼ`." TA6's NAT-order Depends entry: "NAT-order (NatStrictTotalOrder) — invoked transitively through TA-PosDom's postcondition for Conjunct 2; TA-PosDom's Case `#z ≥ k` uses NAT-order's definitional unfold... and Conjunct 2 inherits both steps without repeating them."

**Issue**: TA6's own proof performs the `tⱼ ≠ 0 ⟹ tⱼ > 0` bridge *before* invoking TA-PosDom. The converse step requires unfolding NAT-order's `0 ≤ tⱼ ⟺ 0 < tⱼ ∨ 0 = tⱼ` to eliminate the equality disjunct against `tⱼ ≠ 0`, and the forward step invokes strictness (irreflexivity) of `<`. Both are direct NAT-order uses in TA6, not transitive consumption of TA-PosDom. The Depends entry only describes the transitive use through TA-PosDom's Cases `#z ≥ k` and `#z < k`, omitting accounting for TA6's own `≠ 0 ⟺ > 0` bridge step — even though the parallel NAT-zero entry in the same Depends list explicitly attributes "strictness of `<`" and the combination step to NAT-order in a way that the NAT-order entry itself does not mirror.

**What needs resolving**: TA6's NAT-order Depends entry must be expanded to enumerate the direct use at the `≠ 0 ⟺ > 0` bridge (the `m ≤ n ⟺ m < n ∨ m = n` defining clause at `m = 0, n = tⱼ` and the irreflexivity/strictness of `<`) alongside the transitive use through TA-PosDom, matching the per-step convention TumblerSub's precondition-consequence case (ii), TA2's sub-case (ii), and ActionPoint's third postcondition all apply for the structurally identical inference.
