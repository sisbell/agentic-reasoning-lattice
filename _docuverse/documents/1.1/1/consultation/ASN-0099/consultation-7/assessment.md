# Revision Categorization — ASN-0079 review-7

**Date:** 2026-03-23 03:28

## Issue 1: Resolution "total count" claim is incorrect under self-transclusion
Category: INTERNAL
Reason: The fix is a precision correction derivable from existing definitions — C2 gives sum of run widths, and the addresses set union loses duplicates under non-injective M(d). The corrected statement is fully specified in the review.

## Issue 2: "Disjoint I-address ranges" claim is not guaranteed
Category: INTERNAL
Reason: The counterexample (same-origin self-transclusion) and the fix (qualify with "from different origins" per S4, or remove) are both derivable from existing properties. F1a already handles non-disjoint unions, so no downstream changes are needed.

## Issue 3: F19 cost model is imprecise
Category: INTERNAL
Reason: Nelson's quoted constraint is unambiguous — non-satisfying links must not impede search. The current formalization conflates output cost with overhead; the fix is a standard complexity-theoretic decomposition of the already-cited design intent. No external evidence is needed.
