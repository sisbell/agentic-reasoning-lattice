# Channel Assignment — ASN-0134 review-22

**Date:** 2026-06-14 03:13

## Issue 1: The idem=⊤ duplicate is presented as a cross-home phenomenon, but it is home-independent
Reason: Internal — the note's own I1a-breaking argument ("the second deposit's own pre-state already carries the first's coverage-equal tuple") is already home-independent, and the structural facts that drive it are all present: clause 2 is scoped to the frontier-read-and-deposit (not the dedup step), and the dedup-read is over the global `A_K` (ASN-0128 I1, already cited). The same-home case follows by clause-2 spacing supplying the distinct deposit addresses that H1 supplies cross-home; no design intent or implementation evidence bears on whether clauses 1–7 permit the duplicate.

## Issue 2: Off-by-one in the anchor-separator index
Reason: Internal — the correction is fixed by the note's own anchor formula `b_C(d) = [d.0.s_C]` (separator immediately after d's last digit, i.e. position #d+1) together with ASN-0093's `DisjointSubAllocatorChains` convention (s_C at #d+2), a cited dependency; counting positions in the note's explicit address `[1.0.1.0.1.0.1]` confirms it. Neither design intent nor the udanax-green implementation is needed to resolve an indexing-convention arithmetic error.
