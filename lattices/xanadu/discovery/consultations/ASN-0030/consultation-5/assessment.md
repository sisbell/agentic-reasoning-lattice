# Revision Categorization — ASN-0030 review-5

**Date:** 2026-03-12 00:53

## Issue 1: A3 terminology collision with formal definition of `reachable`
Category: INTERNAL
Reason: Pure terminology fix within the ASN's own content — replacing an informal use of "reachable" with "achievable" to avoid collision with the formally defined predicate. No external evidence needed.

## Issue 2: A4, A4a, A5 omit document-set frame condition
Category: INTERNAL
Reason: Adding `Σ'.D = Σ.D` as a frame condition is derivable from the ASN's own specification intent and D2 (DocumentPermanence, ASN-0029). The fix is a completeness issue in the formal statement, not a question about design intent or implementation behavior.
