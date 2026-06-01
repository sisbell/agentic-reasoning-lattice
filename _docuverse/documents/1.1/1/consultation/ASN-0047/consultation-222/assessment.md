# Channel Assignment — ASN-0047 review-222

**Date:** 2026-06-01 06:17

## Issue 1: S8★ mislabels and internally contradicts ASN-0036's S8 conditions
Reason: The fix is a relabeling task against ASN-0036's own formal S8 statement, which is a prior spec ASN; the review itself already supplies the correct condition labels (a)=lockstep, (b)=label well-definedness, (c)=uniqueness. Neither design intent (Nelson) nor implementation evidence (Gregory) bears on matching foundation labels — the fix is derivable from the ASN and its cited foundation.

## Issue 2: Redundant pointer table — "Derived structural identities"
Reason: This is a purely editorial deduplication — removing a standalone table whose statements and derivations both back-point to the inline K.δ case (ii) catalogue. No design or implementation input is required.
