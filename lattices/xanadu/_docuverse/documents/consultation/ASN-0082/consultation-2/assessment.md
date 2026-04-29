# Revision Categorization — ASN-0082 review-2

**Date:** 2026-04-09 14:43

## Issue 1: Subspace preservation argument depends on unestablished depth equality between p and V-positions
Category: INTERNAL
Reason: The gap is a missing precondition (#p equals uniform depth of V-positions in the subspace). The fix — adding this precondition — is derivable from the definitions of VD, OrdinalShift, and the v ≥ p comparison already present in the ASN.

## Issue 2: VD's informal justification overstates T10a.1
Category: GREGORY
Reason: Whether child-spawning occurs within a subspace's element field is an implementation fact about the udanax-green allocator. If child allocators are used, VD itself could be false, not just its justification.
Gregory question: Within a single subspace's element field, does the udanax-green allocator ever spawn child allocators (inc(·, k') for k' > 0), or is allocation always flat sibling production?

## Issue 3: VP cited for insertion point p, which is not a V-position
Category: INTERNAL
Reason: The fix is dropping an incorrect citation and restating S ≥ 1 as a direct precondition. The ASN's own definitions make clear that VP applies only to v ∈ dom(M(d)), not to the insertion point.

## Issue 4: Worked example omits mandatory boundary cases
Category: INTERNAL
Reason: The boundary cases (insert at start, insert past end, empty document) are mechanical verifications using the definitions of I3, I3-L, and shift already in the ASN. No external evidence needed.

## Issue 5: Positivity attribution conflates VP and T4
Category: INTERNAL
Reason: Both T4 and VP are already cited in the ASN. The fix is correcting which property justifies which positivity claim — a straightforward attribution correction derivable from the stated definitions.
