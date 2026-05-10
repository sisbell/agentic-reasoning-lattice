# Consultation Answers — Distributed Replication Consistency

**Inquiry:** What must a multi-server Xanadu deployment guarantee about the convergence of replicated global state? How do the system's structural properties constrain the replication model?
**Date:** 2026-02-24 13:53
**Questions:** 15 (10 nelson, 5 gregory)

---

## Question 1 [nelson]

> Since content, once stored, can never be deleted or altered, does this mean two servers that each accept new material can never contradict each other — only be at different stages of completeness?

### Nelson's Answer

## Yes — Precisely So

Two Xanadu servers that each accept new material can never contradict each other. They can only be at different stages of completeness. This is not an accident but a consequence of three properties working together.

### 1. Content Is Immutable Once Created

I-space is append-only. A byte stored at an I-address never changes:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

This means if Server A and Server B both know about I-address X, they must agree on its content. There is no mechanism by which the value at X could differ between them.

### 2. The Addressing System Prevents Collisions

The tumbler baptism mechanism ensures that only the owner of an address subtree can create content there:

> "The basic principle is that of owned numbers. Numbers are owned by individuals or companies, and subnumbers under them are bestowed on other individuals and companies on whatever basis the owners choose. Whoever owns a specific node, account, document or version may in turn designate (respectively) new nodes, accounts, documents and versions, by forking their integers." [LM 4/17]

Server 1 creates addresses under prefix `1.x`, Server 2 under prefix `2.x`. Account 1.3 creates documents under `1.3.x`. No two independent actors can assign the same address to different content because they operate in disjoint subtrees. This eliminates the possibility of address collision without coordination.

### 3. The Docuverse Only Grows

> "New items may be continually inserted in tumbler-space while the other addresses remain valid." [LM 4/19]

Nothing is ever removed from I-space. "Deletion" is a V-space operation that changes the document's current arrangement, not an I-space operation that destroys content.

### The Consequence: Conflict-Free Replication

When Server B receives information from Server A, every piece of that information is either:

- **Content at an address B hasn't seen before** — new knowledge, accepted without conflict
- **Content at an address B already knows** — must be identical by immutability, so it's a no-op

This is exactly why Nelson could describe content flowing between servers so casually:

> "A server's network model, from the null case on up, is at all times unified and operational; whatever information moves between servers is assimilated at once to its overall structure, leaving each server in canonical operating condition with a slightly improved map of what is elsewhere. The contents can slosh back and forth dynamically." [LM 4/72]

The phrase "assimilated at once" is telling — there is no merge conflict to resolve, no reconciliation needed. New information simply fills in gaps. Each server is "a microcosm that shrinks and grows" [LM 4/71], and growth is always monotonic and consistent.

### What About V-Space (Document Arrangements)?

V-space arrangements do change — editing rearranges the V-to-I mapping. But each document has a home server determined by its tumbler address, and only the owner can modify it. Two servers cannot independently edit the same document's V-space. Other servers holding cached copies may be temporarily stale, but never contradictory — they hold an older-but-valid snapshot, and the home server is authoritative.

### What About Links?

Links follow the same pattern. They have permanent I-addresses in the link subspace, are created by their owners, and once created are immutable. Two servers can differ in which links they know about, but never disagree about a link's content.

### The Design Pattern

Nelson designed — whether by insight or by instinct — what modern distributed systems theory calls a **conflict-free replicated data type**. Specifically, the docuverse's permanent layer is a product of grow-only sets: the set of I-space content only grows, the set of links only grows, and the addressing system partitions creation authority so that no coordination is needed. The result is that "different stages of completeness" is the only possible form of divergence between servers, exactly as you describe.

This is also why Nelson could envision a network that "assumes networks are always broken" [LM 4/75] without worrying about consistency. When the only operation is monotonic addition with non-overlapping address authority, disconnection creates incompleteness, never inconsistency.

---

## Question 2 [nelson]

> Every piece of content receives a permanently unique address at the moment of creation. What must the system guarantee so that two servers, acting independently, never assign the same address to different content?

### Nelson's Answer

## Address Uniqueness Without Coordination

The system guarantees collision-free addressing through **hierarchical partitioning by ownership**. The mechanism has two layers: disjoint prefixes between servers, and sequential allocation within each prefix.

### The Owned-Number Principle

Every tumbler address is a path through an ownership tree. The four-field structure—

```
Node.0.User.0.Document.0.Element
```

—encodes, at each level, *who controls the allocation of the next level down*:

> "The basic principle is that of owned numbers. Numbers are owned by individuals or companies, and subnumbers under them are bestowed on other individuals and companies on whatever basis the owners choose. Whoever owns a specific node, account, document or version may in turn designate (respectively) new nodes, accounts, documents and versions, by forking their integers. We often call this the 'baptism' of new numbers." [LM 4/17]

> "The owner of a given item controls the allocation of the numbers under it." [LM 4/20]

### Between Servers: Disjoint Subtrees

Each server node has a unique number in the first field. All content created on that server lives under that prefix. Server 1.2 creates addresses beginning `1.2.0....`; server 1.3 creates addresses beginning `1.3.0....`. These subtrees are disjoint by construction—no address can belong to two different prefixes.

> "The server address always begins with the digit 1, since all other servers are descended from it. This may seem an unnecessary redundancy, but it permits referring to the entire docuverse by '1' on the first position." [LM 4/28]

The only coordination point is the initial "baptism" of a new server's node number, which requires its parent's owner to allocate it. After that one-time assignment, the server operates independently forever:

> "A server node, or station, has ancestors and may have possible descendant nodes. An account, too, and a document, all have possible descendants." [LM 4/19]

### Within a Server: Sequential Forking

Within its own subtree, a server allocates accounts, documents, and content positions by **successive forking**—appending the next sequential digit:

> "One digit can become several by a forking or branching process. This consists of creating successive new digits to the right; we call these 'under' the previous digit." [LM 4/20]

> "For instance, if there is an item 2, it can branch into several more items, each of which is a daughter item. Thus 2.1, 2.2, 2.3, 2.4... are successive items being placed under 2." [LM 4/20]

Account 1.2.0.3 creates documents 1.2.0.3.0.1, then 1.2.0.3.0.2, then 1.2.0.3.0.3—monotonically advancing. No digit is ever reused.

### Why This Suffices

The guarantee rests on three properties:

1. **Prefix disjointness.** Distinct servers have distinct node numbers, so their entire address subtrees are disjoint. Two servers cannot produce the same address because their addresses begin differently.

2. **Monotonic allocation.** Within any owned subtree, new items receive strictly increasing numbers. The counter advances; it never retreats or reuses a value. This prevents collision within a single server.

3. **Ownership containment.** No entity can allocate addresses outside its own subtree. A server cannot "baptize" accounts under another server's prefix. An account cannot create documents under another account's prefix.

> "Typically, the user will have no control over the node address he, she or it is assigned; but once assigned a User account, the user will have full control over its subdivision forevermore." [LM 4/29]

Together these mean: the system partitions the infinite address space into non-overlapping regions at every level of the hierarchy. Each owner independently fills their region by counting upward. No coordination is needed because no two owners share any region.

> "New items may be continually inserted in tumbler-space while the other addresses remain valid. This means that any address of any document in an ever-growing network may be specified by a permanent tumbler address." [LM 4/19]

### The Docuverse as One Forking Tree

Nelson sees this as a single unified structure:

> "So the docuverse is all really one big forking document." [LM 4/18]

> "The entire tumbler works like that: nodes can spin off nodes; accounts can spin off accounts; nodes can spin off accounts; and so on. Thus all numeration in the docuverse is compressed into a single mechanism." [LM 4/19]

The tumbler line—the depth-first linearization of this tree—gives every position a unique, permanent, globally unambiguous address. And because the tree grows only by appending new leaves (never by reassigning existing ones), uniqueness is preserved for all time without any server ever needing to ask another "is this address taken?"

---

## Question 3 [nelson]

> If a user creates a document on one server and another user creates a link to that document's content from a different server, must both servers eventually agree that the link exists and points to the same content?

### Nelson's Answer

## Cross-Server Link Agreement

The short answer: **they must agree on what the link points to** (this is guaranteed by the architecture), but **they need not simultaneously agree that the link exists** (discovery is eventual, not instantaneous).

### Content Agreement Is Guaranteed by Architecture

The link's endsets contain tumbler addresses pointing to I-space content. I-space content is permanent and immutable. There is exactly one piece of content at any I-address, and it never changes. So there is nothing to "agree on" — the tumbler address resolves to one thing universally.

> "New items may be continually inserted in tumbler-space while the other addresses remain valid. This means that any address of any document in an ever-growing network may be specified by a permanent tumbler address." [LM 4/19]

