# Revision Categorization — ASN-0036 review-35

**Date:** 2026-03-28 08:04



## Issue 1: S8 property table omits T3 as a dependency
Category: INTERNAL
Reason: T3 (CanonicalRepresentation) is already established in ASN-0034 and the proof's reliance on it is clear from the existing reasoning — adding it to the dependency list is a mechanical correction derivable from the ASN's own content.

## Issue 2: S8 dependency should cite TA5, not just TA5(c)
Category: INTERNAL
Reason: Both TA5(a) and TA5(c) are established properties in ASN-0034, and the proof's use of TA5(a) for strict inequality is evident from the existing interval construction — broadening the citation is a mechanical correction.
