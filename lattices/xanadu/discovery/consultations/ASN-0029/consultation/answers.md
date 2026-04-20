# Consultation Answers — Document Lifecycle

**Inquiry:** What invariants govern document creation, ownership, and the relationship between documents in the docuverse? What does it mean to open, close, and create documents?
**Date:** 2026-03-10 23:54
**Questions:** 20 (10 nelson, 10 gregory)

---

## Question 1 [nelson]

> When a new document is created, what properties must the system assign to it at the moment of creation that can never change afterward?

### Nelson's Answer

# Properties Assigned at Document Creation That Can Never Change

When the system executes CREATENEWDOCUMENT, it assigns properties that become permanent the instant the document ID is returned. These fall into four categories.

## 1. The Tumbler Address (Document ID)

This is the most fundamental immutable property. The system assigns a tumbler address encoding the document's permanent position in the docuverse tree.

> "New items may be continually inserted in tumbler-space while the other addresses remain valid. This means that any address of any document in an ever-growing network may be specified by a permanent tumbler address." [LM 4/19]

The address has the form `Node.0.User.0.Document.0.Element` [LM 4/26], and the first three fields are fixed at creation. No subsequent operation can change them.

## 2. Ownership

Ownership is not metadata attached to the document — it IS the User field of the tumbler address. Since the address never changes, ownership never changes.

> "Every document has an owner, the person who created and stored it (or someone who arranged it to be created and stored, such as a publishing company)." [LM 2/29]

> "Typically, the user will have no control over the node address he, she or it is assigned; but once assigned a User account, the user will have full control over its subdivision forevermore." [LM 4/29]

The owner is whoever controls the account under which the document is baptized. This is structural, not a property that can be transferred through some "change owner" operation — no such operation exists in FEBE.

## 3. The I-Space Namespace

All native content created in the document will have I-space addresses that fall under this document's tumbler prefix. The document field determines the permanent home location of every byte the owner will ever store there.

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

This means the document's identity as an origin point — the fact that I-address `N.0.U.0.D.0.X` traces back to document `N.0.U.0.D` — is permanent and structural. It is how origin traceability works:

> "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

## 4. Ancestry (for Versions)

When a document is created via CREATENEWVERSION rather than CREATENEWDOCUMENT, the ancestry is encoded in the document ID itself:

> "This creates a new document with the contents of document \<doc id\>. It returns the id of the new document. The new document's id will indicate its ancestry." [LM 4/66]

> "The Document field of the tumbler may be continually subdivided, with new subfields in the tumbler indicating daughter documents and versions." [LM 4/29]

The parent-child relationship in the forking tree is permanent. Once `2.4.1` is baptized under `2.4`, that lineage cannot be altered.

## 5. Position in the Forking Tree

More broadly, the document's position in the universal tree of nodes, accounts, and documents is permanent:

> "So the docuverse is all really one big forking document." [LM 4/18]

> "The owner of a given item controls the allocation of the numbers under it." [LM 4/20]

Once a number is forked, no reorganization ever happens. The document at address `1.3.27.4` is forever the fourth document (or version) under document 27 of account 3 on node 1.

## What Is NOT Immutable

For contrast, the following are mutable:

- **V-space arrangement** — changes with every INSERT, DELETE, REARRANGE
- **Content** — can be added (INSERT, APPEND) or removed from view (DELETEVSPAN)
- **Links** — can be created (MAKELINK) or deleted by owner
- **Publication status** — can transition from private to published (though published cannot easily revert: "its author may not withdraw it except by lengthy due process" [LM 2/43])

## A Note on Time

Time of creation is tracked but is explicitly NOT part of the tumbler:

> "Note that 'time' is not included in the tumbler. Time is kept track of separately." [LM 4/18]

Whether the creation timestamp is immutable is not explicitly stated in the sources. It is reasonable to assume it is (what would it mean to change a creation time?), but Nelson does not specify this directly. NEED_RAW: [4/65, 5/6-5/8] for any additional detail on document creation mechanics and system-maintained metadata.

## Summary

At the moment of creation, the system permanently assigns:

| Property | Where Encoded | Why Immutable |
|----------|---------------|---------------|
| Tumbler address | The ID itself | Addresses are permanent by design |
| Ownership | User field of tumbler | No transfer operation exists |
| I-space namespace | Document field of tumbler | All native bytes will live here |
| Ancestry | Document field subdivisions | Forking tree is append-only |
| Tree position | All fields of tumbler | "No reorganization ever happens" |

These are not five independent properties but five facets of one fact: **the tumbler address, once baptized, is eternal**. Everything that the address encodes — owner, origin, lineage, position — is therefore eternal with it.

---

## Question 2 [nelson]

> What does ownership of a document guarantee to the owner — is it control over content, control over visibility, or something else entirely?

### Nelson's Answer

# Ownership in Xanadu: What It Guarantees

Ownership is **control over the document's content and economic rights** — but emphatically NOT control over how others connect to or quote from published work. Nelson designs ownership as a bundle of specific rights, some of which are deliberately surrendered upon publication.

## What the Owner Controls

### 1. Content Modification (Absolute)

Only the owner may change a document's content or arrangement:

> "Every document has an owner, the person who created and stored it (or someone who arranged it to be created and stored, such as a publishing company). The rightful copyright holder, or someone who has bought the document rights... Only the owner has a right to withdraw a document or change it." [LM 2/29]

This covers all editing operations: INSERT, DELETE, REARRANGE, APPEND, and COPY-into. No one else can alter your document. If someone wants to modify your work, they create their own version — "without damaging the originals" [LM 2/45].

### 2. Out-Links (But Not In-Links)

The owner controls the links stored in their document, but not links others make pointing into it:

> "Ordinarily a document consists of its contents (including history and alternatives) and its out-links, the links it contains that point to other documents. By contrast, a document's in-links are those stored elsewhere which point to it. These out-links are under control of its owner, whereas its in-links are not." [LM 2/31]

This is a critical asymmetry. Your document's outbound connections are yours. But others' connections into your document belong to them.

### 3. Visibility (Pre-Publication)

Before publication, the owner controls who can see the document:

> "A private document may be read and linked-to only by the owner and his or her associates. A published document is available to anyone, and may be read and linked-to by anyone." [LM 2/42]

### 4. Address Space Subdivision

The owner controls allocation of sub-addresses:

> "The owner of a given item controls the allocation of the numbers under it." [LM 4/20]

This means you can create new versions, new sub-documents, and new content under your address without coordinating with anyone.

### 5. Economic Rights

Royalties flow to the owner automatically:

> "In our planned service, there is a royalty on every byte transmitted. This is paid automatically by the user to the owner every time a fragment is summoned." [LM 2/43]

## What the Owner Surrenders Upon Publication

This is where Nelson's design becomes distinctive. Publication is a **binding act** that trades certain controls for universal accessibility and automatic compensation.

### Control Over Incoming Links — Gone

> "Accessibility and free linking make a two-sided coin. On the one hand, each user is free to link to anything privately or publicly. By the same token, each author of a published work is relinquishing the right to control links into that work. This relinquishment must also be part of the publishing contract." [LM 2/43]

### Control Over Quotation — Gone

> "Since the copyright holder gets an automatic royalty, anything may be quoted without further permission. That is, permission has already been granted: for part of the publication contract is the provision, 'I agree that anyone may link and window to my document.'" [LM 2/45]

### Right of Easy Withdrawal — Gone

> "It is in the common interest that a thing once published stay published, as in the world of paper. Other readers and users will come to depend on its accessibility. Consequently its author may not withdraw it except by lengthy due process." [LM 2/43]

The reason is structural: others will have made links to your document — links they own, at their addresses. Withdrawing your document would destroy their property.

## The Deeper Principle

Ownership in Xanadu is **not sovereignty over a territory**. It is closer to authorship of a published book: you wrote it, your name is on it, you get paid when people read it, and you can publish corrections. But you cannot recall copies from libraries, you cannot prevent critics from quoting you, and you cannot stop scholars from annotating your work.

Nelson splits traditional copyright's two goals — compensation and control — and keeps only the first. The owner gets **automatic, guaranteed, proportional compensation**. In exchange, the owner gives up **control over use**. This tradeoff is the engine of the whole system: without it, the web of connections that makes literature self-correcting could never form.

> "There is no way whatever to ascertain or control what happens at the users' terminals. Therefore perforce all use whatever is legitimate, and anyone who plans to be vulnerable to 'misuse,' whatever he or she thinks that may be, had better keep his or her stuff off the system." [LM 2/47]

## Summary

| Right | Private Document | Published Document |
|-------|------------------|--------------------|
| Modify content | Owner only | Owner only |
| Control out-links | Owner only | Owner only |
| Control visibility | Owner chooses who sees it | Everyone sees it |
| Control in-links | Owner controls access | **Surrendered** |
| Control quotation | Owner controls access | **Surrendered** |
| Withdraw document | Freely | Only by "lengthy due process" |
| Receive royalties | N/A | Automatic, per-byte |
| Subdivide address space | Always | Always |

Ownership guarantees **content integrity** and **economic rights**. It does not guarantee control over how the world responds to, connects to, or quotes from your published work. That is by design — it is the price of participating in a living literature.

---

## Question 3 [nelson]

> Can ownership of a document ever transfer from one user to another, or is the creator-owner relationship permanent?

### Nelson's Answer

## Ownership Transfer in Xanadu

Nelson explicitly contemplates ownership transfer. The key passage at 2/29 defines the owner broadly:

> "Every document has an owner, the person who created and stored it (or someone who arranged it to be created and stored, such as a publishing company). The rightful copyright holder, or someone who has bought the document rights... Only the owner has a right to withdraw a document or change it." [LM 2/29]

Three categories of owner are recognized here:

1. **The creator** — the person who actually wrote and stored the document
2. **The arranger** — someone who commissioned its creation (e.g., a publishing company)
3. **The purchaser** — "someone who has bought the document rights"

The phrase "bought the document rights" clearly implies ownership can transfer through sale, paralleling traditional copyright assignment.

### The Structural Tension

However, Nelson specifies **no mechanism** for ownership transfer within the system. The tumbler address permanently encodes the User field — the account under which the document was created:

> "There are four major fields, each expandable indefinitely, with three major dividers between them. These fields are Server, User, Document and Contents." [LM 4/26]

> "Typically, the user will have no control over the node address he, she or it is assigned; but once assigned a User account, the user will have full control over its subdivision forevermore." [LM 4/29]

The address `Node.0.User.0.Document.0.Element` always reflects the *original* creator's account. If ownership transfers, the document still resides at the original user's tumbler address. There is no FEBE operation for reassigning document ownership, and changing the address would violate the permanence guarantee.

### My Intent

Ownership transfer is a **legal and contractual** matter, not an addressing matter. The tumbler address records *provenance* (where the document was born), not necessarily current ownership. Just as a painting by Picasso retains its provenance even when sold to a collector, a Xanadu document retains its creation address even when rights transfer.

The enforcement model supports this interpretation — the system operates through contractual trust, not technical enforcement:

> "Because the conceptual structure expects participants to behave in certain ways, these are embraced in the contract offered to users." [LM 4/4]

Royalty routing, modification rights, and withdrawal authority would follow the current rightful owner, tracked through the contractual layer rather than the addressing layer.

### What Is NOT Specified

- No FEBE command for transferring ownership
- No mechanism for updating royalty routing after transfer
- No specification of what documentation or process validates transfer
- No statement on whether sub-accounts or delegation could model transferred rights

NEED_RAW: [2/29-2/31] — The full passage on document ownership may contain additional context about transfer mechanisms that the curated extract condensed.

---

## Question 4 [nelson]

> What does it mean for a document to be "open" versus "closed" — is this a property of the document's editability, its visibility, or its relationship to the user?

### Nelson's Answer

## "Open" vs "Closed" Documents in Nelson's Design

**Nelson does not define "open" vs "closed" as a document state.** The FEBE protocol contains no OPEN or CLOSE operations. His 17 commands are stateless — you name a tumbler address, issue a command, the back end responds.

### What Nelson Actually Specifies: Private vs Published

Nelson's access model is binary:

> "A document may be private or published. [...] A private document may be read and linked-to only by the owner and his or her associates. A published document is available to anyone, and may be read and linked-to by anyone." [2/42]

From the session-model analysis: "No OPEN/CLOSE operations — Nelson's 17 commands establish no session state on a document. No read vs. write modes — Nelson's model is: you own it (modify freely) or you do not (create a version)."

### Where "Open" and "Closed" DO Appear

Nelson uses these terms **philosophically**, not as document properties:

**"Open hypertext"** — one of his one-liners for the system: "A pluralistic publishing and archiving medium with open hypertext and semi-closed framing" [3/2]. Here "open" means anyone can link to, quote from, and annotate published content. Connections flow freely.

**"Closed systems"** — Nelson's term of condemnation for systems that forbid external contribution:

> "Though interactive videodiscs have begun to proliferate, it is only as closed systems to which others may not add or make variations. This is unacceptable in the long term." [3/23]

A "closed" system is one where the creator controls all connections. In Xanadu, published documents are deliberately NOT closed — "each author of a published work is relinquishing the right to control links into that work" [2/43].

### The Implementation Layer

The OPEN/CLOSE/BERT (Back-End Request Token) mechanism comes from **Roger Gregory's implementation**, not from Nelson's design. As the session-model analysis notes: "Gregory's BERT mechanism — OPEN, CLOSE, READBERT, WRITEBERT, the lock table, denial-as-branching — is the implementation of the session layer that Nelson left undesigned."

### So What Is the Answer?

For Nelson, the relevant distinction is not editability or session state but **relationship to the docuverse**:

- **Published** = open to the world: anyone can read, link, quote, annotate. The author relinquishes control over incoming connections. Royalties flow automatically.
- **Private** = restricted: only owner and designees. Can still link outward to published content.
- **"Closed"** = Nelson's pejorative for systems that prevent external connection. The opposite of what Xanadu is for.

Editability is determined by **ownership**, not by any open/closed state: "Only the owner has a right to withdraw a document or change it" [2/29]. If you don't own it, you don't edit it — you create a version.

NEED_RAW: [4/61-4/65, 4/79] — to verify there is no document-state terminology in the protocol preamble or the "not yet implemented" list that might relate to open/closed semantics.

---

## Question 5 [nelson]

> Must every document in the docuverse be unique, and what prevents two users from creating documents that the system treats as identical?

### Nelson's Answer

