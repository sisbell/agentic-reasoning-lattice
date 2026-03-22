## Question 1 [nelson]

> When content from the permanent storage layer appears in a document's arranged sequence, does link discovery match against the content's original permanent identity or its position in the current arrangement?

## Link discovery matches against permanent Istream identity, not Vstream position.

The evidence from Literary Machines is unambiguous on this point.

### Links attach to bytes, not positions

Nelson explicitly states that links are "to the bytes themselves":

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." [LM 4/30]

And more precisely:

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes." [LM 4/42]

The "strap between bytes" metaphor is critical. The strap attaches to the bytes' permanent identity (Istream address), not to where those bytes happen to sit in the current arrangement (Vstream position). That is the entire basis of link survivability:

> "Links between bytes can survive deletions, insertions and rearrangements, if anything is left at each end." [LM 4/43]

If links matched against Vstream position, they would break on every INSERT (which shifts all subsequent V-addresses). Survivability is only possible because matching occurs against Istream identity, which never changes.

### Endsets map to the permanent address space

Link endsets — the from-set, to-set, and type — map to positions on the universal tumbler line:

> "There is a universal address space, the tumbler line... We may visualize a link's endsets as mapping to it." [LM 4/45]

These are permanent addresses. The endsets are stored as Istream spans, which is why they persist across edits to any document they reference.

### Transclusion makes this consequential

When content from document A appears in document B via transclusion (COPY), it shares the same Istream addresses:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

The FINDDOCSCONTAINING operation exploits this directly — it finds all documents containing particular content by matching on shared Istream origin:

> "This returns a list of all documents containing any of the material specified by the span addresses, regardless of where the native copies are located." [LM 4/63]

So when you search for links FROM a paragraph that was transcluded into your document, the system resolves the V-positions to their underlying I-addresses and searches against those. A link originally made to that content in its home document will be discovered, because the I-addresses match.

### The architectural logic

The separation works like this:

1. **User selects content** — specified as a Vstream range (e.g., "bytes 50–100 in this document")
2. **System resolves to Istream** — the POOM (positional enfilade) maps V→I, yielding the permanent addresses of those bytes
3. **Link search matches on Istream** — FINDLINKSFROMTOTHREE compares the resolved I-addresses against stored link endsets
4. **Results returned** — links whose endsets overlap the queried I-addresses are found, regardless of which documents currently arrange that content or where it sits in their Vstreams

This is why Nelson can guarantee that "a link to one version of a Prismatic Document is a link to all versions" [LM 2/26] — because versions share Istream content, and link discovery matches on that shared identity.

### Summary

Vstream position is ephemeral and user-facing. Istream identity is permanent and system-facing. Links are stored against Istream. Discovery matches against Istream. The front end translates the user's Vstream selections into Istream addresses before searching. This is not an implementation choice — it is the architectural invariant that makes link survivability, version-spanning links, and transclusion-aware discovery possible.
