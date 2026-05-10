# Consultation Answers — Address Permanence

**Inquiry:** What guarantees must the system provide about address stability? Once content is assigned an address, what operations may and may not affect that assignment?
**Date:** 2026-03-07 02:19
**Questions:** 20 (10 nelson, 10 gregory)

---

## Question 1 [nelson]

> Once content is assigned an address in the system, may any operation — editing, deletion, or reorganization — ever cause that address to refer to different content?

### Nelson's Answer

# No. An I-space address is permanently bound to its content.

This is one of the most fundamental invariants of the system. Once a byte is created and assigned its I-space address, no operation — editing, deletion, rearrangement, versioning, transclusion, or any other — can ever cause that address to refer to different content.

## The guarantee is structural, not policy

The system has **two address spaces**, and they behave differently:

**I-space (invariant space):** Content lives here permanently. Addresses are absolute and immutable.

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

**V-space (virtual space):** A document's current arrangement of content. V-addresses *do* shift with editing — that is their nature:

> "The v-stream addresses of any following characters in the document are increased by the length of the inserted text." [LM 4/66]

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." [LM 4/11]

But V-addresses are positional indices into an arrangement. They do not *name* content — they locate it within a view. The I-address is the name.

## Why no operation can violate this

**Editing** changes V-space arrangements only. I-space is append-only:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

**Deletion** removes content from V-space, not I-space:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

**Rearrangement** is a pure V-space operation. The I-space addresses of the rearranged bytes are unchanged.

**Versioning** creates a new V-space arrangement over the same I-space content:

> "There is thus no 'basic' version of a document set apart from other versions — 'alternative' versions — any more than one arrangement of the same materials is a priori better than other arrangements." [LM 2/19]

**Transclusion (COPY)** creates a V-space reference to existing I-space content. No new I-space content is created; the original I-address is shared.

## The tumbler guarantee

At the addressing level, Nelson is explicit:

> "New items may be continually inserted in tumbler-space while the other addresses remain valid. This means that any address of any document in an ever-growing network may be specified by a permanent tumbler address." [LM 4/19]

The forking mechanism ensures new addresses are always created *below* existing ones — by adding digits to the right. No existing address is ever reassigned or reinterpreted.

## Why this matters

The entire system depends on this invariant:

- **Links survive editing** because they point to I-space addresses, not V-space positions: "links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them." [LM 4/42]

- **Attribution is structural** because the I-address encodes the home document: "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

- **Correspondence works** because shared I-space origin is how the system identifies matching parts across versions.

- **Transclusion works** because including content by reference requires that the reference always resolves to the same content.

## Summary

| Address space | Can it refer to different content? | Why |
|---|---|---|
| **I-space** | **Never.** | Append-only; addresses are permanent bindings to content |
| **V-space** | Positions shift with editing | V-addresses are ephemeral indices into an arrangement, not content identifiers |

The I-space address is the identity of the content. To allow it to refer to something else would destroy permanence, attribution, link survivability, transclusion integrity, and version correspondence — effectively every guarantee the system makes.

---

## Question 2 [nelson]

> When new content is inserted into a document, must the addresses of all previously existing content in that document remain unchanged?

### Nelson's Answer

## Answer: It Depends on Which Address Space

Xanadu has **two address spaces**, and the answer is different for each.

### I-Space Addresses: YES — Always Unchanged

Every byte's permanent identity address (its I-space tumbler) is immutable. Insertion, deletion, rearrangement — nothing changes an I-space address. This is the foundational guarantee:

> "New items may be continually inserted in tumbler-space while the other addresses remain valid. This means that any address of any document in an ever-growing network may be specified by a permanent tumbler address." [LM 4/19]

The I-space address encodes where the byte was *born* (server, account, document, element position). That never changes regardless of what happens in any document that references it.

### V-Space Addresses: NO — They Explicitly Shift

