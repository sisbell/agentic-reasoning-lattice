## Question 1 [theory]

> When two regions are transposed, what must be preserved about the identity of the content even though its position within the document changes?

When two regions are transposed (REARRANGE), the content's **Istream identity (I-address) must be preserved**. Only the Vstream position changes; the permanent content address does not.

## What REARRANGE does

REARRANGE is a pure Vstream operation. From the operations reference (4/67):

> "Rearrange transposes two regions of text. With three cuts, the two regions are from cut 1 to cut 2, and from cut 2 to cut 3... With four cuts, the regions are from cut 1 to cut 2, and from cut 3 to cut 4."

This reorders content in the document's *current arrangement* (Vstream) but leaves the underlying content (Istream) untouched.

## What must be preserved: the I-address

Every byte has a permanent Istream address that encodes its identity and origin, distinct from its shifting V-stream position. The V-address is explicitly ephemeral:

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." (4/11)

The document *is* the mapping from V-addresses to I-addresses; rearranging changes the mapping, not the content identity. Nelson states this directly for editorial reordering (4/30):

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them."

## Why this matters: survivability

Because identity is anchored to bytes (I-addresses) rather than positions, links attached to transposed content survive the transposition. From the survivability annotation (4/43):

> "Links between bytes can survive deletions, insertions and rearrangements, if anything is left at each end."

And the underlying principle (4/42):

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes. This has a crucial advantage: it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them."

## Summary

When two regions are transposed:
- **Changes:** the Vstream position (where the content appears in the current document order)
- **Preserved:** the Istream identity (the permanent I-address of each byte), and therefore its origin/home-document traceability and all links "strapped" to it

The transposition rearranges *references* to content, never the content's identity itself — which is exactly why links, attribution, and version correspondence remain intact across a REARRANGE.
