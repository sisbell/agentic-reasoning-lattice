## Question 9 [nelson]

> If two documents share content through quotation or transclusion, does modifying one document's structure affect what the other document displays?

## No. Modifying one document's structure does not affect what another document displays.

This is a direct consequence of the I-space/V-space separation, which is the architectural core of Xanadu.

### The Mechanism

When Document B transcludes content from Document A, B's V-space contains a mapping to bytes in A's **I-space** (permanent content store). It does not reference A's V-space arrangement.

Editing Document A — inserting, deleting, rearranging — changes only A's **V-space** (its current arrangement). The I-space bytes remain exactly where they are, unchanged and permanent.

Nelson states this explicitly:

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

So if Alice writes "hello world" and Bob transcludes it, then Alice "deletes" it from her document — Bob still sees "hello world." Alice's delete only removed the content from her V-space view. The I-space bytes persist, and Bob's document still maps to them.

### Why This Works

The key is that I-space content is **immutable**:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

And the storage model is **append-only**:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

Content is added, never overwritten or removed. Editing is re-arranging references to permanent content, not modifying the content itself.

### The Non-Destruction Guarantee

Nelson frames this as a fundamental principle:

> "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate — without damaging the originals. This is done by inclusion links." [LM 2/45]

And:

> "No copying operations are required among the documents throughout the system, and thus we solve the problems of update — especially the problem of updating documents which depend on other documents. We solve this problem simply by windowing to a changing document." [LM 2/36]

The "distributed update" problem — where changes to one document corrupt dependent documents — is solved by not copying in the first place. Transclusion is reference, not duplication.

### The Two Windowing Modes (A Nuance)

Nelson does describe two modes for how windows can behave:

> "A quotation — an inclusion window — may be fixed to another document in two ways: at a certain point in time, in which case revisions are seen by the user only when he or she asks, 'What has this passage become?' Or second, at a relatively fixed location in the document space, in which case updates are seen automatically." [LM 2/37]

- **Time-fixed**: Frozen reference to specific I-space content. Completely unaffected by any change to the source document.
- **Location-fixed**: Tracks a position in the source document's evolving structure, so if the source publishes a *new version* with different content at that position, the window may reflect it.

But even in the location-fixed case, this is about **versioning** (new content published at a logical position), not about structural edits breaking the reference. The underlying I-space content that the window originally pointed to still exists and is still accessible.

### Summary

| Operation on Document A | Effect on Document B (which transcludes from A) |
|---|---|
| **Rearrange** A's content | None — I-space unchanged |
| **Delete** content from A | None — "bytes remain in all other documents" |
| **Insert** new content in A | None — new bytes get new I-space addresses |
| **Publish new version** of A | Time-fixed window: none. Location-fixed window: may show updated content at that position |

The architectural guarantee is absolute: I-space is permanent, V-space edits are local to the document being edited, and transclusion references I-space. One document's structural changes cannot damage another document's view.
