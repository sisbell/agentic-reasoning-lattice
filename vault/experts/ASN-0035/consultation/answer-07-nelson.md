## Question 7 [nelson]

> Can two distinct nodes hold identical content, or must every node differ from every other node in at least one property?

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
