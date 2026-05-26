## Question 1 [nelson]

> When new content is inserted at a position in a document's stream, does every byte of the existing content retain its original permanent identity, or does shifting content to make room assign new identities?

## Every byte retains its permanent identity. Insertion never reassigns existing identities.

This is the entire point of the Istream/Vstream separation. The two address spaces serve different purposes:

- **Istream** — where content **permanently lives**. Addresses are absolute and immutable. Content at an Istream address never changes. [LM 4/10-4/11]
- **Vstream** — the document's **current arrangement**. A view that references Istream content. Can be rearranged across versions. [LM 4/10-4/11]

### What INSERT actually does

Nelson's specification of INSERT is explicit:

> "This inserts \<text set\> in document \<doc id\> at \<doc vsa\>. The v-stream addresses of any following characters in the document are increased by the length of the inserted text." [LM 4/66]

Three things happen:

1. **New content gets fresh I-addresses.** The inserted bytes are appended to Istream — the append-only store where content permanently resides. Nelson: "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

2. **Vstream addresses shift.** Following characters get higher V-addresses. This is purely a change to the document's arrangement — which positions in the virtual byte stream map to which permanent content.

3. **Istream addresses of existing bytes are untouched.** The bytes that were already in the document retain their permanent identities exactly as before.

### Nelson says this explicitly

On V-addresses changing while identity is preserved:

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." [LM 4/30]

On V-addresses being ephemeral:

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." [LM 4/11]

This quote is about V-addresses (the "address of a byte in its native document" refers to the byte's position in the current arrangement). The I-address — where the byte permanently lives — never changes.

### Why this matters: link survivability

The guarantee that existing bytes retain their identities is what makes link survivability possible:

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes. This has a crucial advantage: it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them." [LM 4/42]

If insertion reassigned I-addresses to existing bytes, links would break on every edit. The entire link survivability guarantee depends on content identity being invariant under editing operations.

### The library analogy

Think of it as Nelson's library stacks versus reading lists:

- **Istream (library stacks):** Each book has a permanent shelf location. Adding a new book means placing it on a **new** shelf. You never move existing books.
- **Vstream (reading list):** Your reading list references shelf locations. Inserting a new reference at position 3 shifts items 3, 4, 5... to positions 4, 5, 6... But the books on the shelves haven't moved.

### Summary

| What changes on INSERT | What does NOT change |
|---|---|
| V-addresses of following bytes (shift up) | I-addresses of any existing bytes |
| The V→I mapping (new entries added) | Content stored at existing I-addresses |
| The document's current arrangement | Links attached to existing bytes |

The document IS the mapping from V-addresses to I-addresses [LM 4/10-4/11]. INSERT modifies that mapping by adding new entries and shifting existing V-positions. It never touches the Istream content or its addresses.
