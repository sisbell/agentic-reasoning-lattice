# Channel Assignment — ASN-0119 review-27

**Date:** 2026-06-10 03:45

## Issue 1: RA1 attributes the bijection equation to the wrong source
Reason: This is an internal attribution correction. The note's own "The transposition as a permutation" section already establishes the pointwise equation `M'(d)(π(v)) = M(d)(v)` as the *definition* of π via R-PPERM/R-SPERM, and sources RA2 there — so RA1's citation of R-RI for the equation contradicts the note's own text. Splitting the attribution aligns RA1 with material already present; the provenance of ASN-0084's R-RI (a peer spec note) is reference material covered by neither channel, and the review has already supplied the precondition/conclusion structure.

## Issue 2: discoverability biconditional derived twice
Reason: Pure redundancy removal derivable from the ASN alone — both derivations of the biconditional (RA7b-aggregate and LP12+RA1) are already in the note, and the fix simply drops the intervening RA7b sentence while retaining the LP12 address-view that the note itself identifies as the deeper "why." No design intent or implementation evidence is implicated.
