## Question 7 [nelson]

> Is the mapping from a document's visible arrangement to the underlying stored content always recoverable — can the system always trace displayed content back to its permanent origin?

# Yes — Traceability from V-Space to I-Space Is Always Recoverable

This is one of the most fundamental architectural guarantees in Xanadu. The system is designed so that every byte visible in a document's current arrangement can always be traced back to its permanent origin. This is not an optional feature but a structural property of the addressing system itself.

## The Architectural Basis

Xanadu maintains two address spaces:

- **I-Space (Invariant Space)** — where content permanently lives. Addresses are absolute and immutable. Content at an I-space address never changes.
- **V-Space (Virtual Space)** — the document's current arrangement. A view that references I-space content. Can be rearranged across versions.

The document IS the mapping from V-addresses to I-addresses. Every version defines a different mapping. The system always holds this mapping — it is the core data structure.

> "Logical addressing of the byte stream is in the form of virtual spans, or vspans. These are sequences of bytes in the document's virtual byte stream, regardless of their native origin." [LM 4/11]

The phrase "regardless of their native origin" is key — V-space presents a seamless stream, but the system always knows where each byte actually came from.

## The I-Address Encodes Origin

Every byte's I-address is a tumbler of the form `Node.0.User.0.Document.0.Element`. The Document field directly encodes which document originally created that byte. This is not metadata attached to content — it IS the address:

> "There are four major fields, each expandable indefinitely, with three major dividers between them. These fields are Server, User, Document and Contents." [LM 4/26]

To fetch content, the system must request it from its home location:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

The retrieval mechanism itself requires knowing the origin. You cannot fetch a byte without knowing its I-address, and the I-address tells you where it came from.

## Transclusions Preserve Identity

When content is included from another document (transclusion), it retains its original I-address. The COPY operation creates a new V-space mapping to existing I-space content — it does not create new content:

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

> "The virtual byte stream of a document may include bytes from any other document." [LM 4/10]

The included bytes look the same to the user but remain traceable to their home document. Two documents with identical text created independently have DIFFERENT I-addresses. Transcluded content SHARES the same I-address. This is how the system distinguishes "wrote the same words" from "quoted from the original."

## Nelson's Explicit Guarantee

Nelson states this as a user-facing promise:

> "This world nevertheless remains simple in design. The virtuality is simple in structure and regular in layout. You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

This guarantee holds even through arbitrarily deep windowing:

> "Think of the present document as a sheet of glass. It may have writing painted on it by the present author; it may have clear glass, windowing to something else; the next pane may be in turn made of more layers of painted glass, with more windows, and so on indefinitely." [LM 2/34]

No matter how many layers deep, the I-address at the bottom traces to the original creator.

## Even "Deleted" Content Remains Traceable

The V→I mapping is recoverable even for content removed from the current view:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

DELETE removes the V-space mapping but not the I-space content. Previous versions still hold the mapping. The bytes remain at their permanent I-addresses.

## The Enfilade Implementation

The POOM enfilade maintains the V→I mapping operationally:

```
User requests V-space position 5
        │
        ▼
   POOM enfilade (V→I mapping)
        │
        ▼
   "Position 5 = I-space address X"
        │
        ▼
   GRAN enfilade (content storage)
        │
        ▼
   Returns actual bytes from X
```

Nelson describes the enfilade as keeping the system in "canonical operating condition" through all changes:

> "All changes, once made, left the file remaining in canonical order, which was an internal mandate of the system." [LM 1/34]

## The V-Address Is Ephemeral; the I-Address Is Eternal

Nelson is explicit that V-addresses shift during editing — but this does not affect traceability:

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." [LM 4/11]

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." [LM 4/30]

The V-address tells you where content appears now. The I-address tells you where it came from forever. The system always holds the mapping between them.

## Summary

The mapping from displayed content to permanent origin is not merely recoverable — it is the fundamental data structure of the system. A Xanadu document IS a V→I mapping. The enfilades maintain it. The tumbler addresses encode it. The retrieval mechanism requires it. Attribution is structural, not metadata. It cannot be severed by any operation within the system.
