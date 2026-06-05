## Question 8 [theory]

> What must the system guarantee about a new document being immediately and unambiguously referable by links the moment it exists?

## What the system must guarantee

The moment a new document exists, the system must guarantee it has a **permanent, unique tumbler address** that is immediately and unambiguously referable. This rests on several interlocking guarantees from Nelson's design:

### 1. An address is assigned at creation, returned to the creator

The `CREATENEWDOCUMENT` operation establishes this directly:

> "This creates an empty document. It returns the id of the new document." (4/65)

So even an *empty* document — one with no content yet — already has its identifier. The id exists before any bytes do.

### 2. The address is unambiguous because it is "owned," not centrally registered

Uniqueness is guaranteed structurally through forking/baptism, with no need for a central allocator that could produce a collision or a delay:

> "The basic principle is that of owned numbers... Whoever owns a specific node, account, document or version may in turn designate (respectively) new nodes, accounts, documents and versions, by forking their integers. We often call this the 'baptism' of new numbers." (4/17)

> "The owner of a given item controls the allocation of the numbers under it." (4/20)

Because the new document's address is forked under its owner's account, no two owners can ever mint the same address — uniqueness is decentralized and immediate.

### 3. The address is permanent — it never breaks or gets reused

> "New items may be continually inserted in tumbler-space while the other addresses remain valid. This means that any address of any document in an ever-growing network may be specified by a permanent tumbler address." (4/19)

A reference made the instant the document exists will remain valid indefinitely.

### 4. Links can reference it even before anything is stored ("ghost elements")

Critically, referability does **not** wait on content existing. Nelson's ghost-element principle means an address is linkable as a pure position in tumbler-space:

> "It is possible to link to a node, or an account, even though there is nothing stored in the docuverse corresponding to them." (4/23)

> "However, these elements are virtually present in tumbler-space, since links may be made to them which embrace all the contents below them." (4/23)

> "A link to or search of an account or node will find any of the documents under it." (4/23)

This is the deepest form of the guarantee: the address space is conceptual, so a document is referable from the moment its position is baptized — even forward-referenced before content arrives.

## Summary

The guarantee is that a new document **immediately occupies a permanent, unique position on the tumbler line** — assigned by ownership-based baptism (so it is unambiguous without central coordination), valid forever (so references never break), and linkable as a position in tumbler-space (so links can target it the instant it exists, even before content is stored). Links attach to the document's address, and that address is guaranteed at creation.

The curated sources fully support the conceptual guarantees. One detail I could not verify from the curated material alone is whether `CREATENEWDOCUMENT` is specified to be atomic/synchronous such that the returned id is usable before any subsequent operation — if you need that implementation-level guarantee stated explicitly: NEED_RAW: 4/65, 4/79.
