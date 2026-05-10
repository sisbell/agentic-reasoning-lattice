# Consultation Answers — Node Ontology

**Inquiry:** What is a node in the Xanadu system? How do nodes enter the docuverse, what invariants govern the node set, and what is the relationship between a node and the accounts it contains?
**Date:** 2026-03-12 20:51
**Questions:** 19 (9 nelson, 10 gregory)

---

## Question 1 [nelson]

> What defines the identity of a node — how is each node permanently distinguished from every other node in the docuverse?

### Nelson's Answer

## What Defines the Identity of a Node

A node's identity is its **tumbler address** — specifically, its unique position in the first field (the Server/Node field) of the tumbler addressing scheme. Nothing else. No name, no IP address, no description. The number IS the node.

### The Address Is the Identity

Every tumbler address has four major fields:

```
Node.0.User.0.Document.0.Element
```

The first field — the Node field — identifies which server node we are talking about. All nodes descend from digit 1, which represents the entire docuverse:

> "The server address always begins with the digit 1, since all other servers are descended from it. This may seem an unnecessary redundancy, but it permits referring to the entire docuverse by '1' on the first position." [LM 4/28]

So node `1.2` is the second node forked from the original. Node `1.2.3` is the third node forked under node `1.2`. Each position on this tree is unique and permanent.

### Baptism: How Nodes Get Their Numbers

A node's identity is created through **forking**, which I call "baptism":

> "A server node, or station, has ancestors and may have possible descendant nodes." [LM 4/19]

> "The owner of a given item controls the allocation of the numbers under it." [LM 4/20]

> "One digit can become several by a forking or branching process. This consists of creating successive new digits to the right; we call these 'under' the previous digit." [LM 4/20]

Whoever owns node `1.2` can baptize nodes `1.2.1`, `1.2.2`, `1.2.3` beneath it. No coordination with any other node is required. No central registry. The owner designates, and the number is born.

### Permanence: The Number Never Changes

> "New items may be continually inserted in tumbler-space while the other addresses remain valid. This means that any address of any document in an ever-growing network may be specified by a permanent tumbler address." [LM 4/19]

Once a node is baptized as `1.2.3`, it is `1.2.3` forever. The network can grow without limit — new nodes forking from existing nodes — and no existing address is ever disturbed.

### A Node Is a Ghost Element

Here is the subtlety that many people miss. A node is not a stored object. It is a **conceptual position** on the tumbler line:

> "While servers, accounts and documents logically occupy positions on the developing tumbler line, no specific element need be stored in tumbler-space to correspond to them. Hence we may call them ghost elements." [LM 4/23]

> "However, these elements are virtually present in tumbler-space, since links may be made to them which embrace all the contents below them." [LM 4/23]

The node's identity exists in the addressing scheme itself. You can link to node `1.2.3` — meaning all accounts, all documents, everything beneath that address — even though no "node object" is stored anywhere. The identity is the position, not a record.

### The Docuverse Is One Big Forking Tree

> "The entire tumbler works like that: nodes can spin off nodes; accounts can spin off accounts; nodes can spin off accounts; and so on. Thus all numeration in the docuverse is compressed into a single mechanism." [LM 4/19]

> "So the docuverse is all really one big forking document." [LM 4/18]

A node is distinguished from every other node by its unique path through this tree. Node `1.2` and node `1.3` are siblings — both forked under `1`, but permanently distinct. Node `1.2.4` is a descendant of `1.2` and could never be confused with `1.3.4`, even though both end in `.4`, because the ancestry is encoded in the full address.

### What a Node Identity Does NOT Include

The tumbler address says nothing about:
- The node's physical location
- What hardware it runs on
- What content it stores
- When it was created (time is kept track of separately — [LM 4/18])
- Any semantic category or classification

> "Tumblers do not affect the user-level structure of the documents; they only provide a mapping mechanism, and impose no categorization and no structure on the contents of a document." [LM 4/17-4/18]

The identity is purely positional — where this node sits in the ever-growing tree of the docuverse.

### Summary

A node is permanently distinguished by its **tumbler address in the Node field** — a unique, permanent, hierarchical number assigned through baptism by its parent node's owner. It requires no stored object (ghost element), no central coordination, and no metadata. The number is the identity, assigned once, valid forever.

---

## Question 2 [nelson]

> What must be true of the global address space when a new node enters the docuverse — must the node receive a unique, permanent portion of that space?

### Nelson's Answer

## Yes — absolutely and by design.

The entire tumbler system exists precisely to solve this problem. When a new node enters the docuverse, it must be **baptized** — given a unique, permanent position in the address tree from which all its future addresses will descend.

### The Mechanism: Owned Numbers and Baptism

The tumbler addressing system is built on a principle I call **owned numbers**:

> "The basic principle is that of owned numbers. Numbers are owned by individuals or companies, and subnumbers under them are bestowed on other individuals and companies on whatever basis the owners choose. Whoever owns a specific node, account, document or version may in turn designate (respectively) new nodes, accounts, documents and versions, by forking their integers. We often call this the 'baptism' of new numbers." [LM 4/17]

A new node receives its address from its parent node. If the existing network has node `1.2`, a new descendant node might be baptized as `1.2.3`. That address — `1.2.3` — becomes permanently reserved. Every account, document, version, and byte created under that node will carry `1.2.3` as the prefix of its address.

> "A server node, or station, has ancestors and may have possible descendant nodes. An account, too, and a document, all have possible descendants." [LM 4/19]

> "The entire tumbler works like that: nodes can spin off nodes; accounts can spin off accounts; nodes can spin off accounts; and so on. Thus all numeration in the docuverse is compressed into a single mechanism." [LM 4/19]

### Why Permanence Is Non-Negotiable

The guarantee is explicit:

> "New items may be continually inserted in tumbler-space while the other addresses remain valid. This means that any address of any document in an ever-growing network may be specified by a permanent tumbler address." [LM 4/19]

Once a node is baptized at position `1.2.3`, that position is occupied forever. No future node can take that address. No reorganization can move it. The address encodes the node's place in the genealogy of the network — and that genealogy is permanent.

### The Tree Structure of the Address Space

The node address is the **first field** of every tumbler in the system. The full I-space address has the form:

```
Node.0.User.0.Document.0.Element
```

> "The server address always begins with the digit 1, since all other servers are descended from it. This may seem an unnecessary redundancy, but it permits referring to the entire docuverse by '1' on the first position." [LM 4/28]

So the entire docuverse is rooted at `1`. Every node is a descendant of `1`. The address `1` refers to *everything*. A new node at `1.2.3` gets not just an address but an entire **subtree** — an infinite space of possible accounts, documents, versions, and bytes beneath it.

### The Node Need Not "Exist" as a Stored Object

Here is a subtle but important point. The node address reserves a position in the address space, but the system need not store anything to represent the node itself:

> "While servers, accounts and documents logically occupy positions on the developing tumbler line, no specific element need be stored in tumbler-space to correspond to them. Hence we may call them ghost elements." [LM 4/23]

> "However, these elements are virtually present in tumbler-space, since links may be made to them which embrace all the contents below them." [LM 4/23]

The node is a **conceptual position** — a ghost element. What gets stored is the content beneath it: bytes and links. But the position is real, permanent, and owned.

### No Central Authority Required

This is the beauty of the design. The node's parent baptizes it. No global registry is consulted:

> "Typically, the user will have no control over the node address he, she or it is assigned; but once assigned a User account, the user will have full control over its subdivision forevermore." [LM 4/29]

The parent node simply forks a new digit. Node `1.2` creates `1.2.1`, then `1.2.2`, then `1.2.3` — each a new server with its own permanent subtree. The forking is local, the effect is global.

> "One digit can become several by a forking or branching process. This consists of creating successive new digits to the right; we call these 'under' the previous digit." [LM 4/20]

### So the Docuverse Is One Big Forking Document

> "So the docuverse is all really one big forking document." [LM 4/18]

When a new node enters, it receives a permanent branch of this ever-growing tree. That branch is its portion of the universal address space — unique, permanent, and infinitely subdivisible. The node owns it, can delegate sub-addresses within it, and nothing that happens elsewhere in the tree can ever disturb it.

That is the guarantee. That is what makes the docuverse a single unified space that grows without bound while every address remains valid forever.

---

## Question 3 [nelson]

> Must every piece of content in the docuverse belong to exactly one node, or can content exist independent of any node?

### Nelson's Answer

## Every piece of content belongs to exactly one node — by address

The tumbler address structure makes this unambiguous. Every I-space address has the form:

```
Node.0.User.0.Document.0.Element
```

> "There are four major fields, each expandable indefinitely, with three major dividers between them. These fields are Server, User, Document and Contents." [LM 4/26]

The Node field is mandatory and always present:

> "The server address always begins with the digit 1, since all other servers are descended from it. This may seem an unnecessary redundancy, but it permits referring to the entire docuverse by '1' on the first position." [LM 4/28]

Since content bytes are the things actually stored in tumbler-space ("In the present implementation (XU.87.1), the only entities actually stored in tumbler-space are content bytes and links" [LM 4/23]), and every tumbler address encodes a node, every piece of content is assigned to exactly one node as part of its permanent identity.

## But physical residence is a different matter

The I-address encodes *origin*, not *current physical location*. Through BEBE, content replicates freely across nodes:

> "The contents can slosh back and forth dynamically." [LM 4/72]

> "Each server contains a map and a subset of the whole — a microcosm that shrinks and grows." [LM 4/71]

Content moves between servers for four reasons (from 4/71):
1. More rapid access to final material
2. More rapid access to needed index material
3. Rebalance in keeping with demand
4. Redundancy and backup

So a byte with I-address `1.3.0.7.0.42.0.1.500` permanently *belongs to* node 1.3, but may physically reside on nodes 1.3, 1.5, and 1.8 simultaneously through replication.

## Content cannot exist independent of a node

Three reasons:

**Structural:** The address format requires a node field. There is no "nodeless" tumbler. The node is as fundamental to the address as the document or element fields.

**Ownership chain:** Forking follows an ownership hierarchy — nodes own accounts, accounts own documents, documents own content. Content without a node has no place in this chain.

> "The owner of a given item controls the allocation of the numbers under it." [LM 4/20]

**Docuverse definition:** The docuverse *is* the occupied tumbler-space, and tumbler-space is rooted at node 1:

> "The docuverse is the occupied tumbler-space — as occupied by conceptually assigned positions, even if nothing represents them in storage." [LM 4/23]

> "So the docuverse is all really one big forking document." [LM 4/18]

## Summary

| Question | Answer |
|----------|--------|
| Must content belong to exactly one node? | **Yes** — by permanent I-address |
| Can content physically reside on multiple nodes? | **Yes** — through BEBE replication |
| Can content exist independent of any node? | **No** — the address structure forbids it |

The node assignment is *identity*, not *location*. It answers "where was this born?" not "where is this stored right now?"

---

## Question 4 [nelson]

> Does a node define an ownership boundary — is the node the authority over the accounts and documents it contains?

### Nelson's Answer

# Does a Node Define an Ownership Boundary?

**Short answer: A node defines an *allocation* boundary, not a *content authority* boundary.**

The node owner controls who gets accounts — but once an account is assigned, the account holder has permanent, irrevocable authority over their subtree. The node operator is a custodian, not an owner of the content it hosts.

## Allocation Authority: Yes

The node owner controls the creation of accounts beneath it. This follows from the general baptism principle:

> "The owner of a given item controls the allocation of the numbers under it." (4/20)

> "Whoever owns a specific node, account, document or version may in turn designate (respectively) new nodes, accounts, documents and versions, by forking their integers." (4/17)

The tumbler hierarchy is Node → Account → Document → Element. The node owner baptizes accounts; account owners baptize documents; and so on downward. The node is the root of a local subtree, and its owner decides who enters that subtree.

## Content Authority: No

Once an account is allocated, the account holder owns their entire subtree permanently. The node operator has no authority over the content within:

> "Typically, the user will have no control over the node address he, she or it is assigned; but once assigned a User account, the user will have full control over its subdivision forevermore." (4/29)

That "forevermore" is significant. The grant is irrevocable. And document ownership is absolute:

> "Every document has an owner, the person who created and stored it... Only the owner has a right to withdraw a document or change it." (2/29)

The node operator cannot modify, withdraw, or control documents belonging to account holders on their node.

## The Node Operator as Custodian

The Storage Vendor contract (Chapter 5) makes the custodial role explicit. The node operator must preserve and protect, but may not exercise authority over content:

> "Storage Vendor agrees to engage in best efforts for the preservation and privacy of all customer material, and not to breach the confidence of any customer, examining customers' stored materials only as required for the orderly maintenance of the system; and not to spy for any private persons, corporations or agencies of any government upon the private materials of any customers, nor discuss such private materials with anyone." (5/14-5/15)

And if the vendor goes away, customer content must be migrated, not lost:

> "Upon notice of cancellation, Storage Vendor will arrange for the orderly transition of all customer-stored materials to other Xanadu locations." (5/16)

## The Interoperation Obligation

The node is also not a silo. Vendors must serve content to users on other nodes:

> "Storage Vendor agrees to honor requests for material from customers connected to servers operated by other Xanadu-licensed storage vendors." (5/14)

This means the node boundary is invisible to users. Content flows across nodes transparently.

## Summary

| Role | Controls | Does NOT Control |
|------|----------|-----------------|
| **Node owner** | Which accounts exist on the node (baptism) | Content within those accounts |
| **Account owner** | All documents and sub-accounts beneath them, "forevermore" | Their node address assignment |
| **Document owner** | All content and versions within their document | Links others make to their published work |

The node is an administrative and physical hosting boundary. It is not an authority boundary over content. The deliberate separation — allocation power at the node level, content authority at the account level, custodial obligation binding the operator — prevents the node from becoming a gatekeeper. This serves Nelson's libertarian principle: the infrastructure serves the users, not the other way around.

---

## Question 5 [nelson]

> Can a document within one node contain content that originates from a different node, or is each document confined to material held locally?

### Nelson's Answer

## Yes — absolutely. Cross-node inclusion is fundamental to the architecture.

A document's virtual byte stream can include bytes from **any** document in the docuverse, regardless of which node stores them. This is not a special case; it is the normal mode of operation.

### The mechanism

Nelson distinguishes two kinds of bytes in a document:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

> "The virtual byte stream of a document may include bytes from any other document." [LM 4/10]

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

The I-space address itself encodes the originating node — `Node.0.User.0.Document.0.Element` — so the system always knows where to fetch non-native bytes. When your document on node 3 transcludes a passage from a document on node 7, the back end requests those bytes from node 7's storage. The user sees a seamless document.

### BEBE makes it invisible

The entire purpose of the inter-server protocol (BEBE) is to make node boundaries disappear:

