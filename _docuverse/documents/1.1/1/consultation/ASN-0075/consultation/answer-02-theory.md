## Question 2 [theory]

> When two documents share history, what does the design require the system to recognize as "deleted content" versus content that was merely never included?

The distinction rests on **temporal Vstream history** for each document, not on shared Istream content. The system must track, per document, whether content was ever part of that document's arrangement.

## The Three States

A given piece of content (identified by its I-address) can be in one of three states relative to a particular document:

1. **Currently included** — present in the document's current Vstream
2. **Deleted** — was previously in this document's Vstream, removed via a DELETE operation
3. **Never included** — exists in Istream (perhaps because it lives in another document or an ancestor's arrangement), but was never part of this document's Vstream

The diagram on page 4/9 makes this explicit by listing "DELETED BYTES" as a recognized state of a document's contents, annotated:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

That annotation does the work. "Awaiting historical backtrack functions" tells you the system MUST remember these bytes were once HERE — that's what makes backtrack possible. "May remain included in other versions" tells you the same I-content can be present elsewhere; that doesn't make it "not deleted" from this document.

## When Two Documents Share History

This is where the design gets exact. Take two cases:

**Case A — Version lineage via CREATENEWVERSION:**

When the system creates a new version, "the new document's id will indicate its ancestry" [LM 4/66]. The child begins life with the parent's Vstream as its starting arrangement. From that moment forward, the child has its own history of edits. Content present in the parent but removed by the child via DELETE is **deleted from the child**. The child carries a record of having had it and removed it.

**Case B — Documents merely sharing Istream content (e.g., one transcluded from the other, or both transcluded from a common source):**

Here there is no ancestry between the two documents. Document B may share I-addresses with Document A because B windowed some of A's content. But content in A that B never windowed was **never included in B**. B has no record of having had it, because B never did.

This is why Nelson's note on 4/11 is precise:

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

The bytes "remain in" other documents where they were *included* — not in documents where they happened to be addressable via shared Istream. Inclusion is a positive act in a document's Vstream history. Without that act, the content is not "present elsewhere awaiting deletion" — it is simply absent from that document's story.

## What the System Therefore Must Maintain

For each document, the design requires a per-document record of Vstream operations sufficient to answer:

- Was this I-content ever in *this* document's Vstream? (If no → never included)
- If yes, is it in the current Vstream? (If yes → currently included; if no → deleted)

This is the substrate that makes historical backtrack possible. Without it, you could only ask "does this content exist in Istream?" — which collapses the two cases the design specifically separates.

## Why This Matters

The distinction is not pedantic. It governs what SHOWRELATIONOF2VERSIONS can report, what historical backtrack can recover, and what the "evolving braid" [LM 2/14] actually means. A braid that lost the memory of strands it once held but later released would not be a braid — it would just be its current state. The whole point of the design is that:

> "When you ask for a given part of a given version at a given time, it comes to your screen." [LM 2/15]

That guarantee fails the moment "deleted" and "never included" are conflated. The system must distinguish them per document, by tracking each document's own Vstream history.
