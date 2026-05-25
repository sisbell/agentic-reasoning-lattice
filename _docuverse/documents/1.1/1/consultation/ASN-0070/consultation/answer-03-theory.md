## Question 3 [theory]

> What is the design's commitment about the form of the resolved result — must it be a contiguous region of visible content, a set of disjoint regions, or something else?

# The Form of Resolved Results

The design commits to **span-sets** — series of spans that may be contiguous OR disjoint. Disjoint resolution is not a degenerate case to be normalized away; it is first-class and architecturally central.

## A single span is contiguous by construction

A span itself, considered as one unit, is contiguous by its very definition. It hangs from the tumbler line as a depth-first spanning tree:

> "A span may be visualized as a zone hanging down from the tumbler line — what is called in computer parlance a depth-first spanning tree." (4/25)

> "The first point of a span may designate a server, an account, a document or an element; so may the last point. There is no choice as to what lies between; this is implicit in the choice of first and last point." (4/25)

So if you specify start and end tumblers, what lies between is structurally determined — contiguous in the tree, contiguous along the tumbler line.

## But the system's fundamental currency is the span-SET

For anything more than a single contiguous range, the design uses **span-sets** (or "spec-sets"):

> "Note: if you want to designate a separated series of items exactly, including nothing else, you do this by a span-set, which is a series of spans." (4/25)

> "A request set is a set of spans, or spanset, presented to the back end in the FEBE protocol... The manipulation of request sets is an important aspect of what front-end functions do." (4/37)

## Disjoint results are explicit, not exceptional

This is most visible in the design of endsets. One end of a link may sit on broken, scattered bytes:

> "We see from above that one end of a link may be on a broken, discontiguous set of bytes. This illustrates the endset: a link may be to or from an arbitrary set of bytes. These may be anywhere in the docuverse." (4/42)

> "The from-set may be an arbitrary collection of spans, pointing anywhere in the docuverse. Similarly, the to-set may be an arbitrary collection of spans pointing anywhere in the docuverse. We adopt the same convention for link types." (4/43)

> "ENDSETS MAY POINT TO SPANS ANYWHERE IN THE DOCUVERSE" (4/45)

## Why I designed it this way

Three reasons make disjoint resolution essential:

**1. Links must survive editing.** If a link attaches to a span and editing inserts content into the middle, what was contiguous becomes split. The link must still resolve — to a span-set whose pieces are no longer adjacent.

> "Links between bytes can survive deletions, insertions and rearrangements, if anything is left at each end." (4/43)

**2. Meaningful connections cross fragmentation.** A critique that touches three separate passages is one connection, not three. The from-set is naturally a span-set.

**3. Resolved content reflects how documents are actually composed.** A document's Vstream is assembled from native bytes plus inclusions from elsewhere. When you resolve a region, the bytes come from wherever they live:

> "The virtual byte stream of a document may include bytes from any other document." (4/10)

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." (4/11)

## What this means for FEBE results

The protocol commands operate on and return span-sets, not single ranges:

- **RETRIEVEV** is "determined by <spec set>" — the request itself is a set of spans
- **SHOWRELATIONOF2VERSIONS** returns "a list of ordered pairs of the spans of the two spec-sets that correspond" (4/70) — pairs, plural, since correspondence is rarely one contiguous chunk
- **RETRIEVEENDSETS** returns endsets, which are themselves span-sets
- **FINDDOCSCONTAINING** returns "a list of all documents containing any portion of the material" — necessarily a set, since the material may be scattered

## The commitment, stated plainly

The system does NOT promise that a resolved result is one visible contiguous region. It promises that the result is a span-set — a series of spans that together designate exactly the content addressed, no more and no less. The number of spans in that set is whatever the structure of the request and the state of the docuverse make it. A span-set may contain one span (the contiguous case), many spans (the disjoint case), or — though Nelson allows it — zero spans:

> "A span that contains nothing today may at a later time contain a million documents." (4/25)

A tumbler-span "does not designate the number of bytes contained. It does not designate a number of anything" (4/24) — it designates a region of the docuverse, and what that region contains is determined by the docuverse itself, not by the request.

NEED_RAW: 4/66-4/67 (exact return format of RETRIEVEV — whether it flattens to a byte stream or preserves the span-set structure in the response). Curated sources confirm spec-sets are the request form but don't pin down whether returned material preserves span boundaries or is concatenated for delivery.
