# Consultation Answers — Frame Condition Completeness

**Inquiry:** What must each operation explicitly guarantee about state it does not intend to modify? What frame conditions must hold across all operations to ensure unaffected properties — ownership, links, addresses — are preserved?
**Date:** 2026-02-25 18:52
**Questions:** 20 (10 nelson, 10 gregory)

---

## Question 1 [nelson]

> When content is appended to a document, must the ownership of every other document in the system remain exactly as it was before the operation?

### Nelson's Answer

# Yes — APPEND Cannot Affect Ownership of Any Other Document

This follows directly from multiple interlocking guarantees in the architecture.

## Ownership Is Structural, Not Mutable State

Ownership is encoded in the tumbler address itself — specifically the User field:

> "There are four major fields, each expandable indefinitely, with three major dividers between them. These fields are Server, User, Document and Contents." [LM 4/26]

> "The basic principle is that of owned numbers. Numbers are owned by individuals or companies, and subnumbers under them are bestowed on other individuals and companies on whatever basis the owners choose." [LM 4/17]

Ownership is not a property that can be written to or overwritten. It is the address. An operation on document A cannot change the User field of document B's tumbler, because tumbler addresses are permanent:

> "New items may be continually inserted in tumbler-space while the other addresses remain valid." [LM 4/19]

## APPEND Operates on Exactly One Document

The operation is scoped to a single document:

> "This appends \<text set\> onto the end of the text space of the document \<doc id\>." [LM 4/67]

APPEND creates new bytes in I-space under the target document and extends that document's V-space. No other document's I-space, V-space, or address is touched.

## Only the Owner May Modify

> "Every document has an owner, the person who created and stored it... Only the owner has a right to withdraw a document or change it." [LM 2/29]

This is a bidirectional constraint. It means the owner controls their document, **and** it means no operation by anyone else — including system-internal side effects of another user's APPEND — can modify your document. If APPEND to document A could somehow alter ownership of document B, it would violate this guarantee for document B's owner.

## The Non-Destruction Guarantee Reinforces This

> "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate — without damaging the originals." [LM 2/45]

If creating entirely new documents from old ones must not damage originals, then merely appending to your own document certainly cannot affect anyone else's ownership.

## Summary

Ownership of every other document must remain exactly as it was after an APPEND, because:

1. **Ownership = address** — the User field of the tumbler is immutable
2. **APPEND is scoped** — it operates on one document only
3. **Modification requires ownership** — no operation on document A can constitute a modification of document B
4. **Addresses are permanent** — no operation reorders, reassigns, or invalidates existing tumbler addresses

This isn't a separate invariant that needs stating — it falls out inevitably from the architecture. An operation that somehow changed another document's ownership would violate the tumbler permanence guarantee, the ownership guarantee, and the non-destruction guarantee simultaneously.

---

## Question 2 [nelson]

> If a link is created between two passages, must all existing links — including those touching the same documents — remain unchanged in their endpoints and meaning?

### Nelson's Answer

# Yes — Creating a Link Cannot Change Existing Links

The Xanadu architecture makes this guarantee through multiple reinforcing properties. No explicit "link independence axiom" appears in Literary Machines, but the guarantee follows necessarily from the system's structural invariants.

## 1. Links Have Permanent, Independent Addresses

Each link occupies its own position in the document's link subspace, numbered by creation order:

> "The links designated by a tumbler address are in their permanent order of arrival. A document includes only the links of which it is the home document." [LM 4/31]

Creating link `2.756` does not renumber or affect links `2.1` through `2.755`. The address scheme is append-only for links — new arrivals get the next number; existing addresses are untouched.

## 2. Endsets Point to Immutable I-Space

A link's three endsets (from-set, to-set, type) point to I-space addresses — permanent content addresses that never change:

> "A Xanadu link is not between points, but between spans of data." [LM 4/42]

Since I-space content is immutable and I-addresses are permanent, no operation — including MAKELINK — can alter what an existing link's endsets refer to. The bytes that link A attaches to are the same bytes before and after link B is created.

## 3. MAKELINK Is Purely Additive

The FEBE protocol defines link creation as:

> "This creates a link in document \<doc id\> from \<from set\> to \<to set\> connected to \<three set\>. It returns the id of the link made." [LM 4/68]

The operation creates one new link and returns its address. There is no described mechanism by which it touches any other link. Contrast this with INSERT, which explicitly states that "the v-stream addresses of any following characters in the document are increased by the length of the inserted text" [LM 4/66] — editing content shifts V-space positions, but link creation has no analogous side effect on other links.

## 4. Links Are Independent Objects

> "A Xanadu link is a connective unit, a package of connecting or marking information. It is owned by a user. It is put in by a user (or a front end), and thereafter maintained by the back end through the back end's inter-indexing mechanisms." [LM 4/41]

Each link is a self-contained "package." Its endsets are its own data, stored at its own address, under its owner's control. No other user's link creation can modify your link's endsets or meaning.

## 5. Link Survivability Confirms Independence

Nelson's survivability guarantee addresses the harder case — what happens when *content itself* is edited:

> "Links between bytes can survive deletions, insertions and rearrangements, if anything is left at each end." [LM 4/43]

If links survive even content editing (the destructive case), they certainly survive the purely additive act of creating another link.

## What Does Change: Discoverability

The one thing that changes when a new link is created is the *set of results* returned by link searches. FINDLINKSFROMTOTHREE will now return one more link when searching the relevant region. But this is additive — existing results remain unchanged in their content and order.

> "THE QUANTITY OF LINKS NOT SATISFYING A REQUEST DOES NOT IN PRINCIPLE IMPEDE SEARCH ON OTHERS." [LM 4/60]

This confirms that links are indexed independently. The presence or absence of other links has no effect on finding or retrieving any given link.

## Summary

Creating a link between two passages:
- **Does not** change any existing link's from-set, to-set, or type
- **Does not** change any existing link's tumbler address
- **Does not** change the I-space content that existing links reference
- **Does** add one new entry to the home document's link subspace
- **Does** add one new result to relevant link searches

The guarantee is architectural, not policy. The system simply has no mechanism by which link creation could modify existing links. Links are independent, self-contained objects with permanent addresses pointing to immutable content.

---

## Question 3 [nelson]

> When a document is shared with a new user, must the permanent addresses of all content within that document remain identical to what they were before sharing?

### Nelson's Answer

## Yes — Permanent Addresses Must Remain Identical

This is not merely a design preference but a **foundational invariant** of the system. When a document is shared with a new user — whether by designating them as an associate of a private document, by publishing it, or by any other access mechanism — all permanent addresses remain exactly as they were.

### The I-Space Guarantee

Every byte in the docuverse has a permanent I-space address that encodes its origin:

```
Node.0.User.0.Document.0.Element
```

This address is assigned at creation and **never changes**, regardless of who accesses the content or how many people access it.

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations."
> — [LM 4/11]

The I-address is not a property of who can *see* the content — it is a property of where the content *lives*. Granting access to a new user changes the access policy, not the storage identity.

### The Tumbler Permanence Guarantee

The document's tumbler address is permanent from the moment of creation:

> "New items may be continually inserted in tumbler-space while the other addresses remain valid. This means that any address of any document in an ever-growing network may be specified by a permanent tumbler address."
> — [LM 4/19]

Nothing in the system — not sharing, not publishing, not editing, not versioning — invalidates an existing tumbler address. This is the core permanence guarantee.

### What "Sharing" Means in Xanadu

Xanadu has no "share" operation. Instead, it has two access states and one structural operation:

1. **Private → Designee access**: The owner designates associates who may read a private document. The document itself is unchanged. Its addresses are unchanged.

2. **Private → Published**: The owner publishes the document, making it universally accessible. The document keeps its tumbler address. Its I-space content keeps its I-space addresses. Nothing moves.

3. **Transclusion (COPY)**: A second user creates their *own* document that references the original's I-space content. The original content stays at its original addresses. The new document creates a V-space arrangement that maps to those same I-space addresses.

> "The virtual byte stream of a document may include bytes from any other document."
> — [LM 4/10]

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies."
> — [LM 4/11]

In all three cases, the permanent addresses of the content are identical before and after.

### Why This Must Be So

Address stability is not a convenience — it is what makes the system work. If addresses changed when content was shared:

- **Links would break.** Links point to I-space addresses. If sharing changed those addresses, every link made before sharing would become invalid.

- **Attribution would be severed.** Origin traceability depends on the I-address encoding which document created each byte. Changing addresses would destroy provenance.

> "You always know where you are, and can at once ascertain the home document of any specific word or character."
> — [LM 2/40]

- **Transclusion would fail.** Other documents that transclude content from the shared document rely on stable I-addresses. Changing them would break every transclusion.

- **Version comparison would be impossible.** Correspondence between versions depends on shared I-space origin. If sharing changed addresses, versions could no longer be compared.

### The Only Thing That Changes

When a document is shared, the only thing that changes is **who may request it**. The access policy is a property of the document's ownership and publication status — not of its address. The content, its addresses, its links, and its relationships to other documents in the docuverse all remain exactly as they were.

> "Only the owner has a right to withdraw a document or change it."
> — [LM 2/29]

Sharing is not a change to the document. It is a change to the visibility of an already-existing, permanently-addressed entity in the docuverse.

---

## Question 4 [nelson]

> Must an editing operation on one version of a document guarantee that all prior versions remain retrievable with identical content?

### Nelson's Answer

# Yes. Absolutely and Without Exception.

This is not a negotiable design property. It is the **foundational invariant** of Xanadu's storage architecture. Every editing operation on any version must leave all prior versions retrievable with identical content. Here is why this is guaranteed by the architecture itself, not merely by policy.

## The Architectural Guarantee: I-Space Immutability

Xanadu separates content from arrangement through two address spaces. **I-Space** (Invariant Space) is where content permanently lives. **V-Space** (Virtual Space) is the document's current arrangement of that content.

Every editing operation — INSERT, DELETE, REARRANGE, COPY — operates on **V-space only**. The I-space content is never modified, never overwritten, never touched.

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

A version IS a V-space arrangement over I-space content. Since I-space content is immutable, and each version's V-space arrangement is preserved, prior versions are always reconstructible from unchanged ingredients.

## Append-Only Storage Makes This Structural

I designed an append-only storage system specifically to abolish destructive replacement:

> "Virtually all of computerdom is built around the destructive replacement of successive whole copies of each current version." [LM 2/14]

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

Content enters the system and **never leaves**. New content is appended. Edits create new V-space mappings. Nothing is overwritten. This is not a backup strategy bolted onto conventional storage — it is the storage paradigm itself.

## DELETE Does Not Destroy

This is where people most commonly misunderstand the system. DELETE in Xanadu removes content from V-space (the current view) but does **not** remove it from I-space:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

When you "delete" from version 5, the bytes vanish from version 5's V-stream. But those bytes still exist at their permanent I-addresses. Versions 1 through 4, which reference those same I-addresses through their own V-space arrangements, are completely unaffected.

## The Explicit User Guarantee

I stated this guarantee directly:

> "The file management system we are talking about automatically keeps track of the changes and the pieces, so that when you ask for a given part of a given version at a given time, it comes to your screen." [LM 2/15]

And emphatically:

> "THE PART YOU WANT COMES WHEN YOU ASK FOR IT." [LM 2/16]

This applies to **any** version, **any** part, at **any** point in the document's history. The system does not privilege the current version:

> "There is thus no 'basic' version of a document set apart from other versions—'alternative' versions—any more than one arrangement of the same materials is a priori better than other arrangements." [LM 2/19]

All versions have equal standing. The "current" version is simply the most recent arrangement.

## Why This Must Be True

Three deeper reasons make this invariant non-optional:

**1. Links depend on it.** Other users will have linked to content in prior versions. Those links point to I-space addresses. If editing could destroy prior version content, it would break other people's links — violating the link survivability guarantee.

> "Links between bytes can survive deletions, insertions and rearrangements, if anything is left at each end." [LM 4/42-4/43]

**2. Transclusions depend on it.** Other documents may transclude content from prior versions. Those transclusions reference I-space addresses. If editing could alter the bytes at those addresses, it would silently corrupt other people's documents.

**3. Correspondence depends on it.** Version comparison works by tracing shared I-space origins across V-space arrangements. If prior versions could be altered, the correspondence relation would become unreliable.

> "Of course, a facility that holds multiple versions of the same material, and allows historical backtrack, is not terribly useful unless it can help you intercompare them in detail—unless it can show you, word for word, what parts of two versions are the same." [LM 2/20]

## Summary

The answer is not merely "yes" but "yes, by construction." The architecture makes it impossible for an editing operation to affect prior versions because:

| Layer | Why prior versions are safe |
|-------|-----------------------------|
| **I-Space** | Immutable. Bytes never change after creation. |
| **V-Space** | Per-version. Each version has its own arrangement. Editing one arrangement does not touch others. |
| **Storage** | Append-only. Nothing is overwritten. |
| **DELETE** | V-space removal only. I-space content persists. |

An implementation that allowed editing to corrupt prior versions would violate the most fundamental architectural decision in the system: the separation of content from arrangement, and the immutability of content once created.

---

## Question 5 [nelson]

> When a user transfers ownership of a document, must every link pointing into or out of that document continue to resolve to the same content as before the transfer?

### Nelson's Answer

# Ownership Transfer and Link Resolution

## Short Answer

Yes — but Nelson never explicitly discusses ownership transfer mechanics. The guarantee follows structurally from deeper architectural invariants that make it impossible for an ownership change to affect link resolution.

## Why Links Are Immune to Ownership Changes

Links in Xanadu point to **I-space addresses**, which are permanent and content-addressed. I-space addresses encode the *originating* document, not the *current owner*:

```
Node.0.User.0.Document.0.Element
```

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

The I-space address is assigned at creation and **never changes**:

> "New items may be continually inserted in tumbler-space while the other addresses remain valid. This means that any address of any document in an ever-growing network may be specified by a permanent tumbler address." [LM 4/19]

Since links attach to I-space byte spans — not to ownership metadata, not to V-space positions — no change of ownership can affect what a link resolves to. The content at an I-address is immutable.

## What Ownership Actually Controls

Nelson defines ownership as a **rights relationship**, not an addressing relationship:

> "Every document has an owner, the person who created and stored it (or someone who arranged it to be created and stored, such as a publishing company). The rightful copyright holder, or someone who has bought the document rights... Only the owner has a right to withdraw a document or change it." [LM 2/29]

Ownership governs:
- Who may **modify** the document (edit V-space)
- Who may **withdraw** the document (subject to due process)
- Who **receives royalties** from byte delivery

None of these affect I-space content or the addresses that links point to.

## Even Editing by a New Owner Preserves Links

If a new owner edits the document (rearranging V-space), links survive because they attach to bytes, not positions:

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes. This has a crucial advantage: it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them." [LM 4/42]

V-space deletion by the new owner also cannot break links, because deletion removes content from the current view only — not from I-space:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

## Even Withdrawal Cannot Easily Break Links

Nelson constrains withdrawal precisely because of link dependencies:

> "It is in the common interest that a thing once published stay published, as in the world of paper. Other readers and users will come to depend on its accessibility. Consequently its author may not withdraw it except by lengthy due process." [LM 2/43]

This obligation binds **whoever owns the document**, not just the original author. The new owner inherits the permanence obligation along with the rights.

## The Tumbler Address Paradox

One subtlety: the User field of a tumbler address permanently encodes the *original creator's account*, not the current owner. If Alice (account 1.2) creates a document and sells it to Bob, the document's address still contains Alice's account number. Nelson acknowledges this:

> "Typically, the user will have no control over the node address he, she or it is assigned; but once assigned a User account, the user will have full control over its subdivision forevermore." [LM 4/29]

This means ownership transfer is a **rights transfer** layered on top of permanent addressing. The address remains Alice's; the rights become Bob's. Links resolve via addresses, so they are unaffected.

## What Nelson Does NOT Specify

Nelson does not detail:
- The **mechanism** of ownership transfer (contract? system operation? both?)
- Whether the **royalty cash register** transfers with the document or resets
- How **out-links** in a transferred document are handled (the owner of the document owns its out-links — does this transfer too?)
- Whether the User field in the tumbler creates any operational complications for the new owner

NEED_RAW: [2/29-2/31, 4/29-4/30, 5/19-5/21] — These pages may contain additional detail on ownership mechanics and the publisher contract's transferability provisions.

## Summary

| Aspect | Affected by ownership transfer? |
|--------|-------------------------------|
| I-space content | No — immutable |
| I-space addresses | No — permanent |
| V-space arrangement | Potentially (new owner may edit) |
| In-links (from others) | No — point to I-space |
| Out-links (from document) | Ownership transfers with document |
| Link resolution | No — links resolve via I-space |
| Permanence obligation | Transfers with ownership |
| Royalty flow | Redirects to new owner |

The architectural answer is unambiguous: **links must and do continue to resolve to the same content**, because they reference permanent I-space addresses that are structurally independent of document ownership. Nelson designed the system so that the question barely arises — ownership is a rights layer above an addressing layer that is, by design, eternal.

---

## Question 6 [nelson]

> If content is inserted at a position within a document, must all content that was not part of the insertion retain its original identity and permanent address?

### Nelson's Answer

# Yes — Absolutely and By Design

Insertion changes **V-space arrangement only**. All pre-existing content retains its permanent I-space identity unchanged. This is not merely a desirable property — it is the architectural foundation on which links, transclusion, correspondence, and historical backtrack all depend.

## The I-Space / V-Space Separation

Xanadu maintains two address spaces precisely to guarantee this:

- **I-Space** addresses are permanent and immutable. Content at an I-space address **never changes** after creation.
- **V-Space** addresses represent the document's current arrangement — a view over I-space content that can be rearranged freely.

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." [LM 4/11]

The "constantly changing" address is the V-space position. The I-space address — the byte's permanent identity — is what remains stable.

## What INSERT Actually Does

The FEBE specification for INSERT states:

