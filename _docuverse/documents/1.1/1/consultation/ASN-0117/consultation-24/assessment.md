# Channel Assignment — ASN-0117 review-24

**Date:** 2026-06-09 10:33

## Issue 1: State-subscripted coverage contradicts the foundation
Reason: Pure notational correction internal to the ASN — the fix replaces state-subscripted `coverage_{Σ}(e)` with the slot-indexed form `coverage(Σ'.L(a).eᵢ)` that LP3★ (already cited) supplies; ASN-0098's definition of `coverage` as state-independent is the only fact needed, and it is already referenced.

## Issue 2: Duplicated range-formulation justification
Reason: Editorial deduplication derivable from the ASN's own structure — consolidate the subspace-split-resolution argument at the S3★ site and have P5 cite it; no design intent or implementation evidence is required.
