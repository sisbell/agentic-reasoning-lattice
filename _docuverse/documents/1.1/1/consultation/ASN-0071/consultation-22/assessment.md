# Channel Assignment — ASN-0071 review-22

**Date:** 2026-06-02 23:59

## Issue 1: Range-union containment is attributed to S3★ alone, but requires SubspaceExhaustiveness (S3★-aux)
Reason: The fix is purely editorial against the foundation corpus — the review already names the exact invariant to cite (S3★-aux SubspaceExhaustiveness, ASN-0047) and the remedy is to add that citation wherever `ran(Σ.M(d)) ⊆ dom(Σ.C) ∪ dom(Σ.L)` is asserted and re-gate the subset-claim/F-find proofs on the routing invariants. This requires neither Nelson's design intent nor udanax-green evidence, only correct attribution to an existing ASN-0047 invariant.
