## Question 4 [nelson]

> Can the creator of a link ever destroy it, or does the system guarantee that once a link exists it is permanent in the same way that content is permanent?

## Can a Link Creator Destroy a Link?

**Yes, the owner can delete a link from their document's current version. No, the link is not truly destroyed.** Links follow exactly the same non-destruction semantics as content bytes.

### The "Deleted Links" State

Nelson explicitly includes "DELETED LINKS" as a valid document state, parallel to deleted bytes:

> "DELETED LINKS (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

This tells us three things:

1. **Links can be deleted** — removed from the document's current Vstream arrangement
2. **Deleted links persist** — they await "historical backtrack functions," meaning they remain in Istream
3. **Deleted links may survive in other versions** — if someone versioned your document before you deleted the link, that version still contains it

### Who Can Delete

Only the owner of the link's home document:

> "A link need not point anywhere in its home document. Its home document indicates who owns it, and not what it points to." [LM 4/12]

> "Only the owner has a right to withdraw a document or change it." [LM 2/29]

This means: if you created a link in your document pointing to someone else's content, only you can delete it. The target document's author cannot delete your link — though they could delete the content it points to, potentially breaking it.

### Why Links Are Never Truly Destroyed

Links are stored in Istream alongside content bytes. The only entities actually stored in tumbler-space are "content bytes and links" [LM 4/23]. Since Istream is append-only — "User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically" [LM 2/14] — deleted links remain in permanent storage just as deleted bytes do.

The parallel is exact:

| | Content Bytes | Links |
|---|---|---|
| **Deletion removes from** | Vstream (current view) | Vstream (current view) |
| **Persists in** | Istream (permanent) | Istream (permanent) |
| **Recoverable via** | Historical backtrack | Historical backtrack |
| **Survives in** | Other versions | Other versions |

### The Published Document Complication

For published documents, there's an additional permanence layer. Published documents cannot be easily withdrawn:

> "It is in the common interest that a thing once published stay published, as in the world of paper. Other readers and users will come to depend on its accessibility." [LM 2/43]

The owner can publish a superseding version without certain links, but "the former version must remain on the network. This is vital because of the links other users may have made to it" [LM 2/43]. So even if you "delete" a link from your published document by publishing a new version, the old version — containing the link — remains accessible.

### Summary

The system treats link deletion identically to content deletion: it is a **Vstream operation**, not an **Istream operation**. The link disappears from the document's current arrangement but remains permanently in storage, recoverable through historical backtrack, and potentially alive in other versions. Nelson's non-destruction guarantee — "without damaging the originals" [LM 2/45] — applies to links just as it applies to every other element in the docuverse.
