# Channel Assignment — ASN-0102 review-41

**Date:** 2026-06-07 23:18

## Issue 1: X8 calls the copied blocks "maximal contiguous I-runs of resolve_Σ(R)" — contradicting the inter-reference coalescence it then asserts
Reason: The fix is internal — the ASN already states the correct formulation ("each `k_i` is the maximal-contiguous-I-run count of reference `r_i` taken in isolation" and `resolve(R) = resolve(r_1) ⌢ … ⌢ resolve(r_q)` from ASN-0058), so the corrected wording is derivable from the ASN's own load-bearing statement without theory or implementation evidence.
