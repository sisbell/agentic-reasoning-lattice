# Channel Assignment — ASN-0132 review-21

**Date:** 2026-06-13 12:11

## Issue 1: The independence-from-enumeration point is stated twice
Reason: Pure editorial consolidation — the fix trims a preview clause and lets CN-ENUM carry the "both bottom out at sat" point once. The substantive content to retain (sat and addressable are reused from ASN-0121) is already cited in the ASN, so no design intent or implementation evidence is required.

## Issue 2: Defensive well-definedness prose and a forward-duplicated cost parenthetical
Reason: Both actions are internal to the ASN — deleting the "no loop / no bound function" sentence leaves the existing finiteness argument (subset of finite `dom(Σ.L)`, FL-DEC decidability) intact, and the cost parenthetical merely relocates to the closing cost discussion, where the same value-vs-cost claim about the back end already appears. No new evidence about the implementation is needed since the realisation's full-enumeration-cost claim is already stated and unchanged by the move.
