# Nelson Design Features

*Generated: 2026-03-01 — from ASN-0001, ASN-0002*

*Generated: 2026-03-01 — from ASN-0001, ASN-0002*

## Addressing

### F-ADDR-01: Unbounded address components

> "very short when a number is small, and as large as it needs to be when the number is big."

**Feature**: Every component of a tumbler address must be an arbitrary-precision integer with no upper limit, ensuring the address space can never be exhausted.

See also: "Our kingdom is already twice the size of Spain, and every day we drift makes it bigger."

**ASNs**: ASN-0001

---

### F-ADDR-02: Tumbler line total order

> "a flat mapping of a particular tree"

**Feature**: The system must impose a total linear order on all tumbler addresses corresponding to the depth-first traversal of the containment hierarchy.

**ASNs**: ASN-0001

---

### F-ADDR-03: Intrinsic address comparison

> "you always know where you are, and can at once ascertain the home document of any specific word or character."

**Feature**: The ordering and containment relationship of any two addresses must be computable from the addresses alone, without consulting any external index or data structure.

**ASNs**: ASN-0001

---

## Allocation

### F-ALLOC-01: Coordination-free allocation by prefix ownership

> "The owner of a given item controls the allocation of the numbers under it."

**Feature**: Each owner must be able to allocate addresses within their hierarchical prefix without coordinating with any other allocator; the prefix structure must guarantee global uniqueness.

**ASNs**: ASN-0001

---

### F-ALLOC-02: Chronological append-only allocation

> "suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically."

**Feature**: Each allocator must produce addresses in strictly monotonically increasing order, with new content appended chronologically and no backfilling of gaps.

**ASNs**: ASN-0001, ASN-0002

---

### F-ALLOC-03: Sequential hierarchical numbering

> "successive new digits to the right ... 2.1, 2.2, 2.3, 2.4 are successive items being placed under 2."

**Feature**: Successive allocations within a branch must produce sequentially numbered addresses, advancing the counter at the appropriate hierarchical level.

**ASNs**: ASN-0001, ASN-0002

---

## Documents

### F-DOC-01: Mutable virtual-space positions

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing."

**Feature**: The virtual-space position of content within a document must be mutable, changing freely with editing operations, independent of the content's permanent I-space address.

**ASNs**: ASN-0001, ASN-0002

---

### F-DOC-02: Non-destructive deletion

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)"

**Feature**: Deletion must remove content only from a document's current virtual arrangement; deleted bytes must remain in the permanent content store and in any other documents that include them.

See also: "the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included."

**ASNs**: ASN-0002

---

## Hierarchy

### F-HIER-01: Four-field hierarchical structure

> "There are four major fields, each expandable indefinitely, with three major dividers between them. These fields are Server, User, Document and Contents."

**Feature**: Every tumbler address must be structured into exactly four hierarchical fields — server, user, document, and contents — each independently expandable.

**ASNs**: ASN-0001

---

### F-HIER-02: Zero-delimited field parsing

> "A tumbler address may have at most three zero digits... These are interpreted as the major dividers, and have lexical significance as punctuation."

**Feature**: The system must use at most three zero-valued components as field separators, and the count of zeros must unambiguously determine the hierarchical level of an address.

**ASNs**: ASN-0001

---

### F-HIER-03: Primordial server root

> "since all other servers are descended from it"

**Feature**: The server field of every address must descend from server 1, establishing a single root for the entire server hierarchy.

**ASNs**: ASN-0001

---

### F-HIER-04: Element subspace separation

> "could be further subdivided"

**Feature**: The element field must use its first component to permanently separate content types (text in subspace 1, links in subspace 2) into disjoint subspaces within each document, with provision for further subdivision.

**ASNs**: ASN-0001

---

## Links

### F-LINK-01: Link survivability through editing

> "Links between bytes can survive deletions, insertions and rearrangements, if anything is left at each end."

**Feature**: Links must survive all editing operations — insertions, deletions, and rearrangements — as long as content remains at each endset.

**ASNs**: ASN-0002

---

### F-LINK-02: Links attach to content identity

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them."

**Feature**: Links must attach to the permanent identity (I-space address) of content, not to its mutable position within any document.

**ASNs**: ASN-0002

---

## Permanence

### F-PERM-01: Permanent tumbler addresses

> "any address of any document in an ever-growing network may be specified by a permanent tumbler address."

**Feature**: Once a tumbler address is assigned to content, the assignment must be permanent — no operation may remove, reassign, or alter the mapping.

**ASNs**: ASN-0001, ASN-0002

---

### F-PERM-02: Content immutability at assigned addresses

> "those bytes remain in all other documents where they have been included."

**Feature**: Content stored at a permanent I-space address must remain unchanged for all time, ensuring stable transclusion and link references across all documents that include it.

**ASNs**: ASN-0001, ASN-0002

---

### F-PERM-03: Ghost element permanence

> "the docuverse is the occupied tumbler-space — as occupied by conceptually assigned positions, even if nothing represents them in storage."

**Feature**: Addresses that have been passed by the allocation frontier but never assigned content (ghost elements) must remain permanently claimed and must never be reused for new content.

See also: "While servers, accounts and documents logically occupy positions on the developing tumbler line, no specific element need be stored in tumbler-space to correspond to them. Hence we may call them ghost elements." And: "these elements are virtually present in tumbler-space, since links may be made to them which embrace all the contents below them."

**ASNs**: ASN-0001, ASN-0002

---

## Spans

### F-SPAN-01: Contiguous spans determined by endpoints

> "The first point of a span may designate a server, an account, a document or an element; so may the last point. There is no choice as to what lies between; this is implicit in the choice of first and last point."

**Feature**: A span defined by two endpoints must capture exactly the contiguous set of addresses between them; the contents of a span must be fully and exclusively determined by its endpoints.

**ASNs**: ASN-0001

---

### F-SPAN-02: Hierarchical span designation

> "A digit of 'one' may be used to designate all of a given version, all versions of a given document, all works of a given author, all documents in a given project, all documents on a given server — or the entire docuverse."

**Feature**: A single span must be able to designate content at any hierarchical level — from a single character to the entire docuverse — using the tumbler hierarchy's prefix structure.

**ASNs**: ASN-0001

---

### F-SPAN-03: Future-valid empty spans

> "A span that contains nothing today may at a later time contain a million documents."

**Feature**: A span with no currently assigned content must remain valid; future allocations within its range must automatically fall within the span without modification to the span itself.

**ASNs**: ASN-0001

---

## Transclusion

### F-TRCL-01: Virtual copies share identity

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies."

**Feature**: Transcluded content must occupy positions in the target document's virtual stream as if native, while retaining its original I-space identity — no content duplication may occur.

**ASNs**: ASN-0002

---

## Versioning

### F-VERS-01: Version numbering implies no derivation

> "the version, or subdocument number is only an accidental extension of the document number, and strictly implies no specific relationship of derivation."

**Feature**: Version numbering within the document field must be purely structural (reflecting allocation hierarchy); the system must not infer derivation or editing history from address structure alone.

**ASNs**: ASN-0001

---

### F-VERS-02: Version creation shares content

> "This creates a new document with the contents of document <doc id>."

**Feature**: Creating a new version of a document must produce a new document identity that references the same I-space content as the source, without duplicating content in the permanent store.

**ASNs**: ASN-0002
