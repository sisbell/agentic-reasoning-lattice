# Consultation Answers — Node Ontology

**Inquiry:** What is a node in the Xanadu system? How do nodes enter the docuverse, and what invariants govern the node set?
**Date:** 2026-03-14 14:09
**Questions:** 17 (10 nelson, 7 gregory)

---

## Question 1 [nelson]

> What is the minimal set of properties that define a node at the moment it enters the docuverse?

### Nelson's Answer

# The Minimal Properties of a Node Entering the Docuverse

The answer has two layers, because Nelson's architecture distinguishes between conceptual existence and operational function.

## Layer 1: Conceptual Existence (Ghost Element)

At its most minimal, a node needs only **one thing**: a tumbler address, baptized by its parent.

> "While servers, accounts and documents logically occupy positions on the developing tumbler line, no specific element need be stored in tumbler-space to correspond to them. Hence we may call them ghost elements." [4/23]

> "It is possible to link to a node, or an account, even though there is nothing stored in the docuverse corresponding to them." [4/23]

A node can exist in the docuverse as pure address — no content, no accounts, no stored representation whatsoever. Other nodes can already link to it. A link to a node "will find any of the documents under it" [4/23] — even if there are none yet.

The address itself carries two facts:
1. **Ancestry** — the node descends from a parent. "A server node, or station, has ancestors and may have possible descendant nodes." [4/19] The server address "always begins with the digit 1, since all other servers are descended from it" [4/28].
2. **Ownership** — "The owner of a given item controls the allocation of the numbers under it." [4/20] Someone baptized this number and controls what spawns beneath it.

That is the conceptual minimum. Address plus ownership. Everything else is operational.

## Layer 2: Operational Function (Live Server)

For a node to actually *serve* — to participate in the docuverse as a functioning station — it needs three additional properties:

### A. A Network Model (Even If Null)

> "Each server contains a continuously valid model or subrepresentation of the entire docuverse and (because of tumbler addressing) a model of the entire network." [4/72]

> "A server's network model, from the null case on up, is at all times unified and operational; whatever information moves between servers is assimilated at once to its overall structure, leaving each server in canonical operating condition with a slightly improved map of what is elsewhere." [4/72]

The phrase **"from the null case on up"** is critical. A new node starts with a null subrepresentation — an empty microcosm — and this is already "unified and operational." The model grows incrementally as requests flow through: "The contents can slosh back and forth dynamically" [4/72].

### B. Protocol Capability (FEBE and BEBE)

The node must speak both protocols:
- **FEBE** to serve users — "the protocol for handing off what the user wants to see, retrieve and follow" [4/62]
- **BEBE** to join the network — "the protocol for connecting nodes of the Xanadu network" whose "function is to meld the contents of separate Xanadu servers into a single unified space" [4/70]

### C. Contractual Standing

> "Storage Vendor agrees to honor requests for material from customers connected to servers operated by other Xanadu-licensed storage vendors." [5/14]

> Storage Vendor must "use software furnished by Project Xanadu without modification." [5/14]

Without the franchise contract, a node cannot participate in the trust model that holds the docuverse together. The contract is as much a part of the system as the code.

## Summary: The Minimal Set

| Property | Ghost Node | Live Node |
|----------|-----------|-----------|
| Tumbler address (baptized) | Required | Required |
| Ownership (who controls sub-numbers) | Required | Required |
| Network model (subrepresentation) | Not needed | Required (null is valid) |
| Protocol capability (FEBE/BEBE) | Not needed | Required |
| Franchise contract | Not needed | Required |

A ghost node is **two properties**: address and ownership. A live node adds **three more**: a (possibly null) network model, protocol compliance, and contractual standing.

The deeper point: the docuverse is populated by concepts, not objects. A node exists the moment its number is baptized. It *functions* the moment it can speak the protocols and honor the contract. Between those two moments, it is a ghost — addressable, linkable, but empty.

NEED_RAW: [4/74-4/75] — these pages discuss the connection model and network resilience in detail; they may contain additional specifics about what a node must establish when it first joins the network (handshake, initial synchronization).

---

## Question 2 [nelson]

> Must every node receive a permanent, globally unique identity, and is that identity assigned by the system or derived from the node's content?

### Nelson's Answer

## Yes — every node receives a permanent, globally unique identity, and it is *assigned*, not content-derived.

### Permanence and Global Uniqueness

Every entity in the docuverse — server nodes, accounts, documents, versions, individual bytes, links — receives a **permanent tumbler address** that is globally unique:

> "New items may be continually inserted in tumbler-space while the other addresses remain valid. This means that any address of any document in an ever-growing network may be specified by a permanent tumbler address." [LM 4/19]

The entire docuverse begins from a single root:

> "The server address always begins with the digit 1, since all other servers are descended from it. This may seem an unnecessary redundancy, but it permits referring to the entire docuverse by '1' on the first position." [LM 4/28]

Every tumbler is unique by construction — the hierarchical forking process guarantees no two entities share an address.

### Assignment, Not Derivation

Identity is assigned through **"baptism"** — a delegation mechanism where the owner of a parent address creates sub-addresses:

> "The basic principle is that of owned numbers. Numbers are owned by individuals or companies, and subnumbers under them are bestowed on other individuals and companies on whatever basis the owners choose. Whoever owns a specific node, account, document or version may in turn designate (respectively) new nodes, accounts, documents and versions, by forking their integers. We often call this the 'baptism' of new numbers." [LM 4/17]

This is purely positional/structural. Nelson is explicit that tumblers carry no semantic weight:

> "Tumblers do not affect the user-level structure of the documents; they only provide a mapping mechanism, and impose no categorization and no structure on the contents of a document." [LM 4/17–4/18]

### Not Content-Addressed

Xanadu uses **identity-based addressing** (where content was created), not **content-based addressing** (what it contains). Two identical strings created independently in different documents receive different I-space addresses. Conversely, transcluded content shares the *same* I-address as the original — not because the bytes match, but because they are literally the same bytes referenced by inclusion.

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

The I-address encodes provenance (Node.0.User.0.Document.0.Element), not a hash of content.

### Ghost Elements: Identity Without Storage

Even entities that have no physical representation in storage receive permanent addresses:

> "While servers, accounts and documents logically occupy positions on the developing tumbler line, no specific element need be stored in tumbler-space to correspond to them. Hence we may call them ghost elements." [LM 4/23]

> "It is possible to link to a node, or an account, even though there is nothing stored in the docuverse corresponding to them." [LM 4/23]

A node's identity exists the moment it is baptized — before any content is stored there, before any accounts are created under it.

### Summary

| Property | Answer |
|----------|--------|
| Globally unique? | Yes — by construction (hierarchical forking) |
| Permanent? | Yes — addresses never become invalid |
| Assigned or derived? | Assigned — through "baptism" by parent owner |
| Content-dependent? | No — identity is positional, not content-based |
| Requires stored object? | No — ghost elements have addresses without storage |

---

## Question 3 [nelson]

> Once a node has entered the docuverse, can it ever be removed, or must the node set grow monotonically?

### Nelson's Answer

## Nodes Cannot Be Removed from the Address Space

The node set must grow monotonically. Once a node address is assigned ("baptized"), it is permanently part of tumbler-space. However, the *physical infrastructure* behind a node can change or disappear — what persists is the address, not the machine.

### The Address Is Permanent

Nelson is explicit that tumbler addresses, once assigned, never become invalid:

> "New items may be continually inserted in tumbler-space while the other addresses remain valid. This means that any address of any document in an ever-growing network may be specified by a permanent tumbler address." [LM 4/19]

Since every document, account, and byte address *beneath* a node includes that node's address as a prefix (e.g., `1.3.0.U.0.D.0.E` for anything on node 1.3), removing the node would invalidate every address under it. This would violate the permanence guarantee.

### Ghost Nodes Are Valid Nodes

Nelson directly addresses what happens when a node has no physical representation — it becomes a **ghost element**:

> "While servers, accounts and documents logically occupy positions on the developing tumbler line, no specific element need be stored in tumbler-space to correspond to them. Hence we may call them ghost elements." [LM 4/23]

> "However, these elements are virtually present in tumbler-space, since links may be made to them which embrace all the contents below them." [LM 4/23]

A node whose physical server has been decommissioned still exists as a position on the tumbler line. Links to that node address (or to any address beneath it) remain valid.

### Physical Infrastructure Can Change

Nelson separates the address from the machine. The vendor contract requires orderly transition when a vendor shuts down:

> "Upon notice of cancellation, Storage Vendor will arrange for the orderly transition of all customer-stored materials to other Xanadu locations." [LM 5/16]

Content migrates; the address stays. The BEBE protocol handles this through subrepresentation — other servers hold copies and maps:

> "Each server contains a map and a subset of the whole — a microcosm that shrinks and grows." [LM 4/71]

Nelson also acknowledges that nodes go offline routinely:

> "It is a truism that 'computer networks are always broken.' Meaning that on the average some nodes are disconnected or not working." [LM 4/75]

Temporary unavailability is handled by redundancy and backup copies, not by removing the node from the address space.

### Why This Must Be So

The docuverse is defined as the *occupied tumbler-space* — occupied by conceptual assignment, not physical storage:

> "The docuverse is the occupied tumbler-space — as occupied by conceptually assigned positions, even if nothing represents them in storage." [LM 4/23]

Removing a node would mean un-assigning its position, which contradicts the fundamental nature of the addressing system. The forking mechanism only adds — "nodes can spin off nodes" [LM 4/19] — and there is no corresponding un-fork operation anywhere in the specification.

### Summary

| Aspect | Can it be removed? |
|--------|-------------------|
| Node address in tumbler-space | **No** — permanent |
| Physical server hardware | Yes — content migrates |
| Vendor license | Yes — with orderly transition |
| Content stored at node | Yes — moves to other locations |
| Links pointing to node's address range | **No** — remain valid (may resolve to ghost or backup) |

The node set grows monotonically in addressing terms. A decommissioned node becomes a ghost element — addressable, linkable, but with no physical representation. Its content lives elsewhere; its address endures.

---

## Question 4 [nelson]

> Is the admission of a new node an atomic event — either fully present in the docuverse or fully absent — with no intermediate state?

### Nelson's Answer

## No — Node Admission Is Explicitly Gradual, Not Atomic

Nelson describes node integration as an **incremental, always-valid process** with clear intermediate states. The evidence comes from three converging aspects of the design.

### 1. The "Null Case" Progression

The most direct evidence is from 4/72, where Nelson describes server state:

> "A server's network model, from the null case on up, is at all times unified and operational; whatever information moves between servers is assimilated at once to its overall structure, leaving each server in canonical operating condition with a slightly improved map of what is elsewhere." [4/72]

The phrase **"from the null case on up"** explicitly names the starting state: empty. The server begins with nothing and accumulates incrementally. Each increment leaves it in "canonical operating condition" — there is no invalid transitional state, but there are many intermediate states between empty and fully populated.

### 2. Ghost Elements: Address Before Content

A new node can exist as a **ghost element** — an addressable position with no stored content:

> "While servers, accounts and documents logically occupy positions on the developing tumbler line, no specific element need be stored in tumbler-space to correspond to them. Hence we may call them ghost elements." [4/23]

> "However, these elements are virtually present in tumbler-space, since links may be made to them which embrace all the contents below them." [4/23]

This means a node address can be "baptized" (forked from a parent) and be linkable, referenceable, and addressable **before any content exists under it**. The node is neither fully absent (its address is valid, links can target it) nor fully present (it holds nothing). This is an explicit intermediate state.

### 3. The Microcosm Model

