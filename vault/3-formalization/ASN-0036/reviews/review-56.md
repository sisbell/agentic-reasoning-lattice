# Proof Review — ASN-0036 (cycle 1)

*2026-04-12 21:05*

32 properties

### subspace(v)

RESULT: FOUND

**Problem**: The formal contract postcondition claims "When `v` satisfies S8a: `subspace(v) ≥ 1`", and the narrative states "by S8a, subspace(v) ≥ 1 in that case" — yet the dependency list is "(none)". S8a is used to establish a postcondition guarantee but is not declared as a dependency. Either S8a must appear in the dependency list, or the conditional postcondition must be removed from the formal contract and the narrative reference downgraded to pure commentary.

**Required**: One of two fixes:
1. Add S8a to the dependency list and keep the conditional postcondition, or
2. Remove "When `v` satisfies S8a: `subspace(v) ≥ 1`" from the postconditions and soften the narrative reference to a non-contractual remark (e.g., "Note: for V-positions, S8a separately guarantees v₁ ≥ 1").

31 verified, 1 found.

## Result

Converged after 2 cycles. 32 verified.

*Elapsed: 529s*