## Document Uniqueness in the Docuverse

**No, documents need not be unique in content.** Two users can independently create documents with byte-for-byte identical text, and the system treats them as entirely distinct documents. Nothing prevents this, and nothing checks for it.

### Identity Is Structural, Not Value-Based

The critical distinction is between **content identity** (where bytes were created) and **content value** (what the bytes say). Xanadu tracks identity, not value.

Every document gets a unique tumbler address determined by its ownership path:

> "There are four major fields, each expandable indefinitely, with three major dividers between them. These fields are Server, User, Document and Contents." [LM 4/26]

If Alice creates a document, it lives at `ServerA.0.Alice.0.Doc1`. If Bob independently types the same text, his document lives at `ServerB.0.Bob.0.Doc1`. Different I-space addresses, different documents — regardless of identical content.

> "The basic principle is that of owned numbers. Numbers are owned by individuals or companies, and subnumbers under them are bestowed on other individuals and companies on whatever basis the owners choose." [LM 4/17]

The tumbler hierarchy guarantees address uniqueness through ownership delegation. No coordination is needed; no central authority checks for duplicates.

### Transclusion vs. Independent Creation

This design is what makes transclusion meaningful. From the provenance model:

- **Transcluded content SHARES I-addresses** — Alice windows Bob's paragraph, and both reference the same I-space bytes. The system knows they are the same content.
- **Independently created content has DIFFERENT I-addresses** — Alice types the same words Bob typed, but her bytes live at her address. The system treats them as unrelated.

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

This is how the system distinguishes "quoted from the original" from "happened to write the same words." The operation `FINDDOCSCONTAINING` finds documents sharing I-space material (transclusions), not documents with identical byte values.

### No Verification of Any Kind

The system explicitly disclaims content verification:

> "User acknowledges that all material on the network is stored by users under similar arrangements to User's own, without verification or assurance of truth, authenticity, accuracy, usefulness or other beneficial character of such materials." [LM 5/17]

There is no uniqueness check, no deduplication, no content hashing. The system does not examine what you store — it only tracks where you store it and who owns it.

### Why This Is By Design

This follows from two principles:

1. **Ownership is absolute.** Your document is yours. Its identity comes from your act of creation at your address, not from what you wrote. Two people writing the same sentence have each created something they own independently.

2. **Attribution is structural.** If the system deduplicated identical content, it would destroy attribution — whose document would the shared bytes "belong" to? By keeping I-addresses distinct per creation event, every byte has exactly one home document and one owner.

> "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

### The Practical Implication

If you want the system to know that your content came from someone else's document, you must **transclude** (use COPY in FEBE), not retype. Retyping creates new I-space bytes at your address. Transclusion creates a V-space reference to existing I-space bytes at the original address. Only transclusion preserves the connection, triggers royalties, and enables `FINDDOCSCONTAINING` to discover the relationship.

---

## Question 6 [nelson]

> Can a document ever be destroyed or removed from the docuverse, or does creation imply permanent existence?

### Nelson's Answer

# Can a Document Be Destroyed or Removed from the Docuverse?

The short answer: **creation does not guarantee absolutely permanent existence, but the system is designed with an overwhelming bias toward permanence.** Nelson distinguishes several cases with different rules.

---

## Published Documents: Near-Permanent

Published documents are the strongest case for permanence. Nelson is explicit that publication creates obligations:

> "It is in the common interest that a thing once published stay published, as in the world of paper. Other readers and users will come to depend on its accessibility. Consequently its author may not withdraw it except by lengthy due process." [LM 2/43]

The reason is structural — other users will have linked to your document, and those links are *their* property:

> "However, for corrections and amendments, the author may readily publish a superseding document, but the former version must remain on the network. This is vital because of the links other users may have made to it — which can now reach through from the previous version (to which they were originally attached) into the newer version." [LM 2/43]

So withdrawal is not absolutely impossible — "lengthy due process" implies a mechanism exists — but the default is permanence. Even superseded documents remain, because links depend on them.

The publication contract reinforces this. From the enforcement model, publishers may withdraw "only with one year's notice and fee" [LM 5/20].

---

## Private Documents: Owner Controls

Private documents are a different matter entirely. The owner has absolute control:

> "Every document has an owner, the person who created and stored it... Only the owner has a right to withdraw a document or change it." [LM 2/29]

Since private documents are accessible "only by the owner and his or her associates" [LM 2/42], no one else has linked to them or depends on their existence. The owner can withdraw them freely.

---

## Privashed Documents: Withdrawable by Design

Nelson explicitly provides a middle path called "privashing":

> "An author who wishes to render his work universally available, but wishes also to retain the right to withdraw it at any time, has a simple means for so doing. The author simply designates his or her document as a private document with unrestricted distribution." [LM 2/48]

Privashed content is publicly accessible but can be withdrawn at any time. The tradeoff: no royalties, and anyone who linked to it has no recourse.

---

## Anonymous Content: Removable by Challenge

Anonymous ("John Doe") publications are explicitly vulnerable to removal:

> "Consider libelous or uncomplimentary John Doe graffiti defaming specific individuals. If John Doe is not available, the affected individual must be able to effect removal of the materials by peremptory challenge." [LM 2/60]

This is the one case where content can be removed by someone other than its owner — precisely because the anonymous owner "won't hang around to defend their acts."

---

## I-Space Content: Append-Only, Never Overwritten

At the storage level, the architecture is append-only:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

Even "deletion" in Xanadu does not destroy I-space content:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

So at the I-space level, content is designed to be physically permanent. "Withdrawal" means removing accessibility, not destroying bytes.

---

## The Storage Funding Question

There is an unresolved tension. Nelson requires that "ALL SERVICES MUST BE SELF-SUPPORTING" [LM 4/5], and storage requires ongoing rental fees. He does not specify what happens when payment lapses — whether content becomes inaccessible, enters a grace period, or is preserved by the Author's Fund. This is a gap in the specification.

Vendor failure is handled: "Upon notice of cancellation, Storage Vendor will arrange for the orderly transition of all customer-stored materials to other Xanadu locations" [LM 5/16]. But individual payment lapse is unaddressed.

---

## Summary

| Document State | Can Be Removed? | By Whom? | Mechanism |
|---|---|---|---|
| **Published** | With great difficulty | Owner only | "Lengthy due process," one year notice + fee |
| **Private** | Yes, freely | Owner | Owner's right to withdraw |
| **Privashed** | Yes, freely | Owner | By design — private with open access |
| **Anonymous (John Doe)** | Yes, if defamatory | Affected party | Peremptory challenge |
| **I-space bytes** | Never destroyed | No one | Append-only by architecture |

Creation implies **strong permanence by default**, especially for published content. But Nelson does not treat permanence as absolute — he provides withdrawal mechanisms for every case, just with varying friction. The key insight is that permanence is a *social obligation* enforced by the link structure (others depend on your content), not a physical impossibility of removal.

---

## Question 7 [nelson]

> When one document includes content that originated in another document, what relationship must the system maintain between those two documents?

### Nelson's Answer

## The Inclusion Relationship: What the System Must Maintain

When document A includes content originating in document B, Xanadu must maintain **six structural relationships** between them. These are not optional features — they are consequences of the architecture itself.

---

### 1. Origin Traceability (Structural, Not Metadata)

The included bytes retain their permanent I-space addresses, which encode their home document. The system fetches included content from its origin:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

The I-address itself — `Node.0.User.0.Document.0.Element` — structurally encodes which document created those bytes. This cannot be stripped or severed:

> "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

---

### 2. Ownership Preservation

The original owner retains ownership of the included content. Inclusion does not transfer ownership:

> "Document A can include Document B, even though Document B is owned by someone else." [LM 2/35]

> "Each compound document is like the other documents: it has an owner and receives royalties." [LM 2/33]

The compound document has its own owner who controls the arrangement. But the included bytes belong to whoever created them. Two ownership claims coexist without conflict — one over the arrangement (V-space), one over the content (I-space).

---

### 3. Non-Destruction of the Original

Inclusion must never alter, damage, or consume the source document:

> "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate — without damaging the originals. This is done by inclusion links." [LM 2/45]

> "The integrity of each document is maintained by keeping the two aspects separate: derivative documents are permanently defined (and stored) in terms of the originals and the changes." [LM 2/37]

The original remains exactly as its author wrote it. Readers of the compound document can always say "Show me what this originally was."

---

### 4. Navigability Between Documents

Users must be able to traverse from included content back to its source, and from the source forward to everything that includes it:

> "Only when you step through the window — turning one glass page and going on in the next — do you reach the original that you wanted. But stepping through the window means you are now in another work." [LM 2/34]

This works in both directions:

> "As already stated, it is possible for the reader to ask to see the materials which are windowed to by a given document. However, it must also be possible for the reader to ask to see whatever documents window to the current document. Both are available at any time." [LM 2/37]

The FEBE operation `FINDDOCSCONTAINING` supports the reverse direction: "This returns a list of all documents containing any portion of the material included by \<vspec set\>." [LM 4/70]

---

### 5. Automatic Royalty Flow

When included content is delivered to a reader, the original owner receives payment automatically:

> "In our planned service, there is a royalty on every byte transmitted. This is paid automatically by the user to the owner every time a fragment is summoned, as part of the proportional use of byte delivery." [LM 2/43]

> "If a modified document is read, the original owner and the modifier split the royalty in proportion to who wrote what, as determined automatically." [LM 2/45]

The system knows which bytes belong to whom (via I-addresses), so the royalty split is mechanical — no negotiation, no tracking, no invoicing.

---

### 6. Liveness (for Location-Fixed Windows)

The system supports two inclusion modes, and the relationship differs:

> "A quotation — an inclusion window — may be fixed to another document in two ways: at a certain point in time, in which case revisions are seen by the user only when he or she asks, 'What has this passage become?' Or second, at a relatively fixed location in the document space, in which case updates are seen automatically." [LM 2/37]

For location-fixed inclusions, the system must maintain a **live connection** — changes to the source propagate to the including document:

> "No copying operations are required among the documents throughout the system, and thus we solve the problems of update — especially the problem of updating documents which depend on other documents. We solve this problem simply by windowing to a changing document." [LM 2/36]

---

### Why This Is Architectural, Not Policy

These six relationships are consequences of the I-space/V-space separation, not features bolted on top. When document A includes content from document B:

- A's V-space maps positions to I-addresses that live under B's ownership
- The COPY operation creates this mapping without duplicating bytes
- Fetching A's content requires resolving those I-addresses back to B's storage
- The I-address encodes B's identity structurally

The alternative — copying bytes and severing the connection — is precisely what Nelson designed the system to prevent:

> "Remember the analogy between text and water. Water flows freely, ice does not. The free-flowing, live documents on the network are subject to constant new use and linkage, and those new links continually become interactively available. Any detached copy someone keeps is frozen and dead, lacking access to the new linkage." [LM 2/48]

---

## Question 8 [nelson]

> Must the system preserve the order in which documents were created, and does a document's position in that ordering carry any meaning?

### Nelson's Answer

## Does Creation Order Matter in Xanadu?

**Short answer:** The system structurally preserves creation order through sequential tumbler assignment, but Nelson explicitly denies that this ordering carries semantic meaning.

### Creation Order IS Preserved

Sequential numbering is an unavoidable consequence of the forking/baptism mechanism. Documents under an account are created by successive forking:

> "For instance, if there is an item 2, it can branch into several more items, each of which is a daughter item. Thus 2.1, 2.2, 2.3, 2.4... are successive items being placed under 2." [LM 4/20]

So document 1.2.3 was necessarily created after 1.2.2 under account 1.2. This is structural — the system cannot assign these numbers out of order.

For **links within a document**, creation order is even more explicitly preserved:

> "The links designated by a tumbler address are in their permanent order of arrival. A document includes only the links of which it is the home document." [LM 4/31]

Link 2.1 is always the first link created; link 2.755 is always the 755th. Deleting link 2.5 does not renumber 2.6 onward.

At the **byte level**, I-space content is append-only — "filed, as it were, chronologically" [LM 2/14]. Later-created bytes have higher I-addresses within a document.

### But the Ordering Carries No Semantic Meaning

Nelson is explicit on two points that drain the ordering of significance:

**Tumblers impose no structure on content:**

> "Tumblers do not affect the user-level structure of the documents; they only provide a mapping mechanism, and impose no categorization and no structure on the contents of a document." [LM 4/17-4/18]

**Time is not encoded in the address:**

> "Note that 'time' is not included in the tumbler. Time is kept track of separately." [LM 4/18]

That document 1.2.3 comes after 1.2.2 tells you about creation sequence but says nothing about the document's subject, importance, or relationship to 1.2.2. The numbering is purely a mechanism for allocating unique, permanent addresses.

### Even Version Numbers Don't Imply Derivation

Perhaps most strikingly, Nelson disclaims semantic meaning even for version/subdocument numbers:

> "In a sense the version, or subdocument number is only an accidental extension of the document number, and strictly implies no specific relationship of derivation." [LM 4/29]

And:

> "There is thus no 'basic' version of a document set apart from other versions—'alternative' versions—any more than one arrangement of the same materials is a priori better than other arrangements." [LM 2/19]

### Summary

| What | Preserved? | Meaningful? |
|------|-----------|-------------|
| Document creation order under an account | Yes (sequential forking) | No (mapping mechanism only) |
| Link creation order within a document | Yes (permanent order of arrival) | Structural fact, but no semantic weight |
| Byte creation order in I-space | Yes (append-only) | Implementation detail, not user-facing |
| Version numbering | Yes (sequential) | Explicitly "no specific relationship of derivation" |
| Timestamps | Tracked separately | Yes — used for filtering (e.g., "links from last week") |

The system **must** preserve creation order because the addressing mechanism makes it structurally inevitable — you cannot assign tumbler 2.3 before 2.2. But this ordering is a side effect of the allocation mechanism, not a semantic property. Nelson designed tumblers as a **mapping mechanism**, not a **categorization system**. Actual temporal information is kept separately as metadata, usable for filtering but not baked into the address structure.

---

## Question 9 [nelson]

> If two documents share content through quotation or transclusion, does modifying one document's structure affect what the other document displays?

### Nelson's Answer

## No. Modifying one document's structure does not affect what another document displays.

This is a direct consequence of the I-space/V-space separation, which is the architectural core of Xanadu.

### The Mechanism

When Document B transcludes content from Document A, B's V-space contains a mapping to bytes in A's **I-space** (permanent content store). It does not reference A's V-space arrangement.