The link lives on Server 2 (in User B's document). Its endsets contain tumbler addresses that encode Server 1 in the Node field. Both servers use the same universal address space. The content at those addresses is determined by the addresses themselves, not by server-local interpretation.

### Link Existence Is Discoverable, Not Synchronized

The link is a first-class object stored in User B's home document on Server 2. Server 1 does not store the link. But Nelson requires that readers of User A's document on Server 1 be able to discover it:

> "The reader should be able to ask, for a given document or place in the document, 'What connects here from other documents?' — and be shown all these outside connections without appreciable delay." [LM 2/46]

This cross-server discovery happens through BEBE:

> "The function of BEBE is to meld the contents of separate Xanadu servers into a single unified space. This is done basically in two ways." [LM 4/70]

> "First, by the forwarding of requests as they fan out from users to servers able to supply..." [LM 4/70]

Nelson's subrepresentation model describes how servers build progressive knowledge of remote content:

> "A server's network model, from the null case on up, is at all times unified and operational; whatever information moves between servers is assimilated at once to its overall structure, leaving each server in canonical operating condition with a slightly improved map of what is elsewhere. The contents can slosh back and forth dynamically." [LM 4/72]

And one of the explicit purposes of inter-server material movement is index replication:

> "Material is moved between servers for a number of purposes: 1. for more rapid access to final material, 2. for more rapid access to needed material which indexes material on other servers, 3. for rebalance in keeping with demand, 4. for redundancy and backup purposes." [LM 4/71]

Point 2 directly addresses this: link index information migrates between servers so that Server 1 can discover links that live on Server 2.

### The System Assumes Partial Availability

Nelson explicitly designs for broken networks:

> "It is a truism that 'computer networks are always broken.' Meaning that on the average some nodes are disconnected or not working." [LM 4/75]

This means the architecture cannot require synchronous agreement. If Server 2 is temporarily unreachable, Server 1 cannot discover User B's link — but the link still exists, still points to the same content, and will become discoverable when connectivity is restored.

### Summary

| Question | Answer |
|----------|--------|
| Must both agree on what the link points to? | **Yes** — guaranteed by universal tumbler addressing and I-space immutability |
| Must both agree the link exists? | **Eventually** — through BEBE forwarding and subrepresentation caching |
| Must agreement be simultaneous? | **No** — the system is designed for partial availability |
| Can agreement be permanent once reached? | **Yes** — links are permanent objects at permanent addresses |

Nelson does not use the term "eventual consistency," but his architecture describes exactly that: each server maintains a continuously valid but progressively improving model of the whole docuverse, with information flowing between servers as connectivity and demand permit. The link on Server 2 is authoritative from the moment of creation; Server 1's awareness of it grows over time through the BEBE protocol.

---

## Question 4 [nelson]

> When a new version of a document is created on one server, must every other server in the network eventually recognize that version as part of the document's history, or can servers legitimately disagree about which versions exist?

### Nelson's Answer

## Version Recognition Across Servers

Nelson's answer is clear in principle but deliberately vague in mechanism: **the docuverse is one unified space, and a version that exists anywhere exists everywhere conceptually** — but servers are not required to proactively replicate or even know about every version. Discovery is demand-driven, not broadcast-driven.

### The Unified Space Principle

Nelson is unambiguous that users experience one docuverse, not a federation of repositories:

> "The function of BEBE is to meld the contents of separate Xanadu servers into a single unified space." [LM 4/70]

A new version, once created, has a permanent tumbler address whose document field "will indicate its ancestry" [LM 4/66]. That address exists in the docuverse from the moment of creation. No server can legitimately deny its existence — there is no mechanism for "rejecting" an address that another server has validly assigned.

### But Servers Hold Subsets, Not the Whole

Each server maintains a partial view:

> "Each server contains a map and a subset of the whole — a microcosm that shrinks and grows." [LM 4/71]

> "Each server contains a continuously valid model or subrepresentation of the entire docuverse and (because of tumbler addressing) a model of the entire network." [LM 4/72]

A server may be **unaware** of a new version — it may not have the content and may not even know the address exists yet. This is not disagreement; it is incomplete knowledge. The subrepresentation is "continuously valid" in the sense that what it knows is correct, not that it knows everything.

### Demand-Driven Discovery, Not Broadcast

Nelson's model is that content flows toward demand, not that creation triggers global notification:

> "whatever information moves between servers is incremental on its overall structure, leaving each server in canonical operating condition with a slightly improved map of what is elsewhere. The contents can slosh back and forth dynamically." [LM 4/72]

When someone requests a version that the local server doesn't have, the request is forwarded:

> "First, by the forwarding of requests as they fan out from users to servers able to supply; and the pass-through of material that is returned to the requesting user in reply." [LM 4/70]

After fulfillment, the local server's map improves — it now knows about that content. Popular versions replicate closer to users; obscure ones stay at their origin until requested.

### The "Always Broken" Assumption

Nelson explicitly designs for partial connectivity:

> "It is a truism that 'computer networks are always broken.' Meaning that on the average some nodes are disconnected or not working." [LM 4/75]

This means that at any given moment, some servers cannot reach others. A newly created version on a disconnected server is invisible to the rest of the network until connectivity is restored. Nelson treats this as normal operation, not as an error state.

### Ancestry Is Structural, Not Negotiated

The tumbler address of a version **encodes** its ancestry through the document field:

> "The Document field of the tumbler may be continually subdivided, with new subfields in the tumbler indicating daughter documents and versions." [LM 4/29]

> "In a sense the version, or subdocument number is only an accidental extension of the document number, and strictly implies no specific relationship of derivation." [LM 4/29]

Any server that encounters the address can parse the ancestry relationship without consulting the origin server. The relationship is in the address itself, not in metadata that must be propagated.

### What Nelson Does NOT Specify

Nelson leaves the BEBE protocol deliberately undefined:

> "BEBE (Back End-Back End) is the protocol for connecting nodes of the Xanadu network. It is still undergoing definition and will not be made public anytime soon." [LM 4/70]

He does not specify:
- Whether version creation triggers any notification to other servers
- An explicit consistency model (eventual consistency, causal consistency, etc.)
- Whether the original document's home server must be notified of derivative versions
- How the "map" at each server is updated (push, pull, or pure demand)
- Timeout or staleness guarantees for the subrepresentation

### Summary

Servers cannot **legitimately disagree** about which versions exist — the docuverse is definitionally unified. But they can legitimately be **temporarily unaware**. Nelson's design is:

| Question | Answer |
|----------|--------|
| Can a server deny a version exists? | No — addresses are permanent and universal |
| Must every server know about every version? | No — servers hold subsets |
| Will every server eventually learn? | Only if demand drives discovery there |
| Can a disconnected server be out of date? | Yes — "networks are always broken" |
| Is ancestry negotiated between servers? | No — it's encoded in the tumbler address |

The model is closer to **eventual discovery** than eventual consistency: a version becomes known to a server when someone asks for it, not through a background replication protocol. Nelson trusts the demand-driven "sloshing" of content to make the unified docuverse practically accessible without requiring global synchronization.

---

## Question 5 [nelson]

> Must the order in which independently created documents and links become visible be the same on every server, or does the design only require that the final accumulated state converge?

### Nelson's Answer

## Convergence, Not Ordering

Nelson's design requires only that the final accumulated state converge. He does not specify — and several design elements actively preclude — a global ordering on when independently created content becomes visible across servers.

### The Subrepresentation Model

The core evidence comes from Nelson's description of how servers relate to the whole:

> "Each server contains a map and a subset of the whole — a microcosm that shrinks and grows." [LM 4/71]

> "A server's network model, from the null case on up, is at all times unified and operational; whatever information moves between servers is assimilated at once to its overall structure, leaving each server in canonical operating condition with a slightly improved map of what is elsewhere. The contents can slosh back and forth dynamically." [LM 4/72]

Two servers can hold different subsets at the same moment. Each must be in "canonical operating condition" — a *local* validity property, not a globally ordered one. Content arrives incrementally and is "assimilated at once," but the order of assimilation across servers is unconstrained.

### Broken Networks Are Expected

> "It is a truism that 'computer networks are always broken.' Meaning that on the average some nodes are disconnected or not working." [LM 4/75]

If some nodes are routinely disconnected, they cannot observe the same visibility sequence as connected nodes. Nelson treats this as a design parameter, not an exceptional condition. The system must function correctly despite it.

### Content Moves on Demand, Not in Sequence

The BEBE protocol moves content between servers for performance and reliability reasons:

> "Material is moved between servers for a number of purposes: 1. for more rapid access to final material, 2. for more rapid access to needed material which indexes material on other servers, 3. for rebalance in keeping with demand, 4. for redundancy and backup purposes." [LM 4/71]

And the forwarding mechanism is demand-driven:

> "First, by the forwarding of requests as they fan out from users to servers able to supply..." [LM 4/70]

Content migrates toward users who request it. There is no broadcast protocol that pushes new content to all servers in a fixed order.

### Ghost Elements Prove Ordering Is Unnecessary

Nelson explicitly supports references to content that doesn't yet exist locally:

> "It is possible to link to a node, or an account, even though there is nothing stored in the docuverse corresponding to them." [LM 4/23]

> "Indeed, there is no need for the presence of elements at the addresses specified. Link types may be ghost elements." [LM 4/45]

If a link can validly point to an address where nothing is stored, then a server can hold a link before it holds the link's target. This means the system is correct even when visibility order differs from creation order. Ghost elements are not a degenerate case — they are a named, designed feature.

### Time Is Not Part of the Address

> "Note that 'time' is not included in the tumbler. Time is kept track of separately." [LM 4/18]

Tumbler addresses encode provenance (server, account, document, element) but not temporal order. Two documents created seconds apart on different servers have addresses that reflect their ownership hierarchy, not their creation sequence. Since the addressing system — the system's fundamental identity mechanism — is time-free, it cannot impose a temporal ordering requirement.

### Permanence Is a State Property, Not an Ordering Property

The permanence guarantee is:

> "New items may be continually inserted in tumbler-space while the other addresses remain valid. This means that any address of any document in an ever-growing network may be specified by a permanent tumbler address." [LM 4/19]

This says that once an address exists, it remains valid forever. It does not say that all servers must observe the address's creation at the same moment or in the same relative order with respect to other addresses.

### What IS Required: Local Validity

Nelson's "canonical operating condition" means each server must be internally consistent at all times. The server's subset of the docuverse must be a valid subset — but it need not be the same subset as any other server's, nor must it have arrived in the same order.

The fundamental guarantees (permanence, attribution, link survivability, version history) are all properties of the *accumulated state*, not of the *arrival sequence*:

- Permanence: an address, once created, never becomes invalid — a monotonic growth property
- Attribution: origin is encoded in the I-address — a structural property independent of observation order  
- Link survivability: links attach to I-space bytes — unaffected by when a server learns about them
- Version history: all versions persist — an accumulation property

### Summary

Nelson designs for convergence: every server eventually contains or can reach any content in the docuverse. He does not design for global ordering: the sequence in which independently created content appears on different servers is unconstrained. The combination of subrepresentations, broken networks, demand-driven content migration, ghost elements, and time-free addressing constitutes a design that is fundamentally order-independent. Each server must be locally valid at all times and globally convergent over time.

---

## Question 6 [nelson]

> If two users on different servers each create a new version of the same document simultaneously, does the design require that these versions be ordered, or can they coexist as parallel branches in the version history?

### Nelson's Answer

## Parallel Branches, Not Required Ordering

Nelson's design explicitly allows — and expects — versions to coexist as parallel branches without any ordering requirement. Multiple pieces of evidence converge on this.

### No Privileged Version

Nelson is direct on this point:

> "There is thus no 'basic' version of a document set apart from other versions—'alternative' versions—any more than one arrangement of the same materials is a priori better than other arrangements." [LM 2/19]

The prismatic metaphor reinforces this: content "refracts" into different views, all equally valid. There is no trunk, no mainline, no canonical ordering.

### The Tumbler System Eliminates Coordination

When two users on different servers each create a version, the tumbler addressing system ensures they never collide. There are two distinct mechanisms at play:

**Owner-created versions** are subdocuments under the original document's address. The owner controls allocation:

> "The owner of a given item controls the allocation of the numbers under it." [LM 4/20]

Since only the owner creates versions under the document's address space, this case is inherently sequential — one owner, one allocation counter.

**User-created derivative versions** (the more relevant case for your question) are independent documents under each user's own account. Nelson describes this explicitly:

> "Another user, however, is free to create his or her own alternative version of the document he or she does not own. This, then, becomes a windowing document using the shared materials by including them. We may call this versioning by inclusion." [LM 2/37]

Alice's version lives at Alice's tumbler address. Bob's version lives at Bob's. They are parallel documents in different parts of the tumbler tree, requiring zero coordination between servers.

### Version Numbers Don't Imply Derivation

Even the address structure refuses to impose ordering:

> "In a sense the version, or subdocument number is only an accidental extension of the document number, and strictly implies no specific relationship of derivation." [LM 4/29]

The version number is a locator, not a sequence number. Two versions with consecutive numbers are not necessarily in a parent-child relationship.

### Comparison, Not Convergence

The system provides SHOWRELATIONOF2VERSIONS to compare versions:

> "This returns a list of ordered pairs of the spans of the two spec-sets that correspond." [LM 4/70]

This operation exists to help users **intercompare** divergent versions:

> "A facility that holds multiple versions of the same material, and allows historical backtrack, is not terribly useful unless it can help you intercompare them in detail — unless it can show you, word for word, what parts of two versions are the same." [LM 2/20]

The design provides tools for **seeing differences**, not for **resolving them into a single version**. Nelson envisions divergence and comparison, not convergence. Merge is a front-end semantic concern, not a system-level operation — there is no MERGE command in the FEBE protocol.

### The BEBE Protocol Doesn't Order Versions

The inter-server protocol (BEBE) melds servers into a unified address space:

> "The function of BEBE is to meld the contents of separate Xanadu servers into a single unified space." [LM 4/70]

But this unification is about **addressability**, not about **ordering or conflict resolution**. Each server's microcosm grows and shrinks with demand, content "sloshes back and forth," but there is no mechanism specified for establishing a total order on concurrent version creation events across servers.

### Summary

The design answer is unambiguous: **parallel branches coexist.** Two users on different servers creating versions simultaneously produce two independent documents, each at its own tumbler address, each equally valid, with no ordering relationship required. The system provides correspondence and comparison tools so users can see how the versions relate, but imposes no canonical ordering and specifies no merge operation. This follows directly from Nelson's vision that literature is an ever-growing web of interconnected alternatives, not a linear sequence of authoritative states.

---

## Question 7 [nelson]

> A document built entirely from shared content — transclusions of material stored elsewhere — depends on that material being findable. What must the network guarantee about the availability of content that other documents reference?

### Nelson's Answer

# Network Availability Guarantees for Transcluded Content

A compound document built entirely from transclusions is, by design, a set of references into I-space content stored at other documents' home locations. If any referenced content becomes unretrievable, the compound document breaks — not gracefully, but fundamentally, since it *has* no local content to fall back on. Nelson addresses this dependency through several interlocking guarantees.

## 1. Transclusion Requires Live Content

The entire point of transclusion is that content is fetched from its origin, not copied:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

> "No copying operations are required among the documents throughout the system, and thus we solve the problems of update—especially the problem of updating documents which depend on other documents. We solve this problem simply by windowing to a changing document." [LM 2/36]

This means the network bears the full burden of availability. There is no local fallback. If the home location is unreachable, the transclusion fails.

## 2. The Permanence Obligation on Published Content

Nelson's primary guarantee is social and contractual: published content must stay published.

> "It is in the common interest that a thing once published stay published, as in the world of paper. Other readers and users will come to depend on its accessibility. Consequently its author may not withdraw it except by lengthy due process." [LM 2/43]

The reason is explicitly about dependencies created by others' links and transclusions:

> "However, for corrections and amendments, the author may readily publish a superseding document, but the former version must remain on the network. This is vital because of the links other users may have made to it—which can now reach through from the previous version (to which they were originally attached) into the newer version." [LM 2/43]

Publication is a binding act. The publisher signs a contract agreeing to these terms, and withdrawal requires "one year's notice and fee" [LM 5/20]. The content itself is not voluntarily removable.

## 3. The Network as Unified Space

BEBE (the back-end to back-end protocol) exists precisely to make distributed content appear as one unified space:

> "The function of BEBE is to meld the contents of separate Xanadu servers into a single unified space." [LM 4/70]

The user never specifies which server holds content. Requests fan out automatically:

> "First, by the forwarding of requests as they fan out from users to servers able to supply; and the pass-through of material that is returned to the requesting user in reply." [LM 4/70]

## 4. Replication and Subrepresentation

Each server maintains a partial model of the whole docuverse that grows toward what is needed:

> "Each server contains a continuously valid model or subrepresentation of the entire docuverse and (because of tumbler addressing) a model of the entire network." [LM 4/72]

> "Each server contains a map and a subset of the whole — a microcosm that shrinks and grows." [LM 4/71]

Content migrates toward demand. Material is moved between servers for four purposes Nelson enumerates:

> "1. for more rapid access to final material,
> 2. for more rapid access to needed material which indexes material on other servers,
> 3. for rebalance in keeping with demand,
> 4. for redundancy and backup purposes." [LM 4/71]

Point 4 is critical: the network replicates content for resilience. A compound document's transclusions are not dependent on a single server remaining online.

## 5. Vendor Interoperation Obligations

Storage Vendors are contractually required to serve cross-vendor requests:

> "Storage Vendor agrees to honor requests for material from customers connected to servers operated by other Xanadu-licensed storage vendors, and accept material for storage from other Xanadu-licensed vendors within the network under prevailing arrangements for request and fulfillment of storage rental performed by Back-End Storage Code." [LM 5/14]

This is not voluntary — it is a condition of the franchise license. A vendor who refuses to serve content to other vendors' customers loses their license.

On vendor failure, the contract requires orderly transition:

> "Upon notice of cancellation, Storage Vendor will arrange for the orderly transition of all customer-stored materials to other Xanadu locations." [LM 5/16]

## 6. Resilience Against Partial Failure

Nelson explicitly designs for the reality that networks break:

> "It is a truism that 'computer networks are always broken.' Meaning that on the average some nodes are disconnected or not working." [LM 4/75]

The system handles this through backup copies and forwarding. A thwarted request routes to backup locations. "Not currently available" is the last resort, not the first response.

The canonical state property of each server ensures that partial information is still usable:

> "A server's network model, from the null case on up, is at all times unified and operational; whatever information moves between servers is assimilated at once to its overall structure, leaving each server in canonical operating condition with a slightly improved map of what is elsewhere. The contents can slosh back and forth dynamically." [LM 4/72]

## 7. The Economic Tension

There is one significant qualification. Nelson requires that all services be economically self-sustaining:

> "ALL SERVICES MUST BE SELF-SUPPORTING. Subsidy between one aspect of the system and another could only work temporarily. This means, for example, that archival storage must be economically self-sustaining." [LM 4/5]

Content owners pay ongoing storage rental. If they stop paying, the curated sources do not specify what happens — whether content goes dark, whether a grace period applies, or whether the Author's Fund can intervene. This is a genuine gap in the specification.

For heavily transcluded content, this creates a dependency: many compound documents rely on the continued economic viability of their source material. Nelson's model partially addresses this through royalties — popular content generates revenue that offsets storage costs. But rarely-transcluded content survives only as long as its owner values it enough to keep paying.

## 8. Why Copies Cannot Substitute

Nelson is emphatic that copying is not a solution:

> "Note also that he or she who makes a paper copy or disk is losing all dynamic link connections, and is left with the inert, non-interactive copy. And that will be a considerable deprivation in the world we are talking about." [LM 2/47]

> "Remember the analogy between text and water. Water flows freely, ice does not. The free-flowing, live documents on the network are subject to constant new use and linkage, and those new links continually become interactively available. Any detached copy someone keeps is frozen and dead, lacking access to the new linkage." [LM 2/48]

A compound document that cached its transclusions locally would lose exactly the properties that make transclusion valuable: live connection to the original, automatic attribution, royalty flow, and participation in the evolving web of links.

## Summary

The network must guarantee five things for transcluded content:

| Guarantee | Mechanism | Source |
|-----------|-----------|--------|
| **Content stays published** | Publication contract; withdrawal requires due process | [LM 2/43] |
| **Any server can reach any content** | BEBE forwarding; vendor interoperation contract | [LM 4/70, 5/14] |
| **Content survives node failure** | Replication, backup copies, orderly vendor transition | [LM 4/71, 5/16] |
| **Content migrates toward demand** | Subrepresentation; dynamic caching | [LM 4/72] |
| **Network tolerates partial outage** | "Networks are always broken" — designed for it | [LM 4/75] |

The one unresolved vulnerability is economic: if a content owner stops paying storage rental, Nelson does not specify what happens to the compound documents that depend on that content. The permanence guarantee for published content is strong ("may not withdraw except by lengthy due process"), but the economic sustainability requirement introduces a tension that Literary Machines does not fully resolve.

---

## Question 8 [nelson]

> Does the principle that editing one document must leave all other documents unaffected simplify or constrain how servers propagate changes to each other?

### Nelson's Answer

## Subspace Independence and Server Propagation

The principle that editing one document must leave all others unaffected **overwhelmingly simplifies** how servers propagate changes. It does so by eliminating the hardest problem in distributed systems: propagating mutations of shared state.

### Why It Simplifies: No Distributed Update Problem

Nelson's I-space/V-space separation is the mechanism. Editing changes only V-space (the document's arrangement), which is entirely local to that document. I-space content — which other documents may transclude — is immutable and append-only:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

