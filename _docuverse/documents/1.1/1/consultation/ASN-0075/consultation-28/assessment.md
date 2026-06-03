# Channel Assignment — ASN-0075 review-28

**Date:** 2026-06-03 00:33

## Issue 1: Supplementary lemma proves only one of two conjuncts per address group
Reason: The fix is derivable from the ASN alone — the missing half follows from R-disjointness plus the DELETED definition already stated, requiring no design intent or implementation evidence.

## Issue 2: Output-half disjointness over-cites D-EXH
Reason: The fix is internal — the disjointness follows directly from the contradictory range-membership conditions (`a ∈ ran(M(d_B))` vs `a ∉ ran(M(d_B))`) in the ASN's own definitions; no channel needed.
