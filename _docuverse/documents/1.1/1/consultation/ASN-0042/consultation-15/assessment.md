# Revision Categorization — ASN-0042 review-15

**Date:** 2026-03-16 00:32



## Issue 1: O14 permits bootstrap nesting that falsifies the Account-level permanence Corollary
Category: INTERNAL
Reason: The fix is a straightforward formal tightening — adding a non-nesting constraint to O14 that the prose already assumes. All necessary reasoning (the Corollary's derivation, the described bootstrap scenarios) is present in the ASN.

## Issue 2: O4's derivation assumes an unstated allocation-closure property
Category: INTERNAL
Reason: This is a gap in the formal proof structure — the ASN already has the analogous closure axiom for principals (O15) and the reasoning for why allocation requires a covering principal (O5). The fix is adding the symmetric closure property for addresses, which is derivable from the existing design intent stated in the ASN.
