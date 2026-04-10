# Revision Categorization — ASN-0081 review-6

**Date:** 2026-04-09 19:55



## Issue 1: D-BJ postcondition does not formally state the bijectivity it claims
Category: INTERNAL
Reason: The fix is purely structural — promoting prose-derived properties (injectivity from order-preservation, surjectivity from Q₃'s definition) into the formal postcondition. All needed reasoning is already present in the ASN.

## Issue 2: OrdinalExtraction and VPositionReconstruction definitions missing preconditions
Category: INTERNAL
Reason: The preconditions (#v ≥ 2 for ord, #o ≥ 1 and S ≥ 1 for vpos) follow directly from T0's length requirement and the definitions themselves. No external design intent or implementation evidence is needed.
