## Question 5 [nelson]

> Must the system distinguish between "content as originally written" and "content as currently arranged for reading" as fundamentally separate concerns?

# Yes. This separation is the architectural foundation of everything.

The distinction between content-as-written (I-space) and content-as-arranged (V-space) is not a feature of Xanadu — it is the *premise* on which all other features stand. Without it, you cannot have permanent addresses, survivable links, non-destructive editing, version history, transclusion, or automatic attribution. Every guarantee I made depends on this separation.

## The Two Spaces

**I-Space (Invariant Space)** is where content permanently lives. Every byte ever created gets a permanent address here. Content at an I-space address never changes.

**V-Space (Virtual Space)** is the document's current arrangement — a view that references I-space content. V-space can be rearranged across versions. It is ephemeral; editing changes V-addresses constantly.

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." [LM 4/11]

The document IS the mapping from V-addresses to I-addresses. Each version defines a different mapping. Edits change the mapping, not the I-space content.

## Why This Must Be So

### 1. Links survive editing because they point to I-space

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes. This has a crucial advantage: it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them." [LM 4/42]

When you insert content, V-space positions shift — but I-space addresses remain stable. Links point to I-space. Therefore links are unaffected by insertion. The link doesn't care where the bytes appear in V-space. It only cares that the bytes it references still exist in I-space.

If you collapsed I-space and V-space into one, every edit would break every link. The entire web of literature would shatter with each keystroke.

### 2. Deletion is non-destructive because it only affects V-space

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

DELETE removes content from V-space (the current arrangement) but does NOT remove it from I-space (permanent storage). Previous versions still contain the deleted content. Other documents that transclude it still show it. Links to it still resolve.

Without the separation, "delete" would mean "destroy" — and with destruction, you lose history, break transclusions, and sever links.

### 3. Version history is structural, not backup

> "Virtually all of computerdom is built around the destructive replacement of successive whole copies of each current version." [LM 2/14]

> "A document is really an evolving ONGOING BRAID." [LM 2/14]

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

Each version is a different V-space arrangement over the same I-space content. Version history emerges naturally from the separation — it is not a bolted-on feature but the inevitable consequence of treating content and arrangement as distinct.

### 4. Correspondence (version comparison) derives from shared I-space origin

> "Of course, a facility that holds multiple versions of the same material, and allows historical backtrack, is not terribly useful unless it can help you intercompare them in detail — unless it can show you, word for word, what parts of two versions are the same." [LM 2/20]

When two V-space positions in different versions map to the same I-space address, those positions *correspond*. The system can show you what is the same and what differs between any two versions — automatically, structurally, without metadata or diff algorithms — because the shared I-space origin IS the correspondence.

### 5. Transclusion works because V-space references I-space across documents

> "The virtual byte stream of a document may include bytes from any other document." [LM 4/10]

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

When you transclude, your V-space includes a reference to someone else's I-space content. The content exists once, permanently, at its I-space address. Your document merely points to it. Attribution is automatic because the I-address encodes which document created those bytes.

### 6. Origin traceability is encoded in the address itself

Every I-space address has the form `Node.0.User.0.Document.0.Element` — the Document field directly encodes which document originally created that byte.

> "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

This is not metadata that can be stripped. It is the address itself. To fetch content, the system must request it from its home location. The connection cannot be severed because the fetching mechanism requires it.

## The Analogy

Think of a library:

```
I-Space (Library Stacks)           V-Space (Reading Lists)
┌─────────────────────┐            ┌─────────────────────┐
│ Shelf A: "hello"    │            │ My Essay v1:        │
│ Shelf B: " world"   │   ──►     │   [ref A, ref B]    │  → "hello world"
│ Shelf C: "!"        │           │                     │
│                     │            │ My Essay v2:        │
│ (never changes)     │   ──►     │   [ref A, ref C]    │  → "hello!"
└─────────────────────┘            └─────────────────────┘
```

The library stacks (I-space) never change. Reading lists (V-space) can be rearranged, versioned, shared, and compared — because they are *about* the stacks, not the stacks themselves.

## The Consequence of Collapsing Them

If you merge "content as written" with "content as arranged," you get conventional file systems: saving overwrites. Editing destroys. Links break. History requires full copies. Attribution requires trust in metadata. Transclusion becomes copying. And copying, as I said:

> "Note also that he or she who makes a paper copy or disk is losing all dynamic link connections, and is left with the inert, non-interactive copy. And that will be a considerable deprivation in the world we are talking about." [LM 2/48]

A dead copy. Frozen. Severed from the living literature.

## Summary

The separation of I-space from V-space is not one feature among many. It is the single architectural decision from which permanence, link survivability, non-destructive editing, version history, correspondence, transclusion, and origin traceability all follow. Remove this distinction and every guarantee collapses simultaneously.

The answer is not merely "yes, the system must distinguish them" — it is that the distinction between content-as-created and content-as-arranged IS the system.
