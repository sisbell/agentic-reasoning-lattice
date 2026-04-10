# Revision Categorization — ASN-0082 review-13

**Date:** 2026-04-09 19:08

## Issue 1: Arrangement invariants violated by the shift are not documented
Category: INTERNAL
Reason: The violations (D-CTG, D-MIN, D-SEQ) are directly derivable from the ASN's own worked example and the definitions in ASN-0036. The fix is editorial: explicitly list which invariants break and add them to the forward-looking note already present in the gap-region paragraph.

## Issue 2: I3-VD establishes S8-depth only for subspace S
Category: INTERNAL
Reason: The missing cross-subspace argument follows immediately from I3-CX (already stated in the ASN) and S8-depth on the pre-state (already cited). The one-sentence derivation is fillable from existing clauses without external evidence.

## Issue 3: I3-C attribution overstates what S9 provides
Category: INTERNAL
Reason: The distinction between S9's preservation direction and the reverse inclusion is a logical observation derivable from S9's definition in ASN-0036 and the ASN's own characterization of the shift as arrangement-only. The fix is correcting the attribution sentence, not resolving a design or implementation question.
