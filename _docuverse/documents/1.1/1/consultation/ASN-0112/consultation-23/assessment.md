# Channel Assignment — ASN-0112 review-23

**Date:** 2026-06-08 09:36

## Issue 1: V2 case 2 asserts "With k = 1" without local justification
Reason: The missing clause is derivable from facts already in the ASN — S8-depth forces single-subspace endpoints to share depth, so `#origin_d > #reach_d` excludes that case and leaves cross-subspace, where divergence is at position 1. No external channel needed.

## Issue 2: V3 explains the same-depth qualifier twice
Reason: Pure deduplication of two statements making the identical point; an internal editing fix requiring no design intent or implementation evidence.

## Issue 3: V3 narrates its own proof structure
Reason: Removing procedural scaffolding and stating the V2 reach biconditional dependency directly is a prose tightening internal to the ASN.

## Issue 4: V17 restates V2's T12 well-formedness
Reason: V2 already derives the T12 legality; redirecting V17 to cite it and keep only its non-redundant content is internal restructuring with no new fact required.

## Issue 5: V3's closing depth-taxonomy over-elaborates
Reason: Trimming an unused taxonomy down to the one same-depth relation V3 needs is derivable from the ASN's own claim structure; no external input required.
