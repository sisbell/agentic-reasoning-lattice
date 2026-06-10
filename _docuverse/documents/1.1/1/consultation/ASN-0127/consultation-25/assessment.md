# Channel Assignment — ASN-0127 review-25

**Date:** 2026-06-10 12:23

## Issue 1: D-ZERO's gloss of a discovery zero drops the region qualifier
Reason: The fix is internal — the correct region-qualified reading is forced by the ASN's own definitions (F-IMG, F-V, F-FULL distinguish sub-region from full-region queries), and the review's counterexample is built entirely from the ASN's worked material. No design intent or implementation evidence is needed to reword the gloss to match what `findlinks_disc` provably asserts.

## Issue 2: the four-position incomparable witness needs pairwise distinctness of `a, b, c`
Reason: The fix is internal — adding the missing hypothesis "`a, b, c` pairwise distinct" is pure set-theoretic repair of a witness construction the ASN itself supplies, parallel to the explicit "`a ≠ b`" already stated in the injective witness. The witness is a mathematical example, not a design or implementation claim.

## Issue 3: duplicated role/emphasis prose (anti-bloat)
Reason: The fix is internal — purely editorial deletion of restating sentences, with the choice of which statement to retain decided by the ASN's own structure (definition slot vs. proof slot vs. application site). Neither design intent nor implementation evidence bears on prose deduplication.
