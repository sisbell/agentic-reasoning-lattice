## Question 7 [theory]

> Must the order in which content is delivered honor the order of the spans as asked for, and what guarantee governs the boundaries between one span's content and the next?

I attempted to open the raw page images to verify the protocol details, but no file-reading tool is available in this environment, so I'm limited to the curated sources. Here is what they support, and where the gap lies.

## What the curated sources establish

**RETRIEVEV is the delivery operation, and it acts on an ordered spec-set.**

> "This returns the material (text and links) determined by `<spec set>`." (4/67)

A spec-set is a request set of spans:

> "A request set is a set of spans, or spanset, presented to the back end in the FEBE protocol... The manipulation of request sets is an important aspect of what front-end functions do." (4/37)

**Spans are how non-contiguous selections are expressed, and each span has definite, self-determining boundaries.** A span's extent is fixed by its endpoints, not by a count:

> "The first point of a span may designate a server, an account, a document or an element; so may the last point. There is no choice as to what lies between; this is implicit in the choice of first and last point." (4/25)

> "Note: if you want to designate a separated series of items exactly, including nothing else, you do this by a span-set, which is a series of spans." (4/25)

So at the *addressing* level, each span's content is precisely bounded by its own start and end tumblers — the boundary between one span's content and the next is determined entirely by where each span begins and ends, with nothing implicit added between them.

**One related operation does carry an explicit ordering guarantee** — but it is SHOWRELATIONOF2VERSIONS, not RETRIEVEV:

> "This returns a list of ordered pairs of the spans of the two spec-sets that correspond." (4/70)

## The gap

The curated sources do **not** state whether RETRIEVEV's *delivery order* must honor the order in which the caller listed the spans in the spec-set, nor do they specify a delimiter, marker, or framing guarantee separating one delivered span's bytes from the next. The boundary guarantee I can support is structural (each span is exactly bounded by its endpoints, span-sets include "nothing else"), but whether the protocol guarantees order-preserving, boundary-marked delivery on the wire is not covered.

NEED_RAW: 4/61–4/70 (FEBE command definitions, especially the RETRIEVEV / spec-set delivery semantics on 4/67), and 4/24–4/25, 4/37 (span / request-set handling) to confirm whether Nelson specifies order-preserving delivery and how returned span contents are demarcated.
