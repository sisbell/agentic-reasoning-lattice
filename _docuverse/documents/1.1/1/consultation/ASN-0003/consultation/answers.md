# Consultation Answers — I-Space and V-Space

**Inquiry:** What is the relationship between permanent content storage (I-space) and mutable document arrangement (V-space)? What invariants connect them?
**Date:** 2026-02-23 15:35
**Questions:** 20 (10 nelson, 10 gregory)

---

## Question 1 [nelson]

> When a user stores content permanently, does the system guarantee that this content can always be retrieved by its original identity, regardless of how documents are later rearranged?

### Nelson's Answer

# Yes — Unconditionally

This is perhaps the single most fundamental guarantee in Xanadu's design. Content stored permanently in I-space can **always** be retrieved by its original identity, regardless of any document rearrangement. The entire architecture exists to make this true.

## The Two-Space Separation

Xanadu maintains two distinct address spaces precisely to decouple content identity from document arrangement:

**I-Space (Invariant Space)** — where content permanently lives. Addresses are absolute and immutable. Content at an I-space address never changes.

**V-Space (Virtual Space)** — the document's current arrangement of content. A view that references I-space content. Can be rearranged freely across versions.

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." [LM 4/11]

That last quote is crucial: V-addresses change constantly during editing, but this is invisible because I-space identity is what matters for retrieval and reference.

## Append-Only Storage

The storage model itself enforces this guarantee:

> "Virtually all of computerdom is built around the destructive replacement of successive whole copies of each current version." [LM 2/14]

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

Content is added to I-space and never overwritten or removed. Nelson calls this a "hyperfile" [LM 2/22].

## DELETE Does Not Destroy

Even "deletion" preserves I-space identity:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

DELETE removes content from a document's V-space arrangement. The I-space content — and its permanent address — remains intact.

## Permanent Tumbler Addresses

The addressing system itself guarantees permanence:

> "New items may be continually inserted in tumbler-space while the other addresses remain valid. This means that any address of any document in an ever-growing network may be specified by a permanent tumbler address." [LM 4/19]

Every I-space address encodes its origin structurally (Node.0.User.0.Document.0.Element), so retrieval by original identity is always possible.

## Origin Always Traceable

> "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

This is not metadata that can be stripped — it is the address itself. To fetch content, the system must request it from its home location. The connection between identity and content is architectural.

## Links Survive Because of This

The link survivability guarantee depends directly on I-space permanence:

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes. This has a crucial advantage: it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them." [LM 4/42]

Links point to I-space addresses. Document rearrangements change only V-space. Therefore links — and any reference by original identity — survive all rearrangements.

## Historical Backtrack Confirms It

The version system is the ultimate proof: if I-space content could be lost through rearrangement, historical backtrack would be impossible. But Nelson guarantees:

> "The file management system we are talking about automatically keeps track of the changes and the pieces, so that when you ask for a given part of a given version at a given time, it comes to your screen." [LM 2/15]

Every previous state is reconstructible because the content persists at its original I-space identity; only the V-space mappings change.

## Summary

The guarantee is threefold:

1. **I-space addresses are permanent** — once assigned, they never change or become invalid
2. **Content at an I-space address is immutable** — it never changes after creation
3. **V-space operations cannot affect I-space** — editing, deleting, rearranging, and versioning all modify V-space mappings only

This separation is not a feature of Xanadu — it *is* Xanadu. The entire system exists to ensure that content identity survives all document manipulation.

---

## Question 2 [nelson]

> Can the same permanent content appear at multiple positions within a single document, or across different documents, without being duplicated in storage?

### Nelson's Answer

# Yes — This Is the Central Architectural Principle

The same permanent content can appear at multiple positions within a single document and across any number of documents, with **zero duplication in storage**. This is not a feature bolted on; it is the foundational design of Xanadu.

## The I-Space / V-Space Separation

Content lives once, permanently, in I-space. Documents are V-space arrangements — views that *reference* I-space content. Multiple V-space positions, in any number of documents, can reference the same I-space bytes.

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

> "The virtual byte stream of a document may include bytes from any other document." [LM 4/10]

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

The word "virtual" is key. The bytes are not duplicated — they are *referenced*. The V-space mapping says "at position 47, show the bytes living at I-address X." Multiple mappings can point to the same I-address.

## Transclusion: Inclusion by Reference

Nelson calls this mechanism "quote-windows," "quote-links," "inclusions," or "windowing." The modern term is **transclusion**.

> "Someone else may create a document which quotes it as much as desired. This mechanism we call the quote-window or quote-link. Through a 'window' in the new document we see a portion of the old." [LM 2/32]

> "A compound document consists of parts of old documents together with new material. Or we may say it really consists of quote-links and new material." [LM 2/32]

> "No copying operations are required among the documents throughout the system, and thus we solve the problems of update — especially the problem of updating documents which depend on other documents. We solve this problem simply by windowing to a changing document." [LM 2/36]

The FEBE COPY operation is the mechanism. Despite its name, it creates a transclusion — a V-space reference to existing I-space content — not a physical duplicate:

> "The material determined by \<spec set\> is copied to the document determined by \<doc id\> at the address determined by \<doc vsa\>." [LM 4/67]

The copy shares I-addresses with the source. Storage holds the bytes once; any number of documents can reference them.

## The Glass Pane Metaphor

Nelson visualizes this as layers of glass:

> "Think of the present document as a sheet of glass. It may have writing painted on it by the present author; it may have clear glass, windowing to something else; the next pane may be in turn made of more layers of painted glass, with more windows, and so on indefinitely." [LM 2/34]

