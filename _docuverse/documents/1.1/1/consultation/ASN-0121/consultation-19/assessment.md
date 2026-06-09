# Channel Assignment — ASN-0121 review-19

**Date:** 2026-06-09 02:26

## Issue 1: FL-DEC proves `sat` decidable but not the addressability filter
Reason: Internal — the fix is the decidability of `nullified(Σ)` membership, which the ASN already has the machinery for (CoverageEqualityDecidable selects `L_R^Σ`, and `a ∈ coverage(G')` is a T2 test) and which ASN-0086 already records for its ActiveSubset/`nullified`. No design intent or implementation evidence is required; the step is derivable and citable from foundations already referenced.

## Issue 2: FL-WP claims K.λ is "the unique result-changing transition" then omits the fresh-retraction-link entry case
Reason: The mathematical wp for a fresh retraction-typed link (carrying the self-retraction term) is internally derivable from FL-DEF and ASN-0086, but the *choice* between computing case (c) and scoping it out rests on whether a retraction link's own discoverability is an intended guarantee of FINDLINKS — a design-intent question for Nelson.
Nelson question: Is a retraction link itself meant to be discoverable as a result of `FINDLINKSFROMTOTHREE` (e.g. via a type-`R` query), or are retraction links intended to be search machinery that the operation is not obliged to surface as ordinary results?
