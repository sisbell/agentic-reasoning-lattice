## Question 1 [nelson]

> Once content is permanently stored, can any document operation — rearrangement, deletion from a document, or versioning — ever alter or destroy that stored content?

# No. Stored content is inviolable.

This is not a side-effect of the design — it is the central architectural principle. Every document operation works exclusively in V-space (the document's current arrangement). I-space (where content permanently lives) is append-only and immutable.

## The foundational separation

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

I-space is where content **permanently lives**. V-space is a **view** — a mapping that references I-space content and can be rearranged across versions. The document IS the mapping, not the content itself.

## What each operation actually does

**DELETE** removes content from V-space only:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

Deletion makes bytes "not currently addressable" in that document's view. The I-space content is untouched.

**REARRANGE** is a pure V-space operation. It transposes regions of the virtual byte stream. The underlying I-space addresses don't change:

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." [LM 4/30]

**INSERT** adds new content to I-space (append-only) and updates the V-space arrangement:

> "The v-stream addresses of any following characters in the document are increased by the length of the inserted text." [LM 4/66]

The new bytes get fresh I-space addresses. No existing I-space content is touched.

**CREATENEWVERSION** creates a new V-space arrangement over the same I-space content:

> "This creates a new document with the contents of document <doc id>. It returns the id of the new document. The new document's id will indicate its ancestry." [LM 4/66]

**COPY** (transclusion) creates a V-space mapping to existing I-space — no duplication, no modification:

> "The material determined by <spec set> is copied to the document determined by <doc id> at the address determined by <doc vsa>." [LM 4/67]

## The storage model forbids it by design

Nelson explicitly rejects destructive replacement:

> "Virtually all of computerdom is built around the destructive replacement of successive whole copies of each current version." [LM 2/14]

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

And the non-destruction guarantee is stated directly:

> "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate — without damaging the originals. This is done by inclusion links." [LM 2/45]

## Why this matters

The immutability of I-space is what makes every other guarantee possible:

- **Permanent addresses work** because the content at an I-address never changes
- **Links survive editing** because they point to I-space, not V-space positions
- **Historical backtrack works** because no previous state has been destroyed
- **Attribution is structural** because I-addresses encode the home document permanently
- **Transclusion works** because the referenced content cannot be altered out from under the reference

As I put it: "A document is really an evolving ONGOING BRAID" [LM 2/14]. The braid grows — strands are added, the arrangement shifts — but no strand is ever cut from the fabric of I-space.
