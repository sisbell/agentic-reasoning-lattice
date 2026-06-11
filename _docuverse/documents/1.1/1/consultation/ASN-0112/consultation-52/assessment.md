# Channel Assignment — ASN-0112 review-52

**Date:** 2026-06-10 22:00

## Issue 1: V5's exact-cover proof mis-attributes the boundary argument to D-CTG★
Reason: The fix is a proof-routing correction using machinery already present in the ASN — prefix-pinning via T1 and the TA5 least-same-length-successor tightness already established in the V3 paragraph. No design intent or implementation evidence is needed; the review even supplies the two-step argument.

## Issue 2: V6's formal statement is too weak to express the dichotomy, and the wp(Exact) derivation relies on the missing strength
Reason: The corrected statement and its witness `w⋆ = [s_C,1,…,1,n_C+1]` are already in the ASN's own V6 proof text; the fix is restating the recorded claim at occupied depth and rerouting the wp necessity step through it. Entirely internal.

## Issue 3: V18's exhaustiveness argument skips the link-only regime
Reason: Both missing sub-cases are discharged by foundations the ASN already cites — D-MIN★ at `S = s_L` pinning the link minimum, and ASN-0047's specification of `K.μ⁺_L` as a depth-preserving append past the maximum — so the uniform restatement is derivable without new evidence. The link-only regime's reachability is already grounded by the cited deletion consultation.

## Issue 4: V-ReachTight stated three times in one passage (anti-bloat)
Reason: Pure editorial deletion of a redundant prose restatement; no semantic content changes and nothing external bears on it.
