# Channel Assignment — ASN-0127 review-2

**Date:** 2026-06-09 23:53

## Issue 1: F-UDIST's consequences are neither derived nor connected to the note's own use sites
Reason: Both required additions are pure algebra over machinery already in the note — the I-monotonicity corollary follows by writing `findlinks(I) = findlinks(I') ∪ findlinks(I ∖ I')` via F-UDIST, and `findlinks_V` distributivity follows from forward-image-of-union (immediate from F-IMG) composed with F-UDIST. No design intent or implementation evidence is consulted.

## Issue 2: F-IMG-SWING's "gain, lose" cases are claimed but only "change membership" is justified
Reason: The fix is internal — the cardinality argument (a bijection on a fixed domain preserves preimage cardinality, so gain/lose requires non-injective `Σ.M(d)`) is elementary, and content sharing (M13/M14, ASN-0058) is already cited in the note as the source of non-injectivity, with the review supplying the concrete shared-content witness.

## Issue 3: "K.λ is the unique single-step source of change in the result" is unqualified and clashes with the note's own findlinks_V framing
Reason: The fix is a scoping correction using distinctions the note already draws — F-INERT/F-LAMBDA range over fixed-`I` `findlinks`, and D-NONMONO already establishes that other transitions move the discovery-anchored result — so qualifying the summary sentence to the existence-anchored object is derivable from the ASN's own content.
