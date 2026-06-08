# Channel Assignment — ASN-0107 review-24

**Date:** 2026-06-08 12:09

## Issue 1: R3 conflates per-slot survival with whole-link counting
Reason: Internal. The fix follows from the ASN's own `sat` definition (conjunctive across all three slots): R3 needs either the single-slot guard already used in R1/R2 (P-slot/P-slot₂) or restatement as a claim about slot-`i`'s contribution to satisfaction. No design intent or implementation evidence is required.

## Issue 2: R2's parenthetical imagines an excluded case and forward-defers to R6, which does not treat it
Reason: Internal. Deleting the parenthetical or replacing it with an honest scope note is a prose correction grounded in what R6 actually delivers (a per-link weakest precondition, not a count-level Δ) — fully visible within the ASN.

## Issue 3: R1 / R2 / R6 mutual cross-referencing accretion
Reason: Internal. Choosing R6 as the anchor and deriving R1 as its `k=1` corollary, then dropping reciprocal pointers, is a structural reorganisation of claims already present in the ASN; no external channel informs the hierarchy.
