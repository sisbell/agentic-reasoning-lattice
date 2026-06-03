# Channel Assignment — ASN-0075 review-72

**Date:** 2026-06-03 11:31

## Issue 1: wp(SHOWDELETIONS, q) is not the weakest precondition
Reason: This is a formal precision defect — the fix (either drop the boundary conjunct from wp or strengthen q to the classification-level postcondition) is derivable entirely from the ASN's own definitions of q, D-EXH, C-fin, and S8-fin. No design intent or implementation evidence bears on what the weakest precondition for the stated postcondition is.

## Issue 2: Section thesis duplicates the D-NEED corollary verbatim
Reason: Purely editorial — collapsing the duplicated conclusion into a one-line section thesis requires only the ASN's existing text; no external channel informs which phrasing to keep.

## Issue 3: Internal redundancy in the granularity paragraph
Reason: Editorial deduplication within a single sentence; the set-granularity fact is fully present in the ASN and needs no design-intent or implementation input.
