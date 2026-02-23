# Consultation Answers — Content Insertion

**Inquiry:** What must INSERT preserve and establish? What are its preconditions, postconditions, and frame conditions with respect to the address space, existing content, and links?
**Date:** 2026-02-23 13:19
**Questions:** 20 (10 nelson, 10 gregory)

---

## Question 1 [nelson]

> When new content is inserted into a document, must every piece of content that existed before the insertion remain retrievable at its original identity?

### Nelson's Answer

## Yes — absolutely and by design.

When new content is inserted into a document, every piece of content that existed before the insertion remains retrievable at its original identity. This is not a side-effect but a foundational architectural guarantee.

### The I-Space/V-Space Separation

Xanadu maintains two distinct address spaces. I-space is where content **permanently lives** — addresses are absolute and immutable. V-space is the document's **current arrangement** — a view that can be rearranged across versions.

INSERT operates on V-space while only *appending* to I-space:

> "This inserts \<text set\> in document \<doc id\> at \<doc vsa\>. The v-stream addresses of any following characters in the document are increased by the length of the inserted text." [LM 4/66]

The operation explicitly shifts *V-stream addresses* of following characters. It says nothing about altering I-space, because I-space is append-only by design. The new content receives fresh I-addresses; existing I-addresses are untouched.

### The Append-Only Storage Model

Nelson explicitly rejects destructive replacement:

> "Virtually all of computerdom is built around the destructive replacement of successive whole copies of each current version." [LM 2/14]

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

In an append-only store, insertion *adds* — it never overwrites, moves, or removes existing content.

### The Permanence Guarantee

> "New items may be continually inserted in tumbler-space while the other addresses remain valid. This means that any address of any document in an ever-growing network may be specified by a permanent tumbler address." [LM 4/19]

This is stated directly in the context of insertion: new items are inserted, and **the other addresses remain valid**. Existing content's identity (its I-address) is unaffected.

### The Non-Destruction Guarantee

> "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate—without damaging the originals. This is done by inclusion links." [LM 2/45]

If even creating *new documents from old ones* cannot damage originals, then insertion within a single document certainly cannot.

### Why V-Address Shifting Doesn't Violate This

After an INSERT, existing content's V-addresses (positions in the current view) do shift. But Nelson explicitly distinguishes this from identity:

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." [LM 4/11]

And crucially:

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." [LM 4/30]

V-addresses are ephemeral positions. I-addresses are permanent identity. INSERT changes the former, never the latter.

### Summary

Every piece of pre-existing content survives an INSERT with its original identity intact because:

1. **I-space is append-only** — new bytes are added; existing bytes are never modified or removed
2. **I-addresses are permanent** — once assigned, they never change
3. **INSERT only affects V-space** — it shifts virtual positions, not content identity
4. **Links survive** — because they attach to I-space bytes, not V-space positions

This is the architectural core of Xanadu: the separation of permanent content identity from mutable document arrangement. Nelson designed the entire system around the principle that no editing operation — insertion, deletion, rearrangement — ever destroys or alters what already exists in I-space.

---

## Question 2 [nelson]

> Does insertion require that the target document already exist and that the inserting user hold appropriate permission over it?

### Nelson's Answer

## Yes to Both

### The Document Must Already Exist

INSERT takes a document ID as a parameter, which presupposes the document has been created:

> "This inserts \<text set\> in document \<doc id\> at \<doc vsa\>. The v-stream addresses of any following characters in the document are increased by the length of the inserted text." [LM 4/66]

Documents come into being through CREATENEWDOCUMENT:

> "This creates an empty document. It returns the id of the new document." [LM 4/65]

The sequence is: create the document first, then insert content into it. INSERT cannot conjure a document into existence — it operates on one that already has an address in the docuverse.

### The Inserting User Must Be the Owner

Nelson is unambiguous:

> "Every document has an owner, the person who created and stored it (or someone who arranged it to be created and stored, such as a publishing company)... Only the owner has a right to withdraw a document or change it." [LM 2/29]

INSERT is a modification operation. Only the owner may perform it.

### The Critical Corollary: Denial Is a Fork, Not an Error

Nelson's access model does not produce "permission denied" as a terminal state. If you cannot modify someone else's document, you create your own version:

> "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate — without damaging the originals. This is done by inclusion links." [LM 2/45]

The session-model principle is: you own it and modify freely, or you do not own it and create a version. Writing always succeeds — it just may succeed in a different document than you initially targeted.

### Summary

| Precondition | Required? | Basis |
|---|---|---|
| Target document exists | Yes | INSERT takes `<doc id>` [LM 4/66] |
| User is owner | Yes | "Only the owner has a right to... change it" [LM 2/29] |
| Non-owner alternative | Create a version | "making whatever changes seem appropriate — without damaging the originals" [LM 2/45] |

---

## Question 3 [nelson]

> Must the position chosen for insertion fall exactly within the document's current content boundaries, or may it extend beyond the last position?

### Nelson's Answer

## INSERT Position: Within Boundaries or Beyond?

Nelson does not explicitly constrain the valid range of the insertion position. His complete specification of INSERT at 4/66 is:

> "This inserts \<text set\> in document \<doc id\> at \<doc vsa\>. The v-stream addresses of any following characters in the document are increased by the length of the inserted text." [LM 4/66]

The phrase "at \<doc vsa\>" names a V-stream address but states no bounds.

### The Empty Document Argument

The strongest evidence that position m+1 must be valid comes from CREATENEWDOCUMENT:

> "This creates an empty document. It returns the id of the new document." [LM 4/65]

An empty document has m=0 bytes. If INSERT were restricted to positions within [1, m], the valid range would be empty — you could never add the first byte. INSERT at position 1 (which is m+1 when m=0) must therefore be permitted. There is no principled reason to allow m+1 only for empty documents but not for non-empty ones.

### The Shift Clause is Vacuously Satisfied

Nelson's effect description — "v-stream addresses of any following characters... are increased by the length of the inserted text" — applies cleanly at position m+1. There are no following characters, so no addresses shift. The new content simply appears at the end. This is consistent, not exceptional.

### Relationship to APPEND

Nelson specifies APPEND separately:

> "This appends \<text set\> onto the end of the text space of the document \<doc id\>." [LM 4/67]

APPEND is semantically equivalent to INSERT at position m+1. The existence of APPEND as a named convenience does not imply that INSERT at m+1 is forbidden — it may simply reflect that "add to the end" is common enough to warrant its own command.

### V-Space Addressing Confirms Position 1 as Lower Bound

V-addresses are dense and start at 1:

> "The digit after the one indicates the byte position in the current ordering of bytes. This is its virtual stream address." [LM 4/30]

Position 0 has no meaning in V-space. The valid range for insertion is therefore **[1, m+1]**, where m is the current document length: position 1 inserts before the first byte, position m+1 appends after the last, and any position between places content within the existing stream.

### Summary

Nelson does not state the valid range explicitly, but the design requires it to be **[1, m+1]**. The empty-document case makes m+1 mandatory; the shift semantics make it well-defined; and V-space addressing starting at 1 establishes the lower bound.

---

## Question 4 [nelson]

> After insertion, must the new content receive a permanent identity that has never been used before and will never be reused?

### Nelson's Answer

## Yes — absolutely and by multiple reinforcing principles.

Nelson's design requires that every insertion creates content at **fresh, never-before-used I-space addresses**. This follows from the convergence of several explicit guarantees.

### 1. Append-only storage

The storage model is fundamentally append-only:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

Content is added to I-space, never overwritten. There is no mechanism by which an existing I-address could be reassigned to new content.

### 2. Address permanence and immutability

> "New items may be continually inserted in tumbler-space while the other addresses remain valid. This means that any address of any document in an ever-growing network may be specified by a permanent tumbler address." [LM 4/19]

An address, once assigned, denotes that content forever. If addresses could be reused, the permanence guarantee would be meaningless — a reference made today could resolve to different content tomorrow.

### 3. The forking mechanism guarantees freshness

New addresses are created by "baptism" — monotonically extending the address tree:

> "One digit can become several by a forking or branching process. This consists of creating successive new digits to the right." [LM 4/20]

> "The owner of a given item controls the allocation of the numbers under it." [LM 4/20]

This is a forward-only process. Addresses are allocated in sequence; there is no mechanism to retreat or recycle. The tree only grows.

### 4. Content identity is creation-based, not value-based

From the content provenance model: content identity is based on **where and when it was created**, not on its byte values. Two insertions of the identical string "hello" into different documents produce **different I-addresses**. This only works if each insertion allocates fresh addresses.

### 5. Historical backtrack depends on it

> "The file management system we are talking about automatically keeps track of the changes and the pieces, so that when you ask for a given part of a given version at a given time, it comes to your screen." [LM 2/15]

If addresses were reused, reconstructing a previous version would be impossible — the system couldn't distinguish old content from new content occupying the same address.

### 6. Attribution depends on it

> "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control." [LM 4/11]

The I-address encodes origin (Node.0.User.0.Document.0.Element). Origin traceability requires that each element position is used exactly once — if reused, the attribution guarantee breaks.

### Summary

The answer is **yes**, by necessity. After insertion, new content must receive a permanent identity that:
- **has never been used before** (append-only storage, monotonic forking)
- **will never be reused** (address permanence, content immutability)

This is not a single explicit statement by Nelson but rather a structural consequence that follows inevitably from multiple interlocking guarantees: append-only storage [LM 2/14], permanent addresses [LM 4/19], monotonic forking [LM 4/20], creation-based identity, historical backtrack [LM 2/15], and origin traceability [LM 2/40]. Remove any one of these, and the system's fundamental promises collapse.

---

## Question 5 [nelson]

> Must all links whose endpoints referenced content in the document before insertion continue to resolve to exactly the same content afterward?

### Nelson's Answer

## Yes — Link Endpoints Are Invariant Under INSERT

INSERT cannot alter what any existing link resolves to. This follows directly from two foundational design choices:

### 1. Links Attach to Bytes, Not Positions

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes." [LM 4/42]

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." [LM 4/30]

Link endsets reference I-space addresses — the permanent identity of content. They do not reference V-space positions (which shift during editing).

### 2. INSERT Does Not Modify Existing I-Space

INSERT creates new bytes (which get fresh I-space addresses) and changes the V-space arrangement (positions after the insertion point shift). But it never touches existing I-space content. Since endsets point to I-space:

- The bytes referenced by every existing endset remain exactly where they were
- The content at those I-addresses is unchanged
- Therefore the link resolves to identical content

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." [LM 4/11]

V-space positions shift; I-space addresses don't. Links reference I-space. So links are unaffected.

### The Explicit Survivability Guarantee

Nelson states this directly as a design property covering all editing operations, INSERT included:

> "Links between bytes can survive deletions, insertions and rearrangements, if anything is left at each end." [LM 4/43]

For INSERT specifically, the "if anything is left" condition is trivially satisfied — INSERT adds content but removes nothing. Every byte that existed before the insertion still exists afterward. Therefore every link endpoint that resolved before continues to resolve to exactly the same content.

### Why This Matters

This is not an incidental property but the core reason for the I-space/V-space separation. Nelson designed the system so that the permanent content layer (I-space) and the mutable arrangement layer (V-space) are independent. Links bind to the permanent layer, making them immune to arrangement changes:

> "Content is permanent (I-space) → enables permanent citations, links. Arrangement is flexible (V-space) → enables editing, versions. Links point to I-space → survive editing. Edits change V-space → don't destroy content."

So yes: all links whose endpoints referenced content before an insertion must continue to resolve to exactly the same content afterward. This is guaranteed by the architecture itself.

---

## Question 6 [nelson]

> Does insertion into one version of a document leave every other version's content and structure completely unchanged?

### Nelson's Answer

## Yes — Insertion Into One Version Leaves All Other Versions Unchanged

This follows directly from Xanadu's architecture. The answer rests on three structural facts.

### 1. Each Version Has Its Own V-Space

Every version is a separate document with its own virtual byte stream. CREATENEWVERSION creates "a new document with the contents of document \<doc id\>" [LM 4/66]. The new document gets its own V→I mapping. From that point forward, the two versions are structurally independent arrangements over shared I-space content.

> "There is thus no 'basic' version of a document set apart from other versions—'alternative' versions—any more than one arrangement of the same materials is a priori better than other arrangements." [LM 2/19]

### 2. INSERT Targets a Single Document

INSERT operates on a specific document identified by `<doc id>`:

> "This inserts \<text set\> in document \<doc id\> at \<doc vsa\>. The v-stream addresses of any following characters in the document are increased by the length of the inserted text." [LM 4/66]

The V-stream address shifts happen only within the targeted document. No other document's V-stream is mentioned or affected.

### 3. I-Space Is Append-Only and Immutable

INSERT adds new bytes to I-space; it never modifies existing I-space content:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

Since other versions' V→I mappings point to existing I-space addresses, and those addresses are immutable, the content those versions reference is untouched. The new I-space bytes created by INSERT exist only in the modified version's V-space arrangement.

### Nelson's Non-Destruction Principle

This version independence is a specific case of Nelson's broader guarantee:

> "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate—without damaging the originals. This is done by inclusion links." [LM 2/45]

And from the delete semantics (which apply equally to the structural reasoning):

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

### Summary

