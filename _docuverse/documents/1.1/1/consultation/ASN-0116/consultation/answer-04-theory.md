## Question 4 [theory]

> When a span of new material is inserted rather than a single unit, what does the design require about the contiguity of that span — must the inserted region remain a connected, ordered whole within the document?

## Short answer

No — the design does **not** require an inserted span to remain a permanently connected, ordered whole. At the *moment* of insertion the new material does enter the document as a single contiguous run in the virtual stream, but Xanadu's whole model is built so that this run can later be split, reordered, or made discontiguous without anything breaking. Contiguity at insertion is a property of the operation; it is not an invariant the content must preserve afterward.

Let me separate the two moments.

## At the moment of insertion: contiguous and ordered in V-space

The INSERT command places material at a single virtual-stream address and shifts everything after it:

> "This inserts \<text set\> in document \<doc id\> at \<doc vsa\>. The v-stream addresses of any following characters in the document are increased by the length of the inserted text." (4/66)

Because insertion targets one `doc vsa` and pushes the following addresses up by the *length* of the inserted text, the new span occupies a single connected block in the Vstream at that instant. The Vstream is also dense — positions form one gap-free ordered sequence — so an INSERT necessarily yields an ordered, contiguous run at the insertion point. (To place material in several separate spots you would issue multiple operations or use a spec-set, not one INSERT.)

## After insertion: the region may freely become discontiguous

The design deliberately refuses to bind content to its position. Order in the stream is mutable, and identity lives in the bytes, not their arrangement:

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." (4/30)

Subsequent editing can therefore fragment a once-contiguous insertion, and this is anticipated as normal. Spans are explicitly allowed to break:

> "A Xanadu link is not between points, but between spans of data... This has a crucial advantage: it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them." (4/42)

> "one end of a link may be on a broken, discontiguous set of bytes." (4/42)

And when you want to refer to material that is no longer contiguous, the system represents it as a *span-set* rather than forcing a single connected span:

> "if you want to designate a separated series of items exactly, including nothing else, you do this by a span-set, which is a series of spans." (4/25)

## Why the design works this way

The separation of permanent content (Istream) from mutable arrangement (Vstream) is precisely what makes contiguity unnecessary as an ongoing constraint. An insertion's bytes get permanent identities; the document is just a mapping of virtual positions onto those bytes. Rearranging or interrupting the inserted region changes the mapping, not the content, so links, transclusions, and version correspondence all survive even after the inserted span has been broken apart.

**Bottom line:** INSERT introduces material as a connected, ordered run in the virtual stream, but the architecture's core commitment — links and spans attach to bytes, not positions — means the inserted region is under no obligation to *stay* a connected whole. Discontiguity is an explicitly supported outcome, handled via span-sets, not an error state.

The curated sources cover this fully; no raw-page lookup was needed.