When Alice on Server 1 edits her document, she is rearranging her V-space mapping. Bob's document on Server 2, which transcludes Alice's content, references I-space addresses. Those addresses still resolve to exactly the same bytes. Server 2 needs no notification whatsoever.

Nelson states this explicitly as a solved problem:

> "No copying operations are required among the documents throughout the system, and thus we solve the problems of update — especially the problem of updating documents which depend on other documents. We solve this problem simply by windowing to a changing document." [LM 2/36]

And the mechanism is clear from the delete semantics:

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

### What BEBE Does NOT Need To Do

Because editing is document-local and I-space is immutable, the BEBE protocol is freed from:

- **Change propagation** — No "document A changed, notify all transclusion dependents"
- **Cache invalidation of existing content** — Cached I-space bytes never become stale
- **Distributed consistency protocols for mutable state** — There is no mutable shared state
- **Conflict resolution** — Two servers cannot have conflicting versions of the same I-space content

This is why Nelson can describe the server model so casually:

> "A server's network model, from the null case on up, is at all times unified and operational; whatever information moves between servers is assimilated at once to its overall structure, leaving each server in canonical operating condition with a slightly improved map of what is elsewhere. The contents can slosh back and forth dynamically." [LM 4/72]

Content can "slosh back and forth" precisely because it is immutable. A server that caches remote content never needs to check whether that content has changed — it hasn't and it can't.

### What BEBE Reduces To

With document-local editing and immutable I-space, BEBE's responsibilities simplify to:

1. **Request forwarding** — Route requests for content to the server that has it: "First, by the forwarding of requests as they fan out from users to servers able to supply" [LM 4/70]

2. **Content replication** — Copy I-space bytes between servers for performance and redundancy. Since content is immutable, replication is trivially correct — a copy is always valid.

3. **New content distribution** — When new bytes are appended to I-space, they may eventually be requested by remote servers. But new bytes are additions, not modifications, so they cannot invalidate anything.

4. **Subrepresentation growth** — "Material is moved between servers for a number of purposes: 1. for more rapid access to final material, 2. for more rapid access to needed material which indexes material on other servers, 3. for rebalance in keeping with demand, 4. for redundancy and backup purposes." [LM 4/71]

All four of these are **additive** operations. Nothing is invalidated, updated, or reconciled.

### The Constraint Side

The simplification is not free. It requires one strict constraint: **I-space must be genuinely immutable across all servers.** If any server allowed modification of existing I-space content, the guarantee would break — other documents' transclusions would silently change meaning, links would point to altered content, and the correspondence relation (shared I-space origin) would become unreliable.

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

Every transclusion resolves by fetching from the "home location." If the home location's content could mutate, every document in the docuverse that transcludes those bytes would be affected. The constraint that I-space is append-only is what makes the simplification possible.

Nelson enforces this through the franchise model — all servers run identical back-end code:

> "Storage Vendor agrees to use software furnished by Project Xanadu without modification." [LM 5/14]

This ensures no rogue server introduces I-space mutation.

### Summary

The principle works as follows: **document-local editing + immutable shared content = no distributed update problem.** This transforms BEBE from a distributed consistency protocol (the hardest kind of distributed system) into a distributed caching and forwarding protocol (among the easiest). The constraint is that I-space immutability must be absolute — but Nelson designed the entire architecture around this from the start.

---

## Question 9 [nelson]

> Links are permanent and their endpoints never change. Does this immutability mean a server can accept and store a link without coordinating with the server that holds the linked content?

### Nelson's Answer

# Link Immutability and Cross-Server Coordination

**Yes.** A server can accept and store a link without coordinating with the server that holds the linked content. This follows directly from several architectural principles Nelson establishes.

## Links Live at Home, Not at Their Targets

A link is stored in its **home document**, which determines ownership — not in the documents it connects:

> "A link need not point anywhere in its home document. Its home document indicates who owns it, and not what it points to. Conversely, links connecting parts of a document need not reside in that document." [LM 4/12]

The MAKELINK operation confirms this:

> "The document must be specified because that determines the actual residence of the link — since a document may contain a link between two other documents." [LM 4/63]

The link is created and stored entirely within the home server's jurisdiction. The target content lives elsewhere and is not consulted.

## Targets Need Not Even Exist

Ghost elements prove that link targets need not be present at creation time — or ever:

> "It is possible to link to a node, or an account, even though there is nothing stored in the docuverse corresponding to them." [LM 4/23]

> "Indeed, there is no need for the presence of elements at the addresses specified. Link types may be ghost elements." [LM 4/45]

If you can link to addresses where **nothing is stored**, then certainly you can link to addresses on a remote server without asking that server's permission or verifying the content exists.

## Immutable Endpoints Eliminate Coordination Need

The reason coordination would be needed in a mutable system is to maintain consistency — if the target could change, the link might need to be updated. But Xanadu links point to **I-space addresses**, which are permanent and immutable:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

I-space content never changes. The link's endsets are fixed at creation. There is nothing to synchronize, because neither the link nor its target will ever change state.

## Coordination Happens at Retrieval, Not Creation

The BEBE protocol handles cross-server communication, but for **request forwarding** — delivering content when someone follows a link — not for validating links at creation:

> "First, by the forwarding of requests as they fan out from users to servers able to supply; and the pass-through of material that is returned to the requesting user in reply." [LM 4/70]

The architectural split is clean:
- **Creation time**: Link is stored locally in the home document. No cross-server communication.
- **Retrieval time**: When someone follows the link, the system forwards the request to the server that holds the target content.

## Endsets Are Pure Address References

Endsets are arbitrary span-sets that **map to the tumbler line** — they are address references, not live pointers requiring validation:

> "ENDSETS MAY POINT TO SPANS ANYWHERE IN THE DOCUVERSE" [LM 4/45]

> "There is a universal address space, the tumbler line... We may visualize a link's endsets as mapping to it." [LM 4/45]

A span on the tumbler line is a mathematical designation — two boundary tumblers. It requires no round-trip to the target server to construct or store.

## Summary

The combination of three properties makes coordination unnecessary:

