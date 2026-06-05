## Question 10 [theory]

> What invariant must the operation maintain so that reading spans together never alters, reorders, or loses any content compared to the document as it stands?

## The invariant: order-preserving, exact, non-overlapping coverage of the Vstream

The operation that reads spans together (RETRIEVEV over a spec-set) faithfully reproduces the document if and only if the spans, resolved through the V→I mapping and concatenated **in ascending V-address order**, reproduce the document's entire Vstream exactly. Concretely, the invariant has four conjuncts:

1. **Total coverage (no loss).** The union of the read spans must equal the document's full V-extent — from the origin to the extent returned by `RETRIEVEDOCVSPAN`, which "returns a span determining the origin and extent of the V-stream of document `<doc id>`" (4/68). Nothing in the document's Vstream may fall outside the spans read.

2. **No gaps.** Because the Vstream is dense and contiguous, the spans must leave no V-address uncovered. The V-address is just "the byte position in the current ordering of bytes" (4/30) — positions run consecutively, so any missing position is a lost byte.

3. **No overlap / no duplication.** Each V-address maps to exactly one I-address (the V→I mapping is a function). Spans must be pairwise disjoint so no byte is delivered twice.

4. **Order preservation (no reordering).** Reading must respect V-order. The retrieved material is "determined by `<spec set>`" (RETRIEVEV, 4/67), and concatenation in ascending V-address order must equal the document as it stands. Note that V-positions are precisely what editing rearranges, while the underlying I-content is stable — "this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them" (4/30). So fidelity is defined against the *current* V-ordering, not the I-ordering.

## Why this is well-defined

Nelson's span model guarantees such a coverage is always exactly expressible: a span's content "is implicit in the choice of first and last point" —

> "The first point of a span may designate a server, an account, a document or an element; so may the last point. There is no choice as to what lies between; this is implicit in the choice of first and last point." (4/25)

And a disjoint series of spans (a span-set) can name exactly the wanted bytes and nothing else:

> "if you want to designate a separated series of items exactly, including nothing else, you do this by a span-set, which is a series of spans." (4/25)

The V-stream itself is addressed as "virtual spans, or vspans... sequences of bytes in the document's virtual byte stream, regardless of their native origin" (4/11) — so even though bytes may be native or transcluded, they each hold "an ordinal position in the byte stream just as if they were native to the document" (4/11). That single ordinal V-position per byte is what makes the partition condition meaningful.

## In one line

The spec-set must **partition the document's V-extent**: disjoint spans whose union is exactly the full Vstream, delivered in V-order — so concatenating the results yields the document with nothing added, dropped, duplicated, or reordered.

---

NEED_RAW: 4/61–4/68 — Nelson's curated text gives the RETRIEVEV / RETRIEVEDOCVSPAN command semantics but does not state a fidelity/partition invariant in so many words; conjuncts 1–4 above are my synthesis from the span and V-address model. If you want this grounded in Nelson's exact protocol wording for RETRIEVEV and the spec-set, those pages should be checked directly.