> "The function of BEBE is to meld the contents of separate Xanadu servers into a single unified space." [LM 4/70]

Requests fan out from the user's local server to whichever servers hold the needed content, and replies funnel back:

> "First, by the forwarding of requests as they fan out from users to servers able to supply..." [LM 4/70]

Each server maintains a "microcosm" — a cached subset of the whole docuverse that grows and shrinks with demand:

> "Each server contains a map and a subset of the whole — a microcosm that shrinks and grows." [LM 4/71]

Popular remote content migrates closer to users who request it. The contents "slosh back and forth dynamically" [LM 4/72].

### The user experience

From the user's perspective, there is one docuverse, not a collection of servers:

> "Document A can include Document B, even though Document B is owned by someone else." [LM 2/35]

> "No copying operations are required among the documents throughout the system, and thus we solve the problems of update—especially the problem of updating documents which depend on other documents. We solve this problem simply by windowing to a changing document." [LM 2/36]

The user never specifies which server to contact. They work with tumbler addresses; the network resolves them.

### Why this matters

If documents were confined to local material, transclusion would be limited to content on the same server — which would fragment the docuverse into isolated silos. The entire vision of a unified, interconnected literature depends on cross-node inclusion working transparently. The vendor interoperation contract makes this a legal obligation, not just a technical capability:

> "Storage Vendor agrees to honor requests for material from customers connected to servers operated by other Xanadu-licensed storage vendors." [LM 5/14]

In short: a document is a V-space arrangement over I-space content. V-space is local to the document; I-space is global to the docuverse. The document reaches anywhere it needs to.

---

## Question 6 [nelson]

> Can links created within one node reference content held in a different node, and if so, must the target node participate in establishing that link?

### Nelson's Answer

## Yes — and no, the target node does not participate

Links can absolutely reference content on any node in the docuverse, and the target node plays no role in establishing the link. This falls out from several reinforcing design principles.

### Endsets reach across the entire docuverse

Nelson is explicit that link endpoints are not constrained to any single node or document:

> "The from-set may be an arbitrary collection of spans, pointing anywhere in the docuverse. Similarly, the to-set may be an arbitrary collection of spans pointing anywhere in the docuverse." [LM 4/43]

> "ENDSETS MAY POINT TO SPANS ANYWHERE IN THE DOCUVERSE" [LM 4/45]

The tumbler address space is unified across all nodes. A link's endset is just a set of tumbler addresses — the system draws no distinction between "local" and "remote" addresses at the link-creation level.

### Link creation is a unilateral, local operation

The MAKELINK operation creates a link in a specified home document. Nelson notes:

> "The document must be specified because that determines the actual residence of the link — since a document may contain a link between two other documents." [LM 4/63]

The home document determines ownership. The target documents — wherever they physically reside — are not consulted. This is reinforced by the ownership principle:

> "A link need not point anywhere in its home document. Its home document indicates who owns it, and not what it points to." [LM 4/12]

### Published content cannot refuse incoming links

Authors who publish explicitly relinquish control over incoming links:

> "Accessibility and free linking make a two-sided coin. On the one hand, each user is free to link to anything privately or publicly. By the same token, each author of a published work is relinquishing the right to control links into that work. This relinquishment must also be part of the publishing contract." [LM 2/43]

If the target *author* cannot control incoming links, the target *node* certainly has no veto power either.

### You can even link to nodes where nothing exists

Ghost elements make the point most starkly:

> "It is possible to link to a node, or an account, even though there is nothing stored in the docuverse corresponding to them." [LM 4/23]

If you can link to an address where nothing is stored, you obviously don't need the target's participation — there may be no target to participate.

### The target node participates only at retrieval time

The target node becomes involved only when someone *follows* the link (content delivery) or *searches* for links pointing to content on that node. This is handled by BEBE:

> "The function of BEBE is to meld the contents of separate Xanadu servers into a single unified space. This is done basically in two ways." [LM 4/70]

> "First, by the forwarding of requests as they fan out from users to servers able to supply." [LM 4/70]

Retrieval is when cross-node communication happens. Link *creation* is purely local to the home document's node. The contractual framework ensures that when retrieval does occur, the target vendor must cooperate:

> "Storage Vendor agrees to honor requests for material from customers connected to servers operated by other Xanadu-licensed storage vendors." [LM 5/14]

### Summary

Creating a link is a one-sided act. You write the link into your document at your address on your node. Its endsets specify tumbler addresses that may point to any node in the docuverse. The target node neither knows nor consents. The unified address space and the publication contract together guarantee that link creation requires no coordination — only link *traversal* requires inter-node communication.

---

## Question 7 [nelson]

> Must node identities be ordered — does the sequence in which nodes enter the docuverse carry permanent meaning in the address space?

### Nelson's Answer

# Must Node Identities Be Ordered?

**Yes.** The sequence in which nodes enter the docuverse is permanently encoded in their tumbler addresses and carries lasting structural significance—though not semantic significance.

## The Mechanism: Sequential Forking

Nodes are created by forking under their parent. The root of the docuverse is node 1. When node 1 spawns child nodes, they receive sequential addresses: 1.1, 1.2, 1.3, and so on. This sequence is permanent.

> "One digit can become several by a forking or branching process. This consists of creating successive new digits to the right; we call these 'under' the previous digit." (4/20)

> "For instance, if there is an item 2, it can branch into several more items, each of which is a daughter item. Thus 2.1, 2.2, 2.3, 2.4... are successive items being placed under 2." (4/20)

> "The owner of a given item controls the allocation of the numbers under it." (4/20)

The parent node controls baptism of child nodes. Node 1.3 was necessarily baptized *after* 1.2—the sequential integers reflect creation order among siblings.

## The Ordering Is Permanent

Once a node receives its address, that address never changes and its position relative to all other addresses is fixed forever:

> "New items may be continually inserted in tumbler-space while the other addresses remain valid. This means that any address of any document in an ever-growing network may be specified by a permanent tumbler address." (4/19)

You cannot retroactively insert a node "between" 1.2 and 1.3. However, you *can* create children under 1.2 (e.g., 1.2.1, 1.2.2), which appear between 1.2 and 1.3 on the tumbler line due to depth-first ordering.

## The Tumbler Line: Total Order via Tree Mapping

All tumblers—including node addresses—map to a single ordered line:

> "In a sense the tumbler line is like the real line, i.e., the line of integers and all the numbers in between. But the tumbler line is a different kind of abstraction from the real line. The real line is the same under all circumstances. The tumbler line is an abstract representation of a particular tree." (4/22)

> "The contents of the tumbler line are determined by the population of entities and relations on the tree it represents. Thus the tumbler line is not definite in the same way as the real line; the tumbler line is a flat mapping of a particular tree, finite but unlimited." (4/22)

This means node ordering is not just sibling-sequential—it's a *total order* on all nodes via the depth-first tree walk. Node 1.2.5 comes after 1.2.4 but before 1.3 on the tumbler line.

## What the Ordering Means (and Doesn't Mean)

The ordering carries **operational significance** but **no semantic significance**:

**Operationally significant:**
- Spans work because ordering is stable. You can address "everything on nodes 1.2 through 1.5" as a single span.
- A span containing node 1.2 implicitly contains all of 1.2's descendants (1.2.1, 1.2.2, ...) because they fall within the span on the tumbler line.
- Ghost elements are addressable at node positions even without stored content: "A link to or search of an account or node will find any of the documents under it." (4/23)

**Semantically neutral:**
- The address says nothing about the node's content, purpose, or importance.
- "Tumblers do not affect the user-level structure of the documents; they only provide a mapping mechanism, and impose no categorization and no structure on the contents of a document." (4/17–4/18)
- Time is explicitly excluded: "Note that 'time' is not included in the tumbler. Time is kept track of separately." (4/18)

## The Root Convention

All nodes descend from a single root:

> "The server address always begins with the digit 1, since all other servers are descended from it. This may seem an unnecessary redundancy, but it permits referring to the entire docuverse by '1' on the first position." (4/28)

This means the ordering begins from a universal anchor point. The "1" is not just the first node—it is the address of the entire docuverse, enabling a span starting at "1" to cover everything.

## Summary

Node sequence carries permanent meaning in three ways:

1. **Creation order among siblings** — node 1.3 was baptized after 1.2; this is immutable
2. **Position on the tumbler line** — determines span coverage and range queries
3. **Hierarchical descent** — a node's children fall within its span, enabling hierarchical addressing

But the sequence carries *no* semantic, temporal, or qualitative meaning. It is a coordinate system, not a ranking.

---

## Question 8 [nelson]

> What invariants must hold over the set of all nodes — must their address portions be non-overlapping, contiguous, or satisfy some other structural property?

### Nelson's Answer

## Node Address Invariants in the Docuverse

Nelson does not state a single "node invariant" explicitly, but several structural properties are derivable from his tumbler and forking design. Here is what the specification establishes:

### 1. Tree-Structured Non-Overlap (Inherent)

Node addresses form a tree rooted at digit 1. Each node owns a unique subtree of the address space. Non-overlap is not an enforced invariant — it is a structural consequence of the addressing scheme.

> "The server address always begins with the digit 1, since all other servers are descended from it. This may seem an unnecessary redundancy, but it permits referring to the entire docuverse by '1' on the first position." [LM 4/28]

> "A server node, or station, has ancestors and may have possible descendant nodes." [LM 4/19]

> "The owner of a given item controls the allocation of the numbers under it." [LM 4/20]

Because sub-nodes are created by appending digits (1 → 1.1, 1.2, 1.3...; 1.2 → 1.2.1, 1.2.2...), sibling subtrees are structurally disjoint. Content at `1.2.0.U.0.D.0.E` cannot also be at `1.3.0.U.0.D.0.E` — the Node field distinguishes them absolutely.

### 2. Not Contiguous — Sparse Population Is Valid

Nodes need **not** be contiguous among siblings. You may have nodes 1.1 and 1.3 without 1.2 ever existing. Ghost elements explicitly allow this:

> "While servers, accounts and documents logically occupy positions on the developing tumbler line, no specific element need be stored in tumbler-space to correspond to them. Hence we may call them ghost elements." [LM 4/23]

> "A span that contains nothing today may at a later time contain a million documents." [LM 4/25]

The address space is sparse by design. The forking mechanism creates addresses on demand through "baptism" — there is no requirement that all integer positions between existing nodes be populated.

### 3. Subtree Contiguity on the Tumbler Line

While nodes need not be contiguous siblings, each node's **subtree** maps to a contiguous range on the tumbler line (which is a depth-first serialization of the tree):

> "In a sense the tumbler line is like the real line... But the tumbler line is a different kind of abstraction from the real line... The tumbler line is a flat mapping of a particular tree, finite but unlimited." [LM 4/22]

> "A span in the tumbler line, represented by two tumblers, refers to a subtree of the entire docuverse." [LM 4/24]

This is the property that makes spans work for node-level operations. A single span can address "everything on node 1.2" — all accounts, documents, versions, and bytes under that prefix — because the depth-first mapping guarantees the subtree is contiguous on the line.

### 4. Content Partition by Home Node

Every byte in the docuverse has exactly one **home** node, determined by the Node field of its I-address. This partitions all native content across nodes:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

> "There are four major fields, each expandable indefinitely, with three major dividers between them. These fields are Server, User, Document and Contents." [LM 4/26]

Note: this is a partition of *ownership*, not physical presence. BEBE allows content to be cached across nodes:

> "The contents can slosh back and forth dynamically." [LM 4/72]

But the I-address (and therefore the home node) never changes.

### 5. Ownership Delegation (Baptism Invariant)

Only the owner of a node can create sub-nodes beneath it. This is the "baptism" principle:

> "The basic principle is that of owned numbers. Numbers are owned by individuals or companies, and subnumbers under them are bestowed on other individuals and companies on whatever basis the owners choose. Whoever owns a specific node, account, document or version may in turn designate (respectively) new nodes, accounts, documents and versions, by forking their integers." [LM 4/17]

This means the tree can only grow downward from existing owned positions. No node can create a sibling or a parent — only children. This preserves the non-overlap property: since you can only subdivide what you own, you cannot create addresses that collide with another node's subtree.

### 6. Single Root

All nodes descend from 1. There is exactly one root. This is both stated and architecturally necessary for the tumbler line to work as a unified space.

### Summary of Invariants

| Property | Holds? | Source |
|----------|--------|--------|
| Non-overlapping subtrees | Yes (structural) | Tree addressing + forking |
| Contiguous siblings | **No** — sparse allowed | Ghost elements [4/23] |
| Contiguous subtree on tumbler line | Yes | Depth-first mapping [4/22, 4/24] |
| Content partitioned by home node | Yes (by I-address) | Native bytes [4/11, 4/26] |
| Downward-only creation (baptism) | Yes | Ownership delegation [4/17] |
| Single root at 1 | Yes | [4/28] |

### What Nelson Does Not Address

Nelson does not discuss:
- Whether a node can be **retired** or **merged** with another (only vendor shutdown with "orderly transition" is specified [5/16])
- Maximum depth of the node tree
- Whether node addresses can be **reassigned** after abandonment
- Formal constraints on the rate or pattern of node creation

NEED_RAW: [4/17-4/21, 4/28-4/29] — these pages cover forking and the server address field in detail. The curated sources provide good coverage, but the raw pages may contain diagrams or marginal notes about structural constraints on node creation that the text extraction missed.

---

## Question 9 [nelson]

> Does a node impose any visibility boundary on its content, or is all content within every node universally addressable across the entire docuverse?

### Nelson's Answer

## No Visibility Boundary at the Node Level

A node imposes **no visibility boundary** on its content. All published content within every node is universally addressable across the entire docuverse. The node field in a tumbler address indicates *where* content is physically stored, not *who* can see it.

### The Unified Space Guarantee

BEBE exists precisely to eliminate node boundaries from the user's perspective:

> "The function of BEBE is to meld the contents of separate Xanadu servers into a single unified space."
> — [LM 4/70]

Each server maintains a model of the whole, not just its own contents:

> "Each server contains a continuously valid model or subrepresentation of the entire docuverse and (because of tumbler addressing) a model of the entire network."
> — [LM 4/72]

The user experience is explicitly one of location transparency:

> "Perhaps the most important thing, and certainly the hardest part to believe, is that everything on such a network-- any subset, substructure or grouping-- can come to the user immediately, even as the aggregation grows to tremendous size."
> — [LM 2/57]

### Visibility Is Per-Document, Not Per-Node

The access control boundary is the **document**, not the server. A document is either private (owner and designees only) or published (everyone):

> "A document may be private or published. [...] A private document may be read and linked-to only by the owner and his or her associates. A published document is available to anyone, and may be read and linked-to by anyone."
> — [LM 2/42]

