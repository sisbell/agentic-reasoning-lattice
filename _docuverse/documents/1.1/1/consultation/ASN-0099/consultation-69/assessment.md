# Channel Assignment — ASN-0099 review-69

**Date:** 2026-06-04 13:54

## Issue 1: A1/A1a is over-layered for "only K.λ modifies Σ.L", and A1a is never stated as its own block
Reason: Purely structural reorganization of lemma statements already present in the ASN; collapsing A1a/A1 layering and removing mechanism prose requires no design intent or implementation evidence.

## Issue 2: F10's closing sentence restates the finite-total-order argument already given
Reason: Deleting a redundant restatement of the finite-total-order argument already in F10's body; entirely internal.

## Issue 3: "Local Atomicity" final sentence is both redundant and imprecise on "undiscoverable"
Reason: The fix restates in terms of `findlinks` inclusion using the F11 note's own arrangement-conditional discoverability distinction (and LP17 orphaned-links point) already referenced in the ASN; derivable internally.

## Issue 4: F11 and F19 carry near-duplicate I-side/V-side asymmetry prose
Reason: Trimming F19's redundant re-derivation down to its existing deferral to F11; purely editorial and internal.
