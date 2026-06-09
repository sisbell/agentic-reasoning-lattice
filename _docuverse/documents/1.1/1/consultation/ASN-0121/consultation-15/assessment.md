# Channel Assignment — ASN-0121 review-15

**Date:** 2026-06-09 02:10

## Issue 1: FL-WP(a) discharges addressability with an invalid inference
Reason: The fix is internal: keep the `ℓ ∉ nullified(Σ')` conjunct explicit, directly mirroring ASN-0086's EmitKWeakestPrecondition Case 2, which this ASN already cites. The ghost-address possibility that breaks the freshness inference is established in the cited foundation (ASN-0086 L4/L9, R5; ASN-0098 LP17/LP18), and the corrected wp is fully spelled out in the review — no design intent or implementation evidence is required.