Each server is described as a growing/shrinking subset:

> "Each server contains a map and a subset of the whole — a microcosm that shrinks and grows." [4/71]

A new node starts with a minimal microcosm and grows it through BEBE exchanges. Content "sloshes" in as demand requires. The server doesn't receive a complete snapshot of the docuverse at admission — it builds its model incrementally.

### What IS Atomic

Two aspects may be atomic, though Nelson does not use the word:

1. **Address baptism** — The parent node owner designates the new node's address. This is a discrete act: "The owner of a given item controls the allocation of the numbers under it" [4/20]. Before baptism, the address doesn't exist; after, it does.

2. **Franchise contract** — The Storage Vendor signs a contract with Project Xanadu [5/14]. This is a legal event, not a technical one.

But neither of these makes the node "fully present in the docuverse." The address exists; the vendor is licensed; the node then begins operating from the null case, incrementally building its model and content.

### The Design Principle

Nelson's architecture is designed so that **every intermediate state is valid**. A server with one document is as "canonical" as a server with a million. There is no bootstrap phase where the node is partially broken. This follows from the same principle that makes the docuverse itself open-ended: a span that "contains nothing today may at a later time contain a million documents" [4/25].

### Summary

Node admission has at least three distinguishable states: (1) address not yet baptized, (2) address exists as ghost element with no content, (3) operational server with growing microcosm. The transition between these is gradual. Nelson explicitly rejects the need for atomicity by ensuring every state along the progression is "unified and operational."

NEED_RAW: [4/72] — The curated BEBE and network extracts give slightly different transcriptions of the same passage ("from the full sweep up" vs "from the null case on up"). The raw page would resolve the exact wording, though both readings support the same conclusion.

---

## Question 5 [nelson]

> Does the design distinguish different kinds of nodes (content-bearing, linking, versioning), or is there a single universal node type?

### Nelson's Answer

## Single Universal Node Type: The Document

Xanadu does **not** distinguish different kinds of nodes. There is one universal container — the **document** — and exactly two stored primitives within it: **bytes** and **links**.

### The Document Is Everything

Nelson is explicit that the document is the sole organizational unit:

> "The Xanadu document is the unit of the system. There is almost nothing in the Xanadu system but Xanadu documents." [LM 4/6]

> "By this convention, then, everything in the system is part of a document. No free-floating materials exist. Thus the 'Jabberwocky' is a document; and a set of links between them, were someone to create it, would yet be a separate document." [LM 2/29]

A document that contains only links is just as valid as one containing only text. A document of annotations pointing into someone else's work is simply a document whose content happens to be links. There is no "link node" or "annotation node" — there are only documents.

### Two Stored Primitives, Not Two Node Types

At the storage level, exactly two kinds of entities exist:

> "In the present implementation (XU.87.1), the only entities actually stored in tumbler-space are content bytes and links." [LM 4/23]

These are distinguished by their address subspace within a document — bytes occupy the `0.1.x` subspace and links occupy the `0.2.x` subspace — but both live inside the same universal document container.

### Versioning Is Not a Separate Node Type

Versions are documents. A version's tumbler address indicates ancestry through the document field's subdivision, but Nelson is careful to note this is structural, not categorical:

> "The Document field of the tumbler may be continually subdivided, with new subfields in the tumbler indicating daughter documents and versions." [LM 4/29]

> "In a sense the version, or subdocument number is only an accidental extension of the document number, and strictly implies no specific relationship of derivation." [LM 4/29]

> "There is thus no 'basic' version of a document set apart from other versions—'alternative' versions—any more than one arrangement of the same materials is a priori better than other arrangements." [LM 2/19]

Versions are not a special node type. They are documents whose address happens to be "under" another document's address.

### Ghost Elements: Addresses Without Nodes

Servers, accounts, and documents themselves are not even stored objects — they are positions on the tumbler line with no corresponding storage:

> "While servers, accounts and documents logically occupy positions on the developing tumbler line, no specific element need be stored in tumbler-space to correspond to them. Hence we may call them ghost elements." [LM 4/23]

This reinforces the uniformity. The only things that actually exist in storage are bytes and links. Everything else — servers, accounts, documents, versions — is an addressing convention, not a node type.

### Links Are Owned by Documents, Not Separate

A crucial design point: links don't float independently. They live in a "home document" that determines ownership:

> "A link need not point anywhere in its home document. Its home document indicates who owns it, and not what it points to. Conversely, links connecting parts of a document need not reside in that document." [LM 4/12]

Your annotations on someone else's work are links in **your** document pointing at **their** content. The link's home determines ownership; its endsets determine what it connects. But it is not a separate node — it is an element within a document.

### Summary

The architecture is radically uniform:

| Level | What exists |
|-------|------------|
| **Stored primitives** | Bytes and links (the only things actually in storage) |
| **Container** | Document (the universal, single node type) |
| **Address positions** | Servers, accounts, versions (ghost elements — no storage representation) |

Nelson captures this uniformity in one sentence:

> "So the docuverse is all really one big forking document." [LM 4/18]

And the link mechanism confirms there are only two things:

> "The link mechanism ties together the whole corpus of materials on the Xanadu system. There is essentially nothing in the Xanadu system except documents and their arbitrary links." [LM 4/41]

---

## Question 6 [nelson]

> Must the set of all nodes carry a total ordering that reflects the sequence in which they entered the docuverse?

### Nelson's Answer

## No. The tumbler line carries a total ordering, but it reflects tree structure, not temporal sequence.

### What the tumbler line does order

All tumblers — including node addresses — fall on a single totally ordered line. This is a depth-first traversal of the forking tree:

> "In a sense the tumbler line is like the real line, i.e., the line of integers and all the numbers in between. But the tumbler line is a different kind of abstraction from the real line. The real line is the same under all circumstances. The tumbler line is an abstract representation of a particular tree." [LM 4/22]

> "The contents of the tumbler line are determined by the population of entities and relations on the tree it represents. Thus the tumbler line is not definite in the same way as the real line; the tumbler line is a flat mapping of a particular tree, finite but unlimited." [LM 4/22]

So yes, every node has a definite position on a totally ordered line — but that ordering encodes **parentage and sibling position**, not time of arrival.

### Sibling order does reflect creation sequence

Under a given parent, children are numbered sequentially as they are created:

> "One digit can become several by a forking or branching process. This consists of creating successive new digits to the right; we call these 'under' the previous digit." [LM 4/20]

> "For instance, if there is an item 2, it can branch into several more items, each of which is a daughter item. Thus 2.1, 2.2, 2.3, 2.4... are successive items being placed under 2." [LM 4/20]

Node 1.1 was created before node 1.2 under the root. That much is encoded.

### But the total ordering does not reflect global temporal sequence

The depth-first traversal puts all descendants of node 1.1 before node 1.2 on the tumbler line:

```
1, 1.1, 1.1.1, 1.1.2, ..., 1.2, 1.2.1, ...
```

Node 1.2 might have been created years before node 1.1.1, yet 1.1.1 precedes 1.2 on the tumbler line. The ordering reflects the tree, not the calendar.

### Time is explicitly excluded from the tumbler

Nelson is direct about this:

> "Note that 'time' is not included in the tumbler. Time is kept track of separately." [LM 4/18]

Time is metadata maintained alongside the address system, not encoded in it. You can ask "when was this node created?" but the answer comes from a separate mechanism, not from the address itself.

### Why this matters architecturally

The tumbler's job is **permanent addressing in a decentralized system**, not temporal ordering. The design priorities are:

1. **Stability** — existing addresses never change when new nodes arrive
2. **Decentralization** — owners baptize sub-addresses without coordination
3. **Span efficiency** — contiguous subtrees map to contiguous ranges

A global temporal ordering would require either a central sequencer (violating decentralization) or consensus among nodes (violating simplicity). Nelson chose tree-structural ordering instead, which requires only local coordination: the parent assigns the next sibling number.

### Summary

| Scope | Does ordering reflect creation sequence? |
|-------|----------------------------------------|
| Among siblings of one parent | **Yes** — sequential baptism |
| Across different branches | **No** — depth-first tree order, not temporal |
| Globally across all nodes | **No** — time is kept separately |

The nodes carry a total ordering, but it is the depth-first linearization of a forking tree — not a chronicle of when they joined the docuverse.

---

## Question 7 [nelson]

> Can two distinct nodes hold identical content, or must every node differ from every other node in at least one property?

### Nelson's Answer

## Two Distinct Nodes CAN Hold Identical Content

Yes, two distinct nodes can — and are *designed* to — hold identical content. This is a core feature of the BEBE protocol, not an edge case.

### Nodes Are Distinct by Address, Not by Content

Every node has a unique tumbler address (the Node field). Nelson states:

> "The server address always begins with the digit 1, since all other servers are descended from it." [LM 4/28]

So nodes always differ in identity. But their *contents* are explicitly expected to overlap.

### Replication Is by Design

Nelson describes four reasons content moves between servers:

> "Material is moved between servers for a number of purposes:
> 1. for more rapid access to final material,
> 2. for more rapid access to needed material which indexes material on other servers,
> 3. for rebalance in keeping with demand,
> 4. for redundancy and backup purposes." [LM 4/71]

Each server holds a "microcosm" of the docuverse that grows and shrinks:

> "Each server contains a map and a subset of the whole — a microcosm that shrinks and grows." [LM 4/71]

> "The contents can slosh back and forth dynamically." [LM 4/72]

Two nodes could hold entirely overlapping content subsets — nothing forbids it, and redundancy actively encourages it.

### But: Home Location Is Singular

While content can be *replicated* across nodes, each byte has exactly one **home location** — its permanent I-space address, which encodes the originating node:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

The I-address structure `Node.0.User.0.Document.0.Element` permanently records *where* content was created. Copies on other nodes are subrepresentations, not native content.

### Independent Creation ≠ Same Content

One important nuance: if two users on different nodes independently type the same text, those are **different content items** with different I-addresses (different Node fields). Content identity is based on creation provenance, not byte value. Identical content on multiple nodes arises through replication (BEBE), not coincidence.

### Summary

| Property | Must nodes differ? |
|----------|-------------------|
| **Tumbler address (Node field)** | Yes — always unique |
| **Content held** | No — overlap is expected and designed for |
| **Native content (home I-addresses)** | Yes — each node's native bytes have that node's address |
| **Cached/replicated content** | No — any node may cache any other node's content |

---

## Question 8 [nelson]

> What preconditions must hold before a node is permitted to enter — must all nodes it references already exist, or can forward references be admitted?

### Nelson's Answer

## Forward References Are Explicitly Admitted

Nelson's architecture imposes **no precondition that referenced nodes must already exist**. The system is designed from the ground up to permit references to addresses where nothing is stored. This is not an edge case or oversight — it is a named, deliberate design feature called **ghost elements**.

### Ghost Elements: The Definitive Statement

From Literary Machines 4/23:

> "While servers, accounts and documents logically occupy positions on the developing tumbler line, no specific element need be stored in tumbler-space to correspond to them. Hence we may call them ghost elements." [LM 4/23]

> "However, these elements are virtually present in tumbler-space, since links may be made to them which embrace all the contents below them." [LM 4/23]

> "It is possible to link to a node, or an account, even though there is nothing stored in the docuverse corresponding to them." [LM 4/23]

This is unambiguous: you can create a link whose endset points to an address that has no stored content. The link is valid. The address is valid. The referenced entity simply doesn't exist yet (or may never exist).

### The Span Guarantee Reinforces This

Spans — the fundamental unit for referencing content — are explicitly designed to tolerate emptiness:

