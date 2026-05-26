## Question 1 [nelson]

> When existing content is placed at a position in a document, is the result a reference to the same content or a new independent copy of it?

## A Reference — Always a Reference

When you place existing content at a position in a document, the result is a **reference to the same content**, not a new independent copy. This is the entire point.

The COPY operation in FEBE creates a new Vstream mapping that points to the **same Istream addresses** as the original. No new bytes are created in permanent storage. The document's virtual byte stream simply includes a reference to bytes that already exist elsewhere:

> "The virtual byte stream of a document may include bytes from any other document." [LM 4/10]

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

The placed content **appears** as part of your document — it has an ordinal position in your byte stream "just as if" it were native. But it is not native. It is fetched from its home location when needed. The connection to the original is structural and permanent.

### Why This Matters

This is not a minor implementation detail. It is the architectural foundation that makes everything else work:

1. **Attribution is automatic.** Because the placed content retains its original I-address, you can always trace it back to its home document. "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

2. **Royalties flow correctly.** The original author gets paid when their bytes are delivered, regardless of which document arranges them. "If a modified document is read, the original owner and the modifier split the royalty in proportion to who wrote what, as determined automatically." [LM 2/45]

3. **No copying means no divergence.** "No copying operations are required among the documents throughout the system, and thus we solve the problems of update — especially the problem of updating documents which depend on other documents." [LM 2/36]

4. **Correspondence is computable.** When two documents share Istream content, the system can identify which parts correspond — enabling version comparison, intercomparison, and refractive link following.

### The Two Operations Compared

| | INSERT | COPY |
|---|---|---|
| **Creates new Istream content?** | Yes | No |
| **Adds to Vstream arrangement?** | Yes | Yes |
| **Content identity** | New I-addresses | Shares source I-addresses |
| **Relationship to source** | None (fresh bytes) | Structural reference |

INSERT is how you create original content. COPY is how you include existing content. The distinction maps directly to the Istream/Vstream separation: INSERT adds to both; COPY adds only to Vstream.

### The Metaphor

> "Think of the present document as a sheet of glass. It may have writing painted on it by the present author; it may have clear glass, windowing to something else; the next pane may be in turn made of more layers of painted glass, with more windows, and so on indefinitely." [LM 2/34]

Painted content (INSERT) is yours — new bytes at your I-address. Clear glass (COPY) is a window through to someone else's bytes at their I-address. The reader sees one coherent document. But the system knows exactly which bytes are native and which are inclusions.

### What a "Copy" Loses

If someone were to make an actual independent copy — extracting bytes and re-storing them as new content — they would sever every connection that makes Xanadu valuable:

> "Note also that he or she who makes a paper copy or disk is losing all dynamic link connections, and is left with the inert, non-interactive copy. And that will be a considerable deprivation in the world we are talking about." [LM 2/48]

The live reference participates in the network. The dead copy does not.

### Delete Does Not Destroy the Reference

Even if the placing document "deletes" the included content from its current version, the original bytes remain in Istream:

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

The reference can be severed from a particular Vstream arrangement, but the underlying content is permanent and other arrangements that include it are unaffected.

---

**In short:** Xanadu has no mechanism for duplicating content within the system. What looks like "placing content" is always the creation of a new view — a Vstream arrangement — over content that exists once and forever in Istream. The word "copy" in COPY is perhaps unfortunate; "include" or "transclude" better captures what actually happens. The bytes do not move. The bytes do not multiply. A new finger simply points at them.