Editing Document A — inserting, deleting, rearranging — changes only A's **V-space** (its current arrangement). The I-space bytes remain exactly where they are, unchanged and permanent.

Nelson states this explicitly:

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

So if Alice writes "hello world" and Bob transcludes it, then Alice "deletes" it from her document — Bob still sees "hello world." Alice's delete only removed the content from her V-space view. The I-space bytes persist, and Bob's document still maps to them.

### Why This Works

The key is that I-space content is **immutable**:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

And the storage model is **append-only**:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

Content is added, never overwritten or removed. Editing is re-arranging references to permanent content, not modifying the content itself.

### The Non-Destruction Guarantee

Nelson frames this as a fundamental principle:

> "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate — without damaging the originals. This is done by inclusion links." [LM 2/45]

And:

> "No copying operations are required among the documents throughout the system, and thus we solve the problems of update — especially the problem of updating documents which depend on other documents. We solve this problem simply by windowing to a changing document." [LM 2/36]

The "distributed update" problem — where changes to one document corrupt dependent documents — is solved by not copying in the first place. Transclusion is reference, not duplication.

### The Two Windowing Modes (A Nuance)

Nelson does describe two modes for how windows can behave:

> "A quotation — an inclusion window — may be fixed to another document in two ways: at a certain point in time, in which case revisions are seen by the user only when he or she asks, 'What has this passage become?' Or second, at a relatively fixed location in the document space, in which case updates are seen automatically." [LM 2/37]

- **Time-fixed**: Frozen reference to specific I-space content. Completely unaffected by any change to the source document.
- **Location-fixed**: Tracks a position in the source document's evolving structure, so if the source publishes a *new version* with different content at that position, the window may reflect it.

But even in the location-fixed case, this is about **versioning** (new content published at a logical position), not about structural edits breaking the reference. The underlying I-space content that the window originally pointed to still exists and is still accessible.

### Summary

| Operation on Document A | Effect on Document B (which transcludes from A) |
|---|---|
| **Rearrange** A's content | None — I-space unchanged |
| **Delete** content from A | None — "bytes remain in all other documents" |
| **Insert** new content in A | None — new bytes get new I-space addresses |
| **Publish new version** of A | Time-fixed window: none. Location-fixed window: may show updated content at that position |

The architectural guarantee is absolute: I-space is permanent, V-space edits are local to the document being edited, and transclusion references I-space. One document's structural changes cannot damage another document's view.

---

## Question 10 [nelson]

> What is the smallest thing that qualifies as a document — can a document be empty at creation, or must it contain at least some content?

### Nelson's Answer

## A Document Can Be Empty at Creation

The answer is explicit in the FEBE protocol. The `CREATENEWDOCUMENT` operation is defined as:

> "This creates an empty document. It returns the id of the new document." [LM 4/65]

A document can be created with zero bytes and zero links. The system assigns it a permanent tumbler address and returns that address. The document exists from that moment — empty but real.

## Why This Makes Architectural Sense

Three points from the design reinforce this:

**1. Documents are positions, not objects.** The ghost elements discussion makes clear that a document is a location in tumbler-space, not a stored thing:

> "While a number on the line may represent a document or an account, that doesn't mean there's an object stored for it. What's stored is the contents--bytes and links." [LM 4/23]

An empty document is a valid position with nothing yet stored beneath it.

**2. Documents can contain only links.** Nelson explicitly says a document of nothing but links is valid:

> "Thus the 'Jabberwocky' is a document; and a set of links between them, were someone to create it, would yet be a separate document." [LM 2/29]

If a document can be pure links with no text, emptiness is just the degenerate case.

**3. Documents are containers, not contents.** The document is the owned unit — an address under which content accumulates over time:

> "A document is really an evolving ONGOING BRAID." [LM 2/14]

A braid with zero strands is still a braid. You create the document first, then populate it with `INSERT` or `APPEND` operations.

## The Lifecycle

The intended workflow is clear from the protocol: `CREATENEWDOCUMENT` creates the empty container and returns its ID, then `INSERT` or `APPEND` adds content to it. Creation and population are separate operations — the document exists before it has content.

---

## Question 11 [gregory]

> When a brand-new document is created (not via CREATENEWVERSION), how is its document-level tumbler address allocated — does `findisatoinsertnonmolecule` walk the granfilade under the user's account range (e.g., `1.1.0.2`) to find max+1, or is there a separate document counter?

### Gregory's Answer

## KB Synthesis

## Document Address Allocation for CREATEDOCUMENT

The answer is: **`findisatoinsertnonmolecule` walks the granfilade tree under the account's address range to find max+1. There is no separate document counter.**

### Mechanism

[SS-ADDRESS-ALLOC Finding 0021] describes the algorithm directly:

1. `makehint(ACCOUNT, DOCUMENT, 0, account_isa, &hint)` sets `depth=2` (encoding the `.0.` boundary between account and document)
2. `upperbound = tumblerincrement(account_isa, depth-1=1, 1)` — produces the next sibling of the account (e.g., `1.1.0.3` for account `1.1.0.2`)
3. `findpreviousisagr` traverses the granfilade tree to find the highest existing address **below** that upper bound
4. A containment check (added after Bug 0013) verifies the found address is actually under the target account prefix
5. If no child exists: allocate first child at `account_isa.0.1` (e.g., `1.1.0.2.0.1`)
6. If a child exists: truncate to the appropriate length and increment (e.g., `1.1.0.2.0.1` → `1.1.0.2.0.2`)

### No Separate Counter

[SS-ADDRESS-SPACE Finding 0077] makes this explicit:

> "There is no single global 'next' counter (no Σ.next). Instead, allocation is a family of independent functions partitioned by tumbler range: `next_doc_addr(granf, parent) = max_child(granf, parent) + 1`"

[SS-ADDRESS-SPACE Finding 0061] confirms: "The allocation is purely derived from current tree state — there is no cached 'next available' pointer."

The same `findisatoinsertnonmolecule` path handles CREATE, VERSION, and all non-content address allocation — distinguished only by what hint (`ACCOUNT→DOCUMENT` vs `DOCUMENT→DOCUMENT`) is passed. The granfilade tree itself is the implicit counter.

The [INV-GLOBAL-ADDRESS-UNIQUENESS] observation that addresses are globally unique across sessions is an emergent consequence of this scheme: all sessions query the same shared granfilade tree, so each call sees the current maximum and allocates above it.

---

## Code Exploration

I have traced the full call chain. Here is the complete answer.

---

## How brand-new document tumbler addresses are allocated

**Short answer:** There is no separate document counter. `findisatoinsertnonmolecule` performs a live walk of the granfilade via `findpreviousisagr` to find the current maximum document address under the user's account, then returns `max + 1`. The granfilade *is* the counter.

---

### Call chain (traced from the protocol handler down)

**1. Entry: `docreatenewdocument`** — `do1.c:234–241`

```c
bool docreatenewdocument(typetask *taskptr, typeisa *isaptr)
{
  typehint hint;
  bool createorglingranf();

    makehint (ACCOUNT, DOCUMENT, 0, &taskptr->account, &hint);
    return (createorglingranf (taskptr, granf, &hint, isaptr));
}
```

`makehint` (`do2.c:78–83`) fills `hint.supertype = ACCOUNT(2)`, `hint.subtype = DOCUMENT(3)`, `hint.atomtype = 0`, and copies `taskptr->account` into `hint.hintisa`. The hint carries the user's account address — e.g. `1.1.0.2` — as the anchor for searching.

No counter is read or written here.

---

**2. `createorglingranf` → `createorglgr`** — `granf1.c:50–55`, `granf2.c:111–128`

```c
bool createorglgr(typetask *taskptr, typegranf fullcrumptr, typehint *hintptr, typeisa *isaptr)
{
    if (!findisatoinsertgr ((typecuc*)fullcrumptr, hintptr, isaptr))
        return (FALSE);
    locinfo.infotype = GRANORGL;
    locinfo.granstuff.orglstuff.orglptr = createenf (POOM);
    ...
    insertseq ((typecuc*)fullcrumptr, isaptr, &locinfo);
    ...
}
```

`findisatoinsertgr` is called first — it fills `*isaptr` with the new address. Only then is the node inserted. No counter is consulted before or after.

---

**3. `findisatoinsertgr` dispatches on `subtype`** — `granf2.c:130–156`

```c
bool findisatoinsertgr(typecuc *fullcrumptr, typehint *hintptr, typeisa *isaptr)
{
    if (hintptr->subtype == ATOM) {
        ...
        findisatoinsertmolecule (fullcrumptr, hintptr, isaptr);
    } else {
        findisatoinsertnonmolecule (fullcrumptr, hintptr, isaptr);
    }
    tumblerjustify(isaptr);
    return (TRUE);
}
```

`subtype = DOCUMENT(3)` ≠ `ATOM(4)`, so the path goes to `findisatoinsertnonmolecule`. The comment in `granf2.c:144–152` confirms this handles `DOCUMENT`, `ACCOUNT`, and `NODE` types.

---

**4. The allocation engine: `findisatoinsertnonmolecule`** — `granf2.c:203–242`

This is the complete function:

```c
static int findisatoinsertnonmolecule(typecuc *fullcrumptr, typehint *hintptr, typeisa *isaptr)
{
  typeisa upperbound, lowerbound, truncated;
  INT depth, hintlength;
  bool lowerbound_under_hint;

    depth = hintptr->supertype == hintptr->subtype ? 1 : 2;
    hintlength = tumblerlength (&hintptr->hintisa);
    tumblerincrement (&hintptr->hintisa, depth - 1, 1, &upperbound);
    clear (&lowerbound, sizeof(lowerbound));
    findpreviousisagr ((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);

    lowerbound_under_hint = FALSE;
    if (!iszerotumbler(&lowerbound)) {
        tumblertruncate(&lowerbound, hintlength, &truncated);
        lowerbound_under_hint = tumblereq(&truncated, &hintptr->hintisa);
    }

    if (iszerotumbler(&lowerbound) || !lowerbound_under_hint) {
        /* Nothing under this hint - create first child as hintisa.0.1 */
        tumblerincrement(&hintptr->hintisa, depth, 1, isaptr);
    } else {
        tumblertruncate (&lowerbound, hintlength + depth, isaptr);
        tumblerincrement(isaptr, tumblerlength(isaptr)==hintlength?depth:0, 1, isaptr);
    }
}
```

Step by step for account `A = 1.1.0.2` (`hintlength = 4` stories, `depth = 2` because `ACCOUNT ≠ DOCUMENT`):

- **`upperbound`** = `tumblerincrement(A, depth-1=1, 1)` → `A.0.1` = `1.1.0.2.0.1`. This is a strict upper bound for the search: "find me the last document address below `1.1.0.2.0.1`."
- **`findpreviousisagr(granf, upperbound, &lowerbound)`** — walks the granfilade tree recursively (see below) to find the highest existing ISA < `upperbound` under this account.
- **If nothing found** (`lowerbound` is zero or not under `A`): `tumblerincrement(A, depth=2, 1)` → `mantissa[idx+2] += 1` where `idx=3` (the `2` in `1.1.0.2`) → result is `1.1.0.2.0.1`. That is the first document.
- **If something found** (e.g. previous doc = `1.1.0.2.0.3`): truncate lowerbound to `hintlength + depth = 6` stories → still `1.1.0.2.0.3`, then `tumblerincrement(isa, 0, 1)` increments the last component → `1.1.0.2.0.4`.

---

**5. The granfilade walk: `findpreviousisagr`** — `granf2.c:255–278`