> "A span that contains nothing today may at a later time contain a million documents." [LM 4/25]

A span is not a count of items. It designates a region of tumbler-space. Whether that region is populated is orthogonal to whether the span is valid.

### Link Types Depend on Forward References

The link type system is built on ghost elements as a core design pattern, not an exception:

> "Indeed, there is no need for the presence of elements at the addresses specified. Link types may be ghost elements." [LM 4/45]

> "What the 'type' designation points to is completely arbitrary. This is because of the way we will be searching for links. The search mechanism does not actually look at what is stored under the 'type' it is searching for; it merely considers the type's address." [LM 4/44-4/45]

Link types are matched by **address**, not by content. An address can designate a type even if nothing is ever stored there. This means the system's type taxonomy itself operates through forward (or permanently vacant) references.

### The Docuverse Is Sparse by Design

Only two kinds of entities are actually stored: content bytes and links. Everything else — servers, accounts, documents — are positions on the tumbler line with no corresponding stored object:

> "In the present implementation (XU.87.1), the only entities actually stored in tumbler-space are content bytes and links. While a number on the line may represent a document or an account, that doesn't mean there's an object stored for it. What's stored is the contents--bytes and links." [LM 4/23]

> "The docuverse is the occupied tumbler-space--as occupied by conceptually assigned positions, even if nothing represents them in storage." [LM 4/23]

The address space is conceptually infinite and mostly empty. Requiring pre-existence of referenced nodes would contradict the fundamental architecture.

### Why This Must Be So

The forking mechanism makes pre-existence requirements impractical. Addresses are created by subdivision — the owner of address 2 can create 2.1, 2.2, 2.3 at will [LM 4/20]. In a decentralized system with no central coordinator, there is no way to atomically verify that a target address is populated before creating a reference to it. Nelson's design sidesteps this entirely: **all addresses are valid; population is optional.**

### Summary

No preconditions on referenced node existence. The architecture admits forward references, permanently vacant references, and references to the entire unpopulated subtree beneath any address. Ghost elements are the mechanism; address-based (not content-based) resolution is the principle.

---

## Question 9 [nelson]

> Must the identity of a node remain stable across all subsequent versions, or does versioning produce a new node with a new identity?

### Nelson's Answer

## Versioning Produces a New Node; the Original's Identity Is Absolutely Stable

The answer is unambiguous across multiple parts of Literary Machines: **versioning creates a new entity with its own distinct identity. The original node retains its address and identity unchanged.**

### The Operation Itself

CREATENEWVERSION is defined as:

> "This creates a new document with the contents of document \<doc id\>. It returns the id of the new document. The new document's id will indicate its ancestry." [LM 4/66]

Three things to note: it creates a **new document**, it returns a **new id**, and that id **indicates ancestry**. The original document is not modified or replaced.

### Address Permanence

The tumbler guarantee is absolute:

> "New items may be continually inserted in tumbler-space while the other addresses remain valid. This means that any address of any document in an ever-growing network may be specified by a permanent tumbler address." [LM 4/19]

The original's tumbler address does not change, expire, or redirect.

### How Version Identity Works in the Address Structure

Versions are encoded as subdivisions of the Document field in the tumbler:

> "The Document field of the tumbler may be continually subdivided, with new subfields in the tumbler indicating daughter documents and versions." [LM 4/29]

So if the original document is `1.0.3.0.7`, a version might be `1.0.3.0.7.1` — a sub-address under the original. But Nelson adds a critical caveat:

> "In a sense the version, or subdocument number is only an accidental extension of the document number, and strictly implies no specific relationship of derivation." [LM 4/29]

The tumbler **encodes** lineage structurally but does **not enforce** that the relationship is one of semantic derivation. The address tells you where the version came from in the forking tree, not what its content relationship is to its parent.

### Both Versions Are Equally Valid

Nelson explicitly rejects the notion of a "primary" version:

> "There is thus no 'basic' version of a document set apart from other versions—'alternative' versions—any more than one arrangement of the same materials is a priori better than other arrangements." [LM 2/19]

Both the original and the new version are first-class documents with their own addresses, their own ownership, and their own V-space arrangements.

### What They Share: I-Space Content

The two versions share I-space content. The new version starts with the same V-to-I mappings as the original. This shared I-space origin is what enables **correspondence** — the system can compute which parts match:

> "Of course, a facility that holds multiple versions of the same material, and allows historical backtrack, is not terribly useful unless it can help you intercompare them in detail—unless it can show you, word for word, what parts of two versions are the same." [LM 2/20]

And links made to one version can follow through to corresponding content in another:

> "Links may be refractively followed from a point or span in one version to corresponding places in any other version. Thus a link to one version of a Prismatic Document is a link to all versions." [LM 2/26]

### Why This Matters

The permanence of published documents depends on this design. Once others have linked to your document:

> "It is in the common interest that a thing once published stay published, as in the world of paper. Other readers and users will come to depend on its accessibility." [LM 2/43]

If versioning mutated the original's identity, every link made to it would be disrupted. Instead, the original stands, the new version stands beside it, and the correspondence mechanism connects them.

### Summary

| Aspect | Original Document | New Version |
|--------|-------------------|-------------|
| **Identity (tumbler)** | Unchanged | New address (sub-address of original) |
| **I-space content** | Unchanged | Initially shares I-space; may diverge with edits |
| **V-space arrangement** | Unchanged | Initially identical; independent thereafter |
| **Status** | First-class document | First-class document (no hierarchy) |
| **Correspondence** | Computable via shared I-addresses | Computable via shared I-addresses |
| **Links to it** | Still valid | New links go to new address |

Versioning is forking, not mutation. The original is permanent; the version is new.

---

## Question 10 [nelson]

> If multiple users simultaneously create nodes, what must the system guarantee about the consistency and disjointness of the resulting node identities?

### Nelson's Answer

## Node Identity: Disjointness and Consistency Under Concurrent Creation

Nelson does not explicitly address the concurrent-creation scenario in Literary Machines. However, the tumbler architecture makes the answer fall out structurally: **disjointness is guaranteed by ownership, not by coordination.**

### The Baptism Mechanism

The core principle is ownership-based delegation:

> "The basic principle is that of owned numbers. Numbers are owned by individuals or companies, and subnumbers under them are bestowed on other individuals and companies on whatever basis the owners choose. Whoever owns a specific node, account, document or version may in turn designate (respectively) new nodes, accounts, documents and versions, by forking their integers. We often call this the 'baptism' of new numbers." [LM 4/17]

> "The owner of a given item controls the allocation of the numbers under it." [LM 4/20]

This means: if Alice owns node `1.2` and Bob owns node `1.3`, Alice creates sub-nodes `1.2.1, 1.2.2, ...` and Bob creates `1.3.1, 1.3.2, ...`. They operate in **structurally disjoint subtrees**. No coordination is needed between them.

### What the System Must Guarantee

**1. Subtree disjointness (architectural, automatic):**
Different owners' subtrees never overlap. Two users creating nodes simultaneously under different parent addresses produce addresses that are guaranteed distinct by the tree structure itself.

**2. Sequential uniqueness within a single owner's scope:**
When a single owner (e.g., a server allocating accounts) must assign successive numbers to concurrent requestors, the system must serialize those assignments. If server `1.2` creates accounts for two simultaneous sign-ups, it must produce `1.2.0.3` and `1.2.0.4`, never `1.2.0.3` twice. This is a local problem — one owner, one counter.

**3. Permanence of assigned addresses:**

> "New items may be continually inserted in tumbler-space while the other addresses remain valid. This means that any address of any document in an ever-growing network may be specified by a permanent tumbler address." [LM 4/19]

Once baptized, an address is permanent. The system must never reassign it.

**4. Canonical condition after every operation:**

> "All changes, once made, left the file remaining in canonical order, which was an internal mandate of the system." [LM 1/34]

> "A server's network model, from the null case on up, is at all times unified and operational; whatever information moves between servers is assimilated at once to its overall structure, leaving each server in canonical operating condition with a slightly improved map of what is elsewhere." [LM 4/72]

After any creation, every server must remain in a valid, queryable state.

### Why Central Coordination Is Not Needed

The architecture eliminates the hard concurrency problem by design. Two servers in different parts of the world can each create thousands of sub-nodes per second without consulting each other, because:

- Server `1.5` creates under `1.5.*`
- Server `1.8` creates under `1.8.*`
- The resulting addresses are structurally guaranteed disjoint

The only point requiring serialization is **within a single owner's allocation counter**, which is local state.

> "The entire tumbler works like that: nodes can spin off nodes; accounts can spin off accounts; nodes can spin off accounts; and so on. Thus all numeration in the docuverse is compressed into a single mechanism." [LM 4/19]

> "So the docuverse is all really one big forking document." [LM 4/18]

### What Nelson Does NOT Specify

Nelson does not address:
- How a single server serializes concurrent allocations internally (implementation detail)
- What happens if two servers claim the same parent address (prevented by the franchise model — servers get assigned disjoint node numbers)
- Consistency protocols for propagating new node existence across the network (BEBE handles this incrementally, but the details are proprietary)

NEED_RAW: [4/70-4/75] — The BEBE protocol pages may contain additional detail about how node creation events propagate between servers, though the curated sources suggest this was still "undergoing definition."

### Summary

The system guarantees:

| Property | Mechanism |
|----------|-----------|
| **Disjointness across owners** | Structural — different subtrees cannot collide |
| **Uniqueness within an owner** | Sequential allocation — local serialization |
| **Permanence** | Once baptized, never reassigned |
| **Canonical state** | Every server remains valid after every operation |

The insight is that Nelson designed away the distributed consensus problem. You don't need agreement on "who gets address X" when every owner has an infinite, exclusive subtree to allocate from.

---

## Question 11 [gregory]

> In the tumbler hierarchy `Node.0.User.0.Doc.0.Element`, what concrete entity does the node field (e.g., `1.1`) represent — a running backend instance, a persistent address partition, or something else?

### Gregory's Answer

## KB Synthesis

The KB describes the node field's structural role clearly but does not characterize what real-world entity it represents.

**What the KB does say:**

The tumbler pattern `1.1` is the top level of the docuverse address hierarchy [SS-TUMBLER, Finding 0001]. Accounts (users) live *under* nodes, separated by a `.0.` boundary — so `1.1.0.1` is account 1 under node `1.1`, and `1.1.0.2` is account 2 under the same node [SS-ADDRESS-SPACE, Finding 0021].

The `makehint` depth table [SS-ADDRESS-SPACE, Finding 0021] shows `NODE → NODE` with depth=1, meaning nodes can be nested under other nodes (no `.0.` crossing for node-under-node). This recursive nesting is structurally identical to version chains under documents [SS-VERSION-ADDRESS, Finding 0068].

The address layout from [SS-ADDRESS-SPACE, Finding 0077] places the node prefix `1.1` above accounts and never elaborates on what instantiated the node. The containment predicate [SS-TUMBLER-CONTAINMENT, Finding 0021] treats node addresses the same as any other prefix — purely as a tumbler hierarchy level.

**What the KB does not say:**

The KB contains no finding that identifies whether node addresses correspond to running backend processes, persistent administrative partitions, hardware machines, or something else. The backend is described as a single daemon ([SS-SESSION-STATE, Finding 0022]), but there is no finding connecting that daemon's identity to the `1.x` node prefix in any explicit way.

The node field's real-world semantics — whether it represents a server in a distributed docuverse network, a logical partition, or an installation-time constant — is not answerable from the KB as written.

---

## Code Exploration

Here is the full answer:

---

## What the Node Field (`1.1`) Represents

