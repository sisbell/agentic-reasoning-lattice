# Channel Assignment — ASN-0119 review-9

**Date:** 2026-06-09 01:08

## Issue 1: Referential-integrity claim contradicts the link-subspace V-positions the ASN accommodates
Reason: The fix is internal to the ASN. Its scope paragraph and its import of ASN-0084 (whose frame R-FRAME-P/S(a) ranges over positions with `subspace(v) ≠ S`) already commit to link-subspace V-positions in `M(d)`; the reviewer identifies that reading as the one the ASN's own commitments require. Restating S3 in per-subspace form (content positions → `dom(C)`, link positions → `dom(L)`) and letting P1's range invariance discharge it is derivable from the ASN's existing content and citations, with no need to consult design intent or the implementation.
