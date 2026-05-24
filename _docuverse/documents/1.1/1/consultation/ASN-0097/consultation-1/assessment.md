# Channel Assignment — ASN-0097 review-1

**Date:** 2026-05-24 10:16

## Issue 1: Transition claims lack explicit proofs
Reason: The proofs are mechanical derivations from the definition of `proj` (introduced in this ASN) and the K.μ contracts already cited from ASN-0047. No external input needed.

## Issue 2: Π10(b) set equality without showing both directions
Reason: Both inclusions follow mechanically from the K.μ~ contract (already cited) and the bijection property of π. Derivable from the ASN's own content.

## Issue 3: Π11 prose-vs-formal mismatch
Reason: This is an authorial choice between two reformulations, both grounded in the ASN's own definition of `proj` and Π8–Π10. Internal.

## Issue 4: R13 (boundary insertion) depends on an unstated link-creation constraint
Reason: The fix requires knowing whether K.λ constrains endset coverage to `dom(Σ.C)` at creation time. Nelson clarifies whether the design intended links to be forward-referenceable; Gregory confirms what the implementation enforces.
Nelson question: At link creation, did the design intend endset coverage to be restricted to already-allocated I-addresses, or are forward references (to addresses not yet in `dom(C)`) permitted?
Gregory question: Does udanax-green's link allocation (the K.λ analogue) verify that each address referenced by an endset is already present in the content store, or does it accept endsets that name unallocated addresses?

## Issue 5: Π15 collapses to Π0
Reason: The reformulation derives from L12 (ASN-0043) and the K.μ⁻ frame condition (ASN-0047), both already referenced in the ASN. Internal.

## Issue 6: No concrete example
Reason: Constructing and walking through a scenario is purely a mechanical application of the ASN's own definitions and the K.μ contracts. Internal.

## Issue 7: Weakest-precondition analysis absent
Reason: A wp computation for K.μ⁻ or K.μ⁺ against `iproj` or `reaches` follows mechanically from the contracts (ASN-0047) and the definitions introduced in this ASN. Internal.
