## Question 8 [theory]

> When content within the region has been edited, what must the endsets in the result reflect about where the links now reside?

## Answer

When content within a region has been edited, the endsets in the result must reflect that the link now attaches to **whatever bytes survive**, at **their current locations** — which may be a **broken, discontiguous set of bytes** rather than a single contiguous span.

The governing principle is that a Xanadu link is anchored to bytes, not positions. Endsets are arbitrary sets of bytes anywhere in the docuverse, and they map to the actual surviving content:

> "We see from above that one end of a link may be on a broken, discontiguous set of bytes. This illustrates the endset: a link may be to or from an arbitrary set of bytes. These may be anywhere in the docuverse." (4/42)

Because the link is a "strap between bytes," editing within the region does not break it — it follows the surviving bytes to wherever they now reside:

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes. This has a crucial advantage: it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them. This also works for alternative versions in which part of each end has survived." (4/42)

The survivability annotation on 4/43 makes explicit which edits the endsets must accommodate:

> "SURVIVABILITY: Links between bytes can survive deletions, insertions and rearrangements, if anything is left at each end." (4/43)

So after an edit within the region:

- **Deletion** of part of an endset's content → the endset reflects only the bytes that remain (it may shrink, or fragment if a middle portion was deleted).
- **Insertion** within the region → the endset still designates the same original bytes; it does not absorb the inserted bytes, so the endset may now describe non-adjacent spans surrounding the insertion.
- **Rearrangement** → the endset reflects the new locations of those bytes, which may now be discontiguous.

In every case, the result is that the endsets describe a **span-set** — potentially several discontiguous spans — locating the link on the surviving bytes wherever they now sit, rather than at any fixed prior position. The link is destroyed only if *all* bytes at an end are removed, leaving nothing to attach to.

This works because endsets are defined against permanent byte identity (Istream addresses) rather than the document's current Vstream positions, which is exactly why the link tracks the content through editing rather than pointing at a now-stale location.
