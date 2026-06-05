## Question 7 [theory]

> What invariant must hold between a part's reported extent and the actual content a reader would find if they retrieved that part?

## The Invariant: Extent Defines Content by Boundaries, Not by Count

The core invariant is this: **a part's reported extent specifies boundaries (from-to), and the content a reader retrieves is exactly whatever currently lies between those boundaries in the address tree — no more, no less.** The extent is a *designation of a region*, not a promise about quantity. What you get back is precisely the population of that region.

This plays out at two levels, with two strengths of the invariant.

### At the docuverse/tumbler level: content is implicit in the boundaries

A span does not report "how much" is there. It reports *where* the edges are, and the contents are whatever the tree holds between them:

> "A tumbler-span is not a conventional number, and it does not designate the number of bytes contained. It does not designate a number of anything." (4/24)

> "The first point of a span may designate a server, an account, a document or an element; so may the last point. There is no choice as to what lies between; this is implicit in the choice of first and last point." (4/25)

Because the contents are *implicit*, the retrieved material can differ across time while the reported extent stays fixed:

> "A span that contains nothing today may at a later time contain a million documents." (4/25)

So the invariant here is not "extent equals byte count" — it is "extent equals the subtree zone, and retrieval returns exactly that zone's current population." (spans concept, drawing on 4/24–4/25)

### At a document's Vstream level: the invariant tightens to density

Within a single version's virtual byte stream, addressing is **dense and contiguous** — there are no gaps, and the extent's width equals the number of retrievable elements (v-space-addresses: "if you have 100 bytes, you have addresses 1 through 100"). This is what `RETRIEVEDOCVSPAN` reports and `RETRIEVEV` must satisfy:

> "RETRIEVEDOCVSPAN: This returns a span determining the origin and extent of the V-stream of document <doc id>." (4/68)

> "RETRIEVEV: This returns the material (text and links) determined by <spec set>." (4/67)

So for a document part, the invariant is: every position inside the reported extent yields content, and the retrieved content spans exactly the reported extent — origin and width agree with what materializes.

### Transclusion does not break the invariant

Crucially, this holds even when a part includes non-native (transcluded) bytes. Included content occupies ordinal positions in the extent just as native content does:

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document." (4/11)

The reader therefore finds a seamless, fully-populated extent regardless of where the bytes physically live — the home-document origin is preserved, but the extent-to-content correspondence is unbroken.

### The user-facing form of the invariant

Nelson's "part-pounce" guarantee is exactly this invariant stated from the reader's side — what you designate by extent materializes precisely when requested:

> "THE PART YOU WANT COMES WHEN YOU ASK FOR IT." (2/16)

---

**Summary:** The reported extent is a boundary specification; the retrieved content must be exactly the region those boundaries enclose. For a document's Vstream the relationship is dense (width = retrievable element count, with no gaps); for arbitrary docuverse spans the relationship is implicit (content = whatever currently populates the subtree, which is *not* any count). What must never happen is a mismatch where the extent claims a region but retrieval returns something other than that region's actual content.

One caveat on the framing: the curated sources describe spans, dense Vstream addressing, and the retrieval operations, but Nelson does not state this "extent ↔ content" relationship as a single named invariant. The synthesis above is assembled from those pieces. If you want his exact wording around the retrieval/span operations and any stated consistency guarantee, NEED_RAW: 4/24–4/25, 4/37–4/39, 4/66–4/68.
