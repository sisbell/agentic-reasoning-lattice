## Question 2 [nelson]

> If a link points to a span of content in the document before the addition, must that link continue to point to exactly the same content afterward?

# Yes — absolutely and by design.

This is one of Xanadu's most fundamental guarantees. A link must continue to point to exactly the same content after any insertion, deletion, or rearrangement. The mechanism is architectural, not incidental.

## Why: Links Point to Content, Not Positions

Links attach to **bytes** (I-space addresses), not to **positions** (V-space addresses). Nelson is explicit:

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes." [LM 4/42]

When you insert content into a document, the V-space positions shift — everything after the insertion point gets renumbered:

> "The v-stream addresses of any following characters in the document are increased by the length of the inserted text." [LM 4/66]

But the link doesn't care about V-space positions. It cares about which bytes it is strapped to, and those bytes haven't changed:

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." [LM 4/30]

## The I-Space / V-Space Separation

This is why the two-address-space architecture exists. I-space addresses are permanent and immutable — a byte's I-address never changes. V-space addresses are ephemeral — they shift with every edit. Links reference I-space, so edits to V-space cannot affect them.

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." [LM 4/11]

The link's endsets resolve to I-space spans. The document's arrangement (V-space) is a separate mapping that can change freely without disturbing any link.

## The Survivability Guarantee

Nelson states the guarantee directly:

> "SURVIVABILITY: Links between bytes can survive deletions, insertions and rearrangements, **if anything is left at each end.**" [LM 4/43]

The only condition for a link breaking is if **all** bytes at one of its endsets are deleted. As long as any referenced bytes remain, the link holds. An insertion — adding new content — cannot remove existing bytes, so it cannot break any link. The link continues to point to exactly the same content it always did.

## Summary

| Operation | V-space effect | I-space effect | Link effect |
|-----------|---------------|----------------|-------------|
| **INSERT** | Positions shift after insertion point | No change — new bytes get new I-addresses | **None** — linked bytes unchanged |
| **DELETE** | Gap closes | No change — bytes remain in I-space | Survives if any endset bytes remain |
| **REARRANGE** | Positions change | No change | **None** — linked bytes unchanged |

The answer to your question is not merely "yes" but "yes, and the entire architecture exists to guarantee this." The separation of I-space from V-space, the span-based (not point-based) link model, and the append-only storage design all converge on this single property: **links follow content, not position.**
