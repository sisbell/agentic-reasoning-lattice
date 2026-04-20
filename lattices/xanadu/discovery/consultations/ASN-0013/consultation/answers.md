# Consultation Answers — Concurrency and Global Indexes

**Inquiry:** What consistency must the system guarantee when multiple users concurrently modify different documents that share I-space addresses? What coordination do the global indexes (span index, link index) require? How does single-writer ownership interact with shared-read global state?
**Date:** 2026-02-24 10:59
**Questions:** 20 (10 nelson, 10 gregory)

---

## Question 1 [nelson]

> When two users simultaneously insert content into their own separate documents, must the system guarantee that neither insertion can observe a partially completed state from the other?

### Nelson's Answer

## Answer: Nelson Does Not Address This — But the Architecture Makes It Largely Moot

**Short answer:** No, Nelson does not make this guarantee explicitly. Literary Machines contains no discussion of transaction isolation, concurrent modification semantics, or observation of partial states. However, the tumbler architecture structurally minimizes the problem for the case you describe.

---

### What Nelson Says About Concurrency

Almost nothing. The relevant passages:

On future concurrent users (4/59):
> "In later versions of the storage system, we expect the back end to combine the search models of different users to create a barrel-roll shared search model which repeatedly crosses the address space on behalf of all a server's users simultaneously."

This addresses search performance optimization, not isolation guarantees.

On server state consistency (4/72):
> "A server's network model, from the null case on up, is at all times unified and operational; whatever information moves between servers is assimilated at once to its overall structure, leaving each server in canonical operating condition with a slightly improved map of what is elsewhere."

This "canonical operating condition" language is about inter-server replication state, not about whether one user can observe another's half-finished insertion.

On the session model: Nelson specifies no session state at all. The protocol is stateless at the command level — you name a document by tumbler address, issue a command, get a response. There is no OPEN/CLOSE, no locking protocol, no read-vs-write modes, and no transaction boundaries.

---

### Why the Architecture Makes It Structurally Unlikely to Matter

For the specific case of **two users inserting into their own separate documents**, the tumbler addressing system provides structural separation:

1. **Separate tumbler subtrees.** Each user's insertions allocate I-space addresses under their own User field. As Nelson says (4/20): "The owner of a given item controls the allocation of the numbers under it." Alice's content goes under her subtree; Bob's under his. There is no shared allocation counter.

2. **Separate V-space arrangements.** Each document has its own V-stream. INSERT into document A modifies A's V-to-I mapping; INSERT into document B modifies B's. These are structurally independent.

3. **Append-only I-space.** Content is added, never overwritten. Two concurrent appends to different regions of I-space cannot conflict — they are writing to different addresses.

4. **Documents are owned units.** Nelson (2/29): "Only the owner has a right to withdraw a document or change it." Two owners modifying their own documents are exercising independent authority over independent objects.

Given this separation, there is no shared mutable state that could produce a "partially completed" observation. Alice's insertion touches only her document's V-space mapping and her I-space subtree. Bob's insertion touches only his. Neither operation reads or writes anything the other touches.

---

### Where the Question Would Bite

The question becomes non-trivial in scenarios Nelson does not address:

- **Transclusion during concurrent insertion.** If Bob's document transcludes content from Alice's document, and Alice is inserting into hers while Bob reads, could Bob see a half-inserted state? Nelson's architecture suggests no (content is fetched from I-space, which is append-only), but he never explicitly guarantees atomicity of observation.

- **Link search during concurrent insertion.** If Alice creates a link whose endset covers a region Bob is simultaneously inserting into, could the link search return inconsistent results? Nelson says only that "THE QUANTITY OF LINKS NOT SATISFYING A REQUEST DOES NOT IN PRINCIPLE IMPEDE SEARCH ON OTHERS" (4/60) — a performance statement, not an isolation guarantee.

- **FINDDOCSCONTAINING during insertion.** This operation searches by I-space origin across the entire docuverse. If Alice is mid-insertion, could this query see her half-written content?

---

### Summary

| Question | Nelson's Answer |
|----------|----------------|
| Must separate-document inserts be isolated from each other? | Not stated |
| Does the architecture prevent conflicts? | Yes, structurally — separate subtrees, separate V-spaces |
| Does Nelson guarantee atomicity of observation? | No |
| Does Nelson discuss concurrent modification at all? | Only as future search optimization (4/59) |
| Is there a transaction or session model? | No — protocol is stateless |

Nelson designed the addressing system so that independent owners operate in independent subtrees. The isolation you ask about is a *consequence of the addressing architecture*, not an *explicit guarantee*. He never discusses the scenario because the tumbler design makes it structurally non-problematic for the case of separate documents. For cases involving cross-document observation (transclusion, link search, FINDDOCSCONTAINING), he is silent.

---

## Question 2 [nelson]

> If the same original content appears in multiple documents through transclusion, must an edit to one document's structure leave the shared content byte-identical for all other documents that reference it?

### Nelson's Answer

## Yes — by architectural necessity, not by special mechanism.

The answer follows directly from Xanadu's I-space/V-space separation. Editing operations modify V-space arrangements (the document's current view), never I-space content (where bytes permanently reside). Transcluded content is not a copy — it is a reference to the same I-space addresses. There is nothing to become non-identical because there was never a second copy.

### The Architecture

When document B transcludes content from document A, both documents' V-space mappings point to the **same I-space addresses**. The bytes exist once, permanently:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

### What Editing Does

INSERT, DELETE, and REARRANGE are V-space operations. They change which I-space addresses a document's virtual byte stream references, and in what order. They do not alter the bytes stored at those I-space addresses:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

Nelson makes this explicit for deletion:

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

This is the direct answer: editing one document's structure cannot affect the shared content as seen by other documents, because the editing never touches I-space.

### Why This Must Be So

Three guarantees converge to make this mandatory:

1. **I-space immutability.** Content at an I-address never changes. The storage model is append-only — new content is added, existing content is never overwritten.

2. **Transclusion is reference.** There is no second copy to diverge. Document B sees the same bytes document A created, fetched from their permanent home:

   > "No copying operations are required among the documents throughout the system, and thus we solve the problems of update — especially the problem of updating documents which depend on other documents." [LM 2/36]

3. **Link survivability depends on it.** Links attach to I-space addresses. If editing could alter I-space content, links would break — violating the permanence guarantee:

   > "Links between bytes can survive deletions, insertions and rearrangements, if anything is left at each end." [LM 4/43]

### The Two Cases

**Alice deletes content from her V-space.** The bytes disappear from Alice's current view but remain at their I-space addresses. Bob's document, which references those same I-space addresses, is completely unaffected. Alice's old versions also still contain the content.

**Alice inserts new content.** New bytes are appended to I-space at fresh addresses. Alice's V-space mapping is updated to include them. Bob's document is unaffected — his V-space mapping still points to the original I-space addresses, unchanged.

**Alice rearranges content.** A pure V-space operation — the order of references changes in Alice's document. I-space content is untouched. Bob sees no change.

### Summary

The question presupposes that "byte-identical" is a condition that must be actively maintained. In Xanadu's architecture, it is not a condition at all — it is a tautology. Transcluded content in multiple documents is not "copies that must be kept in sync" but **the same bytes at the same addresses**, accessed by reference. There is no mechanism by which editing one document's V-space arrangement could alter the I-space content seen by another document. The separation is absolute by design.

---

## Question 3 [nelson]

> Must the global index that tracks where every piece of content currently resides be updated atomically with respect to each document operation, or may it lag behind?

### Nelson's Answer

## The Index May Lag — By Explicit Design

Nelson's architecture answers this question clearly: the global content-location index is designed to be **eventually consistent**, not atomically synchronized. He builds the entire distributed system around the assumption that each server's knowledge of the whole is incomplete and improving incrementally.

### The Subrepresentation Model

Each server maintains what Nelson calls a "subrepresentation" — a local model of the entire docuverse that is always *valid* but never *complete*:

> "Each server contains a continuously valid model or subrepresentation of the entire docuverse and (because of tumbler addressing) a model of the entire network." [LM 4/72]

The critical word is "continuously valid" — not "continuously complete" or "continuously synchronized." The model is always usable, always self-consistent, but it is an approximation:

> "Each server contains a map and a subset of the whole — a microcosm that shrinks and grows." [LM 4/71]

### Incremental Improvement, Not Atomic Update

Nelson explicitly describes updates to the model as incremental and asynchronous:

> "A server's network model, from the null case on up, is at all times unified and operational; whatever information moves between servers is assimilated at once to its overall structure, leaving each server in canonical operating condition with a slightly improved map of what is elsewhere. The contents can slosh back and forth dynamically." [LM 4/72]

Three things to note here:

1. **"from the null case on up"** — the model works even when it knows nothing. It starts empty and improves.
2. **"slightly improved map"** — each update brings marginal improvement, not completeness.
3. **"slosh back and forth dynamically"** — content migrates continuously; the index tracks this migration imperfectly.

### Forwarding Compensates for Lag

The entire BEBE forwarding mechanism exists precisely because the local index does not know everything. When a server cannot satisfy a request from its local knowledge, it forwards:

> "First, by the forwarding of requests as they fan out from users to servers able to supply; and the pass-through of material that is returned to the requesting user in reply." [LM 4/70]

If atomic synchronization were required, forwarding would be unnecessary — every server would already know exactly where everything is.

### Broken Networks Are Normal

Nelson designs for partial knowledge as the default state:

> "It is a truism that 'computer networks are always broken.' Meaning that on the average some nodes are disconnected or not working." [LM 4/75]

If some nodes are always disconnected, their content indexes cannot possibly be atomically consistent with operations happening elsewhere. The system must tolerate this.

### Content Migration Is Asynchronous

Material moves between servers for performance and reliability reasons, and this migration is explicitly not synchronized with document operations:

> "Material is moved between servers for a number of purposes: 1. for more rapid access to final material, 2. for more rapid access to needed material which indexes material on other servers, 3. for rebalance in keeping with demand, 4. for redundancy and backup purposes." [LM 4/71]

This is background optimization, not transactional update.

### What Must Be Consistent

While the global index may lag, Nelson does impose a consistency requirement on each server's local state. The subrepresentation must be "continuously valid" and the server must be in "canonical operating condition" at all times. This means:

- The local model must never be self-contradictory
- Every state of the model must be usable for routing and retrieval
- Assimilation of new information must leave the model valid

This is a **local consistency** requirement, not a **global synchronization** requirement.

### The Implication for Operations Like FINDDOCSCONTAINING

The operation `FINDDOCSCONTAINING` "returns a list of all documents containing any of the material specified by the span addresses, regardless of where the native copies are located" [LM 4/63]. In a lagging-index world, this can only return what is *known* to the queried server. The forwarding mechanism and subrepresentation model handle the gap — the server returns what it knows and can discover through forwarding.

### Summary

Nelson's answer is unambiguous: the global index **may lag**, and the system is designed around this assumption. Each server maintains a valid but incomplete and improving approximation of the whole. Forwarding compensates for gaps. Atomic global synchronization is neither required nor expected. What IS required is that each server's local model remain self-consistent and operational at all times — "canonical operating condition" after every incremental update.

---

## Question 4 [nelson]

> When a new link is created in one document while another user is retrieving links for a different document, must the link index present a consistent snapshot, or may it reflect a partial update?

### Nelson's Answer

## Nelson Does Not Specify Link Index Consistency

Literary Machines does not address this question. The FEBE protocol defines each command's semantics individually, without specifying what happens when multiple users issue commands concurrently.

### What Nelson Does Say

**FEBE is command-response, not transactional.** Each operation is defined in isolation:

> "This creates a link in document \<doc id\> from \<from set\> to \<to set\> connected to \<three set\>. It returns the id of the link made." [LM 4/68]

> "This returns a list of all links which are (1) in \<home set\>, (2) from all or any part of \<from set\>, and (3) to all or any part of \<to set\> and \<three set\>." [LM 4/69]

The word "all" in FINDLINKSFROMTOTHREE implies completeness — but completeness relative to *what moment* is not specified.

**Nelson acknowledges concurrent users** but only in the context of search optimization, not consistency:

> "In later versions of the storage system, we expect the back end to combine the search models of different users to create a barrel-roll shared search model which repeatedly crosses the address space on behalf of all a server's users simultaneously." [LM 4/59]

This envisions concurrent *searches*, but says nothing about their relationship to concurrent *writes*.

**The closest statement to a consistency guarantee** appears in the BEBE (inter-server) protocol, not FEBE:

> "A server's network model, from the null case on up, is at all times unified and operational; whatever information moves between servers is assimilated at once to its overall structure, leaving each server in canonical operating condition with a slightly improved map of what is elsewhere." [LM 4/72]

"At all times unified and operational" and "canonical operating condition" are strong consistency language — but they describe *inter-server* state after BEBE updates, not *intra-server* isolation between concurrent FEBE operations.

### What Nelson Does Not Specify

The session-model analysis confirms these absences:

- No session lifecycle (connect/authenticate/disconnect)
- No OPEN/CLOSE operations on documents
- No locking protocol
- No read vs. write modes
- No mention of concurrent editing of the same document
- No transaction isolation level

Nelson's protocol is "stateless at the command level: you name a document by its tumbler address, issue a command, and the back end responds."

### What the Design Implies Without Stating

Nelson's guarantees — permanent addresses, link survivability, "all links" returned by search — are *state properties*, not *transition properties*. They describe what must be true of the system's state, not how overlapping operations must be ordered.

The spirit of "THE QUANTITY OF LINKS NOT SATISFYING A REQUEST DOES NOT IN PRINCIPLE IMPEDE SEARCH ON OTHERS" [LM 4/60] addresses *performance* isolation (irrelevant links don't slow your search), not *consistency* isolation (concurrent writes don't produce anomalous reads).

### Summary

Nelson designed the user-facing semantics (what operations do, what guarantees hold) and left concurrency control entirely to the implementor. Whether the link index must present a consistent snapshot during concurrent creation is an implementation decision that Literary Machines neither requires nor forbids. The question falls squarely in the gap between Nelson's semantic specification and the engineering decisions needed to realize it.

---

## Question 5 [nelson]

> Does single-writer ownership of a document guarantee that no coordination is ever needed between writers of different documents, even when those documents share content through transclusion?

### Nelson's Answer

## No Write Coordination, But Not Zero Dependencies

Single-writer ownership combined with immutable I-space eliminates **write-write coordination** between document owners. However, transclusion does create **read dependencies** and **contractual obligations** that the system must handle. The answer is: no coordination between *writers*, but coordination within the *infrastructure*.

### Why Write Coordination Is Eliminated

The I-space/V-space separation is the key mechanism. Each writer modifies only their own document's V-space arrangement. The I-space content they reference is permanent and immutable:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

When Alice transcludes from Bob's document, she creates a V-space mapping in *her* document that points to bytes in *Bob's* I-space. Alice never writes to Bob's storage. Bob never writes to Alice's storage. Their write paths are completely disjoint.

Similarly, address allocation requires no coordination because each owner controls their own subtree:

> "The owner of a given item controls the allocation of the numbers under it." [LM 4/20]

### Nelson Explicitly Claims This Solves the Update Problem

Nelson frames transclusion as the *solution* to inter-document coordination, not a source of it:

> "No copying operations are required among the documents throughout the system, and thus we solve the problems of update--especially the problem of updating documents which depend on other documents. We solve this problem simply by windowing to a changing document." [LM 2/36]

In a copy-based system, when Bob updates his document, everyone who copied from Bob must somehow learn about and propagate the change. That requires coordination. In Xanadu, Alice's window simply shows whatever Bob's content currently is. No notification, no synchronization, no conflict resolution.

### What Transclusion Does Create

Three forms of dependency survive, but none require writer-to-writer coordination:

**1. Read-time fetching (BEBE handles this)**

When a reader views Alice's document and it transcludes Bob's content, the system must fetch bytes from Bob's I-space. This is cross-server infrastructure coordination:

> "First, by the forwarding of requests as they fan out from users to servers able to supply; and the pass-through of material that is returned to the requesting user in reply." [LM 4/70]

Alice and Bob do nothing. The servers coordinate automatically.

**2. Royalty accounting (franchise model handles this)**

When Bob's transcluded content is delivered through Alice's document, Bob must be paid:

> "Storage Vendor/Repository Printer will forward a royalty of one Nib to Publisher each time a byte of the Work is delivered to a final user connected anywhere to the Xanadu network." [LM 5/20]

Again, Alice and Bob do nothing. The franchise infrastructure handles accounting.

**3. Contractual permanence (unilateral, not bilateral)**

Once Bob publishes, he cannot easily withdraw content that others depend on:

> "It is in the common interest that a thing once published stay published, as in the world of paper. Other readers and users will come to depend on its accessibility. Consequently its author may not withdraw it except by lengthy due process." [LM 2/43]

This is a constraint *on Bob*, not coordination *between* Alice and Bob. Bob agreed to it when he published. Alice need never communicate with Bob about it.

### Why I-Space Immutability Is the Crucial Guarantee

The reason no coordination is needed is that I-space content cannot change:

> "Content you create gets a permanent I-space address. That address will always return that exact content."

