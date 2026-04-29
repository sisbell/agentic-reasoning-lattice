# Revision Categorization — ASN-0040 review-3

**Date:** 2026-03-15 13:07

## Issue 1: wp formulas omit serialization assumption
Category: INTERNAL
Reason: The ASN already identifies the B4 dependency in prose two paragraphs after the wp formulas. The fix is restructuring the formal presentation — annotating formulas with their assumptions or separating state preconditions from environmental constraints — using content already present.

## Issue 2: B0a uses undefined "valid"
Category: INTERNAL
Reason: B6 defines valid depth later in the same ASN. The fix is adding an explicit forward reference to B6 at the point of B0a's definition and stating the deliberate deferral of the parent-in-B question, both of which are already addressed in the ASN's own content.

## Issue 3: B1 induction covers only the inbound direction
Category: INTERNAL
Reason: The outbound direction follows immediately from B7's symmetry, which is already established in the ASN. The fix is adding one sentence making the bidirectional consequence explicit — no external evidence needed.

## Issue 4: B9 is informally stated
Category: INTERNAL
Reason: The mathematical content needed to formalize B9 as a reachability claim — T0(a), B1, and the sibling stream structure — is all present in the ASN. The fix is replacing the informal "the system permits" with a precise statement using existing definitions.
