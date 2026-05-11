# Channel Assignment — ASN-0040 review-23

**Date:** 2026-05-11 10:08

## Issue 1: B6 necessity case classification leaves p = [0] uncovered
Reason: The fix is a structural reclassification of the proof's case partition. The propagation substance (TA5(b) preservation, sig(c₁) = 2 invariance) is already in the ASN; only the case boundaries need adjustment to exhaustively cover #p = 1 with p₁ = 0.

## Issue 2: B0 is logically redundant given B0a, but the implication is unstated
Reason: The fix is an internal annotation. The ASN already states why B0 is presented separately (proof legibility, independence from T8); only the B0a ⟹ B0 derivation needs to be made explicit.

## Issue 3: Cross-ASN bridge axioms to allocated(Σ) are stated as prose, not labelled forward requirements
Reason: The fix is a formalization restructuring. B3 already provides the labelled-forward-requirement template, and the bridge content is fully specified in the prose; only the labelling and explicit quantification need to be added.
