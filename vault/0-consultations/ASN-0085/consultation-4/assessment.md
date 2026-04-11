# Revision Categorization — ASN-0085 review-4

**Date:** 2026-04-11 01:38



## Issue 1: OrdAddHom proof omits well-definedness check for the RHS application of TumblerAdd
Category: INTERNAL
Reason: The fix is explicitly spelled out in the review — insert a one-line precondition check using `actionPoint(w_ord) = k − 1` and `#ord(v) = m − 1`, both already established in the ASN's own postconditions.

## Issue 2: Subspace preservation is established in the proof but never stated as a formal postcondition
Category: INTERNAL
Reason: The proof already derives `r₁ = v₁` (i.e. `subspace(v ⊕ w) = subspace(v)`) from TumblerAdd, and the inverse property `vpos(subspace(v), ord(v)) = v` is already a postcondition of vpos. Promoting these to a formal property and deriving the full decomposition corollary requires only reorganizing material already present in the ASN.
