## Question 4 [nelson]

> Can a single piece within a document's arrangement map to content of any length, or is there a maximum or minimum size that the design imposes on one contiguous mapping?

## No Minimum or Maximum Size on a Contiguous Mapping

The design imposes **no size constraint** on a single contiguous piece within a document's arrangement. A span — the unit that describes a contiguous region — can range from one byte to the entire docuverse.

Nelson states this explicitly:

> "In fact, a tumbler-span may range in possible size from one byte to the whole docuverse on the whole network." [LM 4/24]

The V-stream (a document's current arrangement) is composed of vspans — contiguous sequences of bytes mapped to I-space content:

> "Logical addressing of the byte stream is in the form of virtual spans, or vspans. These are sequences of bytes in the document's virtual byte stream, regardless of their native origin." [LM 4/11]

Each vspan can reference native bytes (created in this document) or non-native bytes (transcluded from elsewhere), and there is no distinction in how they participate in the arrangement:

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document." [LM 4/11]

### Why no constraint exists

The addressing system is built on humbers (arbitrary-precision integers) and tumblers (sequences of humbers). A span is defined by two tumbler boundaries, not by a count:

> "A tumbler-span is not a conventional number, and it does not designate the number of bytes contained. It does not designate a number of anything." [LM 4/24]

Since humbers have no upper limit ("as large as it needs to be when the number is big" [LM 4/13]) and a span is just a pair of tumbler addresses, there is no structural ceiling. And since the smallest addressable unit is a single byte (the element level of the tumbler), one byte is the natural floor.

### Practical illustration

Nelson's Shakespeare example demonstrates both extremes in one document. E.G. Jewett's modified Hamlet consists of a transclusion spanning nearly the entire play (thousands of bytes in one contiguous mapping), then a single word "luge" (a few bytes of native content), then another large transclusion of the remainder. The system handles a mapping of one word and a mapping of most of a play with identical machinery.

> "A span that contains nothing today may at a later time contain a million documents." [LM 4/25]

This reinforces that the design is deliberately unconstrained — spans are defined by boundaries in an ever-growing address space, not by fixed-size units.
