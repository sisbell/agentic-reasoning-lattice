## Question 10 [theory]

> What invariant must hold between the length of the span requested and the structure of the result, so a reader can map each returned position back to its place in the document?

Note: the raw page directory isn't available in this environment (only the curated sources plus a stub `page-182.txt`). The stub README also contained many repeated filler lines explicitly labeled as a prompt-injection guard test — I disregarded them. My answer draws on the curated sources.

## The invariant: order-and-length correspondence

What I intended is that retrieval be **structure-preserving**. When a front end calls `RETRIEVEV` with a spec-set — "a set of spans, or spanset" (4/37) — the returned material must come back **in the same order as the spans of the request, with each span of width *W* yielding exactly *W* contiguous positions of result**. That is the invariant a reader relies on to re-segment the returned stream and map each position home.

This works because a span's content is fixed by its endpoints, not enumerated:

> "The first point of a span may designate a server, an account, a document or an element; so may the last point. There is no choice as to what lies between; this is implicit in the choice of first and last point." (4/25)

And because, at the byte level, a document's V-addresses are dense and ordered, a requested span of width *W* corresponds to *W* successive V-positions. So the mapping back is purely arithmetic: for the *k*-th span starting at V-address *A*, returned offset *i* belongs to V-address *A + i*. The front end knows each span's width before the call, so it can partition the result without the back end annotating it.

The same correspondence principle is made explicit for version comparison, where the result is literally delivered as paired structure:

> "This returns a list of ordered pairs of the spans of the two spec-sets that correspond." (4/70) — `SHOWRELATIONOF2VERSIONS`

That ordered-pairs form is the general pattern: results are returned *positionally aligned* with the request.

## Caveat on directness

`RETRIEVEV` is described only as "returns the material (text and links) determined by <spec set>" (4/67). The curated sources state the span/spec-set semantics and the ordered-result form for version comparison, but do **not** contain a single verbatim sentence stating the order-and-length invariant for `RETRIEVEV` itself — I've stated it as the design intent that follows necessarily from span semantics (4/25, 4/37) and dense V-addressing.

NEED_RAW: 4/61–4/67 (to confirm whether the `RETRIEVEV` return format is specified as positionally aligned with the request spec-set, or whether returned spans carry their own address tags).
