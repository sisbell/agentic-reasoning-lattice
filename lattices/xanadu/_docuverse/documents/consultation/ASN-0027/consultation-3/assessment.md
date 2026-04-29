# Revision Categorization — ASN-0027 review-3

**Date:** 2026-03-10 10:30

## Issue 1: Invariant preservation unverified for A3, A4, A5
Category: INTERNAL
Reason: All ingredients are present in the ASN. P2, the I-space frame, range preservation (A3), identity clause (A4), and identity mapping (A5) are already stated — the derivations are short chains through existing definitions.

## Issue 2: Cross-document frame missing from A4 and A5
Category: INTERNAL
Reason: A2 and A3 already establish the cross-document frame pattern. The fix is adding analogous clauses to A4 and A5 following the same template, requiring no external evidence.

## Issue 3: A3 swap bijection asserted without verification
Category: INTERNAL
Reason: The segment offset formulas are fully stated in A3. The verification is algebraic — computing image ranges from the given formulas and confirming they partition `[c_1, c_4)`. No design intent or implementation evidence needed.

## Issue 4: A8(iii) redundant with (i) and (ii)
Category: INTERNAL
Reason: The redundancy is visible from the ASN's own definitions. The three-layer separation (validity, immutability, accessibility) is already developed in the opening section and provides the vocabulary to either drop (iii) or sharpen it into the I-space/V-space distinction.
