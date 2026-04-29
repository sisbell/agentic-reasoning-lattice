## Question 4 [nelson]

> Does every unit of content have a stable identity that is independent of which document currently includes it or where it appears?

# Yes — Absolutely and By Design

This is one of the most clearly specified properties of Xanadu. Every unit of content has a **permanent I-space address** that is independent of which document includes it, where it appears within any document, and whether it currently appears in any document at all.

## The Two Address Spaces

Xanadu separates content identity from content arrangement through two distinct address spaces:

**I-Space (Invariant Space)** — where content permanently lives. Addresses are absolute and immutable. Content at an I-space address never changes.

**V-Space (Virtual Space)** — the document's current arrangement of content. A view that references I-space content. Can be rearranged across versions.

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." [LM 4/11]

The V-address (position in the current view) changes freely. The I-address (permanent identity) never does.

## I-Space Address Structure

Every byte gets a permanent tumbler address encoding its origin:

```
Node.0.User.0.Document.0.Element
```

> "There are four major fields, each expandable indefinitely, with three major dividers between them. These fields are Server, User, Document and Contents." [LM 4/26]

This address is assigned at creation and is **permanent**. It encodes which server, which account, which document originally created that byte.

## Identity Is Based on Creation, Not Value

Two documents with identical text created independently have **different** I-addresses. Transcluded content **shares** the same I-address. This is how the system distinguishes "wrote the same words" from "quoted from the original."

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

When content is transcluded into another document, it appears in that document's V-space but retains its original I-space identity. The content doesn't move or get copied — it is *referenced*.

## Independence from Document Inclusion

Content identity survives regardless of how many documents include it or whether any currently do:

1. **Deletion doesn't destroy identity.** DELETE removes content from V-space only. The I-space content remains forever.

   > "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

2. **Transclusion preserves identity.** When document A includes content from document B, the included bytes retain their I-addresses from B.

   > "The virtual byte stream of a document may include bytes from any other document." [LM 4/10]

3. **Origin is always traceable.** No matter where content appears, you can determine where it came from.

   > "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

## Independence from Position

V-space positions shift with every edit. I-space addresses do not:

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." [LM 4/30]

This is why links survive editing — they point to I-space identity, not V-space position.

## The Append-Only Foundation

The underlying storage model guarantees this stability:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

Content is appended, never overwritten. Every byte ever created has an eternal address. The permascroll (Nelson's term: "append-only storage system" or "hyperfile") is the physical manifestation of I-space.

## Summary

Every unit of content in Xanadu has a stable identity (its I-space address) that is:

- **Independent of which document includes it** — transclusion references the original identity
- **Independent of where it appears** — V-space position changes; I-space address does not
- **Independent of whether it currently appears anywhere** — deleted content retains its I-address
- **Permanent** — assigned at creation, never reassigned or invalidated
- **Structural** — encoded in the address itself, not metadata that can be stripped

This separation of identity from arrangement is the architectural foundation that makes permanent links, automatic attribution, version comparison, and the entire Xanadu model possible.