```c
int findpreviousisagr(typecorecrum *crumptr, typeisa *upperbound, typeisa *offset)
{
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

This is a recursive descent through the granfilade enfilade tree. It accumulates `offset` by summing crum widths leftward, then descends into the rightmost subtree that could contain the answer. At height 0 (a leaf), `findlastisaincbcgr` (`granf2.c:280–284`) reads the actual last ISA from the bottom crum. The result is the highest address stored in the granfilade that is less than `upperbound`. There is no counter — the tree *is* the authoritative source.

---

### No counter exists

Checking `init.c` confirms that initialization (`init.c:25–79`) sets up only a dispatch table (`requestfns[]`). No document counter is initialized, stored, or consulted anywhere in the code. The granfilade serves as both the storage structure and the canonical record of what addresses have been allocated. Each `CREATENEWDOCUMENT` call reads the current maximum from the tree and returns `max + 1`.

---

### Summary

| Stage | File | What happens |
|-------|------|--------------|
| `docreatenewdocument` | `do1.c:234–241` | Constructs hint `(supertype=ACCOUNT, subtype=DOCUMENT, hintisa=account_addr)` |
| `createorglgr` | `granf2.c:111–128` | Calls `findisatoinsertgr` to get address, then inserts into granfilade |
| `findisatoinsertgr` | `granf2.c:130–156` | Routes to `findisatoinsertnonmolecule` because `subtype ≠ ATOM` |
| `findisatoinsertnonmolecule` | `granf2.c:203–242` | Computes `upperbound`, calls `findpreviousisagr`, returns `max+1` (or first child) |
| `findpreviousisagr` | `granf2.c:255–278` | Recursive granfilade tree walk — finds the highest existing ISA below `upperbound` |

The `depth = 2` value (because `ACCOUNT ≠ DOCUMENT`) means the document address is exactly 2 mantissa-stories deeper than the account address, producing the `.0.N` suffix: account `1.1.0.2` → documents `1.1.0.2.0.1`, `1.1.0.2.0.2`, etc., each produced by incrementing the granfilade's own maximum.

---

## Question 12 [gregory]

> What state is initialized when a new document is created — is the POOM created empty (zero-height tree), or is there a sentinel entry, and are any granfilade or spanfilade entries written at creation time before any INSERT?

### Gregory's Answer

## KB Synthesis

## Document Creation: Initial State

### POOM State

A newly created document's POOM is **not** a zero-height tree. `createenf(POOM)` produces a minimal height-1 tree with a sentinel bottom node [SS-ENFILADE-TREE]:

- Fullcrum: `isapex=TRUE`, `height=1`, `numberofsons=1`
- One bottom crum: `height=0`, zero width, `infotype=GRANNULL`
- Root-level `cdsp=0`, `cwid=0`

This sentinel bottom crum is structurally critical. Finding 0058 documents that the "never-filled" state and the "deleted-everything" state are **not equivalent**: after delete-everything, `levelpull` (disabled) never collapses the tree, so no bottom crum exists at all. Subsequent INSERT or VCOPY into a deleted-everything document crashes because `firstinsertionnd()` calls `findleftson()` which returns NULL — it assumes a bottom crum always exists. A freshly created document satisfies this assumption; a deleted-empty document does not [EC-EMPTY-DOC].

### Granfilade

Yes — one granfilade entry is written at creation time: the document orgl itself, allocated via `createorglingranf` → `findisatoinsertnonmolecule`. This assigns the document its address in the hierarchical granfilade tree. No content I-addresses are allocated at this point [SS-ADDRESS-ALLOC, ST-ADDRESS-ALLOC].

### Spanfilade

No spanfilade entries are written at creation time for an empty document:

- **DOCISPAN entries** are created only during INSERT and COPY operations [ST-INSERT, SS-DOCISPAN]
- **Link index entries** are created only during CREATELINK [ST-CREATE-LINK]

CREATENEWVERSION is the exception: it additionally calls `docopyinternal` → `insertspanf` to copy the source document's content mappings into the spanfilade [ST-VERSION]. But for a bare CREATEDOCUMENT, the spanfilade is untouched.

### Summary

| Layer | State after CREATEDOCUMENT |
|-------|---------------------------|
| POOM | Height-1 tree, 1 sentinel zero-width bottom crum |
| Granfilade | One orgl entry (document address allocation) |
| Spanfilade | Empty — no DOCISPAN, no link entries |

---

## Code Exploration

I now have everything I need to give a complete, fully-cited answer. Here it is.

---

## What State Is Initialized When a New Document Is Created

### The Call Chain

**`fns.c:276–286`** — `createnewdocument()` calls `docreatenewdocument()`, then puts the response.

**`do1.c:234–241`** — `docreatenewdocument()` does exactly two things:

```c
bool docreatenewdocument(typetask *taskptr, typeisa *isaptr)
{
  typehint hint;
  bool createorglingranf();

    makehint (ACCOUNT, DOCUMENT, 0, &taskptr->account, &hint);
    return (createorglingranf (taskptr, granf, &hint, isaptr));
}
```

That's it. No INSERT, no copy, no spanfilade call — only `makehint` + `createorglingranf`.

---

### What `createorglingranf` Does

**`granf1.c:50–55`** — thin wrapper that calls `createorglgr`.

**`granf2.c:111–128`** — `createorglgr`:

```c
bool createorglgr(typetask *taskptr, typegranf fullcrumptr, typehint *hintptr, typeisa *isaptr)
{
  typegranbottomcruminfo locinfo;
  ...
    if (!findisatoinsertgr ((typecuc*)fullcrumptr, hintptr, isaptr))
        return (FALSE);
    locinfo.infotype = GRANORGL;
    locinfo.granstuff.orglstuff.orglptr = createenf (POOM);      // ← creates the POOM
    reserve ((typecorecrum*)locinfo.granstuff.orglstuff.orglptr);
    locinfo.granstuff.orglstuff.orglincore = TRUE;
    locinfo.granstuff.orglstuff.diskorglptr.diskblocknumber = DISKPTRNULL;
    insertseq ((typecuc*)fullcrumptr, isaptr, &locinfo);          // ← writes to granfilade
    rejuvinate ((typecorecrum*)locinfo.granstuff.orglstuff.orglptr);
    return (TRUE);
}
```

Steps:
1. Computes the new document's ISA address via `findisatoinsertgr`.
2. Calls `createenf(POOM)` — creates the POOM.
3. Writes a single `GRANORGL` bottom-crum entry into the granfilade (`granf`) at the new ISA address, pointing at the fresh POOM. `diskorglptr.diskblocknumber = DISKPTRNULL` means it's in-core only, not yet on disk.

---

### What `createenf(POOM)` Creates — The POOM Structure

**`credel.c:492–516`** — `createenf`:

```c
typecuc *createenf(INT enftype)
{
  typecuc *fullcrumptr;
  typecorecrum *ptr;

    fullcrumptr = (typecuc *) createcrum(1, enftype);   // height-1 apex
    fullcrumptr->cenftype = enftype;
    fullcrumptr->isapex = TRUE;
    fullcrumptr->isleftmost = TRUE;
    adopt(ptr = createcrum(0, enftype), SON, (typecorecrum*)fullcrumptr);  // one bottom crum
    if (enftype == GRAN) {
        ((typecbc *)ptr)->cinfo.infotype = GRANNULL;  // GRAN only — not POOM
    }
    ivemodified (ptr);
    return (fullcrumptr);
}
```

For `POOM` the `if (enftype == GRAN)` branch is **not taken**. The POOM bottom crum is not given a `GRANNULL` sentinel or any special marker.

**`credel.c:541–596`** — `createcruminternal` (called by `createcrum`) shows what happens to the bottom crum:

```c
ptr->height = crumheight;           // 0
ptr->isapex = FALSE;
ptr->cenftype = enftype;            // POOM
ptr->modified = TRUE;
ptr->isleftmost = FALSE;
ptr->age = NEW;
ptr->leftbroorfather = NULL;
ptr->rightbro = NULL;
clear(&ptr->cdsp, sizeof(ptr->cdsp));   // all zeros
clear(&ptr->cwid, sizeof(ptr->cwid));   // all zeros
...
// For POOM/SPAN height-0 crum:
clear(&((type2dcbc *)ptr)->c2dinfo, sizeof(((type2dcbc *)ptr)->c2dinfo));  // all zeros
```

**The freshly-created POOM has:**
- Height = 1 (one-level enfilade: one upper crum (the apex/fullcrum) + one bottom crum beneath it)
- The single bottom crum (`type2dcbc`) has `cwid = 0`, `cdsp = 0`, and `c2dinfo = 0` — it is all-zero structural scaffolding, **not a content sentinel**
- **Not** a zero-height tree — the height is 1, but the bottom crum carries no content and has zero width

---

### The "Emptiness" Predicate

**`genf.c:97–116`** — `isemptyenfilade` on a POOM:

```c
case POOM :
    return (
       iszerolock(ptr->cwid.dsas, (unsigned)widsize(ptr->cenftype))
    && iszerolock(ptr->cdsp.dsas, (unsigned)dspsize(ptr->cenftype)));
