# Channel Assignment — ASN-0098 review-18

**Date:** 2026-05-26 02:53

## Issue 1: Proof support gap for "non-canonical ⟹ infinite F-intersection"
Reason: Pure proof-engineering issue internal to the ASN. The reviewer has both identified the gap (the descendant-mechanism witness only covers `#ℓ ≤ #d_0`) and supplied the fix (the within-chain argument using `actionPoint(ℓ) ≤ #ℓ < #s` together with T1 case (i) on existing chain structure). All facts needed — OrdinalDisplacement, T1, ChainEnumerationInjectivity, and the structural form of `F` — are already established in the ASN's own content and its cited foundations. No design intent (Nelson) or implementation evidence (Gregory) is required.
