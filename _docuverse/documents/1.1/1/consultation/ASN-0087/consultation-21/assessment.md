# Channel Assignment — ASN-0087 review-21

**Date:** 2026-06-03 14:50

## Issue 1: wp omits MAKELINK's own enabledness, diverging from the foundation's wp convention
Reason: Internal. The ASN already states MAKELINK's full enabledness precondition (`d ∈ dom(M)`, `N ≥ 3`, `eᵢ ∈ Endset`, `e₃ ≠ ∅`) in the Preconditions section and cites LP12a's `enabled(…) ∧ …` convention; conjoining `enabled(MAKELINK)` into both wp expressions (or relabeling as wlp) is derivable from material already present.

## Issue 2: M-DepthConv's universal claim is in unresolved tension with the "regardless of its value" hedge
Reason: Resolving universality requires confirming that no substrate operation other than MAKELINK's `K.μ⁺_L` seeds a first link-subspace V-position (the J4/ForkComposite "content-subspace only" claim must be verified against the actual operations) — this is implementation evidence Gregory holds.
Gregory question: In udanax-green, does any operation other than the makelink path (`findnextlinkvsa`/`K.μ⁺_L`) ever create a document's first link-subspace V-position, and does fork copy any link-subspace V-positions — i.e., can a first link ever be placed at a depth other than 2?
