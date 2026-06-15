# Channel Assignment — ASN-0134 review-52

**Date:** 2026-06-14 18:49

## Issue 1: §3's first two paragraphs duplicate each other
Reason: Internal — this is pure deduplication of two paragraphs that both state "program order is not preserved" and repeat the same ≺-incomparable distinct-home sentence already formalized in G0's box. Collapsing them requires only the note's own content; no design intent or implementation evidence bears on which redundant copy to drop.

## Issue 2: A6 pre-establishes the preservation arguments; §5's W0/W1 re-derive them, with placement meta-prose
Reason: Internal — the fix is to cite A6 rather than re-derive its gaplessness/monotonicity preservation argument and to delete document-placement meta-prose. Every piece W0/W1 should retain (the collision-not-hole failure mode, the Gregory counter-style-allocator contrast, the "needs only A0" classification) is already present in the note, so no new evidence from either channel is required.

## Issue 3: W1's recurrence "inc(slot φ, 0) = slot φ+1" overloads φ and reads as off-by-one
Reason: Internal — the correct recurrence follows from §4's own binding (φ_S = |P_S|, next emission at chain slot φ) and the inc(max,·) allocator the note already describes; the review specifies all three acceptable rewrites. Fixing the notation is a consistency repair against the note's own definitions, needing neither design intent nor implementation evidence.

## Issue 4: §2 over-restates the canonical-vs-settled point
Reason: Internal — keeping the relation-not-property formulation plus the two examples and trimming the two echo sentences is a pure editorial judgment about redundant prose within the note; nothing about Nelson's intent or Gregory's code is at stake in deciding which restatements are echoes.
