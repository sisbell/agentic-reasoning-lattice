# Revision Categorization — ASN-0035 review-9

**Date:** 2026-03-14 21:03



## Issue 1: N8 verification claims "all" but enumerates 8 of 16 properties
Category: INTERNAL
Reason: The fix is adding a sentence listing the remaining properties and noting they don't depend on mutable state. All information needed is already present in the ASN.

## Issue 2: Precondition exactness argument — mechanism claim imprecise for the C ≠ ∅ case
Category: INTERNAL
Reason: The fix is splitting the existing argument into two cases using TA5(c) and TA5(d), both of which are already defined and referenced in the ASN. No external evidence needed.
