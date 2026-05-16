## Question 4 [nelson]

> After removal, can a reader still discover that specific content once occupied that position in that document, or does the document appear as though the content was never there?

## The Current Version Shows No Trace; History Reveals Everything

The document appears as though the content was never there — **in the current version**. But the system provides full means to discover what was removed.

### The Vstream Closes the Gap

After DELETE, the Vstream re-densifies. V-addresses are always contiguous:

> "V-address 1 is always the first byte of the document right now. There are no gaps — if you have 100 bytes, you have addresses 1 through 100. DELETE removes addresses (closing the gap)."

If you delete bytes at V-positions 50–60, what was at 61 becomes 50. The current reader sees seamless text with no scar, no placeholder, no marker of absence.

### But Deleted Bytes Are Not Destroyed

The diagram on page 4/9 explicitly names "DELETED BYTES" as a system state:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

"Not currently addressable" is the key phrase. The bytes exist in Istream — permanently, immutably — but the current Vstream arrangement no longer references them. The content has been removed from the *view*, not from *existence*.

### Three Paths to Discovery

A reader can discover the removal through:

**1. Historical backtrack.** Every previous version persists. A reader can request the document at any prior state:

> "The file management system we are talking about automatically keeps track of the changes and the pieces, so that when you ask for a given part of a given version at a given time, it comes to your screen." [LM 2/15]

**2. Version comparison (SHOWRELATIONOF2VERSIONS).** This operation returns "a list of ordered pairs of the spans of the two spec-sets that correspond" [LM 4/70]. By comparing the pre-deletion version with the post-deletion version, the system reveals exactly which spans are present in the old version but absent in the new — exposing the deletion precisely.

> "A facility that holds multiple versions of the same material, and allows historical backtrack, is not terribly useful unless it can help you intercompare them in detail—unless it can show you, word for word, what parts of two versions are the same." [LM 2/20]

**3. Transclusion survival.** If any other document transcludes the deleted content, that content remains visible there. Furthermore, FINDDOCSCONTAINING can locate all documents that include the same Istream bytes, even after those bytes are removed from the original document's current arrangement:

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

### The Design Intent

This is deliberate. Nelson wanted the current view to be clean — a seamless document, not one littered with deletion markers. But he equally wanted nothing to be truly lost:

> "Virtually all of computerdom is built around the destructive replacement of successive whole copies of each current version." [LM 2/14]

Xanadu rejects destructive replacement. DELETE modifies the arrangement (Vstream), never the content (Istream). The current version is authoritative for "what the document says now." The full history is authoritative for "what the document has ever said."

### Summary

| What the reader sees | Deletion visible? |
|---|---|
| Current version (RETRIEVEV) | **No** — seamless, gap closed |
| Previous version (historical backtrack) | **Yes** — content still present |
| Version comparison (SHOWRELATIONOF2VERSIONS) | **Yes** — missing spans identified |
| Other documents transcluding same bytes | **Yes** — content still appears |
| Istream (permanent storage) | **Yes** — bytes exist forever |

The document appears as though the content was never there — but only to a reader who looks at nothing but the present.
