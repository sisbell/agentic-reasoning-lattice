# Channel Assignment — ASN-0084 review-87

**Date:** 2026-05-30 18:12

## Issue 1: Worked Example 1 merge check misstates the disqualifying condition
Reason: Purely editorial correction derivable from the ASN's own Merge definition (V-adjacency = v₂ = v₁ + n₁) and the parenthetical's own "5 ✓ for V-adjacency" marker; no design intent or implementation evidence needed.

## Issue 2: EXT-VAC asserts `c₀ ≤ [S, N+1]` without justification
Reason: The missing step is supplied entirely by the ASN's own Width positivity result (w_α ≥ 1 forces ord(c₀) ≤ N), already established just above EXT-VAC; the fix is internal.

## Issue 3: R-BLK Phase 3 restates the R-COMM→contiguity argument in three overlapping passages
Reason: Pure prose deduplication — collapsing three restatements of the same R-COMM-derived inference into one — with no semantic question about intent or implementation behavior.
