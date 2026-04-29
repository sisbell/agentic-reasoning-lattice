## Question 4 [nelson]

> When content is removed from a document, what must happen to links whose endpoints fall within the removed content?

## Link Behavior When Content Is Removed

The answer has two layers: what happens to the *link itself*, and what happens to the *bytes it points to*.

### 1. The Bytes Are Never Destroyed

DELETE in Xanadu removes content from V-space (the document's current arrangement) but **not** from I-space (permanent storage):

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

The bytes still exist at their permanent I-addresses. They are merely absent from the document's current V-stream.

### 2. Links Point to I-Space, Not V-Space

Links attach to bytes by their permanent identity (I-address), not by their current position (V-address):

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes. This has a crucial advantage: it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them. This also works for alternative versions in which part of each end has survived." [LM 4/42]

Since deletion removes content from V-space but leaves I-space intact, **links whose endpoints fall within removed content still have valid targets**. The I-space bytes are still there; the link's endset still resolves.

### 3. The Survivability Condition

The explicit survivability rule from page 4/43:

> "SURVIVABILITY: Links between bytes can survive deletions, insertions and rearrangements, **if anything is left at each end.**"

In Xanadu's architecture, this condition is *always* met after a DELETE, because DELETE never removes I-space content. The bytes the link points to still exist — they are simply no longer part of the document's current view.

### 4. Where the Linked Content Can Still Be Found

After deletion, the bytes referenced by a link's endset remain accessible through:

- **Previous versions** of the document (historical backtrack)
- **Other documents** that transclude the same I-space content
- **The I-space itself** — the permanent home location

> "The virtual byte stream of a document may include bytes from any other document." [LM 4/10]

### 5. What the Front End Must Handle

Nelson envisions that links made to older versions "reach through" into newer versions:

> "However, for corrections and amendments, the author may readily publish a superseding document, but the former version must remain on the network. This is vital because of the links other users may have made to it — which can now reach through from the previous version (to which they were originally attached) into the newer version." [LM 2/43]

> "When a document is updated, a reader will ordinarily want to see the new version — but the reader may be following a link made to an older version. However, the user's front-end machine may easily be set up to follow the link to the same passage in the most recent version — if it's still there." [LM 2/43]

The front end detects that the linked content no longer appears in the current version and can:
- Show the content from the version where it last appeared
- Navigate to the I-space origin directly
- Indicate to the user that the passage was removed from the current version

### Summary

**Nothing must "happen" to links when content is removed.** This is by design. Links are straps between bytes identified by permanent I-addresses. DELETE only changes V-space arrangement. The linked bytes persist in I-space, in previous versions, and in any documents that transclude them. The link's endsets remain valid. The front end handles presentation — showing the user where the content can still be found — but the link itself is architecturally unaffected.