V-space addresses (positions in the document's virtual byte stream) change on every edit. Nelson specifies this directly in the INSERT operation:

> "This inserts \<text set\> in document \<doc id\> at \<doc vsa\>. The v-stream addresses of any following characters in the document are increased by the length of the inserted text." [LM 4/66]

And from the V-space description:

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." [LM 4/11]

V-addresses are dense and contiguous (1, 2, 3, ...). When you insert 10 bytes at position 5, everything after position 5 shifts by 10. This is by design — V-space is a *view*, not an identity.

### Why This Works: Links Point to I-Space

The architectural reason for the separation is link survivability:

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." [LM 4/30]

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes. This has a crucial advantage: it means that links can survive editing." [LM 4/42]

Links attach to bytes via their permanent I-space identity, not their ephemeral V-space position. So insertion shifts V-addresses but leaves all links intact.

### Summary

| Address type | Changes on INSERT? | Why? |
|---|---|---|
| **I-space** (permanent identity) | No — immutable forever | Content identity is permanent |
| **V-space** (document position) | Yes — shifts after insertion point | V-space is a mutable view |
| **Tumbler** (docuverse-wide) | No — valid forever | The whole point of tumblers |

The genius of the design is that users work with V-space (intuitive sequential positions) while the system preserves I-space (permanent identity). V-space is disposable; I-space is eternal.

---

## Question 3 [nelson]

> If a user deletes a passage from their document, does the address that once referred to that passage become permanently unusable, or may it be reassigned?

### Nelson's Answer

## The Address Is Never Reassigned — But the Answer Depends on Which Address Space

Xanadu has two address spaces, and they behave differently on deletion.

### I-Space Address: Permanently Occupied, Never Reassigned

The I-space (invariant space) address of the deleted passage remains permanently valid and permanently refers to that exact content. The content is not destroyed — it enters the state Nelson labels:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

The bytes still exist at their I-space address. They can be retrieved through historical backtrack or through other documents that transclude them:

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

I-space is append-only. Nothing stored there is ever overwritten or reassigned:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

The I-space address of that passage will refer to that passage for the life of the docuverse. It cannot be given to new content.

### V-Space Address: Positional, Shifts on Editing

The V-space (virtual space) address is a different matter. V-addresses are positional — like array indices, not permanent identifiers. They form a dense, contiguous sequence:

> "The digit after the one indicates the byte position in the current ordering of bytes. This is its virtual stream address." [LM 4/30]

When you delete content, the gap closes. Nelson explicitly states that insertion shifts subsequent addresses:

> "The v-stream addresses of any following characters in the document are increased by the length of the inserted text." [LM 4/66]

Deletion is the inverse: subsequent V-addresses decrease to fill the gap. So the V-address number that once referred to your deleted passage now refers to whatever content follows the deletion point. But this is not "reassignment" — V-addresses were never permanent identifiers. They describe *where content sits right now*, not *what content is*.

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." [LM 4/11]

### Why This Works: Links Point to I-Space

The entire architecture depends on this separation. Links attach to I-space addresses (permanent content identity), not V-space addresses (ephemeral positions):

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." [LM 4/30]

So when a passage is deleted:
- Its **I-space address** remains permanently occupied — the content is still there, still linkable, still retrievable through historical backtrack or transclusion
- Its **V-space position** is reclaimed — subsequent content shifts to fill the gap
- **Links to the passage** still work — they point to I-space, which is unaffected

The principle is absolute: no I-space address is ever reused. The tumbler guarantee applies:

> "New items may be continually inserted in tumbler-space while the other addresses remain valid." [LM 4/19]

"Remain valid" means permanently. An I-space address, once baptized for a piece of content, belongs to that content forever.

---

## Question 4 [nelson]

> Must the address of shared content remain identical across every document that includes it, or may each document assign its own address to the same content?

### Nelson's Answer

## The I-address is identical; the V-address differs

Xanadu's two-address architecture answers this question directly. Shared content has **one permanent identity** (I-space) but **many positions** (V-space, one per including document).

### I-Space: Identity is universal and immutable

When document B transcludes content from document A, B's virtual byte stream references the **same I-space addresses** as A. The content is not copied — it is included by reference to its permanent home location.

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

The I-address encodes the originating server, user, document, and element position. It is permanent and never changes. Content identity is based on creation, not on value — two documents with identical text created independently have **different** I-addresses, while transcluded content **shares** the same I-address.

### V-Space: Position is per-document and ephemeral

Each document assigns its own V-space addresses to the same content. If document A has "hello" at V-positions 1–5 and document B transcludes that same "hello" at V-positions 47–51, the V-addresses differ but the I-addresses are identical.

> "Logical addressing of the byte stream is in the form of virtual spans, or vspans. These are sequences of bytes in the document's virtual byte stream, regardless of their native origin." [LM 4/11]

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." [LM 4/11]

V-addresses shift with every insertion, deletion, and rearrangement. They are dense (no gaps), sequential, and local to the document's current version. The document **is** its V→I mapping.

### Why shared I-addresses are essential

Three system capabilities depend on I-address identity being preserved across all including documents:

**1. FINDDOCSCONTAINING** — finds all documents that include specified content by searching shared I-addresses:

> "This returns a list of all documents containing any portion of the material included by \<vspec set\>." [LM 4/70]

If each document assigned its own identity to shared content, this operation would be impossible.

**2. Correspondence** — the ability to compare versions and find matching parts depends on shared I-space origin:

> "Of course, a facility that holds multiple versions of the same material, and allows historical backtrack, is not terribly useful unless it can help you intercompare them in detail—unless it can show you, word for word, what parts of two versions are the same." [LM 2/20]

**3. Origin traceability** — attribution is structural because the I-address encodes who created the content:

> "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

### The COPY operation makes this explicit

The FEBE COPY command is the transclusion primitive. It places content into a new document at a specified V-position while preserving I-address identity:

> "The material determined by \<spec set\> is copied to the document determined by \<doc id\> at the address determined by \<doc vsa\>." [LM 4/67]

This creates a new V-space mapping (the `<doc vsa>` is a V-address in the target document) pointing to existing I-space content. No new I-addresses are created.

### Summary

| Address type | Shared across documents? | Purpose |
|---|---|---|
| **I-address** | **Yes — must be identical** | Permanent identity, attribution, origin tracing |
| **V-address** | **No — each document assigns its own** | Current position in this document's arrangement |

The entire architecture rests on this separation. I-space permanence enables permanent citation, link survivability, automatic attribution, and royalty tracking. V-space flexibility enables editing, versioning, and per-document arrangement. The document is the mapping between the two.

---

## Question 5 [nelson]

> When a document undergoes a series of edits across multiple versions, must every piece of surviving content retain the same address it had in the original version?

### Nelson's Answer

# Address Permanence Across Versions

The answer depends on **which address space** you mean. Xanadu has two, and they behave oppositely.

## I-Space Addresses: Yes, Permanent Forever

Every byte ever created gets a permanent I-space address that never changes, regardless of what happens to any document or version. This is the foundational guarantee of the entire architecture.

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

The I-address encodes origin (Node.0.User.0.Document.0.Element) and is immutable. A byte created in document D at I-position 47 stays at that I-address through every version, every transclusion, every edit — forever.

## V-Space Addresses: No, They Change Constantly

V-space addresses are explicitly ephemeral. Nelson says so directly:

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." [LM 4/11]

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." [LM 4/30]

The INSERT operation specification makes this concrete:

> "The v-stream addresses of any following characters in the document are increased by the length of the inserted text." [LM 4/66]

Insert 10 bytes at V-position 5, and everything after position 5 shifts by 10. V-addresses are dense sequential positions (1, 2, 3...) that reflow with every edit.

## The Architecture Depends on This Distinction

The whole design rests on separating **identity** (I-space, permanent) from **arrangement** (V-space, mutable):

- **Links point to I-space** → survive editing
- **Users work with V-space** → intuitive sequential positions
- **Versions are different V-space arrangements** over the same I-space content
- **"Deletion" removes from V-space only** → I-space content persists

> "Links between bytes can survive deletions, insertions and rearrangements, if anything is left at each end." [LM 4/42-4/43]

Links survive precisely *because* they attach to permanent I-addresses, not shifting V-addresses. If links pointed to V-positions, every insertion would break every link after the insertion point.

## Each Version Has Its Own V-Space

When you create a new version (CREATENEWVERSION), you get a new V-space arrangement that initially mirrors the source. Subsequent edits to either version change only that version's V-space. The underlying I-space content is shared.

> "There is thus no 'basic' version of a document set apart from other versions—'alternative' versions—any more than one arrangement of the same materials is a priori better than other arrangements." [LM 2/19]

## Summary

| Address type | Survives editing? | Survives versioning? |
|---|---|---|
| **I-space** (identity) | Yes — permanent, immutable | Yes — shared across all versions |
| **V-space** (arrangement) | No — shifts on every edit | Each version has its own V-stream |

Every piece of surviving content retains its **I-space address** permanently. Its **V-space position** changes with every edit and differs across versions. This is not a limitation — it is the core architectural insight that makes permanent linking, version comparison, and transclusion possible.

---

## Question 6 [nelson]

> Do links depend on address stability — that is, must a link's endpoint address continue to reach the same content regardless of what editing has occurred around it?

### Nelson's Answer

# Yes — and the architecture guarantees it structurally

Links depend on **I-space address stability**, which is absolute and immutable by design. They do **not** depend on V-space address stability, which is explicitly ephemeral. This is the central architectural insight that distinguishes Xanadu links from web hyperlinks.

## The two address spaces

Link endsets point to bytes identified by their permanent I-space addresses. Editing only changes V-space — the document's current arrangement of content. I-space content never moves, never changes, never gets overwritten.

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." [LM 4/30]

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." [LM 4/11]

The V-address changes constantly during editing. The I-address never changes. Links point to I-addresses.

## Links as straps between bytes

Nelson visualizes links not as arrows between positions but as physical straps binding specific bytes:

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes. This has a crucial advantage: it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them. This also works for alternative versions in which part of each end has survived." [LM 4/42]

The "strap" metaphor is precise. A strap binds to the thing itself, not to where the thing happens to be sitting. Move the thing — the strap goes with it. Rearrange the shelf — the strap doesn't care.

## What editing does and does not affect

| Operation | V-space effect | I-space effect | Link effect |
|-----------|---------------|----------------|-------------|
| **INSERT** | Shifts V-addresses after insertion point | New bytes get new I-addresses | None — existing I-addresses untouched |
| **DELETE** | Removes V-space mapping | None — bytes remain in I-space | None — link still points to I-space bytes |
| **REARRANGE** | Changes V-address ordering | None | None |
| **COPY** (transclusion) | New V-space mapping to existing I-content | None | None |

The survivability guarantee from page 4/43 states it plainly:

> "SURVIVABILITY: Links between bytes can survive deletions, insertions and rearrangements, **if anything is left at each end.**" [LM 4/43]

## The only way to break a link

A link fails only when **all** bytes at one endset are deleted from every V-space view. Even then, the I-space content still exists — the bytes are merely "not currently addressable, awaiting historical backtrack functions, may remain included in other versions" [LM 4/9]. The link still structurally points to real I-space content; it's just that no current document arrangement exposes those bytes.

## Cross-version stability

This architecture also enables links to work across versions:

> "Links may be refractively followed from a point or span in one version to corresponding places in any other version. Thus a link to one version of a Prismatic Document is a link to all versions." [LM 2/26]

Because versions share I-space content, a link made against version 1 automatically reaches the same content in version 5 — the system traces correspondence through shared I-addresses.

## Summary

The answer to your question is **yes, by construction**. A link's endpoint address always reaches the same content because:

1. Endsets point to I-space addresses
2. I-space addresses are permanent and immutable
3. Content at an I-space address never changes
4. Editing only modifies V-space (the arrangement)
5. Therefore no editing operation can cause a link's endpoint to reach different content

This is not a feature of the link mechanism — it is a consequence of the address space design. Nelson separated content identity (I-space) from content arrangement (V-space) precisely so that links, citations, and transclusions would be immune to editing. The address stability that links depend on is the deepest invariant in the system.

---

## Question 7 [nelson]

> If two users independently incorporate the same shared passage, must the system guarantee that both users' references resolve to the same address?

### Nelson's Answer

## Yes — this is architecturally guaranteed and definitionally required.

When two users both transclude the same passage from a source document, both references **must** resolve to the same I-space address. This is not an optional guarantee — it is the mechanism by which transclusion works at all.

### Why: COPY creates V-space mappings, not new I-space content

The COPY operation in FEBE does not duplicate bytes. It creates a new V-space reference to **existing** I-space content:

> "The material determined by \<spec set\> is copied to the document determined by \<doc id\> at the address determined by \<doc vsa\>." [LM 4/67]

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

Both users' documents contain inclusions — V-space positions that map to the **same** I-space addresses in the source document. The bytes are fetched from their "home locations" at read time. There is only one home.

### The critical distinction: creation vs. transclusion

Content identity is based on **creation**, not **value**:

- If Alice and Bob independently **type** the same words, they get **different** I-addresses (different creation events, different home documents).
- If Alice and Bob both **COPY** (transclude) from the same source passage, they share the **same** I-addresses — because neither created new content; both referenced existing content.

This distinction is stated in the provenance design:

> "Content identity is based on creation, not value. Two documents with identical text created independently have DIFFERENT I-addresses. Transcluded content SHARES the same I-address."

### Three system capabilities depend on this guarantee

**1. FINDDOCSCONTAINING** — Finding all documents that include a given passage requires shared I-addresses:

> "This returns a list of all documents containing any of the material specified by the span addresses, regardless of where the native copies are located." [LM 4/63]

If two transclusions of the same passage resolved to different addresses, this operation could not work.

**2. Correspondence** — Version comparison depends on shared I-space origin:

> "Correspondence is a RELATION — the relationship between V-space positions that share the same I-space origin."

Shared I-addresses are how the system knows two passages "correspond" without being told.

**3. Automatic royalty** — The original author gets paid whenever their bytes are delivered:

> "There is a royalty on every byte transmitted. This is paid automatically by the user to the owner every time a fragment is summoned." [LM 2/43]

If transclusions created separate I-space content, the royalty would flow to the wrong owner (or to no one).

### Summary

The guarantee is absolute: both users' references resolve to the same I-space address because COPY is reference, not duplication. This is not a design choice that could go either way — it is the foundation on which transclusion, correspondence, discovery, and royalty all depend.

---

## Question 8 [nelson]

> Must the system distinguish between "content at this address was removed from this document" and "content at this address no longer exists anywhere in the system"?

### Nelson's Answer

## Answer: No — Because the Second State Cannot Occur

Nelson's architecture makes the distinction unnecessary. The state "content at this address no longer exists anywhere in the system" is **architecturally impossible** in Xanadu. There is only one kind of removal, and it is always V-space removal — never I-space destruction.

### I-Space Is Append-Only

Content in I-space is permanent. There is no operation that removes it:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

The `delete-semantics` extraction makes this explicit: "DELETE in Xanadu does NOT mean what it means in conventional systems. It removes content from a document's V-space (current arrangement) but does NOT remove it from I-space (permanent storage)."

### What "Deleted" Actually Means

The diagram on page 4/9 defines the only removal state the system recognizes:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

Note the careful language: **not currently addressable** — not "destroyed," not "gone," not "no longer exists." The bytes are still in I-space. They are simply no longer part of the document's current V-space arrangement.

And Nelson confirms the broader principle:

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

### Why the Distinction Is Moot

After a DELETE operation, the "removed" content remains accessible through:

1. **Historical backtrack** — previous versions of the same document still contain it
2. **Transclusions** — other documents that include-by-reference still show it
3. **I-address resolution** — links pointing to the I-address still resolve
4. **FINDDOCSCONTAINING** — the system can find all documents containing the material

The system always knows where the content lives (its I-address encodes the home document permanently). A front end encountering a V-space gap can always determine that content *was here but was removed from this arrangement* — and can trace the I-address to find the content itself.

### The Only Ambiguity: Operational Failure

Nelson does acknowledge that content could become *unreachable* through operational failure — vendor shutdown, network partition, storage corruption:

> "User acknowledges that due to possible unreliability of the software, unreliability and vulnerability of transmission systems, and myriad possibilities for intrusion and malicious mischief by unseen parties throughout the universe, all storage, and transmission of contents and links, and attempts to deliver such material, are at User's risk." [LM 5/18]

But this is a **failure mode**, not a **designed system state**. The architecture mitigates it through vendor backup obligations and distributed replication, not through semantic distinctions in the address model. The vendor contract requires orderly transition of all customer materials upon cancellation [LM 5/16]. The system is designed so that content *should* always exist somewhere — even if, in practice, operational failures could make it temporarily or permanently unreachable.

### Summary

The system needs only one concept: **V-space presence or absence**. Content is either in a document's current V-stream or it isn't. If it isn't, the content itself still exists in I-space — permanently, by architectural fiat. The question "does this content exist anywhere?" always has the answer "yes." The only meaningful question is "is this content part of this document's current arrangement?" — and that is simply the V-to-I mapping.

---

## Question 9 [nelson]

> Does the permanence guarantee extend to the address itself, or only to the content-to-address binding — could the system relocate content so long as the original address still resolves?

### Nelson's Answer

## Both — But Physical Location May Change

The permanence guarantee covers two distinct things:

**1. The address itself is permanent.** Forking ensures addresses are never reused or invalidated:

> "New items may be continually inserted in tumbler-space while the other addresses remain valid. This means that any address of any document in an ever-growing network may be specified by a permanent tumbler address." [LM 4/19]

**2. The content-to-address binding is permanent.** Content at an I-space address never changes. I-space is append-only; bytes stored there are immutable.

**3. But physical location is explicitly allowed to change.** This is what BEBE exists for. Nelson says content can migrate between servers freely:

> "The contents can slosh back and forth dynamically." [LM 4/72]

> "Material is moved between servers for a number of purposes: 1. for more rapid access to final material, 2. for more rapid access to needed material which indexes material on other servers, 3. for rebalance in keeping with demand, 4. for redundancy and backup purposes." [LM 4/71]

> "Each server contains a map and a subset of the whole — a microcosm that shrinks and grows." [LM 4/71]

## The Node Field Records Provenance, Not Current Location

The tumbler's Node field (the first major field) identifies the *originating* server — where the content was born. But the system routes around that:

> "Each server contains a continuously valid model or subrepresentation of the entire docuverse and (because of tumbler addressing) a model of the entire network." [LM 4/72]

The user never specifies which server to contact. They present a tumbler address; the system finds the content. If it has migrated, been cached, or been replicated to a closer server, the user is none the wiser.

## The Design Is Explicitly Location-Transparent

Nelson separates what the user sees from where bits physically live:

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." [LM 4/11]

This quote refers to internal storage addresses, but the principle extends to network location. The entire BEBE protocol exists to "meld the contents of separate Xanadu servers into a single unified space" [LM 4/70] — meaning physical distribution is an implementation detail hidden from users.

Even vendor failure triggers relocation:

> "Upon notice of cancellation, Storage Vendor will arrange for the orderly transition of all customer-stored materials to other Xanadu locations." [LM 5/16]

Content moves. The address doesn't.

## Summary

| What | Permanent? |
|------|-----------|
| Tumbler address (identity) | Yes — never reused, never invalidated |
| Content at that address (binding) | Yes — I-space is append-only, immutable |
| Physical server location | No — content "sloshes" between servers via BEBE |
| Node field meaning | Records *origin*, not current location |

The system could — and was designed to — relocate content freely, so long as the tumbler address continues to resolve. That's the entire point of the BEBE protocol and the subrepresentation model. Permanence lives in the address and the binding, not in the physical bits.

---

## Question 10 [nelson]

> When content is copied rather than shared, must the copy receive a new and distinct address, or may the system treat the copy as the same content at the same address?

### Nelson's Answer

## Copy IS Transclusion: Same I-Address, New V-Address

In Xanadu, the COPY operation does **not** create new content. It creates a new V-space mapping that points to the **same** I-space address as the original. The "copy" and the original are the same bytes — viewed from different documents.

### The COPY Operation

The FEBE COPY command is defined as:

> "The material determined by \<spec set\> is copied to the document determined by \<doc id\> at the address determined by \<doc vsa\>." [LM 4/67]

This creates what Nelson calls an **inclusion** or **virtual copy** — the copied bytes appear in the target document's V-stream but remain at their original I-space address:

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

The "copied" bytes are fetched from their **home location** — the original document. They are not duplicated in storage.

### Why This Matters: Content Identity Is Based on Creation

Content identity in Xanadu is determined by where content was **created**, not by its value. Two documents with identical text created independently have **different** I-addresses. Transcluded content **shares** the same I-address.

This is the foundation for several guarantees:

1. **Attribution**: You can always trace content back to its origin because the I-address encodes the home document.

2. **Discovery**: FINDDOCSCONTAINING works because copies share I-addresses — "This returns a list of all documents containing any portion of the material included by \<vspec set\>." [LM 4/70]

3. **Royalties**: The system knows whom to pay because shared I-addresses identify the original owner.

4. **Correspondence**: Version comparison works because shared I-addresses reveal what content two versions have in common.

### The Two Paths to "Same Text"

| Operation | I-Space Effect | V-Space Effect | Identity |
|-----------|---------------|----------------|----------|
| **COPY** | No new bytes created | New V-mapping to existing I-address | Same content (shared identity) |
| **INSERT** | New bytes created at new I-address | New V-mapping to new I-address | Different content (independent identity) |

If you INSERT the text "hello" into document A, and separately INSERT "hello" into document B, those are **different bytes** at different I-addresses — structurally unrelated despite being textually identical.

If you COPY "hello" from document A into document B, document B's V-stream references the **same bytes** at document A's I-address. The system knows they are the same content.

### Nelson's Design Intent

Nelson frames this as the solution to a fundamental problem:

> "No copying operations are required among the documents throughout the system, and thus we solve the problems of update — especially the problem of updating documents which depend on other documents. We solve this problem simply by windowing to a changing document." [LM 2/36]

And the contrast with dead copies:

> "Note also that he or she who makes a paper copy or disk is losing all dynamic link connections, and is left with the inert, non-interactive copy. And that will be a considerable deprivation in the world we are talking about." [LM 2/48]

### Summary

A copy **must** share the same I-space address as the original. This is not an optimization — it is the architectural foundation of transclusion, attribution, discovery, and royalty. The system has no mechanism for "duplicate content at a new address" through COPY. If you want independent content that happens to have the same value, you INSERT it fresh, creating new I-space bytes with a new address and no structural connection to the original.

---

## Question 11 [gregory]

> Once a byte is stored in the granfilade at a given I-address, is there any operation — including internal maintenance, cache eviction, or disk compaction — that can change the byte value at that I-address, or is the mapping truly write-once-read-forever?

### Gregory's Answer

## KB Synthesis

## Yes — the granfilade mapping is write-once-read-forever for byte content.

The KB confirms this across multiple independent lines of evidence, with a few important caveats about durability vs. immutability.

### What never changes

**[INV-IADDR-IMMUTABILITY]** (Findings 0030, 0031, 0064) states it plainly: "I-addresses, once assigned to content, never change." The granfilade is append-only — `inserttextingranf` always allocates fresh addresses at the end and never overwrites existing entries. The Xanadu principle "bytes never die, addresses never change" is cited explicitly in **[FC-GRANF-ON-DELETE]**.

No documented operation mutates content bytes at an existing I-address:

- **DELETE** — operates exclusively on POOM V-to-I mappings via `deletend`. The granfilade is untouched: `dodeletevspan` has no call to any granf insertion or deletion function [FC-GRANF-ON-DELETE, ST-DELETE].
- **REARRANGE** — modifies V-address displacements only (`cdsp.dsas[V]`). I-addresses are never touched [ST-REARRANGE, INV-REARRANGE-IDENTITY].
- **CREATELINK** — allocates a new I-address for the link orgl; does not modify any existing I-address [ST-CREATE-LINK].
- **Tree rebalancing (split/recombine)** — `splitcrumseq`, `recombinend`, `levelpush` all restructure parent-child linkage and displacements; they do not modify bottom crum content bytes [ST-REBALANCE-2D, ST-SPLIT-2D].
- **Cache eviction (grim reaper)** — writes the in-memory crum faithfully to its assigned disk block via `orglwrite()`, then frees it. The write is a direct copy; no byte transformation occurs. The `modified` flag is cleared after the write and is only re-set by insert operations [SS-CACHE-MECHANISM].
- **Disk compaction** — the KB documents no compaction mechanism. `enf.enf` uses fixed-block allocation with no GC [SS-UNIFIED-STORAGE].
- **[INV-NO-IADDR-REUSE]** — deleted I-addresses are never reallocated. Even if content is removed from every document's V-stream, the I-address persists in the granfilade tree and the next allocation increments past it.

### The durability caveat (loss, not mutation)

**[INV-DURABILITY-BOUNDARY]** and **[SS-CACHE-MECHANISM]** note that in-memory content is not written to disk until `writeenfilades()` is called (session exit) or the grim reaper evicts the crum. A crash before either event loses the content — the I-address was allocated in memory but the bytes were never persisted. This is **loss**, not **mutation**: no byte at any I-address changes value; the address simply has no on-disk representation yet.

**[EC-CRASH-MID-WRITE]** describes a structural corruption scenario: the bottom-up write order (`subtreewriterecurs`) can leave the on-disk root pointing to stale subtree data while newly written children are orphaned. But again, this corrupts tree traversal — it does not change the byte values in any written block.

### Summary

Once a byte sequence is persisted to disk at an I-address, it is immutable. The only mechanisms that affect I-address content are:
1. Pre-persistence loss (crash before `writeenfilades()`) — bytes never reach disk
2. Post-crash tree corruption — previously written bytes become unreachable, but are unchanged on disk

There is no insert-update, no in-place edit, no compaction, and no eviction logic that overwrites existing content bytes. The granfilade is strictly append-only at every level of the storage stack.

---

## Code Exploration

I have now read all the relevant code. Here is my full answer.

---

## Is the Granfilade Truly Write-Once-Read-Forever?

**Yes. The I-address → byte mapping is write-once-read-forever.** No operation in the codebase — including insertion, deletion, cache eviction, disk block recycling, or enfilade restructuring — can change the byte value at a previously-assigned I-address. Every relevant code path was checked. Here is the evidence.

---

### 1. New Insertions Always Claim Fresh I-Addresses

The entry point for storing text bytes is `inserttextgr()` [`granf2.c:83`], which calls `findisatoinsertgr()` [`granf2.c:130`] to compute where to insert.

For text content (`ATOM` hint), `findisatoinsertmolecule()` is called [`granf2.c:158`]:

```c
// granf2.c:162-176
tumblerincrement (&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound);
clear (&lowerbound, sizeof(lowerbound));
findpreviousisagr ((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);
```

`findpreviousisagr()` [`granf2.c:255`] walks the enfilade tree to find the **highest existing I-address** below the upper bound. The result is then incremented further to produce a strictly-greater address:

```c
// granf2.c:166-169
if (tumblerlength (&hintptr->hintisa) == tumblerlength (&lowerbound)) {
    tumblerincrement (&lowerbound, 2, hintptr->atomtype, isaptr);
    tumblerincrement (isaptr, 1, 1, isaptr);
} else if (hintptr->atomtype == TEXTATOM) {
    tumblerincrement (&lowerbound, 0, 1, isaptr);
```

The resulting `isaptr` is the start of the new allocation. It is **never equal to any existing I-address** — it always lands past everything already in the granfilade. Collision with existing content is structurally prevented.

---

### 2. The Only In-Memory Append Is Safe

Within `insertseq()` [`insert.c:17`], if the last bottom crum already holds GRANTEXT and has room, `fillupcbcseq()` is called to pack the new bytes in rather than allocating a new crum:

```c
// insert.c:34-42
if (info->infotype == GRANTEXT
 && ptr->cinfo.infotype == GRANTEXT
 && ptr->cinfo.granstuff.textstuff.textlength < GRANTEXTLENGTH) {
    if (!fillupcbcseq (ptr, &nextaddress, info)) {
```

`fillupcbcseq()` [`insert.c:75`] writes **only at offset `crumlength`** — after the existing bytes:

```c
// insert.c:87
movmem(&info->granstuff.textstuff.textstring,
       (char*)(&(ptr->cinfo.granstuff.textstuff))+crumlength,
       textlength);
```

Bytes at offsets `0..crumlength-1` (the original content, at their original I-addresses) are **never touched**. The new bytes land at the immediately following I-addresses, which were freshly allocated by `findisatoinsertgr()`.

---

### 3. Cache Eviction Is Byte-Faithful

When memory pressure triggers the grim reaper, `grimlyreap()` [`credel.c:106`] calls `reap()` [`credel.c:292`], which calls `subtreewrite()` → `subtreewriterecurs()` [`corediskout.c:426`]. For each modified parent, `uniqueoutloaf()` [`corediskout.c:511`] packs the subtree to disk via `packloaf()` → `hputinfo()`.

For GRANTEXT crums, `hputinfo()` serializes:

```c
// corediskout.c:237-244
if (ptr->cinfo.infotype == GRANTEXT) {
    humberput(ptr->cinfo.granstuff.textstuff.textlength, ...);
    movmem(ptr->cinfo.granstuff.textstuff.textstring, (*loafptrptr),
           ptr->cinfo.granstuff.textstuff.textlength);
    *loafptrptr += ptr->cinfo.granstuff.textstuff.textlength;
```

And `hgetinfo()` reads it back verbatim:

```c
// corediskin.c:257-262
ptr->cinfo.granstuff.textstuff.textlength = intof((humber)*loafptrptr);
(*loafptrptr) += lengthof((humber)*loafptrptr);
movmem((*loafptrptr), ptr->cinfo.granstuff.textstuff.textstring,
       ptr->cinfo.granstuff.textstuff.textlength);
(*loafptrptr) += ptr->cinfo.granstuff.textstuff.textlength;
```

The round-trip is a literal `memcpy` of the `textstring` array. No transformation, no loss. The `textlength` is serialized as a prefix, so the reader knows exactly how many bytes to restore.

After eviction, the next access to those I-addresses triggers `findleftson()` [`genf.c:206`], which detects `ptr->leftson == NULL` and calls `inloaf()` [`corediskin.c:152`] to page the disk copy back in. The bytes returned are identical to what was stored.

---

### 4. `deletevspan` Does Not Touch the Granfilade

```c
// do1.c:158-167
bool dodeletevspan(typetask *taskptr, typeisa *docisaptr, typevspan *vspanptr)
{
    return (
       findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
    && deletevspanpm (taskptr, docisaptr, docorgl, vspanptr)
    );
}
```

`findorgl()` retrieves the document's POOM orgl from the granfilade, then `deletevspanpm()` operates solely on that POOM (the virtual address tree), removing the V→I mapping entries. The granfilade itself — the 1D enfilade of I-addresses and their byte content — is **never written to** by this path.

Deleted content's bytes remain in the granfilade at their I-addresses. They are simply unreachable via V-space navigation from that document, but `ispan2vstuffset()` [`granf2.c:286`] would still retrieve them if given the I-span directly.

---

### 5. Disk Block Recycling Is Safe

When an enfilade parent crum is rewritten to a new disk block, the old block's reference count is decremented via `deletewithgarbageddescendents()` [`corediskout.c:388`]:

```c
// corediskout.c:397
if (!deletefullcrumflag || !changerefcount(diskptr,-1)) {
```

`changerefcount()` [`disk.c:60`] calls `diskfree()` when the count reaches zero, returning the block number to the free bitmap. `diskalloc()` [`diskalloc.c:27`] can then hand that number out for a new purpose.

However, by the time a block is freed, the live enfilade tree **no longer contains any pointer to that block**. The `sonorigin` fields in parent crums point to the new disk block (written before the old one was freed). Any lookup for the content that was once in the freed block will now follow the new block pointer and find the same bytes (since the content didn't change — only the tree structure around it was rewritten). The freed block may be reused for entirely new content at new I-addresses, and old I-addresses that previously lived in that block are no longer in scope from the tree's perspective.

There is no disk compaction pass. `diskfree()` / `diskalloc()` operate purely on block-number availability; bytes in old blocks are simply abandoned, not zeroed or compacted.

---

### 6. Enfilade Restructuring (Split) Moves Crums, Not Bytes

`splitcrumseq()` [`split.c:70`] triggers when a parent crum has too many children. It creates a new sibling parent and moves the rightmost half of the existing children to it:

```c
// split.c:83-89
for (i = 0, ptr = findrightmostson(father); i < halfsons && ptr; ++i, ptr = next) {
    next = findleftbro(ptr);
    disown(ptr);
    adopt(ptr, LEFTMOSTSON, new);
    rejuvinate(ptr);
    ivemodified(ptr);
}
```

Entire bottom crums (cbcs) — including their `textstring` — move as atomic units. No byte inside a crum's `textstring` is touched. The I-address ranges (`cwid`) of the moved crums are recomputed at the parent level via `setwispupwards()`, but the bytes remain exactly as stored.

`recombine()`, called from `insertseq()` at `insert.c:68`, triggers `splitcrumseq()` when the tree becomes unbalanced. Same property holds.

---

### 7. No Mechanism Exists for In-Place Overwrite

Surveying all write paths to `cinfo.granstuff.textstuff.textstring`:

- **`inserttextgr()`** → `insertseq()` → `moveinfo()`: copies a fresh info block into a freshly created crum. New crum, new I-address range.
- **`fillupcbcseq()`**: appends to existing crum at offset `crumlength`, never below it.
- **`hgetinfo()`** (`corediskin.c:257`): restores `textstring` from disk during page-in. This is a read-back, not a mutation.

There is no `memset`, no targeted overwrite, no `memmove` within an existing crum's byte buffer that could change a byte already placed at a given I-address. The source was checked completely.

---

### Conclusion

The granfilade's I-address space is **strictly append-only and immutable**:

| Operation | Effect on existing bytes at I-addresses |
|---|---|
| New text insertion | None — new I-addresses always beyond existing content |
| `fillupcbcseq()` append optimization | None — writes only past existing `textlength` offset |
| `deletevspan` | None — operates on POOM only, granfilade untouched |
| Cache eviction (reap) | None — faithful `memcpy` round-trip through disk |
| Disk block free/realloc | None — freed blocks are no longer tree-reachable |
| `splitcrumseq()` restructuring | None — moves whole crums atomically |
| No compaction exists | — |

**Once a byte is stored at I-address X, every future read of I-address X through the granfilade will return that same byte value, for the lifetime of the data store.** The mapping is truly write-once-read-forever.

---

## Question 12 [gregory]

> When `findisatoinsertmolecule` computes the next I-address as max+1, does the system guarantee that a failed or partially-completed INSERT (e.g., process crash mid-operation) can never leave the granfilade in a state where the same I-address could be allocated twice on restart?

### Gregory's Answer

## KB Synthesis

## Analysis: I-Address Double-Allocation After Failed INSERT

The short answer: **the system cannot guarantee against re-allocation of I-addresses that were partially written to disk but not integrated into the reachable tree.** However, this does not corrupt any committed state.

---

### The Allocation Mechanism Is Reachability-Bounded

`findisatoinsertmolecule` works by querying the granfilade tree via `findpreviousisagr` — a tree traversal from the root finding the highest existing I-address in a bounded subtree [SS-ADDRESS-ALLOC, Finding 0061]. Critically:

> "The allocation is purely derived from current tree state — there is no cached 'next available' pointer."

This means **the allocator only sees I-addresses reachable from the root**. Orphaned crums (written to disk but whose parents weren't updated) are invisible to it.

---

### Three Failure Scenarios

**Scenario 1: Crash before any eviction (crum in RAM only)**

INSERT allocates I.5 in an in-memory crum. Crash occurs. RAM lost. On restart, `findpreviousisagr` scans the on-disk tree, which never received the I.5 allocation. Next INSERT re-allocates I.5.

This is **semantically correct**: the first allocation was never committed. Re-use is not a violation — there is no prior committed data at I.5.

**Scenario 2: Crash during partial disk write** [EC-CRASH-MID-WRITE]

`subtreewriterecurs` writes bottom-up. If Leaf (with I.5) is written to disk but the parent isn't updated before crash:

- The on-disk root still references the old tree
- The new leaf is on disk but orphaned (unreachable from root)
- On restart, `findpreviousisagr` traverses the OLD reachable tree
- I.5 is not found → it is re-allocated by the next INSERT

This **violates INV-NO-IADDR-REUSE** in the raw disk sense — I.5 occupies a disk block and also gets freshly allocated. But:
- The orphaned block's data is inaccessible (no root path leads to it)
- The only live allocation of I.5 is the new one
- No simultaneously-reachable state ever contains I.5 twice

**Scenario 3: Grim reaper evicts completed subtrees** [SS-CACHE-MECHANISM, EC-CROSS-ENFILADE-EVICTION]

If the grim reaper evicted a completed subtree (all levels including parent updates written) before the crash, the I-address is fully integrated into the reachable tree and `findpreviousisagr` will find it. No re-allocation occurs. This is the safe case.

---

### What the System Lacks to Prevent This

- **No transaction log**: There is no write-ahead journal to roll back partial writes [SS-DURABILITY-BOUNDARY]
- **No startup validation**: `initenffile` loads whatever is on disk with no consistency check [EC-NO-STARTUP-VALIDATION]
- **No fsync**: `write()` syscalls go to OS buffers without forced sync [SS-DURABILITY-BOUNDARY]
- **No atomic multi-block commit**: The bottom-up write order is a partial mitigation but not a guarantee [EC-CRASH-MID-WRITE]

---

### The Precise Invariant

INV-NO-IADDR-REUSE [Finding 0061] holds **only over reachable I-addresses**:

> "Deleted I-addresses are never reused... the granfilade is never modified by DELETE, and allocation always queries the granfilade for the current maximum."

The invariant is conditional on the granfilade being in a consistent state. After a crash mid-write, the reachable granfilade tree is the **last fully-committed state**, and within that state the invariant holds. An I-address that exists only in an orphaned (unreachable) crum is effectively uncommitted and may be re-allocated — but this produces no logical duplication in the committed address space.

The system provides **session-level durability** (all-or-nothing at clean shutdown), not **operation-level durability** (each INSERT atomically committed). The re-allocation risk exists only in the gap between those two granularities.

---

## Code Exploration

I now have all the information needed to answer the question definitively. Let me trace every link in the chain.

---

## Answer

**No, the system does not guarantee this. A crash between I-address allocation and disk flush can cause the same I-address to be allocated twice across restarts.** Here is the full trace.

---

### 1. How `findisatoinsertmolecule` allocates an I-address

`findisatoinsertmolecule` [granf2.c:158-181] works by querying the **live in-memory granfilade**:

```c
static int findisatoinsertmolecule(typecuc *fullcrumptr, typehint *hintptr, typeisa *isaptr)
{
  typeisa upperbound, lowerbound;
    tumblerincrement (&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound);
    clear (&lowerbound, sizeof(lowerbound));
    findpreviousisagr ((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);  // [granf2.c:164]
    ...
    } else if (hintptr->atomtype == TEXTATOM) {
            tumblerincrement (&lowerbound, 0, 1, isaptr);  // max + 1  [granf2.c:169]
    }
```

`findpreviousisagr` [granf2.c:255-278] traverses the in-memory enfilade tree to find the highest existing I-address below `upperbound`. The returned `lowerbound` is that highest address. The new address is `lowerbound + (0, 1)` — i.e., max+1 **from whatever the tree currently holds in memory**.

The caller `inserttextgr` [granf2.c:83-109] then passes this address to `insertseq` [granf2.c:99] which modifies the in-memory tree.

`insertseq` [insert.c:17-70] calls `ivemodified()` at lines [insert.c:39, 47, 61] to flag the modified crums. `ivemodified` [genf.c:522-544] sets `ptr->modified = TRUE` and propagates it upward through `leftbroorfather` links.

**At this point the mutation is entirely in memory. No disk write has occurred.**

---

### 2. The persistence model: batch checkpointing, no WAL

The only functions that write in-memory state to disk are:

- **`writeenfilades()`** [corediskout.c:68-88] — writes the granfilade and spanfilade to disk at fixed locations (`GRANFDISKLOCATION`, `SPANFDISKLOCATION`). It calls `orglwrite()` → `subtreewriterecurs()` which walks nodes with `modified == TRUE`.
- **`diskflush()`** [corediskout.c:58-64] — calls `writeenfilades()`.

These are called only at specific moments:

```c
// bed.c:105 — only when no frontend is connected:
if (n_players < 1) {
    diskflush();
```
```c
// bed.c:134 — on QUIT after current request finishes:
writeenfilades();
closediskfile();
exit(0);
```
```c
// bed.c:183 — on SIGINT, only if mightbeblocked:
writeenfilades();
closediskfile();
exit(0);
```
```c
// corediskout.c:44 — on normal single-user exit via diskexit():
writeenfilades();
```

**There is no write-ahead log. There is no per-operation fsync. There is no journaling.** Every INSERT, COPY, or CREATELINK modifies the in-memory tree and returns; the disk is only updated in bulk on the above events.

---

### 3. What happens on restart

On startup, `initmagicktricks()` [entexit.c:41-46] calls `initkluge()` [corediskin.c:18-41] if a disk file exists:

```c
void initkluge(typecuc **granfptr, typecuc **spanfptr)
{
    tempcbc->cinfo.granstuff.orglstuff.diskorglptr.diskblocknumber = GRANFDISKLOCATION;
    inorgl (tempcbc);           // reads granf from disk
    *granfptr = tempcbc->cinfo.granstuff.orglstuff.orglptr;
```

`inorgl` → `inorglinternal` [corediskin.c:175-231] deserializes the on-disk loaf into fresh in-memory crums. Crucially, at [corediskin.c:148] in `varunpackloaf` and [corediskin.c:223] in `inorglinternal`:

```c
ptr->modified = FALSE;   // [corediskin.c:148, 223]
```

The restored tree **only reflects what was last written to disk**. Any in-memory mutations from the previous session that were not flushed are gone.

---

### 4. The crash scenario: duplicate I-address

Here is the precise failure sequence:

1. **Session A**: Granfilade on disk has highest text I-address = N−1. Process starts; `initkluge()` loads this state.
2. INSERT arrives. `findisatoinsertmolecule` calls `findpreviousisagr` on the in-memory tree → `lowerbound = N−1`. Returns `isaptr = N`.
3. `insertseq` [granf2.c:99] adopts a new bottom crum at address N into the in-memory tree. `ivemodified()` marks it dirty.
4. **Process crashes** (SIGKILL, segfault, power failure) — `writeenfilades()` never runs.
5. **Session B starts**. `initkluge()` reads from disk. Disk still has N−1 as highest address (N was never written).
6. Another INSERT arrives. `findisatoinsertmolecule` → `findpreviousisagr` on the freshly-loaded tree → `lowerbound = N−1` → `isaptr = N`.
7. **Address N is allocated again for different content.** The previous use of N is lost; the new use of N occupies the same I-address.

---

### 5. The `putinsert`-before-`doinsert` aggravation

In `fns.c:84-98`, the INSERT handler has this ordering:

```c
void insert(typetask *taskptr)
{
    (void) getinsert (taskptr, &docisa, &vsa, &textset);
    putinsert (taskptr);           // response sent BEFORE operation [fns.c:91]
    if (!doinsert (taskptr, &docisa, &vsa, textset)) ...
}
```

Compare the commented-out original version [fns.c:69-82] and the pattern used by `createnewdocument`, `createnewversion`, `createlink` — all of which send the response *after* the operation completes. The current `insert` sends `putinsert` before `doinsert`, meaning the client's acknowledgment window precedes even the in-memory write, further decoupling protocol-level confirmation from durable state.

---

### 6. Within-session safety (no concurrent hazard)

Within a single uninterrupted session, allocations are safe. The event loop in `bed.c:103-148` processes one request per `select()` iteration [bed.c:118-142]. `findpreviousisagr` always queries the live tree, which already contains the address allocated by the prior `insertseq`. No two concurrent insertions can read the same `lowerbound`.

---

### Summary

The system provides **no crash-safety guarantee** for I-address uniqueness across restarts. The failure mode is structural:

| Property | What the code does |
|---|---|
| I-address source | Computed as `max(current in-memory tree) + 1` [granf2.c:164-169] |
| When memory → disk | Only on idle flush, QUIT, or SIGINT [bed.c:105, 134; corediskout.c:44] |
| On restart | In-memory tree rebuilt strictly from last disk state [corediskin.c:18-41] |
| Missing: | Write-ahead log, per-operation fsync, persistent address counter, crash recovery |

If the process is killed between `insertseq()` modifying the tree [insert.c:17] and `writeenfilades()` flushing it [corediskout.c:68], the allocated I-address exists nowhere on disk. On restart, `findisatoinsertmolecule` will compute the same max+1 and hand the identical I-address to new content. This is a fundamental property of the architecture: a memory-resident enfilade with periodic bulk checkpointing, not a durably-logged transactional store.

---

## Question 13 [gregory]

> After INSERT shifts V-positions rightward via `makegappm`, do the shifted POOM entries retain their exact original I-address values byte-for-byte, or could the tumbler arithmetic in `tumbleradd` introduce any rounding, normalization, or exponent change that alters the I-address representation?

### Gregory's Answer

## KB Synthesis

The I-address values in shifted POOM entries are completely unaffected — byte-for-byte identical before and after the shift.

**The mechanism is dimensional isolation.** The `makegappm` shift call (from [ST-INSERT] / Finding 0054) is:

```c
tumbleradd(&ptr->cdsp.dsas[V], &width->dsas[V], &ptr->cdsp.dsas[V])
```

This explicitly targets only `dsas[V]` — the V-dimension of the POOM crum's displacement. The I-dimension `dsas[I]` is a separate field and is never passed to `tumbleradd`. No arithmetic of any kind touches it during the shift phase.

**This is not accidental.** [ST-REARRANGE] / Finding 0056 confirms the same design for REARRANGE's displacement arithmetic: *"The code modifies only `ptr->cdsp.dsas[index]` (the V-address component of the displacement). The I-address, stored separately, is never touched."* `makegappm`'s shift follows the same convention.

**The `setwispupwards` concern.** After insertion, `setwispnd` recalculates the tree's root displacement across all dimensions (Finding 0066). For a 2D enfilade, this absorbs the minimum child displacement — including the I-dimension — into the parent and adjusts children to relative encoding. However, this is purely a representational change: the *absolute* logical I-address (sum of ancestor I-displacements + node's I-displacement) is invariant under this re-encoding. No content identity is altered; only how displacements are split between parent and child nodes in the tree structure.

**The invariants confirm it globally:**
- [INV-IADDR-IMMUTABILITY]: *"INSERT shifts V-addresses but preserves every existing I-address assignment. Content 'C' that had I-address I.3 before insertion still has I-address I.3 after insertion."*
- [FC-INSERT-IADDR]: *"INSERT does not modify the I-address of any pre-existing content... No I-address is lost; they may appear at different V-positions but the I-address itself is invariant."*

**Bottom line:** No rounding, normalization, or exponent change to I-addresses is possible because `tumbleradd` is never applied to `dsas[I]` during the shift. The only tumbler arithmetic during `makegappm` is on the V-dimension, and the two dimensions of a POOM crum are stored and modified independently.

---

## Code Exploration

I now have everything needed. Here is the complete answer.

---

## Answer: I-addresses are preserved byte-for-byte after `makegappm`

### The single `tumbleradd` call in `makegappm` touches only `dsas[V]`

The entire gap-making logic in `makegappm` iterates over POOM children of the insertion point and classifies each one with `insertcutsectionnd`. For nodes that fall to the right of the cut (case `1`), it shifts their V-displacement:

**`insertnd.c:161–164`:**
```c
case 1:/*9-17-87 fix */
    tumbleradd(&ptr->cdsp.dsas[V],&width->dsas[V],&ptr->cdsp.dsas[V]);
    ivemodified (ptr);
    break;
```

`dsas[V]` is index `1` — the V-dimension. `dsas[I]` is index `0` — the I-dimension. This is defined unambiguously in `wisp.h:19–20`:

```c
#define I  0
#define V  1
```

The I-address field `ptr->cdsp.dsas[I]` is **never written** in `makegappm`. The loop body only ever modifies `dsas[V]`, or does nothing (cases `0` and `2`). `insertcutsectionnd` (`edit.c:207–233`) is purely a classifier — it calls `whereoncrum` to determine position and returns an integer; it does not modify any tumbler fields.

---

### What `absadd` does to the V-dimension (and what it cannot do to I)

`tumbleradd` is a macro that expands to `functiontumbleradd` (`common.h:197`). In the same-sign case (the only one that applies to a positive V-shift), `functiontumbleradd` calls `absadd` (`tumble.c:374–376`):

```c
} else if (aptr->sign == bptr->sign) {
    absadd (aptr, bptr, cptr);
    cptr->sign = aptr->sign;
```

**`absadd` (`tumble.c:460–484`)** performs digit-by-digit alignment and addition without carry propagation. When `aptr->exp == bptr->exp`, it does:

```c
ansmant[0] = amant[0] + bmant[0];
```

There is no carry into `ansmant[1]`. If the sum overflows `tdigit` (defined as `UINT`, `common.h:57`), the result wraps silently. This is a latent overflow risk in V-arithmetic, but it is structurally impossible for it to affect I-addresses because `absadd` is only ever called on the V-component.

**No post-add normalization occurs.** The `functiontumbleradd` code has this comment at `tumble.c:377–383`:

```c
/*absadd returns justified result so no need to justify*/
/*
if(cptr->mantissa[0] == 0){
    partialtumblerjustify (cptr);
}
*/
```

The call to `partialtumblerjustify` is commented out for same-sign additions. `absadd` itself also does not call `tumblerjustify`. Since `tumbleradd` only operates on V-displacements, none of this normalization logic touches I-addresses regardless.

---

### `movetumbler` is a raw struct copy — no transformation

`movetumbler` is defined as:

**`common.h:73`:**
```c
#define movetumbler(A,B) (*((tumbler *)(B)) = *((tumbler *)(A)))
```

A plain struct assignment. No arithmetic, no normalization, no field reinterpretation. Whenever a node is moved in the tree during cuts (`makecutsnd`) and insertion, its I-address is carried unchanged.

---

### Summary

| Component | Touched by `makegappm`? | Arithmetic applied? | Normalization risk? |
|---|---|---|---|
| `ptr->cdsp.dsas[I]` | **No** | **None** | **None** |
| `ptr->cdsp.dsas[V]` | Yes | `absadd` (no carry, no justify) | Overflow possible on carry |

The shifted POOM entries retain their exact original I-address values (`cdsp.dsas[I]`) byte-for-byte. The `tumbleradd` call in `makegappm` is surgically scoped to `dsas[V]`. The `absadd` implementation does not normalize, justify, or canonicalize its result for same-sign addition — and even if it did, I-addresses are not operands or outputs of any `tumbleradd` call in this path.

---

## Question 14 [gregory]

> When REARRANGE moves content via `makeoffsetsfor3or4cuts`, the KB says I-addresses are preserved — but does the implementation copy POOM bottom crums with their original I-displacement and I-width fields untouched, or does it reconstruct them through arithmetic that could theoretically drift?

### Gregory's Answer

## KB Synthesis

REARRANGE preserves I-fields by **not touching them at all** — it modifies only the V-component of each POOM crum's displacement in-place. The I-fields are physically untouched memory.

The operative code is `edit.c:125`:

```c
tumbleradd(&ptr->cdsp.dsas[index], &diff[i], &ptr->cdsp.dsas[index])
```

In the POOM 2D enfilade, `cdsp.dsas` is a two-component displacement array: one index for SPANRANGE (V-dimension) and one for ORGLRANGE (I-dimension). The `rearrangend()` loop applies offsets exclusively to `dsas[SPANRANGE]`. The `dsas[ORGLRANGE]` component (the I-displacement) and `cwid.dsas[ORGLRANGE]` (the I-width) are never referenced in the offset application.

This means:

- **No copying**: crums are mutated in-place, not reconstructed
- **No I-arithmetic**: the I-dimension of each crum is untouched bytes
- **No drift possible**: you can't accumulate arithmetic error on fields you never compute over

[ST-REARRANGE] (Finding 0056) states explicitly: "The operation modifies V-addresses exclusively — it calls `tumbleradd(&ptr->cdsp.dsas[index], ...)` which updates the displacement's **V-address component**. No I-addresses are touched, no content is copied, no new permascroll entries are created."

[INV-REARRANGE-IDENTITY] (Finding 0056) formalizes the consequence: `∀ c ∈ content(doc): i_addr(c, doc_after) = i_addr(c, doc_before)`. The proof obligation is trivial given the above — I-fields are preserved because nothing writes to them.

The only arithmetic involved in REARRANGE is tumbler addition on V-displacements. I-displacements and I-widths are preserved bit-for-bit from before the operation.

---

## Code Exploration

I now have everything needed to give the full answer.

---

## How REARRANGE handles POOM bottom-crum I-address fields

The implementation uses **two different mechanisms** depending on whether a crum exists before the cuts or is created by them. Neither mechanism is a pure field-copy, but only one involves arithmetic reconstruction.

---

### Phase 1 — `makecutsnd` slices crums that straddle cut boundaries

`rearrangend` [edit.c:108–110] calls `makecutsnd`, which walks the tree and eventually calls `slicecbcpm` [ndcuts.c:373] whenever a bottom crum is `THRUME` (straddles) a cut knife. This is the code that creates new crums.

```c
// ndcuts.c:396–447  (slicecbcpm)
tumblersub (cut, &grasp.dsas[index], &localcut);   // localcut = V-distance from crum start to cut
// ...
movewisp (&ptr->cwid, &newwid);                    // copy all widths into newwid
for (i = 0; i < widsize(enftype); i++) {           // widsize(POOM) = WIDSIZEPM = 2 (V and I)
    /* I really don't understand this loop */
    newwid.dsas[i].mantissa[0] = localcut.mantissa[0];   // applies V-cut distance to ALL dims
    tumblerjustify (&newwid.dsas[i]);
}
locksubtract ((tumbler*)&ptr->cwid, (tumbler*)&newwid, (tumbler*)&new->cwid, 2);  // new->cwid = old - split
movewisp (&newwid, &ptr->cwid);                           // ptr->cwid = split
dspadd (&ptr->cdsp, &ptr->cwid, &new->cdsp, enftype);    // new->cdsp = ptr->cdsp + ptr->cwid
move2dinfo (&((type2dcbc *)ptr)->c2dinfo, &((type2dcbc *)new)->c2dinfo);  // copy homedoc
adopt(new, RIGHTBRO, ptr);
```

`widsize(POOM)` is `WIDSIZEPM = 2` [wisp.h:27,60], and `dspsize(POOM)` is `DSPSIZEPM = 2` [wisp.h:26,61]. So `dspadd` [wisp.c:15–17] operates on **both** the V and I components: `lockadd(a->dsas, b->dsas, c->dsas, dspsize(POOM))`.

The new right-half crum's fields after `slicecbcpm`:
- **I-width**: `new->cwid.dsas[I] = old->cwid.dsas[I] − localcut` (arithmetic)
- **I-displacement**: `new->cdsp.dsas[I] = ptr->cdsp.dsas[I] + localcut` (arithmetic via `dspadd`)

The original left-half crum `ptr`:
- **I-width**: set to `localcut` (arithmetic, **modified in place**)
- **I-displacement**: **unchanged** (untouched)

The author's comment at `ndcuts.c:439` — `/* I really don't understand this loop */` — is there in the shipping code. The loop applies `localcut.mantissa[0]` (a V-axis scalar) uniformly to **all** width dimensions, implicitly relying on the invariant that V-width and I-width are always equal in POOM bottom crums. There is no assertion or guard checking this assumption.

---

### Phase 2 — `rearrangend` shifts V-displacement of moved crums

After `makecutsnd` finishes, the rearrangement loop in `rearrangend` [edit.c:113–136] classifies each child and applies offsets:

```c
// edit.c:124–128
case 1:  case 2:  case 3:
    tumbleradd (&ptr->cdsp.dsas[index], &diff[i], &ptr->cdsp.dsas[index]);
    ivemodified((typecorecrum*)ptr);
    break;
```

Here `index = V`, confirmed by the sole call site in `orglinks.c:139`:

```c
// orglinks.c:139
rearrangend((typecuc*)docorgl, cutseqptr, V);
```

`tumbleradd` modifies only `cdsp.dsas[V]`. For all moved crums:
- **I-displacement** (`cdsp.dsas[I]`): **completely untouched**
- **I-width** (`cwid.dsas[I]`): **completely untouched**

---

### Summary table

| Crum type | I-displacement | I-width |
|---|---|---|
| **Existing crum that moves** (cases 1–3, rearrangend:125) | Preserved verbatim | Preserved verbatim |
| **Left half of split crum** (slicecbcpm:445–446) | Preserved verbatim | Replaced with `localcut` (arithmetic) |
| **New right-half crum** (slicecbcpm:444, 446) | `old_cdsp.dsas[I] + localcut` (arithmetic) | `old_cwid.dsas[I] − localcut` (arithmetic) |

---

### Can the arithmetic theoretically drift?

All arithmetic is exact integer tumbler operations — no floating-point, no rounding, no accumulation error in the IEEE sense.

However, there is a **structural fragility**. The loop at `ndcuts.c:439–442` is a single-scalar operation that conflates V-space and I-space by writing `localcut.mantissa[0]` (a V-axis cut distance) to **both** `newwid.dsas[V]` and `newwid.dsas[I]`. This is only correct if the POOM invariant holds: the V-width of a bottom crum equals its I-width (1 V-unit → 1 I-unit). No assertion enforces this.

If a prior operation (an undetected bug elsewhere) introduced a V/I-width mismatch, `slicecbcpm` would construct incorrect I-displacements for right-half crums — and do so silently, without error. Subsequent operations on the same POOM would propagate the bad I-addresses. There is no re-derivation from the granfilade; the POOM is the authoritative store of the V↔I mapping and there is no cross-check against it during rearrangement.

---

### Bottom line

The KB claim that "I-addresses are preserved" is **accurate for the move step** (phase 2): existing crums that are displaced get only their V-displacement incremented by `diff[i]`, and their I fields are never touched. But it is **incomplete for the slice step** (phase 1): every bottom crum that crosses a cut boundary has its I-width rewritten, and the new right-half crum receives an I-displacement computed by `dspadd(ptr->cdsp, ptr->cwid, new->cdsp, POOM)` [ndcuts.c:446] — pure arithmetic. This arithmetic is correct as long as the V=I alignment invariant holds throughout, which the code assumes but does not verify.

---

## Question 15 [gregory]

> If CREATELINK advances the I-address allocation counter past the text range, creating a gap, is that gap permanently reserved — meaning no future text INSERT can ever fill those gap I-addresses — or could a different document or session allocate into that gap region?

### Gregory's Answer

## KB Synthesis

## Gap I-Addresses After CREATELINK Are Permanently Inaccessible

**For the same document (any session):** The gap is permanently unavailable — no future text INSERT into that document can ever allocate those addresses.

The mechanism is layered:

1. **Monotonic allocation** [INV-MONOTONIC, Finding 0061]: `findpreviousisagr` returns the highest existing I-address below the upper bound, then increments by 1. There is no free-list and no gap-filling — allocation always continues upward from the current maximum.

2. **No reuse** [INV-NO-IADDR-REUSE]: "Once allocated in the granfilade, I-addresses are permanent... the I-address space grows strictly monotonically and permanently."

3. **Shared per-document allocator** [Finding 0063]: Both link orgl and text content use `findisatoinsertmolecule` for the same document's allocation space. After CREATELINK advances the maximum into the link orgl's address range, subsequent text INSERTs find the link orgl as the maximum and allocate above it — the gap addresses are simply skipped forever. The empirical proof: INSERT "ABC" → CREATELINK → INSERT "DEF" produces 2 shared span pairs (gap visible), while INSERT "ABC" → VERSION → INSERT "DEF" produces 1 pair (no gap, VERSION does not touch content allocation) [Finding 0077].

4. **Sessions share state** [Finding 0042, INV-ATOMICITY]: The backend is single-threaded with run-to-completion dispatch. All sessions query the same granfilade tree. A different session inserting into the same document would see the same maximum and allocate above the same gap.

**For different documents:** Unaffected. Allocation is partitioned by document — the upper-bound search in `findisatoinsertmolecule` is scoped to the specific document's subtree [Finding 0065: "element_number is scoped to the document, not global"; Finding 0077: "both query the same granfilade tree but search different subtrees"]. A gap in document A's I-address space has no bearing on document B's text allocation counter.

**Summary:** The gap is a permanent artifact of the monotonic, no-reuse design. The gap I-addresses are structurally inaccessible in perpetuity for any operation on that document, in any session. Different documents have independent allocation spaces and are entirely unaffected.

---

## Code Exploration

The user hasn't granted write access. Here is the complete answer based on code analysis:

---

## Answer: CREATELINK Does Not Create a Gap in the Text I-Address Range

The premise of the question requires correction. **CREATELINK does not advance the text I-address counter at all.** The "gap" it creates is in **V-space** (virtual document position), not in I-space.

---

### I-Address Subspace Separation — The Core Mechanism

`findisatoinsertmolecule` (`granf2.c:158-181`) is the allocation function for both text and link atoms. It uses `atomtype` to create strict, non-overlapping search bounds:

```c
tumblerincrement (&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound);
```

With `TEXTATOM = 1` and `LINKATOM = 2` (`xanadu.h:145-146`):

| Atom type | `atomtype` | `upperbound` | Allocated I-range |
|-----------|-----------|--------------|------------------|
| TEXTATOM  | 1         | `docisa.0.2` | `docisa.0.1.*`   |
| LINKATOM  | 2         | `docisa.0.3` | `docisa.0.2.*`   |

For text allocation, `findpreviousisagr` searches for the highest ISA **strictly less than** `docisa.0.2`. Link ISAs live at `docisa.0.2.*`, which is **greater than** `docisa.0.2`. They are invisible to the text search. The text I-counter never sees a link ISA.

This is confirmed by Finding 0065's golden data: link ISA `1.1.0.1.0.1.0.2.1` is in element field `0.2`, while text ISAs are in field `0.1`. Document A's second link (`1.1.0.1.0.1.0.2.2`) is consecutive with its first (`1.1.0.1.0.1.0.2.1`) even after intervening operations in another document. There is no shared counter.

---

### What CREATELINK Actually Does to Allocation State

`docreatelink` (`do1.c:195-221`) calls:

1. **`createorglingranf`** — allocates a `GRANORGL` node at `docisa.0.2.1` (link subspace) via `findisatoinsertmolecule` with `LINKATOM`. This modifies the granfilade, but only in the `docisa.0.2.*` range.

2. **`findnextlinkvsa`** (`do2.c:151-167`) — computes the link's **V-address** (position in the document's virtual space) as `max(text_vspan_end, 2.1)`:

```c
tumblerclear (&firstlink);
tumblerincrement (&firstlink, 0, 2, &firstlink);  // firstlink = 2
tumblerincrement (&firstlink, 1, 1, &firstlink);  // firstlink = 2.1
(void) doretrievedocvspan (taskptr, docisaptr, &vspan);
tumbleradd (&vspan.stream, &vspan.width, &vspanreach);
if (tumblercmp (&vspanreach, &firstlink) == LESS)
    movetumbler (&firstlink, vsaptr);   // link goes at 2.1
else
    movetumbler (&vspanreach, vsaptr);
```

3. **`docopy`** — inserts the link's I-address reference into the document's POOM (V→I enfilade) at the V-position computed above.

---

### The Gap Is in V-Space

If a document's text occupies V-positions 1.1 through (say) 1.4, `findnextlinkvsa` places the link at V-position 2.1, leaving a gap at V-positions ~1.4 to 2.0 with no content. This explains the 2 span pairs in Finding 0063's `compare_versions` result: ABC text is at V-positions 1.1–1.3, and DEF text (inserted "at end" after the link) lands in the 2.x V-range. The two documents being compared have different V-space mappings for the same I-addresses — hence 2 pairs, not 1. Finding 0063's explanation ("link orgl advances the text I-counter") is incorrect. Its golden file comment is correct: `"CREATELINK modifies POOM enfilade only, not granfilade"`.

---

### Is the V-Space Gap Permanently Reserved?

No. `acceptablevsa` (`do2.c:110-113`) is an unconditional stub:

```c
bool acceptablevsa(tumbler *vsaptr, typeorgl orglptr)
{
    return (TRUE);
}
```

Any V-address is accepted. A client can INSERT text at gap V-positions (between text-end and 2.1) and the backend will accept it. There is no enforcement preventing this. In practice, clients inserting "at end" will push further into the 2.x range, widening the gap rather than filling it, but this is a client convention, not a backend constraint.

---

### Cross-Document Isolation

I-addresses are scoped by document ISA prefix. The `upperbound` in `findisatoinsertmolecule` is constructed from `hintptr->hintisa`, which is the owning document's ISA (`do2.c:78-84`). `findpreviousisagr` searches only within that document's address range. A different document's CREATELINK — or any operation — cannot touch this document's text or link I-address subspaces. Allocation for document A does not advance any counter visible to document B.

---

### Cross-Session Persistence

There is no session-local allocation counter. On every INSERT, `findisatoinsertmolecule` calls `findpreviousisagr` (`granf2.c:255-278`) to query the current granfilade tree for the highest existing ISA below the bound. This is stateless — the granfilade is the authoritative persistent store. Once an ISA is allocated, it remains in the tree permanently (no free list, no garbage collection). A future session will find the same highest ISA and continue monotonically from there. No reuse of addresses is possible.

---

### Summary

| Property | Answer | Code location |
|----------|--------|---------------|
| Does CREATELINK advance the text I-counter? | **No** | `granf2.c:162` — separate `upperbound` per `atomtype` |
| Is there a text I-space gap from CREATELINK? | **No** | Text ISAs `docisa.0.1.*` never overlap link ISAs `docisa.0.2.*` |
| Is there a V-space gap? | **Yes** | `do2.c:157-163` — link placed at `max(end, 2.1)` |
| Is the V-gap reserved/enforced? | **No** | `do2.c:110-113` — `acceptablevsa` always returns `TRUE` |
| Can a different document fill the I-gap? | **N/A** (no I-gap exists) | `granf2.c:162` — bound is per-`docisa` |
| Can a different session fill the I-gap? | **N/A** (no I-gap exists) | `granf2.c:255` — stateless query of persistent tree |

---

## Question 16 [gregory]

> When `strongsub`'s exponent guard fires during DELETE and returns a link V-position unchanged, is this a guaranteed no-op on the POOM entry (the crum is literally not touched), or does the code write back the same value, risking any subtle modification through the write path?

### Gregory's Answer

## KB Synthesis

The KB gives us enough to answer this precisely, though with one residual uncertainty.

## What `strongsub` actually does on the exponent guard

From [SS-TUMBLER] / [FC-SUBSPACE] (Finding 0055), the guard at `tumble.c:544` is:

```c
if (bptr->exp < aptr->exp) { movetumbler(aptr, cptr); return(0); }
```

The call site from [ST-DELETE] (Finding 0055) is:

```c
// edit.c:63
tumblersub(&ptr->cdsp.dsas[index], width, &ptr->cdsp.dsas[index])
```

Notice that the first argument (input `a`) and the third argument (output `c`) are **the same pointer**: `&ptr->cdsp.dsas[index]`. So when `strongsub` fires the exponent guard and executes `movetumbler(aptr, cptr)`, it is copying the tumbler from a memory address **to itself**.

**This is not a true no-op at the memory level.** The write path is exercised — `movetumbler` performs a memory copy, it just happens to copy `x` into `x`. The crum's V-displacement field is written, but with its own current value.

## The residual uncertainty: dirty marking

The KB documents that on INSERT, `ivemodified()` is called to mark the crum and its ancestors as `modified = TRUE` ([SS-CACHE-MECHANISM], Finding 0059). For DELETE, the KB does not specify exactly where in `deletend()`'s Case 2 path `ivemodified()` is called relative to the `tumblersub` invocation.

- If `ivemodified()` is called **unconditionally** for every Case 2 crum that `deletend` visits, then link crums at `2.x` would be unnecessarily marked dirty and queued for a disk write by the grim reaper — a performance cost but no correctness issue.
- If `ivemodified()` is called **only when `tumblersub` actually changes the value**, then the link crum's dirty bit is never set and the write is completely skipped.

The KB's code references don't resolve this distinction; it would require reading `edit.c:31-76` directly.

## Spec implication

For the formal model, the consequence is clear either way: **the V-displacement value of the link crum is unchanged** — `entry.vpos' = entry.vpos` holds as a value invariant [FC-SUBSPACE]. Whether the implementation writes an identical value back is an implementation detail beneath the abstraction boundary. The frame condition `∀ entry with entry.vpos.exp > width.exp : entry.vpos' = entry.vpos` is satisfied in both cases. The dirty-marking question is relevant only to the durability/performance model ([SS-DURABILITY-BOUNDARY]), not to the behavioral specification.

---

## Code Exploration

I have everything I need. Here is the complete analysis.

---

## Answer

**The exponent guard is a guaranteed no-op. The POOM crum field is not modified — not even a same-value write-back in any meaningful sense, because the output pointer aliases the input pointer, making the write a C struct self-assignment.**

---

### 1. The `movetumbler` macro

`common.h:73`:
```c
#define movetumbler(A,B) (*((tumbler *)(B)) = *((tumbler *)(A)))
```

It is a plain struct-copy via `=`. When `A == B`, this becomes `*A = *A` — a C self-assignment. The C standard gives no undefined behaviour for this; the stored bytes are unchanged.

---

### 2. The exponent guard in `strongsub`

`tumble.c:534–547`:
```c
int strongsub(tumbler *aptr, tumbler *bptr, tumbler *cptr)
{
  tumbler answer;          // local, stack-only
  register INT i, j;

    tumblerclear(&answer); // clears local 'answer' — does NOT touch cptr
    if (tumblereq (aptr, bptr)) {
        movetumbler (&answer, cptr);  // would write zero — but only if equal
        return(0);
    }
    if (bptr->exp < aptr->exp) {   // ← THE GUARD
        movetumbler(aptr,cptr);    // ← the write in question
        return(0);
    }
    ...
```

Before the guard fires, only two things happen:

- `tumblerclear(&answer)` — writes to the **local** `answer` variable; the crum is not referenced.
- `tumblereq(aptr, bptr)` — a pure comparison; no write.

So if the guard fires, the crum has not been touched at all yet.

---

### 3. Pointer aliasing through the DELETE call chain

The delete path is `edit.c:63`:
```c
case 2:
    tumblersub (&ptr->cdsp.dsas[index], width, &ptr->cdsp.dsas[index]);
```

`ptr->cdsp.dsas[index]` is the POOM crum's displacement tumbler in the V-space dimension (`enf.h:47–48`, `wisp.h:50–51`). Crucially, **the same address is passed as both `aptr` (arg 1) and `cptr` (arg 3).**

This aliasing propagates through every layer:

| Frame | `aptr` | `cptr` | Same address? |
|---|---|---|---|
| `tumblersub` (`tumble.c:406`) | `&cdsp.dsas[index]` | `&cdsp.dsas[index]` | yes |
| → `tumbleradd` / `functiontumbleradd` (`tumble.c:428`, `385`) | `&cdsp.dsas[index]` | `&cdsp.dsas[index]` | yes |
| → → `strongsub` (`tumble.c:385`) | `&cdsp.dsas[index]` | `&cdsp.dsas[index]` | yes |

Inside `tumblersub`, the else-branch (`tumble.c:426–429`) copies `bptr` (`width`) into a local `temp` on the stack, negates its sign, and calls `tumbleradd(aptr, &temp, cptr)`. The local `temp` is the `bptr` that reaches `strongsub`. The `aptr`/`cptr` aliasing is preserved throughout.

---

### 4. What the guard actually executes

When the guard fires inside `strongsub`, with `aptr == cptr == &ptr->cdsp.dsas[index]`:

```c
movetumbler(aptr, cptr);
// expands to:
*((tumbler *)(cptr)) = *((tumbler *)(aptr));
// with aptr == cptr, this is:
*((tumbler *)(&cdsp.dsas[index])) = *((tumbler *)(&cdsp.dsas[index]));
// i.e., the struct copies itself to itself — no bytes change.
```

---

### 5. Nothing after `strongsub` touches the crum either

Back in `functiontumbleradd` (`tumble.c:385–389`):
```c
strongsub (aptr, bptr, cptr);   // returned with guard — cptr unchanged
cptr->sign = aptr->sign;         // aptr == cptr: self-assignment of sign field, no-op
if(cptr->mantissa[0] == 0){      // false for a normalized V-position tumbler
    partialtumblerjustify (cptr);
}
```

Back in `tumblersub` (`tumble.c:430`):
```c
tumblerjustify (cptr);
```
`tumble.c:296–298`:
```c
if (mantissaptr[0] != 0) {
    return(0);   // exits immediately for a normalized tumbler
}
```

A valid link V-position tumbler is always normalized (`mantissa[0] != 0`), so `tumblerjustify` exits without touching anything.

---

### 6. Conclusion

The exponent guard in `strongsub` is a **guaranteed no-op** on the POOM crum. The code does issue a write via `movetumbler(aptr, cptr)` (`tumble.c:545`), but because `aptr` and `cptr` are the same pointer (both resolved from `&ptr->cdsp.dsas[index]` at `edit.c:63`), the write is a C struct self-assignment: `*cptr = *cptr`. No byte of the crum's `cdsp.dsas[index]` field changes value. The crum is **literally not touched in any observable way**.

There is no write path that could introduce subtle modification: the only write is the self-assignment, and every subsequent operation (`cptr->sign = aptr->sign`, the `tumblerjustify` early-exit) is also a no-op for a well-formed V-position tumbler.

---

## Question 17 [gregory]

> For CREATENEWVERSION, the new document's POOM entries point to the same I-addresses as the original — are these entries independent copies in the B-tree, so that subsequent edits to either document's POOM cannot corrupt the other's I-address mappings through shared pointers or aliased crums?

### Gregory's Answer

## KB Synthesis

Yes — the version's POOM is a fully independent B-tree. Here is the synthesis across the KB:

## How CREATENEWVERSION builds the version's POOM

The call chain is: `docreatenewversion` → `createorglingranf` (allocates a **new orgl**) → `doretrievedocvspanfoo` (reads source text vspan) → `docopyinternal` → `insertpm` + `insertspanf` [ST-VERSION] [ST-VERSION-CREATE].

`createorglingranf` creates a fresh root node for the version's enfilade tree. `docopyinternal` then calls `insertpm`, which is the same POOM insertion function used by regular COPY. `insertpm` → `insertnd` allocates new bottom crums in the *version's* orgl tree, establishing V→I mappings pointing at the shared I-addresses in the immutable granfilade [PRE-COPY].

**What is shared:** The I-addresses themselves — entries in the granfilade, which is append-only and immutable [INV-IADDR-IMMUTABILITY]. The version and original point to the same bytes in I-space, but through independent POOM trees.

**What is not shared:** The POOM crum nodes. Each document has its own orgl (root pointer), and `insertpm` allocates fresh crums under the version's root. There is no pointer aliasing between the original's POOM tree and the version's POOM tree.

## Why subsequent edits cannot corrupt the other document

[FC-VERSION-ISOLATION] states this explicitly: "edits to the original document modify only the original's POOM. Edits to the version modify only the version's POOM. Neither affects the other."

[ST-DELETE] (Finding 0064) provides the strongest confirmation: `deletevspanpm` calls `deletend` on a single document's orgl, and "other documents that reference the same I-addresses through transclusion are completely unaffected — their POOM mappings remain intact." The POOM is scoped strictly to one orgl.

[SS-POOM-MUTABILITY] confirms the POOM is mutated in-place with no copy-on-write semantics. This design is only safe *because* each document has an independent tree — if crums were shared, in-place mutation would corrupt the other document immediately.

## The one nuance

All crums (original and version) share the same unified disk file and grim reaper cache [SS-UNIFIED-STORAGE] [SS-CACHE-MECHANISM]. This means memory pressure from operating on one document's POOM can evict modified crums from the other to disk. This affects **durability ordering** but not **correctness** — each crum belongs to exactly one orgl, and eviction does not change what V-address maps to what I-address [EC-CROSS-ENFILADE-EVICTION].

**Summary:** The version receives new POOM crum nodes under a new orgl root; only I-addresses (granfilade content) are shared. Edits to either document's POOM are fully isolated — they operate on structurally separate B-trees that happen to leaf into the same immutable I-address space.

---

## Code Exploration

I now have all the information needed to give a complete, cited answer.

---

## Answer: POOM Entries After CREATENEWVERSION Are Fully Independent Copies

**Yes — the new document's POOM crum nodes are independent, freshly allocated structures. No shared pointers or aliased crums exist between the original and the new document's POOM trees.**

Here is the complete traced path, with every claim cited.

---

### 1. Entry Point

**`fns.c:289-300`** — `createnewversion()` calls:
```c
docreatenewversion(taskptr, &originaldocisa, &originaldocisa, &newdocisa)
```

---

### 2. `docreatenewversion` — New POOM Created From Scratch

**`do1.c:260-299`** — Three key steps:

**Step A — allocate an empty POOM for the new document:**
```c
// do1.c:277
if (!createorglingranf(taskptr, granf, &hint, newisaptr))
    return (FALSE);
```
This calls `createorglgr` in **`granf2.c:111-128`**:
```c
locinfo.granstuff.orglstuff.orglptr = createenf(POOM);   // granf2.c:120
```
`createenf(POOM)` (in **`credel.c:492-516`**) allocates a brand-new, empty POOM enfilade — a `typecuc` apex node with one empty bottom `type2dcbc`, no children sharing anything with the original document's POOM. This POOM is stored in the granfilade indexed by the *new* document's ISA. Completely separate from the original's.

**Step B — retrieve original document's V-span:**
```c
// do1.c:281-288
doretrievedocvspanfoo(taskptr, isaptr, &vspan);
vspec.docisa = *isaptr;        // the *original* doc's ISA
vspec.vspanset = &vspan;
```
This constructs a `vspec` whose `docisa` names the original document.

**Step C — populate the new POOM by copying:**
```c
// do1.c:293
docopyinternal(taskptr, newisaptr, &vspan.stream, &vspec);
```

---

### 3. `docopyinternal` → `insertpm`

**`do1.c:66-82`** — `docopyinternal` fetches the *new* document's freshly-created POOM orgl and calls:
```c
// do1.c:78
insertpm(taskptr, docisaptr, docorgl, vsaptr, ispanset)
```
where `docorgl` is the new document's empty POOM.

**`orglinks.c:75-134`** — `insertpm` iterates over the I-span set from the original document. For each span it calls `unpacksporgl`:
```c
// orglinks.c:101
unpacksporgl(sporglset, &lstream, &lwidth, &linfo);
```

**`sporgl.c:178-203`** — `unpacksporgl` extracts data using `movetumbler` calls:
```c
movetumbler(&((typesporgl *)sporglptr)->sporglorigin, streamptr);   // sporgl.c:185
movetumbler(&((typesporgl *)sporglptr)->sporglwidth, widthptr);     // sporgl.c:186
movetumbler(&((typesporgl *)sporglptr)->sporgladdress, &infoptr->homedoc); // sporgl.c:187
```

**`movetumbler` is defined in `common.h:73` as:**
```c
#define movetumbler(A,B) (*((tumbler *)(B)) = *((tumbler *)(A)))
```
This is a C struct assignment — a **by-value copy** of the entire `tumbler` struct (a fixed-size integer array with no internal pointers). No aliasing is possible.

Then `insertpm` calls:
```c
// orglinks.c:130
insertnd(taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);
```
The I-address data (`lstream`, `lwidth`, `linfo.homedoc`) are all local variables on `insertpm`'s stack, copied from the sporgl by value above.

---

### 4. `insertnd` → `insertcbcnd` — Fresh Crum Allocation

**`insertnd.c:15-111`** — For POOM, `insertnd` calls `makegappm` then `doinsertnd`, which eventually calls `insertcbcnd`.

**`insertnd.c:242-275`** — `insertcbcnd` creates a brand-new crum:
```c
// insertnd.c:260
new = createcrum(0, (INT)father->cenftype);
// ...
// insertnd.c:267
move2dinfo(infoptr, &((type2dcbc *)new)->c2dinfo);
```

**`wisp.h:110`** — `move2dinfo` is:
```c
#define move2dinfo(A,B) movmem((A),(B),sizeof(type2dbottomcruminfo))
```
And `movmem` is `memmove` (`common.h:163`). The struct being copied is:
```c
// wisp.h:107-109
typedef struct struct2dbottomcruminfo {
    tumbler homedoc;
} type2dbottomcruminfo;
```
`homedoc` is a plain `tumbler` value with no internal pointers. The whole thing is blitted by value into the new crum's private storage.

Similarly for span/width:
```c
// insertnd.c:263
dspsub(origin, grasp, &new->cdsp, father->cenftype);
// insertnd.c:266
movewisp(width, &new->cwid);
```
`movewisp` is `memmove(B, A, sizeof(typewisp))` — again, by-value copy into the new crum's own fields.

---

### 5. `createcrum` — Fresh Memory Allocation Every Time

**`credel.c:518-596`** — `createcrum(0, POOM)` → `createcruminternal`:
```c
// credel.c:568
ptr = (typecorecrum *)eallocwithtag(crumsize, CBCTAG);
// credel.c:572-591: all fields zeroed/initialized fresh
ptr->height = crumheight;
ptr->isapex = FALSE;
ptr->modified = TRUE;
ptr->age = NEW;
ptr->leftbroorfather = NULL;
ptr->rightbro = NULL;
clear(&ptr->cdsp, sizeof(ptr->cdsp));
clear(&ptr->cwid, sizeof(ptr->cwid));
clear(&((type2dcbc *)ptr)->c2dinfo, sizeof(...));
```
Each call returns a **uniquely heap-allocated** block. There is no crum pooling, recycling, or sharing between documents' POOM trees.

---

### Summary

The call chain for CREATENEWVERSION is:

```
createnewversion (fns.c:289)
  → docreatenewversion (do1.c:260)
      → createorglingranf  → createenf(POOM)      ← new empty POOM, fresh allocation
      → doretrievedocvspanfoo                      ← reads original doc's V-span
      → docopyinternal (do1.c:66)
          → insertpm (orglinks.c:75)
              → unpacksporgl                        ← movetumbler: by-value copy
              → insertnd (insertnd.c:15)
                  → insertcbcnd (insertnd.c:242)
                      → createcrum(0, POOM)         ← fresh heap allocation
                      → move2dinfo                  ← memmove: by-value copy
                      → movewisp                    ← memmove: by-value copy
```

At no point is a pointer to an original document's crum stored in the new document's POOM. Every crum in the new document's POOM is:
1. **Freshly allocated** by `createcrum` → `eallocwithtag` [`credel.c:568`]
2. **Populated by value copy** via `memmove`/struct-assignment macros [`common.h:73`, `wisp.h:58`, `wisp.h:110`]
3. **Linked only into the new document's tree** via `adopt()` [`genf.c:419`], which sets only sibling/parent pointer fields in the new crums — no cross-document pointers

The I-addresses (stream, width, homedoc) encoded in the new POOM's bottom crums are identical *values* to those in the original's POOM, but they live in wholly independent crum objects. Subsequent edits to either document's POOM — insertions, deletions, splits, recombinations — operate entirely on that document's own crum tree. There is no mechanism by which a mutation in one document's POOM could reach or corrupt the other's crum nodes.

---

## Question 18 [gregory]

> When COPY detects I-address contiguity via `isanextensionnd` and extends an existing POOM crum rather than creating a new one, does the extended crum's I-displacement remain identical to the original, with only the width growing — or does the extension recompute the displacement?

### Gregory's Answer

## KB Synthesis

The I-displacement remains identical — only the width grows.

The condition `isanextensionnd` checks is that the new content's I-address origin equals the existing crum's **reach** (i.e., `crum.origin + crum.width`) [ST-INSERT, Finding 0062]:

> `isanextensionnd()` checks two conditions: (1) the new mapping has the same `homedoc` as an existing crum, and (2) the new mapping starts exactly where the existing crum ends (contiguous in both V and I dimensions). If both hold, the existing crum's **width is extended in place** — no new crum is allocated.
> — `insertnd.c:293-301` (check), `insertnd.c:243` (extension)

[PRE-COPY, Finding 0046] confirms the same path for COPY specifically:

> The new mapping starts exactly where the existing crum ends (contiguous in both V and I dimensions). If both hold, the existing crum's width is extended in place.

The logic is self-consistent: the extension precondition is `new_origin == crum.origin + crum.width`. If the displacement were recomputed to point at the new content, the original I-addresses covered by the crum would be orphaned. Instead, the crum's I-origin stays fixed at its original value, the I-width grows to `old_width + new_width`, and the crum now spans `[origin, origin + old_width + new_width)` — absorbing the appended content contiguously to the right.

The same holds for the V-dimension: [SS-INSERT-VWIDTH-ENCODING, Finding 0076] confirms V-width and I-width are independently encoded but represent the same numeric value, both growing by the same amount during extension.

---

## Code Exploration

I now have everything needed for a complete answer. Here it is:

---

## Answer: The I-displacement is never touched. Only the width grows.

### Execution path

`docopy` [`do1.c:45`] → `insertpm` → `insertnd` [`insertnd.c:15`] → `doinsertnd` [`insertnd.c:185`] → `insertmorend` [`insertnd.c:219`] → `insertcbcnd` [`insertnd.c:242`] (once `father->height == 1`).

---

### `insertcbcnd`: the extension branch

```c
// insertnd.c:249-258
for (ptr = findleftson (father); ptr; ptr = findrightbro (ptr)) {
    if (isanextensionnd ((typecbc*)ptr, grasp, origin, infoptr)) {
        dspadd (&ptr->cwid, width, &ptr->cwid, (INT)father->cenftype);  // line 251
        ivemodified (ptr);
        setwispupwards (father,1);
        ...
        return(FALSE);
    }
}
```

Line 251 is the **only mutation** that occurs on the extension path. It does:

```
ptr->cwid = ptr->cwid + width
```

`ptr->cdsp` — the crum's displacement (containing both its I- and V-address offsets) — **is not assigned, not read-for-write, not touched at all.**

---

### What `isanextensionnd` actually checks

```c
// insertnd.c:301-309
bool isanextensionnd(typecbc *ptr, typedsp *offsetptr, typedsp *originptr, type2dbottomcruminfo *infoptr)
{
  typedsp grasp, reach;
    if (!tumblereq (&infoptr->homedoc, &((type2dcbc *)ptr)->c2dinfo.homedoc))
        return (FALSE);
    prologuend ((typecorecrum*)ptr, offsetptr, &grasp, &reach);
    return (lockeq (reach.dsas, originptr->dsas, (unsigned)dspsize(ptr->cenftype)));
}
```

`prologuend` [`retrie.c:334-339`] computes:

```c
grasp = offset + ptr->cdsp    // absolute start of the crum
reach = grasp  + ptr->cwid    // absolute end   of the crum
```

Then `lockeq` compares `reach` to `origin` across `dspsize(POOM) = 2` tumblers [`wisp.h:26-27`]:

```c
#define DSPSIZEPM 2   // wisp.h:26 — covers both I (index 0) and V (index 1)
```

So contiguity is verified in **both** I and V simultaneously. The extension fires only when `reach.dsas[I] == origin.dsas[I]` AND `reach.dsas[V] == origin.dsas[V]`.

---

### What `dspadd` does to the width

```c
// wisp.c:15-18
int dspadd(typedsp *a, typewisp *b, typedsp *c, INT enftype)
{
    lockadd (a->dsas, b->dsas, c->dsas, (unsigned)dspsize(enftype));
}
```

`lockadd` loops over `dspsize(POOM) = 2` tumblers and calls `tumbleradd` on each [`wisp.c:269-273`]. The call at `insertcbcnd:251` is:

```c
dspadd (&ptr->cwid, width, &ptr->cwid, (INT)father->cenftype);
//       src=cwid    src2=new_width  dst=cwid   type=POOM
```

Result: `ptr->cwid.dsas[I] += width->dsas[I]`, `ptr->cwid.dsas[V] += width->dsas[V]`.

---

### Summary

| Field | Extension path |
|-------|---------------|
| `ptr->cdsp.dsas[I]` (I-displacement) | **Unchanged** — not touched |
| `ptr->cdsp.dsas[V]` (V-displacement) | **Unchanged** — not touched |
| `ptr->cwid.dsas[I]` (I-width) | **Grows** — `+= width->dsas[I]` |
| `ptr->cwid.dsas[V]` (V-width) | **Grows** — `+= width->dsas[V]` |

The I-displacement of the extended crum is left **identical to the original**. The extension is purely additive to the width field; no displacement recomputation occurs. This is consistent with the contiguity precondition: because `isanextensionnd` already confirmed that `reach == origin` (the existing crum's right edge exactly abuts the new content's left edge), the crum's origin (`cdsp`) needs no adjustment — the crum already starts in the right place; it simply needs to be made wider.

---

## Question 19 [gregory]

> The spanfilade DOCISPAN entries are never deleted — but can they be modified in place? If a document's content is rearranged so the same I-addresses map to different V-positions, do the existing DOCISPAN entries remain frozen at their original values, or are they updated?

### Gregory's Answer

## KB Synthesis

DOCISPAN entries remain frozen at their original values after REARRANGE. They cannot be modified in place, and there is no need to modify them.

**The spanfilade has no modification operation**

[INV-SPANF-WRITE-ONLY] (Finding 0057) establishes this structurally: `insertspanf`, query functions, and nothing else. No `deletespanf`, no `modifyspanf`, no in-place update exists in `spanf1.c` or `spanf2.c`. The spanfilade is append-only by construction.

**DOCISPAN entries don't record V-positions**

This is the key point. From [SS-DOCISPAN] (Findings 0036, 0047), a DOCISPAN entry is:

```
(ISpan: {start: IAddress, width: Nat}) → DocISA
```

It answers: *"Document D contains content at I-address range α..α+n."* V-positions are not stored. DOCISPAN entries live entirely in I-space.

**REARRANGE changes V-positions only**

[INV-REARRANGE-IDENTITY] (Findings 0016, 0018, 0056) states the multiset of I-addresses in a document is invariant under rearrangement — `tumbleradd` modifies only `cdsp.dsas[V]`, never the I-address component. After a pivot or swap, the document still contains the same I-addresses at the same I-addresses; they just appear at different V-positions.

Because DOCISPAN entries record I-address presence, not V-position, a rearrangement that changes where "ABC" appears in V-space does not change the truth of "Document D contains I-addresses α₁..α₃." The entries remain accurate without modification.

**REARRANGE doesn't touch the spanfilade at all**

[FC-CONTENT-SPANF-ISOLATION] confirms this operationally: REARRANGE calls no spanf function. The only operations that write DOCISPAN entries are INSERT (via `docopy` → `insertspanf(..., DOCISPAN)`) and COPY [ST-INSERT], [ST-COPY].

**Summary**

| Question | Answer |
|----------|--------|
| Can DOCISPAN entries be modified in place? | No — the spanfilade has no modification mechanism ([INV-SPANF-WRITE-ONLY]) |
| Are they updated after REARRANGE? | No — REARRANGE doesn't call any spanf function ([FC-CONTENT-SPANF-ISOLATION]) |
| Do they need updating? | No — they record I-address→DocISA, which REARRANGE doesn't change ([INV-REARRANGE-IDENTITY]) |
| Do they remain valid? | Yes — same I-addresses still present in the document, just at different V-positions |

The design is elegant here: by indexing in I-space rather than V-space, DOCISPAN entries are immune to all V-space mutations. INSERT and COPY add new entries; DELETE, REARRANGE, and VERSION leave the spanfilade untouched ([FC-GRANF-ON-DELETE]).

---

## Code Exploration

I have all the evidence I need. Let me write the complete answer.

---

## DOCISPAN Entries Are Frozen — The Spanfilade Is Append-Only

The answer is definitive: **DOCISPAN entries in the spanfilade are never modified in place.** After a document rearrangement, the existing entries remain frozen at their original I-address values. The V-position changes are recorded exclusively in the POOM (permutation matrix), which the spanfilade neither knows about nor replicates.

---

### How DOCISPAN Entries Are Written

`insertspanf` in `spanf1.c:15` is the sole write path into the spanfilade for content-type entries. For a DOCISPAN, it is called as:

```c
insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN)   // do1.c:62
```

Inside `insertspanf` (`spanf1.c:22–51`), each I-span in the `sporglset` becomes one spanfilade crum:

```c
prefixtumbler (isaptr, spantype, &crumorigin.dsas[ORGLRANGE]);   // spanf1.c:22
tumblerclear (&crumwidth.dsas[ORGLRANGE]);                        // spanf1.c:23
// ...
movetumbler (&lstream, &crumorigin.dsas[SPANRANGE]);             // spanf1.c:49
movetumbler (&lwidth, &crumwidth.dsas[SPANRANGE]);               // spanf1.c:50
insertnd(taskptr,(typecuc*)spanfptr,&crumorigin,&crumwidth,&linfo,SPANRANGE);  // spanf1.c:51
```

The resulting crum layout:
- **ORGLRANGE** origin = `DOCISPAN.{doc-isa}` = `4.{doc-isa}` (prefixed with the constant 4)
- **ORGLRANGE** width = 0 (a point, not a span — just a document identity marker)
- **SPANRANGE** origin = the I-address (permascroll stream)
- **SPANRANGE** width = the I-span width (permascroll extent)

`insertnd` inserts along the SPANRANGE dimension. This is pure insertion — `insertnd` can only **add** crums, not replace them.

---

### What `dorearrange` Actually Does

`dorearrange` (`do1.c:34–43`) is the document rearrangement entry point:

```c
bool dorearrange(typetask *taskptr, typeisa *docisaptr, typecutseq *cutseqptr)
{
    typeorgl docorgl;
    bool findorgl(), rearrangepm();;

    return (
       findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
    && rearrangepm (taskptr, docisaptr, docorgl, cutseqptr)
    );
}
```

`rearrangepm` (`orglinks.c:137–142`) does exactly one structural operation:

```c
bool rearrangepm(typetask *taskptr, tumbler *docisaptr, typeorgl docorgl, typecutseq *cutseqptr)
{
    rearrangend((typecuc*)docorgl, cutseqptr, V);
    logbertmodified(docisaptr, user);
    return (TRUE);
}
```

`rearrangend` (`edit.c:78`) operates on `docorgl` — the **POOM node** for the document — along the **V dimension**. It shifts crum V-offsets inside the POOM to reflect the new ordering. The spanfilade (`spanf`) is **never passed** to `rearrangend`, `deletend`, or any other mutating function.

---

### Comprehensive Audit: What Operations Touch `spanf`

All uses of `spanf` in the codebase:

| Location | Operation | Read/Write |
|---|---|---|
| `do1.c:62` | `insertspanf(spanf, ..., DOCISPAN)` | **write** (insert) |
| `do1.c:79` | `insertspanf(spanf, ..., DOCISPAN)` | **write** (insert) |
| `do1.c:191,219` | `insertendsetsinspanf(spanf, ...)` → `insertspanf` | **write** (insert) |
| `spanf1.c:171` | `retrieverestricted((typecuc*)spanf, ...)` | read |
| `spanf1.c:245` | `retrieverestricted((typecuc*)spanf, ...)` | read |
| `spanf1.c:124` | `findlinksfromtothreesp(spanf, ...)` | read |
| `do1.c:352,359` | `findlinksfromtothreesp(spanf, ...)` | read |

There is **no call to `rearrangend(spanf, ...)`** and **no call to `deletend(spanf, ...)`** anywhere in the codebase. The grep for `spanf.*rearrange` and `rearrange.*spanf` returns only two debug `fprintf` print statements inside `#ifdef UnDeFINed` blocks (`edit.c:96`, `edit.c:153`), which are compiled out.

The same is true for `dodeletevspan` (`do1.c:158–167`): it calls `deletevspanpm` (`orglinks.c:145–152`), which calls `deletend((typecuc*)docorgl, ...)` — again only the POOM, never the spanfilade.

---

### The Structural Reason: Different Dimensions Encode Different Facts

The spanfilade and the POOM encode orthogonal information:

- **POOM** (`docorgl`): maps **V-positions → I-spans** for a single document. This is a mutable 2D enfilade that changes on every insert, delete, and rearrange. It tracks *where* content currently appears in a document.

- **Spanfilade** (`spanf`): maps **I-spans → document ISAs** across all documents. The ORGLRANGE dimension identifies the document (prefixed by span type), the SPANRANGE dimension identifies the permascroll region. This tracks *which* documents have ever incorporated given permascroll content.

These record different semantic facts. The POOM answers: "what is at V-position N in document D?" The spanfilade answers: "which document incorporates I-span S?" The second question has a permanent answer — permascroll content is immutable and never leaves a document's identity once incorporated. Rearranging the V-positions of content does not change the fact that the content belongs to the document.

---

### Consequence: DOCISPAN Entries Persist Through Deletion Too

Because `dodeletevspan` also only modifies the POOM and never the spanfilade, a DOCISPAN entry is not removed even when a V-span is deleted. If you insert content (creating a DOCISPAN entry for that I-span), then delete that V-span from the document, the spanfilade still records the document as containing that permascroll region. `finddocscontainingsp` (`spanf1.c:151`) will still return that document for queries against that I-span.

This means the spanfilade's DOCISPAN entries are **permanent historical provenance records**, not current-state membership records. They accumulate monotonically over the lifetime of the store.

---

## Question 20 [gregory]

> When multiple FEBE sessions are active and one session's INSERT allocates new I-addresses, does the run-to-completion scheduling guarantee that no other session can observe the granfilade in a state where the I-address exists but the content bytes are not yet stored?

### Gregory's Answer

## KB Synthesis

Yes, the guarantee holds. The answer follows from the interaction of three KB facts.

**Run-to-completion scheduling is total serialization**

[INV-SEQUENTIAL-DISPATCH] / [INV-ATOMICITY] (Finding 0042): The `bed.c` event loop calls `xanadu(&task)` and blocks until it returns before calling `select()` again. Even when multiple frontends have pending requests, they are dispatched one at a time. No two operations ever interleave.

**INSERT is a single `xanadu()` call**

[ST-INSERT] (Finding 0036) describes the full call chain within one invocation:

```
doinsert → inserttextingranf   (allocates I-addresses AND stores content bytes into a crum)
         → docopy → insertpm   (updates POOM)
                  → insertspanf (creates DOCISPAN)
```

All four steps complete before `xanadu()` returns. There is no yield point between I-address allocation and content storage.

**The in-memory state is shared globally**

[SS-SESSION-STATE] (Finding 0022): The granfilade is global state, not per-session. All sessions read from the same in-memory enfilade. Because run-to-completion ensures no other session runs during an INSERT, the first moment any other session can read the granfilade is after the inserting session's full `xanadu()` call completes — at which point both the I-address and its content bytes are already present in the in-memory crum (marked `modified = TRUE` per [SS-CACHE-MECHANISM] / Finding 0059).

**The disk durability question is separate and does not affect this**

[EC-CRASH-MID-WRITE] (Finding 0059) establishes that crums may not be on disk, but the question concerns observable state between live sessions, not crash recovery. Both the I-address and content bytes reside in the shared in-memory grim-reaper cache immediately after INSERT completes.

**Answer**: The run-to-completion guarantee is sufficient and complete. A session S2 can only observe the granfilade after S1's INSERT has finished executing, at which point the I-address and its content bytes are atomically present together in the in-memory state. The partial state — I-address allocated but content not yet stored — exists transiently within S1's `xanadu()` call and is invisible to all other sessions.

---

## Code Exploration

Now I have everything I need. Let me trace the complete picture across all relevant files.

---

## Answer

The run-to-completion scheduling **does guarantee** that no other session can observe the granfilade in a state where an I-address exists but its content bytes are not yet stored. The guarantee is structural — it flows from the event loop architecture, not from any explicit locking. Here is the evidence, layer by layer.

---

### Layer 1 — The event loop is single-threaded (bed.c)

```c
// bed.c:103-141
for (;;) {
    // ...
    if (select(nfds+1, &inputfds2, 0, 0, &timeout) < 0) { ... }
    else {
        for (i = 0; i <= nfds; i++) {
            if ((1<<i) & inputfds2) {
                user = fdtoplayer[i];           // bed.c:120 — set global user
                task.inp = player[user].inp;
                task.outp = player[user].outp;
                // ...
                xanadu(&task);                  // bed.c:128 — runs to completion
            }
        }
    }
    leave(player, &n_players);
    new_players(player, &n_players, FALSE, &task);
}
```

One request is handled at a time. `xanadu()` is called for session `i`, and only after it **returns** does the loop advance to the next ready file descriptor [bed.c:118–141]. The grep for `pthread`, `mutex`, `semaphore`, `fork`, and `SIGIO` across all backend `.c` files returns nothing. There are no threads, no async I/O signals, and no way for another session's code to run while `xanadu()` is executing.

`xanadu()` itself is equally simple [bed.c:153–172]:

```c
int xanadu(typetask *taskptr)
{
    // ...
    if (getrequest(taskptr, &request)) {
        (*requestfns[request])(taskptr);   // bed.c:162 — full handler runs here
        sendresultoutput(taskptr);         // bed.c:163 — then flush output
    }
    tfree(taskptr);
    // ...
}
```

The request handler (e.g. `insert()`) runs to completion — including all data-structure mutations — before `sendresultoutput()` flushes and before control returns to the `select()` loop.

---

### Layer 2 — The INSERT handler (fns.c:84–98)

```c
void insert(typetask *taskptr)
{
    (void) getinsert(taskptr, &docisa, &vsa, &textset);  // fns.c:90
    putinsert(taskptr);                                   // fns.c:91 — buffers response
    if (!doinsert(taskptr, &docisa, &vsa, textset))      // fns.c:92 — does the work
        fprintf(stderr,"requestfailed in insert\n");
}
```

`putinsert()` buffers the response; `doinsert()` then mutates the granfilade. Both happen inside the same `xanadu()` invocation. stdout is explicitly buffered with `setbuf(stdout, outputbuffer)` [bed.c:90], and player output is flushed only via `sendresultoutput()` [bed.c:163] after `insert()` returns. Another session cannot receive the reply and act on it before `doinsert()` has completed.

---

### Layer 3 — doinsert's call sequence (do1.c:87–123)

```c
bool doinsert(typetask *taskptr, typeisa *docisaptr, tumbler *vsaptr, typetextset textset)
{
    makehint(DOCUMENT, ATOM, TEXTATOM, docisaptr, &hint);
    ret = (inserttextingranf(taskptr, granf, &hint, textset, &ispanset)  // do1.c:118
        && docopy(taskptr, docisaptr, vsaptr, ispanset));                 // do1.c:119
    return(ret);
}
```

`inserttextingranf` [granf1.c:44–47] is a thin wrapper: it calls `inserttextgr` [granf2.c:83–109], which is where the I-address is allocated and content is stored.

---

### Layer 4 — inserttextgr: address allocation and content storage (granf2.c:83–109)

```c
bool inserttextgr(typetask *taskptr, typegranf fullcrumptr, typehint *hintptr,
                  typetextset textset, typeispanset *ispansetptr)
{
    tumbler lsa, spanorigin;
    typegranbottomcruminfo locinfo;

    if (!findisatoinsertgr((typecuc*)fullcrumptr, hintptr, &lsa))  // granf2.c:92
        return (FALSE);
    movetumbler(&lsa, &spanorigin);
    for (; textset; textset = textset->next) {          // granf2.c:95
        locinfo.infotype = GRANTEXT;
        locinfo.granstuff.textstuff.textlength = textset->length;
        movmem(textset->string, locinfo.granstuff.textstuff.textstring,  // granf2.c:98
               locinfo.granstuff.textstuff.textlength);
        insertseq((typecuc*)fullcrumptr, &lsa, &locinfo);  // granf2.c:99
        tumblerincrement(&lsa, 0, textset->length, &lsa);  // granf2.c:100
    }
    // build and return ispanset ...
}
```

`findisatoinsertgr` computes the next available I-address but does **not** write anything to the granfilade — it only reads. The address is held in local variable `lsa`.

`insertseq` [insert.c:17–70] then creates a new bottom crum and writes both the address metadata and the content bytes before returning:

```c
int insertseq(typecuc *fullcrumptr, tumbler *address, typegranbottomcruminfo *info)
{
    // ...
    new = createcrum(0, (INT)ptr->cenftype);          // insert.c:44
    reserve((typecorecrum*)ptr);
    reserve(new);
    adopt(new, RIGHTBRO, (typecorecrum*)ptr);         // insert.c:46 — link into tree
    ivemodified(new);
    splitsomething = splitcrumupwards(findfather(new));
    // ...
    moveinfo(info, &((typecbc*)new)->cinfo);          // insert.c:52 — write content bytes
    // then set width (address range) at lines 54–59
    ivemodified((typecorecrum*)ptr);
    setwispupwards(...);
    // ...
}
```

The new crum enters the tree via `adopt` [insert.c:46], and its content (`moveinfo` [insert.c:52]) and its width (I-address range, lines 54–59) are both set inside the same `insertseq` call. There is no yield point, no blocking I/O, and no other code that could run between these steps.

---

### Layer 5 — The multi-chunk case

If `textset` contains multiple chunks [granf2.c:95], `insertseq` is called once per chunk. After the first chunk's `insertseq` returns and before the second begins, the granfilade logically has an I-address for the first chunk but not the second. This is a real intermediate state — but it is **invisible to all other sessions** because the single-threaded event loop prevents any other `xanadu()` call from running until the entire `insert()` handler returns.

---

### Summary

| Guarantee | Mechanism | Evidence |
|---|---|---|
| No concurrent sessions | Single-process, no threads | No `pthread`/`fork` in backend; single `select()` loop |
| No preemption | Cooperative run-to-completion | `xanadu()` returns only after full handler completes [bed.c:128, 162–163] |
| No async interruption | No SIGIO, only SIGPIPE/SIGHUP/SIGINT | Signal handlers either crash or set a flag; no I/O occurs |
| I-address + content are co-installed | `insertseq` writes both in one call | `adopt` + `moveinfo` + width-setting in [insert.c:46–59] |
| Reply not flushed until after mutation | `putinsert` buffers; `sendresultoutput` flushes | [fns.c:91–92, bed.c:162–163] |

The run-to-completion guarantee is total: the granfilade is a purely in-memory enfilade structure, and the only observation point is a `retrievecrums()` call inside a future `xanadu()` invocation, which can only begin after the INSERT's `xanadu()` invocation has already returned and all crum insertions are complete.
