## Question 7 [theory]

> What permanence guarantee governs the reported span, given that the document's content may be shared with or referenced by other documents?

## Permanence Guarantee for a Shared/Referenced Span

The governing guarantee is **Istream permanence**: the bytes a span reports live at permanent Istream (I-stream) addresses that never change and are never destroyed. Because a span attaches to *content* (bytes identified by their permanent I-addresses), not to positions, the reported span survives regardless of how the content is shared, transcluded, or edited elsewhere.

### Why sharing strengthens, rather than weakens, the guarantee

When content is transcluded into other documents, "deletion" by the originating owner does **not** destroy it. Nelson is explicit that deleted bytes persist precisely because they may be included elsewhere:

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." (4/11)

The architecture treats "deleted" bytes as a valid, recoverable state rather than destruction:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" (4/9)

So a span pointing to shared content keeps resolving: even if removed from the current Vstream of its home document, the bytes remain in Istream and in any document that transcludes them.

### Transclusion is reference, not copy

Shared content is included by reference. Non-native bytes are fetched from their home location, so the connection (and thus the span's target) is structural and permanent:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." (4/11)

> "Non-native bytes are as much a logical part of a document as native bytes." (4/11)

### Span survivability under editing

Because a span/link binds to bytes rather than positions, it persists through insertion, deletion, and rearrangement as long as any referenced bytes remain — and this holds across the alternative versions that sharing produces:

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes. This has a crucial advantage: it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them. This also works for alternative versions in which part of each end has survived." (4/42)

> "Links between bytes can survive deletions, insertions and rearrangements, **if anything is left at each end.**" (4/43)

### The permanent-address backbone

This all rests on the permanence of tumbler/Istream addressing:

> "New items may be continually inserted in tumbler-space while the other addresses remain valid. This means that any address of any document in an ever-growing network may be specified by a permanent tumbler address." (4/19)

### Summary

A reported span is governed by the **permanence of Istream content addressing**: its target bytes are immutable, never destroyed, and remain resolvable even after the originating owner "deletes" them — because the same bytes persist in Istream and in every other document that has referenced or transcluded them. Sharing therefore does not threaten the span; it is exactly the condition under which Istream permanence and the "if anything is left at each end" survivability rule keep the span valid.
