## Question 8 [nelson]

> Is address permanence a property of the content itself or of the relationship between the content and the storage system — that is, could the system migrate content internally while preserving the address?

## Address Permanence Is a Property of the Coordinate System, Not of Physical Storage

The answer is unambiguous in the architecture: **the system can and must migrate content internally while preserving addresses.** Address permanence is a property of the logical coordinate system (tumbler-space), not of any physical storage arrangement.

### The Address Space Is Abstract

Tumbler-space is a conceptual coordinate system that exists independently of what is physically stored:

> "The docuverse is the occupied tumbler-space--as occupied by conceptually assigned positions, even if nothing represents them in storage." [LM 4/23]

> "Thus the address population of tumbler-space is also an abstraction, since things may be addressed even though nothing is there to represent them in storage." [LM 4/23]

Ghost elements prove the point decisively: addresses can exist with **nothing stored at them**. The address is not a property of stored bytes — it is a position in an abstract coordinate space that bytes may or may not occupy.

### Physical Migration Is Explicitly Designed In

The BEBE protocol describes content actively moving between servers:

> "The contents can slosh back and forth dynamically." [LM 4/72]

Content migrates for four explicit reasons:

> "Material is moved between servers for a number of purposes: 1. for more rapid access to final material, 2. for more rapid access to needed material which indexes material on other servers, 3. for rebalance in keeping with demand, 4. for redundancy and backup purposes." [LM 4/71]

Each server holds a subset of the whole — a "microcosm that shrinks and grows" [LM 4/71]. Content replicates toward demand. The physical location of bytes is a performance optimization, not an identity property.

### Physical Storage Is Explicitly Hidden from Users

The FEBE protocol hides all physical details:

> "Now that some of these commands are to be seen by the user: The user's concerns are document content and links, and the complications of the protocol are to be handled invisibly by programs in the user's front-end machine, leaving the user free to think about other things." [LM 4/61]

Users work with tumbler addresses. Where bytes physically reside is invisible and irrelevant to them.

### The I-Address Encodes Provenance, Not Location

The I-space address has the form `Node.0.User.0.Document.0.Element` [LM 4/26]. The Node field records which server **originally created** the content — its provenance. But content migrates between servers freely via BEBE. The Node field is a birth certificate, not a GPS coordinate.

This is confirmed by how "native" and "non-native" bytes work:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

The system **fetches** content from wherever it currently lives. The address tells you where to start looking (the home location), but BEBE's forwarding and subrepresentation mechanisms handle the actual retrieval regardless of physical location.

### The V-Space Address Is Explicitly Mutable

To sharpen the contrast: V-space addresses (the document's current arrangement) change constantly during editing:

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." [LM 4/11]

I-space addresses are permanent. V-space addresses are ephemeral. But even I-space permanence refers to the **logical identity** of the content (this byte was created at this coordinate), not to the physical location of the storage medium holding it.

### The Enfilades Handle the Mapping

The internal data structures (enfilades) exist precisely to maintain the mapping between logical addresses and physical storage:

> "His new method would allow linkages to keep up with all changes. It was instantaneous and permanent and could grow indefinitely. All changes, once made, left the file remaining in canonical order, which was an internal mandate of the system." [LM 1/34]

The enfilades are the mechanism that makes addresses permanent while storage is reorganized. They map the abstract coordinate (tumbler address) to wherever the bytes currently live.

### Summary

Address permanence in Xanadu is a three-layer design:

| Layer | What it is | Permanent? |
|-------|-----------|------------|
| **Tumbler address** | Logical coordinate in abstract space | Yes — forever |
| **I-space content** | The bytes themselves (immutable once created) | Yes — append-only |
| **Physical storage location** | Where bytes reside on which server | No — migrates freely |

The guarantee to users is: **this coordinate will always resolve to this content.** The system is free — indeed required — to migrate, replicate, cache, and redistribute the physical bytes to meet the "soft corridor" performance requirement. Tumblers are coordinates in a conceptual space. Storage is an optimization problem solved by enfilades and BEBE. The two concerns are deliberately decoupled.
