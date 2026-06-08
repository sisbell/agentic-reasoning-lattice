# Channel Assignment — ASN-0107 review-22

**Date:** 2026-06-08 11:53

## Issue 1: R2's endpoint-removal mechanism ignores the canonical-prefix contraction discipline
Reason: Internal. The fix follows from ASN-0047's PerSubspaceContractionScope (already cited) and R1's own (P-max) precondition; conditioning R2 on the arrangement-maximal endpoint or restating the bound over the actually-removed prefix is derivable from material already in the note.

## Issue 2: Repeated deferrals to the retrieval operation across three sections
Reason: Internal. Pure editorial deduplication — state the out-of-scope boundary once and remove the two restatements; no design intent or implementation evidence required.

## Issue 3: Reviser drift — meta-prose justifying preconditions and a non-necessity digression
Reason: Internal. Compression of meta-prose; the preconditions and D2's operative fact already stand on their own content, so dropping the rationale and digression needs nothing external.

## Issue 4: R5 restates E4 and D2 without adding content
Reason: Internal. R5 is a synthesis of E4 and D2 already in the note; folding or removing it is an editorial decision derivable from the ASN's own claims.

## Issue 5: "Withdrawn link" terminology contradicts the no-retraction model
Reason: Internal. R1 already establishes the no-retraction model and names the actual mechanism (endpoint contraction); the terminology fix is a rename consistent with content already present.
