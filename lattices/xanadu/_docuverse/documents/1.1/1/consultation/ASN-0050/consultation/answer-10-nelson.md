## Question 10 [nelson]

> When content is removed from a document, must the system preserve enough information for any holder of a link to the removed content to discover both that the content once appeared in that document and where the content still resides?

## Yes — and this falls out structurally from multiple interlocking guarantees

Nelson does not state this as a single explicit guarantee, but the system's architecture makes it unavoidable. Three mechanisms combine to ensure that a link holder can always discover both that content once appeared in a document and where it still resides.

### 1. The content is never destroyed

DELETE in Xanadu removes content from V-space (the document's current arrangement) but never from I-space (permanent storage). Nelson's diagram on page 4/9 shows "DELETED BYTES" as a valid system state:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

And explicitly:

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

Since I-space is append-only, the bytes a link points to **always exist**. The link never loses its target.

### 2. The link itself always survives

Links attach to I-space bytes, not V-space positions. A link doesn't care whether the bytes currently appear in any document's V-stream — it cares only that the bytes exist in I-space:

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes. This has a crucial advantage: it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them." [LM 4/42]

Since DELETE never removes I-space bytes, "anything is left at each end" is always true after a V-space deletion. The link survives unconditionally.

### 3. The I-address encodes where the content resides

Every byte's permanent I-address has the form `Node.0.User.0.Document.0.Element` [LM 4/26]. The Document field directly encodes which document originally created that byte. A link holder can inspect the I-address of the bytes their link points to and immediately determine the home document.

> "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

This is structural, not metadata:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

### 4. Historical backtrack reveals past presence

Previous versions of the document still contain the deleted content in their V-streams. The system preserves the complete version history:

> "The file management system we are talking about automatically keeps track of the changes and the pieces, so that when you ask for a given part of a given version at a given time, it comes to your screen." [LM 2/15]

So a link holder can reconstruct that the content *was* in document D by examining D's version history.

### 5. FINDDOCSCONTAINING locates current appearances

The FEBE operation FINDDOCSCONTAINING lets you find all documents that currently include specific content:

> "This returns a list of all documents containing any of the material specified by the span addresses, regardless of where the native copies are located." [LM 4/63]

A link holder can use their link's I-space target to query for every document that currently transcludes that content — discovering not just the home document but everywhere the content appears *right now*.

### Two cases worth distinguishing

**Native content** (bytes created in document D, then deleted from D's V-stream): The I-address encodes D as home. The bytes are still physically stored under D's control. Previous versions of D show the content. The link resolves directly to D's I-space.

**Transcluded content** (bytes from document E, included in D, then removed from D's V-stream): The I-address encodes E as home. The content still exists at E. Previous versions of D show the transclusion. FINDDOCSCONTAINING finds E and any other documents still transcluding it.

### Summary

The answer is **yes**, and it is not a separate guarantee but an emergent consequence of three structural properties: I-space permanence (content is never destroyed), I-address encoding (origin is always readable from the address), and historical backtrack (all previous arrangements are reconstructible). A link holder's link always resolves, always reveals the content's home document, and can always be used to find every document that currently contains that content.