1. **Locality of storage** — links live at their home, not their targets
2. **Immutability of endpoints** — I-space addresses never change, so there is no state to synchronize
3. **Ghost element validity** — targets need not exist, let alone be verified

This is architecturally significant: it means the link creation path is entirely local, which is essential for a decentralized system where "computer networks are always broken" [LM 4/75]. A server that cannot reach the target server can still accept links pointing to it. The docuverse's coherence emerges at retrieval time through BEBE forwarding, not at creation time through distributed consensus.

---

## Question 10 [nelson]

> Must the system guarantee that a reader consulting any server in the network will eventually see every piece of content and every link that has been created anywhere, or is partial knowledge of the global state acceptable?

### Nelson's Answer

## Partial Knowledge Is the Explicit Design

Nelson does **not** require total replication. Each server holds a subset of the docuverse plus a map of where the rest lives. The user guarantee is **access on demand from any point**, not **every server eventually holding everything**.

---

### The Subrepresentation Model

Nelson's architecture is built on partial, demand-driven knowledge:

> "Each server contains a map and a subset of the whole — a microcosm that shrinks and grows." [LM 4/71]

> "Each server contains a continuously valid model or subrepresentation of the entire docuverse and (because of tumbler addressing) a model of the entire network." [LM 4/72]

The word "subrepresentation" is precise — it is a partial model, not a complete copy. The microcosm "shrinks and grows" dynamically based on demand, not toward some eventual completeness.

### What Makes the Partial Knowledge Work

Two mechanisms compensate for incomplete local state:

**1. Request forwarding.** When a server lacks content, it routes the request:

> "First, by the forwarding of requests as they fan out from users to servers able to supply; and the pass-through of material that is returned to the requesting user in reply." [LM 4/70]

**2. Demand-driven migration.** Content moves toward where it is needed:

> "Material is moved between servers for a number of purposes: (1) for more rapid access to final material, (2) for more rapid access to needed material which indexes material on other servers, (3) for rebalance in keeping with demand, (4) for redundancy and backup purposes." [LM 4/71]

The result is that each server's knowledge improves incrementally but never needs to become total:

> "A server's network model, from the null case on up, is at all times unified and operational; whatever information moves between servers is assimilated at once to its overall structure, leaving each server in canonical operating condition with a slightly improved map of what is elsewhere. The contents can slosh back and forth dynamically." [LM 4/72]

Note "from the null case on up" — a server with zero content and zero links is still in a valid operating state. It just has a very sparse map.

### Broken Networks Are Normal

Nelson explicitly designs for partial availability:

> "It is a truism that 'computer networks are always broken.' Meaning that on the average some nodes are disconnected or not working." [LM 4/75]

This means temporary inability to reach content is an expected condition, not a system failure. The guarantee degrades gracefully — content may be "not currently available" as a last resort rather than permanently lost.

### The User Guarantee Is Access, Not Replication

What Nelson promises is that any user at any access point can **reach** any content — not that every server **holds** all content:

> "Perhaps the most important thing, and certainly the hardest part to believe, is that everything on such a network — any subset, substructure or grouping — can come to the user immediately, even as the aggregation grows to tremendous size." [LM 2/57]

> "The function of BEBE is to meld the contents of separate Xanadu servers into a single unified space." [LM 4/70]

The word "meld" is significant — it means "make appear as one," not "replicate everywhere." The unified space is a logical property experienced by users, not a physical property of each server.

### The Link Discovery Question

Links raise a subtler issue. Nelson promises comprehensive link discovery:

> "The reader should be able to ask, for a given document or place in the document, 'What connects here from other documents?' — and be shown all these outside connections without appreciable delay." [LM 2/46]

This implies that link search should be **functionally complete** — you should find all relevant links, not just locally-known ones. But the mechanism is distributed search (forwarding through BEBE), not total link replication at every server. The guarantee in Nelson's words is about the result ("all these outside connections"), not the means.

Nelson also guarantees that search scales:

> "THE QUANTITY OF LINKS NOT SATISFYING A REQUEST DOES NOT IN PRINCIPLE IMPEDE SEARCH ON OTHERS." [LM 4/60]

This is a performance guarantee about filtering efficiency, not a replication guarantee.

### The Scalability Argument

Total replication would violate Nelson's "soft corridor" performance requirement — the system must slow only logarithmically as it grows:

> "An ever-growing network, instantaneously supplying text and graphics to millions of simultaneous users, would be impossible if it slowed down too fast as it grew. (It can't be linear. The system cannot slow down by half as its size doubles.)" [LM 4/2]

If every server had to hold a copy of everything, growth would impose linear storage and synchronization costs on every node. The subrepresentation model — partial knowledge plus routing — is what makes logarithmic scaling feasible.

### Summary

| Question | Answer |
|----------|--------|
| Must every server hold all content? | No — "a subset of the whole" |
| Must every server hold all links? | No — distributed search satisfies requests |
| Must every server eventually converge to total knowledge? | No — microcosms "shrink and grow" with demand |
| Is temporary unavailability acceptable? | Yes — "networks are always broken" |
| What IS guaranteed? | Any user can reach any content from any access point |
| What mechanism provides this? | Request forwarding + demand-driven migration + subrepresentation |

**Partial knowledge is not a concession — it is the architecture.** The docuverse is unified at the logical level and distributed at the physical level. Each server holds what it needs, knows where to find the rest, and improves its model incrementally through use.

---

## Question 11 [gregory]

> When two separate backend processes each call `findisatoinsertmolecule` for the same document simultaneously, does the tumbler node-account hierarchy (the `1.NODE.0.ACCOUNT.0.DOC` prefix) provide sufficient partitioning to prevent I-address collisions, or was single-process execution the only mechanism preventing duplicate I-address allocation?

### Gregory's Answer

## KB Synthesis

## Two Concurrent Processes: I-Address Allocation Safety

**Short answer:** Single-process execution is the *only* safety mechanism. The tumbler hierarchy provides partitioning between documents and between nodes, but offers no protection when two processes simultaneously insert into the same document.

---

### What the hierarchy partitions

The tumbler address structure for text content is:

```
1.NODE.0.ACCOUNT.0.DOC.3.0.ELEMENT_NUM
```

`findisatoinsertmolecule` bounds its `findpreviousisagr` search to the calling document's address range — specifically, it sets `upperbound` to `docISA.3.1` (the top of the text element subspace for that document) [SS-ADDRESS-SPACE Finding 0065, Finding 0077]. This means:

- **Across documents:** Two processes inserting into different documents search non-overlapping tumbler ranges. No collision possible — the allocation function is partition-safe between documents.
- **Across accounts:** Same reasoning — `1.1.0.1.0.1.3.x` and `1.1.0.2.0.1.3.x` are disjoint.
- **Across nodes:** If each process is associated with a different node prefix (e.g., `1.1.x` vs. `1.2.x`), their entire address spaces are disjoint.

### What the hierarchy does NOT partition

When two processes both call `findisatoinsertmolecule` for the **same document**:

1. Both search the same tumbler range (`docISA.3.0.1` through `docISA.3.1`)
2. Both call `findpreviousisagr` against their own **in-memory granfilade tree**
3. Both see the same "current max" I-address (assuming neither has flushed recent writes to disk)
4. Both compute `max + 1` and arrive at the same fresh address
5. Both write their content at that address — a silent collision with no error

The allocation is explicitly described as "stateless query-and-increment on different tumbler ranges" with "no hidden session state" [SS-ADDRESS-SPACE Finding 0061]. That statelessness is safe *within a single process* where the in-memory tree is authoritative and mutations are serialized. Between separate processes it becomes a race condition.

### Why single-process execution is the only guard

[PRE-CONCURRENT-INSERT] (Finding 0041) states this directly:

> "Concurrent unsynchronized insertion into the same enfilade is unsafe. The `adopt(new, RIGHTBRO, ptr)` call modifies shared pointers, `father->numberofsons` can suffer lost updates, and split/rebalance operations assume exclusive access. Serialization is required for structural integrity."

[INV-ATOMICITY] (Finding 0042) explains the mechanism:

> "The `bed.c` event loop processes each FEBE operation atomically via run-to-completion scheduling... There are no threads, no state-modifying signal handlers, and no preemption."

And [INV-SEQUENTIAL-DISPATCH] (Finding 0042) confirms the scope:

> "The system's concurrency model is total serialization... all operations are serialized."

This serialization exists *within a single daemon process*. There is no inter-process mechanism (no file locking on `enf.enf`, no shared memory mutex, no distributed coordinator) that would extend this guarantee to a second process [SS-UNIFIED-STORAGE Finding 0059]:

> "All persistent state... resides in a single disk file `enf.enf`."

The KB notes no `fsync` calls and no transaction log [SS-DURABILITY-BOUNDARY Finding 0059], so even the durability model assumes a single writer.

### Summary

| Scenario | Collision possible? | Why |
|----------|---------------------|-----|
| Same process, same document, sequential | No | Event-loop serialization |
| Same process, two documents | No | Disjoint tumbler ranges |
| Two processes, different documents on same node | No | Disjoint tumbler ranges |
| **Two processes, same document, same node** | **Yes** | Stale in-memory trees, no locking |
| Two processes, different nodes | No | Disjoint node prefix |

The node-account hierarchy is a sufficient *namespace* partition but not a *concurrency* partition. The freshness invariant P1 — "I-addresses are globally unique" — is guaranteed by sequential execution alone, not by the address structure [SS-ADDRESS-SPACE Finding 0061].

## Code Exploration

I now have everything needed for a comprehensive answer. Here it is:

---

## Answer: Tumbler Hierarchy vs. Single-Process Execution as the I-Address Collision Guard

### Short answer

**Single-process execution is the only mechanism preventing duplicate I-address allocation.** The tumbler node-account hierarchy provides namespace partitioning — isolation between different accounts — but it provides zero protection against collisions between two processes operating under the **same account**. If two separate backend processes simultaneously call `findisatoinsertmolecule` for the same document, they will compute the same next I-address.

---

### The process model

There are two backends:

- **`be.c`** — single-user backend. One Unix process, one client. A tight `for(;;)` loop calls `xanadu()` sequentially [be.c:90-95]. Strictly one request at a time.
- **`bed.c`** — multi-user daemon. Still **a single Unix process**. Multiple frontends are multiplexed with `select()` [bed.c:111]. The event loop dispatches exactly one `xanadu()` call per iteration and waits for it to complete before re-entering `select` [bed.c:118-143]. Single-threaded, cooperative — no preemption.

In both cases, all request processing is serialized within a single process. There is no threading.

---

### The global in-memory granfilade

`granf` is a process-global pointer to the root of the in-memory enfilade tree:

```c
// corediskout.c:21
typegranf granf;

// xanadu.h:14
extern typegranf granf;
```

At startup, `initmagicktricks()` [entexit.c:19-47] calls `initenffile()` which reads `enf.enf` into this in-memory tree (or creates an empty one):

```c
// entexit.c:41-46
if (initenffile()) {
    initkluge ((typecuc**)&granf, (typecuc**)&spanf);
} else {
    granf = (typegranf) createenf (GRAN);
    spanf = (typespanf) createenf (SPAN);
}
```

From that point on, all operations read and mutate this in-memory tree. Disk write-back is lazy — `diskflush()` is called only when all players disconnect [bed.c:105] or on `QUIT` [bed.c:134-137]. The `be.c` backend never calls `diskflush()` during normal operation.

---

### What `findisatoinsertmolecule` actually does

```c
// granf2.c:158-181
static int findisatoinsertmolecule(typecuc *fullcrumptr, typehint *hintptr, typeisa *isaptr)
{
  typeisa upperbound, lowerbound;

    tumblerincrement (&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound);
    clear (&lowerbound, sizeof(lowerbound));
    findpreviousisagr ((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);
    if (tumblerlength (&hintptr->hintisa) == tumblerlength (&lowerbound)) {
        tumblerincrement (&lowerbound, 2, hintptr->atomtype, isaptr);
        tumblerincrement (isaptr, 1, 1, isaptr);
    } else if (hintptr->atomtype == TEXTATOM) {
            tumblerincrement (&lowerbound, 0, 1, isaptr);
    } else if (hintptr->atomtype == LINKATOM) {
        ...
    }
}
```

