# Channel Assignment — ASN-0100 review-23

**Date:** 2026-05-28 13:28

## Issue 1: The "precisely two-fold" atomicity scope is asymmetric between R and C
Reason: Internal. The inconsistency is purely logical — the set-difference/coupling argument the ASN already deploys for R applies identically to the K.α→K.μ⁺ window for C, and all three resolution paths (extend scope, interleave allocation-with-placement, or drop the cross-composite framing) are reframings using machinery already present in the ASN: J0/J1★/J1'★ couplings (ASN-0047), the Class (a)/(b) per-state-vs-boundary distinction (ASN-0047), and SequentialTransitionAxiom (ASN-0093). No design intent or implementation evidence is needed to pick a self-consistent story.
