## Question 5 [nelson]

> Must the pieces that compose a document's arrangement be non-overlapping — that is, can a single document position ever be claimed by more than one piece simultaneously?

## No — V-stream positions are non-overlapping by design

The V-stream (a document's current arrangement) is explicitly a **byte stream with ordinal positions**. Each position maps to exactly one I-space byte. Nelson describes it as:

> "Logical addressing of the byte stream is in the form of virtual spans, or vspans. These are sequences of bytes in the document's virtual byte stream, regardless of their native origin." [LM 4/11]

> "The digit after the one indicates the byte position in the current ordering of bytes. This is its virtual stream address." [LM 4/30]

The V-stream is dense and contiguous — no gaps, no overlaps. Every byte (whether native or transcluded) gets exactly one ordinal position:

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document." [LM 4/11]

### Evidence from the editing operations

The FEBE operations confirm this structurally:

- **INSERT** shifts subsequent addresses: "The v-stream addresses of any following characters in the document are increased by the length of the inserted text." [LM 4/66] — This only makes sense if each position is occupied by exactly one byte.

- **REARRANGE** uses cuts that partition the stream into non-overlapping regions, then transposes them. [LM 4/67]

- **DELETEVSPAN** removes a span and the stream closes up — no gaps left behind.

All three operations treat the V-stream as a total ordering where each position is uniquely occupied.

### The V→I mapping is a function, not a relation

The POOM enfilade maps V-addresses to I-addresses. A document IS this mapping. Each V-position resolves to exactly one I-position — it is a function, not a many-to-one or many-to-many relation.

### The important converse: I-space CAN be multiply referenced

While each V-position maps to one I-byte, the **same I-byte can appear at multiple V-positions** — both within a single document and across documents. This is transclusion (COPY). Two V-positions pointing to the same I-address is not overlap; it's two distinct positions in the arrangement that happen to reference the same permanent content.

### Summary

A document's V-stream is a sequence. Each position is claimed by exactly one piece. The pieces that compose the arrangement are non-overlapping and contiguous. Overlap is structurally impossible given Nelson's byte-stream model with ordinal addressing.