Your document has original writing (native I-space content) and transparent windows (V-space references to other documents' I-space content). The layering is unlimited.

## Versioning: Same Content, Different Arrangement

CREATENEWVERSION is the most dramatic example. It creates an entirely new document whose V-space references the *same* I-space content:

> "This creates a new document with the contents of document \<doc id\>. It returns the id of the new document. The new document's id will indicate its ancestry." [LM 4/66]

No bytes are duplicated. The new version is a new V-space arrangement pointing to the same I-space bytes.

## Why This Matters

Three consequences follow from non-duplication:

1. **Attribution is structural.** Because transcluded content is fetched from its home I-address, the origin is always traceable: "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

2. **Correspondence is automatic.** When two documents share I-space content, the system can identify which parts correspond — enabling version comparison without metadata: "a facility that holds multiple versions is not terribly useful unless it can help you intercompare them in detail — unless it can show you, word for word, what parts of two versions are the same." [LM 2/20]

3. **Discovery works.** FINDDOCSCONTAINING "returns a list of all documents containing any portion of the material included by \<vspec set\>." [LM 4/70] This is possible precisely because shared I-addresses let the system find every document that references a given piece of content.

## Live vs Dead

Nelson draws a sharp line between transclusion (live reference) and conventional copying (dead duplication):

> "Remember the analogy between text and water. Water flows freely, ice does not. The free-flowing, live documents on the network are subject to constant new use and linkage, and those new links continually become interactively available. Any detached copy someone keeps is frozen and dead, lacking access to the new linkage." [LM 2/48]

Content that exists once and is referenced everywhere remains alive — connected to every link, every annotation, every new use. A physical copy severs all those connections.

## Summary

The same permanent content can appear at any number of positions in any number of documents without storage duplication. This is the entire point of the I-space/V-space architecture: I-space stores each byte once, permanently; V-space arranges references to those bytes into documents. Transclusion, versioning, and quotation all exploit this separation. It is not an optimization — it is the mechanism that makes permanence, attribution, correspondence, and automatic royalty possible.

---

## Question 3 [nelson]

> When a user edits a document — inserting, deleting, or rearranging — does any permanently stored content ever change or disappear from the system?

### Nelson's Answer

# No. Permanently stored content never changes or disappears.

This is one of the most fundamental architectural guarantees of Xanadu. Editing operations affect only **V-space** (the document's current arrangement); they never touch **I-space** (permanent content storage).

## The Core Principle: Append-Only Storage

Nelson explicitly rejects the conventional model of destructive replacement:

> "Virtually all of computerdom is built around the destructive replacement of successive whole copies of each current version." [LM 2/14]

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

Content, once written to I-space, is **immutable**. The document is not a block of data that gets overwritten — it is an evolving arrangement of permanent content:

> "A document is really an evolving ONGOING BRAID." [LM 2/14]

## What Each Operation Actually Does

**INSERT** adds new bytes to I-space (they get fresh, permanent I-addresses) and updates the V-space mapping so the new content appears at the desired position. Existing I-space content is untouched.

> "The v-stream addresses of any following characters in the document are increased by the length of the inserted text." [LM 4/66]

Only V-addresses shift. I-addresses are permanent.

**DELETE** removes content from the V-space arrangement only. The I-space bytes remain:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

**REARRANGE** transposes regions within V-space. It changes the order in which content appears to the user but modifies nothing in I-space. The same bytes at the same I-addresses simply appear in a different V-space sequence.

## Why This Works: The Two Address Spaces

The separation of I-space from V-space is the architectural key:

- **I-space** (permanent): Where content lives forever. Addresses are absolute and immutable. Content at an I-address never changes.
- **V-space** (ephemeral): The document's current arrangement. A view that references I-space content. Can be rearranged across versions.

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." [LM 4/11]

The V-address changes; the I-address never does.

## Links Survive Because Content Survives

Because I-space content is permanent, links — which attach to I-space addresses — survive all editing:

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes. This has a crucial advantage: it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them." [LM 4/42]

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." [LM 4/30]

## Historical Backtrack: The Proof

The fact that no content is ever destroyed is what makes historical backtrack possible:

> "The file management system we are talking about automatically keeps track of the changes and the pieces, so that when you ask for a given part of a given version at a given time, it comes to your screen." [LM 2/15]

> "The user of such a system may scroll through an individual document, at successive instants of time, alive in the space-time vortex." [LM 2/15]

If content could be destroyed, reconstructing past states would be impossible.

## Even "Modification" of Others' Work Preserves Originals

> "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate — without damaging the originals. This is done by inclusion links." [LM 2/45]

The old viewpoint is always recoverable:

> "you can always say, 'Show me what this originally was.'" [LM 2/45]

## Summary

| Operation | I-space effect | V-space effect |
|-----------|---------------|----------------|
| **INSERT** | New bytes appended (permanent) | Mapping updated; following addresses shift |
| **DELETE** | None — bytes remain forever | Mapping entries removed from current view |
| **REARRANGE** | None | Order of mapping entries transposed |
| **COPY** | None (references existing I-addresses) | New mapping entries point to existing content |

The answer is unambiguous: **no permanently stored content ever changes or disappears.** Editing is rearrangement of references, not modification of content. I-space is append-only, and every byte ever created retains its permanent address forever.

---

## Question 4 [nelson]

> Must every character visible in a document correspond to exactly one piece of permanently stored content, with no gaps or phantom positions?

### Nelson's Answer

## Yes — with precision about what "visible" and "stored" mean

Nelson's architecture enforces a strict invariant: every position in a document's virtual byte stream (V-space) maps to exactly one permanently stored byte in I-space. There are no gaps, no phantom positions, and no empty slots.

### V-Space Is Dense and Contiguous

V-addresses form a gapless sequence. From the curated source on V-space addresses:

> "V-address 1 is always the first byte of the document right now. There are no gaps — if you have 100 bytes, you have addresses 1 through 100."

When content is deleted, the gap closes. INSERT shifts subsequent addresses up; DELETE closes the hole. There is never a V-position that points to nothing.

### Every V-Position Resolves to I-Space

Every byte in the virtual stream is either native (created in this document) or transcluded (included from another). Both kinds have permanent I-space addresses:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

The document IS the mapping from V-positions to I-addresses. Every V-position maps to a real, permanently stored byte somewhere in the docuverse.

### The Mapping Is Total, Not Partial

Nelson's "part-pounce" guarantee depends on this:

> "THE PART YOU WANT COMES WHEN YOU ASK FOR IT." [LM 2/16]

If any V-position could be a phantom — pointing to nothing — this guarantee would fail. The system constructs the requested content "from the many fragments of its actual storage" [LM 2/16], which requires that every fragment actually exists.

### Ghost Elements Are Structural, Not Content-Level

Nelson does define "ghost elements" — addresses where nothing is stored — but these exist at the document, account, and server level, never within a document's byte stream:

> "In the present implementation (XU.87.1), the only entities actually stored in tumbler-space are content bytes and links. While a number on the line may represent a document or an account, that doesn't mean there's an object stored for it. What's stored is the contents--bytes and links." [LM 4/23]

Ghost elements are structural placeholders in the address hierarchy. Within a document's V-stream, every position is backed by real stored bytes.

### The Many-to-One Direction

One important nuance: the mapping is many-to-one from V-space to I-space, but total and functional. Multiple V-positions across different documents (or versions) can map to the same I-space byte — that is precisely what transclusion is. But no V-position maps to zero I-space bytes.

> "The virtual byte stream of a document may include bytes from any other document." [LM 4/10]

### Summary

| Property | Holds? | Basis |
|----------|--------|-------|
| Every V-position maps to exactly one I-space byte | Yes | V→I mapping is the document's definition |
| No gaps in V-space | Yes | Dense, contiguous addressing; DELETE closes gaps |
| No phantom positions (V-entries with no backing content) | Yes | Part-pounce guarantee; append-only I-space |
| Ghost elements within V-streams | No | Ghosts exist only at document/account/server level |
| Multiple V-positions can share one I-space byte | Yes | This is transclusion |

Every character you see corresponds to exactly one piece of permanently stored content. The system is designed so that this is not merely a convention but a structural consequence of how V-space and I-space relate.

---

## Question 5 [nelson]

> If content is removed from a document's visible arrangement, does the system still retain that content so other documents or links referencing it remain valid?

### Nelson's Answer

# Yes — Absolutely and By Design

This is one of Xanadu's most fundamental guarantees. Content removed from a document's visible arrangement (V-space) is **permanently retained** in I-space, ensuring that all other documents and links referencing it remain valid.

## The Two Address Spaces

Xanadu separates content identity from content arrangement:

- **I-Space (Invariant Space):** Where content permanently lives. Addresses are absolute and immutable. Content at an I-space address never changes.
- **V-Space (Virtual Space):** The document's current arrangement — a view that references I-space content. Can be rearranged across versions.

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

## What "Delete" Actually Means

DELETE in Xanadu does **not** mean what it means in conventional systems. Nelson's diagram on page 4/9 explicitly includes "DELETED BYTES" as a valid system state:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

And he makes the ownership point explicit:

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

So deletion removes content from the V-space arrangement only. The I-space content is untouched.

## The Append-Only Storage Principle

The entire storage model rejects destructive replacement:

> "Virtually all of computerdom is built around the destructive replacement of successive whole copies of each current version." [LM 2/14]

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

> "A document is really an evolving ONGOING BRAID." [LM 2/14]

Content is added to I-space but never removed from it. This is not version control bolted on after the fact — it is the fundamental nature of the storage system.

## Links Remain Valid

Because links point to I-space addresses (content identity), not V-space positions (current arrangement), they survive all editing operations:

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes. This has a crucial advantage: it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them." [LM 4/42]

A link doesn't care where bytes appear in V-space or whether they appear at all in the current version. It cares only that the bytes it references still exist in I-space — and they always do.

## Transclusions Remain Valid

When another document transcludes (includes by reference) content from your document, that transclusion points to I-space addresses. If you "delete" the content from your current version, the other document's transclusion is unaffected:

> "The virtual byte stream of a document may include bytes from any other document." [LM 4/10]

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

The transclusion fetches bytes from their home I-space location. Whether those bytes appear in the home document's current V-space arrangement is irrelevant.

## Previous Versions Remain Accessible

The historical backtrack guarantee ensures all prior arrangements survive:

> "The file management system we are talking about automatically keeps track of the changes and the pieces, so that when you ask for a given part of a given version at a given time, it comes to your screen." [LM 2/15]

And the non-destruction guarantee is stated plainly:

> "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate — without damaging the originals. This is done by inclusion links." [LM 2/45]

## Summary

| What happens after DELETE | Affected? |
|---------------------------|-----------|
| V-space arrangement (current view) | **YES** — content removed |
| I-space content (permanent storage) | **NO** — bytes remain forever |
| Previous versions of the document | **NO** — still contain the content |
| Transclusions in other documents | **NO** — still resolve to I-space |
| Links pointing to the content | **NO** — still attached to I-space bytes |
| Origin traceability | **NO** — I-address still encodes home document |

The system was designed from the ground up so that "deletion" is a change of *view*, never a destruction of *content*. This is not a safety feature added on top — it is the architecture itself.

---

## Question 6 [nelson]

> Does the design require a fixed mapping from each position in a document's visible arrangement to a specific piece of permanent content, and must that mapping update atomically during edits?

### Nelson's Answer

## Yes — Both Requirements Are Present in Nelson's Design

### The Fixed Mapping: The Document IS the V→I Map

Nelson's design requires a deterministic mapping from every position in a document's visible arrangement (V-space) to a specific piece of permanent content (I-space). This is not merely a feature of the design — it is the *definition* of what a document is.

From the v-space-addresses design intent:

> "The mapping V -> I is the essence of document structure. The document IS the mapping from V-addresses to I-addresses. Each version defines a different mapping. Edits change the mapping, not the I-space content."

Nelson specifies that V-space is dense and gap-free:

> "Logical addressing of the byte stream is in the form of virtual spans, or vspans. These are sequences of bytes in the document's virtual byte stream, regardless of their native origin." [LM 4/11]

> "The digit after the one indicates the byte position in the current ordering of bytes. This is its virtual stream address." [LM 4/30]

Every V-position maps to exactly one I-address. There are no unmapped positions:

> "V-address 1 is always the first byte of the document right now. There are no gaps — if you have 100 bytes, you have addresses 1 through 100."

The mapping is also total over heterogeneous origins — native and transcluded bytes are indistinguishable in the V-stream:

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

### Atomicity: Operations Produce Coherent New Mappings

Nelson does not use the word "atomic," but his operation descriptions and retrieval guarantees require it.

**Operations describe indivisible state transitions.** Consider INSERT:

> "This inserts \<text set\> in document \<doc id\> at \<doc vsa\>. The v-stream addresses of any following characters in the document are increased by the length of the inserted text." [LM 4/66]

This is a single command with two coupled effects: (1) new content appears at the specified V-position, and (2) all following V-addresses shift. If only one happened — content placed but addresses not shifted, or addresses shifted but no content placed — the mapping would be inconsistent. Nelson describes them as one operation, not two sequential steps.

Similarly, REARRANGE:

> "Rearrange transposes two regions of text. With three cuts, the two regions are from cut 1 to cut 2, and from cut 2 to cut 3." [LM 4/67]

Transposing two regions involves multiple simultaneous mapping changes. The result must be a new coherent mapping, not a partially transposed intermediate.

**The canonical order mandate.** Nelson describes the enfilade invariant after edits:

> "All changes, once made, left the file remaining in canonical order, which was an internal mandate of the system." [LM 1/34]

"Once made" implies the transition is complete — there is no observable intermediate state where the file is *not* in canonical order. This is an atomicity requirement stated as a design mandate.

**Retrieval assumes coherent state.** Nelson's part-pounce model guarantees consistent reconstruction:

> "The file management system we are talking about automatically keeps track of the changes and the pieces, so that when you ask for a given part of a given version at a given time, it comes to your screen." [LM 2/15]

The phrase "a given part of a given version at a given time" implies that at any point in time, the version has a definite, self-consistent arrangement. A partially updated mapping would make "a given version at a given time" meaningless — the user could observe a state that is neither the pre-edit version nor the post-edit version.

**Link coherence requires it.** Nelson's survivability guarantee depends on the mapping being consistent:

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." [LM 4/30]

Links are to bytes (I-addresses), and they "remain stably attached" through edits. This works only if the V→I mapping transitions cleanly from one consistent state to another. A half-updated mapping could cause link resolution to return wrong content or fail spuriously.

### Summary

| Requirement | Present? | Basis |
|---|---|---|
| Fixed V→I mapping | **Yes** — definitional | "The document IS the mapping from V-addresses to I-addresses" |
| Dense, gap-free V-space | **Yes** — explicit | "There are no gaps" [LM 4/11, 4/30] |
| Operations produce new coherent mappings | **Yes** — implicit from operation definitions | INSERT shifts all following addresses as part of one command [LM 4/66] |
| No observable intermediate state | **Yes** — implicit from retrieval guarantee | "a given part of a given version at a given time" [LM 2/15]; "canonical order" as "internal mandate" [LM 1/34] |

Nelson designs at the semantic level — he specifies *what* the user observes, not *how* the implementation achieves it. The user observes coherent documents at all times, operations that transition between coherent states, and links that remain stably attached through edits. These observations are only possible if the V→I mapping updates atomically.

---

## Question 7 [nelson]

> Can a document's visible arrangement ever reference content that does not exist in permanent storage, or must the system prevent such dangling references?

### Nelson's Answer

# Dangling References in V-Space: Design Intent

The short answer is: **the system must prevent them, and does so by design through the append-only storage model.**

## The Architecture Makes Dangling References Impossible

The entire I-space/V-space separation exists precisely to guarantee this. V-space is an arrangement — a mapping from positions to I-space addresses. I-space is permanent storage where content lives forever once created.

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

Content enters I-space and **never leaves**. There is no operation in FEBE that removes bytes from I-space. DELETE removes from V-space only:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

Since I-space is append-only, and V-space references I-space, every V-space reference resolves. Always.

## No Operation Creates Orphan References

Consider every FEBE operation that touches V-space:

- **INSERT** creates new bytes in I-space *and simultaneously* maps them into V-space. The content exists before the mapping does.
- **COPY** creates a V-space mapping to *already existing* I-space content: "The material determined by \<spec set\> is copied to the document" [LM 4/67]. You can only copy what exists.
- **CREATENEWVERSION** creates a new V-space arrangement over the *same I-space content* the source document already references: "This creates a new document with the contents of document \<doc id\>." [LM 4/66]
- **REARRANGE** permutes existing V-space mappings. No new I-space references are introduced.
- **DELETE** removes V-space mappings. It cannot create them.

There is simply no pathway through the protocol that produces a V-space entry pointing at an I-space address where nothing lives.

## Ghost Elements Are a Different Matter

One might confuse this with ghost elements, but those are a separate concept entirely. Ghost elements are hierarchical positions — servers, accounts, documents — that exist conceptually in tumbler-space without stored objects:

> "In the present implementation (XU.87.1), the only entities actually stored in tumbler-space are content bytes and links. While a number on the line may represent a document or an account, that doesn't mean there's an object stored for it." [LM 4/23]

Ghost elements are about the **structural hierarchy** of the address space. They have nothing to do with V-space referencing non-existent content. A ghost element is an account or document position with no content under it — not a content reference that fails to resolve.

## Transclusion Depends on This Guarantee

The entire transclusion model collapses without it. When your document includes content from another document:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

If home locations could vanish, transclusion would be unreliable, attribution would break, and the "live" vs "dead" distinction Nelson emphasizes would lose its force:

> "The free-flowing, live documents on the network are subject to constant new use and linkage, and those new links continually become interactively available. Any detached copy someone keeps is frozen and dead, lacking access to the new linkage." [LM 2/48]

Live documents work *because* the references always resolve. The liveness guarantee rests on the permanence guarantee.

## The Permanence Guarantee Is the Foundation

> "New items may be continually inserted in tumbler-space while the other addresses remain valid. This means that any address of any document in an ever-growing network may be specified by a permanent tumbler address." [LM 4/19]

This is not merely about addresses being *syntactically valid* — it means the content at those addresses remains retrievable. The entire system — links, transclusion, version history, royalties — depends on I-space content being permanent. A V-space arrangement referencing non-existent I-space content would violate the most fundamental property of the system.

## Summary

The system **must** prevent dangling references, and does so through two complementary mechanisms:

1. **I-space is append-only** — content is never removed, so references cannot become dangling after the fact
2. **All operations that create V-space mappings reference existing I-space content** — references are born valid, and the append-only guarantee keeps them valid forever

This is not a defensive check bolted on afterward. It is the foundational architectural decision from which permanence, attribution, transclusion, and link survivability all follow.

---

## Question 8 [nelson]

> When a new version of a document is created, does it share the same permanent content as the original, or does the system create fresh copies of the stored material?

### Nelson's Answer

## New Versions Share the Same Permanent Content

When a new version is created, the system does **not** create fresh copies. The new version is a new V-space arrangement that references the **same** I-space content as the original. This is fundamental to how Xanadu works.

### The I-Space/V-Space Separation

The entire architecture rests on separating permanent content (I-space) from its arrangement (V-space):

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

I-space content is permanent and immutable. V-space is the document's current arrangement — a mapping from sequential positions to I-space addresses. A version IS a particular V-space mapping.

### CREATENEWVERSION Creates a New Mapping, Not New Content

The operation specification states:

> "This creates a new document with the contents of document \<doc id\>. It returns the id of the new document. The new document's id will indicate its ancestry." [LM 4/66]

"With the contents" means the new version's V-space points to the same I-space addresses. No bytes are duplicated. The new document gets a fresh V-space arrangement that initially maps identically to the original's V-space, but both map to the **same** underlying I-space content.

Nelson describes the result as prismatic — the same content refracted through different arrangements:

> "We call this system of storage Prismatic because we may think of a given part, or section, as being prismatically refracted when we pass from one version to another. We believe our Prismatic storage can support virtually instantaneous retrieval of any portion of any version (historical or alternative)." [LM 2/19]

And crucially:

> "There is thus no 'basic' version of a document set apart from other versions — 'alternative' versions — any more than one arrangement of the same materials is a priori better than other arrangements." [LM 2/19]

The phrase "the same materials" confirms that versions share content, not duplicate it.

### Why This Must Be So: Correspondence Depends On It

The system's ability to compare versions structurally **requires** shared I-space addresses:

> "Of course, a facility that holds multiple versions of the same material, and allows historical backtrack, is not terribly useful unless it can help you intercompare them in detail — unless it can show you, word for word, what parts of two versions are the same." [LM 2/20]

Correspondence works because two V-space positions that map to the same I-space address are, by definition, "the same content." If CREATENEWVERSION created fresh copies with new I-addresses, the system could never determine which parts correspond — the structural basis for comparison would be destroyed.

This is also what enables refractive link following:

> "Links may be refractively followed from a point or span in one version to corresponding places in any other version. Thus a link to one version of a Prismatic Document is a link to all versions." [LM 2/26]

Links point to I-space. If two versions share the same I-space addresses, a link to content in one version automatically reaches the same content in the other.

### No Copying — By Design

Nelson is explicit that the system avoids copying:

> "No copying operations are required among the documents throughout the system, and thus we solve the problems of update — especially the problem of updating documents which depend on other documents." [LM 2/36]

The COPY operation in FEBE is itself transclusion — inclusion by reference, not duplication:

> "The material determined by \<spec set\> is copied to the document determined by \<doc id\> at the address determined by \<doc vsa\>." [LM 4/67]

This "copy" creates a V-space mapping to existing I-space content. CREATENEWVERSION does the same thing for the entire document.

### What Happens After Versioning

Once the new version exists with its shared V→I mapping:

- **Edits to the new version** (INSERT, DELETE, REARRANGE) change only the new version's V-space. The original version's V-space is untouched.
- **New content** added via INSERT gets fresh I-space addresses in the new version's address range.
- **Deleted content** is removed from the new version's V-space but remains in I-space, still visible in the original version.
- **Shared content** — anything not yet edited in the new version — continues to reference the original I-addresses.

This is the "ongoing braid" Nelson describes:

> "Think of the process of making editorial changes as re-twisting this braid when its parts are rearranged, added or subtracted... and think then of successive versions of the document, at successive instants of time, as alive in this space-time vortex." [LM 2/15]

### Summary

| Aspect | What Happens |
|--------|-------------|
| I-space content | Shared — no duplication |
| V-space arrangement | New mapping created, initially identical to original |
| Correspondence | Automatic — shared I-addresses are the mechanism |
| Links | Survive across versions via shared I-space |
| Subsequent edits | Diverge V-space; original unchanged |
| New insertions | Get fresh I-addresses in the new version's space |

The answer is unambiguous: CREATENEWVERSION shares the same permanent content. The new version is a new view over existing material, not a copy of it. This is not an optimization — it is the architectural foundation that makes correspondence, link survivability, and non-destructive editing possible.

---

## Question 9 [nelson]

> Must the system guarantee that two users viewing the same document position always see the same permanent content, or can the arrangement-to-content mapping vary by viewer?

### Nelson's Answer

## The V→I Mapping Is Viewer-Independent

Nelson's architecture requires that the arrangement-to-content mapping be a property of the **document version**, not the viewer. Two users requesting the same position in the same version must receive the same permanent content from the back end.

### The Core Evidence

The RETRIEVEV operation is deterministic:

> "This returns the material (text and links) determined by \<spec set\>." [LM 4/67]

The spec set (a collection of V-space spans) determines the result. No viewer parameter exists. The back end maps V-addresses to I-addresses based on the document's structure alone.

Nelson makes the stronger claim that content identity is always ascertainable:

> "This world nevertheless remains simple in design. The virtuality is simple in structure and repeats in layers. You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

"You" here is universal — any user, any time. The home document of a character at a given position is a fact about the document, not about the viewer.

### What the V→I Mapping Is

A document version defines a virtual byte stream — a sequence of I-space references:

> "Logical addressing of the byte stream is in the form of virtual spans, or vspans. These are sequences of bytes in the document's virtual byte stream, regardless of their native origin." [LM 4/11]

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document." [LM 4/11]

The virtual byte stream is a property of the document. It is not parameterized by who is reading it. Position 5 maps to whichever I-address the document's POOM (positional mapping) says it maps to — the same answer for every viewer.

### Where Viewer Experience Can Diverge

Nelson does describe several mechanisms that cause different users to see different things, but none of them involve the V→I mapping itself varying:

**1. Version selection (front-end choice)**

> "the reader may be following a link made to an older version. However, the user's front-end machine may easily be set up to follow the link to the same passage in the most recent version—if it's still there." [LM 2/43]

Two users may be viewing *different versions* — one follows a link to version 1, another reads version 3. Each version has its own deterministic V→I mapping. The front end chooses which version to present; the back end serves whichever version is requested.

**2. Location-fixed windows (temporal variation, not per-viewer)**

> "A quotation—an inclusion window—may be fixed to another document in two ways: at a certain point in time, in which case revisions are seen by the user only when he or she asks, 'What has this passage become?' Or second, at a relatively fixed location in the document space, in which case updates are seen automatically." [LM 2/37]

A location-fixed window (floating in time) transcludes the *current* state of the source. If the source changes between Alice's access and Bob's, they see different bytes at that position. But this is temporal variation in the source document, not per-viewer variation. At any single instant, Alice and Bob would see the same content.

**3. Link filtering (presentation, not content)**

> "it becomes necessary to apply some kind of filter, saying, 'What links come in from Spain? From last week? From persons of importance to me?'" [LM 2/47]

Different users may filter links differently. But link filtering is a front-end presentation choice. The back end returns the same link data regardless of viewer.

**4. Front-end rendering**

> "None of these commands are to be seen by the user. The user's concerns are to be seen on the screen; the complications of the protocol are to be handled invisibly by programs in the user's front-end machine." [LM 4/61]

Different front ends may render content differently — typography, layout, zoom level. But the bytes returned by the back end are identical.

### The Principle

Nelson separates the system into layers with strict responsibilities:

- **Back end**: stores content, maintains mappings, serves bytes deterministically
- **Front end**: chooses what to request, how to present it, which version to follow

The V→I mapping lives in the back end. It is structural, deterministic, and viewer-independent. All variation in user experience comes from **which version is requested** (front-end choice) and **how results are presented** (front-end rendering), never from the mapping itself producing different results for different requesters.

This is architecturally necessary for several Nelson guarantees to hold:
- **Attribution** requires that position X in version V always traces to the same I-address
- **Correspondence** requires that shared I-addresses between versions be computable from structure alone
- **Royalties** require deterministic accounting of which bytes were delivered
- **Origin traceability** requires "you can at once ascertain the home document of any specific word or character" — a viewer-dependent mapping would make this indeterminate

### Summary

The mapping is **fixed per document version**. Two users viewing version V of document D at position P will always receive the same I-space content from the back end. What can vary across viewers is which version they choose to view (front-end navigation), what links they see (front-end filtering), and how content is rendered (front-end presentation). The back end's V→I mapping is a structural fact about the document, not a per-viewer computation.

---

## Question 10 [nelson]

> If the system assigns a permanent identity to a piece of content at storage time, must that identity remain unique forever — never reassigned to different content, even after the content is removed from all documents?

### Nelson's Answer

# Yes — Absolutely and Without Exception

The answer is an unqualified yes. An I-space address, once assigned to content, must remain bound to that content forever. It can never be reassigned to different content, regardless of whether the content is removed from every document's V-space arrangement.

This follows from multiple interlocking guarantees in Literary Machines.

## 1. Addresses Are Permanent by Design

The tumbler addressing system is explicitly designed so that addresses never become invalid or available for reuse:

> "New items may be continually inserted in tumbler-space while the other addresses remain valid. This means that any address of any document in an ever-growing network may be specified by a permanent tumbler address." [LM 4/19]

The "baptism" mechanism — where new addresses are created by forking digits to the right — only produces fresh addresses. There is no mechanism for reclaiming or recycling old ones:

> "The owner of a given item controls the allocation of the numbers under it." [LM 4/20]

Allocation goes forward. It never retreats.

## 2. Storage Is Append-Only

Nelson explicitly rejects destructive replacement as a storage paradigm:

> "Virtually all of computerdom is built around the destructive replacement of successive whole copies of each current version." [LM 2/14]

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

In an append-only store, content is added and never overwritten. An I-address that has been written to can never become "empty" — the content remains there permanently. There is nothing to reassign.

## 3. "Deletion" Does Not Free I-Space Addresses

When content is deleted from a document, it is removed from the V-space arrangement only. The I-space content persists:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

The phrase "not currently addressable" refers to V-space accessibility — the bytes vanish from the document's current view. But they remain at their I-space address, recoverable through historical backtrack and still present in any other document that transcludes them.

## 4. Content Immutability Implies Address Uniqueness

Nelson states that I-space content is immutable:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

The "home location" is permanent. The byte at that location never changes. If the address could be reassigned to different content, this immutability guarantee would be violated.

## 5. Links Depend on Address Permanence

Link survivability is predicated on I-space address stability:

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes. This has a crucial advantage: it means that links can survive editing." [LM 4/42]

Links attach to I-space addresses. If an address were reassigned to different content, every link referencing that address would silently point to the wrong content — a far worse failure than a broken link, because it would be undetectable. The system's integrity requires that address identity is permanent and unique.

## 6. Origin Traceability Requires Uniqueness

The I-address structurally encodes provenance:

> "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

The document field of an I-address tells you which document created that content. If addresses were recycled, this structural attribution would become meaningless — an address might point to content from a completely different document than the one encoded in its tumbler.

## 7. Historical Backtrack Requires Permanence

The entire version model depends on I-addresses remaining stable:

> "The file management system we are talking about automatically keeps track of the changes and the pieces, so that when you ask for a given part of a given version at a given time, it comes to your screen." [LM 2/15]

Previous versions reconstruct by replaying V-space arrangements over permanent I-space content. If an I-address had been reassigned, reconstructing an old version would produce a document containing content that never existed in that version — a silent corruption of history.

## Summary

Nelson's design creates a system where I-space addresses are:

- **Created** by append-only allocation (never recycled)
- **Bound** to content permanently (never reassigned)
- **Immutable** in their content (never overwritten)
- **Structurally meaningful** in their provenance (the address IS the attribution)
- **Relied upon** by links, versions, transclusions, and historical backtrack

An I-space address that has been assigned to content is occupied forever. Even if every document in the docuverse removes that content from its V-space arrangement, the content remains at its I-address — "awaiting historical backtrack functions" — and that address can never point to anything else.

This is not merely a design choice but a logical necessity. Permanence, attribution, link survivability, version reconstruction, and origin traceability all collapse if address uniqueness is not eternal.

---

## Question 11 [gregory]

> When `insertpm` creates a new POOM bottom crum mapping V-displacement to I-displacement, does it verify that the I-addresses actually exist in the granfilade, or does it trust the caller unconditionally?

### Gregory's Answer

## KB Synthesis

Looking through the knowledge base, `insertpm` **trusts the caller unconditionally** — it performs no verification that I-addresses actually exist in the granfilade before creating POOM mappings.

## Evidence

**No validation documented in operation flows:**

[ST-INSERT] documents that for INSERT, the flow is: `inserttextingranf` allocates fresh I-addresses in granf → `docopy` → `insertpm` creates POOM mappings. The I-addresses exist because they were just allocated, but there's no mention of `insertpm` verifying this.

[ST-VCOPY] and [PRE-COPY] document that COPY reads I-addresses from source POOM and creates mappings in target POOM. Finding 0046 explicitly states: "The COPY operation performs NO duplicate checking before inserting V→I mappings into the target document's POOM. The `insertpm()` function in `orglinks.c:75-134` delegates to `insertnd()` in `insertnd.c:15-111`, which calls `isanextensionnd()` to check only whether the new content is contiguous with an existing crum — **never whether the I-address already exists** in the target."

The "never whether the I-address already exists" refers to checking duplication within the target POOM, but no validation against the granfilade is mentioned either.

**Convention-based system:**

[INV-SUBSPACE-CONVENTION] (Finding 0011) establishes the architectural pattern: "The subspace convention (V-position 0.x = links, 1.x = text) is a social contract enforced by convention, not by runtime checks." The system relies on callers following conventions rather than runtime validation.

[PRE-VCOPY] (Finding 0010) confirms: "`docopy` performs no validation that the source I-address types match the destination subspace. Text I-addresses (permascroll) can be copied into the link subspace (`0.x`), and link ISAs can be copied into the text subspace (`1.x`). The `acceptablevsa` check is a no-op."

**Silent failures on invalid I-addresses:**

[PRE-RETRIEVE-CONTENTS] (Finding 0010) shows what happens when invalid I-addresses are used: "Looking up a link ISA in the permascroll produces NULL or garbage bytes — a silent failure." There's no validation preventing the invalid mapping from being created.

[EC-GHOST-LINK] (Finding 0048) describes I-addresses in POOM that have no granfilade content: "When a link's endset contains I-addresses that are not in any document's POOM (unreferenced addresses per DEL5), FOLLOWLINK succeeds but returns empty or partial results." The system tolerates POOM mappings to I-addresses that may not resolve to actual content.

[INV-ITOV-FILTERING] (Finding 0048) shows the filtering happens at **retrieval** time, not creation time: "At `span2spanset()`, `retrieverestricted()` searches the target document's POOM for the I-address. If not found (returns NULL), the I-address is dropped from the result without error."

**Error handling pattern:**

[EC-ERROR-ABORT] (Finding 0011) establishes that convention violations produce crashes, not graceful validation errors: "When implicit contracts are violated, the system's error handling is to crash immediately via `qerror`/`abort`... Violations of conventions produce fatal aborts rather than error codes or exceptions."

## Conclusion

The architecture follows a **trust-based model**: operations are expected to provide valid I-addresses, and `insertpm` creates POOM mappings unconditionally. Invalid mappings result in silent failures (NULL/empty results) at retrieval time rather than being prevented at creation time. This is consistent with the broader convention-over-enforcement pattern documented throughout the system.

## Code Exploration

## Answer: No Validation — Trust-Based Design

**`insertpm` does NOT verify that I-addresses exist in the granfilade.** It trusts the caller unconditionally.

---

## Code Path Analysis

### Entry Point: `insertpm` in `orglinks.c:75-134`

```c
bool insertpm(typetask *taskptr, tumbler *orglisa, typeorgl orgl, 
              tumbler *vsaptr, typesporglset sporglset)
{
    // ... validation of V-address only (lines 86-98)
    
    for (; sporglset; sporglset = (typesporglset) sporglset->xxxxsporgl.next) {
        unpacksporgl (sporglset, &lstream, &lwidth, &linfo);
        
        movetumbler (&lstream, &crumorigin.dsas[I]);     // [orglinks.c:105]
        movetumbler (&lwidth, &crumwidth.dsas[I]);       // [orglinks.c:109]
        movetumbler (vsaptr, &crumorigin.dsas[V]);       // [orglinks.c:113]
        
        // Calculate V-width from I-width
        // ... lines 115-120 ...
        
        insertnd (taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);  // [orglinks.c:130]
    }
}
```

**No validation.** The I-address from the sporgl is copied directly into `crumorigin.dsas[I]` without checking if it exists in the granfilade.

---

### Insertion Path: `insertnd` → `insertcbcnd`

The call chain is:
1. `insertnd()` [insertnd.c:15] → validates V-width only
2. `doinsertnd()` [insertnd.c:185] → checks for empty enfilade
3. `insertcbcnd()` [insertnd.c:242] → creates or extends bottom crum

At the bottom crum creation [insertnd.c:260-274]:

```c
new = createcrum (0, (INT)father->cenftype);
reserve (new);
adopt (new, SON, (typecorecrum*)father);
dspsub (origin, grasp, &new->cdsp, (INT)father->cenftype);
movewisp (width, &new->cwid);
move2dinfo (infoptr, &((type2dcbc *)new)->c2dinfo);  // [insertnd.c:267]
```

The I-address is stored in `new->cdsp.dsas[I]` and the I-width in `new->cwid.dsas[I]` with **no verification** that these addresses exist in the granfilade.

---

## Where Do I-Addresses Come From?

### 1. Insert Operations: `doinsert()` [do1.c:87]

```c
inserttextingranf(taskptr, granf, &hint, textset, &ispanset)  // [do1.c:118]
    && docopy (taskptr, docisaptr, vsaptr, ispanset)          // [do1.c:119]
```

- `inserttextingranf()` allocates **new** I-addresses in the granfilade for the text
- Those newly allocated addresses are passed to `docopy()` → `insertpm()`
- **Assumption:** Just-allocated addresses are valid

### 2. Copy Operations: `docopy()` [do1.c:45]

```c
specset2ispanset (taskptr, specset, &ispanset, NOBERTREQUIRED)  // [do1.c:54]
    && insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset) // [do1.c:60]
```

The conversion chain:
1. `specset2ispanset()` [do2.c:14] → converts V-spans to I-spans
2. `vspanset2ispanset()` [orglinks.c:397] → permutes through POOM
3. `permute()` [orglinks.c:404] → retrieves bottom crums
4. `retrieverestricted()` [retrie.c:56] → walks POOM tree

**Assumption:** I-addresses retrieved from an existing POOM are valid because they were inserted correctly in the past.

---

## Design Philosophy: Convention Over Enforcement

This is **intentional**, not a bug. From [Finding 0011-convention-over-enforcement-design.md]:

> "Udanax Green follows a **'convention over enforcement'** design philosophy. The system provides powerful, uniform primitives but relies on calling code to use them correctly."

### The Contract

**Caller's responsibility:**
- Ensure I-addresses exist before passing them to `insertpm()`
- Either by allocating them first (insert)
- Or by retrieving them from a consistent POOM (copy)

**`insertpm`'s responsibility:**
- Map V-displacements to I-displacements
- Maintain tree structure
- Update widths

### No Defensive Validation

```c
// From do2.c:110-113 (related validation function)
bool acceptablevsa(tumbler *vsaptr, typeorgl orglptr)
{
    return (TRUE);  // Always accepts — no validation
}
```

The pattern is consistent: **trust the caller, crash on violation.**

---

## Consequences

### If POOM Contains Invalid I-Addresses

**Scenario 1: Deleted content**
- POOM maps V→I where I-address was deleted from granfilade
- Retrieval fails when dereferencing I-address
- Likely: crash or empty result

**Scenario 2: Corrupted POOM**
- POOM contains garbage I-addresses
- `insertpm()` copies them into another document
- Corruption propagates through copy operations
- Hard to debug: no error at insertion time

**Scenario 3: Inconsistent state**
- granfilade and POOM out of sync
- V-spans appear valid but reference non-existent content
- spanf (link index) may become inconsistent

### Why This Works (Usually)

The system maintains consistency through:

1. **Atomic allocation**: `inserttextingranf()` allocates before `insertpm()`
2. **No deletion**: Content is immutable (no `deletefromgranf()` operation)
3. **Trusted code**: Backend operations follow conventions
4. **Small codebase**: Easier to verify correctness manually

---

## Related Findings and Bugs

| Reference | Title | Relevance |
|-----------|-------|-----------|
| **Bug 0010** | No V-Position Validation | Same pattern — `acceptablevsa()` always TRUE |
| **Finding 0011** | Convention Over Enforcement | Design philosophy explaining this |
| **Finding 0012** | Dual Enfilade Architecture | Explains granf/POOM separation |
| **Bug 0009** | compare_versions crash | Convention violation consequence |

---

## Verification Test

To verify this behavior, I could write a test that:

1. Creates a document and inserts text (allocates I-addresses)
2. Manually constructs a POOM with **non-existent** I-addresses
3. Attempts `docopy()` with those invalid addresses
4. Observes: insertion succeeds, retrieval fails or crashes

But the FEBE protocol doesn't expose raw POOM manipulation, and the backend assumes all internal state is consistent.

---

## Conclusion

**`insertpm` trusts the caller unconditionally.** It does not validate that I-addresses exist in the granfilade. This is by design:

- **For insert operations:** I-addresses are freshly allocated
- **For copy operations:** I-addresses come from existing POOMs (assumed consistent)
- **Philosophy:** Convention over enforcement — validate at system boundaries, not internal boundaries
- **Trade-off:** Simpler code, better performance, but corruption can propagate silently

The system relies on maintaining invariants through careful operation sequencing rather than defensive validation at every boundary.

---

## Question 12 [gregory]

> After `deletend` removes a V→I mapping and `subtreefree` reclaims the POOM nodes, is there any remaining structure in the POOM that records which I-addresses were once referenced — or is the association completely erased from the document's perspective?

### Gregory's Answer

## KB Synthesis

# Answer: The Association is Completely Erased from the Document's POOM

After `deletend` removes V→I mappings and `subtreefree` reclaims the POOM nodes, **no structure remains in the POOM that records which I-addresses were once referenced**. The association is fully erased from the document's operational perspective.

## Three-Layer Evidence

The knowledge base reveals a critical three-layer split [SS-THREE-LAYER-MODEL Finding 0040]:

1. **I-space (granfilade):** I-addresses and content persist permanently, unaffected by DELETE [INV-IADDR-IMMUTABILITY Finding 0064]
2. **Spanfilade (DOCISPAN):** I-address → document mappings are append-only; DELETE does not remove them [INV-SPANF-WRITE-ONLY Finding 0057]
3. **POOM:** V-address → I-address mappings are destructively modified; DELETE fully erases them [SS-POOM-MUTABILITY Finding 0072]

## What DELETE Does to the POOM

From [ST-DELETE Finding 0064, Finding 0072]:

> "The `deletend` function performs tree surgery: nodes falling entirely within the deletion range are `disown`ed (removed from parent/sibling pointers) and then `subtreefree`d (recursively freed). No copy of the pre-deletion tree state is preserved anywhere — there is no undo log, edit history, shadow copy, or transaction journal."

The freed nodes are deallocated memory — they contain no record of what I-addresses they once mapped. The POOM tree after DELETE has no metadata, tombstones, or traces of the removed mappings.

## The Spanfilade Remembers

However, the **spanfilade retains stale references** [INT-DELETE-SPANF-DIVERGENCE Finding 0057]:

> "After DELETE, the POOM no longer contains the mapping, but the spanfilade still claims the document contains those I-addresses."

This creates observable divergence [EC-STALE-SPANF-REFERENCE Finding 0057]:

```
After DELETE from document D:
  find_documents(i) → {D, ...}      # spanf still indexes D
  retrieve_contents(D, vspan) → []   # POOM has no mapping
```

The spanf entry is a **ghost reference** — an index pointing to a document that no longer operationally contains the content.

## Why This Matters

This complete erasure explains two key properties:

1. **DELETE is not the inverse of INSERT** [INV-DELETE-NOT-INVERSE Finding 0064]:
   > "DELETE followed by INSERT of identical text does NOT restore the original document state... All relationships indexed by I-address are permanently severed: transclusions, link endpoints, version comparison results, and provenance chains."

   Re-inserting allocates fresh I-addresses because the POOM has no memory of the prior ones.

2. **Only COPY can restore I-address associations** [ST-COPY Finding 0064]:
   > "COPY is the identity-preserving operation... When used to 'undelete' content — by copying from a document that still references the original I-addresses — COPY restores both the V-space content AND the I-space identity."

## Summary

From the **document's perspective** (operations that query the POOM like `retrieve_contents`), the I-address association is **completely erased**. From the **system's perspective** (operations that query the spanf like `find_documents`), the association **persists as a stale index entry**.

The POOM contains zero record of deleted I-addresses. The only "memory" is in the spanfilade's append-only index — a memory that produces ghost references rather than operational access [SS-DUAL-ENFILADE Finding 0023].

## Code Exploration

Now I have traced through the complete deletion path. Let me compile my findings with specific code citations.

---

## Answer: No Trace Remains in the POOM — But Content Persists in the Granfilade

After `deletend` removes a V→I mapping and `subtreefree` reclaims the POOM nodes, **the association is completely erased from the document's POOM enfilade**. However, the actual content at those I-addresses **remains in the Granfilade** — creating orphaned, unreachable data.

### The Deletion Path

**1. V-span deletion entry point** [`do1.c:158-167`]

```c
bool dodeletevspan(typetask *taskptr, typeisa *docisaptr, typevspan *vspanptr)
{
    return (
       findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
    && deletevspanpm (taskptr, docisaptr, docorgl, vspanptr) );
}
```

**2. POOM deletion** [`orglinks.c:145-152`]

```c
bool deletevspanpm(typetask *taskptr, tumbler *docisaptr, typeorgl docorgl, typevspan *vspanptr)
{
    if (iszerotumbler(&vspanptr->width))
        return (FALSE);
    deletend((typecuc*)docorgl, &vspanptr->stream, &vspanptr->width, V);
    logbertmodified(docisaptr, user);
    return (TRUE);
}
```

**3. Tree node deletion** [`edit.c:31-76`]

```c
int deletend(typecuc *fullcrumptr, tumbler *origin, tumbler *width, INT index)
{
    // ... cuts around the deletion region ...
    for (ptr = (typecuc *) findleftson (father); ptr; ptr = next) {
        next = (typecuc *) findrightbro((typecorecrum*)ptr);
        switch (deletecutsectionnd ((typecorecrum*)ptr, &fgrasp, &knives)) {
          case 1:
            disown ((typecorecrum*)ptr);
            subtreefree ((typecorecrum*)ptr);  // [edit.c:59-60]
            break;
          // ...
        }
    }
    setwispupwards (father,1);
    recombine (father);
}
```

**4. Recursive memory reclamation** [`credel.c:413-432`]

```c
void subtreefree(typecorecrum *ptr)
{
    if (ptr->height > 0) {
        for (p = ((typecuc *)ptr)->leftson; p; p = right) {
            right = p->rightbro;
            disown (p);
            subtreefree (p);  // Recursively free children
        }
    } else if (ptr->cenftype == GRAN 
            && ((typecbc *)ptr)->cinfo.infotype == GRANORGL 
            && ((typecbc *)ptr)->cinfo.granstuff.orglstuff.orglincore)
        orglfree (((typecbc *)ptr)->cinfo.granstuff.orglstuff.orglptr);
    freecrum (ptr);  // [credel.c:429-431]
}
```

**Critical observation:** Only GRANORGL crums (references to other documents) trigger recursive cleanup. POOM crums that stored V→I mappings are simply freed.

**5. Memory deallocation** [`credel.c:434-453`]

```c
void freecrum(typecorecrum *ptr)
{
    // Remove from grimreaper list
    if (grimreaper == ptr){
        grimreaper = grimreaper->nextcrum;
    }
    ptr->nextcrum->prevcrum = ptr->prevcrum;
    ptr->prevcrum->nextcrum = ptr->nextcrum;
    --crumnumber;
    efree ((char*)ptr);  // [credel.c:442-452]
}
```

### What Happens to the I-Addresses?

The POOM enfilade structure stores V→I mappings as 2D crums with both V and I coordinates [`orglinks.c:100-131`]:

```c
bool insertpm(typetask *taskptr, tumbler *orglisa, typeorgl orgl, 
              tumbler *vsaptr, typesporglset sporglset)
{
    for (; sporglset; sporglset = (typesporglset) sporglset->xxxxsporgl.next) {
        movetumbler (&lstream, &crumorigin.dsas[I]);  // I-coordinate
        movetumbler (vsaptr, &crumorigin.dsas[V]);    // V-coordinate
        movetumbler (&lwidth, &crumwidth.dsas[I]);
        // ...
        insertnd (taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);
    }
}
```

When `deletend` removes these crums and `subtreefree` frees them, **the V→I mapping is completely destroyed**. No trace remains in the POOM of which I-addresses were once referenced.

### But the Content Persists

The actual text content lives in the **Granfilade**, not the POOM. The Granfilade uses GRANTEXT crums [`wisp.h:69-78`, `granf2.c:83-108`]:

```c
#define GRANTEXT        1  // [wisp.h:69]

typedef struct structgrantext {
    char textstring[GRANTEXTLENGTH];  // Actual content bytes
    unsigned textlength;
} typegrantext;  // [wisp.h:75-78]
```

When text is inserted [`granf2.c:96-99`]:

```c
locinfo.infotype = GRANTEXT;
locinfo.granstuff.textstuff.textlength = textset->length;
movmem(textset->string, 
       locinfo.granstuff.textstuff.textstring, 
       locinfo.granstuff.textstuff.textlength);
insertseq ((typecuc*)fullcrumptr, &lsa, &locinfo);
```

**The Granfilade is never modified by POOM deletions.** The GRANTEXT crums storing content at I-addresses remain intact, even though no V-addresses map to them anymore.

### No Garbage Collection for Orphaned Content

The disk garbage collection mechanism [`corediskout.c:388-411`] only applies to GRANORGL crums (document references):

```c
int deletewithgarbageddescendents(typediskloafptr diskptr, 
                                   typecuc *father, bool deletefullcrumflag)
{
    if (!deletefullcrumflag ||!changerefcount(diskptr,-1)) {
        // ... recursive deletion for GRAN fathers ...
        if (father->cenftype == GRAN
            && ((typecbc *)father)->cinfo.infotype == GRANORGL  // Only GRANORGL
            && ((typecbc *)father)->cinfo.granstuff.orglstuff.orglincore) {
            deletefullcrumandgarbageddescendents(...);  // [corediskout.c:402-407]
        }
    }
}
```

GRANTEXT content is **never garbage collected**. Once inserted into the Granfilade, it persists indefinitely, even after all V→I references are deleted.

### Conclusion

**From the POOM's perspective:** The V→I association is completely erased. No structure records which I-addresses were once referenced.

**From the system's perspective:** The content at those I-addresses remains in the Granfilade as orphaned data — unreachable through normal document operations but still consuming storage. This is a document-level "memory leak": deleted content accumulates permanently in the Granfilade with no mechanism for reclamation.

The I-addresses could theoretically still be accessed if you knew the exact tumbler coordinates, but without the V→I mapping, there's no way to discover what those addresses are or that they once belonged to the document.

---

## Question 13 [gregory]

> When `isanextensionnd` detects that a new POOM entry's I-address is contiguous with an existing entry (reach == origin), does it check that the V-addresses are also contiguous, or could it merge entries that are V-discontinuous but I-contiguous?

### Gregory's Answer

## KB Synthesis

Looking at the knowledge base, `isanextensionnd` checks **both V-contiguity AND I-contiguity**, along with matching homedoc.

From [ST-INSERT] (Finding 0062):
> The function `isanextensionnd()` checks two conditions: (1) the new content has the same `homedoc` as the existing crum, and (2) the new content's origin equals the existing crum's reach.

From [PRE-COPY] (Finding 0046), which provides more explicit detail:
> The function `isanextensionnd()` at `insertnd.c:293-301` checks two conditions: (1) the new mapping has the same `homedoc` (I-address origin document) as an existing crum, and (2) **the new mapping starts exactly where the existing crum ends (contiguous in both V and I dimensions)**.

The dual-space nature of POOM crums is confirmed in [SS-POOM-BOTTOM-CRUM] (Finding 0076):
```
BottomCrum = {
  origin: { dsas[I]: Tumbler,  dsas[V]: Tumbler },
  width:  { dsas[I]: Tumbler,  dsas[V]: Tumbler }
}
```

For extension to succeed, the new entry must satisfy:
1. **Homedoc match**: Same I-address origin document as existing crum
2. **V-contiguity**: `new.origin.dsas[V] == existing.reach.dsas[V]`
3. **I-contiguity**: `new.origin.dsas[I] == existing.reach.dsas[I]`

This prevents merging entries that are V-contiguous but I-discontinuous. This is observable through [INT-LINK-INSERT] (Finding 0063), where CREATELINK breaks I-address contiguity for subsequent text inserts. Even though consecutive INSERTs place content at adjacent V-positions, the I-address gap created by the intervening link orgl allocation prevents extension, forcing creation of separate crums.

The calling context (ONMYRIGHTBORDER from `whereoncrum`) pre-filters to cases where V-contiguity is already established at the knife-cutting level, but `isanextensionnd` independently verifies both dimensions to ensure true dual-space contiguity before extending the crum in place.

## Code Exploration

---

# Answer: V-Address Contiguity Check in `isanextensionnd`

**Yes, `isanextensionnd` checks that BOTH V-addresses AND I-addresses are contiguous.** The function cannot merge entries that are V-discontinuous but I-contiguous.

## Code Evidence

The `isanextensionnd` function `[insertnd.c:301-309]` performs the extension check:

```c
bool isanextensionnd(typecbc *ptr, typedsp *offsetptr, typedsp *originptr, type2dbottomcruminfo *infoptr)
{
  typedsp grasp, reach;
  bool lockeq();
	if (!tumblereq (&infoptr->homedoc, &((type2dcbc *)ptr)->c2dinfo.homedoc))
		return (FALSE);
	prologuend ((typecorecrum*)ptr, offsetptr, &grasp, &reach);
	return (lockeq (reach.dsas, originptr->dsas, (unsigned)dspsize(ptr->cenftype)));
}
```

### The Critical Check `[insertnd.c:308]`

```c
return (lockeq (reach.dsas, originptr->dsas, (unsigned)dspsize(ptr->cenftype)));
```

This line compares the **entire dsp** (displacement) of both dimensions:

1. **`dspsize(POOM)` returns 2** `[wisp.h:26]` — indicating 2 dimensions to compare
2. **`reach.dsas`** is an array containing `[I-address, V-address]` `[wisp.h:19-20]`
3. **`originptr->dsas`** contains the new entry's `[I-address, V-address]`

### The `lockeq` Function `[wisp.c:261-267]`

```c
bool lockeq(tumbler *lock1, tumbler *lock2, unsigned loxize)
{
        while (loxize--)
               if (!tumblereq (lock1++, lock2++))
                        return(FALSE);
        return(TRUE);
}
```

With `loxize=2` (for POOM), this iterates through both dimensions and checks:
- **`reach.dsas[I]` == `originptr->dsas[I]`** (I-address contiguity)
- **`reach.dsas[V]` == `originptr->dsas[V]`** (V-address contiguity)

Both must match for `lockeq` to return TRUE.

### How `reach` is Computed `[retrie.c:334-339]`

```c
int prologuend(typecorecrum *ptr, typedsp *offset, typedsp *grasp, typedsp *reach)
{
        dspadd (offset, &ptr->cdsp, grasp, (INT)ptr->cenftype);
        if (reach)
                dspadd (grasp, &ptr->cwid, reach, (INT)ptr->cenftype);
}
```

The `reach` represents the **end position** of the existing entry:
- `grasp = offset + ptr->cdsp` (entry start position)
- `reach = grasp + ptr->cwid` (entry end position)

This is computed in **both V and I dimensions**.

## Conclusion

**The function enforces 2D contiguity.** An entry can only be extended if:

1. The home document matches `[insertnd.c:305-306]`
2. **BOTH** the V-address **AND** I-address are contiguous `[insertnd.c:308]`

**This prevents merging entries that are I-contiguous but V-discontinuous.**

The check is symmetric — it verifies that `reach == origin` in all dimensions defined by `dspsize`. For POOM, this means checking both V and I simultaneously, ensuring complete 2D contiguity before allowing the optimization of extending an existing entry instead of creating a new one.

---

## Question 14 [gregory]

> Can a single I-address span appear at multiple V-positions within the same POOM (via self-transclusion), and if so, does `permute` in the I→V direction return all such V-positions or only the first one found?

### Gregory's Answer

## KB Synthesis

# Answer

**Yes, a single I-address can appear at multiple V-positions within the same POOM via self-transclusion, and `permute` in the I→V direction returns ALL such V-positions, not just the first one.**

## Evidence

### Self-Transclusion Capability

[EC-SELF-TRANSCLUSION] from Finding 0028 explicitly confirms that internal transclusion is valid: "A document can transclude content from itself. Given document containing 'Original', vcopy of 'Orig' (positions 1–4) to the end produces 'OriginalOrig'. The transcluded portion shares I-position identity with the original content within the same document."

### POOM as Multimap

[SS-POOM-MULTIMAP] from Finding 0039 establishes the structural foundation:

> "The POOM (Permutation Of Ordered Mappings) is a 2D enfilade (B-tree) that stores `(V-position, I-address)` entries. Critically, it functions as a **multimap**: a single I-address can map to multiple V-positions within the same document."

### Retrieval Returns All Matches

Finding 0039 specifies the retrieval behavior:

> "The search algorithm `findcbcinarea2d()` traverses all siblings at each B-tree level and recursively descends into all qualifying subtrees, **accumulating every matching leaf node**. The accumulation function `incontextlistnd()` inserts each found context into a sorted linked list, **never replacing existing entries**. This means a query by I-address returns **ALL V-positions** referencing that address."

### Concrete Example

Finding 0039 provides verification:

```
Document has "B" at V-positions 1.2, 1.4, and 1.5, all referencing I-address i_B.

ispan2vspanset(poom, i_B) = {
  VSpan(1.2, width=0.1),
  VSpan(1.4, width=0.1),
  VSpan(1.5, width=0.1)
}

Result set cardinality = 3 (one per V-position referencing i_B)
```

### Link Discovery Confirms Behavior

[INV-LINK-IDENTITY-DISCOVERY] from Finding 0039 extends this to link discovery:

> "Links bound to an I-address are discoverable from ALL V-positions that reference that I-address, including multiple positions within the same document created by internal transclusion."

## Implementation Details

The retrieval path is:
- `ispan2vspanset()` → `permute()` → `span2spanset()` → `findcbcinarea2d()` → `incontextlistnd()`

**Code references:**
- `orglinks.c:389-394` — `ispan2vspanset()` delegates to `permute()` with direction I→V
- `retrie.c:229-268` — `findcbcinarea2d()` B-tree traversal accumulates all matches
- `context.c:75-111` — `incontextlistnd()` accumulates without replacement

**Provenance:** [SS-POOM-MULTIMAP], [EC-SELF-TRANSCLUSION], [INV-LINK-IDENTITY-DISCOVERY]

## Code Exploration

Perfect! Now I have traced the complete execution path. Let me write my final answer with all code citations.

---

## Answer: Self-Transclusion and I→V Mapping in udanax-green

**Yes, a single I-address span can appear at multiple V-positions within the same POOM (self-transclusion is possible), and `permute` in the I→V direction returns ALL such V-positions, not just the first one.**

### Evidence from Code

#### 1. Self-Transclusion Is Possible

There are no constraints in `insertpm` [orglinks.c:75-134] that prevent inserting the same I-address at multiple V-positions. The function validates:
- Zero tumbler check [orglinks.c:86]
- Negative vsa check [orglinks.c:93]  
- Zero width check [orglinks.c:121]

None of these prevent duplicate I-addresses at different V-positions.

#### 2. Permute Returns ALL V-Positions

The I→V conversion path is:

**Entry point**: `ispan2vspanset` [orglinks.c:389-393]
```c
typevspanset *ispan2vspanset(typetask *taskptr, typeorgl orgl, typeispan *ispanptr, typevspanset *vspansetptr)
{
  typespanset *permute();
	return permute(taskptr, orgl, ispanptr, I, vspansetptr, V);
}
```

**Core function**: `permute` [orglinks.c:404-422]
```c
typespanset *permute(typetask *taskptr, typeorgl orgl, typespanset restrictionspanset, INT restrictionindex, typespanset *targspansetptr, INT targindex)
{
  // ...
  for (; restrictionspanset; restrictionspanset = restrictionspanset->next) {
    targspansetptr = span2spanset(taskptr, orgl, restrictionspanset, restrictionindex, targspansetptr, targindex);
  }
  return (save);
}
```

**Critical step**: `span2spanset` [orglinks.c:425-454]
```c
typespanset *span2spanset(typetask *taskptr, typeorgl orgl, typespanset restrictionspanptr, INT restrictionindex, typespanset *targspansetptr, INT targindex)
{
  typecontext *context, *c, *retrieverestricted();
  // ...
  context = retrieverestricted((typecuc*)orgl, restrictionspanptr, restrictionindex, (typespan*)NULL, targindex, (typeisa*)NULL);
  for (c = context; c; c = c->nextcontext) {  // LOOPS THROUGH ALL CONTEXTS
    context2span (c, restrictionspanptr, restrictionindex, &foundspan, targindex);
    nextptr = (typespan *)onitemlist (taskptr, (typeitem*)&foundspan, (typeitemset*)targspansetptr);
  }
  // ...
}
```

**Tree traversal**: `findcbcinarea2d` [retrie.c:229-268]
```c
int findcbcinarea2d(typecorecrum *crumptr, typedsp *offsetptr, tumbler *span1start, tumbler *span1end, INT index1, tumbler *span2start, tumbler *span2end, INT index2, typecontext **headptr, typebottomcruminfo *infoptr)
{
  for (; crumptr; crumptr = getrightbro (crumptr)) {  // WALKS ALL SIBLINGS
    if (!crumqualifies2d (...)) continue;
    if (crumptr->height != 0) {
      // Recurse into children
      findcbcinarea2d (findleftson ((typecuc*)crumptr), &localoffset, ...);
    } else {
      context = makecontextfromcbc ((typecbc*)crumptr, (typewid*)offsetptr);
      incontextlistnd (headptr, context, index1);  // ADDS TO LIST
    }
  }
}
```

**List building**: `incontextlistnd` [context.c:75-111]
```c
int incontextlistnd(typecontext **clistptr, typecontext *c, INT index)
{
  // Inserts context into sorted list, maintaining ALL entries
  // Does not stop at first match - builds complete list
}
```

The algorithm walks the entire tree and collects **every crum** that intersects the I-span into a context list, then converts each context to a V-span.

#### 3. Empirical Proof from Golden Tests

**Test**: `internal_transclusion_with_link` [golden/internal/internal_transclusion_with_link.json]

1. Insert: "Original text here"
2. Transclude "text" to end → "Original text heretext"
3. Create link on FIRST "text" at V-positions 1.10-1.13
4. Search for links from SECOND "text" at V-positions 1.19-1.22
5. **Result**: Link IS found

**Why this proves ALL positions are returned:**

Link finding [spanf1.c:56-103] uses this path:
1. Convert V-spec to I-span via `vspanset2ispanset` → `permute` [orglinks.c:397-401]
2. Find links at I-addresses via `sporglset2linkset` [sporgl.c:222-269]

The link was created on V-position 1.10-1.13 but discovered from V-position 1.19-1.22. Both positions map to the same I-address. The ONLY way this works is if `permute` returns both V-positions when converting I→V during link discovery.

**Additional test**: `internal_transclusion_multiple_copies` [golden/internal/internal_transclusion_multiple_copies.json]

Creates three copies of "B" at V-positions 1.2, 1.4, and 1.5. All three are recognized as sharing identity via `compare_versions`, confirming all three V-positions map to the same I-address and all are discovered during I→V conversion.

### Conclusion

1. **Self-transclusion works**: Same I-address can exist at multiple V-positions
2. **Permute is exhaustive**: Returns ALL V-positions, not just the first
3. **Implementation**: Tree traversal collects all matching crums via `findcbcinarea2d` → `incontextlistnd`
4. **Verified behavior**: Golden tests demonstrate link discovery across multiple V-positions with shared I-addresses

---

## Question 15 [gregory]

> When `vspanset2sporglset` walks the POOM to convert V-spans to I-spans, does it handle the case where a single contiguous V-span maps to multiple non-contiguous I-address ranges — specifically, how many sporgl entries does it produce for a V-span that crosses an I-address discontinuity?

### Gregory's Answer

## KB Synthesis

# Answer: One sporgl per contiguous I-address region

When `vspanset2sporglset` walks the POOM to convert V-spans to I-spans, **it produces one sporgl for each contiguous I-address region**, regardless of how many V-spans were in the input. A single contiguous V-span that crosses an I-address discontinuity produces multiple sporgls.

## The Mechanism

The conversion chain is `[ST-LINK-CREATE, Finding 0037]`:

1. **`vspanset2ispanset`** walks the POOM tree via `permute` → `span2spanset` → `retrieverestricted` to discover all I-address regions
2. **Returns one I-span per contiguous I-address range** (not per V-span)
3. **Inner loop at `sporgl.c:49-58`** iterates over every I-span and creates one sporgl per I-span

The key code is `[ST-LINK-CREATE]`:
```c
// sporgl.c:49-58 — inner loop creating one sporgl per I-span
for (; ispanset; ispanset = next) {
    // ... create sporgl from this I-span ...
}
```

## Concrete Example `[ST-LINK-CREATE]`

Document C contains "AABB" at V-positions 1.1–1.4 where:
- "AA" was transcluded from document A (I-addresses from A's permascroll)
- "BB" was transcluded from document B (I-addresses from B's permascroll)

```
create_link(source = V-span 1.1 width 0.4 in doc C, ...)

Input:  1 V-span covering all of "AABB"
Output: 2 sporgls in source endset:
  sporgl₁: origin = I-addr(A,"AA"), width = 0.2, doc = C
  sporgl₂: origin = I-addr(B,"BB"), width = 0.2, doc = C
```

The I-addresses for A and B are non-contiguous in the permascroll, so they **cannot** be represented as a single I-span. The split happens automatically during POOM traversal.

## Why This Matters

`[SS-LINK-ENDPOINT, Finding 0037]` establishes the formal property: **`|Endset| ≥ |input_vspans|`**. The endset cardinality is determined by the I-address structure of the referenced content, not by the number of V-spans provided.

This splitting is essential for:
- **`[INT-LINK-TRANSCLUSION]`**: Links work correctly when endpoints reference transcluded content from multiple sources
- **`[EC-LINK-PARTIAL-SURVIVAL]`**: Each sporgl independently tracks its content; partial deletion affects individual sporgls, not the entire endset atomically
- **`[INT-SPORGL-VERSION-COMPARE]`**: Version comparison intersects sporgls by I-address to find shared content

The mechanism also applies to other operations using sporgls `[INT-SPORGL-TRANSCLUSION]`: vcopy uses the same conversion path to carry I-address identity through the copy operation.

## Code Exploration

Now I have traced through the complete execution path. Let me write a comprehensive answer:

---

## Answer: Multiple sporgl entries per I-address discontinuity

When `vspanset2sporglset` walks the POOM to convert V-spans to I-spans, **it produces one sporgl entry for each contiguous I-address segment**. If a single V-span maps to multiple non-contiguous I-address ranges, it produces multiple sporgl entries.

### The Conversion Flow

**1. Entry point: `vspanset2sporglset` [sporgl.c:35-65]**

The function iterates through each V-span in the input set:

```c
for (; vspanset; vspanset = vspanset->next) {
    (void) vspanset2ispanset (taskptr, orgl, vspanset, &ispanset);
    for (; ispanset; ispanset = ispanset->next) {
           sporglset = (typesporgl *) taskalloc (taskptr, sizeof(typesporgl));
           // ... create sporgl from this I-span ...
           *sporglsetptr = (typesporglset)sporglset;
           sporglsetptr = (typesporglset *)&sporglset->next;
    }
}
```

Line 48 converts one V-span to potentially multiple I-spans, then lines 49-58 create **one sporgl for each I-span** returned.

**2. V→I conversion: `vspanset2ispanset` → `permute` → `span2spanset` [orglinks.c:397-454]**

The conversion delegates to `span2spanset`, which calls `retrieverestricted` to walk the POOM:

```c
context = retrieverestricted((typecuc*)orgl, restrictionspanptr, restrictionindex, 
                             (typespan*)NULL, targindex, (typeisa*)NULL);
for (c = context; c; c = c->nextcontext) {
    context2span (c, restrictionspanptr, restrictionindex, &foundspan, targindex);
    nextptr = (typespan *)onitemlist (taskptr, (typeitem*)&foundspan, 
                                      (typeitemset*)targspansetptr);
}
```

Lines 439-445 show that **each context entry produces a separate I-span**.

**3. POOM traversal: `retrieverestricted` → `findcbcinarea2d` [retrie.c:56-268]**

The POOM walk at line 262-263 creates one context per bottom crum (CBC):

```c
for (; crumptr; crumptr = getrightbro (crumptr)) {
    if (!crumqualifies2d (crumptr, offsetptr, span1start, span1end, index1, 
                          span2start, span2end, index2, (type2dbottomcruminfo*)infoptr)){
        continue;
    }
    if (crumptr->height != 0) {
        // recurse down...
        findcbcinarea2d (findleftson ((typecuc*)crumptr), &localoffset, 
                         span1start, span1end, index1, span2start, span2end, 
                         index2, headptr, infoptr);
    } else {
        context = makecontextfromcbc ((typecbc*)crumptr, (typewid*)offsetptr);
        incontextlistnd (headptr, context, index1);
    }
}
```

**Each CBC that intersects the V-span produces its own context entry** [retrie.c:262-263]. The `incontextlistnd` function [context.c:75-111] inserts contexts into a sorted list without merging.

**4. Context extraction: `context2span` [context.c:176-212]**

Each context entry is converted to a span:

```c
movetumbler (&grasp.dsas[idx2], &foundspanptr->stream);
tumblersub(&reach.dsas[idx2],&grasp.dsas[idx2],&foundspanptr->width);
foundspanptr->itemid = index2itemid (idx2, context);
```

Lines 206-209 extract the stream and width from the context's target index to produce one I-span.

### The Answer

**A single V-span that crosses an I-address discontinuity produces N sporgl entries, where N equals the number of bottom crums (CBCs) in the POOM that intersect that V-span.**

Since each CBC represents a contiguous segment of the POOM mapping, and I-address discontinuities are represented by separate CBCs with gaps between them, **you get one sporgl entry per contiguous I-address segment**.

For example, if a V-span maps to:
- I-span [0.1, 0.5) 
- I-span [0.8, 1.2)

with a discontinuity at 0.5-0.8, then `vspanset2sporglset` produces **two sporgl entries** — one for each contiguous segment.

---

## Question 16 [gregory]

> Does the POOM enforce that every V-position maps to exactly one I-address (bijectivity in the V→I direction), or can the tree structure represent overlapping V-ranges that map to different I-addresses?

### Gregory's Answer

## KB Synthesis

# POOM V→I Mapping: Function, Not Bijection

The POOM enforces that **every V-position maps to exactly one I-address**, but **does not enforce bijection** in the strict mathematical sense. The mapping is a function in the V→I direction but a multimap in the I→V direction.

## Core Structure: Non-Overlapping V-Ranges

The POOM bottom crums represent contiguous V-range to I-range mappings [SS-POOM-BOTTOM-CRUM]. Each crum contains:
```
BottomCrum = {
  origin: { dsas[V]: V-start, dsas[I]: I-start },
  width:  { dsas[V]: V-width,  dsas[I]: I-width }
}
```

The tree structure enforces **non-overlapping V-ranges** across crums:

1. **Knife-cutting mechanisms** [SS-TWO-BLADE-KNIFE, ST-DELETE] use `whereoncrum()` to classify each crum as being before, interior, or after an operation range. This classification assumes crums partition the V-space — overlapping ranges would make classification ambiguous.

2. **Retrieval logic** [INV-RETRIEVAL-V-SORTED] accumulates contexts by sorting them in V-address order. Overlapping V-ranges would produce undefined behavior (which context wins for an overlapping V-position?).

3. **Coalescing via extension** [ST-INSERT, Finding 0062]: The `isanextensionnd()` check merges adjacent same-homedoc insertions, which prevents creating overlapping crums for contiguous content.

## The Multimap Property: I→V, Not V→I

Multiple V-positions **can** map to the same I-address, but this occurs through **multiple non-overlapping crums** mapping to the same I-range [SS-POOM-MULTIMAP]:

```
Internal transclusion creates:
  Crum 1: V[1.2, 1.3) → I[i_B, i_B+0.1)
  Crum 2: V[1.4, 1.5) → I[i_B, i_B+0.1)  (same I-range)
  Crum 3: V[1.5, 1.6) → I[i_B, i_B+0.1)  (same I-range)
```

Each V-position appears in exactly one crum [INV-POOM-BIJECTIVITY]. That crum defines a single I-address for that position. Therefore:
- **V→I is a function** (single-valued): `poom(v) = i`
- **I→V is a multimap**: `poom⁻¹(i) = {v₁, v₂, v₃, ...}`

This is validated by test scenarios [EC-SELF-TRANSCLUSION, Finding 0039]: "A document can reference the same I-address at N distinct V-positions (tested with N=2 and N=3)."

## The "Bijectivity" Invariant (I₁)

Finding 0053 references "EWD-018 invariant I₁: `poom_d` is a bijection" [INV-POOM-BIJECTIVITY]. However, the actual invariant enforced is:

```
forall v in valid_V_addresses: exists unique i: poom(v) = i
```

The "bijection" language is misleading given the multimap property. What I₁ actually enforces is:
1. **Domain constraint**: Every V-address in the document's extent has a mapping
2. **Functional property**: Each V-address maps to exactly one I-address
3. **No overlapping V-ranges**: Each V-position belongs to exactly one crum

The invariant can be **violated** by DELETE creating negative V-positions [INV-POOM-BIJECTIVITY]:
> "DELETE can violate this invariant by creating POOM entries with negative V-positions. A negative V-position is in the domain of the stored POOM map but does not correspond to any valid V-address in the document's V-stream."

## Conclusion

**The POOM enforces that V-ranges do not overlap.** Each V-position maps to exactly one I-address via the unique crum containing that position. Overlapping V-ranges would violate the tree structure's partitioning assumption and break retrieval, insertion, and deletion algorithms that depend on `whereoncrum()` classification. The multimap property exists only in the I→V direction through internal transclusion creating multiple non-overlapping crums that reference the same I-addresses.

## Code Exploration

Now I have enough information to provide a complete answer. Let me write up my findings with specific code citations.

---

# Answer: The POOM Enforces Bijectivity in V→I Direction

**The POOM strictly enforces that every V-position maps to exactly one I-address.** The tree structure cannot represent overlapping V-ranges that map to different I-addresses. This is enforced through multiple mechanisms in the code:

## 1. Gap-Making Mechanism Prevents Overlaps

**[insertnd.c:124-172] `makegappm`**

Before inserting new V→I mappings, the system creates a "gap" in V-space:

```c
for (ptr = findleftson (father); ptr; ptr = findrightbro (ptr)) {
    i=insertcutsectionnd(ptr,&fgrasp,&knives);
    switch (i) {
        ...
        case 1:/*9-17-87 fix */
            tumbleradd(&ptr->cdsp.dsas[V],&width->dsas[V],&ptr->cdsp.dsas[V]);
            ivemodified (ptr);
            break;
```

**[insertnd.c:162]** - Crums positioned after the insertion point have their V-displacement **shifted right** by the insertion width. This ensures that all existing content after the insertion point moves to make room, preventing any overlap.

## 2. Tree Structure Maintains Non-Overlapping Ranges

**[retrie.c:345-398] `whereoncrum`**

The retrieval system classifies where an address falls relative to a crum:

```c
INT whereoncrum(typecorecrum *ptr, typewid *offset, tumbler *address, INT index)
{
    ...
    case POOM:
        tumbleradd(&offset->dsas[index],&ptr->cdsp.dsas[index], &left);
        cmp = tumblercmp(address,&left);
        if(cmp == LESS){
            return(TOMYLEFT);
        }else if(cmp == EQUAL){
            return(ONMYLEFTBORDER);
        }
        tumbleradd (&left, &ptr->cwid.dsas[index], &right);
        cmp = tumblercmp(address,&right);
        if(cmp == LESS){
            return(THRUME);  // address is within this crum
        }...
```

**[retrie.c:356-367]** - This function returns **exactly one classification**. There is no code path for "address could be in multiple crums" - the data structure assumes this is impossible.

## 3. Retrieval Breaks on First Match

**[retrie.c:208-227] `findcbcnd`**

When looking up a V-address to find its I-mapping:

```c
if (father->height != 0) {
    prologuend (father, offsetptr, &grasp, (typedsp*)NULL);
    for (ptr = findleftson ((typecuc*)father); ptr; ptr = getrightbro (ptr))
        if (retr = findcbcnd (ptr, &grasp, address, index))
            break;  // <-- BREAKS ON FIRST MATCH
}
```

**[retrie.c:221]** - The code **breaks as soon as it finds a match** among sibling crums. This would be incorrect if overlapping ranges were possible - the system assumes each V-address can be in at most one child.

## 4. Cutting Mechanism Splits Overlapping Crums

**[ndcuts.c:77-90] `makecutsbackuptohere`**

When making cuts in the tree (during rearrange or insert operations):

```c
if (ptr->height == 0) {
    for (i = 0; i < knives->nblades; i++) {     
        if (whereoncrum((typecorecrum*)ptr, offset, &knives->blades[i], 
                        knives->dimension) == THRUME) {
            new = (typecuc *)createcrum((INT)ptr->height,(INT)ptr->cenftype);
            ...
            slicecbcpm((typecorecrum*)ptr, offset, (typecorecrum*)new, 
                      &knives->blades[i], knives->dimension);
```

**[ndcuts.c:79-84]** - If a cut passes **through** a crum (`THRUME` means "cut is inside this crum"), the crum is **split into two pieces**. This maintains the invariant that each crum represents a single contiguous range with no internal gaps or ambiguities.

## 5. Insertion Finds Single Target Crum

**[insertnd.c:277-299] `findsontoinsertundernd`**

When inserting, the system finds which child should contain the new content:

```c
for (; ptr; ptr = findrightbro(ptr)) {
    tumbleradd(&grasp->dsas[index],&ptr->cdsp.dsas[index],&sonstart);
    ...
    if (
       whereoncrum(ptr,grasp,&origin->dsas[index],index)>=ONMYLEFTBORDER
    && whereoncrum (ptr, grasp, &spanend, index) <= ONMYRIGHTBORDER)
        return (ptr);  // <-- RETURNS FIRST MATCH
}
```

**[insertnd.c:293-296]** - Returns **a single crum** that contains the insertion range. No provision for "insertion could go under multiple crums" - the structure guarantees this cannot happen.

## Conclusion

**The POOM enforces strict bijectivity in the V→I direction.** The tree structure maintains these invariants:

1. **Sibling crums have non-overlapping, ordered V-ranges** - enforced by `makegappm` shifting content during insertion
2. **Each V-position falls into exactly one crum at each level** - assumed by `whereoncrum` returning a single classification
3. **V→I lookups return exactly one result** - `findcbcnd` breaks on first match
4. **Crums that span cut points are split** - `makecutsbackuptohere` maintains single contiguous ranges

Every V-position maps to exactly one path through the tree → one bottom crum → one I-address. The data structure cannot represent overlapping V-ranges mapping to different I-addresses.

---

## Question 17 [gregory]

> When `makegappm` shifts V-positions during INSERT, does it modify the I-displacement or I-width fields of the shifted POOM entries in any way, or are those fields guaranteed untouched?

### Gregory's Answer

## KB Synthesis

# Answer: I-dimension Fields Are Guaranteed Untouched

When `makegappm` shifts V-positions during INSERT, the I-displacement and I-width fields of shifted POOM entries are **guaranteed untouched**. Only the V-dimension component is modified.

## Evidence from the Knowledge Base

### Explicit Code-Level Evidence

[ST-INSERT] from Finding 0054 provides the precise mechanism:

> The `makegappm` function classifies existing POOM crums [...] case 1 (THRUME — beyond insertion point) are shifted by adding the insertion width to their V-dimension displacement.

The actual operation at `backend/insertnd.c:162` is:

```c
tumbleradd(&ptr->cdsp.dsas[V], &width->dsas[V], &ptr->cdsp.dsas[V])
```

This explicitly operates on the **V-component only** (`dsas[V]`). The I-component (`dsas[I]`) is never referenced in the shift operation.

### Structural Confirmation

[SS-POOM-BOTTOM-CRUM] from Finding 0076 confirms that POOM crums store dual-space coordinates:

> Each crum contains an origin and width in both V-space and I-space

The fields are:
- `cdsp.dsas[V]` — V-displacement (modified by shift)
- `cdsp.dsas[I]` — I-displacement (untouched)
- `cwid.dsas[V]` — V-width (encoding of width at V-space precision)
- `cwid.dsas[I]` — I-width (direct copy from I-space span)

### Invariant-Level Guarantee

[INV-IADDR-IMMUTABILITY] from Finding 0030 establishes the system-wide invariant:

> I-addresses, once assigned to content, never change. INSERT shifts V-addresses but preserves every existing I-address assignment.

And [FC-INSERT-IADDR] states:

> INSERT does not modify the I-address of any pre-existing content [...] Within the target document, existing I-addresses are preserved — only V-addresses change.

### Parallel from REARRANGE

[INV-REARRANGE-IDENTITY] from Finding 0056 confirms the same pattern holds for REARRANGE:

> The code modifies only `ptr->cdsp.dsas[index]` (the V-address component of the displacement). The I-address, stored separately, is never touched.

## Summary

The shift operation in `makegappm` is a pure V-dimension operation:
- **Modified**: `cdsp.dsas[V]` (V-displacement increased by insertion width)
- **Untouched**: `cdsp.dsas[I]` (I-displacement), `cwid.dsas[I]` (I-width), `cwid.dsas[V]` (V-width)

This selective modification is what preserves content identity ([INV-IADDR-IMMUTABILITY]) while shifting content position in the document's visible V-stream.

## Code Exploration

Perfect. Now I have all the information needed to answer your question definitively.

---

## Answer: I-displacement and I-width fields are **guaranteed untouched**

When `makegappm` shifts V-positions during INSERT, it **only** modifies the V-displacement field of shifted POOM entries. The I-displacement and I-width fields remain completely untouched.

### Data Structure Layout

For POOM entries, the displacement and width structures contain two dimensions [wisp.h:41-42]:

```c
pm:  |    I          I
     |      V          V
```

- `ptr->cdsp.dsas[I]` — I-displacement
- `ptr->cdsp.dsas[V]` — V-displacement  
- `ptr->cwid.dsas[I]` — I-width
- `ptr->cwid.dsas[V]` — V-width

### The Only Modification in `makegappm`

The function loops through POOM entries and classifies them using `insertcutsectionnd`, which returns:
- `0` or `2`: Entry doesn't need shifting
- `1`: Entry is to the left of the insertion point and needs shifting
- `-1`: Error (THRUME)

**The only field modification occurs at [insertnd.c:162]:**

```c
case 1:/*9-17-87 fix */
    tumbleradd(&ptr->cdsp.dsas[V],&width->dsas[V],&ptr->cdsp.dsas[V]);
    ivemodified (ptr);
    break;
```

This adds the insertion width to the **V-displacement only**. It does NOT touch:
- `ptr->cdsp.dsas[I]` (I-displacement)
- `ptr->cwid.dsas[I]` (I-width)
- `ptr->cwid.dsas[V]` (V-width)

### Other Operations in `makegappm`

**`setwidnd(father)` [insertnd.c:170; wisp.c:235-247]:**
- Recalculates the father's width by taking the maximum of all child widths
- Only **reads** child widths via `lockmax` comparisons
- Only **writes** to `father->cwid`, never to children

**`makecutsnd` [insertnd.c:148; ndcuts.c:15-31]:**
- Splits crums at the insertion boundaries to prepare for the gap
- Does not shift positions or modify widths
- Only creates new crums at split points

### Conclusion

The I-displacement (`ptr->cdsp.dsas[I]`) and I-width (`ptr->cwid.dsas[I]`) fields of shifted POOM entries are **guaranteed untouched** by `makegappm`. Only the V-displacement (`ptr->cdsp.dsas[V]`) is modified during the shift operation.

This makes sense architecturally: INSERT operations affect the V-dimension (version space), while the I-dimension (content addresses) represents immutable content that never shifts.

---

## Question 18 [gregory]

> If content at I-address range [X, X+5] is transcluded into two documents and then deleted from one, does `findlinksfromtothreesp` still find links through the surviving document's POOM — confirming that I-space permanence makes link discovery independent of any single document's V-space state?

### Gregory's Answer

## KB Synthesis

# Answer: Yes, with Important Nuances

Link discovery **continues to work through the surviving document's POOM**, confirming I-space permanence, but the deleted document creates a "stale reference" that reveals the system's layered architecture.

## The Three-Layer Structure

The scenario demonstrates three independent persistence layers [SS-THREE-LAYER-MODEL]:

1. **I-space (permanent layer)**: Content at I-addresses [X, X+5] exists permanently in the granfilade [INV-IADDRESS-PERMANENT]
2. **Spanfilade (append-only index)**: Link L is indexed by I-addresses [X, X+5] in the spanf [INV-SPANF-WRITE-ONLY]
3. **POOM (mutable view)**: Each document's V→I mapping layer [SS-POOM-MUTABILITY]

## Step-by-Step Behavior

**After transclusion into Documents A and B:**
- Both documents' POOMs map their V-positions to the same I-addresses [X, X+5] [ST-VCOPY]
- Link L is indexed in spanf by those I-addresses [SS-SPANF-OPERATIONS]
- Both documents can discover link L via content identity [INV-LINK-GLOBAL-VISIBILITY]

**After DELETE from Document A:**
- Document A's POOM removes V→I mappings for [X, X+5] [ST-DELETE]
- Document B's POOM is **completely unaffected** [FC-DELETE-CROSS-DOC]
- Spanf index **retains all entries** — no deletion function exists [INV-SPANF-WRITE-ONLY]
- I-addresses [X, X+5] remain permanent in granfilade [INV-IADDRESS-PERMANENT]

## Link Discovery Through Document B

`findlinksfromtothreesp` works through Document B because [ST-FIND-LINKS]:

1. Query specset from B is converted to I-addresses via `vspanset2sporglset` [ST-VSPAN-TO-SPORGL]
2. Document B's POOM **still maps** V-positions to I-addresses [X, X+5]
3. These I-addresses query the spanf index directly [SS-SPANF-OPERATIONS]
4. Spanf returns link L because the I-address mapping is permanent

The search path: **B's V-space → B's POOM → I-addresses [X, X+5] → spanf lookup → link L found**

## The Stale Reference Phenomenon

Document A creates an edge case [EC-STALE-SPANF-REFERENCE]:
- `find_documents([X, X+5])` **still returns A** (spanf never removes entries)
- But A's POOM has no V→I mappings for those I-addresses
- Attempting to **resolve** those I-addresses through A yields empty [INV-ITOV-FILTERING]
- A's stale spanf entry is **harmless** — it causes no corruption, just returns a superset

The formal invariant: `actual_docs(i) ⊆ find_documents(i)` but not vice versa [EC-STALE-SPANF-REFERENCE].

## Confirming I-Space Independence

This confirms three critical properties:

1. **I-addresses are the source of truth** [INV-IADDRESS-PERMANENT]: Once allocated, they never change or disappear
2. **Link discovery is I-space-based** [INT-LINK-TRANSCLUSION]: Links are indexed by content identity, not document membership
3. **V-space deletion is local** [FC-DELETE-CROSS-DOC]: Removing content from one document's view has zero effect on other documents

As long as **any document maintains a V→I mapping** to the content, links remain discoverable through that document [INT-TRANSCLUSION-LINK-SEARCH]. The system is robust to partial deletion — link discovery degrades gracefully, not catastrophically.

## Practical Implications

- Links survive **distributed across multiple documents** via transclusion
- Deleting source content doesn't destroy links if copies exist
- The "stale reference" in A is a discovery artifact, not a correctness violation
- Document B becomes the **functional discovery path** after A is deleted

**Final answer: YES** — `findlinksfromtothreesp` successfully finds links through Document B's POOM, proving that I-space permanence makes link discovery independent of any single document's V-space state. The surviving document provides the V→I bridge to the permanent I-space layer where links are indexed.

## Code Exploration

Based on my analysis of the source code, I can now answer your question definitively.

## Answer: YES

**`findlinksfromtothreesp` DOES find links through the surviving document's POOM, confirming I-space permanence.**

Here's the execution path and evidence:

### 1. Link Discovery Operates in I-Space

When `findlinksfromtothreesp` is called [spanf1.c:56-103], it:

**Converts V-space to I-space** [spanf1.c:71-75]:
```c
if (fromvspecset)
    specset2sporglset (taskptr, fromvspecset, &fromsporglset,NOBERTREQUIRED);
if (tovspecset)
    specset2sporglset (taskptr, tovspecset, &tosporglset,NOBERTREQUIRED);
if (threevspecset)
    specset2sporglset (taskptr, threevspecset, &threesporglset,NOBERTREQUIRED);
```

**Searches the spanfilade using I-space ranges** [spanf1.c:77, 85, 93]:
```c
sporglset2linkset (taskptr, (typecuc*)spanfptr, fromsporglset, &fromlinkset, orglrange, LINKFROMSPAN);
```

### 2. V→I Conversion Uses Document's POOM

The conversion path `specset2sporglset` → `vspanset2sporglset` [sporgl.c:35-65]:

```c
// Line 44: Find document's POOM
if (!findorgl (taskptr, granf, docisa, &orgl,type)){
    return (NULL);
}
// Line 48: Convert V-spans to I-spans using POOM
(void) vspanset2ispanset (taskptr, orgl, vspanset, &ispanset);
```

This calls `vspanset2ispanset` [orglinks.c:397-402], which uses the POOM to convert V-space addresses to I-space addresses via the `permute` function.

### 3. Spanfilade Search is I-Space Based

`sporglset2linksetinrange` [sporgl.c:239-269] searches the spanfilade enfilade:

```c
// Line 259: Retrieve from spanfilade using I-space range
context = retrieverestricted (spanfptr, (typespan*)sporglset, SPANRANGE, &range, ORGLRANGE, (typeisa*)infoptr);
// Lines 263-266: Extract link addresses from results
for (c = context; c; c = c->nextcontext) {
    beheadtumbler(&c->totaloffset.dsas[ORGLRANGE],&linksa);
    onlinklist (taskptr, linksetptr, &linksa);
}
```

The spanfilade is indexed by I-space addresses in the SPANRANGE dimension. The search does NOT depend on any document's POOM — it operates purely on I-space coordinates.

### 4. Deletion Only Affects V-Space POOM

When content is deleted via `dodeletevspan` [do1.c:158-167]:

```c
return (
   findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
&& deletevspanpm (taskptr, docisaptr, docorgl, vspanptr)
);
```

This only modifies the document's POOM (removes V→I mapping). It does NOT:
- Delete the I-space content from the granfilade
- Remove link entries from the spanfilade
- Affect other documents' POOMs

### 5. The Complete Flow

**Scenario:**
1. Content at I-range [X, X+5] exists
2. Doc A and Doc B both transclude it (both POOMs map V-spans → I-span [X, X+5])
3. Link created with source at I-range [X, X+5]
4. Content deleted from Doc A (Doc A's POOM no longer maps to [X, X+5])
5. Search for links via Doc B's V-span

**What happens:**
- Doc B's POOM converts V-span → I-span [X, X+5] [sporgl.c:48]
- `sporglset2linkset` searches spanfilade for links at I-range [X, X+5] [sporgl.c:259]
- Spanfilade returns link because it's indexed by I-space, not V-space
- **Link is found** ✓

### Conclusion

This confirms **I-space permanence**: Link discovery is independent of any single document's V-space state. The link exists in I-space (in the spanfilade), and as long as ANY document has a POOM mapping to that I-range, the link can be discovered through that document.

The surviving document (Doc B) can find the link because:
1. Its POOM still maps V-space → I-space [X, X+5]
2. The spanfilade still contains the link at I-space [X, X+5]  
3. The search operates entirely in I-space after the initial V→I conversion

---

## Question 19 [gregory]

> When `findisatoinsertmolecule` queries the granfilade for max+1 allocation, does it search only within the target document's I-address subtree, or could a concurrent session's allocation under a different document influence the result?

### Gregory's Answer

## KB Synthesis

Looking at the allocation mechanism in detail:

## Per-Document Scoping

`findisatoinsertmolecule` searches **within the target document's I-address subtree**, not globally. Concurrent sessions allocating under different documents use independent allocation sequences and cannot interfere with each other.

### Evidence from Knowledge Base

**[ST-ADDRESS-ALLOC] Finding 0065** is explicit for link allocation:
- `upperbound` is set to `docISA.2.3` (bounding search to the document's link subspace)
- "the new link's I-address is strictly greater than all existing link I-addresses in **the same document**, and independent of link I-addresses in **other documents**"

**[INV-MONOTONIC] Finding 0065** demonstrates per-document independence:
```
MAKELINK(docA) → docA.2.1
MAKELINK(docB) → docB.2.1  
MAKELINK(docA) → docA.2.2  (monotonic within A despite intervening B)
```

Both documents can have `.2.1` independently — only possible with document-scoped search.

**[SS-ADDRESS-SPACE] Finding 0077** formalizes the partitioning:
- "allocation is a family of independent functions partitioned by tumbler range"  
- `next_content_addr(granf, doc) = max_content(granf, doc) + 1`
- The `doc` parameter indicates per-document scoping

### Mechanism

From **[ST-ADDRESS-ALLOC] Finding 0065**, the code reference shows:
```c
tumblerincrement(&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound)
```

Where:
- `hintptr->hintisa` = document ISA
- Level 2 = element_field position in hierarchy
- `atomtype + 1` = increment amount (LINKATOM=2 → 3, TEXTATOM=1 → 2)

This computes an upperbound from the document ISA that restricts `findpreviousisagr` to search only within that document's address subtree.

### Cross-Type Interference Within a Document

**[INT-LINK-INSERT] Finding 0063** shows that text and link orgls **do** share allocation within the same document:
```
INSERT "ABC" → I.1, I.2, I.3
CREATELINK   → link orgl at ~I.2.0  
INSERT "DEF" → I.2.1+ (gap from link orgl)
```

So the allocation sequence is:
- Per-document: docA and docB have independent sequences
- Cross-type: within one document, text atoms and link orgls compete for the same counter

### Answer

A concurrent session allocating content under document B **cannot** influence allocation in document A. Each document maintains an independent `max + 1` allocation counter within its tumbler subtree. The granfilade is a single flat tree, but `findisatoinsertmolecule` bounds its search using document-scoped upper limits computed from the target document's ISA.

## Code Exploration

---

# Answer: Molecule Allocation is Document-Isolated

**Short answer: `findisatoinsertmolecule` searches ONLY within the target document's I-address subtree.** Concurrent allocations in different documents cannot interfere with each other.

## How It Works

### 1. Upperbound Constraint

`backend/granf2.c:158-164` shows the allocation entry point:

```c
static int findisatoinsertmolecule(typecuc *fullcrumptr, typehint *hintptr, typeisa *isaptr)
{
  typeisa upperbound, lowerbound;

  tumblerincrement (&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound);
  clear (&lowerbound, sizeof(lowerbound));
  findpreviousisagr ((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);
```

The `upperbound` is computed by **extending the document's hintisa address**. For document `1.1.0.1.0.1` allocating text (TEXTATOM=1), the upperbound becomes approximately `1.1.0.1.0.1.0.0.2`.

### 2. Search Algorithm

`backend/granf2.c:255-278` implements `findpreviousisagr`:

```c
int findpreviousisagr(typecorecrum *crumptr, typeisa *upperbound, typeisa *offset)
{ RECURSIVE
  INT tmp;
  typecorecrum *ptr, *findleftson();

  if (crumptr->height == 0) {
    findlastisaincbcgr ((typecbc*)crumptr, offset);
    return(0);
  }
  for (ptr = findleftson((typecuc*)crumptr); ptr; ptr = findrightbro(ptr)) {
    if (
     (tmp= whereoncrum (ptr, (typewid*)offset, upperbound, WIDTH)) == THRUME
    || tmp == ONMYRIGHTBORDER
    || !ptr->rightbro) {
      findpreviousisagr (ptr, upperbound, offset);
      return(0);
    } else {
      tumbleradd(offset, &ptr->cwid.dsas[WIDTH], offset);
    }
  }
}
```

This walks the granfilade tree, using `whereoncrum` at each node to check if the upperbound falls within that node's range. It finds the **maximum address < upperbound**.

### 3. Range Checking

`backend/retrie.c:345-353` shows how `whereoncrum` works:

```c
INT whereoncrum(typecorecrum *ptr, typewid *offset, tumbler *address, INT index)
{
  tumbler left, right;

  switch (ptr->cenftype) {
    case GRAN:
       tumbleradd (&offset->dsas[WIDTH], &ptr->cwid.dsas[WIDTH], &right);
       return (intervalcmp (&offset->dsas[WIDTH], &right, address));
```

This checks if the upperbound address falls within the interval `[offset, offset+width)` for the current node.

## Isolation Proof

**Example scenario:**
- Document A at `1.1.0.1.0.1`
- Document B at `1.1.0.1.0.2`
- Document B has allocated at `1.1.0.1.0.2.0.0.1`

**When Document A allocates:**
- `upperbound ≈ 1.1.0.1.0.1.0.0.2`
- `findpreviousisagr` searches for max < `1.1.0.1.0.1.0.0.2`

**Tumbler comparison** (`backend/tumble.c:72-85`):
- Compare `1.1.0.1.0.2.0.0.1` (Document B) vs `1.1.0.1.0.1.0.0.2` (upperbound)
- Mantissa comparison: `[1,1,0,1,0,2,...]` vs `[1,1,0,1,0,1,...]`
- At position 5: `2 > 1`
- Result: Document B's address is **GREATER** than the upperbound

Since Document B's allocation is greater than Document A's upperbound, it **will never be returned** by `findpreviousisagr`.

## Conclusion

The search operates on the **entire granfilade** but is **constrained by the upperbound** parameter. Because:

1. The upperbound is derived from the document's hintisa address
2. Tumbler addresses are hierarchical
3. Addresses from different documents have different prefixes
4. Tumbler comparison respects this hierarchy

**Result: Allocations are isolated at the document level.** Concurrent sessions working in different documents cannot interfere with each other's max+1 calculations.

---

## Question 20 [gregory]

> Does the V-width stored in a POOM bottom crum always equal the I-width in logical magnitude, even though they use different tumbler exponents — and is there any operation that could cause them to diverge?

### Gregory's Answer

## KB Synthesis

# Does V-width equal I-width in POOM bottom crums?

## Yes — By Construction, With One Verification Gap

According to **[INV-WIDTH-VALUE-EQUIVALENCE]**, the V-width and I-width stored in a POOM bottom crum always encode the same logical magnitude. The tumbler representations differ (V-width uses 2 digits at exp=-1, I-width uses 6-9 digits at exp=-8 or similar), but extracting the numeric value via `tumblerintdiff` yields identical integers from both.

## How the Invariant is Established

**[ST-INSERT-VWIDTH-ENCODING]** defines the creation mechanism in `insertpm`:

1. Extract the integer value from I-width: `inc = tumblerintdiff(&lwidth, &zero)`
2. Compute V-address precision: `shift = tumblerlength(vsaptr) - 1`
3. Encode V-width at that precision: `tumblerincrement(&zero, shift, inc, &crumwidth.dsas[V])`
4. Copy I-width directly: `movetumbler(&lwidth, &crumwidth.dsas[I])`

This construction guarantees: `tumblerintdiff(crum.width.dsas[V], zero) == tumblerintdiff(crum.width.dsas[I], zero)`.

## Operations That Preserve The Invariant

**Creation paths** (all use `insertpm`):
- **[ST-INSERT]**: Text insertion — V-width encoded from I-width
- **[ST-VCOPY]**: Transclusion via `docopy` → `insertpm` — same encoding
- **[ST-CREATE-LINK]**: Link creation via `docopy` → `insertpm` — same encoding

**Non-modifying operations**:
- **[ST-DELETE]**: Removes crums entirely via `disown` + `subtreefree` — does not modify width fields of surviving crums
- **[ST-REARRANGE]**: Modifies displacement (`cdsp.dsas[V]`) only, not width — Finding 0056 confirms: `tumbleradd(&ptr->cdsp.dsas[index], &diff[i], &ptr->cdsp.dsas[index])`
- **[ST-REBALANCE-2D]**: Moves entire crums between nodes — does not modify internal fields

## Potential Divergence Scenario: Coalescing (Verification Gap)

**[ST-INSERT]** Finding 0062 describes rightward extension when `isanextensionnd` succeeds:

> "When the insertion point equals an existing crum's reach and homedoc matches: `post_insert_coalesce(crum, content) = crum.width' = crum.width + content.width`"

The knowledge base states the crum's width is extended **in place** but does not explicitly confirm that:
1. **Both** V-width and I-width dimensions are updated
2. The extension uses the same encoding mechanism as crum creation
3. The addition preserves the invariant relationship

This is a **verification gap**. The coalescing code path (at `insertnd.c:243`) is not detailed in the findings. If only the V-width is extended while the I-width remains unchanged, or if the addition is done at different precisions, the invariant would be violated.

## Edge Case: Zero-Address (Likely Impossible)

**[EC-VWIDTH-ZERO-ADDRESS]** identifies a hypothetical edge case:

If `vsaptr` (V-address) is zero:
- `shift = tumblerlength(0) - 1 = -1`
- V-width would have `exp = 1` (positive exponent, not negative)
- This creates qualitatively different structure

The original developer's comment `/*I'm suspissious of this shift <reg> 3/1/85 zzzz*/` suggests awareness of this concern. However, **[SS-POOM-BOTTOM-CRUM]** examples show V-addresses like `0.5`, `1.1` — always non-zero. Normal INSERT operations target non-zero V-positions, so this case may never arise in practice.

## Formal Answer

**Invariant holds**: `∀ crum ∈ bottom_crums(poom) :: tumblerintdiff(crum.width.dsas[V], zero) == tumblerintdiff(crum.width.dsas[I], zero)`

**Established by**: Explicit encoding during crum creation (all paths use `insertpm`'s V-width construction from I-width value)

**Preserved by**: Operations that don't create/modify crums (DELETE, REARRANGE, rebalancing)

**Verification gap**: Coalescing extension path — the knowledge base does not provide explicit evidence that width extension preserves the invariant

**Edge case**: Zero-address shift computation produces positive exponent, but likely impossible in practice given V-address conventions

**No evidence of actual divergence**: All documented operations either establish the invariant (creation) or don't touch width fields (modification/deletion). The coalescing gap is a documentation/verification issue, not confirmed misbehavior.

## Code Exploration

Let me present my findings while the file write is pending approval:

---

# Answer: V-width and I-width Divergence in POOM Bottom Crums

## Summary

**NO** — V-width and I-width do NOT always maintain equal logical magnitude. While they start with the same magnitude at creation, they use **different tumbler exponents** based on V-address insertion depth. Standard tumbler arithmetic does not preserve integer magnitude equality, causing them to diverge.

## Key Evidence from Source Code

### 1. Initial Creation [orglinks.c:115-117]

V-width is constructed from I-width using:
```c
shift = tumblerlength (vsaptr) - 1;
inc = tumblerintdiff (&lwidth, &zero);
tumblerincrement (&zero, shift, inc, &crumwidth.dsas[V]);
```

**Example:** Same I-width, different V-depth:
- Insert at V=`1.2`, I-width=`5` → V-width: `exp=-1, m[0]=5` (notation: `0.5`)
- Insert at V=`1.2.3`, I-width=`5` → V-width: `exp=-2, m[0]=5` (notation: `0.0.5`)

Both have I-width magnitude 5, but **different V-width exponents**.

**Developer's own suspicion** [orglinks.c:114]:
```c
/*I'm suspissious of this shift <reg> 3/1/85 zzzz*/
```

### 2. Extension Causes Divergence [insertnd.c:251]

When extending an existing crum:
```c
dspadd (&ptr->cwid, width, &ptr->cwid, (INT)father->cenftype);
```

This uses `tumbleradd` → `absadd` [tumble.c:460-478], which aligns by **exponent**, not magnitude.

**Concrete example of divergence:**

Adding two crums with same I-width (5) but different V-exponents:

**I-width addition:**
```
5 + 5 = 10
Result: exp=0, mantissa=[10,0,...]  
→ Magnitude: 10
```

**V-width addition:**
```
0.5 (exp=-1, m=[5,0,...]) + 0.0.5 (exp=-2, m=[5,0,...])

absadd chooses larger exp (-1):
  answer.exp = -1
  ansmant[0] = 5      (from first operand)
  ansmant[1] = 0 + 5  (shifted second operand)
  
Result: exp=-1, mantissa=[5,5,0,...]
→ Tumbler: 0.5.5 (multi-story, NOT magnitude 10)
```

**The widths have diverged**: I-width says 10, V-width is a multi-story tumbler.

### 3. Debugging Evidence [insertnd.c:114-122]

The system includes a `widdiffs()` function that compares only the **last digit** of V-width and I-width:

```c
static INT widdiffs(typecuc *crumptr) {
    i = lastdigitintumbler(&crumptr->cwid.dsas[I]);
    v = lastdigitintumbler(&crumptr->cwid.dsas[V]);
    return(i-v);
}
```

This suggests awareness that full magnitude might not match. Debug code checking this was **disabled** [line 80]:
```c
if(FALSE&&(fullcrumptr->cenftype==POOM)&&olddiff != newdiff){
```

## Why This Happens

1. **V-space is hierarchical** — addresses at different depths (1.1 vs 1.1.1)
2. **V-width exponent = insertion depth** — reflects tumbler structure
3. **I-space is flat** — all I-widths use exp=0 (simple integers)
4. **Tumbler addition preserves exponent relationships** — not integer sums

When crums from different V-depths are combined, incompatible exponents create multi-story V-widths that don't match integer I-widths.

## Operations That Cause Divergence

1. **Crum extension** — `dspadd` when V-widths have different exponents
2. **Width recalculation** — `setwispnd` combining children at mixed depths
3. **Any `lockadd` operation** on tumblers with mismatched exponents

## Implications

- **I-width is authoritative** for character count
- **V-width represents tumbler-space extent**, not character count
- **V-width cannot reliably compute I-width** after operations
- **This appears to be expected behavior** given disabled debug checks

## Code References

- `backend/orglinks.c:75-134` — V-width creation in `insertpm`
- `backend/insertnd.c:242-275` — Crum extension in `insertcbcnd`
- `backend/tumble.c:444-485` — Exponent handling in `absadd`
- `backend/insertnd.c:114-122` — Debug function `widdiffs`
- `backend/wisp.c:15-18, 269-273` — `dspadd` and `lockadd`
