# Channel Assignment — ASN-0134 review-21

**Date:** 2026-06-14 02:53

## Issue 1: §7's nesting vignette contradicts the H1 proof on whether the anchor argument distinguishes nesting-home deposits
Reason: Pure internal-consistency fix. The H1 proof in §4 already contains both the separator/anchor argument and the correct motivation (origin is general because it covers the cross-subspace cross-document case); the concrete anchors for the nesting pair are computable from the note's own address definitions. §7 must simply be brought into line with H1 — no design intent or implementation evidence is in play.

## Issue 2: H3(b)'s commutation is mislabeled "disjoint-write"
Reason: Pure internal-correctness fix. The K.σ effect on `dom(M)` (membership-test precondition plus insertion) and the freshness hypothesis are both already stated in the note; recharacterizing (b)'s commutation as shared read-write commuting by distinct-element non-interference is derivable from that content alone.
