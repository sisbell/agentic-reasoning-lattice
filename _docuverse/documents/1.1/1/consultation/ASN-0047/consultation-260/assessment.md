# Channel Assignment — ASN-0047 review-260

**Date:** 2026-06-01 15:25

## Issue 1: FrontierEquivalence reverse direction does not exclude node baptism before invoking GlobalUniqueness
Reason: The fix is derivable from the ASN alone — TA5(c) gives `zeros(inc(t,0)) = zeros(t) ≥ 1` since `¬Node(t)`, so `inc(t,0)` is non-node and cannot be a NodeBaptism output, all from existing notation and lemmas already cited in the proof.

## Issue 2: J4 restates the content-source / address-allocation distinction and the same implementation citation multiple times
Reason: This is an anti-bloat de-duplication of an already-stated fact and its existing Nelson/Gregory grounding; consolidating to the load-bearing site requires no new design intent or implementation evidence.

## Issue 3: K.δ per-sub-case discharge is duplicated between the K.δ definition and the dedicated discharge section
Reason: Editorial trim — the per-k conjuncts are already established in the K.δ definition; reducing the dedicated section to the activation/spawnPt material and cross-referencing the definition needs no external channel.
