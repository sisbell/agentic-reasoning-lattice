# Revision Categorization — ASN-0081 review-7

**Date:** 2026-04-09 20:11



## Issue 1: D-SEP(b) proof conflates two cases under a single D-CTG application
Category: INTERNAL
Reason: The fix is a proof restructuring — splitting into v = r and v > r cases — using only definitions and properties already present in the ASN.

## Issue 2: Foundation Citations section incomplete
Category: INTERNAL
Reason: All missing citations (D-SEQ, D-MIN, S2, S3, S8-fin, S0) are ASN-0036 properties already cited inline in the proofs; completing or retitling the section requires only the ASN's own content.

## Issue 3: D-CS registry entry drops quantifier domain
Category: INTERNAL
Reason: The correct formulation already exists in the body text; the registry entry just needs to be updated to match it.

## Issue 4: OrdinalDisplacementProjection lacks w_ord > 0 postcondition
Category: INTERNAL
Reason: The positivity of w_ord follows directly from the contraction preconditions (w > 0, w₁ = 0) already stated in the ASN; adding the postcondition and verifying it in the TA4 citation requires only existing definitions.
