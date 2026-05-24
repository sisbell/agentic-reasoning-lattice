# Revision Categorization — ASN-0051 review-16

**Date:** 2026-03-23 01:57

## Issue 1: SV11 block decomposition scope in the two-subspace model
Category: INTERNAL
Reason: The fix requires choosing between two options (restrict B to content-subspace, or justify reading v₁ ≥ 1 as v₁ = s_C), both derivable from existing definitions in ASN-0058 (B1, M12) and ASN-0047 (two-subspace model, SC-NEQ). No design intent or implementation evidence needed.

## Issue 2: SV7 conflates discovery mechanism with valid composite construction
Category: INTERNAL
Reason: The review itself states the fix: add a sentence noting J1★ (ASN-0047) may require K.ρ in a valid composite, but K.ρ modifies R not L or M, so discovery is unaffected. All relevant definitions (J1★, discover_s, K.ρ's frame) are already present in the ASNs.

## Issue 3: SV11 fragment overlap under within-document sharing
Category: INTERNAL
Reason: The clarification that fragments form a cover rather than a partition follows directly from S5 (UnrestrictedSharing permits non-injective M(d)) and the set-union formula already stated in SV11. The fix is a mathematical observation about existing definitions, not a design or implementation question.
