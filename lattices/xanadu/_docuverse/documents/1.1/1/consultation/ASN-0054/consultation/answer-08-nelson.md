## Question 8 [nelson]

> When content is deleted from a document, must the remaining pieces close the gap so the document's positions stay contiguous, or can the deletion leave a hole in the address space?

## The gap closes. V-space positions are always contiguous.

Deletion in Xanadu removes content from the document's **V-space** (virtual byte stream) — the current arrangement the user sees. The remaining positions close up to maintain a dense, gap-free sequence. Nothing happens to **I-space** — the permanent content store.

### Evidence from the specification

**1. V-space is defined as always contiguous.**

The virtual byte stream is exactly that — a *stream*. Positions always run from 1 through *n* with no holes:

> "Logical addressing of the byte stream is in the form of virtual spans, or vspans. These are sequences of bytes in the document's virtual byte stream, regardless of their native origin." [LM 4/11]

**2. INSERT explicitly renumbers, so DELETE must too.**

The INSERT operation states:

> "The v-stream addresses of any following characters in the document are increased by the length of the inserted text." [LM 4/66]

If insertion shifts all subsequent addresses *forward*, deletion must shift them *back*. The V-stream is a logical sequence that reflows on every edit — there is no fixed grid with permanent slots.

**3. V-addresses are ephemeral by design.**

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." [LM 4/11]

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." [LM 4/30]

V-addresses *routinely* change. They are not permanent identifiers — they are positions in the current arrangement. A hole would contradict this: it would mean a V-address persists even after the content it addressed is gone.

**4. Deleted bytes still exist — just not in V-space.**

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

The content is *not currently addressable* in this document's V-stream. It hasn't been destroyed — it lives on at its permanent I-address, accessible through old versions, through other documents that transclude it, and through links that point to its I-address.

### Why this matters architecturally

The V-space/I-space separation is precisely what makes gap-closing safe:

- **V-space** is a *view* — a mapping from sequential positions to I-addresses. Edits change the mapping. Gaps in a mapping are meaningless.
- **I-space** is *permanent* — append-only, never rewritten, never compacted. I-addresses never become invalid.
- **Links** point to **I-addresses**, not V-addresses. So closing the V-space gap cannot break any link.

If V-space left holes, it would undermine the entire model. The document would no longer be a coherent byte stream — it would be a sparse array with undefined positions. Front-end applications would need to handle gaps in what is supposed to be sequential text. And there would be no benefit: the content is already preserved in I-space regardless.

### The analogy

Think of it like a reading list. If you remove item 3 from a 5-item list, items 4 and 5 become the new 3 and 4. The list stays dense. The *books themselves* (I-space) haven't moved — they're still on the same shelves. You've only changed the list (V-space).
