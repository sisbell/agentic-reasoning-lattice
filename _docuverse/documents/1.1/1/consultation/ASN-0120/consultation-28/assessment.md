# Channel Assignment — ASN-0120 review-28

**Date:** 2026-06-11 06:07

## Issue 1: The worked example stipulates the resolution outputs instead of computing them
Reason: The fix is internal — the review specifies the exact spec-sets to exhibit, and the computation (checking `wf`, evaluating `⟦σ⟧`, applying the active-position filter, reading images through `Σ.M(A)`) uses only the ASN's own definitions of `wf` and `ρ` on data already present in the example. No design intent or implementation evidence is required.
