# Consultation Answers — Two Space

**Inquiry:** What is the relationship between permanent content storage (I-space) and mutable document arrangement (V-space)? What invariants connect them?
**Date:** 2026-03-14 14:23
**Questions:** 18 (10 nelson, 8 gregory)

---

## Question 1 [nelson]

> Must every piece of content that has ever been stored remain retrievable even after it no longer appears in any document's current arrangement?

### Nelson's Answer

## Yes — with important nuance about mechanism and economics.

Nelson's design requires that content stored in I-space remains retrievable even after removal from every document's current V-space arrangement. This follows from three reinforcing commitments: append-only storage, historical backtrack, and link survivability.

---

### The Append-Only Architecture

The storage model is explicitly non-destructive:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

> "The true storage of text should be in a system that stores each change and fragment individually, assimilating each change as it arrives, but keeping the former changes." [LM 2/15]

Content enters I-space once and stays. No operation removes it. DELETE is a V-space operation only — it changes the current arrangement, not the permanent store.

### DELETE Does Not Destroy

Nelson is explicit about what deletion means. His technical diagram on page 4/9 labels a specific category:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

And further:

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

"Not currently addressable" means absent from the current V-stream — not absent from the system. The bytes are described as "awaiting historical backtrack functions," which presupposes they remain in storage for that purpose.

### Historical Backtrack Requires It

The version history guarantee is meaningless without I-space persistence:

> "The file management system we are talking about automatically keeps track of the changes and the pieces, so that when you ask for a given part of a given version at a given time, it comes to your screen." [LM 2/15]

If the system can reconstruct "a given part of a given version at a given time," the underlying bytes must still exist. You cannot reconstruct a historical state from content that has been destroyed.

### Link Survivability Requires It

Links attach to I-space addresses, not V-space positions:

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes. This has a crucial advantage: it means that links can survive editing." [LM 4/42]

If content vanished from I-space once removed from all current V-streams, links to that content would silently break — violating the survivability guarantee. The "strap between bytes" metaphor only works if the bytes persist.

### The Economic Tension

There is one significant caveat. Nelson's funding model requires ongoing storage rental:

> "ALL SERVICES MUST BE SELF-SUPPORTING. Subsidy between one aspect of the system and another could only work temporarily. This means, for example, that archival storage must be economically self-sustaining." [LM 4/5]

Nelson does **not** specify what happens when storage rental lapses. The curated storage-funding source explicitly notes this gap: Nelson does not address whether there is a grace period, whether the Author's Fund can preserve orphaned content, or how payment obligations interact with the permanence guarantee over centuries.

The technical architecture says "never destroy." The economic architecture says "someone must pay." Nelson leaves the collision unresolved.

### Summary

| Question | Answer | Basis |
|----------|--------|-------|
| Does the architecture permit destroying I-space content? | **No** — append-only by design | [LM 2/14] |
| Can deleted content be retrieved? | **Yes** — through historical backtrack | [LM 2/15, 4/9] |
| Do links to such content still resolve? | **Yes** — links point to I-space | [LM 4/42] |
| Is perpetual storage economically guaranteed? | **Unspecified** — requires ongoing payment | [LM 4/5] |

The design intent is unambiguous: I-space content persists regardless of its presence in any current V-space arrangement. Whether the economic model can sustain this guarantee indefinitely is a question Nelson acknowledged but did not resolve.

---

## Question 2 [nelson]

> Can the same stored content appear at multiple positions within a single document or across different documents simultaneously?

### Nelson's Answer

# Yes — This Is the Architectural Foundation

The same stored content can appear at multiple positions both within a single document and across different documents simultaneously. This capability is not a special feature but the fundamental consequence of Xanadu's two-address-space design.

## The I-Space / V-Space Separation

Content lives permanently in **I-space** (invariant space) at a single, immutable address. Documents are **V-space** (virtual space) arrangements — mappings that reference I-space content. Multiple V-space positions can point to the same I-space bytes.

> "The virtual byte stream of a document may include bytes from any other document." (4/10)

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." (4/11)

The content exists once in storage. What varies is how many places reference it.

## Across Documents: Transclusion

This is Nelson's primary use case — the "quote-window" or "inclusion":

> "Someone else may create a document which quotes it as much as desired. This mechanism we call the quote-window or quote-link. Through a 'window' in the new document we see a portion of the old." (2/32)

> "Document A can include Document B, even though Document B is owned by someone else." (2/35)

The layering is unlimited:

> "A document may have a window to another document, and that one to yet another, indefinitely. Thus A contains part of B, and so on. One document can be built upon another, and yet another document can be built upon that one, indefinitely: each having links to what was already in place." (2/35-2/36)

The COPY operation implements this at the protocol level. It creates a V-space mapping to existing I-space content — the bytes are not duplicated:

> "The material determined by \<spec set\> is copied to the document determined by \<doc id\> at the address determined by \<doc vsa\>." (4/67)

## Within a Single Document

Nothing in the architecture prevents the same I-space bytes from appearing at multiple V-space positions within one document. The V-stream is a mapping; mappings are not required to be injective (one-to-one). The COPY operation takes a target `<doc id>` that could be the source document itself.

## Across Versions

CREATENEWVERSION explicitly creates a new V-space arrangement over the same I-space content:

> "This creates a new document with the contents of document \<doc id\>. It returns the id of the new document." (4/66)

Every version of a document shares I-space content with its predecessors. This is how correspondence works — matching parts across versions are identified by their shared I-space origin.

## Discovery: FINDDOCSCONTAINING

The system provides a dedicated operation to find all documents sharing content:

> "FINDDOCSCONTAINING: This returns a list of all documents containing any portion of the material included by \<vspec set\>." (4/70)

This operation exists precisely because the same content routinely appears in multiple documents.

## Why This Matters

Nelson frames this as the solution to the distributed update problem and the copy-divergence problem:

> "No copying operations are required among the documents throughout the system, and thus we solve the problems of update — especially the problem of updating documents which depend on other documents. We solve this problem simply by windowing to a changing document." (2/36)

And crucially, shared I-space origin is what makes content **live** rather than **dead**:

> "Remember the analogy between text and water. Water flows freely, ice does not. The free-flowing, live documents on the network are subject to constant new use and linkage, and those new links continually become interactively available. Any detached copy someone keeps is frozen and dead, lacking access to the new linkage." (2/48)

Content identity is structural, not value-based: "Two documents with identical text created independently have DIFFERENT I-addresses. Transcluded content SHARES the same I-address." This distinction is how the system knows the difference between coincidental similarity and actual quotation.

---

## Question 3 [nelson]

> When a document's arrangement changes, does the underlying stored content remain byte-identical and at its original permanent address?

### Nelson's Answer

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

---

## Question 4 [nelson]

> Does every unit of content have a stable identity that is independent of which document currently includes it or where it appears?

### Nelson's Answer

# Yes — Absolutely and By Design

This is one of the most clearly specified properties of Xanadu. Every unit of content has a **permanent I-space address** that is independent of which document includes it, where it appears within any document, and whether it currently appears in any document at all.

## The Two Address Spaces

Xanadu separates content identity from content arrangement through two distinct address spaces:

**I-Space (Invariant Space)** — where content permanently lives. Addresses are absolute and immutable. Content at an I-space address never changes.

**V-Space (Virtual Space)** — the document's current arrangement of content. A view that references I-space content. Can be rearranged across versions.

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." [LM 4/11]

The V-address (position in the current view) changes freely. The I-address (permanent identity) never does.

## I-Space Address Structure

Every byte gets a permanent tumbler address encoding its origin:

```
Node.0.User.0.Document.0.Element
```

> "There are four major fields, each expandable indefinitely, with three major dividers between them. These fields are Server, User, Document and Contents." [LM 4/26]

This address is assigned at creation and is **permanent**. It encodes which server, which account, which document originally created that byte.

## Identity Is Based on Creation, Not Value

Two documents with identical text created independently have **different** I-addresses. Transcluded content **shares** the same I-address. This is how the system distinguishes "wrote the same words" from "quoted from the original."

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

When content is transcluded into another document, it appears in that document's V-space but retains its original I-space identity. The content doesn't move or get copied — it is *referenced*.

## Independence from Document Inclusion

Content identity survives regardless of how many documents include it or whether any currently do:

1. **Deletion doesn't destroy identity.** DELETE removes content from V-space only. The I-space content remains forever.

   > "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

2. **Transclusion preserves identity.** When document A includes content from document B, the included bytes retain their I-addresses from B.

   > "The virtual byte stream of a document may include bytes from any other document." [LM 4/10]

3. **Origin is always traceable.** No matter where content appears, you can determine where it came from.

   > "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

## Independence from Position

V-space positions shift with every edit. I-space addresses do not:

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." [LM 4/30]

This is why links survive editing — they point to I-space identity, not V-space position.

## The Append-Only Foundation

The underlying storage model guarantees this stability:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

