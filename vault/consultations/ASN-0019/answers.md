# Consultation Answers — Operation Journaling

**Inquiry:** What must the system guarantee about recording and replaying the history of operations performed on content? What properties must an operation log satisfy for faithful state reconstruction?
**Date:** 2026-02-25 15:59
**Questions:** 15 (10 nelson, 5 gregory)

---

## Question 1 [nelson]

> Must the system preserve a complete, ordered record of every operation performed on a document, such that any prior state can be faithfully reconstructed?

### Nelson's Answer

# Must the System Preserve a Complete Record of Every Operation?

The answer has two parts: the **guarantee** is absolute, but the **mechanism** is more flexible than your question implies.

## The Guarantee: Any Prior State Must Be Reconstructable

This is non-negotiable. I said it plainly:

> "The file management system we are talking about automatically keeps track of the changes and the pieces, so that when you ask for a given part of a given version at a given time, it comes to your screen." [LM 2/15]

And:

> "THE PART YOU WANT COMES WHEN YOU ASK FOR IT." [LM 2/16]

The user must be able to reach backward through time to any prior state of any document. This is what I called **historical backtrack**, and it is fundamental — not an add-on, not a feature, but part of what a document IS:

> "A document is really an evolving ONGOING BRAID." [LM 2/14]

The braid includes its entire history. A document that loses its past is a damaged document.

## The Mechanism: Append-Only Storage with Chronological Filing

I described the storage approach quite specifically:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

Changes are filed chronologically — yes, there is an ordering. And I-space is append-only — content, once written, is never overwritten or destroyed. This is not conventional versioning bolted onto a file system. This is the fundamental storage paradigm.

The **historical trace enfilade** was designed specifically for this temporal dimension:

> "we redesigned Barus's linking enfilade system, designed the historical trace enfilade, and formulated the general theory of enfilades" [LM 1/36]

And the enfilade system was built so that:

> "All changes, once made, left the file remaining in canonical order, which was an internal mandate of the system." [LM 1/34]

## But: Operations vs. States

Now here is where I must be precise about what your question actually asks. You ask about preserving "every operation." I described a system that preserves every **change** — every piece of content added, every arrangement — such that states can be reconstructed. This is subtly different from recording every abstract operation as a command log.

The I-space/V-space separation is what makes this work:

- **I-space is append-only.** Every byte ever written has a permanent address. Content is never destroyed. [LM 4/10-4/11]
- **V-space is the arrangement.** Each version defines a different mapping from V-addresses to I-addresses. [LM 4/11]
- **"Deleted" content remains in I-space.** It becomes "not currently addressable, awaiting historical backtrack functions, may remain included in other versions." [LM 4/9]

So the system preserves all CONTENT (I-space, append-only) and must preserve enough about ARRANGEMENTS (V-space mappings) to reconstruct any prior state. Whether this is achieved by recording abstract operations (INSERT at position 5, DELETE span 3-7) or by preserving the V-space mappings directly is an implementation matter.

I acknowledged this flexibility when discussing backtrack for linear text versus hypertext:

> "Being able to go back through changes, and perhaps restore an earlier state, is called the problem of historical backtrack. For simple, linear textual documents this can be done by storing lists of changes and undoing them; and indeed several commercial versioning and backtrack systems are now on the market. But it is rather more difficult to do this for hypertext." [LM 3/13]

Note: "storing lists of changes and undoing them" is ONE method. For hypertext, something more sophisticated is needed — which is precisely why we designed the historical trace enfilade.

## The Prismatic Guarantee

The storage system I called **Prismatic** must support retrieval of any version:

> "We call this system of storage Prismatic because we may think of a given part, or section, as being prismatically refracted when we pass from one version to another. We believe our Prismatic storage can support virtually instantaneous retrieval of any portion of any version (historical or alternative)." [LM 2/19]

And there is no privileged "current" version:

> "There is thus no 'basic' version of a document set apart from other versions—'alternative' versions—any more than one arrangement of the same materials is a priori better than other arrangements." [LM 2/19]

## Summary

| Question | Answer |
|----------|--------|
| Must any prior state be faithfully reconstructable? | **Yes, absolutely.** This is a core guarantee. |
| Must changes be preserved in order? | **Yes.** Changes are "filed chronologically" [LM 2/14]. |
| Must the system store every abstract operation as a command? | **Not specified.** The guarantee is state reconstruction, not operation replay. |
| Must I-space content be preserved permanently? | **Yes.** Append-only, never destroyed. |
| Must V-space arrangements be recoverable for any past version? | **Yes.** This is what historical backtrack means. |

The system must preserve enough ordered information to reconstruct any prior state of any document. Whether that takes the form of an operation log, a sequence of V-space snapshots, or the historical trace enfilade's approach is a question of implementation — but the result must be the same: you pounce on any part of any version at any time, and it materializes.

> "You pounce like a cat on a given thing, and it seems to be there, having been constructed while you wait, as it were, in midair." [LM 2/16]

---

## Question 2 [nelson]

> What must the system guarantee about the identity of each recorded operation — must every operation be uniquely and permanently identifiable?

### Nelson's Answer

# Operation Identity in Xanadu

## The Short Answer

**Literary Machines does not guarantee unique, permanent identity for operations themselves.** What it guarantees is permanent identity for the *results* of operations — the bytes, links, documents, and versions that operations create. Operations are the mechanism; their products are the first-class citizens.

## What IS Permanently Identifiable

Every FEBE operation that creates something returns a permanent identifier for what it created:

- **CREATENEWDOCUMENT**: "This creates an empty document. It returns the id of the new document." [LM 4/65]
- **CREATENEWVERSION**: "This creates a new document with the contents of document \<doc id\>. It returns the id of the new document. The new document's id will indicate its ancestry." [LM 4/66]
- **MAKELINK**: "This creates a link in document \<doc id\>... It returns the id of the link made." [LM 4/68]
- **INSERT**: Content inserted gets permanent I-space addresses. "Native bytes of a document are those actually stored under its control and found directly in storage under its control." [LM 4/11]

Links specifically receive sequential, permanent addresses reflecting their order of creation:

> "The links designated by a tumbler address are in their permanent order of arrival." [LM 4/31]

A link's address — `N.0.U.0.D.V.0.2.755` for the 755th link created in a document — is permanent. Deleting link `2.5` does not renumber `2.6` through `2.N`.

## The Append-Only Model Preserves Traces, Not Operation Records

Nelson's storage model is explicitly append-only:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

This means every operation leaves a permanent trace in I-space. But the trace is *content*, not an operation record. When you INSERT text, new bytes appear at fresh I-space addresses. When you DELETE, those bytes become "not currently addressable, awaiting historical backtrack functions" [LM 4/9] — but the bytes themselves persist. The *operation* that created or removed them is not itself an addressed entity.

## Historical Backtrack Implies Reconstructibility, Not Operation Identity

Nelson promises you can reconstruct any previous state:

> "The file management system we are talking about automatically keeps track of the changes and the pieces, so that when you ask for a given part of a given version at a given time, it comes to your screen." [LM 2/15]

This guarantees that the *effects* of operations are recoverable, not that each operation has its own permanent address. The system knows the pieces and can reconstruct any moment — but it reconstructs *document states*, not *operation histories*.

## Time Is Metadata, Not Address

Nelson explicitly excludes time from the tumbler:

> "Note that 'time' is not included in the tumbler. Time is kept track of separately." [LM 4/18]

Time exists as metadata for filtering — "What links came in from last week?" — but operations are not indexed by time in the address space. There is no tumbler that means "the 47th edit to document D at 3:42 PM."

## What Tumbler-Space Contains

Only two kinds of entities are actually stored in tumbler-space:

> "In the present implementation (XU.87.1), the only entities actually stored in tumbler-space are content bytes and links." [LM 4/23]

Operations are not stored entities. They are actions that create or rearrange stored entities. Documents and accounts are "ghost elements" — conceptual positions without stored objects. Operations are not even ghost elements; they have no position on the tumbler line at all.

## Summary

| Question | Answer |
|----------|--------|
| Must every byte be uniquely identifiable? | **Yes** — permanent I-space address |
| Must every link be uniquely identifiable? | **Yes** — permanent tumbler in order of arrival |
| Must every document be uniquely identifiable? | **Yes** — permanent tumbler address |
| Must every version be uniquely identifiable? | **Yes** — tumbler indicates ancestry |
| Must every operation be uniquely identifiable? | **Not specified** |

Nelson designed a system where the *products* of intellectual work — content, connections, documents, versions — are permanent and addressable. The *acts* of creation and modification are recoverable through the append-only model and version history, but they are not themselves first-class citizens in the address space.

If an implementation needs operation identity (for audit trails, conflict resolution, replication), it would need to extend beyond what Literary Machines specifies — perhaps by recording operations as content within documents (which would then get permanent I-space addresses), or by maintaining an operation log as a separate mechanism. But Nelson does not require this.

NEED_RAW: [4/61-4/70] — The full FEBE protocol pages may contain additional detail about whether command invocations carry identifiers or sequence numbers. The curated sources quote selectively from these pages.

---

## Question 3 [nelson]

> Must the operation history itself be permanent and append-only, or may entries be revised or removed after recording?

### Nelson's Answer

# Must the Operation History Be Permanent and Append-Only?

## Short Answer

Nelson does not address the operation history as a separate artifact. But the architectural constraints make the answer effectively **yes** — the information that constitutes the history must be permanent, because the system's fundamental guarantees depend on it.

## What Nelson Actually Specifies

Nelson specifies an **append-only storage system** where changes accumulate and all previous states remain reconstructable:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

> "The true storage of text should be in a system that stores each change and fragment individually, assimilating each change as it arrives, but keeping the former changes; integrating them all by means of an indexing method that allows any previous instant to be reconstructed." [LM 2/15]

The historical backtrack guarantee is explicit:

> "The file management system we are talking about automatically keeps track of the changes and the pieces, so that when you ask for a given part of a given version at a given time, it comes to your screen." [LM 2/15]

Even deleted content is preserved for this purpose:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

> "DELETED LINKS (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

## The Key Distinction: Content vs. Log

Nelson never discusses an "operation log" as a separate entity. In his architecture, history is **structural**, not journaled:

- **I-space is append-only** — content bytes, once written, never change or disappear
- **V-space arrangements are per-version** — each version defines its own mapping over I-space content
- **Versions are permanent** — "There is thus no 'basic' version of a document set apart from other versions" [LM 2/19]

The operation history is not a separate log that sits alongside the data. It **is** the data. The sequence of I-space content plus the succession of V-space arrangements together constitute the complete history. There is no separate record to revise or remove.

## Why Revision of History Would Violate the Architecture

If you could revise or remove entries from the history (however represented), you would break three explicit guarantees:

**1. Historical backtrack:**
> "The user of such a system may scroll through an individual document, at successive instants of time, alive in the space-time vortex." [LM 2/15]

Removing any intermediate state makes this impossible.

**2. I-space immutability:**
Content at an I-space address never changes. Since I-space is append-only, removing an entry would mean removing content from I-space — a direct violation.

**3. Version reconstructability:**
The guarantee that "when you ask for a given part of a given version at a given time, it comes to your screen" [LM 2/15] requires that every version's V-space mapping and all referenced I-space content remain intact.

## The Historical Trace Enfilade

Nelson mentions a specific data structure designed for this purpose:

> "we redesigned Barus's linking enfilade system, designed the historical trace enfilade, and formulated the general theory of enfilades" [LM 1/36]

The historical trace enfilade is named but not fully described in the curated sources. Its existence as a dedicated data structure confirms that history tracking is a first-class architectural concern, not an afterthought.

NEED_RAW: [1/33-1/38] — The enfilade section may contain more detail about the historical trace enfilade's properties and guarantees.

## What Nelson Leaves Open

Nelson does not address:

- **Compaction** — Could an implementation compact the representation of history (e.g., merging redundant intermediate states) while preserving the ability to reconstruct any previous state? Nothing forbids this, as long as reconstructability is maintained.
- **Storage optimization** — Could entries be re-encoded, deduplicated, or compressed? The append-only principle applies to the logical content, not necessarily the physical representation.
- **Granularity** — Must every keystroke be preserved, or only version boundaries? Nelson says "successive versions" and "a given version at a given time" — suggesting version-level granularity, not keystroke-level.

## My Design Intent

The operation history must be permanent in the sense that **no previous state may become unrecoverable**. Whether this is implemented as a literal append-only log, or as the structural consequence of immutable I-space and permanent version mappings, is an implementation choice. But the information must never be revised or removed, because the system's identity depends on it.

The whole point of Xanadu's storage model is to reject "destructive replacement":

> "Virtually all of computerdom is built around the destructive replacement of successive whole copies of each current version." [LM 2/14]

Allowing the history itself to be destructively modified would reintroduce the very problem the entire system was designed to solve. It would be self-defeating — like building a permanent archive with an eraser.

---

## Question 4 [nelson]

> What must the system guarantee about attributing each operation to the user who performed it, and must that attribution be tamper-proof?

### Nelson's Answer

# Attribution of Operations to Users

## What the System Guarantees: Structural Attribution Through Ownership

Xanadu guarantees that every piece of content and every link is permanently attributed to the account that created it. This attribution is **structural**—encoded in the address itself—not metadata that can be stripped or falsified within the system.

The tumbler address encodes four fields:

```
Node.0.User.0.Document.0.Element
```