The three steps are:
1. Compute an upper bound by incrementing `hintisa` [granf2.c:162]
2. Call `findpreviousisagr` to find the highest existing ISA below that upper bound [granf2.c:164]
3. Increment that to derive the next available ISA [granf2.c:166-175]

`findpreviousisagr` [granf2.c:255-278] is **pure in-memory tree traversal** — it walks `typecorecrum *` pointers through the in-memory enfilade. There is no disk read during the scan phase. It reads exactly what is in `granf` at the moment of the call.

This is a **check-then-act** sequence with no locking. Its atomicity depends entirely on the serialized single-threaded execution model.

---

### What happens with two separate processes

`enf.enf` is opened with a plain `open(2)` — no exclusive lock, no coordination:

```c
// disk.c:364
fd = open ("enf.enf", 2 /*rw*/, 0);
```

No `O_EXCL`, no `flock()`, no `fcntl(F_SETLK)`. Two processes can open and operate on the same file simultaneously with no kernel-enforced coordination.

The disk block allocator also loads its free-list bitmap into private process memory:

```c
// diskalloc.c:36-53
for (i = 0; i < BITMAPSIZE && !diskheader.bitmap[i]; ++i);
...
diskheader.bitmap[i] = diskheader.bitmap[i] & ~mask[j];
ret.diskblocknumber = i*8+j;
```

`diskheader` is in-process memory. Two processes would each think the same blocks are free and independently allocate them — causing disk-level corruption independently of the ISA collision problem.

For the ISA collision specifically: if Process A and Process B both start with the same `enf.enf` state and both insert text under document `1.1.0.1.0.1`:

- Both call `findisatoinsertmolecule` with `hintisa = 1.1.0.1.0.1`
- Both call `findpreviousisagr` on their respective private in-memory `granf` trees
- Both see the same "last" ISA (say `1.1.0.1.0.1.0.3`)
- Both compute `1.1.0.1.0.1.0.4` as the next ISA
- Both call `insertseq()` at `1.1.0.1.0.1.0.4`
- When each process eventually writes to disk, one write silently overwrites the other — no merge, no conflict detection, no error

---

### What the tumbler hierarchy actually provides

The ISA address structure for ATOM content under a document is:

```
NODE . ACCOUNT . 0 . DOC . 0 . atomtype . sequence
e.g.:  1.1      0.1  0.1    0.1  0.1
```

The hierarchy means:
- **Different accounts** produce different `hintisa` prefixes (e.g., `1.1.0.1` vs. `1.1.0.2`). `findpreviousisagr` for one account searches a non-overlapping region of the granfilade relative to the other. Two processes handling **different accounts** will compute ISAs in distinct address subspaces. No collision.
- **Same account, same document**: The `hintisa` is identical. Both processes search the same region of the granfilade, find the same previous ISA, and compute the same next ISA. **Full collision.**

The hierarchy is a **namespace** partitioning mechanism. It isolates tenants (accounts) from each other. It does not isolate concurrent processes from each other within the same tenant.

---

### Conclusion

| Scenario | Collision risk |
|---|---|
| Two users within one `bed.c` daemon, same account | **None** — serialized by single-threaded `select` event loop |
| Two `be.c` processes, different accounts | **None** — tumbler prefix partitions the search/allocation space |
| Two `be.c` processes, same account and document | **Certain** — both processes read from independent in-memory `granf` copies, compute the same next ISA, overwrite each other on disk |
| Two `bed.c` daemons (hypothetical) | Same as above — independent in-memory trees, shared disk, no locking |

The real guard is **mutual exclusion at the process level**: the system is architected so that exactly one backend process runs against one `enf.enf` file at a time. Within that process, the single-threaded event loop serializes all check-then-act sequences. The tumbler hierarchy is the mechanism for **per-account namespace isolation** among clients of that single process — it was never designed to handle multi-process write concurrency, and there is no code in the system to provide it.

---

## Question 12 [gregory]

> If two replicas of the granfilade each append content under the same document's I-address range and later merge, does the append-only property guarantee that both sets of I-addresses coexist without conflict, or can overlapping allocations produce two different content bytes at the same I-address?

### Gregory's Answer

## KB Synthesis

The append-only property does **not** guarantee conflict-free coexistence. Two replicas inserting under the same document's I-address range will produce overlapping allocations, and a merge can place two different content bytes at the same I-address.

## Why Conflicts Arise

**The allocation function is purely local state** [SS-ADDRESS-SPACE, Finding 0061]:

```
next_iaddr(granf) = findpreviousisagr(granf) + 1
```

There is no session-local counter, no distributed coordinator, and no reservation mechanism. `findpreviousisagr` queries the local granfilade tree to find the current maximum I-address and increments by 1 [SS-ADDRESS-ALLOC]. The result is completely determined by whatever the local replica sees as its current maximum.

Two replicas that diverge from the same base state will compute identical allocation sequences for their independent insertions. Replica A inserts "X" → allocates I.4. Replica B independently inserts "Y" → also allocates I.4. On merge, I.4 has two claimants with different content — a genuine conflict.

## What the Append-Only Property Actually Guarantees

The append-only invariants are scoped to a **single replica**:

- **INV-MONOTONIC** [Finding 0061]: Within one replica, allocations are strictly increasing; `time(alloc_a) < time(alloc_b) ⟹ iaddr(alloc_b) > iaddr(alloc_a)`.
- **INV-NO-IADDR-REUSE** [Finding 0061]: A single replica never re-allocates a freed I-address; the granfilade is never modified by DELETE.
- **INV-IADDR-IMMUTABILITY** [Finding 0064]: Once allocated, content at an I-address never changes *within a replica*.

None of these properties constrain what a second independent replica does with the same address space.

## Tumbler Partitioning Only Helps If Replicas Are Partitioned

The address hierarchy does partition I-space by document [SS-ADDRESS-SPACE, Finding 0065]:

- Text I-addresses for document D live at `D.0.3.x`
- Link orgls for D live at `D.0.2.x`
- Different documents have non-overlapping allocation ranges

If two replicas work under **different documents**, their I-address ranges are structurally disjoint and merge is conflict-free. But the question posits the same document — in which case both replicas query the same subrange and produce identical allocation sequences from the same starting maximum.

## What Would Be Needed for Conflict-Free Replication

The KB describes no replication or merge protocol. The system is explicitly single-node [INV-ATOMICITY, INV-SEQUENTIAL-DISPATCH, Finding 0042]: a single-threaded `select()` event loop serializes all operations. The CRDT characterization in the abstract spec (EWD layer) assumes tumbler partitioning *assigns disjoint I-address subranges to each replica* — but the implementation's allocation algorithm `max_iaddr(local_granf) + 1` does not enforce this partition for concurrent replicas of the same document.

Conflict-free merging of granfilade replicas for the same document would require at minimum:
1. **Pre-assigned disjoint allocation subranges** per replica (e.g., replica A allocates `D.0.3.1.x`, replica B allocates `D.0.3.2.x`)
2. **A coordination protocol** gating allocation
3. **Content-addressable storage** (different content → different address by construction)

None of these are present in the implementation [SS-UNIFIED-STORAGE, SS-CACHE-MECHANISM]. The implementation's append-only guarantee is a *local* monotonicity property, not a *global* uniqueness property across replicas.

## Code Exploration

I now have enough to answer the question precisely. Here is the full analysis with source citations.

---

## Answer: Does the Append-Only Property Guarantee Conflict-Free I-Address Allocation Across Replicas?

**Short answer: No.** The append-only property is a local, single-instance guarantee. Concurrent replicas computing I-addresses from the same initial state will allocate the same ISA for different content. There is no distributed coordination mechanism in this codebase.

---

### 1. The Tumbler / ISA Structure Has No Replica Identity Field

The tumbler type is defined in `common.h:59-65`:

```c
typedef struct structtumbler {
    humber xvartumbler;
    char varandnotfixed;
    char sign;
    short exp;
    tdigit mantissa[NPLACES];   /* NPLACES = 16 */
} tumbler;
```

`typedef tumbler typeisa;` — `xanadu.h:23`

There is no node ID, machine ID, replica ID, timestamp, UUID, Lamport clock, or any other site-distinguishing field. The `NODEID = 4` in `xanadu.h:30` is a *type tag for item headers*, not an address component.

Similarly, the `typehint` struct (`xanadu.h:148-153`) that drives ISA allocation contains only `supertype`, `subtype`, `atomtype`, and `hintisa` (the parent address). No instance identity enters it.

---

### 2. ISA Allocation Is Computed Purely From Local Granfilade State

Every insert follows this call chain:

```
doinsert (do1.c:87)
  → inserttextingranf (do1.c:118)
    → inserttextgr (granf2.c:83)
      → findisatoinsertgr (granf2.c:130)
        → findisatoinsertmolecule  (for ATOM types)  (granf2.c:158)
          OR
          findisatoinsertnonmolecule (for documents, accounts) (granf2.c:203)
```

Both leaf functions work the same way: **find the highest existing ISA below an upper bound in the local tree, then increment by one.**

**`findisatoinsertmolecule`** (`granf2.c:158-181`):

```c
tumblerincrement (&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound);
clear (&lowerbound, sizeof(lowerbound));
findpreviousisagr ((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);
if (tumblerlength (&hintptr->hintisa) == tumblerlength (&lowerbound)) {
    tumblerincrement (&lowerbound, 2, hintptr->atomtype, isaptr);
    tumblerincrement (isaptr, 1, 1, isaptr);
} else if (hintptr->atomtype == TEXTATOM) {
    tumblerincrement (&lowerbound, 0, 1, isaptr);
} ...
```

**`findisatoinsertnonmolecule`** (`granf2.c:203-242`):

```c
findpreviousisagr ((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);
...
if (iszerotumbler(&lowerbound) || !lowerbound_under_hint) {
    tumblerincrement(&hintptr->hintisa, depth, 1, isaptr);
} else {
    tumblertruncate (&lowerbound, hintlength + depth, isaptr);
    tumblerincrement(isaptr, tumblerlength(isaptr)==hintlength?depth:0, 1, isaptr);
}
```

`findpreviousisagr` (`granf2.c:255-278`) is a recursive tree walk that descends the granfilade to find the *last leaf* below the given upper bound:

```c
if (crumptr->height == 0) {
    findlastisaincbcgr ((typecbc*)crumptr, offset);
    return(0);
}
for (ptr = findleftson((typecuc*)crumptr); ptr; ptr = findrightbro(ptr)) {
    if ((tmp = whereoncrum(...)) == THRUME || tmp == ONMYRIGHTBORDER || !ptr->rightbro) {
        findpreviousisagr (ptr, upperbound, offset);
        return(0);
    } else {
        tumbleradd(offset, &ptr->cwid.dsas[WIDTH], offset);
    }
}
```

**There is no global counter, no server-to-server lock, no vector clock, no timestamp, no UUID appended to the result.** The output of `findpreviousisagr` is entirely determined by what is already in the local in-memory granfilade tree.

---

### 3. The Granfilade Is a Single Global Singleton

```c
extern typegranf granf;   /* xanadu.h:14 */
extern typespanf spanf;   /* xanadu.h:16 */
```

The system has exactly one `granf` and one `spanf`. The architecture is a single-server event loop (`bed.c`), serializing all requests. Multiple FEBE clients connect to *one process sharing one tree* (`players.h:23-33`). The `bert.c` access-control layer (`checkforopen`, `findbert`) governs write permissions per document, not per-replica identity.

There is no synchronization protocol, no gossip layer, no Merkle DAG, no CRDT infrastructure — nothing that would enable safe multi-master replication.

---

### 4. The Conflict Scenario: Both Replicas Compute the Same ISA

Given two replicas A and B starting from identical granfilade state, both called to append text to document D:

1. Both call `doinsert` → `inserttextingranf` → `inserttextgr` → `findisatoinsertgr`.
2. Both call `findisatoinsertmolecule` with identical `hintisa = D`.
3. Both call `findpreviousisagr` on their local (identical) trees.
4. Both find the same `lowerbound` — the same highest existing ISA under D.
5. Both execute `tumblerincrement(&lowerbound, 2, TEXTATOM, isaptr)` then `tumblerincrement(isaptr, 1, 1, isaptr)`.
6. Both get the **identical ISA** — call it X.
7. Replica A stores byte string "hello" at ISA X. Replica B stores "world" at ISA X.

