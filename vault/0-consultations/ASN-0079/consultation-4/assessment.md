# Revision Categorization — ASN-0079 review-4

**Date:** 2026-03-23 01:56

## Issue 1: F0 — Derivation through wrong foundation
Category: INTERNAL
Reason: The fix replaces an incorrect citation (S9) with the correct derivation through ASN-0058's resolution definitions (C1a, B3). All required properties are already defined in referenced ASNs.

## Issue 2: F8 — Statement ambiguous about home constraint; proof omits three conjuncts
Category: INTERNAL
Reason: The fix explicitly states H = ⊤ and Sⱼ = ⊤ for j ≠ i, then notes the trivially satisfied conjuncts. All definitions (F1, sat, home constraint) are already present in this ASN.

## Issue 3: F18 — Imprecise citation for dom(L) membership
Category: INTERNAL
Reason: L12 is already cited in the same proof for value preservation; the fix extends the same citation to cover domain membership preservation, eliminating the incorrect T8 reference.

## Issue 4: F19 — Ambiguous complexity phrasing
Category: INTERNAL
Reason: The fix separates two already-stated claims (sublinear requirement vs. tree-based indexing observation) into distinct sentences. No new information is needed — only clearer phrasing of content already present.
