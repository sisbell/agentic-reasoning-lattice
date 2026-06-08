# Channel Assignment — ASN-0110 review-8

**Date:** 2026-06-08 01:11

## Issue 1: Deduplication key in `Eᵢ` left implicit — value or coverage?
Reason: Derivable from the ASN alone. RE-result already defines `Eᵢ` as a set of stored endset *values* `{Σ.L(a).eᵢ : …}`, and RE-full fixes that values are returned verbatim; coverage-keyed touching (RE-touch) versus value-keyed membership is an internal consequence of these definitions, and the L8 contrast is already present in the referenced ASN-0043.

## Issue 2: Empty endsets in non-type slots not covered in the boundary catalog
Reason: Derivable from the ASN alone. `coverage(∅) = ∅` follows from the coverage definition (empty union), so `touches(∅, I)` is false by RE-touch; nothing about design intent or implementation behavior is needed to state the one-line note.

## Issue 3: RE-wp mischaracterizes the K.λ precondition
Reason: Derivable from the spec alone. The correct K.λ binding precondition and the freshness-as-derived-lemma distinction both live in ASN-0093, which this ASN already cites; restating `pre` is a matter of aligning with that sibling ASN, not querying Nelson or Gregory.