Content is appended, never overwritten. Every byte ever created has an eternal address. The permascroll (Nelson's term: "append-only storage system" or "hyperfile") is the physical manifestation of I-space.

## Summary

Every unit of content in Xanadu has a stable identity (its I-space address) that is:

- **Independent of which document includes it** — transclusion references the original identity
- **Independent of where it appears** — V-space position changes; I-space address does not
- **Independent of whether it currently appears anywhere** — deleted content retains its I-address
- **Permanent** — assigned at creation, never reassigned or invalidated
- **Structural** — encoded in the address itself, not metadata that can be stripped

This separation of identity from arrangement is the architectural foundation that makes permanent links, automatic attribution, version comparison, and the entire Xanadu model possible.

---

## Question 5 [nelson]

> Must the system distinguish between "content as originally written" and "content as currently arranged for reading" as fundamentally separate concerns?

### Nelson's Answer

# Yes. This separation is the architectural foundation of everything.

The distinction between content-as-written (I-space) and content-as-arranged (V-space) is not a feature of Xanadu — it is the *premise* on which all other features stand. Without it, you cannot have permanent addresses, survivable links, non-destructive editing, version history, transclusion, or automatic attribution. Every guarantee I made depends on this separation.

## The Two Spaces

**I-Space (Invariant Space)** is where content permanently lives. Every byte ever created gets a permanent address here. Content at an I-space address never changes.

**V-Space (Virtual Space)** is the document's current arrangement — a view that references I-space content. V-space can be rearranged across versions. It is ephemeral; editing changes V-addresses constantly.

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." [LM 4/11]

The document IS the mapping from V-addresses to I-addresses. Each version defines a different mapping. Edits change the mapping, not the I-space content.

## Why This Must Be So

### 1. Links survive editing because they point to I-space

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes. This has a crucial advantage: it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them." [LM 4/42]

When you insert content, V-space positions shift — but I-space addresses remain stable. Links point to I-space. Therefore links are unaffected by insertion. The link doesn't care where the bytes appear in V-space. It only cares that the bytes it references still exist in I-space.

If you collapsed I-space and V-space into one, every edit would break every link. The entire web of literature would shatter with each keystroke.

### 2. Deletion is non-destructive because it only affects V-space

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

DELETE removes content from V-space (the current arrangement) but does NOT remove it from I-space (permanent storage). Previous versions still contain the deleted content. Other documents that transclude it still show it. Links to it still resolve.

Without the separation, "delete" would mean "destroy" — and with destruction, you lose history, break transclusions, and sever links.

### 3. Version history is structural, not backup

> "Virtually all of computerdom is built around the destructive replacement of successive whole copies of each current version." [LM 2/14]

> "A document is really an evolving ONGOING BRAID." [LM 2/14]

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

Each version is a different V-space arrangement over the same I-space content. Version history emerges naturally from the separation — it is not a bolted-on feature but the inevitable consequence of treating content and arrangement as distinct.

### 4. Correspondence (version comparison) derives from shared I-space origin

> "Of course, a facility that holds multiple versions of the same material, and allows historical backtrack, is not terribly useful unless it can help you intercompare them in detail — unless it can show you, word for word, what parts of two versions are the same." [LM 2/20]

When two V-space positions in different versions map to the same I-space address, those positions *correspond*. The system can show you what is the same and what differs between any two versions — automatically, structurally, without metadata or diff algorithms — because the shared I-space origin IS the correspondence.

### 5. Transclusion works because V-space references I-space across documents

> "The virtual byte stream of a document may include bytes from any other document." [LM 4/10]

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

When you transclude, your V-space includes a reference to someone else's I-space content. The content exists once, permanently, at its I-space address. Your document merely points to it. Attribution is automatic because the I-address encodes which document created those bytes.

### 6. Origin traceability is encoded in the address itself

Every I-space address has the form `Node.0.User.0.Document.0.Element` — the Document field directly encodes which document originally created that byte.

> "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

This is not metadata that can be stripped. It is the address itself. To fetch content, the system must request it from its home location. The connection cannot be severed because the fetching mechanism requires it.

## The Analogy

Think of a library:

```
I-Space (Library Stacks)           V-Space (Reading Lists)
┌─────────────────────┐            ┌─────────────────────┐
│ Shelf A: "hello"    │            │ My Essay v1:        │
│ Shelf B: " world"   │   ──►     │   [ref A, ref B]    │  → "hello world"
│ Shelf C: "!"        │           │                     │
│                     │            │ My Essay v2:        │
│ (never changes)     │   ──►     │   [ref A, ref C]    │  → "hello!"
└─────────────────────┘            └─────────────────────┘
```

The library stacks (I-space) never change. Reading lists (V-space) can be rearranged, versioned, shared, and compared — because they are *about* the stacks, not the stacks themselves.

## The Consequence of Collapsing Them

If you merge "content as written" with "content as arranged," you get conventional file systems: saving overwrites. Editing destroys. Links break. History requires full copies. Attribution requires trust in metadata. Transclusion becomes copying. And copying, as I said:

> "Note also that he or she who makes a paper copy or disk is losing all dynamic link connections, and is left with the inert, non-interactive copy. And that will be a considerable deprivation in the world we are talking about." [LM 2/48]

A dead copy. Frozen. Severed from the living literature.

## Summary

The separation of I-space from V-space is not one feature among many. It is the single architectural decision from which permanence, link survivability, non-destructive editing, version history, correspondence, transclusion, and origin traceability all follow. Remove this distinction and every guarantee collapses simultaneously.

The answer is not merely "yes, the system must distinguish them" — it is that the distinction between content-as-created and content-as-arranged IS the system.

---

## Question 6 [nelson]

> If two documents share the same content by reference rather than by copying, must a reader be able to discover that the content is shared?

### Nelson's Answer

## Yes — discovery of shared content is a structural guarantee

Nelson makes this clear at multiple levels: structural, operational, and as an explicit user-facing promise.

### The structural basis: I-space identity

When content is shared by reference (transclusion), both documents' V-space arrangements point to the **same I-space addresses**. This is not metadata — it is the mechanism itself. The system knows content is shared because the addresses are identical.

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

Content identity is based on creation, not value. Independently created identical text gets different I-addresses; transcluded content shares the same I-address. The sharing relationship is therefore always computable from the addresses alone.

### The explicit user promise

Nelson states this as a guarantee:

> "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

And for windowed (transcluded) content specifically, he requires **two-way** discoverability:

> "As already stated, it is possible for the reader to ask to see the materials which are windowed to by a given document. However, it must also be possible for the reader to ask to see whatever documents window to the current document. Both are available at any time." [LM 2/37]

### The operational mechanism

The FEBE protocol includes a dedicated operation for exactly this:

> **FINDDOCSCONTAINING**: "This returns a list of all documents containing any portion of the material included by \<vspec set\>." [LM 4/70]

This means: given any content, you can ask the system "what other documents contain this same material?" and get a complete answer.

### A nuance: automatic display vs. queryable discovery

There is one important distinction Nelson draws. A **quote-link** (explicit quotation) is visually indicated to the reader. But a plain **inclusion** may not be automatically shown:

> "Note that a quote-link is not the same as an inclusion, which is not ordinarily indicated." [LM 4/53]

So the system distinguishes between:

| Mechanism | Automatically visible? | Discoverable on request? |
|-----------|----------------------|--------------------------|
| **Quote-link** (explicit quotation) | Yes | Yes |
| **Inclusion** (plain transclusion) | Not necessarily | Yes — always |

Even for plain inclusions, the reader **can always discover** the sharing. The front end may not highlight it by default, but the structural information is always present and the FINDDOCSCONTAINING operation always works.

### Summary

The answer is unambiguous: **yes, a reader must be able to discover that content is shared.** This is:

1. **Structural** — shared I-space addresses make the relationship computable
2. **Operational** — FINDDOCSCONTAINING is a core protocol command
3. **Guaranteed** — "you can at once ascertain the home document of any specific word or character"

The only question is whether the front end *automatically shows* the sharing or requires the reader to ask. For quote-links, it is shown. For plain inclusions, the reader may need to query — but the system must always answer truthfully.

---

## Question 7 [nelson]

> Is the mapping from a document's visible arrangement to the underlying stored content always recoverable — can the system always trace displayed content back to its permanent origin?

### Nelson's Answer

# Yes — Traceability from V-Space to I-Space Is Always Recoverable

This is one of the most fundamental architectural guarantees in Xanadu. The system is designed so that every byte visible in a document's current arrangement can always be traced back to its permanent origin. This is not an optional feature but a structural property of the addressing system itself.

## The Architectural Basis

Xanadu maintains two address spaces:

- **I-Space (Invariant Space)** — where content permanently lives. Addresses are absolute and immutable. Content at an I-space address never changes.
- **V-Space (Virtual Space)** — the document's current arrangement. A view that references I-space content. Can be rearranged across versions.

The document IS the mapping from V-addresses to I-addresses. Every version defines a different mapping. The system always holds this mapping — it is the core data structure.

> "Logical addressing of the byte stream is in the form of virtual spans, or vspans. These are sequences of bytes in the document's virtual byte stream, regardless of their native origin." [LM 4/11]

The phrase "regardless of their native origin" is key — V-space presents a seamless stream, but the system always knows where each byte actually came from.

## The I-Address Encodes Origin

Every byte's I-address is a tumbler of the form `Node.0.User.0.Document.0.Element`. The Document field directly encodes which document originally created that byte. This is not metadata attached to content — it IS the address:

> "There are four major fields, each expandable indefinitely, with three major dividers between them. These fields are Server, User, Document and Contents." [LM 4/26]

To fetch content, the system must request it from its home location:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

The retrieval mechanism itself requires knowing the origin. You cannot fetch a byte without knowing its I-address, and the I-address tells you where it came from.

## Transclusions Preserve Identity

When content is included from another document (transclusion), it retains its original I-address. The COPY operation creates a new V-space mapping to existing I-space content — it does not create new content:

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

> "The virtual byte stream of a document may include bytes from any other document." [LM 4/10]

The included bytes look the same to the user but remain traceable to their home document. Two documents with identical text created independently have DIFFERENT I-addresses. Transcluded content SHARES the same I-address. This is how the system distinguishes "wrote the same words" from "quoted from the original."

## Nelson's Explicit Guarantee

Nelson states this as a user-facing promise:

> "This world nevertheless remains simple in design. The virtuality is simple in structure and regular in layout. You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

This guarantee holds even through arbitrarily deep windowing:

> "Think of the present document as a sheet of glass. It may have writing painted on it by the present author; it may have clear glass, windowing to something else; the next pane may be in turn made of more layers of painted glass, with more windows, and so on indefinitely." [LM 2/34]

No matter how many layers deep, the I-address at the bottom traces to the original creator.

## Even "Deleted" Content Remains Traceable

The V→I mapping is recoverable even for content removed from the current view:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

DELETE removes the V-space mapping but not the I-space content. Previous versions still hold the mapping. The bytes remain at their permanent I-addresses.

## The Enfilade Implementation

The POOM enfilade maintains the V→I mapping operationally:

```
User requests V-space position 5
        │
        ▼
   POOM enfilade (V→I mapping)
        │
        ▼
   "Position 5 = I-space address X"
        │
        ▼
   GRAN enfilade (content storage)
        │
        ▼
   Returns actual bytes from X
```

Nelson describes the enfilade as keeping the system in "canonical operating condition" through all changes:

> "All changes, once made, left the file remaining in canonical order, which was an internal mandate of the system." [LM 1/34]

## The V-Address Is Ephemeral; the I-Address Is Eternal

Nelson is explicit that V-addresses shift during editing — but this does not affect traceability:

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." [LM 4/11]

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." [LM 4/30]

The V-address tells you where content appears now. The I-address tells you where it came from forever. The system always holds the mapping between them.

## Summary

The mapping from displayed content to permanent origin is not merely recoverable — it is the fundamental data structure of the system. A Xanadu document IS a V→I mapping. The enfilades maintain it. The tumbler addresses encode it. The retrieval mechanism requires it. Attribution is structural, not metadata. It cannot be severed by any operation within the system.

---

## Question 8 [nelson]

> Must the permanent content layer be append-only, or can stored content ever be modified in place after initial storage?

### Nelson's Answer

## The Permanent Content Layer Must Be Append-Only

Content in I-space **cannot be modified in place after initial storage**. This is not a preference but a structural requirement — the entire architecture depends on it.

### Nelson's Explicit Statement

Nelson proposes append-only storage as the foundation:

> "Virtually all of computerdom is built around the destructive replacement of successive whole copies of each current version." [LM 2/14]

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

He elaborates on what "true storage" must be:

> "The true storage of text should be in a system that stores each change and fragment individually, assimilating each change as it arrives, but keeping the former changes." [LM 2/15]

### Why Modification Is Structurally Impossible

Six system guarantees depend on I-space immutability:

**1. Permanent addresses.** An I-space address always returns the same bytes. If content could be modified in place, the address would return different content at different times, violating the permanence guarantee.

**2. Link survivability.** Links attach to I-space byte spans. If those bytes could change, links would still "survive" but would connect to different content — silently corrupting every link in the docuverse that references the modified bytes.

> "Links between bytes can survive deletions, insertions and rearrangements, if anything is left at each end." [LM 4/43]

This guarantee means the bytes themselves must be stable, not just their addresses.

**3. Transclusion integrity.** When document A transcludes content from document B, readers see B's bytes. If B's owner could modify those bytes in place, A's meaning would change without A's owner's knowledge or consent. Nelson explicitly says:

> "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate — without damaging the originals." [LM 2/45]

Modification in place would damage every document that transcludes the modified content.

**4. Version history / historical backtrack.** The ability to reconstruct any previous state depends on the permanence of stored content:

> "The file management system we are talking about automatically keeps track of the changes and the pieces, so that when you ask for a given part of a given version at a given time, it comes to your screen." [LM 2/15]

If I-space content could be overwritten, previous versions could not be reconstructed.

**5. Correspondence.** Version comparison works because shared I-space addresses identify corresponding parts across versions. Modifying content in place would break this structural relationship.

**6. Origin traceability.** Attribution is guaranteed because I-addresses encode the home document:

> "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

This only holds if the bytes at an I-address are the same bytes that were originally stored there.

### The FEBE Protocol Confirms It

Of the 17 FEBE commands Nelson specifies, **none modifies existing I-space content**. The editing operations work exclusively on V-space arrangements:

- **INSERT** — adds new bytes to I-space; updates V-space mapping [LM 4/66]
- **DELETEVSPAN** — removes a span from V-space only; I-space unchanged [LM 4/66]
- **COPY** — creates V-space mapping to existing I-space (transclusion) [LM 4/67]
- **REARRANGE** — pure V-space operation [LM 4/67]
- **APPEND** — adds new bytes to I-space at document end [LM 4/67]

There is no MODIFY, UPDATE, or REPLACE operation. The absence is deliberate.

### DELETE Does Not Modify I-Space

Nelson is explicit that deletion is a V-space operation:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

"Deleted" bytes continue to exist at their I-space addresses. They are removed from the current V-space view, nothing more.

### Summary

The permanent content layer is unconditionally append-only. Nelson designed the entire system around the rejection of "destructive replacement" [LM 2/14]. Every guarantee — permanence, attribution, link survivability, transclusion integrity, version history, and correspondence — depends on the invariant that **once a byte is stored at an I-space address, it is that byte forever**.

---

## Question 9 [nelson]

> When content is included in a document by reference, does the document's arrangement record the precise extent of content referenced, or only a pointer to a larger stored unit?

### Nelson's Answer

## The Document Records Precise Extent

The arrangement records the **precise extent** — specific I-space spans — not a pointer to a larger stored unit.

### Evidence from the COPY Operation

The COPY command (which IS the transclusion mechanism) takes a `<spec set>` — a set of spans specifying exactly which bytes to include:

> "The material determined by `<spec set>` is copied to the document determined by `<doc id>` at the address determined by `<doc vsa>`." [LM 4/67]

A spec set is a **span-set**: one or more tumbler pairs, each designating a precise range of I-space bytes. The COPY doesn't say "include document D" — it says "include bytes from I-address X to I-address Y."

### Evidence from V-Space Structure

The V-space arrangement is a mapping from V-positions to I-addresses, byte by byte:

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

> "Logical addressing of the byte stream is in the form of virtual spans, or vspans. These are sequences of bytes in the document's virtual byte stream, regardless of their native origin." [LM 4/11]

Non-native bytes occupy precise V-space positions. The system knows exactly which I-space bytes are mapped to which V-space positions — not "somewhere in document D" but "I-space addresses X through Y mapped to V-space positions A through B."

### Evidence from Span Semantics

Spans themselves are precise:

> "A span in the tumbler line, represented by two tumblers, refers to a subtree of the entire docuverse" [LM 4/24]

A span's content is "implicit in the choice of first and last point" [LM 4/25]. There is no ambiguity about what is included.

### The Enfilade Implementation

The POOM enfilade (V→I mapping) maintains precisely which I-space addresses correspond to which V-space positions. This is how the system reconstructs any version on demand — it knows exactly which bytes to fetch and in what order.

### Why This Matters

If inclusions pointed only to "document D" rather than to precise byte ranges within D, several guarantees would break:

- **Correspondence** couldn't work — SHOWRELATIONOF2VERSIONS returns "ordered pairs of spans" [LM 4/70], which requires knowing exactly which I-space bytes each version shares
- **Royalty splitting** couldn't be proportional — "the original owner and the modifier split the royalty in proportion to who wrote what, as determined automatically" [LM 2/45]
- **Part-pounce** couldn't work — the system materializes "a certain part of a certain version" [LM 2/15] by assembling precisely the right I-space bytes

The document's arrangement is a precise V→I mapping at byte granularity, not a collection of document-level pointers.

---

## Question 10 [nelson]

> Must the system guarantee that the permanent content layer and the document arrangement layer are never merged — that no operation on arrangements can corrupt or alter stored content?

### Nelson's Answer

# Yes — The Separation of I-Space and V-Space Is a Structural Invariant

Nelson's design requires that no operation on arrangements (V-space) can corrupt or alter stored content (I-space). This is not merely an implementation preference but a load-bearing architectural invariant on which multiple guarantees depend.

## Nelson States the Separation Explicitly

The clearest statement comes from the discussion of derivative documents:

> "The integrity of each document is maintained by keeping the two aspects separate: derivative documents are permanently defined (and stored) in terms of the originals and the changes." [LM 2/37]

"The two aspects" are content (I-space) and arrangement (V-space). Nelson says integrity *depends on* keeping them separate — not that separation is convenient, but that it is necessary for integrity.

## I-Space Is Append-Only by Design

Nelson rejects the conventional model of destructive replacement:

> "Virtually all of computerdom is built around the destructive replacement of successive whole copies of each current version." [LM 2/14]

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

Content enters I-space and never changes. The I-space guarantee from the curated concept file states: "Content at an I-space address never changes" and "Content is immutable — it never changes after creation."

## Every FEBE Operation Respects the Boundary

Examining all editing operations Nelson specifies:

| Operation | I-Space Effect | V-Space Effect |
|-----------|---------------|----------------|
| **INSERT** | Appends *new* bytes | Updates arrangement |
| **APPEND** | Appends *new* bytes at end | Extends V-stream |
| **DELETEVSPAN** | None | Removes span from current view |
| **REARRANGE** | None | Transposes regions |
| **COPY** | None | Creates V-space mapping to *existing* I-space |
| **CREATENEWVERSION** | None | New V-space arrangement over same I-space |

No operation modifies existing I-space content. INSERT and APPEND create *new* I-space entries; they never touch existing ones. DELETE, REARRANGE, and COPY are pure V-space operations. COPY is especially telling — it is transclusion, meaning it creates a V-space reference to someone else's I-space bytes without duplicating or altering them.

Nelson describes DELETE explicitly:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

Delete removes from V-space. I-space is untouched.

## The Invariant Is Load-Bearing

If any V-space operation could mutate I-space content, the following guarantees would collapse:

**Historical backtrack** — Nelson promises "when you ask for a given part of a given version at a given time, it comes to your screen" [LM 2/15]. Reconstructing past states requires that the I-space fragments from which those states are assembled remain unchanged.

**Link survivability** — Links point to I-space bytes. Nelson: "since the links are to the bytes themselves, any links to those bytes remain stably attached to them" [LM 4/30]. If I-space content could be mutated by arrangement operations, links would silently point to altered content.

**Transclusion integrity** — When document A transcludes content from document B, both reference the same I-space bytes. If B's owner could corrupt those bytes through an editing operation, A's content would be silently damaged — violating "without damaging the originals" [LM 2/45].

**Origin traceability** — "You always know where you are, and can at once ascertain the home document of any specific word or character" [LM 2/40]. This depends on I-addresses being permanently meaningful. Mutated content at a stable address would make the address a lie.

**Correspondence** — Version comparison works by finding shared I-space origins: "a facility that holds multiple versions is not terribly useful unless it can help you intercompare them in detail" [LM 2/20]. If I-space content changed, the correspondence relation would become unreliable.

## The Analogy Nelson Uses

Nelson's library analogy captures the invariant precisely:

```
I-Space (Library)              V-Space (Reading Lists)
┌─────────────────────┐        ┌─────────────────────┐
│ Shelf A: "hello"    │        │ My Essay v1:        │
│ Shelf B: " world"   │   ──►  │   [ref A, ref B]    │
│ Shelf C: "!"        │        │ My Essay v2:        │
│ (never changes)     │   ──►  │   [ref A, ref C]    │
└─────────────────────┘        └─────────────────────┘
```

The library stacks never change. Reading lists can be rearranged, extended, or abandoned — but no reading-list operation alters the books on the shelves.

## Conclusion

The system must guarantee that the permanent content layer and the document arrangement layer are never merged. Nelson states this directly ("integrity... maintained by keeping the two aspects separate" [LM 2/37]), designs every operation to respect it, and builds at least five user-facing guarantees on top of it. Violating this invariant would not break one feature — it would break the architectural foundation on which permanence, survivability, transclusion, traceability, and version comparison all rest.

---

## Question 11 [gregory]

> When two documents both hold V→I mappings to the same I-address range (via transclusion), does the system record which document originally created that content, or are all V→I references to shared I-addresses indistinguishable at the storage level?

### Gregory's Answer

## KB Synthesis

The system records provenance at two distinct levels, but with different precision.

## At the POOM level: provenance is recorded per-crum

Each POOM bottom crum has a `homedoc` field (the `sporgladdress`) that records which document the I-addresses originated from [SS-SPORGL]. The `isanextensionnd()` function checks this field — it only coalesces adjacent content when the `homedoc` matches [ST-INSERT, Finding 0046, EC-LINK-PARTIAL-SURVIVAL]. This means two documents that both transcluded from the same source will have crums that share I-addresses but carry the same `homedoc` origin [INV-IADDR-PROVENANCE].

**Concretely:** if document B inserts "hello" natively (I-addresses α₁–α₅, homedoc=B) and document C transcludes that content (same I-addresses α₁–α₅, homedoc=B), both POOMs carry the same provenance. The `homedoc` records the *original allocator* (B), not the transcluder (C). This is a key asymmetry: INSERT allocates fresh I-addresses under the target document's address space, so the allocating document IS the homedoc; COPY shares existing I-addresses, so the homedoc is inherited from the original.

## At the granfilade level: I-addresses are fully distinguishable by address structure

I-addresses are allocated per-document within element subspace 3 (for text): `account.0.document.0.3.N` [SS-ADDRESS-SPACE, Finding 0065]. The document component is encoded directly in the I-address tumbler. So by inspection of the I-address itself, you can determine which document allocated it.

## At the spanfilade level: DOCISPAN entries record document-to-I-address associations

The DOCISPAN index maps I-address ranges to document ISAs [SS-DOCISPAN]. Every INSERT and COPY creates entries, so the index reflects *which documents hold references* — but since DELETE never removes spanfilade entries [INV-SPANF-WRITE-ONLY], this is a historical superset, not a current-state answer [EC-STALE-SPANF-REFERENCE].

## Summary

| Level | What's recorded | Distinguishable? |
|-------|----------------|-----------------|
| I-address structure | Allocating document encoded in tumbler digits | Yes — by address inspection |
| POOM crum `homedoc` | Original allocating document | Yes — per-crum field |
| Spanfilade DOCISPAN | All documents that have ever referenced the I-address | Yes, but stale after DELETE |

Two different documents' V→I references to the same shared I-address range are **distinguishable** — each POOM crum carries a `homedoc` field pointing to the original creator, and the I-address itself encodes the origin document [INV-IADDR-PROVENANCE]. What the system cannot tell you is which documents *currently* hold live references (POOM mappings) vs. which ones *ever did* (spanfilade) — that distinction requires cross-referencing both layers [INT-DELETE-SPANF-DIVERGENCE].

---

## Code Exploration

I have now read all the relevant source files directly. Here is my full answer.

---

## V→I Mapping Provenance in udanax-green

**Short answer:** The system stores V→I mappings per-document, so two documents transcluding the same I-address range produce *distinguishable* spanfilade entries — each tagged with the transcluding document's ISA. However, there is **no flag or field distinguishing "content creator" from "content transcluder"** at the spanfilade level. The original creator is recorded elsewhere (granfilade hints), not in the V→I mapping itself.

---

### The spanfilade: one global 2D index

There is a single global spanfilade (`spanf`). Every V→I mapping from every document is stored there. It is a 2D enfilade:

- **Axis 1 (`ORGLRANGE`):** document ISA, prefixed with `DOCISPAN = 4` [`xanadu.h:39`]. This identifies *which document* holds this V→I mapping.
- **Axis 2 (`SPANRANGE`):** I-address range (the invariant content address).

Every leaf node is a `type2dcbc` (2D core bottom crum) [`enf.h:108-131`]:

```c
struct struct2dcbc {
    ...
    typedsp  cdsp;
    typewid  cwid;
    type2dbottomcruminfo c2dinfo;   /* [enf.h:129] */
};
```

And `type2dbottomcruminfo` is defined in `wisp.h:106-109`:

```c
typedef struct struct2dbottomcruminfo {
    tumbler homedoc;
} type2dbottomcruminfo;
```

So each leaf carries exactly one extra tumbler: `homedoc`. This stores the ISA of the document that performed the `docopy()` call.

---

### How `homedoc` is populated: `insertspanf`

`insertspanf` [`spanf1.c:15-54`] is the write path for all V→I registrations. For each item in the sporglset it sets `linfo.homedoc` and calls `insertnd`:

```c
if (itemid == ISPANID) {
    movetumbler(&((typeispan*)sporglset)->stream, &lstream);
    movetumbler(&((typeispan*)sporglset)->width,  &lwidth);
    movetumbler(isaptr, &linfo.homedoc);            /* [spanf1.c:29] — transcluding doc */
} else if (itemid == SPORGLID) {
    movetumbler(&((typesporgl*)sporglset)->sporglorigin,  &lstream);
    movetumbler(&((typesporgl*)sporglset)->sporglwidth,   &lwidth);
    movetumbler(&((typesporgl*)sporglset)->sporgladdress, &linfo.homedoc); /* [spanf1.c:33] */
} else if (itemid == TEXTID) {
    ...
    movetumbler(isaptr, &linfo.homedoc);            /* [spanf1.c:42] */
}
insertnd(taskptr, (typecuc*)spanfptr, &crumorigin, &crumwidth, &linfo, SPANRANGE);
```

`isaptr` is the **calling document's ISA** — the document doing the transcluding. When two documents A and B both `docopy()` the same I-range, `insertspanf` is called twice (once per `docopy`), and each call inserts a separate spanfilade node with its own `homedoc` value.

**The two V→I references are therefore distinguishable by `homedoc`.**

---

### `doinsert` vs `docopy`: same storage, different granfilade

`doinsert` [`do1.c:87-123`] first creates new I-space content in the granfilade, then immediately transclubes it into the originating document via `docopy`:

```c
makehint(DOCUMENT, ATOM, TEXTATOM, docisaptr, &hint);  /* [do1.c:117] */
inserttextingranf(taskptr, granf, &hint, textset, &ispanset);
docopy(taskptr, docisaptr, vsaptr, ispanset);           /* [do1.c:119] */
```

`docopy` [`do1.c:45-65`] is the shared V→I registration path:

```c
specset2ispanset(taskptr, specset, &ispanset, NOBERTREQUIRED);
findorgl(taskptr, granf, docisaptr, &docorgl, WRITEBERT);
insertpm(taskptr, docisaptr, docorgl, vsaptr, ispanset);  /* [do1.c:60] */
insertspanf(taskptr, spanf, docisaptr, ispanset, DOCISPAN); /* [do1.c:62] */
```

The `ispanset` items passed into `insertspanf` have `ISPANID` type — bare I-spans with no embedded owner field. In that branch, `homedoc` is always set to `isaptr` (the calling document) [`spanf1.c:29`].

**Conclusion on doinsert vs docopy:** The spanfilade entry produced by the creator document (via `doinsert → docopy`) is structurally identical to the entry produced by any other document that later calls `docopy` on the same I-range. Both receive `homedoc = their own ISA`. The spanfilade cannot tell you which document was first.

The original creator *is* recorded — but in the **granfilade** via the `hint` (`TEXTATOM`, document ISA) stored in `inserttextingranf`. That is a separate lookup path from the V→I mapping.

---

### `finddocscontaining`: all transclusions are returned as equals

The FEBE command `FINDDOCSCONTAINING` [`fns.c:20-29`] calls:
```
finddocscontaining → dofinddocscontaining [do1.c:15] → finddocscontainingsp [spanf1.c:151]
```

In `finddocscontainingsp` [`spanf1.c:151-188`], the spanfilade is queried for all `ORGLRANGE` entries that overlap the requested I-span:

```c
tumblerincrement(&docspace.stream, 0, DOCISPAN, &docspace.stream);  /* [spanf1.c:168] */
tumblerincrement(&docspace.width, 0, 1, &docspace.width);
context = retrieverestricted((typecuc*)spanf, &docspace, ORGLRANGE, ispanset, SPANRANGE, (typeisa*)NULL);
for (c = context; c; c = c->nextcontext) {
    movetumbler(&c->totaloffset.dsas[ORGLRANGE], &docid);
    beheadtumbler(&docid, &document.address);       /* [spanf1.c:174] strip prefix → doc ISA */
    ...
}
```

This returns every document whose `ORGLRANGE` axis falls in the `DOCISPAN` band and whose `SPANRANGE` overlaps the query I-span. The content creator and every transcluder appear here identically. There is no "created by" bit in the result.

---

### The `homedoc` filter exists but is dead code at the call site

`crumqualifies2d` [`retrie.c:270-280`] contains a filter:

```c
if ((crumptr->height == 0) && infoptr
&& !tumblereq(&infoptr->homedoc, &(((type2dcbc*)crumptr)->c2dinfo.homedoc))) {
    return (FALSE);
}
```

This would allow retrieval restricted to a specific document's homedoc. But `findcbcinarea2d` — the only caller — unconditionally errors if `infoptr` is non-NULL:

```c
#ifndef DISTRIBUTION
if(infoptr){
    fprintf(stderr,"not NULL infoptr versions mumble specialcase 11/27/84 ...");
    gerror("findcbcinarea2d");
}
#else
    if (infoptr) gerror("!NULL");   /* [retrie.c:249-250] */
#endif
```

The comment "shouldnt happen till we try something fancier" [`retrie.c:245-246`] confirms this was planned but never activated. The filter is unreachable in any shipped build.

---

### Summary

| Question | Answer | Evidence |
|---|---|---|
| Are two transclusions of the same I-range distinguishable? | **Yes** — by `homedoc` in each spanfilade leaf | `wisp.h:108`, `spanf1.c:29`, `enf.h:129` |
| Does `homedoc` identify the original content creator? | **No** — it identifies the document that called `docopy()` | `spanf1.c:29,42` (always set to `isaptr` = caller) |
| Where is the original creator recorded? | In the **granfilade** via `makehint(TEXTATOM, docisaptr)` | `do1.c:117`, `inserttextingranf` |
| Does `finddocscontaining` distinguish creator from transcluder? | **No** — all are returned as equal document ISAs | `spanf1.c:168-179` |
| Is the `homedoc` retrieval filter active? | **No** — `findcbcinarea2d` crashes if `infoptr != NULL` | `retrie.c:244-251` |

**Bottom line:** The spanfilade records one node per `(document, I-range)` pair. Two documents mapping to the same I-range produce two separate, homedoc-distinguished nodes. But both nodes look identical in type — neither is marked as "original creator." Creation provenance lives in the granfilade hint, not in the V→I mapping. At the spanfilade storage level, all V→I references to a shared I-address range are structurally indistinguishable from one another.

---

## Question 12 [gregory]

> I-addresses encode a document-level prefix (e.g., `1.1.0.1.0.1.0.1.x`) — does the system ever use this prefix to look up the originating document for a piece of content, or is the hierarchy purely a namespace partitioning convention with no runtime semantic role?

### Gregory's Answer

## KB Synthesis

The prefix has active runtime semantic roles — it is not purely a namespace convention — but those roles are confined to allocation time. At retrieval time, a separate index handles document attribution.

## Allocation-time use (active runtime semantics)

During INSERT and MAKELINK, the document ISA is used to compute an upper bound that scopes the `findpreviousisagr` tree search:

- For text: `tumblerincrement(&hintptr->hintisa, 2, atomtype + 1, &upperbound)` bounds the search to the document's content subspace [SS-ADDRESS-SPACE Finding 0065, SS-ADDRESS-ALLOC Finding 0065]
- For links: `upperbound = docISA.2.3` bounds search to the document's link subspace [SS-ADDRESS-ALLOC Finding 0065]
- For documents/versions: `upperbound = tumblerincrement(hintisa, depth-1, 1)` bounds to the parent's child range [SS-ADDRESS-ALLOC Finding 0021]

After finding the candidate address, `tumblertruncate` + `tumblereq` explicitly verify the found address is actually contained under the target parent — this check was added to fix Bug 0013, which showed cross-account allocation when the containment check was missing [PRE-ADDRESS-ALLOC, SS-TUMBLER-CONTAINMENT].

So the document prefix is semantically load-bearing during allocation: the system *derives which I-address range to search* from the document ISA.

## Retrieval-time: prefix NOT parsed

When you have an I-address and need to know which document it came from, the system does **not** parse the prefix. Instead, it uses two separately maintained data structures:

1. **DOCISPAN index** (spanfilade type 4): `insertspanf(..., DOCISPAN)` explicitly records the I-address → document mapping at insert time. `find_documents` queries this index [SS-DOCISPAN, Finding 0036, 0047].

2. **Sporgl `sporgladdress` field**: explicitly stores the source document ISA in the sporgl struct, not derived from the I-address [SS-SPORGL Finding 0013].

3. **POOM crum `homedoc` field**: `isanextensionnd()` reads an explicit `homedoc` stored in the crum, not inferred from the I-address [INV-IADDR-PROVENANCE Finding 0046].

## Summary

| Use | Prefix hierarchy used? | Mechanism |
|-----|----------------------|-----------|
| Allocating next I-address | **Yes** — bounds the search range | `tumblerincrement` on document ISA |
| Verifying allocation stays in-bounds | **Yes** — containment check | `tumblertruncate` + `tumblereq` |
| Looking up originating document | **No** | DOCISPAN index (spanfilade) |
| Provenance in POOM crums | **No** | Explicit `homedoc` field |
| Provenance in sporgls | **No** | Explicit `sporgladdress` field |

The hierarchy is a genuine structural invariant with runtime enforcement during allocation, but once an I-address is allocated, its document of origin is tracked through separately maintained indices rather than by parsing the address itself.

---

## Code Exploration

I now have everything needed for a complete answer. Here it is:

---

## I-Address Prefix: Runtime Semantic Role in udanax-green

**Short answer: The I-address document prefix is not a passive namespace partition. It is the primary lookup key into the granfilade, drives BERT access control, and constrains content allocation — but it does NOT walk the prefix hierarchy at retrieval time to identify "the originating document." That identity must be supplied by the caller.**

---

### 1. The Granfilade Is Indexed by I-Address — Document Lookup via Prefix

The global `granf` structure is a 1D enfilade indexed on the WIDTH dimension using I-addresses as keys. Every document in the system has a leaf node in this tree at its exact I-address, holding its orgl (permutation matrix).

The path is:

`findorgl()` [`granf1.c:17`] → `fetchorglgr()` [`granf2.c:22`] → `retrievecrums()` [`retrie.c:15`] → `findcbcseqcrum()` [`retrie.c:167`]

`findcbcseqcrum` descends the granfilade tree by comparing `address` against each crum's WIDTH span, until it reaches the leaf whose totaloffset equals the requested I-address:

```c
// granf2.c:34-40
if ((context = retrievecrums ((typecuc*)fullcrumptr, address, WIDTH)) == NULL)
    return NULL;
if (!tumblereq((tumbler*)&context->totaloffset, address)) {
    crumcontextfree(context);
    return (NULL);  // exact match required
}
```

The I-address prefix thus directly encodes _where in the granfilade tree_ the document's orgl lives. A document at `1.1.0.1.0.1.0.1.x` is found by traversing the WIDTH dimension of the granfilade to that exact position. This is structural, not symbolic.

---

### 2. V↔I Translation Requires Fetching the Document's Orgl First

`specset2ispanset()` [`do2.c:14–46`] shows the critical runtime flow when a retrieve operation arrives with a V-spec (document ISA + V-span set):

```c
// do2.c:34-36
findorgl(taskptr, granf, &((typevspec *)specset)->docisa, &docorgl, type)
    && (ispansetptr = vspanset2ispanset(taskptr, docorgl, ...))
```

The document's I-address (`docisa`) is passed to `findorgl`, which traverses the granfilade to retrieve the orgl. That orgl is then passed to `permute()` [`orglinks.c:404`] to perform the V→I conversion via `span2spanset()`. Without the I-address lookup, there is no orgl, and the V→I mapping is impossible. The I-address prefix is the indirection handle for all document content operations.

---

### 3. BERT Access Control Uses the Exact I-Address

`findorgl()` first calls `checkforopen()` [`bert.c:52`] before touching the granfilade:

```c
// granf1.c:22
if ((temp = checkforopen(isaptr, type, user)) <= 0) { ... return FALSE; }
```

`checkforopen` computes `hashoftumbler(tp)` [`bert.c:234`] — a weighted sum of all mantissa digits and `exp` — and searches `berttable[hash]` for an exact `tumblereq()` match on the full I-address. The BERT table stores one entry per `(connection, documentid)` pair. Access is enforced at the exact I-address level; no prefix walking occurs here.

Account-level ownership is checked via `isthisusersdocument()`, which internally uses `tumbleraccounteq()` [`tumble.c:38`]. That function walks the mantissa comparing until the account tumbler terminates (two consecutive zeros), returning TRUE if the document I-address shares the account prefix at all non-zero positions. This is the one place where a prefix relationship is semantically used — to determine whether an unopened document is "owned" by the current user's account and can be read without an explicit open.

---

### 4. Address Allocation Validates Prefix Membership

`findisatoinsertnonmolecule()` [`granf2.c:203–241`] allocates new I-addresses for new documents/accounts. It:

1. Calls `findpreviousisagr()` to find the highest existing ISA below an upper bound
2. Verifies the found address is actually under `hintptr->hintisa` by truncating and comparing:

```c
// granf2.c:231-232
tumblertruncate(&lowerbound, hintlength, &truncated);
lowerbound_under_hint = tumblereq(&truncated, &hintptr->hintisa);
```

3. If the lowerbound is from a different prefix subtree, treats it as absent and generates the first child as `hintisa.0.1`

The prefix is thus a structural constraint on where new identities may be allocated — all content under a document must share that document's I-address prefix.

---

### 5. The `homedoc` Field and `crumqualifies2d` — Dead Code

`crumqualifies2d()` [`retrie.c:270–279`] contains a `homedoc` comparison that _looks_ like it would filter orgl crums by their originating document:

```c
if ((crumptr->height == 0) && infoptr &&
    !tumblereq(&infoptr->homedoc, &(((type2dcbc *)crumptr)->c2dinfo.homedoc))) {
    return (FALSE);
}
```

However, this is dead code. The only caller that could pass a non-NULL `infoptr` is `retrieverestricted()` [`retrie.c:56`], but `span2spanset()` calls it with `(typeisa*)NULL` at [`orglinks.c:435`]. More definitively, `findcbcinarea2d()` — which receives `infoptr` and passes it to `crumqualifies2d` — contains an explicit guard:

```c
// retrie.c:244-250
if(infoptr){
    fprintf(stderr,"not NULL infoptr versions mumble ... shouldent happen till we try something fancier\n");
    gerror("findcbcinarea2d");
}
```

Both DISTRIBUTION and non-DISTRIBUTION builds call `gerror()` if `infoptr` is non-null. The `homedoc` check was intended future functionality (the comment dates to `11/27/84`) but was never activated.

---

### Summary

| Mechanism | Role of I-address prefix | Active? |
|---|---|---|
| `fetchorglgr` / granfilade lookup | Primary index — prefix encodes tree position of document's orgl | **Yes** |
| `checkforopen` / BERT table | Exact I-address match for per-connection access control | **Yes** |
| `tumbleraccounteq` / ownership | Prefix comparison to determine if document is under user's account | **Yes** |
| `findisatoinsertnonmolecule` | Prefix validates that new ISAs stay within the parent hierarchy | **Yes** |
| `crumqualifies2d` / `homedoc` | Content-level document membership filtering at retrieval | **Dead — never activated** |

The hierarchy is not a pure namespace convention. The prefix is the granfilade's physical index structure, meaning a document at `1.1.0.1.0.1.0.1.x` is found by traversing the WIDTH dimension of the tree to that location. However, the system does **not** dynamically "walk the prefix" to discover which document owns a piece of content at retrieval time — that document identity must be supplied by the caller as an explicit `docisa` argument. The prefix tells you _where_ to look; it does not tell you _what_ to look for without being provided as a query parameter.

---

## Question 13 [gregory]

> Was permanent retention of all I-space content always the design intent, or was garbage collection of I-addresses unreferenced by any V-space mapping ever planned or prototyped?

### Gregory's Answer

## KB Synthesis

The KB is clear on what the implementation does, but only partially answers the question of *original intent*.

## What the implementation unambiguously shows

Permanent retention was built in from the start, not retrofitted:

**No GC infrastructure exists at any layer.** The granfilade allocation mechanism is query-and-increment with no free-list — `findpreviousisagr` finds the highest existing I-address and increments past it, never filling gaps [INV-NO-IADDR-REUSE]. There's nowhere to put a freed address even if you wanted to reclaim it.

**The spanfilade has no delete functions.** Inspection of `spanf1.c` and `spanf2.c` shows only insertion and query operations — no `deletespanf`, no removal path [INV-SPANF-WRITE-ONLY]. This isn't a stub or placeholder; the data structures weren't designed with deletion in mind.

**DELETE deliberately touches only the POOM.** `dodeletevspan` calls `deletevspanpm` → `deletend`, with no call to any granfilade or spanfilade removal function [FC-GRANF-ON-DELETE]. The result is permanent divergence: after delete, the spanfilade still indexes I-addresses that no V-space mapping references [INT-DELETE-SPANF-DIVERGENCE]. If GC had been planned, you'd expect at least a stub or commented-out call here.

**The grim reaper is RAM management only.** The cache eviction mechanism writes modified crums to disk and frees memory — it preserves content permanently, it doesn't reclaim it [SS-CACHE-MECHANISM].

## The design principle

[FC-GRANF-ON-DELETE] explicitly frames this as the Xanadu "bytes never die, addresses never change" principle. The combination of permanent I-addresses enabling transclusion identity [INV-IADDR-IMMUTABILITY], permanent spanfilade entries enabling provenance history [INV-IADDRESS-PERMANENT], and the fact that [INV-DELETE-NOT-INVERSE] is a *property* rather than a defect — all point to permanence being load-bearing, not accidental.

## What the KB cannot answer

Whether GC was ever *planned, prototyped, or debated* — the KB is derived from implementation behavior, not design discussions or source history. I built udanax-green; the permanence was intentional in what I shipped. But whether there were whiteboard sessions about GC, or commented-out experiments, isn't derivable from the findings here.

What I can tell you with confidence: nothing in the codebase was left behind as a GC stub. The disabled `levelpull` (tree height reduction, commented out at `genf.c:318-342`) [INV-ENFILADE-MINIMALITY] is the only major "designed but not implemented" feature the KB surfaces — and that's about tree structure optimization, not content reclamation. For I-space GC specifically, there's no trace of scaffolding.

---

## Code Exploration

I now have sufficient evidence to give a definitive answer. Let me compile it.

---

## Permanent Retention of I-Space Content: Design Intent vs. GC Plans

### Short Answer

Permanent retention appears to be the *operational reality*, but the code contains explicit evidence that **disk-level GC was planned and partially scaffolded — and then deliberately disabled or left incomplete**. No mechanism exists at any level to detect or reclaim I-space addresses orphaned by V-span deletion.

---

### Evidence Trail

#### 1. GC Was Explicitly Named as a Design Goal

`backend/coredisk.h:18-19` — the `typediskloafhedr` struct (used for every on-disk enfilade block) carries a `refcount` field whose comment reads:

```c
SINT refcount;      /* for subtree sharing, */
                /* disk garbage collecting */
```

This is not speculative. The field exists; the intent is annotated in the header. GC was part of the original design vocabulary.

---

#### 2. The "Grim Reaper" Is Explicitly NOT Garbage Collection

`backend/NOTES:39`:

```
credel.c  crum create&delete   memory collection (not gc, but data age stuff)
```

The authors drew this line themselves. `credel.c`'s `grimlyreap()` / `reap()` machinery is **age-based LRU eviction** of in-memory crums — it writes old crums to disk to free RAM. It is not referential GC. Crums are never freed because their I-space content is unreferenced; they are freed because they are old.

---

#### 3. Disk-Level GC Infrastructure Exists — and Is Disabled

`backend/corediskout.c` contains two GC functions:

- `deletefullcrumandgarbageddescendents()` [line 358]
- `deletewithgarbageddescendents()` [line 388]

These traverse on-disk crum tree nodes and decrement refcounts via `changerefcount()`. When a refcount would reach zero, a disk block is eligible for freeing.

But the punchline is at `corediskout.c:410`:

```c
/*subtreefree(ptr);*/ /*12/04/86*/
```

The actual reclamation call was **commented out on December 4, 1986**. The traversal runs; nothing gets freed. This is the skeleton of a GC system with the collection step removed.

---

#### 4. The Context in Which Disk GC Is Called: Not Deletion

These GC functions are called only from `orglwrite()` [corediskout.c:328-355], which runs when a **modified orgl is persisted to disk**. The trigger is a copy-on-write update to the crum tree (writing a changed tree to a new disk location and decrementing the refcount on the old location). It is structural GC of the tree encoding — not semantic GC of content.

It is **never called from `dodeletevspan`**.

---

#### 5. `dodeletevspan` Never Touches I-Space

The full call chain for V-span deletion:

```
dodeletevspan()         [do1.c:158]
  → deletevspanpm()     [orglinks.c:145]
    → deletend()        [edit.c:31]  — operates on the SPANFILADE only
        → disown()      [genf.c:349] — removes crum from tree, restructure only
        → subtreefree() [edit.c:60]  — frees the V-space crum node in memory
```

`deletend` [edit.c:31-76] cuts the span out of the spanfilade (V↔I mapping). The **granfilade** (I-space content store) is never touched. The I-addresses that backed the deleted V-span remain in the granfilade, intact, with no pointer back to indicate they are now unreferenced.

---

#### 6. No Reverse Index Exists to Enable I-Space GC

`orglinks.c` converts V-spans → I-spans (`vspanset2ispanset`) and I-spans → V-spans (`ispan2vspanset`). The `ispan2vspanset` direction uses `retrieverestricted()` in `retrie.c`, which scans the spanfilade for any V-span that maps to a given I range. This is a forward query tool — not a maintained reverse index. To GC an I-address range, you would need to confirm that *no* V-span references it, requiring a full spanfilade scan. No such scan is ever initiated anywhere in the delete path.

---

#### 7. `levelpull()` — Tree Compaction Disabled

`backend/genf.c:318-342`:

```c
int levelpull(typecuc *fullcrumptr)
{
/*  typecuc *ptr; */
return(0);
/*
    if (!isfullcrum (fullcrumptr))
        gerror ("Levelpull not called with fullcrum.");
    if (fullcrumptr->numberofsons > 1)
        return;
    if (fullcrumptr->height <= 1)
        return;
    ptr = (typecuc *) findleftson (fullcrumptr);
    dspadd (&fullcrumptr->cdsp, &ptr->cdsp, &fullcrumptr->cdsp, fullcrumptr->cenftype);
    disown (ptr);
    fullcrumptr->height--;
    transferloaf (ptr, fullcrumptr);
    setwispupwards (fullcrumptr,1);
    freecrum (ptr);
*/
}
```

This was meant to collapse single-child enfilade nodes (reduce tree height after deletions make internal nodes redundant). It is a complete stub. Tree height only grows; it never shrinks.

---

### Summary

| Question | Finding | Evidence |
|---|---|---|
| Was GC of I-space ever designed? | Planned, named, not implemented | `coredisk.h:18-19` |
| Is the "grim reaper" GC? | No — explicitly called "data age stuff, not gc" | `NOTES:39` |
| Does disk-level GC infrastructure exist? | Exists, but the free step was commented out (12/04/86) | `corediskout.c:410` |
| Does V-span deletion reclaim I-addresses? | Never. `dodeletevspan` → `deletend` never touches granfilade | `do1.c:158`, `edit.c:31-76` |
| Is there a reverse I→V index to enable GC? | No. `ispan2vspanset` is a query, not a maintained structure | `orglinks.c`, `retrie.c` |
| Is tree compaction after deletion implemented? | No. `levelpull()` is a stub returning 0 | `genf.c:318` |

**Conclusion:** I-space is append-only and permanently retained in udanax-green — not as a philosophical commitment baked into the architecture, but as an artifact of incomplete implementation. The design contemplated GC (the `refcount` field exists; the function names say "garbage"); the structural machinery was partially built; and then the actual reclamation was commented out with a date stamp (1986) and never reinstated. What remains is a system that accumulates I-space content forever because the mechanism to do otherwise was never finished.

---

## Question 14 [gregory]

> The storage layer is byte-opaque with one I-position per byte. Was there ever a design for variable-width content atoms (a character, a media element) that would each occupy a single I-position, or was byte-granularity always the intended resolution for the permascroll?

### Gregory's Answer

## KB Synthesis

Answering strictly from what I can derive from the implementation — the KB captures behavior, not design history, so I'll be clear about the limits.

**What the implementation does**

The permascroll is byte-granular at the I-address level, unconditionally [INV-SINGLE-CHAR-GRANULARITY], [SS-CONTENT-IDENTITY Finding 0034]:

- Each inserted byte receives exactly one I-address. `inserttextgr` allocates by calling `tumblerincrement(&lsa, 0, textset->length, &lsa)` — width equals byte count [ST-INSERT Finding 0031].
- V-space width equals byte count. `strlen()` gives the length field. A 4-byte UTF-8 emoji occupies 4 V-positions.
- The I-width stored in POOM bottom crums represents a byte count [SS-POOM-BOTTOM-CRUM Finding 0076].

**Storage atoms are variable-width, but addressing is not**

There is a distinction the KB makes visible: the physical storage unit `typegrantext` holds up to 950 bytes (`GRANTEXTLENGTH`) as a chunk [SS-CONTENT-IDENTITY Finding 0034]. A single INSERT call stores a block of up to 950 bytes in one gran atom. But this is an implementation convenience — the I-address range over that block is still byte-by-byte contiguous. The atom is the *allocation* unit; the byte is the *addressing* unit.

**What the KB cannot answer**

The design history question — whether variable-width character atoms (one I-position per glyph, media element, or semantic unit) were ever specified or prototyped — is not answerable from the KB. The KB extracts behavioral properties from code; it has no access to pre-implementation design documents, Nelson's original spec language, or any design decisions that were considered but not built.

What I can say: there is *no evidence in the code* of any variable-width atom design. No type tags, no multi-byte-character boundary logic, no encoding metadata. The system treats content as `seq<byte>` throughout, and the byte granularity appears structural rather than an oversight (it's what `strlen`, `movmem`, `GRANTEXTLENGTH` all reinforce). If a variable-width atom design existed, it left no trace in the implementation.

---

## Code Exploration

---

## Answer: Byte-Granularity, Atomic Links, and the Unresolved Design Seam

Reading the source directly, I find two coexisting models inside udanax-green that make this question sharper than a simple yes/no.

---

### What the code does now: TEXTATOM is byte-granular

`inserttextgr` in `granf2.c:83–109` is the definitive path for all text insertion. After writing each `textset` node into the granfilade, it advances the running I-address by the raw byte count of that chunk:

```c
// granf2.c:100
tumblerincrement (&lsa, 0, textset->length, &lsa);
```

The resulting I-span width is computed at `granf2.c:106` as the tumbler difference between `lsa` (final) and `spanorigin` (initial). The permascroll records one I-position per byte. There is no character-level or element-level re-encoding happening here; `textlength` is a plain `unsigned` count of raw bytes (`wisp.h:77`: `unsigned textlength`), and `movmem` copies that many bytes verbatim (`granf2.c:98`).

So for text: **one I-position = one byte, always.**

---

### But LINKATOM already embodies a different model

Links are created through `tumbler2spanset` (`do2.c:48–61`), which builds the I-span for a link atom:

```c
// do2.c:58
tumblerincrement (&spanptr->width, tumblerlength (tumblerptr)-1/*zzzzz*/, 1, &spanptr->width);
```

The `/*zzzzz*/` is a developer uncertainty marker — it appeared also at `do2.c:41` (`/*zzz ... */`) on a commented-out null assignment. Here it marks the width calculation as known-provisional: the width is `1` at mantissa position `tumblerlength(address)-1`, which is the finest-grained unit at that tumbler depth — effectively "one logical point" rather than one byte.

A LINKATOM's I-address is allocated in `findisatoinsertmolecule` (`granf2.c:158–181`). The function partitions the I-address space by atomtype using **mantissa[2]**:

```c
// granf2.c:162
tumblerincrement (&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound);
```

For TEXTATOM (`atomtype=1`), new text ISAs are allocated by incrementing the main counter (`mantissa[0]`) by 1 (`granf2.c:169`). For LINKATOM (`atomtype=2`), ISAs are allocated into a distinct sub-space via `mantissa[2]=2` (`granf2.c:171`):

```c
} else if (hintptr->atomtype == LINKATOM) {
    tumblerincrement (&hintptr->hintisa, 2, 2, isaptr);
```

A link gets one *address point*, not a byte sequence. It occupies a logical I-position measured at a finer tumbler mantissa level — not the same scale as bytes.

This is qualitatively different from text. A LINKATOM is the system's working model of "a content atom that is one logical unit regardless of how many bytes might back it."

---

### The ceiling: only two atom types, and it's load-bearing

`xanadu.h:144–146`:
```c
                      /* atom types - don't change these */
#define TEXTATOM  1
#define LINKATOM  2
```

The comment `/* atom types - don't change these */` is not decorative. The values 1 and 2 are arithmetic operands in `findisatoinsertmolecule` — they are added directly to tumbler mantissa positions to carve out address subspaces. Changing or adding values would corrupt existing address allocation.

The validation at `do2.c:94` enforces this:
```c
|| (hintptr->atomtype > 2)
```

No `atomtype=3` (say, an image atom or audio atom) is possible without extending both the address arithmetic and the hint validator.

---

### The `spanset2tumbler` commented-out function

Notably, `do2.c:63–76` contains a fully commented-out function:

```c
/*  bool
spanset2tumbler (taskptr, spanset, tmblptr)
...
{
    if (spanset->next || !iszerotumbler(&spanset->width))
        return (FALSE);
```

Its guard condition — returning FALSE if the span has nonzero width — treats an atom as valid only when its width **is zero**. This is the inverse of the byte-granular model: a zero-width atom is the expected case. The function was written, then abandoned. The `// SUSPECT //` annotation on line 74 (`movetumbler (&spanset->stream, tmblptr// SUSPECT //);`) marks it as doubted even when it was active. This is another artifact of the unresolved tension between "I-position = byte" and "I-position = atom."

---

### Synthesis

The code shows **two simultaneous models that were never fully reconciled**:

| Content type | I-span model | Mechanism |
|---|---|---|
| TEXTATOM | byte-granular: width = byte count | `granf2.c:100,106`, `tumblerincrement(..., 0, textset->length, ...)` |
| LINKATOM | atomic: width = 1 at finest tumbler depth | `do2.c:58`, `/*zzzzz*/` |

The byte-granular model for text was the **implemented** and **intended** resolution for the permascroll when storing character content. There is no multi-byte character encoding, no variable-width character remapping — bytes go in, byte positions come back out.

But the LINKATOM design embodies exactly the "variable-width atom" concept you are asking about: a single logical unit at one I-position, independent of byte count. The mantissa[2] partitioning infrastructure in `findisatoinsertmolecule` is extensible — atomtype 3, 4, 5 for image, audio, or other media would each get their own sub-address space. The `/* don't change these */` comment and the `> 2` ceiling in `validhint` mark the boundary where the design stopped being implemented without abandoning the extensible structure.

The `/*zzzzz*/` at `do2.c:58` is the most honest artifact: the developer who wrote the link span calculation was not certain whether a link should have any I-extent at all — zero or one? That unresolved question *is* the design seam between byte-granular permascroll and atom-granular permascroll. The code never chose a definitive answer.

**Conclusion**: Byte-granularity for text was the intended and implemented resolution. Variable-width atoms — where each logical content unit (character, media element) would occupy one I-position — existed as a structural affordance in the address arithmetic and atom-type design, instantiated only for LINKATOM, and never extended to other media types. The design anticipated it but did not finish it.

---

## Question 15 [gregory]

> Is the fan-out from I-space to V-space unbounded — can any number of documents map V-addresses to the same I-address range — or was there a practical or design limit on how many V→I references could share a single I-address span?

### Gregory's Answer

## KB Synthesis

The fan-out is **unbounded by design**. Multiple KB entries converge on this:

**POOM multimap within a single document**

[SS-POOM-MULTIMAP] (Finding 0039) establishes that the POOM is explicitly a multimap. `findcbcinarea2d()` accumulates *every* matching leaf node; `incontextlistnd()` inserts each into a sorted list and never replaces. A query by I-address returns all V-positions referencing it. [EC-SELF-TRANSCLUSION] confirms "no limit observed on number of V-positions per I-address" — tested at N=2 and N=3, with the mechanism making N unbounded.

**Cross-document fan-out via the spanfilade**

[SS-DOCISPAN] (Finding 0047): each COPY/INSERT creates one DOCISPAN entry per I-span in the spanfilade, mapping that I-address range to the document. Any number of documents can accumulate entries for the same I-address range. [INV-SPANF-WRITE-ONLY] (Finding 0057) confirms the spanfilade is append-only — entries are never removed. [PRE-COPY] (Finding 0046) confirms COPY performs no duplicate checking whatsoever.

**The design requires unbounded fan-out**

The entire Xanadu transclusion model depends on it. [INT-LINK-TRANSCLUSION] states links are discoverable from *any* document sharing content identity — which only works if an arbitrary number of documents can reference the same I-address range. [INV-IADDRESS-PERMANENT] and [INV-NO-IADDR-REUSE] ensure I-addresses persist forever, meaning the fan-out set can only grow.

**Practical constraints (not design limits)**

The only limits are resource-level:
- Memory: the grim reaper cache (all enfilades share one pool per [SS-CACHE-MECHANISM])
- Disk: `enf.enf` block allocator capacity per [SS-UNIFIED-STORAGE]
- Spanfilade growth: O(number of COPY/INSERT operations) per [INV-SPANF-GROWTH], not O(total bytes), so each transclusion event adds exactly one entry regardless of content size

There is no architectural cap, no reference-count limit, and no structural mechanism that would reject an N+1th document transcluding an already-N-times-transcluded I-address span.

---

## Code Exploration

Now I have everything I need. Here is my full answer.

---

## Fan-out from I-space to V-space in udanax-green

**Short answer:** The fan-out is architecturally unbounded in both directions. Any number of documents can map V-addresses to the same I-address range, and within a single document the same I-range can appear at multiple V-positions. There is no designed cap — the opposite is true: the entire infrastructure exists to support unlimited sharing.

---

### How V→I and I→V mappings are stored

Each document has an **orgl** — a POOM (permutation-matrix) enfilade. A POOM crum carries a two-dimensional width/displacement: `dsas[I]` for I-space and `dsas[V]` for V-space [wisp.h:19-21]. Every crum records one contiguous V→I mapping for one document.

```c
/* wisp.h:19-21 */
#define I  0
#define V  1
```

A global **spanfilade** (SPAN enfilade) serves as an inverted index: it maps I-address ranges back to document ISAs. Its crums use `dsas[ORGLRANGE]` (the document's prefix-tumbler'd ISA) and `dsas[SPANRANGE]` (the I-address range) [wisp.h:15-16].

---

### Cross-document fan-out: every `docopy` adds one more reference

When content is transcluded into a document, `docopy` [do1.c:45-65] does two things:

```c
/* do1.c:60-62 */
&& insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)
&&  insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN)
```

1. **`insertpm`** [orglinks.c:75-134] inserts a crum into *this document's orgl* mapping the requested V-address to the I-span.
2. **`insertspanf`** [spanf1.c:15-54] inserts a crum into the *global spanfilade* recording that this document now contains that I-span:

```c
/* spanf1.c:49-51 */
movetumbler (&lstream, &crumorigin.dsas[SPANRANGE]);
movetumbler (&lwidth, &crumwidth.dsas[SPANRANGE]);
insertnd(taskptr,(typecuc*)spanfptr,&crumorigin,&crumwidth,&linfo,SPANRANGE);
```

There is **no limit check** and **no deduplication across documents** anywhere in this path. Each call to `docopy` from a different document adds one more crum to the spanfilade for the same I-range. Ten thousand documents can independently reference the same I-span; the spanfilade accumulates ten thousand crums.

---

### How I→V fan-out is retrieved

`finddocscontainingsp` [spanf1.c:151-188] answers "which documents contain this I-span?" It calls `retrieverestricted` → `retrieveinarea` → `findcbcinarea2d` [retrie.c:229-268]:

```c
/* retrie.c:252-264 */
for (; crumptr; crumptr = getrightbro (crumptr)) {
    if (!crumqualifies2d (...)) {
        continue;
    }
    if (crumptr->height != 0) {
        findcbcinarea2d (findleftson ((typecuc*)crumptr), &localoffset, ...);
    } else {
        context = makecontextfromcbc ((typecbc*)crumptr, (typewid*)offsetptr);
        incontextlistnd (headptr, context, index1);
    }
}
```

This is a recursive traversal of the entire matching subtree. Every qualifying crum is appended to `headptr` — a linked list. Back in `finddocscontainingsp`:

```c
/* spanf1.c:170-180 */
for (; ispanset; ispanset = ispanset->next) {
    context = retrieverestricted ((typecuc*)spanf, &docspace, ORGLRANGE, ispanset, SPANRANGE, (typeisa*)NULL);
    for (c = context; c; c = c->nextcontext) {
        movetumbler (&c->totaloffset.dsas[ORGLRANGE], &docid);
        beheadtumbler (&docid, &document.address);
        ...
        addresssetptr = (typelinkset *) onitemlist(taskptr, (typeitem*)&document, (typeitemset*)addresssetptr);
    }
    contextfree (context);
}
```

The inner loop has no `break`, no maximum count, no page size. It collects every document that references the I-span. The result list is as long as the fan-out is deep.

---

### Per-document fan-out: same I-range at multiple V-positions

Within a single document, the same I-range can appear at multiple V-addresses. `insertpm` [orglinks.c:100-132] loops over `sporglset` and calls `insertnd` for each entry:

```c
/* orglinks.c:100-131 */
for (; sporglset; sporglset = (typesporglset) sporglset->xxxxsporgl.next) {
    unpacksporgl (sporglset, &lstream, &lwidth, &linfo);
    movetumbler (&lstream, &crumorigin.dsas[I]);
    movetumbler (vsaptr, &crumorigin.dsas[V]);
    ...
    insertnd (taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);
    tumbleradd (vsaptr, &crumwidth.dsas[V], vsaptr);
}
```

Calling `docopy` twice with the same `ispanset` and different `vsaptr` values yields two crums in the orgl with the same `dsas[I]` but different `dsas[V]`. There is no uniqueness constraint on I-addresses within an orgl. The I→V conversion `ispan2vspanset` [orglinks.c:389-394] → `permute` → `span2spanset` → `retrieverestricted` → `findcbcinarea2d` returns all matching crums — again without a limit.

---

### The one place fan-out is *reduced*: `isanextensionnd`

In `insertcbcnd` [insertnd.c:242-275], before creating a new bottom crum the code checks whether the incoming span is a contiguous extension of an existing one from the *same* source document:

```c
/* insertnd.c:249-258 */
for (ptr = findleftson (father); ptr; ptr = findrightbro (ptr)) {
    if (isanextensionnd ((typecbc*)ptr, grasp, origin, infoptr)) {
        dspadd (&ptr->cwid, width, &ptr->cwid, (INT)father->cenftype);
        ivemodified (ptr);
        setwispupwards (father,1);
        ...
        return(FALSE);
    }
}
```

`isanextensionnd` [insertnd.c:301-309] checks two things: the `homedoc` fields must match (same source document), and the new span must start exactly where the existing crum ends (`reach == origin`). If both are true, the existing crum is widened rather than a new one created.

This is a **fragmentation-reduction optimization**, not a fan-out cap. It only merges runs *within the same document* that are strictly contiguous in both dimensions. Two different documents referencing the same I-range never trigger this merge, so cross-document fan-out is never pruned.

---

### What the constants actually bound

| Constant | Value | What it limits |
|---|---|---|
| `NPLACES` [common.h:53] | 16 | Depth of tumbler addresses (16 digit levels, each `uint32_t`) |
| `MAXUCINLOAF` [enf.h:26] | 6 | Children per upper crum in one on-disk loaf |
| `MAX2DBCINLOAF` [enf.h:27] | 4 | 2D bottom crums per loaf |
| `MAXCUTS` [common.h:108] | 4 | Cut positions in one `dorearrange` call |

None of these is a logical cap on the number of documents sharing an I-span. `MAXUCINLOAF` and `MAX2DBCINLOAF` are disk storage granularity constants; the `splitcrumupwards` mechanism [called from `insertcbcnd` line 272] grows the tree upward when a loaf fills up, so the enfilade height is unbounded.

The only genuine constraint is the address space: `NPLACES = 16` mantissa digits of `tdigit = uint32_t` per tumbler. This makes the I-address space astronomically large (up to ~(2³²)¹⁶ positions per document) but not literally infinite. In practice, storage exhaustion (heap + disk) is the effective limit long before the address space runs out.

---

### Conclusion

**The fan-out is unbounded by design.** The architecture explicitly expects — and is engineered to support — an arbitrary number of documents referencing any single I-address span. The spanfilade exists precisely to make that many-to-one reverse mapping queryable at scale. There is no counter, cap, `MAX_TRANSCLUSIONS` constant, or any other limiting mechanism anywhere in the code path from `docopy` through `insertspanf` through `finddocscontainingsp`. The only thing that narrows this in practice is available memory and disk, moderated by the grim reaper cache eviction (`age` field, [enf.h:41]).

---

## Question 16 [gregory]

> When content becomes unreachable from all V-space mappings, it persists in I-space indefinitely — is there any mechanism or query to enumerate these orphaned I-address ranges, or are they invisible unless you already know their addresses?

### Gregory's Answer

## KB Synthesis

No. Orphaned I-address ranges — content in the granfilade with no current POOM mapping — are invisible through any available query mechanism unless you already know their addresses.

## What persists and why

[INV-IADDRESS-PERMANENT] and [INV-NO-IADDR-REUSE] establish the situation: every I-address ever allocated lives forever in the granfilade, and DELETE never removes them — it only removes the POOM (V→I) mappings [FC-GRANF-ON-DELETE]. The I-space grows monotonically and unconditionally.

## The only reverse-lookup mechanism: FINDDOCSCONTAINING

[INV-IADDRESS-PERMANENT] documents that `FINDDOCSCONTAINING(i)` continues to report documents even after deletion removes the V-space mapping. But [EC-STALE-SPANF-REFERENCE] makes this problematic: the spanfilade is append-only ([INV-SPANF-WRITE-ONLY]) and is never cleaned up after DELETE ([INT-DELETE-SPANF-DIVERGENCE]). The formal relationship is:

```
actual_docs(i) ⊆ find_documents(i)
```

The reverse does not hold. FINDDOCSCONTAINING returns a **superset** — stale references to documents whose POOM no longer maps those I-addresses. To distinguish live from orphaned, you'd need to perform I-to-V conversion in every returned document: [INV-ITOV-FILTERING] specifies that the conversion layer silently drops any I-address with no current POOM mapping, returning empty results for orphaned addresses. But this requires you to already have the I-addresses to query.

## No scan or enumeration exists

The granfilade is a B-tree keyed by I-address, but no FEBE operation exposes "walk all allocated I-addresses" or "find I-addresses with no V-space mapping." [SS-UNIFIED-STORAGE] confirms all state is in a single tree structure, but tree traversal is not an exposed operation. The FEBE protocol offers:

- Content retrieval (requires knowing V-positions)
- FINDDOCSCONTAINING (requires knowing I-addresses, returns stale superset)
- I-to-V conversion (silently filters misses per [INV-ITOV-FILTERING], requires knowing I-addresses)

None of these let you enumerate the set of orphaned addresses from scratch.

## Compound workaround (partial)

If you know a specific I-address is suspect, the closest approximation is:
1. Call FINDDOCSCONTAINING to get candidate documents
2. For each candidate, attempt I-to-V conversion
3. Empty results → orphaned in that document; empty across all candidates → globally orphaned

But there is no way to discover the orphaned I-addresses themselves without prior knowledge of their values. [EC-GHOST-LINK] notes this in the link context: permanent I-space existence doesn't imply reachability, and reconstitution is possible if you know the address — but discovery from scratch is not supported.

---

## Code Exploration

## Orphaned I-Address Ranges in Udanax-Green: No Enumeration Mechanism Exists

The short answer: **orphaned I-address ranges are invisible to the system.** There is no mechanism to discover them, and the architecture makes no provision for it.

---

### How I-Space Is Structured

I-space content lives in the **granfilade** — a tree of enfilades stored on disk. Addresses are allocated during insertions (`findisatoinsertmolecule` in `backend/granf2.c`) and persist permanently. There is no free-list, no reference count per I-address, and no allocation bitmap for I-space.

The only traversal primitive that walks the granfilade is `findpreviousisagr()` [`backend/granf2.c:255-278`], which searches *downward* to find an address below an upper bound — used purely as an allocation hint, not enumeration.

---

### The V↔I Asymmetry

The bridge functions in `backend/orglinks.c` all operate *one direction only when you already know something*:

- `vspanset2ispanset()` [`:397`] — converts V-spans → I-spans (you must supply the V-spans)
- `ispan2vspanset()` [`:389`] — converts I-spans → V-spans (you must supply the I-spans)
- `permute()` [`:404-422`] — iterates over a *provided* restriction spanset; it cannot discover spans that have no V-space existence

There is no "what I-spans exist?" query. All I-space access flows through V-space references.

---

### What the Find/Query Functions Cover

Every query in `backend/do2.c` and `backend/fns.c` requires V-space input:

- `dofind` / `finddocscontaining` [`backend/do1.c:15-23`, `backend/fns.c:20-32`] — finds documents containing *specified* content, not unspecified orphans
- `findnextlinkvsa()` [`backend/do2.c:151`] — scans for links within a *specified* document's V-space
- `doretrieve()` — retrieves at a *known* I-address

None of these can discover content for which there is no surviving V-space reference.

---

### Memory Management Is Not Content Tracking

`grimlyreap()` [`backend/credel.c:106-162`] and `isreapable()` [`:164-289`] manage the **in-memory crum cache** — they free RAM, not disk content. The doubly-linked `nextcrum`/`prevcrum` ring in `backend/enf.h:37-38,61-62` connects in-memory crums for reaping purposes only; it is not a traversal of all I-space addresses.

`diskalloc()` [`backend/diskalloc.c:27-54`] tracks **disk loaf block allocation** via bitmap, not I-address usage. Reclaiming a disk block does not reclaim an I-address range.

---

### Conclusion

When a V-span is deleted, its corresponding I-spans become permanently orphaned:

1. The granfilade retains the content nodes on disk
2. No reference counter decrements
3. No free-list records the now-unreachable range
4. No scan can discover the gap without already knowing the I-addresses

**To enumerate orphans would require:** a forward I-space iterator (no `getNextIAddress()` exists), an allocation registry for I-space (only disk blocks are tracked), and a cross-reference sweep comparing all allocated I-ranges against all V-space mappings. The architecture provides none of these. The content is not invisible *because* it is orphaned — it was always invisible; V-space was the only way to point at it, and once that pointer is gone, the data is unreachable but not freed.

---

## Question 17 [gregory]

> The V→I mapping within a single document can become arbitrarily fragmented (many small spans rather than a few large ones) through editing — does this fragmentation degrade any system behavior beyond requiring more mapping entries, or is it purely a representation cost?

### Gregory's Answer

## KB Synthesis

Fragmentation is not purely a representation cost. It has several behavioral consequences:

## Observable behavioral changes

**Link endset fragmentation** [ST-LINK-CREATE/Finding 0037]: When a vcopy or link endpoint spans content assembled from multiple non-contiguous I-address regions, `vspanset2sporglset` creates one sporgl per contiguous I-address run. Fragmented source content → more sporgls per endpoint. This is observable: `retrieve_endsets` returns more V-spans, and the bugs [EC-PIVOT-LINK-FRAGMENTATION], [EC-MULTISPAN-LINK-DUPLICATION] arise directly from this — after pivot rearrangement, links can appear duplicated in `find_links` results because the endset decomposes into redundant entries.

**Spanfilade growth** [SS-DOCISPAN/Finding 0047, INV-SPANF-GROWTH]: COPY of fragmented content creates DOCISPAN entries proportional to the number of I-spans, not bytes. A heavily edited document used as a VCOPY source permanently increases the spanfilade entry count per copy operation. Since the spanfilade is write-only [INV-SPANF-WRITE-ONLY], these entries accumulate forever.

## Permanent structural degradation

**Tree height ratchet** [SS-ENFILADE-TREE/Finding 0058]: Each cursor repositioning costs +2 crums [ST-CRUM-BOUND], and the POOM tree height grows monotonically (`levelpull` is disabled). The tree never shrinks even after delete-everything. This means heavily-edited documents carry permanently inflated lookup overhead — O(log N) where N is the lifetime crum count, not the current content size.

**CREATELINK breaks I-address contiguity** [INT-LINK-INSERT/Finding 0063]: CREATELINK allocates an orgl in the granfilade's content address range, causing all subsequent text inserts to allocate non-contiguous I-addresses relative to pre-link text. This makes `compare_versions` report two spans instead of one for otherwise contiguous text, and increases DOCISPAN entry count for any COPY spanning the gap.

## Purely representational costs

The following are costs without behavioral change:
- More crums in the cache → more memory pressure → more grim-reaper evictions [EC-CROSS-ENFILADE-EVICTION], but this affects durability ordering, not correctness
- V-span output is consolidated [INV-VSPAN-CONSOLIDATION] — `retrieve_vspanset` hides I-space fragmentation from callers retrieving text content

## Summary

The critical threshold is whether fragmented content is used as a **link endpoint or vcopy source**. At that point, fragmentation propagates into the spanfilade as permanent additional entries [SS-DOCISPAN], produces observable endset fragmentation bugs [EC-PIVOT-LINK-FRAGMENTATION], and increases the complexity of `find_links` intersection [SS-FIND-LINKS/Finding 0035]. For documents that are only read, fragmentation is representational overhead only.

---

## Code Exploration

Now I have everything I need to give a complete answer.

---

## V→I Fragmentation: Behavioral Degradation Beyond Representation Cost

Fragmentation is **not** purely a representation cost. The code shows six concrete degradation mechanisms, each tied to specific source lines.

---

### 1. `permute()` multiplies every V↔I conversion into N independent enfilade traversals

Both `vspanset2ispanset()` and `ispan2vspanset()` route through a single function [orglinks.c:397-401, 389-394]:

```c
typespanset *permute(...) {
    for (; restrictionspanset; restrictionspanset = restrictionspanset->next) {
        targspansetptr = span2spanset(taskptr, orgl, restrictionspanset,
                                      restrictionindex, targspansetptr, targindex);
    }
    return (save);
}
```
[orglinks.c:404-422]

Each iteration calls `span2spanset()` [orglinks.c:425-453], which calls `retrieverestricted()` — a full 2D POOM tree walk. For N fragments, this is **N independent enfilade traversals**, not one.

---

### 2. The retrieval inner loop is the documented CPU hotspot — and fragmentation fires it repeatedly

`retrieverestricted()` → `retrieveinarea()` → `findcbcinarea2d()` [retrie.c:229-268] recursively walks the POOM tree, calling `crumqualifies2d()` at every node. The comment on that function [retrie.c:270]:

```c
bool crumqualifies2d(...) /* 6-28-84 old code; NOTE in retrieves this is ---40% -- of cpu */
```

This is the identified bottleneck. Every fragment fires it from the root.

---

### 3. Each fragment permanently grows the POOM and spanfilade

`insertpm()` [orglinks.c:100-132] loops over the sporglset (one entry per ispan fragment) and calls `insertnd()` for each:

```c
for (; sporglset; sporglset = (typesporglset) sporglset->xxxxsporgl.next) {
    ...
    insertnd (taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);
    tumbleradd (vsaptr, &crumwidth.dsas[V], vsaptr);
}
```

Likewise `insertspanf()` [spanf1.c:25-52] adds one spanfilade node per fragment:

```c
for (; sporglset; sporglset = (typesporglset)((typeitemheader *)sporglset)->next) {
    ...
    insertnd(taskptr,(typecuc*)spanfptr,&crumorigin,&crumwidth,&linfo,SPANRANGE);
}
```

After `insertnd()`, `recombine()` is called [insertnd.c:76] to rebalance — but the enfilade can only grow (see next point).

---

### 4. `levelpull` is completely stubbed — the enfilade never shrinks

`recombinend()` [recombine.c:104-131] tries to shrink the tree when it's underpopulated [recombine.c:129-130]:

```c
if (father->isapex)
    levelpull (father);
```

But `levelpull` [genf.c:318-342] is dead code:

```c
int levelpull(typecuc *fullcrumptr)
{
    return(0);
    /*
        [entire implementation commented out]
    */
}
```

The enfilade trees — POOM and spanfilade — are monotonically increasing. Every fragmented insertion adds permanent nodes. Since the tree height grows logarithmically with node count, a heavily-fragmented document has a deeper tree, and all future retrievals pay deeper recursion in `findcbcinarea2d()`.

---

### 5. `finddocscontainingsp()` and `retrievesporglsetinrange()` both loop per fragment

"Find which documents contain this content" [spanf1.c:170-182]:

```c
for (; ispanset; ispanset = ispanset->next) {
    context = retrieverestricted ((typecuc*)spanf, &docspace, ORGLRANGE,
                                  ispanset, SPANRANGE, (typeisa*)NULL);
    ...
    contextfree (context);
}
```

And the link-following path's `retrievesporglsetinrange()` [do2.c:244-266]:

```c
for (; sporglptr; sporglptr = (typesporglset)sporglptr->xxxxsporgl.next) {
    context = retrieverestricted((typecuc*)spanf, (typespan*)sporglptr,
                                  SPANRANGE, whichspace, ORGLRANGE, ...);
    ...
}
```

Both are: one enfilade traversal per fragment. A logical content range split into N fragments by editing causes both queries to cost N× what they would for an unfragmented document.

---

### 6. Result list accumulation is O(N²) via `onitemlist()`

Every result span is appended by scanning to the list tail [orglinks.c:522-534]:

```c
for (temp = *itemsetptr;
     temp && ((typeitemheader *)temp)->next;
     temp = (typeitem *)((typeitemheader *)temp)->next)
    ;
((typeitemheader *)temp)->next = (typeitemheader *)newitem;
```

With N fragments each producing results, the accumulation cost is quadratic in the total result count.

---

### 7. Consolidation was recognized as the fix — and abandoned

Inside `permute()`, there is a commented-out call [orglinks.c:412-413]:

```c
/*consolidatespans(restrictionspanset);
foospanset("restrictionset after consolidation is ",restrictionspanset); */
```

At the end of the file there's an incomplete stub [orglinks.c:456-462]:

```c
/*
consolidatespanset(spanset);
  typespan *spanset;
{
    for(;spanset->next;spanset = spanset->next){
        if(
    }
}*/
```

The body stops mid-expression. `cleanupvspanlist()` [orglinks.c:297-311], which does merge adjacent spans, exists inside an `#ifdef UnDEFined` block — also disabled.

The developers diagnosed the problem, attempted a fix, and abandoned it.

---

### Summary

| Operation | Fragmentation effect |
|---|---|
| `vspanset2ispanset` / `ispan2vspanset` | N enfilade traversals instead of 1, at the documented 40%-of-CPU hotspot |
| `finddocscontainingsp` | N enfilade traversals instead of 1 |
| `retrievesporglsetinrange` (link follow) | N enfilade traversals instead of 1 |
| `insertpm` / `insertspanf` (copy/insert) | N permanent POOM/spanfilade nodes added |
| `onitemlist` result accumulation | O(N²) list-scan overhead |
| Enfilade tree height | Monotonically increases; `levelpull` is stubbed, so fragmentation-induced growth is permanent |

The enfilade's log-depth guarantee applies **per query**, not across a span set. N fragments = N queries = N × log(height) work. And because `levelpull` is stubbed, every fragmented insertion ratchets the tree permanently deeper, making all future traversals more expensive. There is no consolidation, no self-healing, and no upper bound on fragment count.

---

## Question 18 [gregory]

> Was the two-space architecture (mutable V-positions over immutable I-identities) present from the earliest Xanadu designs, or did it emerge during green's implementation as a solution to a specific problem like transclusion tracking or content-addressed linking?

### Gregory's Answer

## KB Synthesis

The KB does not contain information to answer this question.

The entries document what the implementation does and why specific mechanisms work the way they do, but contain no historical or archival evidence about design chronology — no references to design documents, early prototypes, Nelson's notebooks, or the evolution of the architecture over time.

What the KB *does* show is that the two-space architecture has strong internal coherence: the `acceptablevsa()` stub [SS-SUBSPACE-CONVENTION, Finding 0010] signals the subspace convention was a *planned* enforcement point that was never completed, suggesting the V/I distinction predates the green implementation as a design intent rather than emerging from it. The clean separation of `granf` and `spanf` into distinct global structures initialized at startup [SS-DUAL-ENFILADE, Finding 0012] also suggests deliberate upfront architectural choice rather than organic accretion.

But whether that design intent originated in 1960s Xanadu theory, the ZigZag period, or earlier in green's development — that's not answerable from this KB. You'd need the design documents or my direct recollection of those conversations, which isn't what this KB captures.

---

## Code Exploration

Now I have everything I need. Here is my full answer.

---

## The Two-Space Architecture in udanax-green: Code Evidence

The question is whether the V-position / I-identity split was designed from the beginning or emerged during implementation. The source code answers this decisively — but the answer requires tracing through the actual data structures rather than relying on retrospective accounts.

---

### What the Code Actually Defines

The two-space architecture is encoded in its most primitive, non-derivable form in `wisp.h:18-20`:

```c
/* wid and dsp indexes for pm */
#define I  0
#define V  1
```

These two constants — `I` for invariant, `V` for variant — are indices into every positional array in the system. They appear at the bottom of the type hierarchy, before any enfilade-specific logic.

The type that carries both coordinates is `typewid`/`typedsp`, defined at `wisp.h:48-55`:

```c
#define MAXLOXIZE 2    

struct structwid {
    tumbler dsas[MAXLOXIZE];
};
typedef struct structwid typewid;
typedef typewid typedsp;
```

`MAXLOXIZE = 2`: one slot for I, one for V. Both slots are tumblers — the system's arbitrary-precision address type. There is no asymmetry in representation; I and V are equal citizens in the struct.

The diagram in `wisp.h:29-44` makes explicit what each enfilade type carries in each dimension:

```
                   wid             dsp
    -----------------------------------------
   gr:  |           WIDTH           WIDTH
        |
   sp:  |         ORGLRANGE         ORGLRANGE
        |           SPANRANGE         SPANRANGE
        |
   pm:  |             I                 I
        |               V                 V
```

The POOM (permutation matrix) is the only enfilade that carries both I and V. This is the architectural fact: POOM is a **2D tree**, and its dimensionality is not an afterthought — it is what makes it a POOM.

---

### How the Two-Space Structure Propagates

Every crum in the tree carries both coordinates. From `enf.h:47-48` (the shared header for all crum types):

```c
typewid cwid;
typedsp cdsp;
```

`cwid` is the width in both dimensions; `cdsp` is the displacement in both dimensions. Since both are `typewid` (i.e., `tumbler dsas[2]`), every crum — from the apex down to each bottom leaf — simultaneously knows its extent in I-space (`dsas[I]`) and its extent in V-space (`dsas[V]`). This is not a mapping between two separate structures. It is one structure with two coordinate axes.

The rearrangement cut structure in `ndenf.h:12-16` makes the directional asymmetry visible:

```c
typedef struct structknives {
    INT nblades;
    tumbler blades[MAXCUTS];
    INT dimension;  /* always V, assigned by rearrange2d */
} typeknives;
```

The comment `/* always V, assigned by rearrange2d */` is the only dimension-specific comment in the headers. Document editing — rearranging content — happens exclusively in V-space. I-addresses do not move. They cannot move. They are the identity axis.

---

### The POOM Insertion: Where Both Axes Are Set

The core two-space assignment happens in `insertpm()` (`orglinks.c:75-134`). This is the function that records content into a document's permutation matrix. At lines 105 and 113:

```c
movetumbler (&lstream, &crumorigin.dsas[I]);   /* line 105 */
...
movetumbler (vsaptr, &crumorigin.dsas[V]);      /* line 113 */
```

`lstream` is the I-address: where the content lives in the permascroll. It comes from the sporgl (span-original), which was set when the content was first written — immutable by design. `vsaptr` is the V-address: where the user placed this content in the current document. It is mutable; it shifts when other content is inserted or deleted around it.

Both are written into the same `crumorigin` struct — into `dsas[I]` and `dsas[V]` respectively — and inserted into the POOM tree together via `insertnd()` at line 130:

```c
insertnd (taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);
```

The `V` argument to `insertnd` tells the tree insertion code which dimension is the primary ordering axis (V-positions order the document). But the I-coordinate rides along, stored in the same crum, accessible immediately without a separate lookup.

The inline comment at line 114 is an artifact of the development era:

```c
/*I'm suspissious of this shift <reg> 3/1/85 zzzz*/
```

This is a timestamped note — March 1, 1985 — from someone initialed "reg" who was uncertain about the tumbler shift calculation in `insertpm`. Note what is and is not in doubt: the arithmetic of one implementation detail is questioned; the two-axis structure of the crum origin is not questioned at all. It was not under review.

---

### The Conversion Functions: Architectural Symmetry

The V↔I conversion functions in `orglinks.c:389-454` exhibit perfect symmetry:

```c
/* line 389 */
typevspanset *ispan2vspanset(typetask *taskptr, typeorgl orgl, 
                              typeispan *ispanptr, typevspanset *vspansetptr)
{
    return permute(taskptr, orgl, ispanptr, I, vspansetptr, V);
}

/* line 397 */
typeispanset *vspanset2ispanset(typetask *taskptr, typeorgl orgl, 
                                 typevspanset vspanptr, typeispanset *ispansetptr)
{
    return permute(taskptr, orgl, vspanptr, V, ispansetptr, I);
}
```

Both delegate to a single `permute()` at line 404:

```c
typespanset *permute(typetask *taskptr, typeorgl orgl, 
                     typespanset restrictionspanset, INT restrictionindex,
                     typespanset *targspansetptr, INT targindex)
```

`permute()` takes a restriction dimension and a target dimension as generic integer parameters. The logic is completely symmetric — `I→V` and `V→I` are the same function, called with swapped arguments. This is not the shape of a function that was added retroactively to solve a transclusion tracking problem. It is the shape of a function that was written knowing from the beginning that both directions would be needed in equal measure.

---

### The Type System Encodes the Distinction

From `xanadu.h:73-76`:

```c
typedef typespan typevspan;
typedef typevspan * typevspanset;
typedef typespan typeispan;
typedef typeispan * typeispanset;
```

`typevspan` and `typeispan` are identical in representation — both are `typespan` with `stream` and `width` tumblers. The distinction is semantic, not structural. This is a C-era design choice that says: "these two things are the same bits, but they must not be confused." The naming convention enforces at the type level what the architecture enforces at the data level. You do not build this vocabulary into your type system unless you plan to use it throughout.

---

### What the Code Cannot Tell Us

The code contains no design rationale comments explaining *why* I and V exist. Every comment in `orglinks.c`, `wisp.h`, and `enf.h` treats the two-space model as an established fact. There is no "we added this because..." note, no historical comment explaining the motivation. The vocabulary — permutation matrix, invariant, variant, virtual space address — is used without explanation, as though it required none.

The comment header of `orglinks.c:9` identifies the file's purpose:

```
/* orglinks.d - permutation matrix enfilade calls */
```

The name "permutation matrix" encodes the architecture: a matrix that permutes between two coordinate systems. This is what a POOM is. The naming is not incidental.

---

### The Answer

The two-space architecture was **present from the earliest design** and is not a solution to a problem discovered during implementation.

The evidence for this in the code:

1. **It is structurally irreducible.** `MAXLOXIZE = 2` is a named constant embedded in the lowest primitive type. Every crum — in every enfilade — carries a 2-slot array. You cannot peel the I/V duality off the data structure without redesigning the data structure.

2. **The conversion is symmetric.** `permute()` was written to handle both `I→V` and `V→I` with identical generality. This is first-class design, not a retrofit.

3. **The type system encodes it.** `typevspan` and `typeispan` are named distinct types despite being structurally identical. The distinction is semantic intent baked into the type aliases before any function was written.

4. **Rearrangement is V-only by invariant.** `ndenf.h:15` says `dimension; /* always V, assigned by rearrange2d */`. The I-axis does not rearrange. This is not a constraint added after the fact; it is the definition of what I means.

5. **The POOM is the architecture.** The POOM is a 2D tree. Its two dimensions ARE the two spaces. Transclusion tracking — finding every document containing a given I-address — is the natural query in this structure: walk the POOM restricted to a given I-range and collect all corresponding V-positions. This query (`ispan2vspanset`) is exactly what `permute()` provides.

The V/I separation corresponds to Ted Nelson's published distinction between "virtual" addresses (positions in a particular document) and "invariant" addresses (permanent locations in the permascroll). That vocabulary predates udanax-green. The code is a faithful implementation of a conceptual model that was already articulated before any of this C was written. The two-space architecture did not emerge to solve a specific implementation problem. It was the problem the implementation was designed to encode.