> "This inserts \<text set\> in document \<doc id\> at \<doc vsa\>. The v-stream addresses of any following characters in the document are increased by the length of the inserted text." [LM 4/66]

Note carefully what changes and what does not:

| Aspect | Changes? | Explanation |
|--------|----------|-------------|
| V-addresses after insertion point | **Yes** — shifted forward | "increased by the length of the inserted text" |
| I-addresses of existing content | **No** — permanently fixed | I-space is append-only |
| I-addresses of new content | N/A — newly assigned | New bytes get fresh I-space addresses |
| Links to existing content | **No** — survive intact | Links point to I-space, not V-space |

## The Append-Only Storage Model

The underlying storage is explicitly append-only:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

Inserted content is **appended** to I-space with new addresses. Existing I-space content is never moved, overwritten, or re-addressed. The only thing that changes is the V-space mapping — which positions in the virtual byte stream point to which I-space addresses.

## Link Survivability Confirms This

The link survivability guarantee depends on this property:

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." [LM 4/30]

And explicitly for insertions:

> "Links between bytes can survive deletions, insertions and rearrangements, if anything is left at each end." [LM 4/43]

If insertion could alter the I-space identity of existing bytes, links would break. The fact that Nelson guarantees link survivability through insertions is proof that existing content's identity is preserved.

## The Braid Metaphor

Nelson visualizes the document as an "ongoing braid" where edits re-twist the arrangement but do not destroy the strands:

> "Think of the process of making editorial changes as re-twisting this braid when its parts are rearranged, added or subtracted." [LM 2/15]

The strands (I-space content) persist. The twisting (V-space arrangement) changes.

## Summary

**When content is inserted at a position within a document, all content that was not part of the insertion retains its original identity and permanent I-space address.** This is guaranteed by:

1. The **append-only** storage model — existing content is never overwritten [LM 2/14]
2. The **I-space/V-space separation** — only V-addresses shift; I-addresses are permanent [LM 4/11, 4/66]
3. The **link survivability** invariant — which would be impossible if insertion altered existing content identity [LM 4/30, 4/43]
4. The **enfilade architecture** — designed so that "all changes, once made, left the file remaining in canonical order" [LM 1/34]

This is not a feature of Xanadu. It is the **defining characteristic** of its storage model — the thing that distinguishes it from "virtually all of computerdom" which is "built around the destructive replacement of successive whole copies of each current version" [LM 2/14].

---

## Question 7 [nelson]

> When a new document is created, must the system guarantee that no existing document's structure — its sequence of content, its boundaries, its permissions — is altered in any way?

### Nelson's Answer

# Yes — Creating a Document Must Not Alter Any Existing Document

This is one of the most deeply guaranteed properties of Xanadu, emerging from multiple reinforcing architectural principles rather than a single rule. Let me trace the evidence.

## I-Space Immutability

The strongest foundation is I-space permanence. Content, once written, never changes:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control." [LM 4/11]

I-space is append-only:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

Creating a new document allocates fresh I-space addresses for its native content and establishes a new V-space arrangement. Neither operation touches any existing document's I-space content or V-space mapping.

## Tumbler Address Stability

The addressing system was specifically designed so that new items never disturb existing addresses:

> "New items may be continually inserted in tumbler-space while the other addresses remain valid. This means that any address of any document in an ever-growing network may be specified by a permanent tumbler address." [LM 4/19]

New addresses are created by *forking* — subdividing under an owned address — never by renumbering:

> "One digit can become several by a forking or branching process. This consists of creating successive new digits to the right." [LM 4/20]

> "The owner of a given item controls the allocation of the numbers under it." [LM 4/20]

This means document creation is structurally incapable of shifting, renumbering, or invalidating any existing address.

## Ownership Exclusivity

Only the owner may modify a document:

> "Every document has an owner, the person who created and stored it... Only the owner has a right to withdraw a document or change it." [LM 2/29]

Creating document B cannot modify document A because only A's owner has that right. This is not a policy that could be overridden — it is the fundamental ownership model.

## The CREATENEWDOCUMENT Operation

The operation itself is pure creation with no side effects on existing state:

> "CREATENEWDOCUMENT: This creates an empty document. It returns the id of the new document." [LM 4/65]

Even CREATENEWVERSION, which references an existing document, produces a *new* document without touching the source:

> "CREATENEWVERSION: This creates a new document with the contents of document \<doc id\>. It returns the id of the new document. The new document's id will indicate its ancestry." [LM 4/66]

## The Non-Destruction Guarantee

Nelson states this as a core principle, not just a feature:

> "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate — without damaging the originals. This is done by inclusion links." [LM 2/45]

> "The integrity of each document is maintained by keeping the two aspects separate: derivative documents are permanently defined (and stored) in terms of the originals and the changes." [LM 2/37]

## Transclusion Does Not Modify Source

When a new document transcludes content from an existing document, the new document's V-space maps to the existing document's I-space content. The existing document is untouched:

> "No copying operations are required among the documents throughout the system, and thus we solve the problems of update." [LM 2/36]

> "Document A can include Document B, even though Document B is owned by someone else." [LM 2/35]

The source document gains no new content, loses no content, and has no structural change. The new document merely *references* the same I-space bytes.

## Links Are Non-Invasive

Creating a new document may involve creating links pointing to existing documents. But links do not modify their targets:

> "A link need not point anywhere in its home document. Its home document indicates who owns it, and not what it points to. Conversely, links connecting parts of a document need not reside in that document." [LM 4/12]

Links live in their *home* document (the new one). The target document gains discoverable in-links but its structure — its content sequence, its out-links, its permissions — is unchanged.

## Canonical Order Preservation

At the implementation level, the enfilade structures maintain invariants after every operation:

> "All changes, once made, left the file remaining in canonical order, which was an internal mandate of the system." [LM 1/34]

This "internal mandate" means that operations (including document creation) must leave the entire system in a consistent state.

## Summary

The guarantee emerges from the convergence of:

| Property | Source | Effect |
|----------|--------|--------|
| I-space immutability | 2/14, 4/11 | Content never changes after creation |
| Address stability | 4/19-4/20 | New addresses never disturb existing ones |
| Ownership exclusivity | 2/29 | Only the owner may modify a document |
| Append-only storage | 2/14 | No overwriting, only accumulation |
| Non-destructive operations | 2/37, 2/45 | New documents never damage originals |
| Link independence | 4/12 | Links don't modify target documents |
| Canonical order mandate | 1/34 | System invariants preserved across operations |

**The answer is unambiguous: yes.** Creating a new document must guarantee that no existing document's content sequence, boundaries, or permissions are altered. This is not a single rule to be enforced but a structural property that follows from Xanadu's fundamental architecture — the separation of I-space and V-space, the append-only storage model, the forking address scheme, and the ownership model collectively make it impossible for document creation to have side effects on existing documents.

---

## Question 8 [nelson]

> Must a deletion or rearrangement within one document guarantee that any other document quoting or including the same content still resolves correctly?

### Nelson's Answer

# Yes — Absolutely and By Design

This is one of Xanadu's most fundamental architectural guarantees. A deletion or rearrangement in one document **cannot** affect content resolution in any other document. This isn't an implementation detail; it's the reason the I-space/V-space separation exists.

## The Direct Statement

Nelson addresses this explicitly on page 4/11:

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

This is unambiguous. Deletion in document A has zero effect on document B's transclusions of the same content.

## Why This Is Structurally Guaranteed

The guarantee emerges from three architectural properties working together:

### 1. I-Space Is Append-Only

Content lives permanently in I-space. It is never overwritten, never removed:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

Every byte ever created has a permanent I-space address that always returns that exact content.

### 2. Deletion Only Affects V-Space

DELETE removes content from a document's *current arrangement* (V-space), not from permanent storage (I-space):

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

The parenthetical is key: "may remain included in other versions" — and, by extension, in other documents entirely.

### 3. Transclusions Reference I-Space

When document B includes content from document A, it references the content's permanent I-space address. It does not depend on document A's V-space arrangement:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

Document B fetches content from its **home location** in I-space — not from document A's current V-space view.

## Rearrangement Is Even Simpler

Rearrangement is a pure V-space operation. It changes the order of content within one document's virtual byte stream. I-space addresses are completely untouched. Other documents' references to the same I-space content are not even aware that a rearrangement occurred.

## The Design Intent

Nelson frames this as solving "the problems of update":

> "No copying operations are required among the documents throughout the system, and thus we solve the problems of update — especially the problem of updating documents which depend on other documents. We solve this problem simply by windowing to a changing document." [LM 2/36]

And more broadly:

> "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate — without damaging the originals. This is done by inclusion links." [LM 2/45]

The phrase "without damaging the originals" applies in both directions: modifying a derivative doesn't damage its sources, and modifying a source's V-space arrangement doesn't damage documents that include its content.

## Summary

| Operation in Document A | Effect on Document A | Effect on Document B (transcludes from A) |
|---|---|---|
| **Delete content** | Content removed from A's V-space | No effect — B references I-space directly |
| **Rearrange content** | Content reordered in A's V-space | No effect — B has its own V-space arrangement |
| **Insert new content** | A's V-space expands | No effect — B's references unchanged |

The guarantee is absolute because it is structural. There is no pathway by which a V-space operation in one document can reach the I-space content that another document references. The separation is the architecture itself.

---

## Question 9 [nelson]

> When permissions on a document are narrowed or revoked for one user, must the visibility and access for all other authorized users remain completely unchanged?

### Nelson's Answer

## Answer: Independence of Access Across Users

Nelson's model is too coarse-grained to address this question directly — but the structural principles strongly imply **yes**, one user's access change must not affect any other user's access.

### Nelson's Access Model Is Binary, Not Per-User

Nelson specifies only two states for a document:

> "A document may be private or published. [...] A private document may be read and linked-to only by the owner and his or her associates. A published document is available to anyone, and may be read and linked-to by anyone." [LM 2/42]

There is no per-user permission matrix. There is no "Alice can read but Bob cannot" for a published document. The granularity is:

| State | Who Can Access |
|-------|---------------|
| **Private** | Owner + designated associates |
| **Published** | Everyone, irrevocably |

### For Published Documents: Access Cannot Be Narrowed At All

Once published, a document's accessibility is irrevocable — not just for individual users but for everyone:

> "It is in the common interest that a thing once published stay published, as in the world of paper. Other readers and users will come to depend on its accessibility. Consequently its author may not withdraw it except by lengthy due process." [LM 2/43]

The reason is structural, not just policy. Other users will have created links that depend on continued accessibility. Those links are **their property**, stored at their addresses:

> "A link need not point anywhere in its home document. Its home document indicates who owns it, and not what it points to." [LM 4/12]

Revoking Alice's access to a published document would break Alice's links — which are Alice's property. Nelson's architecture does not permit this.

### For Private Documents: Mechanics Are Unspecified

Nelson mentions "associates" and "designees" who may access private documents, but never specifies how this list is managed — how designees are added, removed, or whether removal of one designee has any structural consequence for others.

What he does note is that private documents were not even implemented:

> "Private documents. (Currently all documents are visible to all users.)" [LM 4/79]

### Structural Independence Is Implied

Although Nelson doesn't directly address per-user permission revocation, several architectural properties make access inherently independent across users:

**1. No shared state between users' access paths.** Each user accesses content through their own front-end machine connecting to the back-end. There is no "shared session" or group context that could couple one user's access to another's.

**2. Links are independently owned.** If Alice and Carol both have links to Bob's document, those links live at Alice's address and Carol's address respectively. Any change to Alice's relationship with Bob's document has no structural connection to Carol's links.

**3. The system must not surveil.** Nelson constrains what the system may know about individual users:

> "The network will not, may not monitor what is read or what is written in private documents." [LM 2/59]

A system that couples one user's access to another's would require tracking both users' states in relation to the same document — precisely the kind of monitoring Nelson prohibits.

**4. Tumbler addresses are permanent and user-independent.** Content addresses don't encode who may access them. The address `1.0.3.0.27.1.0.1.1` means the same thing regardless of who requests it. Access control is a layer on top of addressing, not embedded in it.

### The Principle

Nelson's design treats each user's relationship to content as structurally independent. This follows from the deeper principle that **ownership is the only coupling**: only the owner modifies a document, and each user owns their own links, their own documents, and their own compound works independently.

Narrowing one user's access could not, under this architecture, propagate to other users without violating the independence of ownership that is foundational to the system.

### What Nelson Does NOT Specify

Nelson does not address:
- Fine-grained per-user access control lists
- The mechanics of adding or removing "designees" from private documents
- Whether a private document's designee list changes are atomic or per-user
- Any scenario where revoking one user's access is even contemplated for published content

NEED_RAW: 2/41-2/43 — to check whether there is any language about the designee mechanism for private documents beyond what the curated sources capture.

---

## Question 10 [nelson]

> If a version is marked or labeled, must the system guarantee that the content, links, and ownership associated with every other version of that document remain unmodified?

### Nelson's Answer

# Version Isolation Is Unconditional, Not Contingent on Marking

The short answer: **yes**, but for a deeper reason than the question implies. The system guarantees that the content, links, and ownership of every version remain unmodified — not because any version is "marked," but because this is a **fundamental architectural invariant** that applies to all versions unconditionally.

No version operation in Xanadu can affect any other version. This isn't a policy; it's a structural consequence of how the system stores content.

---

## 1. I-Space Content Is Immutable

Every byte ever created has a permanent I-space address that never changes. Versions are V-space arrangements — views over this immutable content. Editing a version changes its V-space mapping, not the underlying bytes.

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

DELETE removes content from a version's V-space arrangement. The I-space content remains forever. Other versions that reference those same I-space bytes are unaffected because they have their own independent V-space mappings.

---

## 2. Each Version Has an Independent V-Space

Each version is a separate V-space arrangement over shared I-space content. Operations like INSERT, DELETE, and REARRANGE apply to a specific version's V-stream. They cannot reach into another version's arrangement.

> "A document is really an evolving ONGOING BRAID." [LM 2/14]

> "There is thus no 'basic' version of a document set apart from other versions—'alternative' versions—any more than one arrangement of the same materials is a priori better than other arrangements." [LM 2/19]

CREATENEWVERSION "creates a new document with the contents of document \<doc id\>. It returns the id of the new document. The new document's id will indicate its ancestry." [LM 4/66]. The new version gets its own V-space. Subsequent modifications to either version are isolated from each other.

---

## 3. Links Are Permanently Addressed and Version-Local

Links within a document occupy the 2.x subspace and are addressed by creation order:

> "The links designated by a tumbler address are in their permanent order of arrival. A document includes only the links of which it is the home document." [LM 4/31]

Link addresses are permanent — link 2.5 is always the 5th link created in that document. A new version receives its own link space. Adding or removing links in one version does not alter the link space of another version.

Furthermore, links point to I-space content (bytes), not V-space positions. This means:

> "Links between bytes can survive deletions, insertions and rearrangements, if anything is left at each end." [LM 4/43]

A link made against version 1 survives because it attaches to I-space bytes, not to version 1's arrangement. Editing version 2 cannot break a link attached to version 1's content, because that content exists in I-space regardless of what any version's V-space does.

---

## 4. Ownership Cannot Be Altered by Version Operations

Ownership is encoded structurally in the tumbler address (the User field):

> "Every document has an owner, the person who created and stored it... Only the owner has a right to withdraw a document or change it." [LM 2/29]

Creating a new version does not change the ownership of the original document. The tumbler address of the original — including its User field — is permanent. No operation on any version can alter the ownership encoded in another version's address.

---

## 5. The Append-Only Foundation

The storage model itself prevents cross-version contamination:

> "Virtually all of computerdom is built around the destructive replacement of successive whole copies of each current version." [LM 2/14]

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

In an append-only system, modification means *adding new content and updating V-space mappings*. It never means overwriting existing content. Previous versions' content, links, and structure are preserved not by policy but by the physical impossibility of overwriting in an append-only store.

---

## 6. Nelson's Explicit Non-Destruction Guarantee

Nelson states the principle directly in the context of publishing modified versions:

> "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate—without damaging the originals. This is done by inclusion links." [LM 2/45]

> "The integrity of each document is maintained by keeping the two aspects separate: derivative documents are permanently defined (and stored) in terms of the originals and the changes." [LM 2/37]

"Without damaging the originals" is not conditional on marking. It is a universal guarantee.

---

## Summary

| Property | Protected? | Mechanism |
|----------|-----------|-----------|
| Content of other versions | Yes | I-space immutability; V-space independence |
| Links of other versions | Yes | Permanent link addressing; separate link subspaces |
| Ownership of other versions | Yes | Structural encoding in tumbler addresses |
| Accessibility of other versions | Yes | Append-only storage; historical backtrack |

The guarantee Nelson provides is **stronger** than what the question asks. It is not that *marked* versions protect other versions from modification. It is that **no operation on any version can modify any other version**, period. This is not a feature that must be implemented — it is a consequence of I-space immutability, V-space independence, append-only storage, and structural ownership encoding. The architecture makes cross-version contamination structurally impossible.

---

## Question 11 [gregory]

> When `docopy` reads the source document's POOM to extract I-addresses, is the source POOM guaranteed to be completely unmodified afterward — no rebalancing, no displacement updates, no cache-dirty flags set on source nodes?

### Gregory's Answer

## KB Synthesis

## Source POOM Modification During `docopy` Read

The KB allows a confident answer for most of this question, with one explicit gap.

---

### What `docopy` does to the source POOM

`docopy` reads the source document's POOM in a single V→I translation step: `specset2ispanset` → `permute` → `span2spanset` → `retrieverestricted` → `findcbcinarea2d`. After extracting the I-spans, it writes to the **target** document's POOM via `insertpm`. [SS-DUAL-ENFILADE, Finding 0012; ST-VCOPY, Finding 0002; FC-DELETE-CROSS-DOC, Finding 0064]

---

### Rebalancing: No

