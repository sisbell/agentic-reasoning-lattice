# Channel Assignment — ASN-0131 review-5

**Date:** 2026-06-13 06:46

## Issue 1: The editing taxonomy claims to exhaust the vocabulary but never classifies K.μ⁺_L
Reason: Internal. The fix only applies K.μ⁺_L's established frame (it adds a link-subspace V-position `v_ℓ ↦ ℓ` and frames `Σ.L`, a definitional fact from the cited ASN-0047 vocabulary, restated in the review) together with the note's own `W ⊆ s_C` restriction to conclude `v_ℓ ∉ W` hence the image is unchanged — no design intent or implementation evidence is in question.

## Issue 2: Retraction "removal only" is not discharged for the emitter's type slot
Reason: Both channels — the note must establish whether the designated retraction type `R` has a structural property placing `coverage(R)` outside content; Gregory supplies what udanax-green's retraction type actually is structurally, and Nelson supplies whether the design *requires* that disjointness as an invariant the note can lean on (vs. needing the option-(b) hedge).
Nelson question: Does the design intend the retraction (deletion) type to be a reserved system type seated outside the content space, so that retraction-type endsets are structurally guaranteed disjoint from content addresses?
Gregory question: What is the structural form of the conventional retraction type address in udanax-green's nullification mechanism — does it sit at an element-level address in a dedicated non-content subspace, so that `coverage(R) ∩ dom(Σ.C) = ∅` holds structurally rather than by convention?
