# Channel Assignment — ASN-0047 review-290

**Date:** 2026-06-01 21:22

## Issue 1: C1c (and M1) inherited invariants are never accounted for
Reason: Derivable internally. L1c already provides the exact template (first emission via SubAllocatorBundle, subsequent via TA5(c)), C1c is the symmetric content analogue with identical shape, and both C1c and M1 are already-cited ASN-0093 foundation invariants — no design intent or implementation evidence is needed to add the parallel row and the `dom(M)` vs `dom(M(d))` clarifier.

## Issue 2: The ~30-label per-state invariant list is enumerated verbatim three times
Reason: Pure deduplication of an existing label list; consolidating to the `ExtendedReachableStateInvariants` definition and referencing it elsewhere requires no external input.

## Issue 3: Clause (v)'s independence construction restates what LRP already establishes
Reason: Internal exposition fix. The relationship between clause (v), LRP, and the *Link V-position permanence* walk-back is fully present in the ASN; collapsing the two passes and relabeling clause (v) as a realisation artifact is derivable from the existing proof structure.

## Issue 4: Rationale-over-statement prose around P4★ and J0
Reason: Trimming existing meta-prose. The P4★/P7 incompatibility is already made structural by S3★/L14, and J0's Nelson citation is already present in the text — reducing to one clause each needs no new channel input.
