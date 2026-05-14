# Review of ASN-0042

## REVISE

### Issue 1: Worked example doesn't trace prerequisite baptisms required by ASN-0040 B1

**ASN-0042, Worked Example (Delegation section; Field-opening boundary case)**: 

For π_A's delegation introducing pfx(π_A) = [1, 0, 2]: since [1, 0, 2] = c_2 in S([1], 2) (where c_1 = inc([1], 2) = [1, 0, 1] via TA5(d) and c_2 = inc(c_1, 0) = [1, 0, 2]), ASN-0040 B1 (ContiguousPrefix) requires c_1 = [1, 0, 1] to be in Σ_1.B. The worked example traces Bop([1, 0, 2], 2) calls during pre-delegation but doesn't trace any baptism producing [1, 0, 1].

For π_B's delegation introducing pfx(π_B) = [1, 0, 2, 3]: since [1, 0, 2, 3] = c_3 in S([1, 0, 2], 1), B1 requires [1, 0, 2, 1] and [1, 0, 2, 2] to be in Σ_3.B. The "Sub-account namespace" paragraph acknowledges this ("[1, 0, 2, 3] is the third baptism in S(pfx(π_A), 1), preceded by [1, 0, 2, 1] and [1, 0, 2, 2] (or by sub-delegations whose prefixes occupy those slots)") but the Field-opening boundary case never traces these in the main timeline.

**Problem**: The worked example asserts delegations whose validity depends on prerequisite baptisms required by B1, but doesn't trace those prerequisites. Combined with O18's freshness conjunct (pfx(π') ∉ Σ.B prior), this leaves an unstated structural assumption: the prerequisite sibling tumblers must already be in Σ.B without violating freshness for the delegated prefix.

**Required**: Either (a) explicitly trace prior Bop calls (e.g., Bop([1], 2) baptizing [1, 0, 1] before π_A's delegation; Bop([1, 0, 2], 1) baptizing [1, 0, 2, 1] and [1, 0, 2, 2] before π_B's delegation, with the corresponding O5 authorizations), or (b) state that the relevant pre-baptized tumblers are part of Σ_0.B as initial setup (covered by π_N per O14's coverage clause) and explain why this is consistent with O18's freshness for the actually-delegated prefixes.

### Issue 2: Worked example's "Sub-account namespace" and "Verifying O8" use the same prefix in conflicting ways

**ASN-0042, Worked Example (Sub-account namespace; Verifying O8)**:

The "Sub-account namespace" paragraph posits ("Now suppose...") that π_A baptizes [1, 0, 2, 3] as an organizational namespace, then derives that O18 forecloses any later delegation of that prefix. The subsequent "Verifying O8" and "Field-opening boundary case" sections then treat Σ_3 as "after π_A delegates sub-account [1, 0, 2, 3] to π_B" — which the earlier paragraph just argued is impossible if [1, 0, 2, 3] was baptized as a namespace.

**Problem**: These scenarios are presented sequentially in the same worked example timeline without explicit marking that they are alternative futures. A reader following the example as a single timeline encounters a contradiction.

**Required**: Mark these as explicit alternative scenarios (e.g., "Scenario A — namespace baptism" and "Scenario B — sub-delegation"), or restructure so that the main timeline doesn't baptize [1, 0, 2, 3] before the Field-opening case's delegation.

## OUT_OF_SCOPE

None significant — the Open Questions appropriately defer ownership transfer, federation, and revocation to future ASNs.

VERDICT: REVISE
