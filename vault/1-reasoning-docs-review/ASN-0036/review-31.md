# Rebase Review of ASN-0036

## REVISE

(none)

All citations to ASN-0034 foundation properties are correct:

- **S1→T8**: Correctly characterized as content-store specialization of AllocationPermanence.
- **S4→T9, T10, T10a, TA5, T3**: Three cases (same-allocator, non-nesting cross-allocator, nesting-prefix) are exhaustive and correctly argued. Nesting-prefix case: parent outputs at depth `d`, child at depth `d + k'` by TA5(d), distinct by T3.
- **S7→S7a, S7b, T4, T9, T10, T10a, TA5, T3**: Same three-case structure applied to document prefixes rather than I-addresses. The `origin()` definition correctly uses T4 for field parsing, S7a/S7b for scoping, and the three cases for uniqueness.
- **S8→S8-fin, S8a, S2, S8-depth, T1, T5, T10, TA5(c), TA7a**: Singleton decomposition proof correctly uses T5+T10 for cross-subspace disjointness, TA5(c) for ordinal successor depth preservation, T1 for ordering in the uniqueness argument.
- **D-CTG-depth→T0(a), T1**: Contradiction argument correctly uses T0(a) for unbounded component values and T1 for intermediate ordering.
- **ValidInsertionPosition→OrdinalShift, TumblerAdd, T3**: Depth-2 lower bound correctly derived from TumblerAdd action-point semantics; distinctness of N+1 positions correctly follows from T3.

Registry entries match body text dependencies throughout. No broken references, no orphaned text, no silent dependencies.

VERDICT: CONVERGED
