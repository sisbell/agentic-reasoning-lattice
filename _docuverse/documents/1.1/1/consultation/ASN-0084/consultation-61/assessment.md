# Channel Assignment — ASN-0084 review-61

**Date:** 2026-05-30 13:53

## Issue 1: Dangling reference to a non-existent "Scope note"
Reason: Pure internal cross-reference repair — the correct carrier (R-NS(NS-run), V-extent confinement) is already present in this ASN; no design intent or implementation evidence is involved.

## Issue 2: The "post-state S8 follows from foundation S8" claim is stated four times
Reason: De-duplication of a claim restated across four sections of this ASN; consolidating to a single statement is internal editorial restructuring.

## Issue 3: R-SP largely re-walks the "Invariant preservation" paragraph it cites
Reason: Collapsing R-SP's body to the S8 step plus a pointer is internal restructuring; the mechanisms it re-enumerates are already established within the ASN.

## Issue 4: R-NS(NS-run) "Phases 2 and 3" duplicates R-BLK's non-S handling
Reason: Resolving mutual deferral between two passages by making R-NS authoritative is internal editorial work, with both passages already in this ASN.

## Issue 5: Disclaimer meta-prose about claim posture
Reason: Removing scope-hedging sentences is internal; the lemma names and postconditions already delimit the claims.

## Issue 6: Cancellation citation does not cover the zero shift amount
Reason: The reviewer already identifies the correct fix (restrict to the positive sub-domain used, or add the TS4 ShiftStrictIncrease step); the relevant tumbler-algebra properties are sibling-ASN content the fix can cite directly, so no design-intent or implementation channel is needed.
