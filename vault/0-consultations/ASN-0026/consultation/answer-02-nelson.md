## Question 2 [nelson]

> When a document arranges content in a particular order, does the document hold its own copy of that content, or does it refer to the single permanent instance?

## The Document Refers — It Does Not Copy

A document's arrangement is a **mapping** that refers to content stored permanently in I-space. The document does not hold its own copy. This is the central architectural distinction of Xanadu.

### The Two Spaces

Every document has a **V-space** (virtual space) arrangement that points to **I-space** (invariant space) content. The V-space is the order the reader sees; I-space is where the bytes permanently live. Nelson:

> "The virtual byte stream of a document may include bytes from any other document." [LM 4/10]

> "Logical addressing of the byte stream is in the form of virtual spans, or vspans. These are sequences of bytes in the document's virtual byte stream, regardless of their native origin." [LM 4/11]

The phrase "regardless of their native origin" is key. The document's arrangement treats all content identically — whether the bytes were originally created in this document or in some other document across the docuverse. The V-space is a sequence of references, not a container of duplicated bytes.

### Native vs. Non-Native — Both in I-Space

There are two kinds of content in a document's byte stream:

1. **Native bytes** — created originally in this document, stored "under its control"
2. **Non-native bytes** — included from other documents by reference

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

Even native bytes live in I-space — in the permanent, append-only store. The document doesn't "contain" content in the way a file contains data. It arranges references to content that lives in I-space.

### The COPY Operation Creates References, Not Duplicates

When content moves between documents via the COPY command, no bytes are duplicated:

> "The material determined by \<spec set\> is copied to the document determined by \<doc id\> at the address determined by \<doc vsa\>." [LM 4/67]

This "copy" is transclusion — a new V-space mapping to the same I-space bytes. Nelson makes the absence of duplication explicit:

> "No copying operations are required among the documents throughout the system, and thus we solve the problems of update — especially the problem of updating documents which depend on other documents." [LM 2/36]

### Editing Changes the Map, Not the Territory

When you edit a document, you change its V-space arrangement. The I-space content is untouched:

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." [LM 4/11]

The V-address (position in the current arrangement) shifts with every insert and delete. But the I-address (permanent identity) never changes. Nelson on the conventional alternative he rejects:

> "Virtually all of computerdom is built around the destructive replacement of successive whole copies of each current version." [LM 2/14]

Xanadu replaces this with append-only storage:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

### Why This Matters

The reference-not-copy model enables every fundamental guarantee:

- **Links survive editing** — links point to I-space addresses, which don't change when V-space is rearranged
- **Attribution is structural** — every byte's I-address encodes its home document, so origin is always traceable
- **Versions are cheap** — a new version is a new V-space mapping over the same I-space content, not a full copy
- **Correspondence is computable** — two versions that share I-space content can be compared automatically
- **Transclusion preserves connection** — the included content IS the original, not a severed copy

Nelson's analogy captures it precisely:

> "Think of the present document as a sheet of glass. It may have writing painted on it by the present author; it may have clear glass, windowing to something else; the next pane may be in turn made of more layers of painted glass, with more windows, and so on indefinitely." [LM 2/34]

The glass pane (V-space) arranges what you see. The content visible through windows (I-space references) lives elsewhere permanently. The document is the arrangement, not the content.
