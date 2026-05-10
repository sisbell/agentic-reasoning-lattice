## Question 4 [nelson]

> Must each endpoint of a link identify a specific contiguous span of content, or may an endpoint designate a non-contiguous selection or an entire document?

## An Endset Is an Arbitrary Span-Set, Not a Single Span

Each endpoint of a link — the from-set, the to-set, and the type (three-set) — may be a **non-contiguous collection of spans pointing anywhere in the docuverse**. A single contiguous span is merely the degenerate case.

Nelson is explicit on this point:

> "We see from above that one end of a link may be on a broken, discontiguous set of bytes. This illustrates the endset: a link may be to or from an arbitrary set of bytes. These may be anywhere in the docuverse." [LM 4/42]

> "The from-set may be an arbitrary collection of spans, pointing anywhere in the docuverse. Similarly, the to-set may be an arbitrary collection of spans pointing anywhere in the docuverse. We adopt the same convention for link types." [LM 4/43]

The three endsets are treated symmetrically — all three follow the same convention. The type endset gets the same power as from and to.

## Entire Documents (and Larger Units) Are Valid Targets

An endset can also designate an entire document, an entire account, a server node, or even the whole docuverse. This works through the tumbler span mechanism:

> "A digit of 'one' may be used to designate all of a given version, all versions of a given document, all works of a given author, all documents in a given project, all documents on a given server — or the entire docuverse." [LM 4/38]

> "In fact, a tumbler-span may range in possible size from one byte to the whole docuverse on the whole network." [LM 4/24]

This applies even when nothing is physically stored at the target address (the "ghost element" case):

> "It is possible to link to a node, or an account, even though there is nothing stored in the docuverse corresponding to them." [LM 4/23]

> "A link to or search of an account or node will find any of the documents under it." [LM 4/23]

## Summary

| Question | Answer |
|----------|--------|
| Must an endset be a single contiguous span? | **No.** It is an arbitrary collection of spans. |
| Can an endset be discontiguous? | **Yes.** "A broken, discontiguous set of bytes." |
| Can spans in one endset touch different documents? | **Yes.** "Anywhere in the docuverse." |
| Can an endset designate a whole document? | **Yes.** A single span covering the document's full range. |
| Can an endset designate something larger than a document? | **Yes.** Accounts, servers, the entire docuverse. |
| Are all three endsets treated the same way? | **Yes.** "We adopt the same convention for link types." |
