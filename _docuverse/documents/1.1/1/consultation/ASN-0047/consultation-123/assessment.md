# Channel Assignment — ASN-0047 review-123

**Date:** 2026-05-19 17:44

## Issue 1: Transcluded replacement implicit precondition
Reason: The fix is derivable from the ASN's own J1★ semantics — J1★ is range-based and already states "(a, d) ∈ R already — from a prior insertion-deletion cycle — K.μ⁺ re-introducing a requires no new K.ρ." J4 (fork) already establishes the K.δ + K.μ⁺ + K.ρ pattern for first-time transclusion. Either restricting the two-step form's applicability (option a) or naming a third K.μ⁻ + K.μ⁺ + K.ρ composite (option b) follows mechanically from existing J1★ + J4 structure.

## Issue 2: S4 matrix row conflates content-S4 with entity/link distinctness
Reason: Pure labeling defect within the ASN. S4 is defined in ASN-0036 over dom(C); the K.δ and K.λ matrix cells supply entity and link-address distinctness, which are separate properties already discharged in body prose. Fix is a matrix restructuring (split rows or introduce a generalized symbol), derivable from the ASN's own definitions without external input.
