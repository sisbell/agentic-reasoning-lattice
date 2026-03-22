# Revision Categorization — ASN-0063 review-5

**Date:** 2026-03-21 19:24



## Issue 1: K.μ~ preservation of S3★ is asserted without proof
Category: INTERNAL
Reason: The argument is fully derivable from the existing definitions of K.μ~, the amended K.μ⁺, and S3★ — all present in this ASN and ASN-0047. The review even sketches the three-step proof needed.

## Issue 2: CL3 postcondition omits the arrangement change
Category: INTERNAL
Reason: The missing postcondition clauses (f) and (g) follow directly from K.μ⁺_L's definition and frame, both specified in this ASN. No external design intent or implementation evidence is needed.

## Issue 3: K.μ⁺_L precondition uses post-state notation
Category: INTERNAL
Reason: This is a notational consistency fix aligning with the pre-state convention established in ASN-0047. The correct variable name (unprimed L) and the reasoning are already present in the ASN.

## Issue 4: CL2 claimed for the direct I-span form where it does not apply
Category: INTERNAL
Reason: The fix requires choosing between generalizing CL2 or scoping it to V-space only — both options are derivable from the definitions already in this ASN. No Nelson design intent or Gregory implementation evidence is needed.
