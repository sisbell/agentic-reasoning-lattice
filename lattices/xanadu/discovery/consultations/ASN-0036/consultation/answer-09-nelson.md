## Question 9 [nelson]

> When content is included in a document by reference, does the document's arrangement record the precise extent of content referenced, or only a pointer to a larger stored unit?

## The Document Records Precise Extent

The arrangement records the **precise extent** — specific I-space spans — not a pointer to a larger stored unit.

### Evidence from the COPY Operation

The COPY command (which IS the transclusion mechanism) takes a `<spec set>` — a set of spans specifying exactly which bytes to include:

> "The material determined by `<spec set>` is copied to the document determined by `<doc id>` at the address determined by `<doc vsa>`." [LM 4/67]

A spec set is a **span-set**: one or more tumbler pairs, each designating a precise range of I-space bytes. The COPY doesn't say "include document D" — it says "include bytes from I-address X to I-address Y."

### Evidence from V-Space Structure

The V-space arrangement is a mapping from V-positions to I-addresses, byte by byte:

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

> "Logical addressing of the byte stream is in the form of virtual spans, or vspans. These are sequences of bytes in the document's virtual byte stream, regardless of their native origin." [LM 4/11]

Non-native bytes occupy precise V-space positions. The system knows exactly which I-space bytes are mapped to which V-space positions — not "somewhere in document D" but "I-space addresses X through Y mapped to V-space positions A through B."

### Evidence from Span Semantics

Spans themselves are precise:

> "A span in the tumbler line, represented by two tumblers, refers to a subtree of the entire docuverse" [LM 4/24]

A span's content is "implicit in the choice of first and last point" [LM 4/25]. There is no ambiguity about what is included.

### The Enfilade Implementation

The POOM enfilade (V→I mapping) maintains precisely which I-space addresses correspond to which V-space positions. This is how the system reconstructs any version on demand — it knows exactly which bytes to fetch and in what order.

### Why This Matters

If inclusions pointed only to "document D" rather than to precise byte ranges within D, several guarantees would break:

- **Correspondence** couldn't work — SHOWRELATIONOF2VERSIONS returns "ordered pairs of spans" [LM 4/70], which requires knowing exactly which I-space bytes each version shares
- **Royalty splitting** couldn't be proportional — "the original owner and the modifier split the royalty in proportion to who wrote what, as determined automatically" [LM 2/45]
- **Part-pounce** couldn't work — the system materializes "a certain part of a certain version" [LM 2/15] by assembling precisely the right I-space bytes

The document's arrangement is a precise V→I mapping at byte granularity, not a collection of document-level pointers.
