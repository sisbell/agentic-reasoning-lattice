# Revision Categorization — ASN-0025 review-7

**Date:** 2026-03-07 12:02

## Issue 1: REARRANGE link-subspace frame relies on unestablished cross-subspace ordering
Category: INTERNAL
Reason: The fix is to add an explicit link-subspace frame postcondition matching INSERT and DELETE, which already provide the pattern. All needed definitions and conventions are present in the ASN.

## Issue 2: REARRANGE interior postconditions under-determined
Category: INTERNAL
Reason: The prose already describes 3-cut rotation and 4-cut swap semantics, and Gregory evidence for displacement arithmetic is already included. The author can either formalize zone-level postconditions from existing content or explicitly state the constraint-level choice is deliberate.

## Issue 3: V-space contiguity invariant unstated
Category: INTERNAL
Reason: The invariant is implicit in the definitions of `next(d, Σ)`, `next_link(d, Σ)`, and the shift postconditions of all seven operations already defined in the ASN. Stating and verifying it requires only the existing operation specifications.

## Issue 4: P6 status ambiguous between constraint and theorem
Category: NELSON
Reason: Whether P6 is a universal constraint (documents are irremovable by design) or merely a theorem about the current seven operations depends on whether Nelson intended document permanence as a system guarantee alongside content permanence.
Nelson question: Did you intend document permanence — that a document, once created, can never be removed from the system — as a design requirement on par with content permanence, or is it merely a consequence of the operations you defined?
