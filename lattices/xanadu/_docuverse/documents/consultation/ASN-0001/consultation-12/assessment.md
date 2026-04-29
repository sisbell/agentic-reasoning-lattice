# Revision Categorization — ASN-0001 review-12

**Date:** 2026-03-01 19:44

## Issue 1: TA3 is falsified by a counterexample involving prefix-related operands with zero-padding
Category: INTERNAL
Reason: The counterexample is constructed entirely from the ASN's own constructive definition of ⊖ and zero-padding. The fix (weakening to ≤, adding a same-length precondition, or restructuring the strict/weak split) is derivable from the existing definitions without external evidence.

## Issue 2: TA3 proof Case 0 contains an incorrect intermediate claim
Category: INTERNAL
Reason: The error is in a proof step that overstates which positions the subtraction results agree on. The correct reasoning follows from the ASN's own subtraction definition and zero-padding rules — no design intent or implementation evidence is needed.

## Issue 3: TA3 proof omits the case a = w
Category: INTERNAL
Reason: The missing case is handled by the ASN's own subtraction definition (equal operands produce the zero tumbler) and TA6 (zero tumblers are less than positive tumblers). The one-sentence argument is already sketched in the review finding itself.
