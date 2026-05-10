# Revision Categorization — ASN-0067 review-2

**Date:** 2026-03-21 16:29

## Issue 1: C3 claims "every foundational invariant" but the proof omits three
Category: INTERNAL
Reason: P4a, P5, and P3 are all defined in ASN-0047; the review itself notes each verification is trivial and one-sentence. The fix is derivable entirely from existing definitions.

## Issue 2: C12a text–formula mismatch
Category: INTERNAL
Reason: The text says "runs" (k) but the formula gives total width (Σnⱼ). This is an internal inconsistency between two parts of the same lemma statement — aligning them requires no external evidence.

## Issue 3: Elementary Decomposition uses K.μ~ as if elementary
Category: INTERNAL
Reason: K.μ~ is defined as a composite in ASN-0047. Unfolding it into K.μ⁻ + K.μ⁺ and verifying the K.μ⁻ precondition requires only the definitions already present in ASN-0047.

## Issue 4: ContentReference does not require level-uniform V-spans
Category: INTERNAL
Reason: The constraint #ℓ = m follows from the existing framework — S8-depth requires fixed-depth V-positions, and the span algebra (ASN-0053) is developed for level-uniform spans. Adding the requirement is derivable from properties already stated.

## Issue 5: Five-step construction omits non-text-subspace frame
Category: INTERNAL
Reason: The elementary decomposition already in the ASN shows link-subspace positions (v₁ = 0) are below the text-subspace insertion point and map to themselves under K.μ~. The fix is stating explicitly what the decomposition already implies.

## Issue 6: ValidInsertionPosition depth underdetermined for empty documents
Category: INTERNAL
Reason: That m = #v follows from the parameter list. That the first operation establishes permanent depth follows from S8-depth (ASN-0036). Both are derivable from existing definitions — no design intent or implementation evidence needed.
