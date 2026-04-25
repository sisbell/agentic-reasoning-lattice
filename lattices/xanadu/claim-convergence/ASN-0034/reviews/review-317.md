# Cone Review — ASN-0034/D2 (cycle 4)

*2026-04-18 18:53*

Looking at the ASN as a whole, focusing on cross-property consistency between D0, D1, D2, TumblerSub, and the foundation definitions.

### D2 Step 2 skips the ActionPoint min-formula routing that D0 and D1 make explicit
**Foundation**: ActionPoint's defining minimum-formula `actionPoint(w) = min({i : 1 ≤ i ≤ #w ∧ wᵢ ≠ 0})`. TumblerSub's conditional postcondition `actionPoint(a ⊖ w) = zpd(a, w)` is the export that downstream users consume.
**ASN**: D2 Step 2 — "TumblerSub's action-point identification gives actionPoint(b ⊖ a) = zpd(b, a) = k. Since k ≤ #a, TA0's preconditions are satisfied." D2's ActionPoint Depends entry reads only "supplies the action-point function used in the precondition `actionPoint(w) ≤ #a` and in Step 2's claim that `b ⊖ a` has action point `k`."
**Issue**: D0 and D1 both explicitly route this identification through ActionPoint's defining minimum-formula: D0 says "the postcondition `actionPoint(b ⊖ a) = divergence(a, b)` uses ActionPoint's definition (derived via TumblerSub's conditional postcondition and the ZPD–Divergence identification)"; D1 says "The conditional postcondition itself rests on ActionPoint's defining minimum-formula ... applied to w — every component before position k is zero by TumblerSub's component formulas, and wₖ > 0 by Pos(w) ... so the minimum is k; this matches D0's routing". D1 explicitly declares this as a coordinated pattern with D0. D2 uses the same export at the same derivation site but omits both the prose explanation of the min-formula application and the Depends-level declaration of the routing — creating a three-property inconsistency where D0↔D1 coordinate but D2 diverges.
**What needs resolving**: Either expand D2's Step 2 and ActionPoint Depends to route through ActionPoint's defining minimum-formula in the same manner as D0/D1, or justify why D2's terser citation is sufficient despite D1's explicit declaration that the min-formula routing is a shared convention.

---

### TumblerSub's motivation conflates two distinct prefix-case failure modes under a single "actionPoint > #a" description
**Foundation**: TumblerSub's Definition branches on whether `zpd(a, w)` is defined: when defined, `Pos(a ⊖ w)` and `actionPoint(a ⊖ w) = zpd(a, w)`; when undefined (zero-padded-equal), `a ⊖ w` is the zero tumbler and neither postcondition holds.
**ASN**: TumblerSub motivation — "when `a` is a proper sequence-prefix of `b`, the action point of `b ⊖ a` satisfies `actionPoint(b ⊖ a) = zpd(b, a) ≥ #a + 1 > #a`, violating TumblerAdd's precondition `actionPoint(w) ≤ #a`."
**Issue**: The quoted chain presupposes `zpd(b, a)` is defined. But the proper-prefix case splits into two sub-cases: (a) `b` has a nonzero component beyond `#a` — then `zpd(b, a) ≥ #a + 1` as stated; (b) all of `b`'s trailing components past `#a` are zero — then `b` and `a` are zero-padded-equal, `zpd(b, a)` is undefined, `b ⊖ a` is the zero tumbler, and `a ⊕ (b ⊖ a)` is undefined because `Pos(b ⊖ a)` fails rather than because `actionPoint(b ⊖ a) > #a`. Both sub-cases arise under the "proper prefix" hypothesis the motivation names, but the motivation narrates only the first failure mode. A reader verifying that D0's `divergence(a, b) ≤ #a` precondition correctly excludes the full prefix case needs to see both modes addressed.
**What needs resolving**: Either split the motivation's proper-prefix case into the two failure modes (actionPoint-too-big and Pos-fails), or reframe the motivation so the `≥ #a + 1` claim is qualified by "when zpd is defined" and the undefined branch is noted separately.
