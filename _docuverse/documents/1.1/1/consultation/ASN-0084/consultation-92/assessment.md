# Channel Assignment — ASN-0084 review-92

**Date:** 2026-05-30 18:48

## Issue 1: Merge asserts a run without establishing S8-cons, while Split proves it
Reason: Internal — the junction derivation uses Extended Associativity and the I-adjacency/V-adjacency conditions already stated, exactly mirroring the Split proof present in the same section. No design intent or implementation evidence is needed.

## Issue 2: Essay paragraph on maximality coincidence is consumed by no proof
Reason: Internal — purely an editorial relocation/removal decision about content the ASN itself does not consume; the relevant Open Question is already in the ASN. No external channel needed.

## Issue 3: Duplicated deferral of the post-state S8 existence/uniqueness discharge
Reason: Internal — consolidating two cross-referencing paragraphs that establish the same foundation-S8 application is a self-contained exposition fix derivable from the ASN's own structure.

## Issue 4: R-BLK "Outside ⋃ₖ V(bₖ)" re-derives EXT-VAC
Reason: Internal — the compression simply cites EXT-VAC (already proved in Consequences of R-PRE) in place of re-walking CS2–CS4 + R-PRE(iv); the review even supplies the replacement sentence. No external channel needed.
