# Channel Assignment — ASN-0111 review-1

**Date:** 2026-06-04 22:00

## Issue 1: RL5 asserts a from/to-vs-type "existing content" asymmetry that does not exist
Reason: Internal. The correction is fully determined by claims already cited in this ASN and ASN-0043 — L4 (EndsetGenerality), L9 (ghosts), and this note's own RL8 and RL-GEN all establish that from/to endsets are equally unbound to existing content. No external intent or implementation evidence is needed to delete a self-contradictory asymmetry.

## Issue 2: RL7 multi-step determinacy is derived from single-step immutability without closing over the transition sequence
Reason: Internal. The fix is a formal one: either add induction over `Σ →* Σ'` or cite the already-available multi-step result LP13 / Store Monotonicity★ (ASN-0098), which RL8 already uses. Both routes are derivable from the ASN's own references.

## Issue 3: No concrete worked example
Reason: Internal. The worked read instantiates `readlink` and RL1/RL2/RL5/RL8 directly from this note's own definitions; constructing a link with scattered from-spans, an empty to-set, a ghost type, and an orphan instance requires only the spec already present, not design intent or implementation behaviour.

## Issue 4: The only wp computed is trivial
Reason: Internal. Whether a pure stateless read admits a non-trivial wp (e.g. over a composite read-after-transition postcondition) or whether RL0's membership condition is the complete picture is a reasoning question answerable from this ASN's own definition and RL7's transition closure.
