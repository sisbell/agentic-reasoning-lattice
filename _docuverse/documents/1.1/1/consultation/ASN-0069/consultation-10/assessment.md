# Channel Assignment — ASN-0069 review-10

**Date:** 2026-05-25 14:37

## Issue 1: V1's parent-equality induction for the subsequent-fork case is too compressed
Reason: The fix is mechanical — spell out an induction over `A_v(d_src)`'s emission chain using KDeltaParentK01 (ASN-0047) at each step, matching V2's already-present structural-ancestry induction template. All axioms and the inductive template are already present in the ASN and its cited foundation.

## Issue 2: V0 does not explicitly preclude interleaving within the fork composite
Reason: Whether composites are uninterrupted sequences is a property of ValidComposite★ as defined in ASN-0047 — the fix is to make V0's reliance on that definition explicit (and add the parallel intra-composite no-interleaving clause that V11 already states at the inter-composite level). No design-intent or implementation evidence needed beyond cited foundation.

## Issue 3: V8b's restoration discussion buries the load-bearing claim
Reason: Pure editorial tightening — keep `Π_g ⊆ F` and `Π_{Σ'} = F`, the derivation, and a one-line non-monotonicity remark with forward reference to K.μ⁻/K.μ⁺ semantics in ASN-0047. The operational details being removed are properties of ASN-0047's transitions, not facts about forking that need fresh evidence.
