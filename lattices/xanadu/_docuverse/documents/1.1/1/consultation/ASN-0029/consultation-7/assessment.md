# Revision Categorization — ASN-0029 review-7

**Date:** 2026-03-11 16:18

## Issue 1: D7a formal statement is too weak to support the home-document derivation
Category: INTERNAL
Reason: The prose already states the stronger property ("Each fresh address has the form `d.0.E₁...Eδ`") and the derivation already uses the element separator at position `#d + 1`. The fix is aligning the formal statement with existing prose — no external evidence needed.

## Issue 2: D14's ≺ definition admits degenerate tumblers, breaking the forest derivation
Category: INTERNAL
Reason: All three proposed fixes (restrict parent to Σ.D, add non-degeneracy to ≺, or refine document-identifier definition) are derivable from definitions already in the ASN and ASN-0001. The review itself identifies option (a) as most economical, aligning with the operational derivation already present.

## Issue 3: D2 verification for DELETE, COPY, REARRANGE is unsubstantiated
Category: INTERNAL
Reason: The reasoning chain (P7 → V-space defined → Σ.D membership) uses only properties already defined in ASN-0026. The fix is either spelling out the existing chain or explicitly noting the proof obligation on future postconditions — both derivable from current content.

## Issue 4: ASN-0026 invariants not verified for new operations
Category: INTERNAL
Reason: The review itself notes the verifications are trivial — P0/P1 preserved because I-space is unchanged, P2 for D12 follows from D12(c)+P2+D12(e). All reasoning uses existing properties from ASN-0026; no design intent or implementation evidence is needed.