`recombinend` (rebalancing) is invoked only from `deletend` in the DELETE path, and `splitcrumupwards` (splitting) only from `insertseq` in the INSERT path. The read traversal via `findcbcinarea2d` is a pure B-tree walk that accumulates contexts into a sorted linked list without modifying any node's `numberofsons`, displacing any `cdsp` field, or triggering `setwispupwards`. [SS-ENFILADE-TREE, Findings 0058/0071; SS-CONTEXT-LIST, Finding 0078; ST-REBALANCE-2D; ST-SPLIT-2D]

### Displacement updates: No

`setwispnd` / `setwispupwards` — which recompute root displacement and adjust children to relative coordinates — are called only after structural mutations. The read path in `retrieverestricted` calls `prologuend` to compute the running `offset + cdsp` grasp for traversal, but this is a local computation that does not write back to any crum. [SS-ENFILADE-TREE, Finding 0066; INV-ENFILADE-RELATIVE-ADDRESSING]

### `modified` flag: No

`ivemodified` — which sets `modified = TRUE` on a crum and its ancestors — is explicitly called after INSERT and no other operation. The KB directly states: "On INSERT, text is copied into an in-memory bottom crum, and the crum plus its ancestors are marked `modified = TRUE` via `ivemodified()`." No equivalent call appears in the read path. Without a `modified = TRUE` mark, the grim reaper will not write source POOM crums to disk on their behalf. [ST-INSERT, Finding 0059; SS-CACHE-MECHANISM, Finding 0059; INV-DURABILITY-BOUNDARY]

### Structural mutations broadly: No

[SS-POOM-MUTABILITY] (Finding 0072) explicitly enumerates the operations that modify a POOM in-place: INSERT, DELETE, REARRANGE. Reading via `docopy` is not in that set. [INV-ENFILADE-QUERY-INDEPENDENCE] (Finding 0041) formalizes this: "Query operations return results that are independent of the physical tree structure" — queries are observation functions, not mutations. [FC-DELETE-CROSS-DOC] (Finding 0064) provides the cross-document corollary: a POOM operation on document D leaves all other documents' POOMs as frame-condition invariants.

---

### The one gap: `age` counter

The KB is silent on whether the traversal path updates the `age` counter on crums it reads. [SS-CACHE-MECHANISM] (Finding 0059) describes the age counter as the basis for grim-reaper eviction (`age >= OLD`), but does not state whether read access resets it. If reads do update `age` (marking crums as recently accessed), this would affect *which* source POOM crums are eligible for eviction by the grim reaper, but it would not mark them `modified` or trigger any write-back. The `modified` flag and the `age` counter are independent — the grim reaper only writes crums that are both old **and** `modified`. A pure age update from a read would be operationally invisible to any formal postcondition about disk state or POOM structure.

---

### Summary

| Concern | Answer from KB |
|---------|---------------|
| Rebalancing triggered | **No** — only after DELETE/INSERT [SS-ENFILADE-TREE] |
| Displacement (`cdsp`) modified | **No** — `setwispupwards` not called in read path [INV-ENFILADE-RELATIVE-ADDRESSING] |
| `modified` flag set | **No** — `ivemodified` only called after INSERT [ST-INSERT, Finding 0059] |
| Tree structure changed | **No** — reads are pure traversals [INV-ENFILADE-QUERY-INDEPENDENCE, SS-POOM-MUTABILITY] |
| `age` counter updated | **Not answerable from KB** — gap in documented behavior |

## Code Exploration

Now I have the full picture. Let me compile the complete answer.

---

## Answer

### The Execution Path Through `docopy`

`docopy` [do1.c:45–64] executes this sequence:

```c
specset2ispanset (taskptr, specset, &ispanset, NOBERTREQUIRED)   // read source POOM
&& findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)     // find DESTINATION POOM
&& acceptablevsa (vsaptr, docorgl)
&& asserttreeisok(docorgl)
&& insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)      // mutate DESTINATION
&&  insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN)  // mutate spanfilade
```

The source POOM is accessed only in step 1, `specset2ispanset`. Steps 4–6 operate exclusively on the destination document.

---

### Step 1: How the Source POOM is Traversed

`specset2ispanset` [do2.c:14–46] calls `findorgl` on the *source* docisa [do2.c:35], then:

```
specset2ispanset → vspanset2ispanset → permute → span2spanset
  → retrieverestricted → retrieveinarea → findcbcinarea2d
```

`findcbcinarea2d` [retrie.c:229–268] walks the POOM tree:

```c
for (; crumptr; crumptr = getrightbro (crumptr)) {
    if (!crumqualifies2d (...)) continue;
    if (crumptr->height != 0) {
        findcbcinarea2d (findleftson ((typecuc*)crumptr), ...);  // descend
    } else {
        context = makecontextfromcbc ((typecbc*)crumptr, ...);  // harvest
        incontextlistnd (headptr, context, index1);
    }
}
```

All operations in `crumqualifies2d` [retrie.c:270–305] and `whereoncrum` [retrie.c:345–398] are pure reads of `cdsp`, `cwid`, and `height`. They do not call `ivemodified`, do not write to structural fields.

---

### What IS Modified on Source Nodes

**1. The `age` field is written on every traversed crum.**

`rejuvinateifnotRESERVED` is defined [common.h:126]:
```c
#define rejuvinateifnotRESERVED(x)  (((x)->age==RESERVED)?(int)(x):((x)->age = NEW))
```
This macro fires on every node touched by `routinegetrightbro` [genf.c:34–42], `funcfindrightbro` [genf.c:177–186], `findleftson` [genf.c:230], and others. It unconditionally writes `age = NEW`.

`makecontextfromcbc` [context.c:151–174] does an explicit bracket around every bottom crum it inspects:
```c
reserve((typecorecrum*)crumptr);   // age = RESERVED, reservnumber++
// ... copies wid, cdsp, cinfo out into heap context ...
rejuvinate((typecorecrum*)crumptr); // age = NEW, adjusts reservnumber
```
`reserve` [credel.c:364–379] and `rejuvinate` [common.h:128] write the `age` field. These are LRU-management side-effects of any cache-aware traversal; they are not conditional on the node being logically modified.

**2. `leftson` and `numberofsons` are populated for disk-backed source nodes.**

`findleftson` [genf.c:206–232]:
```c
if (ptr->leftson == NULL) {
    if (ptr->sonorigin.diskblocknumber == DISKPTRNULL) { return (NULL); }
    reserve ((typecorecrum*)ptr);
    inloaf (ptr);           // sets ptr->leftson and ptr->numberofsons
    if (oldage != RESERVED)
        rejuvinate ((typecorecrum*)ptr);
}
```
`inloaf` → `varunpackloaf` [corediskin.c:56–150] allocates child crums, calls `adopt()` to link them under `ptr` (writing `ptr->numberofsons` and `ptr->leftson`), and sets each child's `modified = FALSE` [corediskin.c:148]. The parent's `leftson` goes from NULL to a live pointer. This is structural mutation of the in-memory crum, though it faithfully reflects on-disk state.

---

### What Is NOT Modified on Source Nodes

**No `ivemodified` is ever called on the source POOM during retrieval.**

`ivemodified` [genf.c:522–544] is the only function that sets `ptr->modified = TRUE`. Tracing every function called by `findcbcinarea2d` on the source orgl confirms none of them reach `ivemodified`. The `modified` flag — the disk-dirty bit the grim reaper uses to decide whether to flush before eviction — is never set.

**No `makegappm` is called on the source POOM.**

`makegappm` [insertnd.c:124–172] is the function that cuts the POOM and adjusts sibling displacements:
```c
tumbleradd(&ptr->cdsp.dsas[V],&width->dsas[V],&ptr->cdsp.dsas[V]);
ivemodified (ptr);
```
It is called only inside `insertnd` [insertnd.c:54] under the POOM case. `insertnd` is only called by `insertpm` [orglinks.c:130], which operates on the destination `docorgl`, not on any source orgl. The source POOM's `cdsp` displacement fields are never written.

**No `recombine` is called on the source POOM.**

