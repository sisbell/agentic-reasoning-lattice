# Revision Categorization — ASN-0058 review-9

**Date:** 2026-03-22 20:27



## Issue 1: M4 cites TA5 instead of TA0/OrdinalShift
Category: INTERNAL
Reason: The fix is purely a citation correction — the ASN already defines OrdinalShift and uses TA0 elsewhere. The correct references (TA0, OrdinalShift) are present in ASN-0034 and the reasoning is already established in this ASN's own definitions.

## Issue 2: M7 necessity argument attributes violation to M1 instead of B3
Category: INTERNAL
Reason: The fix replaces one already-defined property label (M1) with another (B3), both defined within this ASN. The correct reasoning — that the merged block would be inconsistent with M(d) at the boundary position — follows directly from B3's definition stated earlier in the same document.
