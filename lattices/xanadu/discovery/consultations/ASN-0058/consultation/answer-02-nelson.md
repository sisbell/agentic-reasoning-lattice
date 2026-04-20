## Question 2 [nelson]

> If a mapping unit pairs a region of a document with its original content, must both sides of that pairing always describe the same number of characters?

## Yes — both sides must always describe the same number of bytes.

This is a structural consequence of how Istream and Vstream relate. The Vstream is a byte-level view over Istream content. Each position in the virtual byte stream corresponds to exactly one byte in the identity stream. A mapping unit groups a contiguous run of these 1:1 correspondences into a single pair of spans for efficiency, but the width is always equal on both sides.

### Why this must be so

The Vstream is defined as a sequence of byte positions, each of which resolves to a specific Istream byte:

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document." [LM 4/11]

> "Logical addressing of the byte stream is in the form of virtual spans, or vspans. These are sequences of bytes in the document's virtual byte stream, regardless of their native origin." [LM 4/11]

Every V-position maps to one I-position. A mapping unit that says "V-positions 1–5 correspond to I-positions 100–104" has width 5 on both sides. There is no mechanism for a single V-byte to expand into multiple I-bytes, or for a V-position to map to a zero-width I-region. The relationship is strictly bijective within each mapping unit.

### Confirmed by the editing operations

Every operation that creates or modifies mappings preserves this width equality:

- **INSERT**: Creates new Istream bytes and new Vstream positions. "The v-stream addresses of any following characters in the document are increased by the length of the inserted text." [LM 4/66] — Same length on both sides.

- **COPY** (transclusion): "The material determined by \<spec set\> is copied to the document." [LM 4/67] — Creates V-positions pointing to existing I-positions. The transcluded region has the same byte count on both sides.

- **DELETE**: Removes V-positions entirely. Istream content is unchanged. No asymmetric mapping is created — the mapping unit is simply removed from the Vstream arrangement.

- **REARRANGE**: Transposes V-regions. The mapping units are reordered but their internal width-equality is preserved.

### The deeper reason

The Vstream is not a transformation of Istream content — it is an *arrangement* of it. Nelson's analogy is clear: Istream is the library stacks (permanent shelf locations for books), Vstream is a reading list (references to those books in a chosen order). A reading list entry that says "books on shelves 100–104" always refers to exactly 5 books. You cannot have a reading list entry that refers to 3 shelves but somehow yields 7 books.

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." [LM 4/11]

The V-address changes; the I-address does not. But each V-byte always resolves to exactly one I-byte, making equal-width spans the only valid mapping unit.