After this, X has two different byte values in two different backends. The append-only property does not prevent this, because it only guarantees that within a single sequential instance, `insertseq` (`insert.c:17`) places each new crum at a freshly allocated address — it says nothing about coordination with any other instance.

---

### 5. Append-Only Is a Local Invariant, Not a Distributed One

`insertseq` (`insert.c:17-70`) retrieves the relevant bottom-crum via `retrievecrums`, then inserts a new crum as a right brother:

```c
context = retrievecrums (fullcrumptr, address, WIDTH);
...
adopt (new, RIGHTBRO, (typecorecrum*)ptr);
```

This guarantees that *within a single backend*, the same ISA is never inserted twice, because each successful call to `findisatoinsertgr` finds the current highest-ISA, advances it, and immediately commits it to the live tree. A second sequential call within the same process finds the first call's result and advances further.

But this is a sequential-access property over a single shared mutable tree, not a distributed uniqueness guarantee. The moment two processes diverge from a common snapshot, each advances its private copy of the "high-water mark" independently.

---

### Conclusion

**The append-only property of the granfilade is a single-instance, sequential invariant.** It guarantees that within one running udanax-green process, no two insertions produce the same ISA. It provides no protection against two replicas, each computing the same "next available" ISA from their identical starting state and writing different content there. Overlapping allocations across replicas *will* produce two different byte values at the same I-address. The code contains no mechanism — no node-local namespace, no distributed counter, no merge protocol — that would prevent this conflict or resolve it after the fact.

---

## Question 13 [gregory]

> Was the spanfilade's write-only design (no `deletespanf` exists) an intentional choice to make DOCISPAN entries safe for uncoordinated replication — meaning two servers adding entries for the same I-span in different documents would simply union without conflict — or was it purely a simplification for single-server operation?

### Gregory's Answer

## KB Synthesis

The KB doesn't contain explicit design documentation about the spanfilade's write-only property being chosen for replication safety. I can tell you what the evidence shows, but the intent question is partially unanswerable from what I have.

**Evidence pointing toward single-server simplification:**

The system is firmly single-server, single-threaded [INV-SEQUENTIAL-DISPATCH], [INV-ATOMICITY]. Concurrent unsynchronized insertion into the same enfilade is explicitly unsafe [PRE-CONCURRENT-INSERT] — `adopt(new, RIGHTBRO, ptr)` modifies shared pointers without locking. No replication mechanism of any kind is present in the codebase. The stale-entry problem from DELETE is treated as an accepted limitation [EC-STALE-SPANF-REFERENCE], [INT-DELETE-SPANF-DIVERGENCE], not as a design trade-off documented anywhere. The write-only property means FIND_DOCUMENTS returns a superset of current reality after content deletion — a divergence you'd want to eliminate in a serious replication scheme, not accept.

The commented-out `insertspanf` in APPEND [EC-APPEND-NO-DOCISPAN] and the `TRUE||` guard that breaks orgl filtering in find_links [EC-FIND-LINKS-GLOBAL] suggest code that was simplified or left incomplete, not code that was carefully designed for distribution.

**The structural property is real but looks like a consequence:**

The spanfilade is a G-Set — entries only accumulate, never retract [INV-SPANF-WRITE-ONLY]. The permanent layer (ispace + spanf) is logically confluent under concurrent additions [INV-ENFILADE-CONFLUENCE]: any serialization order of additions produces the same queryable content. This would make spanfilade entries safe for uncoordinated replication in the sense that two servers independently inserting DOCISPAN entries for the same I-span would union without conflict. The write-only design is structurally compatible with eventual consistency.

But "compatible with" is not "designed for." The code shows no wire protocol for replication, no vector clocks, no node identity, no conflict detection. The durability model is session-level-only with no fsync [SS-DURABILITY-BOUNDARY] — a foundation you'd need to harden considerably before replication was meaningful.

**My honest assessment:**

