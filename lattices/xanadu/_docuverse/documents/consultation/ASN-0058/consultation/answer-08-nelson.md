## Question 8 [nelson]

> If a document contains content from multiple original creation events, must the boundaries between mapping units align exactly with the boundaries between those distinct creation events?

## No — Nelson does not require mapping unit boundaries to align with creation event boundaries

The V→I mapping is defined by the **current arrangement** of content, not by how or when content entered Istream. Nelson's design is explicit on this point.

### The key statement

> "Logical addressing of the byte stream is in the form of virtual spans, or vspans. These are sequences of bytes in the document's virtual byte stream, **regardless of their native origin.**"
> — [LM 4/11]

Vspans are defined by position in the virtual stream. The system does not require — or even expose to the front end — where creation event boundaries fall within those spans.

### What determines mapping boundaries

The V→I mapping tracks which I-address each V-position resolves to. In any span-based representation, a new mapping entry is needed whenever the I-address sequence becomes **discontinuous** in V-order. This discontinuity arises from the *arrangement*, not from creation history per se.

Consider: if two consecutive INSERTs to the same document produce I-addresses D.0.1.5 through D.0.1.10 and D.0.1.11 through D.0.1.15, and both runs remain adjacent in V-space, the I-addresses form a single contiguous range (D.0.1.5 through D.0.1.15). Nothing in Nelson's design requires a mapping boundary between them, even though they came from distinct creation events.

Conversely, a single REARRANGE operation can split one creation event's bytes across non-adjacent V-positions, forcing multiple mapping entries for content from one event:

> "Rearrange transposes two regions of text."
> — [LM 4/67]

### The front end doesn't see I-addresses at all

Nelson explicitly shields the user layer from I-space details:

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this."
> — [LM 4/11]

The front end works entirely in V-addresses. Whether a contiguous V-range maps to one or many I-ranges — and whether those I-ranges came from one or many creation events — is invisible at the protocol level.

### What the system *does* track

The system tracks **I-address identity**, not creation event history. This is what enables correspondence:

> "A facility that holds multiple versions of the same material, and allows historical backtrack, is not terribly useful unless it can help you intercompare them in detail — unless it can show you, word for word, what parts of two versions are the same."
> — [LM 2/20]

Correspondence works by comparing I-addresses across versions. Two V-positions correspond if they map to the same I-address. The system doesn't need to know *when* those I-addresses were created — only *that they are the same*.

### Why the distinction matters

In practice, distinct creation events almost always produce non-contiguous I-addresses (because the append-only store interleaves content from all documents chronologically: [LM 2/14]). So mapping boundaries and creation event boundaries usually coincide. But this is a **practical consequence** of the append-only storage model, not a **design requirement** of the V→I mapping.

The two cases where they diverge:

1. **Consecutive appends to the same document** with no intervening operations — I-addresses are contiguous, so a single mapping unit suffices despite multiple creation events
2. **REARRANGE splitting a creation event** — one event's bytes end up in non-adjacent V-positions, requiring multiple mapping units for a single event

### Summary

Nelson defines the V→I mapping in terms of I-address identity and V-position, not creation event provenance. Mapping unit boundaries are determined by I-address contiguity in V-order. Creation events determine *which I-addresses exist*; the arrangement determines *how they map*. These are independent concerns in Nelson's architecture.
