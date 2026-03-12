## Question 1 [nelson]

> What does a link actually connect — whole documents, specific spans of content within documents, or both?

# What Does a Link Connect?

**Both.** A link connects **arbitrary span-sets** — which can be specific byte ranges within documents, whole documents, or even collections spanning multiple documents. The mechanism is unified; there is no separate "document link" vs "span link."

## The Core Mechanism: Spans, Not Points

Nelson is explicit that links are not point-to-point:

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes." [LM 4/42]

Each link has three endsets (from-set, to-set, type), and each endset is an **arbitrary collection of spans**:

> "The from-set may be an arbitrary collection of spans, pointing anywhere in the docuverse. Similarly, the to-set may be an arbitrary collection of spans pointing anywhere in the docuverse." [LM 4/43]

> "We see from above that one end of a link may be on a broken, discontiguous set of bytes. This illustrates the endset: a link may be to or from an arbitrary set of bytes. These may be anywhere in the docuverse." [LM 4/42]

A single endset can touch bytes scattered across multiple documents. This is the general case.

## Whole-Document Links: Metalinks

Nelson explicitly addresses whole-document linking through **metalinks**:

> "METALINKS: These are links expected to apply to whole documents, whether from outside or from inside." [LM 4/52]

Examples include Title links (from title text to the whole document), Author links (from author name to the whole document), and Supersession links (declaring one document replaces another). These use the same link mechanism — the endset simply spans the entire document rather than a fragment within it.

## The Scale Is Continuous

The span mechanism makes the scale continuous, from one byte to the entire docuverse:

> "A digit of 'one' may be used to designate all of a given version, all versions of a given document, all works of a given author, all documents in a given project, all documents on a given server--or the entire docuverse." [LM 4/38]

> "In fact, a tumbler-span may range in possible size from one byte to the whole docuverse on the whole network." [LM 4/24]

So a link's from-set could be a single word, a paragraph, a chapter, a whole document, or every document on a server — all using the same addressing and search machinery.

## Why This Matters

This design yields **link survivability**. Because links attach to bytes (via I-space addresses), not to positions:

> "This has a crucial advantage: it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them. This also works for alternative versions in which part of each end has survived." [LM 4/42]

If links connected only whole documents, survivability would be trivial but the link would lack precision. If links connected only single points, they would be fragile. Span-based linking gives both precision and resilience — the strap stays attached to whatever bytes remain.

## Summary

A Xanadu link connects **span-sets to span-sets**, where each span-set can be:
- A single byte
- A contiguous passage
- A discontiguous collection of passages across multiple documents
- An entire document
- An entire account or server's worth of content

There is one mechanism, not two. Metalinks (whole-document links) are simply links whose endsets happen to span entire documents.