The **User field** permanently identifies who owns the content. Every byte you create lives under your account address forever.

> "There are four major fields, each expandable indefinitely, with three major dividers between them. These fields are Server, User, Document and Contents." [LM 4/26]

> "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

For links specifically:

> "A Xanadu link is a connective unit, a package of connecting or marking information. It is owned by a user." [LM 4/41]

> "A link need not point anywhere in its home document. Its home document indicates who owns it, and not what it points to." [LM 4/12]

## Operations Are Attributed Through the Ownership Model

Only the owner may modify a document:

> "Every document has an owner, the person who created and stored it (or someone who arranged it to be created and stored, such as a publishing company)... Only the owner has a right to withdraw a document or change it." [LM 2/29]

This means every operation that changes state—INSERT, DELETE, REARRANGE, APPEND, MAKELINK—is implicitly attributed to the document's owner. If content appears at an address under your account, you put it there. If a link exists in your document, you created it. The address IS the attribution.

## Must Attribution Be Tamper-Proof? No.

Nelson is explicit: the system provides **no cryptographic verification or tamper detection**. Attribution relies on **contractual trust** in the Storage Vendor franchise, not on mathematical proof.

> "User acknowledges that all material on the network is stored by users under similar arrangements to User's own, without verification or assurance of truth, authenticity, accuracy, usefulness or other beneficial character of such materials." [LM 5/17]

> "Storage Vendor makes no guarantee as to the correctness or authenticity of any material received from other Users." [LM 5/18]

> "User acknowledges that due to possible unreliability of the software, unreliability and vulnerability of transmission systems, and myriad possibilities for intrusion and malicious mischief by unseen parties throughout the universe, all storage, and transmission of contents and links, and attempts to deliver such material, are at User's risk." [LM 5/18]

The system does NOT:
- Hash content for integrity
- Sign operations cryptographically
- Provide tamper detection at retrieval
- Verify that content at an address is what the original author wrote

## What Provides Trust Instead

Three mechanisms substitute for cryptographic verification:

1. **Contractual obligation of Storage Vendors**: Vendors are contractually bound to preserve content faithfully and "not to spy for any private persons, corporations or agencies of any government upon the private materials of any customers" [LM 5/14-5/15]. Violation is a breach of the franchise agreement.

2. **Structural traceability**: The I-address permanently encodes origin. You cannot reference content without going through the address system, which inherently identifies the home document and its owner.

3. **Legal liability**: "Responsibility for the accuracy of material on the network rests with those users furnishing and publishing it; that liability for the consequences of inaccurate material rests with those users who furnish or publish it and represent it to be correct and usable." [LM 5/17-5/18]

This is a pre-cryptographic architecture (1981-1987). The solution to trust is social and legal, not mathematical. If the Storage Vendor is honest, the attribution holds. If compromised, there is no technical backstop.

## The Privacy Constraint

Any audit trail for operations must also respect the privacy guarantee:

> "The network will not, may not monitor what is read or what is written in private documents." [LM 2/59]

This constrains what the system may record. Reading leaves no trace by design. Writing is attributed through address ownership, but there is no specified "operation log" or "audit trail" beyond the structural fact that content exists at an address owned by a particular account.

## Summary

| Aspect | What Nelson Specifies |
|--------|----------------------|
| **Content attribution** | Structural, via I-address (User field) — permanent and unseverable within the system |
| **Operation attribution** | Implicit through ownership — only owners modify their documents |
| **Link attribution** | Via home document address — link's home identifies its owner |
| **Tamper-proofing** | Explicitly NOT provided — trust is contractual, not cryptographic |
| **Verification** | None specified — no hashing, signing, or integrity checks |
| **Trust model** | Franchise contract with Storage Vendors |
| **Privacy constraint** | System must not monitor reading; writing attributed only through ownership structure |

The system guarantees you can always determine WHO owns content (structural attribution). It does NOT guarantee that the infrastructure faithfully preserved what the owner originally wrote (no tamper-proofing). The gap between these two is filled by contractual trust in the franchise, not by technical mechanisms.

---

## Question 5 [nelson]

> Must replaying the history of operations on a document produce exactly the same content and link structure as existed at the original moment, with no deviation?

### Nelson's Answer

# Replay vs. Reconstruction: Nelson's Model

Nelson does not frame historical recovery as "replaying operations." His architecture makes the question largely moot—but the underlying guarantee (exact recovery of any past state) is explicit and absolute.

## Nelson's Guarantee: Exact Reconstruction

The system stores content permanently and reconstructs any previous state on demand:

> "The file management system we are talking about automatically keeps track of the changes and the pieces, so that when you ask for a given part of a given version at a given time, it comes to your screen." — 2/15

> "The true storage of text should be in a system that stores each change and fragment individually, assimilating each change as it arrives, but keeping the former changes; integrating them all by means of an indexing method that allows any previous instant to be reconstructed." — 2/15

The word "reconstructed" is precise. The system does not re-execute a sequence of editing commands. It reads permanently stored fragments and assembles them according to the version's arrangement. The result is deterministic because it is a read operation, not a computation.

## Why Replay Is the Wrong Frame

Nelson's architecture separates **content** (I-space, permanent) from **arrangement** (V-space, per-version). Editing does not mutate stored data—it creates new I-space content and new V-space mappings:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." — 2/14

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." — 4/11

Because I-space content is immutable and V-space mappings are stored per-version, recovering a past state means reading the V-space mapping for that version and fetching the referenced I-space bytes. There is no sequence of operations to replay. The state IS the stored data.

This is also why deletion does not destroy:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" — 4/9

Deleted content persists in I-space. A previous version's V-space mapping still references it. Reconstruction reads the old mapping and finds the bytes exactly where they always were.

## Content: Exactly Preserved

Every byte ever created has a permanent I-space address that never changes:

> "New items may be continually inserted in tumbler-space while the other addresses remain valid. This means that any address of any document in an ever-growing network may be specified by a permanent tumbler address." — 4/19

Content at an I-space address is immutable. Reconstruction returns exactly those bytes—there is no possibility of deviation because there is no transformation involved.

## Links: Exactly Preserved

Links have permanent creation-order addresses:

> "The links designated by a tumbler address are in their permanent order of arrival. A document includes only the links of which it is the home document." — 4/31

Deleted links, like deleted bytes, remain in storage:

> "DELETED LINKS (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" — 4/9

A previous version's link structure is recoverable because the links themselves persist at their permanent addresses. The version's V-space mapping determines which links were active at that point.

## The Enfilade Invariant

Nelson describes the data structure requirement that makes this work:

> "All changes, once made, left the file remaining in canonical order, which was an internal mandate of the system." — 1/34

The "canonical order" invariant means the system is always in a consistent, queryable state. Every edit leaves the structure ready to reconstruct any version. This is not about replay producing canonical order—it is about the storage structure maintaining it at all times.

## What Nelson Actually Requires

The guarantee is **not** "replaying operations produces the same result." The guarantee is stronger:

1. **Any previous state is exactly recoverable** — "any previous instant" can be "reconstructed" [2/15]
2. **Recovery is by direct read, not by replay** — content and mappings are permanently stored
3. **No deviation is possible** — I-space content is immutable; V-space mappings are stored per-version
4. **Part-pounce works for any version** — you can request "a certain part of a certain version at a certain point in time" and get exactly that [2/15-2/16]

## Summary

Nelson's architecture makes exact historical recovery a **structural property**, not a computational achievement. The question "must replay produce the same result?" presupposes an operation-log model that Nelson explicitly rejected in favor of append-only storage with version mappings. In his model, there is nothing to replay—the past state is still there, waiting to be read. The answer to the spirit of the question is **yes, past states must be exactly recoverable with no deviation**, but the mechanism is reconstruction from permanent storage, not replay of operations.

---

## Question 6 [nelson]

> What must the system guarantee about the ordering of operations when multiple users edit shared content concurrently — must a single canonical sequence be established?

### Nelson's Answer

# Concurrent Operation Ordering

The short answer: Literary Machines does not require a single canonical sequence of operations across multiple users because **the architecture makes the problem largely moot**. The ownership model, append-only storage, and versioning-by-forking collectively prevent the scenarios that would demand global ordering.

---

## Ownership Prevents Concurrent Editing

The most important structural fact: **only the owner may modify a document.**

> "Every document has an owner, the person who created and stored it (or someone who arranged it to be created and stored, such as a publishing company). The rightful copyright holder, or someone who has bought the document rights... Only the owner has a right to withdraw a document or change it." [LM 2/29]

There is no scenario in my design where Alice and Bob simultaneously edit the same document. If Alice owns it, Bob cannot INSERT, DELETE, REARRANGE, or APPEND to it. Period. The concurrent-editing ordering problem simply does not arise for document content.

When Bob wants to modify Alice's work, he creates his own version:

> "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate--without damaging the originals. This is done by inclusion links." [LM 2/45]

Bob's version is a **new document under Bob's ownership**. Two owners editing two documents is not a concurrency conflict — it is independent creation.

---

## I-Space Is Append-Only

Content storage is inherently ordered because it is append-only:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

Every byte ever created gets a permanent I-space address. Content is never overwritten, never moved, never modified in place. New content is appended. This means I-space operations have a natural total order: the order in which bytes were appended.

The enfilade system was specifically designed to maintain internal consistency after every operation:

> "His new method would allow linkages to keep up with all changes. It was instantaneous and permanent and could grow indefinitely. All changes, once made, left the file remaining in canonical order, which was an internal mandate of the system." [LM 1/34]

"Canonical order" is an **internal mandate** — the data structure must be in a valid, consistent state after every operation. But this is a storage-level invariant, not a user-visible ordering guarantee across multiple actors.

---

## Links: The One Concurrent-Write Scenario

Links are the one area where multiple users DO write to shared state simultaneously. Any user can create links pointing to any published content. These links live at the creator's address, but they affect what other users discover when they query "what links to this document?"

The design handles this through the link search model:

> "A link satisfies a search request if one span of each endset satisfies a corresponding part of the request." [LM 4/58]

> "THE QUANTITY OF LINKS NOT SATISFYING A REQUEST DOES NOT IN PRINCIPLE IMPEDE SEARCH ON OTHERS." [LM 4/60]

Links are indexed by their endsets. The search model is declarative ("find all links matching these constraints"), not positional ("find the link at position N"). This means link creation by different users doesn't create ordering conflicts — each user's links live at their own addresses and are independently discoverable.

The link address structure reinforces this. Links within a document are numbered by **permanent order of arrival**:

> "The links designated by a tumbler address are in their permanent order of arrival. A document includes only the links of which it is the home document." [LM 4/31]

Each user's links are ordered within their own document. There is no need for global ordering across all users' link-creation events because link search is constraint-based, not position-based.

---

## The Network Model: Eventual Consistency, Not Global Ordering

For the distributed case (multiple servers), Nelson describes a model that sounds remarkably like eventual consistency:

> "A server's network model, from the null case on up, is at all times unified and operational; whatever information moves between servers is assimilated at once to its overall structure, leaving each server in canonical operating condition with a slightly improved map of what is elsewhere. The contents can slosh back and forth dynamically." [LM 4/72]

Each server is always in "canonical operating condition" — a locally consistent state. Information arriving from other servers is "assimilated" incrementally. The system does not require global synchronization; it requires that each node be valid after each incremental update.

> "It is a truism that 'computer networks are always broken.' Meaning that on the average some nodes are disconnected or not working." [LM 4/75]

A system designed to function with "always broken" networks cannot rely on global operation ordering. It must work with partial knowledge and asynchronous updates.

---

## What I Did NOT Specify

I did not specify:

1. **No locking protocol** — no mention of locks, mutexes, or concurrency control primitives
2. **No session model** — no OPEN/CLOSE, no read/write modes, no session lifecycle
3. **No conflict resolution** — no merge algorithms, no "last writer wins," no vector clocks
4. **No transaction semantics** — no commit/rollback, no isolation levels

The session-model design intent document confirms: "Nelson's protocol is stateless at the command level: you name a document by its tumbler address, issue a command, and the back end responds."

The one mention of concurrent users is about **search optimization**, not editing:

> "In later versions of the storage system, we expect the back end to combine the search models of different users to create a barrel-roll shared search model which repeatedly crosses the address space on behalf of all a server's users simultaneously." [LM 4/59]

This "barrel-roll" is about efficiently serving multiple concurrent readers/searchers, not about ordering concurrent writes.

---

## The Architectural Answer

The system does not need to establish a single canonical sequence of operations across users because:

| Concern | How the architecture handles it |
|---------|--------------------------------|
| Concurrent document edits | Impossible — single owner per document |
| User wants to modify others' work | Creates own version (new document, own address) |
| Concurrent link creation | Links live at creator's address; search is constraint-based, not position-based |
| Cross-server consistency | Each server maintains locally canonical state; updates assimilated incrementally |
| I-space ordering | Append-only; natural chronological order |
| V-space ordering | Per-document, per-owner; no shared mutable state |

The principle is: **fork, don't lock**. When you can't modify something, you create your own version. This turns potential conflicts into independent creations, each with its own owner and its own address.

NEED_RAW: [4/59, 4/30-4/31] — The barrel-roll concurrent search passage and the link ordering passage would benefit from direct verification against the page images, as these are the closest Nelson comes to addressing concurrency explicitly.

---

## Question 7 [nelson]

> Must the operation history preserve the relationship between editing operations and the specific version of a document they produced, so that every version is reachable by replay?

