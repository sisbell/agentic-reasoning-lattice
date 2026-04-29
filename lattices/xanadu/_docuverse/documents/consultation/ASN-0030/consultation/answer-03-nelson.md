## Question 3 [nelson]

> What is the distinction between a document no longer displaying certain content and that content's address ceasing to be valid?

# Display vs. Existence: The Central Architectural Distinction

This question goes to the heart of what makes Xanadu different from every conventional storage system. The distinction is between **V-space** (what a document currently shows) and **I-space** (where content permanently lives). These are two separate address spaces with fundamentally different properties.

## The Two Spaces

**I-Space (Invariant Space)** is where content permanently resides. Every byte ever created gets a permanent I-space address that never changes and never becomes invalid:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

**V-Space (Virtual Space)** is the document's current arrangement — a view that references I-space content. V-addresses are ephemeral and shift with every edit:

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." [LM 4/11]

A document **is** the mapping from V-addresses to I-addresses. Each version defines a different mapping. Editing changes the mapping, not the content.

## What "Delete" Actually Means

When you delete content from a document, you remove it from V-space only. The I-space content is untouched. Nelson's diagram on page 4/9 explicitly shows "DELETED BYTES" as a valid system state:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

And more directly:

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

The content's address has not ceased to be valid. The document has merely stopped *displaying* it. The distinction is between:

| What happened | V-space effect | I-space effect |
|---|---|---|
| Content deleted from document | Removed from current arrangement | **None** — bytes remain forever |
| Content rearranged | Positions shift | **None** — bytes unchanged |
| New version created | New arrangement | **None** — same content, different view |

## Why This Matters

Nelson designed this separation to solve what he saw as the fundamental flaw of conventional computing:

> "Virtually all of computerdom is built around the destructive replacement of successive whole copies of each current version." [LM 2/14]

His alternative:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

The consequences cascade through the entire system:

1. **Links survive editing** — because links point to I-space addresses, not V-space positions. A link to content that has been "deleted" from a document still resolves, because the I-address is still valid:

   > "A Xanadu link is not between points, but between spans of data... links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them." [LM 4/42]

2. **Historical backtrack works** — because every previous V-space arrangement can be reconstructed from the permanent I-space content:

   > "The file management system we are talking about automatically keeps track of the changes and the pieces, so that when you ask for a given part of a given version at a given time, it comes to your screen." [LM 2/15]

3. **Transclusions survive** — if Document A transcludes content from Document B, and Document B's owner "deletes" that content from Document B's current version, the content still exists in I-space and Document A still shows it.

4. **Modifications never damage originals** — because modifications operate on V-space arrangements, not I-space content:

   > "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate--without damaging the originals." [LM 2/45]

## The Analogy

Think of it as a library versus a reading list:

```
I-Space (Library)              V-Space (Reading Lists)
┌─────────────────────┐        ┌─────────────────────┐
│ Shelf A: "hello"    │        │ My Essay v1:        │
│ Shelf B: " world"   │   ──►  │   [ref A, ref B]    │  → "hello world"
│ Shelf C: "!"        │        │                     │
│                     │        │ My Essay v2:        │
│ (never changes)     │   ──►  │   [ref A, ref C]    │  → "hello!"
└─────────────────────┘        └─────────────────────┘
```

Removing " world" from the reading list does not burn the book on Shelf B. The shelf address remains valid. The reading list simply no longer references it.

## The Permanence Guarantee

This is not a side effect of the implementation but the **foundational guarantee** of the system:

> "New items may be continually inserted in tumbler-space while the other addresses remain valid. This means that any address of any document in an ever-growing network may be specified by a permanent tumbler address." [LM 4/19]

A content address ceasing to be valid would violate Xanadu's deepest invariant. The whole point of the system is that **display is mutable but existence is permanent**. A document choosing not to show something is an editorial decision. An address becoming invalid would be a system failure.
