# Channel Assignment — ASN-0058 review-60

**Date:** 2026-05-30 10:01

## Issue 1: M2's "V-extent translation" is established but never used to derive B1 ∧ B2
Reason: Internal — the fix is a proof-structure question about whether the interval/M-int machinery in M2 is consumed by its own conclusion. Both the disjoint-union partition claim (S8, ASN-0036) and the OrdinalShiftBase notational identity are already present in the ASN, so resolving "delete the dead reasoning vs. cite its downstream use" requires only inspecting this ASN's own derivations. No design intent or implementation evidence bears on it.
