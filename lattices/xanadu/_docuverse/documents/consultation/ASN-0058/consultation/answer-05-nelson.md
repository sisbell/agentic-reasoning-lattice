## Question 5 [nelson]

> Must every character position in a document map to exactly one position in the permanent content record, or can a document position exist without such a mapping?

## Every Vstream Position Maps to Exactly One Istream Position

**Yes, the mapping is total and functional.** Every character position in a document's Vstream must resolve to exactly one Istream address. A Vstream position without such a mapping is architecturally impossible—it would be a reference to nothing.

### The Document IS the Mapping

The Vstream is not an independent data structure that *happens* to reference Istream content. The document's identity at any moment IS the V→I mapping. Nelson describes the retrieval chain:

> "Logical addressing of the byte stream is in the form of virtual spans, or vspans. These are sequences of bytes in the document's virtual byte stream, regardless of their native origin." [LM 4/11]

Every byte in the virtual stream has an origin—either native (created in this document) or non-native (transcluded):

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document." [LM 4/11]

There is no third category. Every Vstream byte is either native or included—both cases resolve to a definite Istream address.

### The Enfilade Architecture Confirms This

The POOM enfilade (V→I mapping) sits between the user's request and the content store:

```
V-address → POOM → I-address → GRAN → actual bytes
```

There is no "null" case in this chain. A V-address that the POOM cannot resolve to an I-address would be a corrupted document, not a valid state.

### Operations Never Create Unmapped Positions

Every operation that adds positions to the Vstream simultaneously establishes an I-mapping:

- **INSERT** creates new Istream content AND maps new V-positions to it [LM 4/66]
- **COPY** (transclusion) maps new V-positions to *existing* Istream content [LM 4/67]
- **APPEND** adds to Istream at document end [LM 4/67]

And every operation that removes mappings closes the gap:

- **DELETE** removes V-positions entirely; "The v-stream addresses of any following characters in the document are increased [decreased]" — the Vstream contracts, leaving no holes [LM 4/66]
- **REARRANGE** transposes regions — same mappings, different V-order [LM 4/67]

No operation creates a V-position without a corresponding I-address.

### The Converse Does Not Hold

While every V-position maps to exactly one I-position, the converse is many-to-one:

- **Multiple V-positions can map to the same I-position** — this is transclusion. When document B includes content from document A, B's V-positions map to A's I-addresses.
- **I-positions can exist with no current V-mapping** — deleted content remains in Istream but has no Vstream position in the current version. Nelson explicitly describes this state: "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

### Ghost Elements Are Not Unmapped Positions

The one concept that might seem to suggest unmapped positions—ghost elements—applies to the *address hierarchy* (servers, accounts, documents), not to byte positions within a document:

> "While servers, accounts and documents logically occupy positions on the developing tumbler line, no specific element need be stored in tumbler-space to correspond to them." [LM 4/23]

Ghost elements are organizational nodes in the tumbler tree. They say "document 1.2.3 is a valid address even if empty." They do not say "position 5 in document 1.2.3 can exist without content."

### Summary

The V→I mapping is **total** (every V-position has a mapping) and **functional** (each V-position maps to exactly one I-position). A document position without an Istream mapping cannot exist—there is no operation to create one, no state to represent one, and no semantic meaning for one.
