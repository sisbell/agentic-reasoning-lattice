# Channel Assignment — ASN-0040 review-32

**Date:** 2026-05-11 12:30

## Issue 1: TA5 citation error in three places
Reason: The fix is a citation correction internal to the ASN — substitute TA5's unlabeled `t' ∈ T` postcondition (from ASN-0034) for the fabricated "positivity precondition" of TA5(c). All needed material is in TA5's contract; neither design intent nor implementation evidence bears on the fix.

## Issue 2: Concrete trace omits d = 1 baptism
Reason: The fix is mechanical application of axioms already present — pick a same-level parent, apply `inc(p, 1)` via TA5(d), verify B5/B6/B1 against the result. The trace pattern from the existing d = 2 steps transfers directly, and Nelson's "Items 2.1, 2.2, 2.3, 2.4" passage already cited in the ASN documents d = 1 intent.
