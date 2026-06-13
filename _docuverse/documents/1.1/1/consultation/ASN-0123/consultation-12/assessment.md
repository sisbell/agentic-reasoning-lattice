# Channel Assignment — ASN-0123 review-12

**Date:** 2026-06-13 01:34

## Issue 1: B2's stated precondition is not discharged by VN-B1
Reason: The fix is internal — route (a) recomposes the conclusion from facts already proved or cited in the ASN: VN-B1 (proved here) gives the contiguous prefix `{c₁,…,c_m}`, S0/StreamOrdering (already cited in V5(a)) gives `c_m = max`, and the stream recurrence `c₁ = inc(d,1)`, `cₙ₊₁ = inc(cₙ,0)` (stated in the `S(d,1)` definition) yields the gap-free successor without invoking B2's global B1 hypothesis. No design intent or implementation evidence is at issue.
