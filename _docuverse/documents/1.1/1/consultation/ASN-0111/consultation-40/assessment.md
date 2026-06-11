# Channel Assignment — ASN-0111 review-40

**Date:** 2026-06-10 23:04

## Issue 1: RL5's screen-passing branch claims allocatability that the transition vocabulary does not provide
Reason: The corrected dichotomy and both witness families are derivable from the cited model facts (TA5(c), NodeLineage, K.λ), but the new claim that screen-passing addresses at element-field depth > 2 are *permanently* unallocatable rests on the allocator emitting only depth-2 frontier addresses — this should be checked against what the implementation actually does before the spec asserts permanence. No design-intent question arises; the caching-discipline rationale (undecidability from the address alone) follows from the ASN's own RL0 insufficiency argument.
Gregory question: Does udanax-green's link allocator ever emit a link address whose element field has depth greater than 2 (anything other than incrementing the final digit of `d.0.s_L.n`), or allocate links homed under nodes outside the `n₀` lineage — or is the frontier chain `inc(·, 0)` at depth 2 the only allocation path?

## Issue 2: RL4's non-vacuity construction leaves its own base hypothesis unwitnessed
Reason: The fix is internal — the review specifies the exact two-step K.δ prefix from `Σ₀` (account `[1.0.1]`, then document `[1.0.1.0.1]`), and every precondition it discharges (operand zeros bound, parent membership, ChildSpawnFreshness) is already part of the ASN-0047 vocabulary the note cites. No design-intent or implementation evidence is involved.

## Issue 3: RL0's "no partial-success middle state" passage duplicates RL1 (anti-bloat)
Reason: Purely editorial restructuring within the ASN's own content — delete the duplicated completeness sentences from the RL0 section and move the one-sentence codomain-closure observation into RL1. No external fact is needed to perform or verify the change.
