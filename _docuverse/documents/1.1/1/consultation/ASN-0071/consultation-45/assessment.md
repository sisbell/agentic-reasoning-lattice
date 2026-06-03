# Channel Assignment — ASN-0071 review-45

**Date:** 2026-06-03 09:35

## Issue 1: Same deferrals stated twice — "What we do not specify" duplicates Open Questions
Reason: Pure editorial deduplication — the ASN states the same two deferrals (replica freshness, visibility filtering) in two sections. Choosing which location keeps the forward pointer requires no design intent or implementation evidence; both framings are already present in the ASN.

## Issue 2: The σ′ paragraph analyzes a case the precondition already excludes
Reason: The fix is removal of precondition-rationale prose for a span the `actionPoint(ℓ) = #u` precondition already rejects. The ASN's own precondition statement and the valid `σ_E` demonstration settle the matter; no external channel is needed.
