# Channel Assignment — ASN-0113 review-5

**Date:** 2026-06-05 00:32

## Issue 1: W15's independence derivation rests on a false universal premise about K.μ⁻
Reason: Internal fix. The correction concerns ASN-0047's K.μ⁻ semantics, which the ASN already cites, and the corrected derivation rests on W1 (`n_S = |V_S(d)|` decided by the predicate `v₁ = S`) — all present in the note. No design intent or implementation evidence is at stake; the independence conclusion is re-grounded on existing content.

## Issue 2: The single-occupied-subspace result is never concretely exercised
Reason: Internal fix. Adding a text-only worked instance verifying W3, W4, W7, W13, W14 is purely mechanical instantiation of the note's own definitions (`ext`, `VSlice`, `occupied`, `n_S`) against specific tumblers. Nothing about Nelson's intent or Gregory's code is needed.