A node could contain a mix of private and published documents. The node itself has no "wall" around it.

### Vendors Must Honor Cross-Node Requests

The contractual structure makes this explicit. Storage Vendors are obligated to serve content to users on other vendors' servers:

> "Storage Vendor agrees to honor requests for material from customers connected to servers operated by other Xanadu-licensed storage vendors, and accept material for storage from other Xanadu-licensed vendors within the network."
> — [LM 5/14]

A vendor cannot refuse to serve its published content to outside users. That would break the unified docuverse.

### The Node Address Is Routing, Not Scoping

Tumblers encode the node purely as a storage/routing mechanism:

> "Tumblers do not affect the user-level structure of the documents; they only provide a mapping mechanism, and impose no categorization and no structure on the contents of a document."
> — [LM 4/17-4/18]

The node field tells the network *where to find* the content. Ghost elements reinforce this — you can link to a node address and reach everything beneath it:

> "A link to or search of an account or node will find any of the documents under it."
> — [LM 4/23]

### Summary

The docuverse is one space, not a federation of walled nodes. Nodes are storage locations within that space. The only visibility boundary Nelson specifies is the document-level private/published distinction — and that boundary is orthogonal to which node stores the document.

---

## Question 10 [gregory]

> What tumbler structure identifies a node — is a node always a single non-zero digit (e.g., `1`), or can node addresses be multi-digit (e.g., `1.3`), and how many tumbler fields does the node occupy before the first `.0.` separator?

### Gregory's Answer

## KB Synthesis

## Node Tumbler Structure

Nodes **can be multi-digit** — the node address is not constrained to a single digit. It grows by appending digits **without** any `.0.` separator as you descend the node hierarchy.

### How node nesting works

From [SS-ADDRESS-SPACE] Finding 0021, the `makehint` table:

| supertype | subtype | depth | Meaning |
|-----------|---------|-------|---------|
| NODE | NODE | 1 | Node under node |
| ACCOUNT | DOCUMENT | 2 | Document under account |

`depth = (supertype == subtype) ? 1 : 2`

Depth=1 means no `.0.` boundary is crossed. Each nested node level appends one more digit sequentially:

- Top-level: `1`, `2`, `3` ...
- Under node `1`: `1.1`, `1.2`, `1.3` ...
- Under node `1.1`: `1.1.1`, `1.1.2` ...
- Under node `1.1.1`: `1.1.1.1` ...

Examples from Finding 0021:
> "Nodes under a node: `1.1.0.1.1`, `1.1.0.1.2` (no `.0.` boundary)"

### Field count before the first `.0.`

The node occupies **all leading digits up to (but not including) the first `.0.` separator**. From the docuverse convention ([SS-TUMBLER] Finding 0001):

> The `.0.` field dividers give the pattern `Node.0.User.0.Doc.0.Element`

So in `1.1.0.2.0.1`:
- Node: `1.1` (2 digits)
- Account: `2` (1 digit after first `.0.`)
- Document: `1` (1 digit after second `.0.`)

In `1.1.0.1.0.1.0.2.1` from [SS-ADDRESS-SPACE] Finding 0065:
- Node: `1.1` (2 digits)
- Account: `1`
- Document: `1`
- Element (link 2, number 1): `2.1`

The node field length is unbounded — it equals the depth of the node in the node-under-node hierarchy, with no upper limit other than the tumbler's 16-mantissa-digit capacity ([SS-TUMBLER] Finding 0031).

### Containment check

[SS-TUMBLER-CONTAINMENT] Finding 0021 confirms the prefix-match semantics apply: `tumblertruncate(A, length(B))` then compare. Whether `1.1.0.1.1` is under `1.1.0.1` is determined by truncating `1.1.0.1.1` to length 5 and comparing with `1.1.0.1` — yielding `1.1.0.1.1` ≠ `1.1.0.1`, so **no** (node siblings are not contained in each other). But `1.1.0.1.0.1` truncated to length 5 = `1.1.0.1.0` ≠ `1.1.0.1` — also no. Only addresses that have `1.1.0.1` as an exact prefix (same digits at the same positions) satisfy containment.

---

## Code Exploration

Now I have all the information needed. Let me compile the complete answer.

---

## Answer: Tumbler Structure of a Node Address

### 1. The `tumbler` Struct

Defined in `backend/common.h:59-65`:
```c
typedef struct structtumbler {
    humber xvartumbler;
    char varandnotfixed;
    char sign  BIT;  /* 1 if negative, otherwise 0 */
    short exp;
    tdigit mantissa[NPLACES];
} tumbler;
```

Where `NPLACES = 16` [`common.h:53`] and `tdigit = UINT = uint32_t` [`common.h:57`, `defs.h:12`]. Each mantissa slot is one "digit" (story) in the tumbler. A value of `0` in a mantissa slot is the `.0.` separator in string notation.

---

### 2. Is a Node Always a Single Non-Zero Digit?

**Yes — each node creation appends exactly ONE mantissa digit to the parent address.**

From `backend/do1.c:251` and `granf2.c:209-241`:

```c
// do1.c:251
makehint(NODE, NODE, 0, &isa, &hint);
result = createorglingranf(taskptr, granf, &hint, &isa);
```

```c
// granf2.c:209
depth = hintptr->supertype == hintptr->subtype ? 1 : 2;
```

When `supertype == NODE` and `subtype == NODE`, `depth = 1`. The first allocation path is:

```c
// granf2.c:237
tumblerincrement(&hintptr->hintisa, depth, 1, isaptr);
```

`tumblerincrement(aptr, rightshift, bint, cptr)` at `tumble.c:599-623` places `bint` at the slot `lastNonZero(aptr) + rightshift`. With `depth=1` and `rightshift=1`, it appends `1` at exactly **one position** beyond the last non-zero digit of the parent address.

For subsequent nodes (when something already exists), `granf2.c:239-240`:
```c
tumblertruncate(&lowerbound, hintlength + depth, isaptr);
tumblerincrement(isaptr, tumblerlength(isaptr)==hintlength?depth:0, 1, isaptr);
```

This increments the last existing slot by 1 — still one digit.

**Golden test evidence** (`golden/accounts/create_multiple_nodes.json`):
```
Account: 1.1.0.1
Node 1:  1.1.0.1.1   ← parent + digit 1
Node 2:  1.1.0.1.2   ← parent + digit 2 (same slot incremented)
Node 3:  1.1.0.1.3   ← parent + digit 3
```

Each node is exactly **one additional mantissa slot**. The digit is always a single `uint32_t` value ≥ 1. It can be any positive integer (e.g., `3`), but it always occupies **one slot** — never a multi-digit sequence like `.1.3`.

Contrast with document allocation, where `depth = 2` (ACCOUNT → DOCUMENT, different types), which inserts a `.0.` separator then the document number — two additional slots.

---

### 3. How Many Fields Before the First `.0.` Separator?

**Two fields.** In every observed address in this system, mantissa positions 0 and 1 are both non-zero (both `= 1`), and position 2 is the first zero.

For example:
| Address | mantissa |
|---|---|
| `1.1.0.1` (account) | `[1, 1, 0, 1, 0, 0, ...]` |
| `1.1.0.1.1` (node) | `[1, 1, 0, 1, 1, 0, ...]` |
| `1.1.0.1.0.1` (document) | `[1, 1, 0, 1, 0, 1, ...]` |
| `1.1.0.1.1.0.1` (doc under node) | `[1, 1, 0, 1, 1, 0, 1, ...]` |

The `1.1` prefix (two mantissa fields) before the first `.0.` is the **network/host node identifier** — the Xanadu global node address identifying this server in the wider network. All addresses within this backend share the same `1.1` prefix.

This two-field prefix is confirmed by `tumbleraccounteq` at `tumble.c:54-68`, which scans past zeros in the account address. For account `1.1.0.1` (mantissa = `[1,1,0,1,0,0,...]`), the first zero at position 2 is encountered, counted once; the terminating second zero is found at the trailing positions. The scan logic confirms the first separator `.0.` is at slot index 2.

Also confirmed by `Address.split()` in `febe/client.py:201-205`:
```python
def split(self):
    """For a global address, return the docid and local components."""
    delim = len(self.digits) - 1
    while self.digits[delim] != 0: delim = delim - 1
    return Address(self.digits[:delim]), Address(self.digits[delim+1:])
```

Splitting `1.1.0.1.0.1` at its **last** `.0.` yields `docid = 1.1.0.1`, `local = 1`. The first `.0.` (at position 2) separates the host-node prefix `1.1` from the rest.

---

### Summary

| Question | Answer | Source |
|---|---|---|
| Node mantissa slots added per level | **1** — single digit appended | `granf2.c:209, 237` — `depth=1` for NODE→NODE |
| Can a node be multi-digit (e.g. `.1.3`)? | **No** — always exactly one slot | `tumblerincrement` with `rightshift=1` |
| Fields before first `.0.` | **2** (the host/network node `1.1`) | `common.h:53`, `tumble.c:54-68`, golden tests |
| `.0.` role | Separates hierarchy levels — inserted only when crossing type boundaries (depth=2) | `granf2.c:209` |

The two fields before `.0.` (`1.1` in this implementation) are the **Xanadu network node address** — a two-level global identifier for this backend instance. Everything within the system (accounts, documents, nodes, content) is addressed within that prefix. Nodes in the `NODE` type sense each occupy exactly **one additional mantissa digit** beyond their parent, with no `.0.` separator — that separator only appears between the account/node level and the document level (`depth=2`, ACCOUNT→DOCUMENT).

---

## Question 11 [gregory]

> When a fresh backend instance starts for the first time, what initialization steps create the node's identity — is there a node address written into the granfilade or spanfilade root, or is the node address purely a configuration parameter external to the enfilade state?

### Gregory's Answer

## KB Synthesis

The KB does not contain sufficient detail to answer this definitively. Here is what the KB does and does not tell us:

**What the KB says about initialization:**

[SS-DUAL-ENFILADE, Finding 0012] — `entexit.c:44-45` shows the initialization sequence:
```c
granf = createenf(GRAN);
spanf = createenf(SPAN);
```

[SS-ENFILADE-TREE, Finding 0058] — `createenf(POOM)` produces a minimal height-1 tree with one zero-width bottom node (`infotype=GRANNULL` for GRAN). The fresh enfilade has no content.

[SS-UNIFIED-STORAGE, Finding 0059] — All persistent state lives in `enf.enf`. Fixed locations on disk: granf root at `GRANFDISKLOCATION`, spanf root at `SPANFDISKLOCATION`. On startup, `disk.c:364-382` opens or creates this file.

[EC-NO-STARTUP-VALIDATION, Finding 0059] — `initenffile()` opens the file and reads the block allocation table via `readallocinfo()`. No tree traversal or consistency check occurs. The KB doesn't describe what is written into a *newly created* `enf.enf` on first run.

**What the KB implies but does not confirm:**

The bootstrap document at `1.0.2.x` must exist for link type creation to work — [SS-LINK-ENDPOINT, Finding 0024] references JUMP (`1.0.2.2`), QUOTE (`1.0.2.3`), FOOTNOTE (`1.0.2.6`) as pre-existing entries. This implies some initial granfilade content is either pre-seeded at first run or shipped as a pre-built `enf.enf`.

All document addresses embed the node prefix (e.g., `1.1.0.1.0.1`) [SS-ADDRESS-SPACE, Finding 0021], and `makehint` uses `hintisa` as the parent for allocation — but where that initial hint address originates (config file, command-line argument, or a seeded granfilade entry) is not covered in the KB.

**The gap:** The KB does not trace the `xumain.c` startup path beyond the `strlen()` reference at line 143, does not describe `init.c`'s role in node address setup, and does not explain whether `1.1` (or the local node address) is stored as state inside the granfilade or supplied externally at daemon launch. The bootstrap document existence is asserted but its creation mechanism is not documented.

To answer your question, the KB evidence would need to include what `initenffile()` writes on first creation vs. re-open, and how `makehint`'s root `hintisa` gets populated on a clean node.

---

## Code Exploration

I now have everything needed for a definitive, fully-cited answer.

---

## Node Identity Initialization in udanax-green

### Short Answer

The node address is a **hardcoded compile-time constant** embedded in `be.c`. It is **not written into the granfilade or spanfilade root nodes**, and it is **not a configurable parameter** in any runtime config file. The enfilade roots are pure structural containers; identity lives only in a runtime task variable.

---

### The `main()` Entry Points

There are two entry points, and they handle node identity differently:

**`be.c` (FEBE server mode — the primary path used by the test harness):**

```c
// be.c:37
tumbler defaultaccount = {0,0,0,0, 1,1,0,1,0,0,0,0}; /* 1.1.0.1 */

// be.c:83–88
init (1);
inittask (&task);
initmagicktricks ();
movetumbler(&defaultaccount,&task.account);
```

The node address `1.1.0.1` is a C static aggregate initializer baked into the binary. `movetumbler` is a macro [`common.h:73`] that does a raw struct copy: `*B = *A`. The address lands in `task.account`, a runtime-only variable on the stack.

**`xumain.c` (standalone mode):**

```c
// xumain.c:49
getaccount(&task,&task.account);
```

`getaccount` in `task.c:28–41` simply calls `tumblerclear(accountptr)`, zeroing the entire tumbler struct. The standalone mode runs with address `0.0.0.0`.

---

### Tumbler Structure

```c
// common.h:53–65
#define NPLACES 16
typedef UINT tdigit;
typedef struct structtumbler {
    humber xvartumbler;       // unused ptr field
    char varandnotfixed;
    char sign;                // 1 = negative
    short exp;
    tdigit mantissa[NPLACES]; // hierarchical address digits
} tumbler;

#define ZEROTUMBLER  {0,0,0,0,  0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0}
```

`defaultaccount = {0,0,0,0, 1,1,0,1,0,0,0,0}` maps to: `xvartumbler=0, varandnotfixed=0, sign=0, exp=0, mantissa={1,1,0,1,0,...}` — which the comment confirms decodes to tumbler address `1.1.0.1`.

---

### Enfilade Initialization: Fresh vs. Resume

`initmagicktricks()` in `entexit.c:19–47` dispatches:

```c
// entexit.c:41–46
if (initenffile()) {
    initkluge ((typecuc**)&granf, (typecuc**)&spanf);
} else {
    granf = (typegranf) createenf (GRAN);
    spanf = (typespanf) createenf (SPAN);
}
```

**`initenffile()` in `disk.c:340–383`** resolves which path to take:

