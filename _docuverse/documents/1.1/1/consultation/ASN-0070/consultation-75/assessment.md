# Channel Assignment — ASN-0070 review-75

**Date:** 2026-06-03 03:36

## Issue 1: Forward-reference justification embedded in a definition
Reason: Purely editorial—deleting the parenthetical removes meta-prose from a DEF slot, and the justification it gestures at (F-canonical Step 1) already exists in the ASN. No design intent or implementation evidence is required.

## Issue 2: F-det attributes V-restricted uniqueness to S9, which governs full-T denotation
Reason: The correct citation chain (F-canonical Step 4's "Bridge" recovering `(s_j, c_j)` from `⟦σ_j⟧_V`) is already proven within this ASN; the fix is to re-point F-det's step 4 at that bridge instead of S9 directly. Fully derivable internally.