```

Both `cwid` and `cdsp` are zero on the freshly created fullcrum — so `isemptyenfilade` returns **TRUE**.

**`orglinks.c:539–544`** — `isemptyorgl` (called by `doretrievedocvspanset`):

```c
bool isemptyorgl(typeorgl fullcrumptr)
{
    return (
       iszerolock ((tumbler*)&((typecuc*)fullcrumptr)->cwid, widsize(POOM))
    && iszerolock ((typecuc*)((typecuc*)fullcrumptr)->cdsp, dspsize(POOM)));
}
```

Same test. Used at **`do1.c:330–332`**:

```c
if (isemptyorgl (docorgl)) {
    *vspansetptr = NULL;  /* Empty document returns empty vspanset */
    return TRUE;
}
```

So a freshly created document returns an empty vspanset from `RETRIEVE_DOC_VSPAN_SET`.

---

### No Spanfilade Entries at Creation Time

`docreatenewdocument` never calls `insertspanf`, `insertnd`, or any spanfilade function. Contrast this with `docopy` [`do1.c:53–65`] and `docreatenewversion` [`do1.c:260–299`], both of which explicitly call `insertspanf` after inserting content. The spanfilade is only written when content (text or link references) is placed into the document.

---

### Summary

At `CREATENEWDOCUMENT`, the following and **only** the following state is initialized:

| Structure | What is written |
|-----------|----------------|
| **Granfilade (`granf`)** | One `GRANORGL` bottom-crum entry at the new document's ISA address. Points to the new POOM. `diskorglptr = DISKPTRNULL` (in-core only). |
| **POOM** | Height-1 enfilade: one apex (`typecuc`, `isapex=TRUE`) + one bottom crum (`type2dcbc`, all fields zero). Both `cwid` and `cdsp` are all-zero. `isemptyorgl()` → TRUE. |
| **Spanfilade (`spanf`)** | **Nothing.** No entries written. |
| **Content (permascroll atoms)** | **Nothing.** No text, no links. |

The POOM is **not** a zero-height tree — it has a height-1 apex plus one all-zero bottom crum — but it IS functionally empty by the `isemptyenfilade`/`isemptyorgl` tests, which check that all widths are zero. There is no sentinel content entry; the bottom crum is unavoidable structural scaffolding that `createenf` always installs (the enfilade is never truly height-0). First content insertion hits the `isemptyenfilade` branch in `doinsertnd` [`insertnd.c:191–193`], which routes to `firstinsertionnd` to overwrite that bottom crum with real content rather than creating a new one.

---

## Question 13 [gregory]

> When `OPENDOCUMENT` is called, does it do anything beyond inserting a BERT entry — for instance, does it load or pin the document's POOM in the cache, or is POOM loading deferred until the first operation on that document?

### Gregory's Answer

## KB Synthesis

The KB does not contain a finding that directly answers this question. Here is what can be derived from what is recorded:

**What the KB does say:**

[SS-DOCUMENT-LIFECYCLE] (Finding 0027b) establishes that there is an explicit "open list" maintained by the backend, separate from the BERT table. `findorgl` checks whether a document orgl is in this open list — it is not just a BERT lookup. The backend log line `orgl for ... not open in findorgl temp = 0` confirms these are tracked separately.

[PRE-OPEN-DOC] (Finding 0014) describes `checkforopen` as the BERT-layer access control gate that returns access type, "needs opening", or denial. This is distinct from the open list check in `findorgl`.

[SS-CACHE-MECHANISM] (Finding 0059) describes the grim reaper cache: all crums (including POOM nodes) are in a shared in-memory circular list with age-based eviction. There is no "pinning" mechanism documented — crums are subject to eviction regardless of whether their document is open.

**What cannot be answered from the KB:**

The KB has no finding covering `doopen` (the backend handler for OPENDOCUMENT). Specifically, it does not record whether:
- OPENDOCUMENT eagerly reads the document's orgl/POOM into cache
- Or simply registers the document in the open list (BERT + orgl list), with actual POOM loading deferred to the first operation that calls `findorgl` / `retrieverestricted`

The cache architecture ([SS-CACHE-MECHANISM]) is consistent with deferred loading — crums are loaded on demand and evicted by age — but this is inference, not a finding. The question is not answerable from the KB as it stands.

---

## Code Exploration

I now have everything needed to answer definitively. Here is the full trace.

---

## `OPENDOCUMENT`: What It Does and What It Defers

### Call chain for OPEN

`bed.c:162` dispatches `(*requestfns[request])(taskptr)`. The `OPEN` opcode (35) is registered to `myopen` at `init.c:66`. That lands in:

```c
// fns.c:388–401
void myopen(typetask *taskptr)
{
  tumbler t, newt;
  int type, mode;
  bool getopen(), doopen();

    if (
        getopen(taskptr, &t, &type, &mode)
        &&  doopen(taskptr, &t, &newt, type, mode, user)) {
        putopen(taskptr, &newt);
    } else {
        putrequestfailed(taskptr);
    }
}
```

Three steps: parse the wire request, run `doopen`, send the response. The POOM is not touched in `getopen` or `putopen`; they only read/write the FEBE byte stream. The question is entirely about `doopen`.

---

### What `doopen` does — `bert.c:264–322`

```c
// bert.c:264
bool doopen(typetask *taskptr, tumbler *tp, tumbler *newtp, int type, int mode, int connection)
{
  INT openState;
  bool docreatenewversion();

   if (type == NOBERTREQUIRED) { return 1; }

   if (mode == BERTMODECOPY) {
    docreatenewversion(taskptr, tp, &taskptr->account, newtp);   // see below
    addtoopen(newtp, connection, TRUE, type);
    return 1;
   }

   openState = checkforopen(tp, type, connection);   // pure hash-table lookup

   if (openState == 0) {
    addtoopen(tp, connection, FALSE, type);
    tumblercopy(tp, newtp);
    return 1;
   }

   switch (mode) {
    case BERTMODECOPYIF:
    if (openState == -1) {
        docreatenewversion(taskptr, tp, &taskptr->account, newtp);
        addtoopen(newtp, connection, TRUE, type);
    } else if (type != WRITEBERT && openState != WRITEBERT) {
        incrementopen(tp, connection);   // pure table increment
        tumblercopy(tp, newtp);
    } else {
        docreatenewversion(taskptr, tp, &taskptr->account, newtp);
        addtoopen(newtp, connection, TRUE, type);
    }
    return 1;
    case BERTMODEONLY:
    if (openState == -1 || openState == WRITEBERT) { return 0; }
    else if (openState == 0) {
        addtoopen(tp, connection, FALSE, type);
        tumblercopy(tp, newtp);
        return 1;
    } else {
        incrementopen(tp, connection);
        tumblercopy(tp, newtp);
        return 1;
    }
   }
}
```

`checkforopen` and `addtoopen`/`incrementopen` only manipulate the **in-memory `berttable`** — a hash table of `bertentry` structs keyed by tumbler. Those structs hold `{connection, documentid, created, modified, count, type}`. Nothing else. No enfilade traversal, no disk I/O.

---

### `addtoopen` — `bert.c:128–151`

```c
int addtoopen(tumbler *tp, int connection, int created, int type)
{
  bertentry *ptr = eallocwithtag(sizeof(bertentry), BERTTAG);
  tumblercopy(tp, &ptr->documentid);
  ptr->connection = connection;
  ptr->count = 1;
  ptr->created = created;
  ptr->modified = FALSE;
  ptr->type = type;
  // insert ptr into berttable[hash]
}
```

Allocates a small `bertentry`, populates it, chains it into the hash bucket. **No POOM, no disk.**

---

### Where POOM loading actually happens

Every document operation (insert, delete, rearrange, retrieve) reaches the POOM through `findorgl` in `granf1.c:17–41`:

```c
// granf1.c:17
bool findorgl(typetask *taskptr, typegranf granfptr, typeisa *isaptr, typeorgl *orglptr, int type)
{
    if ((temp = checkforopen(isaptr, type, user)) <= 0) {
        ...return FALSE;  // access check
    }
    *orglptr = fetchorglgr(taskptr, granfptr, isaptr);   // <-- POOM fetch
    return (*orglptr ? TRUE : FALSE);
}
```

`fetchorglgr` (in `granf2.c:22–81`) navigates the granfilade to find the crum for the given ISA. **If the POOM is not yet in memory** (`!orglincore`), it calls `inorgl` to load it from disk:

```c
// granf2.c:51–61
if (context->corecrum->cinfo.infotype == GRANORGL) {
    if (!context->corecrum->cinfo.granstuff.orglstuff.orglincore) {
        // disk block number must be valid
        inorgl (context->corecrum);   // <-- LAZY LOAD FROM DISK
    }
    ret = context->corecrum->cinfo.granstuff.orglstuff.orglptr;
}
```

`inorgl` is defined in `corediskin.c:171` and reads the enfilade tree for that document from the disk file. After loading, `orglincore` is set so subsequent calls skip the disk read.

`findorgl` is **never called** from `myopen`, `doopen`, or `addtoopen`. It is only called by the operational do-functions: `dorearrange` [do1.c:40], `docopy` [do1.c:55], `dodeletevspan` [do1.c:164], `doretrievedocvspan` [do1.c:318], `doretrievedocvspanset` [do1.c:327], `doretrievedocvspanfoo` [do1.c:307], and others in `do2.c`.

---

### Special case: `BERTMODECOPY` / write-conflict in `BERTMODECOPYIF`

When `OPENDOCUMENT` is called with mode `BERTMODECOPY` (or `BERTMODECOPYIF` against a write-locked document), `doopen` calls `docreatenewversion` [do1.c:260–299]. This function **does** touch the POOM of the **source** document: it calls `doretrievedocvspanfoo` → `findorgl` → `fetchorglgr` to get the source's V-span, then runs `docopyinternal` to copy content into the freshly-created empty POOM. However, this is the copy-on-open operation itself — the result is a brand-new document whose POOM is already in memory (`orglincore = TRUE`, `diskorglptr = DISKPTRNULL` [granf2.c:123–124]).

---

### Summary

| Mode | BERT table updated | POOM loaded |
|---|---|---|
| `BERTMODEONLY` (plain open) | Yes — `addtoopen` or `incrementopen` | **No — deferred to first operation** |
| `BERTMODECOPYIF` (no conflict) | Yes — `incrementopen` | **No — deferred** |
| `BERTMODECOPYIF` or `BERTMODECOPY` (write conflict / explicit copy) | Yes — `addtoopen` on new version | Yes — source POOM loaded to copy content into new version |

**For a standard open (`BERTMODEONLY` or `BERTMODECOPYIF` against an unlocked document), `OPENDOCUMENT` does exactly one thing beyond the wire protocol: it inserts a `bertentry` into the in-memory `berttable` hash table.** The document's POOM is not loaded, not pinned, not touched. POOM loading is deferred until the first actual document operation, which calls `findorgl` → `fetchorglgr`, which calls `inorgl` only if `orglincore` is false.

---

## Question 14 [gregory]

> When `CLOSEDOCUMENT` is called, does it flush dirty POOM nodes for that document to disk, or does it only remove the BERT entry and leave cache eviction to the grim reaper?

### Gregory's Answer

## KB Synthesis

The KB does not directly describe the implementation of `CLOSEDOCUMENT`. No finding covers what the close handler does internally.

That said, the KB provides strong contextual evidence for an informed inference:

**Against per-document flush:**

- [SS-DURABILITY-BOUNDARY] (Finding 0059): Durability is session-level. `writeenfilades()` is called only from `bed.c:134` during daemon shutdown. There is no documented per-document or per-operation flush. The section explicitly states: "Within-session consistency comes from the in-memory cache, not from disk state."

- [SS-CACHE-MECHANISM] (Finding 0059): The grim reaper selects eviction victims by age (`age >= OLD`), not by document state or close events. Eviction is triggered by memory pressure, not lifecycle events.

- [SS-UNIFIED-STORAGE] (Finding 0059): All enfilade types share a single cache and allocator. There is no per-document cache partition that could be selectively flushed.

**What close almost certainly does:**

Based on [SS-BERT] and [PRE-OPEN-DOC], `CLOSEDOCUMENT` removes the document from the session's open list and updates the BERT table (decrement reference count or remove the entry). This is consistent with the access control model where `checkforopen` tests open-list membership before allowing content operations.

**Bottom line:** The KB cannot confirm this with a code-level citation, but all documented mechanisms point to the grim reaper handling dirty POOM node eviction independently of document close. `CLOSEDOCUMENT` almost certainly only manages the BERT entry and open-list membership — no flush.

If this matters for a spec precondition, the gap should be filled by direct code inspection of the `CLOSEDOCUMENT` handler in `do2.c` or `do1.c`.

---

## Code Exploration

I have enough information to give a complete answer. Here is the full trace:

---

## `CLOSEDOCUMENT`: BERT entry removal only — no disk flush

### Execution path

**`CLOSEDOCUMENT`** is handled by `myclose()` [`fns.c:404`]:

```c
void myclose(typetask *taskptr)
{
    if(getclose(taskptr, &t) && doclose(taskptr, &t, user))
        putclose(taskptr);
    else
        putrequestfailed(taskptr);
}
```

`doclose()` [`bert.c:325`] does exactly one thing:

```c
bool doclose(typetask *taskptr, tumbler *tp, int connection)
{
    if (!removefromopen(tp, connection))
        fprintf(stderr, "Bert was not open!\n");
    return TRUE;
}
```

`removefromopen()` [`bert.c:154`]:
1. Finds the matching `bertentry` in the hash table.
2. Decrements `bert->count` [`bert.c:169`]. If the count is still > 0 (multiple opens), returns immediately — nothing else happens.
3. When count reaches 0: evaluates `bert->created && !bert->modified` [`bert.c:173`]. If true (doc was created but never written to), calls `deleteversion()`.
4. Calls `efree(p->stuff)` and splices the conscell out of the hash chain [`bert.c:177-188`].

That is the entire operation. **There is no call to `diskflush()`, `writeenfilades()`, `orglwrite()`, `subtreewrite()`, or any other disk-write function.**

### `deleteversion()` is a stub

```c
int deleteversion(tumbler *tp)
{
#ifndef DISTRIBUTION
    fprintf(stderr,"deleteversion: tp = ");
    dumptumbler(tp);
    fprintf(stderr,"\n");
#endif
}
```
[`bert.c:348-353`] — The body is empty. It does nothing. In `DISTRIBUTION` builds it emits zero bytes.

Note also that the condition in `removefromopen` — `bert->created && !bert->modified` — is the *opposite* of what `exitbert()` checks. `exitbert()` [`bert.c:210`] calls `deleteversion` when `modified && created` (to roll back an abandoned session). `removefromopen` calls it when `created && !modified` — a created-but-untouched document. Either way, `deleteversion()` is currently a no-op.

### When does disk I/O actually happen?

**1. The Grim Reaper — memory-pressure eviction (`credel.c:106–329`)**

When `ealloc()` runs out of free memory [`credel.c:70-75`], it calls `grimlyreap()`, which walks the `grimreaper` ring looking for an `isreapable()` node. `reap()` then either:

- Calls `orglwrite((typecbc*)temp)` [`credel.c:309`] for apex POOM nodes
- Calls `subtreewrite(temp)` [`credel.c:329`] for non-apex nodes

Both paths eventually call `writeloaf()` to write blocks to disk. This is the only path that flushes dirty POOM nodes on demand during normal operation — and it is triggered by **memory pressure, not by `CLOSEDOCUMENT`**.

**2. Last user disconnects (`bed.c:105`)**

```c
if (n_players < 1) {
    diskflush();   /* Write out everything when no one around */
    ...
}
```

`diskflush()` [`corediskout.c:58`] calls `writeenfilades()` + `initkluge()`, serializing the entire granfilade and spanfilade to disk.

**3. QUIT or SIGINT (`bed.c:134-135`, `bed.c:183-184`)**

```c
writeenfilades();
closediskfile();
```

Both the `quitafteruser` path and the `flagquitting()` SIGINT handler call this before `exit()`.

**4. Single-user exit via `diskexit()` (`corediskout.c:30-53`)**

Same: `writeenfilades()` + `closediskfile()`.

### Answer

**`CLOSEDOCUMENT` only removes the BERT entry.** It has no effect on POOM nodes or the in-core enfilade. Dirty POOM nodes accumulate in memory and are flushed in one of three ways:

1. **Lazily by the grim reaper** — only when `ealloc()` fails under memory pressure, via `reap()` → `orglwrite()` / `subtreewrite()` [`credel.c:292-329`]
2. **Globally when the last user leaves** — via `diskflush()` [`bed.c:105`]
3. **On process exit** — via `writeenfilades()` in `diskexit()`, `quitxanadu()`, or signal handlers

So the second framing in your question is correct: `CLOSEDOCUMENT` removes the BERT entry and **leaves cache eviction entirely to the grim reaper** (and to the exit path). There is no per-document flush on close.

---

## Question 15 [gregory]

> The Node.0.User.0.Doc tumbler hierarchy implies a two-level ownership model — is the node address (`1.1`) assigned at server startup and fixed, and is the user account address (`1.1.0.N`) allocated at account creation time, or can these be assigned dynamically?

### Gregory's Answer

## KB Synthesis

The KB describes the tumbler hierarchy and allocation mechanisms in detail, but does not contain findings that directly address how node addresses (`1.1`) are assigned or when account addresses (`1.1.0.N`) are created.

**What the KB does say:**

The `Node.0.User.0.Doc.0.Element` structure is a docuverse convention, not type enforcement — tumblers are unconstrained digit sequences and the `.0.` separators are purely positional semantics [SS-TUMBLER, Finding 0001].

The address hierarchy is encoded by `.0.` boundary count:
- Node address: `1.1` (no `.0.`)
- Account under node: `1.1.0.2` (one `.0.` boundary)
- Document under account: `1.1.0.2.0.1` (two `.0.` boundaries)

[SS-ADDRESS-SPACE, Finding 0021]

The allocation algorithm (`findisatoinsertnonmolecule`) with `depth=1` handles NODE→NODE and DOCUMENT→DOCUMENT placement, while `depth=2` handles ACCOUNT→DOCUMENT. This tells us how children are allocated under existing parents, but says nothing about how the root node addresses (`1.1`, `1.2`, etc.) are established [SS-ADDRESS-ALLOC, Finding 0021].

**What the KB cannot answer:**

There are no findings covering:
- Whether node addresses are pre-configured at server initialization vs. dynamically allocated
- The bootstrapping mechanism for the initial node (`1.1`) and its account children
- Whether multiple nodes (e.g., `1.2`, `1.3`) can coexist or how they'd be created

The KB's coverage begins at the account level and below. The node-level bootstrapping is not answerable from available findings.

---

## Code Exploration

Now I have all the evidence I need. Here is my complete analysis.

---

## Tumbler Address Assignment: Node, User Account, and Document

### The Hierarchy in Brief

The actual addresses seen in practice are:

| Level | Example | Context |
|-------|---------|---------|
| Node | `1.1` | Client-chosen root prefix |
| Account/User | `1.1.0.N` | Client passes; server allocates N |
| Document | `1.1.0.N.0.D` | Server allocates D sequentially |
| Sub-node | `1.1.0.N.K` | Server allocates K sequentially |

This is confirmed explicitly in `febe/scenarios/accounts.py:7` ("Xanadu tumbler structure: Node.0.User.0.Doc.0.Element") and by the golden test results.

---

### Is the Node Address `1.1` Fixed at Startup?

**No.** The node address `1.1` is not assigned or initialized anywhere in the backend at startup. There is no hardcoded node bootstrap.

At startup, `xumain.c:49` calls:

```c
getaccount(&task, &task.account);
```

The implementation in `task.c:28-41` simply zeroes the account tumbler:

```c
bool getaccount(typetask *taskptr, typeisa *accountptr) {
    tumblerclear(accountptr);
    return(TRUE);
    /* ...prompt and gettumbler code is commented out... */
}
```

The **client** is entirely responsible for establishing what node address to operate under. It does so via the `XACCOUNT` command (opcode 34). `fns.c:364-373` handles it:

```c
void xaccount(typetask *taskptr) {
    if (getxaccount(taskptr, &(player[user].account))) {
        putxaccount(taskptr);
    }
}
```

And `get1.c:190-204` (or `get1fe.c:213-226`) reads the tumbler from the wire:

```c
bool getxaccount(typetask *taskptr, typeisa *accountptr) {
    gettumbler(taskptr, accountptr) && validaccount(taskptr, accountptr);
    taskptr->account = *accountptr;
    return(TRUE);
}
```

The backend's `validaccount()` in `get2fe.c:338-341` performs **no validation**:

```c
bool validaccount(typetask *taskptr, typeisa *accountptr) {
    return(TRUE);
}
```

So the client can pass any tumbler as its operating account. The `1.1` prefix is a **client-side convention** — the default from `febe/scenarios/common.py:12`:

```python
DEFAULT_ACCOUNT = Address(1, 1, 0, 1)
```

The only hardcoded `1.1`-containing value in the entire backend is the **unused** `socketbe.c:35`:

```c
tumbler defaultaccount = {0,0,0,0,  1,1,0,14,0};
```

This declares a default of `1.1.0.14`, but the code that would have used it (`socketbe.c:113-115`) is commented out.

---

### Is Account Address `1.1.0.N` Allocated Dynamically?

**Yes, but with a dual mechanism**: the base prefix (`1.1.0`) comes from the client-supplied hint; the `N` component is allocated sequentially by the server.

The `CREATENODE_OR_ACCOUNT` command (opcode 38) handles creation. The call path:

1. `fns.c:375-386`: reads the client-supplied hint tumbler via `getcreatenode_or_account()`
2. `get1.c:208-212`: `gettumbler(taskptr, tp)` — the hint comes off the wire
3. `do1.c:243-258`:

```c
bool docreatenode_or_account(typetask *taskptr, typeisa *isaptr) {
    typeisa isa;
    typehint hint;
    tumblercopy(isaptr, &isa);
    makehint(NODE, NODE, 0, &isa, &hint);
    result = createorglingranf(taskptr, granf, &hint, &isa);
    if (result) { tumblercopy(&isa, isaptr); }
    return result;
}
```

The `makehint(NODE, NODE, ...)` sets both `supertype` and `subtype` to `NODE` [do2.c:78-84]. This matters critically inside `findisatoinsertnonmolecule` (`granf2.c:203-242`):

```c
depth = hintptr->supertype == hintptr->subtype ? 1 : 2;
```

Since `NODE == NODE`, **depth = 1**. The server finds the last-allocated child of the hint and increments by one position:

```c
tumblerincrement(&hintptr->hintisa, depth, 1, isaptr);   // for the empty case
```

With `depth=1` and hint `1.1.0.1`, the first call appends `.1` → result is `1.1.0.1.1`. The second appends `.2` → `1.1.0.1.2`. Confirmed by `golden/accounts/create_multiple_nodes.json`:

```json
{"op": "create_node", "account": "1.1.0.1", "result": "1.1.0.1.1"},
{"op": "create_node", "account": "1.1.0.1", "result": "1.1.0.1.2"},
{"op": "create_node", "account": "1.1.0.1", "result": "1.1.0.1.3"}
```

---

### Document Addresses Under Accounts

For comparison: documents use `makehint(ACCOUNT, DOCUMENT, ...)` in `do1.c:239`:

```c
makehint(ACCOUNT, DOCUMENT, 0, &taskptr->account, &hint);
```

Here `ACCOUNT != DOCUMENT`, so **depth = 2** — the server inserts a `.0.` separator before the sequential number. Account `1.1.0.1` → first document `1.1.0.1.0.1`, second `1.1.0.1.0.2`. Confirmed by `golden/accounts/account_switch.json`.

The `.0.` separator is not a conceptual zero — it is a structural artifact of the `depth=2` increment: `tumblerincrement(hintisa, 2, 1, isaptr)` appends at two places past the last digit.

---

### The Hierarchy Is Arbitrarily Deep

The `node_then_documents.json` golden test proves the address hierarchy is recursive, not hardcoded to two levels:

```
account = 1.1.0.1
create_node(1.1.0.1) → 1.1.0.1.1     ← depth=1, single increment
account = 1.1.0.1.1
create_document() → 1.1.0.1.1.0.1    ← depth=2, adds .0.N
create_document() → 1.1.0.1.1.0.2
```

Any tumbler can serve as an account. The address space can nest arbitrarily: a "node" returned by `create_node` can itself be passed as an account to create sub-nodes or documents under it.

---

### Summary

| Question | Answer |
|----------|--------|
| Is `1.1` the node address fixed at server startup? | **No.** The backend initializes the account to zero at startup [`task.c:31`]. `1.1` is a client-supplied convention sent via `XACCOUNT`. |
| Is `1.1.0.N` allocated at account creation time? | **Partly.** The `1.1.0` prefix is client-supplied as a hint; the server appends the sequential `N` using `findisatoinsertnonmolecule` with `depth=1` (NODE/NODE) [`granf2.c:209`]. |
| Can these be assigned dynamically? | **Yes, fully.** There is no hardcoded root node. The backend is address-agnostic; `validaccount()` always returns `TRUE` [`get2fe.c:340`]. The server's only role is sequential allocation under whatever hint the client provides. |

The `Node.0.User.0.Doc` structure is not a two-level fixed schema enforced by the server. It is an emergent pattern from the combination of the client-supplied `1.1.0.N` account tumbler and the server's depth-1 (for nodes) vs. depth-2 (for documents) sequential allocation strategy in `findisatoinsertnonmolecule` [`granf2.c:203`].

---

## Question 16 [gregory]

> Can a user create a document under another user's account range (e.g., user `1.1.0.2` creating doc `1.1.0.3.0.5`), or does the backend enforce that document allocation stays within the creating user's own account subtree?

### Gregory's Answer

## KB Synthesis

The KB does not contain a finding that directly tests cross-account document creation (e.g., session with current account `1.1.0.2` attempting to allocate under `1.1.0.3`). But the architectural evidence across several entries points clearly to: **no, the backend does not enforce account ownership at allocation time.**

## What the KB says

**Account is session-local state, set by command.**
[SS-SESSION-STATE] describes `account` as per-session state. Any session can call `account(X)` for any `X`. There is no documented authentication or authorization check on that call.

**The allocation algorithm follows the hint, not the user.**
[SS-ADDRESS-ALLOC] / [PRE-ADDRESS-ALLOC] (Finding 0021): `findisatoinsertnonmolecule` takes a hint ISA derived from `makehint(ACCOUNT, DOCUMENT, ...)`. The hint is the *current session account* (`wheretoputit`). Bug 0013's fix added a *containment check* — after finding the candidate address, verify it is under the target parent. This check ensures correctness of placement within the specified account, not that the session is authorized to use that account.

**BERT is advisory, not enforced.**
[INT-BERT-FEBE] and [EC-RESPONSE-BEFORE-CHECK] (Finding 0050): The BERT access-control machinery is a cooperative protocol between front end and back end. For mutations, the back end sends the success response *before* executing the operation. A non-compliant front end can perform mutations on any document regardless of BERT state. The KB explicitly states: "system_correct ↔ (backend_correct ∧ all_frontends_compliant)."

**The subspace and account conventions are caller-enforced throughout.**
[INV-ACCOUNT-ISOLATION] (Finding 0021) is stated as an invariant maintained by the allocation algorithm, not by authorization logic. [INV-SUBSPACE-CONVENTION] is similarly caller-enforced with no runtime check. The pattern is consistent: the back end trusts the front end.

## Synthesis

If a session calls `account(1.1.0.3)`, the hint ISA becomes `1.1.0.3`, and the allocation algorithm will correctly place the new document at `1.1.0.3.0.1` (or the next available child). No check verifies that the session "belongs to" account `1.1.0.3`. The containment fix from Bug 0013 ensures the allocation is *internally correct* (the new address is genuinely under the specified account), but this is a correctness property of the allocator, not an access control gate.

The KB does not provide a golden test confirming this behavior, so the above is strong architectural inference rather than direct observation. If this matters for spec, a finding explicitly testing cross-account allocation would be needed to confirm.

---

## Code Exploration

I now have everything I need. Here is the complete answer.

---

## Answer: No Enforcement — Account Boundaries Are Not Checked

The backend does **not** enforce that a user creates documents within their own account subtree. The claim can be verified by tracing the full execution path from the `createnewdocument` request through to address allocation.

---

### Call Chain: `createnewdocument`

**`fns.c:276-286`**
```c
void createnewdocument(typetask *taskptr)
{
    getcreatenewdocument();
    if (docreatenewdocument (taskptr, &newdocisa))
        putcreatenewdocument (taskptr, &newdocisa);
    ...
}
```

`getcreatenewdocument()` takes **no parameters from the wire** — it is an empty stub in both `get1.c:158-160` and `get1fe.c:132`. The document address is never requested from the client here; it is derived entirely from `taskptr->account`.

**`do1.c:234-241`**
```c
bool docreatenewdocument(typetask *taskptr, typeisa *isaptr)
{
    typehint hint;
    makehint (ACCOUNT, DOCUMENT, 0, &taskptr->account, &hint);
    return (createorglingranf (taskptr, granf, &hint, isaptr));
}
```

The new document is allocated **as a child of `taskptr->account`** — whatever that is. The `hint` with `supertype=ACCOUNT`, `subtype=DOCUMENT` tells `findisatoinsertnonmolecule` (`granf2.c:203-242`) to find the next free slot under that account tumbler.

---

### How `taskptr->account` Is Populated

**`bed.c:123`**
```c
task.account = player[user].account;
```

Every time a request is dispatched, `task.account` is loaded from `player[user].account`. That field is set by the `XACCOUNT` command.

**`fns.c:364-373`**
```c
void xaccount(typetask *taskptr)
{
    if (getxaccount(taskptr,&(player[user].account))) {
        putxaccount(taskptr);
    }
    ...
}
```

**`get1fe.c:213-225`** (and identically `get1.c:190-203`)
```c
bool getxaccount(typetask *taskptr, typeisa *accountptr)
{
    gettumbler (taskptr, accountptr)
    && validaccount(taskptr, accountptr);
    player[user].account = *accountptr;
    taskptr->account = *accountptr;
    return(TRUE);
}
```

The client sends **any tumbler it wants** over the wire. `validaccount` is called, but:

**`get2.c:157-160`** (and `get2fe.c:338-341`)
```c
bool validaccount(typetask *taskptr, typeisa *accountptr)
{
    return (TRUE);
}
```

**`validaccount` is a stub that unconditionally returns `TRUE`.** No check is made against the current user's identity. The supplied account tumbler is accepted as-is and stored into `player[user].account`.

---

### The `isthisusersdocument` Check — Only Used for BERT Open State, Not Creation

`isthisusersdocument` appears in two places:

**`bert.c:81`**
```c
if (!foundnonread && (type == READBERT || isthisusersdocument(tp))) {
    return 0;
}
```

**`do1.c:270`**
```c
if (tumbleraccounteq(isaptr, wheretoputit) && isthisusersdocument(isaptr)) {
    makehint (DOCUMENT, DOCUMENT, 0, isaptr, &hint);
} else {
    makehint (ACCOUNT, DOCUMENT, 0, wheretoputit, &hint);
}
```

Both versions of `isthisusersdocument` compare a document's address against the current `player[user].account`:

**`socketbe.c:197-201`**
```c
int isthisusersdocument(tumbler *tp)
{
    return tumbleraccounteq(tp, &(player[user].account));
}
```

**`be.c:171-176`**
```c
int isthisusersdocument(tumbler *tp)
{
    bool result = tumbleraccounteq(tp, &taskptrx->account);
    return result;
}
```

But since `player[user].account` was set from the **user-supplied** `XACCOUNT` payload — with no validation — the "this user's document" check is trivially bypassed. Set `account = 1.1.0.2` via `XACCOUNT`, and `isthisusersdocument` will return true for all documents under `1.1.0.2`.

---

### `tumbleraccounteq` — What "Ownership" Means

**`tumble.c:38-70`**
```c
bool tumbleraccounteq(tumbler *aptr, tumbler *bptr)
{
    // Returns true if aptr's address falls under bptr's account subtree
    // by matching all non-zero positions of bptr against aptr
    for (j_b = 0, i = 0; i < NPLACES; i++) {
        if (bptr->mantissa[i] == 0) {
            if (++j_b == 2) return(TRUE);  // Account terminated
        } else {
            if (aptr->mantissa[i] != bptr->mantissa[i]) return(FALSE);
        }
    }
    return (TRUE);
}
```

This is a correct prefix-match — but it only enforces the check against `player[user].account`, which the user controls.

---

### Conclusion

**A user can create documents under any account subtree.** The mechanism that should prevent this — `validaccount` — is an **unconditional stub** (`return TRUE`) in every compilation path (`get2.c:157`, `get2fe.c:338`). Since `XACCOUNT` accepts any tumbler and stores it as the user's account, a client sending `XACCOUNT 1.1.0.2` followed by `createnewdocument` will allocate a document at e.g. `1.1.0.2.0.1` — inside user `1.1.0.2`'s address space — regardless of who is actually connected.

The access-control infrastructure (`checkforopen`, `isthisusersdocument`, `tumbleraccounteq`) is architecturally correct in design but operates entirely against the user-supplied, unvalidated account tumbler, making it ineffective as a security boundary.

---

## Question 17 [gregory]

> CREATENEWVERSION allocates the version under the source document if owned, or under the user's account if not — what exactly is the ownership test in `makehint`? Is it a tumbler prefix match between the session's account address and the source document's address?

### Gregory's Answer

## KB Synthesis

The KB gives a partial but clear answer.

## What the KB Says

[SS-VERSION-ADDRESS] Finding 0068 identifies the ownership predicate explicitly:

```c
tumbleraccounteq(isaptr, wheretoputit) && isthisusersdocument(isaptr)
```

Where:
- `isaptr` = address of the source document being versioned
- `wheretoputit` = the session's current account/context

[ST-VERSION-OWNERSHIP] adds the interpretive gloss: "ownership is determined by account prefix matching, not by an explicit permissions table."

## Is It a Prefix Match?

Yes — `tumbleraccounteq` compares the **account-level prefix** of both tumblers. [SS-TUMBLER-CONTAINMENT] tells us the general containment primitive is:

```c
tumblertruncate(&A, tumblerlength(&B), &truncated);
tumblereq(&truncated, &B);
```

`tumbleraccounteq` is a variant of this applied to the account field — the portion of the address up through the first `.0.` separator after the node component (e.g., `1.1.0.1` in `1.1.0.1.0.1`).

## The Two-Condition Check

The ownership gate is a conjunction:

1. **`tumbleraccounteq(isaptr, wheretoputit)`** — the source document's account prefix matches the session's current account. This is the prefix match you're asking about.

2. **`isthisusersdocument(isaptr)`** — a secondary check the KB doesn't elaborate further, but whose semantic role is to confirm the document "belongs to" the current user (as distinct from merely being in the same account).

## What the KB Does Not Provide

The exact implementation of `isthisusersdocument` is not in the KB — whether it checks orgl ownership flags, BERT entries, or something else is unresolved.

## Concrete Confirmation

From the examples in [SS-VERSION-ADDRESS] Finding 0068:
- User (account `1.1.0.1`) versions own doc `1.1.0.1.0.1` → both tumblers share account prefix `1.1.0.1` → predicate TRUE → child allocation `1.1.0.1.0.1.1`
- User B (account `1.1.0.2`) versions User A's doc `1.1.0.1.0.1` → account prefixes differ → predicate FALSE → account allocation `1.1.0.2.0.1`

So yes: `tumbleraccounteq` is a tumbler prefix match at the account level. The `isthisusersdocument` component adds an additional ownership check whose mechanism the KB doesn't fully expose.

---

## Code Exploration

I have everything I need. Let me now compile the complete answer.

---

## The Ownership Test in `docreatenewversion` / `makehint`

### Short answer

`makehint` itself contains **no ownership test** — it is a plain four-field struct initializer. The ownership test lives in `docreatenewversion` at `do1.c:270`, immediately **before** `makehint` is called. It is a two-part conjunction, both parts of which use `tumbleraccounteq`, which does perform a tumbler prefix match.

---

### `makehint` is just a struct initializer

`do2.c:78–84`:

```c
int makehint(INT typeabove, INT typebelow, INT typeofatom, typeisa *isaptr, typehint *hintptr)
{
    hintptr->supertype = typeabove;
    hintptr->subtype   = typebelow;
    hintptr->atomtype  = typeofatom;
    movetumbler(isaptr, &hintptr->hintisa);
}
```

It copies four values into a `typehint` struct. No comparison, no access control, no conditional logic. The interesting question is *which arguments* the caller passes — and that choice is determined by the ownership test upstream.

---

### The actual ownership test: `docreatenewversion` at `do1.c:268–276`

```c
/* ECH 7-13 introduced test for ownership to do right thing for explicit creation
   of new version of someone else's document */
