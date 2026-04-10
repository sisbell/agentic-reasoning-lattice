# Revision Categorization — ASN-0084 review-12

**Date:** 2026-04-10 11:55

## Issue 1: R-DISP proof is incomplete — five region cases hand-waved
Category: INTERNAL
Reason: The fix requires expanding algebraic computations using formulas already present in R-PPERM and R-SPERM within this ASN. No external design intent or implementation evidence is needed.

## Issue 2: Range-preservation argument attributes "exactly one" to surjectivity alone
Category: INTERNAL
Reason: The fix is a single word change ("surjective" → "bijection") using the bijectivity already established in the preceding sentence of the same paragraph.
