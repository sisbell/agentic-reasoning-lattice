# Revision Categorization — ASN-0053 review-8

**Date:** 2026-03-19 06:44



## Issue 1: LeftCancellation proof omits the length-equality step required by T3
Category: INTERNAL
Reason: The fix requires inserting a derivation using T3 and TumblerAdd's result-length formula, both defined in ASN-0034 and already referenced in this ASN. All necessary definitions are present.

## Issue 2: S5 associativity well-definedness is asserted, not verified
Category: INTERNAL
Reason: The fix requires expanding the parenthetical into explicit sub-cases using positivity of d and d' (established in S4's proof) and the action-point bound from TA0. All definitions and prerequisites are already present in ASN-0053 and ASN-0034.
