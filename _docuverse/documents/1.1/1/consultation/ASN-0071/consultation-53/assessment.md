# Channel Assignment — ASN-0071 review-53

**Date:** 2026-06-03 10:32

## Issue 1: PC-RANGE assumes every arrangement position has depth ≥ #u
Reason: The fix is a proof-completeness matter fully internal to the ASN — either add `#u ≤ m_C` as a PC-RANGE precondition or case-split on `#v < #u` and show those positions contribute to neither side via PC's totality (already proven here). Both the vspec preconditions and the depth machinery (S8a, PC) are present in the ASN; no design intent or implementation evidence is required.

## Issue 2: The same "coarse-coordinate reach" motif is restated three times
Reason: Purely editorial deduplication — state the coarse-coordinate consequence once at PC-RANGE, let the example illustrate numerically, and drop the recurring "promised in the introduction" back-references. No external input needed.

## Issue 3: "Partial overlap suffices" restates F-find/F-PART already in the claims table
Reason: Editorial trimming — remove the re-derived F-PART biconditional (already in the table) while keeping the extent-measure observation. Derivable from the ASN's own structure alone.
