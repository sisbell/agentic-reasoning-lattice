# Consultation Answers — Address Permanence

**Inquiry:** What guarantees must the system provide about address stability? Once content is assigned an address, what operations may and may not affect that assignment?
**Date:** 2026-03-10 00:34
**Questions:** 20 (10 nelson, 10 gregory)

---

## Question 1 [nelson]

> Once content is assigned a permanent address, must that address remain valid and resolvable for the entire lifetime of the system?

### Nelson's Answer

# Yes — With an Important Distinction

The answer is **yes**, but Nelson distinguishes between two forms of permanence: **address validity** (the address is never reassigned) and **address resolvability** (content is actually accessible). Both are intended to be permanent, but they rest on different foundations.

## Address Validity Is Absolute

The tumbler addressing system is specifically designed so that no address is ever invalidated or reassigned:

> "New items may be continually inserted in tumbler-space while the other addresses remain valid. This means that any address of any document in an ever-growing network may be specified by a permanent tumbler address." [LM 4/19]

This is an architectural guarantee, not a policy choice. The forking mechanism ensures new content gets new sub-addresses without disturbing existing ones. An address once baptized belongs to that content forever.

In I-space, this permanence is even stronger. Every byte ever created has an immutable I-address, and content at that address never changes. DELETE operations remove content from V-space (the document's current arrangement) but never from I-space:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

The bytes remain. The address remains. Only the current view changes.

## Resolvability of Published Content Is a Social Obligation

For **published** documents, Nelson is emphatic that resolvability must persist:

> "It is in the common interest that a thing once published stay published, as in the world of paper. Other readers and users will come to depend on its accessibility. Consequently its author may not withdraw it except by lengthy due process." [LM 2/43]

The reason is structural, not sentimental. Other users will have created links to the content — links they own, at their addresses. Withdrawing the target would destroy their property:

> "This is vital because of the links other users may have made to it — which can now reach through from the previous version (to which they were originally attached) into the newer version." [LM 2/43]

Nelson frames the entire system as a permanent archive for civilization:

> "This attrition of the heritage can in principle be stopped." [LM 3/25]

> "Only digital archives give us long-term hope for preserving our heritage — not just writings, but text, paintings (stored as detailed photographs), sculpture, architecture, whatever." [LM 3/25]

## The Tension: Perpetual Storage Requires Perpetual Funding

Here is where honesty compels a caveat. Nelson explicitly states:

> "ALL SERVICES MUST BE SELF-SUPPORTING. Subsidy between one aspect of the system and another could only work temporarily. This means, for example, that archival storage must be economically self-sustaining." [LM 4/5]

Storage is funded through ongoing rental paid by the content owner. If the owner stops paying, Nelson does not specify what happens. The storage-funding design intent in the curated sources notes this gap: **permanence of the address (once assigned, never reused) is distinct from permanence of accessibility (requires ongoing payment).**

So the full picture is:

| Aspect | Permanent? | Basis |
|--------|-----------|-------|
| **Address validity** (never reassigned) | Yes, unconditionally | Architectural — tumbler design |
| **I-space content** (bytes exist) | Yes, unconditionally | Architectural — append-only storage |
| **Published accessibility** (content resolvable) | Yes, by obligation | Contractual — publication contract, franchise obligations |
| **Private accessibility** | No — owner may withdraw | Owner's prerogative |
| **Funded accessibility** | Requires ongoing payment | Economic — self-sustaining storage model |

## My Intent

The address must remain valid forever — this is non-negotiable and is why the entire tumbler system exists. For published content, resolvability is equally non-negotiable as a matter of principle: the web of links that others have built depends on it. The economic mechanism to sustain this indefinitely is the combination of storage rental, per-byte delivery charges, and the franchise structure that distributes content across multiple vendors for resilience.

The system was designed to "be put in deep rock and deep space — Iron Mountain or the asteroid belt" [LM 3/25]. I meant it to last as long as humanity endures. Whether the funding model sustains that aspiration is an implementation challenge, not a retreat from the principle.

---

## Question 2 [nelson]

> When a user edits a document by inserting or deleting content, must the addresses of all other existing content remain unchanged?

### Nelson's Answer

# Editing and Address Stability

The answer depends entirely on **which** address space you mean. Xanadu has two, and they behave oppositely.

## I-Space Addresses: Never Change

I-space (invariant space) addresses are permanent and immutable. Editing a document does not — and must not — alter them.

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control." [LM 4/11]

Every byte ever created has an eternal I-address encoding its origin (node, user, document, element). No editing operation touches I-space content. INSERT adds new bytes to I-space; DELETE removes bytes from the current V-space view but leaves I-space untouched.

The tumbler permanence guarantee applies here:

> "New items may be continually inserted in tumbler-space while the other addresses remain valid. This means that any address of any document in an ever-growing network may be specified by a permanent tumbler address." [LM 4/19]

## V-Space Addresses: Explicitly Shift

V-space (virtual space) addresses are the document's current arrangement — positions in the "virtual byte stream" as the user sees it now. These **do** change on every edit. Nelson specifies this directly in the INSERT operation:

> "This inserts \<text set\> in document \<doc id\> at \<doc vsa\>. The v-stream addresses of any following characters in the document are increased by the length of the inserted text." [LM 4/66]

And from the general description of V-space:

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." [LM 4/11]

V-addresses are always dense and contiguous (no gaps), so insertions push everything after the insertion point forward, and deletions close the gap.

## Why This Works

The separation is the architectural key. Links and transclusions point to **I-space** addresses, so they survive editing:

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes. This has a crucial advantage: it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them." [LM 4/42]

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." [LM 4/30]

Users work with V-space positions (intuitive, sequential). The system resolves those to I-space addresses (permanent, immutable). Editing changes the V→I mapping — the document's arrangement — while the underlying content and all references to it remain stable.

## Summary

| Address Space | Changes on edit? | Why? |
|---|---|---|
| **I-space** | Never | Content identity is permanent; this is the guarantee that makes links, transclusion, and correspondence work |
| **V-space** | Always | The document's arrangement is what editing *means*; V-addresses shift to maintain a dense, contiguous byte stream |

The invariant is: **I-space addresses of existing content must never change.** V-space addresses are expected to change — that is editing.

---

## Question 3 [nelson]

> If the same content appears in multiple documents through inclusion, must it be reachable through a single stable address regardless of how many documents reference it?

### Nelson's Answer

**Yes.** This is not merely a feature but a foundational architectural property. Content lives at exactly one permanent I-space address, and every inclusion references that same address.

## The Architecture

Xanadu separates content identity (I-space) from document arrangement (V-space). When content is created, it gets a permanent I-address. When another document includes that content, it creates a V-space mapping that points to the *same* I-address — it does not create a second copy.

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

The COPY operation (which implements transclusion) explicitly shares I-addresses with the source. It does not duplicate content into a new I-space location.

## Why This Must Be So

Three guarantees depend on it:

**1. Origin traceability.** The I-address encodes which document created the bytes. If inclusion created new addresses, origin would be lost.

> "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

**2. Content discovery.** FINDDOCSCONTAINING works by searching for shared I-addresses:

> "This returns a list of all documents containing any portion of the material included by \<vspec set\>." [LM 4/70]

If each inclusion had its own address, this operation would be impossible — there would be no structural link between the "same" content in different documents.

**3. Automatic royalties.** The system pays the original author when their bytes are delivered. This requires knowing that bytes in document B are the *same bytes* as those in document A — which is determined by shared I-address, not by content comparison.

## The Fetching Mechanism Enforces It

When a front end requests content from a compound document, non-native bytes are "obtained by front-end or back-end requests to their home locations" [LM 4/11]. The content is fetched from its single permanent location. The connection cannot be severed because the retrieval mechanism *requires* the I-address to function.

Content identity in Xanadu is based on creation, not on value. Two documents with identical text created independently have *different* I-addresses. Transcluded content *shares* the same I-address. This distinction — same-content-by-reference vs. same-content-by-coincidence — is only possible because there is one stable address per piece of created content, regardless of how many documents include it.

## Summary

The single stable I-address is not just reachable — it is the *only* address for that content. Each including document has its own V-address for where that content appears in its arrangement, but the underlying identity is always the one permanent I-space address. Ten thousand documents can include the same paragraph; there is still exactly one I-address for it, and that address resolves to the same bytes forever.

---

## Question 4 [nelson]

> Must the address of content be determined solely by when it was created, or may the system reassign addresses to optimize retrieval?

### Nelson's Answer

# Addresses Are Permanent: The Non-Negotiable Invariant

**The address of content is determined at creation and may never be reassigned.** This is not a design preference — it is the invariant upon which the entire system depends.

## The Two Address Spaces

Xanadu has two address spaces with fundamentally different permanence properties:

**I-Space addresses are permanent and immutable.** Content gets an I-space address when created, and that address returns that exact content forever. The permascroll is append-only:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

**V-Space addresses are explicitly ephemeral.** They change with every edit:

> "The v-stream addresses of any following characters in the document are increased by the length of the inserted text." [LM 4/66]

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." [LM 4/30]

V-space is the system's built-in mechanism for "reassigning" the user-visible arrangement without touching content identity.

## Why I-Space Reassignment Is Forbidden

The permanence of I-space addresses is the foundation for every major guarantee:

| Guarantee | Depends on permanent I-addresses because... |
|-----------|----------------------------------------------|
| **Link survivability** | Links point to I-space; they survive editing because I-addresses don't change |
| **Transclusion** | Inclusion by reference works because the reference (I-address) is stable |
| **Version comparison** | Correspondence is detected via shared I-space origin |
| **Origin traceability** | The I-address encodes the home document — reassignment would sever attribution |
| **Permanent citation** | A reference made today must work forever |

Nelson states this directly:

> "New items may be continually inserted in tumbler-space while the other addresses remain valid. This means that any address of any document in an ever-growing network may be specified by a permanent tumbler address." [LM 4/19]

## Physical Location May Change; Addresses May Not

The system explicitly separates logical address from physical location. The BEBE protocol moves content between servers for performance optimization:

> "Material is moved between servers for a number of purposes: 1. for more rapid access to final material, 2. for more rapid access to needed material which indexes material on other servers, 3. for rebalance in keeping with demand, 4. for redundancy and backup purposes." [LM 4/71]

> "The contents can slosh back and forth dynamically." [LM 4/72]

This is the correct place for retrieval optimization: move the bytes closer to demand, cache popular content, replicate for resilience — but the tumbler address stays fixed. The user sees the same address regardless of which server physically holds the content.

## The Enfilade Solution

Nelson's enfilades are specifically designed to make permanent addressing efficient despite continuous editing:

> "His new method would allow linkages to keep up with all changes. It was instantaneous and permanent and could grow indefinitely. All changes, once made, left the file remaining in canonical order, which was an internal mandate of the system." [LM 1/34]

The enfilades maintain the V→I mapping (POOM enfilade) and the content storage (GRAN enfilade) so that retrieval remains fast even as the mapping grows complex. The "eye in the pyramid" insight was precisely about making permanent addresses work efficiently — solving the performance problem without sacrificing the permanence invariant.

## Time Is Not the Address

One subtlety: while I-space is append-only (chronological), time itself is not encoded in the tumbler:

> "Note that 'time' is not included in the tumbler. Time is kept track of separately." [LM 4/18]

The address encodes *provenance* (server, user, document, element position), not timestamp. Within a document's I-stream, later-created content gets higher element numbers because append-only storage is sequential — but the address is a structural identifier, not a temporal one.

## Summary

The system has a clear answer to your question:

- **I-space addresses**: determined solely at creation, permanent, never reassigned — this is inviolable
- **V-space addresses**: ephemeral by design, change with every edit — this is the intended mechanism for rearrangement
- **Physical location**: may change freely for optimization — BEBE handles this transparently
- **Performance**: achieved through data structures (enfilades) and caching (subrepresentations), never through address reassignment

Reassigning I-space addresses would be like reassigning DNA — it would sever every relationship (links, transclusions, version correspondence, attribution) that depends on content identity. The entire docuverse is built on the assumption that I-space addresses are eternal.

---

## Question 5 [nelson]

> When a new version of a document is created, must content retained from the prior version keep its original address, or may versioning introduce new addresses for the same material?

### Nelson's Answer

## Answer: Retained Content Must Keep Its Original I-Space Addresses

This is not a design choice left to implementors — it is architecturally required. The entire Xanadu model collapses without it.

### The Direct Evidence

CREATENEWVERSION is described as:

> "This creates a new document with the contents of document \<doc id\>. It returns the id of the new document. The new document's id will indicate its ancestry." [LM 4/66]

The new document gets a **new document address** (with ancestry encoded in the tumbler), but its content — its V-space — maps to the **same I-space bytes** as the original. The operation creates a new arrangement, not new content.

This is confirmed by the COPY operation, which explicitly shares I-addresses:

> "The material determined by \<spec set\> is copied to the document determined by \<doc id\> at the address determined by \<doc vsa\>." [LM 4/67]

COPY is transclusion — inclusion by reference to existing I-space content. CREATENEWVERSION is effectively a COPY of the entire document's content into a new document shell.

### Why This Is Required, Not Optional

**1. Correspondence depends on it.**

Correspondence — the ability to identify which parts of two versions are the same — is defined as a structural relation based on shared I-space origin:

> "Of course, a facility that holds multiple versions of the same material, and allows historical backtrack, is not terribly useful unless it can help you intercompare them in detail — unless it can show you, word for word, what parts of two versions are the same." [LM 2/20]

SHOWRELATIONOF2VERSIONS:

> "This returns a list of ordered pairs of the spans of the two spec-sets that correspond." [LM 4/70]

If versioning introduced new I-addresses for retained material, this operation would have **nothing to match on**. The system identifies corresponding parts by finding V-space positions in different versions that map to the same I-space addresses. No shared I-addresses means no correspondence, which means no version comparison.

**2. Content identity is based on origin, not value.**

Two documents with identical text created independently have **different** I-addresses. Transcluded content **shares** the same I-address. This is how the system distinguishes "wrote the same words independently" from "quoted from the original." If versioning created new I-addresses, the system would lose the provenance chain — it could no longer tell whether version 2 retained content from version 1 or merely happened to contain the same words.

**3. Non-destruction requires it.**

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

Versions share I-space content. Deleting from one version's V-space does not affect other versions because they all reference the same permanent I-space bytes. If each version had its own I-space copy, this guarantee would require a completely different (and far more complex) mechanism.

**4. The append-only model implies it.**

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

Content is written once to I-space and never duplicated. Each version is a different V-space arrangement over the same I-space content. Only genuinely **new** content (insertions, additions) gets new I-space addresses.

**5. Refractive link following requires it.**

> "Links may be refractively followed from a point or span in one version to corresponding places in any other version. Thus a link to one version of a Prismatic Document is a link to all versions." [LM 2/26]

A link made to version 1 "reaches through" to version 2 because both versions' V-spaces map to the same I-space bytes. The link targets I-space; the system traces which V-space positions in any version correspond to those I-space addresses. Without shared I-addresses, refractive following would be impossible.

### Summary

When CREATENEWVERSION is called:

| What gets a new address | What keeps its original address |
|---|---|
| The document itself (new tumbler with ancestry) | All retained content (same I-space bytes) |
| New V-space arrangement | I-space addresses of every retained byte |

The new version is a **new view** (V-space) over **existing content** (I-space). Only content that is genuinely new — inserted or appended after versioning — receives fresh I-space addresses. Everything retained from the prior version keeps its original address. This is not an optimization; it is the mechanism by which correspondence, attribution, link survivability, and version comparison all function.

---

## Question 6 [nelson]

> Must links that reference content by address continue to resolve correctly after any sequence of editing operations performed on the linked document?

### Nelson's Answer

# Yes — Links Must Resolve After Any Editing Sequence

This is one of the most fundamental guarantees I designed into Xanadu. Links attach to **bytes**, not to **positions**. Editing changes positions; it does not change bytes. Therefore editing cannot break links.

## The Mechanism

The key is the separation of I-space (permanent content) from V-space (current arrangement):

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." [LM 4/30]

When you INSERT, DELETE, or REARRANGE, you are modifying V-space — the document's current arrangement. The I-space addresses where content permanently lives are untouched. Links point to I-space. Therefore:

- **INSERT** shifts V-space positions after the insertion point. Links are unaffected — they don't point to V-space positions.
- **DELETE** removes content from V-space but not from I-space. The bytes still exist at their permanent addresses. Links still resolve.
- **REARRANGE** reorders V-space. The bytes themselves don't move in I-space. Links still resolve.
- **COPY** (transclusion) creates new V-space mappings to existing I-space content. Original links still point to the same I-space bytes.

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." [LM 4/11]

V-space addresses are ephemeral. I-space addresses are eternal. Links use I-space.

## The Survivability Guarantee

I stated this explicitly:

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes. This has a crucial advantage: it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them. This also works for alternative versions in which part of each end has survived." [LM 4/42]

And the visual annotation on the facing page:

> "SURVIVABILITY: Links between bytes can survive deletions, insertions and rearrangements, **if anything is left at each end.**" [LM 4/43]

## The Qualification: "If Anything Is Left"

The one condition is that **some bytes must remain at each endset**. If every byte that a link's from-set or to-set references is deleted from V-space, the link has nothing to display in the current version.

But even this is not true destruction. Deleted bytes enter the state I described:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

The bytes still exist in I-space. The link still resolves to them. They are merely "not currently addressable" in the current V-space arrangement. Previous versions still contain them, other documents that transclude them still show them, and historical backtrack can reconstruct them.

## Why This Matters for Published Documents

This guarantee is not merely technical — it is the foundation of the publication contract:

> "It is in the common interest that a thing once published stay published, as in the world of paper. Other readers and users will come to depend on its accessibility. Consequently its author may not withdraw it except by lengthy due process." [LM 2/43]

> "However, for corrections and amendments, the author may readily publish a superseding document, but the former version must remain on the network. This is vital because of the links other users may have made to it — which can now reach through from the previous version (to which they were originally attached) into the newer version." [LM 2/43]

Links made by other users are **their property**, stored at **their addresses**. Those links depend on the continued resolvability of the content they reference. This is precisely why published content cannot be withdrawn — doing so would break others' property.

## Summary

The answer is **yes, unconditionally** at the I-space level. Links always resolve to the same permanent bytes regardless of editing. At the V-space level, the bytes may no longer appear in the current version (if deleted), but they remain in I-space, in previous versions, and in any other documents that transclude them. The link never "breaks" — the content it references is permanent by design.

---

## Question 7 [nelson]

> If a user deletes content from a document, must the system preserve the address assignment so that historical references and links remain valid?

### Nelson's Answer

## Yes — absolutely and by multiple reinforcing principles.

Deletion in Xanadu removes content from the document's **V-space** (current arrangement) but does **not** remove it from **I-space** (permanent storage). The address assignment is permanent. This is not a design preference — it is load-bearing architecture upon which links, versions, transclusion, and attribution all depend.

---

### 1. DELETE is a V-space operation, not an I-space operation

The diagram on page 4/9 explicitly shows "DELETED BYTES" as a valid system state:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

And Nelson clarifies:

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

The bytes are removed from the current view. They are not destroyed, and their I-space addresses remain occupied.

---

### 2. Tumbler addresses are permanent by design

> "New items may be continually inserted in tumbler-space while the other addresses remain valid. This means that any address of any document in an ever-growing network may be specified by a permanent tumbler address." [LM 4/19]

An address, once assigned, is never invalidated and never reused. This applies to all content — including content that has been "deleted" from a document's current version.

---

### 3. Links depend on I-space permanence

Links attach to spans of bytes in I-space, not to positions in V-space:

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes. This has a crucial advantage: it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them." [LM 4/42]

If deletion destroyed I-space addresses, every link to the deleted content would break — violating the survivability guarantee. The entire link architecture assumes that I-space content is permanent.

---

### 4. Historical backtrack requires reconstructability

> "The file management system we are talking about automatically keeps track of the changes and the pieces, so that when you ask for a given part of a given version at a given time, it comes to your screen." [LM 2/15]

If deleted content lost its address, previous versions could not be reconstructed. The historical backtrack guarantee — that you can always return to any previous state — requires that all I-space content remain at its permanent address.

---

### 5. The storage paradigm is append-only

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

> "Virtually all of computerdom is built around the destructive replacement of successive whole copies of each current version." [LM 2/14]

Nelson designed Xanadu specifically to reject destructive replacement. The append-only model means content is added but never overwritten or removed. Deletion is a change to the arrangement (V-space), not the archive (I-space).

---

### 6. Transclusion depends on permanent addresses

Other documents may transclude the "deleted" content:

> "The virtual byte stream of a document may include bytes from any other document." [LM 4/10]

If Alice's document transcludes a paragraph from Bob's document, and Bob "deletes" that paragraph from his current version, Alice's document still shows it — because Alice's V-space mapping points to Bob's I-space address, which is permanent. Destroying the address would break Alice's document.

---

### Summary

The answer follows from the fundamental separation of I-space and V-space. Deletion is a V-space operation — it changes what the document currently shows. The I-space address, the content at that address, and all references to it (links, transclusions, version history) remain intact. This is not optional; it is the architectural invariant upon which permanence, link survivability, historical backtrack, and transclusion all rest.

---

## Question 8 [nelson]

> Must every unit of content ever added to the system receive a unique address that is never reused for different content?

### Nelson's Answer

# Yes — Absolutely and By Design

Every unit of content in Xanadu receives a unique address that is never reused for different content. This is not merely a policy but an architectural invariant that follows from multiple interlocking design decisions.

## The Permanent Address Guarantee

Nelson states the guarantee directly:

> "New items may be continually inserted in tumbler-space while the other addresses remain valid. This means that any address of any document in an ever-growing network may be specified by a permanent tumbler address." [LM 4/19]

The key phrase is "while the other addresses remain valid." Inserting new content never disturbs existing addresses. Reusing an address for different content would violate this — the old address would no longer be "valid" for its original content.

## Append-Only Storage Enforces It

The storage model is explicitly append-only:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

In an append-only system, content is added to the end of the store. Nothing is overwritten. Every byte gets a fresh position. This is the physical mechanism that prevents address reuse.

## I-Space Immutability

Content in I-space (the permanent identity space) never changes at its address. Nelson describes native bytes as permanently residing at their "home locations":

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

The I-address encodes which server, which user, which document, and which element position created the content. To reuse that address for different content would be to claim a different origin than the content actually has.

## Forking Creates, Never Recycles

The tumbler forking mechanism creates new addresses by subdivision — adding digits to the right:

> "One digit can become several by a forking or branching process. This consists of creating successive new digits to the right; we call these 'under' the previous digit." [LM 4/20]

> "The owner of a given item controls the allocation of the numbers under it." [LM 4/20]

This is a tree that only grows. Addresses are "baptized" by their owners, never reclaimed and reassigned. There is no garbage collection of address space.

## Even "Deletion" Preserves the Address

When content is "deleted," it is removed from the document's V-space arrangement but remains at its I-space address:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

"Deleted" bytes are not erased — they become "not currently addressable" in that particular view. The I-address still holds the original content. This is the strongest evidence that address reuse is impossible by design.

## Origin Traceability Depends On It

Nelson guarantees that you can always trace content to its origin:

> "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

If address `1.0.3.0.7.0.42` means "the 42nd byte of document 7 by user 3 on server 1," and that address were later reused for different content, this guarantee would be meaningless. The address IS the provenance. Reuse would be forgery.

## The Ministry of Truth Problem

Nelson was explicitly concerned about systems that allow replacement of content at the same address:

> "A reference article, say, in an encyclopedia can be changed simply by storing another one in its place—and poof! history is changed." [LM 3/19–3/22]

Xanadu's entire architecture is designed to make this impossible. Permanent, unique, never-reused addresses are the mechanism that prevents it.

## Summary

The uniqueness and non-reuse of addresses is not a single stated rule but the convergence of every major architectural decision: append-only storage ensures no overwriting, forking addressing ensures no recycling, I-space immutability ensures no mutation, deletion semantics ensure no erasure, and origin traceability ensures addresses carry permanent meaning. To reuse an address would simultaneously violate the permanence guarantee, the attribution guarantee, the version history guarantee, and the non-destruction guarantee.

---

## Question 9 [nelson]

> When content is quoted or transcluded into a new document, must the address visible to the reader be the original author's address, preserving the connection to source?

### Nelson's Answer

## Yes — and it's structural, not optional

When content is transcluded, the original author's I-space address **is** the address of that content. There is no separate copy with a different address. The connection to source is not a feature that could be turned on or off — it is an architectural consequence of how transclusion works.

### The mechanism

Transclusion (COPY in FEBE) creates a V-space mapping to **existing** I-space content. The I-space address encodes the originating document:

```
Node.0.User.0.Document.0.Element
```

When a reader encounters transcluded content, the system fetches it from its home location:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

The transcluded bytes are not duplicated — they are referenced. The I-address of every byte permanently encodes which document created it, which user owns that document, and which server stores it. This cannot be severed because the fetching mechanism requires it.

### The guarantee

Nelson states this as an absolute:

> "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

And from the fundamental guarantees: attribution is **structural, not metadata that can be stripped**. In conventional systems, an author field or copyright notice can be removed during copying. In Xanadu, the I-address IS the attribution — to access the content at all, you must resolve its home address.

### What the reader sees

The reader interacts through V-space — the document's current arrangement. Transcluded content occupies V-space positions in the quoting document "just as if they were native to the document" [LM 4/11]. But the system always knows the difference:

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

Nelson's glass-pane metaphor makes the reader experience vivid:

> "Think of the present document as a sheet of glass. It may have writing painted on it by the present author; it may have clear glass, windowing to something else; the next pane may be in turn made of more layers of painted glass, with more windows, and so on indefinitely." [LM 2/34]

The reader can always "step through the window" to reach the original work. And from any character, the reader can query which document is its home. The front end determines how prominently this information is displayed, but the system must always make it available.

### Bidirectional discovery

The connection works in both directions. Not only can a reader of the quoting document trace content back to its source, but a reader of the **original** document can discover all documents that transclude from it:

> FINDDOCSCONTAINING: "This returns a list of all documents containing any portion of the material included by \<vspec set\>." [LM 4/70]

This is possible precisely because transcluded content shares I-addresses with the original — the system can find every document that references a given piece of I-space content.

### Why this matters

This is not an incidental property. It is the mechanism that makes automatic royalties, permanent attribution, and the "pluralistic publishing form" possible. When content is transcluded and delivered to a reader, the system knows exactly whose content it is delivering and can route payment accordingly:

> "If a modified document is read, the original owner and the modifier split the royalty in proportion to who wrote what, as determined automatically." [LM 2/45]

The original author's address is preserved not merely as a courtesy but as the structural foundation of the entire economic and intellectual model. Sever the connection, and you break attribution, royalties, bidirectional discovery, and the web of literature itself.

---

## Question 10 [nelson]

> Must the system guarantee that no operation — creation, editing, deletion, sharing, or reorganization — can cause two distinct pieces of content to share the same address?

### Nelson's Answer

## Yes — Address Uniqueness Is a Necessary Guarantee

The system must guarantee that no operation causes two distinct pieces of content to share the same address. This is not stated as a single explicit axiom in Literary Machines, but it is an inescapable consequence of multiple architectural properties that Nelson *does* specify, and its violation would break several fundamental guarantees.

---

### The Architectural Properties That Enforce It

**1. I-Space Immutability**

Content at an I-space address never changes. Nelson states:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control." [LM 4/11]

The I-space guarantee in the curated sources is explicit: "Every byte you create gets a permanent I-space address. That address will always return that exact content. Content is immutable — it never changes after creation."

If two distinct pieces of content could occupy the same I-address, the system could not honor "that address will always return that exact content" — it would not know which content to return.

**2. Append-Only Storage**

Nelson explicitly rejects overwriting:

> "Virtually all of computerdom is built around the destructive replacement of successive whole copies of each current version." [LM 2/14]

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

Append-only means new content always gets new addresses. No existing address is ever reused or overwritten.

**3. Ownership-Based Address Allocation (Baptism)**

The forking mechanism prevents collisions through delegated ownership:

> "The owner of a given item controls the allocation of the numbers under it." [LM 4/20]

> "For instance, if there is an item 2, it can branch into several more items, each of which is a daughter item. Thus 2.1, 2.2, 2.3, 2.4... are successive items being placed under 2." [LM 4/20]

Each owner allocates sequential sub-addresses under their own prefix. No coordination between owners is needed because their address subtrees are disjoint by construction.

**4. Unbounded Address Space (Humbers)**

The address space can never be exhausted, eliminating forced collisions:

> "Humber stands for 'humungous number.' ... they are a data structure of the class usually called Bignums, that is, a way of representing numbers that may range up to very great size." [LM 4/13]

> "Small incremental humbers are one byte long. But very large humbers adhere to the same format." [LM 4/13]

Because each tumbler digit has no upper limit, the system can always allocate fresh addresses.

---

### Why Violation Would Break the System

Address uniqueness is load-bearing — without it, multiple fundamental guarantees collapse:

**Permanence.** Nelson guarantees: "any address of any document in an ever-growing network may be specified by a permanent tumbler address" [LM 4/19]. If two things shared an address, "permanent addressing" becomes meaningless — you cannot permanently refer to something if the reference is ambiguous.

**Origin Traceability.** Nelson guarantees: "You always know where you are, and can at once ascertain the home document of any specific word or character" [LM 2/40]. The I-address encodes the home document (Node.0.User.0.Document.0.Element). If two distinct pieces of content shared an I-address, the system could not determine which document created which content.

**Correspondence.** Shared I-space origin is how the system detects that two V-space positions correspond across versions. If addresses could collide, false correspondences would appear — the system would claim two passages correspond when they merely happen to share a collided address.

**Royalties.** The cash register "increments whenever bytes or links are delivered out of the document" [LM 5/13]. Ambiguous addresses would mean ambiguous payment — the system couldn't determine which owner to credit.

**Link Integrity.** Links point to I-space spans. If those spans could refer to two different pieces of content, the link's meaning becomes indeterminate.

---

### No Operation Can Produce a Collision

Examining each FEBE operation:

| Operation | Why No Collision |
|-----------|-----------------|
| **INSERT** | Creates new I-space bytes with fresh addresses; V-addresses shift but I-addresses are new [LM 4/66] |
| **APPEND** | Adds to I-space at document end — new bytes, new addresses [LM 4/67] |
| **DELETEVSPAN** | Removes V-space mapping only; I-space unchanged [LM 4/9] |
| **COPY** | Transclusion — references *existing* I-addresses, does not create new content [LM 4/67] |
| **REARRANGE** | Pure V-space reordering; I-space unchanged [LM 4/67] |
| **CREATENEWDOCUMENT** | System allocates a new unique document address [LM 4/65] |
| **CREATENEWVERSION** | New document address via forking; I-space content is shared by design [LM 4/66] |
| **MAKELINK** | Links get sequential addresses in the 2.x subspace: "permanent order of arrival" [LM 4/31] |

Note the important distinction with COPY (transclusion): this intentionally shares I-addresses, but that is the *same* content referenced from multiple V-space locations — not two *distinct* pieces of content at the same address. Nelson makes this explicit:

> "Content identity is based on creation, not value. Two documents with identical text created independently have DIFFERENT I-addresses. Transcluded content SHARES the same I-address."

This is the design working as intended. Transclusion means "this IS that content," not "this happens to be at the same address as that content."

---

### Summary

Address uniqueness — that each I-space address maps to exactly one piece of content — is a necessary system guarantee. It follows from the conjunction of append-only storage (no overwriting), ownership-based address allocation (no collisions between owners), I-space immutability (content at an address never changes), and unbounded address space (no exhaustion forcing reuse). Nelson does not state it as an isolated axiom because it emerges inevitably from these design choices, any one of which would be independently sufficient to prevent collision. Its violation would cascade into failures of permanence, attribution, correspondence, royalties, and link integrity.

---

## Question 11 [gregory]

> When `findisatoinsertmolecule` allocates a new I-address as max+1, is there any scenario — concurrent sessions, CREATELINK interleaving, or version creation — where two distinct content insertions could receive the same I-address?

### Gregory's Answer

## KB Synthesis

No. Two distinct content insertions cannot receive the same I-address. Here is the synthesis:

## The Allocation Mechanism

`findisatoinsertmolecule` is stateless — it queries the granfilade tree for the current maximum I-address via `findpreviousisagr`, then returns max+1 [SS-ADDRESS-SPACE, Finding 0061]. There is no cached counter; allocation is a pure function of the in-memory granfilade state at call time.

## Why Collision Is Impossible

**1. Sequential dispatch eliminates interleaving.**

The `bed.c` event loop processes every FEBE operation via run-to-completion scheduling. `xanadu(&task)` — which includes request parsing, the full `doXXX` path (allocation + granfilade write + POOM update), response emission, and cleanup — completes entirely before `select()` is called again [INV-ATOMICITY, INV-SEQUENTIAL-DISPATCH, Finding 0042].

Even when multiple sessions have simultaneous pending requests, the loop iterates over ready file descriptors sequentially. Session A's INSERT runs to completion — including writing the new I-address into the granfilade — before session B's INSERT begins. When B calls `findpreviousisagr`, it reads the live in-memory granfilade and sees A's I-address as the new maximum. B allocates max+1, which is strictly greater.

**2. I-addresses are never reused.**

The granfilade is append-only. DELETE and REARRANGE modify only the POOM (V-to-I mappings) and never touch the granfilade [FC-GRANF-ON-DELETE, Finding 0061]. Since `findpreviousisagr` returns the highest I-address present in the granfilade — including those of content deleted from V-space — no gap created by deletion can be filled by a subsequent allocation [INV-NO-IADDR-REUSE].

**3. CREATELINK does not cause collision — only non-contiguity.**

CREATELINK allocates a link orgl I-address from the same granfilade via `createorglingranf`. This advances the allocation ceiling, so a subsequent text INSERT receives an I-address above the link orgl's — creating a gap in the text I-address subsequence [INT-LINK-INSERT, Finding 0063]. But because CREATELINK runs to completion atomically before any subsequent INSERT begins, the two allocations are strictly ordered and cannot produce the same value. Contiguity is broken; uniqueness is not.

**4. CREATENEWVERSION is irrelevant.**

VERSION allocates only a document address (via `findisatoinsertnonmolecule` for non-molecules). It does NOT call `findisatoinsertmolecule` or any content I-address allocator [ST-VERSION, Finding 0077]. It leaves the content allocation ceiling untouched, so it cannot interfere with text I-address allocation at all.

## Summary

| Scenario | Can it cause I-address collision? | Why |
|---|---|---|
| Concurrent sessions | No | Sequential dispatch: operations never interleave |
| CREATELINK interleaving | No | CREATELINK completes atomically before next INSERT; only breaks contiguity |
| Version creation | No | Does not allocate content I-addresses |
| DELETE between INSERTs | No | Granfilade is append-only; max only increases |

The monotonic invariant `∀ alloc_a, alloc_b : time(a) < time(b) ⟹ iaddr(b) > iaddr(a)` holds unconditionally [INV-MONOTONIC]. Combined with sequential dispatch [INV-SEQUENTIAL-DISPATCH] and no I-address reuse [INV-NO-IADDR-REUSE], uniqueness of allocated I-addresses is guaranteed across all scenarios.

---

## Code Exploration

I now have everything needed. Here is the complete analysis.

---

## Can `findisatoinsertmolecule` Produce Duplicate I-Addresses?

**Short answer: No.** Three independent properties of the implementation jointly guarantee uniqueness. Here is the proof from source.

---

### 1. The Event Loop Is Strictly Single-Threaded

`bed.c:103-143` shows the main loop:

```c
for (;;) {
    inputfds2 = inputfds;
    if (select(nfds+1, &inputfds2, 0, 0, &timeout) < 0) { ... }
    else {
        for (i = 0; i <= nfds; i++) {
            if ((1<<i) & inputfds2) {
                user = fdtoplayer[i];
                ...
                xanadu(&task);          // [bed.c:128]
```

`xanadu()` at `bed.c:153-172` processes **one request to full completion** — including `sendresultoutput` — before the outer `for` loop re-enters `select`. There are no OS threads, no coroutines, and no preemption. The global `int user` at `bed.c:28` is a single value, not per-thread.

**Consequence:** No two invocations of `findisatoinsertmolecule` from different sessions can interleave. "Concurrent sessions" in this backend means *multiplexed serial*, not parallel.

---

### 2. Allocation Is Immediately Committed to the Enfilade Before Any Return

`findisatoinsertmolecule` is the allocation function. Its two callers — `inserttextgr` and `createorglgr` — both call `insertseq()` as the very next operation after the allocation completes:

**`createorglgr` [granf2.c:111-128]:**
```c
if (!findisatoinsertgr ((typecuc*)fullcrumptr, hintptr, isaptr))
    return (FALSE);
locinfo.infotype = GRANORGL;
locinfo.granstuff.orglstuff.orglptr = createenf (POOM);
...
insertseq ((typecuc*)fullcrumptr, isaptr, &locinfo);  // ← immediate commit
```

**`inserttextgr` [granf2.c:92-101]:**
```c
if (!findisatoinsertgr ((typecuc*)fullcrumptr, hintptr, &lsa))
    return (FALSE);
movetumbler (&lsa, &spanorigin);
for (; textset; textset = textset->next) {
    ...
    insertseq ((typecuc*)fullcrumptr, &lsa, &locinfo);  // ← immediate commit
    tumblerincrement (&lsa, 0, textset->length, &lsa);  // advance, not re-allocate
}
```

Note that multi-chunk text insertions do not re-call `findisatoinsertmolecule` — `lsa` is incremented directly and `insertseq` is called for each chunk. So there is no re-entry into the allocator within a single `inserttextgr` call.

**`insertseq` [insert.c:17-60]** modifies the in-memory enfilade tree immediately:

```c
reserve ((typecorecrum*)ptr);
new = createcrum (0,(INT)ptr->cenftype);
reserve (new);
adopt (new, RIGHTBRO, (typecorecrum*)ptr);
ivemodified (new);
splitsomething = splitcrumupwards (findfather (new));
...
moveinfo (info, &((typecbc *)new)->cinfo);
```

This is entirely synchronous in-memory tree restructuring. There is no write buffer, no journal, no deferred phase. The node is inserted into the live tree before `insertseq` returns.

---

### 3. `findpreviousisagr` Always Reads the Live In-Memory Tree

The "find max" step in `findisatoinsertmolecule` [granf2.c:164]:

```c
findpreviousisagr ((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);
```

`findpreviousisagr` [granf2.c:255-278] recursively traverses the enfilade using `findleftson` / `findrightbro` (via `genf.c`), which call `rejuvinate` to page in nodes from disk on demand. The in-memory tree is always the authoritative current state — any I-address committed via `insertseq` in a prior call is already in this tree and will be found as `lowerbound`, causing the next allocation to increment past it.

---

### 4. No Single Request Calls the Allocator Twice for the Same Namespace

Tracing every path that reaches `findisatoinsertmolecule` through the ATOM branch of `findisatoinsertgr` [granf2.c:135-143]:

| Request handler | Calls into allocator |
|---|---|
| `doinsert` [do1.c:87] | `inserttextingranf` once → `inserttextgr` → allocates text I-span; then `docopy` → `insertpm` + `insertspanf` (no allocator call) |
| `docreatelink` [do1.c:195] | `createorglingranf` once → `createorglgr` → allocates link orgl; then `tumbler2spanset`, `findnextlinkvsa`, `docopy` (no allocator call) |
| `docreatenewdocument` [do1.c:234] | `createorglingranf` once (DOCUMENT hint, non-ATOM path via `findisatoinsertnonmolecule`) |
| `docreatenewversion` [do1.c:260] | `createorglingranf` once; then `docopyinternal` → `insertpm` + `insertspanf` (no allocator call) |

No request triggers two ATOM-path allocations in the same document namespace without committing between them.

---

### 5. The LINKATOM Branch: Structurally Safe But Subtle

The LINKATOM allocation branch [granf2.c:170-175]:

```c
tumblerincrement (&hintptr->hintisa, 2, 2, isaptr);   // base = doc.0.2
if (tumblercmp (&lowerbound, isaptr) == LESS)
    tumblerincrement (isaptr, 1, 1, isaptr);            // → doc.0.2.0.1
else
    tumblerincrement (&lowerbound , 0, 1, isaptr);      // → prev + {0:1}
```

Text atoms occupy `doc.0.1.x` and link atoms occupy `doc.0.2.x` (both are `tumblerincrement(&hintisa, 2, atomtype, ...)` where `TEXTATOM=1`, `LINKATOM=2`). When `lowerbound` is a text entry at `doc.0.1.x`, it is numerically LESS than `doc.0.2`, so the first link always lands at `doc.0.2.0.1`. Subsequent links find a `lowerbound` at `doc.0.2.x` which is GREATER-OR-EQUAL to the base, taking the `else` branch: `lowerbound + {0:1}`.

This is safe because `lowerbound` is freshly queried from the live tree each time.

---

### Conclusion

There is **no scenario** — including concurrent sessions, CREATELINK interleaving, or version creation — where two distinct content insertions receive the same I-address. The guarantee rests on three interlocking facts:

1. **Single-threaded serial dispatch** [`bed.c:103-143`]: The `select`-based event loop processes requests one at a time. "Concurrent sessions" means queued, not parallel.

2. **Immediate in-memory commit** [`granf2.c:99`, `granf2.c:125`]: `insertseq` places the allocated address into the live enfilade tree synchronously. When the next request runs, `findpreviousisagr` will find it.

3. **No re-entrant allocation within a request** [`do1.c:87-122`, `do1.c:195-220`]: Every request calls the allocator at most once per document namespace before committing. Subsequent operations (`insertpm`, `insertspanf`, `docopy`) work with already-allocated I-addresses and do not call `findisatoinsertmolecule`.

The only scenario that *could* produce a collision would require OS-level threading (absent: single process, no `pthread_create`) or a deferred allocation buffer (absent: `insertseq` is synchronous in-memory tree surgery). Neither exists in this codebase.

---

## Question 12 [gregory]

> After DELETE shifts a POOM entry's V-position leftward via `tumblersub`, can any subsequent operation (INSERT, COPY, REARRANGE) restore the original V-position, or is the pre-delete V-address layout permanently lost?

### Gregory's Answer

## KB Synthesis

After DELETE shifts a surviving POOM entry's V-displacement leftward via `tumblersub`, the original V-position **can** be numerically restored by a subsequent INSERT or COPY. But whether the full pre-delete layout is restored depends on the operation used.

## Mechanics of the Shift

From [ST-DELETE] (Finding 0053/0055): DELETE subtracts the deletion width from the V-displacement of every POOM entry after the deletion range, using `tumblersub` → `strongsub`. The `strongsub` exponent guard means only same-exponent entries shift; cross-subspace entries are immune [FC-SUBSPACE].

The shift is pure arithmetic: `vpos_after = vpos_before - delete_width`.

## INSERT/COPY Restoration

[ST-INSERT] (Finding 0054) shows that INSERT at position `P` of width `w` shifts all POOM entries in `[P, subspace_boundary)` **rightward** by `+w` via `tumbleradd`. This is arithmetically the inverse of the DELETE shift.

If you INSERT (or COPY) at the same position and with the same width as the deleted span:
- All surviving entries that were shifted left by `-w` are shifted right by `+w`
- Their V-displacements return to their pre-delete values

**So yes — V-positions of surviving entries are restorable.**

## I-Address Restoration: The Critical Distinction

[INV-DELETE-NOT-INVERSE] establishes that DELETE+INSERT is NOT a true inverse:
- INSERT allocates **fresh I-addresses** (`next_iaddr(granf) + 1`) — never reuses old ones [INV-NO-IADDR-REUSE]
- The V-positions are numerically restored, but the I-addresses in the gap differ

[ST-COPY] documents the alternative: COPY shares **existing** I-addresses via `insertpm`. If you COPY from a version (or any document) that still references the original I-addresses:
- V-positions of surviving entries are restored (same INSERT-style shift)
- The new POOM entries in the gap reference the original I-addresses
- Full V+I layout is restored — [INV-IADDR-IMMUTABILITY] confirms the original I-addresses still exist in the granfilade ([FC-GRANF-ON-DELETE]: DELETE never touches the granfilade)

## REARRANGE

[ST-REARRANGE] only permutes existing POOM entries; it creates no new ones. It cannot restore deleted content — there are no POOM entries to rearrange back. It also cannot shift entries to arbitrary target positions since offsets are computed from cut geometry, not absolute targets.

## The Deeply Orphaned Case

[EC-DEEPLY-ORPHANED-LINK] (Finding 0053, corrected by 0055) notes that if DELETE somehow pushed a same-exponent entry's V-position **negative**, that entry becomes invisible but still exists in the POOM tree. A subsequent INSERT cannot rescue it: INSERT's knife only shifts entries at `>= insertion_point`, and a negative V-position is below any positive insertion point. The entry remains unreachable. However, Finding 0055 clarifies this negative-shift scenario is prevented for cross-subspace entries by the `strongsub` exponent guard.

## Summary

| Goal | INSERT | COPY (from original I-addresses) | REARRANGE |
|------|--------|----------------------------------|-----------|
| Restore V-positions of surviving entries | ✓ | ✓ | ✗ |
| Restore deleted content at original V-positions | ✓ (new I-addrs) | ✓ (original I-addrs) | ✗ |
| Restore original I-addresses in the gap | ✗ | ✓ | ✗ |
| Full pre-delete layout (V + I) | ✗ | ✓ | ✗ |

The only path to complete identity-preserving restoration is COPY from a document that retained the original I-addresses (typically a version created before the DELETE). This is the design intent of CREATENEWVERSION as documented in [ST-VERSION-CREATE] and [INV-DELETE-NOT-INVERSE] — "undo" in Xanadu is not INSERT but COPY-from-version.

---

## Code Exploration

Now I have a complete picture. Let me trace through all the relevant paths carefully.

---

## Answer

### The Delete Mechanism

`dodeletevspan` [do1.c:158–167] calls `deletevspanpm` [orglinks.c:145–152], which calls `deletend` [edit.c:31–76].

Inside `deletend`, for every POOM crum that lies **entirely to the right** of the deleted span (case 2 in `deletecutsectionnd` [edit.c:235–248]):

```c
// edit.c:63
tumblersub (&ptr->cdsp.dsas[index], width, &ptr->cdsp.dsas[index]);
```

This subtracts the deleted span's `width` from each surviving crum's V-displacement, collapsing the gap. Crums that fall **inside** the deleted span (case 1) are permanently removed:

```c
// edit.c:59–60
disown ((typecorecrum*)ptr);
subtreefree ((typecorecrum*)ptr);
```

The V→I bindings for those disowned crums no longer exist anywhere.

---

### Can INSERT Restore the Original V-Position Layout?

`doinsert` [do1.c:87–123] → `docopy` → `insertpm` [orglinks.c:75–134] → `insertnd` [insertnd.c:15–111] → `makegappm` [insertnd.c:124–172].

Inside `makegappm`, for every crum that lies at or after the insertion point (case 1 from `insertcutsectionnd`):

```c
// insertnd.c:162
tumbleradd(&ptr->cdsp.dsas[V], &width->dsas[V], &ptr->cdsp.dsas[V]);
```

This is the **exact inverse** of `tumblersub` — it shifts surviving crums rightward by `width`. So if an INSERT is placed at the original `origin` address with the same `width`:

1. `makegappm` opens the gap.
2. All crums that were shifted leftward by the delete are shifted rightward by the same amount.
3. Their V-addresses are restored to what they were before the delete.

**The relative V-address layout of surviving content is geometrically restored.**

However, there is a guard in `makegappm` [insertnd.c:140–143]:

```c
if (iszerotumbler (&fullcrumptr->cwid.dsas[V])
|| tumblercmp (&origin->dsas[V], &grasp.dsas[V]) == LESS
|| tumblercmp (&origin->dsas[V], &reach.dsas[V]) != LESS)
    return(0);
```

This means `makegappm` is skipped if the insertion point is **outside** the current document V-range (`grasp` to `reach`). After a delete, if the deleted region was at the end of the document and nothing follows it, the insertion point may fall outside this range — and no gap-opening occurs. In that case V-addresses of other content are unaffected (there are none after).

---

### Can COPY Restore the Original V-Position Layout?

`docopy` [do1.c:45–65] calls `insertpm` directly, which calls `insertnd` → `makegappm`. The gap-opening mechanics are **identical to INSERT**. COPY at the original V-address with the same width also geometrically restores the V-layout of all surviving crums.

Note: `acceptablevsa` [do2.c:110–113] — the function that checks whether a V-address is acceptable for insertion — is a stub that **always returns TRUE**:

```c
bool acceptablevsa(tumbler *vsaptr, typeorgl orglptr)
{
    return (TRUE);
}
```

There is no validation preventing re-use of a previously-deleted V-address.

---

### Can REARRANGE Restore the Original V-Position Layout?

`dorearrange` [do1.c:34–43] → `rearrangepm` [orglinks.c:137–142] → `rearrangend` [edit.c:78–160].

`rearrangend` computes offsets via `makeoffsetsfor3or4cuts` [edit.c:164–184], using `tumblersub` and `tumbleradd` on the cut positions, then applies them to surviving crums:

```c
// edit.c:124–126
tumbleradd (&ptr->cdsp.dsas[index], &diff[i], &ptr->cdsp.dsas[index]);
```

REARRANGE can move surviving crums to **any V-positions**, including ones previously occupied before a delete. So yes, rearrange can in principle restore any set of V-addresses for surviving content — but only for content that still exists. It cannot resurrect deleted entries.

---

### Is the Pre-Delete V-Address Layout Permanently Lost?

There are two separate questions here:

**1. V-positions of surviving content**: NOT permanently lost. Any of INSERT, COPY, or REARRANGE can restore the V-positions of surviving entries:
- INSERT/COPY at the original `origin` with the same `width` inverts the `tumblersub` via `tumbleradd` [insertnd.c:162], exactly restoring prior positions.
- REARRANGE can move any surviving content to any V-address.

**2. The original V→I bindings of deleted content**: PERMANENTLY LOST. The disowned POOM crums [edit.c:59–60] are freed. The V→I mapping that specified *which permascroll I-spans* sat at those V-addresses is destroyed and cannot be recovered by any subsequent operation. INSERT/COPY at the same V-address places *new* I-span references there — not the originals.

---

### Summary

| Operation | Restores V-positions of surviving content | Restores original V→I binding of deleted content |
|-----------|------------------------------------------|--------------------------------------------------|
| INSERT at original VSA, same width | **Yes** — `makegappm` inverts the `tumblersub` [insertnd.c:162] | **No** — new I-spans, not original content |
| COPY at original VSA, same width | **Yes** — same path as INSERT | **No** — copied I-spans, not original binding |
| REARRANGE (with correct cut positions) | **Yes** — arbitrary V-address reassignment [edit.c:124–126] | **No** — only moves surviving crums |

The `tumblersub` applied by DELETE [edit.c:63] to surviving crums is **arithmetically reversible** — `tumbleradd` of the same `width` at the same `origin` exactly undoes it. But the V→I bindings for the deleted crums are gone. The `disown`/`subtreefree` [edit.c:59–60] is not reversible: the pre-delete V-address layout, in the sense of *which content was at which V-address*, is permanently lost the moment the crums are freed.

---

## Question 13 [gregory]

> The `strongsub` exponent guard in DELETE returns the link position unchanged when width.exp < pos.exp — was this intentional isolation design or an accident that happens to work, and are there tumbler configurations where the guard fails to protect link subspace positions?

### Gregory's Answer

## KB Synthesis

## The `strongsub` Guard: Accidental, Not Intentional

The KB is explicit on this. [INT-DELETE-SUBSPACE-ASYMMETRY] states directly:

> INSERT's protection is robust — it was designed intentionally (the source contains explanatory comments). DELETE's protection is accidental — **there is no comment suggesting awareness of the exponent guard as a subspace protection mechanism**.

[FC-SUBSPACE] (Finding 0055) draws the same contrast: INSERT uses `findaddressofsecondcutforinsert()` to compute an explicit second knife blade at the next subspace boundary `(N+1).1`. DELETE's knife is simply `[origin, origin + width]` — no subspace boundary calculation. The guard is incidental arithmetic, not design.

---

## When the Guard Fails

The guard in `strongsub` is: **if `b.exp < a.exp`, return `a` unchanged** (i.e., skip the subtraction).

[ST-DELETE] (Finding 0055) gives the concrete numbers for why it works in the normal case:
- Text deletion width: exp = −1 (e.g., `0.3` for 3 characters)
- Link position: exp = 0 (e.g., `2.1`)
- Guard: −1 < 0 → TRUE → link position unchanged ✓

The guard fails when **`width.exp ≥ link_pos.exp`**, i.e., when the width has exponent 0 or greater. This happens when a deletion spans a whole-unit V-range, producing a width like `1.0` (exp = 0).

**Concrete failure scenario:**

Delete from position `1.1` with width `1.0` (spanning the full space from text subspace into the link subspace boundary):

```
width = 1.0    (exp = 0)
link  = 2.1    (exp = 0)

strongsub(2.1, 1.0):
  b.exp (0) < a.exp (0)  → FALSE
  Subtraction proceeds: 2.1 − 1.0 = 1.1
  Link position shifts from 2.1 → 1.1
  Text content now occupies what was the link subspace position
```

The link has crossed from `2.x` into `1.x` — the invariant is violated. Nothing in the DELETE path prevents this. [PRE-DELETE] documents that DELETE has no subspace guard, and [FC-SUBSPACE] (Finding 0049, 0051) already established two other violation paths (INSERT at wrong subspace, REARRANGE across boundary). This is a third.

---

## The Structural Invariant Being Relied On

[INT-DELETE-SUBSPACE-ASYMMETRY] formalizes the implicit assumption: `∀ width, entry : different_subspace(width, entry) ==> width.exp < entry.vpos.exp`.

This holds under normal operation because:
1. Text content is addressed at character granularity within `1.x`, so widths are sub-unit (exp = −1)
2. Link positions are in `2.x` at integer precision (exp = 0)
3. No well-behaved deletion spans more than one subspace unit

But the system has **no enforcement of this invariant**. A caller specifying `DELETE(doc, pos=1.1, width=1.0)` — which syntactically looks like a large text deletion — would trigger the failure. The guard only works because of the implicit convention that text deletions are character-sized and link positions are integer-sized, not because `strongsub` was designed to enforce subspace isolation.

[INT-DELETE-SUBSPACE-ASYMMETRY] puts it plainly: "If `strongsub` were modified to handle cross-exponent subtraction correctly, DELETE would break subspace isolation while INSERT would remain safe" — confirming that INSERT's protection is structural and robust, while DELETE's is arithmetic and fragile.

---

## Code Exploration

I have everything I need. Here is the complete analysis.

---

## The `strongsub` Exponent Guard in DELETE: Intentional Isolation or Accident?

### The Guard

`strongsub` [tumble.c:534–565] computes `a - b` when `a > b` (called from `functiontumbleradd` [tumble.c:385] only after `abscmp` confirms this). The guard at lines 544–547:

```c
if (bptr->exp < aptr->exp) {
    movetumbler(aptr,cptr);
    return(0);
}
```

When `bptr` (the subtrahend) has a more negative exponent than `aptr` (the minuend), it silently returns `aptr` unchanged instead of computing any difference.

---

### The DELETE Call Chain

```
fns.c:341      getdeletevspan(taskptr, &docisa, &vspan)
fns.c:342      dodeletevspan(taskptr, &docisa, &vspan)
do1.c:163-166  → deletevspanpm(taskptr, docisaptr, docorgl, vspanptr)
orglinks.c:149 →   deletend((typecuc*)docorgl, &vspanptr->stream, &vspanptr->width, V)
edit.c:63      →     case 2: tumblersub(&ptr->cdsp.dsas[index], width, &ptr->cdsp.dsas[index])
tumble.c:427   →       tumbleradd(pos, -width, pos)
tumble.c:385   →         strongsub(pos, width, pos)   [when |pos| > |width|]
tumble.c:544   →           GUARD: if width.exp < pos.exp → return pos unchanged
```

Case 2 in `deletend` [edit.c:58–65] identifies crums whose left border is at or beyond `blades[1]` (the end of the deleted span) — i.e., nodes that lie entirely *after* the deletion. The adjustment `tumblersub(pos, width, pos)` is supposed to slide them backward to close the V-address gap.

---

### V-Address Exponent Structure

**Text content** in the document POOM is allocated starting at `"1.1"`:

```c
// orglinks.c:42-43, findvsatoappend:
tumblerincrement(vsaptr, 0, 1, vsaptr);  // → exp=0, mantissa=[1,...] = "1"
tumblerincrement(vsaptr, 1, 1, vsaptr);  // → exp=0, mantissa=[1,1,...] = "1.1"
```

Successive text crums are at `"1.1"`, `"1.6"`, `"1.11"` etc., all with **exp=0**.

**Text widths** in the POOM are built by `insertpm` [orglinks.c:115–117]:

```c
shift = tumblerlength(vsaptr) - 1;   // = 2-1 = 1  for "1.1" address
inc   = tumblerintdiff(&lwidth, &zero);
tumblerincrement(&zero, shift, inc, &crumwidth.dsas[V]);
// → exp = -shift = -1, mantissa=[inc,...]
```

So text crum **V-widths always have exp=−1**.

**Link ISA references** in the parent document's POOM are placed by `findnextlinkvsa` [do2.c:151–167] at V-addresses starting from `"2.1"`:

```c
tumblerincrement(&firstlink, 0, 2, &firstlink);  // → exp=0, mantissa=[2,...] = "2"
tumblerincrement(&firstlink, 1, 1, &firstlink);  // → exp=0, mantissa=[2,1,...] = "2.1"
```

These are **exp=0**, mantissa=[2,N,...] addresses.

**Link endpoint data** in the link's own POOM uses fixed VSAs from `setlinkvsas` [do2.c:169–183]:

```c
fromvsa = "1.1"  (exp=0, mantissa=[1,1,...])
tovsa   = "2.1"  (exp=0, mantissa=[2,1,...])
threevsa = "3.1" (exp=0, mantissa=[3,1,...])
```

All are **exp=0**.

---

### What the Guard Actually Does in the Normal Delete Case

When text is deleted — say from `"1.1"` to `"1.6"` (5 chars) — the width is computed as a tumbler difference of same-prefix addresses. Tracing `strongsub("1.6", "1.1")` [tumble.c:549–555]:

```c
answer.exp = aptr->exp = 0;
// Loop: i=0, mantissa[0]: 1 == 1 → --answer.exp → answer.exp = -1, i=1
// i=1, mantissa[1]: 6 != 1 → break
answer.mantissa[0] = 6 - 1 = 5;
// Result: exp=-1, mantissa=[5,...] = "0.5"
```

Deletion width: **exp=−1**.

Now adjusting a link crum at `"2.1"` [edit.c:63]:

```c
tumblersub(&ptr->cdsp.dsas[V], width, &ptr->cdsp.dsas[V])
// = tumblersub("2.1", "exp=-1, [5,...]", result)
// → tumbleradd("2.1", neg-width, result)
// → abscmp("2.1", "exp=-1, [5,...]"): "2.1".exp=0 > width.exp=-1 → GREATER
// → strongsub("2.1", "exp=-1, [5,...]", result)
//   → guard: bptr->exp(-1) < aptr->exp(0) → TRUE → return "2.1" unchanged ✓
```

The link ISA at `"2.1"` is not touched.

---

### Was This Intentional?

**It was a defensive precision check that happens to provide the right isolation — not a purposeful isolation design.**

Evidence for **precision check, not isolation design**:

1. The guard appears in `strongsub` whose contract is same-exponent exact subtraction (contrast with `weaksub` which explicitly handles exponent mismatches for less precise arithmetic). The guard is a safety net when that contract is violated — it returns the minuend unchanged rather than producing garbage.

2. The case-2 adjustment code in `deletend` [edit.c:62–65] and its comment `/* This will get set to modified in setwisp */` treats the shift as a real operation expected to produce a new value. If the isolation were intentional, `deletend` would simply not call `tumblersub` for dimension V at all.

3. `strongsub` is called from `functiontumbleradd` [tumble.c:384–389] in general arithmetic contexts (not just delete). The guard protects those contexts from exponent overflow too.

4. The function name "strong" vs "weak" in Xanadu's own terminology refers to precision, not protection. `strongsub` is exact; `weaksub` is approximate.

The alignment between the guard's firing condition and the semantically correct behavior — link V-addresses persist, text deletion widths are exp=−1, link positions are exp=0 — is a consequence of the V-address allocation scheme, not explicit guard design.

---

### Configurations Where the Guard Fails to Protect Link Subspace Positions

The guard fires only when `width.exp < pos.exp`. It does **not** fire when `width.exp >= pos.exp`. Specifically, width has exp=0 whenever the deletion spans across level-1 node boundaries (different leading mantissa digit).

**Configuration 1 — Cross-subspace deletion:**

A V-span deletion from `"1.5"` (text subspace, mantissa[0]=1) to `"2.2"` (link subspace, mantissa[0]=2) produces:

```c
// strongsub("2.2", "1.5", width):
// mantissa[0]: 2 != 1 → no --answer.exp
// answer.mantissa[0] = 2 - 1 = 1, answer.exp = 0
// width = exp=0, mantissa=[1,...] = "1"
```

The link ISA at `"2.3"` (case 2, beyond blade[1]="2.2") would then be adjusted:

```c
// tumblersub("2.3", "1", result) → strongsub("2.3", "1", result)
// bptr->exp(0) NOT < aptr->exp(0) → guard does NOT fire
// mantissa[0]: 2 != 1 → answer.mantissa[0] = 2-1 = 1, answer.exp = 0
// Result: "1.3" — link position silently corrupted from "2.3" to "1.3"
```

**Configuration 2 — Deletions targeting link subspace itself:**

Deleting a link ISA from `"2.1"` to `"2.2"` produces width exp=−1 (same-prefix subtraction, one `--answer.exp`), so the guard fires for adjacent link ISAs at `"2.2"`, `"2.3"`, etc. — they do NOT shift. This means link ISA positions in the parent document are **immovable** even after other link ISAs are deleted, creating persistent V-address gaps. This may or may not be the intended behavior, but it is not the guard "protecting" anything — it is simply failing to implement gap closure.

**Configuration 3 — Client-specified exp=0 width:**

The FEBE protocol allows clients to specify arbitrary V-spans to delete [fns.c:333–347]. A client providing a `typevspan` with `width.exp=0` directly bypasses the guard for any link position with `pos.exp=0`.

---

### Summary

The guard at `tumble.c:544–547` is a **defensive precision check** — added because `strongsub` cannot correctly compute a difference when `bptr` is more precise than `aptr`. Its effect as link-position isolation is an **accident that works** because normal text deletion widths (exp=−1) are always one level finer than link positions (exp=0), causing the guard to fire every time.

The guard **fails** when deletion produces exp=0 widths. This happens in any deletion spanning two different top-level V-nodes — most relevantly, a cross-subspace deletion from text to link space (`"1.x"` → `"2.y"`) produces an exp=0 width that bypasses the guard and shifts case-2 link ISA crums by incorrect amounts, corrupting their V-addresses in the parent document POOM.

---

## Question 14 [gregory]

> When COPY creates a new V→I mapping in the target document, does the target's POOM entry store an independent copy of the I-displacement, or does it share a pointer with the source — i.e., could any mutation of the source POOM corrupt the target's I-address reference?

### Gregory's Answer

## KB Synthesis

The target's POOM entry stores an independent copy of the I-displacement. There is no shared pointer.

**Structural evidence:**

The POOM bottom crum type holds its own displacement and width as value fields — `cdsp.dsas[I]` and `cdsp.dsas[V]` — embedded directly in the struct, not as pointers to external data [SS-POOM-BOTTOM-CRUM]. When `insertnd` creates a new crum (the non-extension path at `insertnd.c:252-260`), it allocates a fresh crum and copies the I-address and V-address values into it [ST-VCOPY Finding 0046].

**Behavioral evidence:**

[FC-VERSION-ISOLATION] is the clearest empirical proof: after `CREATENEWVERSION`, edits to the original's POOM do not affect the version's POOM and vice versa. If the two POOMs shared pointer-level I-address references, in-place operations like `tumbleradd` on `ptr->cdsp.dsas[V]` during DELETE or REARRANGE would corrupt both. They don't.

Similarly, [SS-POOM-MUTABILITY] states there are no copy-on-write semantics — each POOM is a distinct mutable tree, which is only coherent if the displacement values are owned by each crum independently.

**DELETE confirms value semantics:**

[ST-DELETE Finding 0053/0055] shows `deletend` applies `tumblersub(&ptr->cdsp.dsas[index], width, ...)` — arithmetic directly on the crum's own displacement field. If displacements were shared references, deleting from one document would silently shift crums in all documents that copied from it. This is explicitly ruled out by [FC-DELETE-CROSS-DOC]: DELETE in document D has zero effect on any other document's POOM mappings.

**Bottom line:**

The I-displacement in the target POOM crum is a copied value, fully owned by the new crum struct. Source POOM mutations cannot corrupt target I-address references. The sharing happens at the I-address *value* level (both POOMs independently record the same tumbler coordinate), not at a memory pointer level.

---

## Code Exploration

I now have all the evidence needed. Here is the complete answer.

---

## COPY and POOM I-Address Storage: Independent Value Copies, No Pointer Sharing

### Call chain through COPY

`docopy` [do1.c:45–65] orchestrates two operations:

```c
&& insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)   // do1.c:60
&&  insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN)  // do1.c:62
```

`insertpm` in `orglinks.c:75–134` is where the new V→I mapping is built and written into the target's POOM tree. Every value transition in this path uses value-copy semantics.

---

### `insertpm`: Stack-local intermediates, no source references retained

```c
// orglinks.c:100–131
for (; sporglset; sporglset = ...) {
    unpacksporgl (sporglset, &lstream, &lwidth, &linfo);    // → local tumblers
    movetumbler (&lstream, &crumorigin.dsas[I]);             // orglinks.c:105
    movetumbler (&lwidth,  &crumwidth.dsas[I]);              // orglinks.c:109
    movetumbler (vsaptr,   &crumorigin.dsas[V]);             // orglinks.c:113
    ...
    insertnd (taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);  // orglinks.c:130
}
```

`lstream`, `lwidth`, `linfo`, `crumorigin`, `crumwidth` are all **stack-local** to `insertpm`. `unpacksporgl` [sporgl.c:178–203] itself uses `movetumbler` to extract the I-address from the sporgl into those locals:

```c
// sporgl.c:185–187
movetumbler (&((typesporgl*)sporglptr)->sporglorigin, streamptr);
movetumbler (&((typesporgl*)sporglptr)->sporglwidth,  widthptr);
movetumbler (&((typesporgl*)sporglptr)->sporgladdress, &infoptr->homedoc);
```

Once `insertnd` is called, the source sporgl is no longer referenced.

---

### `insertcbcnd`: New crum allocated, all fields deep-copied

The insertion bottoms out in `insertcbcnd` [insertnd.c:242–275]:

```c
new = createcrum (0, (INT)father->cenftype);   // insertnd.c:260 — fresh heap allocation
reserve (new);
adopt (new, SON, (typecorecrum*)father);
dspsub  (origin, grasp, &new->cdsp, ...);      // insertnd.c:263 — computed, stored by value
movewisp(width,          &new->cwid);           // insertnd.c:266 — memmove deep copy
move2dinfo(infoptr, &((type2dcbc *)new)->c2dinfo);  // insertnd.c:267 — memmove deep copy
```

The displacement field `cdsp` is written by `dspsub` [wisp.c:21–24], which calls `locksubtract` — it computes a result and writes it directly into `new->cdsp`. The width field is written by `movewisp` and the home-doc info by `move2dinfo`.

---

### Copy primitive definitions — all value semantics

| Primitive | Definition | Semantics |
|---|---|---|
| `movetumbler(A,B)` | `(*((tumbler*)(B)) = *((tumbler*)(A)))` [common.h:73] | C struct assignment — copies all bytes of the tumbler by value |
| `movewisp(A,B)` | `memmove(B, A, sizeof(typewisp))` [wisp.h:58] | Byte-for-byte deep copy of the entire wisp |
| `move2dinfo(A,B)` | `memmove(B, A, sizeof(type2dbottomcruminfo))` [wisp.h:110] | Byte-for-byte deep copy |
| `dspsub(a,b,c,t)` | `locksubtract(a->dsas, b->dsas, c->dsas, dspsize(t))` [wisp.c:23] | Arithmetic result written to destination |

---

### The `xvartumbler` pointer field: dead code, always NULL

The `tumbler` struct does contain one pointer field [common.h:59–65]:

```c
typedef struct structtumbler {
    humber xvartumbler;      // unsigned char * — a pointer
    char varandnotfixed;
    char sign;
    short exp;
    tdigit mantissa[NPLACES];
} tumbler;
```

`movetumbler`'s struct assignment would shallow-copy this pointer. This would be a shared-pointer aliasing risk **if** `xvartumbler` were ever non-NULL in the COPY path. It isn't:

- Every arithmetic function that produces a new tumbler value sets `xvartumbler = 0` explicitly [tumble.c:456–457]
- `tumblerclear` is `clear(ptr, sizeof(tumbler))` — zeros all bytes including the pointer
- `corediskin.c` (disk deserialization) never sets `xvartumbler`
- The only reference to it as a non-null value is in `tumbleari.c:319`, marked with comment `/* ZZZ ECH 8-26-88 */` — an unfinished 1988 experiment behind no active code path

All tumblers entering the INSERT path through `specset2ispanset` → `insertpm` carry `xvartumbler == 0`. The struct copy propagates NULL, not a shared heap reference.

---

### Conclusion

**The target POOM crum stores a fully independent, value-copied I-address. No pointer is shared with the source.**

The sequence is: sporgl's I-address → `movetumbler` into stack locals → `movetumbler` into `crumorigin`/`crumwidth` → `movewisp`/`dspsub`/`move2dinfo` into freshly allocated crum node. Every transition is a complete byte-for-byte value copy. After `insertpm` returns, the new POOM crum is entirely self-contained. No mutation of the source document's POOM, its sporgl list, or any intermediate structure can reach or corrupt the target crum's `cdsp`/`cwid`/`c2dinfo` fields.

---

## Question 15 [gregory]

> If a document's entire text content is deleted and then new text is inserted, the new text gets fresh I-addresses — but does the POOM's V-address numbering restart from 1.1, or does it continue from the shifted position left by the delete?

### Gregory's Answer

## KB Synthesis

## V-Address Numbering After Delete-All + Insert

**Short answer:** V-addresses restart from whatever the client specifies (typically 1.1), but there is a crash bug that makes this case non-operational currently.

---

### The POOM Resets to Zero After Delete-All

From [SS-ENFILADE-TREE] / Finding 0058 and [EC-EMPTY-DOC] / Finding 0066:

When all content is deleted, `deletend` Case 1 (`disown + subtreefree`) frees every bottom crum. `setwispnd` then zeroes both fields on the empty root:

```
After delete-all: root.cdsp = 0, root.cwid = 0
```

This is confirmed by [INV-ENFILADE-RELATIVE-ADDRESSING]: "When all children of a 2D enfilade are deleted, `setwispnd` clears both `cdsp` and `cwid` to zero, restoring the empty state."

There is **no accumulated position offset** left over. The POOM is structurally empty.

---

### V-Addresses Are Caller-Specified, Not Auto-Incremented

From [ST-INSERT]: the client provides `vsaptr` (the target V-address) to `doinsert`. There is no internal "next position" counter. The system places content at whatever V-address the caller requests.

After delete-all with an empty POOM (`cdsp=0, cwid=0`), a subsequent `INSERT` at V-position 1.1 would set the first bottom crum's absolute displacement to 1.1, and `setwispnd` would set `root.cdsp = 1.1`. V-numbering **restarts from 1.1**, not from some post-delete shift residual.

---

### The Critical Caveat: Bug 0019

From [EC-EMPTY-DOC] / Finding 0058:

> "Finding 0064 confirms that the empty-after-delete state causes INSERT and VCOPY to crash (Bug 0019) because `firstinsertionnd()` assumes a bottom crum always exists. When `findleftson()` returns NULL (no bottom nodes), the code dereferences a null pointer."

So while the POOM *conceptually* resets to a state from which inserts would start at V:1.1, the implementation currently **crashes** if you attempt this. The delete-all + insert sequence is not operational.

---

### I-Addresses Do Not Restart

Even if the V-numbering resets, the I-addresses for new content do **not** restart. From [INV-MONOTONIC] and [INV-NO-IADDR-REUSE]:

- The granfilade is append-only; `findpreviousisagr` always finds the current maximum
- Deleted I-addresses are never reclaimed
- New inserts after delete-all get I-addresses beyond those of the formerly-deleted content

So: V-space numbering restarts from 1.1 (conceptually), I-space numbering continues monotonically from wherever the granfilade maximum sits — and `compare_versions` between the pre-delete state and the re-inserted content would report **no shared spans** ([INV-DELETE-NOT-INVERSE]).

---

## Code Exploration

---

## Answer

**The V-address numbering restarts from 1.1.** The delete leaves the POOM structurally empty — there is no "shifted position" to continue from, and no high-water mark anywhere in the system.

---

### Trace: The Delete Path

`dodeletevspan` [do1.c:158-167] → `deletevspanpm` [orglinks.c:145-152] → `deletend` [edit.c:31-76].

Inside `deletend`, each crum in the intersection of the delete range is classified by `deletecutsectionnd` [edit.c:235-248]:

- **Case 1** (crum entirely within the deleted range): `disown` + `subtreefree` — the crum is physically removed from the tree.
- **Case 2** (crum to the right of the deleted range): `tumblersub` shifts the crum's displacement left by `width`.

```c
case 1:
    disown ((typecorecrum*)ptr);
    subtreefree ((typecorecrum*)ptr);   // [edit.c:59-60]
    break;
case 2:
    tumblersub (&ptr->cdsp.dsas[index], width, &ptr->cdsp.dsas[index]);  // [edit.c:63]
    break;
```

When the **entire** document content is deleted, every text crum falls into Case 1. No crums survive. Case 2 (the shift that would "leave a position") never fires. After `setwispupwards(father, 1)` [edit.c:74] propagates widths back up, the POOM root's `cwid.dsas[V]` is zero.

`isemptyorgl` [orglinks.c:539-543] confirms the result:

```c
bool isemptyorgl(typeorgl fullcrumptr)
{
    return (
       iszerolock ((tumbler*)&((typecuc*)fullcrumptr)->cwid, widsize(POOM))
    && iszerolock ((tumbler*)&((typecuc*)fullcrumptr)->cdsp, dspsize(POOM)));
}
```

Both `cwid` (width) and `cdsp` (displacement) are zero. The POOM is indistinguishable from `createenf(POOM)` — a fresh, never-used document.

---

### Trace: The Re-insert Path

`doinsert` [do1.c:87-123] calls `docopy(taskptr, docisaptr, vsaptr, ispanset)` [do1.c:119], passing the **client-provided VSA** unchanged.

`acceptablevsa` [do2.c:110-113] is a stub:

```c
bool acceptablevsa(tumbler *vsaptr, typeorgl orglptr)
{
    return (TRUE);
}
```

No validation. Any non-zero VSA is accepted.

`docopy` → `insertpm` [orglinks.c:75-134]. The only rejection is zero:

```c
if (iszerotumbler (vsaptr)){
    return (FALSE);   // [orglinks.c:86-91]
}
```

`insertpm` places the VSA directly into the new crum:

```c
movetumbler (vsaptr, &crumorigin.dsas[V]);   // [orglinks.c:113]
...
insertnd (taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);  // [orglinks.c:130]
```

`insertnd` → `doinsertnd` [insertnd.c:185-197]. After delete-all, `isemptyenfilade(father)` is TRUE, so it calls `firstinsertionnd`:

```c
if (isemptyenfilade (father)) {
    firstinsertionnd (father, origin, width, infoptr);  // [insertnd.c:192-193]
    return(FALSE);
}
```

`firstinsertionnd` [insertnd.c:199-218] creates a new bottom crum (if needed) and places the origin directly:

```c
movewisp (origin, &ptr->cdsp);   // [insertnd.c:212] — client's VSA becomes the crum displacement
movewisp (width, &ptr->cwid);
```

Whatever the client passed as VSA is now the displacement of the first POOM crum. **The POOM has no memory of previous V-addresses.**

---

### The Append Case Is Even More Explicit

For append operations, `appendpm` [orglinks.c:17-27] calls `findvsatoappend` [orglinks.c:29-49]:

```c
if (
   iszerolock ((tumbler*)&ptr->cwid, widsize(POOM))   // empty POOM
|| (tumblercmp (&grasp.dsas[V], &linkspacevstart) != LESS)) {
    tumblerincrement (vsaptr, 0, 1, vsaptr); /* no text in doc */
    tumblerincrement (vsaptr, 1, 1, vsaptr);           // VSA = 1.1
```

When the POOM is empty after delete-all, `iszerolock` on `cwid` is TRUE, and the function explicitly returns **1.1**.

---

### Golden Test Confirmation

The `delete_all_content_simple` golden test records actual backend behavior:

```json
// After insert "Test content" at 1.1:
"before_delete": { "spans": [{ "start": "1.1", "width": "0.12" }] }

// After deleting the entire span:
"after_delete": { "spans": [] }

// After re-inserting "After delete" at 1.1:
"reinsert_vspans": { "spans": [{ "start": "1.1", "width": "0.12" }] }
```

The re-inserted content occupies **1.1 → 1.1+0.12** — identical to the first insertion. The `empty_document_never_filled` baseline shows the same: a fresh document's first insert at 1.1 produces `start=1.1, width=0.13`.

---

### Summary

| Mechanism | Behavior |
|---|---|
| `deletend` case 1 [edit.c:58-60] | Frees all crums when all content is deleted |
| `deletend` case 2 [edit.c:63] | Shifts surviving crums — never fires in total delete |
| `isemptyorgl` [orglinks.c:539] | Confirms POOM is empty after delete-all |
| `acceptablevsa` [do2.c:110-113] | Always returns TRUE — no VSA validation |
| `firstinsertionnd` [insertnd.c:199] | Places client-provided VSA directly into new crum |
| `findvsatoappend` [orglinks.c:41-43] | Explicitly returns 1.1 when POOM is empty |

**The POOM carries no "high-water mark."** After delete-all, it is structurally identical to `createenf(POOM)`. The V-address for the next insert is **entirely determined by the client's argument** — and both the FEBE test harness and the `doappend` path choose 1.1. The numbering restarts at 1.1.

---

## Question 16 [gregory]

> CREATENEWVERSION copies text-subspace POOM entries — are the I-displacements in the version's POOM byte-identical copies of the original's, or are they recomputed, and could recomputation ever produce different tumbler representations for the same logical I-address?

### Gregory's Answer

## KB Synthesis

## CREATENEWVERSION: I-Displacement Copy vs. Recomputation

The answer requires distinguishing three separate things: the I-address origin values, the I-width tumblers, and the V-width tumblers.

### I-Address Origins: Logically Identical, Physically May Differ

The copy path is: `docreatenewversion` → `doretrievedocvspanfoo` → `docopyinternal` → `specset2ispanset` → `insertpm` → `setwispnd` [ST-VERSION, Finding 0077].

`specset2ispanset` reads the I-address tumblers **directly from the source POOM's bottom crums** — these are the same tumblers originally placed there by `inserttextingranf`. They are not recomputed from the permascroll content. The I-origins passed to `insertpm` are byte-identical copies of what `specset2ispanset` extracted.

However, once `insertpm` places these into the version's new enfilade tree, `setwispnd` recalculates relative displacements [INV-ENFILADE-RELATIVE-ADDRESSING, Finding 0066]:

> `absolute_grasp(node) = absolute_grasp(parent) + node.cdsp`

The `cdsp` field at any given tree node stores a **relative** value — the absolute address minus the parent's grasp. As the version's tree grows through sequential `insertpm` calls and `setwispnd` rebalances, the relative `cdsp` values depend on tree shape (insertion order, splits) and will generally **differ numerically** from the source tree's `cdsp` values, even though the absolute I-addresses they encode are identical.

### I-Width Tumblers: Byte-Identical

From [SS-INSERT-VWIDTH-ENCODING] (Finding 0076):

> `movetumbler(&lwidth, &crumwidth.dsas[I])` — I-width is copied directly without transformation.

The I-width in the version's POOM crums is a byte-identical copy of the source's.

### V-Width Tumblers: Re-Encoded, But Numerically Identical If V-Addresses Match

The V-width is **recomputed** during `insertpm` via [SS-INSERT-VWIDTH-ENCODING]:

```
shift = tumblerlength(vsaptr) - 1
inc   = tumblerintdiff(&lwidth, &zero)
tumblerincrement(&zero, shift, inc, &crumwidth.dsas[V])
```

This produces a tumbler with `exp = -shift` and `mantissa[0] = inc`. Since CREATENEWVERSION copies the text subspace V-span structure intact (same V-positions, same widths), `vsaptr` lengths are the same in both source and version, so `shift` and `inc` are identical, producing **byte-identical V-width tumblers**.

### The Normalization Question

[SS-TUMBLER] (Finding 0031) establishes that after `tumblerjustify`, tumbler equality is unambiguous — "no normalization ambiguity." The I-address origins extracted by `specset2ispanset` are already in normalized form from the source POOM. When written into the version, they remain normalized. There is no recomputation pathway that could produce a different tumbler representation for the same logical I-address value.

### Summary

| Component | Mechanism | Result |
|---|---|---|
| I-address origin (absolute) | Read from source POOM via `specset2ispanset` | Byte-identical |
| I-address origin (as `cdsp`) | Recomputed by `setwispnd` as relative displacement | Numerically differs by tree position |
| I-width tumbler | `movetumbler` direct copy | Byte-identical |
| V-width tumbler | Re-encoded via `tumblerincrement` | Byte-identical (same V-positions) |

The key risk the question probes — whether re-encoding could produce a different tumbler representation for the same logical I-address — does not arise, because the I-origins are never re-encoded. They are extracted and stored as-is. The only re-encoding occurs for V-widths, and that re-encoding is deterministic given the same V-address inputs. [ST-VERSION, ST-VERSION-CREATE, SS-POOM-BOTTOM-CRUM, SS-INSERT-VWIDTH-ENCODING, INV-ENFILADE-RELATIVE-ADDRESSING]

---

## Code Exploration

I have all the evidence I need. Here is my complete answer.

---

## Answer

### The short answer

The I-displacements in the new version's POOM are **not byte-identical copies** of the original's — they are recomputed by a full V→I permutation traversal. However, for a simple (flat, single-level) source POOM the recomputed absolute I-addresses happen to equal the source's stored values. For a deep (multi-level) source POOM the recomputation accumulates partial sums via `tumbleradd`, and a latent limitation in `absadd` creates a narrow but real risk that the result differs in representation from what direct storage would produce.

---

### Execution path

**`docreatenewversion`** [`do1.c:260`] never copies POOM crums. It:

1. Calls `doretrievedocvspanfoo` → `retrievedocumentpartofvspanpm` [`orglinks.c:155`], which reads the root POOM node's `cdsp.dsas[V]` and `cwid.dsas[V]` directly:
   ```c
   movetumbler (&((typecuc *) orgl)->cdsp.dsas[V], &vspanptr->stream);
   movetumbler (&((typecuc *) orgl)->cwid.dsas[V], &vspanptr->width);
   ```
   This gives the overall V-span of the original document.

2. Builds a `vspec` with `docisa = *isaptr` (original doc) and `vspanset = &vspan` [`do1.c:285-288`], then calls `docopyinternal(taskptr, newisaptr, &vspan.stream, &vspec)` [`do1.c:293`].

**`docopyinternal`** [`do1.c:66`] calls `specset2ispanset` → `vspanset2ispanset` → `permute`. This does **not** copy crums; it walks the source POOM to produce an I-spanset.

**`permute`** [`orglinks.c:404`] calls `span2spanset` → `retrieverestricted` → `findcbcinarea2d` [`retrie.c:229`]. At each matching bottom-level crum, `makecontextfromcbc` is called.

**`makecontextfromcbc`** [`context.c:151`]:
```c
movewisp(offsetptr, &context->totaloffset);          // accumulated parent offset
movewisp(&crumptr->cwid, &context->contextwid);
if (crumptr->cenftype != GRAN)
    dspadd(&context->totaloffset, &crumptr->cdsp,    // + this crum's displacement
           &context->totaloffset, (INT)crumptr->cenftype);
```
`context->totaloffset.dsas[I]` is now the **absolute** I-address of this crum (sum of all relative displacements from tree root to this leaf).

**`context2span`** [`context.c:176`] extracts the output:
```c
movetumbler (&grasp.dsas[idx2], &foundspanptr->stream);  // stream = absolute I-address
tumblersub(&reach.dsas[idx2],&grasp.dsas[idx2],&foundspanptr->width);
```

**`insertpm`** [`orglinks.c:100-131`] unpacks this ispan and writes it into the new POOM:
```c
unpacksporgl (sporglset, &lstream, &lwidth, &linfo);
movetumbler (&lstream, &crumorigin.dsas[I]);
movetumbler (vsaptr, &crumorigin.dsas[V]);
...
insertnd (taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);
```

For the **first** insertion into the fresh empty document, `insertnd` → `doinsertnd` → `firstinsertionnd` [`insertnd.c:199`] stores the value directly:
```c
movewisp (origin, &ptr->cdsp);   // ptr->cdsp.dsas[I] = lstream
```

For **subsequent** insertions (multiple I-spans), `insertcbcnd` [`insertnd.c:263`] stores a *relative* displacement in the new tree:
```c
dspsub (origin, grasp, &new->cdsp, (INT)father->cenftype);
```
where `grasp` is the accumulated offset within the *new* POOM.

---

### Are they byte-identical?

**Structurally, no.** The source POOM stores relative I-displacements (each crum's offset relative to its parent). The new POOM receives absolute I-addresses derived from summing those relative displacements via `makecontextfromcbc` + `dspadd`. For all but the first inserted section (in a multi-section document), the new POOM's crums then re-derive relative displacements within the *new* tree, which will generally differ from the source's relative displacements.

**For a flat single-level source POOM** (no splits have occurred): the source's one bottom crum has `cdsp.dsas[I]` equal to the absolute I-address (since the parent offset is zero). `makecontextfromcbc` computes `dspadd(zero, crum->cdsp.dsas[I])`, which by the identity check in `functiontumbleradd` [`tumble.c:368`] returns the source value unchanged:
```c
if (iszerotumbler(bptr)){
    movetumbler (aptr, cptr);  return;
} else if (iszerotumbler(aptr)){
    movetumbler (bptr, cptr);  return;  // <-- hits here: zero + source_value = source_value
}
```
In this case the I-address reaching `insertpm` is byte-for-byte the original. For a **single-section** document the new POOM crum's `cdsp.dsas[I]` is then exactly the source value (via `firstinsertionnd`).

---

### Could recomputation produce different tumbler representations for the same logical I-address?

Yes — **in principle, for deep source POOMs** — due to a limitation in `absadd` [`tumble.c:444`].

When `aptr->exp == bptr->exp` (Case 1, the case that arises when both operands are at the same hierarchical scale):
```c
if (aptr->exp == bptr->exp) {
    answer.exp = aptr->exp;
    ansmant[0] = amant[0] + bmant[0];   // adds only first digits
    i = j = 1;
}
...
while ( j <= NPLACES -1 ) {    
    ansmant[j++] = bmant[i++];           // copies b's remaining digits; a's are discarded
}
```
`amant[1], amant[2], ...` are **never added to anything**. The code silently discards the higher-order digits of the first operand. This is correct only when the first operand's `mantissa[1:]` are all zero — i.e., when relative displacements are single-digit integers (the overwhelmingly common case in practice).

For a **deep source POOM** where a relative I-displacement at some level happens to have two significant digits (which could arise after complex splits and re-insertions), `dspadd` → `lockadd` → `tumbleradd` → `absadd` would silently drop those higher digits, producing a `totaloffset` that misrepresents the absolute I-address. The new POOM would then record a wrong I-address — not merely a different representation of the same address, but a genuinely wrong logical address.

---

### Summary

| Scenario | Byte-identical? | Same logical address? |
|---|---|---|
| Flat source POOM, single-section document | **Yes** | Yes |
| Flat source POOM, multi-section document | No (new tree reindexes) | Yes |
| Deep source POOM, all single-digit displacements | No | Yes |
| Deep source POOM, any multi-digit I-displacement | No | **Not guaranteed** — `absadd` drops `amant[1:]` [`tumble.c:462-484`] |

The V→I path via `specset2ispanset` → `makecontextfromcbc` → `context2span` → `insertpm` always recomputes I-addresses rather than copying them. For the nearly universal case of single-digit integer I-displacements, the recomputed logical I-addresses are correct and the new POOM faithfully reflects the original permascroll addresses. But `absadd`'s inability to carry from digit[0] into digit[1] means that any source POOM crum whose accumulated I-offset requires two significant mantissa digits will produce a silently corrupted I-address in the copy — a different tumbler representation pointing to a different logical I-address.

---

## Question 17 [gregory]

> When `isanextensionnd` coalesces a new insertion into an existing POOM crum by extending its width, does this change the I-displacement of the existing crum, or only the width — and can coalescing ever cause an adjacent crum's displacement to shift?

### Gregory's Answer

## KB Synthesis

When `isanextensionnd` coalesces a new insertion into an existing crum, **only the width changes — neither the I-displacement nor the V-displacement of the existing crum is modified**. Coalescing never causes adjacent crums to shift.

## Mechanics

The key is the interaction between `makegappm`'s early-exit and `isanextensionnd`'s width-extension path.

**Step 1: `makegappm` exits early before constructing a knife.**

From [SS-WHEREONCRUM] and [ST-INSERT] (Finding 0062), `makegappm` has this guard at `insertnd.c:137-143`:

```c
if (...|| tumblercmp(&origin->dsas[V], &reach.dsas[V]) != LESS) return(0);
```

When the insertion point equals an existing crum's reach (`ONMYRIGHTBORDER`), `origin >= reach`, so `makegappm` returns 0 immediately. No knife is constructed, `makecutsnd` is never called, and `insertcutsectionnd` — the function that shifts subsequent crums — is never invoked. **No adjacent crum's displacement is touched.**

**Step 2: `isanextensionnd` extends width in place.**

With no shifting having occurred, `insertnd` proceeds to the extension check (`insertnd.c:293-301`). When both conditions hold — same `homedoc` AND new content's I-origin equals the existing crum's I-reach — the existing crum is extended at `insertnd.c:243`. Per [SS-POOM-BOTTOM-CRUM] (Finding 0076), each POOM bottom crum stores:

```
BottomCrum = {
  origin: { dsas[I]: Tumbler, dsas[V]: Tumbler },   ← UNCHANGED
  width:  { dsas[I]: Tumbler, dsas[V]: Tumbler }    ← ONLY THIS CHANGES
}
```

Both the V-origin and I-origin remain at their prior values. The new content's I-addresses are contiguous with the crum's existing I-range (that was the extension precondition), so extending width is sufficient — the crum's start point doesn't move.

**Step 3: Parent widths update, but parent displacements are unchanged.**

After extension, `setwispupwards` propagates the larger `cwid` up the tree per [ST-INSERT] (Finding 0066). Because the extended crum's origin (displacement) didn't change, `setwispnd`'s minimum-displacement recalculation produces the same `cdsp` as before. Parent nodes gain larger widths but retain the same displacements. Per [INV-ENFILADE-RELATIVE-ADDRESSING], relative addressing invariants are preserved.

## Summary

| What changes | What doesn't change |
|---|---|
| Existing crum's V-width | Existing crum's V-origin |
| Existing crum's I-width | Existing crum's I-origin |
| Ancestor `cwid` fields | Ancestor `cdsp` fields |
| — | All other crums (no shifting) |

This is precisely why [ST-INSERT] (Finding 0062) documents the coalescing cost as `Δcrums = 0` and `Δshifts = 0` for sequential interior typing after the first character at a new position. The ONMYRIGHTBORDER classification makes `makegappm` a no-op, and `isanextensionnd` handles the rest purely through in-place width mutation.

---

## Code Exploration

I now have everything needed. Here is the complete analysis:

---

## `isanextensionnd`: Coalescing, Displacement, and Adjacent Crums

### The predicate itself — `insertnd.c:301-309`

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

Two conditions must hold:

1. `homedoc` of the new insertion equals `homedoc` of the existing crum.
2. `reach == origin` in **all dsp dimensions**.

`prologuend` computes `reach = offset + cdsp + cwid` [retrie.c:334-339]. The `dspsize(POOM) = DSPSIZEPM = 2` [wisp.h:26], so `lockeq` runs over **both** `dsas[I]` (index 0) and `dsas[V]` (index 1) [wisp.h:19-20, 26]. The new insertion must be contiguous in **both** I-space and V-space simultaneously for coalescing to fire.

---

### What changes during coalescing — `insertnd.c:249-258`

```c
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

`dspadd` [wisp.c:15-18] is `lockadd` over `dspsize` tumblers:

```c
int dspadd(typedsp *a, typewisp *b, typedsp *c, INT enftype) {
    lockadd(a->dsas, b->dsas, c->dsas, (unsigned)dspsize(enftype));
}
```

This is `ptr->cwid = ptr->cwid + width` — component-wise tumbler addition across both I and V slots.

**`ptr->cdsp` is not touched.** Not by `dspadd`, not anywhere in the coalescing branch. The I-displacement (and V-displacement) of the coalesced crum are unchanged.

---

### Why `makegappm` is a no-op for extensions — `insertnd.c:124-172`

For POOM insertions, `makegappm` is called **before** `doinsertnd` [insertnd.c:54]. Its early-return guard is:

```c
if (iszerotumbler (&fullcrumptr->cwid.dsas[V])
|| tumblercmp (&origin->dsas[V], &grasp.dsas[V]) == LESS
|| tumblercmp (&origin->dsas[V], &reach.dsas[V]) != LESS)
    return(0);    /* this if for extensions to bc without calling cut*/
```

The comment is explicit. Because `isanextensionnd` requires `reach == origin`, the condition `tumblercmp(&origin->dsas[V], &reach.dsas[V]) != LESS` evaluates to `EQUAL != LESS` → TRUE. `makegappm` returns 0 immediately, performing no cuts and no shifts.

The only place in `makegappm` that modifies a crum's cdsp is the `case 1` displacement shift [insertnd.c:161-165]:

```c
case 1:   /*9-17-87 fix */
    tumbleradd(&ptr->cdsp.dsas[V], &width->dsas[V], &ptr->cdsp.dsas[V]);
    ivemodified(ptr);
    break;
```

This loop — which shifts rightward siblings' V-displacements to make room — **never executes** for a coalescing extension because `makegappm` returns before reaching it.

---

### Why `makeroomonleftnd` is also a no-op — `makeroom.c:13-49`

```c
for (i = 0; i < widsize(father->cenftype); ++i) {
    if (tumblercmp(&origin->dsas[i], &grasp->dsas[i]) == LESS) {
        ...
        expandcrumleftward(...);
    }
}
```

`expandcrumleftward` [makeroom.c:52-74] shifts **all** sons' `cdsp.dsas[index]` by adding a base offset. But for an extension, `origin >= grasp` in all dimensions (we are appending to the right end), so the condition `origin < grasp` is never true. `makeroomonleftnd` does nothing.

---

### Why `setwispupwards` cannot shift adjacent crums — `wisp.c:171-228`

After coalescing, `setwispupwards(father, 1)` calls `setwispnd(father)` [wisp.c:171]. The critical section:

```c
/* find new upper-left corner */
movewisp(&ptr->cdsp, &mindsp);
for (ptr = getrightbro(ptr); ptr; ptr = getrightbro(ptr))
    lockmin((tumbler*)&mindsp, (tumbler*)&ptr->cdsp, (tumbler*)&mindsp, ...);
lockiszerop = iszerolock((tumbler*)&mindsp, (unsigned)dspsize(father->cenftype));
if (!lockiszerop) {
    somethingchangedp = TRUE;
    dspadd(&father->cdsp, &mindsp, &newdsp, (INT)father->cenftype);
} ...
for (ptr = findleftson(father); ptr; ptr = getrightbro(ptr)) {
    if (!lockiszerop) {
        ptr->modified = TRUE;
        dspsub(&ptr->cdsp, &mindsp, &ptr->cdsp, (INT)ptr->cenftype);  // ← shifts ALL sons
    }
    ...
}
```

This normalization loop at [wisp.c:208-215] would subtract `mindsp` from every son's `cdsp` — which would shift adjacent crums. But it only fires when `!lockiszerop`, i.e., when `mindsp != 0`. Since coalescing does not modify any `cdsp`, and a valid enfilade always has its leftmost son at `cdsp = {0, 0}` (the minimum is zero before and after), `mindsp` stays zero, `lockiszerop = TRUE`, and the subtraction loop is skipped. Only `cwid` propagation happens upward.

---

### Summary

| Field | Effect of coalescing |
|-------|---------------------|
| `ptr->cwid` (width, both I and V) | **Increased** by `dspadd` [insertnd.c:251] |
| `ptr->cdsp` (I-displacement and V-displacement) | **Unchanged** — not touched |
| Adjacent siblings' `cdsp` | **Unchanged** — `makegappm` returns early [insertnd.c:140-143]; `makeroomonleftnd` no-ops [makeroom.c:26]; `setwispnd` skips normalization when `mindsp==0` [wisp.c:197] |

**The I-displacement of the coalesced crum does not change.** Only its width grows. And because the extension path bypasses every mechanism (`makegappm` cuts, `expandcrumleftward` shifts, `setwispnd` normalization) that would alter a sibling's displacement, **coalescing can never cause an adjacent crum's displacement to shift.**

---

## Question 18 [gregory]

> The spanfilade DOCISPAN entries persist after DELETE with no cleanup — if document D1 once contained I-span X and D1 is later queried via `find_documents_containing(X)`, does the system return D1 even though D1's current POOM no longer maps to X, or is there a POOM cross-check?

### Gregory's Answer

## KB Synthesis

Yes — `find_documents_containing(X)` returns D1 even after DELETE has removed X from D1's POOM. There is no POOM cross-check.

**The spanfilade is write-only.** [INV-SPANF-WRITE-ONLY] establishes that no delete function exists anywhere in `spanf1.c` or `spanf2.c`. DELETE calls only `deletevspanpm` → `deletend` on the document's POOM (granf layer) with no spanf call. [ST-DELETE / Finding 0057] confirms this explicitly: `dodeletevspan` has no call to any spanf removal function.

**The result is permanent divergence.** [INT-DELETE-SPANF-DIVERGENCE] formalizes exactly this situation: after DELETE, the POOM and spanfilade diverge. The spanfilade continues to assert D1 contains X; the POOM no longer maps any V-address to X. This divergence is permanent — no reconciliation mechanism exists.

**`find_documents_containing` queries the spanfilade, not the POOM.** [SS-DOCISPAN / Finding 0036] establishes that DOCISPAN is the type-4 spanfilade index that `FINDDOCSCONTAINING` queries. It is populated on INSERT/COPY via `insertspanf(..., DOCISPAN)` and never pruned.

**Observational confirmation.** [INV-IADDRESS-PERMANENT / Finding 0023] documents this directly with golden test evidence: after deleting content from D, `find_documents("Findable")` still returns D — the I-address association persists in the spanf index despite V-stream removal. The spanf index for a document only grows over its lifetime.

**The invariant is asymmetric.** [EC-STALE-SPANF-REFERENCE] states the formal relationship: `actual_docs(i) ⊆ find_documents(i)` — the spanfilade returns a **superset** of documents currently containing X. Consumers who need current-state accuracy must post-filter via I-to-V conversion. [INV-ITOV-FILTERING] provides that post-filter: `linksporglset2specset` silently drops I-addresses with no POOM mapping, so converting the stale spanfilade hit back to a V-address yields empty — distinguishing live from ghost references.

In summary: `find_documents_containing(X)` returns D1 (stale reference). No POOM cross-check occurs at query time. The caller must apply I→V conversion to determine whether D1 actually has a current V-position for X.

---

## Code Exploration

I now have all the evidence. Here is the complete answer.

---

## Answer: No POOM Cross-Check — Stale DOCISPAN Entries Cause False Positives

### The Short Answer

**Yes, `find_documents_containing(X)` returns D1 even after D1's content was deleted.** There is no POOM cross-check. The spanfilade is append-only with respect to DOCISPAN entries; DELETE never writes to it.

---

### Traced Call Chain

#### 1. How DOCISPAN entries enter the spanfilade (INSERT)

`doinsert` [do1.c:117-123] → `docopy` [do1.c:45-65]:

```c
// do1.c:62
&&  insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN)
```

`insertspanf` [spanf1.c:15-54]:

```c
// spanf1.c:22
prefixtumbler (isaptr, spantype, &crumorigin.dsas[ORGLRANGE]);
```

This writes a 2D spanfilade crum keyed on:
- **ORGLRANGE** = `DOCISPAN.docisa` (the constant `4` [xanadu.h:39] prefixed to D1's ISA)
- **SPANRANGE** = the I-span X being inserted

Then at [spanf1.c:51]: `insertnd(taskptr,(typecuc*)spanfptr,&crumorigin,&crumwidth,&linfo,SPANRANGE)` actually places the crum into the spanfilade tree.

#### 2. What DELETE does (nothing to the spanfilade)

`dodeletevspan` [do1.c:158-167]:

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

`deletevspanpm` [orglinks.c:145-152]:

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

`deletend` operates only on `docorgl` — the document's own POOM (permutation matrix enfilade) in the V dimension. **`spanf` is never mentioned.** A codebase-wide search for `deletend.*spanf` or `spanf.*deletend` returns zero matches.

There is no counterpart to `insertspanf` on the delete path. No tombstone, no inverse write, nothing.

#### 3. How `find_documents_containing` queries (spanfilade only, no POOM check)

`finddocscontaining` in `fns.c` [line 24-28] → `dofinddocscontaining` [do1.c:15-23] → `finddocscontainingsp` [spanf1.c:151-188]:

```c
// spanf1.c:167-171
clear (&docspace, sizeof(typespan));
tumblerincrement (&docspace.stream, 0, DOCISPAN, &docspace.stream);
tumblerincrement (&docspace.width, 0, 1, &docspace.width);
for (; ispanset; ispanset = ispanset->next) {
    context = retrieverestricted ((typecuc*)spanf, &docspace, ORGLRANGE,
                                   ispanset, SPANRANGE, (typeisa*)NULL);
```

This calls `retrieverestricted` [retrie.c:56-85] which calls `retrieveinarea` → `findcbcinarea2d` [retrie.c:229-268]. The 2D search finds every spanfilade crum whose:
- ORGLRANGE intersects `docspace` (i.e., has DOCISPAN prefix = 4)
- SPANRANGE overlaps the query I-span

For each match [spanf1.c:172-179]:

```c
for (c = context; c; c = c->nextcontext) {
    movetumbler (&c->totaloffset.dsas[ORGLRANGE], &docid);
    beheadtumbler (&docid, &document.address);  // strip DOCISPAN prefix
    if (isinlinklist(*headptr, &document.address))
        continue;
    document.itemid = LINKID;
    document.next = NULL;
    addresssetptr = (typelinkset *) onitemlist(taskptr, (typeitem*)&document, (typeitemset*)addresssetptr);
}
```

The `beheadtumbler` [tumble.c:673] strips the DOCISPAN digit to recover D1's ISA, then adds D1 to the result set.

**There is no further step.** The function returns after `contextfree(context)`. It never:
- Opens D1's POOM via `findorgl`
- Calls `permute` or `vspanset2ispanset` to check whether I-span X still maps to a V-position in D1
- Discards the result if D1's POOM no longer covers X

#### 4. `crumqualifies2d` does not help

The filter inside `findcbcinarea2d` is `crumqualifies2d` [retrie.c:270-305], which matches based on the ORGLRANGE and SPANRANGE tumbler intervals stored in the crum itself. It compares crum origin/width against the query bounds. Since the stale crum still has the same SPANRANGE (I-span X) and ORGLRANGE (DOCISPAN.D1-ISA), it passes the filter. The POOM's current state is not consulted during this filter.

---

### Conclusion

The spanfilade DOCISPAN index is **write-once, never retracted**. When D1 inserts content at I-span X, a crum is written to the spanfilade at [ORGLRANGE=DOCISPAN.D1, SPANRANGE=X]. When D1's content is later deleted:
- The POOM removes the V→I mapping (`deletend` on `docorgl`)
- The spanfilade crum at [DOCISPAN.D1, X] is **left in place**

`find_documents_containing(X)` queries only the spanfilade, finds the stale crum, strips the DOCISPAN prefix, and returns D1 — **a false positive**. The system has no POOM cross-check. D1 will be returned as containing X indefinitely, regardless of how many times its content is deleted or replaced.

---

## Question 19 [gregory]

> REARRANGE preserves I-addresses while changing V-addresses — when a pivot moves content from V:1.2 to V:1.4, does the POOM entry's I-displacement field remain bit-identical, or is it rewritten during the rearrangement even though the logical value is unchanged?

### Gregory's Answer

## KB Synthesis

The I-displacement field remains **bit-identical** after rearrangement. The KB is explicit on the mechanism.

[ST-REARRANGE] (Finding 0056) documents the exact code path:

> "The operation modifies V-addresses exclusively — it calls `tumbleradd(&ptr->cdsp.dsas[index], &diff[i], &ptr->cdsp.dsas[index])` which updates the displacement's **V-address component**. No I-addresses are touched, no content is copied, no new permascroll entries are created."

The `index` variable selects the V dimension (SPANRANGE), not the I dimension (ORGLRANGE). The I-address component (`cdsp.dsas[I]`) is never passed to `tumbleradd` and never written.

[INV-REARRANGE-IDENTITY] (Finding 0056) states this as a formal invariant:

> "`∀ c ∈ content(doc): i_addr(c, doc_after) = i_addr(c, doc_before)`. This is what makes rearrange the **unique** identity-preserving move operation. A delete+insert would: (1) destroy the original I-address, (2) allocate a new I-address..."

The [SS-POOM-BOTTOM-CRUM] entry confirms the dual-field structure:

```
BottomCrum = {
  origin: { dsas[I]: Tumbler, dsas[V]: Tumbler },
  width:  { dsas[I]: Tumbler, dsas[V]: Tumbler }
}
```

Rearrangement touches only the `dsas[V]` component of `origin` (via `tumbleradd`). The `dsas[I]` components of both `origin` and `width` are untouched — same bits, same memory location, zero rewriting.

This is not a logical equivalence that happens to be preserved; it is literal non-modification of those memory words.

---

## Code Exploration

Now I have everything needed for a complete, code-grounded answer.

---

## Answer: REARRANGE and I-Displacement Bit-Identity

### The Short Answer

The I-displacement field (`cdsp.dsas[I]`) is **not touched by the rearrangement displacement step**, but **can be rewritten by tree-restructuring side effects** — specifically by `newpeelcrumoffnd` when a crum is moved to a new parent during cuts. The logical I-address is always preserved; the stored bits may change only when the crum's parent changes.

---

### The Data Structure

`wisp.h:19-20`:
```c
#define I  0
#define V  1
```

`wisp.h:48-54`:
```c
struct structwid {
    tumbler dsas[MAXLOXIZE];  /* MAXLOXIZE = 2 */
};
typedef struct structwid typewid;
typedef typewid typedsp;
```

`enf.h:47-48`:
```c
typewid cwid;
typedsp cdsp;
```

Every POOM crum carries a `cdsp` with two tumbler slots: `dsas[I]` (index 0) and `dsas[V]` (index 1). These are **parent-relative** displacements, not absolute addresses.

---

### The REARRANGE Call Chain

`do1.c:34-43` → `dorearrange` calls `rearrangepm`.

`orglinks.c:137-142`:
```c
bool rearrangepm(typetask *taskptr, tumbler *docisaptr, typeorgl docorgl, typecutseq *cutseqptr)
{
    rearrangend((typecuc*)docorgl, cutseqptr, V);   /* index = V = 1 */
    logbertmodified(docisaptr, user);
    return (TRUE);
}
```

`rearrangepm` passes `V` as the `index` argument. This is the **only** call site for `rearrangend` [protos.h:445 confirms the signature].

---

### The Displacement-Modification Step

`edit.c:113-136`:
```c
for (ptr = (typecuc*)findleftson(father); ptr; ptr = (typecuc *)findrightbro((typecorecrum*)ptr)) {
    i = rearrangecutsectionnd((typecorecrum*)ptr, &fgrasp, &knives);
    switch (i) {
      case 0:  case 4: /* these never move */
        break;
      case 1:  case 2:  case 3: /* 3 only moves in 4 cuts */
        tumbleradd (&ptr->cdsp.dsas[index], &diff[i], &ptr->cdsp.dsas[index]);
        ivemodified((typecorecrum*)ptr);
        break;
    }
}
```

With `index = V`, only `ptr->cdsp.dsas[V]` is written. `ptr->cdsp.dsas[I]` is never referenced here. This answers the primary case: **the rearrangement displacement-addition step leaves I-displacement bits untouched**.

---

### The Cut Phase: Where Bits Can Change

Before displacement-adjustment, `rearrangend` calls `makecutsnd` [edit.c:110] to split any crum that straddles a cut boundary. Two relevant paths:

#### 1. `slicecbcpm` — splitting a bottom crum at a V-cut

`ndcuts.c:373-449`. When a V-cut falls inside a bottom crum (THRUME), it's split in two:

```c
/* ndcuts.c:438-446 */
movewisp (&ptr->cwid, &newwid);
for (i = 0; i < widsize(enftype); i++) {  /* loops over I and V both */
    newwid.dsas[i].mantissa[0] = localcut.mantissa[0];
    tumblerjustify (&newwid.dsas[i]);
}
locksubtract ((tumbler*)&ptr->cwid, (tumbler*)&newwid, (tumbler*)&new->cwid, (unsigned)widsize(enftype));
movewisp (&newwid, &ptr->cwid);
dspadd (&ptr->cdsp, &ptr->cwid, &new->cdsp, enftype);  /* new->cdsp = ptr->cdsp + left-half-cwid */
```

The existing crum `ptr` keeps its original `cdsp.dsas[I]` unchanged. The new right-half crum `new` gets `new->cdsp.dsas[I] = ptr->cdsp.dsas[I] + (left_half_I_width)`. This is a logically correct computed value, not a corruption. Note `localcut` is computed from the V dimension but applied to both `dsas[I]` and `dsas[V]` — this works because POOM bottom crums are 1-to-1 (equal V and I spans within a block).

#### 2. `newpeelcrumoffnd` — moving a crum to a new parent

`ndcuts.c:262-335`. When tree restructuring moves a crum to a sibling or new uncle node:

```c
/* ndcuts.c:287 */
dspadd(&father->cdsp, &ptr->cdsp, &origin, (INT)father->cenftype);
/* ... */
/* ndcuts.c:302 */
dspadd(&father->cdsp, &ptr->cdsp, &temp, (INT)ptr->cenftype);
/* ndcuts.c:311 */
dspsub(&temp, &newuncle->cdsp, &ptr->cdsp, (INT)ptr->cenftype);
```

`dspadd`/`dspsub` operate on the full `typedsp` (both I and V slots). At line 311, `ptr->cdsp` is **rewritten for both dimensions**. The absolute I-address is preserved: `new_cdsp_I = old_absolute_I - newuncle_cdsp_I`. The **stored bits in `cdsp.dsas[I]` change**, even though the logical content address is identical.

---

### Summary

| Operation | Writes `cdsp.dsas[I]`? | Logical I-address preserved? |
|-----------|----------------------|------------------------------|
| `rearrangend` displacement step (`tumbleradd`, `edit.c:125`) | **No** — `index=V` only | N/A |
| `slicecbcpm` on existing crum `ptr` | **No** — `ptr->cdsp` unchanged | Yes |
| `slicecbcpm` on new right-half crum | **Yes** — computed fresh | Yes |
| `newpeelcrumoffnd` reparenting | **Yes** — recalculated relative to new parent | Yes |

**The core rearrangement step never touches `dsas[I]`.** However, the cut-preparation phase (`makecutsnd`) can rewrite `cdsp.dsas[I]` bits in two cases: (a) when creating a new right-half crum from a split, and (b) when `newpeelcrumoffnd` reparents a crum during tree rebalancing. In both cases the absolute I-address is preserved — the displacement is always parent-relative, so the bits must change when the parent changes.

**The I-displacement field is NOT guaranteed to be bit-identical after REARRANGE** — it will be rewritten whenever the crum is reparented during cut-phase tree restructuring. The field stores a relative displacement, and maintaining that invariant requires recomputing it when the crum moves to a different parent node.

---

## Question 20 [gregory]

> After CREATELINK advances the I-address allocation counter past the text range, subsequent text inserts receive non-contiguous I-addresses — does this gap in the I-address space have any effect on `findpreviousisagr` performance or correctness, and can the gap ever be reclaimed?

### Gregory's Answer

## KB Synthesis

## CREATELINK I-Address Gap: Performance, Correctness, and Reclamation

### Performance Effect on `findpreviousisagr`

No meaningful effect. From [SS-ADDRESS-SPACE] (Finding 0061), `findpreviousisagr` performs a B-tree traversal to find the highest existing I-address below an upper bound. The link orgl's I-address occupies exactly one granfilade node — structurally identical to a text character entry. The traversal is O(log N) regardless of whether the maximum found is a text atom or link orgl. The gap between text I-addresses doesn't create any additional nodes to traverse; it's just empty address space that the traversal skips over by going directly to the tree maximum.

### Correctness Effect

No correctness issue. From [INV-MONOTONIC] (Finding 0063), the monotonic invariant `∀ alloc_a, alloc_b : time(a) < time(b) ⟹ iaddr(b) > iaddr(a)` spans all entity types — text characters and link orgls share the same monotonic sequence. When the next text INSERT calls `findpreviousisagr`, it correctly finds the link orgl as the highest existing address and allocates one above it. This is the intended behavior.

The observable consequence — `compare_versions` returning two shared span pairs instead of one for INSERT + CREATELINK + INSERT sequences [INT-LINK-INSERT] — is a semantic artifact, not a data corruption. The I-addresses are allocated correctly; they're just non-contiguous in the text subsequence.

### Can the Gap Be Reclaimed?

No. Three converging properties make this permanent:

1. **Append-only granfilade**: From [FC-GRANF-ON-DELETE] (Finding 0061), DELETE and REARRANGE never modify the granfilade. The link orgl's I-address persists regardless of subsequent operations.

2. **No I-address reuse**: From [INV-NO-IADDR-REUSE], the allocator never backfills gaps. Allocation is purely `findpreviousisagr + 1` — it always advances forward from the current maximum, never returns to fill space vacated by the link orgl (which can't be vacated anyway).

3. **No free list**: From [SS-ADDRESS-SPACE] (Finding 0077), "there is no single global 'next' counter (no Σ.next). Allocation is stateless query-and-increment." There is no free-list mechanism, no gap-tracking, and no garbage collection.

The gap is a permanent structural feature of the granfilade. All future text inserts continue upward from above the link orgl's I-address. The only way to avoid the gap would have been to not call CREATELINK between the two text inserts — once made, the allocation cannot be undone.

---

## Code Exploration

Now I have all the information needed to give a complete, code-cited answer. Let me synthesize.

---

## Full Answer

### 1. How CREATELINK Allocates its I-address

`docreatelink` (`do1.c:207`) calls:
```c
makehint(DOCUMENT, ATOM, LINKATOM, docisaptr, &hint);
createorglingranf(taskptr, granf, &hint, linkisaptr)
```
This reaches `findisatoinsertmolecule` (`granf2.c:158`) with `atomtype=LINKATOM=2` (`xanadu.h:146`). The upper bound for the link search is:
```c
tumblerincrement(&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound);
// LINKATOM+1 = 3 → upperbound = docisa.0.3
```
`findpreviousisagr` (`granf2.c:255`) is called with this `docisa.0.3` upper bound, which traverses the entire atom range (text and links both fall below `docisa.0.3`). The first link then lands at `docisa.0.2.1`, the second at `docisa.0.2.2`, and so on (`granf2.c:170-175`).

For **text insertion**, `doinsert` (`do1.c:117`) uses `TEXTATOM=1` (`xanadu.h:145`), and the upper bound is:
```c
tumblerincrement(&hintptr->hintisa, 2, TEXTATOM + 1, &upperbound);
// TEXTATOM+1 = 2 → upperbound = docisa.0.2
```

---

### 2. The Premise Is Incorrect: There Is No Cross-Contamination

The text and link I-address subspaces are **structurally disjoint**:

- Text atoms live at `docisa.0.1.N` (mantissa `[..., 0, 1, N, ...]`)
- Link atoms live at `docisa.0.2.N` (mantissa `[..., 0, 2, N, ...]`)

Because link ISAs are at `docisa.0.2.N` (where `N ≥ 1`), they are all **numerically ≥ `docisa.0.2`** (`tumblercmp` [tumble.c:72] compares mantissa digit-by-digit: `[...,0,2,1,...]` > `[...,0,2,0,...]`). The text-insertion upper bound is exactly `docisa.0.2`.

In `findpreviousisagr` (`granf2.c:267-276`):
```c
for (ptr = findleftson((typecuc*)crumptr); ptr; ptr = findrightbro(ptr)) {
    if ((tmp = whereoncrum(ptr, (typewid*)offset, upperbound, WIDTH)) == THRUME
    || tmp == ONMYRIGHTBORDER || !ptr->rightbro) {
        findpreviousisagr(ptr, upperbound, offset);
        return(0);
    } else {
        tumbleradd(offset, &ptr->cwid.dsas[WIDTH], offset);
    }
}
```

`whereoncrum` (`retrie.c:345-398`) computes:
```c
right = offset + ptr->cwid.dsas[WIDTH];
return intervalcmp(offset, right, address=docisa.0.2);
```

Any granfilade crum whose interval begins at `docisa.0.2.1` or later will return `TOMYLEFT` for the text upper bound (`docisa.0.2`), meaning `docisa.0.2 < left_boundary_of_crum`. That crum will **not** have its width accumulated, and traversal never enters the link subspace.

**CREATELINK does not advance the text I-address counter at all.** After a link is created at `docisa.0.2.1`, the text `findpreviousisagr` call (upperbound=`docisa.0.2`) will find the last *text* atom and return that as `lowerbound`. Text allocation continues sequentially within `docisa.0.1.*`, completely unaffected.

---

### 3. How WIDTH Values Encode Gaps — and Why Gaps Don't Add Nodes

`insertseq` (`insert.c:17-70`) encodes item boundaries as **tumbler differences** in `cwid.dsas[WIDTH]`:
```c
if (iszerotumbler(&ptr->cwid.dsas[WIDTH])) {  /* last crum in granf */
    tumblerclear(&new->cwid.dsas[WIDTH]);
    tumblersub(&nextaddress, &offset.dsas[WIDTH], &ptr->cwid.dsas[WIDTH]);
} else {
    dspadd(&offset, &ptr->cwid, &reach, GRAN);
    tumblersub(&reach.dsas[WIDTH], &nextaddress, &new->cwid.dsas[WIDTH]);
    tumblersub(&nextaddress, &offset.dsas[WIDTH], &ptr->cwid.dsas[WIDTH]);
}
```

Each granfilade crum's WIDTH is the tumbler distance from its left boundary to the next item. A large gap (e.g., the "jump" from text subspace `docisa.0.1.*` to link subspace `docisa.0.2.*`) is encoded entirely within the WIDTH of the **crum immediately preceding the gap** — it does not create any additional nodes in the enfilade tree.

Because `findpreviousisagr` accumulates these WIDTH values (`tumbleradd(offset, &ptr->cwid.dsas[WIDTH], offset)`) to reconstruct absolute ISA positions, and because gap width is folded into one crum's WIDTH field, **no extra traversal steps occur for gaps**. Performance is strictly O(height of enfilade), which grows logarithmically with the number of inserted **items** — not with the size of any gap between them.

---

### 4. The Asymmetry: Link Search *Does* Traverse Text Subspace

The reverse is true for link allocation. CREATELINK uses upperbound `docisa.0.3`, which **does** span the entire text subspace. A document with N text chunks will cause `findpreviousisagr` to traverse those text crums when allocating each subsequent link. However, this is also O(height) due to the enfilade structure, so it does not degrade performance pathologically; it just means link-space `findpreviousisagr` touches more of the tree than text-space `findpreviousisagr` does.

---

### 5. Gap Reclamation: Impossible by Design

There is no ISA-reclamation or renumbering operation anywhere in the codebase. The granfilade is purely additive. `dodeletevspan` (`do1.c:158`) removes content from the POOM (V-space document tree), not from the granfilade (I-space). The permascroll's permanent-address guarantee means once an ISA is allocated — and the WIDTH of the preceding crum is adjusted to account for the gap — that gap is structurally fixed forever.

Gaps in I-space are not "wasted" in the sense of consuming extra storage: they exist only as larger WIDTH tumbler values in the preceding crum, which is a fixed-size field. Reclaiming them would require re-assigning ISAs globally, which would invalidate every link, span, and cross-document reference in the system — a foundational violation of the Xanadu model.

---

### Summary

| Question | Answer | Citation |
|---|---|---|
| Does CREATELINK advance the text I-address counter? | No. Text search upper bound is `docisa.0.2`; link ISAs at `docisa.0.2.*` are ≥ that bound, invisible to text search. | `granf2.c:162`, `granf2.c:168-169` |
| Does any gap affect `findpreviousisagr` performance? | No. Gap magnitude is encoded in a preceding crum's WIDTH field; no extra tree nodes. | `insert.c:53-60`, `granf2.c:255-278` |
| Does any gap affect `findpreviousisagr` correctness? | No. WIDTH-based offset accumulation gives correct absolute ISA regardless of gap size. | `granf2.c:275`, `tumble.c:365-404` |
| Can gaps be reclaimed? | No. The granfilade is insert-only; no ISA-delete or renumber operation exists. Gaps are permanent Width values in predecessor crums. | `insert.c:17-70`, `do1.c:158-167` |
