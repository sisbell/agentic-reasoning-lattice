# Revision Categorization — ASN-0065 review-7

**Date:** 2026-03-21 23:00

## Issue 1: P4 preservation not derived
Category: INTERNAL
Reason: The fix requires deriving P4 preservation from R-CP, R-XD, and J3 — all of which are already established within the ASN. The three-step chain (Contains(Σ') = Contains(Σ) ⊆ R = R') uses only definitions and results present in the document.

## Issue 2: Incorrect position labels in composition discussion
Category: INTERNAL
Reason: The fix is a straightforward correction of interval arithmetic using the pivot postcondition (R-P1, R-P2) already defined in the ASN. The correct positions [c₀, c₀ + w_μ) and [c₀ + w_μ, c₂) follow directly from the existing definitions.
