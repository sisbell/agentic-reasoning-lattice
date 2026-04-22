# Tumblers

Source: Literary Machines, pages 4/15-4/19 (raw 182-186)

## Semantic Intent

### What It Means

A tumbler is Xanadu's universal addressing system - a specially designed multi-part number that can name anything in the docuverse: server nodes, user accounts, documents, versions, and positions within text. The name comes from the rotating mechanisms in locks, where independent cylinders slide and increment separately - tumblers work the same way, with each "digit" (an unbounded integer) operating independently.

The key insight is that conventional numbering systems fail for an ever-growing, decentralized universe of documents. A simple large integer domain would waste bits on unoccupied space. The Dewey Decimal System inspired the solution: forking numbers that can be continually subdivided to make room for new items without disturbing existing addresses.

Critically, tumblers are purely a mapping mechanism - they impose no structure, categorization, or organization on the content they address. A document's tumbler address says nothing about its subject matter or how it relates to other documents semantically.

Importantly, **time is not encoded in the tumbler**. While tumblers can address versions of documents, they do not record when something was created or modified. Time is "kept track of separately" - as metadata that can be used for filtering (e.g., "What links came in from last week?") but is not part of the address itself. This keeps tumblers focused purely on *where* things are in the docuverse, not *when* they appeared.

### User Guarantee

**Any address, once assigned, remains valid forever.** New items can be continually inserted in tumbler-space while all existing addresses remain unchanged and functional. This means a reference you make today to a document, version, or piece of text will work indefinitely - the system never invalidates old addresses.

### Principle Served

Tumblers solve the fundamental problem of building a permanent, decentralized literary system. Without a central authority managing address allocation, the system still needs to:
- Allow the network to grow unpredictably
- Allow documents and versions to proliferate indefinitely
- Keep all addresses permanently valid
- Support efficient arithmetic for searches and offsets

The "baptism" principle makes this work: whoever owns a specific address can designate new sub-addresses by forking their integers, without coordinating with anyone else.

### How Users Experience It

- Every piece of content has a permanent, unique address
- References never "break" due to reorganization or growth
- You can reference content at any granularity: whole documents, versions, or specific character positions
- The address tells you something about provenance: which server, which account, which document lineage
- No central registration required - owners simply "baptize" new addresses under their own
- Addresses don't constrain content organization - you structure your documents however you want; tumblers just locate them

### Nelson's Words

> "Our kingdom is already twice the size of Spain, and every day we drift makes it bigger." (4/15, epigraph)

> "Tumbler addressing is concerned with the management of storage--the spontaneous creation of places to put things, and remembrance of where they are." (4/16)

> "In one big flash of insight, Mark Miller saw that everything could be named within a common structure, and that an arithmetic could be developed for this structure to be the common internal language throughout the search procedures of the system." (4/16)

> "The basic principle is that of owned numbers. Numbers are owned by individuals or companies, and subnumbers under them are bestowed on other individuals and companies on whatever basis the owners choose. Whoever owns a specific node, account, document or version may in turn designate (respectively) new nodes, accounts, documents and versions, by forking their integers. We often call this the 'baptism' of new numbers." (4/17)

> "Tumblers do not affect the user-level structure of the documents; they only provide a mapping mechanism, and impose no categorization and no structure on the contents of a document." (4/17-4/18)

> "New items may be continually inserted in tumbler-space while the other addresses remain valid. This means that any address of any document in an ever-growing network may be specified by a permanent tumbler address." (4/19)

> "A tumbler consists of a series of integers. Each integer has no upper limit; since its number base is irrelevant, we call it a 'digit.' The digits of the tumbler are separated by minor dividers, or points." (4/19)

> "So the docuverse is all really one big forking document." (4/18)

> "Note that 'time' is not included in the tumbler. Time is kept track of separately." (4/18)

---

## Related Concepts

| Concept | Relationship |
|---------|--------------|
| [spans](spans.md) | Spans are tumbler pairs (start + width or start + end) |
| [i-space-v-space](i-space-v-space.md) | Both spaces use tumbler addressing |
| [docuverse](docuverse.md) | The universe of all tumbler-addressed content |
| [humbers](humbers.md) | Alternative name/concept for tumblers |
| [documents](documents.md) | Documents have tumbler addresses |
| [links](links.md) | Links have tumbler addresses; endsets point to tumblers |

## FEBE Operations

Tumblers are the addressing foundation - every FEBE operation uses them:

| Operation | How tumblers apply |
|-----------|-------------------|
| **INSERT, APPEND** | New content gets fresh tumbler addresses |
| **CREATENEWDOCUMENT** | Document gets permanent tumbler address |
| **CREATENEWVERSION** | Version ID is a tumbler (indicates ancestry) |
| **MAKELINK** | Link gets tumbler address; endsets are tumbler spans |
| All retrieval ops | Specify targets via tumbler addresses |

See [Concept-Operation Map](../concept-operation-map.md) for full mapping.