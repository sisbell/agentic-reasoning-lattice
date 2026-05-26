# Channel Assignment — ASN-0069 review-15

**Date:** 2026-05-25 17:19

## Issue 1: V0 effects table cites V5/V5a for a universal frame condition that requires composite frame composition
Reason: Citation accuracy fix derivable from ASN-0047's elementary frame conditions (K.δ, K.μ⁺, K.ρ) already in scope; no design intent or implementation evidence needed.

## Issue 2: V10(a) cites T10a.6 to rule out a cross-allocator equality that cannot arise
Reason: Citation pruning; V1 already fixes both siblings to `A_v(d_src)`, so T10a.7's within-allocator injectivity alone closes the argument. Internal logic fix.

## Issue 3: V8b derivation conflates Corr_g and Π_g when arguing K.μ⁺_L invariance
Reason: Logical clarification — the reviewer's suggested option (b) uses only `F ⊆ V_{s_C}(d_src)` and definitions already in V8b. Internal fix derivable from the ASN's own content.
