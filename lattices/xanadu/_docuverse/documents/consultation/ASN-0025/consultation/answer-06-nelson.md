## Question 6 [nelson]

> Do links depend on address stability — that is, must a link's endpoint address continue to reach the same content regardless of what editing has occurred around it?

# Yes — and the architecture guarantees it structurally

Links depend on **I-space address stability**, which is absolute and immutable by design. They do **not** depend on V-space address stability, which is explicitly ephemeral. This is the central architectural insight that distinguishes Xanadu links from web hyperlinks.

## The two address spaces

Link endsets point to bytes identified by their permanent I-space addresses. Editing only changes V-space — the document's current arrangement of content. I-space content never moves, never changes, never gets overwritten.

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." [LM 4/30]

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." [LM 4/11]

The V-address changes constantly during editing. The I-address never changes. Links point to I-addresses.

## Links as straps between bytes

Nelson visualizes links not as arrows between positions but as physical straps binding specific bytes:

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes. This has a crucial advantage: it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them. This also works for alternative versions in which part of each end has survived." [LM 4/42]

The "strap" metaphor is precise. A strap binds to the thing itself, not to where the thing happens to be sitting. Move the thing — the strap goes with it. Rearrange the shelf — the strap doesn't care.

## What editing does and does not affect

| Operation | V-space effect | I-space effect | Link effect |
|-----------|---------------|----------------|-------------|
| **INSERT** | Shifts V-addresses after insertion point | New bytes get new I-addresses | None — existing I-addresses untouched |
| **DELETE** | Removes V-space mapping | None — bytes remain in I-space | None — link still points to I-space bytes |
| **REARRANGE** | Changes V-address ordering | None | None |
| **COPY** (transclusion) | New V-space mapping to existing I-content | None | None |

The survivability guarantee from page 4/43 states it plainly:

> "SURVIVABILITY: Links between bytes can survive deletions, insertions and rearrangements, **if anything is left at each end.**" [LM 4/43]

## The only way to break a link

A link fails only when **all** bytes at one endset are deleted from every V-space view. Even then, the I-space content still exists — the bytes are merely "not currently addressable, awaiting historical backtrack functions, may remain included in other versions" [LM 4/9]. The link still structurally points to real I-space content; it's just that no current document arrangement exposes those bytes.

## Cross-version stability

This architecture also enables links to work across versions:

> "Links may be refractively followed from a point or span in one version to corresponding places in any other version. Thus a link to one version of a Prismatic Document is a link to all versions." [LM 2/26]

Because versions share I-space content, a link made against version 1 automatically reaches the same content in version 5 — the system traces correspondence through shared I-addresses.

## Summary

The answer to your question is **yes, by construction**. A link's endpoint address always reaches the same content because:

1. Endsets point to I-space addresses
2. I-space addresses are permanent and immutable
3. Content at an I-space address never changes
4. Editing only modifies V-space (the arrangement)
5. Therefore no editing operation can cause a link's endpoint to reach different content

This is not a feature of the link mechanism — it is a consequence of the address space design. Nelson separated content identity (I-space) from content arrangement (V-space) precisely so that links, citations, and transclusions would be immune to editing. The address stability that links depend on is the deepest invariant in the system.