Insertion into version A:
- **Creates** new I-space bytes (append-only; existing content untouched)
- **Modifies** version A's V-space mapping (shifts subsequent V-addresses)
- **Does not touch** any other version's V-space mapping
- **Does not modify** any existing I-space content that other versions reference

Every other version's content and structure remain exactly as they were.

---

## Question 7 [nelson]

> Must the system guarantee that the inserted content becomes immediately and permanently retrievable — that no future operation can make it vanish?

### Nelson's Answer

# Yes — On Both Counts

Nelson's design makes inserted content both immediately available and permanently indestructible within the system. These are not incidental properties but load-bearing guarantees that the entire architecture depends upon.

## Immediate Retrievability

Nelson is explicit that content materializes the moment you request it:

> "THE PART YOU WANT COMES WHEN YOU ASK FOR IT." [LM 2/16]

> "We call this pounce. You pounce like a cat on a given thing, and it seems to be there, having been constructed while you wait, as it were, in midair." [LM 2/16]

This is a user-facing guarantee, not merely an aspiration. The system is designed so that once an operation completes, the content is part of the living docuverse — addressable, retrievable, linkable. There is no staging area, no pending state, no eventual consistency in Nelson's model. Content that has been inserted IS content in the system.

## Permanent Retrievability

No operation in the FEBE protocol destroys I-space content. Nelson's storage model is explicitly append-only:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

Every byte receives a permanent I-space address:

> "New items may be continually inserted in tumbler-space while the other addresses remain valid. This means that any address of any document in an ever-growing network may be specified by a permanent tumbler address." [LM 4/19]

## DELETE Cannot Make Content Vanish

