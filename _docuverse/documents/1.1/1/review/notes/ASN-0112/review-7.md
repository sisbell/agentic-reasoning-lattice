# Review of ASN-0112

## REVISE

### Issue 1: Deletion's effect on the span is invoked but never derived — and one case contradicts the naive reading of V8

**ASN-0112, "The origin is permanent..." section (V9/V10)**: V9 asserts the general principle "*changing how much content there is → extent changes*" and explicitly frames the relevant editing primitives as "*Insertion and deletion, by contrast, change O(d)*." But only the insertion direction is formalized — V10 ("insertion monotonicity, content-maximal case") and its proof. The deletion direction is asserted as a consequence and then left underived.

**Problem**: This is not a symmetric mirror that can be left to the reader. The deletion case contains a genuinely non-obvious consequence the note nowhere addresses: if a document with both content and link positions has its **entire content subspace deleted** while links remain (`V_{s_C}(d)` → ∅, `V_{s_L}(d) ≠ ∅`), then `min O(d)` jumps from the content anchor `[s_C,1,…,1]` to the link minimum `[s_L,1,…,1]` — the reported **origin moves**. V8 only guarantees origin permanence "*while the content subspace is non-empty*," so this is precisely the boundary V8 excludes, yet the note never states what the origin becomes when content is cleared but the document is not empty. Likewise, deletion exhibits the same subspace-dependent split V10 makes for insertion (deleting content while links occupy the max leaves reach/extent invariant; deleting in the content-maximal case retreats reach by ordinal steps), none of which is derived. By the standard "claims invoked must be derived" and "consequences not explored," V9's quantity-changes-extent principle is half-proven.

**Required**: Either (a) add a deletion-consequence claim mirroring V10 — covering the content-maximal retreat, the link-maximal invariance, and explicitly the origin-shift when content is fully cleared with links surviving — or (b) remove the deletion framing from V9 so the note does not assert a principle (composition change ⇒ extent change) it only proves in the insertion direction. Option (a) is preferable, since the origin-shift case is a real boundary of V8 that a caller needs.

## OUT_OF_SCOPE

(none to add — the note correctly defers per-subspace exact extents to a span-set operation and marks content delivery, region reads, and link counting out of scope.)

VERDICT: REVISE
