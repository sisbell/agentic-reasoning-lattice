# Channel Assignment — ASN-0112 review-2

**Date:** 2026-06-05 00:08

## Issue 1: V5 exact-cover is unproven for a link-only document
Reason: Derivable internally. The reviewer already identifies the needed grounding — ASN-0047's per-subspace foundation facts (D-CTG★/D-MIN★/D-SEQ★) — and rules out the unreachability escape, so the author either cites those facts or restricts V5's scope. No design-intent or implementation evidence is required; the foundation facts and the existing V5/V6 partition supply everything.

## Issue 2: V2 single-subspace divergence reasoning is stated only for content
Reason: Derivable internally. The fix is fully specified by facts already in the note: single-subspace ⇒ `#origin_d = #reach_d` by S8-depth (with OrdinalShift depth preservation) ⇒ `divergence ≤ #origin_d`. Swapping the content-specific prefix argument for this level-uniformity argument needs no external channel.
