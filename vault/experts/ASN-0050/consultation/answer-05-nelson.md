## Question 5 [nelson]

> Must the system preserve the fact that specific content was once part of a document's arrangement at a particular version, even after removal?

## Yes — Unambiguously

Nelson requires that the system preserve the complete arrangement history of every version. This is not optional; it is the core of what he calls **historical backtrack**.

### The Direct Evidence

The strongest statement comes from the DELETE semantics diagram on page 4/9:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

Content removed from a document's current V-space arrangement enters a specific state: **not currently addressable, but preserved and awaiting recall**. The phrase "awaiting historical backtrack functions" means the system must retain enough information to reconstruct the arrangement that included those bytes.

Nelson makes the reconstruction guarantee explicit:

> "The file management system we are talking about automatically keeps track of the changes and the pieces, so that when you ask for a given part of a given version at a given time, it comes to your screen." [LM 2/15]

This is a **three-dimensional request** — part, version, and time — and it requires the system to know what content belonged to which arrangement at which point. If the system discarded the fact of prior membership, it could not fulfill this guarantee.

### Why Preserving Content Alone Is Insufficient

I-space permanence guarantees the bytes survive forever. But that only answers "does this content exist?" It does not answer "was this content part of document D at version V?" — which is what historical backtrack requires.

The V-space arrangement is the document. Two documents can reference entirely different I-space content but present the same text. What makes a version *that version* is its specific V→I mapping. Nelson's system must preserve these mappings, not just the I-space content they point to.

This is confirmed by the version comparison operation:

> "This returns a list of ordered pairs of the spans of the two spec-sets that correspond." [LM 4/70, on SHOWRELATIONOF2VERSIONS]

To return corresponding span pairs between two versions, the system must know the full V-space composition of both — including content that may have been removed from one but not the other.

### The Append-Only Foundation

Nelson's storage model makes this architecturally inevitable:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

> "The true storage of text should be in a system that stores each change and fragment individually, assimilating each change as it arrives, but keeping the former changes." [LM 2/15]

The append-only model means V-space mappings accumulate — they are never overwritten. Each version's arrangement is a permanent record. The "historical trace enfilade" [LM 1/36] exists specifically to support this: reconstructing any prior arrangement from the accumulated changes.

### The Ownership Dimension

Nelson adds a cross-document constraint:

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

This means deletion is purely local to the V-space of the document being edited. Other documents that transclude the same I-space content are unaffected. But even within the originating document, the prior version's arrangement — which included those bytes — must remain reconstructable.

### The Braid Metaphor

Nelson's metaphor captures the design intent precisely:

> "A document is really an evolving ONGOING BRAID." [LM 2/14]

> "Think of the process of making editorial changes as re-twisting this braid when its parts are rearranged, added or subtracted... and think then of successive versions of the document, at successive instants of time, as alive in this space-time vortex." [LM 2/15]

A braid does not lose its earlier twists when new ones are added. The prior shape remains visible in the structure. This is the point: the system preserves not just content but the **history of arrangement**.

### Summary

The system must preserve three things:

1. **The content itself** — I-space permanence (bytes never deleted)
2. **The fact of membership** — which content belonged to which version's V-space arrangement
3. **The ordering** — the V-space positions within each version

Without all three, the fundamental guarantee — "when you ask for a given part of a given version at a given time, it comes to your screen" — cannot be met.
