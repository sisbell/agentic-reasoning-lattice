## Question 3 [nelson]

> When a document's arrangement changes, does the underlying stored content remain byte-identical and at its original permanent address?

# Yes — absolutely and by design.

This is the central architectural invariant of Xanadu. Nelson separates content storage (I-space) from document arrangement (V-space), and the entire system depends on I-space content being permanent and immutable.

## The Core Principle

I-space is where content **permanently lives**. V-space is the document's **current arrangement** of that content. Editing changes V-space; I-space is never touched.

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." (4/11)

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." (4/11)

That second quote is key: the V-address ("the address of a byte in its native document") changes constantly during editing. But the I-address — the permanent home location — never changes.

## Append-Only Storage

The storage model is explicitly append-only. Content is never overwritten:

> "Virtually all of computerdom is built around the destructive replacement of successive whole copies of each current version." (2/14)

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." (2/14)

New content gets appended to I-space with a fresh permanent address. Existing content at existing addresses is never modified.

## What Editing Actually Does

Every editing operation modifies the V→I mapping, not the I-space content:

| Operation | V-space effect | I-space effect |
|-----------|---------------|----------------|
| **INSERT** | Shifts V-addresses after insertion point | New bytes appended to I-space |
| **DELETE** | Removes V-address mapping | None — bytes remain at I-address |
| **REARRANGE** | Reorders V-address mapping | None |
| **COPY** | Creates new V-mapping to existing I-addresses | None — transclusion, not duplication |

Nelson is explicit about deletion:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" (4/9)

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." (4/11)

Deletion removes the V-space mapping. The I-space content is untouched. The bytes are still there, still at the same address, still accessible through old versions or other documents that transclude them.

## Why This Matters

Three guarantees depend on I-space immutability:

1. **Link survivability.** Links point to I-space addresses. Since I-space never changes, links survive all editing:

   > "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." (4/30)

2. **Version reconstruction.** Any previous version can be reconstructed because the content is all still there — only the arrangement changed:

   > "The file management system we are talking about automatically keeps track of the changes and the pieces, so that when you ask for a given part of a given version at a given time, it comes to your screen." (2/15)

3. **Origin traceability.** Every byte's I-address encodes which document created it. Since I-addresses are permanent, attribution is structural and unseverable:

   > "You always know where you are, and can at once ascertain the home document of any specific word or character." (2/40)

## The Document IS the Mapping

A document is not its content — it is its arrangement of content. Nelson calls it "an evolving ONGOING BRAID" (2/14). Each version is a different V-space arrangement over the same I-space content. The braid is re-twisted when parts are rearranged, added, or subtracted — but the strands (I-space bytes) remain intact.

> "There is thus no 'basic' version of a document set apart from other versions — 'alternative' versions — any more than one arrangement of the same materials is a priori better than other arrangements." (2/19)

To answer your question directly: yes, when a document's arrangement changes, the underlying stored content remains byte-identical and at its original permanent I-space address. This is not merely a feature — it is the foundational invariant upon which permanence, link survivability, version history, transclusion, and origin traceability all depend.
