# Channel Assignment — ASN-0102 review-106

**Date:** 2026-06-08 05:36

## Issue 1: X15 asserts atomicity but only gestures at why COPY is irreducibly atomic
Reason: The required derivation is fully internal — it follows from `ValidComposite★`'s per-state invariant obligation (every intermediate state must satisfy D-CTG★/D-SEQ★, a distinction the ASN already draws in X17) combined with the displacement structure in X7/X16. Any displace-then-fill decomposition exposes an intermediate `s_C` V-gap, and that the per-state invariants bind every reachable state (not just composite boundaries) is already stated in the ASN; no design-intent or implementation evidence is needed to forbid the hole.
