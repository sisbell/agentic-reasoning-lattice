## Question 2 [nelson]

> Must every node receive a permanent, globally unique identity, and is that identity assigned by the system or derived from the node's content?

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
