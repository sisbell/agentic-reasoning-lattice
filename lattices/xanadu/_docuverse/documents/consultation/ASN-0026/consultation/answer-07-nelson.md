## Question 7 [nelson]

> When a new version of a document rearranges its content differently, must the system preserve the previous arrangement as well, or only the underlying content?

## Both Are Preserved

The system must preserve **both** the previous arrangement and the underlying content. This is fundamental to Xanadu's architecture.

### The Arrangement IS the Version

A version in Xanadu is not a snapshot of content — it *is* a particular V-space arrangement over permanent I-space content. Each version has its own V-stream mapping. When you create a new version with a different arrangement, the old version's arrangement remains as a distinct, accessible V-space mapping.

> "There is thus no 'basic' version of a document set apart from other versions—'alternative' versions—any more than one arrangement of the same materials is a priori better than other arrangements." [LM 2/19]

### The Two-Layer Guarantee

**I-space (content):** Always preserved. Append-only, never overwritten.

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

**V-space (arrangement):** Each version's arrangement is independently preserved and reconstructable.

> "The file management system we are talking about automatically keeps track of the changes and the pieces, so that when you ask for a given part of a given version at a given time, it comes to your screen." [LM 2/15]

### Why Arrangement Preservation Is Required

Three capabilities depend on it:

1. **Historical backtrack** — Users must be able to reconstruct any previous state, which means reconstructing the previous *arrangement*, not just knowing the content existed.

2. **Intercomparison** — Comparing versions requires both arrangements to exist simultaneously:

   > "Of course, a facility that holds multiple versions of the same material, and allows historical backtrack, is not terribly useful unless it can help you intercompare them in detail—unless it can show you, word for word, what parts of two versions are the same." [LM 2/20]

3. **Correspondence** — The system must show which parts of one arrangement correspond to which parts of another. This is only meaningful if both arrangements are preserved:

   > "The user may scroll through any two versions to see corresponding parts; and much more." [LM 2/21]

### The Braid Metaphor

Nelson's metaphor makes this explicit — editing is *re-twisting* the braid, not replacing it:

> "Think of the process of making editorial changes as re-twisting this braid when its parts are rearranged, added or subtracted... and think then of successive versions of the document, at successive instants of time, as alive in this space-time vortex." [LM 2/15]

The braid accumulates strands. Each twist (rearrangement) adds to the history; it does not erase what came before. Users can "scroll through an individual document, at successive instants of time" [LM 2/15] — which requires each arrangement to persist.

### Summary

Preserving only the content without the arrangement would violate historical backtrack, intercomparison, and correspondence — three of Xanadu's core capabilities. The V-space mapping of every version is as permanent as the I-space content it references.
