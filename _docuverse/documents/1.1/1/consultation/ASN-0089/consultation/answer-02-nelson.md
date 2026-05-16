## Question 2 [nelson]

> After insertion, if a reader retrieves the document, must the new content appear at exactly the specified position with all prior content in its original relative order on either side?

## Yes — Nelson specifies this explicitly.

The INSERT command definition at [LM 4/66] states:

> "This inserts \<text set\> in document \<doc id\> at \<doc vsa\>. The v-stream addresses of any following characters in the document are increased by the length of the inserted text."

This gives three guarantees:

1. **New content appears at the specified V-address.** The `<doc vsa>` parameter is the exact Vstream position where the inserted text will begin.

2. **Content before the insertion point is undisturbed.** V-addresses 1 through P-1 remain unchanged — Nelson says only "following characters" are affected.

3. **Content after the insertion point preserves its relative order**, shifted uniformly by the insertion length. "Increased by the length of the inserted text" means every post-insertion byte shifts by the same amount, preserving their relative ordering exactly.

### Why this follows from the Vstream model

The Vstream is always a dense, contiguous sequence. Nelson at [LM 4/30]:

> "The digit after the one indicates the byte position in the current ordering of bytes. This is its virtual stream address."

There are no gaps in V-addresses. If you have N bytes, you have positions 1 through N. After inserting `len` bytes at position P, the result is positions 1 through N+len, with the new content occupying P through P+len-1 and the formerly-at-P-and-after content occupying P+len through N+len.

### Istream is unaffected

At [LM 4/11]:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control."

INSERT adds new bytes to Istream (append-only storage) and updates the Vstream mapping to splice them in. No prior Istream content is moved or altered. The shift is purely a Vstream phenomenon — the mapping from virtual positions to permanent content addresses is updated.

This is further confirmed by the link survivability guarantee at [LM 4/30]:

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them."

Links survive insertion precisely because they point to Istream addresses (permanent), not Vstream positions (which shift). The prior content's identity is unchanged; only its virtual position moves.

### Summary

After INSERT at position P with content of length L:
- V-positions 1..P-1: unchanged (same content, same addresses)
- V-positions P..P+L-1: the new content
- V-positions P+L..N+L: the prior content that was at P..N, in original relative order

This is not inferred — it is the direct, specified semantics of INSERT at [LM 4/66].
