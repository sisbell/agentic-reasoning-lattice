# Revision Categorization — ASN-0043 review-40

**Date:** 2026-04-09 15:15



## Issue 1: Home derivation cites GlobalUniqueness where document identity suffices
Category: INTERNAL
Reason: The fix replaces an incorrect derivation chain with a correct one using T3 (CanonicalRepresentation) and L1a, both already present in the ASN. No external design intent or implementation evidence is needed.

## Issue 2: L1c absent from L9 and L11b invariant checklists
Category: INTERNAL
Reason: L1c is already defined in the ASN, and the required verification text follows mechanically from the allocation patterns already described in each proof. The fix is adding explicit checklist entries with justifications derivable from existing definitions.
