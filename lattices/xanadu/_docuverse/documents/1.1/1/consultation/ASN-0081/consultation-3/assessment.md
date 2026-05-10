# Revision Categorization — ASN-0081 review-3

**Date:** 2026-04-09 19:11



## Issue 1: Invariant proofs have uncovered case when L = ∅ and R = ∅
Category: INTERNAL
Reason: The fix adds vacuous-truth cases to existing proofs using only definitions and logic already present in the ASN. No design intent or implementation evidence is needed — the empty-set cases follow directly from the formal definitions of L, R, Q₃, and the stated preconditions.

## Issue 2: Missing S8-depth-post and S8a-post invariant preservation
Category: INTERNAL
Reason: The required lemmas follow entirely from the ASN's own definitions (vpos, ord, σ), the cited ASN-0036 invariants (S8-depth, S8a), and the already-stated frame conditions (D-L, D-CS). The D-SHIFT section already contains the informal argument for S8a; promoting it to a formal lemma requires no external evidence.

## Issue 3: Missing R = ∅ boundary worked example
Category: INTERNAL
Reason: The worked examples are mechanical instantiations of the ASN's own definitions and postconditions with specific numeric values. The R = ∅ and full-deletion cases require no design intent or implementation evidence — they follow from the same contraction setup and shift definitions already specified.
