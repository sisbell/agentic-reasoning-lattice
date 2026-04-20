# Revision Categorization — ASN-0034 review-6

**Date:** 2026-03-13 09:43



## Issue 1: TA5 preservation of T4 — structural constraint omitted
Category: INTERNAL
Reason: The fix is purely logical — the adjacent-zeros constraint follows from T4's definition already present in the ASN. The correct bound (k ≤ 2) is derivable from the existing definitions of inc and T4 without any external evidence.

## Issue 2: TA3 proof Case 0 — false intermediate claim and missing sub-case
Category: INTERNAL
Reason: This is a proof repair issue. The zero-padding divergence logic and the missing sub-case are both derivable from the constructive definition of subtraction already in the ASN. No design intent or implementation evidence is needed.

## Issue 3: Partition Monotonicity theorem — statement does not capture what the proof establishes
Category: INTERNAL
Reason: The proof already establishes the cross-allocator ordering via the Prefix Ordering Extension lemma. The fix is to align the theorem statement with what the proof proves — all content is already present in the ASN.
