# Consultation Answers — Address Permanence

**Inquiry:** What guarantees does the system provide about address permanence? Once content is assigned an address, can that assignment ever change? What is the relationship between permanence of content identity and the ability to reach that content?
**Date:** 2026-03-11 23:14
**Questions:** 20 (10 nelson, 10 gregory)

---

## Question 1 [nelson]

> Once content is assigned an address in the system, can any operation — editing, deletion, or reorganization — ever cause that address to refer to different content?

### Nelson's Answer

# No operation can cause an I-space address to refer to different content. V-space addresses routinely shift.

The answer depends entirely on which of Xanadu's two address spaces you mean.

## I-Space: Absolutely Not

An I-space address is permanent and immutable. No operation — not editing, not deletion, not reorganization — can ever cause an I-space address to refer to different content than it originally identified.

> "Content at an I-space address **never changes**."

The I-space guarantee from Nelson's design:

- Every byte gets a permanent I-space address at creation
- That address will always return that exact content
- Content is immutable after creation

This is enforced by the append-only storage model:

> "Virtually all of computerdom is built around the destructive replacement of successive whole copies of each current version." [LM 2/14]

Nelson explicitly rejects this. Instead:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

Even **deletion** does not affect I-space:

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

Deleted bytes enter a state described as:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

"Not currently addressable" refers to the V-space view — the bytes are gone from the current arrangement. But they remain in I-space, permanently, at the same address.

## V-Space: Yes, Routinely

V-space addresses shift with every edit. This is by design — they represent the document's **current arrangement**, not content identity.

> "The v-stream addresses of any following characters in the document are increased by the length of the inserted text." [LM 4/66]

After an INSERT at position 3 in a document, what was at V-address 5 is now at V-address 6. The V-address 5 now refers to different content. Nelson acknowledges this explicitly:

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." [LM 4/11]

And:

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." [LM 4/30]

## Why This Matters: Links Point to I-Space

The entire architecture depends on this distinction. Links attach to I-space addresses (content identity), not V-space positions (current arrangement). This is why links survive editing:

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes. This has a crucial advantage: it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them." [LM 4/42]

## Tumbler Addresses: Never Reused

At the tumbler level, the forking mechanism ensures addresses are only ever created, never reassigned:

> "New items may be continually inserted in tumbler-space while the other addresses remain valid. This means that any address of any document in an ever-growing network may be specified by a permanent tumbler address." [LM 4/19]

New addresses are created by subdivision (forking digits to the right). No existing address is ever repurposed. The address space grows monotonically.

## Summary

| Address Space | Can refer to different content? | Mechanism |
|---|---|---|
| **I-Space** | Never | Append-only, immutable |
| **V-Space** | Yes, after any edit | INSERT shifts, DELETE closes gaps |
| **Tumbler (structural)** | Never | Forking only creates, never reuses |

The invariant is: **an I-space address is a permanent name for specific content**. The separation of I-space (identity) from V-space (arrangement) is the architectural foundation that makes permanent addressing, link survivability, version comparison, and origin traceability all possible simultaneously.

---

## Question 2 [nelson]

> If a user removes content from their document, does the content's original address continue to exist, and must the system still be able to locate that content through it?

### Nelson's Answer

## Yes — absolutely and unconditionally.

When a user removes content from their document, the content's original I-space address continues to exist permanently, and the system must still be able to locate that content through it. This is not a special case or edge behavior — it is the foundational design principle of Xanadu storage.

### What DELETE actually does

