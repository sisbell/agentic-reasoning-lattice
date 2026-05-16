# Consultation Answers — CREATELINK Operation

**Inquiry:** What is the precise effect of creating a new link with endsets referencing Istream content? What is allocated, what is indexed, and what invariants must the completed operation maintain?
**Date:** 2026-03-21 17:10
**Questions:** 20 (10 nelson, 10 gregory)

---

## Question 1 [nelson]

> When a new link is created, does the link itself become permanent content with its own identity, or is it a mutable annotation that can be withdrawn?

### Nelson's Answer

## Links Are Permanent Content — But Owners Can "Delete" Them

A link, once created, is **permanent content with its own identity**. It is also **withdrawable by its owner** — but "withdrawal" in Xanadu means the same thing as "deletion" of bytes: removal from the current view, not destruction from existence.

### Links Are First-Class Stored Entities

Links are one of only two things actually stored in tumbler-space:

> "In the present implementation (XU.87.1), the only entities actually stored in tumbler-space are content bytes and links." [LM 4/23]

Each link has its own permanent tumbler address in the `2.x` subspace of its home document, and these addresses are permanently ordered by creation:

> "The links designated by a tumbler address are in their permanent order of arrival." [LM 4/31]

Unlike bytes, which can be rearranged in Vstream, **links keep their creation-order addresses permanently**. Link `2.1` is always the first link created in that document; link `2.755` is always the 755th. Deleting link `2.5` does not renumber `2.6` onward.

Because links have addresses, they can be targets of other links:

> "Because of the universality of tumbler-space, and the fact that links are located there as well as data, it becomes easy for a link to point at another link." [LM 4/49]

This confirms links have the same ontological status as content — addressable, referenceable, linkable.

### Owners Can Delete Links — But Deletion Is Not Destruction

Nelson explicitly includes "DELETED LINKS" as a valid document state on page 4/9, with language identical to deleted bytes:

> "DELETED LINKS (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

This follows the same non-destructive semantics as byte deletion. Only the owner of the link's home document can delete it:

> "A link need not point anywhere in its home document. Its home document indicates who owns it, and not what it points to." [LM 4/12]

> "Only the owner has a right to withdraw a document or change it." [LM 2/29]

So if Alice creates a comment link pointing to Bob's document, **Bob cannot delete Alice's link** — it lives at Alice's address. Alice can delete it, but even then it remains in Istream, recoverable through historical backtrack, and may persist in other versions of Alice's document.

### The Parallel with Bytes

| Property | Bytes | Links |
|----------|-------|-------|
| Stored in tumbler-space | Yes | Yes |
| Has permanent I-address | Yes | Yes |
| Owner can "delete" | Yes | Yes |
| Deletion removes from Istream | No | No |
| Recoverable via historical backtrack | Yes | Yes |
| May persist in other versions | Yes | Yes |
| Rearrangeable in Vstream | Yes | **No** — permanent order of arrival |

Links are actually **more permanent** than bytes in one respect: bytes can be rearranged within a document's Vstream, but links maintain their creation-order addresses forever.

### Summary

A link is permanent content with its own identity. Its creator can withdraw it from the current version of their document, but this is Vstream deletion — the link remains in Istream, is recoverable through historical backtrack, and may survive in other versions. The link's tumbler address is never reused or reassigned. In this sense, a link is not a "mutable annotation" — it is an immutable record that can be hidden from view but never truly destroyed.

---

## Question 2 [nelson]

> Must the system guarantee that a newly created link is immediately visible to all users who retrieve any content referenced by that link's endsets?

### Nelson's Answer

## No — Nelson Does Not Guarantee Immediate Link Visibility

Nelson specifies that link discovery should be *fast* and that the docuverse should *appear unified*, but he does not guarantee that a newly created link is immediately visible to all users across the network. Several aspects of his design actively work against such a guarantee.

### What Nelson DOES Say About Link Discovery Timing

The closest statement to a visibility guarantee is about *querying* existing links, not about propagation after creation:

> "The reader should be able to ask, for a given document or place in the document, 'What connects here from other documents?'— and be shown all these outside connections without appreciable delay." [LM 2/46]

"Without appreciable delay" addresses **query latency**, not **propagation latency**. It says: once the system knows about a link, finding it should be fast. It does not say: the system must know about a link everywhere instantly after creation.

### What Works Against Immediate Visibility

**1. Networks are assumed broken.**

> "It is a truism that 'computer networks are always broken.' Meaning that on the average some nodes are disconnected or not working." [LM 4/75]

If nodes are routinely disconnected, immediate global visibility is physically impossible. Nelson builds this assumption into the architecture rather than fighting it.

**2. Servers hold subrepresentations, not complete state.**

> "Each server contains a map and a subset of the whole — a microcosm that shrinks and grows." [LM 4/71]

> "Each server contains a continuously valid model or subrepresentation of the entire docuverse." [LM 4/72]

"Continuously valid" means internally consistent — not globally synchronized. Each server's view is correct for what it contains, but it doesn't contain everything.

**3. Content (and by extension, links) propagate gradually.**

> "A server's network model, from the null case on up, is at all times unified and operational; whatever information moves between servers is assimilated at once to its overall structure, leaving each server in canonical operating condition with a slightly improved map of what is elsewhere. The contents can slosh back and forth dynamically." [LM 4/72]

"Slosh back and forth dynamically" and "slightly improved map" describe eventual consistency — the network converges over time, not instantly. Material moves between servers for performance and redundancy reasons:

> "Material is moved between servers for a number of purposes: 1. for more rapid access to final material, 2. for more rapid access to needed material which indexes material on other servers, 3. for rebalance in keeping with demand, 4. for redundancy and backup purposes." [LM 4/71]

**4. The "inter-indexing mechanisms" are back-end maintenance, not real-time broadcast.**

> "A Xanadu link is a connective unit, a package of connecting or marking information. It is owned by a user. It is put in by a user (or a front end), and thereafter maintained by the back end through the back end's inter-indexing mechanisms." [LM 4/41]

"Thereafter maintained" implies ongoing maintenance — the back end keeps indexes up to date over time, not that index updates are instantaneous and global.

### The Local vs. Distributed Case

Nelson's FEBE protocol presents commands as request-response pairs (MAKELINK returns a link ID, FINDLINKSFROMTOTHREE returns matching links). For a single back-end server, the natural reading is that a created link is findable on subsequent queries to that same server. But Nelson does not explicitly state even this local guarantee.

For the distributed case, the architecture clearly contemplates delay. A link created on server A will become visible to users on server B through the BEBE forwarding and subrepresentation mechanisms — but on a timeline governed by network health, demand patterns, and caching, not by a hard consistency bound.

### What Nelson Guarantees Instead

Rather than immediate visibility, Nelson guarantees:

1. **Efficient search** — "THE QUANTITY OF LINKS NOT SATISFYING A REQUEST DOES NOT IN PRINCIPLE IMPEDE SEARCH ON OTHERS." [LM 4/60]

2. **Scalable performance** — the "soft corridor" ensures query times grow logarithmically, not linearly, as the docuverse expands [LM 4/2]

3. **Eventual completeness** — through subrepresentation growth and BEBE forwarding, links will propagate to servers where they're needed

4. **Resilience** — the system handles partial network failure gracefully rather than requiring global consistency

### Summary

Nelson designs for a world where link creation is local and link discovery is eventually global. The system prioritizes **availability and partition tolerance** over **immediate consistency** — a choice forced by his explicit assumption that "networks are always broken." The user-facing promise is that links are discoverable "without appreciable delay" once the system knows about them, not that the system knows about them everywhere the instant they are created.

---

## Question 3 [nelson]

> Does creating a link allocate new content storage for the link's own structure, or does the link exist purely as an index entry over existing content?

### Nelson's Answer

## Links Are Stored Entities, Not Mere Index Entries

Creating a link **allocates new storage** in tumbler-space. A link is a concrete, addressable object — not a derived index over existing content.

### The Direct Evidence

Nelson is explicit that links and content bytes are the **only two kinds of stored entities**:

> "In the present implementation (XU.87.1), the only entities actually stored in tumbler-space are content bytes and links. While a number on the line may represent a document or an account, that doesn't mean there's an object stored for it. What's stored is the contents--bytes and links." [LM 4/23]

Links have their own addresses in a document's element subspace. From the link address structure:

```
N.0.U.0.D.V.0.2.1    → first link in document
N.0.U.0.D.V.0.2.755  → 755th link in document
```

> "The links designated by a tumbler address are in their permanent order of arrival." [LM 4/31]

And from the link-to-link discussion, the storage status is stated directly:

> "Because of the universality of tumbler-space, and the fact that links are located there as well as data, it becomes easy for a link to point at another link." [LM 4/49]

### What Gets Stored

A link is described as:

> "A Xanadu link is a connective unit, a package of connecting or marking information. It is owned by a user. It is put in by a user (or a front end), and thereafter maintained by the back end through the back end's inter-indexing mechanisms." [LM 4/41]

The stored structure contains the three endsets (from-set, to-set, type) — each an arbitrary span-set referencing addresses elsewhere in the docuverse. The endsets are **pointers** to existing content; they don't copy the content. But the link itself — the "package" holding those three pointers together — is a newly allocated stored object.

MAKELINK confirms this: it creates a new entity and returns its identity:

> "This creates a link in document \<doc id\> from \<from set\> to \<to set\> connected to \<three set\>. It returns the id of the link made." [LM 4/68]

### Links Parallel Bytes in Every Way

The document's technical contents (page 4/9) list two parallel categories:

| Category | Stored? | Has addresses? | Can be "deleted"? |
|----------|---------|-----------------|-------------------|
| **Bytes** | Yes | Yes (byte subspace) | Yes — enters historical backtrack state |
| **Links** | Yes | Yes (link subspace) | Yes — enters historical backtrack state |

> "DELETED LINKS (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

This is the same language used for deleted bytes. Both are permanent entries that can be made "not currently addressable" but never truly removed — consistent with append-only storage.

RETRIEVEDOCVSPANSET counts both categories as part of a document's contents:

> "This returns a span-set indicating both the number of characters of text and the number of links in document \<doc id\>." [LM 4/68]

### Separate Storage Infrastructure

