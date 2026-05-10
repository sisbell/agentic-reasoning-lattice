## Question 1 [nelson]

> When new content is added to a document, does the system create a new version of that document, or does the document itself change in place?

## The document changes in place — but nothing is lost

Nelson's answer is unambiguous: **editing operations modify the document directly**, without creating a new version. But the system's append-only storage ensures every previous state remains reconstructable.

### Two separate operations

The FEBE protocol distinguishes these clearly:

**INSERT** modifies the existing document:
> "This inserts \<text set\> in document \<doc id\> at \<doc vsa\>. The v-stream addresses of any following characters in the document are increased by the length of the inserted text." [LM 4/66]

**CREATENEWVERSION** creates a distinct new document:
> "This creates a new document with the contents of document \<doc id\>. It returns the id of the new document. The new document's id will indicate its ancestry." [LM 4/66]

INSERT, DELETE, REARRANGE, and APPEND all operate on the document's V-space arrangement directly. None of them create new versions.

### How this works without destruction

The key is the I-space / V-space separation:

- **I-space is append-only.** New content is added to permanent storage. Nothing is overwritten.
- **V-space is the current arrangement.** INSERT changes which I-space bytes appear at which positions in the document's virtual byte stream.
- **History is reconstructable.** The system tracks every change chronologically.

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

> "The true storage of text should be in a system that stores each change and fragment individually, assimilating each change as it arrives, but keeping the former changes; integrating them all by means of an indexing method that allows any previous instant to be reconstructed." [LM 2/15]

### The "ongoing braid" model

Nelson's metaphor is precise:

> "A document is really an evolving ONGOING BRAID." [LM 2/14]

> "Think of the process of making editorial changes as re-twisting this braid when its parts are rearranged, added or subtracted... and think then of successive versions of the document, at successive instants of time, as alive in this space-time vortex." [LM 2/15]

The braid is one continuous thing that evolves — not a series of snapshots. Each edit re-twists the braid. The system can reconstruct any prior twist:

> "The file management system we are talking about automatically keeps track of the changes and the pieces, so that when you ask for a given part of a given version at a given time, it comes to your screen." [LM 2/15]

### So what is a "version"?

There are two distinct senses:

1. **Implicit history** — Every prior state of the document is accessible through historical backtrack. These are moments in the braid's evolution, not separate objects.

2. **Explicit version (CREATENEWVERSION)** — A deliberate fork that creates a new document with its own tumbler address, sharing I-space content with the original. This is used for alternative arrangements, published corrections, or branching.

> "There is thus no 'basic' version of a document set apart from other versions — 'alternative' versions — any more than one arrangement of the same materials is a priori better than other arrangements." [LM 2/19]

### Summary

When you INSERT content into a document, the document itself changes. No new version is created. But the change is non-destructive: new bytes go to I-space (permanent), the V-space mapping updates (current view shifts), and the previous arrangement remains reconstructable. The document is one evolving entity with full history — not a chain of frozen copies.
