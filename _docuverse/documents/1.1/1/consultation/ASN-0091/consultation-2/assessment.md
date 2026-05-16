# Revision Categorization — ASN-0065 review-2

**Date:** 2026-03-21 20:48



## Issue 1: No worked example for the 4-cut swap
Category: INTERNAL
Reason: The 4-cut swap postconditions (R-S1, R-S2, R-S3) and permutation (R-SPERM) are fully defined in the ASN. Constructing a worked example requires only applying these existing definitions to concrete values — no external design intent or implementation evidence is needed.

## Issue 2: Arrangement invariants not explicitly verified
Category: INTERNAL
Reason: The ASN already identifies REARRANGE as K.μ~ and establishes dom(M'(d)) = dom(M(d)) via the bijection π, R-PIV/R-SWP for functionality, and R-CP for range preservation. The missing S2/S3/S8a/S8-depth/S8-fin verifications follow directly from these established facts combined with ASN-0047's definitions — the review itself notes the arguments are "trivial" and spells out exactly how each follows.
