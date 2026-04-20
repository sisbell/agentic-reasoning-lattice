## Question 7 [nelson]

> Must the source document from which the content originates remain completely unaffected by the placement into a different document?

## Yes — Absolute Non-Modification of the Source

This is one of the most emphatically stated guarantees in Literary Machines. The source document must remain completely unaffected when its content is placed into another document. Nelson states this principle repeatedly from multiple angles.

### The Explicit Guarantee

> "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate—**without damaging the originals**. This is done by inclusion links." [LM 2/45]

This is not qualified. "Without damaging" means without any modification whatsoever to the source.

### Why It's Structurally Impossible to Affect the Source

Transclusion works by **reference**, not copy. The destination document's Vstream creates a mapping to the source's Istream content. No operation touches the source document:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

> "The virtual byte stream of a document may include bytes from any other document." [LM 4/10]

The COPY operation in FEBE inserts a Vstream mapping *in the destination*. The source is read, never written.

> "No copying operations are required among the documents throughout the system, and thus we solve the problems of update—especially the problem of updating documents which depend on other documents." [LM 2/36]

### Ownership Forbids It

Even if the system *could* modify the source, ownership rules would prohibit it:

> "Every document has an owner, the person who created and stored it... Only the owner has a right to withdraw a document or change it." [LM 2/29]

If Bob transcludes from Alice's document, Bob has no authority to modify Alice's document, and the system provides no mechanism by which his transclusion could do so.

### Even In-Links Don't Touch the Source

One might ask: does the *link* created by transclusion modify the source? No. Nelson explicitly separates in-links from the document itself:

> "Ordinarily a document consists of its contents (including history and alternatives) and its out-links, the links it contains that point to other documents. By contrast, a document's in-links are those stored elsewhere which point to it. These out-links are under control of its owner, whereas its in-links are not." [LM 2/31]

The transclusion link lives in the *destination* document (or wherever the link creator places it). The source document's contents are untouched.

### The Reverse Also Holds

Remarkably, even when the source owner *deletes* content from their own document, the transcluding document is unaffected:

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

This is because deletion only removes Vstream mappings; Istream content is permanent. Both documents operate independently on their own Vstreams over shared Istream content.

### The Glass Pane Metaphor

Nelson's metaphor captures the non-interference precisely:

> "Think of the present document as a sheet of glass. It may have writing painted on it by the present author; it may have clear glass, windowing to something else; the next pane may be in turn made of more layers of painted glass, with more windows, and so on indefinitely." [LM 2/34]

You see *through* to the source. Looking through glass does not change what is on the other side.

### Summary

The source document is unaffected in every dimension:
- **Content**: No bytes added, removed, or rearranged
- **Vstream**: No mappings changed
- **Istream**: Immutable by definition
- **Out-links**: Unchanged (transclusion links live elsewhere)
- **Ownership**: Unchanged
- **Version history**: Unchanged

The only effect is *economic*: the source owner's cash register increments when transcluded content is delivered to readers, generating royalty. But that is accounting metadata external to the document, not a modification of the document itself.
