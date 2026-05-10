## Question 4 [nelson]

> When content is shared into a second document, does editing the original document's structure affect how that content appears in the receiving document?

## No — structural edits to the source do not affect the receiving document

The answer follows directly from Xanadu's two-address-space architecture.

### The mechanism

When Document B transcludes content from Document A, it creates a V-space mapping in B that points to I-space bytes native to A. The COPY operation "shares I-addresses with the source" — B references the same permanent bytes, not A's arrangement of them.

Editing Document A (INSERT, DELETE, REARRANGE) changes only A's V-space — its current arrangement. The I-space bytes are immutable:

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

This is explicit and unambiguous. DELETE removes content from the source's view; transclusions elsewhere are unaffected.

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." [LM 4/30]

While that quote is about links, the same principle applies to transclusions — both reference I-space addresses, not V-space positions.

### Why this works

The separation is fundamental to the design:

- **I-space** (permanent): content lives here forever, addresses never change
- **V-space** (ephemeral): each document arranges its own view over I-space content

Document A rearranging its V-space is like rearranging books on your shelf. Document B holds references to specific books (I-space addresses), not to shelf positions. The books don't move; only the arrangement does.

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." [LM 4/11]

### The two window modes — a nuance

Nelson does describe two windowing modes with different behavior regarding *content updates* (not structural rearrangement):

> "A quotation — an inclusion window — may be fixed to another document in two ways: at a certain point in time, in which case revisions are seen by the user only when he or she asks, 'What has this passage become?' Or second, at a relatively fixed location in the document space, in which case updates are seen automatically." [LM 2/37]

A **time-fixed** window shows content as it was at a specific version — completely insulated from all changes.

A **location-fixed** window tracks a position in the source document's V-space. If the source author publishes a *new version* that reorganizes content around that location, the window could show different content. But this is a front-end presentation choice about *which version to display*, not a back-end change to the transcluded bytes.

### Summary

| Source document operation | Effect on receiving document |
|--------------------------|------------------------------|
| REARRANGE | None — I-space bytes unchanged |
| INSERT new content | None — new bytes have new I-addresses |
| DELETE content | None — bytes remain in I-space and in all transclusions |
| Publish new version | Time-fixed windows: none. Location-fixed windows: may show updated content at that position, depending on front-end resolution |

The design guarantee is clear: transclusion references permanent content identity, not ephemeral arrangement. Structural edits to the source cannot corrupt, break, or alter what the receiving document shows.