### Nelson's Answer

# Must Operation History Be Preserved for Version Replay?

## Short Answer

Nelson's specification requires that **every version be reconstructable**, but it does **not** mandate operation replay as the mechanism. The user guarantee is about results (any previous state is accessible), not about how reconstruction is achieved internally.

## What Nelson Requires: The User Guarantee

Nelson is explicit that every historical state must be reachable:

> "The file management system we are talking about automatically keeps track of the changes and the pieces, so that when you ask for a given part of a given version at a given time, it comes to your screen." [LM 2/15]

> "The user of such a system may scroll through an individual document, at successive instants of time, alive in the space-time vortex." [LM 2/15]

> "THE PART YOU WANT COMES WHEN YOU ASK FOR IT." [LM 2/16]

The guarantee is clear: the system must deliver any part of any version at any time. But Nelson separates the **what** (version accessibility) from the **how** (reconstruction mechanism).

## Operation Replay: Mentioned But Not Mandated

Nelson explicitly discusses operation replay as *one known approach*, then notes its limitations:

> "Being able to go back through changes, and perhaps restore an earlier state, is called the problem of historical backtrack. For simple, linear textual documents this can be done by storing lists of changes and undoing them; and indeed several commercial versioning and backtrack systems are now on the market. But it is rather more difficult to do this for hypertext." [LM 3/13]

This is significant. Nelson:
1. Names the approach ("storing lists of changes and undoing them")
2. Acknowledges it works for linear text
3. Flags it as insufficient for hypertext
4. Does **not** adopt it as Xanadu's mechanism

## What Nelson Actually Built: Structural, Not Procedural

Nelson's solution to version history is **structural**, through data structures and address-space design, not through operation logs:

**The historical trace enfilade:**
> "we redesigned Barus's linking enfilade system, designed the historical trace enfilade, and formulated the general theory of enfilades" [LM 1/36]

This is a dedicated data structure for historical navigation — not a replay log but a queryable structure that can reconstruct any state.

**The I-space/V-space separation** provides the alternative mechanism:
- I-space content is permanent and append-only [LM 2/14]
- Each version is a different V-space arrangement over the same I-space content
- Reconstruction means recovering the V→I mapping for a given version, not replaying operations

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

Content accumulates in I-space. Versions are different views (V-space arrangements) of that permanent content. You reconstruct a version by recovering its V-space mapping, not by replaying the edits that produced it.

## The CREATENEWVERSION Operation

The FEBE protocol treats versioning as an explicit act, not an implicit consequence of editing:

> "CREATENEWVERSION: This creates a new document with the contents of document <doc id>. It returns the id of the new document. The new document's id will indicate its ancestry." [LM 4/66]

Note what this does: it creates a **new document** whose ID **indicates ancestry**. This is structural provenance through the address system, not operation-log provenance.

## A Tension in the Text

There is a tension between Chapter 2's vision and Chapter 4's mechanism:

- **Chapter 2** describes continuous historical states: "successive instants of time, alive in the space-time vortex" [LM 2/15] — suggesting every editing state is recoverable
- **Chapter 4** provides only CREATENEWVERSION as an explicit versioning operation — suggesting versions are deliberate snapshots

The "deleted bytes" state from the technical diagram hints at incomplete implementation:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

The phrase "awaiting historical backtrack functions" suggests the fine-grained reconstruction mechanism was still under development in XU.87.1.

## Conclusion

| Aspect | Required? | Evidence |
|--------|-----------|----------|
| Every version reconstructable | **Yes** | "a given part of a given version at a given time" [2/15] |
| Operation replay as mechanism | **No** | Named as one approach, flagged as insufficient for hypertext [3/13] |
| Operation log preserved | **Not specified** | Nelson designed structural alternatives (historical trace enfilade, I/V-space) |
| Ancestry traceable from address | **Yes** | "The new document's id will indicate its ancestry" [4/66] |

Nelson guarantees the **destination** (any version, any time, any part) but leaves the **route** to the implementation. The I-space/V-space architecture, the historical trace enfilade, and append-only storage together provide a structural reconstruction path that does not depend on operation replay. The system must *keep track of the changes and the pieces* [LM 2/15], but whether those "changes" are stored as replayable operations or as structural mappings is an implementation decision.

NEED_RAW: [2/15-2/16, 4/9] — to verify whether Nelson's "space-time vortex" language implies continuous state capture or merely poetic description of explicit versioning, and to see the full deleted-bytes diagram context.

---

## Question 8 [nelson]

> What must the system guarantee about links that reference a historical state of content — must following such a link reconstruct the document as it appeared at that point in its history?

### Nelson's Answer

# Links to Historical Content: What Must the System Guarantee?

The short answer: **No.** The system does not guarantee that following a link reconstructs the full document as it appeared at a historical moment. What it guarantees is more precise — and more powerful.

## Links Point to Bytes, Not to Versions

Xanadu links do not reference "a historical state." They reference **spans of bytes in I-space** — permanent content addresses that never change:

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes." [LM 4/42]

Because I-space content is immutable — "Content at an I-space address never changes" — the bytes a link attaches to are always retrievable. The link doesn't say "go to version 3, position 47." It says "go to these bytes." Those bytes exist permanently.

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

## Historical Reconstruction Is a Separate Capability

The system *does* guarantee that any previous state can be reconstructed:

> "The file management system we are talking about automatically keeps track of the changes and the pieces, so that when you ask for a given part of a given version at a given time, it comes to your screen." [LM 2/15]

But this is a **version operation**, not a link operation. You can always ask the system to show you version N of document D. That's the historical backtrack guarantee. It's orthogonal to link following.

## The Front End Decides How to Follow

Nelson explicitly places the version-resolution decision in the **front end**, not the back end:

> "When a document is updated, a reader will ordinarily want to see the new version — but the reader may be following a link made to an older version. However, the user's front-end machine may easily be set up to follow the link to the same passage in the most recent version — if it's still there." [LM 2/43]

This is a policy choice, not a system invariant. The front end can:

1. **Show the old version** — reconstruct the historical state the link was made against
2. **Follow to the current version** — use correspondence to find the same content now
3. **Offer both** — let the user choose

## Refractive Following: A Link to One Version Is a Link to All

The most striking guarantee is **refractive following** — because links point to I-space bytes, and correspondence tracks which bytes appear in which versions, a link to any version implicitly reaches all versions:

> "Links may be refractively followed from a point or span in one version to corresponding places in any other version. Thus a link to one version of a Prismatic Document is a link to all versions." [LM 2/26]

This is computed via the `SHOWRELATIONOF2VERSIONS` operation:

> "This returns a list of ordered pairs of the spans of the two spec-sets that correspond." [LM 4/70]

The correspondence is **structural** — it derives from shared I-space origin, not from metadata. If two V-space positions in different versions map to the same I-address, they correspond. The system can always compute this.

## The Windowing Parallel

Nelson's treatment of transclusion windows establishes the same pattern of time-fixed vs. floating access:

> "A quotation — an inclusion window — may be fixed to another document in two ways: at a certain point in time, in which case revisions are seen by the user only when he or she asks, 'What has this passage become?' Or second, at a relatively fixed location in the document space, in which case updates are seen automatically." [LM 2/37]

This shows Nelson was explicitly aware of both modes — frozen historical reference and live current reference — and made them user/front-end choices rather than system-level mandates.

## Summary of Guarantees

| What the system guarantees | Source |
|---|---|
| The bytes a link points to are always retrievable | I-space permanence [LM 4/11] |
| Any previous version can be reconstructed on demand | Historical backtrack [LM 2/15] |
| Correspondence between versions is always computable | Shared I-space origin [LM 2/20, 4/70] |
| A link to one version can reach any other version | Refractive following [LM 2/26] |

| What the system does NOT guarantee | Why |
|---|---|
| Following a link reconstructs the full historical document | Front-end policy, not back-end invariant [LM 2/43] |
| Links "know" which version they were made against | Links point to I-space bytes, not version numbers |
| The historical context is shown by default | The front end chooses: old version, current version, or user's choice |

The design is deliberately more flexible than "reconstruct the historical state." The bytes are permanent. The versions are reconstructible. The correspondences are computable. But *how* to present this to the user — whether to show the frozen past or the living present — is a front-end design decision, not a system invariant.

---

## Question 9 [nelson]

> Must the operation log record not only changes to content but also changes to sharing permissions, link creation, and other non-content operations with equal fidelity?

### Nelson's Answer

# Must Non-Content Operations Be Logged with Equal Fidelity?

## Short Answer

For **links**: yes, explicitly. For **permissions and administrative operations**: Nelson barely specifies these, so the question mostly dissolves. The key insight is that in Nelson's architecture, almost everything that matters IS either content or links — and both receive equal historical treatment.

## Links Are Explicitly Equal to Content

The strongest evidence comes from the document structure diagram on page 4/9, which shows both content and links receiving identical treatment under deletion:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

> "DELETED LINKS (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

The phrasing is identical. Deleted links occupy the exact same conceptual state as deleted bytes — not destroyed, merely removed from the current V-space arrangement, awaiting historical backtrack, potentially surviving in other versions. This is not accidental parallelism; it reflects the design principle that links are stored entities in the same tumbler space as content bytes.

Furthermore, links receive permanent creation-order addresses:

> "The links designated by a tumbler address are in their permanent order of arrival. A document includes only the links of which it is the home document." [LM 4/31]

Link 2.1 is always the first link created; link 2.755 is always the 755th. Deleting link 2.5 does not renumber 2.6 through 2.N. This permanence of link addresses mirrors the permanence of content addresses in I-space.

## Most "Metadata" IS Links

A critical architectural insight: operations that look like "metadata changes" in other systems are **link operations** in Xanadu. Nelson's metalink types include:

- **Title** — a link from the title text to the whole document [LM 4/52]
- **Author** — a link from the author's name to the whole document [LM 4/52]
- **Supersession** — a link declaring one document replaces another [LM 4/52-4/53]

Since these are all ordinary links stored in the link subspace, they inherit the same historical backtrack guarantees. Changing a document's title means creating a new title link — the old one remains in I-space. Disputing authorship means creating a competing author link from your own address. The history of these changes is preserved by the same mechanism that preserves content history.

> "Note that the Author link can also be used from outside a document to claim that the author is really someone else." [LM 4/52, footnote]

This is not special metadata handling — it falls out of the universal link architecture.

## Sharing Permissions Barely Exist

Nelson's access model is strikingly minimal:

> "A document may be private or published. [...] A private document may be read and linked-to only by the owner and his or her associates. A published document is available to anyone." [LM 2/42]

Publication is described as a solemn, essentially irreversible act:

> "It is in the common interest that a thing once published stay published, as in the world of paper. Other readers and users will come to depend on its accessibility. Consequently its author may not withdraw it except by lengthy due process." [LM 2/43]

There is no concept of toggling permissions, granting per-user access, or changing sharing settings over time. Publication is a one-way transition. Private documents have "designees," but Nelson never specifies a mechanism for changing designees or tracking such changes historically.

Moreover, private documents were not even implemented in XU.87.1:

> "Private documents. (Currently all documents are visible to all users.)" [LM 4/79]

So the question "must permission changes be logged?" is almost moot — there are essentially no permission changes to log. The one state transition that exists (private → published) is meant to be permanent.

## Administrative Operations Are Separate

Nelson places accounting information outside the document model:

> "Each published document has a cash register. [...] It is in the user's system area, along with passwords and accounting information." [LM 5/13]

The "system area" is architecturally distinct from document content and links. Nelson does not specify historical backtrack for cash registers, passwords, or accounting data. These appear to be operational state, not part of the literary record.

## The Deeper Principle

Nelson's append-only storage model is described in sweeping terms:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

The word "changes" here is unqualified — it suggests all modifications to documents, not just content modifications. And since a document "consists of its contents (including history and alternatives) and its out-links" [LM 2/31], the document's full evolution — content AND links — constitutes the "ongoing braid" that historical backtrack preserves.

> "A document is really an evolving ONGOING BRAID." [LM 2/14]

## Summary

| Operation Type | Historical Fidelity Required? | Evidence |
|---|---|---|
| Content changes (bytes) | **Yes** — explicitly | Append-only storage, deleted bytes await backtrack [LM 4/9] |
| Link creation/deletion | **Yes** — explicitly equal | Deleted links get identical treatment to deleted bytes [LM 4/9]; permanent creation-order addresses [LM 4/31] |
| Metadata changes | **Yes** — because metadata IS links | Title, Author, Supersession are all link types [LM 4/52] |
| Permission changes | **Nearly moot** | Access is binary; publication is irreversible; private docs unimplemented in XU.87.1 [LM 4/79] |
| Administrative state | **Not specified** | Cash registers, passwords in separate "system area" [LM 5/13]; no historical backtrack mentioned |

The answer to your question is: **yes, link operations must be recorded with equal fidelity to content operations** — this is explicitly stated. But the question of "sharing permissions and other non-content operations" largely dissolves because (a) most metadata IS links, (b) permissions barely exist as a concept, and (c) administrative state is architecturally separate from the literary record.

---

## Question 10 [nelson]

> What must the system guarantee if an operation depends on content originating in another document — must the log capture that cross-document provenance so replay remains faithful even across document boundaries?

### Nelson's Answer

# Cross-Document Provenance in Operations

## The Short Answer

