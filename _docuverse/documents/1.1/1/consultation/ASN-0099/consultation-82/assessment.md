# Channel Assignment — ASN-0099 review-82

**Date:** 2026-06-04 15:25

## Issue 1: "The Empty Query" forward-references claims defined in later sections
Reason: Purely structural reorganization — relocating or restricting the empty-query discussion to claims already in scope. No design intent or implementation evidence is needed; the dependency order is internal to the document.

## Issue 2: The match existential is written twice
Reason: Mechanical de-duplication — introduce `matches` once and reference it in the `findlinks` definition. The two predicates are already identical in the ASN, so the fix is fully internal.

## Issue 3: Claim labels are non-contiguous and out of document order
Reason: Editorial renumbering plus a confirmation that no F7/F16/F17/F18 references exist (the review already notes none found). This is bookkeeping derivable from the ASN's own text.
