# Channel Assignment — ASN-0115 review-14

**Date:** 2026-06-05 07:12

## Issue 1: The "deeper positions are T1-interior" justification in R6 is false for extensions past the active frontier
Reason: The fix is internal — the correct reason is already present in the ASN (S8-depth: every subspace-`S` active position has depth exactly `m_S`, so any depth-`>m_S` named position is absent from `dom(Σ.M(d))` and filtered from `act`). T1 ordering facts (case (ii): proper extensions are strictly greater) are also stated in the ASN. No design intent or implementation evidence is needed; only the false bracketing/interiority prose must be removed and replaced by the depth argument already on hand.
