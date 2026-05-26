## Question 3 [nelson]

> If the same content appears in multiple documents through sharing, does inserting into one document's stream affect the position or appearance of that shared content in any other document?

## No. Insertion into one document's stream does not affect shared content in any other document.

This is a direct consequence of the Istream/Vstream separation.

### Each document has its own independent Vstream

When content is shared between documents (via COPY/transclusion), both documents' Vstreams contain mappings that point to the same Istream bytes. But the Vstreams themselves are completely independent structures.

INSERT is explicitly scoped to a single document:

> "This inserts \<text set\> in document \<doc id\> at \<doc vsa\>. The v-stream addresses of any following characters **in the document** are increased by the length of the inserted text." [LM 4/66]

The phrase "in the document" is the key constraint. Only the target document's V-addresses shift. Every other document's Vstream is untouched.

### Istream content is immutable

INSERT creates **new** Istream bytes and weaves them into the target document's Vstream. It does not modify existing Istream content. The shared bytes remain at their permanent I-addresses, unchanged:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

The I-address of shared content never changes. No operation on any document can alter what lives at an I-address.

### Nelson confirms this explicitly for DELETE (the parallel case)

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

If DELETE from one document doesn't affect other documents containing the same content, INSERT certainly doesn't either. Both are Vstream operations scoped to a single document.

### The analogy

Using Nelson's library analogy: Istream is the library stacks (permanent shelf locations), Vstream is a reading list (references that can be reordered). If two professors have reading lists that both reference the same book on shelf A, one professor inserting a new book into her reading list does not change the other professor's reading list, nor does it move the book on the shelf.

### The windowing nuance

There is one case where changes to Document A can be *visible through* Document B: when Document B has a **location-fixed window** into Document A (floating in time). In that mode:

> "at a relatively fixed location in the document space, in which case updates are seen automatically." [LM 2/37]

But this is not shared content being affected — it is Document B's window *designed to follow* Document A's current Vstream arrangement. The mechanism is fundamentally different from content sharing via COPY. The window is tracking a live view of another document, not holding independent references to shared Istream bytes.

### Summary

| What happens | Effect on other documents |
|---|---|
| INSERT into Doc A's Vstream | None. Other documents' Vstreams unchanged. |
| New Istream bytes created | Other documents don't reference them. |
| Doc A's V-addresses shift | Other documents' V-addresses unaffected. |
| Shared Istream bytes | Remain at same I-addresses, immutable. |

The entire architecture is designed so that editing is a per-document Vstream operation with no side effects on other documents. This is what makes the system safe for concurrent use by independent authors building on shared content.
