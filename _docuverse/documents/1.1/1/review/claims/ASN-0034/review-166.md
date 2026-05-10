# Cone Review — ASN-0034/ActionPoint (cycle 2)

*2026-04-17 14:36*

### ActionPoint second postcondition omits lower bound on quantified index `i`
**Foundation**: T0 (CarrierSetDefinition), whose formal contract states the component projection `·ᵢ` yields `aᵢ ∈ ℕ` only *"for each `1 ≤ i ≤ #a`"* — `wᵢ` is not defined for `i < 1`.
**ASN**: ActionPoint, second postcondition *"wᵢ = 0 for all i < actionPoint(w)"*.
**Issue**: The quantifier `for all i < actionPoint(w)` has no lower bound. Since `actionPoint(w) ≥ 1` by the first postcondition, the stated range includes `i = 0` and negative `i`, on which T0 does not define `wᵢ`. The claim `wᵢ = 0` at such `i` is ill-formed under T0's domain. TA-Pos's analogous proof step is careful to write *"For `1 ≤ i < k`"* and its formal postcondition `(A i : 1 ≤ i ≤ #z : …)` restricts the index explicitly; ActionPoint's postcondition departs from that convention. The supporting derivation *"any smaller index with wᵢ ≠ 0 would be a smaller member of the set"* implicitly relies on `i ≥ 1` (membership in `{i : 1 ≤ i ≤ #w ∧ wᵢ ≠ 0}`), but the postcondition itself does not say so.
**What needs resolving**: Either restrict the second postcondition's quantifier to `1 ≤ i < actionPoint(w)` so that every `wᵢ` referenced lies in T0's defined domain, or otherwise make the postcondition's claim well-typed against T0's component-projection convention and consistent with TA-Pos's explicit lower-bound style.

## Result

Cone converged after 3 cycles.

*Elapsed: 690s*