**Short answer:** The node field is a **persistent, statically-assigned address prefix** for a server/site in the Xanadu distributed address space — the top-level namespace partition. In udanax-green it is hardcoded to `1.1` and never changes at runtime.

---

### The Tumbler Structure

`common.h:59-67`:
```c
typedef struct structtumbler {
    humber xvartumbler;
    char varandnotfixed;
    char sign BIT;
    short exp;
    tdigit mantissa[NPLACES];  /* NPLACES = 16 */
} tumbler;

#define ZEROTUMBLER  {0,0,0,0,  0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0}
```

The mantissa is a flat array of integers. **Zero is a level separator.** So the tumbler `1.1.0.1.0.1` is stored as `mantissa[] = {1, 1, 0, 1, 0, 1, 0, 0, ...}`.

The four hierarchy levels are named in `xanadu.h:140-143`:
```c
#define NODE      1
#define ACCOUNT   2
#define DOCUMENT  3
#define ATOM      4
```

These are not runtime IDs — they are constants used as arguments to `makehint()` to describe what kind of address to allocate.

---

### Node = `1.1` Is Hardcoded

`be.c:37` (single-connection backend):
```c
tumbler defaultaccount = {0,0,0,0, 1,1,0,1,0,0,0,0}; /* 1.1.0.1 */
```

`socketbe.c:35` (multi-connection backend):
```c
tumbler defaultaccount = {0,0,0,0,  1,1,0,14,0};
```

In both cases the mantissa starts `[1, 1, 0, ...]`. The comment `/* 1.1.0.1 */` confirms the encoding: node = mantissa positions 0–1 = `1.1`, separator = `0`, account = `1`.

This value is placed directly into `task.account` at startup (`be.c:88`):
```c
movetumbler(&defaultaccount, &task.account);
```

And in the multi-user backend, it is populated per-connection from the `player[]` array (`bed.c:123`):
```c
task.account = player[user].account;
```

There is **no code that assigns a node ID based on the running process, socket, PID, or network**. No node configuration exists in `.backendrc` either — `rcfile.c` supports configuring `port`, `host`, `allocsize`, directory names, but has no `node` key.

---

### How Node-Level Addresses Are Created

`do1.c:243-258`:
```c
bool docreatenode_or_account(typetask *taskptr, typeisa *isaptr)
{
    typeisa isa;
    typehint hint;
    tumblercopy(isaptr, &isa);
    makehint(NODE, NODE, 0, &isa, &hint);
    result = createorglingranf(taskptr, granf, &hint, &isa);
    if (result) {
        tumblercopy(&isa, isaptr);
    }
    return result;
}
```

The `makehint(NODE, NODE, ...)` call means: *allocate a new address at the node level, within an existing node's subtree*. The hint tumbler `isa` (passed in from the frontend) is used as the parent. `findisatoinsertnonmolecule` (`granf2.c:203-241`) then finds the highest existing address at that level and increments it, returning the newly allocated node address.

The comment at `granf2.c:150-151` makes the format explicit:
> "making the first document get the account address itself (`1.1.0.1` instead of `1.1.0.1.0.1`)"

So a full document address has the form: **`Node.0.Account.0.Document.0.Atom`** = e.g. `1.1.0.1.0.1.0.1`.

---

### What the Node Field Concretely Is

The node field was designed as the **globally unique persistent identifier for a Xanadu server/site** in a federated network. The two-component form (`1.1`) mirrors how Xanadu originally envisioned multi-level server hierarchies (think of it as a org-level + server-level address, analogous to how IP addresses were conceived for networks).

In udanax-green's actual implementation:

| Hypothesis | Verdict | Evidence |
|---|---|---|
| Running backend instance | **No** | Node is hardcoded; multiple instances would all say `1.1` |
| Persistent address partition | **Yes** | Same value survives restarts; hardcoded in source |
| Configurable per-site | **Intended yes, implemented no** | No node key in `.backendrc`; no command-line argument |
| Network-assigned in federated Xanadu | **Intended yes** | Design artifact of the distributed Xanadu vision |

In udanax-green as shipped, **the node field is a permanently fixed, hardcoded namespace prefix** — a vestige of the distributed-Xanadu architecture. Every document address on this server starts with `1.1.0.`. The concept of distinct nodes (`2.1`, `3.4`, etc.) exists in the address space and allocation logic, but no running instance of this codebase ever claims any node other than `1.1`.

---

## Question 12 [gregory]

> How is a node's tumbler address assigned — is there a global allocation authority, a bootstrap configuration file, or does the first backend instance self-assign from a convention?

### Gregory's Answer

## KB Synthesis

Not fully answerable from the KB.

The KB extensively documents how addresses are allocated *within* an existing hierarchy: documents under accounts via `findisatoinsertnonmolecule` [SS-ADDRESS-ALLOC], links under documents via `findisatoinsertmolecule` [SS-ADDRESS-SPACE, Finding 0065], versions under documents [SS-VERSION-ADDRESS, Finding 0068]. The pattern is always the same: query the granfilade for the highest existing address below an upper bound, then increment.

But the KB stops at the account level. We know from the address structure that a docuverse address like `1.1.0.1.0.2` encodes `Node.0.User.0.Doc`, making `1.1` the node prefix [SS-TUMBLER, Finding 0001]. We know `enf.enf` is the single persistent file that stores all state [SS-UNIFIED-STORAGE, Finding 0059], and that initialization calls `createenf(GRAN)` and `createenf(SPAN)` [SS-DUAL-ENFILADE, Finding 0012]. We also know type registry entries live at bootstrap document `1.0.2.x` [SS-LINK-ENDPOINT, Finding 0024], implying some initial state exists.

What the KB does not contain is any finding about:
- How the node's own tumbler (`1.1`, `1.2`, etc.) is chosen at startup
- Whether there is a configuration file that sets the node address
- Whether the backend self-assigns from a convention (e.g., always `1.1` for a single-node deployment)
- Whether a global authority allocates node addresses before a backend can join

The exploration work captured findings about operation-level allocation mechanics but did not probe the bootstrap question — how the initial granfilade state with a node address comes to exist in the first place.

---

## Code Exploration

I now have a complete picture of the entire address-assignment machinery. Here is the answer.

---

## How a Node's Tumbler Address is Assigned in udanax-green

**Short answer: self-assignment from a hardcoded compile-time constant. There is no global allocation authority and no configuration file for this.**

---

### 1. The backend's identity address is a static literal

The backend's own tumbler address — its "account" — is declared as an initialized global variable in `be.c:37`:

```c
tumbler defaultaccount = {0,0,0,0, 1,1,0,1,0,0,0,0}; /* 1.1.0.1 */
```

The `tumbler` struct (`common.h:59-65`) is:

```c
typedef struct structtumbler {
    humber xvartumbler;   /* = 0 */
    char varandnotfixed;  /* = 0 */
    char sign;            /* = 0  (positive) */
    short exp;            /* = 0  (normalized) */
    tdigit mantissa[16];  /* {1, 1, 0, 1, 0, 0, ...} */
} tumbler;
```

So `defaultaccount` decodes to tumbler `1.1.0.1`. This is a literal constant in source code, not read from anywhere at runtime.

It is installed into the active task context immediately after startup at `be.c:88`:

```c
movetumbler(&defaultaccount, &task.account);
```

Every subsequent request handler reads the account from `taskptr->account`, which now permanently equals `1.1.0.1`.

---

### 2. The `.backendrc` configuration file is irrelevant to tumbler addresses

`rcfile.c` defines every key the `.backendrc` file recognizes (`rcfile.c:19-29`):

```c
#define PORTMETANAME                 "port"
#define HOSTMETANAME                 "host"
#define BACKENDDIRECTORYMETANAME     "backenddir"
#define BACKENDFILEMETANAME          "backend"
#define ACCOUNTFILEMETANAME          "accountfile"
#define FRONTENDFILEMETANAME         "frontend"
#define BACKENDGLUEFILEMETANAME      "backglue"
#define FRONTENDGLUEFILEMETANAME     "frontglue"
#define ALLOCSIZENAME                "allocsize"
#define INCREMENTALALLOCSIZENAME     "incrementalallocsize"
```

There is no tumbler-address key. `processrcfile()` is called at `be.c:73` (and `xumain.c:39`) before `initmagicktricks`, but it cannot affect the node's identity — there is no field for it.

---

### 3. The interactive standalone build uses the zero address instead

The standalone `xumain.c` build calls `getaccount` at `xumain.c:49`:

```c
getaccount(&task, &task.account);
```

But `task.c:28-33` shows `getaccount` simply zeroes the tumbler:

```c
bool getaccount(typetask *taskptr, typeisa *accountptr)
{
  bool validaccount();
  tumblerclear(accountptr);
  return (TRUE);
```

The interactive-terminal version of the backend has account `0` (the zero tumbler). Only the FEBE backend (`be.c`) has the `1.1.0.1` default. There is no prompt, no file, no network query — `getaccount` was scaffolding that was commented out before shipping (`task.c:34-41`).

---

### 4. Child document addresses are allocated sequentially within the account's namespace

When `docreatenewdocument` is called (`do1.c:239`):

```c
makehint(ACCOUNT, DOCUMENT, 0, &taskptr->account, &hint);
return (createorglingranf(taskptr, granf, &hint, isaptr));
```

The call chain is:
- `createorglingranf` → `createorglgr` (`granf2.c:111-128`)
- `createorglgr` → `findisatoinsertgr` (`granf2.c:130-156`)
- `findisatoinsertgr` → `findisatoinsertnonmolecule` (`granf2.c:203-242`)

Inside `findisatoinsertnonmolecule`, because `supertype=ACCOUNT ≠ subtype=DOCUMENT`, the depth is 2 (`granf2.c:209`):

```c
depth = hintptr->supertype == hintptr->subtype ? 1 : 2;
```

And the algorithm (`granf2.c:235-241`):

```c
if (iszerotumbler(&lowerbound) || !lowerbound_under_hint) {
    /* Nothing under this hint - create first child as hintisa.0.1 */
    tumblerincrement(&hintptr->hintisa, depth, 1, isaptr);
} else {
    tumblertruncate(&lowerbound, hintlength + depth, isaptr);
    tumblerincrement(isaptr, tumblerlength(isaptr)==hintlength?depth:0, 1, isaptr);
}
```

So under account `1.1.0.1`:
- First document: `1.1.0.1.0.1` (hintisa incremented at depth 2 → two zeros appended then increment)
- Second document: `1.1.0.1.0.2`
- etc.

This is purely local sequential allocation within the enfilade tree. No coordination with any external authority occurs.

---

### 5. NODE-level address creation

The `docreatenode_or_account` function (`do1.c:243-258`) uses `makehint(NODE, NODE, ...)`, which gives `depth=1` (same supertype and subtype). The caller passes a hint ISA, and the function finds the next sequential address one level below that hint. But this is for creating *entries* in the enfilade representing node or account objects — it does not change the backend's own identity, which is still the hardcoded `1.1.0.1`.

The hierarchy from `xanadu.h:140-143` is:

```c
#define NODE     1
#define ACCOUNT  2
#define DOCUMENT 3
#define ATOM     4
```

`1.1.0.1` sits at the ACCOUNT level of the hierarchy. An enclosing NODE would be at a shorter address like `1.1`.

---

### Summary