Alice's transclusion points to I-space addresses. Those addresses are permanent. Bob cannot alter what lives at those addresses. He can only change his own V-space arrangement (removing content from *his* current view), but the I-space bytes remain. Alice's transclusion always resolves.

This means:
- Bob cannot break Alice's transclusion by editing his document
- Alice cannot affect Bob's document by transcluding from it
- No race condition exists because transclusion is a read on the source and a write on the target, and each writer writes only to their own document

### The Link Case Is Identical

Links follow the same pattern. Alice can link to Bob's content without Bob's permission or knowledge:

> "Each user is free to link to anything privately or publicly. By the same token, each author of a published work is relinquishing the right to control links into that work." [LM 2/43]

Alice's link lives in Alice's document. Bob's document is unmodified. The back-end indexes the link for discoverability, but that is system bookkeeping, not writer coordination.

### Summary

| Concern | Coordination needed? | Who handles it? |
|---------|---------------------|-----------------|
| Writing to own document | No | Single owner |
| Address allocation | No | Tumbler subtree ownership |
| Reading transcluded content | Infrastructure only | BEBE protocol |
| Royalty accounting | Infrastructure only | Franchise model |
| Permanence obligation | Unilateral constraint | Publication contract |
| Link creation | No | Link lives in creator's doc |

Single-writer ownership, combined with immutable I-space and decentralized tumbler allocation, means that **no writer ever needs to coordinate with any other writer**. The system infrastructure coordinates reads, accounting, and routing — but from the writers' perspective, each works independently in their own address space, and transclusion creates only observation, never interference.

---

## Question 6 [nelson]

> If a reader queries "find all documents containing this content" while a writer is mid-operation on one of those documents, what must the reader see — the state before the operation, after, or is either acceptable?

### Nelson's Answer

# Concurrent Read During Write: What Must the Reader See?

I did not specify this. Let me be precise about what I *did* specify and what I left to implementors.

## What I Specified

The operation FINDDOCSCONTAINING "returns a list of all documents containing any portion of the material included by \<vspec set\>" [LM 4/70]. This is stated as a definite operation on a definite state — it returns *all* documents containing the material. Not "some," not "approximately all," but all.

Every operation in the FEBE protocol is defined this way — as acting on a consistent, complete picture of the docuverse. INSERT inserts. RETRIEVE retrieves what is there. FINDDOCSCONTAINING finds what contains. The definitions assume the system is in a settled condition when the operation executes.

I also specified that each server maintains "a continuously valid model or subrepresentation of the entire docuverse" and remains in "canonical operating condition" at all times:

> "A server's network model, from the null case on up, is at all times unified and operational; whatever information moves between servers is assimilated at once to its overall structure, leaving each server in canonical operating condition with a slightly improved map of what is elsewhere."
> — [LM 4/72]

## What I Did Not Specify

I did not design a concurrency protocol. The session-model extraction correctly notes that Literary Machines contains no locking protocol, no transaction isolation level, and no specification of what "mid-operation" means to an observer. I anticipated multiple simultaneous users but left the mechanics to future work:

> "In later versions of the storage system, we expect the back end to combine the search models of different users to create a barrel-roll shared search model which repeatedly crosses the address space on behalf of all a server's users simultaneously."
> — [LM 4/59]

That passage envisions concurrent *search*, not concurrent read-write isolation. I was describing a performance optimization, not a consistency guarantee.

## What My Design Implies

Though I did not specify isolation semantics, my design constraints narrow the answer considerably:

**1. The reader must not see a partial state.** The "canonical operating condition" requirement means the system is never in a state where an operation is half-done from any observer's perspective. If a writer is inserting content that creates a transclusion (making their document contain the queried material), the reader's FINDDOCSCONTAINING must return a coherent answer — either the writer's document is in the result or it is not. It must not return the document with half its invariants satisfied.

**2. Either before or after is acceptable.** Nothing in my specification requires that a reader see the *latest* state. The FINDDOCSCONTAINING definition says "all documents containing" — but "containing" is evaluated against some state of the docuverse. If the reader's query executes against the state just before the writer's operation takes effect, that is a valid answer. If it executes against the state just after, that is also valid. Both are consistent states in canonical operating condition.

**3. The reader need not be told an operation is in progress.** My privacy principle — "The network will not, may not monitor what is read or what is written in private documents" [LM 2/59] — extends naturally here. The system should not leak information about who is writing what, or that a write is underway, through the query results.

## The Honest Summary

My FEBE commands are defined as if they execute instantaneously on a consistent state. I did not address the question of which consistent state a concurrent reader observes, because I did not design the concurrency layer. What I *did* require is that the system always present a valid, canonical model — never a torn or partial one.

So: **before or after, either is acceptable. A partial or inconsistent view is not.** The choice between "before" and "after" is an implementation decision I left open. What I forbade, implicitly through the "canonical operating condition" requirement, is any answer that could not have arisen from some complete, settled state of the docuverse.

NEED_RAW: [4/58-4/60] — The link search satisfaction model on these pages may contain additional constraints on what "satisfying a request" means during concurrent modification. The curated sources cover the key quote about quantity not impeding search, but there may be additional relevant detail about search semantics.

---

## Question 7 [nelson]

> Must the system enforce a total ordering of all operations across all documents, or is it sufficient that operations within each document are ordered and operations on different documents are independent?

### Nelson's Answer

# Ordering of Operations Across Documents

## Short Answer

Per-document ordering is sufficient. Nothing in my design requires — or even suggests — a total ordering across all documents. The architecture actively works against such a requirement.

## What I Actually Specified

The FEBE protocol defines commands that operate on **named documents**. Every mutating operation — INSERT, DELETEVSPAN, COPY, REARRANGE, APPEND, MAKELINK — takes a `<doc id>` parameter that identifies the target document. The back end responds to these commands; it does not impose a global sequence among them.

> "What the Xanadu storage and hypertext system does — and thus is — is defined by the commands to which it responds."
> — [LM 4/61]

I designed for millions of simultaneous users:

> "An ever-growing network, instantaneously supplying text and graphics to millions of simultaneous users, would be impossible if it slowed down too fast as it grew."
> — [LM 4/2]

A system that requires total ordering of all operations across all documents cannot serve millions of simultaneous users. The performance constraint alone rules it out.

## Why the Architecture Implies Independence

Three design decisions make cross-document independence not just possible but inevitable:

### 1. Ownership Isolates Writers

> "Every document has an owner, the person who created and stored it... Only the owner has a right to withdraw a document or change it."
> — [LM 2/29]

If only the owner writes to a document, there are no write-write conflicts between documents owned by different users. Two users editing their own documents need not coordinate at all.

### 2. Tumbler Forking Eliminates Address Coordination

> "The owner of a given item controls the allocation of the numbers under it."
> — [LM 4/20]

Address allocation is local to each owner's subtree. When I create a new byte in my document, I fork a new address under my document's tumbler. You do the same under yours. We need no coordination because our address spaces are disjoint by construction.

### 3. I-Space Is Append-Only and Immutable

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically."
> — [LM 2/14]

Once content exists in I-space, it never changes. When your document transcludes my content (via COPY), it references my immutable I-space addresses. No lock is needed on my content because it cannot change. Your COPY writes only to your document's V-space — that's a write to your document, not mine.

## Cross-Document Operations Do Not Require Global Ordering

Consider the operations that touch multiple documents:

| Operation | What it reads | What it writes | Coordination needed? |
|-----------|--------------|----------------|---------------------|
| **COPY** | Source I-space (immutable) | Target V-space (owner's doc) | No — reads immutable data |
| **MAKELINK** | Nothing external | Home document's link subspace | No — writes to one document |
| **FINDLINKSFROMTOTHREE** | Link index (read-only) | Nothing | No — pure query |
| **FINDDOCSCONTAINING** | I-space origin index (read-only) | Nothing | No — pure query |
| **SHOWRELATIONOF2VERSIONS** | Two documents' V→I mappings (read-only) | Nothing | No — pure query |

Every mutating operation writes to exactly one document. Every cross-document interaction reads immutable I-space content or performs read-only queries. There is no operation that writes to two documents atomically.

## What About the Distributed Network?

The BEBE protocol explicitly describes servers maintaining independent, eventually-consistent views:

> "Each server contains a continuously valid model or subrepresentation of the entire docuverse... The contents can slosh back and forth dynamically."
> — [LM 4/72]

> "A server's network model, from the null case on up, is at all times unified and operational; whatever information moves between servers is assimilated at once to its overall structure, leaving each server in canonical operating condition with a slightly improved map of what is elsewhere."
> — [LM 4/72]

The language here — "subrepresentation," "slosh back and forth," "slightly improved map" — describes eventual convergence, not synchronized global state. Each server is always in "canonical operating condition" regardless of what other servers are doing. This is incompatible with requiring a total order across servers.

## The Enfilade Guarantee

What I did require is that within a single document, changes leave the structure valid:

> "His new method would allow linkages to keep up with all changes. It was instantaneous and permanent and could grow indefinitely. All changes, once made, left the file remaining in canonical order, which was an internal mandate of the system."
> — [LM 1/34]

"Canonical order" is a per-document invariant. Each document's enfilade must be internally consistent after each operation. This says nothing about ordering across documents.

## What I Did Not Specify

I deliberately left unspecified:

- No locking protocol between documents or users
- No transaction model spanning multiple documents
- No global sequence numbers or vector clocks
- No read-write isolation guarantees across documents

These are implementation concerns. The semantic design requires only that each document maintains its own integrity and that I-space content, once created, is permanent and immutable.

## The Principle

The docuverse grows by independent acts of creation. Each user works in their own space, creating content and links under their own addresses. The tumbler system was designed precisely so that this independent creation requires no coordination:

> "So the docuverse is all really one big forking document."
> — [LM 4/18]

The word "forking" is key. Forks diverge independently. The tree grows at its leaves without the leaves needing to know about each other. Per-document ordering — or more precisely, per-owner ordering — is not merely sufficient. It is the natural consequence of the architecture.

---

## Question 8 [nelson]

> When a user creates a new version of a document, must the global content index and the global link index both reflect the new version at the same instant, or may they update separately?

### Nelson's Answer

## Nelson Does Not Address This

Literary Machines does not discuss the atomicity of index updates, either for CREATENEWVERSION or for any other operation. Nelson works at a level of abstraction where each FEBE command is a complete semantic action:

> "CREATENEWVERSION: This creates a new document with the contents of document <doc id>. It returns the id of the new document. The new document's id will indicate its ancestry." [LM 4/66]

The protocol is request-response. You issue a command; the back end responds with a result. Nelson does not discuss what happens *during* a command's execution, nor whether internal indices may be transiently inconsistent.

## What Nelson's Design Implies

Two passages suggest Nelson expects operations to leave the system in a fully consistent state:

On the network model:

> "A server's network model, from the null case on up, is at all times unified and operational; whatever information moves between servers is assimilated at once to its overall structure, leaving each server in canonical operating condition with a slightly improved map of what is elsewhere." [LM 4/72]

"At all times unified and operational" and "canonical operating condition" suggest Nelson envisions a system where users never observe partial updates. But this passage concerns inter-server synchronization (BEBE), not intra-server index consistency.

On the front-end contract:

> "The user's concerns are document content and links, and the complications of the protocol are to be handled invisibly by programs in the user's front-end machine, leaving the user free to think about other things." [LM 4/61]

The complications are *invisible*. This implies the back end presents a clean, consistent view after each operation completes.

## Why the Question Is Partly Moot for CREATENEWVERSION

CREATENEWVERSION specifically creates a new document sharing the *text content* of the original. The new version starts with no links of its own - links are owned by their home document:

> "The links designated by a tumbler address are in their permanent order of arrival. A document includes only the links of which it is the home document." [LM 4/31]

So there is no "link index update" for CREATENEWVERSION. The only structural change is a new V-to-I mapping (the new document's arrangement of shared content). Links that previously pointed to the old version's content reach the new version's content because they share I-addresses:

> "Links may be refractively followed from a point or span in one version to corresponding places in any other version. Thus a link to one version of a Prismatic Document is a link to all versions." [LM 2/26]

This refractive following works because link endsets point to I-space content, and the new version shares that same I-space. No link index update is needed for this to work - it falls out of the addressing model.

## The General Case

For operations that DO affect both content and links (such as INSERT, which extends text content, or MAKELINK, which creates a link), Nelson still does not address whether indices update atomically. His specification treats each command as a single semantic action that either happens or does not.

The question of whether internal indices may be transiently inconsistent during execution is an implementation concern that Nelson explicitly places below his level of design:

> "The starting point in designing a computer system must be the creation of the conceptual and psychological environment--the seeming of the system--what I and my associates call the virtuality. You begin by designing a conceptual structure and how it should feel, then work back into the mechanics." [LM 1/3]

Nelson designs the *virtuality* - what the system seems to be. In that virtuality, operations are atomic: you issue a command, you get a result, the system is in a new consistent state. Whether the mechanics achieve this through locking, journaling, or some other mechanism is not his concern.

## Summary

Nelson's specification is silent on index synchronization. His design philosophy implies that users should never observe a state where content is visible but links are not, or vice versa - each operation should leave the system in "canonical operating condition." But this is an implication of his design stance, not an explicit requirement. The specific mechanism for achieving atomicity is left to the implementor.

---

## Question 9 [nelson]

> Can the owner of a document ever be blocked or delayed by operations another user performs on a completely separate document, or must document independence be absolute?

### Nelson's Answer

## Document Independence in Xanadu

Nelson does not explicitly state a "document independence" guarantee in the form "operations on document A must never block operations on document B." However, the design of the system strongly implies this property through multiple converging principles.

### The Protocol is Stateless and Document-Scoped

Every FEBE command names its target document explicitly. There is no session state, no locking protocol, and no mechanism by which one command could create a dependency on another document:

> "What the Xanadu storage and hypertext system does—and thus is—is defined by the commands to which it responds." [LM 4/61]

INSERT takes a `<doc id>` and a `<doc vsa>`. DELETEVSPAN takes a document and a span. MAKELINK specifies the home document. No command references two documents in a read-modify-write pattern that could create cross-document contention.

The session-model analysis in the curated sources confirms: Nelson specifies "no locking protocol—no mention of concurrent editing of the same document," let alone cross-document locking. His 17 commands establish no session state whatsoever.

### Ownership Isolates Authority

> "Every document has an owner, the person who created and stored it... Only the owner has a right to withdraw a document or change it." [LM 2/29]

Ownership is encoded structurally in the tumbler address:

> "The owner of a given item controls the allocation of the numbers under it." [LM 4/20]

Each document occupies its own subtree of the tumbler tree. Operations on one subtree have no reason to touch another. There is no shared mutable state between documents—I-space content is permanent and immutable once created.

### I-Space Immutability Eliminates Read Conflicts

Transclusion creates the one apparent cross-document dependency: document A may include content whose I-space origin is in document B. But because I-space is append-only and immutable:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

Fetching transcluded content is a read of permanent data. The owner of document B cannot be performing any operation that would make those bytes unavailable—they are immutable. No write operation on B can interfere with a read of B's I-space content.

### The Soft Corridor Implies No Global Bottlenecks

Nelson's performance requirement for the docuverse explicitly demands that growth does not create blocking:

> "An ever-growing network, instantaneously supplying text and graphics to millions of simultaneous users, would be impossible if it slowed down too fast as it grew. (It can't be linear. The system cannot slow down by half as its size doubles.)" [LM 4/2]

If one user's operations could block another user working on an unrelated document, the system would fail this logarithmic scaling requirement. As the number of concurrent users grows, cross-document blocking would produce exactly the linear (or worse) slowdown Nelson prohibits.

### Link Search Is Explicitly Non-Blocking

The one operation that spans the entire docuverse—link search—comes with an explicit guarantee:

> "THE QUANTITY OF LINKS NOT SATISFYING A REQUEST DOES NOT IN PRINCIPLE IMPEDE SEARCH ON OTHERS." [LM 4/60]

This is stated as a design principle, not just a performance goal. The link search mechanism is designed so that the volume of irrelevant links does not slow down finding relevant ones.

### Freedom Principles Oppose Imprisonment

Nelson's broader philosophy resists any design where users can constrain each other:

> "In some new environments... it is possible to trap the user fully, giving him or her no options whatever except what the planner intended, with no overview and no way to step out of it. I submit that this can be highly oppressive." [LM 3/19-3/22]

While this passage addresses UI imprisonment rather than resource contention, the underlying principle applies: users must not be constrained by forces outside their control.

### The One Legitimate Dependency: Network Availability

The only cross-document dependency Nelson acknowledges is network availability. If the server holding document B is unreachable, transclusions from B into your document A cannot be fulfilled:

> "It is a truism that 'computer networks are always broken.' Meaning that on the average some nodes are disconnected or not working." [LM 4/75]

But this is infrastructure availability, not user-caused blocking. Nelson addresses it through the BEBE protocol's subrepresentation and backup mechanisms:

> "Each server contains a continuously valid model or subrepresentation of the entire docuverse... The contents can slosh back and forth dynamically." [LM 4/72]

### Conclusion

Nelson does not state document independence as an explicit axiom, but the architecture makes cross-document blocking structurally impossible under normal operation:

- The protocol is stateless and document-scoped
- Ownership is isolated by tumbler subtree
- I-space immutability eliminates write-read conflicts across documents
- The soft corridor requirement prohibits global bottlenecks
- Link search is explicitly designed to be non-blocking

The answer to your question: **no, the owner of a document should never be blocked by operations on a separate document.** This is not because Nelson states it as a guarantee, but because the system's architecture provides no mechanism through which such blocking could occur. Document independence is an emergent property of stateless commands, immutable I-space, and tumbler-partitioned ownership—not a separately stated axiom.

NEED_RAW: 4/2-4/5 (for any explicit statements about operational independence or resource isolation in the performance/economics sections that the curated sources may not fully capture)

---

## Question 10 [nelson]

> If two documents both contain links whose endpoints reference content in each other, must any operation on either document preserve the validity of all four link endpoints simultaneously?

### Nelson's Answer

# No — The Architecture Makes This Unnecessary

The scenario you describe — two documents with mutual cross-links — does not require any special atomicity or simultaneous preservation guarantee. Nelson's architecture eliminates the problem at the root by making link endpoint invalidation impossible through normal operations.

## Why the Problem Cannot Arise

**Links point to I-space, and I-space is permanent.**

Links attach to bytes via their permanent I-space addresses, not their ephemeral V-space positions:

> "A Xanadu link is not between points, but between spans of data." [LM 4/42]

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." [LM 4/30]

I-space content is append-only and immutable:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

An operation on Document A (INSERT, DELETE, REARRANGE) modifies A's V-space arrangement. It cannot destroy I-space content. Therefore it cannot invalidate any link endpoint anywhere — not in A, not in B, not in any other document.

## DELETE Does Not Destroy

The operation most likely to seem threatening is DELETE. But DELETE is V-space removal, not I-space destruction:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

If Document A's owner deletes content from A's current V-space that Link L2 (in Document B) references, the I-space bytes persist. L2 remains valid. The survivability guarantee is explicit:

> "Links between bytes can survive deletions, insertions and rearrangements, if anything is left at each end." [LM 4/43]

Since I-space content is never destroyed, "anything is left at each end" is always satisfied.

## Operations Are Per-Document, Independence Is Structural

FEBE operations target specific documents. There is no cross-document atomicity mechanism because none is needed:

- INSERT on A adds to I-space and updates A's V-space. B's links to A's I-space content are unaffected.
- DELETE on A removes from A's V-space only. B's links still resolve to the permanent I-space content.
- REARRANGE on A is pure V-space. No I-space effect at all.

The two documents' links are structurally independent:

> "A link need not point anywhere in its home document. Its home document indicates who owns it, and not what it points to." [LM 4/12]

L1 lives in A and is A's property. L2 lives in B and is B's property. Neither operation on A nor operation on B can affect the other's links, because both links point to permanent I-space content that no operation can destroy.

## The Deeper Point

Your question implicitly assumes the failure mode of conventional systems: that editing content can break references to it. Nelson designed Xanadu specifically to eliminate this:

> "Virtually all of computerdom is built around the destructive replacement of successive whole copies of each current version." [LM 2/14]

Xanadu's answer is the separation of content identity (I-space) from content arrangement (V-space). Links bind to identity. Editing changes arrangement. The two cannot interfere.

**The four endpoints in your scenario are valid before the operation, and remain valid after it — not because the operation "preserves" them, but because no operation in the system can invalidate an I-space address.** The permanence guarantee is unconditional, not conditional on atomicity across documents.

---

## Question 11 [gregory]

> When two FEBE sessions each INSERT into different documents in the same select() iteration, does the event loop fully complete one session's INSERT (including granfilade append, POOM update, and spanfilade DOCISPAN creation) before beginning the other session's INSERT, or can their sub-steps interleave?

### Gregory's Answer

## KB Synthesis

The event loop fully completes one session's INSERT before beginning the other's. Sub-steps cannot interleave.

The mechanism is run-to-completion scheduling in `bed.c`. From [INV-ATOMICITY] (Finding 0042): the `xanadu(&task)` call executes the entire operation — request parsing, state mutation, response sending, and memory cleanup — before returning to `select()`. From [INV-SEQUENTIAL-DISPATCH] (Finding 0042): even when multiple FDs are simultaneously ready in `select()`'s result, the loop iterates over them sequentially, and `xanadu()` for frontend *i* blocks until complete before frontend *i+1* is touched.

This means for two concurrent INSERTs into different documents:

- Session A's INSERT runs to completion: `inserttextingranf` (granfilade append, allocating fresh I-addresses), `insertpm` (POOM update), `insertspanf(..., DOCISPAN)` (spanfilade entry creation) — all three sub-steps finish atomically.
- Only then does Session B's INSERT begin its own three-step sequence.

There is no threading, no preemption, and no state-modifying signal handlers [INV-ATOMICITY]. The system's concurrency model is total serialization — stronger than per-document serialization [INV-SEQUENTIAL-DISPATCH].

One consequence noted in [SS-ADDRESS-SPACE] / [INV-MONOTONIC] (Finding 0061): because I-address allocation queries the granfilade for the current maximum at the moment of each INSERT, the strict serialization guarantees that Session B's allocation sees Session A's newly appended I-addresses. Each session's `findpreviousisagr` call observes a fully committed prior state, never a partial one.

## Code Exploration

Now I have everything I need. Here is the complete answer.

---

## Answer: No Interleaving — Sessions Are Fully Serialized

The event loop in `bed.c` is a **single-threaded `select()`-based server**. When two sessions both have data ready in the same `select()` iteration, their INSERTs are processed one after the other in strict sequential order. No sub-steps can interleave. Here is the precise code path proving this.

---

### 1. The Event Loop (`bed.c:103–142`)

```c
for (;;) {
    ...
    inputfds2 = inputfds;
    if (select(nfds+1, &inputfds2, 0, 0, &timeout) < 0) {  /* bed.c:111 */
        ...
    } else {
        for (i = 0; i <= nfds; i++) {                       /* bed.c:118 */
            if ((1<<i) & inputfds2) {
                user = fdtoplayer[i];                        /* bed.c:120 */
                task.inp = player[user].inp;
                ...
                xanadu(&task);                               /* bed.c:128 */
                ...
                ntaskorcommand++;
            }
        }
    }
    ...
}
```

`select()` [bed.c:111] returns a single bitmask of all ready file descriptors. The outer `for` loop [bed.c:118] then iterates over every bit in that bitmask sequentially, calling `xanadu(&task)` [bed.c:128] for each ready session. Because this is a single-threaded C process — no `fork`, no `pthread_create`, no coroutines anywhere in the codebase — `xanadu()` for session A must **return** before the `for` loop increments `i` and tests whether session B's fd is ready.

---

### 2. `xanadu()` Dispatches Synchronously (`bed.c:153–172`)

```c
int xanadu(typetask *taskptr)
{
    ...
    } else if (getrequest(taskptr, &request)) {
        (*requestfns[request])(taskptr);    /* bed.c:162 — calls insert() */
        sendresultoutput(taskptr);          /* bed.c:163 */
        ...
    }
    tfree(taskptr);                         /* bed.c:168 */
    ...
}
```

The function-pointer dispatch at [bed.c:162] calls the INSERT handler (`insert()` in `fns.c`), waits for it to return, then sends the result and frees task memory. Nothing yields control between these steps.

---

### 3. `insert()` Calls All Three Sub-Steps Synchronously (`fns.c:84–98`)

```c
void insert(typetask *taskptr)
{
    (void) getinsert(taskptr, &docisa, &vsa, &textset);   /* fns.c:90 */
    putinsert(taskptr);                                    /* fns.c:91 */
    if (!doinsert(taskptr, &docisa, &vsa, textset))       /* fns.c:92 */
        ...
}
```

`doinsert()` is a plain synchronous call.

---

### 4. `doinsert()` Executes All Three Phases In One C Stack Frame (`do1.c:87–123`)

```c
bool doinsert(typetask *taskptr, typeisa *docisaptr, tumbler *vsaptr, typetextset textset)
{
    makehint(DOCUMENT, ATOM, TEXTATOM, docisaptr, &hint);  /* do1.c:117 */
    ret = (inserttextingranf(taskptr, granf, &hint, textset, &ispanset)  /* do1.c:118 — granfilade append */
        && docopy(taskptr, docisaptr, vsaptr, ispanset)                  /* do1.c:119 — POOM + spanfilade */
    );
    return(ret);
}
```

- **Granfilade append**: `inserttextingranf()` [do1.c:118] allocates a new ISA address and writes the content crum into the granfilade tree (via `insertseq()` / `findisatoinsertmolecule()` in `granf2.c` and `insert.c`).
- **POOM update + DOCISPAN creation**: `docopy()` [do1.c:119] contains both sub-steps:

```c
bool docopy(typetask *taskptr, typeisa *docisaptr, tumbler *vsaptr, typespecset specset)
{
    ...
    && insertpm(taskptr, docisaptr, docorgl, vsaptr, ispanset)          /* do1.c:60 — POOM update */
    && insertspanf(taskptr, spanf, docisaptr, ispanset, DOCISPAN)       /* do1.c:62 — spanfilade DOCISPAN */
    ...
}
```

Both `insertpm()` [do1.c:60] and `insertspanf()` [do1.c:62] are ordinary synchronous function calls. `insertpm()` eventually calls `insertnd()` in `insertnd.c` (which dispatches to `makegappm` + `doinsertnd` + `recombine` for the POOM tree [insertnd.c:54–76]). `insertspanf()` does the same for the span filade. None of these calls ever yield, block on I/O, or invoke a scheduler.

---

### 5. Queues and Task Memory Are Not Dispatch Mechanisms

`queues.c` implements plain doubly-linked list manipulation (no thread signaling, no work queues). `task.c`'s `talloc`/`tfree` is a simple per-request slab allocator that is freed at the end of `xanadu()` [bed.c:168]. Neither introduces any asynchrony.

---

### Conclusion

**The sub-steps cannot interleave.** The udanax-green backend is a single-threaded process. When two sessions both become ready in the same `select()` call, the event loop processes them in fd-number order via a sequential `for` loop [bed.c:118]. For each session, `xanadu()` [bed.c:128] is called and must return before the next session is touched. Inside `xanadu()`, the entire INSERT — `inserttextingranf()` (granfilade append) → `insertpm()` (POOM update) → `insertspanf(DOCISPAN)` (spanfilade DOCISPAN creation) — executes atomically on the C call stack. Session A's INSERT is 100% complete before session B's INSERT begins.

---

## Question 12 [gregory]

> If two users each own different documents that share I-addresses via transclusion, and both perform INSERT simultaneously into their respective documents, does `findisatoinsertmolecule` ever return the same I-address for both allocations — given that each document has an independent I-address range under its own document orgl?

### Gregory's Answer

## KB Synthesis

No. Two different documents can never receive the same I-address from `findisatoinsertmolecule`, regardless of whether they share I-addresses via transclusion. There are two independent reasons.

## 1. Per-document address namespaces are structurally disjoint

`findisatoinsertmolecule` computes an `upperbound` derived from the calling document's hint ISA before calling `findpreviousisagr`. From [SS-ADDRESS-SPACE] Finding 0065:

```
tumblerincrement(&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound)
```

For TEXTATOM (atomtype=1), this produces an upper bound scoped to the document's own content subspace. The address layout from [SS-ADDRESS-SPACE] Finding 0077 makes this explicit:

```
1.1.0.1.0.1.3.0.1.1    ← content I-address for text in doc 1.1.0.1.0.1
1.1.0.1.0.2.3.0.1.1    ← content I-address for text in doc 1.1.0.1.0.2
```

Since two users own different documents, their documents have different ISAs ([INV-GLOBAL-ADDRESS-UNIQUENESS]). The `upperbound` for each document's allocation search falls in a different region of the granfilade tree. The search ranges are non-overlapping by tumbler prefix structure, so `findpreviousisagr` for doc A never returns an address that could be incremented into doc B's content subrange, and vice versa.

The transclusion relationship is irrelevant here: transclusion shares *existing* I-addresses by copying V→I mappings into the target POOM ([ST-VCOPY], [FC-INSERT-IADDR]) — it does not co-mingle the allocation namespaces of the source and target documents. The shared I-addresses remain permanently attributed to the document that originally allocated them ([INV-IADDR-PROVENANCE]).

## 2. Concurrent allocation is structurally impossible

Even setting aside the namespace separation, "simultaneous" INSERT is precluded by the event loop architecture ([INV-ATOMICITY], [INV-SEQUENTIAL-DISPATCH] — Finding 0042). The `bed.c` select() loop processes each operation atomically to completion before the next begins. Two INSERT operations from different sessions cannot interleave at any point in their execution, including the `findpreviousisagr` → `tumblerincrement` allocation sequence.

## Summary

The structural guarantee flows from: (a) each document's content I-addresses are allocated within a subrange of the global granfilade keyed to that document's ISA [SS-ADDRESS-SPACE] Finding 0077, (b) different documents have globally unique ISAs [INV-GLOBAL-ADDRESS-UNIQUENESS], and (c) allocation is bounded by `upperbound` derived from the document's own ISA [SS-ADDRESS-ALLOC] Finding 0065. Even if concurrent execution were possible, the disjoint search bounds would prevent collision. The actual single-threaded event loop ([INV-SEQUENTIAL-DISPATCH]) provides an additional, orthogonal guarantee.

## Code Exploration

I now have everything needed for a complete answer.

---

## Analysis: Can `findisatoinsertmolecule` Return the Same I-Address for Two Different Documents?

**Short answer: No.** Two independent protections prevent it — one architectural (serialization), one structural (namespace disjointness). Neither requires the other, and both are confirmed by direct code reading.

---

### 1. The Backend Is Single-Threaded — "Simultaneous" Is an Illusion

The multi-user backend runs a single-threaded `select()`-based event loop [`bed.c:103–143`]:

```c
for (;;) {
    /* ... */
    if (select(nfds+1, &inputfds2, 0, 0, &timeout) < 0) { … }
    else {
        for (i = 0; i <= nfds; i++) {
            if ((1<<i) & inputfds2) {
                user = fdtoplayer[i];
                /* ... */
                xanadu(&task);   // processes ONE complete request
            }
        }
    }
```

`xanadu()` at `bed.c:153` dispatches to the request handler and returns only when the full operation completes. There is no threading, no coroutine interleaving. User 1's INSERT runs to completion before User 2's INSERT begins. The premise of true simultaneous execution is false at the process level.

---

### 2. The Single Global `granf`, But Document-ISA-Scoped Allocation

`granf` is a single global granfilade for the entire process, declared at `corediskout.c:21`:

```c
typegranf granf;
```

and declared extern in `xanadu.h:14`:

```c
extern typegranf granf;
```

Every INSERT by every user writes into this one tree. But the address search is scoped by the target document's ISA.

---

### 3. The Full Call Chain for INSERT

```
fns.c:insert()              [fns.c:84]
  → do1.c:doinsert()        [do1.c:87]
      makehint(DOCUMENT, ATOM, TEXTATOM, docisaptr, &hint)   [do1.c:117]
      inserttextingranf(taskptr, granf, &hint, textset, ...)  [do1.c:118]
        → granf2.c:inserttextgr()                            [granf2.c:83]
            findisatoinsertgr(fullcrumptr, hintptr, &lsa)    [granf2.c:92]
              → findisatoinsertmolecule()                    [granf2.c:142]
            insertseq(...) — actually mutates the tree       [granf2.c:99]
```

`makehint` at `do2.c:78–84`:

```c
int makehint(INT typeabove, INT typebelow, INT typeofatom, typeisa *isaptr, typehint *hintptr)
{
    hintptr->supertype = typeabove;   // DOCUMENT
    hintptr->subtype = typebelow;     // ATOM
    hintptr->atomtype = typeofatom;   // TEXTATOM = 1
    movetumbler(isaptr, &hintptr->hintisa);  // hintisa = *docisaptr
}
```

The hint carries the target document's ISA directly as `hintisa`.

---

### 4. `findisatoinsertmolecule` Computes an Upper Bound Scoped to `hintisa`

At `granf2.c:158–181`:

```c
static int findisatoinsertmolecule(typecuc *fullcrumptr, typehint *hintptr, typeisa *isaptr)
{
    typeisa upperbound, lowerbound;

    tumblerincrement(&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound);
    //                ^^^^^^^^^^^^^^^^^                                        ^
    //                = docisaptr                                  = TEXTATOM+1 = 2
    // upperbound = docisa with .0.0.2 appended at positions [idx+2]

    clear(&lowerbound, sizeof(lowerbound));
    findpreviousisagr((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);
    // Searches global granf for the highest ISA strictly below upperbound
```

`tumblerincrement` at `tumble.c:599–622`:

```c
int tumblerincrement(tumbler *aptr, INT rightshift, INT bint, tumbler *cptr)
{
    /* ... */
    for (idx = NPLACES; aptr->mantissa[--idx] == 0 && idx > 0;);
    // idx = index of last non-zero digit in docisa
    cptr->mantissa[idx + rightshift] += bint;
    // appends bint (=2) at position idx+2, i.e. docisa.0.0.2
```

So `upperbound` is `docisa` with `.0.0.2` appended — it is entirely within the `docisa`-rooted subtree of the granfilade.

The subsequent search `findpreviousisagr(granf, &upperbound, &lowerbound)` finds the highest existing ISA below this document-specific `upperbound`. The returned `lowerbound` is necessarily ≤ `upperbound`, hence within `docisa`'s subtree.

The final ISA computation (lines `165–176`) either increments `lowerbound` or starts from `hintisa` itself — in both cases producing an address within `docisa`'s sub-range.

---

### 5. Different Documents Have Disjoint ISA Sub-ranges

The `docisaptr` for each document is unique per user per document. Documents live under different account tumblers (e.g., User 1's account at `1.1.0`, User 2's account at `1.2.0`). Their documents are at addresses like:

- User 1, Doc A: `d1 = 1.1.0.1.0.1`
- User 2, Doc B: `d2 = 1.2.0.1.0.1`

From these:

- `d1`'s text upper bound: `d1.0.0.2` (lives entirely under `1.1.0.1.0.1`)
- `d2`'s text upper bound: `d2.0.0.2` (lives entirely under `1.2.0.1.0.1`)

Because `d1 ≠ d2`, these ISA sub-ranges are **structurally disjoint**. They share no overlap in the global granfilade tree. `findpreviousisagr` searching below `d1.0.0.2` cannot return any ISA from `d2`'s range, and vice versa.

---

### 6. Transclusion Does Not Affect Allocation

When Document B transcluded content from Document A, it borrowed Document A's existing I-spans (immutable content atoms already recorded in `granf` under `d1`). Those atoms are referenced through Document B's virtual address space (the orgl / POOM), but they live at their original `d1`-derived I-addresses. When User 2 now inserts new text into Document B, `makehint` at `do1.c:117` sets `hintisa = d2` (Document B's address). All new allocations go into `d2`'s sub-range, not `d1`'s. The transcluded content is read-only reference; it is not in the range from which new allocations are drawn.

---

### Conclusion

`findisatoinsertmolecule` cannot return the same I-address for two distinct documents' insertions for two independent reasons:

1. **Serialization** (`bed.c:118–141`): The backend's `select()` event loop processes one complete request at a time. There is no true concurrency. The second INSERT begins only after the first has called `insertseq()` and committed its result to the granfilade tree.

2. **Namespace disjointness** (`granf2.c:162–164`): Even under hypothetical concurrency, the upper bound passed to `findpreviousisagr` is `docisa.0.0.2` — derived exclusively from the target document's ISA. Two different documents at addresses `d1` and `d2` produce upper bounds in different, non-overlapping subtrees of the global `granf`. The newly allocated ISA is always confined to the sub-range of its own document.

The question's assumption — "each document has an independent I-address range under its own document orgl" — is correct and directly verified by `granf2.c:162` and `tumblerincrement` at `tumble.c:621`. This range independence is structural: it is encoded in the tumbler arithmetic that defines upper bounds, not merely a policy enforced elsewhere.

---

## Question 13 [gregory]

> When session A is executing a `findlinksfromtothreesp` spanfilade traversal and session B completes an INSERT that adds a new DOCISPAN entry to the same spanfilade, can session A see a partially-written spanfilade node — or does the run-to-completion guarantee mean session A's traversal either fully precedes or fully follows session B's write?

### Gregory's Answer

## KB Synthesis

The run-to-completion guarantee means the two operations are strictly serialized — session A's traversal either **fully precedes** or **fully follows** session B's INSERT. A partially-written spanfilade node cannot be observed.

## Why

[INV-ATOMICITY] (Finding 0042) establishes the mechanism: the `bed.c` event loop dispatches each FEBE operation via a single blocking call to `xanadu(&task)`, which executes the entire operation — request parsing, all state mutations, response sending, and memory cleanup — before returning to `select()`. No preemption, no threads, no state-modifying signal handlers exist.

[INV-SEQUENTIAL-DISPATCH] (Finding 0042) makes this explicit for the multi-session case: even when multiple frontend file descriptors are simultaneously ready in `select()`'s result, the loop iterates over them sequentially. Session i's operation runs to completion before session i+1's operation begins.

Applied to the question:

- `findlinksfromtothreesp` is the implementation of FINDLINKSFROMTOTHREE. It executes as a single `requestfns[request]` invocation inside `xanadu()`.
- Session B's INSERT also executes as a single `xanadu()` invocation — allocating I-addresses, writing to granf, writing the new DOCISPAN entry to spanf, and updating the POOM all as one uninterruptible unit [ST-INSERT].

These two `xanadu()` calls cannot interleave. The event loop serializes them. Session A's traversal sees either the spanfilade state *before* session B's DOCISPAN write (if A ran first) or *after* it (if B ran first). There is no intermediate state where the spanfilade node is partially written.

[PRE-CONCURRENT-INSERT] (Finding 0041) confirms the concern is real at the B-tree pointer level — concurrent unsynchronized insertions would be unsafe — but also confirms that serialization is required and the single-threaded event loop provides it. The pointer-level unsafety is therefore never realized.

## Code Exploration

I now have everything I need. Here is the complete answer:

---

## Concurrency Analysis: `findlinksfromtothreesp` vs. Concurrent INSERT in udanax-green

### Short Answer

**Session A can never see a partially-written spanfilade node from session B.** The run-to-completion guarantee is absolute and structurally enforced by the backend's single-threaded event loop. Either session A's traversal runs entirely before session B's write, or entirely after — interleaving at any granularity, including at the node level, is architecturally impossible.

---

### 1. The Event Loop: One Request at a Time

The entire concurrency model lives in `bed.c`. The `main()` function runs a single `select()` loop:

```c
// bed.c:103-149
for (;;) {
    ...
    inputfds2 = inputfds;
    if (select(nfds+1, &inputfds2, 0, 0, &timeout) < 0) { ... }
    else {
        for (i = 0; i <= nfds; i++) {
            if ((1<<i) & inputfds2) {
                user = fdtoplayer[i];
                task.inp  = player[user].inp;
                task.outp = player[user].outp;
                ...
                xanadu(&task);   // ← ONE request, runs to completion
                ...
            }
        }
    }
    leave(player, &n_players);
    new_players(player, &n_players, FALSE, &task);
}
```

**`xanadu()` processes exactly one request and does not return until it is finished** [bed.c:153-172]:

```c
int xanadu(typetask *taskptr)
{
    ...
    if (getrequest(taskptr, &request)) {
        (*requestfns[request])(taskptr);   // dispatch and run
        sendresultoutput(taskptr);         // send response
        ...
    }
    tfree(taskptr);                        // free task memory
}
```

The outer `for(;;)` loop does not call `select()` again until `xanadu()` returns. While session A's `findlinksfromtothreesp` is executing, session B's request bytes sit unread in the OS socket buffer. The backend does not see them until session A's request completes and control returns to the `main()` loop for the next `select()`.

---

### 2. Session A: The Traversal Call Chain (Fully In-Memory)

Starting from the FEBE dispatch:

| Function | File | Line |
|---|---|---|
| `findlinksfromtothree()` | `fns.c` | 189 |
| `dofindlinksfromtothree()` | `do1.c` | 348–353 |
| `findlinksfromtothreesp()` | `spanf1.c` | 56–103 |
| `sporglset2linkset()` | `sporgl.c` | 222–237 |
| `sporglset2linksetinrange()` | `sporgl.c` | 239–268 |
| `retrieverestricted()` | `retrie.c` | 56–85 |
| `retrieveinarea()` | `retrie.c` | 87–110 |
| `findcbcinarea2d()` | `retrie.c` | 229–268 |

The leaf function, `findcbcinarea2d()` [retrie.c:229-268], is a pure recursive in-memory tree walk — no disk I/O, no blocking, no external calls:

```c
// retrie.c:252-265
for (; crumptr; crumptr = getrightbro (crumptr)) {
    if (!crumqualifies2d (...)) { continue; }
    if (crumptr->height != 0) {
        dspadd (offsetptr, &crumptr->cdsp, &localoffset, ...);
        findcbcinarea2d (findleftson ((typecuc*)crumptr), &localoffset, ...); // recurse
    } else {
        context = makecontextfromcbc ((typecbc*)crumptr, (typewid*)offsetptr);
        incontextlistnd (headptr, context, index1);
    }
}
```

No point in this traversal touches a socket, calls `select()`, blocks, or yields.

---

### 3. Session B: The INSERT Call Chain (Also Fully In-Memory)

```c
// fns.c:84-98  insert()
getinsert(...);
putinsert(...);           // ← response sent BEFORE doinsert runs (optimistic protocol)
doinsert(...);            // actual mutation
```

`doinsert()` [do1.c:87-123] calls `inserttextingranf()` followed by `docopy()` [do1.c:45-65], which calls:

```c
// do1.c:62
insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN)
```

`insertspanf()` [spanf1.c:15-54] iterates over the span set and for each entry calls:

```c
// spanf1.c:51
insertnd(taskptr, (typecuc*)spanfptr, &crumorigin, &crumwidth, &linfo, SPANRANGE);
```

`insertnd()` [insertnd.c:15-...] calls `doinsertnd()` and `recombine()` — all in-memory enfilade manipulations with no I/O, no blocking.

---

### 4. Confirming the Absence of Yield Points

A grep for any concurrency primitive in the backend source:

```
backend/bed.c:111      select(nfds+1, ...)     ← outer loop, outside xanadu()
backend/socketbe.c:74  select(32, ...)          ← new-player polling, also outside
```

There are **no** calls to `pthread_*`, `fork`, `sleep`, `yield`, or any other threading or cooperative-yielding primitive. The only `select()` calls are in `bed.c:111` (the outer loop) and `socketbe.c:74` (new-player detection) — neither is reachable from inside a running request handler.

---

### 5. Signal Handlers Cannot Interrupt Mid-Request

`bed.c:70-73` installs four signal handlers:

```c
signal(SIGPIPE, crash);       // terminates process entirely
signal(SIGHUP,  crash);       // terminates process entirely
signal(SIGXCPU, SIG_IGN);     // ignored
signal(SIGINT,  flagquitting); // sets quitafteruser = TRUE
```

`flagquitting()` [bed.c:175-188] only sets a flag:

```c
void flagquitting() {
    signal(SIGINT, SIG_IGN);
    if (mightbeblocked) { ... exit(0); }
    else
        quitafteruser = TRUE;   // flag checked AFTER xanadu() returns
}
```

That flag is checked at `bed.c:129-137` only after `xanadu()` has returned. Even SIGINT cannot interrupt a request mid-execution.

---

### 6. Summary

The backend is a **single-process, single-threaded, cooperative event loop** with no preemption. The invariant is:

> The call to `xanadu()` [bed.c:128] for session A's request runs completely to completion — including the entire `findcbcinarea2d()` spanfilade traversal — before the `main()` loop calls `select()` again, and therefore before session B's INSERT request is even read from the socket.

Session A's traversal and session B's write are strictly serialized. Session A either sees the spanfilade as it was before session B's INSERT, or (if session B ran first) as it was after. Partial visibility of an in-progress write is not possible. The run-to-completion guarantee is total.

---

## Question 14 [gregory]

> Does the grim reaper's cache eviction (`grimlyreap`) hold any lock or guard that prevents a second session's operation from reading a half-written disk block if eviction is triggered mid-operation — or is this impossible because the event loop is single-threaded and eviction completes synchronously within the triggering operation?

### Gregory's Answer

## KB Synthesis

The race condition you describe is **structurally impossible** — no locking or guard is needed because the event loop eliminates the possibility.

## Reasoning

**The event loop is run-to-completion single-threaded** [INV-ATOMICITY, INV-SEQUENTIAL-DISPATCH]:

> The `xanadu(&task)` call executes the entire operation — request parsing, state mutation, response sending, and memory cleanup — before returning to `select()`. There are no threads, no state-modifying signal handlers, and no preemption.

The grim reaper is triggered by `ealloc` on allocation failure [SS-CACHE-MECHANISM]:

```
ealloc (credel.c:54-76) → grimlyreap() → scans grim reaper list → orglwrite() → free
```

This entire sequence runs **synchronously within the current `xanadu()` invocation**, which means:

1. Eviction begins mid-operation (e.g., mid-INSERT when a new crum cannot be allocated)
2. `grimlyreap()` writes modified crums to disk and frees them from memory
3. The current operation continues
4. Only after `xanadu()` returns does `select()` run again and potentially dispatch a second session's request

No second session's operation can interleave at step 2 because `select()` is not re-entered until step 4. The single-threaded model provides mutual exclusion over the entire operation, including any internally-triggered evictions.

## The Only Related Concern

The real durability hazard is **crash-during-write**, not inter-session races [EC-CRASH-MID-WRITE]:

> `subtreewriterecurs` writes modified subtrees bottom-up. If a crash occurs mid-write (after writing leaf/middle nodes but before updating the root), the on-disk enfilade enters an inconsistent state.

But this is a crash-safety problem, not a concurrency problem. It requires no lock because there is no concurrent reader — only the single active operation and the OS write buffer.

## Summary

The grim reaper holds no lock and needs none. The single-threaded run-to-completion event loop [INV-SEQUENTIAL-DISPATCH] is the guard: eviction completes synchronously within the operation that triggered it, and no other session's code runs until that operation returns to `select()`. The architecture eliminates the race by construction [INV-ATOMICITY].

## Code Exploration

I now have all the evidence needed. Here is the full answer.

---

## `grimlyreap` and the Absence of Inter-Session Disk Guards

### Short answer

`grimlyreap` holds **no lock or guard that protects against a second session reading a half-written disk block**. It does not need one. The event loop is strictly single-threaded and processes one full request to completion before examining any other session's socket. Eviction always completes synchronously within the triggering operation. The only guards present are intra-call-stack reentrancy protections, not inter-session protections.

---

### 1. The event loop is single-threaded and non-preemptive

`bed.c:103–143` is the outer dispatch loop:

```c
for (;;) {
    ...
    if (select(nfds+1, &inputfds2, 0, 0, &timeout) < 0) {
        ...
    } else {
        for (i = 0; i <= nfds; i++) {
            if ((1<<i) & inputfds2) {
                user = fdtoplayer[i];
                task.inp = player[user].inp;
                ...
                xanadu(&task);     // [bed.c:128]
            }
        }
    }
    ...
}
```

`xanadu()` [bed.c:153–172] calls the request handler, waits for it to return, then sends the result. Control never returns to the `select()` loop — and thus no other session's fd is ever examined — until `xanadu()` has returned. There is no threading, no coroutine yield, and no signal handler that can dispatch another session mid-request (SIGPIPE calls `crash()`, SIGINT only sets `quitafteruser = TRUE` [bed.c:187], neither of which dispatches a second user's request).

---

### 2. `grimlyreap` is called only from `ealloc`, deep on the current request's call stack

`ealloc()` [credel.c:54–77] is the custom slab allocator. When `falloc()` returns NULL and `grimreaper != NULL`, it calls `grimlyreap()`:

```c
// credel.c:70-75
if (grimreaper == NULL){
    xgrabmorecore();
    continue;
}
grimlyreap();
```

This executes synchronously, without yielding, on the call stack of whatever request handler caused the allocation pressure.

---

### 3. `grimlyreap` has no inter-session guards — only an intra-call-stack reentrancy flag

`grimlyreap` [credel.c:106–162]:

```c
ingrimreaper = TRUE;   // credel.c:112
...
// walks grimreaper ring, calls reap() on first reapable crum
...
ingrimreaper = FALSE;  // credel.c:161
```

`ingrimreaper` is checked by `falloc()` [alloc.c:106–114]:

```c
if(ingrimreaper){
    gerror("falloc called from under grimreaper\n");
}
```

This is a **reentrancy guard**: it prevents `falloc()` from being called recursively _while a reap is in progress on the same call stack_. It is not a mutex, semaphore, or any construct that could block or coordinate with another session. It is a single global boolean.

---

### 4. What actually happens during a reap: synchronous disk write

When `grimlyreap` finds a reapable crum, it calls `reap()` [credel.c:292–330]:

- Apex crum path: `orglwrite((typecbc*)temp)` [credel.c:309] → `corediskout.c:281`
- Non-apex path: `subtreewrite(temp)` [credel.c:329] → `corediskout.c:414`

Both paths ultimately call `writeloaf()` → `actuallywriteloaf()` [disk.c:300–338]:

```c
// disk.c:328-333
if (lseek(enffiledes, (long)diskblocknumber*NUMBYTESINLOAF, 0) < 0) {
    gerror("lseek failed\n");
}
if (write(enffiledes, (char*)loafptr, sizeof(*loafptr)) <= 0) {
    qerror("write\n");
}
```

This is a single blocking `write()` call to the `enf.enf` file. The C process does not return from it until the kernel has accepted the full block. The write is atomic at the application level: no other C code executes between the `lseek` and the `write` completing.

---

### 5. The `RESERVED` age flag — a second intra-call-stack guard

There is one more guarding mechanism inside `orglwritepart2()` [corediskout.c:300–356]:

```c
// corediskout.c:326
reserve((typecorecrum*)orglcbcptr);
...
subtreewriterecurs(taskptr, orglptr);
```

`reserve()` [credel.c:364–379] sets `ptr->age = RESERVED`. `isreapable()` [credel.c:176] returns FALSE for any crum with `age == RESERVED`:

```c
if(localreaper->age < OLD || localreaper->age == RESERVED){
    *fuckinap = 1;
    return(FALSE);
}
```

This prevents `grimlyreap()` from evicting a crum that is currently being serialized to disk, in the scenario where `subtreewriterecurs()` itself triggers a memory allocation (and therefore another `ealloc()` → `grimlyreap()` call). This is again purely about reentrancy within the same call stack, not inter-session safety.

---

### 6. The disk-side cache (`cashedisk.c`) adds no locking either

`cashedisk.c` is a simple 301-slot random-replacement hash:

```c
// cashedisk.c:56-65
INT blockisinhash(INT blocknumber) {
    INT temp;
    temp = hash(blocknumber);
    if(xhashtable[temp].blocknumber == blocknumber){
        return temp;
    } else {
        return 0;
    }
}
```

There are no locks here either. `writethruhash()` is called by `actuallywriteloaf()` (though in the current code the call is commented out — `/**writethruhash(loafptr,diskblocknumber);*/` at disk.c:305). No second session can observe a partial cache state for the same reason: single-threaded execution.

---

### Conclusion

The correct hypothesis is the second: **the absence of inter-session guards is not a hazard — it is an architectural consequence of the single-threaded event loop**. The full call chain is:

```
select() returns one fd
→ xanadu(&task)
  → (*requestfns[request])(taskptr)     [bed.c:162]
    → ... → ealloc()                    [credel.c:54]
      → grimlyreap()                    [credel.c:75]
        → reap()                        [credel.c:148]
          → subtreewrite() / orglwrite()  [credel.c:309,329]
            → writeloaf()               [corediskout.c:545]
              → actuallywriteloaf()     [disk.c:300]
                → lseek() + write()     [disk.c:328-332]  ← completes
← select() loop iterates, next fd checked
```

No second session's request is ever dispatched between the `lseek` and `write`, or at any point during `grimlyreap`. The two actual guards in the code — `ingrimreaper` [credel.c:112, alloc.c:106] and `RESERVED` age [credel.c:326, reap.h:11] — both protect only against recursive invocation within a single request's call stack, not against concurrent sessions.

---

## Question 15 [gregory]

> When session A has document D open with WRITEBERT and session B calls `find_links` with a specset that resolves to I-addresses shared with document D, does session B's spanfilade search require any BERT check on document D, or does the global spanfilade bypass per-document access control entirely?

### Gregory's Answer

## KB Synthesis

Session B's `find_links` call requires **no BERT check on document D**. The spanfilade is a global index accessed entirely outside the per-document BERT gate.

## Why no BERT check applies

**BERT checks happen through `findorgl`**. Every content operation that touches a specific document's orgl — INSERT, DELETEVSPAN, REARRANGE, RETRIEVE — calls `findorgl(taskptr, granf, docisaptr, &docorgl, access_type)`, which internally invokes `checkforopen()` to verify BERT state [SS-BERT]. This is the sole mechanism by which BERT access control is enforced.

**`find_links` routes through the spanfilade, not `findorgl`**. `dofindlinksfromtothree()` at `do1.c:386-391` delegates entirely to `findlinksfromtothreesp()`, which searches the spanfilade by I-address intersection [SS-SPANF-OPERATIONS, FC-CONTENT-SPANF-ISOLATION]. The call chain never touches a document orgl, so no `findorgl` call — and thus no BERT check — occurs for document D or any other document in the link index.

**The spanfilade is a write-once global index**. It accumulates I-address → link mappings from all documents without per-document scoping. Searching it is an unconditional read of global state [INV-SPANF-WRITE-ONLY]. The orgl-dimension filter that was meant to scope results by document is itself disabled by a `TRUE||` guard, making all searches globally unscoped in practice [EC-FIND-LINKS-GLOBAL].

**Finding 0027 confirms this directly**: "Operations that work through I-address lookup (e.g., `find_links` via span-f) do NOT require the referenced document to be open" [SS-DOCUMENT-LIFECYCLE]. Document D doesn't even need to be open, let alone BERT-checked.

## The separation is architectural

The dual-enfilade design explicitly isolates these access paths [SS-DUAL-ENFILADE]:

- **granfilade** (content): access controlled per-document via `findorgl` + BERT
- **spanfilade** (link index): global, no per-document access control

Session A's WRITEBERT on document D prevents other sessions from writing to D's content via the granfilade path. It has no effect on the spanfilade search path, which operates in an entirely separate subsystem.

## Caveat: the input specset conversion

If session B's input specset references V-spans in a document session B already has open, that V-to-I conversion goes through `findorgl` for *session B's own open documents* — not document D. The I-addresses found in the spanfilade may have *originated* from document D (e.g., D's content was transcluded into session B's document), but the spanfilade search itself is indifferent to which document currently holds WRITEBERT on those I-addresses [INT-BERT-FEBE].

In summary: BERT is a cooperative protocol for coordinating write access to document content [INT-BERT-FEBE]. The spanfilade search is structurally outside that coordination domain.

## Code Exploration

I now have the complete call chain. Here is the full answer.

---

## `find_links` and BERT: The Global Spanfilade Bypasses Per-Document Access Control Entirely

### Answer

**Session B's `find_links` performs zero BERT checks on document D.** The global spanfilade is searched without any per-document access control, regardless of whether another session holds a WRITEBERT on any document whose I-addresses overlap with the query.

---

### Complete Call Chain Trace

**Step 1 — FEBE handler: `fns.c:189-202`**

```c
void findlinksfromtothree(typetask *taskptr) {
    ...
    getfindlinksfromtothree(taskptr, &fromvspecset, &tovspecset, &threevspecset, &homeset)
    && dofindlinksfromtothree(taskptr, fromvspecset, tovspecset, threevspecset,
                              (typeispan*)NULL/*homeset*/, &linkset)
    ...
}
```

Note that `homeset` — the per-document filter — is **explicitly nulled out** with `(typeispan*)NULL` even though it was received from the client.

**Step 2 — Thin wrapper: `do1.c:348-353`**

```c
bool dofindlinksfromtothree(typetask *taskptr, typespecset fromvspecset, ...) {
    return findlinksfromtothreesp(taskptr, spanf, fromvspecset, tovspecset,
                                  threevspecset, orglrangeptr, linksetptr);
}
```

No BERT type passed here. The global `spanf` is handed directly in.

**Step 3 — Specset → Sporglset with `NOBERTREQUIRED`: `spanf1.c:70-75`**

```c
if (fromvspecset)
    specset2sporglset(taskptr, fromvspecset, &fromsporglset, NOBERTREQUIRED);
if (tovspecset)
    specset2sporglset(taskptr, tovspecset, &tosporglset, NOBERTREQUIRED);
if (threevspecset)
    specset2sporglset(taskptr, threevspecset, &threesporglset, NOBERTREQUIRED);
```

The constant `NOBERTREQUIRED` (= 0, defined at `common.h:165`) is explicitly passed for all three endpoint sets.

**Step 4 — `specset2sporglset` → `vspanset2sporglset`: `sporgl.c:14-33`**

For each `VSPECID` spec in the specset (i.e., each V-address pointing into some document including document D):

```c
sporglsetptr = vspanset2sporglset(taskptr, &((typevspec*)specset)->docisa,
                                   ((typevspec*)specset)->vspanset,
                                   sporglsetptr, type);   // type = NOBERTREQUIRED
```

**Step 5 — `vspanset2sporglset` calls `findorgl` with `NOBERTREQUIRED`: `sporgl.c:44`**

```c
if (!findorgl(taskptr, granf, docisa, &orgl, type)) {   // type = NOBERTREQUIRED
    return(NULL);
}
```

This must open document D's orgl (its POOM tree) to perform V→I address translation.

**Step 6 — `findorgl` calls `checkforopen`: `granf1.c:22`**

```c
if ((temp = checkforopen(isaptr, type, user)) <= 0) {   // type = NOBERTREQUIRED
    ...
    return FALSE;
}
```

**Step 7 — `checkforopen` immediately returns on `NOBERTREQUIRED`: `bert.c:59-61`**

```c
if (type == NOBERTREQUIRED) {
    return 1;   /* Random > 0 */
}
```

The function returns **before scanning the bert table at all.** It does not check:
- Whether document D is open by any connection
- Whether session A holds WRITEBERT on document D
- Whether document D is owned by the current user

The entire hash table scan (`berttable[hashoftumbler(tp)]` loop at `bert.c:63-79`) is skipped. The `foundnonread` logic that would return `-1` for a WRITEBERT held by another connection is never reached.

**Step 8 — Spanfilade search: `sporgl.c:239-269` → `retrie.c:56-85`**

After converting V-addresses to I-addresses (sporgls), `sporglset2linksetinrange` calls:

```c
context = retrieverestricted(spanfptr, (typespan*)sporglset, SPANRANGE,
                              &range, ORGLRANGE, (typeisa*)infoptr);
```

where `infoptr` is **always NULL** due to the explicitly disabled version-tracking at `sporgl.c:251-255`:

```c
if (FALSE/*trying to kluge links followable thru versions */
    && ((typeitemheader*)sporglset)->itemid == SPORGLID) {
    infoptr = &linfo;
    ...
} else
    infoptr = NULL;
```

`retrieverestricted` → `retrieveinarea` → `findcbcinarea2d` (all in `retrie.c`) is a pure tree traversal with no BERT calls anywhere in the path.

---

### Summary Table

| Step | Function | File | BERT Check? |
|------|----------|------|-------------|
| V-spec → orgl | `findorgl` | `granf1.c:22` | `checkforopen(…, NOBERTREQUIRED, …)` — immediately returns 1 [`bert.c:59`] |
| orgl → I-spans | `vspanset2ispanset` | `orglinks.c` | No BERT call |
| Spanfilade query | `retrieverestricted` | `retrie.c:56` | No BERT call |
| Tree traversal | `findcbcinarea2d` | `retrie.c:229` | No BERT call |

---

### Architectural Explanation

This design is intentional. The spanfilade is a **global permascroll-indexed index** — its keys are I-addresses (immutable content identity), not V-addresses (mutable document addresses). Since I-addresses in the permascroll never change, there is no data consistency problem from session A holding WRITEBERT on document D while session B queries for links that reference D's content. Session A's WRITEBERT only gates mutation of D's POOM tree (V-address structure), not the immutability of D's underlying I-addresses already registered in the global spanfilade.

**Session B's `find_links` will find all links referencing document D's I-addresses regardless of any BERT state on document D, any other session's WRITEBERT, or even whether document D has been opened at all.**

---

## Question 16 [gregory]

> If session A performs CREATENEWVERSION on a document that session B currently has open with WRITEBERT, does the version creation read session B's in-progress POOM state (including any uncommitted INSERT shifts), or does it read from disk — and does `checkforopen` block the version creation if the source document is write-locked by another session?

### Gregory's Answer

## KB Synthesis

Two separate questions here — I'll address each.

---

## 1. Does CREATENEWVERSION see session B's "in-progress" POOM state?

There is no such state. The single-threaded event loop processes each FEBE operation to completion before the next one begins [INV-SEQUENTIAL-DISPATCH, INV-ATOMICITY]. Session B's INSERTs, once dispatched, run entirely — `inserttextingranf`, `insertpm` (POOM update), `insertspanf` (DOCISPAN), and all internal tree rebalancing — before `select()` returns and session A's CREATENEWVERSION is dispatched.

When CREATENEWVERSION runs, the in-memory POOM reflects every operation session B has completed. There is no partial or uncommitted INSERT shift visible to another operation, because there is no interleaving possible.

The read is from in-memory cache, not from disk [SS-CACHE-MECHANISM]. The grim reaper may have evicted some crums to disk, but reads fetch from the in-memory enfilade tree, which is the authoritative state. Disk is only a persistence backing, not the live read target.

---

## 2. Does `checkforopen` block CREATENEWVERSION when B holds WRITEBERT?

**Yes, according to the access matrix.**

`docreatenewversion` must read the source document's content to copy it: it calls `doretrievedocvspanfoo` → `retrievedocumentpartofvspanpm`, which needs the source orgl open and readable [ST-VERSION-CREATE]. This goes through `findorgl` with a READ-type access, triggering `checkforopen`.

The `checkforopen` matrix [PRE-OPEN-DOC] is explicit:

> READ request on a document open for WRITE by a **different** connection → **-1 (denied)**

Session A's read request on session B's WRITE-held document returns -1. The `findorgl` call returns FALSE, and `doXXX` is skipped.

**However**: [EC-RESPONSE-BEFORE-CHECK] applies. For most FEBE mutations, the success response is sent *before* `doXXX` executes. Session A likely receives a success response (and a new version address) before the internal BERT check runs. The version orgl is allocated by `createorglingranf` (step 1 of `docreatenewversion`) before the source document read. If `doretrievedocvspanfoo` then fails the BERT check, the version orgl exists as an address in the granfilade but with no copied content — a structural orphan analogous to the CREATELINK orphan case [SS-ADDRESS-SPACE].

The intended protocol behavior from [INT-BERT-VERSION]: `checkforopen` returning -1 signals the client to create a version instead of a direct write. But here, the client *is* creating a version — the -1 return blocks even that. The front end receives no reliable error signal.

**Address allocation**: Separately, if session A's account differs from the document's owning account, [ST-VERSION-OWNERSHIP] applies — the ownership check `tumbleraccounteq ∧ isthisusersdocument` fails, and the version address is allocated under session A's account rather than as a child of the source document. This is independent of the BERT outcome.

---

**Summary**: The event loop guarantees session A sees a consistent, fully-committed POOM state — no partial shifts. BERT's `checkforopen` denies the content read (-1), but due to response-before-check, the failure is silent: session A gets a success response, the version address is allocated, but the content copy is silently skipped.

## Code Exploration

Now I have everything I need. Let me compose the full answer.

---

# Answer: CREATENEWVERSION vs. Session B's Uncommitted POOM State

## Short answer

1. **`docreatenewversion` reads session B's in-memory POOM directly** — it bypasses `checkforopen` entirely for the source document and reads the single shared global enfilade, which contains every INSERT session B has performed, committed or not.

2. **`checkforopen` does NOT block explicit CREATENEWVERSION** — the write-lock held by session B is invisible to the version-creation path.

---

## Trace: `createnewversion` → `docreatenewversion`

`fns.c:289-300`:
```c
void createnewversion(typetask *taskptr)
{
  typeisa originaldocisa, newdocisa;
  ...
  if (
     getcreatenewversion (taskptr, &originaldocisa)
  && docreatenewversion (taskptr, &originaldocisa, &originaldocisa, &newdocisa))
        putcreatenewversion (taskptr, &newdocisa);
  else
        putrequestfailed (taskptr);
}
```

The handler calls `docreatenewversion` directly, with no prior bert check on the source.

---

## Inside `docreatenewversion`

`do1.c:260-299`:
```c
bool docreatenewversion(typetask *taskptr, typeisa *isaptr, typeisa *wheretoputit, typeisa *newisaptr)
{
  ...
  if (!createorglingranf(taskptr, granf, &hint, newisaptr)) {
      return (FALSE);
  }

  if (!doretrievedocvspanfoo (taskptr, isaptr, &vspan)) {   // <-- reads source
      return FALSE;
  }
  ...
  addtoopen(newisaptr, user, TRUE, WRITEBERT);
  docopyinternal(taskptr, newisaptr, &vspan.stream, &vspec);
  logbertmodified(newisaptr, user);
  doclose(taskptr, newisaptr, user);
  return (TRUE);
}
```

The content of the source document is obtained via `doretrievedocvspanfoo` (`do1.c:301-309`):
```c
bool doretrievedocvspanfoo(typetask *taskptr, typeisa *docisaptr, typevspan *vspanptr)
{
  typeorgl docorgl;
  ...
  return (
     findorgl (taskptr, granf, docisaptr, &docorgl, NOBERTREQUIRED)
  && retrievedocumentpartofvspanpm (taskptr, docorgl, vspanptr) );
}
```

The bert type passed is **`NOBERTREQUIRED`**.

---

## Why `NOBERTREQUIRED` bypasses the write-lock check

`granf1.c:17-41`:
```c
bool findorgl(typetask *taskptr, typegranf granfptr, typeisa *isaptr, typeorgl *orglptr, int type)
{
  int temp;
  if (/*backenddaemon &&*/(temp = checkforopen(isaptr, type, user)) <= 0) {
      ...return FALSE;
  }
  *orglptr = fetchorglgr(taskptr, granfptr, isaptr);
  return (*orglptr ? TRUE : FALSE);
}
```

`checkforopen` is called, but with `type == NOBERTREQUIRED`. `bert.c:59-61`:
```c
if (type == NOBERTREQUIRED) {
    return 1;   /* Random > 0 */
}
```

The function returns positive immediately, skipping the entire bert table scan. Session B's WRITEBERT entry for the source document is **never consulted**. The check that would return `-1` for `conn != source` + `type == WRITE` (see the table at `bert.c:44-51`) is never reached.

---

## What `fetchorglgr` actually returns

`granf2.c:22-81`. The granfilade is a **single global** `typegranf granf`, declared at `corediskout.c:21` and initialized at `entexit.c:44`:
```c
granf = (typegranf) createenf (GRAN);
spanf = (typespanf) createenf (SPAN);
```

There is one `granf`, shared by all connections. `fetchorglgr` searches it for the document ISA, faults the orgl in from disk if necessary (`granf2.c:60: inorgl(context->corecrum)`), and returns the in-memory orgl pointer (`granf2.c:62: ret = context->corecrum->cinfo.granstuff.orglstuff.orglptr`).

That returned orgl pointer **is the same POOM tree** that session B has been modifying via INSERT. There is no per-session copy, no snapshot, no write buffer. The backend is a single-process, single-memory-space event loop (`bed.c`). Every INSERT session B performs calls `makegappm` and `doinsertnd` (`insertnd.c:54,57`) which mutate the POOM in place, immediately, in shared memory.

---

## Does `checkforopen` ever block `docreatenewversion` on the source document?

**Not for explicit CREATENEWVERSION.** The only call to `checkforopen` for the source document goes through `findorgl` with `NOBERTREQUIRED`, which short-circuits immediately.

The bert table IS consulted for the source document in one path: `doopen` (`bert.c:279`), when a session tries to OPEN a document with BERTMODECOPYIF or BERTMODEONLY. In `doopen`, if `checkforopen` returns -1 for the source (because session B has it write-locked, conn != current), `doopen` calls `docreatenewversion` to create a copy. That is the OPEN-with-copy path, not the explicit CREATENEWVERSION command.

Looking at the table `bert.c:44-51`:
```
type      Not Open    |  Open READ      |  Open WRITE
  v     !owned|owned  # conn==|conn!= # conn==|conn!=
READ       0  |  0   #  READ |  0    # WRITE | -1
WRITE     -1  |  0   #  -1   | -1    # WRITE | -1
```

If session A calls explicit CREATENEWVERSION while session B holds WRITEBERT on the same document: the `-1` case (right column, bottom row) would apply if `checkforopen` were called — but it is never called for the source document in this path. The version creation proceeds regardless.

---

## Summary

| Question | Answer | Key code |
|---|---|---|
| Does `docreatenewversion` read session B's POOM state? | **Yes** — unconditionally. There is one global `granf` in memory; all inserts mutate it immediately. | `do1.c:281`, `granf2.c:62` |
| Does it read from disk or memory? | **Memory** (faults from disk only if not yet cached, but then reflects session B's mutations since those are in the same in-core POOM) | `granf2.c:51-63` |
| Does `checkforopen` block CREATENEWVERSION if source is write-locked by session B? | **No** — `NOBERTREQUIRED` short-circuits `checkforopen` to return 1 before the bert table is scanned | `bert.c:59-61`, `do1.c:307` |
| When DOES `checkforopen` block on a write-locked document? | Only in `doopen` (`bert.c:279`), the explicit OPEN operation, not the CREATENEWVERSION command | `bert.c:279-322` |

**Architectural consequence:** CREATENEWVERSION on a document that session B has open for writing will silently snapshot whatever in-memory POOM state session B has produced so far — including any INSERT shifts that session B has not yet "committed" in any meaningful sense, since there is no commit boundary in the protocol. The new version is a snapshot of the live, mutating, in-memory tree at the moment `doretrievedocvspanfoo` runs.

---

## Question 17 [gregory]

> When two sessions each CREATELINK in different documents but both links reference the same I-address range as an endset, do both `insertendsetsinspanf` calls write to the same spanfilade region — and if so, can the second write's `splitcrumupwards` corrupt the tree structure left by the first write, or does single-threaded execution prevent this?

### Gregory's Answer

## KB Synthesis

Single-threaded execution prevents any corruption. The two CREATELINK operations never actually run concurrently.

**Do both writes target the same spanfilade region?**

Yes. Both `insertendsetsinspanf` calls will insert entries keyed by the shared I-address range into the same region of the spanfilade B-tree. This is by design — the spanfilade is a multimap from I-address ranges to (link ISA, endpoint type) pairs [SS-SPANF-OPERATIONS], so multiple links legitimately coexist at the same I-address key. The second insert does not replace the first; it adds a sibling entry at that I-address region.

**Can the second `splitcrumupwards` corrupt the tree from the first write?**

No, because the two operations execute sequentially, not concurrently.

The `bed.c` event loop uses run-to-completion scheduling: `xanadu(&task)` executes an entire FEBE operation — request parsing, all state mutations, response sending, memory cleanup — before returning to `select()` [INV-ATOMICITY]. Even when both sessions have pending requests simultaneously, the loop iterates over ready file descriptors one at a time, completing each fully before advancing [INV-SEQUENTIAL-DISPATCH].

This means the first CREATELINK's complete execution — including the full `insertendsetsinspanf` call and any `splitcrumupwards` it triggers — finishes and leaves the spanfilade in a fully consistent, rebalanced state before the second CREATELINK begins. The second write sees a clean, settled tree.

This directly addresses the concern raised in [PRE-CONCURRENT-INSERT]: unsynchronized concurrent insertion into the same enfilade *would* be unsafe (shared pointer modifications in `adopt`, lost updates to `numberofsons`, split/rebalance assuming exclusive access). But [INV-SEQUENTIAL-DISPATCH] guarantees this situation cannot arise — the serialization is structural, not via locks.

The result is that after both CREATELINKs complete, the spanfilade contains two independent entries at the shared I-address region — one for each link — with the tree correctly rebalanced after each sequential insertion.

## Code Exploration

I now have all the information needed. Here is the complete analysis:

---

## Answer

### 1. Do both `insertendsetsinspanf` calls write to the same spanfilade region?

**Yes.** The spanfilade is a global singleton.

`xanadu.h:15–16`:
```c
#define typespanf INT *   /* temp -- INT for alignment */
extern typespanf spanf;
```

Every `docreatelink` call passes this same global `spanf` all the way down:

`do1.c:219`:
```c
&& insertendsetsinspanf (taskptr, spanf, linkisaptr, fromsporglset, tosporglset, threesporglset)
```

`do2.c:116–128` (`insertendsetsinspanf`): delegates to `insertspanf` three times (LINKFROMSPAN, LINKTOSPAN, LINKTHREESPAN), each time passing `spanfptr` — the global `spanf`.

`spanf1.c:49–51` (`insertspanf`): sets `crumorigin.dsas[SPANRANGE]` to `lstream` — the I-address drawn from the sporglset endset — and calls:
```c
insertnd(taskptr,(typecuc*)spanfptr,&crumorigin,&crumwidth,&linfo,SPANRANGE);
```

When two links both reference the **same I-address range** as an endset, `lstream` is the same value, so `crumorigin.dsas[SPANRANGE]` is the same value, and `insertnd` navigates to the **same subtree** of the single global `spanf`. The two inserts land in the same region of the spanfilade tree.

---

### 2. Can the second write's `splitcrumupwards` corrupt the tree left by the first?

**No.** Single-threaded execution makes this impossible.

The proof is in `bed.c`. The main event loop (`bed.c:103–148`) is a single-threaded `select()`-based dispatcher:

```c
for (;;) {
    inputfds2 = inputfds;                             /* bed.c:110 */
    if (select(nfds+1, &inputfds2, 0, 0, &timeout) < 0) {
        ...
    } else {
        for (i = 0; i <= nfds; i++) {                 /* bed.c:118 */
            if ((1<<i) & inputfds2) {
                user = fdtoplayer[i];
                task.inp = player[user].inp;
                ...
                xanadu(&task);                        /* bed.c:128 */
                ...
            }
        }
    }
    ...
}
```

Each call to `xanadu(&task)` at `bed.c:128` dispatches and completes **exactly one request** before returning. The body of `xanadu()` (`bed.c:153–172`) is:

```c
int xanadu(typetask *taskptr) {
    ...
    } else if (getrequest(taskptr, &request)) {
        (*requestfns[request])(taskptr);   /* bed.c:162 — dispatches createlink */
        sendresultoutput(taskptr);
        ...
    }
    tfree(taskptr);
    ...
}
```

`(*requestfns[request])` resolves to `createlink` (`fns.c:100`), which calls `docreatelink` (`do1.c:195`), which calls `insertendsetsinspanf` (`do2.c:116`), which calls `insertspanf` (`spanf1.c:15`), which calls `insertnd` (`insertnd.c:15`), which calls `insertcbcnd` (`insertnd.c:242`), which calls `splitcrumupwards` (`split.c:16`). **All of this runs to completion inside a single `xanadu()` call.**

The inner `for (i = 0; i <= nfds; i++)` at `bed.c:118` is sequential. Even if Session B's fd is also ready in the same `select()` snapshot, Session B's `xanadu()` call does not begin until the loop advances past Session A's fd — after Session A's `xanadu()` has already returned.

There are no threads, no coroutines, no callbacks from signal handlers that touch the enfilade (signal handlers are: `SIGPIPE → crash`, `SIGHUP → crash`, `SIGXCPU → SIG_IGN`, `SIGINT → flagquitting`, none of which call enfilade code — `bed.c:70–73`).

---

### 3. What actually happens when Session B's `insertcbcnd` runs

After Session A's `splitcrumupwards` finishes, the spanfilade is in a valid state. `splitcrumupwards` (`split.c:16–44`) leaves the tree balanced: it either:

- Calls `levelpush(father)` + `splitcrum(findleftson(father))` if the fullcrum needs a height increase (`split.c:29–35`), or
- Calls `splitcrum(father)` which calls `splitcrumsp(father)` (`split.c:95`) → `peelcrumoffnd` (`split.c:130`), which uses `disown` + `adopt` + `movewisp` to redistribute a child into a new sibling node — leaving the tree structurally intact.

`insertnd` (`insertnd.c:76`) also calls `recombine(fullcrumptr)` afterward, which for SPAN enfilades calls `recombinend` (`recombine.c:22–34`), merging any under-full nodes.

When Session B subsequently runs `insertmorend` on the same `spanf` subtree, it reads the tree state that Session A left — fully valid. Session B's `insertcbcnd` may itself call `splitcrumupwards` if that insertion makes a node overfull, and this too completes before any other session sees the tree.

---

### Summary

| Question | Answer | Evidence |
|---|---|---|
| Do both calls write to same `spanf` region? | **Yes** — `spanf` is a global singleton; I-address from endset determines the subtree | `xanadu.h:15–16`, `do2.c:119–120`, `spanf1.c:49–51` |
| Can second `splitcrumupwards` corrupt first's tree? | **No** — strictly single-threaded | `bed.c:118–130`: sequential for-loop over fds, one `xanadu()` completes before next begins |
| Mechanism | Each `xanadu()` call is an atomic request/response cycle; no interleaving is possible | `bed.c:153–172` |

The single-threaded `select()` loop in `bed.c` is the complete safety guarantee. The two CREATELINK operations are serialized at the request level — they are not concurrent in any sense. Session B's `insertendsetsinspanf` reads a spanfilade that Session A's `splitcrumupwards` has already finished modifying and left in a valid state.

---

## Question 18 [gregory]

> After session A performs DELETE on document D₁ removing content at I-addresses that session B's document D₂ also references via transclusion, does session B's subsequent `find_links` on D₂ still discover links whose endsets overlap those I-addresses — confirming that DELETE in D₁ has zero effect on D₂'s link discoverability?

### Gregory's Answer

## KB Synthesis

**Yes, session B's `find_links` on D₂ still discovers those links.** DELETE on D₁ has zero effect on D₂'s link discoverability. The reasoning follows from three independent properties of the system.

---

## 1. DELETE modifies only the target document's POOM

`[ST-DELETE]` (Finding 0057): `dodeletevspan` calls `deletevspanpm` → `deletend`, which operates exclusively on D₁'s document orgl in the granf layer. There is no call to any spanfilade function. D₁'s POOM loses the V-to-I mappings for the deleted I-addresses; D₂'s POOM is not touched.

`[FC-DELETE-CROSS-DOC]` (Finding 0064) states this explicitly:

> DELETE in one document has zero effect on any other document's POOM mappings. If document T transcluded content from document D (sharing I-addresses via COPY), and D subsequently deletes that content, T's POOM still maps to the shared I-addresses. T's content is unaffected — the transclusion survives the source document's deletion.

## 2. The spanfilade link index is unchanged

`[INV-SPANF-WRITE-ONLY]` (Finding 0057): The spanfilade is append-only. No `deletespanf` function exists anywhere in the codebase. Links indexed by those I-addresses remain indexed regardless of what DELETE operations occur in any document.

`[FC-DELETE-CROSS-DOC]` formalises this: `delete(D₁, vspan) ⟹ spanfilade_after = spanfilade_before`.

## 3. `find_links` operates entirely in I-space via the spanfilade

`[SS-FIND-LINKS]` (Finding 0028): `find_links(search_specset)` converts the search specset to I-addresses, then searches the spanfilade for link endpoints whose I-addresses overlap. Document identity and V-position are irrelevant to this lookup.

Since D₂'s POOM still maps the shared I-addresses to V-positions (point 1), D₂'s search specset still converts to those I-addresses. Since the spanfilade link index is unchanged (point 2), the lookup still returns the links.

## 4. INT-TRANSCLUSION-LINK-SEARCH confirms this exact scenario

`[INT-TRANSCLUSION-LINK-SEARCH]` (Finding 0029) directly covers this case:

> When content is transcluded (vcopy'd) to another document, the copy retains the original content identity (I-stream addresses). If the original content is deleted, links referencing that content become undiscoverable from the original document but remain discoverable from the copy, because the copy's V-stream still contains content at those I-stream addresses.

The observable asymmetry: `find_links(D₁, deleted_span)` now returns nothing (D₁'s POOM no longer maps those I-addresses), while `find_links(D₂, transcluded_span)` continues to return the links unchanged.

---

## Summary

| Layer | State after DELETE on D₁ | Effect on D₂'s `find_links` |
|---|---|---|
| D₁'s POOM | I-addresses unmapped | None — only D₁ affected |
| D₂'s POOM | **Unchanged** | D₂ still resolves those I-addresses |
| Granfilade (content) | **Unchanged** (append-only) | None |
| Spanfilade link index | **Unchanged** (write-only) | Links still indexed by those I-addresses |

DELETE on D₁ is POOM-local `[FC-DELETE-CROSS-DOC]`, the spanfilade is write-only `[INV-SPANF-WRITE-ONLY]`, and link discovery is a pure I-address intersection against the spanfilade `[SS-FIND-LINKS]`. All three properties independently guarantee that D₂'s link discoverability is unaffected.

## Code Exploration

Now I have everything needed. Here is the full analysis with code citations.

---

## Answer: DELETE in D₁ Has Zero Effect on D₂'s Link Discoverability

**Yes, session B's subsequent `find_links` on D₂ still discovers all links whose endsets overlap those I-addresses.** The DELETE in D₁ has zero effect. Here is the complete code trace that confirms it.

---

### The DELETE Path — What It Touches

**Entry point** [`fns.c:333-347`]: `deletevspan()` calls `dodeletevspan`.

**`dodeletevspan`** [`do1.c:158-167`]:
```c
bool dodeletevspan(typetask *taskptr, typeisa *docisaptr, typevspan *vspanptr)
{
  typeorgl docorgl;
    return (
       findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
    && deletevspanpm (taskptr, docisaptr, docorgl, vspanptr)
    /*&& TRUE*/ /* ht stuff */ );
}
```
`findorgl` opens **D₁'s POOM entry in the granfilade** (`granf`). Nothing else.

**`deletevspanpm`** [`orglinks.c:145-152`]:
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
Calls `deletend` on **`docorgl`** — D₁'s POOM tree root — and marks D₁ as modified in the bert table. **No call to anything in `spanf1.c` or `spanf2.c`.**

**`deletend`** [`edit.c:31-76`]:
```c
int deletend(typecuc *fullcrumptr, tumbler *origin, tumbler *width, INT index)
{
    ...
    makecutsnd(fullcrumptr, &knives);
    newfindintersectionnd(fullcrumptr, &knives, &father, &foffset);
    for (ptr = findleftson(father); ptr; ptr = next) {
        switch (deletecutsectionnd(ptr, &fgrasp, &knives)) {
          case 1:  disown(ptr); subtreefree(ptr);          break;  // fully inside deletion range
          case 2:  tumblersub(&ptr->cdsp.dsas[index], ...); break;  // past deletion range, adjust V-offset
        }
    }
    setwispupwards(father, 1);
    recombine(father);
}
```
All tree traversal (`findleftson`, `findrightbro`, `findfather`) navigates **only within `fullcrumptr`** — the root of D₁'s POOM tree. `disown`+`subtreefree` remove crums from D₁'s tree. `tumblersub` adjusts V-displacements of remaining crums in D₁'s tree. The function receives a single tree root pointer and mutates only that tree.

**Critical finding**: There is no `deletespanf` function anywhere in the codebase. The entire `spanf1.c` and `spanf2.c` contain only insertion and query functions — never removal. This is confirmed in Finding 0057. The global `spanf` is **write-only by document operations**.

---

### The `find_links` Path on D₂

**Entry point** [`fns.c:189-202`]: `findlinksfromtothree()` calls `dofindlinksfromtothree`.

**`dofindlinksfromtothree`** [`do2.c:348-353`]:
```c
bool dofindlinksfromtothree(typetask *taskptr, typespecset fromvspecset, typespecset tovspecset,
  typespecset threevspecset, typeispan *orglrangeptr, typelinkset *linksetptr)
{
    return findlinksfromtothreesp(taskptr, spanf, fromvspecset, tovspecset, threevspecset,
                                  orglrangeptr, linksetptr);
}
```
This passes the **global `spanf`** — the same global that was never touched by DELETE.

**`findlinksfromtothreesp`** [`spanf1.c:56-103`]:
```c
if (fromvspecset)
    specset2sporglset(taskptr, fromvspecset, &fromsporglset, NOBERTREQUIRED);
if (fromvspecset) {
    sporglset2linkset(taskptr, (typecuc*)spanfptr, fromsporglset, &fromlinkset, orglrange, LINKFROMSPAN);
```
Steps: (1) convert D₂'s V-specset → I-sporglset; (2) search `spanf` with those I-addresses.

**Step 1 — V→I conversion using D₂'s own POOM:**

**`specset2sporglset`** [`sporgl.c:14-33`] dispatches to **`vspanset2sporglset`** [`sporgl.c:35-65`]:
```c
bool vspanset2sporglset(..., typeisa *docisa, typevspanset vspanset, ...)
{
    findorgl(taskptr, granf, docisa, &orgl, type);   // opens D₂'s POOM — not D₁'s
    for (; vspanset; vspanset = vspanset->next) {
        vspanset2ispanset(taskptr, orgl, vspanset, &ispanset);  // V→I via D₂'s POOM
        for (; ispanset; ispanset = ispanset->next) {
            sporglset->sporgladdress = *docisa;               // home doc = D₂
            sporglset->sporglorigin  = ispanset->stream;      // I-address (permascroll)
            sporglset->sporglwidth   = ispanset->width;
```
D₂'s POOM was never touched by session A's DELETE. D₂ still maps its V-addresses to I-addresses **X** — the same permascroll addresses. The sporglset carries I-addresses X unchanged.

**Step 2 — Spanfilade query by I-address:**

**`sporglset2linksetinrange`** [`sporgl.c:239-269`]:
```c
int sporglset2linksetinrange(typetask *taskptr, typecuc *spanfptr, typesporglset sporglset,
  typelinkset *linksetptr, typeispan *orglrange, INT spantype)
{
    for (; sporglset; sporglset = ...) {
        if (FALSE/*trying to kluge links followable thru versions */
            && ((typeitemheader*)sporglset)->itemid == SPORGLID) {
            infoptr = &linfo;
            movetumbler(&((typesporgl *)sporglset)->sporgladdress, &linfo.homedoc);
        } else
            infoptr = NULL;    // ← always taken
        context = retrieverestricted(spanfptr, (typespan*)sporglset, SPANRANGE,
                                     &range, ORGLRANGE, (typeisa*)infoptr);
        for (c = context; c; c = c->nextcontext) {
            beheadtumbler(&c->totaloffset.dsas[ORGLRANGE], &linksa);
            onlinklist(taskptr, linksetptr, &linksa);
        }
```
Note the `FALSE` condition: the home-document filter (`infoptr`) is **always NULL**. The query is a pure I-address range lookup against the spanfilade's `SPANRANGE` axis, with no home-doc filtering. Any link whose endset I-addresses overlap X is returned, regardless of which document that link was originally created against.

---

### How Links Are Stored in `spanf`

**`insertendsetsinspanf`** [`do2.c:116-128`] is called during `docreatelink` [`do1.c:195-221`]:
```c
insertspanf(taskptr, spanfptr, linkisaptr, fromsporglset, LINKFROMSPAN)
insertspanf(taskptr, spanfptr, linkisaptr, tosporglset, LINKTOSPAN)
insertspanf(taskptr, spanfptr, linkisaptr, threesporglset, LINKTHREESPAN)
```

**`insertspanf`** [`spanf1.c:15-54`]:
```c
prefixtumbler(isaptr, spantype, &crumorigin.dsas[ORGLRANGE]);  // key = prefixed link ISA
movetumbler(&lstream, &crumorigin.dsas[SPANRANGE]);            // value = I-address of endset content
movetumbler(&lwidth, &crumwidth.dsas[SPANRANGE]);
insertnd(taskptr, (typecuc*)spanfptr, &crumorigin, &crumwidth, &linfo, SPANRANGE);
```

The spanfilade maps: **SPANRANGE (I-address) → ORGLRANGE (prefixed link ISA)**. The key is the **permascroll I-address** of the content in the link endset — a permanent, document-agnostic address. It is not keyed to any particular document's V-addresses.

---

### The Full Mechanism

Let I-addresses **X** denote the permascroll range that D₁ and D₂ both reference via transclusion.

| Event | Operation | Effect on `granf` | Effect on `spanf` |
|---|---|---|---|
| Link L created with endset at X | `insertendsetsinspanf` | L's POOM entry created | SPANRANGE=X → L added |
| Session A: DELETE from D₁ at V-positions covering X | `deletend(D₁.orgl)` | D₁'s V→I mapping for X removed | **Nothing** |
| Session B: `find_links` on D₂ | `findlinksfromtothreesp` | D₂'s POOM queried: V→I yields X | X queried in `spanf`, L found |

**Execution invariants that make this hold:**

1. **POOM tree isolation** [`edit.c:31-76`]: `deletend` receives `fullcrumptr` — a pointer to the root of D₁'s enfilade tree. All mutations (`disown`, `subtreefree`, `tumblersub`) navigate exclusively within that tree. There is no code path to D₂'s tree.

2. **`spanf` write-once** [`spanf1.c`, `spanf2.c`]: No `deletespanf` function exists. Confirmed by the complete absence of any removal call in the DELETE path and by inspection of both spanf source files (Finding 0057).

3. **Link endsets keyed to I-addresses** [`spanf1.c:49-51`]: `insertspanf` stores links against **permascroll I-addresses**, not V-addresses in any document. This is a structural invariant of the dual-enfilade architecture (Finding 0012).

4. **D₂'s POOM untouched by F0** [`edit.c:31-76`, Finding 0067]: The frame axiom is confirmed: `insertnd`/`deletend` operate exclusively on the pointer passed to them. D₂'s orgl pointer is never passed to any operation initiated by session A's DELETE.

5. **Home-doc filter disabled** [`sporgl.c:251`]: The `FALSE` guard in `sporglset2linksetinrange` means the spanfilade query is purely by I-address range. Even if the link was originally created against D₁'s V-addresses, as long as the endset I-addresses overlap X, the link is returned for D₂'s query.

---

### Conclusion

**DELETE in D₁ has zero effect on D₂'s link discoverability.** The DELETE path (`dodeletevspan` → `deletevspanpm` → `deletend`) operates exclusively on D₁'s POOM entry in `granf` [`orglinks.c:145-152`, `edit.c:31-76`] and contains no call to any spanf function. The global `spanf` is structurally append-only — no deletion primitive exists. Links are indexed in `spanf` against permanent permascroll I-addresses [`spanf1.c:49-51`]. Session B's `find_links` on D₂ converts D₂'s (unchanged) V-addresses to the same I-addresses X via D₂'s (unchanged) POOM [`sporgl.c:47-58`], then queries the (unchanged) `spanf` for links whose endsets overlap X [`sporgl.c:259`]. The result is identical before and after the DELETE.

This is the intended Xanadu invariant: content at a given I-address carries its link relationships permanently, independent of which documents currently transclude it and independent of edits to other documents that reference the same underlying content.

---

## Question 19 [gregory]

> If a session crashes (TCP connection drops) mid-INSERT — after `createenf` has appended to the granfilade but before `insertpm` has updated the POOM — does the orphaned granfilade entry affect any other session's I-address allocation via `findisatoinsertmolecule`, causing the next allocation to skip past the orphaned range?

### Gregory's Answer

## KB Synthesis

Yes, but only under a specific combination of conditions, and never through a live cross-session path.

## Why Cross-Session Contamination Cannot Happen During Normal Operation

The system is single-threaded. From [INV-SEQUENTIAL-DISPATCH] and [INV-ATOMICITY], each FEBE operation runs to completion inside a single `xanadu(&task)` call before `select()` returns control. No other session can invoke `findisatoinsertmolecule` while Session A's INSERT is executing — the entire INSERT (including `inserttextingranf` → `insertpm` → `insertspanf`) is an uninterruptible unit from every other session's perspective. A TCP connection drop cannot interrupt the operation mid-execution; the backend would complete the INSERT and only discover the dropped connection when it attempts to send the response.

## The Crash-and-Restart Case

The question does have force if "crash" means a process-level termination (SIGKILL, power failure, SIGSEGV) that interrupts between `inserttextingranf` and `insertpm`. Whether the orphaned granfilade entries survive depends entirely on whether the grim reaper flushed them before the crash.

**Normal case — entries still in-memory:** From [SS-DURABILITY-BOUNDARY], INSERT writes content into in-memory crums marked `modified=TRUE` via `ivemodified()`. No `fsync` is called. On crash, in-memory crums are lost. On restart, `findpreviousisagr` does not find the orphaned entries; allocation resumes from the pre-crash maximum. **No allocation gap.**

**Grim reaper case — entries already on disk:** From [SS-CACHE-MECHANISM] and [EC-CROSS-ENFILADE-EVICTION], the grim reaper evicts old modified crums to disk when memory allocation fails. If `insertpm`'s own allocations triggered the grim reaper, it could have flushed the `inserttextingranf` crums to disk before `insertpm` completed. After a crash in this window, those I-addresses survive on disk in the granfilade but no POOM references them.

On restart, from [SS-ADDRESS-SPACE] (Finding 0061): `next_iaddr(granf) = max_iaddr(granf) + 1`, queried from the granfilade tree without regard to whether any POOM maps those addresses. So yes — `findisatoinsertmolecule` would find the orphaned entries as the current maximum and allocate above them, **creating a permanent allocation gap**.

## Consequences of the Gap

These dark I-addresses are permanent by [INV-NO-IADDR-REUSE]: the granfilade never removes entries and allocation never retreats. They satisfy `a ∈ dom.ispace ∧ ¬(∃d,v : poom.d(v) = a)` — unreferenced in the sense of DEL5 from [EC-GHOST-LINK]. No future INSERT or COPY will ever reference them (no POOM entry points there), so they are dead storage.

The practical effect on subsequent operations:
- `findisatoinsertmolecule` allocates above the gap, so next text I-addresses are non-contiguous with pre-crash text. This is identical in structure to what [INT-LINK-INSERT] (Finding 0063) documents for CREATELINK: a gap in the text I-address subsequence caused by an intervening allocation.
- `compare_versions` results would show two separate shared span pairs where one contiguous pair would otherwise appear — the same fragmentation as when CREATELINK intervenes between two INSERTs.

## Summary

The single-threaded event loop [INV-SEQUENTIAL-DISPATCH] makes live cross-session interference impossible. The crash scenario is the only path to the described outcome, and it requires the grim reaper to have coincidentally flushed the granfilade crums to disk during the same INSERT's execution before the process died — a race between two operations happening within a single synchronous call. When it does occur, [INV-MONOTONIC] guarantees the allocation skips past the orphaned range permanently, and [INV-NO-IADDR-REUSE] guarantees those dark I-addresses are never reclaimed.

## Code Exploration

I now have everything I need. Here is the full analysis:

---

## Answer

### The Execution Path in Question

The question describes a crash between two writes: (1) a granfilade append, and (2) a POOM update via `insertpm`. These correspond to two distinct paths in the code depending on operation type.

---

### Factual Correction: `createenf` Does Not Write to the Granfilade

`createenf` at `credel.c:492` only creates a new enfilade structure **in memory**:

```c
typecuc *createenf(INT enftype)
{
    fullcrumptr = (typecuc *) createcrum(1,enftype);
    fullcrumptr->cenftype = enftype;
    fullcrumptr->isapex = TRUE;
    fullcrumptr->isleftmost = TRUE;
    adopt(ptr = createcrum(0, enftype), SON, (typecorecrum*)fullcrumptr);
    ...
}
```

It allocates two crum nodes and sets up the empty tree. No write to the global `granf` occurs here. The write to the global granfilade happens later via `insertseq` at `granf2.c:125`, inside `createorglgr`:

```c
bool createorglgr(typetask *taskptr, typegranf fullcrumptr, typehint *hintptr, typeisa *isaptr)
{
    if (!findisatoinsertgr ((typecuc*)fullcrumptr, hintptr, isaptr))
        return (FALSE);
    locinfo.infotype = GRANORGL;
    locinfo.granstuff.orglstuff.orglptr = createenf (POOM);   // ← in-memory only [granf2.c:120]
    ...
    insertseq ((typecuc*)fullcrumptr, isaptr, &locinfo);       // ← THIS writes to global granf [granf2.c:125]
    return (TRUE);
}
```

The question's phrase "after `createenf` has appended to the granfilade" is thus a conflation of two consecutive operations in `createorglgr`: `createenf` followed by `insertseq`.

---

### The Two Distinct Crash Scenarios

**Scenario A — Crashed text INSERT** (`doinsert` → `inserttextgr` → `insertseq`, then crash before `docopy`/`insertpm`)

The text INSERT path [do1.c:87–123]:
```c
bool doinsert(...)
{
    makehint(DOCUMENT, ATOM, TEXTATOM, docisaptr, &hint);
    ret = (inserttextingranf(taskptr, granf, &hint, textset, &ispanset)   // ← granf written [do1.c:118]
        && docopy (taskptr, docisaptr, vsaptr, ispanset)                  // ← POOM written [do1.c:119]
    );
}
```

`inserttextingranf` → `inserttextgr` [granf2.c:83–109]:
```c
findisatoinsertgr ((typecuc*)fullcrumptr, hintptr, &lsa);       // allocates ISA
...
insertseq ((typecuc*)fullcrumptr, &lsa, &locinfo);              // writes GRANTEXT to global granf [granf2.c:99]
```

`docopy` → `insertpm` [orglinks.c:75–134] writes into the per-document POOM (the `orgl` tree), recording the V→I mapping:
```c
insertnd (taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);  // [orglinks.c:130]
```

If the TCP drops after `insertseq` [granf2.c:99] but before `insertpm` [orglinks.c:130]: the GRANTEXT entry exists in the global granfilade but the document's POOM has no V→I mapping to it.

**Scenario B — Crashed document creation** (`createorglgr`/`createenf` completes, crash before `docopyinternal`/`insertpm`)

In `docreatenewversion` [do1.c:260–299]:
```c
if (!createorglingranf(taskptr, granf, &hint, newisaptr))  // granf written [do1.c:277]
    return (FALSE);
...
docopyinternal(taskptr, newisaptr, &vspan.stream, &vspec);  // new POOM populated via insertpm [do1.c:293]
```

If crash between line 277 and 293: GRANORGL at `newisaptr` is in the global granfilade; the new document's POOM (created by `createenf`) is empty.

---

### `findisatoinsertmolecule`: What It Searches and Why It Matters

`findisatoinsertmolecule` [granf2.c:158–181] is called for ATOM (text/link) insertions into an existing document D. It computes:

```c
tumblerincrement (&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound);  // [granf2.c:162]
clear (&lowerbound, sizeof(lowerbound));
findpreviousisagr ((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);      // [granf2.c:164]
```

For TEXTATOM (atomtype=1) and document D at ISA `[...d0, d1, d2, d3, d4, d5]` (e.g. `1.1.0.1.0.1`), `tumblerincrement` works by finding the index `idx` of the last non-zero mantissa digit and adding at `idx + rightshift` [tumble.c:599–623]. With rightshift=2, amount=2: `upperbound = D.0.2` (two mantissa positions beyond D's last digit, value 2).

`findpreviousisagr` [granf2.c:255–278] traverses the **global** granfilade to find the highest ISA entry < `upperbound`. At a leaf crum, `findlastisaincbcgr` [granf2.c:280–284] is called:

```c
int findlastisaincbcgr(typecbc *ptr, typeisa *offset)
{
    if (ptr->cinfo.infotype == GRANTEXT)
        tumblerincrement (offset, 0, (INT) ptr->cinfo.granstuff.textstuff.textlength - 1, offset);
    // No increment for GRANORGL — offset stays at the entry's base ISA
}
```

This returns the ISA of the last character for GRANTEXT, or the base ISA for GRANORGL.

---

### Does the Orphaned Entry Affect Subsequent Allocations?

**Scenario A (orphaned GRANTEXT):** YES, directly.

Text atoms for document D are at ISAs `D.0.1.0.1`, `D.0.1.0.2`, etc. If session A's GRANTEXT entry at ISA `D.0.1.0.1` with `textlength=N` was written to the granfilade but the POOM was never updated, then when session B inserts text into D:

1. `findisatoinsertgr` → `findisatoinsertmolecule` with `upperbound = D.0.2`
2. `findpreviousisagr` traverses the global `granf` — the orphaned GRANTEXT is in the tree
3. `findlastisaincbcgr` returns `lowerbound = D.0.1.0.N` (orphaned start + (N-1), accounting for textlength)
4. In `findisatoinsertmolecule` [granf2.c:168–169]:
   ```c
   } else if (hintptr->atomtype == TEXTATOM) {
       tumblerincrement (&lowerbound, 0, 1, isaptr);  // D.0.1.0.(N+1)
   ```
5. Session B's text is allocated at `D.0.1.0.(N+1)`, **skipping the orphaned range `D.0.1.0.1` through `D.0.1.0.N`**.

These ISA addresses are now **permanently dark**: they exist in the granfilade pointing to text content, but no POOM in any document contains a V→I mapping to them. They consume ISA space and deflect future allocations but are unreachable from any document's V-address.

**Scenario B (orphaned GRANORGL, the actual `createenf` scenario):** Depends on which hint path was used.

For a new sibling document (ACCOUNT→DOCUMENT, depth=2 in `findisatoinsertnonmolecule` [granf2.c:209]): the new document's ISA `D2 = A.0.M2` where M2 > any existing document number. For text search under existing document `D1 = A.0.M1` (where M1 < M2), `upperbound = D1.0.2`. Comparing mantissa at position `idx`: D2 has `M2 > M1` at that position, while `D1.0.2` has `M1`. So `D2 > upperbound`. **The orphaned GRANORGL is NOT found by `findpreviousisagr` for text insertions into D1.** The orphaned entry only affects `findisatoinsertnonmolecule` for future document creation.

For a new document version (DOCUMENT→DOCUMENT, depth=1 in `findisatoinsertnonmolecule` [granf2.c:209]): the version ISA is `D.0.1` (one level deeper). Since `D.0.1 < D.0.2` (the text upperbound), the orphaned version GRANORGL at `D.0.1` **IS found** by `findpreviousisagr`. The `findlastisaincbcgr` returns its base ISA `D.0.1` unchanged (it's a GRANORGL, not GRANTEXT). Then `findisatoinsertmolecule` for TEXTATOM allocates `tumblerincrement(D.0.1, 0, 1) = D.0.2`, which equals the upper bound and lies outside the intended text atom range (`D.0.1.0.*`), corrupting subsequent text address allocation.

---

### No Isolation, No Rollback

There is no session isolation in the granfilade. It is a single global in-memory structure referenced by all sessions. Once `insertseq` [granf2.c:99 or granf2.c:125] executes, the entry is immediately visible to every subsequent call from **any session**. There is no transaction layer, no rollback on session drop, and no mechanism to reap an orphaned entry.

An additional timing concern is visible in `fns.c:insert` [fns.c:84–98]:
```c
void insert(typetask *taskptr)
{
    (void) getinsert (taskptr, &docisa, &vsa, &textset);
    putinsert (taskptr);        // ← response sent FIRST [fns.c:91]
    if (!doinsert (taskptr, &docisa, &vsa, textset))   // ← granf written SECOND [fns.c:92]
        ...
}
```

The acknowledgment is sent to the client **before** `doinsert` writes to the granfilade at all — meaning the crash window is actually wide open from the client's perspective even without a TCP drop.

---

### Summary

| Scenario | Orphaned entry type | Found by `findisatoinsertmolecule`? | Effect |
|---|---|---|---|
| Crashed text INSERT | GRANTEXT at `D.0.1.0.K` | **Yes** | Next text allocation placed at `D.0.1.0.(K+textlength)`, skipping orphaned range |
| Crashed new sibling doc (`createenf`) | GRANORGL at `A.0.M2` (M2 > existing) | **No** | Affects only `findisatoinsertnonmolecule` for future document creation |
| Crashed new version (`createenf`, DOCUMENT→DOCUMENT) | GRANORGL at `D.0.1` | **Yes** | Displaces text atom allocation to `D.0.2`, outside the expected text range — address corruption |

**Direct answer to the question:** For the strict `createenf` code path (document creation via `createorglgr`), the orphaned GRANORGL entry affects `findisatoinsertmolecule` only in the DOCUMENT→DOCUMENT version creation case, where the version's ISA (`D.0.1`) falls within the text atom search range. In the more common cross-account/new-document case, the orphaned GRANORGL's ISA is numerically above the text search upper bound and is not seen. For the everyday text-INSERT crash (no `createenf` involved), the orphaned GRANTEXT is always found and does cause the next session's allocation to skip past the orphaned I-address range. In either case there is no recovery path: orphaned entries are permanent.

---

## Question 20 [gregory]

> When multiple sessions are connected and the `writeenfilades` flush occurs at session end, does it flush ALL modified nodes across ALL sessions' operations, or only nodes dirtied by the exiting session — and if the former, could a still-active session's partially-built tree state be written to disk prematurely?

### Gregory's Answer

## KB Synthesis

## Flush Scope and Session Interaction

**`writeenfilades()` flushes ALL modified crums, not just those from the exiting session.**

### Why: The cache is globally shared

From [SS-CACHE-MECHANISM], all enfilades — granfilade, spanfilade, and all document POOMs — share a **single circular doubly-linked list** managed by the `grimreaper` global pointer. There is no per-session dirty set, no session-tagged ownership on crums, and no separation between "session A's work" and "session B's work." The cache is a single pool of all in-memory crums across all concurrent connections.

`writeenfilades()` at `bed.c:134` recursively walks the granfilade and spanfilade trees writing all crums with `modified = TRUE`. It has no mechanism to distinguish which session dirtied which crum.

### When it fires: daemon shutdown, not per-session exit

From [SS-DURABILITY-BOUNDARY], `writeenfilades()` is called "during daemon shutdown" — specifically `bed.c:134,183`. The daemon is a single process with up to 25 connections (MAX_PLAYERS) multiplexed via `select()`. If sessions A, B, and C are connected and C disconnects, the daemon continues running for A and B; `writeenfilades()` is not triggered. The flush fires when the daemon itself terminates.

This means if the daemon is killed while sessions remain active, only crums previously evicted by the grim reaper survive — everything else in RAM is lost [SS-DURABILITY-BOUNDARY].

### The grim reaper path: also global, fires mid-operation

There is a second flush path: when `ealloc` fails during memory allocation, `grimlyreap()` scans the entire shared crum list for crums with `age >= OLD` and `age != RESERVED`, writes modified ones via `orglwrite()`, and frees them [SS-CACHE-MECHANISM]. This fires during normal operation — potentially while another conceptual "session's" prior work sits in RAM alongside the current operation's in-progress crums.

### Protection against partial state: RESERVED, not session scope

Your concern about "a still-active session's partially-built tree state being written prematurely" has a partial answer.

Within a single atomic operation, crums currently being manipulated can carry `age == RESERVED`. The grim reaper's `isreapable` check skips these [FC-RESERVED-CRUM]. Since the event loop is single-threaded and run-to-completion [INV-ATOMICITY] [INV-SEQUENTIAL-DISPATCH], when `grimlyreap()` fires it is always called from within the currently-executing operation — all *previous* operations have already completed and their state is fully consistent. The grim reaper will only flush crums from completed past operations (age advanced past RESERVED) while protecting crums currently in use by the running operation (age == RESERVED).

So the risk is not "another session's in-flight partial state gets flushed" — there is no interleaving. The risk is [EC-CRASH-MID-WRITE]: within a single operation's `subtreewriterecurs()` flush, a crash after writing children but before writing the parent leaves the on-disk tree with orphaned blocks, because there is no atomic commit or fsync.

### Summary

| Question | Answer |
|----------|--------|
| Does flush cover all sessions' work? | Yes — single shared cache, no per-session distinction |
| When does `writeenfilades()` fire? | Daemon shutdown only, not per-session exit |
| Can a running operation's in-flight crums be prematurely flushed? | No — RESERVED flag + single-threaded atomicity prevents this |
| Can completed-but-not-yet-flushed work from any session be flushed by grim reaper? | Yes — age-based, not session-based eviction |
| Is the on-disk state consistent after grim reaper eviction? | Yes for the evicted subtrees individually; no cross-enfilade atomicity guarantee |

## Code Exploration

Now I have everything I need to give a complete answer. Let me compile the full analysis:

---

## `writeenfilades` Flush Scope: Global, Session-Blind, and Potentially Premature

### Short Answer

`writeenfilades()` flushes **all modified nodes across all sessions' operations** — it is unconditionally process-global. There is no session attribution on the `modified` flag and no per-session dirty tracking. Yes, a still-active session's partially-built tree state **can** be written to disk prematurely if the flush is triggered by SIGINT.

---

### 1. `granf` and `spanf` Are Process-Global Singletons

```c
// corediskout.c:21-22
typegranf granf;
typespanf spanf;
```

Externed as:
```c
// xanadu.h:14,16
extern typegranf granf;
extern typespanf spanf;
```

There is exactly one `granf` and one `spanf` for the entire backend process. The multi-user daemon (`bed.c`) uses `select()` to multiplex multiple frontend connections (`bed.c:110-143`), but they all share the same address space and thus the same global enfilades. Sessions are not separate processes and do not have separate tree roots.

---

### 2. `writeenfilades()` Is Unconditionally Global

```c
// corediskout.c:68-88
int writeenfilades(void)
{
  typecbc temporgl;

	temporgl.leftbroorfather = NULL;
	temporgl.modified = TRUE;
	temporgl.cinfo.granstuff.orglstuff.orglincore = TRUE;
	temporgl.cinfo.granstuff.orglstuff.diskorglptr.diskblocknumber = GRANFDISKLOCATION;
	...
	temporgl.cinfo.granstuff.orglstuff.orglptr = (typecuc *)granf;
	((typecuc *)granf)->leftbroorfather = (typecorecrum *)&temporgl;
	orglwrite (&temporgl);  // writes entire granf tree
	      
	temporgl.modified = TRUE;
	...
	temporgl.cinfo.granstuff.orglstuff.orglptr = (typecuc *)spanf;
	((typecuc *)spanf)->leftbroorfather = (typecorecrum *)&temporgl;
	orglwrite (&temporgl);  // writes entire spanf tree
}
```

It takes no parameters. It constructs two synthetic `typecbc` root pointers — one into the global `granf`, one into the global `spanf` — and calls `orglwrite()` on each. `orglwrite()` calls `subtreewriterecurs()` (`corediskout.c:426-494`), which recurses depth-first through the tree writing any node whose `modified` bit is `TRUE`.

---

### 3. The `modified` Flag Is Per-Node, Never Per-Session

```c
// enf.h:34 (inside struct structcorecrumhedr)
bool modified BIT;
```

This is set by `ivemodified()`, which propagates `TRUE` up the tree from any changed leaf to all its ancestors:

```c
// genf.c:522-543
int ivemodified(typecorecrum *ptr)
{
  bool fatherflag;
    ...
    fatherflag = TRUE;
    while (ptr) {
        rejuvinateifnotRESERVED (ptr);
        if (fatherflag) {
            ptr->modified = TRUE;  // genf.c:539
        }
        fatherflag = ptr->isleftmost;
        ptr = ptr->leftbroorfather;
    }
}
```

`ivemodified()` is called by every structural mutation — inserts, splits, wid/dsp recalculations (`wisp.c:210`, `credel.c:575`, `split.c:149`). The `modified` bit carries no session identity. When Session A modifies a node, it looks identical to Session B modifying the same node — the bit is either set or unset, with no provenance.

---

### 4. Where `writeenfilades()` Is Called in the Multi-User Daemon

There are three call sites in `bed.c` / `corediskout.c`:

**A. `diskflush()` between sessions — the ONLY safe flush:**
```c
// bed.c:104-108
if (n_players < 1) {
    diskflush();   // bed.c:105 — "Write out everything when no one around"
    mightbeblocked = TRUE;
    new_players(player, &n_players, TRUE, &task);
    ...
}
```
```c
// corediskout.c:57-64
/* Update disk copy of all enfilades, and reset core versions for multiuser */
int diskflush(void)
{
  void initkluge();
    writeenfilades();
    initkluge((typecuc**)&granf, (typecuc**)&spanf);  // reload from disk!
}
```
This is safe because it only fires when all sessions have disconnected (`n_players == 0`). Critically, it also calls `initkluge()` afterward, which re-reads `granf` and `spanf` from disk into fresh in-core structures — resetting state for the next session. `initkluge()` (`corediskin.c:18-41`) constructs brand-new in-core trees by reading from `GRANFDISKLOCATION` and `SPANFDISKLOCATION`.

**B. `quitafteruser` path — fires after one request, while other sessions may be connected:**
```c
// bed.c:128-137
xanadu(&task);
if (quitafteruser) {
    ...
    writeenfilades();   // bed.c:134
    closediskfile();
    exit(0);
}
```
`quitafteruser` is set to `TRUE` by `flagquitting()` (the SIGINT handler) when the backend is actively serving a request — it defers the quit until after the current request finishes. But it does NOT check whether other sessions are active. As soon as the current request completes, all in-core state from all sessions is flushed and the process exits.

**C. SIGINT while blocked in `select()` — immediate unconditional flush:**
```c
// bed.c:175-188
void flagquitting()
{
    signal(SIGINT, SIG_IGN);
    if (mightbeblocked) {
        ...
        writeenfilades();   // bed.c:183
        closediskfile();
        exit(0);
    } else
        quitafteruser = TRUE;
}
```
`mightbeblocked` is `TRUE` when the main loop is sitting in `select()` waiting for any session to send input. If SIGINT fires here, the flush and exit happen immediately, mid-stream for any session that is connected but hasn't sent a request yet.

---

### 5. The `diskexit()` / `decrementusers()` Guard — Limited Scope

```c
// corediskout.c:37-54
static int indiskexit(void)
{
    if (decrementusers()) {  // returns TRUE if n_players > 1
        return(0);           // skip the flush, just decrement
    }
    writeenfilades();
    closediskfile();
    exit(0);
}
```
```c
// bed.c:236-242
bool decrementusers(void)
{
    if (n_players > 1) {
        player[user].wantsout = 1;
    }
    return (n_players > 1);
}
```

This guard prevents `diskexit()` from triggering a flush while other sessions are active. But in daemon mode, individual session quit (`FEBE QUIT`) does NOT call `diskexit()` at all:

```c
// fns.c:419-432
void quitxanadu(typetask *taskptr)
{
    putquitxanadu(taskptr);
    if (!backenddaemon) {
        ...
        diskexit();          // single-user mode only
    } else
        dobertexit(user);    // daemon mode: only clean up bert entries, no flush
}
```

So in the daemon, individual session disconnects are handled by `dobertexit(user)` (`bert.c:339-345`), which cleans up the session's open-document table but does NOT flush enfilades. The flush is deferred until `n_players == 0`.

---

### 6. Answer to the Core Question: Can a Still-Active Session's Partial State Be Written Prematurely?

**Yes, under specific conditions:**

| Scenario | Sessions Active | Flush Triggered | Partial State Written? |
|----------|-----------------|-----------------|----------------------|
| Last session quits (`n_players → 0`) | None | `diskflush()` at `bed.c:105` | No — no active sessions |
| FEBE `QUIT` from one of many sessions | Others still active | No flush (daemon path skips to `dobertexit`) | No flush occurs |
| SIGINT while backend blocked in `select()` | Any | `flagquitting()` at `bed.c:183` | **Yes** |
| SIGINT while backend serving a request | Any | `quitafteruser` fires after current request at `bed.c:134` | **Yes** — other sessions' partial nodes included |

The structural hazard is:

1. Session A sends a multi-step operation (e.g., insert text then create a link). After the insert, the granf contains new nodes with `modified = TRUE`. Session A has not yet sent the link creation request.
2. Session B sends a QUIT request.
3. The backend processes Session B's QUIT, which sets `quitafteruser = TRUE`.
4. After Session B's request completes, `writeenfilades()` runs at `bed.c:134`.
5. Session A's partially-modified tree — with the new text nodes but no link yet — is flushed to disk.

There is no per-operation transaction, no rollback mechanism, and no way for `writeenfilades()` to skip nodes that "belong to" a session with unfinished business. The `modified` bit is purely structural.

---

### 7. `diskflush()` vs `writeenfilades()`: The Intended Multi-User Mechanism

The distinction between `diskflush()` and raw `writeenfilades()` is precisely this multiuser reset:

```c
// corediskout.c:57-64 — "reset core versions for multiuser"
int diskflush(void)
{
    writeenfilades();
    initkluge((typecuc**)&granf, (typecuc**)&spanf);  // re-read from disk
}
```

`diskflush()` is designed to be called between sessions: flush everything, then reload clean state. Calling `writeenfilades()` alone (as the SIGINT paths do) writes to disk but leaves the in-core tree in a potentially inconsistent partially-modified state — though that's moot if the process is about to `exit(0)`.

The absence of `initkluge()` after the SIGINT-triggered `writeenfilades()` calls is not a bug per se — the process exits immediately after. But it does confirm that those flush points were designed for process termination, not for mid-operation session handoff.

---

### Summary

`writeenfilades()` is unconditionally global: it walks the entire shared `granf`/`spanf` tree and persists every node whose `modified` bit is set, regardless of which session caused the modification. There is no session-scoped dirty tracking anywhere in the codebase. The multi-session safety in `bed.c`'s daemon mode relies entirely on the guarantee that `diskflush()` — the only flush that also resets in-core state — fires only when `n_players == 0`. But the SIGINT-triggered flush paths at `bed.c:134` and `bed.c:183` do not have this guarantee: they write all in-core modified state and exit, potentially committing partially-built tree structures from sessions that never got a chance to complete their operations.
