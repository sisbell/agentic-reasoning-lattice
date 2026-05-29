# Channel Assignment — ASN-0036 review-126

**Date:** 2026-05-28 22:31

## Issue 1: S8 image-structure-preservation corollary is orphaned from the theorem it sits in
Reason: Purely structural relocation of an existing corollary; the ASN already states the corollary is just ShiftPreservation composed with S3 and independent of run cardinality. No design intent or implementation evidence is needed.

## Issue 2: "Why the axiom is needed" prose inside Depends fields
Reason: Editorial trim of justification prose to a bare dependency relation; both T10a.4's bound and S7b's strengthening are already present in the ASN. Internal.

## Issue 3: D-CTG-depth non-triviality bound explained twice in different words
Reason: Deduplication of two paragraphs saying the same thing about the `m ≥ 3` precondition; both texts are already in the ASN. Internal.

## Issue 4: S8a proof is meta-commentary on what counts as a derivation
Reason: Collapse of narration to the one load-bearing derivation step, which is already stated (positivity from `zeros(v) = 0` + T0/NAT-discrete). Internal.

## Issue 5: ShiftPreservation conclusion (i) over-narrates "nonzero ⇒ ≥ 1"
Reason: Factoring a repeated elementary ℕ fact into a single named sub-lemma cited thereafter; the underlying axioms (T0, NAT-discrete) are already in use. Internal.
