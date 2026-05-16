## Question 7 [nelson]

> After a link is created, must the system guarantee that retrieving the referenced content will always return the link as part of the retrieval — that is, are links permanently bound to the content they reference?

## Are Links Permanently Bound to Referenced Content?

The answer requires distinguishing two architectural concepts Nelson keeps separate: **link survivability** (do links stay attached to bytes?) and **link retrieval** (does retrieving content automatically return associated links?).

### Links Are Bound to Bytes, Not Positions

Yes, links are permanently attached to the content they reference — specifically, to the **bytes** themselves, not to positions in a document:

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes. This has a crucial advantage: it means that links can survive editing. If any of the bytes are left to which a link is attached, the link remains on them." [LM 4/42]

This binding persists through insertions, deletions, and rearrangements. It breaks only when **all** referenced bytes at an endset are deleted.

### But Retrieval Does NOT Automatically Include Links

Nelson separates content retrieval from link discovery into **distinct FEBE operations**:

- **RETRIEVEV** — returns "the material (text and links) determined by \<spec set\>" [LM 4/67]
- **FINDLINKSFROMTOTHREE** — returns "a list of all links which are (1) in \<home set\>, (2) from all or any part of \<from set\>, and (3) to all or any part of \<to set\> and \<three set\>" [LM 4/69]

The "links" in RETRIEVEV are the document's **own out-links** — links stored in that document. Nelson is explicit about this distinction:

> "Ordinarily a document consists of its contents (including history and alternatives) and its out-links, the links it contains that point to other documents. By contrast, a document's in-links are those stored elsewhere which point to it. These out-links are under control of its owner, whereas its in-links are not." [LM 2/31]

In-links — links made by others pointing TO your content — require a **deliberate query**:

> "The reader should be able to ask, for a given document or place in the document, 'What connects here from other documents?'— and be shown all these outside connections without appreciable delay." [LM 2/46]

This is not automatic inclusion; it is an explicit request with filtering:

> "Thus it becomes necessary to apply some kind of filter, saying, 'What links come in from Spain? From last week? From persons of importance to me?'" [LM 2/47]

### Links Create Permanence Obligations on Content

While links are not returned with content automatically, they do create a binding obligation in the other direction — content **cannot be withdrawn** because links depend on it:

> "It is in the common interest that a thing once published stay published, as in the world of paper. Other readers and users will come to depend on its accessibility. Consequently its author may not withdraw it except by lengthy due process." [LM 2/43]

> "This is vital because of the links other users may have made to it — which can now reach through from the previous version (to which they were originally attached) into the newer version." [LM 2/43]

### Links Themselves Can Be Deleted

The binding is not absolute from the link side. Link owners can delete their own links:

> "DELETED LINKS (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

Even deleted links are not truly destroyed — they remain in Istream, recoverable through historical backtrack.

### Summary

| Question | Answer |
|----------|--------|
| Do links stay attached to referenced bytes? | **Yes** — they survive editing as long as any referenced bytes remain |
| Does retrieving content return all associated links? | **No** — in-links require a separate FINDLINKS query |
| Does a document's own out-links come with retrieval? | **Yes** — out-links are part of the document |
| Can content be withdrawn if others have linked to it? | **No** — links create permanence obligations |
| Are links permanently irrevocable? | **No** — the link owner can delete them (but they persist in Istream) |

The system guarantees that links **survive** as long as referenced bytes exist, and that referenced content **cannot be withdrawn** while links depend on it. But it does **not** guarantee that retrieving content automatically surfaces all links pointing to it — that is a separate, user-initiated discovery operation.