| Mechanism | What it does |
|-----------|-------------|
| `be.c:37` — `tumbler defaultaccount = {...} /* 1.1.0.1 */` | Hardcodes the backend's own identity as a compile-time constant |
| `be.c:88` — `movetumbler(&defaultaccount, &task.account)` | Installs it into every request's task context |
| `rcfile.c` / `.backendrc` | Configures ports, filenames, alloc sizes only — no address fields |
| `task.c:31` — `tumblerclear(accountptr)` | The standalone `xumain` build gets account `0` instead |
| `granf2.c:203-242` — `findisatoinsertnonmolecule` | Allocates sequential child addresses under the account prefix |

**The answer is: self-assignment from a hardcoded convention.** The FEBE backend unconditionally claims address `1.1.0.1` every time it starts. There is no allocation authority, no bootstrap file, no discovery protocol. The reference implementation implicitly assumes a single-backend deployment where address conflict cannot arise.

---

## Question 13 [gregory]

> When udanax-green initializes via `entexit.c`, does it bind to exactly one node address, and if so, where is that node identity stored and how is it threaded through I-address allocation in `findisatoinsertmolecule`?

### Gregory's Answer

## KB Synthesis

## Node Binding at Initialization

The KB does not directly document `entexit.c` binding to a specific node address. What it does say is limited to one reference:

> `entexit.c:44-45` — initialization: `granf = createenf(GRAN); spanf = createenf(SPAN)` [SS-DUAL-ENFILADE, Finding 0012]

This is the entirety of what the KB records about `entexit.c`. Whether it also initializes a node identity global is not documented.

---

## What the KB Does Reveal About Node Structure

The address convention [SS-TUMBLER, Finding 0001] uses `.0.` as a field separator with the pattern `Node.0.User.0.Doc.0.Element`. All docuverse addresses in the KB use the `1.1.0.x` prefix, implying a single node `1.1`. Permascroll I-addresses use a different prefix (`2.1.0.x...`) [SS-ADDRESS-SPACE, Finding 0033], suggesting node `2` is the permascroll namespace.

Whether `1.1` is hardcoded in source, derived from the granfilade tree at startup, or set by an initialization routine outside `entexit.c` — the KB does not say.

---

## How Document Context Is Threaded Through `findisatoinsertmolecule`

The node identity is not passed as a separate parameter. It is embedded in the document ISA, which is carried through a hint structure:

1. The caller constructs `makehint(DOCUMENT, ATOM, TEXTATOM, docisaptr, &hint)`, which copies `docisaptr` into `hintptr->hintisa` [SS-ADDRESS-SPACE, Finding 0065]
2. `findisatoinsertmolecule` computes: `tumblerincrement(&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound)` — this sets the search boundary to `docISA.element_field.(atomtype+1)`, scoping the allocation to the document's content subspace [SS-ADDRESS-ALLOC, Finding 0065]
3. `findpreviousisagr` traverses the granfilade tree within `[docISA.element_field.0, upperbound)` to find the current maximum I-address, then increments by 1 [SS-ADDRESS-SPACE, Finding 0061]

The node prefix (`1.1` or `2.1`) is implicit in `docisaptr` — the allocation is scoped by document, not by node. Since all documents under a single node share the same node prefix, the node identity propagates automatically through the ISA hierarchy. There is no separate node argument to `findisatoinsertmolecule`.

---

**Summary:** The KB cannot answer whether `entexit.c` binds to a node address — it only shows enfilade creation there. Node identity is implicit in all tumbler addresses (hierarchical prefix) and threads through `findisatoinsertmolecule` via the document ISA hint, not as an explicit parameter.

---

## Code Exploration

Now I have everything needed for a complete answer. Here is the full analysis with all code citations:

---

## Initialization, Node Identity, and I-Address Allocation in udanax-green

### 1. What `entexit.c` Actually Does

The file named `entexit.c` contains a single function, `initmagicktricks()` [entexit.c:19-47]. Despite the filename, it performs **no node address binding**. Its sole job is to initialize the enfilade storage infrastructure:

```c
// entexit.c:19-47
int initmagicktricks(void)
{
    varcrums = TRUE;
    numbytesinloaf = NUMBYTESINLOAF;
    ...
    initgrimreaper();
    initqueues();
    clear(&ZEROTUMBLERvar, sizeof(tumbler));
    if (initenffile()) {
        initkluge((typecuc**)&granf, (typecuc**)&spanf);  // load from disk
    } else {
        granf = (typegranf) createenf(GRAN);               // fresh enfilades
        spanf = (typespanf) createenf(SPAN);
    }
}
```

`initkluge()` is defined in `corediskin.c:18-41`. It reads the granfilade and spanfilade roots from fixed disk locations (`GRANFDISKLOCATION`, `SPANFDISKLOCATION`) into the global pointers `granf` and `spanf`. No tumbler is assigned here.

---

### 2. The Single Node Address and Where It Lives

The node identity is bound **one step later**, in `be.c`, which is the backend binary actually compiled and used by the test harness. After `initmagicktricks()` returns, this single line executes:

```c
// be.c:88
movetumbler(&defaultaccount, &task.account);
```

Where `defaultaccount` is defined at [be.c:37]:

```c
tumbler defaultaccount = {0,0,0,0, 1,1,0,1,0,0,0,0}; /* 1.1.0.1 */
```

This is a tumbler with `exp=0, sign=0, mantissa=[1,1,0,1,0,0,...]` — the address **1.1.0.1**. This is the only node address ever set at startup.

**Storage location:** The account tumbler lives in `typetask.account` [common.h:102]:

```c
typedef struct structtask {
    FILE *inp, *outp, *errp;
    typetthingheader *tempspacehead;
    typetthingheader *tempspacetail;
    tumbler account;     /* ← the node identity */
    bool charinbuff;
    char charbuff;
} typetask;
```

`be.c` has a single global `typetask task` [be.c:41] and a matching global pointer `typetask *taskptrx` [be.c:36]. `isthisusersdocument()` [be.c:171-176] reads from `taskptrx->account` to enforce ownership:

```c
int isthisusersdocument(tumbler *tp)
{
    bool result = tumbleraccounteq(tp, &taskptrx->account);
    return result;
}
```

`tumbleraccounteq()` [tumble.c:38-70] checks whether `tp`'s mantissa prefix matches the account tumbler's non-zero digits — it treats two consecutive zeros as the account terminator, allowing document addresses like `1.1.0.1.0.1` to match account `1.1.0.1`.

Note: `socketbe.c:35` declares a different `defaultaccount = {0,0,0,0, 1,1,0,14,0}` (representing `1.1.0.14`) but it is **never assigned to any task or player** in the socket path — it is dead code in that file.

In `xumain.c` (the standalone binary), `getaccount()` [task.c:28-41] simply clears the account to zero:

```c
bool getaccount(typetask *taskptr, typeisa *accountptr)
{
    tumblerclear(accountptr);
    return (TRUE);
}
```

The commented-out code below [task.c:35-40] shows the original intent to read the account from user input, but it was disabled. The test harness uses `be.c`, not `xumain.c`.

---

### 3. How the Node Address Threads Through I-Address Allocation

The account tumbler `1.1.0.1` is the root of the I-address hierarchy. It propagates as follows:

#### Step 1 — Document creation (`docreatenewdocument`, do1.c:234)

```c
bool docreatenewdocument(typetask *taskptr, typeisa *isaptr)
{
    typehint hint;
    makehint(ACCOUNT, DOCUMENT, 0, &taskptr->account, &hint);
    return (createorglingranf(taskptr, granf, &hint, isaptr));
}
```

`makehint()` [do2.c:78-84] copies `taskptr->account` into `hint.hintisa`, with `supertype=ACCOUNT`, `subtype=DOCUMENT`. This hint then travels:

```
createorglingranf → createorglgr [granf2.c:111] → findisatoinsertgr [granf2.c:130]
```

#### Step 2 — Routing at `findisatoinsertgr` [granf2.c:130-156]

```c
bool findisatoinsertgr(typecuc *fullcrumptr, typehint *hintptr, typeisa *isaptr)
{
    if (hintptr->subtype == ATOM) {
        findisatoinsertmolecule(fullcrumptr, hintptr, isaptr);
    } else {
        findisatoinsertnonmolecule(fullcrumptr, hintptr, isaptr);
    }
    tumblerjustify(isaptr);
    return (TRUE);
}
```

For **document creation** (`subtype=DOCUMENT ≠ ATOM`), `findisatoinsertnonmolecule` is called, **not** `findisatoinsertmolecule`. With `hintisa=1.1.0.1` and `depth=2` (supertype≠subtype), it allocates the first document as `1.1.0.1.0.1`.

#### Step 3 — When `findisatoinsertmolecule` is actually called

`findisatoinsertmolecule` [granf2.c:158-181] is called only for **ATOM subtypes** — text content (`TEXTATOM=1`) and link content (`LINKATOM=2`). The call chains are:

**Text insertion** (`doinsert`, do1.c:87):
```c
makehint(DOCUMENT, ATOM, TEXTATOM, docisaptr, &hint);  // hintisa = docisa (e.g. 1.1.0.1.0.1)
inserttextingranf → inserttextgr → findisatoinsertgr → findisatoinsertmolecule
```

**Link creation** (`docreatelink`, do1.c:195):
```c
makehint(DOCUMENT, ATOM, LINKATOM, docisaptr, &hint);  // hintisa = docisa
createorglingranf → createorglgr → findisatoinsertgr → findisatoinsertmolecule
```

At this point, `hintisa` is the **document address** (e.g. `1.1.0.1.0.1`) — the account prefix `1.1.0.1` is already embedded in it. `findisatoinsertmolecule` does not see the raw account tumbler; it only uses the document ISA as its base.

#### Step 4 — Inside `findisatoinsertmolecule` [granf2.c:158-181]

```c
static int findisatoinsertmolecule(typecuc *fullcrumptr, typehint *hintptr, typeisa *isaptr)
{
    typeisa upperbound, lowerbound;

    tumblerincrement(&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound);
    clear(&lowerbound, sizeof(lowerbound));
    findpreviousisagr((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);
    if (tumblerlength(&hintptr->hintisa) == tumblerlength(&lowerbound)) {
        tumblerincrement(&lowerbound, 2, hintptr->atomtype, isaptr);
        tumblerincrement(isaptr, 1, 1, isaptr);
    } else if (hintptr->atomtype == TEXTATOM) {
        tumblerincrement(&lowerbound, 0, 1, isaptr);
    } else if (hintptr->atomtype == LINKATOM) {
        tumblerincrement(&hintptr->hintisa, 2, 2, isaptr);
        if (tumblercmp(&lowerbound, isaptr) == LESS)
            tumblerincrement(isaptr, 1, 1, isaptr);
        else
            tumblerincrement(&lowerbound, 0, 1, isaptr);
    }
}
```

With `hintisa = docisa` (e.g. `1.1.0.1.0.1`):

- **TEXTATOM:** `upperbound = docisa + {2}` (i.e., `docisa.0.2`). Searches backward for the previous ISA under that bound. The new text address is placed after whatever was found.
- **LINKATOM:** `upperbound = docisa + {3}` (i.e., `docisa.0.3`). The first link address is `docisa.0.2`, then incremented past any existing links.

The account/node prefix `1.1.0.1` is baked into `docisa` and flows through the arithmetic invisibly.

---

### 4. The Complete Address Hierarchy

The single node address `1.1.0.1` set at [be.c:88] anchors the entire I-address tree:

| Level | Address | Allocated by |
|-------|---------|-------------|
| Node | `1` | Hardcoded in `defaultaccount` |
| Account | `1.1` | Hardcoded in `defaultaccount` |
| Sub-node | `1.1.0` | Hardcoded in `defaultaccount` |
| Account ISA | **`1.1.0.1`** | `defaultaccount` → `task.account` [be.c:88] |
| First document | `1.1.0.1.0.1` | `findisatoinsertnonmolecule` via `docreatenewdocument` |
| Text in doc | `1.1.0.1.0.1.0.N` | `findisatoinsertmolecule` (TEXTATOM) |
| Links in doc | `1.1.0.1.0.1.0.2`, `.0.3`, … | `findisatoinsertmolecule` (LINKATOM) |

### Summary

1. **`entexit.c` / `initmagicktricks()`** does **not** bind any node address. It only initializes enfilade disk infrastructure.

2. The single node address **`1.1.0.1`** is bound at [be.c:88] via `movetumbler(&defaultaccount, &task.account)`, immediately after `initmagicktricks()` returns.

3. The node identity lives in **`typetask.account`** [common.h:102], with the live global pointer at `taskptrx` [be.c:36].

4. `findisatoinsertmolecule` [granf2.c:158-181] is **only called for ATOM subtypes** (text and links). It never receives the raw account tumbler; by the time it is called, the account prefix is already embedded in the document's ISA via the `hint.hintisa` field. The account's `1.1.0.1` flows through: `task.account` → `hint.hintisa` (via `makehint` in `do1.c:117` or `207`) → document address → `hintisa` argument to `findisatoinsertmolecule` — where it appears as the prefix of the document address from which atom sub-addresses are derived.

---

## Question 14 [gregory]

> Is the node set fixed at system genesis, or can new nodes enter the docuverse after initial startup — and if so, what mechanism registers them and ensures their tumbler prefix doesn't collide with existing nodes?

### Gregory's Answer

## KB Synthesis

The KB does not describe a mechanism for adding new top-level nodes after system genesis, nor does it document any inter-server federation or registration protocol. Here is what the KB does and doesn't say:

---

## What the KB says about node structure

Tumbler addresses encode a strict containment hierarchy [SS-ADDRESS-SPACE, Finding 0021]:

```
Node:    1.1
Account: 1.1.0.2   (Node.0.Account — depth=2 crossing)
Document: 1.1.0.2.0.1
```

The `makehint` dispatch table includes a `NODE → NODE` case with `depth=1` (no `.0.` boundary), meaning nodes can be allocated as children of existing nodes. This is the same stateless query-and-increment mechanism used for all address allocation [SS-ADDRESS-ALLOC, Finding 0021]: find the highest existing address under the parent via `findpreviousisagr`, then increment.

## Collision prevention within the system

Within the single deployed system, collisions are structurally impossible because:

1. **Single granfilade** — all persistent state lives in one `enf.enf` file [SS-UNIFIED-STORAGE, Finding 0059]. There is one global allocator.
2. **Monotonic allocation** — `findisatoinsertmolecule` / `findisatoinsertnonmolecule` always allocate strictly above the current maximum [INV-MONOTONIC, Findings 0033, 0061]. No address is ever reused [INV-NO-IADDR-REUSE].
3. **Containment check** — allocation under a parent verifies the candidate address is actually under that parent before accepting it [PRE-ADDRESS-ALLOC, Finding 0021]. This is the fix for Bug 0013, which caused cross-account allocation pollution.
4. **Sequential dispatch** — the event loop is single-threaded with run-to-completion semantics [INV-SEQUENTIAL-DISPATCH, INV-ATOMICITY, Finding 0042], so no concurrent allocation races are possible.

## What the KB cannot answer

The KB has no evidence of:

- A node registration or bootstrapping protocol that admits new top-level nodes (`1.1`, `1.2`, …) from outside the existing deployment
- Inter-server communication, federation, or docuverse-wide coordination
- A global node registry distinct from the local granfilade

The system as documented is a single-server daemon. The `1.x` address prefix where `1` is the root appears fixed at deployment time. The only node-addition mechanism in the KB is the local `NODE → NODE` allocation, which adds subnodes under an existing node within the same granfilade — it is not a mechanism for incorporating a new independent server.

**Bottom line:** Within udanax-green as documented, the node set is effectively fixed at system genesis. The collision prevention is total within the single granfilade by monotonic allocation plus containment checking. How a new peer node would enter a multi-server docuverse — the Nelson-vision scenario — is not answered by this implementation.

---

## Code Exploration

I now have everything needed. Here is the full answer.

---

## Are Nodes Fixed at Genesis?

**No.** The node set is not sealed at startup. New nodes can enter the docuverse at any time through a live FEBE request. There is no genesis block or pre-assigned node table baked into initialization.

---

## What Happens at Startup

`bed.c:92` calls `init(1)`, which at `init.c:42-65` does nothing but fill the `requestfns[]` dispatch table:

```c
for (i = 0; i < NREQUESTS; ++i)
    requestfns[i] = nullfun;
/* ... */
requestfns[CREATENODE_OR_ACCOUNT] = createnode_or_account;   /* init.c:65 */
```

No node objects are created. The persistent enfilade tree is loaded from disk by `initmagicktricks()` (`bed.c:95`). After that the daemon sits in its `select()` loop waiting for frontend connections (`bed.c:103-148`). The granfilade on disk is the only authoritative record of which nodes exist.

`bert.c` is not a node registry — it is a per-connection document open/close lock table (`bert.c:13-29`). It knows nothing about node addresses.

---

## The Registration Mechanism

A client registers a new node by sending FEBE request 38 (`requests.h:45: #define CREATENODE_OR_ACCOUNT 38`) with one argument: a tumbler that serves as the desired parent (hint) address.

**Layer 1 — wire decode** (`get1.c:208-212`):
```c
int getcreatenode_or_account(typetask *taskptr, tumbler *tp) {
    gettumbler(taskptr, tp);
    return(TRUE);
}
```
The client supplies exactly one tumbler — its desired namespace prefix.

**Layer 2 — FEBE handler** (`fns.c:375-386`):
```c
void createnode_or_account(typetask *taskptr) {
    tumbler t;
    if (getcreatenode_or_account(taskptr, &t)
     && docreatenode_or_account(taskptr, &t))
        putcreatenode_or_account(taskptr, &t);
    else
        putrequestfailed(taskptr);
}
```

**Layer 3 — implementation** (`do1.c:243-258`):
```c
bool docreatenode_or_account(typetask *taskptr, typeisa *isaptr) {
    typeisa isa;
    typehint hint;
    tumblercopy(isaptr, &isa);
    makehint(NODE, NODE, 0, &isa, &hint);           /* do1.c:251 */
    result = createorglingranf(taskptr, granf, &hint, &isa);  /* do1.c:252 */
    if (result) tumblercopy(&isa, isaptr);
    return result;
}
```

`makehint(NODE, NODE, 0, ...)` (`do2.c:78-84`) sets `supertype=NODE(1)`, `subtype=NODE(1)`, `atomtype=0`, with the client-supplied tumbler as `hintisa`. This is a self-referential node hint — it says "allocate a NODE-level object in the NODE namespace rooted at this address."

**Layer 4 — granfilade allocation chain**:

`createorglingranf()` (`granf1.c:50-55`) is a thin wrapper:
```c
bool createorglingranf(typetask *taskptr, typegranf granfptr,
                       typehint *hintptr, typeisa *isaptr) {
    return createorglgr(taskptr, granfptr, hintptr, isaptr);
}
```

`createorglgr()` (`granf2.c:111-128`):
1. Calls `findisatoinsertgr()` to compute the new node's address
2. Calls `createenf(POOM)` to allocate a fresh POOM enfilade for the node's content
3. Calls `insertseq()` to register the node in the granfilade tree

---

## How Tumbler Addresses Are Generated (Collision Prevention)

`findisatoinsertgr()` (`granf2.c:130-156`) dispatches to `findisatoinsertnonmolecule()` for NODE/ACCOUNT/DOCUMENT types.

`findisatoinsertnonmolecule()` (`granf2.c:203-242`):

```c
depth = hintptr->supertype == hintptr->subtype ? 1 : 2;  /* granf2.c:209 */
```

For NODE→NODE, `depth = 1`. For ACCOUNT→DOCUMENT, `depth = 2`.

```c
tumblerincrement(&hintptr->hintisa, depth-1, 1, &upperbound);  /* granf2.c:213 */
clear(&lowerbound, sizeof(lowerbound));
findpreviousisagr((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);  /* granf2.c:217 */
```

`findpreviousisagr()` (`granf2.c:255-278`) recursively walks the enfilade tree to find the highest-addressed existing object with an address strictly less than `upperbound`. This is a tree walk — the entire history of allocated addresses is encoded in the enfilade's node structure.

