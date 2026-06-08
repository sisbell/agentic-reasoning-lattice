## Question 6 [theory]

> What must happen to a link anchored to content that a document's arrangement no longer includes after a deletion?

## The link survives — it stays attached to the bytes in Istream

The short answer: **nothing destructive happens to the link.** A deletion removes content only from a document's *Vstream* (its current arrangement), not from *Istream* (where the bytes permanently live). Because Xanadu links attach to bytes — addressed in Istream — rather than to positions in the current arrangement, the link remains attached to those bytes even when the current version no longer displays them.

### Why deletion doesn't break the link

Nelson designed links as "straps between bytes," not pointers to positions:

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes. This has a crucial advantage: it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them. This also works for alternative versions in which part of each end has survived." (4/42)

The survivability rule, stated as a visual annotation on page 4/43:

> "SURVIVABILITY: Links between bytes can survive deletions, insertions and rearrangements, **if anything is left at each end.**" (4/43)

### What "deletion" actually does

A DELETE operation removes content from the Vstream view but leaves the Istream bytes intact. Nelson's own diagram (4/9) labels deleted content as a valid system state:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" (4/9)

So the deleted bytes are merely "not currently addressable" *in that document's current arrangement* — they persist in Istream, in prior versions, and in any other documents that transclude them. The link's endset still resolves to those bytes.

### The reader's experience

Because the content still exists, a link made to it continues to resolve. Nelson describes how a front end handles the case where content has moved between versions:

> "When a document is updated, a reader will ordinarily want to see the new version—but the reader may be following a link made to an older version. However, the user's front-end machine may easily be set up to follow the link to the same passage in the most recent version—if it's still there." (2/43)

### The one case where a link does NOT survive

The qualifier "if anything is left at each end" is the boundary condition: a link breaks **only when *all* bytes at one of its endsets are deleted** so that nothing remains to attach to. Removing content from a single document's arrangement does not meet that bar, because the bytes still live in Istream. (See `Design Intent/link-survivability.md` and `Design Intent/delete-semantics.md`.)

### Summary

| Operation | Effect on the link |
|-----------|-------------------|
| Content removed from a document's Vstream (deletion) | Link **survives** — bytes remain in Istream; content stays in prior versions/transclusions |
| Front-end follow of the link | Resolves to Istream; can be pointed to the same passage in the current version "if it's still there" (2/43) |
| *All* bytes at an endset destroyed everywhere | Link no longer has anything to attach to at that end |

The arrangement no longer including the content is not destruction — it is a Vstream change. The link is anchored to the permanent bytes, so it persists.
