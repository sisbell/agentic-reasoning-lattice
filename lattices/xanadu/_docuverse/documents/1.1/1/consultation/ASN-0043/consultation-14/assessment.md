# Revision Categorization — ASN-0043 review-14

**Date:** 2026-03-22 22:50



## Issue 1: GlobalUniqueness proof — missing the comparable-prefix case
Category: INTERNAL
Reason: The fix is fully specified in the review itself — add the third case using T10a, TA5, and T3, all of which are already established in ASN-0034. No external evidence needed.

## Issue 2: L12 prose contradicts the formal model on link arrangement
Category: GREGORY
Reason: The formal model excludes links from arrangements (S3 + L0), but the prose references "Vstream removal" as the deletion mechanism. Whether links have any Vstream/arrangement presence in the implementation — and if so, how deletion works — requires checking the udanax-green code.
Gregory question: In udanax-green, do links have entries in the document's Vstream/permutation matrix, and if so, how does link deletion (or hiding) work mechanically — is it Vstream removal, granfilade marking, or something else?
