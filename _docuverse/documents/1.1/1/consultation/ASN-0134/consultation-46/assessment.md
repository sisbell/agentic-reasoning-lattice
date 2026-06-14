# Channel Assignment — ASN-0134 review-46

**Date:** 2026-06-14 14:52

## Issue 1: Content-run prefixes are claimed "readable," but the formalized read surface exposes no content read
Reason: Internal. The finding is an inconsistency between §1 and the note's own §8, which already commits the modeled read surface to link-store `Observe_K` active-view reads plus link-subspace frontier descents — and §8 (the formalization) is authoritative over §1's prose example. Option (a) ("prefix exposed by no modeled read," content runs non-atomic only structurally) is a statement about the modeled surface, derivable from §8 + A6's mid-batch canonicity; content reads play no role in the note's quiescence/verdict machinery, so nothing motivates the (b) alternative that would require external evidence.

## Issue 2: The `K.σ` shared-frontier conditional is over-introduced and over-repeated
Reason: Internal. Pure restructuring and deduplication of content already present — state the realization conditional once at H3, relocate the registration treatment after H0–H2 as a corollary, and shrink the pre-H0 preamble to the one load-bearing fact (the committed stack carries no document-allocator-conformance invariant). No new facts required.

## Issue 3: G1(i) re-derives the §5 contiguity-vs-uniqueness partition inline
Reason: Internal. Deduplication only — replace G1(i)'s inline re-argument with citations to A6 (per-state package) and W3/§5 (the "contiguity free, uniqueness bought" split), all of which already exist in the note and are forward-referenced there.

## Issue 4: Smaller repetitions to collapse
Reason: Internal. Editorial cleanup of existing text — cut A6's self-undercutting representative-members list, reduce the "states that never coexisted" phrase to its earned occurrence at the V2 trace, and trim the §9 `wp` gloss. No external input needed.
