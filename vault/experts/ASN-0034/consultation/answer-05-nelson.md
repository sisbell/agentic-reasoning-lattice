## Question 5 [nelson]

> Must a contiguous range of addresses be expressible as a compact pair (start, end), and must every such range denote an unbroken sequence of content units?

## Compact Pairs and Unbroken Sequences in Tumbler-Space

### Part 1: Compact Pair Representation — YES

Every contiguous range of tumbler addresses is expressible as a compact pair. This is the **span** mechanism, and it is fundamental to the design.

> "A span in the tumbler line, represented by two tumblers, refers to a subtree of the entire docuverse" [LM 4/24]

Nelson specifies two equivalent compact representations:

1. **Pair of tumblers** — start address and end address
2. **Address + difference tumbler** — start address plus a "width" tumbler

Tumbler arithmetic converts between these forms. The difference representation is more compact when the span is small relative to the addresses.

This compactness is a design requirement, not a convenience. The entire FEBE protocol operates on spans and span-sets. Link endsets are span-sets. Retrieval targets are span-sets. Search constraints are span-sets. Without compact pair representation, the protocol would be unworkable.

The "1-positions" reinforce this — a single span can express selections at any scale:

> "A digit of 'one' may be used to designate all of a given version, all versions of a given document, all works of a given author, all documents in a given project, all documents on a given server--or the entire docuverse." [LM 4/38]

---

### Part 2: Unbroken Sequence of Content Units — NO (at the docuverse level)

A span denotes a contiguous range of **address space**, not a contiguous sequence of **content units**. Nelson is explicit that the region a span covers may be sparse, heterogeneous, or entirely empty:

> "A span that contains nothing today may at a later time contain a million documents." [LM 4/25]

> "A tumbler-span is not a conventional number, and it does not designate the number of bytes contained. It does not designate a number of anything." [LM 4/24]

> "The first point of a span may designate a server, an account, a document or an element; so may the last point. There is no choice as to what lies between; this is implicit in the choice of first and last point." [LM 4/25]

The tumbler line is a depth-first linearization of a tree. A span cuts a contiguous region from that linearization. Within that region:

- **Ghost elements** may exist — addresses with nothing stored [LM 4/23]
- **Entire empty subtrees** may exist — accounts with no documents, servers with no content
- **Heterogeneous content** may be included — bytes, links, documents, servers all share the same line

> "While servers, accounts and documents logically occupy positions on the developing tumbler line, no specific element need be stored in tumbler-space to correspond to them. Hence we may call them ghost elements." [LM 4/23]

Nelson visualizes this as a zone:

> "A span may be visualized as a zone hanging down from the tumbler line--what is called in computer parlance a depth-first spanning tree." [LM 4/25]

The zone includes whatever populates it. The span's boundaries determine the region; the region's population is a separate fact about the state of the docuverse.

---

### The V-Stream Exception

Within a single document's **V-stream** (virtual byte stream), addresses ARE dense and contiguous. V-addresses form a gap-free sequence from position 1 to position N. There are no ghost elements in V-space. INSERT shifts subsequent addresses; DELETE closes gaps.

> "The v-stream addresses of any following characters in the document are increased by the length of the inserted text." [LM 4/66]

So a V-span within a single document version DOES denote an unbroken sequence of content units. This is by design — V-space is the user's view, and users expect sequential addressing within a document.

The distinction is:

| Space | Dense? | Span = unbroken sequence? |
|-------|--------|--------------------------|
| **V-space** (within one document version) | Yes — contiguous positions 1..N | Yes |
| **I-space** (within one document's native bytes) | Yes — append-only, sequential | Yes |
| **Tumbler-space** (across the docuverse) | No — ghost elements, empty subtrees | No |

---

### Why This Matters

For non-contiguous selections, Nelson specifies **span-sets** (collections of spans):

> "Note: if you want to designate a separated series of items exactly, including nothing else, you do this by a span-set, which is a series of spans." [LM 4/25]

This is how link endsets work — each endset is an arbitrary span-set, potentially discontiguous, potentially spanning multiple documents. The compact pair representation applies to each individual span within the set, but the set as a whole can cover arbitrary scattered regions.

---

### Summary

A contiguous range of tumbler addresses is always expressible as a compact pair — this is architecturally required. But such a range does NOT necessarily denote an unbroken sequence of content units at the docuverse level. It denotes a region of address space whose population is determined by the current state of the tree. Within a single document's V-stream, however, spans do denote unbroken sequences, because V-space is dense by construction.