`recombine` [recombine.c:22–34] is called only from `insertnd` [insertnd.c:70–77], after a mutation. It is gated on `father->height < 2 || !father->modified` [recombine.c:112]. Since `modified` is never set on source nodes, even if `recombine` were called on a source node (it isn't), it would exit immediately. But it is never reached via the retrieval path.

---

### Summary

| Concern | Answer |
|---|---|
| Rebalancing (`recombine`) | **Does not occur.** `recombine` is called only inside `insertnd`, which only runs on the destination orgl. |
| Displacement updates (`cdsp`) | **Does not occur.** `makegappm` is not called on source nodes; retrieval only reads `cdsp`. |
| `modified` dirty flag | **Does not occur.** `ivemodified` is never called on any source crum during retrieval. |
| `age` (LRU field) | **Does occur.** Every source crum traversed by `findleftson`, `routinegetrightbro`, and `makecontextfromcbc` has its `age` written by `reserve`/`rejuvinate`/`rejuvinateifnotRESERVED`. This is a cache-management side-effect, not a logical mutation. |
| `leftson` / `numberofsons` | **May occur.** `findleftson` faults in children from disk if not already in memory, populating these fields. The result reflects disk truth; `modified` is set `FALSE` on the children. |

**The source POOM's logical content — widths, displacements, and the `modified` disk-dirty flag — is guaranteed unmodified.** The code is clean in that regard: no `ivemodified`, no `makegappm`, no `recombine` touches the source.

What the code does not guarantee is complete bitwise identity: the `age` field is updated on every source crum that is touched, and `findleftson` may hydrate previously-unloaded subtrees. If "cache-dirty flag" means the `modified` bit (which controls `orglwrite` in `reap` [credel.c:309]), then the source POOM acquires no dirty flags. If it means any transient write to any crum field, the `age` field is written by the LRU mechanism on every single traversed node.

---

## Question 12 [gregory]

> During `deletend`, after POOM entries are disowned via `subtreefree`, does the code make any attempt to touch granfilade nodes for the orphaned I-addresses, or is the granfilade entirely out of scope for the delete path?

### Gregory's Answer

## KB Synthesis

The granfilade is entirely out of scope for the delete path. `deletend` has zero interaction with granfilade nodes, and the I-addresses do not become "orphaned" in any meaningful sense — they remain permanently intact.

## What `deletend` actually frees

The `disown` + `subtreefree` sequence at `edit.c:76-84` operates exclusively on **POOM crums** — the `typecorecrum` nodes that constitute the document's V-to-I mapping tree. `subtreefree` at `credel.c:413-436` is a recursive memory deallocator for these POOM tree nodes. It walks the POOM subtree and releases in-memory crum structs from the grim reaper cache list.

This is structurally separate from the granfilade, which is a different enfilade tree with its own root pointer (`granf`) and its own content nodes. Even though POOM crums and granfilade crums share the same underlying `typecorecrum` struct and the same grim reaper cache, the delete path never traverses the granfilade tree. [FC-GRANF-ON-DELETE]

## The granfilade frame condition is absolute

The KB documents this as an unconditional frame condition:

> `∀ op ∈ {DELETE, REARRANGE} : granf_after(op) = granf_before(op)` — The granfilade is write-once-never-delete: only INSERT adds entries, and no operation removes them. [FC-GRANF-ON-DELETE, Finding 0061]

The call chain confirms this structurally. From `dodeletevspan` at `do1.c:162-171`, the path is:

```
dodeletevspan → findorgl (POOM lookup) → deletevspanpm → deletend
```

`deletevspanpm` at `orglinks.c:145-152` calls only `deletend` and `logbertmodified`. There is no call to any granfilade function — no `findisatoinsertgr`, no `inserttextingranf`, no `subtreewriterecurs` targeting the granf root. [ST-DELETE, Finding 0057]

## The content bytes simply persist

From [INV-IADDR-IMMUTABILITY, Finding 0064]:

> DELETE frees the POOM bottom crums that *reference* I-addresses, but the I-addresses themselves persist in the granfilade unconditionally... There is no mechanism to reuse, reassign, or deallocate I-addresses.

So what `subtreefree` destroys is the **V-to-I mapping record** — the POOM crum that said "V-address 1.3 maps to I-address α." The granfilade entry that says "I-address α contains byte 'C'" is untouched and remains permanently allocated. Subsequent `findpreviousisagr` calls will still find α as an existing I-address and allocate beyond it. [INV-NO-IADDR-REUSE]

This is also why [SS-THREE-LAYER-MODEL] explicitly lists the three layers and notes that no operation removes from I-space, and why FINDDOCSCONTAINING continues to return the document even after content deletion — the granfilade entries that the spanfilade indexes remain fully intact. [INV-IADDRESS-PERMANENT, INT-DELETE-SPANF-DIVERGENCE]

## Summary

`deletend` is purely a POOM-layer operation. The granfilade is not merely "not modified" — it is structurally unreachable from the delete code path. The V-to-I mapping records are freed from the in-memory cache; the I-address content entries in the granfilade are untouched, undiscoverable from the delete path, and permanent.

## Code Exploration

I now have everything needed. Here is the full answer:

---

## `deletend`, `subtreefree`, and the Granfilade

**Short answer:** After `subtreefree` is called in `deletend`, no code in the entire delete path touches granfilade nodes for the orphaned I-addresses. The granfilade is completely out of scope.

---

### The Complete Call Chain

**Entry point** — `dodeletevspan` [do1.c:158–167]:

```c
bool dodeletevspan(typetask *taskptr, typeisa *docisaptr, typevspan *vspanptr)
{
  typeorgl docorgl;
  bool findorgl(), deletevspanpm();

    return (
       findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
    && deletevspanpm (taskptr, docisaptr, docorgl, vspanptr)
    /*&& TRUE*/ /* ht stuff */ );
}
```

`findorgl` [do1.c:164] does touch `granf` — but only to look up the document's orgl (POOM enfilade) by ISA. It is a read of one granfilade crum. Nothing is written to granf here.

**Layer 2** — `deletevspanpm` [orglinks.c:145–152]:

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

`deletevspanpm` calls nothing granfilade-related. It calls `deletend` on `docorgl`, which is a POOM-type enfilade, and `logbertmodified` to record the access-control dirty state. No granf call.

**Layer 3** — `deletend` [edit.c:31–76]:

```c
int deletend(typecuc *fullcrumptr, tumbler *origin, tumbler *width, INT index)
{
    ...
    for (ptr = (typecuc *) findleftson (father); ptr; ptr = next) {
        next = (typecuc *) findrightbro((typecorecrum*)ptr);
        switch (deletecutsectionnd ((typecorecrum*)ptr, &fgrasp, &knives)) {
          case 1:
            disown ((typecorecrum*)ptr);
            subtreefree ((typecorecrum*)ptr);   // <-- the call in question
            break;
          case 2:
            tumblersub (&ptr->cdsp.dsas[index], width, &ptr->cdsp.dsas[index]);
            break;
        }
    }
    setwispupwards (father, 1);
    recombine (father);
}
```

`deletend` operates entirely within the POOM enfilade. For case 1 (crum is fully inside the deleted span), it calls `disown` + `subtreefree`. For case 2 (crum is partially overlapping, i.e. the right neighbour that needs its displacement shrunk), it adjusts the displacement in V-space only. No granf function is called anywhere in the loop body.

**Layer 4** — `subtreefree` [credel.c:413–432]:

```c
/* assumes crum is disowned */
void subtreefree(typecorecrum *ptr)
{
  typecorecrum *p, *right;

    if (ptr->height > 0) {
        for (p = ((typecuc *)ptr)->leftson; p; p = right) {
            right = p->rightbro;
            disown (p);
            subtreefree (p);                    // recurse
        }
    } else if (ptr->cenftype == GRAN             // <-- only for GRAN leaves
            && ((typecbc *)ptr)->cinfo.infotype == GRANORGL
            && ((typecbc *)ptr)->cinfo.granstuff.orglstuff.orglincore)
        orglfree (((typecbc *)ptr)->cinfo.granstuff.orglstuff.orglptr);
    freecrum (ptr);
}
```

The leaf-level branch that touches anything granfilade-related fires **only when `ptr->cenftype == GRAN`** [credel.c:429]. The crums being freed here are POOM crums — their `cenftype` is `POOM`. That entire `else if` branch is dead code for this call path.

POOM bottom crums are `type2dcbc` structs: they contain V-space and I-space displacement/width pairs, not granfilade content. When `freecrum` is called on them [credel.c:431], it simply calls `efree((char*)ptr)` — raw memory deallocation, nothing more.

---

### Why the `subtreefree` GRAN Branch Exists (But Not for This Path)

The `else if (ptr->cenftype == GRAN && ... && orglincore)` guard in `subtreefree` [credel.c:429–430] is for the inverse direction: freeing a **granfilade crum** that happens to have an in-core POOM (`orglincore == TRUE`) for a link orgl. When the granf crum is reaped to disk, the in-memory POOM it owns must be freed. That is granf→POOM cleanup. The delete path is POOM→granf, and there is no symmetric cleanup going the other way.

---

### The Architectural Reason

The POOM is V-space (visible address space). The granfilade is I-space (permascroll — the permanent content store, indexed by ISA). V-space deletion removes mappings from the POOM: it removes the record of "these V-addresses point at these I-addresses." The I-addresses themselves and their granfilade nodes are permanent and immutable. The content stays in the granfilade after deletion — it is still there, still addressable by I-address, just no longer mapped by any V-span in this document version.

This is not an oversight. It is the intended design: permascroll content is never destroyed.

---

### Summary Table

| Call | Granfilade touched? | What it does |
|------|--------------------|-|
| `dodeletevspan` [do1.c:164] | READ only | `findorgl` reads granf to look up the document's POOM orgl |
| `deletevspanpm` [orglinks.c:149] | No | Calls `deletend` on POOM enfilade |
| `deletend` [edit.c:59–60] | No | `disown` + `subtreefree` on POOM crums |
| `subtreefree` [credel.c:413–432] | No (GRAN branch dead for POOM crums) | Recursively frees POOM tree; GRAN-specific `orglfree` branch is unreachable here |
| `freecrum` [credel.c:434–453] | No | Raw `efree` of the POOM crum memory |

**Conclusion:** The granfilade is entirely out of scope for the delete path. After `subtreefree` discards orphaned POOM crums, the granfilade nodes for the corresponding I-addresses are never examined, modified, or freed. The orphaned I-addresses continue to exist in the granfilade unchanged.

---

## Question 13 [gregory]

> When `makegappm` shifts V-positions rightward during INSERT, does it walk only the POOM entries within the current subspace (between the two blades), or does it visit entries in all subspaces and rely on the blade classification to skip them?

### Gregory's Answer

## KB Synthesis

## `makegappm` Visit Pattern: All Crums, Classification-Based Skipping

`makegappm` visits **all POOM entries** via `insertcutsectionnd` and relies on the blade classification to skip cross-subspace entries. It does not pre-filter to the current subspace.

### The Mechanism

The two-blade knife construction [SS-TWO-BLADE-KNIFE] sets:
- `blade[0]` = insertion V-position
- `blade[1]` = `(N+1).1` (next subspace boundary, computed by `findaddressofsecondcutforinsert`)

`insertcutsectionnd()` then iterates over **each** POOM crum and classifies it into one of three cases [ST-INSERT, Finding 0054]:

| Case | Condition | Action |
|------|-----------|--------|
| 0 | crum position < `blade[0]` | No shift |
| 1 | `blade[0]` ≤ crum position < `blade[1]` | Shift right by insertion width |
| 2 | crum position ≥ `blade[1]` | No shift |

### How Cross-Subspace Entries Are Skipped

The classification process for a 2-blade knife first checks each crum against `blade[1]`. For a link crum at V-position `2.1` with `blade[1] = 2.1` [FC-SUBSPACE, Finding 0054]:

> `whereoncrum` returns `ONMYLEFTBORDER` (-1). Since `cmp <= ONMYLEFTBORDER`, the crum is classified as **case 2** (no shift) and the `blade[0]` check is never reached.

This is confirmed by the code at `edit.c:207-233` — the classification is exhaustive over all crums; case 2 simply means "do nothing."

### Key Point: Walk Is Global, Not Bounded

The KB is unambiguous: `insertcutsectionnd` classifies **each** POOM crum [ST-INSERT]. The phrase "shifts only POOM entries within the bounded region" describes the *effect*, not the *scope of traversal*. The function walks the entire POOM tree; the blade classification produces case 2 (no-op) for any entry in a higher subspace.

This architecture means subspace isolation is enforced by classification logic, not by a pre-filtered traversal. It also explains why INSERT's subspace isolation is considered a "deliberate structural guard" [INT-DELETE-SUBSPACE-ASYMMETRY] — the second blade was intentionally placed at the subspace boundary (`findaddressofsecondcutforinsert` contains the source comment: "needs this to give it a place to find intersection of for text is 2.1").

### Contrast with DELETE

DELETE's `deletecutsectionnd` also visits all crums, but lacks the deliberate second-blade computation. Cross-subspace isolation for DELETE is instead an incidental consequence of `strongsub`'s exponent guard [FC-SUBSPACE, Finding 0055; INT-DELETE-SUBSPACE-ASYMMETRY] — a different mechanism producing the same observable effect.

## Code Exploration

---

## Answer

`makegappm` **visits entries in all subspaces** — specifically all direct sons of the full POOM root — and relies entirely on the blade classification from `insertcutsectionnd` to skip sons that don't need shifting.

---

### Step 1: `father` is always the root — `newfindintersectionnd` is a stub

The pivotal fact is `ndinters.c:38-42`:

```c
int newfindintersectionnd(typecuc *fullcrumptr, typeknives *knives,
                          typecuc **ptrptr, typewid *offset)
{
    *ptrptr = fullcrumptr;
    clear (offset,sizeof(*offset));
}
```

This function **ignores `knives` entirely**. It sets `*ptrptr = fullcrumptr` (the root) and `offset = 0`. The old `findintersectionnd` (commented out directly above at `ndinters.c:18-37`) would have descended the tree to find the lowest common ancestor of both blade cuts — a node that truly contained only the region between the blades. That descent was replaced by this no-op stub.

So when `makegappm` calls:

```c
newfindintersectionnd (fullcrumptr, &knives, &father, &foffset);
```

`father` is always `fullcrumptr` itself — the entire POOM root — regardless of where the insertion is happening.

---

### Step 2: The loop walks all direct sons of the root

`insertnd.c:149-169`:

```c
prologuend ((typecorecrum*)father, &foffset, &fgrasp, (typedsp*)NULL);
for (ptr = findleftson (father); ptr; ptr = findrightbro (ptr)) {
    i = insertcutsectionnd(ptr, &fgrasp, &knives);
    switch (i) {
      case 0:
      case 2:
        break;                         /* skip: no position change */
      case -1:                         /* THRUME — impossible after makecutsnd */
        dump(ptr);
        gerror ("makegappm can't classify crum\n");
        break;
      case 1:
        tumbleradd(&ptr->cdsp.dsas[V], &width->dsas[V], &ptr->cdsp.dsas[V]);
        ivemodified (ptr);
        break;
      default:
        gerror ("unexpected cutsection\n");
    }
}
```

Since `father = fullcrumptr`, `findleftson(father)` starts at the leftmost son of the root. The `findrightbro` chain then visits **every direct son of the root** — including sons belonging to every subspace (every document) in the POOM. There is no pre-filtering to a specific V-subrange.

---

### Step 3: Blade classification via `insertcutsectionnd` does the work

`edit.c:207-233`:

```c
INT insertcutsectionnd(typecorecrum *ptr, typewid *offset, typeknives *knives)
{
    if (knives->nblades == 2) {
        i = 1;
        cmp = whereoncrum(ptr, offset, &knives->blades[i], knives->dimension);
        if (cmp == THRUME)  return (-1);           /* error: span across blade[1] */
        else if (cmp <= ONMYLEFTBORDER) return (2);/* blade[1] ≤ crum.start: AFTER */
    }
    i = 0;
    cmp = whereoncrum(ptr, offset, &knives->blades[i], knives->dimension);
    if (cmp == THRUME)  return (-1);               /* error: span across blade[0] */
    else if (cmp <= ONMYLEFTBORDER) return (1);    /* blade[0] ≤ crum.start: AT/RIGHT */
    return (0);                                    /* crum entirely before blade[0] */
}
```

`whereoncrum` (SPAN/POOM branch, `retrie.c:354-372`) computes:

```c
left  = offset[V] + ptr->cdsp[V]          /* absolute start of crum */
right = left + ptr->cwid[V]               /* absolute end of crum */
/* Returns TOMYLEFT(-2), ONMYLEFTBORDER(-1), THRUME(0),
           ONMYRIGHTBORDER(1), TOMYRIGHT(2)  [common.h:86-90] */
```

So `cmp <= ONMYLEFTBORDER` means `address ≤ crum.start` — the blade is at or before the crum's left edge, i.e., **the crum lies entirely at or to the right of that blade**.

Classification with `makecutsnd` having already ensured no crum spans either blade:

| Result | Condition | Meaning | Action in `makegappm` |
|--------|-----------|---------|------------------------|
| 0 | crum.end < blade[0] | entirely before insertion | skip |
| 1 | crum.start ≥ blade[0] AND crum.start < blade[1] | at/right of insertion point | **shift V rightward by width** |
| 2 | crum.start ≥ blade[1] | after second blade | skip |
| -1 | THRUME | straddles a blade | `gerror` (impossible post-cut) |

---

### Step 4: Why THRUME is impossible — `makecutsnd` guarantees clean splits

`insertnd.c:148`:
```c
makecutsnd (fullcrumptr, &knives);
```

`ndcuts.c:15-31` — `makecutsnd` descends the entire POOM tree, splitting any bottom crum (`height==0`) that straddles a blade position (`ndcuts.c:77-91`: `slicecbcpm` via `makecutsbackuptohere`). After this pass, every crum's V-range is cleanly on one side of both blades. The `-1` / THRUME path in `makegappm`'s switch is therefore an error guard, not a normal code path.

---

### Step 5: The two blades, and what `findaddressofsecondcutforinsert` does

`makegappm` sets up the knives at `insertnd.c:144-147`:

```c
movetumbler (&origin->dsas[V], &knives.blades[0]);          /* blade[0] = insertion point */
findaddressofsecondcutforinsert(&origin->dsas[V], &knives.blades[1]); /* blade[1] = companion */
knives.nblades = 2;
knives.dimension = V;
```

`findaddressofsecondcutforinsert` (`insertnd.c:174-183`) produces a companion tumbler address at a different level of the hierarchy from `origin`. Its stated purpose is "to give it a place to find intersection" — that is, it was needed by the old `findintersectionnd` to distinguish the intersection node from its neighbors. The comment "for text is 2.1" hints that for a character address like `2.1`, the companion is at a sub-level like `2.0.N` or `2.1.x`.

With `newfindintersectionnd` being a stub, the companion cut's role in finding the intersection is entirely moot. But the cut still happens via `makecutsnd`, so the tree is split at two V-positions. The sons of the root then fall into the three regions above. In practice, the "between blades" region (case 1) captures the crum(s) sitting at exactly the insertion address, which are the ones whose V-displacements need to be bumped rightward to open space.

---

### Summary

**`makegappm` visits all subspaces, not just the region between the blades.**

- `newfindintersectionnd` is a stub that always returns the full POOM root as `father` [`ndinters.c:38-42`].
- The `for` loop therefore iterates over every direct son of the root — covering all V-subspaces and all documents in the POOM [`insertnd.c:151`].
- `insertcutsectionnd` classifies each son against `blade[0]` (the insertion point) and `blade[1]` (its companion cut) [`edit.c:207-233`].
- Only sons classified as case 1 (V-start ≥ blade[0] and < blade[1]) have their `cdsp[V]` incremented by `width` [`insertnd.c:161-164`]. Sons in other subspaces return case 0 or case 2 and are silently skipped.

The subspace isolation is entirely a consequence of blade classification, not of any pre-narrowing of which sons are visited. The old `findintersectionnd` (commented out in `ndinters.c:18-37`) would have descended to the true intersection node before the loop, limiting the walk to the smallest subtree that contains the insertion point. In the current code that descent was eliminated, and the loop compensates by classifying every root-level son.

---

## Question 14 [gregory]

> If REARRANGE moves content from V-position `1.x` to a position that numerically falls in `0.2.x` (the link subspace), does the POOM accept this new mapping without error, and does `retrievevspansetpm` subsequently return it as a link-subspace entry?

### Gregory's Answer

## KB Synthesis

## Synthesized Answer

### 1. Can REARRANGE Move Content to `0.2.x`?

Yes, but through a mechanism distinct from the `2.x` cross-subspace case documented in Finding 0051.

REARRANGE applies displacements exclusively via `tumbleradd(&ptr->cdsp.dsas[V], &diff[i], ...)` [ST-REARRANGE, Finding 0056]. This is critical: `tumbleradd` has **no exponent guard**. The `strongsub` exponent guard that makes DELETE cross-subspace-safe [FC-SUBSPACE, Finding 0055] does not apply here [INT-DELETE-SUBSPACE-ASYMMETRY]. With appropriate cut placement, arithmetic can carry a `1.x` V-position (exp=0) into the `0.x` fractional range (exp=−1).

**Concrete arithmetic**: Pivot with cuts `[0.5, 1.3, 1.6]`:
- `diff[2] = −(1.3 − 0.5) = −0.8`
- Content at V=`1.4`: `tumbleradd(1.4, −0.8) = 0.6` → lands in `0.x`

More specifically, cuts `[0.0, 1.3, 1.5]` would displace region-2 content by `−1.3`, pushing a value like `1.32` down to `0.02.x`. The POOM has no subspace-membership check on resulting addresses [PRE-REARRANGE, Finding 0051; EC-REARRANGE-CROSS-SUBSPACE].

---

### 2. Does the POOM Accept It?

**Yes, unconditionally.** The POOM is a mutable 2D enfilade that stores `(V-address, I-address)` pairs numerically [SS-POOM-MUTABILITY]. There is no runtime validation of subspace membership — `acceptablevsa()` in `do2.c:110-113` always returns `TRUE` [PRE-SUBSPACE-CONVENTION, Finding 0010], and REARRANGE bypasses even that stub by operating directly on `cdsp.dsas[V]` fields in-place [ST-REARRANGE, Finding 0056].

The 2D enfilade's displacement-tracking mechanism (`setwispnd`) would update the root's `cdsp.dsas[V]` to the new minimum across all entries [SS-ENFILADE-TREE, Finding 0066]. If content lands at `0.2`, the root's minimum displacement becomes `0.2` rather than the prior `1.x` start, restructuring the relative addressing accordingly.

---

### 3. Does `retrievevspansetpm` Return It as a Link-Subspace Entry?

**Not in the same normalized fashion as `2.x` content — but the behavior is formally unspecified in the KB for this case.** The distinction matters:

The **internal** link subspace is at `2.x` (mantissa[0]=2, exp=0). The `0.x` output from `retrievevspansetpm` is a **presentation normalization** of that `2.x` content — the function zeroes mantissa[1] for link spans and constructs separate spans using `maxtextwid()` [SS-DUAL-ENFILADE, Finding 0038]. Content stored at `0.2.x` (fractional addresses, exp=−1) is structurally different from `2.x` link orgls.

The documented analogous case is **Finding 0049/0051** (content moved to `2.x`, the actual internal link subspace):

> "After pivot [1.1, 1.4, 2.5]: 'ABC' at V:2.2–2.4 — vspanset: {at 0 for 0.2, at 1 for 1}"

Here, text moved to `2.x` **was** returned as `{at 0, width 0.2}` — i.e., `retrievevspansetpm` treated it as a link-subspace entry and normalized it accordingly. The `is1story()` check detected the multi-subspace width and applied the link normalization.

For content moved to **`0.2.x`** (not `2.x`), the link normalization path would **not** be triggered the same way, because:
- The `is1story()` check looks at the width structure to detect `2.x`-range content
- `maxtextwid()` computes text extent from the `1.x` displacement, not from `0.x`
- `retrievedocumentpartofvspanpm` reads `cdsp.dsas[V]` which now points to `0.2` (below the expected `1.x` start) [SS-DUAL-ENFILADE, Finding 0043]

The likely outcome is that the content at `0.x` falls into a structural gap: below where `retrievedocumentpartofvspanpm` expects text to start (at `1`), and not at the `2.x` position that triggers the link normalization. The KB does not document this specific configuration, so the precise output of `retrievevspansetpm` for genuine `0.x` POOM entries (placed there by REARRANGE, not by link creation) is **not answerable from the KB** with certainty.

What can be said:
- The content **is** retrievable at its `0.2.x` position via `retrieve_contents` (by analogy with Finding 0049's text-at-`2.x` case)
- It is **not** the same as a link-subspace entry produced through `docreatelink → setlinkvsas` at `2.x` [SS-LINK-SUBSPACE, Finding 0052]
- `RETRIEVEDOCVSPAN` would return a meaningless bounding box [SS-VSPAN-VS-VSPANSET, EC-VSPAN-MISLEADING-SIZE], while `retrievevspansetpm`'s behavior for this structural novelty is formally unspecified

---

### Summary Table

| Question | Answer | Key Citations |
|---|---|---|
| Can `tumbleradd` cross the `1.x`→`0.x` exponent boundary? | Yes — no exponent guard in `tumbleradd` | [INT-DELETE-SUBSPACE-ASYMMETRY], [ST-REARRANGE, F0056] |
| Does POOM accept the result? | Yes — no subspace validation | [PRE-SUBSPACE-CONVENTION, F0010], [SS-POOM-MUTABILITY] |
| Is subspace convention violated? | Yes | [INV-SUBSPACE-CONVENTION], [EC-REARRANGE-CROSS-SUBSPACE] |
| Does `retrievevspansetpm` normalize it as a link entry? | Not as `2.x`→`0.x` link normalization; behavior unspecified for genuine `0.x` | [SS-DUAL-ENFILADE, F0038], [Finding 0049/0051 by analogy] |
| Is it retrievable at `0.2.x`? | Yes, by analogy with F0049 | [PRE-SUBSPACE-CONVENTION, F0049] |

The `strongsub` exponent guard makes DELETE's cross-subspace behavior structurally safer than REARRANGE's `tumbleradd` path — this asymmetry is a fragile invariant that the spec must document explicitly [INT-DELETE-SUBSPACE-ASYMMETRY, FC-SUBSPACE, Finding 0055].

## Code Exploration

I now have all the evidence needed for a complete answer. Let me compile it.

---

## Full Answer

### Notation Clarification

The question's "0.2.x (the link subspace)" requires a notation disambiguation. There are **two distinct representations** of the link subspace in this codebase:

| Context | V-Position | C Internal |
|---|---|---|
| **Internal POOM storage** | `2.x` (e.g., `2.1`, `2.2`) | `{mantissa[0]=2, mantissa[1]=n, exp=0}` |
| **`retrievevspansetpm` output** (when text + links coexist) | `{start:"1", width:"1"}` (synthetic) | Derived from `cwid.mantissa[0]` |
| **`retrievevspansetpm` text output** (synthetic sentinel) | `{start:"0", width:"0.x"}` | From `maxtextwid` |

Finding 0038 confirms: *"Link subspace is 2.x internally (not 0.x). The 0.x representation is an output format convention, not the internal V-address."*

Link references are placed at `2.1`, `2.2` etc. by `findnextlinkvsa` [`do2.c:151-167`]:
```c
tumblerclear (&firstlink);
tumblerincrement (&firstlink, 0, 2, &firstlink);  // {mantissa[0]=2, exp=0} = "2"
tumblerincrement (&firstlink, 1, 1, &firstlink);  // {mantissa[0]=2, mantissa[1]=1} = "2.1"
```

The question's "0.2.x" most likely refers to this `2.x` subspace (as reported through the `retrievevspansetpm` normalized output). I answer that case in full. At the end I note what literally happens with sub-integer "0.2.x" positions.

---

### Does REARRANGE Accept the Move Without Error?

**Yes, unconditionally.**

`rearrangepm` [`orglinks.c:137-142`] is a trivially thin wrapper:
```c
bool rearrangepm(typetask *taskptr, tumbler *docisaptr, typeorgl docorgl, typecutseq *cutseqptr)
{
    rearrangend((typecuc*)docorgl, cutseqptr, V);
    logbertmodified(docisaptr, user);
    return (TRUE);                        /* always TRUE */
}
```

It always returns `TRUE`. There is no guard against target positions crossing into the link subspace.

`rearrangend` [`edit.c:78-160`] implements the operation by adding computed tumbler offsets to each crum's `cdsp.dsas[V]`:
```c
tumbleradd (&ptr->cdsp.dsas[index], &diff[i], &ptr->cdsp.dsas[index]);  // edit.c:125
ivemodified((typecorecrum*)ptr);
```

The offsets (`diff[]`) are pure tumbler arithmetic on the cut positions [`edit.c:162-183`]:
```c
int makeoffsetsfor3or4cuts(typeknives *knives, tumbler diff[])
{
    if (knives->nblades == 3) {
        tumblersub (&knives->blades[2], &knives->blades[1], &diff[1]);
        tumblersub (&knives->blades[1], &knives->blades[0], &diff[2]);
        diff[2].sign = !diff[2].sign;
        ...
    }
}
```

No check is made on whether `ptr->cdsp.dsas[V] + diff[i]` lands in the text subspace (`1.x`) or link subspace (`2.x`). The operation proceeds regardless.

The FEBE dispatch layer also provides no backstop [`fns.c:159-173`]:
```c
void rearrange(typetask *taskptr) {
    (void) getrearrange (taskptr, &docisa, &cutseq);
    putrearrange (taskptr);               /* reply sent BEFORE calling dorearrange */
    if (!dorearrange (taskptr, &docisa, &cutseq))
        fprintf(stderr,"rearrange failed \n");   /* silent failure in DISTRIBUTION */
}
```

`acceptablevsa` [`do2.c:110-113`], which validates V-space addresses for `docopy`, returns `TRUE` unconditionally:
```c
bool acceptablevsa(tumbler *vsaptr, typeorgl orglptr)
{
    return (TRUE);
}
```

**The POOM accepts any mapping REARRANGE produces, including cross-subspace moves.**

---

### Concrete Demonstration

The golden test `golden/rearrange/pivot_cross_subspace_boundary.json` proves it:

```json
{
  "op": "insert", "address": "1.1", "text": "ABC"
},
{
  "op": "insert", "address": "1.5", "text": "DEF"
},
{
  "op": "vspanset_before",
  "result": "<VSpec in 1.1.0.1.0.1, at 1.1 for 0.7>"
},
{
  "op": "pivot_attempt",
  "cut1": "1.1", "cut2": "1.4", "cut3": "2.5",
  "status": "succeeded"
},
{
  "op": "retrieve_after_2x",
  "result": "['ABC']"
},
{
  "op": "vspanset_after",
  "result": "<VSpec in 1.1.0.1.0.1, at 0 for 0.2, at 1 for 1>"
}
```

With cuts at `1.1`, `1.4`, `2.5`:
- `diff[1] = "2.5" − "1.4" = "1.1"` (forward offset for region 1 content)
- `diff[2] = −("1.4" − "1.1") = −"0.3"` (backward offset for region 2 content)

ABC (text at region 1, relative cdsp = `0`) gets `cdsp += "1.1"` → new relative cdsp = `"1.1"`.
DEF (text at region 2, relative cdsp = `"0.4"`) gets `cdsp += −"0.3"` → new relative cdsp = `"0.1"`.

After `setwispnd` [`wisp.c:171-227`] normalizes the tree:
- New root `cdsp.dsas[V]` = old root `"1.1"` + min(`"0.1"`, `"1.1"`) = `"1.1" + "0.1"` = **`"1.2"`**
- New root `cwid.dsas[V]` = max reach of children = **`"1.4"`** (`{mantissa[0]=1, mantissa[1]=4}`)
- ABC's normalized child `cdsp` = `"1.1"` (unchanged because `"1.1" − "0.1" = "1.1"` in tumbler arithmetic: `strongsub` returns `a` when `a.exp > b.exp`)
- Absolute ABC position: root.cdsp `"1.2"` + child.cdsp `"1.1"` = **`"2.1"`** (V-position in link subspace)

Content is retrievable from `2.x`, confirming ABC is now stored there.

---

### Does `retrievevspansetpm` Return It as a Link-Subspace Entry?

**Yes, structurally — but via cwid heuristics, not semantic type-checking.**

The function [`orglinks.c:173-221`] first tests:
```c
if (is1story (&ccptr->cwid.dsas[V])) {
    /* text-only path: single vspan */
    ...
} else {
    /* multi-subspace path: two vspans */
    ...
}
```

After the cross-subspace rearrange, `ccptr->cwid.dsas[V]` = `"1.4"` = `{mantissa[0]=1, mantissa[1]=4, exp=0}`. `is1story` returns **FALSE** (`mantissa[1]=4 ≠ 0`). This triggers the two-span path.

**Computing the "link" span** from cwid:
```c
linkvspan.stream = ccptr->cwid.dsas[V];        // "1.4" = {1,4,0,...}
linkvspan.stream.mantissa[1] = 0;              // → {1,0,0,...}
tumblerjustify(&linkvspan.stream);             // already justified → "1"

linkvspan.width = ccptr->cwid.dsas[V];         // same process
linkvspan.width.mantissa[1] = 0;               // → {1,0,...} = "1"
```

Wire: `0.1~` → Python `Tumbler([1])` = **`"1"`**.

**Computing the "text" span** via `maxtextwid`:

`maxtextwid` recursively walks crums, skipping any that `islinkcrum` identifies [`orglinks.c:255-261`]:
```c
bool islinkcrum(typecorecrum *crumptr)
{
    if(crumptr->cdsp.dsas[V].mantissa[0] == 1 && crumptr->cdsp.dsas[V].mantissa[1] != 0)
        return TRUE;
    return FALSE;
}
```

ABC's normalized relative `cdsp.dsas[V]` = `"1.1"` → `mantissa[0]=1`, `mantissa[1]=1 ≠ 0` → **`islinkcrum(ABC) = TRUE`** → **ABC is SKIPPED** by `maxtextwid`.

DEF's normalized relative `cdsp.dsas[V]` = `0` → `mantissa[1]=0` → `islinkcrum(DEF) = FALSE`. `istextcrum(DEF)` = `mantissa[1]==0 && is1story(cwid)` = TRUE. DEF is counted:
```c
tmpwid = voffset + DEF.cdsp = "1.2" + 0 = "1.2"
maxwid = "1.2"  // {mantissa[0]=1, mantissa[1]=2}
```

The text vspan is then built:
```c
tumblerclear (&vspan.stream);           // stream = 0
movetumbler (&maxwid, &vspan.width);    // width = "1.2" = {1,2,0,...}
vspan.width.mantissa[0] = 0;           // → {0,2,0,...}
```

Wire: `0.0.2~` → Python `Tumbler([0, 2])` = **`"0.2"`**.

`putvspaninlist` inserts both spans sorted by stream. Final result:

| Python output | Source |
|---|---|
| `{start: "0", width: "0.2"}` | Text sentinel: `maxtextwid` found DEF at `"1.2"` |
| `{start: "1", width: "1"}` | Link sentinel: derived from `cwid.mantissa[0]=1` |

This is `at 0 for 0.2, at 1 for 1` — matching the golden test exactly.

**The moved text content (ABC) IS returned as part of the `{start:"1", width:"1"}` "link" span.** More precisely: ABC's contribution to the cwid's `mantissa[1]` entry (the `"4"` in `"1.4"`) is what extends the "link" span's width from `"1"` to potentially larger values in other scenarios.

---

### Why `retrievevspansetpm` Treats It as Link-Subspace

The mechanism has two interlocking behaviors:

1. **`islinkcrum` test** [`orglinks.c:255-261`]: Any crum with relative `cdsp.dsas[V].mantissa[0]=1` and `mantissa[1]≠0` is classified as a "link crum" and excluded from the text-extent calculation. After the rearrange, ABC has exactly this displacement shape (`"1.1"`), so it is excluded from `maxtextwid` and falls instead into the link-span computation via cwid.

2. **`is1story(cwid)` test** [`orglinks.c:184`]: A root `cwid.dsas[V]` is "1-story" only when a single mantissa digit is nonzero. Moving content to a position that causes `cwid.mantissa[1] ≠ 0` (as happens when content spans both `mantissa[0]=1` and `mantissa[1]>0` levels) forces the two-span code path, which segregates text and link entries.

---

### Regarding Literally Sub-Integer "0.2.x" Positions

If "0.2.x" is taken literally as V-positions `< 1` — C internal `{mantissa[0]=2, exp=-1}` = Python `"0.2"` — these differ fundamentally from the link subspace (`2.x`). They are sub-integer positions below the text subspace.

REARRANGE can reach them via a 3-cut pivot where region 2 (moving backward) overshoots below `1.x`. For example, cuts at `"0.2"`, `"1.1"`, `"1.4"` would put region-2 content at `"0.2 + (1.4 − 1.1) → ~0.2.3"`. **No validation in `rearrangend` or `rearrangepm` prevents this.** The POOM would accept it silently.

For `retrievevspansetpm` with content at sub-integer positions: `cwid.dsas[V]` would have `exp < 0` and `mantissa[0] < 1`, which is not a multi-story tumbler in the `mantissa[1]` sense. The `is1story` branch might fire (if only sub-integer content exists) or might not, depending on the exact cwid value. The function's cwid-based heuristics were clearly not designed for this case and would produce semantically meaningless output.

---

### Summary

| Question | Answer |
|---|---|
| Does the POOM accept the move? | **Yes, unconditionally.** `rearrangepm` always returns TRUE [`orglinks.c:141`]; `rearrangend` adds offsets without subspace checks [`edit.c:125`]; `acceptablevsa` returns TRUE unconditionally [`do2.c:112`]. |
| Is content retrievable from the new (2.x) position? | **Yes.** Golden test `pivot_cross_subspace_boundary.json` confirms `retrieve_after_2x: ['ABC']`. |
| Does `retrievevspansetpm` classify it as link-subspace? | **Yes, structurally.** The moved crum acquires relative `cdsp.dsas[V]` matching the `islinkcrum` pattern (`mantissa[0]=1, mantissa[1]≠0`), so `maxtextwid` skips it. Its contribution to root cwid makes `is1story(cwid)` false, triggering the two-span output where it appears in the `{start:"1", width:"1"}` "link" span. The golden test confirms `vspanset_after = at 0 for 0.2, at 1 for 1`. |
| Is the classification semantically correct? | **No.** The content is text (character bytes) but is structurally classified as link-subspace based on cwid heuristics. This is the CD0 violation documented in Finding 0051. |

---

## Question 15 [gregory]

> When `insertendsetsinspanf` indexes a new link's endsets, does it read or modify any existing spanfilade entries for those same I-address ranges, or does it strictly append new entries alongside whatever already exists?

### Gregory's Answer

## KB Synthesis

`insertendsetsinspanf` strictly appends new entries alongside whatever already exists. It does not read existing entries for deduplication, update, or removal.

**The write-only nature of the spanfilade**

[INV-SPANF-WRITE-ONLY] establishes the foundational property: inspection of `spanf1.c` and `spanf2.c` reveals only insertion and query functions — `insertspanf`, `findlinksfromtothreesp`, `retrieveendsetsfromspanf`, `finddocscontainingsp`, `findnumoflinksfromtothreesp`. No `deletespanf`, `removespanf`, or modification function exists anywhere. The set of spanfilade entries is monotonically non-decreasing.

**The insertion mechanism**

[INT-SPORGL-LINK-INDEX] describes exactly what happens: `insertendsetsinspanf()` receives sporglsets for each endpoint type (FROM, TO, THREE) and calls `insertspanf` for each, adding entries tagged with the new link's ISA and endpoint type. The resulting entries map I-address ranges → (link ISA, endpoint type).

[SS-DOCISPAN] (Finding 0047) shows the granularity: `insertspanf` iterates over the ispanset linked list and makes one `insertnd` call per `typeispan` struct — one new B-tree insertion per contiguous I-address range, without consulting what is already stored there.

**The underlying B-tree traversal**

[SS-ENFILADE-TREE] (Finding 0041) describes that `insertseq` adopts new crums as the `RIGHTBRO` of the retrieval position. This traversal necessarily *reads* existing B-tree nodes to find the correct insertion point in the sorted structure, but this is a structural navigation, not a semantic read. The existing entry at the traversal position is not inspected for existing link associations and is not modified — the new entry is inserted alongside it as a sibling.

**Coexistence of entries at overlapping I-addresses**

The purely additive behavior is confirmed by two edge cases:

[EC-STALE-SPANF-REFERENCE] shows that after DELETE removes a document's POOM mappings, the old spanfilade entries persist unchanged. If subsequent operations create new links at the same I-address ranges, both old and new entries coexist — there is no deduplication or consolidation pass during insertion.

[INV-DUAL-ENFILADE-CONSISTENCY] models the spanfilade as `Map<IAddress, Set<LinkISA>>` — a multimap that accumulates link associations at each I-address. New links simply add to whatever set already exists for a given range.

**Summary**

When `insertendsetsinspanf` runs during link creation, it: (1) traverses the B-tree to find insertion positions (structural reads of existing tree nodes), and (2) inserts new entries as right siblings at those positions. It never reads, modifies, merges, deduplicates, or removes any existing spanfilade entries. If two links share endpoint I-addresses, both entries coexist independently in the tree.

## Code Exploration

I now have everything needed to answer the question. Here is the full analysis:

---

## Does `insertendsetsinspanf` Read or Modify Existing Spanfilade Entries?

**Short answer:** It does both — it reads existing entries to decide what to do, and it can modify existing entries in two distinct ways. It is not a pure append.

---

### Call Chain

#### `insertendsetsinspanf` — `do2.c:116-128`

```c
bool insertendsetsinspanf(typetask *taskptr, typespanf spanfptr, typeisa *linkisaptr,
    typesporglset fromsporglset, typesporglset tosporglset, typesporglset threesporglset)
{
  bool insertspanf();
  if (!(
    insertspanf(taskptr,spanfptr,linkisaptr,fromsporglset,LINKFROMSPAN)
      &&insertspanf(taskptr,spanfptr,linkisaptr,tosporglset,LINKTOSPAN)))
        return (FALSE);
  if (threesporglset) {
    if(!insertspanf(taskptr,spanfptr,linkisaptr,threesporglset,LINKTHREESPAN))
        return (FALSE);
  }
  return(TRUE);
}
```

This is a thin wrapper. It calls `insertspanf` up to three times — once each for the from-endset, to-endset, and (if present) three-endset. The `linkisaptr` is the new link's I-address; it becomes the ORGLRANGE key.

---

#### `insertspanf` — `spanf1.c:15-54`

For each sporgl in the sporglset, this builds a 2D address:

- `crumorigin.dsas[ORGLRANGE]` = `prefixtumbler(linkisaptr, spantype)` — the link's I-address prefixed by the endset role (LINKFROMSPAN=1, LINKTOSPAN=2, LINKTHREESPAN=3) [`spanf1.c:22`]
- `crumwidth.dsas[ORGLRANGE]` = zero (cleared) [`spanf1.c:23`]
- `crumorigin.dsas[SPANRANGE]` = the sporgl's stream (I-address of endset content) [`spanf1.c:49`]
- `crumwidth.dsas[SPANRANGE]` = the sporgl's width [`spanf1.c:50`]

Then calls:
```c
insertnd(taskptr,(typecuc*)spanfptr,&crumorigin,&crumwidth,&linfo,SPANRANGE);
```
[`spanf1.c:51`] — `SPANRANGE` as the primary index means the spanfilade is keyed and sorted in the SPANRANGE dimension (the I-address of the endset content).

---

#### `insertnd` — `insertnd.c:15-111`

The general enfilade insertion entry point. For a SPAN-type enfilade (which the spanfilade is), the POOM-specific `makegappm` is **not** called. It goes directly to `doinsertnd` [`insertnd.c:63`], then calls `recombine` if the tree grew [`insertnd.c:76`].

---

#### `doinsertnd` — `insertnd.c:185-197`

```c
if (isemptyenfilade (father)) {
    firstinsertionnd (father, origin, width, infoptr);
    return(FALSE);
}
clear (&offset, sizeof(typedsp));
return(insertmorend (father, &offset, origin, width, infoptr, index));
```

Two paths: empty enfilade (reuse or create the single leaf), or non-empty (full insertion descent).

---

#### `insertmorend` — `insertnd.c:219-239`

```c
makeroomonleftnd (father, offset, origin, &grasp);
if (father->height == 1) {
       return(insertcbcnd (father, &grasp, origin, width, infoptr));
}
ptr = findsontoinsertundernd (father, &grasp, origin, width, index);
temp = insertmorend ((typecuc*)ptr, &grasp, origin, width, infoptr, index);
```

Two significant things happen here before a leaf is ever created.

---

### Modification #1: `makeroomonleftnd` / `expandcrumleftward`

`makeroomonleftnd` (`makeroom.c:13-49`) is called at **every level of the descent**. For each dimension where the new origin is to the left of the current subtree's grasp, it calls `expandcrumleftward`:

```c
// makeroom.c:41
expandcrumleftward ((typecorecrum*)father, &newdsp.dsas[i], &base, i);
```

`expandcrumleftward` (`makeroom.c:52-74`) **modifies existing crums**:

```c
// makeroom.c:58-59
movetumbler (newdsp, &crumptr->cdsp.dsas[index]);           // sets parent's offset
tumbleradd(base,&crumptr->cwid.dsas[index],&crumptr->cwid.dsas[index]); // widens parent

// makeroom.c:64-66 — adjusts every child's relative offset
for (; ptr; ptr = (typecorecrum *)findrightbro(ptr)) {
    tumbleradd(base,&ptr->cdsp.dsas[index],&ptr->cdsp.dsas[index]);
    ivemodified(ptr);
}
```

This is a coordinate-system adjustment — when the new entry lands to the left of the current subtree, all existing children have their `cdsp` (relative offset) incremented by `base`, and the parent's `cwid` (width) is grown accordingly. Existing entries' stored positions are changed.

---

### Modification #2: Extension merging in `insertcbcnd`

`insertcbcnd` (`insertnd.c:242-275`) is the leaf-level insertion. It **reads every existing leaf crum** first:

```c
// insertnd.c:249-258
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

`isanextensionnd` (`insertnd.c:301-309`) returns TRUE if and only if:
1. The new entry's `homedoc` equals the existing crum's `homedoc` [`insertnd.c:305`]
2. The reach (end boundary) of the existing crum exactly equals the new entry's origin [`insertnd.c:308`] — i.e., they are perfectly contiguous

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

When an extension is found, the existing leaf crum's width is **widened in place**:
```c
dspadd (&ptr->cwid, width, &ptr->cwid, (INT)father->cenftype);  // insertnd.c:251
```

This is not a new entry alongside the old — it is the old entry being grown to absorb the new range.

Only when no extension exists is a new leaf crum created and adopted alongside the existing ones [`insertnd.c:260-273`].

---

### Summary

| Situation | What `insertendsetsinspanf` does to existing entries |
|---|---|
| New entry is contiguous with an existing crum (same `homedoc`, adjacent range) | **Modifies** the existing crum's `cwid` in place — merges the new range into it |
| New entry lands to the left of the current subtree extent | **Modifies** existing crums' `cdsp` (offsets) and the parent's `cwid` via `expandcrumleftward` |
| New entry is non-contiguous, within current tree extent | Reads (but does not modify) existing entries; inserts a new leaf alongside them |

`insertendsetsinspanf` does **not** strictly append. It reads every existing leaf crum at the target level to check for adjacency. It will silently **merge** a new I-address range into an existing crum if they are contiguous for the same link. It will also **shift the stored coordinate offsets** of existing crums as a structural side effect whenever the insertion point lies to the left of the current tree's covered range.

---

## Question 16 [gregory]

> During CREATENEWVERSION, `docopyinternal` copies text-subspace POOM entries — does this copying process create any new entries in the granfilade or spanfilade for the version document, or are those layers touched only by the DOCISPAN registration?

### Gregory's Answer

## KB Synthesis

## What `docopyinternal` Touches During CREATENEWVERSION

The answer requires distinguishing three storage layers: the granfilade content region, the granfilade document region, and the spanfilade.

### The Call Chain

From [ST-VERSION] (Finding 0077), the full sequence is:

```
docreatenewversion
  → createorglingranf        (granfilade — document address allocation only)
  → doretrievedocvspanfoo    (reads source's text V-span)
  → docopyinternal
      → specset2ispanset     (converts source V-spans to I-spans — read only)
      → insertpm             (writes new version's POOM)
      → insertspanf          (writes DOCISPAN entries to spanfilade)
```

### What Each Layer Gets

**Granfilade — content region**: Untouched by `docopyinternal`. No new I-addresses are allocated. [FC-GRANF-ON-VERSION] (Finding 0077) states the frame condition explicitly: `granf_content_after = granf_content_before`. The existing I-addresses from the source document are simply referenced, not duplicated. This is confirmed by [INV-MONOTONIC] (Finding 0077): VERSION does not advance the content I-address allocation counter, unlike CREATELINK.

**Granfilade — document region**: Modified once, *before* `docopyinternal` is called, by `createorglingranf`. This allocates the new version's document address. `docopyinternal` itself never calls `findisatoinsertgr` for content.

**POOM (via `insertpm`)**: `docopyinternal` populates the new version's POOM with text-subspace V→I mappings, sharing the source's existing I-addresses. No link-subspace entries are copied — [ST-VERSION-CREATE] (Finding 0043) confirms the link subspace at 2.x is excluded because `retrievedocumentpartofvspanpm` returns only the text subspace displacement.

**Spanfilade (via `insertspanf`)**: `docopyinternal` creates DOCISPAN entries registering the version document as containing the shared I-addresses. This is part of `docopyinternal`'s own execution, not a separate registration step. [ST-VERSION] (Finding 0077) notes that `insertspanf` here "records SPAN entries with provided I-addresses (no allocation)" — it indexes but does not create.

### Summary

The DOCISPAN registration happens **inside** `docopyinternal` via `insertspanf`, not separately. `docopyinternal` writes to exactly two layers: the version's POOM (`insertpm`) and the spanfilade (`insertspanf`). The granfilade content region is a frame condition — `docopyinternal` reads it (to convert V-spans to I-spans) but never writes it.

## Code Exploration

I now have all the information needed for a complete answer. Here is the full trace:

---

## Does `docopyinternal` create new granfilade or spanfilade entries?

### Executive Summary

**`insertpm` writes new nodes into the POOM subtree inside the granfilade, but creates no new top-level granfilade entries (no new ISA→POOM registrations). The spanfilade is touched exactly once, exclusively by the explicit `insertspanf(DOCISPAN)` call at the end of `docopyinternal`.**

---

### Full Execution Trace

#### 1. Before `docopyinternal` is called: `createorglingranf`

`docreatenewversion` [do1.c:277] calls:

```c
if (!createorglingranf(taskptr, granf, &hint, newisaptr)) { ... }
```

This is the **only** moment a new top-level granfilade entry is born for the version document. Tracing through:

- `createorglingranf` [granf1.c:50] → `createorglgr` [granf2.c:111]
- `createorglgr` [granf2.c:120] allocates a brand-new empty POOM enfilade:
  ```c
  locinfo.granstuff.orglstuff.orglptr = createenf(POOM);
  ```
- Then [granf2.c:125] registers it with `insertseq((typecuc*)fullcrumptr, isaptr, &locinfo)`, writing a `GRANORGL`-type leaf into the granfilade sequential-access tree at the address `*newisaptr`.

At this point the new version has a granfilade entry, but its POOM tree is **empty** (zero width, zero displacement).

---

#### 2. Entering `docopyinternal` [do1.c:66-82]

```c
bool docopyinternal(typetask *taskptr, typeisa *docisaptr, tumbler *vsaptr, typespec *specset)
{
    if (!specset2ispanset(taskptr, specset, &ispanset, NOBERTREQUIRED)) return FALSE; // [74]
    if (!findorgl(taskptr, granf, docisaptr, &docorgl, NOBERTREQUIRED)) return FALSE; // [75]
    if (!acceptablevsa(vsaptr, docorgl)) return FALSE;                                // [76]
    if (!asserttreeisok(docorgl)) return FALSE;                                       // [77]
    if (!insertpm(taskptr, docisaptr, docorgl, vsaptr, ispanset)) return FALSE;       // [78]
    if (!insertspanf(taskptr, spanf, docisaptr, ispanset, DOCISPAN)) return FALSE;    // [79]
    ...
}
```

The `specset` passed in from `docreatenewversion` [do1.c:293] is a `vspec` with `docisa = source_isa`, `vspanset = entire vspan of source`.

---

#### Step A: `specset2ispanset` [do1.c:74] — reads source, no writes

`specset2ispanset` [do2.c:14] receives a VSPECID item, so it calls:

```c
findorgl(taskptr, granf, &source_isa, &docorgl, NOBERTREQUIRED)    // [do2.c:35]
&& vspanset2ispanset(taskptr, docorgl, vspanset, ispansetptr)       // [do2.c:36]
```

- `findorgl` [granf1.c:17] on the **source** document: pure read. Calls `fetchorglgr` [granf2.c:22] which calls `retrievecrums` — no writes.
- `vspanset2ispanset` [orglinks.c:397] calls `permute` → `span2spanset` [orglinks.c:404,425], which calls `retrieverestricted` on the source POOM — pure read.

**Result**: An in-memory `ispanset` (list of permascroll I-spans) is produced. **No granfilade or spanfilade writes.**

---

#### Step B: `findorgl` [do1.c:75] — fetches new version's POOM root, no writes

`findorgl(taskptr, granf, newisaptr, &docorgl, NOBERTREQUIRED)` — fetches the POOM root allocated by `createorglingranf`. This is a read of the already-existing granfilade leaf.  
- `fetchorglgr` [granf2.c:22] calls `retrievecrums` and returns `orglptr`. **No writes.**

---

#### Step C: `insertpm` [do1.c:78] — writes into the POOM, not into the granfilade top-level structure

`insertpm` [orglinks.c:75]:

```c
bool insertpm(typetask *taskptr, tumbler *orglisa, typeorgl orgl, tumbler *vsaptr, typesporglset sporglset)
{
    ...
    logbertmodified(orglisa, user);                          // [line 99] — bert table only
    for (; sporglset; sporglset = ...) {
        unpacksporgl(sporglset, &lstream, &lwidth, &linfo);
        movetumbler(&lstream, &crumorigin.dsas[I]);
        movetumbler(&lwidth,  &crumwidth.dsas[I]);
        movetumbler(vsaptr,   &crumorigin.dsas[V]);
        ...
        insertnd(taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);   // [line 130]
        tumbleradd(vsaptr, &crumwidth.dsas[V], vsaptr);
    }
    return TRUE;
}
```

The critical call: `insertnd(taskptr, (typecuc*)orgl, ...)` where `orgl` is the **new version's POOM root** — a POOM-type enfilade that was allocated inside the granfilade by `createorglgr`. `insertnd` [insertnd.c:51] switches on `fullcrumptr->cenftype == POOM` and calls `makegappm` then `doinsertnd` to physically insert new bottom-level CBC nodes into the POOM B-tree.

**These are new in-memory/on-disk crum nodes within the POOM's subtree**, recording the 2D V↔I mapping. They physically reside within the granfilade's storage, but they are **not** new `GRANORGL`-type entries and not new ISA registrations. The granfilade's own sequential structure (which maps ISAs to POOM roots) is not modified — no new `insertseq` is called.

The `insertnd` call operates exclusively on the POOM (cenftype `POOM`); the `spanf` global is never referenced inside `insertpm`.

**Granfilade**: POOM content nodes written. No new top-level entry.  
**Spanfilade**: untouched.

---

#### Step D: `insertspanf` [do1.c:79] — the sole spanfilade write

```c
insertspanf(taskptr, spanf, docisaptr, ispanset, DOCISPAN)
```

`insertspanf` [spanf1.c:15]:

```c
prefixtumbler(isaptr, spantype, &crumorigin.dsas[ORGLRANGE]);  // builds 2D key: (newisa.DOCISPAN, ispan)
for (; sporglset; ...) {
    ...
    insertnd(taskptr, (typecuc*)spanfptr, &crumorigin, &crumwidth, &linfo, SPANRANGE);  // [line 51]
}
```

This is the first and only reference to `spanf` (the global spanfilade) in the entire `docopyinternal` call chain. It inserts one CBC node per I-span into the spanfilade, keyed on `(newVersionISA prefixed with DOCISPAN, permascroll-ispan)`. This is what makes the new version's content addressable via FINDDOCUMENTCONTAINING and related queries.

---

### Diagram of What Each Layer Receives

| Structure | What happens during `docreatenewversion` |
|-----------|------------------------------------------|
| **Granfilade** — top-level (`GRANORGL` entries) | **One** new entry created by `createorglingranf` before `docopyinternal`. `docopyinternal` creates none. |
| **Granfilade** — POOM subtree for new version | New CBC crum nodes inserted by `insertpm` → `insertnd(POOM)` to record V↔I mapping. These are granfilade-internal writes, not new ISA registrations. |
| **Spanfilade** | New CBC crum nodes inserted **only** by `insertspanf(DOCISPAN)` at [do1.c:79]. No other code path inside `docopyinternal` touches it. |
| **Source granfilade** (source doc's POOM) | Read-only. `specset2ispanset` uses `retrieverestricted` to translate V-spans to I-spans; no writes. |

---

### Key Supporting Quotes

- `createorglgr` [granf2.c:119–125] — the only place `GRANORGL`/`insertseq` writes for the new version:
  ```c
  locinfo.infotype = GRANORGL;
  locinfo.granstuff.orglstuff.orglptr = createenf(POOM);
  ...
  insertseq((typecuc*)fullcrumptr, isaptr, &locinfo);
  ```

- `insertpm` [orglinks.c:130] — POOM target confirmed:
  ```c
  insertnd(taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);
  ```
  `orgl` is the POOM root; `spanf` is never mentioned inside `insertpm` or any function it calls.

- `insertspanf` [spanf1.c:51] — only spanfilade write:
  ```c
  insertnd(taskptr, (typecuc*)spanfptr, &crumorigin, &crumwidth, &linfo, SPANRANGE);
  ```
  `spanfptr` is the `spanf` global passed in from [do1.c:79].

---

### Conclusion

The copying process in `docopyinternal` **does** write new crum nodes into the granfilade — but only into the POOM subtree of the newly created version document, recording the V↔I translation. No new top-level granfilade entry (`GRANORGL`) is created; that entry was already created by `createorglingranf` before `docopyinternal` is called.

The spanfilade is touched **exactly once**, exclusively by the `insertspanf(DOCISPAN)` call at [do1.c:79]. This is the registration step that makes the copied permascroll I-spans queryable as belonging to the new version. There is no other spanfilade write anywhere in the `docopyinternal` call tree.

---

## Question 17 [gregory]

> When multiple FEBE sessions have the same document open for read access, and one session performs a `find_links` that triggers heavy spanfilade traversal and cache eviction via `grimlyreap`, can this eviction corrupt or modify the in-memory POOM state that another session's concurrent read operation depends on?

### Gregory's Answer

## KB Synthesis

## Answer: No — Eviction Cannot Corrupt Concurrent Read State

The scenario described is impossible at the backend level, and even where eviction does occur, it preserves rather than corrupts POOM state. Here is the synthesis:

---

### 1. There Is No Concurrent Execution

The foundational fact is that udanax-green's backend is strictly single-threaded with run-to-completion scheduling.

From [INV-ATOMICITY]: `xanadu(&task)` executes the entire operation — request parsing, state mutation, response sending, memory cleanup — before returning to `select()`. There are **no threads, no state-modifying signal handlers, and no preemption.**

From [INV-SEQUENTIAL-DISPATCH]: Even when multiple frontends have pending requests simultaneously (multiple FDs set in `select()`'s result), the event loop processes them **strictly sequentially**. Frontend i's request completes entirely before frontend i+1's request begins.

This means the premise of the question — two sessions executing operations concurrently — does not hold. Session B's read cannot be "in progress" while Session A's `find_links` runs. They are serialized.

---

### 2. What the Grim Reaper Actually Does During Eviction

From [SS-CACHE-MECHANISM]: When memory allocation fails, the grim reaper scans the circular list for crums with `age >= OLD` and not `RESERVED`, **writes modified ones to disk via `orglwrite()`**, then frees them.

Eviction does not corrupt in-memory data — it **preserves** it by flushing to disk before freeing. A POOM crum evicted during a `find_links` operation is written to disk first, then the memory is reclaimed. If that crum is subsequently needed (by the same or a later operation), it is reloaded from disk.

---

### 3. `find_links` Does Not Modify the POOM

From [FC-CONTENT-SPANF-ISOLATION]: "Link search operations access only `spanf` and never modify `granf`."

The `find_links` path (`findlinksfromtothreesp` → spanfilade traversal → I-to-V conversion) is **read-only with respect to POOM crums**. Loading spanfilade crums into the cache during link search may trigger grim reaper eviction of *other* crums (including POOM crums), but `find_links` itself never writes to any POOM. The evicted POOM crums were modified by *prior completed operations*, not by the current `find_links`.

---

### 4. Cross-Enfilade Eviction Is a Durability Concern, Not a Correctness Concern

From [EC-CROSS-ENFILADE-EVICTION]: Memory pressure from spanfilade traversal can evict modified POOM crums from other documents. The concern documented there is about **durability ordering** (which data gets written to disk first), not about data corruption.

From [INV-DURABILITY-BOUNDARY]: "On crash/kill: Only crums previously evicted by the grim reaper survive. Recent INSERTs still in cache are lost." Ironically, a large `find_links` that triggers grim reaper eviction of recently-inserted POOM crums **improves** their crash durability by forcing them to disk earlier.

---

### 5. RESERVED Crums Are Protected

From [SS-CACHE-MECHANISM]: the grim reaper skips crums with `age == RESERVED`. From [FC-RESERVED-CRUM]: reserved crums are invariant under rebalancing as well. Any crum actively held by an in-progress tree operation is protected from eviction.

---

### Summary

| Concern | Analysis |
|---------|----------|
| Concurrent read corruption | Impossible — sequential dispatch [INV-SEQUENTIAL-DISPATCH] |
| `find_links` writing to POOM | Impossible — `find_links` is spanfilade-only [FC-CONTENT-SPANF-ISOLATION] |
| Eviction destroying POOM data | Impossible — modified crums are written to disk before freeing [SS-CACHE-MECHANISM] |
| Eviction of active crums | Impossible — RESERVED crums are skipped [SS-CACHE-MECHANISM] |
| Cross-enfilade eviction ordering | Real, but a durability concern only [EC-CROSS-ENFILADE-EVICTION], not correctness |

The grim reaper's cross-enfilade eviction during `find_links` writes POOM crums from prior operations to disk and reclaims their memory. This is transparent to subsequent operations, which will reload from disk as needed. No corruption or loss of observable state can result.

## Code Exploration

Now I have enough to write a complete, fully-cited answer.

---

## Answer: Can `grimlyreap` During `find_links` Corrupt Concurrent Session POOM State?

**Short answer: No, corruption is not possible.** The reasons are architectural (single-threaded dispatch) and mechanical (the RESERVED/rejuvinate guard protocol). Let me trace both.

---

### 1. There Is No Concurrent Execution

The first and most important fact: udanax-green is **single-threaded**. The event loop in `bed.c:103-149` uses `select()` to identify which file descriptor has data, then calls `xanadu()` for exactly one session at a time:

```c
// bed.c:111-128
if (select(nfds+1, &inputfds2, 0, 0, &timeout) < 0) { ... }
else {
    for (i = 0; i <= nfds; i++) {
        if ((1<<i) & inputfds2) {
            user = fdtoplayer[i];
            ...
            xanadu(&task);   // ← one complete request, no interleaving
        }
    }
}
```

`xanadu()` at `bed.c:153-172` dispatches to `(*requestfns[request])(taskptr)` and only returns after the entire request is complete. While session A's `find_links` is executing, session B is blocked — it cannot be reading anything. The premise of the question (concurrent execution) does not hold in this implementation.

---

### 2. The `grimlyreap` Call Chain

`find_links` dispatches via `fns.c:189-202` → `findlinksfromtothreesp` (`spanf1.c:56-103`) → `sporglset2linkset` → `retrieverestricted` (`retrie.c:56`) → `retrieveinarea` (`retrie.c:87`) → `findcbcinarea2d` (`retrie.c:229`).

At each level, `findleftson` (`genf.c:206`) loads children from disk. If children are absent:

```c
// genf.c:212-229
if (ptr->leftson == NULL) {
    if (ptr->sonorigin.diskblocknumber == DISKPTRNULL) return (NULL);
    reserve ((typecorecrum*)ptr);    // ← MARK RESERVED
    inloaf (ptr);                    // ← disk read → may call ealloc → grimlyreap
    if (oldage != RESERVED)
        rejuvinate ((typecorecrum*)ptr); // ← CLEAR RESERVED
}
rejuvinateifnotRESERVED (ptr->leftson);
return (ptr->leftson);
```

`ealloc` (`credel.c:54-77`) calls `grimlyreap()` only when `falloc` returns NULL and `grimreaper != NULL`:

```c
// credel.c:70-75
if (grimreaper == NULL) {
    xgrabmorecore();
    continue;
}
grimlyreap();
```

`grimlyreap` (`credel.c:106-162`) walks the doubly-linked `grimreaper` ring, incrementing ages of non-reapable crums, and evicts (writes to disk + frees) the first eligible one.

---

### 3. Age Constants and Reap Eligibility

From `reap.h:9-15`:

```c
#define RESERVED 0xff   // keeps a crum from being reaped
#define NEW 0
#define OLD 1           // set this as you wish, age up to it from NEW
```

From `enf.h:65`: `age` is declared `unsigned char`.

From `common.h:126-128`:
```c
#define rejuvinateifnotRESERVED(x) \
    (((x)->age==RESERVED)?(int)(x):((x)->age = NEW))

#define rejuvinate(x) \
    ((x)->age==RESERVED)?(reservnumber?--reservnumber:testforrejuvinate(x)):0, \
    (x)->age = NEW
```

For a crum to be reaped, `isreapable` (`credel.c:164`) requires:

```c
// credel.c:176
if (localreaper->age < OLD || localreaper->age == RESERVED)
    return(FALSE);
```

A crum starts at age `NEW = 0`. `grimreaper->age++` at `credel.c:159` increments it to 1 (= `OLD`). So it takes at least **one complete pass** through the grimreaper ring for a crum to become eligible.

---

### 4. Four Layers of Protection During Traversal

**Layer A — `findleftson` reserves the parent:**
As shown in `genf.c:216`, before loading children from disk (which may trigger `grimlyreap`), the parent crum is marked `RESERVED`. `grimlyreap` skips RESERVED crums at `credel.c:144`:
```c
if (grimreaper->age == RESERVED) { continue; }
```
After `inloaf` completes, `rejuvinate` clears RESERVED.

**Layer B — `makecontextfromcbc` reserves the leaf:**
In `context.c:158-169`:
```c
reserve((typecorecrum*)crumptr);      // RESERVED before allocation
context = createcontext(crumptr->cenftype);  // → eallocwithtag → may trigger grimlyreap
...
rejuvinate((typecorecrum*)crumptr);   // clear after
```
Every leaf crum being converted to a context is protected.

**Layer C — `createcrumcontext` reserves its crum (`context.c:55`):**
```c
reserve (crumptr);
ret = (typecrumcontext *)eallocwithtag(sizeof(typecrumcontext), CRUMCONTEXTTAG);
```
Same pattern.

**Layer D — `isreapable` refuses any inner node whose children are in memory:**
From `credel.c:201` and `credel.c:217-221` (both code paths, `father->modified` TRUE or FALSE):
```c
if (p->height > 0 && ((typecuc *)p)->leftson) {
    return(FALSE);
}
```
Any crum with `leftson != NULL` — i.e., any inner node currently traversed and with children in memory — is not reapable. This cascades upward: if we are inside `findcbcinarea2d` recursing into node X (child of Y), then Y->leftson = X ≠ NULL, so Y cannot be reaped.

**Layer E — `getrightbro` rejuvenates every sibling as it is visited:**
`routinegetrightbro` (`genf.c:34-42`) calls `rejuvinateifnotRESERVED` on both the current and next crum, resetting age to 0 each time a sibling is traversed.

---

### 5. What `grimlyreap` Actually Evicts

`reap` (`credel.c:292-330`) calls `subtreewrite(father)` before freeing anything:

```c
// credel.c:318-329
temp = weakfindfather(localreaper);
...
if (!temp->leftson) {
    grimreaper = grimreaper->nextcrum;
    return(0);
}
subtreewrite(temp);  // write-before-free
```

All evicted crums are serialized to disk before their memory is released. No data is lost; it is only moved back to disk.

---

### 6. Effect on Session B's Previous State

After session A's `find_links` completes and before session B's next request executes:

- Crums loaded by session B in prior requests may have been aged and evicted by `grimlyreap`
- Their on-disk representation is current (written by `subtreewrite`/`orglwrite`)
- When session B's next request calls `findleftson` on an evicted node, `inloaf` re-reads it from disk (`genf.c:225`)

This is correct cache behavior — not corruption. The POOM enfilade's logical state is invariant across evictions.

---

### 6. The One Real Risk: `reservnumber` Accounting

There is a subtle fragility, not a hard corruption: `reserve()` at `credel.c:364-379` increments `reservnumber` and asserts it stays consistent:

```c
void reserve(typecorecrum *ptr) {
    if (ptr->age != RESERVED) {
        ++reservnumber;
    } else {
        gerror("reserve already reserved \n");  // fatal error if double-reserve
    }
    ptr->age = RESERVED;
}
```

If a crum is passed to `reserve()` twice without an intervening `rejuvinate()`, the backend aborts with `gerror`. This is a defensive check, not a corruption path, but it does mean the `find_links` traversal is brittle in the face of any code path that calls `reserve` on an already-reserved crum. Under normal single-session operation this invariant holds, but any future refactoring toward multi-threaded dispatch would break it immediately.

---

### Summary

| Concern | Mechanism | Source |
|---|---|---|
| Concurrent execution | Single-threaded `select()` loop; no interleaving | `bed.c:111-128` |
| Current inner node evicted mid-traversal | `leftson != NULL` → not reapable | `credel.c:201,217-221` |
| Current leaf evicted during context alloc | `reserve()` + `rejuvinate()` bracket every alloc | `context.c:158-169` |
| Parent evicted during disk load | `reserve()` before `inloaf`, `rejuvinate()` after | `genf.c:216-228` |
| Data loss on eviction | `subtreewrite`/`orglwrite` before free | `credel.c:309,329` |
| RESERVED crum skipped by reaper | Age check: `if (age == RESERVED) continue` | `credel.c:144` |

**`grimlyreap` cannot corrupt or modify in-memory POOM state** that another session's read depends on. The backend processes one request at a time; session B is blocked while session A's `find_links` runs. The RESERVED/rejuvinate guard protocol ensures session A's own traversal is internally safe. Eviction of session B's previously-loaded crums is correct cache-flushing behavior: dirty crums are written to disk before being freed, and they will be re-loaded on session B's next access.

---

## Question 18 [gregory]

> After `deletevspanpm` removes a link's V→I mapping from the POOM, does the link's orgl structure in the granfilade remain byte-identical — same endset I-spans, same type reference — or could the deletion path touch the orgl's internal structure?

### Gregory's Answer

## KB Synthesis

The link orgl's internal structure — its endset I-spans, type reference, and all stored data — remains byte-identical after `deletevspanpm`. The deletion path never touches it.

## Why

The system has a strict three-layer architecture [SS-THREE-LAYER-MODEL]:

1. **I-space (link orgl)** — the link object at a permanent I-address (e.g., `1.1.0.1.0.1.0.2.1`), stored in the granfilade as content bytes. Contains the endset references (FROM, TO, TYPE). Cannot be modified by any deletion path.
2. **Spanfilade (DOCISPAN/endset index entries)** — append-only, no delete function exists [INV-SPANF-WRITE-ONLY].
3. **POOM (document V-stream)** — the V→I mapping in the document's orgl enfilade. This is the **only** layer `DELETEVSPAN` touches.

The code path is narrow and explicit. `dodeletevspan` calls `deletevspanpm` (`orglinks.c:145-152`), which calls `deletend` (`edit.c:31-76`) on the **document's** orgl — not on the link orgl. `deletend` removes or shifts bottom crums in the V-dimension of that document's POOM tree. There is no call to any granfilade write function, no call to any spanfilade function, and no traversal to the link orgl's own address [FC-LINK-DELETE-ISOLATION]:

> `edit.c:31-76` — `deletend()` removes crums in V-dimension without affecting I-space or spanfilade.

This is confirmed by the operational evidence from [SS-THREE-LAYER-MODEL]:

```
After DELETEVSPAN(2.1):
  I-space:     link orgl at 1.1.0.1.0.1.0.2.1 (unchanged)
  Spanfilade:  DOCISPAN entry still present (unchanged)
  POOM:        V-position 2.1 removed
  find_links(source_specs) → still finds the link
  follow_link(link_id, SOURCE) → still works
```

The frame condition is stated precisely in [ST-DELETE] (Finding 0040): `delete(D, 2.x, r) ⟹ ispace' = ispace ∧ spanfilade' = spanfilade`. And from [FC-GRANF-ON-DELETE]: "DELETE and REARRANGE are frame-condition-preserving with respect to the granfilade. These operations modify only the spanfilade (V-to-I mappings) and leave the granfilade (I-space content storage) completely unchanged."

The granfilade is append-only; there is no mechanism to modify or delete an existing orgl entry [INV-LINK-PERMANENCE]. The link orgl's bytes at its I-address are written once at creation and never touched again. `follow_link` succeeds after `DELETEVSPAN` precisely because `link2sporglset()` reads the link orgl directly from its ISA — and finds it byte-identical to what was written at creation time [SS-FOLLOWLINK].

## Code Exploration

I now have all the code I need to give a complete, cited answer. Here it is.

---

## Answer

**The link's orgl structure in the granfilade is untouched. `deletevspanpm` is strictly bounded to the document's POOM and cannot reach the link's orgl by any path in the call graph.**

Here is the full trace.

---

### The Entry Point

`dodeletevspan` at `do1.c:158-167` calls two things in sequence:

```c
findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
&& deletevspanpm (taskptr, docisaptr, docorgl, vspanptr)
```

`findorgl` at `granf1.c:17-41` locates the **document's** POOM via `fetchorglgr` (`granf2.c:22`), which looks up the document's ISA in the granfilade and follows the `cinfo.granstuff.orglstuff.orglptr` pointer to get the in-core POOM root. The `docorgl` returned is this document-POOM root — it has `cenftype == POOM`.

The link's orgl is stored in the granfilade under a **different** ISA (the link's ISA), in a separate GRAN bottom crum (`typecbc`) with `cinfo.infotype == GRANORGL`. It is never referenced by `docorgl`.

---

### `deletevspanpm` — `orglinks.c:145-152`

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

`deletend` is called with `(typecuc*)docorgl` — the document's POOM root. `logbertmodified` marks the **document** (not the link) as modified in the access-control layer. Neither call references the link's orgl.

---

### `deletend` — `edit.c:31-76`

```c
int deletend(typecuc *fullcrumptr, tumbler *origin, tumbler *width, INT index)
{
    ...
    makecutsnd (fullcrumptr, &knives);                          // [edit.c:44]
    newfindintersectionnd (fullcrumptr, &knives, &father, ...); // [edit.c:45]
    ...
    for (ptr = (typecuc *) findleftson (father); ptr; ptr = next) {
        switch (deletecutsectionnd ((typecorecrum*)ptr, &fgrasp, &knives)) {
          case 1:
            disown ((typecorecrum*)ptr);
            subtreefree ((typecorecrum*)ptr);  // [edit.c:60]
            break;
          case 2:
            tumblersub (&ptr->cdsp.dsas[index], width, &ptr->cdsp.dsas[index]); // [edit.c:63]
            break;
        }
    }
    setwispupwards (father, 1);
    recombine (father);
}
```

Every pointer touched here descends from `fullcrumptr` (== `docorgl`, a POOM). All crums in the document's POOM have `cenftype == POOM`. No pointer into the granfilade or into any link's orgl is ever dereferenced.

---

### The Critical Guard in `subtreefree` — `credel.c:413-432`

The one function that *can* reach a link's orgl from within the deletion machinery is `subtreefree`. It has a GRAN-specific branch:

```c
void subtreefree(typecorecrum *ptr)
{
    if (ptr->height > 0) {
        for (p = ((typecuc *)ptr)->leftson; p; ...) {
            disown (p);
            subtreefree (p);
        }
    } else if (ptr->cenftype == GRAN                                        // [credel.c:429]
            && ((typecbc *)ptr)->cinfo.infotype == GRANORGL
            && ((typecbc *)ptr)->cinfo.granstuff.orglstuff.orglincore)
        orglfree (((typecbc *)ptr)->cinfo.granstuff.orglstuff.orglptr);     // [credel.c:430]
    freecrum (ptr);
}
```

`orglfree` at `credel.c:470-490` would destroy the orgl tree by calling `subtreefree` on it and nulling the `orglptr`. This is the only path that could touch a link's orgl.

**This path is categorically unreachable from `deletend` operating on a POOM.** The condition at `credel.c:429` requires `ptr->cenftype == GRAN`. Every crum that `deletend` passes to `subtreefree` at `edit.c:60` was allocated as part of `docorgl` — a POOM tree — and therefore has `cenftype == POOM`. The guard fails immediately. `orglfree` is never called.

This type invariant is enforced by `createcrum` at `credel.c:518-596`: `cenftype` is set at allocation (`GRAN`, `SPAN`, or `POOM`) and never mutated except by `adopt` which copies the type from a sibling (`genf.c:438`: `new->cenftype = old->cenftype`) — so all crums within a POOM subtree stay `POOM`.

---

### `makecutsnd` and `slicecbcpm` — `ndcuts.c`

`makecutsnd` at `ndcuts.c:15-31` calls `makecutsdownnd` and `makecutsbackuptohere`, which call `slicecbcpm` at `ndcuts.c:373-450` to split bottom crums at cut points. `slicecbcpm` copies the `c2dinfo` struct (not `cinfo`) via `move2dinfo` at `ndcuts.c:447`:

```c
move2dinfo (&((type2dcbc *)ptr)->c2dinfo, &((type2dcbc *)new)->c2dinfo);
```

For GRAN crums it copies only `infotype` (`ndcuts.c:81-83`), not the `orglptr`. But GRAN crums are not present in a POOM tree at all — the relevant bottom crum type is `type2dcbc`, which holds `c2dinfo.homedoc` (the source document's ISA), not an orgl pointer. No path in `slicecbcpm` reads or writes any link's orgl.

---

### Where the Link's Orgl Actually Lives

`createorglingranf` → `createorglgr` at `granf2.c:111-128`:

```c
locinfo.infotype = GRANORGL;
locinfo.granstuff.orglstuff.orglptr = createenf (POOM);    // [granf2.c:120]
reserve ((typecorecrum*)locinfo.granstuff.orglstuff.orglptr);
locinfo.granstuff.orglstuff.orglincore = TRUE;
locinfo.granstuff.orglstuff.diskorglptr.diskblocknumber = DISKPTRNULL;
insertseq ((typecuc*)fullcrumptr, isaptr, &locinfo);        // [granf2.c:125]
```

The link's orgl is a freshly allocated POOM (`createenf(POOM)`), stored as the payload of a GRAN bottom crum (`typecbc`) inserted into the granfilade (`fullcrumptr == granf`) at the link's ISA address. It lives in a completely separate subtree from the document's POOM.

`deletevspanpm` never calls `fetchorglgr`, never traverses the granfilade, and never dereferences a GRAN crum. The two structures — document POOM and link orgl — share no tree ancestry and no pointer relationship reachable from the deletion path.

---

### Summary

After `deletevspanpm` completes:

- **The document's POOM** (`docorgl`) has had crums removed or their V-displacements decremented to reflect the deleted V-span. The crums that represented the link's V→I mapping in the document are gone (or shrunk).
- **The link's orgl** — stored in the granfilade under the link's ISA, containing the endset I-spans and type reference — is **byte-identical**. The deletion path is confined to the document's POOM subtree. `subtreefree`'s `orglfree` branch requires `cenftype == GRAN`, which is false for every crum in a POOM tree. `deletend` never touches the granfilade.

The link's endset I-spans, type reference (`homedoc` in `c2dinfo`), and the complete internal V↔I mapping structure within the link's own POOM are unaffected.

---

## Question 19 [gregory]

> When `strongsub` fires its exponent guard during DELETE shifting (returning the link position unchanged), does this guarantee extend to ALL entries with higher exponents than the deletion width, or only to entries in the specific `0.2.x` link subspace range?

### Gregory's Answer

## KB Synthesis

## The `strongsub` Exponent Guard Is Fully General — Not Subspace-Specific

The guard extends to **all entries whose V-displacement exponent exceeds the deletion width's exponent**, with no special-casing for the `0.2.x` link range. The KB is explicit about this.

### The Mechanism

From [SS-TUMBLER] Finding 0055, the `strongsub` guard is:

```c
if (bptr->exp < aptr->exp) { movetumbler(aptr, cptr); return(0); }
```

This is a pure comparison of the `exp` fields of two tumblers. `strongsub` has no knowledge of subspaces, V-address semantics, or whether a displacement belongs to a link orgl or a text atom.

### Why Link Crums Are Protected in Practice

The incidental alignment that makes subspace isolation work is:

- **Text deletion widths** (e.g., `0.3` for 3 characters): `exp = -1`  
- **Text crum displacements** (e.g., `0.5`, relative to parent grasp): `exp = -1`  
- **Link crum displacements** at `2.x` (e.g., `1.0` relative to root): `exp = 0`

So `strongsub(link_disp [exp=0], delete_width [exp=-1])`: `b.exp(-1) < a.exp(0)` → guard fires, displacement returned unchanged.

But `strongsub(text_disp [exp=-1], delete_width [exp=-1])`: exponents match → subtraction proceeds, text is shifted.

[FC-SUBSPACE] Finding 0055 states this directly:
> Text crums within the deletion's subspace have displacements at exp=-1 (same level as the width), so `strongsub` proceeds to the main subtraction path and they shift. **Link crums at exp=0 are unaffected because `strongsub` returns them unchanged.**

### Generality Confirmed — and Its Fragility Noted

[INT-DELETE-SUBSPACE-ASYMMETRY] Finding 0055 makes the generality explicit:

> For DELETE, the frame condition depends on the invariant that **deletion widths always have a lower tumbler exponent than cross-subspace entry displacements**. If `strongsub` were modified to handle cross-exponent subtraction correctly, DELETE would break subspace isolation while INSERT would remain safe.

The protection is general: **any POOM entry whose V-displacement has a higher exponent than the deletion width is protected**, regardless of what subspace it belongs to. The `0.2.x` link entries are protected because they happen to carry `exp=0` displacements, not because the implementation has any awareness of the link subspace.

### The Corrected Formal Statement

From [ST-DELETE] / [PRE-DELETE] Finding 0055, the postcondition for DELETE shifting is:

```
∀ entry ∈ poom(doc) : entry.vpos > delete_end ∧ entry.vpos.exp = width.exp
  ==> entry.vpos' = entry.vpos - delete_width

∀ entry ∈ poom(doc) : entry.vpos.exp > width.exp
  ==> entry.vpos' = entry.vpos   (guard fires, no-op)
```

The discriminating predicate is `entry.vpos.exp vs width.exp`, not `which subspace`.

### Implication for Violations of the Subspace Convention

If text were placed at V-position `2.1` (a violation confirmed possible by [PRE-INSERT] Finding 0049), those text bytes would have V-displacement crums at `exp=-1`. The `strongsub` guard would NOT protect them during a text-subspace DELETE — they would be shifted into negative territory or corrupted just like same-subspace text, even though they are nominally "in the link subspace." The guard offers no subspace-semantic protection, only exponent-arithmetic protection.

## Code Exploration

---

## Answer

The `strongsub` exponent guard is a **general arithmetic property**, not a subspace-specific guard. It protects **all** entries whose `exp` field is greater than the deletion width's `exp` — not only entries in any specific link subspace range. The `0.2.x` premise in the question is also factually incorrect about the actual link V-address structure. Here is the full trace.

---

### 1. The exponent guard itself

`tumble.c:534–565`:

```c
int strongsub(tumbler *aptr, tumbler *bptr, tumbler *cptr)
{
    tumbler answer;
    register INT i, j;

    tumblerclear(&answer);
    if (tumblereq (aptr, bptr)) {
        movetumbler (&answer, cptr);
        return(0);
    }
    if (bptr->exp < aptr->exp) {   // ← THE EXPONENT GUARD
        movetumbler(aptr,cptr);
        return(0);
    }
    ...
```

The guard at `tumble.c:544–546` fires when `bptr->exp < aptr->exp`. It returns `aptr` unchanged — the subtraction is skipped entirely. The condition inspects **only the `exp` fields**. There is no address range check, no subspace identifier, no comparison to any tumbler value. It is purely: *if b's scale is at a finer hierarchy level than a's scale, a is unaffected.*

`strongsub` ignores the `sign` field entirely — only `exp` and `mantissa` are used. The sign is applied by the caller (`tumble.c:385–389`):

```c
} else if (abscmp (aptr, bptr) == GREATER) {
    strongsub (aptr, bptr, cptr);
    cptr->sign = aptr->sign;
```

---

### 2. The DELETE shifting call path

`dodeletevspan` → `deletevspanpm` → `deletend`, in that order:

**`do1.c:158–167`** — top-level entry:
```c
bool dodeletevspan(typetask *taskptr, typeisa *docisaptr, typevspan *vspanptr)
{
    typeorgl docorgl;
    return (
       findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
    && deletevspanpm (taskptr, docisaptr, docorgl, vspanptr));
}
```

**`orglinks.c:145–152`** — strips to the core op:
```c
bool deletevspanpm(typetask *taskptr, tumbler *docisaptr, typeorgl docorgl, typevspan *vspanptr)
{
    if (iszerotumbler(&vspanptr->width))
        return (FALSE);
    deletend((typecuc*)docorgl, &vspanptr->stream, &vspanptr->width, V);
    ...
}
```

**`edit.c:31–76`** — the shift itself, case 2:
```c
case 2:
    tumblersub (&ptr->cdsp.dsas[index], width, &ptr->cdsp.dsas[index]);
    break;
```

`tumblersub(a, b, c)` negates `b` and calls `tumbleradd(a, -b, c)` (`tumble.c:418–440`). When `|a| > |b|`, `functiontumbleradd` dispatches to `strongsub(a, -b, c)` at `tumble.c:385`. The `exp` of `-b` is the same as the `exp` of the deletion `width` (negation only flips `sign`).

So the guard condition during DELETE shifting is:

> **`deletion_width.exp < crum_address.exp`**

No further condition. No address-range check.

---

### 3. What exponents actually appear in each subspace

**Text crums** in the POOM: inserted at VSAs computed by `findvsatoappend` (orglinks.c:29–49). The first text address is built by:
```c
tumblerincrement (vsaptr, 0, 1, vsaptr);   // vsaptr = 1
tumblerincrement (vsaptr, 1, 1, vsaptr);   // vsaptr = 1.1
```
Result: `{exp=0, mantissa=[1,1,0,...]}`. Text crums are at `exp=0`.

**Link crums** in the source document's POOM: placed by `findnextlinkvsa` (`do2.c:151–167`) at `firstlink`:
```c
tumblerincrement (&firstlink, 0, 2, &firstlink);   // firstlink = 2
tumblerincrement (&firstlink, 1, 1, &firstlink);   // firstlink = 2.1
```
Result: `{exp=0, mantissa=[2,1,0,...]}`. Source-document link crums are at `exp=0`.

**Link endpoint VSAs** inside a link document, set by `setlinkvsas` (`do2.c:169–183`): `1.1`, `2.1`, `3.1` — all `exp=0`.

**`islinkcrum`** (`orglinks.c:255–261`) identifies link crums by:
```c
if(crumptr->cdsp.dsas[V].mantissa[0] == 1 && crumptr->cdsp.dsas[V].mantissa[1] != 0)
```
This matches addresses of the form `1.x` (x≠0), with `exp=0`. **Not `0.2.x`** (which would be `exp=-1` after `tumblerjustify`). The link subspace V-addresses in this codebase are at integer scale (`exp=0`), not at sub-address scale (`exp=-1`).

The only place where link-related tumblers acquire `exp=-1` is the **V-width of POOM crums representing link entries**, computed in `insertpm` (`orglinks.c:114–117`):
```c
shift = tumblerlength (vsaptr) - 1;   // = 1, for a 2-story VSA like 1.1
inc = tumblerintdiff (&lwidth, &zero);
tumblerincrement (&zero, shift, inc, &crumwidth.dsas[V]);
```
`tumblerincrement(&zero, 1, inc, ...)` → `exp=-1`. The **width** of a link entry's POOM crum has `exp=-1`, but the **address** (origin) remains `exp=0`.

---

### 4. Scope of the guarantee

The exponent guard returns `aptr` unchanged whenever:

```
bptr->exp < aptr->exp
```

Because `exp ≤ 0` always (`tumblercheckptr`, `tumble.c:174–179` enforces this), this means: *b is at a finer (more deeply nested) granularity level than a*. Any such crum — text, link, metadata — is returned unchanged. The condition is blind to address values. It does not know about subspaces.

If a deletion has `width.exp = -1` (e.g., deleting a link-width V-span), then **every crum with `address.exp = 0`** — whether it is a text crum, a link crum, or any other kind — triggers the guard and is returned unchanged. Conversely, if a deletion has `width.exp = 0` (typical integer text deletion), the guard never fires for any `exp=0` crum (`0 < 0` is false).

The `0.2.x` range claimed in the question does not correspond to how Udanax Green organizes link V-addresses. The actual link subspace entries in both source documents and link documents use `exp=0` addresses (like `1.1`, `2.1`, `3.1`). The exponent guard's behaviour for those addresses during integer-width deletions (where `width.exp=0`) is: the condition `0 < 0` is false — **the guard does not fire at all** for standard text deletions touching `exp=0` link crums.

---

### Summary

The guarantee from the exponent guard is **universal across all address space entries where `address.exp > deletion_width.exp`**. It is not scoped to `0.2.x` or any other subspace. The guard has no subspace logic whatsoever — only exponent arithmetic. The `0.2.x` link subspace framing is not supported by the code: link V-addresses in Udanax Green are at `exp=0` (e.g., `2.1`, `3.1`), not `exp=-1`. The only `exp=-1` values associated with links are the V-**widths** of POOM crums created during link insertion (`insertpm`, `orglinks.c:114–117`), not their origin addresses.

---

## Question 20 [gregory]

> If two documents each transclude the same I-address range and one document performs INSERT at a V-position before the transcluded content, does the shifting in that document's POOM leave the other document's POOM V-addresses completely unchanged, including the displacement values stored at intermediate tree nodes?

### Gregory's Answer

## KB Synthesis

Yes, the second document's POOM is completely unchanged — including all intermediate tree node displacement values. Here is the chain of reasoning:

## Documents Have Independent POOM Trees

Each document maintains its own POOM enfilade [SS-POOM-MUTABILITY]. The POOM is a per-document structure; there is no shared POOM across documents. The two documents that transclude the same I-address range each hold their own separate `(V-address → I-address)` mapping trees.

## INSERT Operates On Exactly One Document's POOM

`doinsert` → `docopy` → `insertpm` → `insertnd` → `makegappm` operates on the target document's orgl only [ST-INSERT, Finding 0052]. The `makegappm` knife mechanism classifies and shifts crums within the **target document's** POOM tree. No code path in the insert chain touches any other document's orgl.

## The Frame Condition Is Unconditional

[FC-INSERT-IADDR] states this explicitly: "All existing V-to-I mappings outside the target document are completely untouched." This covers both bottom crum V-positions and the displacement values (`cdsp.dsas[V]`) stored at intermediate tree nodes.

## The Displacement Recalculation Is Local

After insertion, `setwispupwards` recalculates root displacement by absorbing the minimum child displacement and adjusting children to relative values [ST-INSERT, Finding 0066; SS-ENFILADE-RELATIVE-ADDRESSING]. This traversal walks only the target document's enfilade tree. The second document's `root.cdsp`, `node.cdsp`, and `node.cwid` at every level are not read, not written, and not recomputed.

## The Shared I-Addresses Are Untouched

The I-addresses themselves are immutable in the granfilade [INV-IADDR-IMMUTABILITY]. The second document's POOM continues to map its V-addresses to the same I-addresses as before. The first document's INSERT allocates fresh I-addresses (for the newly inserted content) and shifts existing V-addresses within its own POOM, but neither action propagates to the second document [FC-INSERT-IADDR, FC-DELETE-CROSS-DOC].

## Summary

The second document's POOM — every bottom crum, every intermediate node, every `cdsp` and `cwid` field at every height — is completely unchanged by the INSERT in the first document. The two POOMs are independent data structures that happen to reference overlapping I-addresses. Operations on one cannot reach the other.

## Code Exploration

I now have everything needed for a complete, cited answer.

---

## Answer: Per-Document POOM Isolation Under INSERT

**Short answer: Yes, Document B's POOM is completely unaffected — including all intermediate-node displacement values.** The two POOMs share no tree structure. The isolation is absolute by architecture.

---

### The Architecture: One POOM Per Document

Each document owns a completely separate POOM tree. When a document is created, `createorglgr` (granf2.c:111-128) allocates a fresh POOM root:

```c
locinfo.granstuff.orglstuff.orglptr = createenf (POOM);   /* granf2.c:120 */
```

This POOM root pointer is stored inside a single granfilade bottom crum, indexed by the document's ISA address. `fetchorglgr` (granf2.c:22-81) retrieves it:

```c
ret = context->corecrum->cinfo.granstuff.orglstuff.orglptr;   /* granf2.c:62 */
```

Document A and Document B each have their own `orglptr`—entirely separate `typecuc *` trees with no shared nodes at any level.

---

### The INSERT Call Chain

**1. `doinsert` (do1.c:87-123)**  
Allocates I-address space in the granfilade (permascroll), then calls:

```c
ret = (inserttextingranf(taskptr, granf, &hint, textset, &ispanset)
    && docopy (taskptr, docisaptr, vsaptr, ispanset)   /* do1.c:118-119 */
```

**2. `docopy` (do1.c:45-64)**  
Retrieves Document A's POOM root and calls `insertpm` against it:

```c
findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)   /* do1.c:55 */
...
&& insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)   /* do1.c:60 */
```

`docorgl` is Document A's POOM root. `findorgl` for Document B would return a different pointer stored at a different granfilade address. Neither function is called for Document B's ISA during Document A's insert.

**3. `insertpm` (orglinks.c:75-134)**  
Passes Document A's orgl directly into `insertnd`:

```c
insertnd (taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);   /* orglinks.c:130 */
```

The parameter is `orgl`, which is Document A's POOM root. Document B's POOM root is never touched.

**4. `insertnd` (insertnd.c:15-111)**  
For the `POOM` case, calls `makegappm` and `doinsertnd`, both on `fullcrumptr` (Document A's POOM root):

```c
case POOM:
    makegappm (taskptr, fullcrumptr, origin, width);   /* insertnd.c:54 */
    ...
    bothertorecombine=doinsertnd(fullcrumptr,origin,width,infoptr,index);   /* insertnd.c:57 */
    break;
```

---

### Where V-Address Displacements Are Modified

The V-address shifting happens entirely inside `makegappm` (insertnd.c:124-172). Here is the full traversal that updates displacements:

```c
makecutsnd (fullcrumptr, &knives);                                       /* insertnd.c:148 */
newfindintersectionnd (fullcrumptr, &knives, &father, &foffset);         /* insertnd.c:149 */
prologuend ((typecorecrum*)father, &foffset, &fgrasp, (typedsp*)NULL);   /* insertnd.c:150 */
for (ptr = findleftson (father); ptr; ptr = findrightbro (ptr)) {        /* insertnd.c:151 */
    i = insertcutsectionnd(ptr, &fgrasp, &knives);
    switch (i) {
        case 1:
            tumbleradd(&ptr->cdsp.dsas[V],&width->dsas[V],&ptr->cdsp.dsas[V]);  /* insertnd.c:162 */
            ivemodified (ptr);
            break;
    }
}
setwidnd(father);
setwispupwards (findfather ((typecorecrum*)father),1);
```

Every operation here is bounded to Document A's POOM:

- `fullcrumptr` is Document A's POOM root (the `typecuc *` returned by `fetchorglgr` for Document A's ISA).
- `makecutsnd(fullcrumptr, &knives)` cuts only within Document A's POOM subtree.
- `newfindintersectionnd(fullcrumptr, ...)` finds an intersection node only within Document A's POOM.
- `father` is some intermediate node **inside Document A's POOM**. Its `leftson` chain contains only Document A's POOM nodes.
- The loop `findleftson(father) → findrightbro(ptr)` traverses only siblings within Document A's POOM. It cannot reach Document B's POOM because the two trees share no nodes.
- The displacement write `ptr->cdsp.dsas[V] += width->dsas[V]` (insertnd.c:162) touches only nodes in Document A's POOM.

The subsequent `recombine(fullcrumptr)` (insertnd.c:76) is also scoped to `fullcrumptr`—Document A's POOM—and the `setwispupwards` calls (insertnd.c:56,58) only propagate upward through Document A's POOM tree, stopping at `isfullcrum` (enf.h:176: `#define isfullcrum(x) ((bool)((typecorecrum *)(x))->isapex)`), which is Document A's POOM root.

---

### Why the Shared I-Address Content Is Irrelevant Here

Both documents transclude the same I-address range (permascroll addresses). The permascroll (granfilade) stores the actual text content. But transclusion is a **read relationship**—the POOM maps a document's V-addresses to I-addresses. The permascroll itself is never modified by an insert into either document; only Document A's POOM is modified. Document B's POOM still maps its own V-addresses to the same I-addresses it always did, and those V-address mappings are untouched.

---

### Summary

The V-address isolation between documents is **complete and structural**, not a policy choice. Each document's POOM is a separate `typecuc` tree created by `createenf(POOM)` (granf2.c:120) and stored under that document's granfilade entry (granf2.c:62). All POOM mutation functions (`makegappm`, `doinsertnd`, `insertcbcnd`, `recombine`, `setwispupwards`) receive `fullcrumptr` and traverse only within that tree. No traversal can cross POOM boundaries because the trees share no node pointers. Document B's intermediate displacement values (`cdsp.dsas[V]` on every node in its POOM) are never read or written during Document A's insert.