Then two guard conditions (added as Bug Fix #2 in the comment at `granf2.c:224-227`):

```c
if (!iszerotumbler(&lowerbound)) {
    tumblertruncate(&lowerbound, hintlength, &truncated);
    lowerbound_under_hint = tumblereq(&truncated, &hintptr->hintisa);  /* granf2.c:232 */
}
```

This verifies the found neighbor actually shares the same hint prefix. Without this check, an existing node at `1.2.0.1` would pollute allocation under a hint at `1.3` — exactly the cross-account collision scenario.

Finally, the address is assigned:

```c
if (iszerotumbler(&lowerbound) || !lowerbound_under_hint) {
    tumblerincrement(&hintptr->hintisa, depth, 1, isaptr);   /* granf2.c:237 — first child */
} else {
    tumblertruncate(&lowerbound, hintlength + depth, isaptr);
    tumblerincrement(isaptr, tumblerlength(isaptr)==hintlength ? depth : 0, 1, isaptr); /* granf2.c:240 */
}
```

- **No prior nodes under this hint:** address = `hintisa` with `depth` extra components, last one = 1. E.g., for hint `1.0`, node gets `1.0.1`.
- **Prior nodes exist:** truncate the predecessor to `hintlength + depth` components, then increment. Each subsequent node gets the next sequential address in the namespace.

The new address is then planted into the granfilade by `insertseq()` (`granf2.c:125`), making it part of the persistent sorted tree that all future `findpreviousisagr()` walks will see.

---

## Summary

| Question | Answer | Citation |
|----------|--------|----------|
| Fixed at genesis? | No — open, on-demand creation | `init.c:42-65` (no node creation at startup) |
| Registration entry point | FEBE request 38: `CREATENODE_OR_ACCOUNT` | `requests.h:45`, `init.c:65` |
| Wire protocol | Client sends one tumbler (hint prefix) | `get1.c:208-212` |
| Hint type used | `makehint(NODE, NODE, 0, hint_tumbler)` | `do1.c:251` |
| Address computation | `findisatoinsertnonmolecule()` with `depth=1` | `granf2.c:203-242` |
| Collision avoidance | Tree walk finds highest prior address; prefix check ensures it's in the same namespace; then sequential increment | `granf2.c:217, 229-232, 237-240` |
| Persistence | `insertseq()` writes into the granfilade; survives across restarts | `granf2.c:125` |
| Offline allocation | Not supported — server is authoritative; no merge protocol exists | (absence of any such mechanism) |

The collision guarantee is entirely structural: the granfilade tree is the authoritative record of all allocated addresses, `findpreviousisagr()` reads it on every allocation, and `tumblerincrement()` always produces a strictly larger address. As long as all allocations go through the live server, uniqueness is guaranteed by construction. There is no separate node-ID registry, no genesis list, and no offline pre-allocation protocol.

---

## Question 15 [gregory]

> Can a single backend process serve multiple node addresses simultaneously, or is there a strict one-process-per-node invariant enforced somewhere in the event loop (`bed.c`)?

### Gregory's Answer

## KB Synthesis

The KB does not document a one-process-per-node invariant, and the architecture described implies a single process serves arbitrary node addresses.

**What the KB says about the event loop**

[SS-SESSION-STATE] (Finding 0022) establishes that `bed.c` manages up to `MAX_PLAYERS = 25` concurrent connections via a `player[]` array and `select()`. Each session has its own **per-session account context** (`wheretoputit`), but all sessions share the same global enfilades. Nothing in the session model constrains which part of the address hierarchy a session can operate in.

[INV-SEQUENTIAL-DISPATCH] (Finding 0042) confirms that `bed.c:118-128` iterates over all ready file descriptors sequentially with no filtering by node:

> The event loop processes each FEBE operation atomically via run-to-completion scheduling...any serialization order produces correct results.

[FC-SESSION-ACCOUNT-ISOLATION] confirms that `account(1.1.0.1)` in session A and `account(1.1.0.2)` in session B are independent — two sessions operating under distinct accounts (and thus distinct node subtrees) coexist in the same process without interference.

[INV-GLOBAL-ADDRESS-UNIQUENESS] (Finding 0022) explicitly validates this: multiple sessions on the same account produce distinct sequential document addresses, and by implication, multiple sessions on different accounts (different nodes) also coexist correctly under one daemon.

**What the KB does not say**

There is no finding documenting a constraint of the form `bed.c` binds to one node address, rejects connections from other node subtrees, or enforces a node-scoped connection check. The address hierarchy ([SS-ADDRESS-SPACE], [SS-TUMBLER-CONTAINMENT]) is a purely logical naming convention over a flat granfilade — it carries no process-affinity semantics.

**Conclusion**

A single backend process serves multiple node addresses simultaneously. The `bed.c` event loop is address-agnostic: it dispatches operations from all sessions regardless of their current account, and the account context is a per-session variable that sessions set independently. No node-per-process invariant exists in the implementation or is implied by any KB entry.

---

## Code Exploration

---

## Answer: A Single Process Explicitly Serves Multiple Node Addresses

The architecture is **not** one-process-per-node. A single backend process is designed to serve multiple simultaneous frontend connections — each potentially with a different account/node address.

---

### 1. The Comment Says It All

`bed.c:10`:
```c
/*
    bed.d	- multi-user backend main
*/
```

This is a multi-user backend from the start. No ambiguity in intent.

---

### 2. `select()`-Based Multiplexing Over All Active Connections

`bed.c:103-142` runs the main event loop:

```c
for (;;) {
    if (n_players < 1) {
        diskflush();
        new_players(player, &n_players, TRUE, &task);  /* wait for fe */
    }
    inputfds2 = inputfds;
    if (select(nfds+1, &inputfds2, 0, 0, &timeout) < 0) { ... }
    else {
        for (i = 0; i <= nfds; i++) {
            if ((1<<i) & inputfds2) {
                user = fdtoplayer[i];             /* bed.c:120 */
                task.inp = player[user].inp;
                task.outp = player[user].outp;
                task.account = player[user].account;  /* bed.c:123 */
                ...
                xanadu(&task);
            }
        }
    }
    leave(player, &n_players);
    new_players(player, &n_players, FALSE, &task);
}
```

`select()` polls **all** connected frontend file descriptors simultaneously. For every ready FD in a single loop iteration, `user = fdtoplayer[i]` switches context and dispatches `xanadu()`. Multiple connections are tracked and served within one process.

---

### 3. The Player Array: Each Entry Has Its Own Account Tumbler

`players.h:13-21`:
```c
typedef struct _player {
    char    *name;
    INT     userid;
    INT     wantsout;
    INT     socket;
    FILE    *inp;
    FILE    *outp;
    tumbler account;    /* xanadu host and account tumbler */
} PLAYER;
```

`socketbe.c:37-38`:
```c
#define MAX_PLAYERS     25
PLAYER player[MAX_PLAYERS];
```

Each connected player carries its own `account` tumbler — its Xanadu node+account address. Up to **25 concurrent connections** are supported before the backend starts refusing (`socketbe.c:85-88`):

```c
if ( *n_playersp >= MAX_PLAYERS ) {
    fprintf(stderr,"TOOMANY frontends: won't log another one\n");
    close(s);
}
```

---

### 4. FD-to-Player Mapping

`socketbe.c:34`:
```c
INT fdtoplayer[32];
```

When `new_players()` accepts a new connection (`socketbe.c:118-121`):

```c
fdtoplayer[s] = *n_playersp;
inputfds |= (1<<s);
nfds = max(s, nfds);
(*n_playersp)++;
```

Each accepted socket FD maps to a player slot. The `inputfds` bitmask accumulates all active FDs. The `select()` bitmask is an `INT` (32-bit), imposing a hard ceiling of **32 file descriptors** regardless of `MAX_PLAYERS`.

---

### 5. Per-Connection Document Access Control in `bert.c`

There is no global "current node" state. The bert (open-document) table is scoped by **connection index**:

`bert.c:52`:
```c
int checkforopen(tumbler *tp, int type, int connection)
```

`bert.c:128`:
```c
int addtoopen(tumbler *tp, int connection, int created, int type)
```

`bert.c:63-79` walks the `berttable[]` hash chain and compares `bert->connection == connection` for every open-state check. Connection 0 and connection 3 have completely independent open sets on the same document. In `fns.c:396`:

```c
doopen(taskptr, &t, &newt, type, mode, user)
```

`user` — the global connection index set in `bed.c:120` — is passed as `connection` throughout.

`isthisusersdocument()` in `socketbe.c:197-201` compares the requested document's account against the *current player's* account tumbler:

```c
int isthisusersdocument(tumbler *tp) {
    return tumbleraccounteq(tp, &(player[user].account));
}
```

This means ownership checks are per-connection, not global. Two players with different account tumblers (different node addresses) are independently authorized.

---

### 6. Account (Node) Setup Is Per-Connection

`fns.c:364-373` — the `XACCOUNT` request (request code 34) sets the node address for a specific connected player:

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

This writes the incoming account tumbler directly into `player[user].account`, where `user` is the current connection index. Each connection independently negotiates its own node identity.

---

### 7. Serialization: Multi-Connection, But Single-Threaded

The global `int user` at `bed.c:28`:

```c
int user = 0;		/* Global current user ID */
```

is set before each `xanadu()` call (`bed.c:120`) and used by all downstream code to index `player[]`. This means requests are **serialized** — only one request is in flight at a time — but connections are **multiplexed**: the `select()` loop cycles through all ready FDs in a single pass. There is no I/O blocking on one connection while another waits.

---

### Summary Table

| Constraint | Value | Source |
|---|---|---|
| Max simultaneous connections | 25 | `socketbe.c:28` `MAX_PLAYERS` |
| FD bitmask ceiling | 32 | `socketbe.c:34` `fdtoplayer[32]`, `INT` select mask |
| Per-connection state | `player[user].account`, bert connection index | `players.h:20`, `bert.c:66` |
| Request execution | Serialized (single-threaded, cooperative) | `bed.c:120-128` global `user` |
| One-process-per-node invariant | **None** | — |

**Conclusion:** A single backend process can and does serve multiple node addresses simultaneously, up to a hard limit of 25 connections (or 32 FD slots, whichever binds first). Each connection independently negotiates its account/node tumbler via `XACCOUNT`. The bert access-control layer scopes all document-open state by connection index. There is no architectural enforcement of one-process-per-node anywhere in `bed.c`, `socketbe.c`, or `bert.c`.

---

## Question 16 [gregory]

> What invariant prevents two different nodes from allocating the same I-address — is it the tumbler prefix partitioning alone, or is there an additional coordination mechanism beyond address-space separation?

### Gregory's Answer

## KB Synthesis

The invariant preventing duplicate I-address allocation is **single-threaded sequential dispatch** — not tumbler prefix partitioning.

## The Allocation Mechanism

The I-address allocator is stateless query-and-increment [SS-ADDRESS-SPACE, Finding 0061]:

1. Call `findpreviousisagr` to find the highest existing I-address below a computed upper bound
2. Increment that address by 1 via `tumblerincrement`

There is no cached "next available" counter, no reserved range, no atomic reservation. The allocation result is a pure function of the current granfilade tree state: `next_iaddr(granf) = max_iaddr(granf) + 1`.

Critically, [SS-ADDRESS-SPACE] (Finding 0061) notes: "any session querying the same granfilade tree will allocate identically." Two concurrent allocators would both find the same maximum and produce the same address. Tumbler prefix partitioning does not prevent this — it merely separates text addresses from document addresses from link orgl addresses by search bounds, but within each partition the query-and-increment is still vulnerable to races.

## The Actual Coordination Mechanism

The uniqueness guarantee comes from [INV-SEQUENTIAL-DISPATCH] and [INV-ATOMICITY] (Finding 0042):

- The `bed.c` event loop processes each FEBE operation to completion before starting the next
- Multi-step operations (allocate I-address, insert into granfilade, update POOM, update spanfilade) execute as a single uninterruptible unit
- No threads, no preemptive scheduling, no signal handlers modify state mid-operation
- Even when multiple frontends have ready file descriptors, the loop iterates sequentially: frontend i's INSERT runs entirely before frontend i+1's

This is why [PRE-CONCURRENT-INSERT] states that concurrent unsynchronized insertion is unsafe — the query-and-increment is NOT atomic at the machine level. The invariant holds only because the event loop eliminates concurrency entirely.

## The Role of Prefix Partitioning

Tumbler prefix partitioning ([SS-ADDRESS-ALLOC], [SS-ADDRESS-SPACE] Finding 0065, 0077) provides a secondary structural property: text allocation searches within a document-scoped range, link orgl allocation searches within a different document-scoped range, version document allocation searches within a parent-scoped range. This means allocations for different (document, entity-type) pairs cannot collide even theoretically, since their upper-bound searches cover disjoint tumbler ranges.

But this is a necessary complement, not the primary mechanism. Within any single (document, entity-type) partition, sequential dispatch is what prevents two allocations from claiming the same address. The prefix partitioning just ensures the searches are bounded correctly so that Bug 0013 ([PRE-ADDRESS-ALLOC]) — where a search crossed account boundaries — cannot produce addresses in the wrong hierarchy.

## Summary

| Mechanism | Prevents |
|-----------|----------|
| Single-threaded event loop ([INV-SEQUENTIAL-DISPATCH]) | Two allocations interleaving on the same granfilade query |
| Tumbler prefix partitioning ([SS-ADDRESS-ALLOC]) | Cross-entity-type and cross-document address collisions |

The uniqueness invariant formally: `∀ alloc_a, alloc_b : time(a) < time(b) ⟹ iaddr(b) > iaddr(a)` [INV-MONOTONIC] — which holds because no two allocations can observe the same "current maximum" given run-to-completion dispatch.

---

## Code Exploration

Here is the full answer, traced directly from the source.

---

## What Prevents Two Nodes from Allocating the Same I-Address?

**The short answer:** Tumbler prefix partitioning is the structural guarantee, but it is not alone. A second layer — the **single-process, shared-granfilade architecture** — serializes all allocations and eliminates the possibility of concurrent collision. BERT (`bert.c`) is a third mechanism but for document *access* enforcement, not address uniqueness.

---

### Layer 1: Tumbler Prefix Partitioning (Structural Invariant)

Every allocation begins with a `typehint`, built by `makehint()` in `backend/do2.c:78–84`:

```c
int makehint(INT typeabove, INT typebelow, INT typeofatom, typeisa *isaptr, typehint *hintptr)
{
    hintptr->supertype = typeabove;
    hintptr->subtype = typebelow;
    hintptr->atomtype = typeofatom;
    movetumbler (isaptr, &hintptr->hintisa);   // stores caller's account/doc ISA as prefix
}
```

The `hintisa` field is the **caller's own account tumbler** — different for every account by construction. Call sites:

- `backend/do1.c:239` — new document: `makehint(ACCOUNT, DOCUMENT, 0, &taskptr->account, &hint)` — prefix is the *current user's account tumbler*
- `backend/do1.c:117` — insert text: `makehint(DOCUMENT, ATOM, TEXTATOM, docisaptr, &hint)` — prefix is the document
- `backend/do1.c:180,207` — create link: `makehint(DOCUMENT, ATOM, LINKATOM, docisaptr, &hint)`

In `findisatoinsertnonmolecule()` (`backend/granf2.c:203–242`), the allocator:

1. Computes an upper-bound address: `tumblerincrement(&hintptr->hintisa, depth-1, 1, &upperbound)` [line 213]
2. Calls `findpreviousisagr()` to find the highest already-allocated address below that bound [line 217]
3. **Explicitly checks that the found address is under the hint prefix** [lines 228–233]:

```c
lowerbound_under_hint = FALSE;
if (!iszerotumbler(&lowerbound)) {
    tumblertruncate(&lowerbound, hintlength, &truncated);
    lowerbound_under_hint = tumblereq(&truncated, &hintptr->hintisa);
}
```

4. If nothing is under this hint (or the found address belongs to a different account), allocates the first child: `tumblerincrement(&hintptr->hintisa, depth, 1, isaptr)` [line 237]. Otherwise, increments the maximum [lines 239–241].

The prefix check at lines 228–233 is the **explicit guard** that stops addresses from "leaking" across account boundaries even when the global tree contains entries from many accounts. Two accounts with prefixes `1.1.0` and `1.2.0` produce non-overlapping children (`1.1.0.0.1`, `1.2.0.0.1`, …) because `tumblertruncate` + `tumblereq` will always reject a lowerbound that shares only a common ancestor, not the exact hint prefix.

---

### Layer 2: Single-Process Shared Granfilade (Coordination Mechanism)

There is **no explicit mutex, semaphore, atomic CAS, or distributed lock** in any of the allocation code. This is not an oversight — the architecture makes them unnecessary.

`backend/granf1.c:10` declares:

```c
int backenddaemon = 0;
```

The backend is a **single process** serving all connections through `socketbe.c`. All connections (all "players") share the same in-memory granfilade tree (`granf`). The granfilade tree is the **implicit registry of all allocated I-addresses** — there is no separate "used address" bitmap or table. `findpreviousisagr()` (`granf2.c:255–278`) walks the tree recursively to discover what has been allocated.

Because all allocation calls go through the same process, in the same address space, against the same tree, they are **sequentially serialized by the C call stack and event loop** (`bed.c`/`socketbe.c`). Concurrent allocation from two connections cannot happen because the process handles one operation at a time.

This means:
- **Within one process instance**: serialization is implicit. No mutex needed.
- **Across distributed nodes** (hypothetical multi-node deployment): there is no inter-node coordination visible in the code. The design assumption appears to be a single backend daemon per installation.

---

### Layer 3: BERT — Access Enforcement, Not Address Uniqueness

`bert.c` implements document open/lock tracking (`checkforopen`, `addtoopen`, `removefromopen`). The `berttable` is a hash map from tumbler → open state, checked in `findorgl()` at `granf1.c:22`:

```c
if ((temp = checkforopen(isaptr, type, user)) <= 0) {
    // reject access if not sufficiently open
}
```

This prevents *concurrent writes* to the same document, but it operates **after** an address has already been assigned. It does not prevent two addresses from being allocated identically — it enforces who may *use* an already-created address.

`isthisusersdocument()` (`socketbe.c:197–201`) similarly uses `tumbleraccounteq()` to compare a document's prefix against the current connection's account tumbler. This is ownership *enforcement*, not address *generation*.

---

### What `tumbleraccounteq` Guarantees

`tumble.c:38–70` defines the account-equality test: it iterates mantissa positions and stops at the second zero of the account (account address terminator), checking that the document prefix matches exactly up to that point. This function is used in `checkforopen` (`bert.c:81`) and `docreatenewversion` (`do1.c:270`) to verify ownership — confirming that a document lives inside an account's prefix — but it is not called during address *allocation*.

---

### Summary

| Layer | Mechanism | Location | Role |
|---|---|---|---|
| 1 | `hintisa` prefix partitioning | `do2.c:78`, `granf2.c:231–233` | Structurally bounds each account's address subspace; prefix-check guard rejects cross-account addresses |
| 2 | Single-process granfilade | `granf1.c:10`, `socketbe.c` | Serializes all allocations; the enfilade tree itself is the implicit allocation registry |
| 3 | BERT open table | `bert.c:52–86` | Enforces document access, prevents concurrent writes; does **not** guarantee address uniqueness |

**Tumbler prefix partitioning alone would be sufficient in a correctly partitioned multi-node system**, but udanax-green as implemented adds the stronger guarantee that all allocations happen serially inside a single process against a shared tree. The `findpreviousisagr` + prefix-truncation check (`granf2.c:217, 229–233`) is the explicit code that enforces the invariant: no matter what the tree contains, only addresses under the caller's hint prefix are considered when computing the next address to assign.

---

## Question 17 [gregory]

> Does a node have any mutable state of its own (e.g., a node-level counter, capability list, or configuration record), or is a node purely an address prefix whose existence is implied by the presence of accounts and documents beneath it?

### Gregory's Answer

## KB Synthesis

Not fully answerable from the KB.

The KB provides partial evidence but no definitive answer about whether nodes carry their own mutable state.

**What the KB does say:**

Nodes appear in the address hierarchy as the outermost prefix component. [SS-TUMBLER, Finding 0001] describes the docuverse address convention as `Node.0.User.0.Doc.0.Element` — e.g., `1.1` is a node, `1.1.0.2` is an account under that node, `1.1.0.2.0.1` is a document under that account.

[SS-ADDRESS-SPACE, Finding 0021] shows that the `makehint` dispatch table includes a `NODE | NODE | depth=1` case, meaning node-under-node allocation uses the same `findisatoinsertnonmolecule` mechanism as version-under-document and document-under-account allocation. This implies node addresses are allocated and tracked in the granfilade hierarchy just as document addresses are.

**What the KB does not say:**

The KB never describes a node orgl with its own POOM, content enfilade, link subspace, or any mutable state. `createorglingranf` is described as "used for documents and links" [SS-GRANF-OPERATIONS], with no mention of node orgls. No finding examines what, if anything, resides at a bare node address — whether it is a full orgl entry or simply a numeric prefix implied by the child addresses beneath it.

**Bottom line:** The KB establishes that nodes exist as address-space entities whose child-address allocation is tracked in the granfilade, but does not reveal whether they have their own orgl records with independent mutable state, or whether they are purely implicit address prefixes whose "existence" is inferred from the presence of accounts and documents beneath them. That question is not answerable from the KB as it stands.

---

## Code Exploration

I now have everything needed to give a definitive, source-grounded answer.

---

## Does a node have mutable state of its own?

**Short answer: No. A node is purely an address prefix. It carries no mutable state — no counter, no capability list, no configuration record — beyond a tumbler and an (empty) POOM enfilade allocated in the granfilade.**

---

### What the code actually shows

#### 1. Node creation allocates a tumbler and an empty POOM

`docreatenode_or_account` [do1.c:243–258]:

```c
bool docreatenode_or_account(typetask *taskptr, typeisa *isaptr) {
  typeisa isa;
  typehint hint;
  tumblercopy(isaptr, &isa);
  makehint(NODE, NODE, 0, &isa, &hint);           // hint: supertype=NODE, subtype=NODE
  result = createorglingranf(taskptr, granf, &hint, &isa);
  if (result) tumblercopy(&isa, isaptr);
  return result;
}
```

`createorglingranf` → `createorglgr` [granf2.c:111–128]:

```c
bool createorglgr(..., typehint *hintptr, typeisa *isaptr) {
  if (!findisatoinsertgr(fullcrumptr, hintptr, isaptr)) return FALSE;
  locinfo.infotype = GRANORGL;
  locinfo.granstuff.orglstuff.orglptr = createenf(POOM);   // empty POOM
  locinfo.granstuff.orglstuff.orglincore = TRUE;
  locinfo.granstuff.orglstuff.diskorglptr.diskblocknumber = DISKPTRNULL;
  insertseq(fullcrumptr, isaptr, &locinfo);
  return TRUE;
}
```

Everything stored for a node is: a tumbler address key + a `typegranorgl` record (`orglptr`, `diskorglptr`, `orglincore`). That is the same record type written for a document [wisp.h:88–92]. There is no separate node-specific data structure.

#### 2. The `typehint` is transient — it guides address placement, nothing more

`typehint` [xanadu.h:148–153]:

```c
typedef struct {
  INT supertype;
  INT subtype;
  INT atomtype;
  typeisa hintisa;
} typehint;
```

`NODE 1`, `ACCOUNT 2`, `DOCUMENT 3` [xanadu.h:140–142] are constants used only inside `findisatoinsertgr` [granf2.c:130–156] to decide which region of the tumbler address space to allocate into. After `createorglgr` returns the hint is gone; nothing about it persists in the granfilade leaf.

#### 3. No `struct node` exists anywhere in the codebase

A search across all headers confirms this. The only node-related type is:
- `NODEID 4` [xanadu.h:30] — an item type tag used in set operations, not a node-entity struct
- `typeboolsetnode` [xanadu.h:91–95] — a boolean-set operation node (linked-list node), completely unrelated to the Xanadu node concept

#### 4. BERT tracks documents, not nodes

The `bertentry` struct [bert.c:13–19]:

```c
typedef struct {
  int connection;
  tumbler documentid;
  char created, modified;
  int type;
  int count;
} bertentry;
```

`checkforopen` [bert.c:52–87] is called with a tumbler to see if a document is open. Nodes never appear as the subject of a BERT open/close. There is no parallel BERT-style table for node state.

#### 5. Access control is derived purely from tumbler prefix, not from a node record

`isthisusersdocument` [socketbe.c:197–200]:

```c
int isthisusersdocument(tumbler *tp) {
  return tumbleraccounteq(tp, &(player[user].account));
}
```

`tumbleraccounteq` [tumble.c:38–53] compares whether the account-prefix portion of a tumbler matches the current user's account tumbler. Ownership is encoded structurally in the address itself — not in any per-node record. A node is "owned" by whichever account contains its address prefix, and that is the account's address, not any stored node metadata.

---

### Summary

| Question | Answer | Evidence |
|---|---|---|
| Does a node have a `struct` of its own? | No | No `struct node` in any `.h` file |
| What is stored when a node is created? | A tumbler address + an empty POOM in the granfilade | `createorglgr` [granf2.c:111–128] |
| Is that representation different from a document's? | No — same `GRANORGL` record type | `wisp.h:88–92`, `granf2.c:119` |
| Does a node have its own capability list? | No | Access control uses `tumbleraccounteq` only |
| Does a node have BERT (open/close) state? | No | `bertentry.documentid`; no node-equivalent |
| Is node existence explicitly tracked? | Only as an address in the granfilade | `createorglgr` inserts into granf |

A node is purely an **address prefix** in the tumbler space. Its only physical manifestation is a granfilade leaf keyed by its tumbler, holding an empty POOM. Everything that would make a node "exist" in a richer sense — accounts, documents, links — is inferred from the presence of sub-addresses beneath it. The `NODE` constant is a routing tag used at creation time to choose the right address sub-range; it leaves no trace in the stored record.
