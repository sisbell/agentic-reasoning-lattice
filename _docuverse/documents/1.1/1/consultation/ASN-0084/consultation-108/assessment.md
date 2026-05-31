# Channel Assignment — ASN-0084 review-108

**Date:** 2026-05-30 21:47

## Issue 1: R-CANON cites TS2 for amount-injectivity; the correct lemma is TS5
Reason: Pure citation fix internal to the formal layer — the ASN itself already cites TS5 correctly for amount-injectivity in its Truncated-subtraction definition, so the correction is derivable from the ASN's own content and ASN-0034's lemma roster. No design intent or implementation evidence is needed.

## Issue 2: Run convention miscites TS3 for the depth-generality of shift
Reason: Pure citation fix — the asserted fact (shift is defined at any depth and increments only the last component) is exactly OrdinalShift's stated content in ASN-0034, so the correct citation is determinable from the foundation definitions alone. Neither design intent nor udanax-green evidence bears on which lemma to cite.
