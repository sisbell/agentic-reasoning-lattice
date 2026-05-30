# Channel Assignment — ASN-0082 review-74

**Date:** 2026-05-30 14:06

## Issue 1: OrdinalExceedsDisplacement quantifies over tumblers its depth justification does not cover
Reason: Internal fix. Both defects are about the ASN's own logical scaffolding — the quantifier domain should be tightened to `v ∈ R ⊆ V_1(d)` (or `#v = 2` added as an explicit hypothesis) and the OrdinalOrderEquivalence-licensing prose relocated to the proof body. The depth scoping axiom `#p = 2`, the definition of R, and the result-length identity for `r = p ⊕ w` are all already present in the ASN, and every application already uses `v ∈ R`, so no design intent or implementation evidence is required.