Yes — but Nelson's architecture doesn't solve this with a log. It solves it **structurally through I-space addresses**. Cross-document provenance is not something the system must *record*; it is something the system cannot *lose*, because the addressing scheme encodes it permanently.

## The Structural Guarantee

Every byte in Xanadu has a permanent I-space address with the form:

```
Node.0.User.0.Document.0.Element
```

The **Document field** directly encodes which document originally created that byte. This is not metadata attached to content — it IS the content's identity.

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

> "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

When any operation references content from another document, the I-addresses of that content carry their origin permanently. The operation doesn't need to "note" the provenance — the addresses themselves are the provenance.

## How Cross-Document Operations Work

### COPY (Transclusion)

The COPY operation is the primary cross-document operation:

> "The material determined by <spec set> is copied to the document determined by <doc id> at the address determined by <doc vsa>." [LM 4/67]

This creates a **V-space mapping** in the target document that points to **existing I-space content** in the source document. The source's I-addresses are preserved — that's the whole point. The bytes are not duplicated; they are referenced.

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

For replay: the COPY command includes a `<spec set>` — tumbler spans identifying the source content. Those tumbler spans encode exactly which document, which version, which byte range. Replaying the COPY with the same spec-set reproduces the same V-to-I mapping, preserving the same cross-document provenance.

### CREATENEWVERSION

> "This creates a new document with the contents of document <doc id>. It returns the id of the new document. The new document's id will indicate its ancestry." [LM 4/66]

The new version's V-space maps to the same I-space content as the source. Every byte in the new version still traces back to its original home document. The version ID itself "will indicate its ancestry" — the tumbler address of the new document encodes its derivation.

### INSERT

INSERT creates **new** I-space content — bytes that originate in the document being edited. No cross-document provenance arises because the content is native.

### DELETE

DELETE removes content from V-space only:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

I-space is unchanged. Cross-document provenance of deleted content survives because the I-addresses persist.

## What Depends on Cross-Document Provenance

Several guarantees would fail if cross-document provenance were lost during replay:

### 1. Correspondence (Version Comparison)

> "A facility that holds multiple versions of the same material, and allows historical backtrack, is not terribly useful unless it can help you intercompare them in detail — unless it can show you, word for word, what parts of two versions are the same." [LM 2/20]

SHOWRELATIONOF2VERSIONS works by examining shared I-space origins:

> "This returns a list of ordered pairs of the spans of the two spec-sets that correspond." [LM 4/70]

If replay lost the cross-document I-addresses, the system could no longer determine which parts of two documents share common ancestry. Correspondence would be destroyed.

### 2. Attribution

> "This world nevertheless remains simple in design. The virtuality is simple in structure and repeats in layers. You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

Attribution is structural — it depends on I-addresses encoding origin. If a COPY operation were replayed in a way that assigned new I-addresses to the transcluded content (treating it as INSERT rather than COPY), attribution to the original author would be severed.

### 3. Royalties

> "In our planned service, there is a royalty on every byte transmitted. This is paid automatically by the user to the owner every time a fragment is summoned." [LM 2/43]

> "If a modified document is read, the original owner and the modifier split the royalty in proportion to who wrote what, as determined automatically." [LM 2/45]

The system determines "who wrote what" by examining I-addresses. If transclusion provenance were lost, the system couldn't determine that bytes originated in someone else's document, and royalty splitting would fail.

### 4. FINDDOCSCONTAINING

> "This returns a list of all documents containing any portion of the material included by <vspec set>." [LM 4/70]

This operation searches by I-space identity. It finds every document whose V-space maps to the specified I-space content. If cross-document provenance were lost (content re-created with new I-addresses), this operation would fail to find the connection.

### 5. Link Refractive Following

> "Links may be refractively followed from a point or span in one version to corresponding places in any other version. Thus a link to one version of a Prismatic Document is a link to all versions." [LM 2/26]

This depends on shared I-space content across versions. If a version operation lost the I-space identity of transcluded content, links could no longer "refract" across version boundaries.

## The Architecture's Answer

Nelson's architecture makes this question almost moot by design:

1. **I-space is append-only** — content is never overwritten or reassigned
2. **I-addresses encode origin** — the Document field IS the provenance
3. **COPY preserves identity** — transclusion shares addresses, doesn't create new ones
4. **V-space is the only thing that changes** — edits rearrange mappings, not content

For any operation log or replay mechanism, the requirement follows naturally: **the log must distinguish between operations that create new I-space content (INSERT, APPEND) and operations that create V-space mappings to existing I-space content (COPY, CREATENEWVERSION).** Conflating these would destroy the I-space identity that is the foundation of attribution, correspondence, royalties, and link survivability.

Nelson does not discuss operation logging or replay explicitly — these are implementation concerns beneath the FEBE protocol level. But the guarantees he specifies (permanent attribution, automatic royalty splitting, version correspondence, content discovery) constitute a **conservation law on I-space identity** that any replay mechanism must respect. If replay produces different I-addresses for content that was originally transcluded, every guarantee that depends on shared I-space origin breaks.

## Summary

The system must preserve cross-document provenance not because Nelson says "log it" — he doesn't discuss logs — but because every major guarantee depends on it. The I-space address IS the provenance. Any faithful replay must preserve the distinction between "new content created here" (INSERT → new I-address) and "content referenced from there" (COPY → existing I-address). Losing that distinction severs attribution, breaks correspondence, disrupts royalties, and defeats link refractive following.

---

## Question 11 [gregory]

> Can the monotonic I-address ordering within the granfilade reconstruct a total temporal ordering of content creation events across documents, or do per-document allocation ranges (via `findisatoinsertmolecule`) only guarantee ordering within a single document's I-address subrange?

### Gregory's Answer

## KB Synthesis

## Monotonic I-Address Ordering: Per-Document Only

The monotonic ordering only guarantees temporal ordering **within a single document's I-address subrange**. It cannot reconstruct a total temporal ordering across documents.

### Why the Ordering Is Per-Document

The critical mechanism is in `findisatoinsertmolecule` [SS-ADDRESS-SPACE, Finding 0065]:

