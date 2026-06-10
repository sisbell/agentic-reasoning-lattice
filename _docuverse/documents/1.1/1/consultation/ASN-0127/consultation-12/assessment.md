# Channel Assignment — ASN-0127 review-12

**Date:** 2026-06-10 02:48

## Issue 1: Mapping-block citation misattributes B1/B2 to the query region
Reason: This is a within-spec citation correction, not a question of design intent or implementation behavior. The reviewer has already identified the correct supporting lemma (C1a, RestrictionDecomposition in ASN-0058), and the substantive claim — that `image(W, d, Σ)` is the union of the *W-restricted* sub-runs rather than full block I-extents — follows directly from F-IMG's own definition (`image(W, d, Σ) = {Σ.M(d)(v) : v ∈ W ∩ dom(Σ.M(d))}`). Which ASN-0058 block lemma to cite is a formal cross-reference resolvable against the spec, and neither Nelson nor Gregory governs it.

## Issue 2: The keystone's reach is overstated — existence anchoring does not propagate from F-CIL
Reason: The contradiction and its resolution are both already on the page. The overstated "propagates to every preservation claim" claim is refuted by the note's own E-INV derivation, which explicitly roots in LP13 (ASN-0098) under a growing store where F-CIL's `Σ.L = Σ'.L` hypothesis fails, with E-MONO and E-CONS chaining off E-INV. Scoping the keystone to the store-fixed lane and naming LP13 as the second keystone is a re-statement from material already present in the ASN.