if (tumbleraccounteq(isaptr, wheretoputit) && isthisusersdocument(isaptr)) {
    makehint (DOCUMENT, DOCUMENT, 0, isaptr/*wheretoputit*/, &hint);
} else {
    /* This does the right thing for new version of someone else's document, as it
       duplicates the behavior of docreatenewdocument */
    makehint (ACCOUNT, DOCUMENT, 0, wheretoputit, &hint);
}
```

Two conditions are ANDed:

1. **`tumbleraccounteq(isaptr, wheretoputit)`** — are the source document and the placement hint in the same account address space?
2. **`isthisusersdocument(isaptr)`** — does the source document belong to the current user?

---

### Caller always passes `isaptr == wheretoputit`

In `fns.c:295–296`:

```c
   getcreatenewversion(taskptr, &originaldocisa)
&& docreatenewversion(taskptr, &originaldocisa, &originaldocisa, &newdocisa)
```

Both `isaptr` and `wheretoputit` are `&originaldocisa` — the same address. Therefore condition 1 (`tumbleraccounteq(isaptr, wheretoputit)`) is a self-comparison and will always be TRUE for any well-formed document address (non-zero mantissa digits trivially match themselves, and the two-zero terminator is always eventually reached). **The only real discriminator is condition 2: `isthisusersdocument`.**

---

### `isthisusersdocument` — two implementations

**`be.c:171–175`** (single-user backend):

```c
int isthisusersdocument(tumbler *tp)
{
    bool result = tumbleraccounteq(tp, &taskptrx->account);
    return result;
}
```

**`socketbe.c:197–201`** (multi-user socket backend):

```c
int isthisusersdocument(tumbler *tp)
{
    /* was &(player[n_players].account)  !!!!!! GRRRR ECH */
    return tumbleraccounteq(tp, &(player[user].account));
}
```

Both delegate to `tumbleraccounteq(document_address, session_account_address)`.

---

### `tumbleraccounteq` — the prefix match algorithm

`tumble.c:38–70`:

```c
bool tumbleraccounteq(tumbler *aptr, tumbler *bptr)
{
    INT i, j_b;

    /* Check if sign matches */
    if (aptr->sign != bptr->sign) {
        return(FALSE);
    }

    /* Compare until account (bptr) terminates with two zeros.
       Document (aptr) may continue beyond the account's address space. */
    for (j_b = 0, i = 0; i < NPLACES; i++) {
        if (bptr->mantissa[i] == 0) {
            /* Account has a zero - check if it's the terminator (second zero) */
            if (++j_b == 2) {
                return(TRUE);  /* Account terminated, document is under this account */
            }
            /* First zero in account - document can have any value here */
        } else {
            /* Account has non-zero - document must match exactly */
            if (aptr->mantissa[i] != bptr->mantissa[i]) {
                return(FALSE);
            }
        }
    }
    return (TRUE);
}
```

The algorithm:

1. **Sign must match.**
2. Walk `bptr` (the account/reference address) digit by digit.
3. For each **non-zero** digit in `bptr`, `aptr` must have the **identical digit** at that position.
4. For each **zero** in `bptr`, the position is skipped (any digit in `aptr` is acceptable there), but a zero counter is incremented.
5. When **two zeros** are seen in `bptr`, the account address has terminated — return TRUE immediately. The document address is "under" this account.

**Yes — this is a tumbler prefix match**, but the "prefix" is defined by the non-zero digits of the account address rather than by simple leading-digit count. Zeros in the account address act as delimiters/wildcards, and the double-zero signals end-of-prefix.

---

### What the two `makehint` calls actually mean

| Condition | Call | Effect on allocation |
|-----------|------|---------------------|
| Source doc **is** owned by current user | `makehint(DOCUMENT, DOCUMENT, 0, isaptr, &hint)` | New version allocated as a child of the source document (DOCUMENT → DOCUMENT nesting) |
| Source doc **is not** owned by current user | `makehint(ACCOUNT, DOCUMENT, 0, wheretoputit, &hint)` | New version allocated under the user's own account (ACCOUNT → DOCUMENT nesting, same as `docreatenewdocument`) |

The `supertype`/`subtype` fields of the hint are used by `createorglingranf` (called at `do1.c:277`) to determine where in the granfilade tree to insert the new document ISA.

---

### Summary

The ownership test is **not in `makehint`**. `makehint` is inert. The ownership gate lives at `do1.c:270`. Since the caller (`fns.c:296`) always passes the same address for both `isaptr` and `wheretoputit`, the effective test is a single question: does `tumbleraccounteq(source_doc_address, current_user_account_address)` return TRUE?

That function implements a **prefix match**: signs must agree; every non-zero mantissa digit of the account address must equal the corresponding digit in the document address; the match succeeds when the account address terminates at its double-zero sentinel. A document is "owned" by a user if and only if the user's account tumbler is a valid prefix of the document's tumbler in this sense.

---

## Question 18 [gregory]

> Is there a CREATEDOCUMENT operation distinct from the first INSERT into a new address, or does the document implicitly come into existence when content is first inserted — i.e., does the POOM get created lazily on first write?

### Gregory's Answer

## KB Synthesis

There is a distinct CREATEDOCUMENT operation — documents do not come into existence lazily.

**Evidence for explicit creation:**

[ST-VERSION-CREATE] Finding 0032 directly contrasts the two mechanisms: "This atomicity distinguishes it from the two-step CREATEDOCUMENT + COPY sequence, which has an observable intermediate state (empty document exists)." This confirms CREATEDOCUMENT is a distinct protocol operation that produces an empty-but-existent document before any content is inserted.

[SS-GRANF-OPERATIONS] Finding 0012 lists `createorglingranf()` as the operation that "creates a new orgl (used for documents and links)." This is called at creation time, not deferred.

[EC-EMPTY-DOC] Finding 0058 identifies two structurally distinct empty states:
- **Never-filled** (`createenf` output): height-1 tree with one zero-width bottom node
- **After delete-everything**: taller tree with empty intermediates, no bottom nodes

The never-filled state is the initial state established at document creation. The POOM is created eagerly via `createenf(POOM)` at that point. This distinction matters operationally: Finding 0064/Bug 0019 shows that inserting into a delete-everything document crashes, because `firstinsertionnd` assumes a bottom crum exists (true for never-filled, false for delete-everything).

[ST-ADDRESS-ALLOC] Finding 0021 establishes that address allocation via `findisatoinsertnonmolecule` happens at creation time, producing a new document address under the parent account. There is no mechanism for lazy address assignment.

[PRE-OPEN-DOC] Finding 0014 requires documents to be opened (BERT token acquired) before mutations. Opening requires the document to already exist in the BERT table and the open list — another precondition that requires prior creation.

**Summary:** CREATEDOCUMENT is a distinct operation that (1) allocates a document address via `findisatoinsertnonmolecule`, (2) creates a document orgl via `createorglingranf`, and (3) initializes a minimal POOM via `createenf(POOM)`. The resulting document has an empty but structurally valid POOM. Subsequent INSERT operations use `firstinsertionnd` to add the first content into this pre-existing structure.

---

## Code Exploration

I now have everything I need. Here is my full answer.

---

## Answer: CREATENEWDOCUMENT is a Real, Distinct, Mandatory Operation

Documents are **not** created lazily on first INSERT. There is an explicit `CREATENEWDOCUMENT` operation (opcode 11), and inserting into a document address that was never created will **immediately fail** — not create anything implicitly.

---

### 1. CREATENEWDOCUMENT is a registered protocol operation

`requests.h:28`:
```c
#define CREATENEWDOCUMENT 11
```

`init.c:52`:
```c
requestfns[CREATENEWDOCUMENT] = createnewdocument;
```

Its get/do/put pipeline:

- **`fns.c:276-286`** — `createnewdocument()`, the top-level handler
- **`get1fe.c:131-136`** — `getcreatenewdocument()` takes no arguments — there is nothing to receive from the client; just logging and emitting the opcode
- **`do1.c:234-241`** — `docreatenewdocument()` — does the actual work
- **`putfe.c:305-314`** — `putcreatenewdocument()` — sends the newly allocated address back

---

### 2. What CREATENEWDOCUMENT actually creates — the POOM

`do1.c:239-240`:
```c
makehint (ACCOUNT, DOCUMENT, 0, &taskptr->account, &hint);
return (createorglingranf (taskptr, granf, &hint, isaptr));
```

The hint type is `ACCOUNT → DOCUMENT`: "find the next available DOCUMENT slot beneath the user's ACCOUNT address."

`createorglingranf()` → `createorglgr()` at `granf2.c:111-128`:
```c
if (!findisatoinsertgr ((typecuc*)fullcrumptr, hintptr, isaptr))
    return (FALSE);