> `upperbound` is set to `docISA.2.3` (bounding search to the document's link subspace). `findpreviousisagr` finds the highest existing I-address **below that bound**.

Each INSERT/MAKELINK operation bounds its search to a document-specific tumbler prefix range. The allocation is `next_content_addr(granf, doc) = max_content(granf, doc) + 1` — the maximum is computed only within the document's own subrange [SS-ADDRESS-SPACE, Finding 0077].

The address layout makes this concrete [SS-ADDRESS-SPACE, Finding 0077]:

```
1.1.0.1.0.1.3.0.1.1   ← text insert #1 in document d1
1.1.0.1.0.1.3.0.1.2   ← text insert #2 in document d1
1.1.0.1.0.2.3.0.1.1   ← text insert #1 in document d2 (entirely separate range)
```

[INV-MONOTONIC, Finding 0065] states explicitly: "This holds independently per document — interleaving MAKELINK calls across documents does not break monotonicity within any single document." The per-document isolation is the design.

### What Cross-Document Comparison Yields

Comparing `1.1.0.1.0.1.3.0.1.5` (5th insert in d1) against `1.1.0.1.0.2.3.0.1.1` (1st insert in d2) via `tumblercmp` yields a lexicographic result [INV-TUMBLER-TOTAL-ORDER]: it tells you the document d1 (`...0.1...`) precedes d2 (`...0.2...`) in the address hierarchy, which reflects *document creation order*, not *content insertion time*.

### No Shared Global Counter

[SS-ADDRESS-SPACE, Finding 0077] explicitly rejects a global counter model:

> "There is no single global 'next' counter (no Σ.next). Allocation is stateless query-and-increment on different tumbler ranges."

[SS-ADDRESS-SPACE, Finding 0061] confirms the mechanism:

> "Each INSERT queries the granfilade tree via `findpreviousisagr` to find the highest existing I-address **below an upper bound**, then increments by 1."

The upper bound is always document-scoped.

### One Cross-Document Interaction: CREATELINK

There is one subtle cross-effect [INT-LINK-INSERT, Finding 0063]: CREATELINK allocates a link orgl in the granfilade, which advances the maximum I-address in that region. This *can* introduce a gap in the text I-address sequence for the **same document** (breaking text-only contiguity). But it still operates within that document's I-address bounds — it does not interleave with another document's allocation range.

### Summary

| Scope | Ordering Guarantee |
|-------|-------------------|
| Within one document's I-address subrange | Strictly monotonic = insertion chronology |
| Across two documents' subranges | Lexicographic tumbler order = document creation order, not content insertion time |
| Global temporal total order | **Not reconstructable** from I-addresses alone |

The physical granfilade tree is a single flat structure [SS-UNIFIED-STORAGE], but the logical allocation is partitioned by document prefix. The monotonic invariant [INV-MONOTONIC] is a family of independent per-document sequences, not a single global sequence.

## Code Exploration

Now I have enough to give a complete, code-grounded answer.

---

## Answer: I-Address Ordering Cannot Reconstruct a Total Temporal Ordering Across Documents

**Short answer:** The monotonic I-address ordering within the granfilade guarantees only *per-document* insertion ordering and *per-account* document-creation ordering. It cannot reconstruct a total temporal ordering of content creation events across documents or accounts. Here is the precise structural reason.

---

## The Tumbler Address Hierarchy

The address space is hierarchically encoded via zero-separated mantissa digits [common.h:53,67]:

```
NPLACES = 16 mantissa slots
NODE      → 1 story:  [n]
ACCOUNT   → 3 stories: [n, 0, a]         = n.0.a
DOCUMENT  → 5 stories: [n, 0, a, 0, d]   = n.0.a.0.d
TEXTATOM  → 7 stories: [n, 0, a, 0, d, 0, t]
LINKATOM  → 7 stories: [n, 0, a, 0, d, 0, l]
```

The zero slots are level separators visible in the bug-fix comment at granf2.c:219:
```
/* 1.1.0.1 is the account */
/* 1.1.0.1.0.1 should be the first document address */
```

---

## How Atom I-Addresses Are Allocated: `findisatoinsertmolecule`

When `doinsert` is called [do1.c:117-123]:
```c
makehint(DOCUMENT, ATOM, TEXTATOM, docisaptr, &hint);
ret = inserttextingranf(taskptr, granf, &hint, textset, &ispanset) ...
```

`makehint` [do2.c:78-84] simply copies `docisaptr` into `hint.hintisa`. The hint's `hintisa` is the *document's own I-address*, not the account or any global reference.

This flows to `findisatoinsertgr` [granf2.c:130-156], which for `subtype == ATOM` calls:

```c
findisatoinsertmolecule (fullcrumptr, hintptr, isaptr);  // granf2.c:142
```

Inside `findisatoinsertmolecule` [granf2.c:158-181]:
```c
tumblerincrement (&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound);
// For TEXTATOM (atomtype=1): upperbound = docisa.0.2
// For LINKATOM (atomtype=2): upperbound = docisa.0.3

clear (&lowerbound, sizeof(lowerbound));
findpreviousisagr ((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);
```

The critical point: `upperbound` is computed *relative to the document's own address* (docisa + two right-shifted stories + atomtype+1). `findpreviousisagr` [granf2.c:255-278] then searches the granfilade's tree for the largest existing I-address strictly less than `upperbound`. Since `upperbound` is just above the current document's atom subrange, **the search is structurally confined to that document's address subspace**. The result is the largest I-address currently allocated within this document.

New atom address = `lowerbound + increment` (per branch logic at granf2.c:165-175). This is always strictly greater than the previous maximum within the document.

**Within a single document**: higher I-address ↔ later insertion. True.

**Across two different documents**: `doc1`'s upper bound (e.g. `1.0.1.0.1.0.2`) and `doc2`'s upper bound (e.g. `1.0.1.0.2.0.2`) are different bounds. Each call to `findpreviousisagr` only finds the maximum *within that document's subrange*. The two documents' atom I-address allocations are **completely independent** — there is no shared counter or coordinating global state.

---

## How Document I-Addresses Are Allocated: `findisatoinsertnonmolecule`

When `docreatenewdocument` is called [do1.c:239-241]:
```c
makehint (ACCOUNT, DOCUMENT, 0, &taskptr->account, &hint);
return (createorglingranf (taskptr, granf, &hint, isaptr));
```

This takes the ACCOUNT→DOCUMENT (non-molecule) path in `findisatoinsertgr` [granf2.c:143-152], calling `findisatoinsertnonmolecule` [granf2.c:203-242]:

```c
depth = hintptr->supertype == hintptr->subtype ? 1 : 2;
// For ACCOUNT→DOCUMENT: depth = 2
tumblerincrement (&hintptr->hintisa, depth - 1, 1, &upperbound);
// upperbound = accountisa + delta(1, 1) = the *next* sibling account address
findpreviousisagr ((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);
```

`upperbound` is the next account's address. `findpreviousisagr` finds the most recently created document under *this* account (the largest document I-address below `upperbound`). The new document gets `truncated(lowerbound, hintlength + depth) + increment`.

**Within a single account**: higher document I-address ↔ later document creation. True.

But this says nothing about *when content was written into each document*. Doc2 was created after Doc1 (doc2 > doc1 in I-address), but the 5th atom in Doc1 may have been inserted an hour after the 3rd atom in Doc2.

---

## Why Cross-Document Temporal Ordering Is Lost

### Reason 1: Disjoint per-document subranges, independently allocated

`findisatoinsertmolecule` scopes every atom allocation to its document's subrange [granf2.c:162-164]. Two documents' atom I-addresses are in non-overlapping regions of I-space:
- Doc1 atoms: `n.0.a.0.1.0.*`
- Doc2 atoms: `n.0.a.0.2.0.*`

I-space ordering says doc2 atoms > doc1 atoms numerically, but this is an artifact of document creation order, not content insertion order.

### Reason 2: No global counter or clock

There is no global sequence number or timestamp anywhere in the allocation path. `findpreviousisagr` is a purely structural operation: it traverses the enfilade tree to find the current maximum within a bounded subrange [granf2.c:263-278]. No state is updated globally when an atom is inserted into any document.

```c
int findpreviousisagr(typecorecrum *crumptr, typeisa *upperbound, typeisa *offset)
{ RECURSIVE
  ...
    for (ptr = findleftson((typecuc*)crumptr); ptr; ptr = findrightbro(ptr)) {
        if (...whereoncrum(ptr, ...) == THRUME || ...) {
            findpreviousisagr (ptr, upperbound, offset);  // recurse into subtree
            return(0);
        } else {
            tumbleradd(offset, &ptr->cwid.dsas[WIDTH], offset);  // accumulate width
        }
    }
}
```

This is width-accumulation in the enfilade tree — purely spatial, no temporal state.

### Reason 3: Different accounts are fully independent

`docreatenewdocument` uses `taskptr->account` as its hint [do1.c:239]. Different users (different account tumblers, stored in `player[user].account` [players.h:20]) allocate documents under completely separate account subranges. Cross-account I-address ordering has no temporal significance whatsoever.

### Reason 4: The granfilade is a spatial index, not a temporal log

`inserttextgr` [granf2.c:83-109] calls `insertseq` to place content into the enfilade tree *at its I-address*. The granfilade is indexed by I-address (WIDTH dimension [granf2.c:34]); its structure reflects spatial address ordering. There is no insertion-time journal.

---

## What the Ordering *Does* Guarantee

| Scope | Guarantee |
|---|---|
| Within one document | Higher I-address = later `doinsert` call for that document |
| Documents within one account | Higher document I-address = later `docreatenewdocument` call for that account |
| Atoms across documents (same account) | **No temporal guarantee** |
| Anything across accounts | **No temporal guarantee** |

---

## Conclusion

**Per-document allocation ranges (via `findisatoinsertmolecule`) only guarantee ordering within a single document's I-address subrange.** The `upperbound` computation at granf2.c:162 (`tumblerincrement(&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound)`) confines every atom allocation to its document-local address space. `findpreviousisagr` is scoped to that space; there is no cross-document maximum tracked. Combined with the absence of any global counter or timestamp in the allocation path, the granfilade's monotonic I-address ordering cannot reconstruct a total temporal ordering of content creation events across documents.

---

## Question 12 [gregory]

> Since the spanfilade is write-only and DOCISPAN entries persist after DELETE removes V→I mappings from the POOM, do the accumulated DOCISPAN entries contain enough information (document ID, I-address span) to distinguish an INSERT from a COPY — or do both operations produce structurally identical spanfilade entries pointing to the same I-addresses?

### Gregory's Answer

## KB Synthesis

## Answer: DOCISPAN Entries Are Structurally Identical for INSERT and COPY

Both operations produce the same DOCISPAN entry structure: `(I-address range → document ISA)`. The spanfilade records **what** content a document references, not **how** it got there.

### What the DOCISPAN Entry Contains

From [SS-DOCISPAN] Finding 0047: `insertspanf` receives an `ispanset` (a linked list of `typeispan` structs, each with `stream` start address and `width`) and a `docisaptr`. It makes one `insertnd` call per `typeispan`. The entry records:

- **Which document** holds the content (`docisaptr`)
- **Which I-address range** it holds (`stream`, `width`)

No operation-type flag, no creation-method marker, no provenance chain.

### How Both Operations Call `insertspanf`

**INSERT path** ([ST-INSERT] Finding 0036):
`doinsert` → `inserttextingranf` (allocates **fresh** I-addresses) → `docopy` → `insertpm` + `insertspanf(taskptr, spanf, docisaptr, ispanset, DOCISPAN)`

**COPY path** ([ST-COPY] Finding 0047):
`docopy` with **pre-existing** I-addresses from source → `insertpm` + `insertspanf(taskptr, spanf, docisaptr, ispanset, DOCISPAN)`

Same call signature. Same entry structure.

### The Indirect Signal: I-Address Multiplicity

Although entries are structurally identical, the **I-addresses themselves** encode the distinction indirectly:

- **INSERT** allocates fresh I-addresses ([INV-MONOTONIC], [INV-NO-IADDR-REUSE]). These addresses appear in DOCISPAN for exactly one document initially — the target. No prior document has a DOCISPAN entry for them.

- **COPY** reuses existing I-addresses ([INV-IADDR-PROVENANCE] Finding 0046). The same I-range appears in DOCISPAN for **both** the source document and the target document. `find_documents()` returns multiple results for a COPY'd range precisely because of this duplication.

The provenance information — which document *natively owns* an I-address — is stored in POOM crums via the `homedoc` field ([INV-IADDR-PROVENANCE] Finding 0046), not in the spanfilade. The spanfilade records current referencing relationships; POOM crums record creation history.

### Complication: Stale Entries Blur the Signal

[INV-SPANF-WRITE-ONLY] ([ST-DELETE] Finding 0057) and [INT-DELETE-SPANF-DIVERGENCE]: DELETE never removes DOCISPAN entries. After a source document deletes its content, its DOCISPAN entries persist. A later observer sees DOCISPAN entries for those I-addresses in *both* source and target documents — identical to the post-COPY state — even if the source deleted first and the target did a later INSERT into the same address range (impossible given [INV-NO-IADDR-REUSE], but the stale entries remain confusing).

### Conclusion

The spanfilade alone **cannot reliably distinguish INSERT from COPY** at the entry level. Full disambiguation requires:

1. **Cross-document correlation**: If an I-range appears in multiple documents' DOCISPAN entries, it was COPY'd (or the source is stale after delete — [EC-STALE-SPANF-REFERENCE]).
2. **POOM `homedoc` inspection**: The `homedoc` field in POOM crums ([INV-IADDR-PROVENANCE]) records which document originally allocated each I-address. This is the authoritative provenance record — it distinguishes native content (INSERT) from referenced content (COPY) regardless of DOCISPAN multiplicity.

The design reflects the system's content-identity model: the spanfilade is an index of *where content can be found*, not *how it was created*. The creation history lives in the granfilade's I-address allocation structure and the POOM's `homedoc` fields.

## Code Exploration

---

## Answer: INSERT vs COPY in the Spanfilade

### The DOCISPAN Crum Format

The spanfilade's bottom-crum payload is defined in `wisp.h:107-109`:

```c
typedef struct struct2dbottomcruminfo {
    tumbler homedoc;
} type2dbottomcruminfo;
```

One field. That's it. Every DOCISPAN entry in the spanfilade records exactly:
- **ORGL axis position**: `prefixtumbler(docisa, DOCISPAN=4)` — the document ISA with span-type prefix 4 [`spanf1.c:22`]
- **SPAN axis position**: the I-address span (`lstream`, `lwidth`) [`spanf1.c:49-50`]
- **Payload**: `homedoc` = the target document ISA [`spanf1.c:29`]

There is no operation-type field, no source-document field, no timestamp.

---

### What INSERT Writes

`doinsert` [`do1.c:87-123`]:

```c
ret = (inserttextingranf(taskptr, granf, &hint, textset, &ispanset)
    && docopy(taskptr, docisaptr, vsaptr, ispanset)
    );
```

1. `inserttextingranf` → `inserttextgr` [`granf2.c:83-109`] allocates **fresh I-addresses** in the permascroll. The resulting `ispanset` contains I-addresses that have never existed in any document's DOCISPAN before.
2. `docopy` is called with this new `ispanset`.
3. Inside `docopy` [`do1.c:60-62`]:
   ```c
   && insertpm(taskptr, docisaptr, docorgl, vsaptr, ispanset)
   && insertspanf(taskptr, spanf, docisaptr, ispanset, DOCISPAN)
   ```
   → Creates crum: **ORGL=(docISA.4), SPAN=(new_I_addr), homedoc=docISA**

---

### What COPY Writes

`docopy` [`do1.c:45-65`]:

```c
return (
   specset2ispanset(taskptr, specset, &ispanset, NOBERTREQUIRED)
&& findorgl(taskptr, granf, docisaptr, &docorgl, WRITEBERT)
&& acceptablevsa(vsaptr, docorgl)
&& insertpm(taskptr, docisaptr, docorgl, vsaptr, ispanset)
&&  insertspanf(taskptr, spanf, docisaptr, ispanset, DOCISPAN)
```

1. `specset2ispanset` converts the source's V-addresses to **existing I-addresses** — the same I-addresses allocated when the source content was originally INSERTed.
2. `insertspanf` with `DOCISPAN` creates: **ORGL=(docISA.4), SPAN=(existing_I_addr), homedoc=docISA**

---

### Are They Structurally Distinguishable?

**No. They are structurally identical.**

The `insertspanf` function at [`spanf1.c:15-54`] writes the same structure for both:

```c
prefixtumbler(isaptr, spantype, &crumorigin.dsas[ORGLRANGE]);  // doc.DOCISPAN
tumblerclear(&crumwidth.dsas[ORGLRANGE]);                       // width=0 (point)
// for ISPANID items:
movetumbler(&((typeispan *)sporglset)->stream, &lstream);       // I-address
movetumbler(&((typeispan *)sporglset)->width, &lwidth);         // I-width
movetumbler(isaptr, &linfo.homedoc);                            // homedoc = doc
// insert crum at (ORGL=doc.4, SPAN=I-address), payload=homedoc
insertnd(taskptr, (typecuc*)spanfptr, &crumorigin, &crumwidth, &linfo, SPANRANGE);
```

Both INSERT and COPY feed an `ispanset` of `ISPANID` items into this same function with the same `isaptr`. The only structural difference is which I-addresses are in `ispanset` — a distinction that is not encoded in the crum itself.

The `isanextensionnd` function [`insertnd.c:301-309`] that decides whether to merge adjacent crums checks only `homedoc` equality:

```c
if (!tumblereq(&infoptr->homedoc, &((type2dcbc *)ptr)->c2dinfo.homedoc))
    return (FALSE);
```

Since both INSERT and COPY set `homedoc = target document ISA`, contiguous I-address ranges from either operation can be silently merged into a single crum, further erasing provenance.

---

### The Indirect Signal

The accumulated DOCISPAN entries **do** carry an indirect signal, just not inside any individual entry:

- If I-address `X` appears in DOCISPAN for **only one document** → it was INSERTed there (or COPYed from a source whose DOCISPAN entry for `X` would still persist — but would also be visible).
- If I-address `X` appears in DOCISPAN for **multiple documents** → a COPY must have occurred at some point involving `X`.

But even this external cross-reference only tells you that content was *shared*, not which document was the INSERT origin and which was the COPY destination. The `finddocscontainingsp` function [`spanf1.c:151-188`] queries exactly this cross-document index — it walks the SPAN axis to find all ORGL (document) hits for a given I-address — but returns an unordered set. Directionality is not recoverable.

---

### Why: Architectural Intent

This is not an omission — it is the design. The DOCISPAN index answers: *"Which documents currently contain this I-address?"* The `finddocscontainingsp` function uses it for exactly that query. The history of *how* each document came to contain that I-address (INSERT vs COPY, which was source, which was destination) is not part of the data model. That semantic lives only in the user's knowledge and in the temporal order of operations, neither of which the spanfilade records.

Transclusion's core semantics — shared I-addresses encoding *common origin* — depends precisely on INSERT and COPY being indistinguishable at the storage level. The DOCISPAN entries asserting (docA, I-addr) and (docB, I-addr) make no claim about priority or direction; they only assert co-reference.

---

### Summary

| | INSERT | COPY |
|---|---|---|
| I-addresses in crum | Freshly allocated (new to permascroll) | Existing (already in source doc's DOCISPAN) |
| Crum structure | `(docISA.4, I-addr, homedoc=docISA)` | `(docISA.4, I-addr, homedoc=docISA)` |
| Structurally identical? | **Yes** | **Yes** |
| Distinguishable from entry alone? | **No** | **No** |
| Distinguishable by cross-referencing? | Partially (COPY ↔ shared I-address appears in ≥2 docs) | Partially |
| Direction of copy recoverable? | **No** | **No** |

Both operations produce structurally identical DOCISPAN crums. The spanfilade accumulates entries from both without distinction. An individual entry encodes only `(document, I-address-span)`; the crum payload `homedoc` is the same as the document in the ORGL axis, providing no additional provenance. The write-only, append-only nature of the spanfilade means deleted content's DOCISPAN entries persist indefinitely, making even the cross-reference signal noisy for determining which document was the original INSERT site.

---

## Question 13 [gregory]

> After DELETE mutates a POOM and the pre-delete V→I mapping is lost, is there any path — using the granfilade's permanent content, the spanfilade's DOCISPAN history, and CREATENEWVERSION snapshots — to reconstruct what V-address a given I-address occupied before the deletion, or is the V-position information irrecoverably destroyed?

### Gregory's Answer

## KB Synthesis

## V-Position Recovery After DELETE: A Synthesis

The answer is: **V-position information is irrecoverably destroyed unless a snapshot was taken before the deletion.** Let me trace through each recovery candidate.

---

### What DELETE Destroys

[ST-DELETE/Finding 0072] makes the core claim explicit:

> "The pre-mutation POOM tree `T` cannot be reconstructed from the post-mutation tree `T'`."

[ST-DELETE/Finding 0064] confirms the mechanism: `deletend` calls `disown` + `subtreefree`, which recursively frees the bottom crums that held the V→I mappings. The physical tree nodes are deallocated — no ghost remains.

---

### The Granfilade: Content Without Position

[FC-GRANF-ON-DELETE] confirms the granfilade is unchanged by DELETE — I-addresses and their content bytes survive permanently ([INV-IADDR-IMMUTABILITY], [INV-NO-IADDR-REUSE]).

But the granfilade stores **I-address → bytes**, not **V-address → I-address**. The V→I direction of the mapping is exclusively the POOM's responsibility. The granfilade can tell you *what* content an I-address holds, and via [INV-MONOTONIC] it can tell you approximately *when* it was allocated (relative order), but it has no record of *where* (V-position) the content was mapped.

---

### The Spanfilade/DOCISPAN: Membership Without Position

[INT-DELETE-SPANF-DIVERGENCE/Finding 0057] and [INV-SPANF-WRITE-ONLY] confirm that DELETE does not remove DOCISPAN entries. [EC-STALE-SPANF-REFERENCE] makes the consequence explicit: `FIND_DOCUMENTS(α)` still returns the document after DELETE, even though `∄ v : poom.D(v) = α`.

However, [SS-DOCISPAN/Finding 0047] specifies what DOCISPAN actually stores:

```
insertspanf(taskptr, spanf, docisaptr, ispanset, DOCISPAN)
```

The parameters are the **document ISA** and the **I-span set** — not the V-address. The DOCISPAN entry records `(I-span α₁..α₁₀) → document D`, asserting membership, with no V-position field. The call site [ST-INSERT/Finding 0036] confirms this: `docopy` calls `insertspanf` after `insertpm`, passing only the I-address ranges and document identifier.

So DOCISPAN answers "did this document ever contain this I-address?" but cannot answer "at what V-position?"

---

### CREATENEWVERSION: The Only Recovery Path

[ST-VERSION-CREATE/Finding 0072] states this directly:

> `recoverable(D, state_at_t) ⟺ ∃ V : CREATENEWVERSION(D) executed at time t, producing V`

When CREATENEWVERSION runs, [ST-VERSION-CREATE/Finding 0046] shows it copies the text subspace V→I mappings from the source document's POOM into a new, independent POOM tree. [FC-VERSION-ISOLATION] guarantees subsequent edits to the original do not affect the version's tree.

So a version created **before** the DELETE preserves the pre-delete POOM state. After the DELETE:

- `ispan2vspanset(version_poom, α)` → returns the V-address that α occupied at version-creation time
- `ispan2vspanset(current_poom, α)` → returns nothing (mapping freed)

Without a prior version, there is no equivalent query. The V-position is gone.

---

### Why This Is Structurally Unavoidable

The three-layer architecture [SS-THREE-LAYER-MODEL] makes the asymmetry structural:

| Layer | Mutability | Records |
|-------|-----------|---------|
| Granfilade | Append-only | I-address → bytes |
| Spanfilade | Write-only | I-address → {DocISA} |
| POOM | **Mutable** | V-address → I-address |

The POOM is explicitly "the sole locus of destructive mutation" [SS-POOM-MUTABILITY]. The other two layers are permanent precisely because they record orthogonal facts (content identity and document membership) that survive V-space restructuring. V-position is a POOM-only fact with no shadow copy in the permanent layers.

[INV-DELETE-NOT-INVERSE] captures the consequence: even perfect knowledge of which I-addresses a document once contained (from DOCISPAN) plus their current content (from granfilade) cannot reconstruct the mapping — because the mapping from V-address to I-address is not stored outside the POOM.

---

### Conclusion

| Recovery Source | What It Provides | V-Position Recoverable? |
|----------------|-----------------|------------------------|
| Granfilade | I-address → content bytes | No |
| Spanfilade/DOCISPAN | I-address → document membership | No |
| CREATENEWVERSION (before DELETE) | Independent POOM snapshot | **Yes** |
| CREATENEWVERSION (after DELETE) | Snapshot of post-delete state | No (already lost) |

The V-position information is irrecoverably destroyed if no version was created before the deletion. This is not a deficiency but the fundamental design: Xanadu's permanence guarantees apply to **content identity** (I-addresses) and **document membership** (DOCISPAN), not to **positional mappings** (POOM state). The version mechanism is the system's explicit answer to the need for positional history preservation.

## Code Exploration

Now I have the complete picture from the source. Let me compile the full analysis.

---

## Analysis: V-Position Recoverability After DELETE

### The Delete Path (Traced to the Machine)

`dodeletevspan` [do1.c:158–167] is the entry point:

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

It fetches the document's POOM via `findorgl`, then calls `deletevspanpm` [orglinks.c:145–152]:

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

`deletend` [edit.c:31–76] is the core:

1. Plants two knife cuts at `origin` and `origin + width` [edit.c:40–44]
2. Finds the common ancestor of both cuts [edit.c:45–46]
3. Walks all children [edit.c:47–73], classifying each bottom crum by position relative to the deleted V-interval:
   - **Case 1** — crum is entirely within the deleted range: `disown(ptr); subtreefree(ptr);` — the crum is removed from the tree and freed
   - **Case 2** — crum is entirely to the right of the deleted range: `ptr->cdsp.dsas[V] -= width` — V-displacement adjusted, I-mapping preserved at new V-position
   - **Case 0** — crum is entirely to the left: unchanged

Each POOM bottom crum (`type2dcbc`) encodes a rectangle in (V, I) space: its `cdsp.dsas[V]` / `cwid.dsas[V]` give V-origin and V-width; its `cdsp.dsas[I]` / `cwid.dsas[I]` give I-origin and I-width. When `subtreefree` fires on a Case-1 crum, `credel.c:413–432` recursively walks and frees all descendant crums via `efree`. The (V, I) rectangle encoded in that crum — the V→I mapping — is gone from both memory and (eventually) disk, since the POOM root is marked `modified` [orglinks.c:150 `logbertmodified`] and will be written out in its post-delete state.

Critically: **`dodeletevspan` calls nothing on the spanfilade or granfilade.** No compensating entry is written anywhere recording what V-address the deleted I-content occupied.

---

### Path 1: Granfilade Permanent Content

The granfilade is a GRAN-type enfilade indexed on a single `WIDTH` dimension — the I-address (permascroll address) axis. Its bottom crums carry `GRANTEXT` payloads [granf2.c:96–101]:

```c
locinfo.infotype = GRANTEXT;
locinfo.granstuff.textstuff.textlength = textset->length;
movmem(textset->string, locinfo.granstuff.textstuff.textstring, ...);
insertseq((typecuc*)fullcrumptr, &lsa, &locinfo);
```

`fetchorglgr` [granf2.c:22–81] retrieves a document's POOM from the granfilade by matching I-address (WIDTH). `ispan2vstuffset` [granf1.c:57–74] → `ispan2vstuffset` [granf2.c:286–318] retrieves text content for a given I-span by walking the GRAN. Neither lookup involves a V dimension anywhere — the GRAN enfilade has no V axis.

**The granfilade records I-address → text content only. It has no architectural slot for V-position. Querying it after deletion yields the permanent text, but zero information about where in V-space that text lived.**

---

### Path 2: Spanfilade DOCISPAN History

`insertspanf` [spanf1.c:15–54] is called during `docopy` (which underlies every INSERT and CREATENEWVERSION) with `spantype = DOCISPAN`:

```c
prefixtumbler(isaptr, spantype, &crumorigin.dsas[ORGLRANGE]);
tumblerclear(&crumwidth.dsas[ORGLRANGE]);
...
movetumbler(&lstream, &crumorigin.dsas[SPANRANGE]);
movetumbler(&lwidth, &crumwidth.dsas[SPANRANGE]);
insertnd(taskptr, (typecuc*)spanfptr, &crumorigin, &crumwidth, &linfo, SPANRANGE);
```

The spanfilade is a SPAN-type 2D enfilade with two dimensions: `ORGLRANGE` (document ISA, prefixed with the endpoint type — `DOCISPAN=3`, `LINKFROMSPAN`, `LINKTOSPAN`) and `SPANRANGE` (I-address from the sporglset). `linfo.homedoc` is the document ISA. **There is no V dimension in any spanfilade crum.**

`finddocscontainingsp` [spanf1.c:151–188] uses the spanfilade to answer "which documents contain this I-span?" by querying `ORGLRANGE × SPANRANGE`. It returns document addresses, not V-positions.

Since `dodeletevspan` does not remove or modify spanfilade entries, the DOCISPAN record created at insert-time persists after deletion. This has a significant side effect: the spanfilade becomes historically true but currently false — it says document D contains I-span I even after I has been deleted from D's V-space. But "contains" here means only membership in the (docISA, I-address) index, with no V coordinate at any time.

**The spanfilade DOCISPAN history cannot recover V-position. It encodes (docISA × I-address), period. The stale entries are in fact a minor semantic bug — the spanfilade doesn't track deletion.**

---

### Path 3: CREATENEWVERSION Snapshots

`docreatenewversion` [do1.c:260–298] is more interesting:

```c
bool docreatenewversion(typetask *taskptr, typeisa *isaptr, typeisa *wheretoputit, typeisa *newisaptr)
{
    ...
    if (!doretrievedocvspanfoo(taskptr, isaptr, &vspan)) return FALSE;
    
    vspec.docisa = *isaptr;
    vspec.vspanset = &vspan;
    
    addtoopen(newisaptr, user, TRUE, WRITEBERT);
    docopyinternal(taskptr, newisaptr, &vspan.stream, &vspec);
    ...
}
```

`doretrievedocvspanfoo` [do1.c:301–309] → `retrievedocumentpartofvspanpm` [orglinks.c:155–162] reads the source POOM's root crum:

```c
movetumbler(&((typecuc*)orgl)->cdsp.dsas[V], &vspanptr->stream);
movetumbler(&((typecuc*)orgl)->cwid.dsas[V], &vspanptr->width);
```

This gives the gross V-span bounds of the source document. Then `docopyinternal` [do1.c:66–82] calls `insertpm` [orglinks.c:75–134], which creates POOM crums in the *new* version's POOM encoding the current V→I mapping of the source. Each sporgl from the source is mapped into the new version's V-space:

```c
movetumbler(&lstream, &crumorigin.dsas[I]);  // I-address from source
movetumbler(vsaptr, &crumorigin.dsas[V]);    // V-address in new version
insertnd(taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);
```

The new version's POOM faithfully records the V→I mapping **as it existed at the moment `docreatenewversion` was called**.

If a version snapshot is taken **before** deletion, you can recover the pre-delete V-position of any I-address by querying the snapshot's POOM:

`ispan2vspanset` [orglinks.c:389–394] → `permute` [orglinks.c:404–422] → `span2spanset` [orglinks.c:425–454] → `retrieverestricted` [retrie.c:56–85] — this traverses the snapshot's POOM looking for crums whose I dimension intersects the target I-span, then reads off the V dimension from `context2span`.

**This is the only path. But it requires the snapshot to have been created before the deletion.**

---

### Verdict

**The V-position information is irrecoverably destroyed unless a CREATENEWVERSION snapshot was taken before the deletion.**

Here is why each alternative fails independently:

| Source | What it records | V-position recoverable? |
|--------|----------------|------------------------|
| Granfilade | I-address → text content (GRAN, WIDTH-only) | **No** — no V axis exists |
| Spanfilade DOCISPAN | (docISA × I-address) pairs, never updated on delete | **No** — V dimension absent; stale entries persist silently |
| CREATENEWVERSION | A new POOM snapshotting V→I mapping at call time | **Yes, if called before deletion** |

The architecture has a clean asymmetry: V-space is mutable (the POOM can be edited) while I-space is permanent (the granfilade grows but never shrinks). After a delete, the POOM crums encoding (V→I) for the removed range are freed via `subtreefree` → `freecrum` → `efree` [credel.c:413–432; 434–453], and no secondary index captures them. The granfilade records the I-content permanently, but the V-coordinate was always the POOM's exclusive responsibility. The spanfilade is a link-navigation structure, not a V-history log.

CREATENEWVERSION works precisely *because* it creates a new POOM (`createorglingranf` → `createenf(POOM)` [granf2.c:120]) and then copies the full V→I structure into it via `insertpm`. That POOM persists independently of any subsequent edits to the source document. The snapshot's POOM is the only durable record of what V-position a given I-address occupied at a specific moment.

If no snapshot was taken before deletion, the mapping is gone. There is no journaling, no undo log, and no indirect reconstruction path through the surviving data structures.

---

## Question 14 [gregory]

> Was there ever a design intent for an operation journal or event log in udanax-green — something beyond the implicit history encoded in the granfilade's append-only structure and the spanfilade's monotonic growth — or was faithful state reconstruction explicitly delegated to the client via CREATENEWVERSION snapshots?

### Gregory's Answer

## KB Synthesis

The KB contains no evidence of a design intent for an operation journal or event log. What it does reveal is a clear architectural pattern: the permanence principle provides implicit history as a *side effect*, while explicit state reconstruction is unambiguously delegated to the client via CREATENEWVERSION snapshots.

## The Implicit History Is Structural, Not Journaled

The append-only structures do encode history, but only incidentally:

- **The granfilade** allocates I-addresses monotonically [INV-MONOTONIC] [SS-ADDRESS-ALLOC]. Sequential inserts produce contiguous I-addresses [ST-INSERT Finding 0033], and CREATELINK interrupts this sequence [INT-LINK-INSERT Finding 0063] — so the allocation order is recoverable. But this is a *content permanence* property, not a log. Finding 0059 explicitly states: **"No transaction log: Within-session consistency comes from the in-memory cache, not from disk state."** [SS-DURABILITY-BOUNDARY]

- **The spanfilade** is write-only, accumulating DOCISPAN entries that never delete [INV-SPANF-WRITE-ONLY]. This makes it a monotonic historical index of *what content was ever placed in which documents*, not a log of *which operations occurred in which order*.

Neither structure records the operation that created the entry. `tumblersub(content_iaddr_1, content_iaddr_2)` tells you the *interval* between allocations; it tells you nothing about whether those allocations came from two INSERTs, one INSERT and one COPY, or some other combination.

## State Reconstruction Is Explicitly the Client's Job

The KB is unambiguous on this point. Finding 0072 states:

> "CREATENEWVERSION is the sole mechanism for preserving a document's state before editing... Critically, there is no automatic invocation of this operation; it must be called explicitly before any edit whose prior state might need recovery." [ST-VERSION-CREATE, FC-VERSION-ISOLATION]

And: **"Without an explicit version, no prior state is recoverable."** [ST-VERSION-CREATE]

The access control machinery reinforces this design. When write access is denied via BERT, the intended protocol response is to create a version and open that instead [INT-BERT-VERSION]. Write contention is not a recoverable error — it is a redirect into the versioning workflow. The architecture presumes that clients manage document history by creating versions at appropriate decision points.

## Non-Invertibility Forecloses Replay

A journaling system would require that operations be replayable. The KB establishes this is structurally impossible:

> DELETE followed by INSERT of identical text does NOT restore the original document state. The V-space content is reconstructed (same characters at same positions), but the I-space identity is entirely different. [INV-DELETE-NOT-INVERSE]

Fresh I-addresses are allocated by `inserttextingranf` on every INSERT [FC-GRANF-ON-DELETE, Finding 0061] — there is no mechanism to "replay" to a prior identity state. This is not an oversight; it follows directly from the append-only allocator. A replay-capable system would require either operation logs or copy-on-write semantics, and the KB documents neither.

## Crash Recovery Is Session-Level, Not Operation-Level

The durability model is explicitly coarse-grained:

> "The system provides session-level durability (all-or-nothing at session boundary), not operation-level durability." [SS-DURABILITY-BOUNDARY]

No `fsync`, no transaction log, no journaling [EC-CRASH-MID-WRITE, EC-NO-STARTUP-VALIDATION]. The disabled `levelpull` function [SS-ENFILADE-TREE] is the only "missing mechanism" visible in the code, and it concerns tree height minimality, not history.

## The Protocol Itself Is Anti-Journal

Finding 0050's response-before-operation pattern [EC-RESPONSE-BEFORE-CHECK] means the FEBE protocol cannot even reliably confirm that individual operations succeeded. A journaling architecture requires reliable operation confirmation as a prerequisite. The KB shows this was not the design: the back end sends success responses before executing operations, and silent failures are acceptable.

---

**Conclusion:** The design intent was permanence-based, not journal-based. The granfilade's monotonic I-address allocation and the spanfilade's write-only growth provide implicit provenance as a consequence of the content permanence axiom [INV-IADDR-IMMUTABILITY, INV-IADDRESS-PERMANENT], not as a designed logging mechanism. Explicit state reconstruction was delegated to clients via CREATENEWVERSION, with the BERT access control system providing the workflow trigger (write denial → version creation) [INT-BERT-VERSION]. The system was designed around the invariant that content is permanent and the POOM is mutable — recovery meant creating a snapshot before mutating, not replaying operations from a log.

## Code Exploration

Now I have a complete picture. Let me compile the full answer.

---

## Was There a Design Intent for an Operation Journal?

**Answer:** Yes — there is evidence of two distinct and separate journaling/history concepts in udanax-green, one of which was partially built (the session replay log), and one of which was explicitly designed but never implemented (the "historical trace" navigation system). Neither was the append-only growth of the enfilades, and neither was CREATENEWVERSION. Here is the full account from the code.

---

### 1. The `interfaceinput` Session Replay Log — Built, But Not a Journal

The daemon (`bed.c`) and test backend (`be.c`) both open a timestamped file at startup:

**`be.c:59,63`:**
```c
febelog = interfaceinput = reallog = logfile = nulllog = fopen ("/dev/null", "a");
...
sprintf(buf,"ln%d.%d.%d:%d",local->tm_mon+1,local->tm_mday,local->tm_hour,local->tm_min);
```

**`bed.c:77,82`:**
```c
febelog = interfaceinput = reallog = logfile = nulllog = fopen("/dev/null", "a");
...
interfaceinput=fopen(buf, "w");
```

This file (`ln1.25.14:30`-style name) receives raw FEBE protocol bytes, but **only for mutating operations**. The flag `logstuff` is set `TRUE` exactly and only in the following `get` handlers in `get1fe.c`:

| Operation | Line |
|---|---|
| `getinsert()` | 26 |
| `getcopy()` | 57 |
| `getrearrange()` | 68 |
| `getcreatelink()` | 77 |
| `getcreatenewdocument()` | 134 |
| `getdeletevspan()` | 141 |
| `getcreatenewversion()` | 151 |
| `getopen()` / `getclose()` | 257, 248 |

**`get1fe.c:26-27`** (representative):
```c
logstuff = TRUE; 
fprintf(interfaceinput, "%d~",INSERT);
```

When `logstuff` is true, every byte of the request parameters flows through `pullc()` in `get2fe.c:56-61`:
```c
if (logstuff && interfaceinput && interfaceinput != nulllog) {
    if (temp == WORDELIM)
        putc ('\n', interfaceinput);
    else
        putc (temp, interfaceinput);
}
```

Query operations — `RETRIEVEV`, `RETRIEVEDOCVSPANSET`, `FOLLOWLINK`, `FINDLINKSFROMTOTHREE`, `SHOWRELATIONOF2VERSIONS` — set no `logstuff` flag and write nothing.

The session closes with a sentinel in `bed.c:131`:
```c
fprintf(interfaceinput, "%d~\n", QUIT);
fclose(interfaceinput);
```

And account switches are recorded via `logaccount()` in `get1fe.c:238-243`:
```c
int logaccount(tumbler *tp)
{
    if (interfaceinput) {
        fprintf(interfaceinput, "%d~",XACCOUNT);  
        puttumbler(interfaceinput,tp);
    }
}
```

**What this is:** A self-contained, replayable, mutation-only FEBE protocol transcript of the session. The format is the raw wire protocol — you could theoretically feed `interfaceinput`'s contents back to a fresh backend to replay the session. But this is **not** persistent like `enf.enf`. It is session-scoped, created fresh each daemon startup (`be.c:63-68`, `bed.c:80-86`), and there is no machinery anywhere to use it for recovery or state reconstruction. It is forensic and diagnostic in intent.

A second, more verbose file — `febelog`, recording ALL bytes both from frontend and backend (annotated with `\nfe:\n` / `\nbe:\n` headers) — was gated behind `#ifndef DISTRIBUTION` in `bed.c:83-87` and `be.c:66-68`, making it debug-only even within the codebase.

There is no write-ahead log, no transactional boundary, no `rollback`, no `undo`, no `checkpoint`, no `transaction` — the grep finds nothing at all for any of these.

---

### 2. The "Historical Trace" — Designed, Never Built

This is the most significant finding. There is a fully assigned **FEBE request opcode** for a history navigation facility, with named stub entry points in every layer of the stack, but every single implementation site is empty or commented out.

**`requests.h:26`:**
```c
#define NAVIGATEONHT 9
```

**`fns.c:236-248`** — The top-level handler:
```c
void navigateonht(typetask *taskptr)
{
#ifndef DISTRIBUTION
error (taskptr, "GACK !  (historical trace)\n");
#endif
/*
  typeisa docisa, htisa;
  typehtpath turninginstructions;
  bool getnavigateonht();
    if (getnavigateonht(taskptr, &docisa, &htisa, &turninginstructions))
       donavigateonht(taskptr, &docisa, &htisa, &turninginstructions);
*/
}
```

The commented-out parameters reveal the design:
- `htisa` — an ISA (permanent identity address) for a **history trace object** — this was a first-class addressable entity, not a derived view
- `turninginstructions` of type `typehtpath` — a navigation path *within* the history trace

**`typehtpath` is declared in `fns.c:243` but is never defined in any header file** — the type has no concrete definition anywhere in the codebase. `common.h`, `xanadu.h`, `crum.h`, `enf.h`, `ndenf.h` — none of them define it.

**`get1.c:146`** (interactive backend input layer):
```c
/* getnavigateonht */
```

**`do1.c:454`** (implementation layer):
```c
/* donavigateonht */
```

**`putfe.c:297`** (output layer):
```c
/* historical trace */
```

**`get1fe.c:267`** (FEBE input layer):
```c
/* historical trace */
```

Every layer of the stack — get, do, put, febe — has a placeholder comment and nothing more.

**`init.c:71-74`** — and the operation is explicitly disabled in safe/daemon mode alongside `SOURCEUNIXCOMMAND`:
```c
if (safe) {
    requestfns[SOURCEUNIXCOMMAND] = nullfun;
    requestfns[NAVIGATEONHT] = nullfun;
```

---

### 3. The "ht stuff" Hooks — The Intended Side-Effect Architecture

The design intent was that history maintenance would be performed **as a side effect of each mutation**, not as a separate journaling operation. Every mutating function in `do1.c` has `/* ht stuff */` as a commented-out final step:

**`do1.c:40-43`** (`dorearrange`):
```c
return (
   findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
&& rearrangepm (taskptr, docisaptr, docorgl, cutseqptr)
/*&& TRUE*/ /* ht stuff */  );
```

**`do1.c:59-64`** (`docopy`):
```c
   && insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)
   &&  insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN)
   && asserttreeisok(docorgl)
/*      &&  ht stuff */ );
```

**`do1.c:117-122`** (`doinsert`):
```c
    ret = (inserttextingranf(taskptr, granf, &hint, textset, &ispanset)
        && docopy (taskptr, docisaptr, vsaptr, ispanset)
    /* no ht stuff here, 'cause it's taken care of in */
    /*   docopy */ );
```

This last comment is revealing: the author consciously noted that `doinsert` does NOT need its own ht hook because `docopy` (which it calls) already has one. This is not a forgotten placeholder — it is deliberate reasoning about where the hook should fire. The `/* ht stuff */` hooks were to be chained at the end of each successful mutation, building up the history structure incrementally. This mirrors the pattern already used by `insertspanf` (which is called for similar side-effect maintenance of the spanfilade).

---

### 4. CREATENEWVERSION — The Implemented Snapshot Mechanism

In the absence of any operational history navigation, state reconstruction is entirely handled by `CREATENEWVERSION`. Its implementation in `do1.c:260-298`:

1. Creates a new granf node (`createorglingranf`) — a new permanent ISA
2. Retrieves the full vspan of the source document (`doretrievedocvspanfoo`)
3. Bulk-copies all content into the new version (`docopyinternal`)
4. Marks the version as modified (`logbertmodified` at line 295)
5. Closes the new version (`doclose`)

This produces a new ISA whose content is a snapshot of the source at the moment of the call. The client is entirely responsible for calling this at the right time; the backend provides no triggering mechanism. Faithful state reconstruction requires that the client has saved the ISA returned by a prior `CREATENEWVERSION` — there is no backend mechanism to answer "what was document X's state at time T?"

---

## Conclusion

The code reveals three distinct and separable concepts:

1. **Implicit append-only growth** of the granfilade and spanfilade — content and link references accumulate monotonically; old ISA positions are never reused.

2. **The `interfaceinput` session replay log** — a mutation-only FEBE wire-format transcript written at runtime, session-scoped, suitable for forensics or manual replay but not integrated into any recovery or reconstruction machinery.

3. **The "historical trace" (`navigateonht`, `htisa`, `typehtpath`, `/* ht stuff */`)** — a designed but entirely unimplemented first-class history navigation system. It would have been a navigable addressable object (its own ISA), built up as a side effect of each mutation. The type `typehtpath` was never defined. The implementation stubs (`donavigateonht`, `getnavigateonht`) were never written. The feature is listed alongside `SOURCEUNIXCOMMAND` as disabled in safe mode.

4. **CREATENEWVERSION** — the sole implemented mechanism for explicit state reconstruction, delegated entirely to client initiative.

The design intent for something beyond the implicit structural history was real and explicit — an `htisa` that you could navigate with `turninginstructions`. It was not merely a vague aspiration; it had a protocol opcode (9), named types, and per-mutation hook sites. But it was never built, and in its absence, reconstruction is indeed the client's responsibility via `CREATENEWVERSION` snapshots.

---

## Question 15 [gregory]

> If a replay mechanism were to reconstruct a document's current POOM state from a sequence of recorded operations, does the `makegappm` shift logic in `insertnd` depend on any transient state (like current tree shape or crum boundaries) that would differ between original execution and replay, or are the V-address shifts purely a function of the insertion point and width regardless of enfilade structure?

### Gregory's Answer

## KB Synthesis

## Replay Determinism of `makegappm` Shift Logic

The short answer: **the shift logic is purely a function of the insertion parameters and the current logical V-positions of crums — no transient state that would diverge between original execution and replay.**

Here is the reasoning across the relevant layers.

---

### What `makegappm` actually consults

[SS-TWO-BLADE-KNIFE] establishes the inputs:

1. **`blade[0]`** — the insertion V-position, directly from the operation parameter
2. **`blade[1]`** — computed by `findaddressofsecondcutforinsert()` as `(N+1).1`, where N is the subspace digit of the insertion position; this is a deterministic arithmetic function of `blade[0]` alone

Then [ST-INSERT (Finding 0054)] describes `insertcutsectionnd`, which classifies each POOM crum into one of three cases based on `whereoncrum(crum, blade[i])`:

- **Case 0** (before `blade[0]`): no shift
- **Case 1** (in `[blade[0], blade[1])`): shift by `+insert_width`
- **Case 2** (at or beyond `blade[1]`): no shift

The shift amount `+insert_width` is an operation parameter. The blade positions are derived from the operation parameter. The only remaining input is **the current logical V-position of each crum**.

---

### Are current crum V-positions transient or deterministic?

[INV-ENFILADE-RELATIVE-ADDRESSING] establishes that the absolute grasp of any 2D enfilade node is `absolute_grasp(parent) + node.cdsp`, computed at `retrie.c:337` as `grasp = offset + ptr->cdsp`. The stored `cdsp` values are relative (maintained by `setwispnd`), but the logical V-positions (absolute grasps) are fully determined by the accumulated history of operations.

Each INSERT shifts crums in `[blade[0], blade[1])` by `+width`. These shifted crums then become the inputs to the next INSERT's classification. Given the same sequence of operations, the logical V-positions are identical at each step — tree reshaping (splits, rebalances) is also deterministic because:

- Split triggers (`toomanysons`) depend only on node occupancy and the fixed branching constants `MAXUCINLOAF=6`, `MAX2DBCINLOAF=4` [SS-ENFILADE-BRANCHING]
- Rebalancing uses diagonal ordering (`shellsort` by `dsas[0]+dsas[1]`) [ST-REBALANCE-2D], computed from the current displacements — themselves deterministic
- `randomness(.3)` always returns TRUE [ST-REBALANCE-2D Finding 0073], so there is no stochastic component

---

### The `makegappm` early exit and `isanextensionnd`

Two additional sub-decisions could in principle differ between runs:

**Early exit at ONMYRIGHTBORDER** [PRE-INSERT Finding 0062]: If the insertion V-position equals the reach of a crum, `makegappm` returns without cutting. This depends on whether a crum's reach equals the insertion point. Crum reaches are fully determined by prior operations, so replay produces identical early-exit behavior.

**Extension vs. new crum** (`isanextensionnd`) [ST-INSERT Finding 0062]: Whether the new content's I-address range is contiguous with an existing crum's I-address range. This checks:
- `homedoc` matches (determined by which document the INSERT targets)
- `new_origin == existing_crum.reach` in I-space

I-address allocation is stateless query-and-increment on the granfilade [SS-ADDRESS-SPACE Finding 0061]: `next_iaddr(granf) = max_iaddr(granf) + 1`. Given the same prior operation sequence, the granfilade state is identical, so I-addresses allocated at each step are identical, so the extension check produces the same result.

---

### The one structural asymmetry that does NOT affect replay

[INT-DELETE-SUBSPACE-ASYMMETRY] and [FC-SUBSPACE] note that DELETE's subspace isolation works through `strongsub`'s exponent guard — an arithmetic accident rather than a structural knife. This means DELETE does not produce any tree-structural variation that would differ between replay and original; `strongsub` is a pure function of tumbler values.

---

### Summary

| Input to `makegappm` | Replay-invariant? | Reason |
|---|---|---|
| `blade[0]` (insertion V-pos) | Yes | Operation parameter |
| `blade[1]` (`(N+1).1`) | Yes | Pure function of `blade[0]` |
| Shift amount (`+width`) | Yes | Operation parameter |
| Crum V-positions | Yes | Deterministic accumulation of prior shifts |
| I-addresses (for extension check) | Yes | Stateless granfilade query-and-increment [SS-ADDRESS-SPACE Finding 0061] |
| Split/rebalance structure | Yes | Fixed branching constants, no randomness |

A replay that applies operations in the same order will produce **identical `makegappm` behavior** — identical knife cuts, identical shift regions, identical extension vs. new-crum decisions. The enfilade state at each step is a pure function of the operation prefix. There is no ambient session state, no clock, and no random component that could cause divergence.

The only caveat is the grim reaper cache eviction order [SS-CACHE-MECHANISM], which could differ if cache pressure patterns vary. But grim reaper eviction affects only which crums are in memory vs. disk — the logical V-positions and the shift arithmetic are unaffected.

## Code Exploration

Now I have everything I need. Let me write the full analysis.

---

## Analysis: `makegappm` Shift Logic — Transient-State Dependencies for Replay

### The Call Sequence

`insertnd.c:51-61` shows that `makegappm` runs exclusively for POOM (not SPAN), immediately before `doinsertnd`:

```c
case POOM:
    makegappm (taskptr, fullcrumptr, origin, width);  /* line 54 */
    checkspecandstringbefore();
    setwispupwards(fullcrumptr,0);
    bothertorecombine=doinsertnd(fullcrumptr,origin,width,infoptr,index);
    setwispupwards(fullcrumptr,1);
    break;
```

`makegappm` opens the V-address space *before* `doinsertnd` places the new crum. Its job is to shift the displacements of sons that come after the insertion point.

---

### The Second Cut Is Purely Arithmetic

`insertnd.c:145`:
```c
findaddressofsecondcutforinsert(&origin->dsas[V], &knives.blades[1]);
```

`findaddressofsecondcutforinsert` (`insertnd.c:174-183`) uses only `tumblerclear`, `tumblerincrement`, `beheadtumbler`, and `tumblerintdiff` — all pure tumbler arithmetic on `position`. No tree is read. With a concrete trace for `position = 2.P` (document 2, V-stream position P):

1. `tumblerincrement(position, -1, 1, secondcut)` → increments the most-significant digit → produces `3.P`  
2. `beheadtumbler(position, &intpart)` → strips the leading `2`, `intpart = P`  
3. `tumblerincrement(secondcut, 0, -P, secondcut)` → subtracts P from the sub-digit → `3.0`  
4. `tumblerincrement(secondcut, 1, 1, secondcut)` → appends `.1` → `3.1`

So **`blade[1]` is always `3.1` for any insertion into document 2**, regardless of the insertion position within that document. `blade[0]` = `origin` and `blade[1]` = start-of-next-document. The cut pair deterministically brackets the entire "current document's subsequent content" zone based only on `origin`'s document-prefix. **No tree state is involved in computing either blade.**

---

### The Guard Condition IS Transient-State-Dependent

`insertnd.c:140-143`:
```c
if (iszerotumbler (&fullcrumptr->cwid.dsas[V])
|| tumblercmp (&origin->dsas[V], &grasp.dsas[V]) == LESS
|| tumblercmp (&origin->dsas[V], &reach.dsas[V]) != LESS)
    return(0);    /* this if for extensions to bc without calling cut*/
```

`grasp` and `reach` come from `prologuend(fullcrumptr, &zero_offset, &grasp, &reach)` (line 139). These reflect the **actual V-extent of the POOM's current content** — the start and end V-address of all crums in the enfilade. If at replay time the POOM has different V-extent (because a prior operation had a different result, or because the enfilade is empty), this guard fires or not fires differently.

This is a **real divergence point**: an insertion that was a no-op during original execution (because `origin` was below `grasp.dsas[V]` or beyond `reach.dsas[V]`) will not be a no-op during replay if the V-extent has changed, and vice versa.

---

### `newfindintersectionnd` Is a Stub — Father Is Always the Fullcrum

`ndinters.c:38-42`:
```c
int newfindintersectionnd(typecuc *fullcrumptr, typeknives *knives, typecuc **ptrptr, typewid *offset)
{
    *ptrptr = fullcrumptr;
    clear (offset,sizeof(*offset));
}
```

The commented-out original `findintersectionnd` would have descended the tree to find the minimal containing ancestor. The current implementation **always sets `father = fullcrumptr` and `foffset = 0`**. The old code is preserved as a block comment at lines 18-37.

Combined with line 138 (`/* fullcrum always has zero offset */`) and the zero `foffset`, `prologuend(father, &foffset=0, &fgrasp, NULL)` yields `fgrasp = 0`. Therefore every son `ptr`'s `cdsp.dsas[V]` is its **absolute V-address**.

---

### The Shift Amount Is Purely `width->dsas[V]`

`insertnd.c:162`:
```c
case 1:/*9-17-87 fix */
    tumbleradd(&ptr->cdsp.dsas[V],&width->dsas[V],&ptr->cdsp.dsas[V]);
    ivemodified (ptr);
    break;
```

The shift is `width->dsas[V]` — a parameter. No tree state contributes to the shift *amount*.

---

### Which Crums Get Shifted — Transient-State-Dependent Through `makecutsnd`

Before `insertcutsectionnd` can classify sons, `makecutsnd(fullcrumptr, &knives)` (`insertnd.c:148`) restructures the tree, splitting any crum that straddles `blade[0]` or `blade[1]`. This is the heart of the tree-state dependency.

`insertcutsectionnd` (`edit.c:207-233`) classifies each son by checking `blades[1]` then `blades[0]`:
- Return `2`: son starts at or after `blade[1]` (entirely right of both cuts) → **no shift**
- Return `1`: son starts at or after `blade[0]` but before `blade[1]` → **shifted by width**
- Return `0`: son entirely before `blade[0]` → **no shift**

After `makecutsnd`:
- **Section 0**: content before the insertion point (V < blade[0]) — no shift
- **Section 1**: content starting at `blade[0]` through `blade[1]` — covers all of the current document's content from insertion point onward — shifted by `width`
- **Section 2**: content at `blade[1]` or beyond — covers content from other documents — no shift

The abstract semantic effect is correct regardless of tree shape: all content of the current document at or after the insertion point gets shifted by `width`.

**But which relative `cdsp` values get modified** is entirely determined by what sons exist at the fullcrum level after `makecutsnd`. This depends on:

1. The tree height before the call
2. The crum fanout and loaf structure (`ndcuts.c:55-66`: `if (toomanysons(ptr)) { levelpush(ptr); makecutsnd(...) }` — recursive)
3. Prior `recombine` decisions that merged or split crums differently

Two trees with identical abstract V-content but different shapes will produce different sets of sons for the classification loop, with different `cdsp` values — but the same absolute V-addresses shifted. The logical result is identical; the internal tree operations are not.

---

### The `doinsertnd` Phase Also Reads Transient State

After `makegappm`, `doinsertnd` calls `insertmorend` → `makeroomonleftnd` (`makeroom.c:13-48`), which calls `expandcrumleftward` to rewrite displacements when the insertion point is to the left of the current father's coverage. `makeroomonleftnd` directly reads and mutates `ptr->cdsp` values of all sons based on `grasp` (line 31: `tumblersub(&grasp->dsas[i], &origin->dsas[i], &base)` — grasp is from `prologuend`, hence tree-state-dependent).

---

### Summary: What Is and Is Not Purely Functional

| Aspect | Depends on Tree State? |
|---|---|
| `blade[0]` (insertion cut) | No — equals `origin->dsas[V]` |
| `blade[1]` (second cut) | No — pure arithmetic on `origin` |
| **Guard condition** (lines 140-143) | **Yes** — depends on POOM's current V-extent |
| Shift amount (`width->dsas[V]`) | No — a direct parameter |
| Which *absolute* V-addresses are shifted | No — all content in `[blade[0], blade[1])` |
| Which *relative* `cdsp` fields are written | **Yes** — depends on what sons `makecutsnd` produces |
| `recombine` tree structure post-insert | **Yes** — depends on fanout at the time of call |
| `doinsertnd` insertion path | **Yes** — depends on post-`makegappm` tree shape |

### Replay Implication

The V-address shifts produced by `makegappm` are **logically determined** by `origin` and `width` alone — any two trees encoding the same abstract V-to-I content will reach the same abstract V-address layout after `makegappm` runs. **However:**

1. The guard at `insertnd.c:140-143` depends on the POOM's current V-extent (`grasp`, `reach`). If a replay reconstructed a POOM with a different V-extent — even one encoding the same content — `makegappm` could silently no-op where the original did not, or vice versa. This is a genuine behavioral divergence that cannot be corrected by replaying only the `cdsp` delta.

2. `makecutsnd` is a destructive tree restructuring step. Its output — the set of fullcrum sons that classification operates on — depends entirely on the current tree topology. A replay that short-circuits to "apply the same `cdsp` deltas to the same relative positions" is not valid: the positions don't correspond unless the tree shapes are identical.

3. The correct replay invariant is: **replay the high-level operation** (`makegappm(origin, width)` → `doinsertnd(origin, width, infoptr)`) on whatever tree exists at replay time. The abstract V-address result will be identical to the original if and only if the abstract POOM content is identical at each step. Internal tree structure after `recombine` may legally diverge between original and replay without affecting correctness.
