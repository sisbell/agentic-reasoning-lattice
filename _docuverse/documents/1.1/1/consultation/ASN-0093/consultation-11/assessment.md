# Channel Assignment — ASN-0093 review-11

**Date:** 2026-05-18 19:52

## Issue 1: L14 discharge matrix entries for K.α and K.λ elide per-transition specifics
Reason: The fix restructures the matrix to distinguish frame preservation (K.σ) from new-key direct derivation (K.α/K.λ). All required facts — L0's C-clause, StoreT4Validity via ChainElementT4Validity, SC-NEQ, T7 — are already established in the ASN, so the fix is derivable internally.

## Issue 2: Cross-document disjointness Case A overstates witness route for `p₂ ⋠ p₁`
Reason: The fix either renames the cited Prefix clause precisely or notes the length-divergence alternative for `p₂ ⋠ p₁`. Both are derivable from ASN-0034's Prefix definition (already a foundation dependency cited throughout the ASN) and from the proof's own length facts (`#p₁ < #p₂`).

## Issue 3: Inductive ordering of ChainPrefixExtension and ChainElementT4Validity needs an explicit dependency note
Reason: This is a purely organizational addition — stating that the six chain lemmas are proved in dependency order so each may cite all earlier ones. No external content is needed; the dependency structure is already implicit in the existing proofs.
