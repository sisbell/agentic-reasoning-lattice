## Question 7 [theory]

> When a link connects spans of content rather than whole documents, what must the read return about the precise boundaries of each connected region?

## Answer

When a link connects spans rather than whole documents, the read operation (**RETRIEVEENDSETS**) must return the **endsets themselves as span-sets** — that is, the precise from-set and to-set, each given by the exact boundaries (start and end tumblers) of every span it contains.

### Why span boundaries, not whole documents

A Xanadu link attaches to ranges of bytes, not points or document identities:

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes." (4/42)

And crucially, each end may be a *broken, discontiguous* collection of spans, so the read cannot return a single boundary pair — it must return all the spans that make up each endset:

> "We see from above that one end of a link may be on a broken, discontiguous set of bytes. This illustrates the endset: a link may be to or from an arbitrary set of bytes. These may be anywhere in the docuverse." (4/42)

### What the read returns

The retrieval operation returns the endsets:

> "RETRIEVEENDSETS ... This returns a list of all link end-sets that are in <spec set>." (4/70)

Each endset is a span-set, and each span is defined entirely by its two boundary points — the content between them is implicit, not enumerated:

> "The first point of a span may designate a server, an account, a document or an element; so may the last point. There is no choice as to what lies between; this is implicit in the choice of first and last point." (4/25)

A span can be represented either as a pair of tumblers (start + end) or as an address plus a difference tumbler (start + width), per the "Two Representations" described in the spans source (4/24).

### Summary

The read must return, for each connected region, its **precise span boundaries** — the start and extent (as tumbler pairs or address-plus-difference tumblers) of every span in the from-set and to-set. Because endsets are arbitrary, possibly discontiguous span-sets, the read must enumerate *all* spans at each end; the actual bytes within each span are determined implicitly by those boundaries rather than returned as a count.

(Note: the curated sources confirm RETRIEVEENDSETS returns from-set and to-set as span-sets, and that spans are boundary-defined. The exact wire format of the returned tumbler pairs is not given verbatim in the curated material — NEED_RAW: 4/70, 4/64–4/68 if a literal representation of the returned span structure is required.)
