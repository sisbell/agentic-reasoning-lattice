## Question 7 [nelson]

> Does the act of adding content to a document affect any other document that shares or includes spans from the modified document?

## No. Adding content to a document does not affect any other document.

This follows directly from the I-space/V-space separation, which is the architectural core of Xanadu.

### Why INSERT/APPEND Cannot Affect Other Documents

**INSERT creates new bytes in I-space with new, unique I-addresses.** Existing bytes — including those transcluded by other documents — retain their permanent I-addresses unchanged.

> "This inserts \<text set\> in document \<doc id\> at \<doc vsa\>. The v-stream addresses of any following characters in the document are increased by the length of the inserted text." [LM 4/66]

The V-stream address shift is **local to the modified document only**. Other documents have their own independent V-space arrangements pointing to specific I-addresses. Those mappings are untouched.

### The DELETE Case Confirms This By Analogy

Nelson is explicit that even the more disruptive operation — deletion — does not propagate:

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

If deletion from V-space doesn't affect other documents' transclusions, addition to V-space certainly cannot.

### The Architectural Reason

Each document's V-space is an **independent mapping** over shared I-space content:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

When document B transcludes content from document A (via COPY), B's V-space records references to specific I-addresses. Those I-addresses are permanent and immutable. Nothing document A does to its own V-space arrangement — inserting, deleting, rearranging — changes the I-space content that B references.

```
Document A (before INSERT):     Document B (transcludes from A):
V-space: [I₁, I₂, I₃]          V-space: [I₂, I₃]

Document A (after INSERT at position 2):
V-space: [I₁, I_new, I₂, I₃]   Document B: still [I₂, I₃]
                                  ↑ completely unaffected
```

### The Window Nuance

Nelson does describe a "location-fixed" windowing mode where a window tracks a position in a changing document, showing whatever is currently there:

> "A quotation—an inclusion window—may be fixed to another document in two ways: at a certain point in time, in which case revisions are seen by the user only when he or she asks, 'What has this passage become?' Or second, at a relatively fixed location in the document space, in which case updates are seen automatically." [LM 2/37]

In this mode, what the **window displays** could change if the source document is edited. But this is about the window's **rendering behavior** — what it chooses to show — not about the transcluding document's content being modified. The transcluding document's own V-space mapping and I-space references remain unchanged. The location-fixed window is a front-end presentation concern, not a structural modification to the transcluding document.

### Summary

Adding content to a document:
- Creates new I-addresses (new bytes)
- Shifts V-addresses **within that document only**
- Does **not** alter any I-addresses referenced by other documents
- Does **not** modify any other document's V-space mapping
- Does **not** affect link endsets pointing to the modified document's content

This isolation is not incidental — it is the entire purpose of the I-space/V-space separation. Content identity (I-space) is permanent; content arrangement (V-space) is per-document and independent.
