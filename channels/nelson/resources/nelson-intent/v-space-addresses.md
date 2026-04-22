# Vstream (Version Space / Virtual Space)

Source: Literary Machines, 4/10-4/11, 4/30, 4/66-4/67

## What It Means

Vstream is the document's current arrangement of content. V-addresses specify positions in the "virtual byte stream" — the logical sequence as the user sees it now.

- **Ephemeral**: V-addresses change during editing
- **Dense**: V-addresses always form a contiguous sequence starting at 1
- **View-based**: Vstream is a view over permanent Istream content
- **Per-version**: Each version has its own V-stream arrangement

The mapping V -> I is the essence of document structure. The document IS the mapping from V-addresses to I-addresses. Each version defines a different mapping. Edits change the mapping, not the Istream content.

## User Guarantee

- V-address 1 is always the first byte of the document right now
- There are no gaps — if you have 100 bytes, you have addresses 1 through 100
- INSERT shifts addresses after the insertion point
- DELETE removes addresses (closing the gap)
- The same content gets different V-addresses after edits

## Principle Served

Separation of identity from arrangement. Vstream lets users edit freely while Istream preserves identity. Links point to I-addresses (survive editing), users work with V-addresses (intuitive positions), versions are different V-arrangements over shared I-content.

## Nelson's Words

> "Logical addressing of the byte stream is in the form of virtual spans, or vspans. These are sequences of bytes in the document's virtual byte stream, regardless of their native origin." (4/11)

> "The digit after the one indicates the byte position in the current ordering of bytes. This is its virtual stream address." (4/30)

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." (4/30)

> "The v-stream addresses of any following characters in the document are increased by the length of the inserted text." (4/66)

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." (4/11)

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document." (4/11)
