# Channel Assignment — ASN-0040 review-65

**Date:** 2026-05-28 23:28

## Issue 1: The "S2 exception" is deferred to from four separate sites
Reason: Pure editorial consolidation — the injectivity motivation is already derived at S2 within the ASN; collapsing the three restatements into label citations requires no design intent or implementation evidence.

## Issue 2: B8 is labeled "Global Uniqueness" but proves only co-reachable uniqueness
Reason: The renaming is internal — the proof scope (co-reachable, single-path) is explicitly stated in B8's own content, and the mismatch with ASN-0034's unconditional `GlobalUniqueness` is visible from the text alone.

## Issue 3: B6 condition-(iii) subsumption explained twice
Reason: Both the duplication and the postcondition tightening are derivable from B6's own necessity proof, which already establishes that (iii) binds independently only at d=2.

## Issue 4: B3 fourth-quadrant sentence enumerates a case the requirement already excludes
Reason: Deleting a sentence that merely restates the contrapositive of B3's own implication is purely internal.

## Issue 5: B9 trace Steps 6–7 are near-verbatim repetitions of Step 5
Reason: Collapsing redundant trace iterations into a summary remark is an editorial change fully derivable from the existing trace structure.