```c
// disk.c:364–376
fd = open ("enf.enf", 2 /*rw*/,0);
if (fd == -1) {                       // No file → fresh start
    fd = creat ("enf.enf", 0666);
    initheader ();
    enffileread = FALSE;
    ret = FALSE;                       // returns FALSE → create empty enfilades
} else {
    ret = readallocinfo (fd);          // Existing file → resume path
    enffileread = TRUE;                // returns TRUE → initkluge reads from disk
}
```

In test mode (`--test-mode`), `initenffile()` unconditionally returns `FALSE` [`disk.c:360`], always creating a fresh empty state.

**Fresh start path:** `createenf(GRAN)` and `createenf(SPAN)` allocate empty root nodes with no content and no embedded address.

**Resume path:** `initkluge()` in `corediskin.c:18–41` reads the enfilade roots from fixed disk locations:

```c
// corediskin.c:25–26
tempcbc->cinfo.granstuff.orglstuff.diskorglptr.diskblocknumber = GRANFDISKLOCATION;
// ...
// corediskin.c:33
tempcbc->cinfo.granstuff.orglstuff.diskorglptr.diskblocknumber = SPANFDISKLOCATION;
```

These constants are:
```c
// coredisk.h:119–120
#define GRANFDISKLOCATION (NUMDISKLOAFSINHEADER+1)
#define SPANFDISKLOCATION (NUMDISKLOAFSINHEADER+2)
```

The enfilade roots at these locations are **structural nodes** — they contain enfilade topology (height, son counts, disk pointers) but **no node address or identity field**.

---

### What `.backendrc` Configures

`rcfile.c:18–93` shows `processrcfile()` parses these keys: `port`, `host`, `backenddir`, `backend`, `accountfile`, `frontend`, `backglue`, `frontglue`, `allocsize`, `incrementalallocsize`. There is **no `account`, `node`, or `address` key** — the rc file cannot configure node identity.

---

### Summary

| Question | Answer | Citation |
|---|---|---|
| Is there a node address in the granfilade root? | No — enfilade roots contain only structural topology | `corediskin.c:18–41` |
| Is there a node address in the spanfilade root? | No — same reason | `corediskin.c:33–38` |
| Where does node identity live? | `task.account` — a runtime stack variable | `be.c:88` |
| What is the address? | `1.1.0.1` (server mode) or `0.0.0.0` (standalone mode) | `be.c:37`, `task.c:31` |
| Is it configurable at runtime? | No — hardcoded in source; `.backendrc` has no account key | `rcfile.c:18–93` |
| Does fresh start write an address anywhere? | No — `createenf(GRAN/SPAN)` creates empty structural roots | `entexit.c:44–45` |

**The node address is purely a configuration parameter external to the enfilade state.** In FEBE server mode, it is a compile-time constant (`1.1.0.1`) copied into `task.account` after enfilade initialization. The granfilade and spanfilade roots store enfilade structure — they carry no node identity whatsoever.

---

## Question 12 [gregory]

