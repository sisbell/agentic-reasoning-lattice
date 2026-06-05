## Question 3 [theory]

> Must the combined result preserve the document's own arrangement, so that fragments appear in the sequence the document defines rather than the sequence requested?

I don't have file-read access in this session (only the curated sources and MCP auth tools are available), so I'll answer from the verified curated material and flag where verification against raw pages is needed.

## Answer

**The principled answer is yes — the document's own arrangement is canonical, so a combined retrieval should present fragments in the sequence the document (Vstream) defines, not in the order the request happened to list them.** But I want to be precise about what the curated sources establish directly versus what follows by inference.

### What the sources establish directly

**1. The document defines a definite sequence (Vstream), and it is dense and ordered.**

From `i-space-addresses` / `v-space-addresses`: the Vstream is "the document's current arrangement of content" — V-addresses "always form a contiguous sequence starting at 1," and "V-address 1 is always the first byte of the document right now." The document *is* the mapping from V-positions to I-positions, so the document itself supplies the authoritative order.

**2. Within a span, ordering is not the caller's to choose — it is implicit in the address structure.**

Nelson is explicit that a span's contents are determined by its endpoints, not enumerated or ordered by the requester:

> "The first point of a span may designate a server, an account, a document or an element; so may the last point. There is no choice as to what lies between; this is implicit in the choice of first and last point." (4/25)

And the tumbler line itself is a fixed canonical (depth-first) ordering of the tree:

> "A span may be visualized as a zone hanging down from the tumbler line--what is called in computer parlance a depth-first spanning tree." (4/25)

So content has a canonical position on the tumbler line / in the Vstream that exists independently of any request.

**3. RETRIEVEV is defined purely by *what* is designated, not by request order.**

From `operations`:

> "RETRIEVEV: This returns the material (text and links) determined by <spec set>." (4/67)

The operation is specified as returning the material *determined by* the spec-set — i.e., the designated content — with no notion of carrying request sequence through to the output.

### The inference

Because (a) the content's order is fixed by the Vstream/tumbler line and is "implicit in the choice of first and last point," and (b) a spec-set is just a set of spans designating *which* content, the natural and consistent reading is that a combined result is delivered in the document's canonical order. The request set selects content; it does not redefine the document's arrangement. This is reinforced by the enfilade design goal that "all changes, once made, left the file remaining in canonical order" (`enfilades`, 1/34) — canonical order is an internal invariant of the storage, not something a query reorders.

### Where I must flag a gap

The curated sources do **not** contain an explicit statement that RETRIEVEV (or COPY, which inserts at a target) re-sorts or guarantees document-order output when a spec-set lists spans out of order, nor do they explicitly forbid request-order output. The conclusion above is an inference from the span/tumbler canonical-order principle, not a verbatim guarantee.

NEED_RAW: 4/66–4/67 (RETRIEVEV and COPY definitions — to confirm whether Nelson states result ordering follows document/Vstream order vs. request order), and 4/37–4/39 (request-set / spanset manipulation, to check for any explicit ordering statement).
