# Channel Assignment — ASN-0047 review-106

**Date:** 2026-05-18 06:29

## Issue 1: K.δ k = 0 maximality conjunct conflates allocator sub-streams
Reason: The reviewer already cites Nelson (LM 4/29) and Gregory (`docreatenewversion`) confirming repeated versioning is intended, and provides three alternative formulations evaluable from foundation properties (T4b, TA5, T10a) within the ASN. Option (b) — `inc(t, 0) ∉ E` — is derivable since inc is invertible at sig(t), making the choice a structural/specification matter not requiring further consultation.

## Issue 2: Matrix entry for S3★ under K.μ~ misorders the dependency
Reason: This is a prose-ordering issue within the ASN itself — the K.μ~ section's existing argument already derives S3★(Σ') from the K.μ⁻ + K.μ⁺ decomposition without invoking fixity, so the matrix entry can be reworded directly from material already present.

## Issue 3: D-SEQ★ derivation Step 2 leaves m = 2 specialisation implicit
Reason: Pure expositional clarity issue. The m = 2 specialisation is already handled correctly in Step 1's base case and the surrounding prose; Step 2 simply needs to make the degeneration explicit, which is derivable from the existing notation conventions in the ASN.
