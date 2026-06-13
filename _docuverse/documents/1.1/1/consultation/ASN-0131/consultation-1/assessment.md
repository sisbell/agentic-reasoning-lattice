# Channel Assignment — ASN-0131 review-1

**Date:** 2026-06-13 04:34

## Issue 1: Fragmentation under rearrangement contradicts the content-identity invariant
Reason: Internal. The note already settles this — RE reports content identity (RE-DEF, RE-TRANS, RE-IDENT) and the V-rendered mode is explicitly deferred to open question 3; the fix is to scope the fragmentation (ASN-0082) passage to V-order display and state that under K.μ~ only membership changes (LP11), reconciling prose with claims already present.

## Issue 2: Boundary behavior of RE is never stated
Reason: Internal. Empty image, no-addressable-links, and empty-endset cases all follow mechanically from RE-DEF and `touch_R(e) ≡ coverage(e) ∩ I ≠ ∅` (with `coverage(∅)=∅`); empty-endset permissibility in slots 1,2 is settled by the already-cited ASN-0043 link structure, not by design intent or implementation.

## Issue 3: Union-distributivity is a derivable consequence, deferred entirely to an open question
Reason: Internal. The union corollary composes forward-image union-distributivity (F-UDIST/F-VDIST, ASN-0127, already cited and tied to RE-SEL) with RE-DEF; the intersection half (broken by content-sharing non-injectivity, M13/M14) is correctly retained as open. No channel needed.

## Issue 4: The "finite, computable object" claim omits decidability of the addressability filter
Reason: Internal. This is a citation patch — invoke ASN-0086's existing decidability of `nullified(Σ)` (CoverageEqualityDecidable + T2 span-membership) to discharge the addressability filter; the result already exists in the cited foundation.

## Issue 5: No concrete worked example
Reason: Internal. The scenario is constructed mechanically by evaluating RE-DEF on a concrete `Σ`; the postconditions it pins down (RE-OVL, RE-CLIP, RE-UNIT, per-slot surfacing) are all already stated claims, so no design-intent or implementation evidence is required to build or check it.

## Issue 6: No weakest-precondition analysis for any non-trivial stability question
Reason: Internal. The `wp(K.μ⁻[d, R], RE unchanged)` derivation parallels the existing wp machinery (D-CWP, ASN-0127; LP12a/b, ASN-0098; wp Cases, ASN-0086) applied to RE-DEF's image-reduction-plus-per-slot-selection; all inputs are already cited foundations.
