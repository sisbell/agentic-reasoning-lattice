# Revision Categorization — ASN-0036 review-5

**Date:** 2026-03-14 16:56



## Issue 1: S8 partition uniqueness depends on S8-depth but this dependency is unstated
Category: INTERNAL
Reason: The fix requires adding a uniqueness argument to the existing proof and updating the properties table — all information needed (S8-depth, T1 prefix extension, the interval structure) is already present in the ASN.

## Issue 2: S7 omits GlobalUniqueness from stated dependencies
Category: INTERNAL
Reason: The prose already cites GlobalUniqueness as the basis for uniqueness; the fix is adding it to the properties table entry — a mechanical correction from the ASN's own content.
