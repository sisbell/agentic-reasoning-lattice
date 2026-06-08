## Question 5 [theory]

> What must the design preserve about the immutability of content when that content is reused in a new document rather than recreated?

## What the Design Must Preserve

When content is **reused** (transcluded) rather than recreated, the design must preserve **content identity through shared addressing**: the reused content keeps its original, permanent Istream address. It is included *by reference*, not copied. The immutable byte never changes, never duplicates, and never loses its connection to its point of origin.

### 1. Reuse is inclusion by reference, not copy

The content exists exactly once, at its home location. A new document that reuses it points back to those native bytes rather than holding its own copy.

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." (4/11)

> "The virtual byte stream of a document may include bytes from any other document." (4/10)

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." (4/11)

### 2. Identity is based on creation, not value

This is the crux of immutability under reuse. Two documents that independently type the same words get *different* I-addresses. Transcluded content keeps the *same* I-address as its source. The system must distinguish "wrote the same words" from "quoted the original."

The reused bytes are full logical members of the new document while remaining the very same bytes:

> "Non-native bytes are as much a logical part of a document as native bytes." (4/11)

### 3. The original is unaffected by the reuse — and the reuse survives changes to the original

Because the content is immutable and referenced (not owned by the reuser), modifications on either side cannot destroy the shared bytes. Critically, even deletion in the source does not remove the bytes from documents that included them:

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." (4/11)

This is the immutability guarantee in action: the Istream byte is permanent. "Deletion" only changes a Vstream arrangement; the immutable content persists wherever it has been reused.

### 4. Attribution remains structural

Because reuse carries the original I-address, the home document is always ascertainable from the address itself — attribution cannot be stripped by reuse:

> "You always know where you are, and can at once ascertain the home document of any specific word or character." (2/40)

### Summary

The design must preserve that reused content is the **same immutable bytes at the same permanent Istream address**, included by reference. Recreation would mint new, independent content with new identity; reuse must instead share identity with the original. This preserves immutability (the byte never changes), permanence (the address never breaks), non-destruction (the original is undamaged and the inclusion survives source deletion), and structural attribution (origin is always traceable).
