# Revision Categorization — ASN-0040 review-6

**Date:** 2026-03-15 13:51

## Issue 1: No consolidated formal definition of the baptize operation
Category: INTERNAL
Reason: All components (preconditions in B6, postcondition in wp section, frame implicit in B0/B0a) are already present in the ASN. The fix is reorganization — consolidating scattered pieces into a formal definition block and reordering the presentation.

## Issue 2: B4 dependency missing from B1 induction and B8 proof
Category: INTERNAL
Reason: B4 is already defined and the wp section already correctly identifies it as a dependency. The fix is adding explicit citations of B4 in the B1 proof and B8 proof, which reference only material already in the ASN.

## Issue 3: B5a precondition not discharged for stream elements
Category: INTERNAL
Reason: The review itself supplies the complete argument from facts already stated in the ASN (TA5(d) gives final component 1, TA5(c) preserves positivity). The fix is a two-sentence inductive discharge using existing definitions.

## Issue 4: Trace does not verify B₀ conformance
Category: INTERNAL
Reason: The verification uses only definitions already in the ASN — no sibling stream contains [1], children is empty for all (p,d), and [1] satisfies T4. The fix is stating explicitly what the review already derives from present material.