The enfilade architecture reinforces this. Nelson describes a dedicated **linking enfilade** (Barus's contribution) separate from the content enfilade:

> "His new method would allow linkages to keep up with all changes. It was instantaneous and permanent and could grow indefinitely." [LM 1/34]

> "Barus's work, which we refer to jocundly as 'the eye in the pyramid,' made possible an efficiently ever-linkable enfilade." [LM 1/34]

This is a separate data structure designed specifically for storing and indexing links — not a secondary index derived from content.

### Summary

A link is a **first-class stored entity** in the Istream alongside content bytes. Creating a link:

1. **Allocates storage** for the link structure (the three endsets)
2. **Assigns a permanent tumbler address** in the document's link subspace
3. **Enters the append-only record** — subject to the same non-destruction guarantees as bytes
4. **Is maintained by dedicated data structures** (the linking enfilade)

The endsets within the link are references (spans pointing to existing content), but the link itself is new stored matter. It is not an index entry derived from content — it is content of a different kind.

---

## Question 4 [nelson]

> What must the system guarantee about the relationship between a link's endsets and the original content they reference — must endsets always resolve to the exact content that existed when the link was created?

### Nelson's Answer

## Endset Resolution: What the System Guarantees

The short answer is: **yes and no**. Endsets always resolve to the same *Istream content* (which is immutable), but the *visible arrangement* of that content may change across versions. Nelson's design separates these two concerns deliberately.

### Istream Immutability: The Core Guarantee

Because endsets point to **Istream addresses** (permanent content identity), and Istream is append-only, the bytes referenced by an endset never change:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control" [LM 4/11]

Content at an I-address is permanent. A link created today pointing to I-address X will resolve to exactly the same bytes at X forever. This is not a feature of links — it is a property of Istream itself. Nothing in the system can modify content at an existing I-address.

### Survivability: Graceful Degradation, Not Exact Preservation

What the system does **not** guarantee is that the endset will always reference the same *quantity* of visible content. Nelson's survivability model explicitly allows partial degradation:

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes. This has a crucial advantage: it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them." [LM 4/42]

And from the survivability diagram on 4/43:

> "Links between bytes can survive deletions, insertions and rearrangements, **if anything is left at each end.**"

So the guarantee is:

| Scenario | Endset resolves? | To what? |
|----------|-----------------|----------|
| Content unchanged | Yes | Exact original span |
| Content partially deleted from Vstream | Yes | Remaining bytes (subset of original) |
| Content rearranged in Vstream | Yes | Same bytes, possibly discontiguous |
| ALL bytes deleted from Vstream | Link breaks | I-content still exists but nothing visible at either end |

The endset doesn't "update" to track new content — it stays attached to the *same bytes*. If those bytes are scattered by editing, the endset becomes discontiguous but still references the original content. Nelson explicitly illustrates this:

> "We see from above that one end of a link may be on a broken, discontiguous set of bytes." [LM 4/42]

### Why This Works: The I/V Separation

The mechanism is the Istream/Vstream separation. Links point to I-addresses (permanent identity). Editing changes V-addresses (current arrangement). Since these are independent:

- **INSERT** in a document: V-addresses shift, I-addresses unaffected, links unaffected
- **DELETE** from a document: V-mapping removed, I-content remains, links still resolve to I-content
- **REARRANGE**: V-order changes, I-addresses unchanged, links follow the bytes

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." [LM 4/30]

### Version-Spanning: Refractive Following

When content evolves through versions, the system can follow links across version boundaries through **correspondence** (shared I-address origin):

> "Links may be refractively followed from a point or span in one version to corresponding places in any other version. Thus a link to one version of a Prismatic Document is a link to all versions." [LM 2/26]

This means the endset resolves to the same I-content always, but the *front end* can choose to show the user where that content appears in the current version — or any version. The link itself doesn't change; the presentation adapts.

### What the System Does NOT Guarantee

Nelson does not guarantee that:

1. **Endsets track editorial intent.** If you link to a paragraph and the author rewrites it (deleting old bytes, inserting new ones), your link stays on the old bytes — it does not "follow" to the replacement text. The old bytes still exist in Istream; the new text has different I-addresses.

2. **Endsets remain contiguous.** Editing may scatter the referenced bytes across the Vstream, producing a "broken, discontiguous set of bytes" [LM 4/42].

3. **Endsets remain visible.** If all referenced bytes are deleted from every Vstream arrangement, the link has nothing to display — though the I-content technically still exists in the permascroll.

### Summary

The guarantee is precise: **endsets resolve to the identical Istream bytes forever** (because Istream is immutable), but the **visible presentation** of those bytes — their position, contiguity, and presence in a given version's Vstream — may change through editing. Links degrade gracefully (surviving partial deletion) rather than breaking catastrophically. The only breaking condition is total removal of all referenced bytes from the Vstream at an end.

This is the "strap between bytes" metaphor in full: the strap doesn't care where the bytes move or how many survive — it holds onto whatever remains.

---

## Question 5 [nelson]

> If a link references content belonging to a document the link creator does not own, what sharing or permission guarantees must the system maintain for that link?

### Nelson's Answer

## Link Permission Guarantees for Cross-Owner References

The answer depends entirely on whether the referenced content is **published** or **private**.

---

### Published Content: No Permission Required

When a link's endsets reference published content owned by someone else, the system requires **zero permission** from the content owner. This is not a gap — it is the explicit design:

> "Accessibility and free linking make a two-sided coin. On the one hand, each user is free to link to anything privately or publicly. By the same token, each author of a published work is relinquishing the right to control links into that work. This relinquishment must also be part of the publishing contract." [LM 2/43]

The publication contract pre-grants all linking rights:

> "Since the copyright holder gets an automatic royalty, anything may be quoted without further permission. That is, permission has already been granted: for part of the publication contract is the provision, 'I agree that anyone may link and window to my document.'" [LM 2/45]

The content owner **cannot prevent, remove, or interfere with** incoming links. The link lives at the creator's address, not the target's:

> "A link need not point anywhere in its home document. Its home document indicates who owns it, and not what it points to. Conversely, links connecting parts of a document need not reside in that document." [LM 4/12]

---

### The System's Obligation: Keep the Target Accessible

The critical guarantee the system must maintain is that **published content remains available** — precisely because others' links depend on it:

> "It is in the common interest that a thing once published stay published, as in the world of paper. Other readers and users will come to depend on its accessibility. Consequently its author may not withdraw it except by lengthy due process." [LM 2/43]

This creates a binding chain:
1. Alice publishes document D
2. Bob creates a link from his document to spans in D
3. Bob's link is Bob's property (at Bob's address)
4. Alice cannot withdraw D because Bob's link depends on it
5. Alice cannot delete Bob's link because it lives in Bob's document

If Alice publishes a superseding version, the old version must remain:

> "However, for corrections and amendments, the author may readily publish a superseding document, but the former version must remain on the network. This is vital because of the links other users may have made to it — which can now reach through from the previous version (to which they were originally attached) into the newer version." [LM 2/43]

---

### Link Survivability: The Structural Guarantee

The system must maintain that links survive editing of the target content:

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes. This has a crucial advantage: it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them." [LM 4/42]

Because links point to Istream addresses (permanent content identity) rather than Vstream positions (current arrangement), the content owner's edits cannot break the link. The link survives "deletions, insertions and rearrangements, if anything is left at each end" [LM 4/43].

---

### Private Content: Restricted Access

For private documents, the situation inverts. A private document "may be read and linked-to only by the owner and his or her associates" [LM 2/42]. Linking to private content requires being an owner or designee — no pre-granted permission exists.

---

### Compensation in Lieu of Control

Nelson explicitly separates **compensation** from **control**. The content owner gives up control over who links to their work but never gives up compensation:

> "In our planned service, there is a royalty on every byte transmitted. This is paid automatically by the user to the owner every time a fragment is summoned, as part of the proportional use of byte delivery." [LM 2/43]

This is the core bargain: the publication contract trades control for guaranteed automatic payment. Permission friction disappears because compensation is structural.

---

### Summary of Guarantees

| Guarantee | Who bears it | Source |
|-----------|-------------|--------|
| **Anyone may link to published content** | System + publication contract | 2/43 |
| **Content owner cannot prevent incoming links** | Publication contract | 2/43 |
| **Published content must remain accessible** | Content owner (contractual) | 2/43 |
| **Links survive target editing** | System (structural, via I-addresses) | 4/42 |
| **Link creator owns the link** | System (home document = ownership) | 4/12 |
| **Content owner receives automatic royalty** | System (per-byte, automatic) | 2/43 |
| **Old versions persist after supersession** | Content owner (contractual) | 2/43 |

The design philosophy is that **no sharing or permission negotiation is needed** — the act of publication is itself the grant of permission, and the royalty mechanism is itself the compensation. The system's obligation is to keep the content accessible and the links attached.

---

## Question 6 [nelson]

> Must every link belong to a document, or can links exist as independent first-class objects outside the document model?

### Nelson's Answer

## Every Link Must Belong to a Document

Nelson is unambiguous: **links cannot exist outside the document model.** They are always housed in a home document that determines their ownership and address.

### The No-Free-Floating Rule

> "By this convention, then, everything in the system is part of a document. No free-floating materials exist. Thus the 'Jabberwocky' is a document; and a set of links between them, were someone to create it, would yet be a separate document." [LM 2/29]

That last clause is the key. Even a collection of links whose sole purpose is to connect *other* documents is itself "a separate document." The document is the universal container. There is no alternative.

This is reinforced at the system level:

> "The Xanadu document is the unit of the system. There is almost nothing in the Xanadu system but Xanadu documents." [LM 4/6]

### Home Document = Ownership, Not Target

While every link must live in a document, the relationship is purely administrative—about *who owns* the link, not *what it connects*:

> "A link need not point anywhere in its home document. Its home document indicates who owns it, and not what it points to. Conversely, links connecting parts of a document need not reside in that document." [LM 4/12]

This is a subtle but critical point. A link connecting passages in documents X and Y might live in document Z, which has nothing to do with either X or Y. The home document is the ownership address, not a topical container.

### Address Structure Confirms This

Links occupy the **2.x subspace** within their home document's tumbler address:

> "N.0.U.0.D.V.0.2.1 (the first link of the document, stored in the document's space)" [LM 4/31]

> "N.0.U.0.D.V.0.2.755 (the 755th link to which the document is home)" [LM 4/31]

A link's tumbler address *contains* a document field. There is no address form for a link that lacks a document component. The addressing system itself makes document-less links structurally impossible.

### Why This Matters

The design serves three purposes:

1. **Ownership is always determinable.** Every link has an owner because every link has a home document, and every document has an owner. There is no orphan link problem.

2. **Links are first-class but not free-standing.** Links have their own addresses in tumbler-space, can be targets of other links, and persist independently of the documents they connect—but they still need a home for ownership and addressing purposes.

3. **Link-only documents are a feature, not a workaround.** Nelson explicitly envisions documents whose entire content is links. A scholar's annotations on someone else's work, a curated set of connections across a corpus—these are documents in their own right, owned by the annotator.

> "A Xanadu link is a connective unit, a package of connecting or marking information. It is owned by a user." [LM 4/41]

### Summary

Links are first-class citizens with their own permanent addresses, their own survival guarantees, and the ability to be targets of other links. But they are not *independent* objects. Every link lives in a home document that gives it an address and an owner. A "bag of links" is simply a document whose content happens to be entirely links. Nelson's architecture has no concept of a free-floating link—and by design, no mechanism to create one.

---

## Question 7 [nelson]

> After a link is created, must the system guarantee that retrieving the referenced content will always return the link as part of the retrieval — that is, are links permanently bound to the content they reference?

### Nelson's Answer

## Are Links Permanently Bound to Referenced Content?

The answer requires distinguishing two architectural concepts Nelson keeps separate: **link survivability** (do links stay attached to bytes?) and **link retrieval** (does retrieving content automatically return associated links?).

### Links Are Bound to Bytes, Not Positions

Yes, links are permanently attached to the content they reference — specifically, to the **bytes** themselves, not to positions in a document:

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes. This has a crucial advantage: it means that links can survive editing. If any of the bytes are left to which a link is attached, the link remains on them." [LM 4/42]

This binding persists through insertions, deletions, and rearrangements. It breaks only when **all** referenced bytes at an endset are deleted.

### But Retrieval Does NOT Automatically Include Links

Nelson separates content retrieval from link discovery into **distinct FEBE operations**:

- **RETRIEVEV** — returns "the material (text and links) determined by \<spec set\>" [LM 4/67]
- **FINDLINKSFROMTOTHREE** — returns "a list of all links which are (1) in \<home set\>, (2) from all or any part of \<from set\>, and (3) to all or any part of \<to set\> and \<three set\>" [LM 4/69]

The "links" in RETRIEVEV are the document's **own out-links** — links stored in that document. Nelson is explicit about this distinction:

> "Ordinarily a document consists of its contents (including history and alternatives) and its out-links, the links it contains that point to other documents. By contrast, a document's in-links are those stored elsewhere which point to it. These out-links are under control of its owner, whereas its in-links are not." [LM 2/31]

In-links — links made by others pointing TO your content — require a **deliberate query**:

> "The reader should be able to ask, for a given document or place in the document, 'What connects here from other documents?'— and be shown all these outside connections without appreciable delay." [LM 2/46]

This is not automatic inclusion; it is an explicit request with filtering:

> "Thus it becomes necessary to apply some kind of filter, saying, 'What links come in from Spain? From last week? From persons of importance to me?'" [LM 2/47]

### Links Create Permanence Obligations on Content

While links are not returned with content automatically, they do create a binding obligation in the other direction — content **cannot be withdrawn** because links depend on it:

> "It is in the common interest that a thing once published stay published, as in the world of paper. Other readers and users will come to depend on its accessibility. Consequently its author may not withdraw it except by lengthy due process." [LM 2/43]

> "This is vital because of the links other users may have made to it — which can now reach through from the previous version (to which they were originally attached) into the newer version." [LM 2/43]

### Links Themselves Can Be Deleted

The binding is not absolute from the link side. Link owners can delete their own links:

> "DELETED LINKS (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

Even deleted links are not truly destroyed — they remain in Istream, recoverable through historical backtrack.

### Summary

| Question | Answer |
|----------|--------|
| Do links stay attached to referenced bytes? | **Yes** — they survive editing as long as any referenced bytes remain |
| Does retrieving content return all associated links? | **No** — in-links require a separate FINDLINKS query |
| Does a document's own out-links come with retrieval? | **Yes** — out-links are part of the document |
| Can content be withdrawn if others have linked to it? | **No** — links create permanence obligations |
| Are links permanently irrevocable? | **No** — the link owner can delete them (but they persist in Istream) |

The system guarantees that links **survive** as long as referenced bytes exist, and that referenced content **cannot be withdrawn** while links depend on it. But it does **not** guarantee that retrieving content automatically surfaces all links pointing to it — that is a separate, user-initiated discovery operation.

---

## Question 8 [nelson]

> When two endsets of a link reference content in different documents owned by different users, who owns the link and what are the system's guarantees about each party's ability to discover it?

### Nelson's Answer

## Link Ownership Across Documents

### Who Owns the Link

**The link's home document determines ownership — not what the link points to.** This is one of the most explicitly stated principles in the link architecture:

> "A link need not point anywhere in its home document. Its home document indicates who owns it, and not what it points to. Conversely, links connecting parts of a document need not reside in that document." [LM 4/12]

The MAKELINK operation makes this concrete:

> "This creates a link in document \<doc id\> from \<from set\> to \<to set\> connected to \<three set\>." [LM 4/68]

> "The document must be specified because that determines the actual residence of the link — since a document may contain a link between two other documents." [LM 4/63]

So if User C creates a link in their Document Z, with the from-set pointing into User A's Document X and the to-set pointing into User B's Document Y — **User C owns the link**. Neither A nor B controls it. Only C can delete it.

### In-Links vs Out-Links

Nelson draws a sharp ownership boundary:

> "Ordinarily a document consists of its contents (including history and alternatives) and its out-links, the links it contains that point to other documents. By contrast, a document's in-links are those stored elsewhere which point to it. These out-links are under control of its owner, whereas its in-links are not." [LM 2/31]

User A and User B see the link as an **in-link** to their respective documents. They cannot control it. The link creator sees it as an **out-link** from their home document. They have full control.

### Discovery Guarantees

**Both parties (and everyone else) can discover the link.** The system indexes links by all three endsets, enabling bidirectional search:

> "The reader should be able to ask, for a given document or place in the document, 'What connects here from other documents?' — and be shown all these outside connections without appreciable delay." [LM 2/46]

The FINDLINKSFROMTOTHREE operation searches by any combination of home-set, from-set, to-set, and type:

> "This returns a list of all links which are (1) in \<home set\>, (2) from all or any part of \<from set\>, and (3) to all or any part of \<to set\> and \<three set\>." [LM 4/69]

> "If the home-set is the whole docuverse, all links between these two elements are returned." [LM 4/63]

And critically:

> "THE QUANTITY OF LINKS NOT SATISFYING A REQUEST DOES NOT IN PRINCIPLE IMPEDE SEARCH ON OTHERS." [LM 4/60]

So User A can query "what links touch my content?" and discover the link. User B can do the same. Neither needs the link creator's cooperation. Discovery is a system guarantee, not dependent on the link owner.

### The Asymmetry by Design

This creates a deliberate asymmetry:

| Capability | Link Owner (C) | Referenced Doc Owners (A, B) |
|---|---|---|
| Create the link | Yes | No (it's not their link) |
| Delete the link | Yes | No — can only delete content the link points to |
| Discover the link | Yes | Yes, via bidirectional search |
| Prevent the link | N/A | No — publication relinquishes this right |

The last point is crucial. Publishing a document contractually surrenders control over in-links:

> "Accessibility and free linking make a two-sided coin. On the one hand, each user is free to link to anything privately or publicly. By the same token, each author of a published work is relinquishing the right to control links into that work. This relinquishment must also be part of the publishing contract." [LM 2/43]

### The Only Recourse

If User A or B dislikes the link, their only structural recourse is to **delete the content the link points to** from their current version. Since links attach to spans of bytes, removing all referenced bytes at one end breaks the link. But the bytes still exist in Istream and in previous versions — so this is a Vstream-level action, not true destruction.

> "Links between bytes can survive deletions, insertions and rearrangements, if anything is left at each end." [LM 4/43]

### Summary

The design separates **ownership** (who controls the link), **reference** (what the link connects), and **discovery** (who can find the link). Ownership lives with the creator. Reference crosses document and user boundaries freely. Discovery is universal and bidirectional. This is what makes the "socially self-constructing" literature Nelson envisions possible — anyone can annotate, connect, and comment on anyone else's published work, without permission and without modifying the target.

---

## Question 9 [nelson]

> Must the system guarantee that creating a link has no effect whatsoever on the content it references — that the referenced content remains byte-identical before and after link creation?

### Nelson's Answer

## Yes — Link Creation Cannot Affect Referenced Content

This is guaranteed by multiple independent architectural principles, all of which converge on the same answer.

### 1. Links Live in the Creator's Document, Not the Target

Links are stored in their **home document**, which belongs to the link's creator — not in the documents they reference.

> "A link need not point anywhere in its home document. Its home document indicates who owns it, and not what it points to. Conversely, links connecting parts of a document need not reside in that document." [LM 4/12]

> "Ordinarily a document consists of its contents (including history and alternatives) and its out-links, the links it contains that point to other documents. By contrast, a document's in-links are those stored elsewhere which point to it. These out-links are under control of its owner, whereas its in-links are not." [LM 2/31]

In-links — links created by others that point INTO your document — are stored elsewhere and are not under your control. They are also not part of your document's contents. They have no mechanism by which to alter your content.

### 2. Istream Content Is Immutable

Content at an Istream address never changes after creation. Links reference I-addresses. There is nothing a link can do to modify what lives at those addresses.

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

The Istream is append-only. New bytes are added; existing bytes are never altered. A link is a separate object stored at its own address — it references I-addresses but cannot write to them.

### 3. Only the Owner Can Modify a Document

> "Every document has an owner, the person who created and stored it... Only the owner has a right to withdraw a document or change it." [LM 2/29]

If link creation modified the target document, then anyone linking to your published work would be modifying your document — a direct violation of the ownership guarantee. The architecture forbids this.

### 4. MAKELINK Operates on the Home Document

The MAKELINK operation specifies a home document for the link, not a target document:

> "This creates a link in document \<doc id\> from \<from set\> to \<to set\> connected to \<three set\>. It returns the id of the link made." [LM 4/68]

> "The document must be specified because that determines the actual residence of the link — since a document may contain a link between two other documents." [LM 4/63]

The `<doc id>` is where the link is *stored*. The `<from set>` and `<to set>` are addresses that *reference* content — they do not write to it.

### 5. Links Are a Separate Layer

Nelson describes links as existing alongside content, not modifying it:

> "The Xanadu link is a meta-virtual structure connecting parts of documents (which are themselves virtual structures)." [LM 4/41]

> "The link mechanism ties together the whole corpus of materials on the Xanadu system. There is essentially nothing in the Xanadu system except documents and their arbitrary links." [LM 4/41]

Documents and links are the two kinds of things. Links connect documents; they do not alter them.

### Summary

The guarantee follows necessarily from the architecture:

| Principle | Why it prevents modification |
|-----------|------------------------------|
| Link home ≠ link target | Link storage is in the creator's space, not the target's |
| Istream immutability | Referenced bytes cannot be altered after creation |
| Owner-only modification | Non-owners cannot change a document; linking is a non-owner action on the target |
| MAKELINK semantics | The operation writes to the home document only |
| Separate layer | Links are meta-structures over content, not modifications to content |

Nelson never needed to state this guarantee as a standalone principle because it is an inevitable consequence of the architecture. A system where links could modify their targets would violate ownership, break Istream immutability, and collapse the distinction between content and connection that is fundamental to the entire design.

---

## Question 10 [nelson]

> Does the design require that the system maintain a complete, queryable index from any span of content to all links whose endsets reference that span, and must this index be updated atomically with link creation?

### Nelson's Answer

## Yes to the index; implied but not explicitly specified for atomicity.

### The Index Requirement: Clearly Specified

Nelson requires a complete, queryable index from content spans to all referencing links. Multiple passages establish this unambiguously.

**The operation that demands it:**

FINDLINKSFROMTOTHREE returns "a list of all links which are (1) in \<home set\>, (2) from all or any part of \<from set\>, and (3) to all or any part of \<to set\> and \<three set\>" [LM 4/69]. This operation takes arbitrary span-sets as input and returns matching links — which requires an index from content addresses to link endsets.

**The performance guarantee that constrains the implementation:**

> "THE QUANTITY OF LINKS NOT SATISFYING A REQUEST DOES NOT IN PRINCIPLE IMPEDE SEARCH ON OTHERS." [LM 4/60]

This is not aspirational — it is a design constraint. A linear scan of all links would violate it. The system must index links by their endsets such that irrelevant links do not impose cost on queries.

**The user-facing promise that requires it:**

> "The reader should be able to ask, for a given document or place in the document, 'What connects here from other documents?'— and be shown all these outside connections without appreciable delay." [LM 2/46]

"Without appreciable delay" for backlink discovery across the entire docuverse requires indexed access, not scanning.

**The back-end responsibility:**

> "A Xanadu link is a connective unit, a package of connecting or marking information. It is owned by a user. It is put in by a user (or a front end), and thereafter maintained by the back end through the back end's inter-indexing mechanisms." [LM 4/41]

Nelson explicitly names "inter-indexing mechanisms" as the back end's responsibility. The index is not optional infrastructure — it is part of what the back end *is*.

**The data structure designed for it:**

> "His new method would allow linkages to keep up with all changes. It was instantaneous and permanent and could grow indefinitely. All changes, once made, left the file remaining in canonical order, which was an internal mandate of the system." [LM 1/34]

Barus's linking enfilade ("the eye in the pyramid") was specifically designed to make this index efficient and scalable — "efficiently ever-linkable" [LM 1/34].

### Atomicity: Implied but Not Explicitly Specified

Nelson does not use the term "atomic" or discuss transaction semantics. However, two properties he does require strongly imply atomic index updates:

**1. Canonical order after every change:**

> "All changes, once made, left the file remaining in canonical order, which was an internal mandate of the system." [LM 1/34]

"An internal mandate" — not a goal but a requirement. After any change (including MAKELINK), the system must be in canonical operating condition. A link that exists but is not yet indexed would violate this, since FINDLINKSFROMTOTHREE would fail to return it.

**2. Server-level consistency invariant:**

> "A server's network model, from the null case on up, is at all times unified and operational; whatever information moves between servers is assimilated at once to its overall structure, leaving each server in canonical operating condition." [LM 4/72]

"At all times unified and operational" describes an invariant, not an eventual-consistency target.

**What Nelson does NOT specify:**

- Concurrent modification semantics (what happens if two users create links simultaneously)
- Read-after-write guarantees across servers
- Whether "canonical order" permits a brief window of inconsistency during a single operation
- Isolation levels between concurrent FINDLINKS and MAKELINK operations

Nelson's session model section [LM 4/79] acknowledges that "Private documents. (Currently all documents are visible to all users.)" — suggesting XU.87.1 had a single-user simplification that made concurrency moot. He mentions future "barrel-roll shared search model which repeatedly crosses the address space on behalf of all a server's users simultaneously" [LM 4/59], but this addresses search scheduling, not transactional atomicity.

### Summary

| Question | Answer | Strength of evidence |
|----------|--------|---------------------|
| Must the system maintain a complete index from content to links? | **Yes** | Explicit — required by FINDLINKSFROMTOTHREE semantics and the 4/60 performance guarantee |
| Must the index cover all three endsets? | **Yes** | Explicit — search operates on home, from, to, and type simultaneously |
| Must updates be atomic with link creation? | **Strongly implied** | The "canonical order" invariant [1/34] and "at all times unified and operational" [4/72] leave no room for a state where a link exists but is not indexed — but Nelson never discusses the transactional mechanics |

The index is a first-class architectural requirement. Atomicity is a consequence of the consistency invariants Nelson imposes, rather than something he specifies directly as a transactional property.

---

## Question 11 [gregory]

> When `docreatelink` creates the link orgl in the granfilade, what is the exact internal structure stored — how are the three endsets (source, target, type) laid out within the orgl, and does each endset support multiple disjoint I-spans or only a single contiguous span?

### Gregory's Answer

## KB Synthesis

## Link Orgl Internal Structure

The KB answers this partially but has a gap at the byte-level serialization layer.

### What the KB confirms

**Endset positions within the link orgl** [SS-FOLLOWLINK]:

`link2sporglset()` extracts each endset by calling `retrieverestricted()` against the link orgl at one of three internal positions:
- `0.1` — FROM endset (source)
- `0.2` — TO endset (target)
- `0.3` — THREE endset (type)

These are I-space sub-addresses within the link orgl itself. The same position constants map to the spanfilade ORGLRANGE subspaces: `LINKFROMSPAN=1`, `LINKTOSPAN=2`, `LINKTHREESPAN=3` [SS-RETRIEVE-ENDSETS].

**Each endset supports multiple disjoint I-spans — confirmed** [SS-LINK-ENDPOINT, Finding 0037]:

> A single user-visible V-span may correspond to multiple I-spans in the endset when the V-span covers content transcluded from multiple sources. Each I-span independently tracks its content identity.

Formally: `Endset = set<Sporgl>` where `|Endset| >= |input_vspans|`. The inner loop in `vspanset2sporglset` (`sporgl.c:49-58`) iterates over every I-span returned by `vspanset2ispanset` and creates a **separate sporgl per contiguous I-address region**. So a V-span over "AABB" (where "AA" came from doc A and "BB" from doc B) produces two sporgls in the endset, not one.

This splitting happens automatically at link creation time — the front end provides contiguous V-spans; the backend decomposes them [ST-LINK-CREATE, Finding 0037].

**What a sporgl contains** [SS-SPORGL]:

```
Sporgl = { origin: IAddress, width: TumblerWidth, source_doc: ISA }
```

Stored as `typesporglset` (linked list), interchangeable with `typeispan` via a union type `typesporglitem`.

### What the KB does not cover

The exact serialization of how a sporglset (linked list of sporgls) is encoded within the granfilade at position 0.1/0.2/0.3 of the link orgl is **not described in the KB**. The KB documents that `retrieverestricted()` is used to access these positions — implying the link orgl has its own internal addressable structure — but does not describe the granfilade node layout for link orgls versus text atoms. The `typegrantext` byte-buffer layout [SS-CONTENT-IDENTITY, Finding 0034] is documented for text atoms, but no equivalent entry exists for link orgl node layout.

### Summary

| Question | Answer | Source |
|----------|--------|--------|
| How many endsets? | Three: FROM (0.1), TO (0.2), TYPE (0.3) | [SS-FOLLOWLINK] |
| Single contiguous span or multiple? | Multiple disjoint I-spans supported | [SS-LINK-ENDPOINT] |
| Internal format of each endset | Sporglset (linked list of sporgls) | [SS-SPORGL] |
| Byte-level serialization in granfilade | Not in KB | — |

---

## Code Exploration

I now have all the code I need. Here is the complete answer.

---

## How `docreatelink` lays out the link orgl

### The call sequence [`do1.c:195–221`]

```c
bool docreatelink(typetask *taskptr, typeisa *docisaptr,
                  typespecset fromspecset, typespecset tospecset,
                  typespecset threespecset, typeisa *linkisaptr)
{
    typehint hint;
    tumbler linkvsa, fromvsa, tovsa, threevsa;
    typesporglset fromsporglset, tosporglset, threesporglset;
    typeorgl link;

    makehint(DOCUMENT, ATOM, LINKATOM, docisaptr, &hint);
    return (
         createorglingranf(taskptr, granf, &hint, linkisaptr)   // 1. alloc new orgl
      && tumbler2spanset(taskptr, linkisaptr, &ispanset)         // 2. link ISA as I-span
      && findnextlinkvsa(taskptr, docisaptr, &linkvsa)           // 3. find V-slot in doc
      && docopy(taskptr, docisaptr, &linkvsa, ispanset)          // 4. insert ref in doc
      && findorgl(taskptr, granf, linkisaptr, &link, NOBERTREQUIRED)  // 5. fetch the orgl
      && specset2sporglset(taskptr, fromspecset, &fromsporglset, ...)  // 6. from→sporgls
      && specset2sporglset(taskptr, tospecset, &tosporglset, ...)      // 7. to→sporgls
      && specset2sporglset(taskptr, threespecset, &threesporglset, ...) // 8. type→sporgls
      && setlinkvsas(&fromvsa, &tovsa, &threevsa)                 // 9. assign V-slots
      && insertendsetsinorgl(taskptr, linkisaptr, link,           // 10. write to orgl
                             &fromvsa, fromsporglset,
                             &tovsa, tosporglset,
                             &threevsa, threesporglset)
      && insertendsetsinspanf(taskptr, spanf, linkisaptr,         // 11. cross-index
                              fromsporglset, tosporglset, threesporglset)
    );
}
```

---

### Step 1: the orgl is a fresh POOM enfilade

`createorglingranf` → `createorglgr` [`granf2.c:111–128`]:

```c
locinfo.infotype = GRANORGL;
locinfo.granstuff.orglstuff.orglptr = createenf(POOM);   // <-- POOM, not GRAN or SPAN
```

Every link's orgl is a **POOM (Permutation Object-Oriented Matrix) enfilade**. A POOM bottom crum has two dimensions [`wisp.h:19–20`]:

- `I` (index 0) — permascroll address (I-span origin + width)
- `V` (index 1) — virtual address within the link's private V-space

These are stored as a `typewid` pair in each crum's `cdsp`/`cwid` fields [`enf.h:53–82`].

---

### Step 2: three fixed V-slots

`setlinkvsas` [`do2.c:169–183`] assigns the starting V-address for each of the three endsets:

```c
bool setlinkvsas(tumbler *fromvsaptr, tumbler *tovsaptr, tumbler *threevsaptr)
{
    tumblerclear(fromvsaptr);
    tumblerincrement(fromvsaptr, 0, 1, fromvsaptr);   // → 1
    tumblerincrement(fromvsaptr, 1, 1, fromvsaptr);   // → 1.1   (FROM)

    tumblerclear(tovsaptr);
    tumblerincrement(tovsaptr, 0, 2, tovsaptr);       // → 2
    tumblerincrement(tovsaptr, 1, 1, tovsaptr);       // → 2.1   (TO)

    if (threevsaptr) {
        tumblerclear(threevsaptr);
        tumblerincrement(threevsaptr, 0, 3, threevsaptr);  // → 3
        tumblerincrement(threevsaptr, 1, 1, threevsaptr);  // → 3.1  (THREE/type)
    }
}
```

`tumblerincrement(src, rightshift, inc, dst)` [`tumble.c:599–623`]: when `src` is zero, sets `dst->exp = -rightshift; dst->mantissa[0] = inc`. When non-zero, it appends a sub-digit by adding `inc` at `mantissa[idx + rightshift]`. The two-call sequence produces a **two-digit tumbler** 1.1, 2.1, or 3.1 — a hierarchical address where the first digit (1/2/3) is the endset discriminant and the second (.1) is the sub-address start.

The V-space layout of every link orgl is therefore:

| V-range | Endset |
|---------|--------|
| [1, 2)  | FROM (source) |
| [2, 3)  | TO (target) |
| [3, 4)  | THREE (type) |

---

### Step 3: writing into the orgl — `insertendsetsinorgl`

[`do2.c:130–149`]:

```c
bool insertendsetsinorgl(typetask *taskptr, tumbler *linkisaptr, typeorgl link,
                         tumbler *fromvsa, typesporglset fromsporglset,
                         tumbler *tovsa, typesporglset tosporglset,
                         tumbler *threevsa, typesporglset threesporglset)
{
    if (!(insertpm(taskptr, linkisaptr, link, fromvsa, fromsporglset)
       && insertpm(taskptr, linkisaptr, link, tovsa, tosporglset)))
        return FALSE;
    if (threevsa && threesporglset)
        insertpm(taskptr, linkisaptr, link, threevsa, threesporglset);
    ...
}
```

Each `insertpm` call operates on the link's POOM. The inner loop [`orglinks.c:100–131`]:

```c
bool insertpm(typetask *taskptr, tumbler *orglisa, typeorgl orgl,
              tumbler *vsaptr, typesporglset sporglset)
{
    for (; sporglset; sporglset = sporglset->xxxxsporgl.next) {
        unpacksporgl(sporglset, &lstream, &lwidth, &linfo);  // one I-span

        movetumbler(&lstream, &crumorigin.dsas[I]);    // I-origin = I-span start
        movetumbler(&lwidth,  &crumwidth.dsas[I]);     // I-width  = I-span width
        movetumbler(vsaptr,   &crumorigin.dsas[V]);    // V-origin = current slot position

        shift = tumblerlength(vsaptr) - 1;             // sub-digit level
        inc   = tumblerintdiff(&lwidth, &zero);        // integer count
        tumblerincrement(&zero, shift, inc, &crumwidth.dsas[V]);  // V-width ∝ I-span width

        insertnd(taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);

        tumbleradd(vsaptr, &crumwidth.dsas[V], vsaptr);  // advance V for next sporgl
    }
}
```

**One POOM crum is created per `typesporgl` in the endset.** Each crum stores:
- `cdsp.dsas[I]` / `cwid.dsas[I]` — the I-span (permascroll origin + width)
- `cdsp.dsas[V]` / `cwid.dsas[V]` — a V-sub-address within this endset's slot
- `c2dinfo.homedoc` — the home-document ISA for the sporgl

After each crum, `vsaptr` advances by `crumwidth.dsas[V]`, so the next I-span occupies the next consecutive sub-address within the same [1,2)/[2,3)/[3,4) window.

---

### Does each endset support multiple disjoint I-spans?

**Yes, unconditionally.** The input sporglset is a linked list, and `insertpm` iterates over every element:

```c
for (; sporglset; sporglset = sporglset->xxxxsporgl.next) { ... }
```

Each disjoint I-span in the endset produces its own POOM bottom crum at a distinct V-sub-address within the slot. There is no merging, no single-span limit, and no guard against multi-span endsets.

The sporgl conversion in `specset2sporglset` / `vspanset2sporglset` [`sporgl.c:14–65`] already iterates over all `vspanset->next` entries — a single specset can produce arbitrarily many sporgls (one per V-span × I-span pair).

---

### Retrieval confirms the layout

`link2sporglset` [`sporgl.c:67–95`] reads back a given endset:

```c
tumblerincrement(&zero, 0, whichend, &vspan.stream);  // stream = 1, 2, or 3
tumblerincrement(&zero, 0/*1*/, 1,   &vspan.width);   // width  = 1

context = retrieverestricted((typecuc*)orgl, &vspan, V,
                             (typespan*)NULL, I, (typeisa*)NULL);
for (c = context; c; c = c->nextcontext) {
    contextintosporgl((type2dcontext*)c, NULL, sporglptr, I);
    ...
}
```

The V-window `[whichend, whichend+1)` (e.g. [1, 2) for FROM) captures every POOM crum stored under that endset, however many there are. Each returned context corresponds to one disjoint I-span. The I-dimension content (`c->totaloffset.dsas[I]` and `c->contextwid.dsas[I]`) gives the permascroll origin and width for that span.

---

### Spanfilade cross-index

In parallel, `insertendsetsinspanf` → `insertspanf` [`do2.c:116–128`, `spanf1.c:15–54`] registers the link in the global spanfilade for reverse lookup. Each I-span in each endset is stored under a prefixed orgl-address:

```c
prefixtumbler(linkisaptr, spantype, &crumorigin.dsas[ORGLRANGE]);
// spantype = LINKFROMSPAN(1), LINKTOSPAN(2), or LINKTHREESPAN(3)
```

So the spanfilade key is `1.<linkISA>`, `2.<linkISA>`, `3.<linkISA>` for FROM/TO/THREE respectively [`xanadu.h:36–39`]. This is the index used by `findlinksfromtothreesp` to find links by content.

---

### Summary

| Property | Value |
|----------|-------|
| Orgl enfilade type | POOM [`granf2.c:120`, `enf.h:14`] |
| Dimensions | I (permascroll) × V (link virtual space) |
| FROM endset V-slot | [1, 2), entries start at V=1.1 |
| TO endset V-slot | [2, 3), entries start at V=2.1 |
| THREE/type endset V-slot | [3, 4), entries start at V=3.1 |
| Multiple disjoint I-spans per endset | **Yes** — one POOM crum per I-span, each at consecutive V-sub-addresses within the slot [`orglinks.c:100–131`] |
| V-sub-address spacing | Proportional to I-span integer width; set via `tumblerincrement(&zero, shift=len-1, inc=width, ...)` |
| Retrieval window | `[whichend, whichend+1)` in V; returns all I-spans for that endset [`sporgl.c:80–83`] |

The three endsets (source=FROM=1, target=TO=2, type=THREE=3) are separated by their first V-digit, not by separate data structures. Multiple disjoint I-spans are first-class: each becomes its own POOM crum at a distinct V-sub-address, and `link2sporglset` recovers all of them in a single `retrieverestricted` call.

---

## Question 12 [gregory]

> `findnextlinkvsa` allocates the link's V-position in the document's link subspace — does it scan existing POOM entries in the `2.x` range to find the maximum, or does it use a separate counter, and what happens if a prior link's POOM entry was removed via DELETEVSPAN?

### Gregory's Answer

## KB Synthesis

## `findnextlinkvsa`: V-Position Allocation for Links

### How the position is determined

`findnextlinkvsa` does **not** scan existing POOM entries in the `2.x` range, nor does it maintain a separate counter. It uses `vspanreach` — the current maximum V-extent of the document as tracked by the POOM tree's root node — with a special-case for the first link [SS-LINK-SUBSPACE]:

- **First link ever**: initializes to `2.1` by incrementing tumbler digit-0 to 2, then digit-1 to 1.
- **Subsequent links**: placed at `vspanreach`, i.e., appended after the current document maximum.

The `vspanreach` value is POOM-derived (from the root node's `cdsp` + `cwid` in the V-dimension). It reflects the live state of the POOM tree at call time. Code reference: `backend/do2.c:151-167` [ST-CREATE-LINK].

### What happens after DELETEVSPAN removes a prior link

This is where the design diverges sharply from I-address allocation:

**I-address allocation is monotonically increasing and never reuses** — `findpreviousisagr` always finds the global maximum in the granfilade (which persists even after DELETE), so addresses only grow [INV-MONOTONIC], [INV-NO-IADDR-REUSE].

**V-position allocation for links has no such guarantee.** After `DELETEVSPAN(2.x)` removes a link's POOM entry:

1. `deletend` removes the POOM crum and calls `setwispupwards` + `recombine`, updating the root node's extent [ST-DELETE, SS-THREE-LAYER-MODEL].
2. If the deleted link was at the maximum V-position (e.g., the only link was at `2.3` and it's removed), `vspanreach` shrinks accordingly.
3. The next call to `findnextlinkvsa` reads the new (smaller) `vspanreach` and would place the next link at that position — **potentially re-occupying a V-address previously held by the deleted link**.

This means V-positions in the link subspace are **mutable and potentially reusable** via the DELETEVSPAN/CREATELINK cycle, unlike I-addresses in the granfilade.

### Implications for the spec

- [FC-LINK-DELETE-ISOLATION] and [INV-LINK-PERMANENCE] confirm the link *object* (in I-space and spanfilade) is permanent — but the link's V-position in the home document's POOM is not.
- The V-position allocated by `findnextlinkvsa` is not a stable identifier; it is an ephemeral POOM slot. The permanent identifier is the link's I-address (ISA).
- [SS-THREE-LAYER-MODEL] captures this three-way distinction: I-space (permanent), spanfilade (append-only), POOM (mutable). `findnextlinkvsa` operates purely in the POOM layer.
- The KB does not contain findings on whether re-occupying a previously deleted V-position causes any observable anomaly (e.g., interaction with `vspanreach` normalization [EC-VSPAN-NORMALIZATION]). That is an open question not answerable from the KB.

---

## Code Exploration

I now have a complete picture. Here is the full answer.

---

## `findnextlinkvsa`: Full Analysis

### The Function

`findnextlinkvsa` lives at `do2.c:151–167`:

```c
bool findnextlinkvsa(typetask *taskptr, typeisa *docisaptr, tumbler *vsaptr)
{
  tumbler vspanreach, firstlink;
  typevspan vspan;
  bool doretrievedocvspan();
    tumblerclear (&firstlink);
    tumblerincrement (&firstlink, 0, 2, &firstlink);
    tumblerincrement (&firstlink, 1, 1, &firstlink);

    (void) doretrievedocvspan (taskptr, docisaptr, &vspan);
    tumbleradd (&vspan.stream, &vspan.width, &vspanreach);
    if (tumblercmp (&vspanreach, &firstlink) == LESS)
        movetumbler (&firstlink, vsaptr);
    else
        movetumbler (&vspanreach, vsaptr);
    return (TRUE);
}
```

---

### What `firstlink` Is

The two `tumblerincrement` calls construct the value `2.1` in Xanadu tumbler notation:

- **First call** `tumblerincrement(&firstlink, 0, 2, ...)`: input is zero, so `exp=0`, `mantissa[0]=2` → tumbler = `2` [`tumble.c:603–607`]
- **Second call** `tumblerincrement(&firstlink, 1, 1, ...)`: input is non-zero, the loop at `tumble.c:611` finds `idx=0` (last non-zero digit), `idx + rightshift = 1`, sets `mantissa[1] += 1` → result = `exp=0, mantissa=[2,1,0,…]` → tumbler = `2.1`

`firstlink = 2.1` is the **hard-coded floor** for the link subspace.

---

### No Counter — No Scan: It Reads the Root Aggregate

The function calls `doretrievedocvspan` (`do1.c:312–320`), which calls `retrievevspanpm` (`orglinks.c:165–172`):

```c
bool retrievevspanpm(typetask *taskptr, typeorgl orgl, typevspan *vspanptr)
{
    vspanptr->next = NULL;
    vspanptr->itemid = VSPANID;
    movetumbler (&((typecuc *) orgl)->cdsp.dsas[V], &vspanptr->stream);
    movetumbler (&((typecuc *) orgl)->cwid.dsas[V], &vspanptr->width);
    return (TRUE);
}
```

This is a **direct struct read from the POOM root node** (`typecuc`): two field copies — `cdsp.dsas[V]` (stream origin) and `cwid.dsas[V]` (aggregate width). There is:

- **No counter** — no integer that ticks up on each `createlink`
- **No scan** — no traversal of POOM leaf nodes in the `2.x` range to find a maximum

`vspanreach = stream + width` is the absolute end of the document's entire V-extent (text *and* links combined). The function returns `max(2.1, vspanreach)`, placing the next link at the tail of the occupied V-space, but never below the link-subspace floor.

---

### How `cwid.dsas[V]` Stays Up-To-Date

`cwid.dsas[V]` at the POOM root is a live bounding-box aggregate maintained by the enfilade wid/wisp machinery. After every structural modification, `setwispupwards` propagates changes upward (`edit.c:74`, `wisp.c:83–111`), calling `setwispnd` (`wisp.c:171–228`) at each level:

```c
/* wisp.c:207-214 */
clear (&newwid, sizeof(newwid));
for (ptr = findleftson (father); ptr; ptr = getrightbro (ptr)) {
  lockadd((tumbler*)&ptr->cdsp, (tumbler*)&ptr->cwid,
          (tumbler*)&tempwid, (unsigned)widsize(ptr->cenftype));
  lockmax((tumbler*)&newwid, (tumbler*)&tempwid,
          (tumbler*)&newwid, (unsigned)widsize(ptr->cenftype));
}
```

`cwid = max(child_dsp + child_wid) for all children` — the rightmost reach of any child in the V dimension. This propagates all the way up to the root, so `retrievevspanpm`'s direct read of `cwid.dsas[V]` always reflects current tree state.

---

### What Happens When a Prior Link Is Removed via DELETEVSPAN

`deletevspanpm` (`orglinks.c:145–152`) calls `deletend` (`edit.c:31–76`):

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

Inside `deletend`, for each POOM node intersecting the deleted span:

- **Fully inside**: `disown(ptr); subtreefree(ptr)` — removed from tree entirely [`edit.c:59–61`]
- **To the right of the deletion**: `ptr->cdsp.dsas[index] -= width` — the node's V-origin is shifted left by the deleted width [`edit.c:63`]
- Then `setwispupwards(father, 1)` and `recombine(father)` propagate the aggregate update to the root [`edit.c:74–75`]

**V-space compresses.** There is no "tombstone" or reserved address — the virtual coordinate space closes the gap and all subsequent nodes shift left. The root's `cwid.dsas[V]` shrinks accordingly.

---

### Consequence: V-Address Reuse After DELETEVSPAN of a Link

Because `findnextlinkvsa` returns the **current** end of V-space (derived from the live aggregate), and DELETEVSPAN compresses V-space:

1. **Last link deleted**: `vspanreach` shrinks by exactly the deleted width. The next `findnextlinkvsa` returns the same starting address the deleted link occupied.

2. **Middle link deleted**: The links that followed it shift down in V-space (their `cdsp` is decremented). `vspanreach` is now the new end. The next link is placed there — which was formerly occupied by what is now shifted content.

3. **No link deleted**: The function returns `max(2.1, current_end)` monotonically advancing as new links are `docopy`-ed in.

There is **no protection against V-address reuse**. The V-coordinate system is purely virtual and session-local; it expresses the *current* content ordering, not a permanent allocation history. Any V-span reference into the `2.x` range that was cached before a DELETEVSPAN will silently address different (shifted or recycled) content afterward.

---

## Question 13 [gregory]

> `findisatoinsertnonmolecule` allocates the link's I-address with a bounded upper limit (`docISA.2.3` for links) — what is the significance of that `2.3` bound, and does it mean link I-addresses and text I-addresses occupy non-overlapping ranges within the same document's I-space?

### Gregory's Answer

## KB Synthesis

## `docISA.2.3` Bound and I-Space Partitioning

### What the bound means

From [SS-ADDRESS-SPACE] Finding 0065, the upper bound is computed as:

```
tumblerincrement(docISA, 2, LINKATOM+1)  =  tumblerincrement(docISA, 2, 3)
```

This adds digit `3` at the 2nd position past the last significant digit of `docISA` in the mantissa, producing a tumbler like `docISA.0.3`. Because `LINKATOM = 2`, the value `LINKATOM+1 = 3` marks the boundary between link element field (2) and whatever follows. All link orgls for document `D` fall in `[docISA.0.2.1, docISA.0.3)`.

The per-document scoping is explicit: each document has an independent allocation counter within its own link subspace — the same `findisatoinsertmolecule` call bounds its search to `docISA.0.2.x`, so link allocations in document A (`1.1.0.1.0.2`) cannot interfere with link allocations in document B (`1.1.0.1.0.1`). [ST-ADDRESS-ALLOC Finding 0065]

### Do link and text I-addresses occupy non-overlapping ranges?

The concrete addresses in the KB suggest yes — their tumbler representations are in distinct subranges:

- **Link orgls**: `1.1.0.1.0.1.0.2.1`, `1.1.0.1.0.1.0.2.2`, ... — digit 0 at position 6, digit 2 at position 7 [SS-ADDRESS-SPACE Finding 0065]
- **Text content**: `1.1.0.1.0.1.3.0.1.1`, `1.1.0.1.0.1.3.0.1.2`, ... — digit 3 at position 6 [SS-ADDRESS-SPACE Finding 0077]

In the tumbler total order (`0 < 3` at position 6), link ISAs sort strictly below text ISAs for the same document. [SS-ADDRESS-SPACE] Finding 0077 explicitly states: "Both query the same granfilade tree but **search different subtrees**." The spec models this as two independent allocation functions, not a single `Σ.next` counter.

### The contiguity interaction from CREATELINK

There is a complication: [INT-LINK-INSERT] Finding 0063 states that CREATELINK breaks text I-address contiguity:

> `INSERT "ABC" → I.1, I.2, I.3 / CREATELINK → link orgl at ~I.2.0 / INSERT "DEF" → I.2.1+`
> `compare_versions reports 2 shared span pairs (gap between ABC and DEF I-addresses)`

This occurs because both text and link allocation call `findisatoinsertmolecule`, which queries `findpreviousisagr` against the same granfilade tree. Even though their nominal search subtrees are distinct, the link orgl's allocation advances the global maximum in a way that the text allocator observes, pushing subsequent text I-addresses past the link orgl's position.

The set of contiguity-breaking operations is therefore `{INSERT, CREATELINK}` — both call into `findisatoinsertgr` for content — while `CREATENEWVERSION` does not break contiguity because it allocates only a document address via `findisatoinsertnonmolecule`, leaving the content allocation maximum unchanged. [SS-ADDRESS-SPACE Finding 0077]

### Summary

| | Range | Allocated by |
|---|---|---|
| Link orgls | `[docISA.0.2.1, docISA.0.3)` | `findisatoinsertmolecule`, LINKATOM bound |
| Text content | `[docISA.0.1.1, docISA.0.2)` approx. | `findisatoinsertmolecule`, TEXTATOM bound |

The two ranges are non-overlapping in the tumbler address space (link ISAs are numerically below text ISAs for the same document), and `docISA.0.3` serves as the ceiling for the link subspace. However, the shared allocation mechanism means CREATELINK is "visible" to subsequent text allocations — link orgl allocation advances the allocation frontier that `findpreviousisagr` uses for text, causing the non-contiguity observed in `compare_versions`. [INT-LINK-INSERT Finding 0063, SS-ADDRESS-SPACE Finding 0077]

---

## Code Exploration

I now have everything. Here is the complete answer.

---

## The `docISA.2.3` Bound: What It Means and Why It Creates Non-Overlapping I-Space Ranges

### First: A Correction on the Function Name

The `docISA.2.3` bound does **not** live in `findisatoinsertnonmolecule`. That function handles non-ATOM types (DOCUMENT, ACCOUNT, NODE). Links are ATOM-typed and take a different path.

Trace the dispatch in `findisatoinsertgr` [`granf2.c:130-156`]:

```c
if (hintptr->subtype == ATOM) {
    ...
    findisatoinsertmolecule (fullcrumptr, hintptr, isaptr);   // links go HERE
} else {
    findisatoinsertnonmolecule (fullcrumptr, hintptr, isaptr); // documents go here
}
```

The hint for link creation is set in `domakelink`/`docreatelink` [`do1.c:180`, `do1.c:207`]:

```c
makehint (DOCUMENT, ATOM, LINKATOM, docisaptr, &hint);
```

`makehint` sets `hint.subtype = ATOM` [`do2.c:78-84`], so links always route to `findisatoinsertmolecule`, never to `findisatoinsertnonmolecule`.

---

### The `docISA.2.3` Bound in `findisatoinsertmolecule`

The relevant constants [`xanadu.h:144-146`]:

```c
/* atom types - don't change these */
#define TEXTATOM  1
#define LINKATOM  2
```

The comment "don't change these" is load-bearing — their integer values encode the I-space layout.

`findisatoinsertmolecule` [`granf2.c:158-181`]:

```c
static int findisatoinsertmolecule(typecuc *fullcrumptr, typehint *hintptr, typeisa *isaptr)
{
  typeisa upperbound, lowerbound;

    tumblerincrement (&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound);  // line 162
    clear (&lowerbound, sizeof(lowerbound));
    findpreviousisagr ((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);
    if (tumblerlength (&hintptr->hintisa) == tumblerlength (&lowerbound)) {
        tumblerincrement (&lowerbound, 2, hintptr->atomtype, isaptr);
        tumblerincrement (isaptr, 1, 1, isaptr);
    } else if (hintptr->atomtype == TEXTATOM) {
            tumblerincrement (&lowerbound, 0, 1, isaptr);
    } else if (hintptr->atomtype == LINKATOM) {
        tumblerincrement (&hintptr->hintisa, 2, 2, isaptr);         // line 171
        if (tumblercmp (&lowerbound, isaptr) == LESS)
            tumblerincrement (isaptr, 1, 1, isaptr);                // line 173
        else
            tumblerincrement (&lowerbound , 0, 1, isaptr);
    }
}
```

#### What `tumblerincrement(x, rightshift, bint, out)` does

From `tumble.c:599-622`: it takes tumbler `x`, finds the index `idx` of its last non-zero mantissa word, then adds `bint` at position `idx + rightshift`. For a non-zero input tumbler, `rightshift=2` appends two additional dot-components (two zeros then the value). So:

- `tumblerincrement(docISA, 2, 3, &upperbound)` → `upperbound = docISA.0.0.3`
- `tumblerincrement(docISA, 2, 2, &isaptr)` → `isaptr = docISA.0.0.2`
- `tumblerincrement(docISA.0.0.2, 1, 1, &isaptr)` → `isaptr = docISA.0.0.2.0.1`

The notation "docISA.2.3" in the question is shorthand: *depth offset 2, value 3*.

---

### Why Each Part of `2.3` is Significant

**The `2` (rightshift = 2):** Every atom lives two sub-levels below its parent document. This `depth=2` is also why the granfilade search can unambiguously identify whether a found address is "inside" the document's atom space versus at the document level itself — a depth-2 child can never equal the parent.

**The `3` (= `LINKATOM + 1`):** This is an **exclusive** upper bound passed to `findpreviousisagr`. The function finds the greatest ISA strictly less than this bound. Using `atomtype + 1` means each atom type gets a private "lane" of width 1 at the 2-deep sub-level:

| atomtype | exclusive upper bound | effective lane |
|----------|----------------------|----------------|
| `TEXTATOM = 1` | `docISA.0.0.2` | `[docISA, docISA.0.0.2)` |
| `LINKATOM = 2` | `docISA.0.0.3` | `[docISA.0.0.2, docISA.0.0.3)` |

---

### Do Text and Link I-Addresses Overlap?

**No. They are structurally non-overlapping by the encoding of `atomtype`.**

For text insertion, `findisatoinsertmolecule` searches with `upperbound = docISA.0.0.2` and places new text at `lowerbound + 1` (at depth 0 relative to lowerbound, i.e., `rightshift=0`). Text ISA addresses are therefore strictly less than `docISA.0.0.2`.

For link insertion, the minimum candidate address is computed at [`granf2.c:171`]:
```c
tumblerincrement (&hintptr->hintisa, 2, 2, isaptr);  // = docISA.0.0.2
```
If no links exist yet (`lowerbound < docISA.0.0.2`), the first link gets [`granf2.c:173`]:
```c
tumblerincrement (isaptr, 1, 1, isaptr);  // = docISA.0.0.2.0.1
```

`docISA.0.0.2.0.1` is a child of `docISA.0.0.2` and in tumbler ordering is strictly **greater than** `docISA.0.0.2` (and thus strictly greater than any text ISA, which must be less than `docISA.0.0.2`). Subsequent links increment from the last link's address using `rightshift=0` (same depth), staying within `[docISA.0.0.2.0.1, docISA.0.0.3)`.

So the I-space partition within a document is:

```
[docISA]               — the document orgl itself (placed by findisatoinsertnonmolecule)
[docISA, docISA.0.0.2) — TEXT atom range (exclusive upper bound = docISA.0.0.2)
[docISA.0.0.2.0.1, docISA.0.0.3) — LINK atom range (starts at first child of docISA.0.0.2)
```

These ranges are non-overlapping. The gap between text's ceiling (`docISA.0.0.2`) and the link floor (`docISA.0.0.2.0.1`) is the address `docISA.0.0.2` itself — which is never assigned to either type, serving as a structural separator.

---

### Summary

The `docISA.2.3` bound encodes two design decisions simultaneously:
1. **Depth 2** (`rightshift=2`): atom I-addresses live two sub-levels below their document, ensuring no atom ISA can equal its containing document's ISA.
2. **Value 3** (`LINKATOM + 1`): the `atomtype` integer (with `TEXTATOM=1`, `LINKATOM=2`) is used as a partition key at that depth. The `+1` makes the search exclusive so each type gets its own lane. This is why `xanadu.h:144` says **"don't change these"** — changing `LINKATOM` or `TEXTATOM` would shift the partition boundaries and corrupt the layout of existing stored documents.

---

## Question 14 [gregory]

> `insertendsetsinspanf` indexes link endsets in the spanfilade — does it create one spanfilade entry per endset, one per I-span within each endset, or one entry covering all three endsets, and what key structure distinguishes source/target/type entries?

### Gregory's Answer

## KB Synthesis

`insertendsetsinspanf` creates **one spanfilade entry per I-span within each endset**, and distinguishes source/target/type via ORGLRANGE subspace tags.

## Granularity: Per I-span per endset

`insertendsetsinspanf` receives three sporglsets — one each for from, to, and type — and calls `insertspanf` once per endset type [INT-SPORGL-LINK-INDEX, Finding 0013, `do2.c:116-128`]. `insertspanf` then iterates over the sporglset linked list and makes **one `insertnd` call per `typeispan` struct** [SS-DOCISPAN, Finding 0047, `spanf1.c:15-53`].

A single user-visible V-span can produce **multiple I-spans** when the spanned content is transcluded from multiple sources. For example, a V-span covering "AABB" where "AA" came from document A and "BB" from document B produces two sporgls → two spanfilade entries for that endset [ST-LINK-CREATE, Finding 0037, `sporgl.c:49-58`].

So for a link with a simple (single-source) endset:
- From endset: 1 spanfilade entry  
- To endset: 1 spanfilade entry  
- Type endset: 1 spanfilade entry  
Total: 3 entries

For a link whose from-endset spans content from N discontiguous I-address regions: N + 1 + 1 = N+2 entries.

## Key structure: ORGLRANGE subspace tags

The spanfilade is a 2D enfilade with two dimensions [SS-RETRIEVE-ENDSETS, Finding 0035]:
- **SPANRANGE** (dimension 0): the I-address content range — keys on the content identity
- **ORGLRANGE** (dimension 1): the link type/origin — distinguishes which endset type an entry belongs to

The three endpoint types occupy separate ORGLRANGE subspaces with hardcoded prefix values:
| Endset | ORGLRANGE value |
|--------|----------------|
| LINKFROMSPAN | 1 |
| LINKTOSPAN | 2 |
| LINKTHREESPAN | 3 |

Each spanfilade entry maps `(I-address range, endset-type prefix) → link ISA`. When RETRIEVEENDSETS searches, it restricts the ORGLRANGE dimension to one of these three prefixes per endset type [SS-RETRIEVE-ENDSETS, `spanf1.c:190-235`].

This is the same structure FINDLINKSFROMTOTHREE uses — it searches all three endset types by intersecting the query I-addresses against the SPANRANGE dimension, collecting links tagged with LINKFROMSPAN, LINKTOSPAN, or LINKTHREESPAN respectively [INT-SPORGL-LINK-INDEX, Finding 0035].

---

## Code Exploration

I now have everything needed. Here is the complete answer.

---

## `insertendsetsinspanf`: Granularity and Key Structure

### Function location

`insertendsetsinspanf` is defined at `backend/do2.c:116-128`:

```c
bool insertendsetsinspanf(typetask *taskptr, typespanf spanfptr, typeisa *linkisaptr,
    typesporglset fromsporglset, typesporglset tosporglset, typesporglset threesporglset)
{  bool insertspanf();
  if (!(
    insertspanf(taskptr,spanfptr,linkisaptr,fromsporglset,LINKFROMSPAN)
      &&insertspanf(taskptr,spanfptr,linkisaptr,tosporglset,LINKTOSPAN)))
        return (FALSE);
  if (threesporglset) {
    if(!insertspanf(taskptr,spanfptr,linkisaptr,threesporglset,LINKTHREESPAN)){
        return (FALSE);
     }
  }
  return(TRUE);
}
```

It makes **three separate calls** to `insertspanf` — one per endset role — passing the endset-type discriminant as the last argument.

---

### How many spanfilade entries are created?

**One entry per I-span within each endset**, not one per endset and not one covering all three.

`insertspanf` [`backend/spanf1.c:15-53`] iterates over the sporglset and calls `insertnd` once per element:

```c
for (; sporglset; sporglset = (typesporglset)((typeitemheader *)sporglset)->next) {
    // extract lstream, lwidth from element ...
    movetumbler (&lstream, &crumorigin.dsas[SPANRANGE]);
    movetumbler (&lwidth,  &crumwidth.dsas[SPANRANGE]);
    insertnd(taskptr,(typecuc*)spanfptr,&crumorigin,&crumwidth,&linfo,SPANRANGE);
                                                          // ^^^ one call per element
}
```

[`spanf1.c:25-52`]

So for a link whose source endset covers three I-spans, the spanfilade receives **three FROM entries, N TO entries, M THREE entries** — one crum per I-span per role.

---

### Key structure distinguishing source / target / type

The spanfilade is a 2D structure (defined in `backend/wisp.h:15-16`):

```c
#define ORGLRANGE 0    // dimension 0: "orgl" axis — the link identity
#define SPANRANGE 1    // dimension 1: "span" axis — the I-span content position
```

Each inserted crum carries a 2D origin and width (`typewid crumorigin`, `typewid crumwidth`), each with two tumbler components.

**ORGLRANGE dimension (dim 0) — link identity + endset role:**

```c
prefixtumbler (isaptr, spantype, &crumorigin.dsas[ORGLRANGE]);   // spanf1.c:22
tumblerclear  (&crumwidth.dsas[ORGLRANGE]);                       // spanf1.c:23
```

`prefixtumbler` [`backend/tumble.c:641-651`] prepends the integer `spantype` as the high component of the tumbler:

```c
int prefixtumbler(tumbler *aptr, INT bint, tumbler *cptr)
{
  tumbler temp1, temp2;
    tumblerclear (&temp1);
    temp1.mantissa[0] = bint;          // high component = spantype
    movetumbler (aptr, &temp2);        // then shift in the link ISA
    if (!iszerotumbler (&temp2))
        temp2.exp -= 1;
    tumbleradd (&temp1, &temp2, cptr); // result = spantype.linkISA
}
```

The three endset roles are assigned these integers [`backend/xanadu.h:36-38`]:

```c
#define LINKFROMSPAN    1     // source endset
#define LINKTOSPAN      2     // target endset
#define LINKTHREESPAN   3     // type/three endset
```

So the ORGLRANGE key is: **`spantype . linkISA`** — the endset-type integer forms the most-significant component, followed by the link's ISA tumbler. Width is zeroed out (`tumblerclear`), making each link ISA a point in the ORGLRANGE axis.

**SPANRANGE dimension (dim 1) — I-span content position:**

```c
movetumbler (&lstream, &crumorigin.dsas[SPANRANGE]);   // spanf1.c:49
movetumbler (&lwidth,  &crumwidth.dsas[SPANRANGE]);    // spanf1.c:50
```

`lstream` and `lwidth` are the I-span's stream address and width, extracted from the sporglset element (an `ISPANID`, `SPORGLID`, or `TEXTID` item). This is the content axis: it records *where in I-space* this endset I-span lives.

**Payload (`linfo.homedoc`):** stores the link ISA (or for SPORGL items, the sporgl's home document), available during retrieval.

---

### Lookup confirms the structure

`retrieveendsetsfromspanf` [`spanf1.c:190-235`] inverts the lookup by constructing ORGLRANGE probes that are single-unit intervals at position 1, 2, or 3:

```c
fromspace.stream.mantissa[0] = LINKFROMSPAN;    // = 1
fromspace.width.mantissa[0]  = 1;

tospace.stream.mantissa[0]   = LINKTOSPAN;      // = 2
tospace.width.mantissa[0]    = 1;

threespace.stream.mantissa[0] = LINKTHREESPAN;  // = 3
threespace.width.mantissa[0]  = 1;
```

Each probe retrieves all spanfilade crums whose ORGLRANGE component falls within `[role, role+1)`, meaning all entries for that endset role regardless of which link they belong to. The link ISA is then read out of the ORGLRANGE key component.

---

### Summary

| Question | Answer |
|---|---|
| Entries per link | One **per I-span per endset role** (not one per endset, not one total) |
| FROM entries | ORGLRANGE key = `1.linkISA`, SPANRANGE key = I-span stream/width |
| TO entries | ORGLRANGE key = `2.linkISA`, SPANRANGE key = I-span stream/width |
| THREE entries | ORGLRANGE key = `3.linkISA`, SPANRANGE key = I-span stream/width |
| Discriminant | High tumbler component of ORGLRANGE: 1=source, 2=target, 3=type |
| Width on ORGLRANGE | Always zero (point, not range) — link ISA is a unique address |
| Payload | `linfo.homedoc` = link ISA (or SPORGL home document) |

The design gives O(log n) lookup in either direction: given an I-span you can find all links that include it (any role) by probing SPANRANGE; given a link ISA you can enumerate its endsets by probing ORGLRANGE. The `LINKFROMSPAN`/`LINKTOSPAN`/`LINKTHREESPAN` prefix is the sole structural distinction between source, target, and type entries — there is no separate index or sub-tree per role.

---

## Question 15 [gregory]

> When an endset specset references content that spans multiple non-contiguous I-address ranges in the source document's POOM, does `vspanset2sporglset` split it into multiple sporgls before link creation, and are all resulting I-spans stored in the link orgl and independently indexed in the spanfilade?

### Gregory's Answer

## KB Synthesis

Yes to all three parts.

## Splitting into multiple sporgls

`vspanset2sporglset` always splits a V-span into one sporgl per contiguous I-address region, regardless of how many V-spans were provided as input. The conversion chain is:

V-span → `vspanset2ispanset` → `permute` → `span2spanset` → `retrieverestricted` → one I-span per contiguous region → one sporgl per I-span.

When a V-span covers content transcluded from multiple source documents, those source documents contribute non-contiguous I-address ranges in the POOM. The inner loop in `vspanset2sporglset` (`sporgl.c:49-58`) iterates over every I-span returned by the V→I conversion and creates a separate sporgl for each. The front end sees a single contiguous V-selection; the backend decomposes it transparently. [SS-LINK-ENDPOINT] (Finding 0037), [ST-LINK-CREATE] (Finding 0037)

**Concrete example:**
```
Doc C has "AABB" at V 1.1..1.4:
  "AA" transcluded from doc A → I-addresses from A's permascroll
  "BB" transcluded from doc B → I-addresses from B's permascroll

create_link(source = V-span 1.1 width 0.4 in C)

Input:  1 V-span
Output: 2 sporgls:
  sporgl₁: origin=I-addr(A,"AA"), width=0.2, doc=C
  sporgl₂: origin=I-addr(B,"BB"), width=0.2, doc=C
```

## Storage in the link orgl

All resulting sporgls are stored as the link's endset. The link endset is internally `set<Sporgl>`, not `set<VSpan>`. The cardinality of the stored endset may exceed the number of input V-spans — one I-span per contiguous I-address region. [SS-LINK-ENDPOINT] (Finding 0037), [SS-SPORGL]

## Independent indexing in the spanfilade

Yes. `insertendsetsinspanf()` (`do2.c:116-128`) receives the full sporglset for each endpoint type (FROM, TO, THREE) and inserts each sporgl as a separate entry into the spanf index, tagged with the link ISA and endpoint type. The spanf maps: `I-address-range → (link-ISA, endpoint-type)`. Each sporgl produces an independent spanf entry covering its own I-address range.

This is why partial I-address overlap is sufficient for `find_links` to discover a link — each sporgl is indexed independently, so matching any one of them returns the link. [INT-SPORGL-LINK-INDEX] (Finding 0013), [ST-CREATE-LINK] (Finding 0012)

The formal postcondition for `create_link`:
```
link.source_endset = { sporgl(origin=i.start, width=i.width, doc=source_doc)
                       | i ∈ V_to_ISpans(source_doc, source_vspan) }

spanf' = spanf ∪ { i-range → (link_isa, LINKFROMSPAN)
                   | i-range ∈ endset_iranges(link.source) }
       ∪ { i-range → (link_isa, LINKTOSPAN)
                   | i-range ∈ endset_iranges(link.target) }
       (+ THREE endset similarly)
```

---

## Code Exploration

Now I have everything I need. Let me trace the full execution path with all citations.

---

## Answer

### The Short Answer

**Yes on both counts.** When an endset's vspanset references content spanning multiple non-contiguous I-address ranges in the source document's POOM, `vspanset2sporglset` does split it into one sporgl per contiguous I-range. Each resulting sporgl is then independently inserted into the link's POOM orgl **and** independently indexed in the spanfilade. Here is the full traced execution:

---

### Step 1: Entry into link creation

`createlink` in `fns.c:100-112` calls `docreatelink` in `do1.c:195`:

```c
// do1.c:195-221
bool docreatelink(typetask *taskptr, typeisa *docisaptr, typespecset fromspecset, ...)
{
  ...
  && specset2sporglset (taskptr, fromspecset, &fromsporglset, NOBERTREQUIRED)   // line 214
  && specset2sporglset (taskptr, tospecset,   &tosporglset,   NOBERTREQUIRED)   // line 215
  && specset2sporglset (taskptr, threespecset,&threesporglset,NOBERTREQUIRED)   // line 216
  && setlinkvsas (&fromvsa, &tovsa, &threevsa)                                  // line 217
  && insertendsetsinorgl (taskptr, linkisaptr, link,
         &fromvsa, fromsporglset, &tovsa, tosporglset, ...)                     // line 218
  && insertendsetsinspanf (taskptr, spanf, linkisaptr,
         fromsporglset, tosporglset, threesporglset)                            // line 219
```

---

### Step 2: `specset2sporglset` dispatches to `vspanset2sporglset`

`sporgl.c:14-33`:

```c
bool specset2sporglset(typetask *taskptr, typespecset specset,
                       typesporglset *sporglsetptr, int type)
{
    ...
    for (; specset; specset = ...) {
        if (itemid == ISPANID) {
            *sporglsetptr = (typesporglset)specset;            // pass through
        } else if (itemid == VSPECID) {
            sporglsetptr = vspanset2sporglset(taskptr,         // line 25
                &((typevspec *)specset)->docisa,
                ((typevspec *)specset)->vspanset,
                sporglsetptr, type);
        }
    }
```

For a client-supplied V-space specset (the normal case), each `VSPECID` entry — including its full `vspanset` list — is passed to `vspanset2sporglset`.

---

### Step 3: `vspanset2sporglset` — the splitting site

`sporgl.c:35-65`:

```c
typesporglset *vspanset2sporglset(typetask *taskptr, typeisa *docisa,
    typevspanset vspanset, typesporglset *sporglsetptr, int type)
{
  typeorgl orgl;
  typesporgl *sporglset;
  typeispanset ispanset;

    ispanset = NULL;
    if (!findorgl(taskptr, granf, docisa, &orgl, type))       // line 44 - find source doc POOM
        return(NULL);
    for (; vspanset; vspanset = vspanset->next) {             // line 47 - for each vspan
        (void) vspanset2ispanset(taskptr, orgl, vspanset,     // line 48 - V→I conversion
                                 &ispanset);
        for (; ispanset; ispanset = ispanset->next) {         // line 49 - for each resulting ispan
            sporglset = (typesporgl *) taskalloc(...);
            sporglset->itemid = SPORGLID;
            movetumbler(docisa, &sporglset->sporgladdress);   // source doc ISA
            movetumbler(&ispanset->stream, &sporglset->sporglorigin); // I-origin
            movetumbler(&ispanset->width,  &sporglset->sporglwidth);  // I-width
            *sporglsetptr = (typesporglset)sporglset;
            sporglsetptr  = (typesporglset *)&sporglset->next;
        }
    }
    return(sporglsetptr);
}
```

The critical structure is the **nested loop** at lines 47–58:

- **Outer loop** (line 47): iterates the vspanset — each client-supplied V-span.
- **`vspanset2ispanset`** (line 48): calls `permute()` in `orglinks.c:404`, which calls `span2spanset()` → `retrieverestricted()`. This walks the POOM enfilade looking for every I-address range that maps to the queried V-span. If the content at that V-address was assembled from three non-contiguous source regions (e.g., copied from I-spans A, B, C into the POOM), `retrieverestricted` returns **three separate context records**, and `permute` converts each into a distinct `typeispan` in `ispanset`.
- **Inner loop** (line 49): allocates **one sporgl per ispan**. So if a single vspan maps to three discontiguous I-ranges, you get three sporgls appended to the sporglset.

---

### Step 4: All sporgls inserted into the link's POOM via `insertendsetsinorgl`

`do2.c:130-148`:

```c
bool insertendsetsinorgl(typetask *taskptr, tumbler *linkisaptr, typeorgl link,
    tumbler *fromvsa, typesporglset fromsporglset, ...)
{
    insertpm(taskptr, linkisaptr, link, fromvsa, fromsporglset)   // line 132
    && insertpm(taskptr, linkisaptr, link, tovsa, tosporglset)    // line 133
```

`insertpm` in `orglinks.c:75-134` iterates the sporglset:

```c
for (; sporglset; sporglset = sporglset->xxxxsporgl.next) {   // line 100
    unpacksporgl(sporglset, &lstream, &lwidth, &linfo);        // line 101
    movetumbler(&lstream, &crumorigin.dsas[I]);                // line 105 - I-stream → origin
    movetumbler(&lwidth,  &crumwidth.dsas[I]);                 // line 109 - I-width
    movetumbler(vsaptr,   &crumorigin.dsas[V]);                // line 113 - V position in link
    ...
    insertnd(taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V); // line 130
    tumbleradd(vsaptr, &crumwidth.dsas[V], vsaptr);            // line 131 - advance V address
}
```

Each sporgl (= each distinct I-range from the source doc) becomes **one crum in the link's POOM**, inserted at a sequentially advancing V-address within the link. The I-addresses are preserved in the crum's `dsas[I]` fields. Three non-contiguous source I-ranges → three crums in the link orgl, placed at consecutive V positions `1.1`, `1.1+w1`, `1.1+w1+w2`, etc.

---

### Step 5: All sporgls indexed independently in the spanfilade via `insertendsetsinspanf`

`do2.c:116-128`:

```c
bool insertendsetsinspanf(typetask *taskptr, typespanf spanfptr,
    typeisa *linkisaptr, typesporglset fromsporglset, ...)
{
    insertspanf(taskptr, spanfptr, linkisaptr, fromsporglset, LINKFROMSPAN)   // line 119
    && insertspanf(taskptr, spanfptr, linkisaptr, tosporglset, LINKTOSPAN)    // line 120
    // optional: insertspanf(..., threesporglset, LINKTHREESPAN)              // line 123
```

`insertspanf` in `spanf1.c:15-54` iterates the sporglset:

```c
for (; sporglset; sporglset = ...) {                       // line 25
    if (itemid == SPORGLID) {
        movetumbler(&sporglset->sporglorigin, &lstream);   // line 31 - I-origin
        movetumbler(&sporglset->sporglwidth,  &lwidth);    // line 32 - I-width
        movetumbler(&sporglset->sporgladdress,&linfo.homedoc); // line 33 - source doc ISA
    }
    movetumbler(&lstream, &crumorigin.dsas[SPANRANGE]);    // line 49
    movetumbler(&lwidth,  &crumwidth.dsas[SPANRANGE]);     // line 50
    insertnd(taskptr, (typecuc*)spanfptr,                  // line 51
             &crumorigin, &crumwidth, &linfo, SPANRANGE);
}
```

Again one `insertnd` call per sporgl. Each non-contiguous I-range becomes its own independent entry in the spanfilade, keyed by its I-address range and tagged with the link's ISA and the endset role (LINKFROMSPAN = 1, LINKTOSPAN = 2, LINKTHREESPAN = 3 — set in `crumorigin.dsas[ORGLRANGE]` via `prefixtumbler` at `spanf1.c:22`).

---

### Summary

| Question | Answer | Key site |
|---|---|---|
| Does `vspanset2sporglset` split a vspan that maps to N non-contiguous I-ranges into N sporgls? | **Yes** — inner loop at `sporgl.c:49-58`, one sporgl per `ispan` returned by `vspanset2ispanset` | `sporgl.c:47-58` |
| Are all resulting I-spans stored in the link orgl? | **Yes** — `insertendsetsinorgl` → `insertpm` iterates the full sporglset, one `insertnd` per sporgl | `orglinks.c:100-131` |
| Are all resulting I-spans indexed independently in the spanfilade? | **Yes** — `insertendsetsinspanf` → `insertspanf` iterates the full sporglset, one `insertnd` per sporgl | `spanf1.c:25-51` |

The system makes **no attempt to re-merge** split sporgls at any stage. Each contiguous I-range from the source document ends up as exactly one crum in the link orgl and one crum in the spanfilade, with its original I-address range preserved intact. This means that a link endset referencing V-content assembled from three scattered source regions will create three independently findable spanfilade entries — all pointing to the same link ISA and the same endset role.

---

## Question 16 [gregory]

> The link's I-address allocation advances past the text range, creating gaps for subsequent text inserts — is this because link and text I-addresses share a single allocation namespace under `docISA.0.1.x` vs `docISA.0.2.x`, or is the gap an artifact of how `findisatoinsertmolecule` scans?

### Gregory's Answer

## KB Synthesis

Both factors are at play, but the scan behavior of `findisatoinsertmolecule` is the proximate cause.

## Address Structure: Separate Element Subspaces

Link and text I-addresses do occupy different element_field subspaces within the document's content region [SS-ADDRESS-SPACE Finding 0065]:

- Links: `docISA.0.2.x` (element_field = 2)
- Text: `docISA.0.3.x` (element_field = 3, based on Finding 0033's `2.1.0.1.0.1.3.x` pattern)

So the `docISA.0.1.x` vs `docISA.0.2.x` framing in the question is close but off by one — it's element_field 2 (links) vs element_field 3 (text). They are nominally in different subspaces.

## Why the Gap Occurs Anyway

The gap is an artifact of the scan. Both text INSERT and CREATELINK call `findisatoinsertmolecule` on the **same global granfilade** [INT-LINK-INSERT, Finding 0063]. The mechanism is stateless query-and-increment: `findpreviousisagr` finds the highest existing I-address **below the caller's upper bound**, then increments by 1.

The critical detail [SS-ADDRESS-SPACE Finding 0077]:

> Allocation is stateless query-and-increment on **different tumbler ranges** via `findpreviousisagr`.

For MAKELINK, the upper bound is computed as `tumblerincrement(docISA, 2, atomtype+1)` where LINKATOM = 2, giving an upper bound in the element_field 3 region — i.e., the same upper bound range that text allocation uses [SS-ADDRESS-SPACE Finding 0065, code]. This means the text allocator's upper bound scan **encompasses the link element subspace** (element_field 2 is below element_field 3 in tumbler order).

After CREATELINK allocates at, say, `docISA.0.2.3`, `findpreviousisagr` for the next text INSERT finds `docISA.0.2.3` as the highest I-address below the text upper bound. It increments to `docISA.0.2.4` — now squarely in the link subspace, and non-contiguous with the previous text run at `docISA.0.3.x`.

The KB states this directly [INT-LINK-INSERT, Finding 0063]:

> "link orgls and text characters share the same allocation sequence... all allocations (text and non-text) draw from the same monotonically increasing sequence"

And [INV-MONOTONIC, Finding 0063]:

> `text_contiguous(insert_a, insert_b) ⟺ ¬∃ alloc_c : time(a) < time(c) < time(b) ∧ alloc_c ∈ content_allocations`

The content allocation set is `{INSERT, COPY, CREATELINK}` — both TEXTATOM and LINKATOM allocations are in scope. CREATENEWVERSION, by contrast, does **not** call `findisatoinsertmolecule` for content (it only allocates a document address via `findisatoinsertnonmolecule`), which is why it does not break text contiguity [INV-MONOTONIC, Finding 0077].

## Summary

The subspaces are nominally distinct (element_field 2 vs 3), so this is not a case of sharing one flat namespace. The gap arises because the text allocator's upper bound for `findpreviousisagr` is set broadly enough to include the link I-address subspace. After CREATELINK, `findpreviousisagr` legitimately finds the link orgl as the current maximum within the scan range and increments from there — a scan artifact, not a shared-counter artifact [SS-ADDRESS-SPACE Finding 0077, INV-MONOTONIC Finding 0063, INT-LINK-INSERT Finding 0063].

---

## Code Exploration

Now I have everything I need. Let me compile the complete answer from the code analysis and empirical data.

---

## Answer

The question contains a partially correct premise. Here is the full picture, traced from the code.

---

### The Namespace Structure: `docISA.0.1.x` for Text, `docISA.0.2.x` for Links

Both text atoms and link atoms are stored in the **same global `granf`** and both go through `findisatoinsertmolecule` [granf2.c:158–181]. The **only** architectural distinction is `hint.atomtype`:

- Text insert [`do1.c:117`]: `makehint(DOCUMENT, ATOM, TEXTATOM, docisaptr, &hint)` → `atomtype = 1`
- Link creation [`do1.c:207`]: `makehint(DOCUMENT, ATOM, LINKATOM, docisaptr, &hint)` → `atomtype = 2`

Both values are defined in [`xanadu.h:145–146`]:
```c
#define TEXTATOM  1
#define LINKATOM  2
```

Inside `findisatoinsertmolecule` [`granf2.c:162`], the **upperbound** for the `findpreviousisagr` scan is:

```c
tumblerincrement (&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound);
```

With `docISA = 1.1.0.1.0.1` (mantissa `[1,1,0,1,0,1,0,…]`, last non-zero at position 5 = idx):

| atomtype | rightshift | bint | upperbound | formula |
|----------|-----------|------|------------|---------|
| TEXTATOM=1 | 2 | 2 | mantissa[7]=2 → `1.1.0.1.0.1.0.2` | `docISA.0.2` |
| LINKATOM=2 | 2 | 3 | mantissa[7]=3 → `1.1.0.1.0.1.0.3` | `docISA.0.3` |

The scan boundaries are separated by exactly one tumbler digit.

---

### How the First Address in Each Subspace Is Assigned

**First text character** — the granfilade is empty except for the doc orgl at `docISA`. `findpreviousisagr` with upper bound `docISA.0.2` returns `lowerbound = docISA` (the doc orgl itself). `tumblerlength(docISA) == tumblerlength(lowerbound)` (both 6), so the **first branch** fires [`granf2.c:165–167`]:

```c
tumblerincrement (&lowerbound, 2, hintptr->atomtype, isaptr);   // docISA.0.1 (atomtype=1)
tumblerincrement (isaptr, 1, 1, isaptr);                        // docISA.0.1.1
```

Tracing: idx=5 in `docISA`, rightshift=2, bint=1 → mantissa[7]=1 → `1.1.0.1.0.1.0.1`. Then rightshift=1, bint=1 → idx=7, mantissa[8]=1 → **`1.1.0.1.0.1.0.1.1`** = `docISA.0.1.1`.

Subsequent text characters increment from lowerbound via `tumblerincrement(&lowerbound, 0, 1, isaptr)` [`granf2.c:169`]: each successive insert yields `docISA.0.1.2`, `docISA.0.1.3`, `docISA.0.1.4`, …

**First link** — after "ABC" at `docISA.0.1.{1,2,3}`, `findpreviousisagr` with upper bound `docISA.0.3` returns `lowerbound = docISA.0.1.3`. `tumblerlength` is 9 ≠ 6, so the **LINKATOM branch** fires [`granf2.c:171–175`]:

```c
tumblerincrement (&hintptr->hintisa, 2, 2, isaptr);   // docISA.0.2
if (tumblercmp (&lowerbound, isaptr) == LESS)          // docISA.0.1.3 < docISA.0.2? YES (pos7: 1<2)
    tumblerincrement (isaptr, 1, 1, isaptr);           // docISA.0.2.1
```

idx=7 (value 2 in `docISA.0.2`), rightshift=1, bint=1 → mantissa[8]=1 → **`1.1.0.1.0.1.0.2.1`** = `docISA.0.2.1`.

This matches the empirically confirmed link ISA in the golden test [`golden/internal/insert_link_insert_iaddress_gap.json:17`]:
```json
"result": "1.1.0.1.0.1.0.2.1"
```
and in Finding 0065's table (L1 in doc `1.1.0.1.0.1` → ISA `1.1.0.1.0.1.0.2.1`).

---

### Does Link Allocation Create a Gap for Subsequent Text?

**No.** This is where the question's premise needs correction.

After CREATELINK inserts the link orgl at `docISA.0.2.1`, the **text allocator's upper bound is still `docISA.0.2`**. The link orgl at `docISA.0.2.1` satisfies:

```
docISA.0.2.1  vs  docISA.0.2:
  mantissa[0..7] equal ([1,1,0,1,0,1,0,2])
  mantissa[8]: 1 > 0  → docISA.0.2.1 > docISA.0.2
```

The link orgl is **above** the text upper bound. `findpreviousisagr` for the next text insert finds only the text chars at `docISA.0.1.x` (all < `docISA.0.2`) and the doc orgl at `docISA` — not the link. The result:

```
lowerbound = docISA.0.1.3  (last text char, ABC)
tumblerincrement(docISA.0.1.3, 0, 1) → docISA.0.1.4  (next text ISA)
```

**Text allocation resumes contiguously at `docISA.0.1.4`.** The link at `docISA.0.2.1` is invisible to the text allocator.

---

### Then Why Does `compare_versions` Show 2 Span Pairs?

The 2-pair result in the golden test is a **V-space artifact**, not evidence of an I-address gap.

After CREATELINK, the document's vspanset is consolidated to include the link subspace (V-position 2.x). `findnextlinkvsa` [`do2.c:151–167`] computes the document's full vspan reach:

```c
(void) doretrievedocvspan (taskptr, docisaptr, &vspan);
tumbleradd (&vspan.stream, &vspan.width, &vspanreach);
if (tumblercmp (&vspanreach, &firstlink) == LESS)
    movetumbler (&firstlink, vsaptr);
else
    movetumbler (&vspanreach, vsaptr);
```

The `retrievedocvspanset` output after CREATELINK is `[{start: 0, width: 0.1}, {start: 1, width: 1}]` (per Finding 0038). The document's total V-reach is now ~2.x. When the test inserts "DEF" "at end", the client places it at V-position ~2 (beyond the link reference at 2.1). "DEF" in the **source** document ends up at V-positions in the 2.x range, while in the version **dest** (without the link), "DEF" sits at V-position 1.4.

`compare_versions` maps shared I-spans back to V-positions in each document. With DEF at different V-positions (source: 2.x, dest: 1.4), the return is two span pairs — one for ABC, one for DEF — even though the underlying I-addresses `docISA.0.1.1`–`docISA.0.1.6` are fully contiguous in the granfilade.

---

### Summary

| Question | Answer |
|----------|--------|
| Do text and link I-addresses share a single allocation namespace? | **Yes** — both go through `findisatoinsertmolecule` in the global `granf` |
| Are they in distinct subspaces? | **Yes** — text at `docISA.0.1.x`, links at `docISA.0.2.x`, encoded by `atomtype` directly into the ISA |
| Is the subspace assignment a `findisatoinsertmolecule` artifact? | They are the same thing — the scan's atomtype-dependent upperbound [`granf2.c:162`] **is** the namespace structure |
| Does link allocation create a gap for subsequent text? | **No** — the text upperbound `docISA.0.2` fences out `docISA.0.2.x` (link subspace), so text continues monotonically in `docISA.0.1.x` |
| What causes the 2-span-pair result in compare_versions? | V-space displacement — "at end" text inserts land at V-position 2.x (after the link reference), creating a V-space gap between ABC (1.x) and DEF (2.x) in the source document |

The mechanism is a **shared namespace with strict subspace isolation** — both framings in the question describe the same design. The `atomtype` field (TEXTATOM=1, LINKATOM=2) is injected into the ISA at mantissa position 7 via [`granf2.c:162`]'s `tumblerincrement`, creating non-overlapping ranges. `findisatoinsertmolecule`'s bounded scan enforces that isolation on every allocation. The "gap" the question observes is in V-space (POOM), not in the granfilade I-address sequence.

---

## Question 17 [gregory]

> When a link's type endset references content at `1.0.2.x` in the global type namespace, is that type content created by a prior INSERT into a dedicated type document, or is there a separate type registration mechanism outside the normal document operations?

### Gregory's Answer

## KB Synthesis

The KB does not contain enough information to answer this fully.

What the KB does establish:

**Type content exists in a bootstrap document** [SS-LINK-ENDPOINT, Finding 0024]:
- Link types are stored as VSpec references to a type registry at addresses like `1.0.2.2` (JUMP), `1.0.2.3` (QUOTE), `1.0.2.6` (FOOTNOTE), `1.0.2.6.2` (MARGIN) in a "bootstrap document (doc 1)"
- The type hierarchy is encoded in the tumbler containment structure — MARGIN is nested under FOOTNOTE because `1.0.2.6.2` is contained within `1.0.2.6`
- The client (`febe/client.py`) constructs VSpecs referencing these addresses directly by address, not by any lookup or registration call

**What the KB does NOT say:**

The KB has no findings that describe *how* those `1.0.2.x` addresses were populated. There is no documented type registration opcode, no finding showing an INSERT into doc 1 producing type content, and no description of bootstrap/initialization procedures that pre-populate the type registry.

The bootstrap document is referenced only as a pre-existing entity whose type addresses the client hardcodes. Whether those addresses were written by normal INSERT operations during system initialization, by a special seeding procedure during installation, or by some other mechanism entirely — the KB is silent on this.

If you need to establish the mechanism, it would require examining the system initialization code (likely in `entexit.c` or similar startup paths) or the bootstrap document creation logic, which have not been covered by the findings in the KB.

---

## Code Exploration

Now I have everything I need. Here is the complete answer sourced directly from the C code.

---

## Answer: Link Type Registration in udanax-green

**There is no separate type registration mechanism.** The backend treats the type endset as an ordinary V-space reference into an ordinary document. Whether content exists at `1.0.2.x` depends entirely on whether a prior operation (INSERT, COPY, etc.) placed content there. Nothing in the backend pre-populates or registers type addresses.

---

### Execution path through `createlink`

**`fns.c:100-112`** — FEBE handler, no special handling of the type endset:
```c
void createlink(typetask *taskptr)
{
    typeisa docisa, linkisa;
    typespecset fromspecset, tospecset, threespecset;
    ...
    if (
       getcreatelink(taskptr, &docisa, &fromspecset, &tospecset, &threespecset)
    && docreatelink(taskptr, &docisa, fromspecset, tospecset, threespecset, &linkisa))
        putcreatelink(taskptr, &linkisa);
```

**`do1.c:195-221`** — `docreatelink`, the type endset is processed identically to FROM and TO:
```c
bool docreatelink(typetask *taskptr, typeisa *docisaptr,
    typespecset fromspecset, typespecset tospecset,
    typespecset threespecset, typeisa *linkisaptr)
{
    ...
    return (
         createorglingranf(taskptr, granf, &hint, linkisaptr)
      && tumbler2spanset(taskptr, linkisaptr, &ispanset)
      && findnextlinkvsa(taskptr, docisaptr, &linkvsa)
      && docopy(taskptr, docisaptr, &linkvsa, ispanset)
      && findorgl(taskptr, granf, linkisaptr, &link, NOBERTREQUIRED)  // line 213
      && specset2sporglset(taskptr, fromspecset, &fromsporglset, NOBERTREQUIRED)  // line 214
      && specset2sporglset(taskptr, tospecset,   &tosporglset,   NOBERTREQUIRED)  // line 215
      && specset2sporglset(taskptr, threespecset, &threesporglset, NOBERTREQUIRED) // line 216
      && setlinkvsas(&fromvsa, &tovsa, &threevsa)
      && insertendsetsinorgl(...)
      && insertendsetsinspanf(...)
    );
}
```

All three endsets pass through exactly the same `specset2sporglset` call with `NOBERTREQUIRED`. There is no type-specific branch.

---

### How `specset2sporglset` resolves the type address

**`sporgl.c:14-33`** — iterates the specset items, dispatches VSpec items to `vspanset2sporglset`:
```c
bool specset2sporglset(typetask *taskptr, typespecset specset,
                       typesporglset *sporglsetptr, int type)
{
    for (; specset; specset = ...) {
        if (...itemid == VSPECID) {
            if (!(sporglsetptr = vspanset2sporglset(
                    taskptr,
                    &((typevspec *)specset)->docisa,   // the type document address
                    ((typevspec *)specset)->vspanset,  // the V-span within it (1.0.2.x)
                    sporglsetptr, type)))
                return (FALSE);
        }
    }
}
```

**`sporgl.c:35-65`** — `vspanset2sporglset` converts V-spans to I-spans (sporgls) by calling `findorgl` on the referenced document:
```c
typesporglset *vspanset2sporglset(typetask *taskptr, typeisa *docisa,
    typevspanset vspanset, typesporglset *sporglsetptr, int type)
{
    typeorgl orgl;
    ...
    if (!findorgl(taskptr, granf, docisa, &orgl, type)) {  // line 44
        return (NULL);                                      // FAILS if doc not found
    }
    for (; vspanset; vspanset = vspanset->next) {
        (void) vspanset2ispanset(taskptr, orgl, vspanset, &ispanset);  // V→I
        for (; ispanset; ispanset = ispanset->next) {
            // builds sporgl from I-coords
        }
    }
}
```

If `findorgl` returns NULL — because the type document doesn't exist in the granfilade — `vspanset2sporglset` returns NULL, `specset2sporglset` returns FALSE, and `docreatelink` fails. **The type document must already exist.**

---

### `NOBERTREQUIRED` bypasses open/close, not existence

**`granf1.c:17-41`** — `findorgl` with `NOBERTREQUIRED`:
```c
bool findorgl(typetask *taskptr, typegranf granfptr, typeisa *isaptr,
              typeorgl *orglptr, int type)
{
    if ((temp = checkforopen(isaptr, type, user)) <= 0) {
        if (!isxumain) {    // in standalone mode, skip the error
            return FALSE;
        }
    }
    *orglptr = fetchorglgr(taskptr, granfptr, isaptr);  // disk lookup
    return (*orglptr ? TRUE : FALSE);
}
```

**`bert.c:52-61`** — `checkforopen` with `NOBERTREQUIRED` short-circuits immediately:
```c
int checkforopen(tumbler *tp, int type, int connection)
{
    if (type == NOBERTREQUIRED) {
        return 1;    /* Random > 0 */
    }
    // ... bert table lookup ...
}
```

`NOBERTREQUIRED` skips the open/close protocol (the bert table) — the type document doesn't need to be explicitly OPENed. But it does not skip the disk lookup (`fetchorglgr`). The orgl must exist in the granfilade.

Additionally, `isxumain = TRUE` is set in **`xumain.c:23`** for the standalone backend, which means even if `checkforopen` returned a failure, the error path in `findorgl` is bypassed. Standalone mode is more permissive still — but `fetchorglgr` returning NULL will still propagate as failure.

---

### No initialization creates type documents

**`entexit.c:19-47`** — `initmagicktricks` initializes only the enfilade infrastructure:
```c
int initmagicktricks(void)
{
    initgrimreaper();
    initqueues();
    clear(&ZEROTUMBLERvar, sizeof(tumbler));
    if (initenffile()) {
        initkluge((typecuc**)&granf, (typecuc**)&spanf);   // restore existing enf
    } else {
        granf = (typegranf) createenf(GRAN);               // fresh granfilade
        spanf = (typespanf) createenf(SPAN);               // fresh spanfilade
    }
}
```

No type documents, no pre-populated addresses, no registration tables. The `init()` function in **`init.c:25-79`** only installs FEBE handler function pointers.

**`xumain.c:30-63`** — the full startup sequence:
```c
int main(void)
{
    processrcfile();
    init(0);
    inittask(&task);
    initmagicktricks();
    getaccount(&task, &task.account);
    for (;;) { xanadu(&task); }
}
```

Nothing here creates content at `1.0.2.x` or any type address.

---

### What happens if the content doesn't exist

If the type document's orgl exists but no content was ever inserted at V-coordinate `1.0.2.x`, then `vspanset2ispanset` returns an empty `ispanset`. The inner `for (; ispanset; ...)` loop in `vspanset2sporglset` never executes. `threesporglset` ends up NULL.

In `do1.c:219` (inside `insertendsetsinspanf`):
```c
if (threesporglset) {                                    // guarded by NULL check
    if (!insertspanf(..., threesporglset, LINKTHREESPAN)) { ... }
}
```

The type endset is silently omitted from the spanfilade index. The link is created but with no type entry. There is no error.

---

### Summary

| Question | Answer |
|---|---|
| Is there a separate type registration mechanism? | **No.** The backend has no such function. |
| How are types at `1.0.2.x` created? | By ordinary INSERT or COPY operations placing content at those V-coordinates in a type document. |
| Does `NOBERTREQUIRED` bypass document existence? | **No.** It bypasses the open/close (bert) protocol only. `fetchorglgr` still requires the orgl to exist on disk. |
| What if no content exists at `1.0.2.x`? | V→I conversion yields empty ispanset; type sporgl is silently dropped; link is created without a type index entry. |
| Is there startup initialization of type documents? | **No.** `initmagicktricks` and `init` create only enfilade infrastructure, never content. |

The `1.0.2.x` addresses are conventional — the client hardcodes them as well-known type coordinates in whatever type document it uses — but the backend has no knowledge of them. From the backend's perspective, a type endset is indistinguishable from a FROM or TO endset. It stores whatever V-span reference it is given, converting via V→I only if that content already exists.

---

## Question 18 [gregory]

> If CREATELINK is called with endsets referencing I-addresses that no current POOM maps to (content that was deleted from all documents but persists in the granfilade), does the link creation succeed, and are the resulting spanfilade entries valid for future discovery if that content is later transcluded?

### Gregory's Answer

## KB Synthesis

## Short answer

CREATELINK cannot succeed through the normal API with endsets referencing I-addresses that no current POOM maps to — but if a link reaches that state through post-creation deletion, its spanfilade entries remain permanently valid for future discovery via transclusion.

---

## Part 1: Can CREATELINK produce endsets with unreferenced I-addresses?

The FEBE CREATELINK API takes V-span specsets as endpoint inputs, not I-addresses. The path is: V-spans → `vspanset2sporglset` → `vspanset2ispanset` → `retrieverestricted`, which walks the home document's POOM to resolve V-positions to I-addresses [SS-VSPAN-TO-SPORGL, ST-LINK-CREATE].

From [INV-ITOV-FILTERING] and [SS-FOLLOWLINK]: if `retrieverestricted` finds no POOM entry for a given V-position, it returns NULL and that I-address is silently dropped. If all endpoint I-addresses are unreferenced, the resulting sporglset is empty. An empty (zero-width) endset passed to link creation crashes the backend (Bug 0017) [PRE-LINK-CREATE].

**Conclusion:** Through the normal interface, CREATELINK cannot produce endsets with unreferenced I-addresses — the V-to-I conversion gate prevents it.

The relevant scenario is the inverse: a link is created while the content exists in a POOM, then the content is subsequently deleted from all documents. The link then holds endsets whose I-addresses are no longer mapped by any POOM — the standard orphaned link state [EC-ORPHANED-LINK, EC-GHOST-LINK].

---

## Part 2: Are the spanfilade entries valid for future discovery?

**Yes, unconditionally.**

Three permanent-layer properties guarantee this:

**The link orgl persists.** No operation removes entries from I-space. The link's orgl at its allocated I-address is permanent [INV-LINK-PERMANENCE].

**The spanfilade entries persist.** `insertendsetsinspanf` writes entries at link creation time. No delete mechanism exists anywhere in `spanf1.c` or `spanf2.c`. The entries are write-only [INV-SPANF-WRITE-ONLY]. The mapping `α → link_ISA` survives indefinitely in the spanfilade regardless of what happens to any POOM.

**Discovery is purely I-address intersection.** `find_links` converts the search specset to I-addresses and intersects against the spanfilade [SS-FIND-LINKS]. If any document later acquires a POOM mapping to those I-addresses — via transclusion — the I-address intersection fires and the link is discovered [INT-LINK-TRANSCLUSION].

From [EC-GHOST-LINK]: "Reconstitution is always possible since I-addresses are permanent. VCOPY `a` into new document D2 → `poom.D2(1.1) = a` → FOLLOWLINK(L, TO, D2) works." The granfilade retains the content bytes at those I-addresses forever [INV-IADDR-IMMUTABILITY, INV-NO-IADDR-REUSE], so the I-addresses are both discoverable via spanfilade and resolvable via granfilade once any POOM maps to them.

**The lifecycle:**
```
t0: CREATELINK(source_vspan, target_vspan)
    → spanfilade: α₁..αₙ → link_ISA (permanent)
    
t1: DELETE content from all documents
    → all POOMs: α₁..αₙ no longer mapped
    → find_links → [] (no POOM to match against)
    → follow_link → [] (no V-position to report)
    → spanfilade: α₁..αₙ → link_ISA (UNCHANGED)
    
t2: VCOPY content sharing α₁..αₙ into new document D
    → poom.D: v → α₁..αₙ now mapped
    → find_links(D, v) → [link_ISA] (spanfilade match fires again)
```

This follows from the three-layer model [SS-THREE-LAYER-MODEL]: I-space and spanfilade are permanent; POOM presence is transient. Link discoverability is gated on POOM state, but the spanfilade entries standing behind that gate are never invalidated.

---

## Code Exploration

I now have a complete picture from the source. Here is the full answer.

---

## CREATELINK with Orphaned I-Addresses: Source Analysis

### Framing: What "I-addresses that no current POOM maps to" means

When content is deleted from all documents, `dodeletevspan` [orglinks.c:145-152] calls `deletend` only on the document's POOM:

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

There is no corresponding deletion from the granfilade. Granfilade content — inserted via `inserttextgr` [granf2.c:83-109] using `insertseq` — is never removed. The I-addresses assigned to that content remain permanently valid in the content store.

---

### How the Protocol Accepts Raw I-Spans

`getspecset` [get2.c:162-192] explicitly offers the caller a choice:

```c
prompt (taskptr,"a span? ");
if(!getbool(taskptr,&type))
    return(FALSE);
if(type) {
    specset=(typespec *)taskalloc(taskptr,sizeof(typespan));
    if (!getspan(taskptr,specset,ISPANID))   // direct I-span
        return(FALSE);
}else{
    specset=(typespec *)taskalloc(taskptr,sizeof(typevspec));
    if (!getvspec(taskptr,specset))           // V-spec (doc + V-spans)
        return(FALSE);
}
```

A client can bypass V→I lookup entirely by supplying raw ISPANID items as endsets — including I-addresses that correspond to content deleted from all documents.

---

### Part 1: Does CREATELINK Succeed?

`docreatelink` [do1.c:195-221] runs this chain:

```c
createorglingranf(taskptr, granf, &hint, linkisaptr)          // 1
&& tumbler2spanset(taskptr, linkisaptr, &ispanset)             // 2
&& findnextlinkvsa(taskptr, docisaptr, &linkvsa)               // 3
&& docopy(taskptr, docisaptr, &linkvsa, ispanset)              // 4
&& findorgl(taskptr, granf, linkisaptr, &link, NOBERTREQUIRED) // 5
&& specset2sporglset(taskptr, fromspecset, &fromsporglset, NOBERTREQUIRED) // 6
&& specset2sporglset(taskptr, tospecset, &tosporglset, NOBERTREQUIRED)     // 7
&& specset2sporglset(taskptr, threespecset, &threesporglset, NOBERTREQUIRED)// 8
&& setlinkvsas(&fromvsa, &tovsa, &threevsa)                    // 9
&& insertendsetsinorgl(...)                                     // 10
&& insertendsetsinspanf(...)                                    // 11
```

The critical step is **6–8**. `specset2sporglset` [sporgl.c:14-33]:

```c
for (; specset; specset = ...) {
    if (((typeitemheader *)specset)->itemid == ISPANID) {
        *sporglsetptr = (typesporglset)specset;   // passed through, NO validation
        sporglsetptr = (typesporglset *)&((typeitemheader *)specset)->next;
    } else if (((typeitemheader *)specset)->itemid == VSPECID) {
        if (!(sporglsetptr = vspanset2sporglset(taskptr, &((typevspec *)specset)->docisa,
              ((typevspec *)specset)->vspanset, sporglsetptr, type))) {
            return (FALSE);
        }
    }
}
```

**For ISPANID items, the code performs zero validation.** The I-span is taken as-is and placed directly into the sporglset. There is no lookup, no POOM consultation, no check that the I-address names content in any live document.

**Step 10** — `insertendsetsinorgl` [do2.c:130-149] → `insertpm` [orglinks.c:75-134] — stores the endsets in the link's own POOM. `insertpm` calls `unpacksporgl` [sporgl.c:178-203], which handles ISPANID correctly by reading `stream` and `width` directly. It only fails if the width is zero; a non-zero I-span proceeds.

**Step 11** — `insertendsetsinspanf` [do2.c:116-128] → `insertspanf` [spanf1.c:15-54] — inserts into the global spanfilade:

```c
if (((typeitemheader *)sporglset)->itemid == ISPANID) {
    movetumbler(&((typeispan *)sporglset)->stream, &lstream);
    movetumbler(&((typeispan *)sporglset)->width, &lwidth);
    movetumbler(isaptr, &linfo.homedoc);  // homedoc = link's own ISA
} ...
movetumbler(&lstream, &crumorigin.dsas[SPANRANGE]);
movetumbler(&lwidth, &crumwidth.dsas[SPANRANGE]);
insertnd(taskptr, (typecuc*)spanfptr, &crumorigin, &crumwidth, &linfo, SPANRANGE);
```

The I-address is recorded in SPANRANGE, the link address (prefixed with LINKFROMSPAN / LINKTOSPAN / LINKTHREESPAN) in ORGLRANGE.

**Conclusion: link creation succeeds unconditionally for ISPANID endsets.** The link is fully formed in the granfilade, its POOM contains the endset spans, and the global spanfilade has entries keyed on the provided I-addresses.

---

### The V-Spec Path Behaves Differently

For completeness: if the client instead supplies a VSPECID specset pointing to content that has been deleted from the document, `vspanset2sporglset` [sporgl.c:35-65] calls `vspanset2ispanset` via `permute` [orglinks.c:404-422] → `span2spanset` [orglinks.c:425-454] → `retrieverestricted` on the document's POOM. Since the deletion removed the V→I mapping from the POOM, `retrieverestricted` returns no context, `span2spanset` produces nothing, and the sporglset is empty. `insertspanf`'s loop over an empty sporglset is a no-op. The link is created but no endset entries appear in the spanfilade. **This case does not produce discoverable links.**

---

### Part 2: Are the Spanfilade Entries Valid for Future Discovery?

When the content is later transcluded into a new document:

1. `docopy` [do1.c:45-65] → `insertpm` adds the V→I mapping to the new document's POOM, and `insertspanf(..., DOCISPAN)` records the document-content relationship in the spanfilade.

2. A subsequent FIND query calls `dofindlinksfromtothreesp` [do1.c:348-353] → `findlinksfromtothreesp` [spanf1.c:56-103] → for each endset type, calls `sporglset2linkset` [sporgl.c:222-237] → `sporglset2linksetinrange` [sporgl.c:239-269]:

```c
for (; sporglset; sporglset = ...) {
    if (FALSE/*kluge*/ && ((typeitemheader *)sporglset)->itemid == SPORGLID) {
        infoptr = &linfo;
        movetumbler(&((typesporgl *)sporglset)->sporgladdress, &linfo.homedoc);
    } else
        infoptr = NULL;    // always NULL — the FALSE short-circuits this branch
    ...
    context = retrieverestricted(spanfptr, (typespan*)sporglset, SPANRANGE,
                                 &range, ORGLRANGE, (typeisa*)infoptr);
    for (c = context; c; c = c->nextcontext) {
        beheadtumbler(&c->totaloffset.dsas[ORGLRANGE], &linksa);
        onlinklist(taskptr, linksetptr, &linksa);
    }
}
```

The `FALSE&&SPORGLID` branch is permanently disabled — `infoptr` is always NULL. Discovery calls `retrieverestricted` with a null `docisaptr`, which means `findcbcinarea2d` [retrie.c:229-268] receives a null `infoptr`, and the `crumqualifies2d` homedoc filter [retrie.c:274-279] is skipped entirely:

```c
if ((crumptr->height == 0) && infoptr &&
    !tumblereq(&infoptr->homedoc, &(((type2dcbc *)crumptr)->c2dinfo.homedoc))) {
    return (FALSE);  // only applies when infoptr != NULL
}
```

Discovery is therefore **purely I-address based**. The spanfilade entries created with orphaned I-addresses — regardless of whether `homedoc` was set to the link's ISA or a source document's ISA — are found by any query that overlaps those I-addresses in SPANRANGE, constrained to the appropriate LINKFROMSPAN / LINKTOSPAN / LINKTHREESPAN subspace.

When the content is transcluded, the new document's POOM maps its V-spans to the same I-addresses. `vspanset2sporglset` recovers those I-addresses and passes them to `sporglset2linksetinrange`, which matches against the spanfilade entries created during the original CREATELINK. **The entries are valid and the links are discovered.**

---

### Summary

| Condition | CREATELINK succeeds? | Spanfilade entries created? | Future discovery works? |
|-----------|---------------------|----------------------------|------------------------|
| Endsets as direct ISPANID (I-spans with no current POOM mapping) | **Yes** — no validation in `specset2sporglset` [sporgl.c:20-22] | **Yes** — `insertspanf` [spanf1.c:49-51] stores I-address in SPANRANGE unconditionally | **Yes** — discovery is purely I-address based; homedoc filtering is disabled [retrie.c:274-279] |
| Endsets as VSPECID pointing to deleted content | Yes (link is created) | **No** — empty sporglset from failed V→I permutation | **No** — no entries to find |

The design is intentional at the granfilade level: content in the granfilade is **permanent and append-only**. The I-address space is the durable identity fabric. CREATELINK with direct I-addresses creates a relationship between content identities, not between document positions. When that content is later made visible again through transclusion into any document, the link relationship correctly surfaces — because the spanfilade was indexed on identity, not on visibility.

The one difference in how the entries are stored: for ISPANID endsets, `insertspanf` [spanf1.c:29] records `homedoc = linkisa` (the link's own address), whereas for SPORGLID endsets (converted from V-specs), it records `homedoc = sporgladdress` (the source document's ISA) [spanf1.c:33]. This distinction is currently inert — the homedoc field in the bottom crum is stored but never consulted during retrieval, because the `infoptr` path in `sporglset2linksetinrange` [sporgl.c:251] is unconditionally dead code.

---

## Question 19 [gregory]

> After CREATELINK completes, does `find_links` on the home document discover the newly created link through the link orgl's own I-address in the POOM, through the endset I-spans in the spanfilade, or through both paths — and which path is the actual discovery mechanism?

### Gregory's Answer

## KB Synthesis

`find_links` discovers the newly created link **exclusively through the spanfilade endset entries** — the POOM 2.x entry plays no role in this path.

## The Two Layers CREATELINK Writes

[ST-CREATE-LINK, SS-THREE-LAYER-MODEL] make clear that CREATELINK produces three effects:

1. **I-space (granfilade):** New link orgl at a fresh ISA (e.g., `1.1.0.1.0.1.0.2.1`)
2. **POOM (home document):** V-position 2.x → link orgl ISA (makes the link visible in the document's V-stream)
3. **Spanfilade:** Endset entries mapping the *endpoint content I-addresses* → link ISA (indexed by `insertendsetsinspanf`)

## What `find_links` Actually Searches

[SS-DUAL-ENFILADE] Finding 0012 states it directly: "Link search (`find_links`) accesses only `spanf`." [SS-SPANF-OPERATIONS] confirms the spanfilade maps I-addresses to the links referencing them, and `dofindlinksfromtothree()` delegates entirely to `findlinksfromtothreesp()`.

The search algorithm ([SS-FIND-LINKS]):
1. Convert the query specset to content I-addresses (permascroll addresses from the text subspace)
2. Search the spanfilade for those I-addresses
3. Return any link ISA whose endpoint I-addresses intersect

## Why the POOM 2.x Entry Is Irrelevant to Discovery

The POOM 2.x entry stores the link orgl's ISA — a document-structure address, not a content identity. `find_links` searches by *endpoint content I-addresses*, not by link orgl positions. The 2.x entries serve `retrieve_vspanset` (showing the link in the document's V-stream) and direct orgl access, but are invisible to the spanfilade search.

[INT-LINK-TRANSCLUSION] confirms this architectural separation: when transcluded content makes a link discoverable from a new document, it works because the transclusion shares content I-addresses that match the spanfilade entries — no POOM 2.x entries are involved or required.

## Consequence

This means `find_links` on the home document after CREATELINK succeeds only when the query specset covers content whose I-addresses match the link's endpoint I-addresses in the spanfilade. Querying the home document's *link subspace* (2.x) would not discover the link — the spanfilade is indexed by endpoint content identity, not by where the link orgl lives. [FC-CONTENT-SPANF-ISOLATION] formalizes this: the two search paths are entirely independent.

---

## Code Exploration

All citations confirmed. Here is the complete answer.

---

## How `find_links` Discovers Links After CREATELINK

The answer is **Path 2 only — the endset I-spans in the spanfilade**. The link's own POOM is written during CREATELINK but is never consulted during discovery. Here is the full trace.

---

### What CREATELINK Writes

`docreatelink` [`do1.c:195–221`] ends with two back-to-back writes:

```c
  && insertendsetsinorgl (taskptr, linkisaptr, link, &fromvsa, fromsporglset, ...)   // do1.c:218
  && insertendsetsinspanf (taskptr, spanf, linkisaptr, fromsporglset, ...)            // do1.c:219
```

**Write 1 — POOM** (`insertendsetsinorgl`, `do2.c:130–148`):

Calls `insertpm` to store the endsets inside the link's own granfilade node. This is internal link structure — used by FOLLOWLINK to navigate *from* a known link to its endsets. It is a dead end for discovery.

**Write 2 — Spanfilade** (`insertendsetsinspanf`, `do2.c:116–128`):

```c
insertspanf(taskptr, spanfptr, linkisaptr, fromsporglset, LINKFROMSPAN)  // do2.c:119
insertspanf(taskptr, spanfptr, linkisaptr, tosporglset,   LINKTOSPAN)    // do2.c:120
insertspanf(taskptr, spanfptr, linkisaptr, threesporglset,LINKTHREESPAN) // do2.c:123
```

Inside `insertspanf` [`spanf1.c:15–54`], for each endset I-span in the sporglset:

```c
prefixtumbler (isaptr, spantype, &crumorigin.dsas[ORGLRANGE]);   // spanf1.c:22
movetumbler (&lstream, &crumorigin.dsas[SPANRANGE]);             // spanf1.c:49
movetumbler (&lwidth,  &crumwidth.dsas[SPANRANGE]);              // spanf1.c:50
insertnd(taskptr,(typecuc*)spanfptr,&crumorigin,&crumwidth,&linfo,SPANRANGE); // spanf1.c:51
```

Each node inserted into the spanfilade encodes:
- **ORGLRANGE key**: link ISA prefixed with `LINKFROMSPAN`/`LINKTOSPAN`/`LINKTHREESPAN`
- **SPANRANGE key**: the actual I-span of the endset content
- **`linfo.homedoc`**: the link ISA

The spanfilade is therefore a 2D index: given an I-span in content space (SPANRANGE), it returns the link ISAs of all links whose endsets cover that span (ORGLRANGE).

---

### What FIND Reads

The call chain for FINDLINKSFROMTOTHREE:

**`fns.c:196–201`**:
```c
getfindlinksfromtothree (taskptr, &fromvspecset, &tovspecset, &threevspecset, &homeset)
dofindlinksfromtothree (taskptr, fromvspecset, tovspecset, threevspecset,
                        (typeispan*)NULL/*homeset*/,    // ← homeset silently dropped
                        &linkset)
```

Note the cast to `NULL`: even though the client sends a `homeset` (orgl address restriction), `fns.c:198` discards it, making the search unconditionally global.

**`do1.c:348–353`** — delegates directly to the spanfilade:
```c
return findlinksfromtothreesp(taskptr, spanf, fromvspecset, tovspecset,
                              threevspecset, orglrangeptr, linksetptr);
```

**`spanf1.c:56–103`** — `findlinksfromtothreesp` converts the query V-specsets to sporglsets (I-span form), then calls:
```c
sporglset2linkset (taskptr, (typecuc*)spanfptr, fromsporglset, &fromlinkset,
                   orglrange, LINKFROMSPAN);   // spanf1.c:77
sporglset2linkset (taskptr, (typecuc*)spanfptr, tosporglset,   &tolinkset,
                   orglrange, LINKTOSPAN);     // spanf1.c:85
```

**`sporgl.c:222–269`** — `sporglset2linkset` → `sporglset2linksetinrange`:

```c
// orglrange is NULL (from fns.c:198), so takes the else branch:
context = retrieverestricted (spanfptr, (typespan*)sporglset, SPANRANGE,
                              (typespan*)NULL, ORGLRANGE,
                              (typeisa*)infoptr);            // sporgl.c:261
for (c = context; c; c = c->nextcontext) {
    beheadtumbler(&c->totaloffset.dsas[ORGLRANGE], &linksa); // sporgl.c:264
    onlinklist (taskptr, linksetptr, &linksa);               // sporgl.c:265
}
```

`retrieverestricted` queries the spanfilade with the endset I-spans as the SPANRANGE key and returns all matching ORGLRANGE values. `beheadtumbler` strips the `LINKFROMSPAN`/`LINKTOSPAN` prefix from the ORGLRANGE value to recover the raw link ISA.

The POOM is never opened.

---

### Summary

| | During CREATELINK | During FIND |
|---|---|---|
| **POOM** (link's granfilade node) | Written by `insertendsetsinorgl` [`do1.c:218`] | Never read |
| **Spanfilade** (2D I-span index) | Written by `insertendsetsinspanf` [`do1.c:219`] → `insertspanf` [`spanf1.c:51`] | Read by `sporglset2linksetinrange` [`sporgl.c:259–265`] |

**The actual discovery mechanism is Path 2: the endset I-spans in the spanfilade.** The spanfilade acts as a pre-built reverse index from content spans to link ISAs. FIND never touches the link's own POOM; it searches the spanfilade directly, resolves matching ORGLRANGE entries back to link ISAs via `beheadtumbler`, and returns them. The POOM write at `do1.c:218` enables FOLLOWLINK (endset traversal from a *known* link) — a structurally separate operation that is not involved in discovery.

---

## Question 20 [gregory]

> For a link with endsets spanning content in multiple documents (e.g., source in doc1, target in doc2), are the spanfilade entries keyed by the I-address spans alone regardless of document origin, so that discovery from any third document transcluding either span would find the link?

### Gregory's Answer

## KB Synthesis

Yes — spanfilade entries are keyed by I-address spans alone, independent of document origin. Discovery from any third document transcluding either endpoint span will find the link.

**Indexing at link creation**

When `docreatelink` runs, `insertendsetsinspanf()` inserts all endpoint sporgls into the spanf [ST-CREATE-LINK, SS-SPORGL]. Each sporgl packages `(origin: IAddress, width, sporgladdress: DocISA)`, but the index key is the I-address range. The spanfilade structure is `Map<IAddress, Set<LinkISA>>` [SS-SPANF-OPERATIONS, SS-DUAL-ENFILADE]. The document of origin (`sporgladdress`) is stored for later V-address *resolution*, not for keying discovery.

**Discovery is pure I-address intersection**

`find_links(S) = { L | I-addresses(S) ∩ I-addresses(L.source) ≠ ∅ }` [SS-FIND-LINKS]. The spanfilade search converts the query specset to I-spans, then searches by I-address regardless of which document those I-addresses came from [INT-SPORGL-LINK-INDEX]. Document identity plays no role in the match.

**The orgl-dimension filter is disabled**

`sporglset2linkset()` contains the guard `if (TRUE||!homeset)`, which permanently replaces any caller-supplied orgl range with a hardcoded width-100 range from tumbler zero [EC-FIND-LINKS-GLOBAL, PRE-FIND-LINKS/Finding 0069]. So even if a caller attempted to scope discovery to a specific document, the implementation ignores it. All `find_links` calls are effectively global in the orgl dimension.

**Transclusion makes this the core mechanism**

Because vcopy shares I-addresses rather than copying them [ST-VCOPY, INT-LINK-TRANSCLUSION], any third document transcluding content from either endpoint inherits the same I-addresses. Since spanfilade lookup is I-address-only, that third document will discover the link identically to the original endpoint documents. This is stated as a system-wide invariant: links are globally visible through content identity [INV-LINK-GLOBAL-VISIBILITY].

**Endpoint resolution (V-addresses) is separate**

After discovery, `FOLLOWLINK` or `RETRIEVEENDSETS` resolves I-addresses back to V-positions through the querying document's POOM [SS-FOLLOWLINK, ST-RETRIEVE-ENDSETS]. The `sporgladdress` field is used at this stage to look up which document holds the content — but by then discovery has already succeeded. Unreferenced I-addresses are silently dropped during I-to-V conversion [INV-ITOV-FILTERING], but that is a post-discovery filter, not a discovery gate.

**Concrete implication**

A link with source in doc1 and target in doc2 is fully discoverable from doc3 if doc3 transcludes any content overlapping either endpoint — even partially [SS-FIND-LINKS/Finding 0028]. The spanfilade contains no document-scoped partitioning that would prevent this.

---

## Code Exploration

Now I have a complete picture. Let me compile the full answer.

---

## Answer: Cross-Document Link Discovery via Spanfilade I-Address Keys

The spanfilade is a 2D enfilade (two axes: SPANRANGE and ORGLRANGE). Link endset entries are **keyed purely on I-address spans in the SPANRANGE axis**. The source document is stored as metadata in the crum bottom info but is **explicitly not used as a filter during retrieval**. Cross-document discovery through transcluded content works because I-addresses are permanent and shared across all transclusions.

---

### 1. The Spanfilade Key Structure: `insertspanf` [spanf1.c:15–54]

When `docreatelink` [do1.c:195–221] stores a link's endsets, it ends up calling `insertendsetsinspanf` [do2.c:116–128], which calls `insertspanf` three times (once per endset type):

```c
insertspanf(taskptr, spanfptr, linkisaptr, fromsporglset, LINKFROMSPAN)
insertspanf(taskptr, spanfptr, linkisaptr, tosporglset,   LINKTOSPAN)
insertspanf(taskptr, spanfptr, linkisaptr, threesporglset, LINKTHREESPAN)
```

Inside `insertspanf` [spanf1.c:22–52], for a SPORGLID item:

```c
movetumbler(&((typesporgl*)sporglset)->sporglorigin, &lstream);   // I-address origin
movetumbler(&((typesporgl*)sporglset)->sporglwidth,  &lwidth);    // I-address width
movetumbler(&((typesporgl*)sporglset)->sporgladdress, &linfo.homedoc); // source doc (metadata)
```

Then:

```c
prefixtumbler(isaptr, spantype, &crumorigin.dsas[ORGLRANGE]); // = spantype.linkISA
movetumbler(&lstream, &crumorigin.dsas[SPANRANGE]);           // = I-address of content
insertnd(taskptr, (typecuc*)spanfptr, &crumorigin, &crumwidth, &linfo, SPANRANGE);
```
[spanf1.c:22, 49–51]

The 2D crum key is:
- **ORGLRANGE axis**: `prefixtumbler(linkISA, spantype)` = the link's ISA with the endset type (1=FROM, 2=TO, 3=THREE) prepended [tumble.c:641–650]
- **SPANRANGE axis**: the **I-address** of the linked content

The `linfo.homedoc` (the document that owns the content) is stored in the **bottom crum info**, not in either key axis. It is not indexed.

---

### 2. How V-Spans Become I-Spans: `specset2sporglset` [sporgl.c:14–65]

`docreatelink` calls `specset2sporglset` [do1.c:214–216] to convert from/to/three V-specs into sporgl sets before inserting. For a V-spec input:

```c
vspanset2sporglset(taskptr, &docisa, vspanset, sporglsetptr, type)  // sporgl.c:25
```

This does V→I permutation via `vspanset2ispanset` [sporgl.c:48], then packages each I-span as a sporgl with:

```c
movetumbler(docisa, &sporglset->sporgladdress);       // source document ISA
movetumbler(&ispanset->stream, &sporglset->sporglorigin); // I-address origin
movetumbler(&ispanset->width,  &sporglset->sporglwidth);  // I-address width
```
[sporgl.c:53–55]

So the sporgl carries the home document address as a **side-channel field**, separate from the I-coordinates that become the spanfilade key.

---

### 3. The Retrieval Side: `sporglset2linksetinrange` [sporgl.c:239–269]

When finding links for a given V-span, the query path is:

`dofindlinksfromtothree` [do1.c:348–353] → `findlinksfromtothreesp` [spanf1.c:56–103] → `sporglset2linkset` [sporgl.c:222–237] → `sporglset2linksetinrange` [sporgl.c:239–269]

Inside `sporglset2linksetinrange`, the critical block is:

```c
if (FALSE/*trying to kluge links followable thru versions*/
    && ((typeitemheader*)sporglset)->itemid == SPORGLID) {
        infoptr = &linfo;
        movetumbler(&((typesporgl*)sporglset)->sporgladdress, &linfo.homedoc);
} else
        infoptr = NULL;
```
[sporgl.c:251–255]

**The `FALSE` guard permanently disables home-document filtering.** `infoptr` is always `NULL`. Then:

```c
context = retrieverestricted(spanfptr, (typespan*)sporglset, SPANRANGE,
                             &range, ORGLRANGE, (typeisa*)infoptr);
```
[sporgl.c:259]

The query presents the sporgl as an I-span restriction (`SPANRANGE`), finds all link ISAs in `ORGLRANGE` that overlap, and **never filters by source document**. The comment "trying to kluge links followable thru versions" shows this was a deliberate design decision — disabling the filter was intentional to make links discoverable through transclusions.

---

### 4. The Full Cross-Document Scenario

Given a link with source endset in doc1 and target in doc2, and a third document (doc3) that transcluces content from doc1:

1. **Link creation**: doc1's V-span → I-span via permutation on doc1's granfilade orgl → stored in spanfilade under that I-span + link ISA key. `linfo.homedoc = doc1-ISA` (stored but not indexed).

2. **Discovery from doc3**: doc3's V-span for the same content → I-span via permutation on doc3's granfilade. Because doc3 transcluded content from doc1's permascroll, **both point to the same I-span**.

3. **Retrieval**: `sporglset2linksetinrange` queries the spanfilade with that I-span in SPANRANGE. It hits the same crum (since the key was the I-span, not the V-span or document ISA). `infoptr = NULL` means no document filter. The link ISA is extracted from ORGLRANGE and returned.

---

### Conclusion

**Yes.** The spanfilade is keyed by I-address spans (SPANRANGE) and link ISA + endset type (ORGLRANGE). The source document is stored in `linfo.homedoc` as crum metadata but is never used as a retrieval filter — the `if (FALSE...)` guard at [sporgl.c:251] ensures it. Any document that transcluces content sharing the same I-address (permascroll identity) will discover links whose endsets reference that content, regardless of which document originally contained it or which document is hosting the transclusion. The architecture makes link traversability a property of permanent content identity, not document ownership.
