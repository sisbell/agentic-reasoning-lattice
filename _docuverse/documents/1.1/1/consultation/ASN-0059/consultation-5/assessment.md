# Revision Categorization — ASN-0059 review-5

**Date:** 2026-03-20 22:54



## Issue 1: I10 B2 verification — within-group disjointness omitted
Category: INTERNAL
Reason: The fix requires adding two sentences deriving within-group disjointness from B2 (already established in ASN-0058) and I7 (established in this ASN). All needed properties are present in the document.

## Issue 2: TA-strict cited for ordinal increment
Category: INTERNAL
Reason: The fix is a citation correction — replacing TA-strict with TA5(a), both defined in ASN-0034. The correct property is already available; only the reference needs updating.

## Issue 3: VContiguity quantifies over invalid and unbounded intermediate positions
Category: INTERNAL
Reason: The fix is adding a clarifying note about the definition's scope at depth ≥ 3, which follows from the interaction of lexicographic ordering (T1, ASN-0034) with S8-fin. No external design intent or implementation evidence is needed — the mathematical observation is self-contained.
