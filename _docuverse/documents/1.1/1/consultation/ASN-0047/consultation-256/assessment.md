# Channel Assignment — ASN-0047 review-256

**Date:** 2026-06-01 14:49

## Issue 1: "Inherited from foundation" preamble contradicts the body's own preservation work
Reason: This is an internal consistency fix between the preamble's claim ("every preservation argument is supplied by the cited foundation") and the body's own Class (a) verification, which locally derives preservation under this ASN's new/amended transitions. Resolving it requires only aligning the preamble with the derivations already present in the ASN — no design intent or implementation evidence is at stake.

## Issue 2: "tracked" sub-allocator terminology is load-bearing but undefined, reinventing ASN-0034's "activated allocator"
Reason: The fix is a notation/terminology alignment against ASN-0034 (a cited foundation), tying "tracked sub-allocator"/"tracked domain" to the foundation's "activated"/`domₛ(A)` vocabulary or adding a one-line synonym definition. This is internal to the formal apparatus the ASN already inherits; neither Nelson's intent nor the implementation bears on whether the term is a synonym for the foundation notion.

## Issue 3: Orphan-links section duplicates the Class (a) link-invariant preservation prose
Reason: This is a purely editorial deduplication — replacing the re-enumerated L0/L1/L1a/L3/L12/L14 preservation list with a pointer to the Class (a) verification, retaining only the coupling-vacuity argument. Fully derivable from the ASN's own structure.