DELETE operates exclusively on V-space (the document's current arrangement). It does not touch I-space (permanent storage). Nelson's diagram on page 4/9 shows "DELETED BYTES" as an explicit system state:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

The phrase "not currently addressable" applies only to that document's current V-stream. The I-space address remains valid.

Nelson makes this explicit:

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

### Why the address must persist

Three guarantees depend on this:

**1. Historical backtrack.** Previous versions of the document still reference this content through their V-space mappings to the same I-space addresses. If the I-space content were destroyed, historical backtrack would be impossible.

> "The file management system we are talking about automatically keeps track of the changes and the pieces, so that when you ask for a given part of a given version at a given time, it comes to your screen." [LM 2/15]

**2. Transclusion integrity.** Other documents may transclude (window) the same content. Their references point to I-space, not to the originating document's V-space. Deletion from one document cannot affect another's view.

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

**3. Link survivability.** Links attach to I-space content, not V-space positions. If I-space content were destroyed on deletion, links would break — violating the survivability guarantee.

> "Links between bytes can survive deletions, insertions and rearrangements, if anything is left at each end." [LM 4/43]

### The architectural basis

Xanadu's storage is append-only by design:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

Every byte ever created has a permanent I-space address of the form `Node.0.User.0.Document.0.Element`. That address encodes origin and never changes. The entire system — tumblers, enfilades, the permanence guarantee — rests on this:

> "New items may be continually inserted in tumbler-space while the other addresses remain valid. This means that any address of any document in an ever-growing network may be specified by a permanent tumbler address." [LM 4/19]

### Summary

| What happens on DELETE | Affected? |
|---|---|
| V-space arrangement (current view) | **Yes** — content removed from current version |
| I-space content (permanent storage) | **No** — bytes remain forever |
| I-space address (permanent identity) | **No** — address remains valid |
| Previous versions | **No** — still contain the content |
| Transclusions in other documents | **No** — still resolve to I-space |
| Links pointing to the content | **No** — still attached to I-space bytes |

The content's original address does not merely "continue to exist" — it *cannot cease to exist*. The system is designed so that destruction of stored content is architecturally impossible. This is the meaning of Nelson's rejection of "destructive replacement" as the storage paradigm. Xanadu's answer to "what happens when you delete?" is: you change the view, never the thing viewed.

---

## Question 3 [nelson]

> What is the distinction between a document no longer displaying certain content and that content's address ceasing to be valid?

### Nelson's Answer

# Display vs. Existence: The Central Architectural Distinction

This question goes to the heart of what makes Xanadu different from every conventional storage system. The distinction is between **V-space** (what a document currently shows) and **I-space** (where content permanently lives). These are two separate address spaces with fundamentally different properties.

## The Two Spaces

**I-Space (Invariant Space)** is where content permanently resides. Every byte ever created gets a permanent I-space address that never changes and never becomes invalid:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

**V-Space (Virtual Space)** is the document's current arrangement — a view that references I-space content. V-addresses are ephemeral and shift with every edit:

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." [LM 4/11]

A document **is** the mapping from V-addresses to I-addresses. Each version defines a different mapping. Editing changes the mapping, not the content.

## What "Delete" Actually Means

When you delete content from a document, you remove it from V-space only. The I-space content is untouched. Nelson's diagram on page 4/9 explicitly shows "DELETED BYTES" as a valid system state:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

And more directly:

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

The content's address has not ceased to be valid. The document has merely stopped *displaying* it. The distinction is between:

| What happened | V-space effect | I-space effect |
|---|---|---|
| Content deleted from document | Removed from current arrangement | **None** — bytes remain forever |
| Content rearranged | Positions shift | **None** — bytes unchanged |
| New version created | New arrangement | **None** — same content, different view |

## Why This Matters

Nelson designed this separation to solve what he saw as the fundamental flaw of conventional computing:

> "Virtually all of computerdom is built around the destructive replacement of successive whole copies of each current version." [LM 2/14]

His alternative:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

The consequences cascade through the entire system:

1. **Links survive editing** — because links point to I-space addresses, not V-space positions. A link to content that has been "deleted" from a document still resolves, because the I-address is still valid:

   > "A Xanadu link is not between points, but between spans of data... links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them." [LM 4/42]

2. **Historical backtrack works** — because every previous V-space arrangement can be reconstructed from the permanent I-space content:

   > "The file management system we are talking about automatically keeps track of the changes and the pieces, so that when you ask for a given part of a given version at a given time, it comes to your screen." [LM 2/15]

3. **Transclusions survive** — if Document A transcludes content from Document B, and Document B's owner "deletes" that content from Document B's current version, the content still exists in I-space and Document A still shows it.

4. **Modifications never damage originals** — because modifications operate on V-space arrangements, not I-space content:

   > "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate--without damaging the originals." [LM 2/45]

## The Analogy

Think of it as a library versus a reading list:

```
I-Space (Library)              V-Space (Reading Lists)
┌─────────────────────┐        ┌─────────────────────┐
│ Shelf A: "hello"    │        │ My Essay v1:        │
│ Shelf B: " world"   │   ──►  │   [ref A, ref B]    │  → "hello world"
│ Shelf C: "!"        │        │                     │
│                     │        │ My Essay v2:        │
│ (never changes)     │   ──►  │   [ref A, ref C]    │  → "hello!"
└─────────────────────┘        └─────────────────────┘
```

Removing " world" from the reading list does not burn the book on Shelf B. The shelf address remains valid. The reading list simply no longer references it.

## The Permanence Guarantee

This is not a side effect of the implementation but the **foundational guarantee** of the system:

> "New items may be continually inserted in tumbler-space while the other addresses remain valid. This means that any address of any document in an ever-growing network may be specified by a permanent tumbler address." [LM 4/19]

A content address ceasing to be valid would violate Xanadu's deepest invariant. The whole point of the system is that **display is mutable but existence is permanent**. A document choosing not to show something is an editorial decision. An address becoming invalid would be a system failure.

---

## Question 4 [nelson]

> Must every piece of content that has ever been stored in the system remain permanently reachable by its original address, or are there conditions under which reachability may be lost while identity is preserved?

### Nelson's Answer

# Reachability vs. Identity in Xanadu

The system distinguishes between **identity** (the permanent association between an I-space address and specific bytes) and **reachability** (the ability to retrieve those bytes on demand). Identity is an absolute technical guarantee. Reachability is not.

## The Technical Guarantee: Addresses Are Permanent

The tumbler architecture guarantees that an address, once assigned, is never reused or invalidated:

> "New items may be continually inserted in tumbler-space while the other addresses remain valid. This means that any address of any document in an ever-growing network may be specified by a permanent tumbler address." [LM 4/19]

This is a property of the number system itself. Tumblers grow by forking — inserting new sub-addresses — so existing addresses are structurally undisturbed.

## Five Conditions Where Reachability Is Lost

### 1. V-Space Deletion

The most explicit case. Nelson's own diagram on page 4/9 defines a system state called "DELETED BYTES":

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

The phrase "not currently addressable" is precise: the I-space content persists, but V-space no longer maps to it. Since FEBE retrieval operates through V-space (the RETRIEVEV command takes virtual span addresses), content deleted from all V-space views becomes unreachable through normal protocol operations — even though it still exists.

Nelson confirms the I-space side is untouched:

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

Identity preserved; reachability lost (pending historical backtrack, which is listed as an intended but not-yet-implemented feature in XU.87.1).

### 2. Storage Funding

Nelson requires that all services be economically self-sustaining:

> "ALL SERVICES MUST BE SELF-SUPPORTING. Subsidy between one aspect of the system and another could only work temporarily. This means, for example, that archival storage must be economically self-sustaining." [LM 4/5]

Content owners pay ongoing storage rental. Nelson does not specify what happens when payment lapses. The curated analysis in the storage-funding source puts it precisely: permanence of the address (never reused) is distinct from permanence of accessibility (requires ongoing payment). Nelson left this gap unresolved — he specifies neither a grace period nor a mechanism for preserving orphaned content.

### 3. Access Control (Private Documents)

> "A private document may be read and linked-to only by the owner and his or her associates." [LM 2/42]

Private content is unreachable to unauthorized users by design. The identity (I-address) exists, but the system refuses delivery. Nelson even notes this was not yet implemented: "Private documents. (Currently all documents are visible to all users.)" [LM 4/79].

### 4. Network Unavailability

> "It is a truism that 'computer networks are always broken.' Meaning that on the average some nodes are disconnected or not working." [LM 4/75]

The BEBE protocol mitigates this through backup copies and forwarding, but Nelson treats temporary unreachability as a normal system state, not a failure. Content may be unavailable while its home server is down and no cached copy exists nearby.

### 5. Peremptory Challenge (Content Removal)

For anonymous ("John Doe") publications:

> "Consider libelous or uncomplimentary John Doe graffiti defaming specific individuals. If John Doe is not available, the affected individual must be able to effect removal of the materials by peremptory challenge." [LM 2/60]

This is an explicit mechanism for making content unreachable. Nelson does not specify whether "removal" means V-space deletion (identity preserved in I-space) or something more drastic.

## The Published-Content Obligation

For **published** documents, Nelson makes the strongest reachability claim:

> "It is in the common interest that a thing once published stay published, as in the world of paper. Other readers and users will come to depend on its accessibility. Consequently its author may not withdraw it except by lengthy due process." [LM 2/43]

But note the qualifier: "except by lengthy due process." Withdrawal is possible — just difficult. And the reason for the obligation is social, not technical: other users' links depend on continued accessibility. The guarantee is contractual (enforced through the publication agreement and vendor franchise), not architectural.

## The Architectural Picture

The system has three layers, each with a different permanence guarantee:

| Layer | Guarantee | Basis |
|-------|-----------|-------|
| **I-space address** | Permanent identity; never reused | Technical (tumbler arithmetic) |
| **I-space content** | Append-only; never overwritten | Architectural (permascroll design) |
| **V-space reachability** | Contingent on arrangement, access, funding, network | Social/contractual |

Nelson designed the addressing system so that identity is an absolute invariant — you can always *name* something by its I-address. But whether that name resolves to delivered bytes depends on conditions outside the address system: whether a V-space mapping exists, whether the owner has paid storage, whether you have access rights, and whether the network path is working.

## Summary

**Identity is permanent. Reachability is not.**

The I-space address is a conservation law — once a byte is assigned an address, that address belongs to that byte forever, and is never reassigned. But the ability to actually retrieve content at that address depends on V-space arrangement, storage economics, access permissions, network availability, and legal process. Nelson's "not currently addressable, awaiting historical backtrack functions" [LM 4/9] is the clearest evidence that he designed the system with this distinction in mind: content can be unreachable while its identity — and the possibility of future recovery — is preserved.

---

## Question 5 [nelson]

> When content is shared across multiple documents, does each document refer to the same address for that content, or does each receive its own address for its own copy?

### Nelson's Answer

## Each document refers to the same I-space address

When content is shared across multiple documents, every document points to the **same permanent I-space address**. There is no duplication. This is the central architectural insight of Xanadu.

### The mechanism

Content is created once and stored permanently at an I-space address. Documents are V-space arrangements — sequences of references to I-space content. When you "include" content from another document, your document's V-space simply adds a mapping to the same I-space bytes that already exist.

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

> "The virtual byte stream of a document may include bytes from any other document." [LM 4/10]

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

The word "virtual" is key. These are not copies in the conventional sense — they are references. The content exists at one I-space address, and multiple V-space arrangements point to it.

### The COPY operation is transclusion, not duplication

The FEBE COPY command does **not** create a second instance of the content:

> "The material determined by \<spec set\> is copied to the document determined by \<doc id\> at the address determined by \<doc vsa\>." [LM 4/67]

Despite the name "COPY," this creates a V-space mapping to existing I-space content. The destination document's V-stream now includes a reference to the same bytes at the same I-space address. No new bytes are stored.

### Identity is structural, not value-based

This distinction matters: content identity is determined by **where it was created**, not by what it says. If I type "hello" and you independently type "hello," those are different I-space addresses — different bytes, different origins. But if you transclude my "hello" into your document, your document points to **my** I-space address. We share the same bytes.

This is how the system knows the difference between coincidental similarity and actual quotation. Shared I-space addresses prove derivation; matching text alone does not.

### Why this matters

Because all documents sharing content point to the same I-space address:

1. **Attribution is automatic** — the I-address encodes which document created the bytes, so origin is always traceable: "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

2. **Correspondence is computable** — the system can identify shared content across versions and documents by comparing I-addresses: "a facility that holds multiple versions of the same material... is not terribly useful unless it can help you intercompare them in detail — unless it can show you, word for word, what parts of two versions are the same." [LM 2/20]

3. **Royalties flow correctly** — when shared bytes are delivered, the system knows whom to pay because the I-address identifies the owner.

4. **No distributed update problem** — since there is only one instance of the content, there is nothing to synchronize: "No copying operations are required among the documents throughout the system, and thus we solve the problems of update — especially the problem of updating documents which depend on other documents." [LM 2/36]

### The analogy

Think of I-space as a library where every book has a permanent shelf location. A document is a reading list — a sequence of references like "shelf A, pages 1-5; shelf B, pages 3-7." Multiple reading lists can reference the same shelf locations. The books are never duplicated; only the reading lists differ.

```
I-Space (permanent)           V-Space (per-document)
┌──────────────────┐          Document A: [ref X, ref Y]  → "hello world"
│ addr X: "hello"  │          Document B: [ref X, ref Z]  → "hello!"
│ addr Y: " world" │          Document C: [ref X, ref Y]  → "hello world"
│ addr Z: "!"      │
└──────────────────┘          A and C share the same I-addresses for
                              identical content — true transclusion.
```

Documents A and C both contain "hello world" and both point to the **same** I-space addresses X and Y. This shared origin is what makes them correspond — not the fact that they happen to display the same text.

---

## Question 6 [nelson]

> If a new version of a document rearranges its content, must the addresses of the individual content elements remain unchanged across versions?

### Nelson's Answer

# Address Stability Across Versions

The answer depends on **which** address you mean. Xanadu has two address spaces, and they behave oppositely under rearrangement.

## I-Space Addresses: Permanently Unchanged

I-space addresses are **immutable by definition**. They encode the permanent identity of content — which server, which user, which document created each byte. Rearranging a document's content does not and cannot change these addresses.

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

I-space is append-only. Content, once created, lives at its I-address forever. A new version does not create new content — it creates a new *arrangement* of existing content.

## V-Space Addresses: Explicitly Designed to Change

V-space addresses — the positions in the document's virtual byte stream — are **expected to change** during rearrangement. This is the entire point of V-space.

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." [LM 4/30]

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." [LM 4/11]

The REARRANGE operation explicitly transposes regions of text [LM 4/67], which shifts V-space positions. INSERT increases V-addresses of following characters by the length of the inserted text [LM 4/66]. These are normal, expected operations.

## The Design Principle

A version **is** a V-space arrangement. Creating a new version means creating a new mapping from V-addresses to I-addresses, over the same underlying I-space content:

```
Version 1 (V→I mapping):    Version 2 (V→I mapping):
  V-pos 1 → I-addr A          V-pos 1 → I-addr C
  V-pos 2 → I-addr B          V-pos 2 → I-addr A
  V-pos 3 → I-addr C          V-pos 3 → I-addr B
```

The I-addresses (A, B, C) are unchanged. The V-addresses have been rearranged. This is precisely what Nelson means by:

> "There is thus no 'basic' version of a document set apart from other versions — 'alternative' versions — any more than one arrangement of the same materials is a priori better than other arrangements." [LM 2/19]

## Why This Matters

Links point to I-space addresses, not V-space positions. This is why links survive editing:

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes. This has a crucial advantage: it means that links can survive editing." [LM 4/42]

And it is why correspondence across versions works — two versions that share I-space content can be compared automatically:

> "Of course, a facility that holds multiple versions of the same material, and allows historical backtrack, is not terribly useful unless it can help you intercompare them in detail — unless it can show you, word for word, what parts of two versions are the same." [LM 2/20]

## Summary

**I-space addresses must remain unchanged** — they are permanent, immutable identifiers. **V-space addresses are expected to change** — that is what rearrangement, versioning, and editing *are*. The separation of identity (I-space) from arrangement (V-space) is the architectural foundation that makes both permanence and flexibility possible simultaneously.

---

## Question 7 [nelson]

> Does the system guarantee that an address assigned today will resolve to the same content a century from now, and what would constitute a violation of that guarantee?

### Nelson's Answer

# Address Permanence and Content Resolution

The question touches the deepest architectural commitment in Xanadu. The answer requires separating two guarantees that people habitually conflate: **address permanence** and **content accessibility**.

## The Address Guarantee: Absolute

The tumbler address assigned today will designate that same content forever. This is not aspirational — it is structural:

> "New items may be continually inserted in tumbler-space while the other addresses remain valid. This means that any address of any document in an ever-growing network may be specified by a permanent tumbler address." [LM 4/19]

The addressing system was designed specifically so that growth never invalidates existing references. Forking creates new sub-addresses beneath existing ones; nothing is renumbered, relocated, or reassigned. The address IS the identity.

In I-space, content is immutable:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control." [LM 4/11]

The append-only storage model means content, once written, is never overwritten:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

Even "deletion" does not touch I-space content. Deleted bytes are described as:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

So: **the I-space address assigned today will, by architectural mandate, designate precisely the same bytes a century from now.** The address cannot be reassigned. The content cannot be overwritten. This is not a policy — it is how the storage works.

## What Would Constitute a Violation

Three things would violate this guarantee:

**1. Address reassignment.** If a tumbler address that once designated content X were made to designate content Y, the entire addressing system collapses. Every permanent citation, every link, every transclusion depends on addresses being eternal. This would be the equivalent of reassigning telephone numbers while people are mid-conversation — except worse, because the damage is permanent and retroactive.

**2. Content mutation at an I-address.** If bytes at an I-space address were modified after storage, the guarantee is broken. The system is append-only precisely to prevent this. Modifying stored bytes would silently corrupt every document that transcludes that content, every link that points to it, every version that includes it.

**3. Unauthorized withdrawal of published content.** Publication creates binding obligations:

> "It is in the common interest that a thing once published stay published, as in the world of paper. Other readers and users will come to depend on its accessibility. Consequently its author may not withdraw it except by lengthy due process." [LM 2/43]

Other users will have linked to it. Their links — which they own, at their addresses — depend on the continued existence of the target. Unilateral withdrawal breaks others' property.

## The Harder Question: Accessibility

Now the uncomfortable part. Address permanence and content immutability are architectural guarantees. But **accessibility** — whether you can actually retrieve the content — depends on economics:

> "ALL SERVICES MUST BE SELF-SUPPORTING. Subsidy between one aspect of the system and another could only work temporarily. This means, for example, that archival storage must be economically self-sustaining." [LM 4/5]

Someone must pay ongoing storage rental. If the content owner stops paying and no one else takes over, the content may become inaccessible — not because the address is invalid or the content destroyed, but because no vendor is contractually obligated to serve it for free.

This is the distinction between the address **being valid** (always) and the content **being delivered** (requires economic support). A book's Library of Congress catalog number doesn't expire when the book goes out of print — but the book may become hard to find.

## What Is NOT a Violation

Several things that might appear to violate the guarantee do not:

- **V-space rearrangement.** If you ask for a document's current arrangement and it has been edited since you last looked, the V-space has changed. But V-space is explicitly ephemeral — "the address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing" [LM 4/11]. The I-address is what's permanent.

- **Content becoming temporarily unreachable.** The system acknowledges that "computer networks are always broken" [LM 4/75]. Temporary unavailability due to network partition or server downtime is expected, not a violation.

- **Supersession.** When a new version supersedes an old one, the old version remains at its address. The supersession link declares "there is something newer," but the original content is untouched.

## The Verification Gap

One final, sobering point. The system provides **no cryptographic verification** that the content returned at an address is what was originally stored:

> "User acknowledges that all material on the network is stored by users under similar arrangements to User's own, without verification or assurance of truth, authenticity, accuracy, usefulness or other beneficial character of such materials." [LM 5/17]

> "Storage Vendor makes no guarantee as to the correctness or authenticity of any material received from other Users." [LM 5/18]

The guarantee that an address resolves to the same content rests on **contractual trust** in the Storage Vendor franchise, not on mathematical proof. If a vendor is honest, the guarantee holds. If a vendor is compromised or dishonest, there is no technical backstop to detect the alteration.

This is a pre-cryptographic architecture. The address is permanent. The content is append-only. But the proof that what you receive is what was stored relies on the integrity of the franchise, not on the bits themselves.

## Summary

| Aspect | Guaranteed? | Mechanism |
|--------|-------------|-----------|
| Address permanence | **Yes, absolutely** | Tumbler architecture — addresses never reassigned |
| Content immutability | **Yes, architecturally** | Append-only I-space — bytes never overwritten |
| Published accessibility | **Yes, contractually** | Publication contract — withdrawal only by "lengthy due process" |
| Ongoing accessibility | **Conditionally** | Requires economic support (storage rental) |
| Content authenticity | **No** | Trust in vendor, not cryptographic verification |

The system guarantees that the address assigned today will **mean** the same thing a century from now. Whether you can **reach** what it means depends on whether civilization maintains the economic and institutional infrastructure to keep serving it — which is precisely why I designed it to be distributable into "deep rock and deep space" [LM 3/25].

---

## Question 8 [nelson]

> Is address permanence a property of the content itself or of the relationship between the content and the storage system — that is, could the system migrate content internally while preserving the address?

### Nelson's Answer

## Address Permanence Is a Property of the Coordinate System, Not of Physical Storage

The answer is unambiguous in the architecture: **the system can and must migrate content internally while preserving addresses.** Address permanence is a property of the logical coordinate system (tumbler-space), not of any physical storage arrangement.

### The Address Space Is Abstract

Tumbler-space is a conceptual coordinate system that exists independently of what is physically stored:

> "The docuverse is the occupied tumbler-space--as occupied by conceptually assigned positions, even if nothing represents them in storage." [LM 4/23]

> "Thus the address population of tumbler-space is also an abstraction, since things may be addressed even though nothing is there to represent them in storage." [LM 4/23]

Ghost elements prove the point decisively: addresses can exist with **nothing stored at them**. The address is not a property of stored bytes — it is a position in an abstract coordinate space that bytes may or may not occupy.

### Physical Migration Is Explicitly Designed In

The BEBE protocol describes content actively moving between servers:

> "The contents can slosh back and forth dynamically." [LM 4/72]

Content migrates for four explicit reasons:

> "Material is moved between servers for a number of purposes: 1. for more rapid access to final material, 2. for more rapid access to needed material which indexes material on other servers, 3. for rebalance in keeping with demand, 4. for redundancy and backup purposes." [LM 4/71]

Each server holds a subset of the whole — a "microcosm that shrinks and grows" [LM 4/71]. Content replicates toward demand. The physical location of bytes is a performance optimization, not an identity property.

### Physical Storage Is Explicitly Hidden from Users

The FEBE protocol hides all physical details:

> "Now that some of these commands are to be seen by the user: The user's concerns are document content and links, and the complications of the protocol are to be handled invisibly by programs in the user's front-end machine, leaving the user free to think about other things." [LM 4/61]

Users work with tumbler addresses. Where bytes physically reside is invisible and irrelevant to them.

### The I-Address Encodes Provenance, Not Location

The I-space address has the form `Node.0.User.0.Document.0.Element` [LM 4/26]. The Node field records which server **originally created** the content — its provenance. But content migrates between servers freely via BEBE. The Node field is a birth certificate, not a GPS coordinate.

This is confirmed by how "native" and "non-native" bytes work:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

The system **fetches** content from wherever it currently lives. The address tells you where to start looking (the home location), but BEBE's forwarding and subrepresentation mechanisms handle the actual retrieval regardless of physical location.

### The V-Space Address Is Explicitly Mutable

To sharpen the contrast: V-space addresses (the document's current arrangement) change constantly during editing:

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." [LM 4/11]

I-space addresses are permanent. V-space addresses are ephemeral. But even I-space permanence refers to the **logical identity** of the content (this byte was created at this coordinate), not to the physical location of the storage medium holding it.

### The Enfilades Handle the Mapping

The internal data structures (enfilades) exist precisely to maintain the mapping between logical addresses and physical storage:

> "His new method would allow linkages to keep up with all changes. It was instantaneous and permanent and could grow indefinitely. All changes, once made, left the file remaining in canonical order, which was an internal mandate of the system." [LM 1/34]

The enfilades are the mechanism that makes addresses permanent while storage is reorganized. They map the abstract coordinate (tumbler address) to wherever the bytes currently live.

### Summary

Address permanence in Xanadu is a three-layer design:

| Layer | What it is | Permanent? |
|-------|-----------|------------|
| **Tumbler address** | Logical coordinate in abstract space | Yes — forever |
| **I-space content** | The bytes themselves (immutable once created) | Yes — append-only |
| **Physical storage location** | Where bytes reside on which server | No — migrates freely |

The guarantee to users is: **this coordinate will always resolve to this content.** The system is free — indeed required — to migrate, replicate, cache, and redistribute the physical bytes to meet the "soft corridor" performance requirement. Tumblers are coordinates in a conceptual space. Storage is an optimization problem solved by enfilades and BEBE. The two concerns are deliberately decoupled.

---

## Question 9 [nelson]

> How does address permanence relate to link integrity — if an address is permanent, does the system guarantee that any link pointing to that address will always connect to the intended content?

### Nelson's Answer

## Address Permanence and Link Integrity

The short answer: address permanence is **necessary but not sufficient** for link integrity. Nelson's architecture achieves link integrity through three distinct guarantees working in concert, not through address permanence alone.

---

### The Three Guarantees

**1. Address Permanence (Tumblers)**

> "New items may be continually inserted in tumbler-space while the other addresses remain valid. This means that any address of any document in an ever-growing network may be specified by a permanent tumbler address." [LM 4/19]

This guarantees that the *location* never changes. Once a tumbler is assigned, it is assigned forever. But a permanent address is just a stable name — it says nothing about what happens to the content at that name.

**2. Content Immutability (I-Space)**

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control." [LM 4/11]

I-space content never changes after creation. A byte stored at I-address X will always be that same byte. This is the deeper guarantee: not just that the address persists, but that what lives there is immutable.

**3. Span-Based Attachment (Link Survivability)**

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes. This has a crucial advantage: it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them." [LM 4/42]

Links attach to **bytes** (I-space entities), not to **positions** (V-space coordinates). This is the mechanism that converts address permanence and content immutability into actual link integrity.

---

### Why Address Permanence Alone Is Insufficient

Consider what would happen if links pointed to V-space positions instead of I-space content:

- V-space addresses shift on every edit: "The v-stream addresses of any following characters in the document are increased by the length of the inserted text." [LM 4/66]
- A link to "V-position 47" would point to different content after any insertion before position 47
- The *address* might be permanent, but it would no longer designate the *intended content*

Nelson explicitly acknowledges this instability:

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." [LM 4/11]

V-space addresses are ephemeral by design. A permanent V-space address would be meaningless because the mapping V→I changes with every edit.

The architectural solution: links point to I-space spans. Since I-space addresses are both permanent (tumbler guarantee) and immutable (append-only guarantee), the link always resolves to the same bytes.

---

### The DELETE Question

This is where the design becomes subtle. "Deleting" content removes it from V-space but NOT from I-space:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

So if Alice links to paragraph P in Bob's document, and Bob "deletes" P:
- P disappears from Bob's current V-stream
- P's I-space content remains forever
- Alice's link still points to valid I-space bytes
- The link **survives** — the content exists, it's just no longer in Bob's current arrangement
- Previous versions of Bob's document still show P
- Any other document that transcludes P still shows it

The link connects to the **intended content** because I-space is immutable. Whether that content is currently *visible in the target document* is a separate question from whether the link is *intact*.

---

### Where the Guarantee Has Limits

Nelson's design guarantees that a link will always point to the same bytes. But there are three areas where "connecting to the intended content" has caveats:

**1. Accessibility depends on storage funding.**

Nelson specifies that "ALL SERVICES MUST BE SELF-SUPPORTING" [LM 4/5]. Storage requires ongoing rental. If the owner stops paying, the content may become inaccessible even though its address remains permanently assigned and the link remains structurally valid. The address is permanent; accessibility is not unconditionally guaranteed.

**2. Authenticity is not cryptographically verified.**

> "User acknowledges that all material on the network is stored by users under similar arrangements to User's own, without verification or assurance of truth, authenticity, accuracy, usefulness or other beneficial character of such materials." [LM 5/17]

The system trusts the Storage Vendor franchise to preserve content faithfully. There is no technical mechanism to verify that bytes returned at an address are the original bytes. A compromised vendor could alter content while the address and link remain "valid." Trust is contractual, not mathematical.

**3. Ghost elements are valid link targets.**

> "While servers, accounts and documents logically occupy positions on the developing tumbler line, no specific element need be stored in tumbler-space to correspond to them. Hence we may call them ghost elements." [LM 4/23]

> "It is possible to link to a node, or an account, even though there is nothing stored in the docuverse corresponding to them." [LM 4/23]

A link can point to an address where nothing has ever been stored. The address is permanent, the link is structurally valid, but there is no "intended content" — only an intended location. This is by design (it enables forward references and hierarchical queries), but it means address permanence does not guarantee content existence.

---

### Version-Spanning: The Strongest Form of the Guarantee

The most powerful expression of the address-permanence-plus-link-integrity relationship is **version-spanning links**:

> "Links may be refractively followed from a point or span in one version to corresponding places in any other version. Thus a link to one version of a Prismatic Document is a link to all versions." [LM 2/26]

Because links point to I-space content, and because correspondence between versions is computed from shared I-space origin, a link made against version 1 of a document automatically works in version 2, version 3, and any future version — as long as the corresponding bytes survive. The permanent address identifies the content; the I-space architecture makes that identification survive across all versions.

---

### Summary

| Guarantee | What It Ensures | What It Does NOT Ensure |
|-----------|----------------|------------------------|
| **Address permanence** | Location never changes | Content exists or is accessible |
| **I-space immutability** | Content at location never changes | Content is accessible or authentic |
| **Span-based linking** | Link attaches to content, not position | All linked bytes still exist |

The three work together: permanent addresses mean the name is stable; I-space immutability means the content at that name is stable; span-based linking means the connection tracks the content, not the arrangement. The result is that a link will always point to the same bytes it originally designated — provided those bytes remain in I-space (which they do, since I-space is append-only) and the storage vendor is trustworthy (which is contractual, not technical).

Nelson's architecture achieves link integrity not through any single mechanism, but through the **separation of identity from arrangement**. The permanent address lives in I-space where content is immutable. Editing happens in V-space where addresses are ephemeral. Links cross from V-space into I-space, anchoring themselves to permanent content. This is why Nelson insists on the I-space/V-space distinction — without it, address permanence would be meaningless for link integrity.

---

## Question 10 [nelson]

> Must the system distinguish between content that is permanently stored but currently inaccessible and content whose address has been invalidated, or are these the same condition?

### Nelson's Answer

## They Are Distinct Conditions — and One Cannot Occur

Nelson's architecture makes these two conditions fundamentally different. In fact, address invalidation **does not exist** in the design.

### Addresses Are Permanent by Construction

Tumbler addresses, once assigned, are valid forever. This is not a policy but a structural property of the addressing system:

> "New items may be continually inserted in tumbler-space while the other addresses remain valid. This means that any address of any document in an ever-growing network may be specified by a permanent tumbler address." (4/19)

There is no INVALIDATE operation in FEBE. There is no mechanism by which a tumbler address ceases to be a valid point in the docuverse. The address space only grows; it never contracts.

### Temporary Inaccessibility Is Expected

Nelson explicitly designs for content that exists but cannot currently be reached:

> "It is a truism that 'computer networks are always broken.' Meaning that on the average some nodes are disconnected or not working." (4/75)

The system handles this through forwarding, backup copies, and subrepresentation. Each server holds "a microcosm that shrinks and grows" (4/71), and "the contents can slosh back and forth dynamically" (4/72). A request that cannot be fulfilled is forwarded to backup locations, with "not currently available" as a last resort — not an error indicating the address is invalid.

### Ghost Elements: Valid Addresses With No Content

Nelson goes further. An address can be valid even when **nothing has ever been stored there**:

> "While servers, accounts and documents logically occupy positions on the developing tumbler line, no specific element need be stored in tumbler-space to correspond to them. Hence we may call them ghost elements." (4/23)

> "It is possible to link to a node, or an account, even though there is nothing stored in the docuverse corresponding to them." (4/23)

Ghost elements demonstrate that "valid address" and "content exists" are independent properties. You can link to an address before anyone puts content there. The address is real; the content is absent. This is by design, not an error state.

### DELETE Creates a Third Distinct State

Nelson's DELETE produces yet another condition — content exists in I-space but is removed from V-space:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" (4/9)

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." (4/11)

The content is permanently stored. The I-address is still valid. But the content is not reachable through the current V-space arrangement. It remains accessible through historical backtrack or through other documents that transclude it.

### The Spectrum of States

Nelson's architecture thus implies at least four distinct conditions for a given address:

| State | Address valid? | Content in I-space? | Currently deliverable? |
|-------|---------------|--------------------|-----------------------|
| Normal | Yes | Yes | Yes |
| Network partition | Yes | Yes | Temporarily no |
| V-space deleted | Yes | Yes | Not via current version |
| Ghost element | Yes | No | No (nothing to deliver) |

Address invalidation — where the address itself ceases to be meaningful — is absent from this table because it cannot occur.

### The Unresolved Tension

There is one scenario Nelson does not fully resolve: what happens when storage payment lapses? He requires that "ALL SERVICES MUST BE SELF-SUPPORTING" (4/5) and frames storage as ongoing rental, but never specifies what happens to content when the owner stops paying. The address would remain valid (tumblers are permanent), but the content might become inaccessible — a state analogous to "network partition" but potentially permanent.

Published content adds another constraint: "It is in the common interest that a thing once published stay published" (2/43), and withdrawal requires "lengthy due process." This creates tension with self-supporting storage but does not resolve it.

### Answer

The system **must** distinguish between these conditions because they are architecturally different. "Permanently stored but currently inaccessible" is a real and expected state — the network routes around it. "Address invalidated" is a condition that **cannot arise** in Nelson's design. Tumblers are permanent. The docuverse only grows. An address, once baptized, is a permanent point in the universal address space regardless of what content — if any — exists there.

---

## Question 11 [gregory]

> Once a byte is stored in the granfilade at a given I-address, is there any code path — including error handling or cache eviction via `grimlyreap` — that can overwrite or remove that byte from its I-address slot?

### Gregory's Answer

## KB Synthesis

No. Once a byte is written to the granfilade at a given I-address, no code path in the system overwrites or removes it.

**The allocation model is append-only by construction**

`inserttextingranf` allocates fresh I-addresses by querying the granfilade tree via `findpreviousisagr` to find the current maximum, then incrementing by one. New content always lands beyond all prior allocations. There is no free-list, no gap-filling, and no reuse mechanism. [INV-NO-IADDR-REUSE], [INV-MONOTONIC]

**DELETE and REARRANGE don't touch the granfilade**

DELETE (`deletevspanpm` → `deletend`) modifies only the document's POOM — it disowns and frees the B-tree crums that *map* V-positions to I-addresses. The I-addresses themselves, and the content bytes at those I-addresses in the granfilade, are untouched. `dodeletevspan` makes no call to any granf removal function. [FC-GRANF-ON-DELETE], [ST-DELETE], [INV-IADDR-IMMUTABILITY]

Same for REARRANGE: it calls `tumbleradd` on `cdsp.dsas[V]` (V-space displacement only). The granfilade is not consulted at all. [FC-GRANF-ON-DELETE]

**`grimlyreap` is write-back, not replacement**

When memory pressure triggers the grim reaper, it scans for crums with `age >= OLD` and `modified == TRUE`, writes them to disk via `orglwrite()`, then frees the in-memory structs. This is a write-back flush — the crum's content is written to *its own assigned disk block*, then the in-memory copy is released. The on-disk content at any previously written I-address block is never overwritten by this path. [SS-CACHE-MECHANISM]

The only wrinkle is [EC-CRASH-MID-WRITE]: if a crash occurs mid-write during `subtreewriterecurs` (which writes bottom-up: children before parents), structural pointers in the root may reference old blocks while new leaf blocks are orphaned. But this affects *tree navigation structure*, not the content bytes at leaf nodes. Leaf granf atoms that were already flushed to disk remain intact at their block addresses; no content byte is overwritten.

**The invariant is explicit throughout the KB**

> "The granfilade is append-only — `inserttextingranf` always allocates fresh addresses at the end. There is no mechanism to reuse, reassign, or deallocate I-addresses." — [INV-IADDR-IMMUTABILITY] (Finding 0064)

> "∀ i, t₁ < t₂ : i ∈ granfilade(t₁) ⟹ i ∈ granfilade(t₂) ∧ content(i, t₁) = content(i, t₂)" — [INV-IADDR-IMMUTABILITY]

This is the foundational Xanadu principle: bytes never die, addresses never change. The implementation honors it completely — there is no back door through error handling, cache pressure, or any other code path.

---

## Code Exploration

I now have everything I need. Here is my answer, with all claims grounded in the actual source code.

---

## Answer: I-Address Immutability in the Granfilade

**Short answer: No.** There is no code path — including `grimlyreap` — that can overwrite or remove a byte from its I-address slot. The granfilade is a strictly append-only, write-once store at the I-address level. Here is the full citation trail.

---

### 1. Insertion always moves forward — no I-address is ever reused

`inserttextgr` (`backend/granf2.c:83`):

```c
if (!findisatoinsertgr ((typecuc*)fullcrumptr, hintptr, &lsa))
    return (FALSE);
movetumbler (&lsa, &spanorigin);
for (; textset; textset = textset->next) {
    ...
    insertseq ((typecuc*)fullcrumptr, &lsa, &locinfo);
    tumblerincrement (&lsa, 0, textset->length, &lsa);  // line 100
}
```

`tumblerincrement` at line 100 advances `lsa` by `textset->length` after every segment. Since insertions always start from the **current high-water mark** (via `findisatoinsertgr`/`findpreviousisagr`) and always increment forward, no I-address is ever targeted twice.

---

### 2. `fillupcbcseq` appends — it never touches existing bytes

When a text crum has room, `insertseq` (`backend/insert.c:34-42`) tries to extend it in-place by calling `fillupcbcseq`:

```c
// insert.c:82-88
crumlength    = ptr->cinfo.granstuff.textstuff.textlength;
remainingroom = GRANTEXTLENGTH - crumlength;
textlength    = info->granstuff.textstuff.textlength;

if (remainingroom > textlength) {
    movmem(&info->granstuff.textstuff.textstring,
           (char*)(&(ptr->cinfo.granstuff.textstuff)) + crumlength,
           textlength);
    ptr->cinfo.granstuff.textstuff.textlength = crumlength + textlength;
```

The destination pointer is `+crumlength` bytes into the buffer — writing strictly **after** the existing bytes. Bytes at positions 0..crumlength-1 are never touched. The overflow path (lines 92-101) similarly writes at `+crumlength` up to `GRANTEXTLENGTH`, then renormalizes the *remaining* bytes in `info` (not in the crum). No overwrite of existing crum content occurs on either branch.

---

### 3. `grimlyreap` is a write-through cache flush, not destruction

When `falloc` fails, `ealloc` (`backend/credel.c:70-76`) calls `grimlyreap()`:

```c
if (grimreaper == NULL) {
    xgrabmorecore();
    continue;
}
grimlyreap();
```

`grimlyreap` (`credel.c:106-162`) iterates the circular `grimreaper` list looking for evictable crums:

```c
// credel.c:144-152
if (grimreaper->age == RESERVED) {
    continue;                    // skip — never evict reserved crums
}
if (isreapable (&eh, grimreaper)) {
    reap (grimreaper);
    ...
    break;
}
```

`reap` (`credel.c:292-330`) does one of two things:

- **Apex (orgl) crums** (line 309): `orglwrite((typecbc*)temp)` — serializes the orgl to disk via `orglwritepart2` (`corediskout.c:300`), then `orglfree` frees the in-core tree.
- **Non-apex crums** (line 329): `subtreewrite(temp)` — serializes the subtree to disk via `subtreewriterecurs` (`corediskout.c:426`), which for unmodified crums calls `loaffree(father)` (line 448) to release the in-memory copies.

The data is **written to disk before the memory is freed**. The I-address → data mapping survives in the disk representation. When the crum is needed again, `corediskin.c` reads it back.

---

### 4. RESERVED crums are immune to `grimlyreap`

`createorglgr` (`backend/granf2.c:111-128`) explicitly reserves every orgl it creates:

```c
// granf2.c:120-121
locinfo.granstuff.orglstuff.orglptr = createenf (POOM);
reserve ((typecorecrum*)locinfo.granstuff.orglstuff.orglptr);
```

`reserve` (`credel.c:364-379`) sets `ptr->age = RESERVED`. The `grimlyreap` loop (`credel.c:144`) hits a `continue` for any such crum. `freecrum` (`credel.c:434-453`) also hard-errors if called on a RESERVED crum. Orgls can only be freed via `orglfree` (`credel.c:470`), which requires a valid disk pointer first — ensuring the content is on disk before the in-core tree is released.

`isreapable` (`credel.c:164-289`) has additional guards that propagate this protection upward: if any child is RESERVED or in-core with an open orgl, the parent is not considered reapable (e.g., lines 198-207, 244-257).

---

### 5. No compaction or slot relabeling exists

`split.c` and `recombine.c` restructure the enfilade tree (adopting and disowning crums, adjusting `cwid.dsas[WIDTH]` widths), but they never move byte content from one I-address to another. The I-address namespace is preserved through all splits and recombinations — they only partition and rebalance the tree topology.

---

### Summary

| Path | Effect on I-address bytes |
|---|---|
| `fillupcbcseq` | Appends after existing bytes; never overwrites bytes 0..crumlength-1 |
| `grimlyreap` → `reap` → `subtreewrite`/`orglwrite` | Flushes to disk, frees in-core; data is preserved at original I-addresses on disk |
| `grimlyreap` + `RESERVED` crums | Skipped entirely (`continue` at `credel.c:144`) |
| `recombine` / `split` | Tree topology only; no I-address relabeling |
| `createorglgr` | Always calls `reserve` before inserting — immune to reaping |

Once a byte is stored at a given I-address in the granfilade, that byte is immutable at that address for the lifetime of the data store.

---

## Question 12 [gregory]

> When `findisatoinsertmolecule` allocates a fresh I-address by querying the granfilade for `max + 1`, can a DELETE that removed content from a POOM ever cause that max to decrease, leading to I-address reuse in a subsequent INSERT?

### Gregory's Answer

## KB Synthesis

No. DELETE cannot cause I-address reuse.

The allocation mechanism in `findisatoinsertmolecule` queries the **granfilade** for the current maximum I-address via `findpreviousisagr`, then increments by 1 [SS-ADDRESS-SPACE, Finding 0061]. The critical property is that DELETE never touches the granfilade.

[FC-GRANF-ON-DELETE] establishes this explicitly: DELETE modifies only the POOM (the document's V-to-I mapping via `deletevspanpm` → `deletend`). No delete path calls any granfilade insertion or deletion function. The granfilade is append-only — its entries are permanent.

Because the deleted I-addresses remain in the granfilade tree, `findpreviousisagr` will still find them as the maximum when the next INSERT runs. The max never decreases. [INV-MONOTONIC] (Finding 0061) states this directly: "deleted content's I-addresses remain in the granfilade tree and continue to influence allocation. Interleaved INSERT-DELETE-INSERT sequences produce contiguous, gap-free I-address sequences: INSERT 'AAA' allocates I.1–I.3, DELETE removes a character (V-space only), INSERT 'BBB' allocates I.4–I.6 (not reusing I.2)."

[INV-NO-IADDR-REUSE] summarizes the invariant: "Deleted I-addresses are never reused. Since the granfilade is never modified by DELETE, and allocation always queries the granfilade for the current maximum, 'gaps' in V-space created by DELETE do not create 'gaps' in I-space. The I-address space grows strictly monotonically and permanently."

So: the POOM may have gaps (V-positions removed), but the granfilade max is monotonically non-decreasing, and no subsequent INSERT can obtain an I-address that was previously allocated.

---

## Code Exploration

Now I have everything I need. Here is the definitive answer:

---

## I-Address Reuse via `findisatoinsertmolecule` — Definitive Analysis

### Short answer

**No.** A DELETE cannot cause the granfilade max to decrease, and therefore cannot cause I-address reuse via `findisatoinsertmolecule`. The granfilade is structurally append-only: no FEBE operation in the codebase ever calls `deleteseq` on the granfilade. The DELETE path operates exclusively on the POOM (V-space), never on the granfilade (I-space).

---

### 1. How `findisatoinsertmolecule` computes the new I-address

`granf2.c:158-181`:

```c
static int findisatoinsertmolecule(typecuc *fullcrumptr, typehint *hintptr, typeisa *isaptr)
{
  typeisa upperbound, lowerbound;

    tumblerincrement (&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound);
    clear (&lowerbound, sizeof(lowerbound));
    findpreviousisagr ((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);  // line 164
    if (tumblerlength (&hintptr->hintisa) == tumblerlength (&lowerbound)) {
        tumblerincrement (&lowerbound, 2, hintptr->atomtype, isaptr);
        tumblerincrement (isaptr, 1, 1, isaptr);  // "max + 1"
    } ...
```

`findpreviousisagr` (`granf2.c:255-278`) walks the granfilade tree, accumulating each node's `cwid.dsas[WIDTH]` (`granf2.c:275`) until it finds the rightmost leaf. At height 0 it calls `findlastisaincbcgr` (`granf2.c:264`) which adjusts for text atom length. The resulting `lowerbound` is the highest existing I-address; the new allocation is `lowerbound + 1`.

The "max" lives in the granfilade's node widths (`cwid.dsas[WIDTH]`), which are computed cumulatively up the tree by `setwidseq`.

---

### 2. The only function that can reduce a granfilade node's `cwid`

`edit.c:16-28` — comment says "use with GRAN":

```c
/* use with GRAN */
int deleteseq(typecuc *fullcrumptr, tumbler *address, INT index)
{
    context = retrievecrums (fullcrumptr, address, index);
    ptr = (typecbc *) context->corecrum;
    freecrum ((typecorecrum*)&context->corecrum);   // removes leaf from tree
    crumcontextfree(context);
    setwispupwards(findfather((typecorecrum*)ptr), 1);  // line 26 — recomputes cwid upward
    recombine(findfather((typecorecrum*)ptr));
}
```

`setwispupwards` (`wisp.c:83-111`) calls `setwisp` repeatedly. For GRAN nodes, `setwisp` dispatches to `setwidseq` (`wisp.c:127-128`):

```c
case GRAN:
    return (setwidseq ((typecuc*)ptr));
```

`setwidseq` (`wisp.c:150-168`) recomputes `cwid` as the **sum of living children** only:

```c
clear (&sum, sizeof (sum));
for (ptr = findleftson (father); ptr; ptr = getrightbro (ptr)){
    widopseq (&sum, &ptr->cwid, &sum);   // line 161 — sum only present children
}
...
movewisp (&sum, &father->cwid);          // line 165 — overwrites parent cwid
```

If a leaf had been freed, it is no longer in the child list, so its span is excluded from the sum — the parent's `cwid.dsas[WIDTH]` **would decrease**.

**But `deleteseq` is dead code.** A grep for `deleteseq` across the entire `backend/` directory returns exactly one hit: its own definition in `edit.c`. It is never called.

---

### 3. What DELETE actually does — the POOM path only

`do1.c:158-167`:

```c
bool dodeletevspan(typetask *taskptr, typeisa *docisaptr, typevspan *vspanptr)
{
    return (
       findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
    && deletevspanpm (taskptr, docisaptr, docorgl, vspanptr)
    );
}
```

`orglinks.c:145-152`:

```c
bool deletevspanpm(typetask *taskptr, tumbler *docisaptr, typeorgl docorgl, typevspan *vspanptr)
{
    if (iszerotumbler(&vspanptr->width))
        return (FALSE);
    deletend((typecuc*)docorgl, &vspanptr->stream, &vspanptr->width, V);  // line 149
    logbertmodified(docisaptr, user);
    return (TRUE);
}
```

`deletend` (`edit.c:31`) is labeled "use with SPAN and POOM". It operates on `docorgl` (a POOM enfilade, looked up from the granfilade at `findorgl`) in the **`V` dimension** (virtual address space). It calls `setwispupwards` (`edit.c:74`) and `recombine` (`edit.c:75`) on the POOM father — not on any granfilade node.

For POOM nodes, `setwisp` dispatches to `setwispnd` (`wisp.c:131`), not `setwidseq`. `setwispnd` (`wisp.c:171-228`) computes a bounding box over V-space children — it has nothing to do with the granfilade's I-space widths.

---

### 4. Structural separation: granfilade vs. POOM

The granfilade (`granf`, type `GRAN`) and the POOM (type `POOM`) are separate enfilade trees:

- The **granfilade** maps I-addresses → content atoms (text, orgls). Its `cwid.dsas[WIDTH]` encodes the cumulative I-address span. Only `inserttextgr` (`granf2.c:83`) and `createorglgr` (`granf2.c:111`) write to it — both via `insertseq` (`granf2.c:99`, `125`), which adds new leaves and calls `setwispupwards` upward, causing the `cwid` sum to **increase only**.
- The **POOM** maps V-addresses → I-spans (version content). `deletend` operates here with `V` dimension, reshaping V-space. The granfilade is read-only from DELETE's perspective — it is consulted only via `findorgl` to locate the POOM.

No FEBE operation ever calls `deleteseq` on the granfilade. No `freecrum` is ever called on a granfilade leaf in any delete path.

---

### 5. Conclusion

The granfilade's node widths (`cwid.dsas[WIDTH]`) are a running sum of allocated I-address spans and are **strictly non-decreasing**. The DELETE path (`dodeletevspan` → `deletevspanpm` → `deletend`) operates solely on the POOM in V-space and never touches the granfilade. `deleteseq`, the only function that could reduce a granfilade node's `cwid`, is dead code — it appears in `edit.c` but is never called from anywhere in the backend.

Therefore: `findisatoinsertmolecule` always finds a max that is at least as large as any previously allocated I-address. **I-address reuse via granfilade max decrease is not possible.**

---

## Question 13 [gregory]

> After DELETE removes a V→I mapping from a document's POOM, does `retrieveendsets` on a link referencing those I-addresses still return the full I-address spans, or does the spanfilade lookup itself degrade when no POOM references the I-addresses?

### Gregory's Answer

## KB Synthesis

The answer requires tracing two separate phases of `retrieveendsets`: the spanfilade lookup and the I→V conversion.

## Phase 1: Spanfilade lookup — does NOT degrade

The spanfilade is write-only [INV-SPANF-WRITE-ONLY]. DELETE removes V→I mappings from the POOM but **never touches the spanfilade** [ST-DELETE, Finding 0057]:

> `dodeletevspan` calls only `deletevspanpm` (granf) and `logbertmodified` — there is no call to any spanf function.

The link's endpoint I-addresses remain indexed in the spanfilade exactly as they were at link creation. `RETRIEVEENDSETS` searches the spanfilade via `retrievesporglsetinrange()` with SPANRANGE/ORGLRANGE restrictions [SS-RETRIEVE-ENDSETS], and this search succeeds — the spanfilade finds the matching I-address entries and returns them as a sporglset.

This is the INT-DELETE-SPANF-DIVERGENCE state: the index claims the document contains those I-addresses even though the POOM no longer maps them.

## Phase 2: I→V conversion — degrades silently

After the spanfilade returns the link's endpoint I-addresses as sporgls, `RETRIEVEENDSETS` calls `linksporglset2specset()` to convert back to V-addresses [SS-RETRIEVE-ENDSETS]. This path is:

```
linksporglset2specset → sporglset2vspanset → ispan2vspanset → permute → span2spanset → retrieverestricted
```

At `span2spanset()`, `retrieverestricted()` searches the **querying document's POOM** for the I-address. Since DELETE removed those I-address mappings from the POOM, `retrieverestricted()` returns NULL — and per [INV-ITOV-FILTERING]:

> unreferenced I-addresses are silently excluded from V-address results with no error

Each unresolvable I-address is dropped. The final result is empty or partial depending on how many of the link's endpoint I-addresses still have POOM mappings.

## Summary

| Layer | State after DELETE | Effect on RETRIEVEENDSETS |
|---|---|---|
| Spanfilade | Unchanged (I-addrs still indexed) | Lookup succeeds, returns sporglset |
| POOM | I→V mapping removed | I→V conversion silently drops unreferenced I-addrs |
| Result | — | Empty or partial V-span result; operation still returns success |

This is the same mechanism documented for FOLLOWLINK in [EC-GHOST-LINK]: the link structure is intact in permanent storage, the spanfilade search finds it, but endpoint resolution through the POOM produces empty spans. The distinction between "spanfilade found it" and "POOM resolved it" is what makes these "ghost links" — permanently existent and discoverable in the index, but resolving to nothing in V-space.

---

## Code Exploration

I have everything needed. Here is the complete answer.

---

## Answer

**Short answer:** The spanfilade lookup itself does not degrade. The degradation occurs one step later, in `linksporglset2specset`, which always attempts to convert the stored I-addresses back to V-spans via the POOM. When the POOM has no V-mappings for those I-addresses, the result is a `VSPECID` specset with a NULL `vspanset` — an empty version-space result. The raw I-address spans are not surfaced to the caller.

---

### The Call Chain

`retrieveendsets` [fns.c:350] → `doretrieveendsets` [do1.c:369] → `retrieveendsetsfromspanf` [spanf1.c:190].

Inside `retrieveendsetsfromspanf`, three sequential operations matter:

```c
specset2sporglset (taskptr, specset, &sporglset, NOBERTREQUIRED)
&& retrievesporglsetinrange(taskptr, sporglset, &fromspace, &fromsporglset)
&& linksporglset2specset (taskptr, &((typevspec *)specset)->docisa, fromsporglset, fromsetptr, NOBERTREQUIRED)
```
[spanf1.c:222–224]

---

### Step 1 — `specset2sporglset` [sporgl.c:14]

Converts the input specset (which identifies the link document) into a sporglset.

```c
if (((typeitemheader *)specset)->itemid == ISPANID) {
    *sporglsetptr = (typesporglset)specset;            // raw I-span: pass-through, no POOM
} else if (((typeitemheader *)specset)->itemid == VSPECID) {
    sporglsetptr = vspanset2sporglset(taskptr, &docisa, vspanset, sporglsetptr, type);
    // ↑ calls findorgl → vspanset2ispanset → POOM V→I lookup
}
```
[sporgl.c:20–28]

If the link is specified by I-address directly, the POOM is not touched here.

---

### Step 2 — `retrievesporglsetinrange` [spanf1.c:237]

Queries the **spanfilade** (not the granfilade/POOM) for the link's endpoint sporgls:

```c
context = retrieverestricted((typecuc*)spanf,
    (typespan*)sporglptr, SPANRANGE,
    whichspace, ORGLRANGE,
    (typeisa*)NULL /*kluge to make links show thru to versions*/);
```
[spanf1.c:245]

This is a pure spanfilade query. It searches for crums that match the link's I-address in `SPANRANGE` and `LINKFROMSPAN`/`LINKTOSPAN`/`LINKTHREESPAN` in `ORGLRANGE`. **The POOM is not consulted here.** The spanfilade itself is unchanged by `dodeletevspan` — it still holds the link's endpoint I-address data. This step succeeds.

---

### Step 3 — `linksporglset2specset` [sporgl.c:97] — where the degradation occurs

```c
if (iszerotumbler(&((typesporgl *)sporglset)->sporgladdress)) {
    // sporgladdress == 0: return raw I-span (ISPANID)
    ((typeitemheader *)specset)->itemid = ISPANID;
    movetumbler(&sporglset->sporglorigin, &((typeispan *)specset)->stream);
    movetumbler(&sporglset->sporglwidth,  &((typeispan *)specset)->width);
} else {
    // sporgladdress != 0: convert I→V through the POOM
    linksporglset2vspec(taskptr, homedoc, &sporglset, (typevspec*)specset, type);
}
```
[sporgl.c:105–117]

`sporgladdress` is set from `context->context2dinfo.homedoc` via `contextintosporgl` [sporgl.c:209], which gets its value from `linfo.homedoc` set during `insertspanf`. For document-referencing link endpoints, this is always the document ISA — non-zero. So the `else` branch is always taken for normal links, driving a POOM lookup.

---

### The POOM I→V Lookup After Deletion

`linksporglset2vspec` [sporgl.c:127] calls `sporglset2vspanset` [sporgl.c:141], which calls:

```c
vspansetptr = ispan2vspanset(taskptr, orgl, &ispan, vspansetptr);
```
[sporgl.c:157]

`ispan2vspanset` [orglinks.c:389] calls `permute(taskptr, orgl, ispanptr, I, vspansetptr, V)` [orglinks.c:404], which calls `span2spanset` [orglinks.c:425]:

```c
context = retrieverestricted((typecuc*)orgl, restrictionspanptr, restrictionindex, (typespan*)NULL, targindex, (typeisa*)NULL);
for (c = context; c; c = c->nextcontext) {
    context2span(c, ...);
    nextptr = (typespan *)onitemlist(taskptr, ...);
}
if (!context) {
    return(targspansetptr);   // ← no V-spans appended; return unchanged
}
```
[orglinks.c:435–448]

**After `dodeletevspan`**, `deletevspanpm` called `deletend((typecuc*)docorgl, &vspanptr->stream, &vspanptr->width, V)` [orglinks.c:149]. This removed the POOM crums at those V-positions. Since the crums are the shared 2D records encoding V↔I, their removal means those I-addresses no longer appear in any POOM traversal. `retrieverestricted` returns NULL context. `span2spanset` returns `targspansetptr` unmodified. `permute` returns `save` — the original, still-empty `vspansetptr`. Back in `linksporglset2vspec`:

```c
specptr->vspanset = NULL;
sporglset2vspanset(taskptr, homedoc, sporglsetptr, &specptr->vspanset, type);
// vspanset remains NULL
```
[sporgl.c:135–136]

---

### Conclusion

| Stage | What happens | POOM involved? |
|---|---|---|
| `retrievesporglsetinrange` [spanf1.c:237] | Spanfilade query succeeds; I-addresses of link endpoints retrieved correctly | No |
| `linksporglset2specset` [sporgl.c:97] | Branches on non-zero `sporgladdress` → calls POOM I→V lookup | **Yes** |
| `span2spanset` [orglinks.c:425] | `retrieverestricted` on POOM returns NULL (crums deleted); no V-spans appended | **Yes, fails silently** |

**The spanfilade does not degrade.** It correctly stores and returns the I-addresses of link endpoints regardless of POOM state. The degradation is entirely in the back-conversion: `linksporglset2specset` always attempts to resolve I-addresses to V-spans via the POOM, and when `deletend(V)` has removed the relevant crums, `span2spanset` silently returns no spans [orglinks.c:446-448]. The caller receives a `VSPECID` specset with `vspanset = NULL` — an empty version-space result — with a `TRUE` return code and no error. The raw I-address spans are never surfaced.

---

## Question 14 [gregory]

> When FOLLOWLINK resolves endset I-addresses back to V-addresses via `span2spanset`, what exactly happens at the I→V conversion step for an I-address that exists in the granfilade but appears in zero POOMs — is the filtering per-span or per-byte?

### Gregory's Answer

## KB Synthesis

The filtering is **per-span** (per sporgl / per I-span), not per-byte. Here's the precise mechanism:

**The conversion chain** [SS-FOLLOWLINK]:

`link2sporglset()` extracts I-address spans from the link orgl via `retrieverestricted()` against the link orgl itself (granfilade read, no POOM involved at this stage). This produces a sporglset — each sporgl carries `(origin: IAddress, width: TumblerWidth, source_doc: ISA)`.

`linksporglset2specset()` then calls `span2spanset()` per sporgl, which calls `retrieverestricted()` against the **queried document's POOM**. This is the filtering step.

**What happens at zero-POOM I-spans** [INV-ITOV-FILTERING]:

`retrieverestricted()` searches the document's POOM B-tree for crums whose I-address range overlaps the query span. If the I-address exists in the granfilade but no POOM in the queried document maps it, `retrieverestricted()` returns NULL. `span2spanset()` at `orglinks.c:446-448` detects this and silently skips the span — no V-span is added to the result.

**Granularity is per-sporgl, not per-byte:**

The sporgl represents a contiguous I-address range. The drop-or-keep decision operates on that entire range when `retrieverestricted()` returns NULL. However, if only *part* of an I-span has POOM mappings (e.g., the span covers I-addresses `a..a+10`, but the POOM only maps `a..a+3`), `retrieverestricted()` returns context entries for just the mapped sub-range — `incontextlistnd()` assembles those into V-spans [SS-CONTEXT-LIST]. So partial presence yields partial V-span results.

**Observable consequences** [EC-GHOST-LINK]:

- All I-spans unreferenced → empty result `[]`, operation succeeds (not an error)
- Some I-spans unreferenced → partial result, only live I-spans converted
- The call chain is identical for FOLLOWLINK and RETRIEVEENDSETS — both share `linksporglset2specset()` [SS-RETRIEVE-ENDSETS]

The granfilade is irrelevant to this filtering step. The granfilade stores the content bytes permanently [INV-IADDR-IMMUTABILITY]; whether those bytes are visible through any POOM is a separate question answered entirely by the POOM lookup.

---

## Code Exploration

I now have the complete picture. Here is the full answer.

---

## I→V Conversion in `span2spanset`: Per-Span or Per-Byte?

The I→V conversion that happens when FOLLOWLINK resolves endset I-addresses to V-addresses runs through two distinct filtering phases. For an I-address that exists in the granfilade but has **zero POOM crums** in the target document, the answer is: **the filtering is per-span (per-crum), and the entire I-span is dropped atomically** — the per-byte clipping phase is never reached.

---

### Full Call Chain

**`followlink` [fns.c:114-127]** → `dofollowlink`

```c
void followlink(typetask *taskptr)
{
  ...
  if (
     getfollowlink (taskptr, &linkisa, &whichend)
  && dofollowlink (taskptr, &linkisa, &specset, whichend)){
      putfollowlink (taskptr, specset);
```

**`dofollowlink` [do1.c:223-232]** is the pivot. It performs two steps:

```c
bool dofollowlink(typetask *taskptr, typeisa *linkisaptr, typespecset *specsetptr, INT whichend)
{
  typesporglset sporglset;
  bool link2sporglset(), linksporglset2specset();

    return (
       link2sporglset (taskptr, linkisaptr, &sporglset, whichend, NOBERTREQUIRED)
    && linksporglset2specset (taskptr, &((typesporgl *)sporglset)->sporgladdress,
                              sporglset, specsetptr, NOBERTREQUIRED));
}
```

**Step 1 — `link2sporglset` [sporgl.c:67-95]**: Looks up the link's own POOM by V-address (`whichend` maps to a V-address like `0.1.1` for FROM, `0.2.1` for TO). Calls `retrieverestricted((typecuc*)orgl, &vspan, V, NULL, I, NULL)` to extract I-spans from that POOM. These become sporgls — records of `(homedoc, ispan_origin, ispan_width)`.

**Step 2 — `linksporglset2specset` [sporgl.c:97-123]**: For each sporgl with a non-zero `sporgladdress`, calls `linksporglset2vspec` [sporgl.c:127] → `sporglset2vspanset` [sporgl.c:141] → `ispan2vspanset` [orglinks.c:389].

```c
// sporglset2vspanset [sporgl.c:150-157]
sporglptr = (typesporgl *)*sporglsetptr;
(void) findorgl (taskptr, granf, homedoc, &orgl, type);
ispan.itemid = ISPANID;
ispan.next = NULL;
movetumbler (&sporglptr->sporglorigin, &ispan.stream);
movetumbler (&sporglptr->sporglwidth, &ispan.width);
vspansetptr = ispan2vspanset (taskptr, orgl, &ispan, vspansetptr);
```

**`ispan2vspanset` [orglinks.c:389-393]**: Immediately delegates to `permute` with the I→V direction:

```c
typevspanset *ispan2vspanset(typetask *taskptr, typeorgl orgl, typeispan *ispanptr, typevspanset *vspansetptr)
{
    return permute(taskptr, orgl, ispanptr, I, vspansetptr, V);
}
```

**`permute` [orglinks.c:404-422]**: Iterates over each span in the input spanset and calls `span2spanset` once per span:

```c
for (; restrictionspanset; restrictionspanset = restrictionspanset->next) {
    targspansetptr = span2spanset(taskptr, orgl, restrictionspanset, restrictionindex, targspansetptr, targindex);
}
```

This is the **per-span loop**: each I-span is processed atomically as a unit.

---

### The Core I→V Lookup: `span2spanset` [orglinks.c:425-454]

```c
typespanset *span2spanset(typetask *taskptr, typeorgl orgl, typespanset restrictionspanptr,
                           INT restrictionindex, typespanset *targspansetptr, INT targindex)
{
  typecontext *context, *c, *retrieverestricted();
  typespan foundspan;
  typespan *nextptr;
  typeitem *onitemlist();

    context = retrieverestricted((typecuc*)orgl, restrictionspanptr, restrictionindex,
                                 (typespan*)NULL, targindex, (typeisa*)NULL);

    for (c = context; c; c = c->nextcontext) {
        context2span (c, restrictionspanptr, restrictionindex, &foundspan, targindex);
        nextptr = (typespan *)onitemlist (taskptr, (typeitem*)&foundspan, (typeitemset*)targspansetptr);
    }
    if(!context){
        return(targspansetptr);      // ← zero-POOM exit point
    }
    contextfree (context);
    return (&nextptr->next);
}
```

There are two phases here. The `if(!context)` guard at line 446 is the zero-POOM exit.

---

### Phase 1 — Per-Crum Filtering: `retrieverestricted` → `findcbcinarea2d` → `crumqualifies2d`

`retrieverestricted` [retrie.c:56-85] converts the I-span into `span1start`/`span1end` bounds:

```c
if (span1ptr) {
    movetumbler (&span1ptr->stream, &span1start);
    tumbleradd (&span1start, &span1ptr->width, &span1end);
} else {
    tumblerclear (&span1start);
    tumblerclear (&span1end);
}
```

Since `span2ptr = NULL` (no V-restriction), `span2start` and `span2end` are cleared to zero. Then it calls `retrieveinarea` [retrie.c:87] → `findcbcinarea2d` [retrie.c:229].

`findcbcinarea2d` [retrie.c:229-268] walks the POOM crum tree, calling `crumqualifies2d` on every crum:

```c
for (; crumptr; crumptr = getrightbro (crumptr)) {
    if (!crumqualifies2d (crumptr, offsetptr, span1start, span1end, index1,
                          span2start, span2end, index2, infoptr)){
        continue;
    }
    if (crumptr->height != 0) {
        dspadd (offsetptr, &crumptr->cdsp, &localoffset, (INT)crumptr->cenftype);
        findcbcinarea2d (findleftson((typecuc*)crumptr), &localoffset, ...);
    } else {
        context = makecontextfromcbc ((typecbc*)crumptr, (typewid*)offsetptr);
        incontextlistnd (headptr, context, index1);
    }
}
```

`crumqualifies2d` [retrie.c:270-305] performs span-level intersection for both I and V dimensions using `whereoncrum`. For the I-dimension:

```c
endcmp = iszerotumbler (span1end) ? TOMYRIGHT : whereoncrum (crumptr, offset, span1end, index1);
if (endcmp <= ONMYLEFTBORDER){
    return(FALSE);   // query ends before or at crum's left edge
}
startcmp = whereoncrum (crumptr, offset, span1start, index1);
if (startcmp > THRUME){
    return (FALSE);  // query starts at or after crum's right edge
}
```

`whereoncrum` [retrie.c:345-398] for a POOM crum computes:

```c
tumbleradd(&offset->dsas[index], &ptr->cdsp.dsas[index], &left);
tumbleradd (&left, &ptr->cwid.dsas[index], &right);
// then returns TOMYLEFT / ONMYLEFTBORDER / THRUME / ONMYRIGHTBORDER / TOMYRIGHT
```

The qualification test is: **does the crum's I-address range `[left, right)` overlap the query `[span1start, span1end)`?** This is a span-level test — a single arithmetic comparison per crum edge. There is no iteration over individual bytes.

For the V-dimension: since `span2end` is zero, `iszerotumbler(span2end)` is true at line 292, so `endcmp = TOMYRIGHT`, which means the V constraint is unbounded — any V-address is acceptable. The sole filter is the I-address range.

**If no POOM crums cover the I-address**, `findcbcinarea2d` returns without adding anything to the context list. `retrieverestricted` returns `NULL`. `span2spanset` hits:

```c
if(!context){
    return(targspansetptr);   // orglinks.c:446-448
}
```

The I-span is **dropped as a whole**. The output `vspanset` is unchanged.

---

### Phase 2 — Per-Byte Clipping: `context2span` [context.c:176-212]

This phase only runs for **qualifying crums**. For each context returned by `retrieverestricted`, `span2spanset` calls:

```c
context2span (c, restrictionspanptr, restrictionindex, &foundspan, targindex);
```

`context2span` [context.c:176-212] clips the crum's V-span to exactly match the I-address intersection:

```c
movetumbler (&restrictionspanptr->stream, &lowerbound);
tumbleradd (&lowerbound, &restrictionspanptr->width, &upperbound);
prologuecontextnd (context, &grasp, &reach);

if (tumblercmp (&grasp.dsas[idx1], &lowerbound) == LESS) {
    // crum starts before the I-restriction: advance V-start by the overshoot
    tumblerincrement (&grasp.dsas[idx2], 0,
                      (INT) tumblerintdiff(&lowerbound, &grasp.dsas[idx1]),
                      &grasp.dsas[idx2]);
}
if (tumblercmp (&reach.dsas[idx1], &upperbound) == GREATER) {
    // crum ends after the I-restriction: shrink V-end by the overshoot
    tumblerincrement (&reach.dsas[idx2], 0,
                      -tumblerintdiff (&reach.dsas[idx1], &upperbound),
                      &reach.dsas[idx2]);
}
movetumbler (&grasp.dsas[idx2], &foundspanptr->stream);
tumblersub(&reach.dsas[idx2], &grasp.dsas[idx2], &foundspanptr->width);
```

This is **per-byte**: the offset arithmetic with `tumblerintdiff` computes exact byte counts. If the query I-span `[15, 25)` partially overlaps a crum covering `[10, 30)` in I-space and `[100, 120)` in V-space, `context2span` outputs V-span `[105, 115)` — shifted by 5 bytes at start, trimmed by 5 bytes at end.

This phase is never reached in the zero-POOM case.

---

### Summary

| Phase | Where | Granularity | Zero-POOM behavior |
|-------|-------|-------------|-------------------|
| Crum qualification | `crumqualifies2d` [retrie.c:270] | Per-crum (span-level) | No crums qualify → NULL context |
| Output clipping | `context2span` [context.c:176] | Per-byte (exact arithmetic) | Never reached |
| Zero-crum exit | `span2spanset` [orglinks.c:446] | Per-span (whole I-span dropped) | Returns unchanged target set |

**The filtering is per-span.** When an I-address exists in the granfilade but appears in zero POOMs for the queried document, `findcbcinarea2d` finds no qualifying crums, `retrieverestricted` returns `NULL`, and `span2spanset` drops the entire I-span in one shot at the `if(!context)` guard [orglinks.c:446]. The per-byte clipping in `context2span` is only invoked for POOM crums that actually contain the I-address; with zero such crums, it never runs. No partial result, no error — the I-span simply produces no V-addresses.

---

## Question 15 [gregory]

> If a deeply orphaned link's endpoint I-addresses are transcluded into a brand-new document years later, does `find_links` rediscover the link immediately, or does the stale DOCISPAN entry for the original (now-deleted) document interfere with the lookup?

### Gregory's Answer

## KB Synthesis

Yes — `find_links` rediscovers the link immediately, and stale DOCISPAN entries do not interfere. Here is the full chain of reasoning:

---

**Why the link is rediscovered**

When the link was created, `insertendsetsinspanf` permanently indexed α₁..αₙ → link_ISA in the spanfilade's **link endset sub-index** [ST-CREATE-LINK, SS-SPANF-OPERATIONS]. Because the spanfilade is write-only and append-only, these entries survive forever regardless of what happens to the documents referencing those I-addresses [INV-SPANF-WRITE-ONLY].

When D_new transcludes the content via COPY, `insertpm` gives D_new's POOM V→I mappings for α₁..αₙ [ST-VCOPY]. Now `find_links` on D_new works as follows:

1. The search specset is converted to I-addresses via D_new's POOM → yields α₁..αₙ [SS-FIND-LINKS].
2. The spanfilade link endset index is queried for those I-addresses [SS-SPANF-OPERATIONS].
3. The link endset entries α₁..αₙ → link_ISA were never removed → intersection succeeds → link returned.
4. FOLLOWLINK succeeds because D_new's POOM now provides V-position resolution for α₁..αₙ [SS-FOLLOWLINK, INV-ITOV-FILTERING].

This is exactly the mechanism documented in [INT-LINK-TRANSCLUSION]: transclusion enables link discovery by sharing I-addresses, with no special "link recovery" logic required.

---

**Why stale DOCISPAN entries don't interfere**

The spanfilade has two independent sub-indices [FC-CONTENT-SPANF-ISOLATION, SS-DOCISPAN]:

- **Link endset index** (written by `insertendsetsinspanf` at link creation): maps I-addresses → link ISAs. This is what `find_links` / `findlinksfromtothreesp` queries.
- **DOCISPAN index** (written by `insertspanf(..., DOCISPAN)` at INSERT/COPY): maps I-addresses → document ISAs. This is what `FINDDOCSCONTAINING` queries.

`find_links` never touches the DOCISPAN portion [SS-GRANF-OPERATIONS, SS-SPANF-OPERATIONS]. Stale DOCISPAN entries from the original (now-empty) document are only relevant to `FINDDOCSCONTAINING` queries, where they cause the "superset" behavior documented in [EC-STALE-SPANF-REFERENCE] — they would spuriously include the old document in those results, but that is completely orthogonal to link discovery.

---

**One relevant quirk**

From [EC-FIND-LINKS-GLOBAL] (Finding 0069), the orgl-range parameter to `find_links` is effectively disabled — searches are global in the orgl dimension. This is actually favorable here: the link endset entries exist in the global orgl space regardless of which document the link was originally created in, so the disabled filter cannot accidentally exclude the result.

---

## Code Exploration

I now have everything I need for a complete, code-grounded answer.

---

## Answer: Does `find_links` Rediscover an Orphaned Link After Retransclusion?

**Yes — `find_links` rediscovers the link immediately. The stale DOCISPAN entry for the deleted document does not interfere at all.** Here is the complete mechanistic explanation.

---

### How Links Are Indexed at Creation Time

When `docreatelink` [do1.c:195–221] is called, it fires `insertendsetsinspanf` [do2.c:116–128]:

```c
bool insertendsetsinspanf(typetask *taskptr, typespanf spanfptr, typeisa *linkisaptr,
    typesporglset fromsporglset, typesporglset tosporglset, typesporglset threesporglset)
{
    insertspanf(taskptr, spanfptr, linkisaptr, fromsporglset, LINKFROMSPAN)
    && insertspanf(taskptr, spanfptr, linkisaptr, tosporglset, LINKTOSPAN)
    ...
}
```

`insertspanf` [spanf1.c:15–54] performs a 2D insert into the spanfilade. The two dimensions of each stored crum are:

- **ORGLRANGE dimension**: the link ISA, prefixed with the span-type tag (e.g. `LINKFROMSPAN` = 1).  
  `prefixtumbler(isaptr, spantype, &crumorigin.dsas[ORGLRANGE]);` [spanf1.c:22]

- **SPANRANGE dimension**: the **raw I-address** of the endpoint content.  
  For a `SPORGLID` (content specified as a document + V-span), the I-address is in `sporglorigin`:  
  `movetumbler(&((typesporgl*)sporglset)->sporglorigin, &lstream);` [spanf1.c:31–32]  
  For an `ISPANID`, the I-address is the stream field directly. [spanf1.c:27–28]

The V→I conversion (for `VSPECID` endpoint specs) happens in `vspanset2sporglset` [sporgl.c:35–65], which calls `vspanset2ispanset` [orglinks.c:397–402] via `permute` to get the absolute I-address at creation time. **Only the I-address is stored in the spanfilade.** The source document ISA is held in `sporgladdress`, but as we will see, it is never used as a filter during lookup.

---

### How `find_links` Searches

The call chain for a `find_links` query:

```
dofindlinksfromtothree       [do1.c:348–353]
  → findlinksfromtothreesp   [spanf1.c:56–103]
    → specset2sporglset       [sporgl.c:14–33]  (convert query specs to sporgls)
    → sporglset2linkset       [sporgl.c:222–237]
      → sporglset2linksetinrange [sporgl.c:239–269]
```

The critical function is `sporglset2linksetinrange` [sporgl.c:239–269]:

```c
int sporglset2linksetinrange(typetask *taskptr, typecuc *spanfptr, typesporglset sporglset,
    typelinkset *linksetptr, typeispan *orglrange, INT spantype)
{
    infoptr = &linfo;
    for (; sporglset; sporglset = ...) {
        if (FALSE/*trying to kluge links followable thru versions */
            && ((typeitemheader *)sporglset)->itemid == SPORGLID) {
            infoptr = &linfo;
            movetumbler(&((typesporgl *)sporglset)->sporgladdress, &linfo.homedoc);
        } else
            infoptr = NULL;   // <-- ALWAYS executes
        ...
        context = retrieverestricted(spanfptr, (typespan*)sporglset, SPANRANGE,
                                     &range, ORGLRANGE, (typeisa*)infoptr);
        ...
    }
}
```

The guard `FALSE && ...` at [sporgl.c:251] ensures `infoptr = NULL` on **every single call** — unconditionally. The developer comment is explicit: *"trying to kluge links followable thru versions"*. This was an intentional design decision to make link discovery document-independent.

With `infoptr = NULL`, `retrieverestricted` performs a pure 2D range scan:
- **Query key (SPANRANGE)**: the I-address extracted from the query sporgl (from the new document's content, via V→I conversion).
- **Result key (ORGLRANGE)**: the link ISAs stored at that I-address.

There is **no filtering by source document** anywhere in this path.

---

### What DOCISPAN Entries Are and Why They Don't Matter

DOCISPAN entries are written by `docopy` [do1.c:62] and `docopyinternal` [do1.c:79] every time content is transcluded into a document:

```c
insertspanf(taskptr, spanf, docisaptr, ispanset, DOCISPAN)  // do1.c:62
```

This inserts a crum with:
- ORGLRANGE: `DOCISPAN.documentISA`
- SPANRANGE: I-address of the transcluded content

The purpose is to answer the question: "given an I-span, which documents currently contain it?" The **only** function that reads DOCISPAN entries is `finddocscontainingsp` [spanf1.c:151–188]:

```c
tumblerincrement(&docspace.stream, 0, DOCISPAN, &docspace.stream);  // spanf1.c:168
...
context = retrieverestricted((typecuc*)spanf, &docspace, ORGLRANGE, ispanset, SPANRANGE, ...);
```

`finddocscontainingsp` is a completely separate operation. It is **never called** from `findlinksfromtothreesp` or anywhere in the link-finding call chain. The two queries live in orthogonal tag-prefixed regions of the ORGLRANGE dimension (DOCISPAN=4 vs. LINKFROMSPAN=1/LINKTOSPAN=2/LINKTHREESPAN=3) and never overlap.

---

### The Scenario, Step by Step

1. **Original link created**: `docreatelink` stores in the spanfilade — SPANRANGE = I-address X, ORGLRANGE = `LINKFROMSPAN.linkISA`. [do1.c:219, spanf1.c:22,49–51]

2. **Original document deleted**: The DOCISPAN entry "I-address X is in document A" remains in the spanfilade. The granfilade orgl for document A may be gone or inaccessible. The LINKFROMSPAN entry for I-address X is **untouched** — there is no garbage-collection step.

3. **Content at I-address X transcluded into new document B**: `docopy` [do1.c:45–65] calls `insertspanf(..., DOCISPAN)` [do1.c:62], writing a new DOCISPAN crum: "I-address X is in document B." The old DOCISPAN entry for document A also remains, but in a different ORGLRANGE slot.

4. **Client calls `find_links` with a VSPECID spec for document B**: `specset2sporglset` [sporgl.c:14–33] calls `vspanset2sporglset` [sporgl.c:35–65], which opens document B's enfilade via `findorgl`, calls `vspanset2ispanset` [orglinks.c:397–402] to map the V-address in B → I-address X, and produces a sporgl with `sporglorigin = X`.

5. **`sporglset2linksetinrange` runs**: `infoptr = NULL` (the `FALSE&&` guard fires) [sporgl.c:254–255]. `retrieverestricted` searches SPANRANGE for I-address X, filtered to ORGLRANGE in the LINKFROMSPAN region. It finds the original link's crum. `beheadtumbler` extracts the link ISA. [sporgl.c:263–265]

6. **Link returned to client.** The stale DOCISPAN entry for document A was never consulted.

---

### Architectural Summary

The spanfilade serves as two independent indexes sharing one data structure, distinguished by the tag prefix in the ORGLRANGE dimension:

| Tag (ORGLRANGE prefix) | Written by | Read by | Meaning |
|---|---|---|---|
| LINKFROMSPAN (1) | `insertendsetsinspanf` | `sporglset2linksetinrange` | I-addr → link ISA (from-end) |
| LINKTOSPAN (2) | `insertendsetsinspanf` | `sporglset2linksetinrange` | I-addr → link ISA (to-end) |
| LINKTHREESPAN (3) | `insertendsetsinspanf` | `sporglset2linksetinrange` | I-addr → link ISA (3-end) |
| DOCISPAN (4) | `docopy` / `docopyinternal` | `finddocscontainingsp` | I-addr → containing document ISA |

These two indexes never cross. Link finding reads only tags 1–3. DOCISPAN entries (stale or fresh) are invisible to it.

The `FALSE&&` at [sporgl.c:251] is the definitive proof that link discovery is intentionally document-blind. The system designers understood that tying link discovery to document membership would break link persistence across versions and transclusions — so they hard-coded the document filter off.

**Conclusion**: The link is rediscovered immediately and completely. The stale DOCISPAN entry for the deleted document sits in a different part of the spanfilade index and is structurally unreachable from the link-finding path. Transclusion's I-address preservation is the mechanism that makes this work: since I-addresses are permanent content identifiers, the LINKFROMSPAN index entry written at link-creation time remains valid and findable as long as any document anywhere contains that content.

---

## Question 16 [gregory]

> Does CREATENEWVERSION produce a version whose POOM entries point to the exact same I-address values as the source, or does `docopyinternal` allocate any fresh I-addresses during the copy — even for metadata or structural bookkeeping?

### Gregory's Answer

## KB Synthesis

The version's POOM entries point to the **exact same I-address values** as the source. `docopyinternal` allocates no fresh I-addresses.

The call chain is: `docreatenewversion` → `doretrievedocvspanfoo` → `docopyinternal` → `specset2ispanset` → `insertpm` + `insertspanf`. The `specset2ispanset` step converts the source's V-spans to their existing I-spans by looking them up in the source's POOM. These I-spans are then passed directly to `insertpm` (to build the version's POOM mappings) and `insertspanf` (to register DOCISPAN entries). Neither call allocates; they record pre-existing I-addresses. [ST-VERSION]

The only allocation in the entire operation is the new document address itself — `createorglingranf` calls `findisatoinsertnonmolecule`, which assigns a child address under the source document. This is a document address, not a content I-address, and it lives in a separate tumbler range that does not affect the content allocation counter. [ST-VERSION-CREATE, SS-ADDRESS-ALLOC]

The KB directly confirms the consequence: inserting text after VERSION produces contiguous I-addresses with any text previously in the source, because the content allocation counter was untouched. Contrast this with CREATELINK, which does call `createorglingranf` for the link orgl (a content-type allocation), breaking subsequent text I-address contiguity. [INV-MONOTONIC]

So: `ispans(version) = ispans(source)` at creation time — a strict equality, not a copy. [ST-VERSION-CREATE]

---

## Code Exploration

I now have a complete picture of the entire call chain. Here is the full analysis.

---

## Does `docopyinternal` allocate fresh I-addresses?

**No. Zero new I-addresses are allocated.** The new version's POOM crums point to the exact same permascroll I-address values as the source document's POOM crums. Here is the code proof, step by step.

---

### Step 1 — `docreatenewversion` sets up the copy [do1.c:260-299]

```c
bool docreatenewversion(typetask *taskptr, typeisa *isaptr, typeisa *wheretoputit, typeisa *newisaptr)
{
  typevspan vspan;
  typevspec vspec;

  createorglingranf(taskptr, granf, &hint, newisaptr);        // [do1.c:277]
  doretrievedocvspanfoo(taskptr, isaptr, &vspan);             // [do1.c:281]

  vspec.docisa = *isaptr;     // source document ISA          // [do1.c:287]
  vspec.vspanset = &vspan;    // source V-span                // [do1.c:288]

  docopyinternal(taskptr, newisaptr, &vspan.stream, &vspec);  // [do1.c:293]
```

`createorglingranf` allocates a new document-ISA tumbler (a document address, not a permascroll content address). `vspan.stream` is the source document's V-space start position, read from the POOM root [do1.c:281].

---

### Step 2 — `doretrievedocvspanfoo` reads the source V-span [orglinks.c:155-162]

```c
bool retrievedocumentpartofvspanpm(typetask *taskptr, typeorgl orgl, typevspan *vspanptr)
{
    vspanptr->stream = ((typecuc *)orgl)->cdsp.dsas[V];   // POOM root displacement
    vspanptr->width  = ((typecuc *)orgl)->cwid.dsas[V];   // POOM root width
    return TRUE;
}
```

Pure read. No allocation. `vspan.stream` is the V-space start of the source document (e.g., `1.1`).

---

### Step 3 — `docopyinternal` [do1.c:66-82]

```c
bool docopyinternal(typetask *taskptr, typeisa *docisaptr, tumbler *vsaptr, typespecset specset)
{
    specset2ispanset(taskptr, specset, &ispanset, NOBERTREQUIRED);   // V→I lookup
    insertpm(taskptr, docisaptr, docorgl, vsaptr, ispanset);          // POOM write
    insertspanf(taskptr, spanf, docisaptr, ispanset, DOCISPAN);       // spanf index
```

Three calls. None of them allocate I-addresses.

---

### Step 4 — `specset2ispanset` performs a pure read [do2.c:14-46]

```c
bool specset2ispanset(typetask *taskptr, typespec *specset, typeispanset *ispansetptr, int type)
{
    for (; specset; ...) {
        if (itemid == VSPECID) {
            findorgl(taskptr, granf, &vspec->docisa, &docorgl, type);       // open source POOM
            vspanset2ispanset(taskptr, docorgl, vspec->vspanset, ispansetptr);  // V→I
        }
    }
}
```

For the `vspec` built in `docreatenewversion`, `docisa = *isaptr` (source document) and `vspanset = &vspan` (source V-span). This looks up the source document's POOM.

---

### Step 5 — `vspanset2ispanset` → `permute` reads source POOM crums [orglinks.c:397-422]

```c
typeispanset *vspanset2ispanset(typetask *taskptr, typeorgl orgl,
    typevspanset vspanptr, typeispanset *ispansetptr)
{
    return permute(taskptr, orgl, vspanptr, V, ispansetptr, I);
}
```

`permute` calls `span2spanset` → `retrieverestricted` → `retrieveinarea` → `findcbcinarea2d` [retrie.c:87-110]. This traverses the source document's existing POOM tree, collecting bottom crums whose V-dimension intersects the query. Then `context2span` extracts the I-dimension values from those crums.

**This is a pure read.** No new content is written to the granfilade. The returned `typeispanset` contains `typeispan` items (itemid = `ISPANID`) holding the exact I-addresses already stored in the source POOM crums.

---

### Step 6 — `insertpm` writes those exact I-addresses into the new POOM [orglinks.c:75-134]

```c
bool insertpm(typetask *taskptr, tumbler *orglisa, typeorgl orgl,
              tumbler *vsaptr, typesporglset sporglset)
{
    for (; sporglset; sporglset = sporglset->next) {
        unpacksporgl(sporglset, &lstream, &lwidth, &linfo);       // extract I-address

        movetumbler(&lstream, &crumorigin.dsas[I]);               // I = verbatim
        movetumbler(vsaptr,   &crumorigin.dsas[V]);               // V = source V-start

        insertnd(taskptr, orgl, &crumorigin, &crumwidth, &linfo, V);

        tumbleradd(vsaptr, &crumwidth.dsas[V], vsaptr);           // advance V-pointer
    }
}
```

And `unpacksporgl` for `ISPANID` items [sporgl.c:178-203]:

```c
if (itemid == ISPANID) {
    movetumbler(&ispanptr->stream, streamptr);   // lstream = source I-address, verbatim
    movetumbler(&ispanptr->width,  widthptr);    // lwidth  = source I-width, verbatim
    tumblerclear(&infoptr->homedoc);             // homedoc = 0 (not carried over)
}
```

The I-address (`lstream`) placed into `crumorigin.dsas[I]` is the **verbatim permascroll address** read from the source POOM. No arithmetic transforms it. No allocation creates a fresh one.

---

### What IS allocated during `docreatenewversion`

| Allocation | Type | Function | Notes |
|---|---|---|---|
| New document ISA (tumbler) | Document address | `createorglingranf` [do1.c:277] | Not an I-address; document identity only |
| New POOM crums | Tree nodes | `insertnd` → `insertcbcnd` → `createcrum` [insertnd.c:260] | POOM structure, not content |
| New spanfilade entries | Index records | `insertspanf` | Link index, same I-addresses |
| Task-local `ispanset` etc. | Transient | `taskalloc` | Freed with task |

---

### Summary

`docreatenewversion` produces a version whose POOM entries carry **the exact same I-address values** as the source. The mechanism is:

1. `doretrievedocvspanfoo` reads the source V-span from the POOM root [orglinks.c:157-160]
2. `specset2ispanset` → `permute` → `retrieverestricted` reads the source POOM crums, extracting their I-dimension values [do2.c:36, orglinks.c:397-422]
3. `insertpm` places those values verbatim into `crumorigin.dsas[I]` of the new POOM crums [orglinks.c:105,130]

`docopyinternal` never calls `inserttextingranf` (the only function that allocates permascroll I-addresses). No I-space allocation occurs, not even for metadata or structural bookkeeping. The permascroll content is shared by reference across both document versions — this is the fundamental transclusional identity mechanism of udanax-green.

---

## Question 17 [gregory]

> When `isanextensionnd` silently merges a COPY's I-span into an adjacent existing POOM entry, does the merged entry preserve the exact original I-address range boundaries, or does the extension alter the stored I-displacement or I-width of the pre-existing crum?

### Gregory's Answer

## KB Synthesis

When `isanextensionnd` triggers a merge, **only the width fields change — the original I-displacement (origin) is preserved exactly**.

The check in `isanextensionnd` (`insertnd.c:293-301`) verifies that the new content's origin equals the existing crum's reach in *both* V and I dimensions simultaneously. This means:

- Existing crum covers I-space: `[origin.dsas[I], origin.dsas[I] + width.dsas[I])`
- New content starts at: `origin.dsas[I] + width.dsas[I]` (the exact reach)
- After extension: crum covers `[origin.dsas[I], origin.dsas[I] + width.dsas[I] + new_width.dsas[I])`

The `insertnd.c:243` path — "Width extension: existing crum grows in place" — modifies only the crum's `width.dsas[I]` and `width.dsas[V]` fields. The `origin.dsas[I]` and `origin.dsas[V]` fields are untouched.

So the pre-existing crum's lower boundary is invariant. The extension is strictly rightward: the crum's stored I-displacement stays fixed at the original starting I-address, while the I-width grows to absorb the new content.

This is consistent with [ST-VCOPY] (Finding 0046):

> "If both hold, the existing crum's width is extended in place (`insertnd.c:243`). Otherwise, a new crum is created (`insertnd.c:252-260`). This means repeated COPYs of the same I-addresses produce either extended crums or separate crums depending on contiguity, **never duplicated entries within a single crum**."

And with [SS-POOM-BOTTOM-CRUM] (Finding 0076), which defines the crum structure as having independent `origin` and `width` tubblers per dimension — the extension operation writes only to the width slot.

One caveat from [SS-INSERT-VWIDTH-ENCODING] (Finding 0076): the V-width tumbler is re-encoded at V-address precision (not a direct copy of the I-width tumbler), but the numeric value they encode remains equal per [INV-WIDTH-VALUE-EQUIVALENCE]. So the extension correctly increments both width fields while preserving the invariant that `value(V-width) == value(I-width)`.

---

## Code Exploration

I now have all the code I need. Let me trace the complete execution path.

---

## Answer

**Short answer:** `isanextensionnd` preserves the pre-existing crum's I-displacement (`cdsp.dsas[I]`) exactly — the lower I-boundary is never touched. Only the I-width (`cwid.dsas[I]`) is increased. The upper I-boundary shifts outward to absorb the appended span; the lower boundary does not move.

---

## Full Trace

### Step 1 — Extension gate: `isanextensionnd` (`insertnd.c:301-309`)

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

Two conditions must both be true:
1. **Home document match** — the new span's `homedoc` tumbler equals the existing crum's `c2dinfo.homedoc`. `[insertnd.c:305]`
2. **Exact adjacency in both dimensions** — `lockeq` at `[insertnd.c:308]` iterates over `dspsize(POOM) = 2` tumblers (`wisp.h:26-27`: `DSPSIZEPM 2`), checking both I (`dsas[0]`) and V (`dsas[1]`) simultaneously. `reach` must equal `originptr` in both dimensions.

### Step 2 — How `reach` is computed: `prologuend` (`retrie.c:334-339`)

```c
int prologuend(typecorecrum *ptr, typedsp *offset, typedsp *grasp, typedsp *reach)
{
    dspadd (offset, &ptr->cdsp, grasp, (INT)ptr->cenftype);   // grasp = offset + ptr->cdsp
    if (reach)
        dspadd (grasp, &ptr->cwid, reach, (INT)ptr->cenftype); // reach = grasp + ptr->cwid
}
```

`dspadd` at `wisp.c:15-18` calls `lockadd`, which iterates over both dimensions. So:
- `grasp.dsas[I] = offset.dsas[I] + ptr->cdsp.dsas[I]`  — absolute I-start
- `reach.dsas[I] = grasp.dsas[I] + ptr->cwid.dsas[I]`  — absolute I-end (exclusive)

The adjacency check at `[insertnd.c:308]` passes only when `reach.dsas[I] == originptr->dsas[I]`, i.e. the new span begins exactly at the existing crum's I-end.

### Step 3 — The merge: `insertcbcnd` (`insertnd.c:250-257`)

```c
if (isanextensionnd ((typecbc*)ptr, grasp, origin, infoptr)) {
    dspadd (&ptr->cwid, width, &ptr->cwid, (INT)father->cenftype);  // [insertnd.c:251]
    ivemodified (ptr);
    setwispupwards (father,1);
    ...
    return(FALSE);
}
```

`dspadd` at `[insertnd.c:251]` expands to (`wisp.c:15-18`):

```c
lockadd(ptr->cwid.dsas, width->dsas, ptr->cwid.dsas, 2 /*DSPSIZEPM*/);
```

which executes two `tumbleradd` calls (`wisp.c:272`):
```
ptr->cwid.dsas[I] += width->dsas[I]   // I-width grows
ptr->cwid.dsas[V] += width->dsas[V]   // V-width grows
```

**`ptr->cdsp` is never touched.** There is no `dspsub`, no `movewisp`, no assignment to `ptr->cdsp.dsas[I]` anywhere in this merge path.

### Step 4 — Struct layout confirms the fields are independent

From `enf.h:127-128` (the `type2dcbc` bottom crum):
```c
typewid cwid;   // width in I and V
typedsp cdsp;   // displacement (origin offset) in I and V
```

`typewid` and `typedsp` are both `struct { tumbler dsas[2]; }` (`wisp.h:50-52`). They are separate fields. The merge at `[insertnd.c:251]` writes only to `cwid`.

---

## Conclusion

When `isanextensionnd` determines that the incoming COPY's I-span is exactly adjacent to an existing POOM bottom crum, the merge at `insertcbcnd:251` performs **only**:

```
ptr->cwid.dsas[I]  +=  width->dsas[I]     // upper I-boundary extends
ptr->cwid.dsas[V]  +=  width->dsas[V]     // upper V-boundary extends
```

The stored I-displacement `ptr->cdsp.dsas[I]` — which encodes the lower I-address boundary — is **not modified at all**. The pre-existing crum's lower I-boundary is preserved exactly as stored. Only the I-width grows to absorb the appended span, shifting the upper boundary outward by exactly `width->dsas[I]`.

---

## Question 18 [gregory]

> For content stored via APPEND (which skips `insertspanf`), the I-address is permanent in the granfilade but has no DOCISPAN entry — can `find_links` ever discover a link whose endset references APPEND-created I-addresses, given that the spanfilade search is the only discovery path?

### Gregory's Answer

## KB Synthesis

Yes — **`find_links` can discover a link whose endset references APPEND-created I-addresses**. The DOCISPAN omission by APPEND is irrelevant to link discovery. Here's why.

## The Two Spanfilade Sub-Indices Are Independent

The KB makes a critical distinction [FC-CONTENT-SPANF-ISOLATION]:

> The spec must model spanf as having two independent sub-indices: `SpanEnfilade = { link_index: Map<IAddress, Set<LinkISA>>, docispan: Map<IAddress, Set<DocISA>> }`

APPEND skips `insertspanf(..., DOCISPAN)` [EC-APPEND-NO-DOCISPAN]. This makes content invisible to `find_documents`. But `find_links` searches the **link endset index**, not DOCISPAN. These are orthogonal.

## Link Creation Populates the Link Endset Index

When a link is created over content — regardless of whether that content arrived via INSERT or APPEND — `docreatelink` calls `insertendsetsinspanf()` [ST-CREATE-LINK]:

> Link creation is a compound state transition that updates both enfilades atomically: (1) create a link orgl in `granf`; (2) copy the link's ISA reference into the document's link subspace; (3) **index all link endpoints in `spanf` via `insertendsetsinspanf()`**.

The endpoint I-addresses are indexed in the link endset sub-index at link creation time. How those I-addresses were originally allocated (INSERT vs APPEND) is irrelevant — they're now in the spanfilade link index.

## The `find_links` Search Path Bypasses DOCISPAN

`find_links` converts the query V-span to I-addresses via the POOM, then searches the spanfilade **link endset** [SS-FIND-LINKS, INT-SPORGL-LINK-INDEX]:

> `find_links(S) = { L | I-addresses(S) ∩ I-addresses(L.source) ≠ ∅ }`

The V→I conversion uses the document's POOM (granfilade), not the DOCISPAN index. As long as the APPEND content has a live POOM mapping (it does — APPEND does write to `insertpm`) and the link endset was indexed at creation time, the search succeeds.

## The Gap

The only scenario where this fails is if the APPEND content's I-addresses are somehow not in the POOM of the queried document — but APPEND does update the POOM (`appendpm`). The content is addressable at its V-positions; `find_links` can convert those V-positions to I-addresses and match against the link endset.

**In summary:** APPEND's omission of DOCISPAN breaks `find_documents` for that content, but `find_links` operates entirely through the link endset sub-index. A link created over APPEND content has its endpoint I-addresses in the link endset, and searching those V-spans finds the link normally.

---

## Code Exploration

## Answer

**No. `find_links` cannot discover a link whose endset references APPEND-created I-addresses.** The spanfilade is the sole discovery path, and APPEND never registers its I-addresses there.

---

### How `find_links` searches

The FEBE `find` command dispatches to `findlinksfromtothree()` [`fns.c:189`], which calls `dofindlinksfromtothree()` [`do1.c:348`]:

```c
return findlinksfromtothreesp(taskptr, spanf, fromvspecset, tovspecset, threevspecset, orglrangeptr, linksetptr);
```

That function [`spanf1.c:56`] converts each vspec to a sporgl-set, then calls `sporglset2linkset()` for each of the three endset roles (FROM, TO, THREE).

Inside `sporglset2linksetinrange()` [`sporgl.c:245`], every candidate span is looked up by calling:

```c
context = retrieverestricted(spanfptr, (typespan*)sporglset, SPANRANGE, &range, ORGLRANGE, (typeisa*)infoptr);
```

The `range` is built with `prefixtumbler(&orglrange->stream, spantype, &range.stream)` where `spantype` is one of `LINKFROMSPAN=1`, `LINKTOSPAN=2`, or `LINKTHREESPAN=3` [`xanadu.h:35-38`]. The search is entirely inside `spanf` — the spanfilade. No other data structure is consulted.

---

### What DOCISPAN is and who creates it

There are four span types [`xanadu.h:35-39`]:

```c
#define LINKFROMSPAN    1
#define LINKTOSPAN      2
#define LINKTHREESPAN   3
#define DOCISPAN        4
```

`DOCISPAN` entries map I-addresses back to the document they live in. They are created by `docopy()` [`do1.c:62`]:

```c
&& insertspanf(taskptr, spanf, docisaptr, ispanset, DOCISPAN)
```

This is called from the normal `doinsert()` path [`do1.c:87-123`].

---

### How APPEND bypasses this

`doappend()` [`do1.c:25-32`]:

```c
bool doappend(typetask *taskptr, typeisa *docptr, typetextset textset)
{
    bool appendpm(),insertspanf(); /*zzz dies this put in granf?*/

    return (appendpm(taskptr, docptr, textset)/*&&
       appendpm includes insertspanf!   insertspanf(taskptr,spanf,docptr,textset,DOCISPAN)*/
    );
}
```

The `insertspanf(…, DOCISPAN)` call is **commented out**. The comment `/*zzz dies this put in granf?*/` signals this was a known open question when the code was written. `appendpm()` [`orglinks.c:17`] finds the end-of-document address via `findvsatoappend()`, then calls `doinsert()` — but `doinsert()` here goes through `inserttextingranf()` to allocate content in the granfilade. The DOCISPAN registration step never executes.

---

### Why this breaks link discovery

For `find_links` to return a link, the V-addresses in the query must:
1. Be converted to sporgl-set entries (I-spans in the spanfilade under LINKFROMSPAN/TO/THREE)
2. Match link endpoint entries in the spanfilade

APPEND-created content gets an I-address in the granfilade via `inserttextingranf()`, but since `insertspanf(…, DOCISPAN)` is skipped, no DOCISPAN entry maps that I-address back to any V-address. And since `docreatelink()` stores link endpoints as LINKFROMSPAN/LINKTOSPAN/LINKTHREESPAN entries in the spanfilade (via the normal `insertspanf` call), if a link *endpoint* were ever created that referenced an APPEND I-address, the lookup would proceed into the spanfilade — but the spanfilade has no record connecting that V-span to the APPEND I-address.

There is no secondary index, no fallback to the granfilade, and no content-walk in the `find_links` path. `sporglset2linksetinrange()` calls only `retrieverestricted()` on `spanf`, and `retrieverestricted()` does a pure enfilade traversal of that one structure.

---

### Conclusion

APPEND-created I-addresses are **dead ends** from the link-discovery perspective:

- They exist in the granfilade (document content), allocated by `inserttextingranf()`.
- They have no DOCISPAN entry in the spanfilade (the `insertspanf` call in `doappend()` is commented out, `do1.c:29-31`).
- If a link were created whose endset happened to reference one of these I-addresses, `find_links` would still fail to return it — because link discovery searches the spanfilade's LINK*SPAN entries, not the granfilade, and can only resolve V→I mappings that were registered via `insertspanf`.
- The spanfilade is the exclusive discovery path [`sporgl.c:259,261`], and APPEND never populates it.

---

## Question 19 [gregory]

> In a multi-session scenario where session A creates content at I-address X and session B immediately copies it, is there any window — given run-to-completion scheduling in `bed.c` — where session B could observe the POOM entry for X but not yet see X in the granfilade?

### Gregory's Answer

## KB Synthesis

No. There is no such window. Run-to-completion scheduling eliminates it entirely.

## Why No Window Exists

**[INV-ATOMICITY]** (Finding 0042) establishes that `bed.c`'s event loop calls `xanadu(&task)` for a single frontend's request and blocks until it returns before calling `select()` again. The entire INSERT operation for session A — including `inserttextingranf` (granfilade allocation) and `insertpm` (POOM entry via `docopy`) — completes as one uninterruptible unit.

**[INV-SEQUENTIAL-DISPATCH]** (Finding 0042) further confirms that even when multiple frontend file descriptors are simultaneously ready in `select()`'s result, the loop iterates over them sequentially. Session B's COPY request cannot begin until session A's INSERT has fully returned to `select()`.

## The Ordering Guarantee Within INSERT

**[ST-INSERT]** (Finding 0036) documents the call chain: `doinsert` → `inserttextingranf` → `docopy` → `insertpm` + `insertspanf`. The granfilade allocation (step 1) precedes the POOM insertion (step 3) within the same atomic dispatch. The in-memory cache is global and shared across all sessions **[SS-CACHE-MECHANISM]** — there is no per-session view of state that could show a POOM entry before its corresponding granfilade entry.

## What Session B Observes

When session B's COPY eventually executes, it calls `findorgl` to locate the source document's orgl (**[PRE-COPY]**, Finding 0046), then `specset2ispanset` to convert V-spans to I-addresses, then `insertpm` to place them in B's POOM. By this point, session A's entire INSERT has completed. The granfilade and POOM entries for X are fully present in the shared in-memory state.

**Verdict:** The causal gap you describe — where the POOM entry exists without the granfilade entry — is structurally impossible under run-to-completion scheduling. Both entries are created within a single atomic operation. Session B will always see a consistent state where either neither exists (if A hasn't run yet) or both exist (if A has completed).

---

## Code Exploration

Now I have everything I need. Let me trace the full execution path carefully.

---

## Analysis: POOM/Granfilade Visibility Window

**Short answer: No such window exists — and the ordering of updates makes it doubly impossible.**

---

### 1. The Event Loop — `bed.c`

The scheduler is a single-threaded, non-preemptive `select()` loop. `bed.c:103-141`:

```c
for (;;) {
    inputfds2 = inputfds;
    if (select(nfds+1, &inputfds2, 0, 0, &timeout) < 0) { ... }
    else {
        for (i = 0; i <= nfds; i++) {
            if ((1<<i) & inputfds2) {
                user = fdtoplayer[i];
                task.inp = player[user].inp;
                // ...
                xanadu(&task);   // line 128
            }
        }
    }
    // ...
}
```

Each fd is dispatched sequentially inside the inner `for` loop. `xanadu()` is called and **must return before the loop advances to the next fd**. There is no threading, no coroutines, no `yield`.

`xanadu()` itself (`bed.c:153-172`):

```c
int xanadu(typetask *taskptr)
{
    typerequest request;
    // ...
    if (getrequest(taskptr, &request)) {
        (*requestfns[request])(taskptr);    // line 162 — handler runs to completion
        sendresultoutput(taskptr);          // line 163 — flush happens after
    }
    tfree(taskptr);
    // ...
}
```

The handler runs to completion; only then is output flushed and control returns to the loop. If session A (fd=i) and session B (fd=i+1) are both ready in the same `select()` wake, A's entire handler completes before B is dispatched.

---

### 2. The Insert Handler — `fns.c`

`fns.c:84-98` (the live implementation — the commented-out canonical version at line 69 was replaced by this "kluged unix version for speed"):

```c
void insert(typetask *taskptr)
{
    typeisa docisa, vsa;
    typetextset textset;
    bool getinsert(), doinsert();

    (void) getinsert (taskptr, &docisa, &vsa, &textset);
    putinsert (taskptr);                           // line 91 — buffers OK response
    if (!doinsert (taskptr, &docisa, &vsa, textset))  // line 92 — updates data structures
        fprintf(stderr,"requestfailed in insert\n");
}
```

Note `putinsert()` [line 91] is called before `doinsert()` [line 92]. But `putinsert()` only **buffers** into `taskptr->outp`; the actual network flush happens in `sendresultoutput()` at `bed.c:163`, which executes **after** the entire handler returns. So session A's client doesn't receive acknowledgment until after the data structures are updated — and crucially, session B's dispatch cannot begin until after `xanadu()` for session A returns.

---

### 3. `doinsert` — The Ordering of Granfilade vs POOM Updates

`do1.c:87-123`:

```c
bool doinsert(typetask *taskptr, typeisa *docisaptr, tumbler *vsaptr, typetextset textset)
{
    typehint hint;
    typespanset ispanset;
    INT ret;
    bool doretrievev(), inserttextingranf(), docopy();

    makehint(DOCUMENT, ATOM, TEXTATOM, docisaptr, &hint);
    ret = (inserttextingranf(taskptr, granf, &hint, textset, &ispanset)  // line 118
        && docopy (taskptr, docisaptr, vsaptr, ispanset)                 // line 119
    );
    return(ret);
}
```

The sequence is unambiguous:

1. **`inserttextingranf()` [do1.c:118]** — content is placed in the granfilade; on return, `ispanset` holds the I-address X.
2. **`docopy()` [do1.c:119]** — uses `ispanset` to update the POOM (via `insertpm()`) and spanfilade (via `insertspanf()`).

`inserttextingranf()` is `inserttextgr()` in `granf2.c:83-109`:

```c
bool inserttextgr(typetask *taskptr, typegranf fullcrumptr, typehint *hintptr, typetextset textset, typeispanset *ispansetptr)
{
    tumbler lsa, spanorigin;
    // ...
    if (!findisatoinsertgr ((typecuc*)fullcrumptr, hintptr, &lsa))
        return (FALSE);
    movetumbler (&lsa, &spanorigin);
    for (; textset; textset = textset->next) {
        // ...
        insertseq ((typecuc*)fullcrumptr, &lsa, &locinfo);  // line 99 — granfilade entry placed
        tumblerincrement (&lsa, 0, textset->length, &lsa);
    }
    // ... build ispanptr from spanorigin to lsa ...
    *ispansetptr = ispanptr;
    return (TRUE);
}
```

The I-address X is allocated and the content is inserted into the granfilade at `granf2.c:99` (`insertseq()`). Only after this function returns does control reach `docopy()` in `do1.c:119`, which calls `insertpm()` (POOM update).

`docopy()` at `do1.c:45-65` confirms:

```c
bool docopy(typetask *taskptr, typeisa *docisaptr, tumbler *vsaptr, typespecset specset)
{
    // ...
    return (
        specset2ispanset (...)              // resolve I-spans
        && findorgl (...)                   // locate document POOM
        && acceptablevsa (vsaptr, docorgl)
        && asserttreeisok(docorgl)
        && insertpm (...)                   // line 60 — POOM updated
        &&  insertspanf (...)               // line 62 — spanfilade updated
        && asserttreeisok(docorgl)
    );
}
```

The update order within a single `doinsert` call is strictly:

```
granfilade (insertseq)  →  POOM (insertpm)  →  spanfilade (insertspanf)
```

---

### 4. Answer to the Question

**No window exists where session B could observe the POOM entry for X without X being present in the granfilade.**

There are two independent reasons:

**Reason 1 — Run-to-completion scheduling forecloses all interleaving.** The inner loop in `bed.c:118-141` processes one fd at a time. Session B's `xanadu()` call cannot begin until session A's `xanadu()` call returns. Between the two dispatches, all of session A's data structure updates — both granfilade and POOM — are already complete and globally visible (they modify shared in-core data structures, not per-session copies).

**Reason 2 — Granfilade is updated *before* POOM within the same request.** Even if preemption existed (it doesn't), the only inconsistent intermediate state that could be observed would be: **granfilade has X, POOM does not yet**. The question posits the *inverse* (POOM has X, granfilade does not), which cannot arise from `doinsert`'s internal ordering (`do1.c:118-119`). I-address X is minted and stored in the granfilade by `inserttextingranf()` before `docopy()` / `insertpm()` ever executes.

The architecture makes this invariant structural: `insertpm()` receives the I-span returned by `inserttextingranf()`, so the granfilade entry is a logical prerequisite. The compiler-enforced call chain (`do1.c:118-119`, short-circuit `&&`) guarantees the granfilade step runs and succeeds before the POOM step is attempted.

---

## Question 20 [gregory]

> When a link is created with endsets spanning content that is later REARRANGED across a subspace boundary (e.g., text moved from V:1.x to V:2.x), do the link's I-address-based endsets remain fully intact in the spanfilade, and does `find_links` still discover the link from the content's new V-position?

### Gregory's Answer

## KB Synthesis

**Yes on both counts — endsets remain intact, and `find_links` still discovers the link — but for reasons that expose a fragile decoupling between the spanfilade and the POOM.**

## Why endsets survive intact

REARRANGE modifies only the V-dimension displacement of POOM crums via `tumbleradd(&ptr->cdsp.dsas[index], &diff[i], ...)` [ST-REARRANGE, Finding 0056]. The I-dimension (`dsas[I]`) is never touched. The spanfilade, which indexes link endsets by I-address, is a write-only structure with no deletion operation [INV-SPANF-WRITE-ONLY, Finding 0057]. Since REARRANGE calls no spanfilade function at all, the endset entries survive unchanged. This is the same invariant that makes REARRANGE identity-preserving: `∀ c : i_addr(c, after) = i_addr(c, before)` [INV-REARRANGE-IDENTITY].

## Why `find_links` still works

`find_links` operates purely in I-space: it converts the query V-span → I-span via the POOM, then searches the spanfilade by I-address [SS-FIND-LINKS, Finding 0028]. After cross-subspace rearrangement, the moved text's POOM crums now reside at V:2.x, but they still carry the original permascroll I-addresses. A query specifying the content at its new V:2.x position goes through:

```
V:2.x → vspanset2ispanset → POOM (still maps 2.x → permascroll I) → 
  spanfilade search → finds link (I-address entry unchanged)
```

The POOM lookup succeeds because the crum was displaced in-place, not deleted. The spanfilade lookup succeeds because REARRANGE never modified it.

## The caveat: convention violation is structurally tolerated

Finding 0051 explicitly confirms this scenario: `retrieve_contents` at V:2.x returns text bytes ("ABC") after a cross-subspace pivot. The backend treats it as valid. The subspace convention that V:2.x should contain only link orgl ISAs is a caller-enforced invariant [INV-SUBSPACE-CONVENTION, PRE-REARRANGE], not a storage-layer enforcement. `acceptablevsa()` is a no-op [Finding 0010].

So link discovery works, but the system is now in a state violating the subspace convention:

- Content at V:2.x is text (permascroll I-addresses), not a link orgl reference
- `find_links` discovers the original link ✓ (I-space unchanged)
- `compare_versions` would **not** find this content — it requires text-subspace input (V ≥ 1.x) [PRE-COMPARE-VERSIONS], and the rearranged content is now at 2.x
- `CREATENEWVERSION` would also miss the displaced content, since `retrievedocumentpartofvspanpm` returns only the text-subspace V-dimension [ST-VERSION-CREATE, Finding 0043]

The subspace-isolation mechanism that normally protects the 2.x subspace (INSERT's two-blade knife [SS-TWO-BLADE-KNIFE, FC-SUBSPACE]) does not apply to REARRANGE — REARRANGE has no equivalent guard [PRE-REARRANGE, Finding 0051]. The missing precondition is `all cuts must lie within the same subspace`.

---

## Code Exploration

Now I have everything needed. Let me trace the full execution path.

---

## Full Answer

### The Short Answer

**Yes, the link's I-address-based endsets remain fully intact in the spanfilade after a rearrangement.** And **yes, `find_links` does discover the link from the content's new V-position** — because `find_links` routes through the POOM (permutation matrix), which is the only structure rearrangement modifies. The spanfilade is never touched by rearrangement.

---

### Part 1: How a Link's Endsets Are Stored at Creation Time

`createlink()` [fns.c:100-112] → `docreatelink()` [do1.c:195-221]:

```c
bool docreatelink(typetask *taskptr, typeisa *docisaptr, typespecset fromspecset, ...)
{
    ...
    specset2sporglset(taskptr, fromspecset, &fromsporglset, NOBERTREQUIRED)  // V → I
    specset2sporglset(taskptr, tospecset,   &tosporglset,   NOBERTREQUIRED)  // V → I
    specset2sporglset(taskptr, threespecset, &threesporglset, NOBERTREQUIRED)
    ...
    insertendsetsinorgl(...)  // stores I-addresses in the link's own POOM
    insertendsetsinspanf(taskptr, spanf, linkisaptr, fromsporglset, tosporglset, threesporglset)
}
```
[do1.c:214-219]

The call to `specset2sporglset` converts the caller's V-addresses into **I-addresses (permascroll spans)** by traversing the document's POOM. The resulting sporglsets hold I-address data (`sporglorigin`, `sporglwidth`), not V-addresses.

`insertendsetsinspanf()` [do2.c:116-128] then calls `insertspanf` three times — once for FROM, TO, and THREE:

```c
insertspanf(taskptr, spanfptr, linkisaptr, fromsporglset, LINKFROMSPAN)
insertspanf(taskptr, spanfptr, linkisaptr, tosporglset,   LINKTOSPAN)
insertspanf(taskptr, spanfptr, linkisaptr, threesporglset, LINKTHREESPAN)
```

Inside `insertspanf()` [spanf1.c:15-54], for a `SPORGLID` item:

```c
movetumbler(&((typesporgl*)sporglset)->sporglorigin,  &lstream);       // I-address
movetumbler(&((typesporgl*)sporglset)->sporglwidth,   &lwidth);        // I-width
movetumbler(&((typesporgl*)sporglset)->sporgladdress, &linfo.homedoc); // home doc ISA
...
movetumbler(&lstream, &crumorigin.dsas[SPANRANGE]);   // I-address → SPANRANGE axis
movetumbler(&lwidth,  &crumwidth.dsas[SPANRANGE]);
insertnd(taskptr, (typecuc*)spanfptr, &crumorigin, &crumwidth, &linfo, SPANRANGE);
```
[spanf1.c:31-51]

The spanfilade is a 2D structure with:
- **ORGLRANGE axis**: `prefixtumbler(linkISA, LINKFROMSPAN/LINKTOSPAN, ...)` — the link's permanent ISA
- **SPANRANGE axis**: the content's **I-address** (permascroll address), completely independent of its V-position

This means from the moment of creation, the spanfilade contains only I-addresses. **V-addresses are nowhere in the spanfilade.**

---

### Part 2: What Rearrangement Does — and Does Not — Touch

`rearrange()` [fns.c:159-173] → `dorearrange()` [do1.c:34-43]:

```c
bool dorearrange(typetask *taskptr, typeisa *docisaptr, typecutseq *cutseqptr)
{
    findorgl(taskptr, granf, docisaptr, &docorgl, WRITEBERT)
    rearrangepm(taskptr, docisaptr, docorgl, cutseqptr)
}
```

`rearrangepm()` [orglinks.c:137-142]:

```c
bool rearrangepm(typetask *taskptr, tumbler *docisaptr, typeorgl docorgl, typecutseq *cutseqptr)
{
    rearrangend((typecuc*)docorgl, cutseqptr, V);  // <-- only the POOM, only the V dimension
    logbertmodified(docisaptr, user);
    return(TRUE);
}
```

`rearrangend()` [edit.c:78-160] operates exclusively on `cdsp.dsas[V]` — the V-displacement of crums within the POOM:

```c
case 1: case 2: case 3:
    tumbleradd(&ptr->cdsp.dsas[index], &diff[i], &ptr->cdsp.dsas[index]);
    ivemodified((typecorecrum*)ptr);
    break;
```
[edit.c:124-126], where `index == V`.

**Neither `dorearrange`, `rearrangepm`, nor `rearrangend` mentions `spanf`.** The spanfilade global is not touched. The I-addresses stored in the SPANRANGE axis of the spanfilade are completely unaffected.

The cross-subspace boundary concern (V:1.x → V:2.x) is irrelevant to the spanfilade because the spanfilade doesn't store V-addresses at all. Only the POOM's V-dimension changes.

---

### Part 3: How V:1.x Became V:2.x — The POOM After Rearrangement

After rearrangement, the POOM crums for the affected content have new `cdsp.dsas[V]` values. The I-dimension (`cdsp.dsas[I]`) of these crums is **not modified** — it still holds the same permascroll origin as when the content was first inserted. This is the permanent identity of the content.

The V↔I mapping invariant of the POOM is preserved: for any content atom, `cdsp.dsas[I]` = permascroll address, `cdsp.dsas[V]` = current version-space position. After rearrangement, `cdsp.dsas[V]` has changed but `cdsp.dsas[I]` has not.

---

### Part 4: How `find_links` Discovers the Link from the New V-Position

`findlinksfromtothree()` [fns.c:189-202] → `dofindlinksfromtothree()` [do1.c:348-353] → `findlinksfromtothreesp()` [spanf1.c:56-103]:

```c
bool findlinksfromtothreesp(typetask *taskptr, typespanf spanfptr,
    typespecset fromvspecset, ...)
{
    ...
    if (fromvspecset)
        specset2sporglset(taskptr, fromvspecset, &fromsporglset, NOBERTREQUIRED);
    ...
    if (fromvspecset) {
        sporglset2linkset(taskptr, (typecuc*)spanfptr, fromsporglset,
                          &fromlinkset, orglrange, LINKFROMSPAN);
        ...
    }
    intersectlinksets(taskptr, fromlinkset, tolinkset, threelinkset, linksetptr);
    return (TRUE);
}
```
[spanf1.c:70-103]

Step 1: `specset2sporglset(taskptr, fromvspecset, &fromsporglset, ...)` — this converts the **query's V-address** (the content's **new** V-position after rearrangement, e.g., V:2.x) to I-addresses by traversing the **current** POOM.

The conversion path: `specset2sporglset` → `specset2ispanset` [do2.c:14-46] → `vspanset2ispanset` [orglinks.c:397-402] → `permute(orgl, vspanset, V, ispanset, I)` [orglinks.c:404-422] → `span2spanset` [orglinks.c:425-454] → `retrieverestricted` [retrie.c:56-85].

`retrieverestricted` searches the POOM's V dimension for crums overlapping V:2.x. After rearrangement, the POOM crums for the content are exactly there (their `cdsp.dsas[V]` was updated by `rearrangend`). The search returns those crums' I-addresses — which are the **same I-addresses** that were stored in the spanfilade at link creation time.

Step 2: `sporglset2linkset(spanfptr, fromsporglset, &fromlinkset, ..., LINKFROMSPAN)` — searches the spanfilade's SPANRANGE axis for those I-addresses. Since the spanfilade contains exactly those I-addresses (stored when the link was created and never modified), the search succeeds.

**The link is found.**

---

### Summary of the Invariant Chain

| Structure | What's stored | Affected by rearrangement? |
|---|---|---|
| Document POOM | V↔I crum mapping | **Yes** — `cdsp.dsas[V]` adjusted by `rearrangend` |
| Spanfilade (SPANRANGE) | I-addresses of link endsets | **No** — never touched by `rearrangepm` |
| Spanfilade (ORGLRANGE) | Link ISA | **No** — link ISA is permanent |

The design guarantees correctness through the single POOM-as-mediator pattern:

1. Link creation: V → POOM → I → stored in spanfilade  
2. Rearrangement: POOM V-dimension updated, spanfilade untouched  
3. `find_links`: new V → updated POOM → same I → found in spanfilade → **link recovered**

The V-subspace boundary crossing (V:1.x → V:2.x) is simply a large displacement in `cdsp.dsas[V]`, handled the same as any other `tumbleradd` in `rearrangend` [edit.c:125]. The tumbler arithmetic is agnostic to subspace boundaries. The link's I-address endsets in the spanfilade are unaffected, and `find_links` succeeds from the new V-position.
