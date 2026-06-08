# Channel Assignment — ASN-0112 review-39

**Date:** 2026-06-08 11:41

## Issue 1: wp is computed over a universally-valid biconditional, not a contingent property
Reason: The fix is internal — it restructures the wp argument by introducing a contingent predicate `Tight ≡ "reach(σ_d) = reach_d"` and deriving its weakest precondition via D0/D1, exactly mirroring the `Exact`/V5/V6 factoring already present in the ASN. All needed machinery (D0, D1, V-ReachTight, the Exact template) is internal to the document; no design intent or implementation evidence is required.