The write-only spanfilade looks like a simplification: deletion from the permanent layer was never implemented because the Xanadu permanence model (P0, P0') treats content accumulation as a feature, not a bug. The spanfilade grows because content identity is permanent. The fact that this produces a CRDT-compatible G-Set is a mathematical consequence of that permanence commitment, not a deliberate engineering choice for distribution. If replication were the motivation, you'd expect the omission of `deletespanf` to be called out somewhere as a deliberate design decision. Nothing in the KB shows that.

What I can't rule out: Ted's broader vision for Xanadu always included a global distributed docuverse, and the permanence-by-default of the storage model may have been chosen partly with that in mind. But that design intent — if it exists — isn't visible in the udanax-green codebase as I built it.

## Code Exploration

I now have enough to give a thorough answer. Let me compile the full analysis.

---

## Analysis: Was the Spanfilade's Write-Only Design Intentional for Replication Safety?

**Short answer:** The write-only design is a *semantic consequence* of permascroll permanence, not an explicit distributed-replication strategy — but it does produce the union-compatible property you describe. The code provides no evidence of distributed replication intent; it was built for single-server operation with permanence as the governing principle.

---

### 1. Confirming the Absence of `deletespanf`

A thorough search of all `.c` source files finds zero occurrences of any `deletespanf` or delete operation targeting the global `spanf` pointer. The full interface for the spanfilade is:

**Write side:**
- `insertspanf()` [spanf1.c:15] — inserts one record keyed by I-span origin and width
- `insertendsetsinspanf()` [do2.c:116] — calls `insertspanf` three times for link endpoints

**Read side:**
- `sporglset2linkset()`, `finddocscontainingsp()`, `retrievesporglsetinrange()`, `findlinksfromtothreesp()`

That is the complete API. No delete path exists.

The general-purpose `deletend()` function [edit.c:31] does support operating on SPAN-type enfilades — the file comment says `/* use with SPAN and POOM */` [edit.c:30], and the SPAN constant is the spanfilade type [enf.h:14]. But `deletend` is only ever called with `docorgl` as its first argument (a per-document POOM entry), never with the global `spanf`:

```c
/* orglinks.c:145-152 */
bool deletevspanpm(typetask *taskptr, tumbler *docisaptr, typeorgl docorgl, typevspan *vspanptr)
{
    if (iszerotumbler(&vspanptr->width))
        return (FALSE);
    deletend((typecuc*)docorgl, &vspanptr->stream, &vspanptr->width, V);
    logbertmodified(docisaptr, user);
    return (TRUE);
}
```

The capability was designed in; the call path was never wired up.

---

### 2. What Gets Written — and What Doesn't

**DOCISPAN entries** (`xanadu.h:39`) are written by `docopy()`:

```c
/* do1.c:53-64 */
return (
   specset2ispanset (taskptr, specset, &ispanset, NOBERTREQUIRED)
&& findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
&& acceptablevsa (vsaptr, docorgl)
&& asserttreeisok(docorgl)
/* the meat of docopy: */
&& insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)
&&  insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN)
&& asserttreeisok(docorgl)
);
```

So every `copy`, `insert`, `createnewversion`, `createlink` writes into the spanfilade. **No operation ever removes from it.**

**Link endpoint entries** (`LINKFROMSPAN`, `LINKTOSPAN`, `LINKTHREESPAN`) are written by `insertendsetsinspanf()` [do2.c:116-128] via `docreatelink()` [do1.c:195-221]. Again, nothing ever deletes them.

---

### 3. The Asymmetry: POOM is Mutable, Spanfilade is Not

`dodeletevspan()` [do1.c:158] deletes from the **granfilade** (POOM), not the spanfilade:

```c
/* do1.c:158-167 */
bool dodeletevspan(typetask *taskptr, typeisa *docisaptr, typevspan *vspanptr)
{
    return (
       findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
    && deletevspanpm (taskptr, docisaptr, docorgl, vspanptr)
    /*&& TRUE*/ /* ht stuff */ );
}
```

The trailing comment `/* ht stuff */` — repeated identically in `docopy()` [do1.c:64], `dodeletevspan()` [do1.c:166], and `dorearrange()` [do1.c:42] — marks slots where historical-trace (hypertext history tracking) was intended but never implemented. This is the *most informative absent code* in the system. Whoever designed the deletion path deliberately chose not to include a corresponding `deletespanf` call there, and left a `/* ht stuff */` placeholder that was never filled.

This is the asymmetry in full: `insertspanf` pairs with `insertpm`; `deletevspanpm` has no spanfilade counterpart.

---

### 4. Semantic Consequence: "Ever Contained" vs. "Currently Contains"

Because DOCISPAN entries accumulate and are never pruned, `finddocscontainingsp()` [spanf1.c:151-188] answers a different question than you might expect:

```c
/* spanf1.c:168-171 */
tumblerincrement (&docspace.stream, 0, DOCISPAN, &docspace.stream);
tumblerincrement (&docspace.width, 0, 1, &docspace.width);
for (; ispanset; ispanset = ispanset->next) {
    context = retrieverestricted ((typecuc*)spanf, &docspace, ORGLRANGE, ispanset, SPANRANGE, (typeisa*)NULL);
```

It queries the ORGL (document-ISA) range within the DOCISPAN slot of the spanfilade. **This returns every document that has ever transcluded this I-span**, even if that V-span was later deleted from the document's POOM. The spanfilade is a provenance log, not a live index.

---

### 5. Does the Design Imply Replication Safety?

Structurally, yes — inserting the same DOCISPAN entry from two independent servers *would* produce union-compatible results, because:

1. Tumbler addresses are globally unique and monotonically assigned, so two servers assigning the same I-span address cannot happen by design.
2. Inserting the same (I-span, doc-ISA) pair twice into the spanfilade would produce duplicate crum entries that would both satisfy a range query — effectively a union.
3. `putvspaninlist()` [orglinks.c:329-387] explicitly handles adjacent/overlapping span merging when building result sets, which is exactly what conflict-free union of independent insertions would produce.

But the code provides **no evidence that this was the design motivation**. Specifically:

- There is no distributed replication machinery anywhere in the codebase. `bert.c`/`bed.c` implement single-server multi-user access control, not multi-server coordination.
- There is no commentary about inter-server synchronization, vector clocks, or replication protocol in any of the files.
- The `doappend()` function [do1.c:25-32] contains a revealing comment:

  ```c
  return (appendpm (taskptr, docptr, textset)/*&&
      appendpm includes insertspanf!  insertspanf(taskptr,spanf,docptr,textset,DOCISPAN)*/
  );
  ```

  This commented-out code shows the spanfilade call was separated from the granfilade call as a deliberate design step — but the comment reads like a note-to-self about system architecture, not like a distributed systems requirement.

---

### 6. The Real Reason: Permascroll Permanence

The write-only design follows directly from the permascroll invariant: **I-span addresses are permanent**. Once content is stored at an I-address, that address and content never change. The facts recorded in the spanfilade — "this I-span was transcluded into this document"; "this I-span is an endpoint of this link" — are also *permanent facts*. They don't un-become true when a V-span is deleted from a document, because the I-span itself still exists in the permascroll at that address.

A `deletespanf` would only make semantic sense in a model where the permascroll could be revised — which it cannot be. The write-only spanfilade is the index over an append-only store, and append-only stores have append-only indexes.

---

### Conclusion

The spanfilade's write-only design was driven by **permascroll semantics** in a single-server implementation, not by distributed replication intent. The absence of `deletespanf` is not a gap or simplification — it reflects that recording "this I-span appeared in this document" is a permanent provenance fact, not mutable state. The consequence that two independent servers adding entries for the same I-span would union without conflict is **correct** given this semantic model, but the code was never actually wired to exploit it: there is no multi-server coordination infrastructure anywhere in udanax-green. The property is latent in the data model, not exercised by the implementation.

---

## Question 14 [gregory]

> Since POOMs are the sole locus of destructive mutation (INSERT shifts, DELETE removes, REARRANGE reorders), and two concurrent POOM modifications to the same document produce order-dependent V-address layouts, did you or Ted ever discuss a mechanism for reconciling divergent POOM states — such as replaying the journal of operations rather than merging tree structures directly?

### Gregory's Answer

## KB Synthesis

Not answerable from the KB — there's no record of design discussions between Ted and me on this specific question.

What I can tell you is what the implementation reveals about the design philosophy, and it answers the question structurally.

**The premise doesn't arise in the implementation.** The system is single-threaded with a run-to-completion event loop [INV-ATOMICITY, INV-SEQUENTIAL-DISPATCH]. Concurrent POOM modifications to the same document are architecturally impossible within one process — `select()` fires, `xanadu()` runs the entire operation including all POOM mutations, response goes out, then the next request runs. There's no interleaving point.

**Cross-session write conflict is handled by routing, not reconciliation.** BERT [SS-BERT] prevents two connections from holding simultaneous WRITEBERT on the same document. When write access is denied, `checkforopen()` returns -1 and the protocol signals the front end to create a version instead [INT-BERT-VERSION]. The two sessions then diverge on separate POOM trees — independent documents — not on the same POOM [EC-CONFLICT-COPY-NO-MERGE].

**There is no journal.** The POOM has no operation log, no WAL, no shadow copy [SS-POOM-MUTABILITY]. The granfilade is append-only and the spanfilade is write-only, but those properties exist for permanence reasons, not for replay. Recovering a POOM after crash means you've lost it — you can reconstruct it from a version if one was taken [ST-VERSION-CREATE], not from replaying events.

**The design philosophy is divergence, not convergence.** The `CONFLICT_COPY` mechanism produces independent branches with no merge path [EC-CONFLICT-COPY-NO-MERGE]. `compare_versions` shows what's shared; it doesn't produce a merge. The right model, as far as I can reconstruct the intent, is that merge is a semantic problem for whoever understands the document's meaning — the system's job is to preserve identity and show correspondence, not to decide how to combine edits.

So: if you're asking whether we designed a journal-replay reconciliation mechanism for divergent POOMs, the answer is no, and the single-writer BERT architecture was the reason we didn't need one. Whether Ted and I ever *talked* about whether journal replay would be the right approach for a hypothetical multi-writer extension — I have no record of that conversation in this KB.

## Code Exploration

I now have enough to give a complete answer. Let me compile it.

---

## The Short Answer

No. There is no journal-replay mechanism, no tree-merge facility, and no operation-log replay infrastructure in this codebase. The architecture answers the divergence problem structurally rather than algorithmically: it prevents divergent POOM states from forming in the first place, and makes no attempt to reconcile them if they do.

---

## The POOM as Sole Mutation Site

The question is correct about where destructive state lives. Every mutation goes through three paths, all bottom-honing into the same 2D B-tree structure:

**INSERT** [`insertnd.c:15-111`]:
```c
case POOM:
    makegappm (taskptr, fullcrumptr, origin, width);  // shift DSPs rightward
    bothertorecombine = doinsertnd(fullcrumptr, origin, width, infoptr, index);
    setwispupwards(fullcrumptr, 1);
```

`makegappm` [`insertnd.c:124-172`] iterates over every crum whose V-position is ≥ the insertion point and adds `width->dsas[V]` to its displacement:
```c
case 1:  /* 9-17-87 fix */
    tumbleradd(&ptr->cdsp.dsas[V], &width->dsas[V], &ptr->cdsp.dsas[V]);
    ivemodified(ptr);
```
This is an irreversible structural mutation — the crum's `cdsp` is overwritten in place. There is no old value saved anywhere.

**DELETE** [`edit.c:31-76`]: `deletend()` calls `subtreefree()` on nodes inside the deletion range and calls `tumblersub()` on nodes to the right:
```c
case 1:
    disown((typecorecrum*)ptr);
    subtreefree((typecorecrum*)ptr);  // physically freed
    break;
case 2:
    tumblersub(&ptr->cdsp.dsas[index], width, &ptr->cdsp.dsas[index]);
    break;
```
Freed crums are gone. No tombstones, no undo list, no prior-state snapshot.

**REARRANGE** [`edit.c:78-160`]: `rearrangend()` applies signed tumbler offsets (computed by `makeoffsetsfor3or4cuts`) to each crum, shifting them by signed deltas into their new positions. Again, the mutation is in-place with no history preserved.

---

## Atomicity Without Concurrency

The event loop in `bed.c` is the key architectural fact:

```c
for (;;) {
    select(nfds+1, &inputfds2, 0, 0, &timeout);
    for (i = 0; i <= nfds; i++) {
        if ((1<<i) & inputfds2) {
            user = fdtoplayer[i];
            xanadu(&task);     // ONE full operation, synchronous
        }
    }
}
```
[`bed.c:103-150`]

`xanadu()` calls `(*requestfns[request])(taskptr)` and does not return until the entire operation — including all internal POOM mutations — completes. [`bed.c:153-172`]. The process is single-threaded with no preemption; SIGINT only sets a flag [`bed.c:175-188`].

**Consequence:** Two connections can never simultaneously mutate the same POOM. The loop iterates over ready file descriptors, but each `xanadu()` call is synchronous and blocking. Even if five frontends are all waiting with queued INSERT requests, they execute one at a time. The serialization is total, not per-document.

---

## The BERT Table: Divergence Prevention, Not Reconciliation

`bert.c` is the concurrency control layer. `checkforopen()` [`bert.c:52-87`] enforces this table:

```
Open state -->
type        Not Open   #   Open READ    #   Open WRITE
              !owned | owned  #  conn==  |conn!=  #  conn==  |conn!=
READ             0  |   0   #  READ   |   0    # WRITE  |  -1
WRITE           -1  |   0   #  -1    |  -1    # WRITE  |  -1
```

If connection B tries to WRITE-open a document that connection A already has open for WRITE (`conn!=`), `checkforopen` returns `-1`. The caller then invokes `docreatenewversion()` to give B its own separate POOM:

```c
case BERTMODECOPYIF:
    if (openState == -1) {
        docreatenewversion(taskptr, tp, &taskptr->account, newtp);
        addtoopen(newtp, connection, TRUE, type);
    }
```
[`bert.c:288-299`]

`docreatenewversion()` [`do1.c:260-299`] creates a new document address via `createorglingranf()`, then deep-copies the entire VSPAN content of the original into the new POOM via `docopyinternal()`. The result is two fully independent POOMs sharing I-address content identity (through the granfilade) but diverged in V-address layout from the moment of branching.

**The critical observation:** After this fork, there is no reconciliation. Finding 0022 confirmed this empirically:
> "True concurrent editing requires application-level merge logic."
> "Changes are NOT merged. Final state depends on which copy is accessed."

---

## The interfaceinput Log Is Not a Journal

`get1fe.c` writes incoming FEBE operations to `interfaceinput` (the `ln...` datestamped file) as they are received:

```c
// INSERT:
logstuff = TRUE;
fprintf(interfaceinput, "%d~", INSERT);   // get1fe.c:27
// followed by tumbler args written by gettumbler()

// DELETEVSPAN:
fprintf(interfaceinput, "%d~", DELETEVSPAN);   // get1fe.c:142

// CREATENEWVERSION:
fprintf(interfaceinput, "%d~", CREATENEWVERSION);   // get1fe.c:152
```

This is an **append-only FEBE protocol log** of incoming requests. It is functionally a replay log of all operations applied to the server in a session. But:

1. No code in the system reads it back. There is no `replaylog()` function, no recovery path that opens the `ln...` file. It is write-only audit infrastructure.
2. The `kluge()` function in `get1fe.c:198-202` has a commented-out `fclose/fopen` of `xueditlog` — an earlier variant of the same idea, also dead code.
3. Even if you replayed the log, you would reconstruct a single linear sequence of operations against a single POOM — not a reconciliation of two divergent states.

---

## showrelationof2versions Is Query, Not Merge

`doshowrelationof2versions()` [`do1.c:428-449`] computes the intersection of I-span sets between two specsets:

```c
return
    specset2ispanset(taskptr, version1, &version1ispans, READBERT)
  && specset2ispanset(taskptr, version2, &version2ispans, READBERT)
  && intersectspansets(taskptr, version1ispans, version2ispans, &commonispans, ISPANID)
  && ispansetandspecsets2spanpairset(taskptr, commonispans, version1, version2, relation)
;
```

This tells you *what* two versions share in common by I-address identity. It is the read-only scaffolding that *could* inform a merge — but nothing here performs a merge. The POOM of either document is untouched.

The `deleteversion()` stub [`bert.c:348-354`] is literally empty:
```c
int deleteversion(tumbler *tp)
{
#ifndef DISTRIBUTION
    fprintf(stderr,"deleteversion: tp = ");
    dumptumbler(tp);fprintf(stderr,"\n");
#endif
}
```
Even the cleanup path for abandoned versions was never implemented.

---

## What the Architecture Actually Implies

The reason journal-replay was not needed is architectural:

1. **I-addresses are permanent and append-only.** Content written to the granfilade gets a monotonically allocated I-address [`granf2.c`, `findisatoinsertgr`] and is never moved. The permanent layer has no concurrent mutation problem because content is only ever added, never overwritten.

2. **V-addresses are ephemeral and per-document.** The POOM is the *current view* of how I-addresses are laid out in V-space for one document. It has no intrinsic identity beyond its current tree state. "Reconciling two POOMs" would mean: given two V-address layouts of overlapping I-address content, produce a third V-address layout that combines them. This is what an application-level three-way merge does — using `showrelationof2versions` to find the common base, then applying the two divergent edit sequences. But the POOM layer provides no primitives for this.

3. **The non-commutativity problem is real but avoided.** An INSERT at V=5 on one branch shifts V ≥ 5 by width. A concurrent DELETE at V=3 on the other branch shifts V ≥ 4 negatively. If applied to the same POOM in different orders, the resulting V-layouts differ. The code avoids this by ensuring — through BERT tokens and serial execution — that no two operations ever reach the same POOM simultaneously.

---

## Direct Answer

There is no evidence in this codebase — not a function, not a data structure, not a comment, not dead code — that Ted or I ever built or contemplated a POOM-level journal-replay or tree-merge mechanism. The `#ifdef UNdeFINed` guards throughout `insertnd.c` and `edit.c` show the debugging evolution of the insert/delete paths, but none of them capture operation history for replay.

The design premise was different: the permanent layer (I-addresses in the granfilade) is confluent and append-only, so it needs no reconciliation. The transient layer (V-addresses in the POOM) is per-document and per-version, so it never needs to merge across documents — versions diverge and stay diverged, related only through the shared I-address provenance readable via `showrelationof2versions`. Any merge at the V-address level is intentionally left to the application, which uses `docopy` (transclusion) to selectively incorporate content from one version into another, creating new I-address-linked content in the process.

The `interfaceinput` log is the closest thing to a journal the system has, but it was never wired for replay. It is session-scoped audit output, not a persistent operation log suitable for POOM reconstruction.

---

## Question 15 [gregory]

> Does the tumbler allocation scheme — where each node gets a distinct first-level address (`1.1`, `1.2`, etc.) and each account gets a distinct second-level address — represent an intentional design for federated operation where separate Xanadu servers would own disjoint tumbler prefixes, making granfilade and spanfilade entries from different servers automatically non-conflicting by construction?

### Gregory's Answer

## KB Synthesis

Yes, the evidence strongly suggests this is intentional federated design, though the examined implementation exercises only single-server operation.

## Address Format Encodes Server Identity

The `.0.`-separated address convention gives the explicit pattern `Node.0.User.0.Doc.0.Element` [SS-TUMBLER, Finding 0001]. The first field is "Node" — a server identifier. Every address in the system is hierarchically rooted at a node prefix (`1.1`, `1.2`, etc.), with accounts, documents, and content descending underneath.

## Disjoint Prefixes by Construction

The allocation mechanism enforces strict prefix containment. `findisatoinsertnonmolecule` computes an upper bound from the parent address and rejects any candidate that doesn't pass the containment check [SS-ADDRESS-ALLOC, Finding 0021, PRE-ADDRESS-ALLOC]. Bug 0013 demonstrated what happens without that check — allocation silently crossed account boundaries — and the fix was to add prefix truncation+equality verification [SS-TUMBLER-CONTAINMENT].

Because all allocations are bounded searches within a parent's address space, a server owning prefix `1.1` can only allocate addresses beginning with `1.1`. Content I-addresses follow the pattern `node.account.document.element_field.element_number` [SS-ADDRESS-SPACE, Finding 0077], so content created on Server A (prefix `1.1`) and content created on Server B (prefix `1.2`) occupy disjoint regions of the granfilade's key space — no coordination required.

The same holds for the spanfilade: DOCISPAN entries map I-address spans to document ISAs, both of which carry the node prefix. Two servers' entries never alias.

## Stateless Allocation Supports Independent Operation

I-address allocation is a pure function of granfilade state — a bounded `findpreviousisagr` query followed by increment [SS-ADDRESS-SPACE, Finding 0061]. There is no global counter. Each server can allocate within its prefix independently, and the results are automatically non-overlapping. This is precisely the property needed for a federated permanent layer: write-once addresses, partitioned by server prefix, no cross-server coordination required at allocation time.

## CRDT-Like Merge Properties

The permanent layer (granfilade + spanfilade) is logically confluent under concurrent additions [INV-ENFILADE-CONFLUENCE, Finding 0041]: inserting entries E1 and E2 in either order produces identical query results. Combined with monotonically increasing, never-reused addresses [INV-MONOTONIC, INV-NO-IADDR-REUSE], the permanent layer behaves as a grow-only set (G-Set) CRDT — exactly what is needed for merging state from independent servers. Two servers can operate independently and later merge their granfilades and spanfilades without conflicts, because their address spaces are disjoint and both structures are append-only.

## The Single-Server Gap

The implementation examined runs as a single daemon with a single `enf.enf` file [SS-UNIFIED-STORAGE, Finding 0059] and a single-threaded event loop [INV-ATOMICITY, Finding 0042]. Federation is in the address space design but not in the code: there is no protocol for merging granfilades across servers, no cross-server spanfilade queries, and no mechanism for routing requests to the correct node.

## Summary

The tumbler address hierarchy encodes a three-tier federated topology — node, account, document — with content addresses descending from documents. The prefix-containment allocation scheme, stateless query-and-increment mechanism, and append-only permanent layer all compose into a design where independently operating Xanadu servers would produce non-conflicting address spaces that could be merged without coordination. The single-server `udanax-green` implementation exercises the allocation discipline correctly (enforcing account isolation after Bug 0013) but leaves the inter-server protocols as unimplemented infrastructure in the address space design itself.

## Code Exploration

---

## The Tumbler Allocation Scheme: Federation by Design, Single-Node in Practice

The evidence in the source code is unambiguous: the hierarchical tumbler structure **is** an intentional design for federated operation. Separate Xanadu servers would own disjoint tumbler prefixes, making granfilade and spanfilade entries automatically non-conflicting by construction. However, the codebase as present is a single-node prototype — the federation machinery is designed but not wired up.

---

### 1. The Tumbler Data Structure

`common.h:59-65`:
```c
typedef struct structtumbler {
    humber xvartumbler;
    char varandnotfixed;
    char sign BIT;
    short exp;
    tdigit mantissa[NPLACES];   /* NPLACES = 16 */
} tumbler;
```

A tumbler is a floating-point-like multi-digit address where each mantissa element is one "digit" at a given level of the hierarchy. The `exp` field is an offset that allows leading-zero levels. The entire addressing scheme is a generalized Dewey Decimal system of arbitrary depth.

---

### 2. The Hardcoded Default Account Reveals the Intended Structure

`be.c:37`:
```c
tumbler defaultaccount = {0,0,0,0, 1,1,0,1,0,0,0,0}; /* 1.1.0.1 */
```

Applied at `be.c:88`:
```c
movetumbler(&defaultaccount, &task.account);
```

This is not an arbitrary value. The structure `1.1.0.1` maps directly to the intended hierarchy:

| Digit | Value | Semantic |
|-------|-------|----------|
| mantissa[0] | 1 | root / global namespace |
| mantissa[1] | 1 | node 1 within root |
| mantissa[2] | 0 | level separator |
| mantissa[3] | 1 | account 1 within node 1 |

---

### 3. Node Addresses Are Sequentially Allocated Under the Root

`do1.c:250-257` (`docreatenode_or_account`):
```c
tumblercopy(isaptr, &isa);
makehint(NODE, NODE, 0, &isa, &hint);
result = createorglingranf(taskptr, granf, &hint, &isa);
```

`makehint` records `supertype=NODE=1, subtype=NODE=1` (`do2.c:78-84`). In `findisatoinsertnonmolecule` (`granf2.c:209`):
```c
depth = hintptr->supertype == hintptr->subtype ? 1 : 2;
```
Since NODE==NODE, `depth=1`.

For a root hint of `1`, with no prior entries:
```c
tumblerincrement(&hintptr->hintisa, depth, 1, isaptr);
```
— `tumblerincrement` (`tumble.c:599-623`) appends at position `idx + rightshift`:
- `idx=0` (last non-zero of `1`), `rightshift=depth=1`
- Result: mantissa[1]=1 → **`1.1`** (first node)

Subsequent nodes: `1.2`, `1.3`, `1.4`, ...

---

### 4. Account Addresses Are Allocated Under Their Node

`do1.c:239-241` (`docreatenewdocument` — note: accounts are documents for administrative purposes):
```c
makehint(ACCOUNT, DOCUMENT, 0, &taskptr->account, &hint);
return (createorglingranf(taskptr, granf, &hint, isaptr));
```

`makehint` records `supertype=ACCOUNT=2, subtype=DOCUMENT=3`. Since ACCOUNT ≠ DOCUMENT, `depth=2`.

For hint `1.1` (node), with no prior entries:
```c
tumblerincrement(&hintptr->hintisa, depth=2, 1, isaptr);
```
- `idx=1` (last non-zero of `1.1`), `rightshift=2`
- mantissa[3] += 1 → mantissa = `[1,1,0,1,...]` → **`1.1.0.1`** ✓ (matches the hardcoded default)

Subsequent accounts under node `1.1`: `1.1.0.2`, `1.1.0.3`, ...

Under node `1.2`, the same algorithm gives: `1.2.0.1`, `1.2.0.2`, ...

---

### 5. Document Addresses Are Allocated Under Their Account

`do1.c:234-241` (`docreatenewdocument`):
```c
makehint(ACCOUNT, DOCUMENT, 0, &taskptr->account, &hint);
```

Documents are created directly under the account, same ACCOUNT→DOCUMENT path with depth=2. For account `1.1.0.1`:
- `idx=3`, `rightshift=2`
- mantissa[5] += 1 → `[1,1,0,1,0,1,...]` → **`1.1.0.1.0.1`**

Subsequent documents: `1.1.0.1.0.2`, `1.1.0.1.0.3`, ...

---

### 6. The Disjointness Guarantee: `tumbleraccounteq`

`tumble.c:38-70`:
```c
bool tumbleraccounteq(tumbler *aptr, tumbler *bptr)
{
    /* Compare until account (bptr) terminates with two zeros. */
    for (j_b = 0, i = 0; i < NPLACES; i++) {
        if (bptr->mantissa[i] == 0) {
            if (++j_b == 2) {
                return(TRUE);  /* Account terminated, document is under this account */
            }
        } else {
            if (aptr->mantissa[i] != bptr->mantissa[i]) {
                return(FALSE);
            }
        }
    }
    return (TRUE);
}
```

The **two-zeros-as-terminator** convention is the key mechanism. For account `1.1.0.1` (mantissa `[1,1,0,1,0,...]`):
- Two zero positions occur at mantissa[2] and mantissa[4]
- The first zero (mantissa[2]) is the inter-level separator
- The second zero (mantissa[4]) terminates the prefix match

Any tumbler beginning with `1.1.0.1...` satisfies `tumbleraccounteq`. Crucially, `1.2.0.1.0.1` (from a different node) does **not** satisfy it — mantissa[1] is `2` ≠ `1`. The non-overlap is structural and unconditional.

`be.c:172-175`:
```c
int isthisusersdocument(tumbler *tp)
{
    bool result = tumbleraccounteq(tp, &taskptrx->account);
    return result;
}
```

---

### 7. The Federation Interface: `XACCOUNT` and `CREATENODE_OR_ACCOUNT`

The protocol includes two commands that only make sense in a federated context.

**`XACCOUNT`** — assert an account identity for the current session:
`fns.c:364-373`:
```c
void xaccount(typetask *taskptr)
{
    if (getxaccount(taskptr, &(player[user].account))) {
        putxaccount(taskptr);
    } else {
        putrequestfailed(taskptr);
    }
}
```
`get1fe.c:213-226`:
```c
bool getxaccount(typetask *taskptr, typeisa *accountptr) {
    gettumbler(taskptr, accountptr) && validaccount(taskptr, accountptr);
    player[user].account = *accountptr;
    taskptr->account = *accountptr;
    return(TRUE);
}
```

A client presents a tumbler like `1.2.0.3` — account 3 on node 2 — and the backend uses it as the ownership context for all subsequent operations. Documents it creates get addresses under `1.2.0.3`. A client on a different node presents a different prefix and gets non-overlapping address space.

**`CREATENODE_OR_ACCOUNT`** — provision new node-level entities:
`fns.c:375-386`:
```c
void createnode_or_account(typetask *taskptr)
{
    tumbler t;
    if (    getcreatenode_or_account(taskptr, &t)
         && docreatenode_or_account(taskptr, &t)) {
        putcreatenode_or_account(taskptr, &t);
    } else {
        putrequestfailed(taskptr);
    }
}
```

The client supplies a parent hint tumbler; the backend allocates the next sequential address under it and registers the node in the granfilade. This is exactly the provisioning step a central registry authority would perform when bringing a new Xanadu server online.

---

### 8. Granfilade and Spanfilade Are Naturally Partitioned

Because all granfilade entries (content atoms and orgls) are indexed by their ISA (invariant space address), and all ISAs are allocated under the creating account's prefix, entries from node `1.1` and node `1.2` are guaranteed to occupy disjoint regions of the 1D granfilade keyspace. The same applies to the spanfilade, which maps ISA spans to V-spans: link endpoints from different nodes carry non-intersecting ISA addresses.

`do1.c` calls like:
```c
inserttextingranf(taskptr, granf, &hint, textset, &ispanset)
```
use the document's ISA as the insertion point. Since the ISA already encodes the node and account prefix, the granfilade is effectively partitioned by node prefix without any explicit segregation logic.

---

### 9. What Is **Not** Implemented: The Single-Node Reality

Despite the federated architecture, the code runs as a single-node prototype with no inter-server machinery:

- **Hardcoded single account**: `be.c:37` uses a fixed `1.1.0.1`, never dynamically assigned from a registry.
- **No namespace coordination**: `rcfile.c` handles only local configuration (port, host, directory path). No inter-node prefix registration protocol exists.
- **Single-user global state**: `be.c:37` uses a single global `taskptrx` for `isthisusersdocument`, not per-connection state.
- **No prefix validation**: `validaccount` at `get2.c:157-160` always returns `TRUE` — any client can assert any account tumbler.
- **Node provisioning is unguarded**: `docreatenode_or_account` allocates under whatever hint the client provides, with no authority check.

---

### Summary

The tumbler allocation scheme is **deliberately and coherently designed for federated operation**. The hierarchy — root → node (e.g. `1.1`) → account (e.g. `1.1.0.1`) → document (e.g. `1.1.0.1.0.1`) — is not accidental. The incremental allocation algorithm in `findisatoinsertnonmolecule` (`granf2.c:203-242`), the prefix ownership semantics in `tumbleraccounteq` (`tumble.c:38-70`), the XACCOUNT session identity mechanism (`get1fe.c:213-226`), and the CREATENODE_OR_ACCOUNT provisioning command (`do1.c:243-258`) all cohere as a system where separate Xanadu servers own disjoint tumbler prefixes and their granfilade/spanfilade entries are non-conflicting by construction.

The implementation, however, is a single-node prototype. The full federated stack — inter-server communication, prefix registration, authoritative namespace allocation — was never built into this codebase. What survives is the address space architecture that makes federation geometrically possible, with the operational machinery left as future work.
