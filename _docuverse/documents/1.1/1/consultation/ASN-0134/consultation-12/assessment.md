# Channel Assignment — ASN-0134 review-12

**Date:** 2026-06-13 22:32

## Issue 1: A6's "per-state canonicity package" omits the contiguity invariant that §2 and §4 depend on
Reason: Internal. The fix reconciles A6's "every single-state invariant" billing with §2's "every chain gapless" prose, §4's use of `ChainMembershipForOrigin`, and §5's W3 by declaring which notion A6 means ("holds at every state of `𝔼`") and adding `ChainMembershipForOrigin`/`L-ContiguousPrefix` — invariants the note already cites (ASN-0093/0086) and already invokes per-state in §4. The resolution is spelled out in the finding and derivable from the note plus its cited foundations; no design intent or implementation evidence is at stake.

## Issue 2: A1 and §8 give inconsistent accounts of multi-type behavioral reads
Reason: Internal. Both characterizations already live in the note; the fix separates "zero steps" (true of all reads) from "single-index read-atomicity" (single-type reads only, cross-type reads only under clause 7), resting on ASN-0128's own definition of `targets_keyed`/default-view reads as cross-type joins — which §8 already quotes. This is a formalization/consistency reconciliation, not a question of what the design intended or what the code does.

## Issue 3: clause 7 is a *global* reader exclusion, mis-framed as "the dual of W4"
Reason: Internal. The scope asymmetry follows entirely from the note's own definitions and the structure of `𝔼` — clause 7 excludes "any interleaving writer step" (any writer advances the single index → global), W4 is per-`(d, s_C)` (local), and a type spans homes (§4's own cross-home same-type emits) so V2's minimal condition is type-scoped, not home-scoped. The correction is a pure framing/consistency fix derivable from the ASN alone.
