# Cone Review — ASN-0034/ReverseInverse (cycle 1)

*2026-04-18 19:44*

### Under-cited `yₖ + wₖ > wₖ` step in ReverseInverse
**Foundation**: NAT-addcompat, NAT-closure, NAT-cancel (not listed in ReverseInverse's Depends)
**ASN**: ReverseInverse, Step 3, sub-proof of `y ⊕ w > w`: "Therefore `yₖ > 0`, giving `(y ⊕ w)ₖ = yₖ + wₖ > wₖ`."
**Issue**: The strict component inequality `yₖ + wₖ > wₖ` from the hypothesis `yₖ > 0` is asserted without per-step axiom citations. TumblerAdd's dominance sub-case `aₖ > 0` discharges the structurally identical step via a four-step chain (NAT-addcompat right order-compatibility lifting `0 ≤ yₖ` to `yₖ + wₖ ≥ 0 + wₖ`; NAT-closure additive identity rewriting `0 + wₖ` to `wₖ`; NAT-cancel summand absorption ruling out the equality disjunct; NAT-order defining clause promoting the non-strict `≥` to strict `>`). ReverseInverse's Depends enumerates TumblerAdd only for the prefix-copy/advance/tail-copy rule and the result-length identity, and enumerates NAT-sub and NAT-order but not NAT-addcompat, NAT-closure, or NAT-cancel. TumblerAdd's exported dominance postcondition `a ⊕ w ≥ w` is non-strict, so transitive availability through TumblerAdd does not supply the strict form this step consumes to feed T1 case (i).
**What needs resolving**: Either expand the step with per-step NAT-addcompat + NAT-closure + NAT-cancel + NAT-order citations (adding those axioms to Depends, matching the discipline TumblerAdd, TA4, and TA3-strict apply at analogous strict-through-addition sites), or strengthen TumblerAdd to export a conditional strict-dominance postcondition (e.g., `Pos(a) ⟹ a ⊕ w > w` when `actionPoint(w) ≤ #a`) and cite it here.
