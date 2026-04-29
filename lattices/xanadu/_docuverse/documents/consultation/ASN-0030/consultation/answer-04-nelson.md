## Question 4 [nelson]

> Must every piece of content that has ever been stored in the system remain permanently reachable by its original address, or are there conditions under which reachability may be lost while identity is preserved?

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
