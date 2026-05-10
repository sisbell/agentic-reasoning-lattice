## Question 6 [nelson]

> What is the finest granularity an address can identify — a single character, a byte, or some other atomic unit of content?

## The Byte Is the Atomic Unit

The finest granularity a tumbler address can identify is **a single byte**. Nelson is consistent and explicit about this throughout the technical specification.

### Direct Evidence

The stored entities are bytes and links — nothing smaller:

> "In the present implementation (XU.87.1), the only entities actually stored in tumbler-space are content bytes and links."
> — [LM 4/23]

V-space addresses resolve to individual byte positions:

> "The digit after the one indicates the byte position in the current ordering of bytes. This is its virtual stream address."
> — [LM 4/30]

Spans explicitly bottom out at one byte:

> "In fact, a tumbler-span may range in possible size from one byte to the whole docuverse on the whole network."
> — [LM 4/24]

Links attach to bytes, not to any finer unit:

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes."
> — [LM 4/42]

### Byte, Not Character

Nelson occasionally uses "characters" informally — for example, "spans of characters" [LM 4/24] — but the technical specification always says **bytes**. This matters because the system is media-agnostic. The same addressing works for text, images, audio, and any other digital content. A "byte" is the universal atomic unit; a "character" is one possible front-end interpretation of bytes.

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control."
> — [LM 4/11]

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document."
> — [LM 4/11]

### Summary

A tumbler address identifies a single byte. Spans address contiguous ranges of bytes. Span-sets address arbitrary (possibly discontiguous) collections of bytes. Every operation in FEBE works in terms of bytes and spans of bytes. There is no sub-byte addressing, and "character" is used only as informal shorthand — the architectural atom is the byte.
