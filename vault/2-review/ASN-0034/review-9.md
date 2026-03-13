# Review of ASN-0034

Based on Alloy modeling-1

## SKIP

### Modeling artifact: T0(a) UnboundedComponents — bounded scope cannot witness unboundedness

The check `UnboundedComponents` produces SAT (counterexample) because T0(a) is an inherently unbounded property: it asserts that for every tumbler and every component position, a tumbler with a strictly larger value at that position exists. Alloy's finite integer scope (`5 Int` = range -16..15) means the maximum representable component value is 15. When a tumbler already has component value 15 at some position, no atom in the finite model can have a larger value there. The counterexample demonstrates the ceiling of Alloy's bounded integers, not a deficiency in the spec.

This is the canonical example of a property that bounded model checking cannot verify — it requires an infinite carrier set by definition. The ASN explicitly acknowledges this: "The address space within any subtree is inexhaustible." No finite model can witness inexhaustibility.

The non-vacuity run (SAT) confirms the model is well-formed.

### Passed properties (29)

All remaining properties — T0(b), T1, T2, T3, T4, T5, T6, T7, T8, T9, T10, T10a, Prefix ordering extension, Partition monotonicity, TA0, TA1, TA1-strict, TA-strict, TA2, TA3, TA3-strict, TA4, Reverse inverse, TA5, TA5 preserves T4, TA6, TA7a, Associativity, T12 — passed bounded check with no counterexamples within scope.

VERDICT: CONVERGED
