# Channel Assignment — ASN-0043 review-142

**Date:** 2026-05-30 22:14

## Issue 1: The worked example omits two state-local invariants it claims to verify
Reason: The fix is internal — D-MIN, S8-fin, and S2 are all discharged directly from the already-constructed state (`min(V_1(d)) = [1,1]`, `|dom(Σ.M(d))| = 2`, single-valued arrangement), using definitions imported from ASN-0036 and already present in the conformance lemma. No design intent or implementation evidence is required.