> Is there a node-level data structure (analogous to a document's POOM) that indexes accounts under a node, or is the node→account relationship implicit in the tumbler prefix convention with no dedicated orgl?

### Gregory's Answer

## KB Synthesis

The KB does not document any dedicated node-level orgl or POOM structure for indexing accounts. Based on the available evidence, the node→account relationship is **implicit in the tumbler prefix convention**, enforced through address arithmetic on the single global granfilade.

## What the KB says

**Single flat tree.** [SS-ADDRESS-ALLOC] Finding 0021 is explicit: "The entire granf (global address enfilade) is a single flat tree; the allocation algorithm enforces hierarchical structure by bounding searches to the parent's address range." There is no per-node secondary index — containment is computed on demand via `findpreviousisagr` bounded searches.

**Containment is arithmetic.** [SS-TUMBLER-CONTAINMENT] Finding 0021 documents the containment predicate: truncate address A to the length of B and compare. This is pure tumbler arithmetic — `tumblertruncate` + `tumblereq` — with no orgl lookup involved.

**The `makehint` table is incomplete for node→account.** [SS-ADDRESS-SPACE] Finding 0021 lists allocation hints:

| supertype | subtype | depth |
|-----------|---------|-------|
| NODE | NODE | 1 |
| ACCOUNT | DOCUMENT | 2 |
| DOCUMENT | DOCUMENT | 1 |
| DOCUMENT | ATOM | — |

There is no NODE→ACCOUNT row. Accounts (`1.1.0.x`) sit two `.0.`-boundaries below a node (`1.1`), but the KB records no dedicated mechanism for traversing or indexing that relationship — only the prefix convention.

**Orgls exist for documents and links, not nodes.** [SS-GRANF-OPERATIONS] documents the granfilade operations: `findorgl()`, `createorglingranf()`, `inserttextingranf()`, `ispanset2vstuffset()`. These are invoked for documents and link orgls. The KB contains no finding describing a node orgl being created or opened.

## Answer

There is no node-level POOM or dedicated index. The node→account→document hierarchy exists entirely in the tumbler digit sequence. Navigation or enumeration of accounts under a node would require walking the global granfilade tree bounded by the node's address prefix — the same `findpreviousisagr` / `tumblertruncate` machinery used for all address-range queries. This is convention over structure: the hierarchy is reconstructible from address arithmetic, not stored as a separate data structure.

This is consistent with the broader design pattern the KB describes — the implementation uses a single flat B-tree and trusts callers to impose hierarchical semantics through address construction. Just as the subspace convention (1.x for text, 2.x for links) is unenforced at the storage layer [SS-SUBSPACE-CONVENTION], the node→account containment relationship is unenforced by any dedicated node-level structure.

---

## Code Exploration

Now I have everything needed. Here is the complete answer.

---

## Is there a node-level data structure indexing accounts under a node?

**Short answer: No.** There is no dedicated node-level orgl that inventories its child accounts. The node→account relationship is entirely implicit in the tumbler address prefix convention. Every node gets a POOM orgl (via the same `createorglgr` pathway as documents), but that POOM stores no children list — it is empty by design. The single global `granf` is the only index, and it is organized by address space: finding children means range-scanning granf for addresses prefixed by the parent.

---

### 1. The Global Index: `granf`

`xanadu.h:13-14`:
```c
#define typegranf INT *   /* temp -- INT for alignment */
extern typegranf granf;
```

There is exactly one granfilade in the system. All nodes, accounts, documents, and atoms are stored as leaf entries in this single tree, keyed by their tumbler address. There is no per-node sub-granf.

---

### 2. What Creating a Node Actually Does

`do1.c:243-258`:
```c
bool docreatenode_or_account(typetask *taskptr, typeisa *isaptr)
{
    typeisa isa;
    typehint hint;
    bool createorglingranf();
    bool result;

    tumblercopy(isaptr, &isa);
    makehint (NODE, NODE, 0, &isa, &hint);
    result = createorglingranf (taskptr, granf, &hint, &isa);
    if (result) {
        tumblercopy(&isa, isaptr);
    }
    return result;
}
```

Notice: this same function handles both nodes and accounts — there is no `docreateaccount` distinct from `docreatenode`. Both call `createorglingranf` with `supertype=NODE, subtype=NODE`. The distinction between "node" and "account" is a naming convention outside the storage layer, not a structural distinction.

`createorglingranf` delegates to `createorglgr` at `granf2.c:111-128`:
```c
bool createorglgr(typetask *taskptr, typegranf fullcrumptr, typehint *hintptr, typeisa *isaptr)
{
    typegranbottomcruminfo locinfo;
    bool findisatoinsertgr();
    typecuc *createenf();

    if (!findisatoinsertgr ((typecuc*)fullcrumptr, hintptr, isaptr))
        return (FALSE);
    locinfo.infotype = GRANORGL;
    locinfo.granstuff.orglstuff.orglptr = createenf (POOM);  // ← a POOM, not a node-index
    reserve ((typecorecrum*)locinfo.granstuff.orglstuff.orglptr);
    locinfo.granstuff.orglstuff.orglincore = TRUE;
    locinfo.granstuff.orglstuff.diskorglptr.diskblocknumber = DISKPTRNULL;
    locinfo.granstuff.orglstuff.diskorglptr.insidediskblocknumber = 0;
    insertseq ((typecuc*)fullcrumptr, isaptr, &locinfo);
    rejuvinate ((typecorecrum*)locinfo.granstuff.orglstuff.orglptr);
    return (TRUE);
}
```

What gets created is a `POOM` enfilade (`createenf(POOM)`) — the same type used for documents. It is immediately inserted into `granf` at the newly-assigned address and left empty. No subsequent call populates this POOM with account references.

---

### 3. The Hint Mechanics — Depth Determines Address Hierarchy

`do2.c:78-84`:
```c
int makehint(INT typeabove, INT typebelow, INT typeofatom, typeisa *isaptr, typehint *hintptr)
{
    hintptr->supertype = typeabove;
    hintptr->subtype   = typebelow;
    hintptr->atomtype  = typeofatom;
    movetumbler (isaptr, &hintptr->hintisa);
}
```

And in `findisatoinsertnonmolecule` at `granf2.c:203-242`, the key line:

```c
depth = hintptr->supertype == hintptr->subtype ? 1 : 2;
```

| Call site | supertype | subtype | depth | Meaning |
|---|---|---|---|---|
| Node/account creation | `NODE(1)` | `NODE(1)` | 1 | One tumbler level deeper |
| New document under account | `ACCOUNT(2)` | `DOCUMENT(3)` | 2 | Two tumbler levels deeper |
| New version in same account | `DOCUMENT(3)` | `DOCUMENT(3)` | 1 | One level deeper |
| Atom in document | `DOCUMENT(3)` | `ATOM(4)` | 2 | Two levels deeper |

`xanadu.h:140-143`:
```c
#define NODE      1
#define ACCOUNT   2
#define DOCUMENT  3
#define ATOM      4
```

When `makehint(NODE, NODE, 0, parentAddr, &hint)` is called and `findisatoinsertnonmolecule` runs, the new node gets address `parentAddr + Δ(depth=1)` — one tumbler component beyond the parent. If parent is `1.0.1`, the first child node/account gets `1.0.1.0.1`. The second child would get `1.0.1.0.2`. These are just arithmetic positions in the global address space; there is no pointer from parent to child stored anywhere.

---

### 4. Finding Children Requires a Range Scan, Not a Pointer Walk

`fetchorglgr` (`granf2.c:22-81`) retrieves the orgl for a known exact address using `retrievecrums`:

```c
typeorgl fetchorglgr(typetask *taskptr, typegranf fullcrumptr, typeisa *address)
{
    ...
    if ((context = retrievecrums ((typecuc*)fullcrumptr, address, WIDTH)) == NULL)
        return NULL;

    if (!tumblereq((tumbler*)&context->totaloffset, address)) {
        crumcontextfree(context);
        return (NULL);    // ← exact match required
    }
    ...
}
```

An exact address match is required. There is no "give me all entries under prefix X" operation in the retrieval interface — `retrievecrums` looks up one specific address. To enumerate all accounts under a node, one would need to range-scan `granf` for the node's prefix interval (from `nodeAddr` to `nodeAddr + 1` in tumbler arithmetic). No such enumeration function is called at node/account creation time, and no index is maintained to avoid it.

---

### 5. Why POOM, Not a Dedicated Node Structure?

The architecture is uniform: **every orgl in `granf` is a POOM**, regardless of whether it belongs to a node, account, document, or link. The `GRANORGL` bottom-crum type (`granf2.c:119`) holds an `orglptr` pointing to a POOM enfilade. There is no `GRANNODE` or `GRANACCOUNT` bottom-crum type. Nodes and documents are structurally identical in storage — they differ only in how they were addressed (via `NODE,NODE` hint vs. `ACCOUNT,DOCUMENT` hint) and in whether content was subsequently inserted into their POOM.

---

### Conclusion

The node→account relationship is **entirely implicit in the tumbler prefix convention**. There is no dedicated node-level orgl that indexes accounts. Creating a node allocates an empty POOM orgl stored in `granf` at the node's address (identical to what document creation does), but nothing writes a child list into that POOM. The sole structural fact encoding the relationship is that a child account's tumbler address begins with the parent node's tumbler address — a pure arithmetic convention enforced at allocation time by `findisatoinsertnonmolecule` and nowhere else.

---

## Question 13 [gregory]

> Does the node's tumbler prefix propagate into I-address space — i.e., does every I-address allocated under node `1` begin with `1.`, making the node recoverable from any I-address by inspecting the first field?

### Gregory's Answer

## KB Synthesis

## Yes — With Caveats on What the KB Directly States

The KB supports a **yes** answer through inference from the allocation mechanism, though it does not state this as an explicit principle.

### The Structural Argument

The allocation mechanism always creates new addresses as **children** of their parent, and "child" means **prefix containment** [SS-TUMBLER-CONTAINMENT]:

> "Containment of address A under prefix B is checked by truncating A to the length of B and comparing for equality."

Every allocation — documents, link orgls, text atoms — is bounded to a parent address:

- **Documents** under account `1.1.0.1` → allocates `1.1.0.1.0.1`, `1.1.0.1.0.2`, ... [SS-ADDRESS-ALLOC]
- **Link orgls** under document `1.1.0.1.0.1` → allocated at `1.1.0.1.0.1.0.2.1`, `1.1.0.1.0.1.0.2.2`, ... [SS-ADDRESS-SPACE/Finding 0065]
- **Text content** under document `1.1.0.1.0.1` → allocated at `1.1.0.1.0.1.3.0.1.1`, `1.1.0.1.0.1.3.0.1.2`, ... [SS-ADDRESS-SPACE/Finding 0077]

Since the allocator enforces `allocated ⊆ children(parent)` recursively all the way up to the node, every I-address in node `1`'s subtree begins with `1.`. The node is recoverable from any I-address by inspecting the first digit.

### Concrete Confirmation

Finding 0077 shows both document addresses and content I-addresses sharing the same node prefix:

```
1.1.0.1           (account under node 1)
├── 1.1.0.1.0.1   (document)
└── 1.1.0.1.0.1.3.0.1.1   (text I-address for that document)
```

Finding 0065 shows the same for link orgls: document `1.1.0.1.0.1` → link at `1.1.0.1.0.1.0.2.1`.

### The Two-Sort Distinction Does Not Contradict This

Finding 0009 notes permascroll I-addresses like `2.1.0.5.0.123` vs. link ISAs like `1.1.0.1.0.2`. This is not a special "permascroll node" — it reflects that the permascroll content was allocated under a document in the `2.x` account namespace. The `2` prefix comes from the owning account being under node 2, not from a separate permascroll region.

### What the KB Does Not State

The KB never explicitly asserts "the node is recoverable from any I-address by inspecting the first field" as a design principle. This is derivable from [SS-TUMBLER-CONTAINMENT] + [SS-ADDRESS-ALLOC], but the `findisatoinsertmolecule` / `findisatoinsertnonmolecule` code is documented as operating by prefix-bounded search — the node invariant is structural, not explicitly named.

**Summary:** Yes — the tumbler address hierarchy is strictly self-similar. Allocation is always prefix-contained, so the node prefix propagates into all descendant I-addresses. The node (and full containing path) is recoverable from any I-address by prefix truncation using the containment predicate in [SS-TUMBLER-CONTAINMENT].

---

## Code Exploration

Now I have everything needed for a complete, citation-backed answer.

---

## Does the node's tumbler prefix propagate into I-address space?

**Yes, unambiguously.** Every I-address allocated under node `1` begins with `1.`, and the node is recoverable from any I-address by inspecting `isa->mantissa[0]` (or `tumblertruncate(isa, tumblerlength(node_isa), &node)` for a multi-digit node address).

---

### 1. Tumbler encoding: printed fields map directly to mantissa slots

`common.h:53–64` defines the tumbler as a 16-slot `tdigit mantissa[NPLACES]` array. `put.c:26–46` (`puttumbler`) confirms the wire format:

```c
// put.c:41–45
for(i = 0; i <= place; ++i) {
    putnum(outfile, tumblerptr->mantissa[i]);
    if (i < place)
        putc('.', outfile);
}
```

Each dot-separated field in printed notation is exactly one mantissa slot. There are no hidden separators. The address `1.1.0.1.0.1` is stored as `mantissa = [1, 1, 0, 1, 0, 1, 0, ...]`.

---

### 2. `tumblerincrement` always creates a proper child

`tumble.c:599–623`:

```c
int tumblerincrement(tumbler *aptr, INT rightshift, INT bint, tumbler *cptr)
{
    // copies aptr to cptr first
    for (idx = NPLACES; aptr->mantissa[--idx] == 0 && idx > 0;);
    cptr->mantissa[idx + rightshift] += bint;   // [line 621]
    tumblerjustify(cptr);                        // [line 622]
}
```

For a non-zero `aptr`: finds the index `idx` of the last non-zero mantissa slot, then adds `bint` at `idx + rightshift`. The original content of `aptr` is untouched at positions 0..idx; the increment lands at `idx + rightshift`. **`aptr` is always a strict prefix of the result.**

Example: `tumblerincrement(1.1.0.1, rightshift=2, bint=1)` → `idx=3`, writes `1` at position `5` → `1.1.0.1.0.1`. ✓

---

### 3. All non-molecule allocation preserves the parent prefix

`granf2.c:203–242` (`findisatoinsertnonmolecule`), for creating nodes, accounts, and documents:

**When nothing yet exists under the hint** (lines 235–237):
```c
if (iszerotumbler(&lowerbound) || !lowerbound_under_hint) {
    tumblerincrement(&hintptr->hintisa, depth, 1, isaptr);
```
New ISA = `hintisa` with `depth` extra levels appended. Direct child, inherits entire prefix.

**When prior content exists** (lines 239–240):
```c
tumblertruncate(&lowerbound, hintlength + depth, isaptr);
tumblerincrement(isaptr, tumblerlength(isaptr)==hintlength ? depth : 0, 1, isaptr);
```
`lowerbound` has already been verified to begin with `hintisa`; truncating and incrementing preserves the prefix.

**Explicit cross-account guard** (lines 228–233):
```c
lowerbound_under_hint = FALSE;
if (!iszerotumbler(&lowerbound)) {
    tumblertruncate(&lowerbound, hintlength, &truncated);
    lowerbound_under_hint = tumblereq(&truncated, &hintptr->hintisa);
}
```
If the best lower-bound candidate belongs to a *different* account/node (e.g., searching under `1.1.0.2` finds `1.1.0.1.0.1`), it is rejected and treated as "nothing found." This prevents cross-contamination. The comment names it **BUG FIX #2** [granf2.c:224–226].

---

### 4. Molecule (text and link atom) allocation also preserves the prefix

`granf2.c:158–181` (`findisatoinsertmolecule`). In the case where the document's GRANORGL is the only existing lower bound (equal lengths):
```c
// lines 165–167
tumblerincrement(&lowerbound, 2, hintptr->atomtype, isaptr);
tumblerincrement(isaptr, 1, 1, isaptr);
```
Both steps append to `lowerbound` (which equals `hintisa` = the document ISA), so the result inherits the full document prefix.

In the case where a prior text ISA exists:
```c
// line 169
tumblerincrement(&lowerbound, 0, 1, isaptr);
```
Increments the last digit of `lowerbound`, which already started with the document prefix. Result: same prefix + 1.

---

### 5. The call chain: root node → account → document → atom

Every allocation call traces back through these `makehint` invocations:

| Call site | Hint construction | `depth` |
|-----------|-------------------|---------|
| `do1.c:251` `docreatenode_or_account` | `makehint(NODE, NODE, 0, parentNodeIsa, &hint)` | 1 |
| `do1.c:239` `docreatenewdocument` | `makehint(ACCOUNT, DOCUMENT, 0, &taskptr->account, &hint)` | 2 |
| `do1.c:271` `docreatenewversion` (same owner) | `makehint(DOCUMENT, DOCUMENT, 0, existingDoc, &hint)` | 1 |
| `do1.c:275` `docreatenewversion` (cross-owner) | `makehint(ACCOUNT, DOCUMENT, 0, wheretoputit, &hint)` | 2 |
| `do1.c:117` `doinsert` | `makehint(DOCUMENT, ATOM, TEXTATOM, docisaptr, &hint)` | — (molecule) |
| `do1.c:207` `docreatelink` | `makehint(DOCUMENT, ATOM, LINKATOM, docisaptr, &hint)` | — (molecule) |

`depth` is computed as `granf2.c:209`: `depth = hintptr->supertype == hintptr->subtype ? 1 : 2`.

At each step the new address extends the parent's address, never breaks away from it.

---

### 6. Empirical confirmation from golden tests

`golden/versions/version_address_allocation.json` records actual backend output with `DEFAULT_ACCOUNT = Address(1, 1, 0, 1)` (`febe/generate_golden.py:17`):

```
Account (pre-set):        1.1.0.1        ← mantissa[0]=1
Document 1:               1.1.0.1.0.1   ← mantissa[0]=1
Document 2:               1.1.0.1.0.2   ← mantissa[0]=1
Version of doc1:          1.1.0.1.0.1.1 ← mantissa[0]=1
Second version of doc1:   1.1.0.1.0.1.2 ← mantissa[0]=1
Version of version:       1.1.0.1.0.1.1.1 ← mantissa[0]=1
```

Every address at every depth begins with `1.`. The first mantissa field equals `1` throughout.

---

### 7. Recovering the node from any I-address

Because `tumblerincrement` always appends beyond the parent, the parent ISA is recoverable as a prefix:

```c
// Recover node from any ISA:
tumblertruncate(isa, tumblerlength(&node_isa), &recovered_node);
// recovered_node == node_isa by construction
```

For the specific case of root node `1` (a single-field tumbler), this reduces to reading `isa->mantissa[0]` — no truncation needed. The account-ownership check in `tumbleraccounteq` (`tumble.c:38–70`) relies on exactly this property: it scans the mantissa comparing field-by-field until the account address's trailing zeros signal its end, confirming prefix containment.

---

### Summary

**Yes.** The node prefix propagates into I-address space by design, not accident. `tumblerincrement` physically encodes parent-child by appending slots to the existing mantissa. `findisatoinsertnonmolecule` enforces this with an explicit "is lowerbound under hint?" guard. The entire allocation call chain from `doinsert` / `docreatenewdocument` / `docreatelink` preserves the chain back to the originating node. The first mantissa field of any I-address identifies its root node, and `tumblertruncate(isa, nodelen)` recovers the full node ISA.

---

## Question 14 [gregory]

> Are the granfilade and spanfilade per-node structures (one pair per node) or single global structures that contain entries from all nodes, distinguished only by their tumbler prefixes?

### Gregory's Answer

## KB Synthesis

**Single global structures, distinguished by tumbler prefixes.**

There is exactly one `granf` and one `spanf` for the entire running system. [SS-DUAL-ENFILADE]

From initialization:

```c
granf = createenf(GRAN);   // one global content/structure enfilade
spanf = createenf(SPAN);   // one global link search index
```

`corediskout.c:21-22` declares these as global variables; `entexit.c:44-45` creates them once at startup. [SS-DUAL-ENFILADE, Finding 0012]

**What's in each:**

- **granf** — everything: the permascroll (text atoms at `2.x.x.x` I-addresses), all document orgls, all link orgls, and the V→I mappings for every document. All of it in one tree. [SS-GRANF-OPERATIONS]

- **spanf** — one global link search index: DOCISPAN entries (I-address → document) and link endset entries (I-address → link ISA) for the entire system. [SS-SPANF-OPERATIONS]

**Separation is by tumbler prefix, not by structure.** Document 1.1.0.1.0.1's content lives at I-addresses like `1.1.0.1.0.1.3.x.x`. Document 1.1.0.1.0.2's content lives at `1.1.0.1.0.2.3.x.x`. Allocation for a document is bounded by searching the global granfilade tree within that tumbler range via `findpreviousisagr` with an upper-bound constraint. [SS-ADDRESS-ALLOC, SS-ADDRESS-SPACE Finding 0077]

**POOMs are different.** Each document has its own per-document POOM enfilade tree (the V→I mapping structure). These are separate enfilade trees, typed `POOM` in their disk block headers, accessed via the document's orgl in the granfilade. They live in the same `enf.enf` disk file alongside GRAN and SPAN blocks, but each is a distinct tree rooted at its document's orgl. [SS-UNIFIED-STORAGE, SS-POOM-MUTABILITY]

So: granfilade = one global tree, spanfilade = one global tree, POOMs = one per document.

---

## Code Exploration

Now I have everything needed. Here is the full answer:

---

## Answer: Granfilade and Spanfilade Are Single Global Structures

Both `granf` and `spanf` are **single global structures** — there is exactly one of each for the entire system. They are not per-node or per-document structures. All content from all documents and all links live inside these two global trees, distinguished by their tumbler addresses.

---

### 1. There Are Exactly Two Globals

In `xanadu.h`:

```c
// xanadu.h:13-16
#define typegranf INT *   /* temp -- INT for alignment */
extern typegranf granf;       
#define typespanf INT *   /* temp -- INT for alignment */
extern typespanf spanf;
```

These are declared as global `extern` variables — one pointer per filade type. The actual definitions live in `corediskout.c`:

```c
// corediskout.c:21-22
typegranf granf;
typespanf spanf;
```

### 2. They Are Created Once at Startup

In `entexit.c:41-46`, during `initmagicktricks()`, the system either loads them from disk or creates them fresh:

```c
if (initenffile()) {
    initkluge ((typecuc**)&granf, (typecuc**)&spanf);
} else {
    granf = (typegranf) createenf (GRAN);
    spanf = (typespanf) createenf (SPAN);
}
```

`createenf(GRAN)` and `createenf(SPAN)` each create a single enfilade root node. The `cenftype` field in every crum's header (`enf.h:34`) is set to one of `GRAN=1`, `POOM=2`, or `SPAN=3` — so every node in the tree carries a type tag, but the tree itself is singular.

### 3. Every Operation Passes the Global Root

Throughout `do1.c`, every document operation passes the same global `granf` or `spanf` root:

- `do1.c:40` — `findorgl(taskptr, granf, docisaptr, &docorgl, WRITEBERT)`
- `do1.c:55` — `findorgl(taskptr, granf, docisaptr, &docorgl, WRITEBERT)`
- `do1.c:62` — `insertspanf(taskptr, spanf, docisaptr, ispanset, DOCISPAN)`
- `do1.c:118` — `inserttextingranf(taskptr, granf, &hint, textset, &ispanset)`
- `do1.c:182` — `createorglingranf(taskptr, granf, &hint, linkisaptr)`
- `do1.c:191` — `insertendsetsinspanf(taskptr, spanf, linkisaptr, ...)`
- `do1.c:240` — document creation: `createorglingranf(taskptr, granf, &hint, isaptr)`

There is no per-document or per-node `granf` / `spanf` pointer — it is always the one global.

### 4. Tumbler Prefixes Are How All Content Is Distinguished

Since the filade is a tumbler-keyed tree, **every entry in the granfilade is distinguished purely by its ISA (Internal Storage Address)**, which is a tumbler. The `typehint` structure passed to insert functions encodes the addressing hierarchy (ACCOUNT → DOCUMENT → ATOM) — but all these addresses live in the same tree.

For example, `insertspanf` in `spanf1.c:22` does:

```c
prefixtumbler(isaptr, spantype, &crumorigin.dsas[ORGLRANGE]);
```

This prefixes the link's ISA with the span type (`LINKFROMSPAN=1`, `LINKTOSPAN=2`, `LINKTHREESPAN=3`, `DOCISPAN=4`) to create the 2D key for the entry in the single global `spanf` tree. All links and documents coexist in `spanf`, separated only by their tumbler prefixes.

Similarly, `granf2.c:34` retrieves an orgl by calling `retrievecrums((typecuc*)fullcrumptr, address, WIDTH)` — where `fullcrumptr` is always the same global root, and `address` is a tumbler that uniquely identifies the entry within the tree.

### 5. Per-Document Version Trees (POOMs) Are Subtrees of `granf`

Each document or link does get its own POOM (the version tree, type `POOM`) — but this POOM is stored **as a leaf entry inside `granf`**, not as a separate parallel structure. In `granf2.c:120`:

```c
locinfo.granstuff.orglstuff.orglptr = createenf(POOM);
insertseq((typecuc*)fullcrumptr, isaptr, &locinfo);
```

The POOM is created and then inserted as a bottom crum's payload into `granf` at the document's ISA address. `fetchorglgr` in `granf2.c:34` retrieves it again by calling `retrievecrums` on the global `granf` root with the document's tumbler address.

---

### Summary

| Structure | Count | Distinguished by |
|-----------|-------|-----------------|
| `granf` (granfilade) | 1 global | Tumbler ISA address per document/link/text-atom |
| `spanf` (spanfilade) | 1 global | 2D (ORGLRANGE × SPANRANGE) tumbler key, ORGLRANGE prefix = span type (1–4) |
| POOM per document | Many, but embedded as payloads inside `granf` bottom crums | ISA address within `granf` |

There is one granfilade and one spanfilade for the entire server process. Content from all documents is interleaved within each, navigable only via tumbler arithmetic.

---

## Question 15 [gregory]

> What defines the boundary of a node's address range — is there an explicit upper-bound tumbler stored somewhere, or does the node own everything matching its prefix with no mechanism to prevent another node's addresses from colliding in the same enfilade?

### Gregory's Answer

## KB Synthesis

The boundary is implicit and computed on demand — there is no explicit upper-bound tumbler stored in any node structure.

## What defines a node's address range

**Prefix convention, not stored bounds.** A node "owns" all tumblers whose leading digits match its own address prefix. This is the `tumblertruncate` + `tumblereq` predicate described in [SS-TUMBLER-CONTAINMENT]: truncate candidate to the length of the prefix, compare for equality. Ownership is a property of the tumbler digit sequence, not a field in the node record.

**The upper bound is computed dynamically.** [SS-ADDRESS-ALLOC] (Finding 0021) shows the allocation algorithm computing `upperbound = tumblerincrement(hintisa, depth-1, 1)` — the next sibling of the parent — as a search fence for `findpreviousisagr`. This bound is created fresh at allocation time and discarded afterward. Nothing stores it.

**The flat granfilade has no inherent hierarchy.** [SS-UNIFIED-STORAGE] / [SS-ENFILADE-TREE] (Finding 0059) confirm that all addresses — documents, versions, content atoms, link orgls — are interleaved in a single flat B-tree (`enf.enf`). The tree treats every tumbler uniformly; there is no structural partitioning by namespace or depth.

## Bug 0013 is the proof

[PRE-ADDRESS-ALLOC] (Finding 0021) documents the critical evidence: the original allocation code, without an explicit containment check, crossed account boundaries. When allocating under account `1.1.0.2`, `findpreviousisagr` found `1.1.0.1.0.1` (under a different account) and incremented to `1.1.0.1.0.2` — a wrong-account address. The tree structure did nothing to prevent this.

The fix added a post-search containment check: after `findpreviousisagr` returns a candidate, verify it is actually under the target parent via prefix matching. Without this application-level guard, the flat tree provides no boundary enforcement at all.

## Summary

| Mechanism | Stored? | Where? |
|-----------|---------|--------|
| Lower bound (node address itself) | Yes | In the granfilade as the node's own tumbler |
| Upper bound | No | Computed as `tumblerincrement(parent, depth-1, 1)` at allocation time |
| Boundary enforcement | No | Pure application-level convention; the B-tree is oblivious |
| Collision prevention | No structural | Monotonic allocation + post-search containment check |

The hierarchy is an invariant maintained by the allocation algorithm [SS-ADDRESS-ALLOC], not an intrinsic property of the storage structure. The enfilade's job is to find the highest address below an upper bound — defining that upper bound correctly is entirely the caller's responsibility.

---

## Code Exploration

I have everything I need. Here is the complete answer.

---

## What Defines the Boundary of a Node's Address Range

The short answer: **there is no stored upper-bound tumbler**. A node's range is defined by two stored fields — `cdsp` (lower origin) and `cwid` (extent) — with the upper bound computed on the fly as `cdsp + cwid`. But the semantics differ sharply between GRAN and SPAN/POOM enfilades, and only GRAN has a structural guarantee against collision.

---

### The Stored Fields

Every crum, regardless of type, carries two fields in `structcorecrumhedr` [enf.h:47-48]:

```c
typewid cwid;
typedsp cdsp;
```

Both `typewid` and `typedsp` are aliases for `typewisp`, which is `struct { tumbler dsas[MAXLOXIZE]; }` [wisp.h:50-55]. So a node stores a lower origin and an extent — nothing else.

---

### GRAN (Sequential) — Implicit Range via Accumulated Offsets

The crucial note is in wisp.h [lines 28-32]:

```
**        Note that dsp's of gr are not stored on crums
**          themselves, but are discovered thru tree walking
```

For GRAN enfilades, `cdsp` is not meaningful as an absolute position. The left boundary of any node is the running sum of its preceding siblings' `cwid`s, accumulated while walking the sibling list. In `whereoncrum()` [retrie.c:351-353]:

```c
case GRAN:
   tumbleradd (&offset->dsas[WIDTH], &ptr->cwid.dsas[WIDTH], &right);
   return (intervalcmp (&offset->dsas[WIDTH], &right, address));
```

`offset` is the accumulated sibling sum passed down through recursion. `right = offset + cwid`. Left = `offset`. No stored upper bound.

The caller in `findcbcseq` [retrie.c:195-198] advances the offset across siblings:

```c
for (; getrightbro (ptr); ptr = ptr->rightbro) {
    if (whereoncrum (ptr, offsetptr, address, WIDTH) <= THRUME)
        break;
    dspadd (offsetptr, &ptr->cwid, offsetptr, (INT)ptr->cenftype);
}
```

Each node it steps past adds its `cwid` to the running offset before checking the next sibling. This is the boundary mechanism for GRAN — entirely implicit, accumulated during traversal.

**Is collision possible in GRAN?** No, by construction. `setwidseq()` [wisp.c:150-168] maintains the invariant that a parent's `cwid` = sum of all children's `cwid`s:

```c
clear (&sum, sizeof (sum));
for (ptr = findleftson (father); ptr; ptr = getrightbro (ptr)) {
    widopseq (&sum, &ptr->cwid, &sum);
}
movewisp (&sum, &father->cwid);
```

Since siblings partition the parent's width additively, their ranges cannot overlap as long as `cwid`s are correct. `setwispupwards()` [wisp.c:83-111] propagates any change upward to the root after every structural modification.

---

### SPAN/POOM (2D) — Explicit `cdsp` + `cwid` Bounding Box

For 2D enfilades, each node does use `cdsp` as an explicit coordinate offset from the parent's origin. In `whereoncrum()` [retrie.c:354-373]:

```c
case SPAN:
case POOM:
    tumbleradd(&offset->dsas[index], &ptr->cdsp.dsas[index], &left);
    tumbleradd (&left, &ptr->cwid.dsas[index], &right);
    /* then compare address against [left, right) */
```

Left = parent_accumulated_offset + `cdsp`. Right = left + `cwid`. The upper bound is computed, never stored.

`setwispnd()` [wisp.c:171-228] maintains this by computing the tightest bounding box over all children after any structural change:

```c
/* find new upper-left corner: minimum cdsp across all children */
movewisp (&ptr->cdsp, &mindsp);
for (ptr = getrightbro(ptr); ptr; ptr = getrightbro (ptr))
    lockmin (&mindsp, &ptr->cdsp, &mindsp, ...);

/* find lower-right corner: max(cdsp + cwid) across all children */
for (ptr = findleftson (father); ptr; ptr = getrightbro (ptr)) {
    lockadd(&ptr->cdsp, &ptr->cwid, &tempwid, ...);
    lockmax(&newwid, &tempwid, &newwid, ...);
}
father->cdsp = newdsp;
father->cwid = newwid;
```

**Is collision possible in SPAN/POOM?** Yes, and it is expected. There is no mechanism that enforces sibling non-overlap. The retrieval code in `findcbcinarea2d()` [retrie.c:252-265] is written to handle this — it iterates over all siblings and descends into every qualifying one:

```c
for (; crumptr; crumptr = getrightbro (crumptr)) {
    if (!crumqualifies2d (crumptr, ...)) continue;
    if (crumptr->height != 0) {
        findcbcinarea2d (findleftson(crumptr), ...);  // descend ALL matching
    } else {
        context = makecontextfromcbc(...);
        incontextlistnd (headptr, context, index1);   // collect all results
    }
}
```

Multiple results are not a bug — the ND enfilade is explicitly multi-valued. The `cwid` bounding-box check in `crumqualifies2d()` [retrie.c:270-305] is a filter to prune dead branches, not a collision guard.

---

### Summary

| | GRAN | SPAN/POOM |
|---|---|---|
| Left boundary stored? | No — accumulated from sibling walk | Yes — `cdsp` offset from parent |
| Right boundary stored? | No — computed as `offset + cwid` | No — computed as `cdsp + cwid` |
| Upper-bound tumbler? | **None** | **None** |
| Collision possible? | No (additive partition invariant) | Yes (bounding-box, not partition) |
| Retrieval model | First match wins | All matches collected |

There is no explicit upper-bound stored anywhere. For GRAN, collision is structurally impossible because `setwidseq` keeps parent.cwid = sum(children.cwid), making siblings tile exactly. For SPAN/POOM, sibling ranges can overlap and retrieval is designed to collect all matching bottom crums rather than to enforce uniqueness.

---

## Question 16 [gregory]

> When `findisatoinsertmolecule` or `findisatoinsertnonmolecule` searches for the current maximum I-address, does the search scope itself to the node's address range, or does it walk the entire granfilade and rely on hierarchical tumbler sorting to land in the right region?

### Gregory's Answer

## KB Synthesis

Both functions use an **upper-bound constraint** passed to `findpreviousisagr` — the search is bounded, not a global walk.

The mechanism, from [SS-ADDRESS-ALLOC] (Finding 0021):

1. Compute `upperbound = tumblerincrement(hintisa, depth-1, 1)` — this is the *next sibling* of the parent address. For a parent at `1.1.0.1.0.1`, upperbound is `1.1.0.1.0.2`.
2. Call `findpreviousisagr(upperbound)` — finds the highest existing address in the granfilade **strictly below** that bound.
3. Verify the found address actually falls under the parent via tumbler containment check (added to fix Bug 0013, per [PRE-ADDRESS-ALLOC]).
4. If nothing is under the parent: allocate first child at `hintisa.0.1`. Otherwise: truncate-and-increment the found address.

The same pattern holds for `findisatoinsertmolecule` (content allocation), per [SS-ADDRESS-ALLOC] Finding 0065:

> `tumblerincrement(&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound)` sets document-scoped bound — e.g., upper bound `docISA.2.3` for link allocation within document `docISA`.

So the scoping is **arithmetic**, not structural. The granfilade is a single flat B-tree containing all addresses — document orgls, text atoms, link orgls, version addresses — all interleaved. There is no separate subtree per namespace [SS-ADDRESS-SPACE] Finding 0077:

> Both query the same granfilade tree but search different subtrees [via different upper bounds].

The B-tree traversal in `findpreviousisagr` uses the upper bound to descend into the correct region — it relies on the total tumbler order ([INV-TUMBLER-TOTAL-ORDER]) to efficiently find the maximum below the bound. But without the containment check, the search *can* return an address from an adjacent namespace (the original Bug 0013: searching under account `1.1.0.2` found `1.1.0.1.0.1` because it was the highest address below the computed upper bound, even though it belonged to a different account). The fix added an explicit `tumblertruncate`/`tumblereq` containment check after `findpreviousisagr` returns. [PRE-ADDRESS-ALLOC], [SS-TUMBLER-CONTAINMENT]

---

## Code Exploration

I now have a complete picture. Here is the full answer.

---

## How `findisatoinsertmolecule` / `findisatoinsertnonmolecule` Scope Their Search

**Short answer: neither function scopes itself to the node's address range. Both walk the entire granfilade from the root and rely on hierarchical tumbler sorting—guided by a computed `upperbound`—to land in the right region. Scoping is implicit, not explicit, and can fail (as Bug Fix #2 in the code documents).**

---

### The Core Primitive: `findpreviousisagr`

Both functions delegate the actual search to `findpreviousisagr` [`granf2.c:255–278`]:

```c
int findpreviousisagr(typecorecrum *crumptr, typeisa *upperbound, typeisa *offset)
{
    if (crumptr->height == 0) {
        findlastisaincbcgr ((typecbc*)crumptr, offset);   // leaf: store the last I-addr here
        return(0);
    }
    for (ptr = findleftson((typecuc*)crumptr); ptr; ptr = findrightbro(ptr)) {
        if (
         (tmp= whereoncrum (ptr, (typewid*)offset, upperbound, WIDTH)) == THRUME
        || tmp == ONMYRIGHTBORDER
        || !ptr->rightbro) {
            findpreviousisagr (ptr, upperbound, offset);   // recurse DOWN
            return(0);
        } else {
            tumbleradd(offset, &ptr->cwid.dsas[WIDTH], offset);  // skip this child
        }
    }
}
```

`crumptr` is always the **apex of the full granfilade**, passed down unchanged from the callers (`inserttextgr` [`granf2.c:83–109`] and `createorglgr` [`granf2.c:111–128`]), which both receive it directly as the `fullcrumptr` argument. There is no subtree-scoping step before the call.

The traversal:

1. Iterates through child nodes left-to-right at each level.
2. For each child, calls `whereoncrum` [`retrie.c:345–398`] to compare `upperbound` against the child's I-address interval `[offset, offset + node_width)`. The five results are `TOMYLEFT (-2)`, `ONMYLEFTBORDER (-1)`, `THRUME (0)`, `ONMYRIGHTBORDER (1)`, `TOMYRIGHT (2)` [`common.h:86–90`].
3. If `upperbound` is **within** the child (`THRUME`), **at its right boundary** (`ONMYRIGHTBORDER`), or the child is the **last sibling** (`!ptr->rightbro`), it recurses into that child.
4. Otherwise it adds the child's width to `offset` and moves right.

This is a pure **enfilade descent guided by a target address**. The tree is sorted by I-address; following `upperbound` down the tree routes to the rightmost leaf at or before that bound. No address-range guard is applied to the root call or at any level.

---

### How Each Caller Computes `upperbound`

#### `findisatoinsertmolecule` [`granf2.c:158–181`]

Called for `ATOM` types (text and links inside a document). The upper bound is:

```c
tumblerincrement (&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound);
```

`tumblerincrement(a, rightshift, bint, c)` [`tumble.c:599–623`] finds the last non-zero digit of `a` and adds `bint` at `rightshift` positions further right. So for a document at address `D` with `atomtype = TEXTATOM (1)`:

- `upperbound = D.0.0.(TEXTATOM+1)` = one unit past the last possible text-atom address under this document.

`findpreviousisagr` then descends the entire granfilade following this bound, and returns whatever leaf I-address it hits. No explicit check confirms the result falls under document `D`. The correctness relies entirely on the tumbler ordering placing all of `D`'s atoms strictly below `upperbound`, and nothing from a *different* document being between `D`'s last atom and `upperbound`.

#### `findisatoinsertnonmolecule` [`granf2.c:203–242`]

Called for non-atom types (DOCUMENT, ACCOUNT, NODE). The upper bound is:

```c
depth = hintptr->supertype == hintptr->subtype ? 1 : 2;
tumblerincrement (&hintptr->hintisa, depth - 1, 1, &upperbound);
```

For the common case (depth=2, e.g., creating a document under an account at `A`), this is `A.0.1` — one level to the right of `A`'s direct child space, i.e., just past all of `A`'s direct children.

Again, `findpreviousisagr` descends from the root following this bound with no hard scope guard.

---

### The Proof That Scoping Is Not Enforced: Bug Fix #2

The code itself documents the failure mode. In `findisatoinsertnonmolecule` [`granf2.c:219–233`]:

```c
/* BUG FIX #2: Also check if lowerbound is actually under hintisa. If the
   found item is from a different account (e.g., 1.1.0.1.0.1 when creating
   under 1.1.0.2), treat it as if nothing was found. Otherwise documents
   get created under the wrong account. */
lowerbound_under_hint = FALSE;
if (!iszerotumbler(&lowerbound)) {
    tumblertruncate(&lowerbound, hintlength, &truncated);
    lowerbound_under_hint = tumblereq(&truncated, &hintptr->hintisa);
}
if (iszerotumbler(&lowerbound) || !lowerbound_under_hint) {
    /* Nothing under this hint - create first child as hintisa.0.1 */
    tumblerincrement(&hintptr->hintisa, depth, 1, isaptr);
} else { ...
```

When creating a document under account `1.1.0.2`, `findpreviousisagr` (starting from the root) could return `1.1.0.1.0.1` — the last document under a *different* account — because that is the rightmost item below `upperbound = 1.1.0.2.0.1`. The post-search truncate-and-compare guard was added specifically because the tree walk does not stay within the hint's subtree.

**`findisatoinsertmolecule` has no equivalent post-search check.** It relies purely on `upperbound` arithmetic being tight enough to exclude other documents' atoms.

---

### Summary

| Function | Starting point | Scope guard | Relies on |
|---|---|---|---|
| `findpreviousisagr` | Root of full granfilade | None | Tumbler total order |
| `findisatoinsertmolecule` | (via above) | None | `upperbound` arithmetic |
| `findisatoinsertnonmolecule` | (via above) | Explicit post-search `lowerbound_under_hint` check | `upperbound` + explicit verification |

The search is a **whole-tree descent guided by an `upperbound`**, not a scoped subtree walk. The hierarchical tumbler sort causes the descent to naturally route toward the target region, but this is an emergent property of the address ordering — not an explicit scope constraint on the traversal. The `findisatoinsertnonmolecule` bug fix is direct evidence that this reliance on ordering alone is insufficient when the target region is empty.

---

## Question 17 [gregory]

> In the original multi-node design intent, was each node expected to carry a complete copy of its own content in its local granfilade, or could a node hold granfilade entries for content originating from other nodes (e.g., after a transclusion from a remote document)?

### Gregory's Answer

## KB Synthesis

The KB cannot answer this question. The knowledge base documents the single-node udanax-green implementation and does not contain findings about the multi-node design intent for content distribution or granfilade replication policy.

What the KB does establish that bears on this question:

**Address structure implies node-scoped I-addresses.** Tumbler addresses follow the pattern `Node.0.User.0.Doc.0.Element` [SS-TUMBLER, Finding 0001]. Permascroll I-addresses in the observed system start with `2.1.0.x...`, distinct from document orgl addresses under `1.1.0.x...`. The addressing scheme is hierarchical, but the KB does not explain whether the leading digits of I-addresses encode node identity such that a remote I-address would be distinguishable from a local one.

**The granfilade holds all content for the running node.** The granfilade stores the permascroll, all document orgls, link orgls, and V→I mappings in a single `enf.enf` file [SS-UNIFIED-STORAGE, Finding 0059]. There is no mechanism in the KB for fetching content from a remote granfilade — all I-address resolution (`findorgl`, `retrieverestricted`, `ispanset2vstuffset`) assumes content is locally present.

**I-address allocation is local and stateless.** `findisatoinsertmolecule` queries the local granfilade tree to find the highest existing I-address and increments [SS-ADDRESS-SPACE, Finding 0061]. There is no inter-node coordination in the allocation path.

**Transclusion assumes local content.** `docopy` [SS-DUAL-ENFILADE, Finding 0012] places I-spans directly into the destination document's POOM. Whether those I-addresses could reference content held on a remote node's granfilade — and whether the receiving node would cache a copy locally — is not addressed anywhere in the KB.

If you have EWD papers or Nelson's design documents describing the multi-node distribution model, those would be the right source. The KB only captures what the udanax-green C source demonstrates about the single-daemon implementation.

---

## Code Exploration

Now I have enough to compose a definitive answer from the code.

---

## Multi-Node Content in Udanax-Green: What the Code Actually Shows

The answer is **yes — a node's spanfilade and POOM could hold entries for content originating from other documents, potentially on other nodes.** The design is explicit and deliberate. Here is the evidence.

---

### 1. The SPORGL Item Type Is the Cross-Document Reference

`xanadu.h:115–121` defines the critical struct:

```c
typedef struct structsporgl{
    struct structsporgl *next;
    typeitemid  itemid;
    tumbler sporglorigin;   // where in I-space the transcluded content starts
    tumbler sporglwidth;    // how wide it is
    typeisa sporgladdress;  // the ISA of the source (home) document
} typesporgl;
```

A SPORGL is not local text. It is a pointer into another document's I-space, carrying the address of the source document in `sporgladdress`. A `typesporglset` (xanadu.h:127) is a heterogeneous list that can mix local `ISPANID` items and cross-document `SPORGLID` items.

---

### 2. Every 2D Crum Records Its Home Document

`wisp.h:107–109`:

```c
typedef struct struct2dbottomcruminfo {
    tumbler homedoc;
} type2dbottomcruminfo;
```

Every bottom-level crum in a spanfilade or POOM carries a `homedoc` tumbler. This is the provenance stamp: the ISA of the document that owns this particular content entry.

---

### 3. `insertspanf` Writes Cross-Document Provenance at Insertion Time

`spanf1.c:25–51` processes a `sporglset` and writes crums into the span file. The `homedoc` field is set based on item type:

```c
if (((typeitemheader *)sporglset)->itemid == ISPANID) {
    movetumbler (&((typeispan *)sporglset)->stream, &lstream);
    movetumbler (&((typeispan *)sporglset)->width, &lwidth);
    movetumbler (isaptr, &linfo.homedoc);            // local doc
} else if (((typeitemheader *)sporglset)->itemid == SPORGLID) {
    movetumbler (&((typesporgl *)sporglset)->sporglorigin, &lstream);
    movetumbler (&((typesporgl *)sporglset)->sporglwidth, &lwidth);
    movetumbler (&((typesporgl *)sporglset)->sporgladdress, &linfo.homedoc); // REMOTE doc
} else if (((typeitemheader *)sporglset)->itemid == TEXTID) {
    movetumbler(isaptr, &lstream);
    // ... width from length ...
    movetumbler(isaptr, &linfo.homedoc);             // local doc
}
insertnd(taskptr, (typecuc*)spanfptr, &crumorigin, &crumwidth, &linfo, SPANRANGE);
```

When the item is a SPORGL, `linfo.homedoc` is set to `sporgladdress` — the remote document's ISA — not the inserting document's ISA. That remote-provenance crum is then inserted into the local spanfilade via `insertnd`. The span file on this node now contains an entry whose `homedoc` points to a foreign document.

`unpacksporgl` (sporgl.c:187) confirms this is the intent: the comment reads `/* should be sourcedoc */`.

---

### 4. `isanextensionnd` Enforces Same-Origin Merging

`insertnd.c:301–309`:

```c
bool isanextensionnd(typecbc *ptr, typedsp *offsetptr, typedsp *originptr, type2dbottomcruminfo *infoptr)
{
    if (!tumblereq (&infoptr->homedoc, &((type2dcbc *)ptr)->c2dinfo.homedoc))
        return (FALSE);
    prologuend ((typecorecrum*)ptr, offsetptr, &grasp, &reach);
    return (lockeq (reach.dsas, originptr->dsas, (unsigned)dspsize(ptr->cenftype)));
}
```

Before the enfilade merges a new crum with an existing adjacent one, it checks that the two share the same `homedoc`. If the home documents differ (line 305), merge is refused and a new crum is created. This guarantees that content from different source documents remains **physically separated** in the tree, even when adjacent — but it is not forbidden from coexisting in the same enfilade.

---

### 5. Retrieval Filters by `homedoc` Across a Mixed Span File

`retrie.c:77–84` sets up the filter for a retrieval:

```c
if (docisaptr) {
    movetumbler(docisaptr, &info.homedoc /*shouldberestrictiondoc*/);
    infoptr = &info;
} else {
    infoptr = NULL;
}
temp = retrieveinarea(fullcrumptr, ...., (typebottomcruminfo*)infoptr);
```

`crumqualifies2d` (retrie.c:274–280) enforces it at the leaf level:

```c
if ((crumptr->height == 0) && infoptr && 
    !tumblereq(&infoptr->homedoc, &(((type2dcbc *)crumptr)->c2dinfo.homedoc))) {
    fprintf(stderr,"mumble homedoc");
    return (FALSE);
}
```

When `docisaptr` is provided, only crums whose `homedoc` matches are returned. When it is NULL, all crums — regardless of origin — are returned. The filter exists precisely *because* the span file is expected to contain entries from multiple source documents mixed together.

---

### 6. The Granfilade Itself Is Local; The Mapping Layers Are Not

There is an important distinction between the three enfilade layers:

- **Granfilade** (`granf2.c:83–109`): Stores actual byte content. `inserttextgr` allocates ISAs within the local hierarchy using `findisatoinsertgr`. The granfilade holds the raw bytes of locally-authored text. There is no `homedoc` on granfilade crums — they use `typegranbottomcruminfo`, which has no provenance field (`wisp.h:100–104`).

- **Spanfilade** and **POOM** (orglinks.c, spanf1.c): These are the *address-mapping* layers. They map virtual span addresses to I-space (granfilade) addresses. It is here that `type2dbottomcruminfo` with `homedoc` appears. These layers can and do hold entries referencing remote documents.

The granfilade belongs to a node; the spanfilade and POOM record how that node's documents are composed — including from remote sources.

---

### 7. `insertpm` Stores Cross-Document Mappings in the POOM

`orglinks.c:75–134`: `insertpm` drives POOM insertion. It calls `unpacksporgl` to extract `lstream`, `lwidth`, and `linfo` (with `linfo.homedoc` = source doc for SPORGLs), then calls `insertnd` with that info. For SPORGL items the POOM entry records a V→I mapping where the I-address belongs to a foreign document.

---

### Summary

| Layer | Contains remote content? | Evidence |
|---|---|---|
| Granfilade | No — byte storage is always local | `typegranbottomcruminfo` has no `homedoc` |
| Spanfilade | **Yes** — crums with remote `homedoc` are inserted | `spanf1.c:33`, `unpacksporgl` sporgl.c:187 |
| POOM | **Yes** — V→I mappings can point into remote I-space | `orglinks.c:101`, `insertpm` drives it |

The design is unambiguous: each node owns its own granfilade (raw text bytes are stored locally) but its spanfilade and POOM are explicitly designed to hold entries for content originating in any document — including documents on remote nodes — identified by the `sporgladdress` / `homedoc` tumbler. The `isanextensionnd` check (insertnd.c:305) and `crumqualifies2d` filter (retrie.c:274) are both *consequences* of this design: they exist to keep foreign-provenance crums from merging with local ones and to allow retrieval scoped to a single home document within the mixed tree. Transclusion from a remote node would produce exactly these cross-provenance crums, and the code is fully prepared to store and retrieve them.

---

## Question 18 [gregory]

> Is the set of valid node addresses fixed at system genesis (a finite, pre-allocated set), or can new node addresses be minted at runtime — and if so, what operation creates a new node entry?

### Gregory's Answer

## KB Synthesis

The KB does not describe a fixed, pre-allocated node address set. Node addresses are minted at runtime via the same stateless query-and-increment mechanism used for all non-molecule (structural) allocations.

**The allocation mechanism** is `findisatoinsertnonmolecule` [SS-ADDRESS-ALLOC, Finding 0021]. When allocating a node under another node, `makehint(NODE, NODE, depth=1, parent_isa, &hint)` is used. The algorithm:

1. Computes `upperbound = tumblerincrement(parent_isa, depth-1, 1)` — the next sibling of the parent
2. Calls `findpreviousisagr` to find the highest existing address under the parent
3. If none found: allocates first child as `parent.1` (e.g., `1.1.1` under node `1.1`)
4. Otherwise: truncates and increments to get the next sibling

The depth formula `depth = (supertype == subtype) ? 1 : 2` means NODE→NODE uses depth=1, producing sibling addresses without a `.0.` boundary (e.g., `1.1.0.1.1`, `1.1.0.1.2` under node `1.1.0.1`) [SS-ADDRESS-SPACE, Finding 0021].

**Runtime minting is confirmed by several invariants:**

- [INV-MONOTONIC]: All structural allocations are strictly monotonically increasing — new addresses are always added, never reused
- [INV-NO-IADDR-REUSE]: The granfilade is append-only; once an address exists, it persists permanently
- [SS-ENFILADE-TREE]: The granfilade starts empty (`createenf` produces a minimal height-1 tree), not pre-populated

**What the KB does not answer:** Whether there is a user-facing FEBE opcode for "create node" is not documented. The `makehint(NODE, NODE, ...)` case exists in the allocation dispatch, but the KB covers primarily document, link, and version creation operations. The genesis/bootstrap state (e.g., what node addresses exist at first startup) is also not described.

In summary: node addresses are **not fixed at genesis** — they follow the same demand-allocated, monotonically-growing address space as all other structural entities in the granfilade.

---

## Code Exploration

I now have everything needed from the source. Here is my complete answer.

---

## Are Node Addresses Fixed at Genesis or Minted at Runtime?

**New node addresses are minted at runtime.** There is no finite, pre-allocated address pool. Every new entry — account, document, node, link, or text span — receives a fresh tumbler computed on demand by searching the existing tree and incrementing past the highest occupied address.

---

## The Tumbler: What a "Node Address" Is

All addresses in udanax-green are **tumblers** — multi-part hierarchical numbers stored as a struct with a 16-place mantissa and an exponent:

```c
/* common.h:59-65 */
typedef struct structtumbler {
    humber xvartumbler;
    char varandnotfixed;
    char sign;
    short exp;
    tdigit mantissa[NPLACES];   /* NPLACES = 16 */
} tumbler;
```

`NPLACES` is 16 [`common.h:53`], explicitly increased from 11 "to support deeper version chains." The address space is effectively unbounded within these 16 positions.

The type hierarchy is defined as integer constants:

```c
/* xanadu.h:140-143 */
#define NODE      1
#define ACCOUNT   2
#define DOCUMENT  3
#define ATOM      4
```

A `typehint` packages the parent address and the desired type transition to guide allocation:

```c
/* xanadu.h:148-153 */
typedef struct {
    INT supertype;
    INT subtype;
    INT atomtype;
    typeisa hintisa;     /* anchor address */
} typehint;
```

---

## The Minting Call Chain

Every creation operation follows this path:

### Layer 1: FEBE operation functions (`do1.c`)

**`docreatenewdocument()`** [`do1.c:234-241`]:
```c
makehint (ACCOUNT, DOCUMENT, 0, &taskptr->account, &hint);
return (createorglingranf (taskptr, granf, &hint, isaptr));
```
The caller's account tumbler becomes the `hintisa` — the parent anchor. The returned `isaptr` is the freshly minted document address.

**`docreatenode_or_account()`** [`do1.c:243-258`]:
```c
tumblercopy(isaptr, &isa);
makehint (NODE, NODE, 0, &isa, &hint);
result = createorglingranf (taskptr, granf, &hint, &isa);
if (result) {
    tumblercopy(&isa, isaptr);
}
```
The input `isaptr` acts as the hint anchor (the parent node), and the output is the newly allocated node address.

**`docreatelink()` / `domakelink()`** [`do1.c:180-221`]:
```c
makehint (DOCUMENT, ATOM, LINKATOM, docisaptr, &hint);
createorglingranf (taskptr, granf, &hint, linkisaptr)
```
Links get addresses minted under the owning document using the ATOM subtype path.

### Layer 2: Granfilade creation (`granf2.c`)

**`createorglingranf()`** [`granf2.c:111-128`]:
```c
if (!findisatoinsertgr ((typecuc*)fullcrumptr, hintptr, isaptr))
    return (FALSE);
locinfo.infotype = GRANORGL;
locinfo.granstuff.orglstuff.orglptr = createenf (POOM);
...
insertseq ((typecuc*)fullcrumptr, isaptr, &locinfo);
```
This function does three things: (1) mint the address, (2) allocate a new enfilade structure in memory, (3) register the address→enfilade mapping in the tree.

**`findisatoinsertgr()`** [`granf2.c:130-156`] routes to the right minting sub-function:

```c
if (hintptr->subtype == ATOM) {
    findisatoinsertmolecule (fullcrumptr, hintptr, isaptr);
} else {
    findisatoinsertnonmolecule (fullcrumptr, hintptr, isaptr);
}
tumblerjustify(isaptr);
```

### Layer 3: The core mint — `findisatoinsertnonmolecule()` [`granf2.c:203-242`]

This is where the address is actually computed:

```c
depth = hintptr->supertype == hintptr->subtype ? 1 : 2;
hintlength = tumblerlength (&hintptr->hintisa);
tumblerincrement (&hintptr->hintisa, depth - 1, 1, &upperbound);
clear (&lowerbound, sizeof(lowerbound));
findpreviousisagr ((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);
```

It asks: *what is the highest existing address below `upperbound`?*

```c
/* BUG FIX comments explain the logic: */
lowerbound_under_hint = FALSE;
if (!iszerotumbler(&lowerbound)) {
    tumblertruncate(&lowerbound, hintlength, &truncated);
    lowerbound_under_hint = tumblereq(&truncated, &hintptr->hintisa);
}

if (iszerotumbler(&lowerbound) || !lowerbound_under_hint) {
    /* Nothing under this hint - create first child as hintisa.0.1 */
    tumblerincrement(&hintptr->hintisa, depth, 1, isaptr);   /* line 237 */
} else {
    tumblertruncate (&lowerbound, hintlength + depth, isaptr);
    tumblerincrement(isaptr, tumblerlength(isaptr)==hintlength?depth:0, 1, isaptr);  /* line 240 */
}
```

Two cases:
- **First child under a parent**: the new address is `hintisa` extended by `depth` zero-separators and `1` (e.g., if hint is `1.1.0.1`, new doc is `1.1.0.1.0.1`).
- **Nth sibling**: take the highest existing sibling, truncate to the appropriate prefix length, and add 1.

### Layer 4: `tumblerincrement()` [`tumble.c:599-623`]

```c
int tumblerincrement(tumbler *aptr, INT rightshift, INT bint, tumbler *cptr)
{
    if (iszerotumbler (aptr)) {
        tumblerclear (cptr);
        cptr->exp = -rightshift;
        cptr->mantissa[0] = bint;
        return(0);
    }
    if (aptr != cptr) movetumbler(aptr,cptr);
    for (idx = NPLACES ; aptr->mantissa[--idx] == 0 && idx > 0;);
    if (idx + rightshift >= NPLACES)
        gerror ("tumblerincrement overflow\n");
    cptr->mantissa[idx + rightshift] += bint;
    tumblerjustify (cptr);
}
```

This is pure arithmetic — no global counter, no registry. It adds `bint` at the position `idx + rightshift` in the mantissa of the existing tumbler. The only error condition is mantissa overflow (consuming all 16 places).

---

## Summary

| Question | Answer |
|----------|--------|
| Fixed at genesis? | **No.** No pre-allocated pool exists anywhere in the source. |
| Minted at runtime? | **Yes.** Every create operation computes a fresh tumbler. |
| Operation that creates a new node entry? | `createorglingranf()` [`granf2.c:111`], called by `docreatenewdocument()`, `docreatenode_or_account()`, `docreatelink()`, and `docreatenewversion()` in `do1.c`. |
| Core address-generation function? | `findisatoinsertnonmolecule()` [`granf2.c:203`], which walks the granfilade tree for the highest occupied sibling and increments past it via `tumblerincrement()`. |
| What limits the space? | Only the 16-place tumbler mantissa (`NPLACES=16`, `common.h:53`) and available memory. There is no logical ceiling imposed by the system. |

The address space is **open-ended and grows monotonically**: new addresses are always strictly greater than all previously issued siblings under the same parent. No address is ever reused (deletions remove enfilade entries but the granfilade address is not reclaimed for reuse). The system is self-indexing — the tree itself is the oracle for "what addresses have been issued."

---

## Question 19 [gregory]

> What is the structural relationship between a node tumbler and the account tumblers it contains — does the system enforce that account `N.0.A` can only allocate documents under `N.0.A.0.D`, or is the nesting purely conventional with no backend check preventing an account from writing outside its node's prefix?

### Gregory's Answer

## KB Synthesis

The relationship is enforced algorithmically within the allocation function, but there is no authorization layer preventing a session from claiming arbitrary account prefixes.

**What the allocation algorithm enforces**

Address allocation in `findisatoinsertnonmolecule` takes the session's current account tumbler as a hint and bounds the search explicitly. The post-Bug 0013 fix adds a containment check: after `findpreviousisagr` finds the highest existing address below the upper bound, the code verifies the result is actually under the target parent via tumbler truncation/comparison (`tumblertruncate` + `tumblereq`). Without this, the allocator crossed account boundaries — it would find `1.1.0.1.0.1` when allocating under `1.1.0.2`, increment it, and produce `1.1.0.1.0.2` (under the wrong account). [PRE-ADDRESS-ALLOC], [INV-ACCOUNT-ISOLATION]

The `.0.` hierarchy is encoded as a depth parameter to `makehint`. The NODE→NODE case uses depth=1 (no `.0.` crossing), while ACCOUNT→DOCUMENT uses depth=2 (crosses one `.0.` boundary). This is what produces `1.1.0.2.0.1` under account `1.1.0.2` rather than `1.1.0.2.1`. [SS-ADDRESS-SPACE] Finding 0021

**What is not enforced**

The session freely declares its current account via a SET_ACCOUNT call. Per-session state is isolated — each session has its own `current_account` — but there is no cross-session authorization check that a session is *permitted* to use a particular account prefix. Session A can set account `1.1.0.1` and session B can set the same account with no conflict; they each allocate sequentially under that namespace. [SS-SESSION-STATE], [FC-SESSION-ACCOUNT-ISOLATION]

The BERT system governs document-level read/write access once a document exists, but it does not gate account namespace selection. [SS-BERT], [PRE-OPEN-DOC]

**Summary**

- Account→document nesting is structurally enforced by the allocation algorithm's containment check — the backend prevents a document from being created outside the hint account's address subtree
- But account selection itself is self-declared by the session; any session can claim any account prefix
- The node→account hierarchy (e.g., node `1.1` containing account `1.1.0.2`) follows the same `.0.` separator convention and the same containment predicate, but is equally unguarded at the session-claim level

The invariant `INV-ACCOUNT-ISOLATION` holds only because well-behaved sessions use the correct account hint — the backend confirmed it requires explicit maintenance, not automatic enforcement from the flat storage structure. [INV-ACCOUNT-ISOLATION]

---

## Code Exploration

Now I have everything I need. Here is my full answer.

---

## Structural Relationship Between Node Tumblers and Account Tumblers

The short answer: **The nesting is real but only partially enforced. The backend checks that documents fall within a declared account prefix (via `tumbleraccounteq`), but it does NOT verify that the declared account tumbler itself falls within the connected node's prefix. `validaccount` is a stub that accepts any tumbler unconditionally.**

---

### 1. The Tumbler Hierarchy (`xanadu.h:140-143`)

```c
#define NODE      1
#define ACCOUNT   2
#define DOCUMENT  3
#define ATOM      4
```

The intended structure is hierarchical: node ⊃ account ⊃ document ⊃ atom, with zero-delimited tumbler digits at each level. An account `N.0.A` is supposed to live under node `N`, and a document `N.0.A.0.D` is supposed to live under that account.

---

### 2. The Ownership Function: `tumbleraccounteq` (`tumble.c:38-70`)

This is the only real structural enforcement in the system. It checks whether a document tumbler `aptr` falls within an account prefix `bptr`:

```c
bool tumbleraccounteq(tumbler *aptr, tumbler *bptr)
{
  INT i, j_b;
    if (aptr->sign != bptr->sign) { return(FALSE); }
    for (j_b = 0, i = 0; i < NPLACES; i++) {
        if (bptr->mantissa[i] == 0) {
            if (++j_b == 2) {
                return(TRUE);  /* Account terminated, document is under this account */
            }
            /* First zero — document can have any value at this position */
        } else {
            /* Non-zero — document must match exactly */
            if (aptr->mantissa[i] != bptr->mantissa[i]) {
                return(FALSE);
            }
        }
    }
    return (TRUE);
}
```

The logic: scan both mantissas in parallel. Whenever the account has a non-zero digit, the document must match exactly. Zeros in the account are level-separators — the **first** zero is skipped (the document may have any digit at that position, including sub-addressing), but the **second** zero terminates the account prefix and returns `TRUE`. For account `N.0.A` (mantissa `[N, 0, A, 0, 0, ...]`):

- Position 0: account=`N`, document must equal `N`
- Position 1: account=`0` → first zero, skip match check
- Position 2: account=`A`, document must equal `A`
- Position 3: account=`0` → second zero → `return TRUE`

So a document `N.0.A.0.D` (mantissa `[N, 0, A, 0, D, ...]`) would pass, and `N.0.B.0.D` would fail at position 2.

---

### 3. `isthisusersdocument` — All Three Implementations Are Identical

`isthisusersdocument` is the caller of `tumbleraccounteq`. All three build variants do the same thing:

- `be.c:171-176`: `return tumbleraccounteq(tp, &taskptrx->account);`
- `socketbe.c:197-201`: `return tumbleraccounteq(tp, &(player[user].account));`
- `xumain.c:198-201`: `return tumbleraccounteq(tp, &taskptrx->account);`

This function answers: "Does this document tumbler fall within the current session's declared account prefix?"

---

### 4. Where Ownership Is Checked (`bert.c:81`)

```c
if (!foundnonread && (type == READBERT || isthisusersdocument(tp))) {
    return 0;   /* can open without being in bert table */
} else {
    return -1;
}
```

If no conflicting open exists AND the document falls under the user's declared account, it can be opened for writing without entering the BERT table. This is the gating check that uses `tumbleraccounteq`.

Also at `do1.c:270`, in `docreatenewversion`:

```c
if (tumbleraccounteq(isaptr, wheretoputit) && isthisusersdocument(isaptr)) {
    makehint (DOCUMENT, DOCUMENT, 0, isaptr, &hint);
} else {
    makehint (ACCOUNT, DOCUMENT, 0, wheretoputit, &hint);
}
```

The ownership check determines whether a new version is created as a sibling of the original (if the user owns it) or as a fresh document under their account (if they don't).

---

### 5. Document Allocation Uses the Declared Account (`do1.c:234-241`)

```c
bool docreatenewdocument(typetask *taskptr, typeisa *isaptr)
{
  typehint hint;
  makehint (ACCOUNT, DOCUMENT, 0, &taskptr->account, &hint);
  return (createorglingranf (taskptr, granf, &hint, isaptr));
}
```

`createorglingranf` → `findisatoinsertgr` → `findisatoinsertnonmolecule` (`granf2.c:203-242`) places the new document at `hintisa.0.N` — that is, `taskptr->account.0.N`, the next available document slot under the declared account. This is real structural placement: documents are genuinely allocated under the account prefix in the granfilade.

---

### 6. The Critical Gap: `validaccount` Is a Stub

The account tumbler itself is set by the `XACCOUNT` protocol command. In `fns.c:364-373`:

```c
void xaccount(typetask *taskptr) {
    if (getxaccount(taskptr,&(player[user].account))) {
        putxaccount(taskptr);
    } else {
        putrequestfailed(taskptr);
    }
}
```

`getxaccount` in `get1.c:190-204` reads a tumbler from the wire then calls `validaccount`:

```c
gettumbler (taskptr, accountptr)
&& validaccount(taskptr, accountptr);
taskptr->account = *accountptr;
return(TRUE);
```

And `validaccount` in **both** `get2.c:157-160` and `get2fe.c:338-341`:

```c
bool validaccount(typetask *taskptr, typeisa *accountptr)
{
    return(TRUE);
}
```

**No validation is performed.** Any tumbler sent by the client is accepted as a valid account. There is no check that `N.0.A` shares the node prefix `N` with the node the client is connected to, no check that the account exists in the granfilade, no check of any kind.

---

### Summary

| Enforcement | Mechanism | Where | Result |
|---|---|---|---|
| Document → Account prefix | `tumbleraccounteq` | `bert.c:81`, `do1.c:270` | **Enforced** |
| Account → Node prefix | `validaccount` | `get2.c:157`, `get2fe.c:338` | **Not enforced — stub returns TRUE** |
| Document allocation under account | `makehint(ACCOUNT, DOCUMENT, ...)` | `do1.c:239` | Correct by construction if account is valid |
| Account validity | `validaccount` | `get1.c:200`, `get1fe.c:222` | **Not enforced — stub returns TRUE** |

**The backend enforces that documents fall under a declared account prefix** (via `tumbleraccounteq`). It does **not** enforce that the declared account falls under the node the client is attached to. A client could send `XACCOUNT 9.0.7` while connected to node `1`, and the backend would accept `9.0.7` as the account, allocate all documents under `9.0.7.0.*`, and the ownership checks would use `9.0.7` as the trust anchor. The node-to-account nesting is entirely conventional — there is no backend check preventing an account from writing outside its node's prefix.