The strongest evidence is what DELETE actually does. It operates on V-space (the document's current arrangement) and leaves I-space (permanent storage) untouched:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

The phrase "not currently addressable" is precise — the content is not gone, merely not visible in the current V-space arrangement. It remains in I-space, accessible through historical backtrack and still present in any other document that transcludes it.

## No Other Operation Threatens I-Space Content

Examining the FEBE operations:

- **INSERT** adds to I-space; never removes
- **DELETE** removes from V-space only
- **REARRANGE** is a pure V-space operation
- **COPY** creates V-space references to existing I-space content
- **CREATENEWVERSION** creates a new V-space arrangement over shared I-space content

There is no FEBE command that removes bytes from I-space. The operation set is designed so that I-space only grows.

## Published Content Has an Additional Social Lock

For published documents, Nelson adds an explicit social guarantee beyond the technical one:

> "It is in the common interest that a thing once published stay published, as in the world of paper. Other readers and users will come to depend on its accessibility. Consequently its author may not withdraw it except by lengthy due process." [LM 2/43]

This is because links made by other users depend on the content's continued existence:

> "However, for corrections and amendments, the author may readily publish a superseding document, but the former version must remain on the network. This is vital because of the links other users may have made to it." [LM 2/43]

## The Deeper Principle

Nelson's non-destruction guarantee is not just a feature — it is the architectural foundation:

> "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate — without damaging the originals. This is done by inclusion links." [LM 2/45]

> "Virtually all of computerdom is built around the destructive replacement of successive whole copies of each current version." [LM 2/14]

Xanadu exists precisely to abolish destructive replacement. If any operation could make inserted content vanish, the system would reduce to conventional file storage — the very thing Nelson designed Xanadu to transcend.

## Summary

The system must guarantee both properties:

1. **Immediate**: Once INSERT completes, the content is retrievable. It has a permanent I-space address, is part of the docuverse, and can be linked to, transcluded, and queried.

2. **Permanent**: No subsequent operation — not DELETE, not REARRANGE, not any combination of FEBE commands — can remove content from I-space. The only thing that can change is *which V-space arrangements reference it*. The content itself endures.

This is the meaning of the append-only storage model: I-space grows monotonically. Once bytes enter, they never leave. The entire edifice of permanent addresses, link survivability, historical backtrack, version comparison, and automatic attribution depends on this being true without exception.

---

## Question 8 [nelson]

> After insertion shifts existing content to later positions, must the correspondence between each piece of content and its permanent identity be preserved exactly?

### Nelson's Answer

## Yes — This Is the Central Architectural Invariant

After INSERT shifts existing content to later V-space positions, the correspondence between each piece of content and its permanent I-space identity **must** be preserved exactly. This is not merely a desirable property — it is the foundation on which permanence, link survivability, attribution, correspondence, and transclusion all depend.

### The V-Space / I-Space Separation

Nelson designed two address spaces precisely to allow editing without disturbing identity:

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." [LM 4/30]

INSERT changes V-space addresses — that is its defined effect:

> "The v-stream addresses of any following characters in the document are increased by the length of the inserted text." [LM 4/66]

But V-space is explicitly ephemeral:

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." [LM 4/11]

The I-space address — the permanent identity — is what must not change. Content at an I-space address is immutable. The document IS the mapping from V-addresses to I-addresses; INSERT modifies that mapping by shifting entries, but must not alter which I-address any pre-existing content maps to.

### What Depends on This Preservation

**Link survivability.** Links attach to I-space content, not V-space positions:

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes. This has a crucial advantage: it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them." [LM 4/42]

If INSERT corrupted the V→I mapping (swapping which I-address a V-position refers to), links would silently attach to wrong content — a silent data corruption worse than breaking.

**Origin traceability.** Nelson guarantees:

> "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

This guarantee holds because I-addresses encode provenance (Node.0.User.0.Document.0.Element). If INSERT scrambled the mapping, you could no longer ascertain the home document of a character at a given position.

**Correspondence.** Version comparison works because shared I-space origin is the basis for identifying which parts of two versions match:

> "a facility that holds multiple versions of the same material, and allows historical backtrack, is not terribly useful unless it can help you intercompare them in detail — unless it can show you, word for word, what parts of two versions are the same." [LM 2/20]

If INSERT in version 2 corrupted the V→I mapping for content that was unchanged, the system would falsely report that unchanged content had changed — or worse, report false correspondences.

**Transclusion.** When content is transcluded (included by reference), the V→I mapping in the including document points to I-addresses owned by another document:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

If INSERT in the including document corrupted the mapping, transcluded content would silently display wrong bytes from wrong origins — violating both attribution and content integrity.

**Royalties.** The economic model pays per-byte to the content owner identified by I-address. A corrupted mapping would pay the wrong author.

### Summary

INSERT shifts V-space positions. It must **not** alter which I-space content any pre-existing V-position refers to. This is not stated as a separate axiom by Nelson because it is intrinsic to the two-space architecture: V-space is arrangement, I-space is identity, and editing changes arrangement while preserving identity. Every guarantee Nelson makes — permanence, attribution, link survivability, correspondence, transclusion, royalty — depends on this preservation being exact.

---

## Question 9 [nelson]

> Must insertion be all-or-nothing — either the new content appears and all bookkeeping updates succeed together, or the document remains as if nothing happened?

### Nelson's Answer

## Nelson Does Not Explicitly Require Atomicity

Literary Machines is silent on whether insertion (or any FEBE operation) must be all-or-nothing. Nelson describes operations purely in terms of their completed effects — what the state looks like *after* the operation — without addressing what happens if an operation fails partway through.

### What Nelson Does Say

**Operations are described as complete transitions.** INSERT is specified as:

> "This inserts \<text set\> in document \<doc id\> at \<doc vsa\>. The v-stream addresses of any following characters in the document are increased by the length of the inserted text." [LM 4/66]

This describes a single, coherent outcome: content appears at a position, and all subsequent addresses shift by the full insertion length. There is no discussion of partial insertion, partial address shifts, or recovery from incomplete operations.

**The enfilade invariant is the closest statement.** Describing Barus's contribution to the data structure design:

> "All changes, once made, left the file remaining in canonical order, which was an internal mandate of the system." [LM 1/34]

This establishes a **consistency requirement** — every change must leave the structure in a valid ("canonical") state. This is an "internal mandate," meaning it is architectural, not optional. But it speaks to *post-change validity*, not to the indivisibility of the change itself.

**Versions are coherent snapshots.** The historical backtrack guarantee assumes that any previous state can be reconstructed:

> "The file management system we are talking about automatically keeps track of the changes and the pieces, so that when you ask for a given part of a given version at a given time, it comes to your screen." [LM 2/15]

This implies that version states are consistent — you get a well-formed document at every point in history, not a half-applied edit.

### What Nelson Does Not Say

Nelson never uses the terms "atomic," "transaction," "rollback," "all-or-nothing," or any equivalent. He does not address:

- What happens if an insertion fails after writing to I-space but before updating V-space
- Whether a reader can observe a partially-completed operation
- Whether the system must undo partial work on failure
- How concurrent readers (if any) are isolated from in-progress changes

The session model section is equally silent — "Nelson does not specify a session model" and there are no OPEN/CLOSE transaction boundaries in the FEBE protocol.

### The Implicit Assumption

Nelson's specification *implicitly assumes* all-or-nothing semantics through three converging patterns:

1. **Operational descriptions are state-to-state.** Every FEBE command is specified as "this does X" — a complete transition from one document state to another. No command is described as having observable intermediate states.

2. **The canonical order mandate.** If "all changes, once made, left the file remaining in canonical order" [LM 1/34], then no change can leave the file in a non-canonical (partially updated) state. For INSERT — which must extend I-space, update the V→I mapping, and shift subsequent addresses — this practically requires atomicity, since any subset of these steps would leave the structure inconsistent.

3. **The coherent version model.** If every historical state is reconstructible and comparable (via SHOWRELATIONOF2VERSIONS), then every state must be a complete, consistent snapshot. Half-applied insertions would create states that are neither the pre-insertion version nor the post-insertion version.

### Summary

Nelson specifies *what* operations do, not *how they fail*. The answer to "must insertion be all-or-nothing?" from Literary Machines alone is: **Nelson does not say so explicitly, but his specification is only consistent with all-or-nothing semantics.** The canonical order mandate [LM 1/34], the complete-effect operational descriptions [LM 4/66], and the coherent version model [LM 2/15] collectively leave no room for observable partial completion. Atomicity is not stated as a requirement — it is an unavoidable consequence of the requirements that *are* stated.

---

## Question 10 [nelson]

> Does insertion into a shared passage affect every document that includes that passage, or only the document where the insertion was requested?

### Nelson's Answer

## Insertion affects only the targeted document

The answer is unambiguous from Nelson's architecture: **insertion affects only the document where it was requested.** Other documents that include the same passage are unaffected.

### The mechanism

INSERT targets a specific document by ID and modifies only that document's V-space arrangement:

> "This inserts \<text set\> in document \<doc id\> at \<doc vsa\>. The v-stream addresses of any following characters **in the document** are increased by the length of the inserted text." [LM 4/66]

The operation creates new bytes in I-space (permanent storage) and splices them into the named document's V-space (its current arrangement). No other document's V-space is touched.

### Why transclusion doesn't propagate edits

When Document B transcludes a passage from Document A, Document B's V-space contains a mapping to Document A's I-space addresses. These are two independent mappings over shared content:

- Document A's V-space: positions 50–100 → I-addresses X through Y
- Document B's V-space: positions 20–70 → I-addresses X through Y (same content)

Inserting into Document A at V-position 75 creates new I-space content and rewrites Document A's V-space mapping. Document B's mapping remains untouched — it still points to the same I-addresses X through Y.

Nelson states the converse case explicitly for DELETE:

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

If deletion from one document doesn't affect other documents' inclusions, insertion certainly doesn't — INSERT doesn't even modify existing I-space content, it only adds new content and adjusts one document's V-space.

### The deeper principle

This follows directly from the I-space/V-space separation. Content lives permanently in I-space; documents are independent V-space views over that content:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

Each document owns its own V-space arrangement. Editing one arrangement says nothing about any other arrangement, even when they reference the same I-space content. This is what makes the architecture work — ownership means control over *your* document, not over everyone else's view of shared content:

> "Only the owner has a right to withdraw a document or change it." [LM 2/29]

### What about "location-fixed" windows?

Nelson does describe a front-end presentation mode where a window can track changes in the source document:

> "A quotation — an inclusion window — may be fixed to another document in two ways: at a certain point in time, in which case revisions are seen by the user only when he or she asks, 'What has this passage become?' Or second, at a relatively fixed location in the document space, in which case updates are seen automatically." [LM 2/37]

This is a **front-end display behavior**, not a back-end state change. A location-fixed window means the front end re-resolves what is currently at a given location in the source document and presents that to the reader. The including document's back-end state (its V-space mapping) is not modified. The reader *sees* the update; the document's structure is unchanged.

### Summary

| What happens | Affected? |
|---|---|
| Target document's V-space | Yes — new content spliced in, subsequent addresses shift |
| Target document's I-space | Yes — new bytes allocated |
| Other documents' V-space | No — their mappings are independent |
| Other documents' I-space references | No — they still point to the same original bytes |
| Links to the shared passage | No — they point to I-space addresses, which are unchanged |
| Front-end location-fixed windows | Potentially — the front end may re-resolve and show the updated arrangement |

---

## Question 11 [gregory]

> When makegappm shifts existing POOM entries right by the insertion width, does it shift every entry with V-position ≥ the insertion point, or only those entries whose V-position falls between the insertion point and the second blade computed by findaddressofsecondcutforinsert?

### Gregory's Answer

## KB Synthesis

# Answer: Bounded Shifting via Two-Blade Knife

`makegappm` shifts **only** entries whose V-position falls strictly between the insertion point and the second blade. Entries at or beyond the second blade are **not shifted**.

## The Two-Blade Mechanism

[SS-TWO-BLADE-KNIFE] Finding 0054 documents the knife construction:

> INSERT constructs a two-blade knife to partition the POOM tree into shift and no-shift regions. `makegappm()` sets `blade[0]` to the insertion V-position and `blade[1]` to the start of the next subspace, computed by `findaddressofsecondcutforinsert()`. For an insertion at `N.x`, the second blade is always `(N+1).1`.

## Three-Case Classification

[ST-INSERT] Finding 0054 specifies how entries are classified:

> `insertcutsectionnd()` classifies each POOM crum into three cases:
> - **Case 0**: crum is before `blade[0]` — no shift
> - **Case 1**: crum is between `blade[0]` and `blade[1]` — shift right by insertion width
> - **Case 2**: crum is at or beyond `blade[1]` — no shift

The postcondition is bounded, not global:

> `∀ entry ∈ poom(doc) : blade[0] ≤ entry.vpos < blade[1] ⟹ entry.vpos' = entry.vpos + insert_width`

Entries outside this range are unchanged.

## Concrete Example

From [ST-INSERT] Finding 0054:

```
Pre-state:
  Text "ABCDE" at V-positions 1.1-1.5
  Link at V-position 2.1

Operation: INSERT "XY" at V-position 1.3
  Knife blades: [1.3, 2.1]

Post-state:
  Text "ABXYCDE" at V-positions 1.1-1.7 (text shifted within 1.x)
  Link STILL at V-position 2.1 (unchanged — case 2, no shift)
```

The link at V-position 2.1 is exactly at `blade[1]`, so it falls into case 2 and is **not shifted**.

## Subspace Isolation Consequence

This bounded shifting is the structural mechanism that implements subspace isolation. [FC-SUBSPACE] Finding 0054 confirms:

> The invariant `∀ N ∈ {1,2,3}, ∀ op = INSERT(N.x) : shift_region(op) ⊆ [N.1, (N+1).1)` holds for all insertions.

Entries beyond `blade[1] = (N+1).1` remain unshifted, ensuring that INSERT at position `1.x` cannot affect entries in subspace `2.x` or beyond.

**Answer**: Only entries in the bounded region `[blade[0], blade[1])` are shifted. The second blade computed by `findaddressofsecondcutforinsert` acts as an upper boundary that protects all entries at or beyond it from being shifted.

## Code Exploration

Now I have all the code paths. Let me trace the exact behavior:

## Answer

**makegappm shifts ONLY those entries whose V-position falls between the insertion point and the second blade computed by findaddressofsecondcutforinsert.**

It does NOT shift all entries with V-position ≥ insertion point.

## Evidence from Source Code

### 1. makegappm Creates Two Blades [insertnd.c:144-146]

```c
movetumbler (&origin->dsas[V], &knives.blades[0]);
findaddressofsecondcutforinsert(&origin->dsas[V],&knives.blades[1]);
knives.nblades = /*1*/2;
```

The commented-out `/*1*/` shows this was originally a single blade, but was changed to use two blades.

### 2. makegappm Classifies Each Crum [insertnd.c:151-169]

```c
for (ptr = findleftson (father); ptr; ptr = findrightbro (ptr)) {
       i=insertcutsectionnd(ptr,&fgrasp,&knives);
    switch (i) {
      case 0:
      case 2:
        break;
      case -1:      /* THRUME*/
        dump(ptr);
        gerror ("makegappm can't classify crum\n");
        break;
      case 1:/*9-17-87 fix */
        tumbleradd(&ptr->cdsp.dsas[V],&width->dsas[V],&ptr->cdsp.dsas[V]);
        /*tumbleradd(&width->dsas[V],&ptr->cdsp.dsas[V],&ptr->cdsp.dsas[V]);*/
        ivemodified (ptr);
        break;
      default:
        gerror ("unexpected cutsection\n");
    }
}
```

Only `case 1` shifts the crum. Cases 0 and 2 do nothing.

### 3. insertcutsectionnd Returns 1 for Crums Between the Two Blades [edit.c:207-233]

```c
INT insertcutsectionnd(typecorecrum *ptr, typewid *offset, typeknives *knives)
{
  INT i, cmp;		       /*hacked from delete*/

    /*for (i = knives->nblades-1; i >= 0; --i){*/
    if (knives->nblades == 2) {
          i = 1;
          cmp = whereoncrum(ptr, offset, &knives->blades[i], knives->dimension);
          if (/*FALSE&&*/cmp == THRUME) {
            dumpwid(&ptr->cwid.dsas[i],ptr->cenftype);
               return (-1);
          } else if (cmp <= ONMYLEFTBORDER)/* compare last to first */{
               return (2);
          }
    }
          i = 0;
          cmp = whereoncrum(ptr, offset, &knives->blades[i], knives->dimension);
          if (cmp == THRUME) {
               dumpwid(&ptr->cwid.dsas[i],ptr->cenftype);
               return (-1);
          } else if (cmp <= ONMYLEFTBORDER)/* compare last to first */{
               return (1);
          }
    
       /* }*/
    return (0);
}   
```

The logic checks blade[1] first, then blade[0]:
- If blade[1] is at or left of the crum (crum is ≥ blade[1]): return **2** (no shift)
- Else if blade[0] is at or left of the crum (crum is ≥ blade[0]): return **1** (shift)
- Else (crum is < blade[0]): return **0** (no shift)

### 4. whereoncrum Compares Address to Crum Boundaries [retrie.c:356-372]

```c
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
    return(THRUME);
}else if (cmp == EQUAL){
    return (ONMYRIGHTBORDER);
}else{
    return(TOMYRIGHT);
}
```

`whereoncrum` returns:
- TOMYLEFT or ONMYLEFTBORDER when address ≤ crum's left border
- THRUME when address is inside the crum
- ONMYRIGHTBORDER or TOMYRIGHT when address ≥ crum's right border

### 5. The Second Blade [insertnd.c:174-183]

```c
int findaddressofsecondcutforinsert(tumbler *position, tumbler *secondcut)
{    /*needs this to give it a place to find intersectionof for text is 2.1*/
  tumbler zero, intpart;

       tumblerclear (&zero);
       tumblerincrement (position, -1, 1, secondcut);
       beheadtumbler (position, &intpart);
       tumblerincrement(secondcut,0,-tumblerintdiff(&intpart,&zero),secondcut);
       tumblerincrement (secondcut, 1, 1, secondcut);
}
```

This computes a second cut point based on the insertion position, defining the right boundary of the shift region.

## Summary

The three-region classification is:
- **Region 0** (V < blade[0]): Entries entirely before the insertion point → **no shift**
- **Region 1** (blade[0] ≤ V < blade[1]): Entries between insertion point and second cut → **shift by width**
- **Region 2** (V ≥ blade[1]): Entries at or after the second cut → **no shift**

The comment `/*9-17-87 fix */` at [insertnd.c:161] suggests this two-blade approach was a bug fix from September 17, 1987, replacing an earlier implementation that may have shifted all entries ≥ the insertion point.

---

## Question 12 [gregory]

> If a document contains text at V:1.1-1.5 and a link at V:0.2.1, and INSERT places new text at V:1.3, does the link entry at V:0.2.1 remain byte-identical in the POOM — same V-displacement, same I-displacement, same widths — with zero modification to any field?

### Gregory's Answer

## KB Synthesis

Looking at the internal POOM representation, **yes, the link entry remains byte-identical with zero modification to any field**.

Here's why:

## Subspace Location

First, clarifying notation: Links are stored internally at **V:2.x** positions, not V:0.2.x [SS-DUAL-ENFILADE, Finding 0038]. The `0.x` notation appears only in normalized output from `retrievedocvspanset`. So the link entry in your scenario is at internal position **V:2.1**.

## The Two-Blade Knife Mechanism

When INSERT operates at V:1.3, it constructs a two-blade knife [SS-TWO-BLADE-KNIFE, Finding 0054]:
- `blade[0] = 1.3` (insertion point)  
- `blade[1] = 2.1` (next subspace boundary, computed as `(1+1).1`)

The knife defines a **half-open interval** `[1.3, 2.1)` as the shift region [ST-INSERT, Finding 0054].

## Entry Classification

The POOM traversal classifies each entry using `whereoncrum` against the blades [FC-SUBSPACE, Finding 0054]:
- Entries with `vpos < 1.3`: case 0 (before insertion, no shift)
- Entries with `1.3 ≤ vpos < 2.1`: case 1 (shifted right by insertion width)
- Entries with `vpos ≥ 2.1`: case 2 (beyond second blade, **no shift**)

The link entry at V:2.1 falls into **case 2** because `2.1 ≥ blade[1]`.

## Frame Condition

From [ST-INSERT, Finding 0054]:
> "The postcondition for INSERT's V-position shifting is bounded, not global: `∀ entry ∈ poom(doc) : blade[0] ≤ entry.vpos < blade[1] ⟹ entry.vpos' = entry.vpos + insert_width`. **Entries outside this range are unchanged.**"

The link at V:2.1 is outside the range `[1.3, 2.1)`, so it is **unchanged**.

## Additional Confirmation

The subspace isolation property confirms this [FC-SUBSPACE, Finding 0067]:
> "INSERT at `1.x` does not affect link entries at `2.x`... Two distinct mechanisms enforce this: **INSERT** uses a deliberate two-blade knife with `blade[1]` at the next subspace boundary."

And [INV-SUBSPACE-CONVENTION, Finding 0054]:
> "INSERT at `1.x` → blades `[1.x, 2.1)` → shifts only text"

## Conclusion

The link entry's **V-displacement, I-displacement, and both width fields remain byte-identical**. The structural guard prevents any modification—not just to the V-position, but to the entire POOM crum structure for that link entry.

## Code Exploration

Based on the existing findings and source code analysis, I can provide a definitive answer:

## Answer: YES - The Link Entry Remains Byte-Identical

When INSERT places text at V:1.3, the link entry at V:0.2.1 remains completely unmodified—same V-displacement, same I-displacement, same widths. Zero bytes change.

## Code Analysis

### The Two-Blade Knife Mechanism

When `doinsert` runs for V:1.3, it calls `insertpm` → `insertnd` → `makegappm` [`insertnd.c:124-172`]:

```c
movetumbler (&origin->dsas[V], &knives.blades[0]);                     // blade[0] = 1.3
findaddressofsecondcutforinsert(&origin->dsas[V], &knives.blades[1]);  // blade[1] = 2.1
knives.nblades = 2;
knives.dimension = V;
```

**blade[0] = 1.3** (insertion point)  
**blade[1] = 2.1** (start of next subspace)

### Classification of the V:0.2.1 Crum

The `insertcutsectionnd` function [`edit.c:207-233`] classifies each POOM crum:

```c
INT insertcutsectionnd(typecorecrum *ptr, typewid *offset, typeknives *knives)
{
    if (knives->nblades == 2) {
        i = 1;
        cmp = whereoncrum(ptr, offset, &knives->blades[1], knives->dimension);
        if (cmp <= ONMYLEFTBORDER) {
            return (2);    // Case 2: At or beyond second blade → NO SHIFT
        }
    }
    i = 0;
    cmp = whereoncrum(ptr, offset, &knives->blades[0], knives->dimension);
    if (cmp <= ONMYLEFTBORDER) {
        return (1);    // Case 1: At or beyond first blade → SHIFT RIGHT
    }
    return (0);    // Case 0: Before first blade → NO SHIFT
}
```

For the link crum at V:0.2.1 with blades [1.3, 2.1]:

| Check | Tumbler Comparison | Result |
|-------|-------------------|--------|
| blade[1]=2.1 vs V:0.2.1 | 0.2.1 < 2.1 → blade is TOMYRIGHT | Fall through |
| blade[0]=1.3 vs V:0.2.1 | 0.2.1 < 1.3 → blade is TOMYRIGHT | Fall through |
| Final classification | - | **Case 0** |

**Case 0** means the crum is entirely before the insertion point.

### What Happens to Case 0 Crums

Back in `makegappm` [`insertnd.c:150-169`]:

```c
for (ptr = findleftson (father); ptr; ptr = findrightbro (ptr)) {
    i = insertcutsectionnd(ptr, &fgrasp, &knives);
    switch (i) {
        case 0:
        case 2:
            break;    // <-- NO ACTION: crum left untouched
        case 1:
            tumbleradd(&ptr->cdsp.dsas[V], &width->dsas[V], &ptr->cdsp.dsas[V]);
            ivemodified(ptr);
            break;
    }
}
```

**Case 0 → `break;` with no preceding code = zero modifications.**

The crum struct remains byte-identical:
- `cdsp.dsas[V]` (V-displacement): unchanged
- `cdsp.dsas[I]` (I-displacement): unchanged
- `cwid.dsas[V]` (V-width): unchanged
- `cwid.dsas[I]` (I-width): unchanged
- `c2dinfo` (metadata): unchanged

## Empirical Evidence

**Golden test:** `golden/subspace/insert_text_check_both_link_positions.json` (Finding 0054)

Setup:
- Text at V:1.1-1.5
- Link at V:2.1

Action: INSERT at V:1.3

Result:
- Link **still at V:2.1** after insert
- FINDLINKS still returns the link
- FOLLOWLINK still resolves

The same mechanism applies to V:0.2.1 (which is even further from the insertion point).

## The General Principle

INSERT at V:1.3 only shifts crums in the range **[1.3, 2.1)**. Any crum outside this range is left byte-identical:

| Crum V-position | Relationship to [1.3, 2.1) | Case | Modified? |
|----------------|---------------------------|------|-----------|
| V:0.2.1 | Before range (0.2.1 < 1.3) | 0 | **NO** |
| V:1.1 | Before range (1.1 < 1.3) | 0 | **NO** |
| V:1.3 | On boundary | 1 | YES (shifts right) |
| V:1.5 | Inside range | 1 | YES (shifts right) |
| V:2.1 | On second boundary | 2 | **NO** |
| V:2.5 | Beyond range (2.5 ≥ 2.1) | 2 | **NO** |

## Why This Matters

This is the **subspace isolation** mechanism. The second blade (computed by `findaddressofsecondcutforinsert`) marks the start of the next tumbler subspace (2.1 = start of "2.x" subspace). This ensures:

1. INSERT in text subspace (1.x) doesn't shift links (2.x)
2. INSERT before text subspace (0.x) is also isolated
3. Each subspace is a self-contained shift domain

## References

- [`insertnd.c:144-146`] — Two-blade knife construction
- [`insertnd.c:174-183`] — `findaddressofsecondcutforinsert` computes 2.1 from 1.3
- [`edit.c:207-233`] — `insertcutsectionnd` classification logic
- [`insertnd.c:150-169`] — Case 0 → no action
- **Finding 0054** — INSERT Does Not Shift Link Subspace
- **Finding 0067** — Frame Axiom F0 Confirmed

**Conclusion:** The link entry at V:0.2.1 is guaranteed by the implementation to remain byte-identical. No field is read, no field is written. The crum exists on disk/in-memory in exactly the same state before and after the INSERT at V:1.3.

---

## Question 13 [gregory]

> When two successive INSERTs target the same V-position (e.g., INSERT "A" at V:1.1 then INSERT "B" at V:1.1), does isanextensionnd ever coalesce these into a single POOM crum, or does same-position insertion always create a separate crum because the new I-address is not adjacent to the shifted entry?

### Gregory's Answer

## KB Synthesis

Looking at this question, I need to trace through the INSERT mechanics for same-position operations, particularly focusing on the extension vs. split decision.

## The Short Answer

**No, successive inserts at the same V-position do NOT coalesce.** Each insert creates a new separate POOM crum. The extension mechanism (`isanextensionnd`) only works for insertions at the **right boundary** of an existing crum (ONMYRIGHTBORDER), not at the left boundary.

## The Mechanics

### First Insert: INSERT "A" at V:1.1
Per `[ST-INSERT]` and `[INV-MONOTONIC]`:
- Allocates I-address α
- Creates POOM crum: V-span [1.1, 1.2) → I-span [α, α+1)
- Crum count: 1

### Second Insert: INSERT "B" at V:1.1  
Per `[ST-INSERT]` from Finding 0027:
> Multiple inserts target the same V-position, each new insertion appears **before** existing content at that position. This produces LIFO (last-in-first-out) ordering.

Here's what happens:

**1. Position Classification**

Per `[SS-WHEREONCRUM]`:
- V-position 1.1 is at the **left boundary** (grasp) of crum_A
- `whereoncrum(crum_A, 1.1)` returns `ONMYLEFTBORDER` (-1)

**2. Extension Early-Exit Check**

Per `[ST-INSERT]` from Finding 0062:
> `makegappm()` performs an early-exit check before constructing the two-blade knife: if the insertion point equals or exceeds the crum's reach, the knife cut is SKIPPED entirely. The condition `tumblercmp(&origin->dsas[V], &reach.dsas[V]) != LESS` evaluates to TRUE when origin >= reach.

For our case:
- origin = 1.1, reach = 1.2
- 1.1 < 1.2 → early exit condition is FALSE
- Knife construction proceeds, shift occurs

**3. The Shift Phase**

Per `[ST-INSERT]` from Finding 0054:
- blade[0] = 1.1 (insertion point)
- blade[1] = 2.1 (next subspace boundary)
- crum_A at [1.1, 1.2) is classified as case 1 (within shift region)
- crum_A is shifted: [1.1, 1.2) → [1.2, 1.3)

**4. The New Crum Creation**

- Allocates I-address β (= α+1 by `[INV-MONOTONIC]`)
- Creates crum_B: V-span [1.1, 1.2) → I-span [α+1, α+2)
- Crum count: 2

## Why Extension Doesn't Apply

The extension mechanism from `[ST-INSERT]` Finding 0062 states:
> When an INSERT at position v+1 encounters a crum whose reach equals v+1 (ONMYRIGHTBORDER), the system performs rightward extension instead of splitting.

The key constraint is **ONMYRIGHTBORDER** — extension only works when:
1. Inserting at the RIGHT edge of an existing crum (position == reach)
2. The early-exit condition is met (no shift occurs)
3. `isanextensionnd()` verifies I-address contiguity and same homedoc

For same-position insertion:
- We're at ONMYLEFTBORDER (position == grasp)
- The early-exit is NOT triggered
- Shift occurs before new content placement
- Extension code path is never reached

## I-Address Contiguity Doesn't Help

After shifting, we have an interesting situation:
- crum_A: V[1.2, 1.3) → I[α, α+1)
- crum_B: V[1.1, 1.2) → I[α+1, α+2)

The crums ARE I-address contiguous (β = α+1), but they're contiguous in the wrong direction — crum_B has later I-addresses but earlier V-addresses. The `isanextensionnd` check looks for `new.I-origin == existing.I-reach`, which would match here, but this check is never reached because the extension code path only activates for ONMYRIGHTBORDER cases where no shift occurs.

## Consistency Check

This is consistent with `[INV-CRUM-BOUND]` from Finding 0062:
> Continuous interior typing at a single cursor position costs exactly +2 crums for the first character, then +0 for every subsequent character.

That describes **advancing** cursor typing (each character at v+1, v+2, v+3...), not same-position typing. The +0 cost comes from ONMYRIGHTBORDER extension. Same-position insertion would have a +2 cost for EACH character since each creates a new crum.

## Conclusion

Successive inserts at the same V-position each produce a separate POOM crum. The system's extension optimization is directional — it works for rightward growth (advancing cursor) but not for leftward insertion (same position with shift). This is why same-position insertion produces LIFO ordering with distinct crums rather than a single coalesced crum.

## Code Exploration

Based on my thorough examination of the source code, I can now provide a definitive answer to your question.

---

## Answer: Successive INSERTs at the Same V-Position Do NOT Coalesce

When two successive INSERTs target the same V-position (e.g., INSERT "A" at V:1.1, then INSERT "B" at V:1.1), `isanextensionnd` **cannot coalesce** them into a single POOM crum. They always create separate crums because the V-dimension becomes non-adjacent after the first insertion, even though the I-addresses are contiguous.

---

## Detailed Execution Trace

### First INSERT "A" at V:1.1

1. **I-address allocation** [granf2.c:168-169]:
   ```c
   else if (hintptr->atomtype == TEXTATOM) {
       tumblerincrement (&lowerbound, 0, 1, isaptr);
   }
   ```
   Allocates I:1.1.0.1.1.1 (first text in document)

2. **POOM insertion** [insertnd.c:242-275]:
   Creates crum: `cdsp=(V:1.1, I:1.1.0.1.1.1)`, `cwid=(V:1, I:1)`
   - Reach = cdsp + cwid = (V:2.1, I:1.1.0.1.1.2)

### Second INSERT "B" at V:1.1

1. **makegappm shifts V-positions** [insertnd.c:124-172]:
   ```c
   findaddressofsecondcutforinsert(&origin->dsas[V],&knives.blades[1]);
   knives.nblades = 2;
   knives.dimension = V;
   makecutsnd (fullcrumptr, &knives);
   ```
   Creates two-blade knife at [0]=V:1.1, [1]=V:2.1 (next subspace boundary)

2. **insertcutsectionnd classifies the first crum** [edit.c:207-233]:
   ```c
   cmp = whereoncrum(ptr, offset, &knives.blades[i], knives->dimension);
   if (cmp <= ONMYLEFTBORDER) {
       return (1);  // Case 1: shift required
   }
   ```
   The "A" crum at V:1.1 is classified as case 1

3. **V-position shifted** [insertnd.c:161-165]:
   ```c
   case 1:/*9-17-87 fix */
       tumbleradd(&ptr->cdsp.dsas[V],&width->dsas[V],&ptr->cdsp.dsas[V]);
       ivemodified (ptr);
       break;
   ```
   First crum's V-position: cdsp.V: 1.1 → 2.1

4. **I-address allocation for "B"** [granf2.c:168-169]:
   Allocates I:1.1.0.1.1.2 (increments previous highest by 1)

5. **Check for coalescing** [insertnd.c:242-275]:
   ```c
   for (ptr = findleftson (father); ptr; ptr = findrightbro (ptr)) {
       if (isanextensionnd ((typecbc*)ptr, grasp, origin, infoptr)) {
           dspadd (&ptr->cwid, width, &ptr->cwid, (INT)father->cenftype);
           // Would coalesce here if TRUE
       }
   }
   ```

6. **isanextensionnd evaluation** [insertnd.c:301-309]:
   ```c
   bool isanextensionnd(typecbc *ptr, typedsp *offsetptr, typedsp *originptr, type2dbottomcruminfo *infoptr)
   {
       typedsp grasp, reach;
       if (!tumblereq (&infoptr->homedoc, &((type2dcbc *)ptr)->c2dinfo.homedoc))
           return (FALSE);
       prologuend ((typecorecrum*)ptr, offsetptr, &grasp, &reach);
       return (lockeq (reach.dsas, originptr->dsas, (unsigned)dspsize(ptr->cenftype)));
   }
   ```

   Checking first crum against new insertion:
   - First crum after shift: cdsp=(V:2.1, I:1.1.0.1.1.1), cwid=(V:1, I:1)
   - reach = (V:3.1, I:1.1.0.1.1.2)
   - origin of "B" = (V:1.1, I:1.1.0.1.1.2)
   
   **V-dimension: 3.1 ≠ 1.1** ❌
   I-dimension: 1.1.0.1.1.2 = 1.1.0.1.1.2 ✓

   Since `lockeq` requires **all dimensions** to match [insertnd.c:308], it returns **FALSE**

7. **Creates new crum** [insertnd.c:260-274]:
   ```c
   new = createcrum (0, (INT)father->cenftype);
   reserve (new);
   adopt (new, SON, (typecorecrum*)father);
   ```
   Second crum: `cdsp=(V:1.1, I:1.1.0.1.1.2)`, `cwid=(V:1, I:1)`

---

## Why This Happens

The **two-phase** nature of POOM insertion prevents coalescing:

1. **Phase 1: makegappm** [insertnd.c:54] — Creates space in V-dimension
   - Shifts all content at or after the insertion point
   - Breaks V-adjacency even for content originally at the same position

2. **Phase 2: doinsertnd** [insertnd.c:57] — Inserts new content
   - Checks for coalescing via `isanextensionnd`
   - But V-dimension is already non-adjacent due to Phase 1

The I-addresses ARE adjacent (1.1.0.1.1.1 + width 1 = 1.1.0.1.1.2), but this alone is insufficient. `isanextensionnd` requires **both V and I dimensions** to be adjacent [insertnd.c:308].

---

## Architectural Significance

This behavior reveals a fundamental property of the POOM layer:

**V-position governs structure, I-addresses provide identity**

- Same-position insertions create separate structural entries (crums)
- Even when content is allocated contiguously in I-space
- The V→I mapping layer maintains separate entries for each insertion
- This preserves the semantic that "INSERT at position N" is a distinct operation each time

This is consistent with Finding 0027 (insertion order semantics) and Finding 0030 (V-space shifts, I-space persists).

---

## References

- `insertnd.c:124-172` — makegappm: V-position shifting mechanism
- `insertnd.c:242-275` — insertcbcnd: coalescing check loop
- `insertnd.c:301-309` — isanextensionnd: adjacency test for both dimensions
- `edit.c:207-233` — insertcutsectionnd: two-blade classification
- `granf2.c:158-181` — findisatoinsertmolecule: I-address allocation
- Finding 0027 — Insertion order semantics (prepend behavior)
- Finding 0030 — INSERT V-space/I-space mapping (shifts vs. identity)
- Finding 0041 — Enfilade insertion order dependency (tree structure)

---

## Question 14 [gregory]

> Does INSERT guarantee that the DOCISPAN entry written to the spanfilade records exactly the contiguous I-address range allocated for this insertion, and never a wider or narrower span — even when isanextensionnd coalesces the new content with an adjacent existing POOM entry?

### Gregory's Answer

## KB Synthesis

# Answer: YES

INSERT guarantees that the DOCISPAN entry records exactly the contiguous I-address range allocated for this insertion, unaffected by POOM-level coalescing.

## Evidence Chain

**[ST-INSERT]** (Finding 0036) establishes the call sequence:
```
doinsert → inserttextingranf → docopy → insertpm + insertspanf(DOCISPAN)
```

The critical insight is that **the same `ispanset` flows to both operations**:
1. `inserttextingranf()` allocates fresh I-addresses and returns them as an `ispanset`
2. `docopy()` receives this `ispanset` and passes it to:
   - `insertpm()` — updates POOM (V-to-I mappings)
   - `insertspanf(..., DOCISPAN)` — indexes in spanfilade

## Coalescing vs. Allocation

**[ST-INSERT]** (Finding 0062) documents that `isanextensionnd()` enables POOM crum coalescing:
> "When both hold, the existing crum's width is extended in place — no new crum is allocated."

This coalescing is a **POOM optimization** that reduces V-space tree structure overhead. It operates on POOM crums (V-to-I mapping nodes), not on I-address ranges.

**[INV-MONOTONIC]** (Finding 0033) confirms I-address allocation is independent:
> "I-address allocation is strictly monotonically increasing within a document. Each new text insert receives an I-address exactly 1 greater than the previous allocation."

The fresh I-addresses from `inserttextingranf` represent the allocation for THIS insert operation — they are disjoint from any previous allocation.

## Spanfilade Writes Exactly What Was Allocated

**[SS-DOCISPAN]** (Finding 0047) specifies DOCISPAN granularity:
> "When `insertspanf` is called, it iterates over the `ispanset` linked list and makes one `insertnd` call per `typeispan` struct."

The `ispanset` passed to `insertspanf` is the return value from `inserttextingranf` — the freshly allocated range. The POOM coalescing that happens in `insertpm` does not mutate this `ispanset`.

## Architectural Separation

**[FC-CONTENT-SPANF-ISOLATION]** (Finding 0036) notes:
> "INSERT writes to both granf (new content) and spanf (DOCISPAN index)."

The operations are separate:
- **Granf layer**: `inserttextingranf` allocates fresh I-addresses
- **POOM layer**: `insertpm` creates/extends V-to-I mappings (coalescing may occur here)
- **Spanf layer**: `insertspanf` indexes the allocated I-addresses (receives the same `ispanset` from step 1)

The POOM is a derived view over the granf content; changes to POOM structure do not retroactively change the granf allocation or its spanf indexing.

## Conclusion

The DOCISPAN entry written by INSERT records precisely the I-address range returned by `inserttextingranf`, which is the allocation for this specific INSERT operation. POOM-level coalescing via `isanextensionnd` affects only V-space structure (crum count), not I-space allocation or spanfilade indexing.

## Code Exploration

Perfect! Now I have traced the complete execution path. Let me provide my answer with full code citations.

---

# Answer

**Yes, INSERT guarantees that the DOCISPAN entry records exactly the contiguous I-address range allocated for this insertion, never a wider or narrower span—even when `isanextensionnd` coalesces the new content with an adjacent existing POOM entry.**

## Execution Flow

### 1. I-Address Allocation Happens First

**[do1.c:118]** - `doinsert()` calls `inserttextingranf()` to allocate I-addresses:
```c
ret = (inserttextingranf(taskptr, granf, &hint, textset, &ispanset)
    && docopy (taskptr, docisaptr, vsaptr, ispanset)
```

**[granf1.c:44-47]** - This is a wrapper for `inserttextgr()`:
```c
bool inserttextingranf(typetask *taskptr, typegranf granfptr, typehint *hintptr, typetextset textset, typeispanset *ispansetptr)
{  bool inserttextgr();
     return (inserttextgr (taskptr, granfptr, hintptr, textset, ispansetptr));
}
```

**[granf2.c:92-107]** - `inserttextgr()` allocates a contiguous I-address range:
```c
if (!findisatoinsertgr ((typecuc*)fullcrumptr, hintptr, &lsa))
    return (FALSE);
movetumbler (&lsa, &spanorigin);  // Save starting address

for (; textset; textset = textset->next) {
    locinfo.infotype = GRANTEXT;
    locinfo.granstuff.textstuff.textlength = textset->length;
    movmem(textset->string,locinfo.granstuff.textstuff.textstring, locinfo.granstuff.textstuff.textlength);
    insertseq ((typecuc*)fullcrumptr, &lsa, &locinfo);
    tumblerincrement (&lsa, 0, textset->length, &lsa);  // Advance by length
}

// Create ispan covering [spanorigin, lsa)
ispanptr = (typeispan *) taskalloc (taskptr, sizeof(typeispan));
ispanptr->itemid = ISPANID;
ispanptr->next = NULL;
movetumbler (&spanorigin, &ispanptr->stream);  // Start = saved start
tumblersub (&lsa, &spanorigin, &ispanptr->width);  // Width = final - start
```

**Key insight**: The ispan is created with `stream = spanorigin` (the starting address found before any insertions) and `width = lsa - spanorigin` (the total length of all text inserted). This range is determined before `docopy()` is called.

### 2. The Same Ispan Goes to Both POOM and Spanfilade

**[do1.c:119]** - The ispan returned from step 1 is passed unchanged to `docopy()`:
```c
&& docopy (taskptr, docisaptr, vsaptr, ispanset)
```

**[do1.c:60-62]** - `docopy()` passes the **same** ispan to both operations:
```c
&& insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)
&&  insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN)
```

### 3. Spanfilade Records the Ispan Directly

**[spanf1.c:26-29]** - `insertspanf()` directly copies the ispan's range:
```c
if (((typeitemheader *)sporglset)->itemid == ISPANID) {
    movetumbler (&((typeispan *)sporglset)->stream, &lstream);
    movetumbler (&((typeispan *)sporglset)->width, &lwidth);
    movetumbler (isaptr,&linfo.homedoc);
}
```

**[spanf1.c:49-51]** - This is inserted into the spanfilade:
```c
movetumbler (&lstream, &crumorigin.dsas[SPANRANGE]);
movetumbler (&lwidth, &crumwidth.dsas[SPANRANGE]);
insertnd(taskptr,(typecuc*)spanfptr,&crumorigin,&crumwidth,&linfo,SPANRANGE);
```

## Content Coalescing Does Not Affect the Recorded Range

### Granfilade Coalescing

**[insert.c:34-42]** - `insertseq()` can coalesce text into existing granfilade entries:
```c
if (			     /* crum can be extended */
   info->infotype == GRANTEXT
&& ptr->cinfo.infotype == GRANTEXT
&& ptr->cinfo.granstuff.textstuff.textlength < GRANTEXTLENGTH) {
    if (!fillupcbcseq (ptr, &nextaddress, info)) {
        ivemodified ((typecorecrum*)ptr);
        return(0);
    }
}
```

**But**: This happens **after** `inserttextgr()` has already saved `spanorigin` and will compute the final ispan width from the incremented `lsa` value. The ispan range is unaffected.

### POOM Coalescing

**[insertnd.c:250-257]** - `insertcbcnd()` can extend existing POOM entries:
```c
for (ptr = findleftson (father); ptr; ptr = findrightbro (ptr)) {
    if (isanextensionnd ((typecbc*)ptr, grasp, origin, infoptr)) {
        dspadd (&ptr->cwid, width, &ptr->cwid, (INT)father->cenftype);
        ivemodified (ptr);
        setwispupwards (father,1);
        // ... return without creating new crum
    }
}
```

**[insertnd.c:301-309]** - `isanextensionnd()` checks if V-addresses are adjacent:
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

**But**: This coalescing happens in the **V-dimension** (V-addresses), not the I-dimension. The I-address range came from the ispan that was already determined by `inserttextgr()`. The POOM entry uses the I-addresses from the ispan, and even if multiple V-addresses map to a coalesced POOM entry, each INSERT still records its own distinct I-address range in the DOCISPAN.

## Conclusion

The DOCISPAN entry recorded in the spanfilade is **exactly** the I-address range `[start, start+length)` allocated by `inserttextgr()` for this specific INSERT operation. This is true regardless of:

1. Whether `fillupcbcseq()` [insert.c:75-103] extends an existing granfilade text crum
2. Whether `isanextensionnd()` [insertnd.c:301-309] coalesces the POOM entry with an adjacent entry

The ispan is created **before** any POOM insertion occurs [granf2.c:102-107], passed unchanged through `docopy()` [do1.c:60,62], and directly copied into the spanfilade [spanf1.c:27-28,49-51]. There is no code path that modifies the ispan's range after allocation.

---

## Question 15 [gregory]

> When INSERT allocates fresh I-addresses via findisatoinsertmolecule, and the document previously had a CREATELINK that advanced the allocation counter past the text range, does the new text I-address start immediately after the link orgl's I-address, or does it resume within the text subspace (.0.1.x) specifically?

### Gregory's Answer

## KB Synthesis

Looking at the I-address allocation mechanism when CREATELINK and INSERT interleave, the answer comes directly from [INT-LINK-INSERT] Finding 0063 and [INV-MONOTONIC] Findings 0063 & 0077:

**The new text I-address starts immediately after the link orgl's I-address** — it does NOT resume within a separate text subspace.

## Key Evidence

### Shared Allocation Sequence
[INT-LINK-INSERT] states explicitly:
> "text characters and link orgls compete for the same monotonic sequence"

[INV-MONOTONIC] Finding 0063 formalizes this:
> "The formal model must account for a shared I-address allocator across all granfilade entities. The allocation function is `next_iaddr(granf) = max_iaddr(granf) + 1` regardless of entity type — text characters and link orgls compete for the same monotonic sequence."

### The Mechanism
Both `findisatoinsertmolecule` (for text) and `findisatoinsertnonmolecule` (for link orgls) ultimately call `findpreviousisagr`, which searches the **same granfilade tree** [INT-LINK-INSERT]:
> "`granf2.c:255-278` — `findpreviousisagr` — tree traversal returns the highest I-address **regardless of entity type**"

### Concrete Example
[INT-LINK-INSERT] Finding 0063 provides the observable behavior:
```
INSERT "ABC" → I-addresses 1.1, 1.2, 1.3
CREATELINK   → link orgl at ~2.0
INSERT "DEF" → allocates at 2.1, 2.2, 2.3
```

The gap from 1.3 to 2.1 demonstrates that the second INSERT continues from where the link orgl left off, not from a separate text-only allocation pool.

### Contrast with Document Addresses
[INV-MONOTONIC] Finding 0077 clarifies that while **document addresses** (from CREATENEWVERSION) allocate in a separate range via `findisatoinsertnonmolecule`, **content entities** (text atoms AND link orgls) share the same allocation sequence:
> "CREATENEWVERSION does NOT break I-address contiguity for subsequent text INSERTs. Unlike CREATELINK (Finding 0063), which allocates a link orgl in the content region of the granfilade and disrupts text I-address contiguity, VERSION allocates only a document address in a separate tumbler range."

## Answer

The new text I-address continues **immediately after the link orgl's I-address** in a single monotonically increasing sequence. There is no subspace-specific allocation that would make text "jump back" to a text-only range. The granfilade uses stateless query-and-increment (`findpreviousisagr` + 1) on a unified tree, causing CREATELINK to advance the allocation counter for all subsequent content allocations, whether text or links.

## Code Exploration

Based on my code analysis, I can now answer your question. Let me provide the complete answer with code citations.

## Answer: Text Resumes in the Text Subspace Specifically

When INSERT allocates fresh I-addresses after a CREATELINK, **the new text I-address resumes within the text subspace (.0.0.1.x) specifically**, NOT immediately after the link orgl's I-address.

## Code Evidence

### 1. Separate Subspace Allocation

**[backend/xanadu.h:145-146]**
```c
#define TEXTATOM  1
#define LINKATOM  2
```

**[backend/granf2.c:158-181]** The `findisatoinsertmolecule` function allocates text and links in separate subspaces:

```c
static int findisatoinsertmolecule(typecuc *fullcrumptr, typehint *hintptr, typeisa *isaptr)
{
  typeisa upperbound, lowerbound;

	tumblerincrement (&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound);
	clear (&lowerbound, sizeof(lowerbound));
	findpreviousisagr ((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);
```

**Line 162:** For `TEXTATOM` (atomtype = 1), upperbound becomes `hintisa.0.0.(1+1)` = **`docisa.0.0.2`**

For `LINKATOM` (atomtype = 2), upperbound becomes `hintisa.0.0.(2+1)` = **`docisa.0.0.3`**

This establishes:
- **Text subspace:** `docisa.0.0.1.x`  
- **Link subspace:** `docisa.0.0.2.x`

### 2. Bounded Search with findpreviousisagr

**[backend/granf2.c:164]** 
```c
findpreviousisagr ((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);
```

**[backend/granf2.c:255-278]** The `findpreviousisagr` function searches for the highest I-address **strictly less than upperbound**:

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

### 3. The Key Isolation

When allocating text with upperbound = `docisa.0.0.2`:
- `findpreviousisagr` finds the highest address < `docisa.0.0.2`
- Link addresses at `docisa.0.0.2.0.1` (or any `.0.0.2.x`) are **>= `docisa.0.0.2`**
- Therefore, links are **NOT found** during text allocation searches
- Text allocation resumes from the last text address (e.g., `docisa.0.0.1.0.50`)

**[backend/granf2.c:168-169]** For subsequent text after initial allocation:
```c
} else if (hintptr->atomtype == TEXTATOM) {
	tumblerincrement (&lowerbound, 0, 1, isaptr);
```

The next text address is simply `lowerbound + 1`, where `lowerbound` is the last text address found (which excludes any link addresses because they're in a different subspace).

## Execution Trace Example

**Scenario:** Text → Link → Text

1. **First text insert:**
   - upperbound = `docisa.0.0.2`
   - findpreviousisagr finds: `docisa` (the document orgl itself)
   - Allocated at: **`docisa.0.0.1.0.1`**

2. **More text inserts:**
   - Last text at: **`docisa.0.0.1.0.50`**

3. **Create link:**
   - upperbound = `docisa.0.0.3`
   - findpreviousisagr finds: `docisa.0.0.1.0.50` (the last text, which is < .0.0.3)
   - Line 171-173: Link allocated at: **`docisa.0.0.2.0.1`**

4. **Next text insert:**
   - upperbound = `docisa.0.0.2`
   - findpreviousisagr searches for highest < `docisa.0.0.2`
   - Link at `docisa.0.0.2.0.1` is >= upperbound, so **NOT found**
   - Finds last text: `docisa.0.0.1.0.50`
   - Line 169: Next text allocated at: **`docisa.0.0.1.0.51`**

## Conclusion

The allocation counter is **not globally shared**. Text and links maintain separate subspaces through the upperbound mechanism. The link's I-address allocation does not advance the text allocation counter because `findpreviousisagr`'s bounded search ensures that each atom type only sees allocations within its own subspace range.

**Answer:** Text resumes within the text subspace `.0.0.1.x` specifically, continuing from the last text I-address as if the link allocation never happened.

---

## Question 16 [gregory]

> If INSERT is called with a V-position beyond the current document extent (e.g., the document spans V:1.1-1.5 and INSERT targets V:1.100), does the backend create the POOM entry at V:1.100 with a gap, or does it clamp or reject the position?

### Gregory's Answer

## KB Synthesis

Looking at the INSERT preconditions and behavior documented in the knowledge base:

**The backend creates a POOM entry at V:1.100, leaving a gap from V:1.5 to V:1.100 where no V→I mappings exist.**

Here's why:

## No Bounds Checking

`insertpm()` performs only two V-position validation checks [PRE-INSERT Finding 0049]:
1. Reject zero tumbler (lines 86-90)
2. Reject negative tumbler (lines 93-98)

Critically, **there is no check that the insertion position falls within or near the current document extent**. The `acceptablevsa()` function that appears in the precondition chain unconditionally returns `TRUE` [PRE-INSERT Finding 0049, Finding 0011].

## TOMYRIGHT Classification

When INSERT encounters a position beyond existing content, `whereoncrum()` classifies it as TOMYRIGHT (value 2) [SS-WHEREONCRUM Finding 0062]:
- `TOMYRIGHT` (2): address > reach (position beyond the crum's end)

For a document spanning V:1.1-1.5, inserting at V:1.100 would be TOMYRIGHT relative to **all** existing crums.

## No Knife Cut, But Insertion Proceeds

The `makegappm()` function performs an early-exit check: "if the insertion point equals or exceeds the crum's reach, the knife cut is SKIPPED entirely" [ST-INSERT Finding 0062]. This means:
- No split occurs for beyond-reach positions
- The function returns early for each existing crum
- But the insertion operation continues and creates a new crum at the specified position

## Gap Creation Confirmed

The enfilade structure inherently supports non-contiguous V-spans. Evidence:
- `retrieve_vspanset` can return multiple separate spans for different subspaces [SS-VSPAN-VS-VSPANSET Finding 0017]
- The POOM is a 2D enfilade where children have arbitrary displacements relative to the root [INV-ENFILADE-RELATIVE-ADDRESSING Finding 0066]
- There is no requirement for V-space to be contiguous

## Observable Consequences

After `INSERT("X") at V:1.100`:
- `retrieve_vspanset` would show two separate spans: one at `1.1 for 0.5` and one at `1.100 for 0.1`
- `retrieve_contents(V:1.50)` would fail — no POOM mapping exists for that position
- The gap contains no V→I mappings; queries within the gap return empty results

This behavior is not explicitly tested in the findings but follows directly from the documented preconditions (no bounds check) and the documented handling of TOMYRIGHT positions (skip knife-cut but proceed with crum creation).

## Code Exploration

Based on my analysis of the C source code, I can now provide a complete answer with specific code citations:

---

## Answer: INSERT Beyond Document Extent

When INSERT is called with a V-position beyond the current document extent, **the behavior depends on whether the document is empty**:

### Case 1: Empty Document
**The backend accepts the arbitrary V-position** and creates the first POOM entry at that exact position.

**Evidence:**
- `insertnd.c:191-197` in `doinsertnd()`:
  ```c
  if (isemptyenfilade (father)) {
      firstinsertionnd (father, origin, width, infoptr);
      return(FALSE);
  }
  ```
- `insertnd.c:199-218` in `firstinsertionnd()` — Creates a crum at the specified position without any bounds checking.

### Case 2: Non-Empty Document  
**The backend silently ignores the insertion** if the V-position is beyond the document's reach (extent).

**Evidence:**
1. **No V-position validation exists** — `do2.c:110-113`:
   ```c
   bool acceptablevsa(tumbler *vsaptr, typeorgl orglptr)
   {
       return (TRUE);
   }
   ```
   The `acceptablevsa()` function always returns TRUE and performs no validation.

2. **Bounds check in makegappm** — `insertnd.c:140-143`:
   ```c
   if (iszerotumbler (&fullcrumptr->cwid.dsas[V])
   || tumblercmp (&origin->dsas[V], &grasp.dsas[V]) == LESS
   || tumblercmp (&origin->dsas[V], &reach.dsas[V]) != LESS)
       return(0);    /* this if for extensions to bc without calling cut*/
   ```
   
   This checks:
   - Is document V-width zero? (empty case)
   - Is origin < grasp? (before start)
   - **Is origin >= reach?** (at or beyond end)
   
   If origin ≥ reach (beyond extent), the function **returns immediately without inserting anything**. The comment "for extensions to bc without calling cut" indicates this is intentional — positions outside the existing tree structure are skipped.

### Summary

| Scenario | Behavior |
|----------|----------|
| Empty document + any V-position | ✅ Creates POOM entry at specified position |
| Non-empty + position < start | ❌ Silently ignores |
| Non-empty + position >= end | ❌ Silently ignores |
| Non-empty + position within extent | ✅ Inserts normally |

**The backend does NOT:**
- Create gaps in V-space
- Clamp positions to valid ranges
- Return errors for out-of-bounds positions

**The backend DOES:**
- Accept arbitrary initial positions in empty documents
- Silently ignore out-of-bounds insertions in non-empty documents

### Call Chain

```
fns.c:insert() [line 84]
  ↓
do1.c:doinsert() [line 87]
  ↓ calls docopy() with vsaptr
do1.c:docopy() [line 45]
  ↓ line 56: acceptablevsa() — always returns TRUE
  ↓ line 60: insertpm()
orglinks.c:insertpm() [line 75]
  ↓ line 113: uses vsaptr as-is
  ↓ line 130: calls insertnd()
insertnd.c:insertnd() [line 15]
  ↓ routes to makegappm() for POOM
insertnd.c:makegappm() [line 124]
  ↓ lines 140-143: OUT-OF-BOUNDS CHECK
  ↓ returns 0 if origin >= reach (SILENTLY IGNORES)
```

This behavior explains why the test harness will show unchanged vspansets and content after attempting insertions beyond the document extent.

---

## Question 17 [gregory]

> After INSERT completes, are ALL pre-existing granfilade entries — both text molecules and link orgls belonging to any document — guaranteed byte-identical to their state before the INSERT?

### Gregory's Answer

## KB Synthesis

Looking at this question, I need to distinguish between different types of "granfilade entries" and understand what INSERT modifies.

## Answer: **NO** - with an important qualification

The target document's orgl/POOM structure is modified, but text molecules and link orgls in the permascroll remain byte-identical.

## Detailed Analysis

### What the Granfilade Contains

From [SS-DUAL-ENFILADE] and [SS-UNIFIED-STORAGE], the granfilade stores:
1. **Permascroll text content**: (I-address → byte data) mappings
2. **Document orgls**: Each document's POOM enfilade structure
3. **Link orgls**: Link objects at permanent I-addresses

### What INSERT Modifies

**Text Molecules (Permascroll Content): UNCHANGED** ✓

From [INV-IADDR-IMMUTABILITY]:
> "I-addresses, once allocated in the granfilade, are permanent and immutable... the content associated with any I-address never changes"

INSERT allocates **new** I-addresses via `inserttextingranf` but never modifies existing text content. The permascroll is append-only [FC-GRANF-ON-DELETE].

**Link Orgls: UNCHANGED** ✓

From [INT-LINK-INSERT]:
> "Links attached to content via I-addresses survive insertion because I-addresses are immutable... The link's I-address endpoints are unchanged"

Link objects store I-addresses for their endpoints [SS-LINK-ENDPOINT], which don't change. From [SS-THREE-LAYER-MODEL], INSERT affects layer 3 (POOM references) but not layer 1 (link orgls in I-space).

**Target Document's POOM: MODIFIED** ✗

From [ST-INSERT] and [SS-POOM-MUTABILITY]:
- `insertpm` modifies the target document's POOM tree structure
- Adds new V→I mappings via `insertnd`
- May split nodes via `splitcrumupwards` [ST-INSERT Finding 0060]
- May extend existing POOM crums via `isanextensionnd` [ST-INSERT Finding 0062]

### Tree Structure Metadata

Even for unchanged leaf content, granf tree restructuring (splits, height increases) can modify:
- Parent pointers
- Sibling links  
- The fullcrum (root) itself [ST-INSERT Finding 0060]

But the **content** at each I-address remains immutable.

## Conclusion

If "granfilade entries" means the **content** stored at I-addresses (text bytes and link endpoint data), then YES - they remain byte-identical due to [INV-IADDR-IMMUTABILITY].

If "granfilade entries" includes the **POOM structure** of the target document, then NO - INSERT necessarily modifies the target document's orgl to add new V→I mappings.

The most precise answer: **Pre-existing permascroll content and link orgls remain byte-identical. The target document's POOM structure is modified, but other documents' POOMs remain unchanged** [FC-INSERT-IADDR].

## Code Exploration

Let me present my findings directly to you while that write is pending:

---

# Answer: NO — Pre-Existing Granfilade Entries Are Modified

After INSERT completes, pre-existing granfilade entries are **NOT** guaranteed to be byte-identical. The implementation modifies existing entries in at least **four distinct ways**:

## 1. Text Buffer Extension (Content Modification)

**[backend/insert.c:87-88]**

When inserting text adjacent to an existing text crum with available space, `fillupcbcseq()` modifies the existing crum in-place:

```c
movmem(&info->granstuff.textstuff.textstring,
       (char*)(&(ptr->cinfo.granstuff.textstuff))+crumlength,
       textlength);
ptr->cinfo.granstuff.textstuff.textlength = crumlength + textlength;
```

The actual **text bytes** in the granfilade crum are modified, and the length field is updated.

---

## 2. Width Field Modification (Tree Metadata)

**[backend/insert.c:53-60]**

When creating a new crum, the width of an adjacent existing crum is recalculated:

```c
tumblersub (&nextaddress, &offset.dsas[WIDTH], &ptr->cwid.dsas[WIDTH]);
```

Line 59 directly modifies `ptr->cwid.dsas[WIDTH]` — the width metadata of a pre-existing crum.

---

## 3. POOM Displacement Shifts

**[backend/insertnd.c:162]**

When inserting into a document's POOM, `makegappm()` shifts the displacement of crums after the insertion point:

```c
tumbleradd(&ptr->cdsp.dsas[V],&width->dsas[V],&ptr->cdsp.dsas[V]);
```

This modifies the `cdsp` (displacement) field of existing crums to "make room" for the inserted content in V-space.

---

## 4. Link Orgl Structure Pointers

**[backend/insert.c:49-51]**

When inserting a new GRANORGL entry, the orgl structure's tree pointers are updated:

```c
if (info->infotype == GRANORGL){
    info->granstuff.orglstuff.orglptr->leftbroorfather = new;
}
```

The orgl's `leftbroorfather` pointer is modified to reflect the new tree sibling relationship.

---

## Scope

- **Within the same document**: Content, metadata, and tree pointers are all subject to modification
- **Across documents**: Content in other documents' address spaces should not be modified, though shared tree structure could be affected by rebalancing

---

## Architectural Observation

The granfilade uses **in-place modification** rather than copy-on-write semantics. This is an optimization: text extension avoids creating many tiny crums, and displacement updates avoid wholesale tree reconstruction. However, it means the data structure is **mutable** during insertions, not immutable or append-only.

---

## Question 18 [gregory]

> When INSERT shifts a POOM entry right via tumbleradd in makegappm, and the entry's V-displacement plus the insertion width would cross the subspace boundary (e.g., V:1.14 + width 0.2 reaching into 2.x), does findaddressofsecondcutforinsert prevent this shift, or could a text entry be pushed into the link subspace?

### Gregory's Answer

## KB Synthesis

Looking at this question, I need to trace through the knife construction mechanism and the shift classification logic.

## The Second Blade Placement

From [SS-TWO-BLADE-KNIFE] and [FC-SUBSPACE] Finding 0054:
- For INSERT at position `N.x`, `findaddressofsecondcutforinsert()` computes `blade[1] = (N+1).1`
- For insertion in text subspace (1.x), `blade[1] = 2.1` (start of link subspace)
- The knife defines shift region `[blade[0], blade[1])`

## The Classification Logic

From [FC-SUBSPACE] Finding 0054, entries are classified:
- Case 0: `v < blade[0]` — before insertion, no shift
- Case 1: `blade[0] ≤ v < blade[1]` — shifted right by insertion width  
- Case 2: `v ≥ blade[1]` — beyond second blade, no shift

**Critically: Classification happens based on the entry's position BEFORE the shift, not after.**

## The Scenario

Consider:
- Text entry at V:1.9 (in text subspace)
- INSERT at V:1.3 with width 0.8
- `blade[0] = 1.3`, `blade[1] = 2.1`
- Entry at 1.9 satisfies `1.3 ≤ 1.9 < 2.1` → **Case 1 (shift)**
- After shift: `1.9 + 0.8 = 2.7` — **crosses into link subspace!**

## The Answer

**No, `findaddressofsecondcutforinsert` does NOT prevent this shift.** 

The second blade protects entries **already at 2.1+** from being shifted (they're case 2, no shift). But it does not prevent entries **in the 1.x range near the boundary** from being pushed across by a large insertion width.

## Evidence of the Gap

From [EC-REARRANGE-CROSS-SUBSPACE] (Finding 0051), REARRANGE has the same issue:
> "Rearrange can move content across subspace boundaries because offsets are computed purely from tumbler arithmetic with no digit-0 (subspace) validation."

From [PRE-REARRANGE] (Finding 0051):
> "REARRANGE has a missing precondition: all cut points must lie within the same subspace, OR the resulting displacements must preserve subspace membership for every affected orgl."

INSERT has the same missing precondition. The system relies on **conventional usage** (reasonable insertion widths, positions not near subspace boundaries) rather than enforcing the constraint. The second blade mechanism provides subspace isolation for the **next** subspace (preventing shifts from propagating across), but not for the **current** subspace (preventing entries from being pushed out).

This is a gap in [INV-SUBSPACE-CONVENTION] enforcement. The formal spec should document this as a precondition: `∀ entry ∈ poom(doc) : blade[0] ≤ entry.vpos < blade[1] ⟹ subspace(entry.vpos + insert_width) = subspace(entry.vpos)`.

## Code Exploration

Based on my reading of the source code, I can now answer your question definitively.

## Answer: No, `findaddressofsecondcutforinsert` does not prevent this shift, but the concern is based on a misconception about subspace boundaries.

### Subspace Structure (from `backend/do1.c:393-408`)

First, the subspace layout in udanax-green is:
- **Link subspace**: V < 1.0 (i.e., 0.x)
- **Text subspace**: V >= 1.0 (i.e., 1.x, 2.x, 3.x, ...)

The boundary is at **V:1.0**, not V:2.0. Both 1.x and 2.x are part of the text subspace.

### How `findaddressofsecondcutforinsert` Works (`backend/insertnd.c:174-183`)

For insertion at position V:1.14:

1. **Line 179**: `tumblerincrement(position, -1, 1, secondcut)` → 2.14 (increments mantissa[0] by 1)
2. **Line 180**: `beheadtumbler(position, &intpart)` → intpart = 14 (removes first digit)
3. **Line 181**: `tumblerincrement(secondcut, 0, -14, secondcut)` → 2.0 (subtracts fractional part)
4. **Line 182**: `tumblerincrement(secondcut, 1, 1, secondcut)` → 2.1 (adds to mantissa[1])

Result: **blade[1] = 2.1**

### What Gets Shifted (`backend/insertnd.c:162`)

In `makegappm`, entries classified by `insertcutsectionnd` as case 1 (starting in [blade[0], blade[1])) are shifted:

```c
case 1:/*9-17-87 fix */
    tumbleradd(&ptr->cdsp.dsas[V],&width->dsas[V],&ptr->cdsp.dsas[V]);
```

For insertion at V:1.14, **all entries in [1.14, 2.1) get shifted**, which includes:
- Text entries from 1.14 through 1.999...
- Text entries from 2.0 through 2.09999...

### Can Entries Cross from 1.x to 2.x?

**Yes**, but only if the insertion width is large enough. In tumbler arithmetic:

- Entry at V:1.99 + width {0, 2} = V:1.101 (stays in 1.x)
- Entry at V:1.99 + width {1, 0} = V:2.99 (moves to 2.x)
- Entry at V:1.14 + width {0, 200} = V:1.214 (stays in 1.x)

To move from 1.x to 2.x requires `width.mantissa[0] >= 1` (i.e., adding 1.0 or more in the first digit).

### Your Specific Example

> V:1.14 + width 0.2 reaching into 2.x

This **cannot** happen with width 0.2:
- V:1.14 (mantissa = {1, 14})
- width 0.2 (mantissa = {0, 2})
- Result: V:1.16 (mantissa = {1, 16})

There is no "carry" in tumbler arithmetic. To reach 2.x from 1.14, the width would need mantissa[0] >= 1.

### Could a Text Entry Be Pushed into Link Subspace?

**No.** Link subspace is V < 1.0 (the 0.x range). Since:
1. Text entries are at V >= 1.0
2. `tumbleradd` only increases values (never decreases)
3. Adding a positive width to any V >= 1.0 keeps V >= 1.0

A text entry cannot be pushed into link subspace (0.x) by INSERT.

### Is This a Bug?

**No.** Both 1.x and 2.x are valid text addresses. The POOM supports arbitrary addresses in the text subspace (>= 1.0). The blade[1] calculation at 2.1 is intentional — it defines a "gap-making range" that extends slightly past the next integer boundary, ensuring all entries that need shifting get shifted together.

### Verification

You can test this with a golden test scenario. If you'd like, I can write one that:
1. Inserts text at V:1.1
2. Inserts text at V:1.99 with width > 1.0
3. Verifies the second entry ends up at V:2.99+

---

**Code citations:**
- Subspace boundaries: `backend/do1.c:393-408`, `backend/correspond.c:143`
- blade[1] calculation: `backend/insertnd.c:174-183`
- Entry classification: `backend/edit.c:207-233`
- Shift logic: `backend/insertnd.c:162`
- tumbleradd: `backend/tumble.c:365-404`

---

## Question 19 [gregory]

> Does INSERT write anything to the spanfilade beyond the single DOCISPAN entry for the newly allocated I-span — for instance, does it update or duplicate DOCISPAN entries for the shifted POOM entries whose V-positions changed?

### Gregory's Answer

## KB Synthesis

No. INSERT writes **only** a single DOCISPAN entry (or small number of entries, depending on I-span consolidation) for the newly allocated I-addresses. It does NOT update or duplicate DOCISPAN entries for the shifted POOM entries.

## The Evidence

From **[ST-INSERT]** (Finding 0036):
> `doinsert` → `inserttextingranf` → `docopy` → `insertpm` + `insertspanf(..., DOCISPAN)`

The call chain shows `inserttextingranf` returns fresh I-addresses as an `ispanset`, which is then passed to `insertspanf`. This ispanset contains ONLY the newly allocated I-addresses, not the existing ones whose V-positions shifted.

From **[SS-DOCISPAN]** (Finding 0036):
> The spanf enfilade contains a type 4 index called DOCISPAN that maps **I-addresses to the documents containing them**.

This is the critical architectural point: DOCISPAN is an **I-address-to-document mapping**, not a V-position-to-document mapping.

From **[ST-INSERT]** (Finding 0030):
> 3. **After insertion point** (V-addr >= p, pre-insert): Each character's V-address shifts by +n. **Its I-address is unchanged.**

When INSERT shifts existing content, the I-addresses remain the same — only V-positions change. Since DOCISPAN indexes by I-address, and those I-addresses still map to the same document, no update is needed.

## Why No Update Is Necessary

The existing DOCISPAN entries remain valid because:

1. **I-addresses are immutable** ([INV-IADDR-IMMUTABILITY])
2. **Document membership is I-address-based**, not V-position-based ([SS-DOCISPAN])
3. **Spanf is write-only** — no update mechanism exists ([INV-SPANF-WRITE-ONLY])

Example state transition:
```
Before INSERT "X" at V(1.2):
  POOM:     V(1.1)→I(5.1), V(1.2)→I(5.2), V(1.3)→I(5.3)
  DOCISPAN: I(5.1)→{doc}, I(5.2)→{doc}, I(5.3)→{doc}

After INSERT:
  POOM:     V(1.1)→I(5.1), V(1.2)→I(5.4), V(1.3)→I(5.2), V(1.4)→I(5.3)
  DOCISPAN: I(5.1)→{doc}, I(5.2)→{doc}, I(5.3)→{doc}, I(5.4)→{doc}  ← only NEW entry added
```

The existing DOCISPAN entries for I(5.1), I(5.2), I(5.3) remain correct: these I-addresses are still in the document, just at different V-positions. DOCISPAN doesn't care about V-positions.

## Confirmation from DELETE Behavior

**[INT-DELETE-SPANF-DIVERGENCE]** (Finding 0057) confirms this by demonstrating the inverse: DELETE removes V-to-I mappings from the POOM but does NOT remove the corresponding DOCISPAN entries. This proves the spanfilade operates independently of V-position changes — it tracks I-address presence in documents, not V-position locations.

## Code Exploration

Perfect. I now have all the evidence I need to answer this question definitively. Let me write up the complete answer:

---

# Answer: Does INSERT write anything to the spanfilade beyond the single DOCISPAN entry?

**No.** INSERT writes exactly ONE DOCISPAN entry to the spanfilade — for the newly allocated I-span only. It does NOT write or update spanfilade entries for the shifted POOM entries whose V-positions changed.

## Evidence from the Code

### 1. The INSERT Operation Flow

From `do1.c:87-123`, `doinsert`:
```c
bool doinsert(typetask *taskptr, typeisa *docisaptr, tumbler *vsaptr, typetextset textset)
{
    makehint(DOCUMENT, ATOM, TEXTATOM, docisaptr, &hint);
    ret = (inserttextingranf(taskptr, granf, &hint, textset, &ispanset)
        && docopy (taskptr, docisaptr, vsaptr, ispanset));
    return(ret);
}
```

The INSERT operation:
1. Allocates new I-space via `inserttextingranf` → returns `ispanset`
2. Calls `docopy` to insert the ispanset at the V-position

### 2. The docopy Operation

From `do1.c:45-65`:
```c
bool docopy(typetask *taskptr, typeisa *docisaptr, tumbler *vsaptr, typespecset specset)
{
    return (
       specset2ispanset (taskptr, specset, &ispanset, NOBERTREQUIRED)
    && findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
    && acceptablevsa (vsaptr, docorgl)
    && asserttreeisok(docorgl)
    && insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)        // [1] POOM update
    && insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN)     // [2] SPANFILADE update
    && asserttreeisok(docorgl)
    );
}
```

Two separate operations:
1. **`insertpm`** — modifies the POOM (V → I mapping)
2. **`insertspanf`** — writes to the spanfilade (docISA, spantype) → I-spans

These are sequential and independent. `insertspanf` receives only the newly allocated `ispanset`.

### 3. How insertpm Shifts Existing POOM Entries

From `insertnd.c:124-172`, `makegappm`:
```c
int makegappm(typetask *taskptr, typecuc *fullcrumptr, typewid *origin, typewid *width)
{
    // Make cuts at insertion point
    movetumbler (&origin->dsas[V], &knives.blades[0]);
    findaddressofsecondcutforinsert(&origin->dsas[V],&knives.blades[1]);
    knives.nblades = 2;
    knives.dimension = V;
    makecutsnd (fullcrumptr, &knives);
    
    // Find intersection and iterate over crums
    newfindintersectionnd (fullcrumptr, &knives, &father, &foffset);
    prologuend ((typecorecrum*)father, &foffset, &fgrasp, (typedsp*)NULL);
    for (ptr = findleftson (father); ptr; ptr = findrightbro (ptr)) {
        i=insertcutsectionnd(ptr,&fgrasp,&knives);
        switch (i) {
          case 0:
          case 2:
            break;    // Crum is before insertion point — no change
          case 1:     // Crum is AFTER insertion point — shift it!
            tumbleradd(&ptr->cdsp.dsas[V],&width->dsas[V],&ptr->cdsp.dsas[V]);
            ivemodified (ptr);
            break;
        }
    }
    setwidnd(father);
    setwispupwards (findfather ((typecorecrum*)father),1);
}
```

**Line 162** is the key: `tumbleradd(&ptr->cdsp.dsas[V],&width->dsas[V],&ptr->cdsp.dsas[V]);`

This:
- ADDS the insertion width to the V-displacement of POOM crums after the insertion point
- Only modifies `cdsp.dsas[V]` — the V-coordinate
- Does NOT change `cdsp.dsas[I]` or `cwid.dsas[I]` — the I-coordinates remain unchanged
- Does NOT call `insertspanf` or touch the spanfilade in any way

**Line 164**: `ivemodified (ptr);` marks the POOM crum as modified for disk write-back.

### 4. What insertspanf Actually Writes

From `spanf1.c:15-54`:
```c
bool insertspanf(typetask *taskptr, typespanf spanfptr, typeisa *isaptr, 
                 typesporglset sporglset, INT spantype)
{
    prefixtumbler (isaptr, spantype, &crumorigin.dsas[ORGLRANGE]);
    tumblerclear (&crumwidth.dsas[ORGLRANGE]);
    clear (&linfo, sizeof(linfo));
    
    for (; sporglset; sporglset = (typesporglset)((typeitemheader *)sporglset)->next) {
        if (((typeitemheader *)sporglset)->itemid == ISPANID) {
            movetumbler (&((typeispan *)sporglset)->stream, &lstream);
            movetumbler (&((typeispan *)sporglset)->width, &lwidth);
            movetumbler (isaptr,&linfo.homedoc);
        }
        // ... handle other item types ...
        
        movetumbler (&lstream, &crumorigin.dsas[SPANRANGE]);
        movetumbler (&lwidth, &crumwidth.dsas[SPANRANGE]);
        insertnd(taskptr,(typecuc*)spanfptr,&crumorigin,&crumwidth,&linfo,SPANRANGE);
    }
    return (TRUE);
}
```

`insertspanf`:
- Receives the `sporglset` parameter — the list of I-spans to write
- For each ispan in the list, constructs a 2D coordinate:
  - **ORGLRANGE**: `(docISA, spantype)` — e.g., `(doc.123, DOCISPAN)`
  - **SPANRANGE**: `(I-stream, I-width)` — the I-span coordinates
- Calls `insertnd` with `index=SPANRANGE` to write into the SPAN enfilade

From `do1.c:62`, the call site:
```c
insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN)
```

It passes:
- `ispanset` — the **newly allocated I-spans only**
- `DOCISPAN` — the span type constant

It does NOT receive or iterate over existing POOM entries.

## Why This Is Architecturally Correct

The spanfilade maps `(docISA, spantype, I-position) → content`.

When INSERT adds content at V-position X:
1. New I-space is allocated for the inserted content
2. The POOM is updated to map `V=X → new I-span`
3. All POOM entries at `V ≥ X` have their V-displacements increased
4. **But their I-coordinates don't change** — they still point to the same I-spans

Since the spanfilade is indexed by I-position (not V-position), and the I-positions of existing content haven't changed, there's no need to update the spanfilade.

This is the fundamental architectural principle: **I-space provides stable addresses independent of V-space rearrangements.**

## Summary

**INSERT writes exactly ONE DOCISPAN entry to the spanfilade** — for the newly allocated I-span. The shifted POOM entries whose V-positions changed do NOT trigger spanfilade updates because:

1. The spanfilade is indexed by `(docISA, spantype, I-position)`
2. The I-positions of existing content are unchanged
3. Only the POOM (V → I mapping) changes
4. The code clearly separates these concerns: `insertpm` modifies POOM only, `insertspanf` writes to spanfilade only, and they are called sequentially with independent data

**Code citations:**
- `[do1.c:60]` — `insertpm` call
- `[do1.c:62]` — `insertspanf` call with `ispanset` parameter
- `[insertnd.c:162]` — V-displacement shift in `makegappm`
- `[spanf1.c:51]` — `insertnd` writes to spanfilade indexed by SPANRANGE (I-position)

---

## Question 20 [gregory]

> When INSERT is dispatched through the FEBE protocol, does putinsert send the success response to the client before doinsert executes the POOM mutation, and if doinsert fails (e.g., findorgl BERT check), does the client receive a success response for a mutation that never occurred?

### Gregory's Answer

## KB Synthesis

# Answer: Yes, the client receives success before mutation and cannot detect silent failure

The answer is **YES** on both counts. This is a known protocol-level issue documented extensively in the knowledge base.

## Response Timing

INSERT follows the problematic pattern documented in **[EC-RESPONSE-BEFORE-CHECK]**:

1. `getinsert()` — parse the request from the client
2. **`putinsert(taskptr)` — send SUCCESS response to client** 
3. `doinsert(taskptr, ...)` — attempt the actual POOM mutation

The success response is sent at step 2, before step 3 executes. This is confirmed by code evidence: `fns.c:84-98` shows `putinsert()` occurs before `doinsert()`.

## Silent Failure Behavior

When `doinsert` calls `findorgl(taskptr, granf, &docisa, &docorgl, WRITEBERT)` and the BERT check fails (returns FALSE), the operation is **silently skipped**. Per **[EC-RESPONSE-BEFORE-CHECK]**:

> When the operation fails internally (BERT check, or any other failure in the `doXXX` path), the back end prints an error to stderr and silently continues. The front end has no way to detect the failure — it has already received a matching success response code.

The client receives success (from step 2) but the document remains unchanged (step 3 failed). The only indication of failure is a stderr message the client never sees.

## Protocol Implication

This makes BERT enforcement a **voluntary protocol**, not an enforced precondition. As stated in **[INT-BERT-FEBE]**:

> The back end trusts the front end to: (1) acquire BERT tokens before mutations, (2) respect write exclusivity, and (3) release tokens when done. The back end provides the BERT machinery for front ends to coordinate among themselves, but does not enforce compliance.

And from **[PRE-INSERT]** (Finding 0050):

> The precondition "caller holds WRITEBERT for the target document" is a *protocol obligation* that the front end must satisfy voluntarily. The back end does not reject operations that violate this precondition — it accepts them (sends success) and then silently discards them.

## Contrast: CREATELINK Does It Correctly

The knowledge base notes that **CREATELINK is the exception** that follows the correct pattern (`fns.c:100-115`):

```
getcreatelink() && docreatelink()  // checked FIRST
if success: putcreatelink(taskptr, &linkisa)  
if failure: putrequestfailed(taskptr)
```

The response is sent AFTER execution, so the client knows the true result.

## Commented-Out Evidence

**[EC-RESPONSE-BEFORE-CHECK]** notes that commented-out code in `fns.c` shows the correct pattern was written for `deletevspan()` but disabled:

> Commented-out code in `fns.c` shows the correct pattern for `deletevspan()` as well, suggesting the implementers were aware of the issue.

## System-Level Consequence

This creates a fundamental trust assumption, per **[INT-BERT-FEBE]**:

> The formal specification must explicitly model the trust assumption: all behavioral guarantees (write exclusivity, access control, concurrent safety) are conditional on front-end compliance with the BERT protocol. This is a system-level assumption, not a component-level invariant. Formalizable as: `system_correct ↔ (backend_correct ∧ all_frontends_compliant)`.

**Conclusion:** The INSERT operation sends success responses to clients before attempting mutations. When BERT checks fail, clients receive success for operations that never executed. This is not a bug but a design choice that makes the FEBE protocol a coordination mechanism rather than an enforcement boundary.

## Code Exploration

Perfect! Now I have the complete execution trace. Let me write the final answer with all code citations.

---

# Answer: Yes — Critical Protocol Bug in INSERT and Other Write Operations

**The client receives a success response BEFORE the mutation executes, and if the mutation fails (including BERT check failures), the client never learns about it.**

## Evidence

### 1. INSERT Sends Response Before Execution

**File: `backend/fns.c:84-98`**

```c
void insert(typetask *taskptr)
{
  typeisa docisa, vsa;
  typetextset textset;
  bool getinsert(), doinsert();
 
   (void) getinsert (taskptr, &docisa, &vsa, &textset);
   putinsert (taskptr);                                    // Line 91: SUCCESS SENT
   if (!doinsert (taskptr, &docisa, &vsa, textset))        // Line 92: MUTATION EXECUTES
#ifndef DISTRIBUTION
    fprintf(stderr,"requestfailed in insert\n");           // Line 94: Only stderr on failure
#else
;
#endif
}
```

**Execution order:**
1. **Line 90**: `getinsert` parses request parameters
2. **Line 91**: `putinsert` **sends success response to client**
3. **Line 92**: `doinsert` **performs the actual mutation** (can fail)
4. **Lines 93-97**: If `doinsert` fails, only prints to stderr (debug builds) or does nothing (production)

### 2. doinsert Calls docopy, Which Performs BERT Check

**File: `backend/do1.c:86-122`**

```c
bool doinsert(typetask *taskptr, typeisa *docisaptr, tumbler *vsaptr, typetextset textset)
{
  // ... setup ...
  
  makehint(DOCUMENT, ATOM, TEXTATOM, docisaptr, &hint);
  ret = (inserttextingranf(taskptr, granf, &hint, textset, &ispanset)
    && docopy (taskptr, docisaptr, vsaptr, ispanset)      // Line 118: Calls docopy
  );
  return(ret);
}
```

**File: `backend/do1.c:44-64`**

```c
bool docopy(typetask *taskptr, typeisa *docisaptr, tumbler *vsaptr, typespecset specset)
{
  typeispanset ispanset;
  typeorgl docorgl;
  bool specset2ispanset(), findorgl(), acceptablevsa(), insertpm(), insertspanf();
  bool asserttreeisok();

  return (
     specset2ispanset (taskptr, specset, &ispanset, NOBERTREQUIRED)
  && findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)  // Line 54: BERT CHECK
  && acceptablevsa (vsaptr, docorgl)
  && asserttreeisok(docorgl)

  /* the meat of docopy: */
  && insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)   // Line 59: POOM mutation
  &&  insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN)
  && asserttreeisok(docorgl)
  );
}
```

**Line 54**: The `findorgl` call with `WRITEBERT` parameter performs the BERT permission check. If this fails, the entire chain returns FALSE.

### 3. findorgl BERT Check Can Fail After Response Sent

**File: `backend/granf1.c:16-40`**

```c
bool findorgl(typetask *taskptr, typegranf granfptr, typeisa *isaptr, typeorgl *orglptr, int type)
{
  typeorgl fetchorglgr();
  int temp;

  if (/*backenddaemon &&*/(temp = checkforopen(isaptr, type, user)) <= 0) {  // Line 21
#ifndef DISTRIBUTION
    if (!isxumain) {
      fprintf(stderr,"orgl for ");
      dumptumbler(isaptr);
      fprintf(stderr," not open in findorgl temp = %d\n",temp);
      return FALSE;                                         // Line 27: RETURNS FALSE
    }
#else
    if (!isxumain) {
      *orglptr = NULL;
      return FALSE;                                         // Line 34: RETURNS FALSE
    }
#endif
  }
  *orglptr = fetchorglgr(taskptr, granfptr, isaptr);
  return (*orglptr ? TRUE : FALSE);
}
```

**Line 21**: `checkforopen(isaptr, type, user)` checks if the document is open with sufficient permissions.  
**Lines 27, 34**: If check fails (returns ≤ 0), returns FALSE immediately.

### 4. checkforopen Permission Logic

**File: `backend/bert.c:51-86`**

```c
int checkforopen(tumbler *tp, int type, int connection)
{
  conscell *p;
  bertentry *bert;
  int foundnonread = FALSE;

  if (type == NOBERTREQUIRED) {
    return 1;
  }

  for (p = berttable[hashoftumbler(tp)]; p && p->stuff; p = p->next) {
    bert = p->stuff;
    if (tumblereq(tp, &bert->documentid)) {
      if (connection == bert->connection) {
        switch (bert->type) {
          case READBERT:
            return (type == READBERT) ? READBERT : /* WRITE */ -1;  // Line 68
          case WRITEBERT:
            return WRITEBERT;                                       // Line 70
        }
      } else {
          if (bert->type != READBERT) {
            foundnonread = TRUE;
          }
      }
    }
  }

  if (!foundnonread && (type == READBERT || isthisusersdocument(tp))) {
    return 0;                                                       // Line 81
  } else {
    return -1;                                                      // Line 83
  }
}
```

**Returns ≤ 0 (failure) when:**
- **Line 68**: Document opened READ, but WRITE requested (returns -1)
- **Line 81**: Document not found in BERT table and requires open (returns 0)
- **Line 83**: Document opened by another connection (returns -1)

## The Original Correct Implementation Was Known

**File: `backend/fns.c:69-82`** (commented out)

```c
/*void insert (taskptr)
  typetask *taskptr;
{
  typeisa docisa, vsa;
  typetextset textset;
  bool getinsert(), doinsert();

  if (
     getinsert (taskptr, &docisa, &vsa, &textset)
  && doinsert (taskptr, &docisa, &vsa, textset))
    putinsert (taskptr);                           // Response sent AFTER doinsert
    else
    putrequestfailed (taskptr);
}*/
```

The commented-out version shows the correct pattern: check both `getinsert` AND `doinsert` before calling `putinsert`.

## Affected Operations

The same bug exists in:
- **INSERT** [`fns.c:84-98`]
- **COPY** [`fns.c:35-47`] (commented-out correct version at lines 49-66)
- **REARRANGE** [`fns.c:159-173`] (commented-out correct version at lines 143-156)
- **DELETEVSPAN** [`fns.c:333-347`] (commented-out correct version at lines 318-331)

All perform BERT checks via `findorgl(..., WRITEBERT)`:
- **dorearrange** [`do1.c:39`]
- **docopy** [`do1.c:54`]
- **dodeletevspan** [`do1.c:163`]

## Consequences

1. Client receives success response before any mutation occurs
2. If BERT check fails (no write permission), client believes mutation succeeded but nothing was written
3. If any other failure occurs in `doinsert` (tree assertions, etc.), client is never notified
4. Only debug builds print failures to stderr — production builds silently fail
5. This violates basic protocol correctness: success responses must indicate actual success

## Conclusion

**Yes, this is a critical protocol bug.** The success response is sent before the BERT permission check and before the POOM mutation executes. If the BERT check fails or any other error occurs during the mutation, the client receives a success response for an operation that never happened.
