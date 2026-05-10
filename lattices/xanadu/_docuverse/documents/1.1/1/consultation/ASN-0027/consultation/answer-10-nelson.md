## Question 10 [nelson]

> Must the system guarantee that no operation — creation, editing, deletion, sharing, or reorganization — can cause two distinct pieces of content to share the same address?

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
