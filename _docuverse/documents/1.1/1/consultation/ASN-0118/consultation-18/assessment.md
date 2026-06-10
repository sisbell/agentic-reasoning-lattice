# Channel Assignment — ASN-0118 review-18

**Date:** 2026-06-09 17:08

## Issue 1: Two contradictory accounts of how S2 (arrangement functionality) is established
Reason: The fix is internal — the ASN already contains both accounts and the correct one (function-ness/no-holes resting on the tiling argument + CP3c + K.μ⁺, with I3 supplying only the shifted positions' well-formedness/depth). Reconciling CP3a to match the later, correct derivation is derivable from the ASN's own reasoning; no design intent or implementation evidence is at stake.

## Issue 2: Standing-precondition paragraphs carry defensive justification and a brittle use-site inventory
Reason: Pure prose reduction — drop the "load-bearing, not decorative" defense, the invariant inventory, and the already-inaccurate "exactly once" count, leaving the reachability scope and composite-boundary scope for P4★. Entirely internal; the substantive scoping content is already in the ASN.

## Issue 3: The ordinal-level non-requirement is restated seven times
Reason: Deletion task — keep the one load-bearing sentence (single-subspace by content-residence, single-depth by S8-depth, so CP0(a) rests on S3★ and CP0(c) on single-subspace, neither on `actionPoint(ℓ)`) and excise the restatements. The optional grounding clause already exists in the ASN, so no channel need supply anything new.

## Issue 4: Partial-binding admissibility is restated with defensive framing
Reason: Internal editorial cleanup — state the restriction semantics once and remove the reviewer-facing reassurances; the review explicitly notes the existing Nelson and Gregory grounding clauses are legitimate and may stay, so nothing new is required from either channel.
