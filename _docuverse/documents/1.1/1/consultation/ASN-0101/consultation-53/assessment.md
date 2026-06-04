# Channel Assignment — ASN-0101 review-53

**Date:** 2026-06-04 05:51

## Issue 1: D11's cross-document wp bullets are trivial inventory
Reason: Pure editorial collapse — the fix removes two wp bullets whose pullback equals the pre-state predicate, derivable entirely from D9's first clause already stated in the ASN. No design intent or implementation evidence bears on the deletion.

## Issue 2: Empty-arrangement "Consequence" over-enumerates states the precondition already excludes
Reason: The reduction to one sentence follows directly from the span-well-formedness precondition `s ∈ V_S(d)` stated in the ASN; the enumerated K.σ/K.δ/post-DEL mechanisms add no constraint. Fully internal.

## Issue 3: Defensive "what the proof does not use" sentence in the D0 reduction
Reason: Relocating or deleting the non-circularity caveat is a presentation choice within the ASN's own proof; the reasoning about candidate `v`'s components is already present. No external channel needed.
