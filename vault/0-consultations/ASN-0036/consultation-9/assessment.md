# Revision Categorization — ASN-0036 review-9

**Date:** 2026-03-14 17:59



## Issue 1: S8a formal quantifier contradicts acknowledged scope
Category: INTERNAL
Reason: The fix is purely notational — restricting the quantifier's range to text-subspace V-positions. All needed definitions (subspace identifier, zeros function) are already present in the ASN.

## Issue 2: S5 within-document witness omits S0 and S1
Category: INTERNAL
Reason: The cross-document witness already contains the exact sentence needed ("S0 is vacuous — single state, no transition to check"). The fix is adding the same vacuity note to the within-document case.

## Issue 3: S8 properties table omits foundation dependencies
Category: INTERNAL
Reason: The S8 proof body already names T5, PrefixOrderingExtension, TA5(c), and TA7a explicitly. The fix is copying those references into the summary table entry.
