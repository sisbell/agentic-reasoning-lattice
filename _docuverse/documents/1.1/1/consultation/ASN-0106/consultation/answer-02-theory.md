## Question 2 [theory]

> What relationship must the returned fragments bear to one another — are they ordered, and if so, by what authority does that ordering arise?

I don't have access to the raw page images in this session (only the curated sources), so I'll answer from the verified curated material and flag where raw verification would strengthen the claim.

## Answer: Returned fragments are ordered, and the ordering authority is the *Vstream arrangement*, not physical storage

### The fragments are ordered — by virtual position, not native origin

When the system retrieves content, it returns scattered fragments assembled into a single ordered sequence. The crucial point is that this order is **independent of where the bytes physically live**. Nelson is explicit that logical position is a property of the document's *virtual* byte stream:

> "Logical addressing of the byte stream is in the form of virtual spans, or vspans. These are sequences of bytes in the document's virtual byte stream, regardless of their native origin." (4/11)

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." (4/11)

So even transcluded fragments — bytes living in someone else's document on another server — take their place in the ordering "just as if they were native." The returned material is a contiguous, ordered stream; the fragmentation in Istream is invisible to the result.

### The authority for that ordering: the document's Vstream, controlled by its owner

The document *is* the mapping from virtual positions to permanent (Istream) addresses. Vstream is dense and ordinal (positions 1…N), and that arrangement is what dictates fragment order. Crucially, this arrangement is authored — it arises from editorial operations that only the owner may perform (INSERT, DELETE, REARRANGE):

> "The v-stream addresses of any following characters in the document are increased by the length of the inserted text." (4/66)

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." (4/30)

This is the "part-pounce" experience: the order you see is reconstructed on demand from storage, but the *order itself* comes from the document's arrangement, not from disk layout:

> "the system gives you that part instantly, materializing it for you from the many fragments of its actual storage." (2/16)

> "THE PART YOU WANT COMES WHEN YOU ASK FOR IT." (2/16)

So within a document, the ordering authority is **editorial/ownership-based**: the owner's arrangement of the Vstream determines the sequence, and Istream native order has no say.

### A second ordering authority: the tumbler line (for docuverse-wide spans)

When a request reaches beyond a single document's content — a span or spec-set addressing regions of the address space itself — ordering arises from a different, structural authority: the **tumbler line**, the depth-first traversal of the docuverse tree. Here the order is not authored by anyone; it is *implicit in the addresses*:

> "A span may be visualized as a zone hanging down from the tumbler line — what is called in computer parlance a depth-first spanning tree." (4/25)

> "The first point of a span may designate a server, an account, a document or an element; so may the last point. There is no choice as to what lies between; this is implicit in the choice of first and last point." (4/25)

So for content selected by tumbler spans, the ordering authority is the **canonical depth-first ordering of tumbler-space** — a structural fact of the addressing system, requiring no owner's decision.

### A special case: correspondence returns *ordered pairs*

For version comparison, the relationship between returned items is explicitly ordered as pairs, with the ordering derived from shared Istream origin:

> "This returns a list of ordered pairs of the spans of the two spec-sets that correspond." (4/70)

Here the authority is neither editorial nor purely positional but **structural identity** — two V-positions correspond because they map to the same I-address.

### Summary

| Retrieval context | Are fragments ordered? | Ordering authority |
|---|---|---|
| Content within a document (RETRIEVEV) | Yes — into one contiguous stream | The Vstream arrangement, authored by the owner via editing operations; native Istream order is irrelevant |
| Spans/spec-sets over the address space | Yes | The tumbler line's depth-first spanning-tree order — structural, implicit in the addresses |
| Version correspondence (SHOWRELATIONOF2VERSIONS) | Yes — as ordered pairs | Shared Istream origin (structural identity) |

The unifying principle: **order is a property of arrangement and address, never of physical storage.** Within a document that arrangement is an act of authorship (and thus of ownership); across the docuverse it is the inherent depth-first order of tumbler-space.

---

NEED_RAW: 4/67 (raw p. 234) — to confirm whether the RETRIEVEV command specification *explicitly* states that returned material preserves spec-set/Vstream order, versus this being inferred from the Vstream addressing model (4/11, 4/30). The curated `operations` source gives RETRIEVEV's definition ("returns the material (text and links) determined by <spec set>") but does not, in the extracted text, state the result's ordering guarantee directly.
