# Review of ASN-0087

## REVISE

### Issue 1: L1c discharge carries a rejected-route digression
**ASN-0087, Per-State Invariants at Σ' (L1c paragraph)**: "We do not identify this d-seeded chain with the sibling stream A_L(d) = S(b_L(d), 1): the chain from d first runs d →[inc(·, 2)]→ b_C(d) →[inc(·, 0)]→ b_L(d) →[inc(·, 1)]→ [d, 0, s_L, 1] →[inc(·, 0)]*→ ℓ, traversing the anchors b_C(d), b_L(d) (each with #E = 1) that A_L(d)'s elements (all with #E = 2) exclude."
**Problem**: The load-bearing discharge is the two sentences that follow ("ℓ enters dom(L) solely via K.λ, and ASN-0093 establishes L1c as an invariant maintained over all of dom(L) under K.λ"). The quoted sentence explains why an *alternative* proof route (identifying the chain with the sibling stream) is not used — it advances nothing in the actual discharge and reads as reviser drift relocated into the spec rather than removed. A reader must skip past the anchor-traversal detour to reach the proof.
**Required**: Delete the rejected-route sentence; keep only the clean K.λ/ASN-0093 discharge.

### Issue 2: M-DiscSymmetry asserted before it is derived
**ASN-0087, "What Is Indexed?"**: "LP12 treats every document uniformly — the home document has no privileged status *in the discovery function itself*. For the *standard content-reach route* ... discoverability is therefore symmetric (M-DiscSymmetry)."
**Problem**: This states the symmetry conclusion and the home-document/reflexive asymmetry as fact, but the supporting derivation is the wp Case 1 vs Case 2 split that appears two sections later. The same point is then restated in the wp section, the side-effects section, and the M-DiscSymmetry/M-WP claim rows. The "What Is Indexed?" occurrence is a forward-anticipation of a later-derived result, duplicating prose without advancing the argument.
**Required**: Either reduce the "What Is Indexed?" passage to the structural claim it owns (discoverability is computed from L and M ⇒ no index state component, M-NoIndexState) and let the wp section establish symmetry, or move the symmetry assertion to where it is derived.

## OUT_OF_SCOPE

### Topic 1: Well-formedness of forward-reaching endsets
**Why out of scope**: The first and fourth Open Questions (constraints on endsets covering not-yet-allocated I-addresses; discoverability once that content is later created) are genuinely new territory. The ASN correctly defers them rather than under-specifying; LP18 resurrection handles the mechanics it needs.

### Topic 2: Protocol-layer atomicity of the composite
**Why out of scope**: M-CompAtomicity correctly places composite-level atomicity (visibility of Σ_mid) at the protocol layer above the substrate. This is a future-ASN concern, not a defect here.

VERDICT: REVISE
