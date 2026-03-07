## Question 5 [nelson]

> When a document undergoes a series of edits across multiple versions, must every piece of surviving content retain the same address it had in the original version?

# Address Permanence Across Versions

The answer depends on **which address space** you mean. Xanadu has two, and they behave oppositely.

## I-Space Addresses: Yes, Permanent Forever

Every byte ever created gets a permanent I-space address that never changes, regardless of what happens to any document or version. This is the foundational guarantee of the entire architecture.

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

The I-address encodes origin (Node.0.User.0.Document.0.Element) and is immutable. A byte created in document D at I-position 47 stays at that I-address through every version, every transclusion, every edit — forever.

## V-Space Addresses: No, They Change Constantly

V-space addresses are explicitly ephemeral. Nelson says so directly:

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." [LM 4/11]

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." [LM 4/30]

The INSERT operation specification makes this concrete:

> "The v-stream addresses of any following characters in the document are increased by the length of the inserted text." [LM 4/66]

Insert 10 bytes at V-position 5, and everything after position 5 shifts by 10. V-addresses are dense sequential positions (1, 2, 3...) that reflow with every edit.

## The Architecture Depends on This Distinction

The whole design rests on separating **identity** (I-space, permanent) from **arrangement** (V-space, mutable):

- **Links point to I-space** → survive editing
- **Users work with V-space** → intuitive sequential positions
- **Versions are different V-space arrangements** over the same I-space content
- **"Deletion" removes from V-space only** → I-space content persists

> "Links between bytes can survive deletions, insertions and rearrangements, if anything is left at each end." [LM 4/42-4/43]

Links survive precisely *because* they attach to permanent I-addresses, not shifting V-addresses. If links pointed to V-positions, every insertion would break every link after the insertion point.

## Each Version Has Its Own V-Space

When you create a new version (CREATENEWVERSION), you get a new V-space arrangement that initially mirrors the source. Subsequent edits to either version change only that version's V-space. The underlying I-space content is shared.

> "There is thus no 'basic' version of a document set apart from other versions—'alternative' versions—any more than one arrangement of the same materials is a priori better than other arrangements." [LM 2/19]

## Summary

| Address type | Survives editing? | Survives versioning? |
|---|---|---|
| **I-space** (identity) | Yes — permanent, immutable | Yes — shared across all versions |
| **V-space** (arrangement) | No — shifts on every edit | Each version has its own V-stream |

Every piece of surviving content retains its **I-space address** permanently. Its **V-space position** changes with every edit and differs across versions. This is not a limitation — it is the core architectural insight that makes permanent linking, version comparison, and transclusion possible.
