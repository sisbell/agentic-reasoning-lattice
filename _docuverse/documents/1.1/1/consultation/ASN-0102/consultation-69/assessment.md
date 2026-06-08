# Channel Assignment — ASN-0102 review-69

**Date:** 2026-06-08 02:34

## Issue 1: PC3 derives the target subspace from the wrong quantity
Reason: The fix is internal — it re-derives `subspace(v) = s_C` from S3★ applied to the target placement (content images at `dom(C)` force `s_C` V-positions, since `dom(C) ∩ dom(L) = ∅`), using only projectors and invariants already stated in the ASN. No design intent or implementation evidence is required.