locinfo.infotype = GRANORGL;
locinfo.granstuff.orglstuff.orglptr = createenf (POOM);   // ← allocates the POOM
reserve ((typecorecrum*)locinfo.granstuff.orglstuff.orglptr);
locinfo.granstuff.orglstuff.orglincore = TRUE;
locinfo.granstuff.orglstuff.diskorglptr.diskblocknumber = DISKPTRNULL;
insertseq ((typecuc*)fullcrumptr, isaptr, &locinfo);       // ← registers in granfilade
```

`createenf(POOM)` allocates a fresh, empty enfilade tree (the POOM — **Permutation Of Ordered Material** — the tree structure that holds a document's content in V-space). This tree is inserted into the granfilade at the newly computed address, which is returned to the caller as the document's permanent ISA (e.g., `1.1.0.1.0.2`).

---

### 3. Why INSERT fails if CREATENEWDOCUMENT was never called

`doinsert()` at `do1.c:117-119`:
```c
makehint(DOCUMENT, ATOM, TEXTATOM, docisaptr, &hint);
ret = (inserttextingranf(taskptr, granf, &hint, textset, &ispanset)
    && docopy (taskptr, docisaptr, vsaptr, ispanset));
```

The hint subtype is `ATOM`. This flows to `inserttextingranf()` → `inserttextgr()` → `findisatoinsertgr()`.

**The decisive guard** at `granf2.c:134-141`:
```c
/* For ATOM types (text/link content), we need a document to exist first */
if (hintptr->subtype == ATOM) {
    if (!isaexistsgr (fullcrumptr, &hintptr->hintisa)) {
#ifndef DISTRIBUTION
        fprintf (stderr,"nothing at hintisa for atom\n");
#endif
        return (FALSE);
    }
    findisatoinsertmolecule (fullcrumptr, hintptr, isaptr);
```

`isaexistsgr()` (at `granf2.c:244-253`) does a live lookup in the granfilade tree for the document's tumbler address. If no `GRANORGL` node exists at that address — because `CREATENEWDOCUMENT` was never called — it returns `FALSE`, which propagates up through `inserttextgr` → `inserttextingranf` → `doinsert` as a hard failure. There is **no fallback, no auto-create path**.

---

### 4. A second guard: the OPEN check

Even if the document's granfilade node *does* exist, `docopy()` (also called from `doinsert`) calls `findorgl()`, which enforces the bert open table:

`granf1.c:22-38`:
```c
if ((temp = checkforopen(isaptr, type, user)) <= 0) {
    ...
    *orglptr = NULL;
    return FALSE;
}
*orglptr = fetchorglgr(taskptr, granfptr, isaptr);
return (*orglptr ? TRUE : FALSE);
```

`checkforopen()` in `bert.c:52-87` returns 0 for "sufficiently open" owned documents that are not yet in the bert table, or -1 when write access is needed but blocked. A document must be opened with `OPEN` (opcode 35, `doopen()`) before its POOM can be fetched. `findorgl` with `WRITEBERT` will fail unless the connection holds a write-open entry in the bert hash table.

The complete mandatory sequence to insert into a document is therefore:
1. **`CREATENEWDOCUMENT`** → allocates POOM, registers in granfilade, returns address
2. **`OPEN`** → adds bert entry (with `WRITEBERT` type) for this connection
3. **`INSERT`** → both guards pass; text is placed in the POOM and V-span recorded

---

### 5. Internal code confirms the same pattern

`xumain.c:127-144` — the `sourceunixcommand` handler, which bulk-loads text, calls `docreatenewdocument()` explicitly before entering the insert loop:
```c
docreatenewdocument (taskptr, &docisa);
putcreatenewdocument (taskptr, &docisa);
...
while (...) {
    doappend (taskptr, &docisa, textsetptr);
```

Even in this internal path, document creation must precede content insertion.

---

### Conclusion

The POOM — the enfilade tree that stores a document's content — is **eagerly allocated** by `CREATENEWDOCUMENT` via `createenf(POOM)` and registered in the granfilade at a new permanent address. There is no lazy creation. The `findisatoinsertgr` guard at `granf2.c:135-141` explicitly checks `isaexistsgr` before allowing any atom (text or link) insertion, and returns `FALSE` with the message `"nothing at hintisa for atom"` if the document node is absent. No INSERT operation has any code path that would create a document node as a side effect.

---

## Question 19 [gregory]

> When multiple FEBE sessions have the same document open with READBERT, and one session upgrades to WRITEBERT, does `checkforopen` reject the upgrade while other readers hold the document, or is there no upgrade path (must close and reopen)?

### Gregory's Answer

## KB Synthesis

Based on the KB, there is **no upgrade path** — the session must close and reopen.

From [PRE-OPEN-DOC] Finding 0014, `checkforopen` returns -1 (denied) for:

> **WRITE request on a document open for READ by any connection → -1 (denied)**

The rule says "any connection" with no carve-out for same-connection upgrades. When other sessions hold READBERT, a WRITE request from the upgrading session still hits this rule and is denied.

Finding 0006 in [PRE-OPEN-DOC] confirms the consequence:

> "To change access mode, the document must be closed and reopened."

The only asymmetric case is the reverse direction: READ requests from the same connection that holds WRITE get silently upgraded to WRITE (`checkforopen` returns WRITE). The downgrade/upgrade path in the opposite direction (READ→WRITE) does not exist.

Combined with [INV-WRITE-EXCLUSIVITY]: write requires that no other connection holds any access. So even if only the requesting session holds READBERT, upgrading in-place to WRITEBERT is not supported by the access matrix — the session must close its READ handle first, after which `checkforopen` can issue the WRITE token if no other readers remain.

---

## Code Exploration

---

## Answer: READBERT-to-WRITEBERT Upgrade in `checkforopen`

**There is no upgrade path.** `checkforopen` rejects same-connection WRITEBERT requests when READBERT is already held, and the data model has no mechanism to promote an existing entry. A session must close and reopen.

Here is the full code trace.

---

### 1. The `bertentry` struct has a fixed `type` field

`bert.c:13–19`:
```c
typedef struct {
    int connection;
    tumbler documentid;
    char created,modified;
    int type;          // READBERT=1 or WRITEBERT=2
    int count;
} bertentry;
```

`addtoopen` (`bert.c:128`) creates a new entry with a fixed type. There is no `upgradeopen`, `modifyopen`, or mutation of `bert->type` anywhere in the codebase — the type is immutable after creation.

---

### 2. Same connection: `checkforopen` returns -1 for WRITEBERT when READBERT is held

`bert.c:66–72`:
```c
if (connection == bert->connection) {
    switch (bert->type) {
        case READBERT:
            return (type == READBERT) ? READBERT : /* WRITE */ -1;
        case WRITEBERT:
            return WRITEBERT;
    }
}
```

When the **same connection** that holds READBERT calls `checkforopen(..., WRITEBERT, connection)`:
- `connection == bert->connection` → TRUE
- `bert->type == READBERT` → matches `case READBERT`
- `type == READBERT` is FALSE (requesting WRITEBERT)
- Returns **-1** ("new version should be made")

This is also confirmed by the inline comment table at `bert.c:44–50`:
```
type         Open READ  conn==   →  WRITE request → -1
```

---

### 3. What `-1` means in `doopen` — no in-place upgrade, only version fork

`bert.c:279–299`:
```c
openState = checkforopen(tp, type, connection);

if (openState == 0) {
    addtoopen(tp, connection, FALSE, type);   // normal open
    return 1;
}

switch (mode) {
case BERTMODECOPYIF:
    if (openState == -1) {
        docreatenewversion(taskptr, tp, ...);  // forks a new version
        addtoopen(newtp, connection, TRUE, type);
    }
    ...
case BERTMODEONLY:
    if (openState == -1 || openState == WRITEBERT) {
        return 0;   // FAIL — no upgrade, no fork
    }
```

- **`BERTMODECOPYIF` + -1**: triggers `docreatenewversion`, opening a *new document version* as WRITEBERT. The original READBERT entry is untouched.
- **`BERTMODEONLY` + -1**: returns 0 (failure). The `myopen` handler in `fns.c:394–401` then sends `putrequestfailed`.

Neither path promotes the existing READBERT entry to WRITEBERT. There is no fork-free upgrade.

---

### 4. Cross-connection case: readers don't block a different writer (if owner)

When **other** connections hold READBERT and a **different** connection requests WRITEBERT:

`bert.c:73–77`:
```c
} else {
    if (bert->type != READBERT) {
        foundnonread = TRUE;
    }
}
```

Other connections' READBERT entries are silently skipped — they do **not** set `foundnonread`. After the loop:

`bert.c:81–85`:
```c
if (!foundnonread && (type == READBERT || isthisusersdocument(tp))) {
    return 0;
} else {
    return -1;
}
```

`isthisusersdocument` (`socketbe.c:197–201`) checks `tumbleraccounteq(tp, &(player[user].account))` — whether the document's tumbler account matches the requesting user's account.

- **Document is owned by requester**: returns 0 → `doopen` calls `addtoopen(..., WRITEBERT)`, creating a *new* independent WRITEBERT entry alongside the existing READBERT entries. **Both entries coexist in the bert table** — there is no reader/writer mutual exclusion enforced at this layer.
- **Document not owned by requester**: returns -1 → COPYIF creates a fork, ONLY fails.

---

### 5. No `upgradeopen` anywhere

A complete grep confirms there is no function that mutates `bert->type`:
- `addtoopen` (`bert.c:128`): sets type at creation, never modifies it
- `incrementopen` (`bert.c:112`): only touches `bert->count`
- `removefromopen` (`bert.c:154`): removes the entry entirely
- `exitbert` (`bert.c:195`): bulk cleanup on disconnect

---

### Summary

| Scenario | `checkforopen` result | Outcome |
|---|---|---|
| Same connection holds READBERT, requests WRITEBERT | -1 | COPYIF: new version forked as WRITEBERT. ONLY: failure. |
| Different connection holds READBERT, same user requests WRITEBERT | 0 (if owner) | New WRITEBERT entry added; READBERT entry remains — no mutual exclusion |
| Different connection holds READBERT, different user requests WRITEBERT | -1 | COPYIF: new version. ONLY: failure. |

**The answer is: there is no upgrade path.** `checkforopen` returns -1 when the same connection already holds READBERT and requests WRITEBERT (`bert.c:69`). The only way to hold WRITEBERT is to either (a) close the READBERT first and reopen as WRITEBERT with a fresh `doopen` call, or (b) use `BERTMODECOPYIF` which forks an entirely new document version rather than upgrading in place.

---

## Question 20 [gregory]

> Is there any mechanism to enumerate all documents in the system — for example, can a session walk the granfilade's document-level address range to discover existing documents, or is document discovery limited to `FINDDOCSCONTAINING` via shared I-addresses?

### Gregory's Answer

## KB Synthesis

Based on the KB, the short answer is: **no general document enumeration mechanism is documented in the FEBE protocol**. Document discovery is limited to content-identity-based lookup.

## What the KB documents

**FINDDOCSCONTAINING** is the only reverse-lookup operation [SS-DOCISPAN]. It queries the DOCISPAN sub-index in the spanfilade — `Map<ISpan, Set<DocISA>>` — to find documents that contain specific I-address ranges. This requires knowing *what content* you're looking for, not "show me everything." [SS-SPANF-OPERATIONS] confirms the spanfilade supports only insertion and range-query; there's no "enumerate all" operation.

**Granfilade structure** does encode all document addresses in a hierarchical B-tree [SS-ADDRESS-ALLOC], [SS-ADDRESS-SPACE]. The internal allocation mechanism `findpreviousisagr` traverses this tree to find the highest existing address under a parent prefix — which is a bounded walk of a sub-tree. In principle this traversal could enumerate all documents under an account. But this is an **internal allocation primitive**, not a user-facing operation. The FEBE request dispatch table (`init.c:requestfns`) doesn't include any such enumeration opcode.

**Tumbler containment** [SS-TUMBLER-CONTAINMENT] provides the predicate `contains(prefix, addr)` via truncation-and-compare, which would be the building block for any address-space walk. But no FEBE operation exposes this as a query.

**Address monotonicity** [INV-MONOTONIC] means the granfilade address sequence is gapless and grows predictably — you could in principle probe `account.0.1`, `account.0.2`, etc. But the system provides no documented way to ask "what is the next valid document address after X?" at the FEBE level.

## What this implies for spec

Document discovery is entirely **content-identity-driven**:
- You find documents by content they've ever contained, via FINDDOCSCONTAINING [INV-IADDRESS-PERMANENT]
- The spanfilade is write-only and append-only [INV-SPANF-WRITE-ONLY], so it accumulates provenance but supports no iteration
- There is no document directory or catalog object

If you need to enumerate your own documents, the only viable path through the documented interface is knowing that your documents are allocated under your account address (e.g., `1.1.0.2.0.1`, `1.1.0.2.0.2`, ...) and probing sequentially — but the KB documents no FEBE opcode to support even that efficiently. The internal `findpreviousisagr` exists, but only as part of the allocation path [SS-ADDRESS-ALLOC].

This is a significant capability gap: the system can answer "which documents contain X?" but not "what documents exist?"

---

## Code Exploration

I now have everything needed. Here is the full answer.

---

## Document Enumeration in udanax-green

### Short answer

**No.** There is no mechanism for a session to enumerate all documents in the system. The granfilade exposes only point-lookup access; it has no range-walk interface through FEBE. Document discovery is entirely mediated by `FINDDOCSCONTAINING` — which itself requires that you already possess I-addresses.

---

### The complete FEBE operation table

From `init.c:43–75`, the full set of registered request handlers is:

```
COPY, INSERT, RETRIEVEDOCVSPANSET, REARRANGE, RETRIEVEV,
NAVIGATEONHT, SHOWRELATIONOF2VERSIONS, CREATENEWDOCUMENT,
DELETEVSPAN, CREATENEWVERSION, RETRIEVEDOCVSPAN, QUIT,
SOURCEUNIXCOMMAND, FOLLOWLINK, FINDDOCSCONTAINING, CREATELINK,
RETRIEVEENDSETS, FINDNUMOFLINKSFROMTOTHREE, FINDLINKSFROMTOTHREE,
FINDNEXTNLINKSFROMTOTHREE, CREATENODE_OR_ACCOUNT, OPEN, CLOSE,
XACCOUNT, DUMPSTATE
```

There is no `LISTDOCUMENTS`, `ENUMERATEDOCUMENTS`, `NEXTDOCUMENT`, or any range-scan operation.

---

### What `FINDDOCSCONTAINING` actually does

```
finddocscontaining [fns.c:20]
  → dofinddocscontaining [do1.c:15]
      → specset2ispanset [do2.c:14]       (convert V-specs to I-spans)
      → finddocscontainingsp [spanf1.c:151]
```

`finddocscontainingsp` [spanf1.c:151–188] works as follows:

1. Accepts an `ispanset` — a set of I-address ranges.
2. Sets `docspace` to the `DOCISPAN` slice of the ORGLRANGE dimension [spanf1.c:168–169]:
   ```c
   tumblerincrement (&docspace.stream, 0, DOCISPAN, &docspace.stream);
   tumblerincrement (&docspace.width, 0, 1, &docspace.width);
   ```
3. For each I-span, calls `retrieverestricted(spanf, &docspace, ORGLRANGE, ispanset, SPANRANGE, NULL)` [spanf1.c:171] — querying the 2D spanfilade for entries where the ORGLRANGE dimension falls in the document slice **and** the SPANRANGE dimension intersects the given I-span.
4. Extracts the document address from `c->totaloffset.dsas[ORGLRANGE]` [spanf1.c:173–174] and strips the DOCISPAN prefix with `beheadtumbler`.

The critical constraint: **this operation is entirely input-driven by I-addresses you already hold.** Without prior I-addresses, you cannot call it meaningfully. It answers "which documents contain this content?", not "what documents exist?"

---

### The granfilade is a point-lookup structure

The granfilade (`granf`, typed `typegranf = INT *` [xanadu.h:13]) is a sequential enfilade (GRAN type) indexed by document tumblers. Document addresses are allocated as sub-tumblers of an account:

- `docreatenewdocument` [do1.c:234–241] calls `makehint(ACCOUNT, DOCUMENT, ...)` with `taskptr->account` as the hint address.
- `findisatoinsertnonmolecule` [granf2.c:203–242] allocates the next free address by calling `findpreviousisagr` to find the highest existing address under the account, then incrementing. Documents under account `1.1` land at `1.1.0.1`, `1.1.0.2`, etc.

But `findpreviousisagr` [granf2.c:255–278] is an **internal allocation helper** — it is never exposed through FEBE. It is called only from `findisatoinsertnonmolecule` during document creation.

The only publicly accessible granfilade lookup is `fetchorglgr` [granf2.c:22–81], called from `findorgl` [granf1.c:17–41], called from every operation that needs to open a document's POOM. It performs an exact-match lookup:

```c
if (!tumblereq((tumbler*)&context->totaloffset, address)) {
    crumcontextfree(context);
    return (NULL);   /* [granf2.c:37–39] */
}
```

If the address does not exist in the granfilade, `fetchorglgr` returns NULL. There is no "next document" or "iterate" path.

---

### Can a session probe sequential addresses?

Theoretically, a session could guess addresses (`account.0.1`, `account.0.2`, …) and issue `RETRIEVEDOCVSPANSET` or `OPEN`. But:

- `OPEN` → `doopen` [bert.c:264] calls `checkforopen` [bert.c:52]. If the document is not open and is owned by you (`isthisusersdocument` [be.c:171–176] checks `tumbleraccounteq`), `checkforopen` returns 0 ("open required"), and `doopen` adds it to the bert table and **returns success** — even if the address does not correspond to any real document in the granfilade. The existence check only fires later, when `findorgl` is called.

- `RETRIEVEDOCVSPANSET` → `doretrievedocvspanset` → `findorgl` → `fetchorglgr`. If `fetchorglgr` returns NULL (no document at that address), the operation fails. But the failure is indistinguishable from a permissions failure; there is no "does not exist vs. not accessible" distinction exposed to the client.

More fundamentally: probing sequential addresses would require knowing the account prefix, knowing the per-account document numbering increment, and the numbers are contiguous only within a single account's creation sequence. Across accounts, addresses are disjoint by the tumbler hierarchy.

---

### `findpreviousisagr` — the closest thing to a range scan

`findpreviousisagr` [granf2.c:255–278] does walk the granfilade tree to find the highest address below a given upper bound:

```c
for (ptr = findleftson((typecuc*)crumptr); ptr; ptr = findrightbro(ptr)) {
    if (
     (tmp= whereoncrum (ptr, (typewid*)offset, upperbound, WIDTH)) == THRUME
    || tmp == ONMYRIGHTBORDER
    || !ptr->rightbro) {
        findpreviousisagr (ptr, upperbound, offset);   /* [granf2.c:272] */
        return(0);
    } else {
        tumbleradd(offset, &ptr->cwid.dsas[WIDTH], offset);  /* [granf2.c:275] */
    }
}
```

This is a recursive descent that could, in principle, be iterated to enumerate all existing document addresses. But it is **not exposed through any FEBE request**. It is used solely in `findisatoinsertnonmolecule` [granf2.c:217] to allocate the next document address. A client session has no way to invoke it.

---

### The architectural conclusion

The design is intentional. Udanax-green's document model assumes the transclusion graph as the navigation primitive:

1. You know a document address (you created it, or were told it).
2. You retrieve content → get I-addresses.
3. You use `FINDDOCSCONTAINING` with those I-addresses to find all documents that include the same content.
4. You follow links with `FOLLOWLINK` / `FINDLINKSFROMTOTHREE` to discover related documents.

The system has no concept of a "document directory" or "document namespace" that can be walked. The granfilade is a sparse address space, not a list. Document discovery is exclusively I-address–mediated: you can only find documents you are already connected to through the content graph.

The `FINDDOCSCONTAINING` operation is the **ceiling** of what the system offers for discovery — and it requires possession of I-addresses as a prerequisite, not an output.
