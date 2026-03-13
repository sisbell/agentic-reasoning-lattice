# Revision Categorization — ASN-0034 review-2

**Date:** 2026-03-13 07:10



## Issue 1: T4 does not explicitly require non-empty fields
Category: INTERNAL
Reason: The fix is adding a syntactic constraint (no adjacent zeros, no leading/trailing zeros) that is derivable from the existing design intent already stated in T4's prose and examples. No external evidence needed.

## Issue 2: T12 omits the TA0 precondition
Category: INTERNAL
Reason: The missing precondition (action point k ≤ #s) is already stated in TA0; T12 simply needs to inherit it explicitly. The fix is purely internal cross-referencing.

## Issue 3: Worked example states a false set equality
Category: INTERNAL
Reason: The ASN itself distinguishes span-as-range from span-as-population elsewhere ("A span that contains nothing today may at a later time contain a million documents"). The fix is correcting the worked example to use language consistent with definitions already present in the ASN.

## Issue 4: TA3 verification, Case 0 has two gaps
Category: INTERNAL
Reason: Both gaps are proof-internal: (a) the a = w sub-case is trivially resolved from existing definitions, and (b) the lexicographic argument replaces an incorrect inference pattern using only T1, which is already stated. No external evidence needed.

## Issue 5: Reverse inverse proof omits a precondition check
Category: INTERNAL
Reason: The missing check (y ⊕ w ≥ w) follows from the constructive definition of ⊕ already given in the ASN — if yₖ > 0 then (y ⊕ w)ₖ = yₖ + wₖ > wₖ. Purely internal reasoning.
