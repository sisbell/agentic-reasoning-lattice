## Question 9 [nelson]

> When content is shared across documents, must each document's mapping to that content be independent, so that rearranging content in one document cannot alter the mapping in another?

## Yes — Absolutely and by Design

Each document's Vstream mapping to shared Istream content is independent. Rearranging content in one document cannot alter any other document's mapping. This is not merely a desirable property but a structural consequence of the Istream/Vstream separation.

### The Architecture Guarantees It

A document IS its V→I mapping. Each document maintains its own independent arrangement of references to permanent Istream content:

> "The virtual byte stream of a document may include bytes from any other document." [LM 4/10]

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

Each document's Vstream is a separate reading list pointing into the same shared library. Two documents can reference identical Istream bytes while arranging them in completely different orders — and neither arrangement constrains the other.

### Nelson States This Explicitly

The clearest statement comes in the context of deletion:

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

If even deletion — the most destructive Vstream operation — cannot affect other documents' mappings, then rearrangement certainly cannot.

### Editing Operations Are Document-Scoped

Every editing operation in FEBE takes a specific `<doc id>` and operates only on that document's Vstream:

> "This inserts \<text set\> in document \<doc id\> at \<doc vsa\>. The v-stream addresses of any following characters **in the document** are increased by the length of the inserted text." [LM 4/66]

> "This removes the given span from **the given document**." [LM 4/66]

The V-address shifts caused by insertion or deletion propagate within the affected document only. Other documents referencing the same Istream content are untouched.

### Why This Must Be So

Three of Nelson's fundamental guarantees depend on mapping independence:

1. **Ownership** — "Only the owner has a right to withdraw a document or change it." [LM 2/29] If Alice's edits could alter Bob's document's mapping, Alice would be changing Bob's document without ownership.

2. **Non-destruction** — "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate — without damaging the originals. This is done by inclusion links." [LM 2/45] If mappings were coupled, modifications *would* damage originals.

3. **Version integrity** — "The integrity of each document is maintained by keeping the two aspects separate: derivative documents are permanently defined (and stored) in terms of the originals and the changes." [LM 2/37]

### The Mechanism

The Istream/Vstream separation makes this natural rather than enforced:

- **Istream is immutable** — content at an I-address never changes
- **Vstream is per-document** — each document holds its own V→I mapping
- **Transclusion creates a new mapping entry**, not a shared pointer into another document's Vstream

When Document B transcludes content from Document A, Document B gets its own Vstream entries pointing to the same Istream addresses that Document A points to. The two Vstream mappings share a destination (the I-addresses) but are structurally independent paths to that destination. Editing either document's Vstream is a local operation on that document's mapping alone.

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." [LM 4/11]

V-addresses are ephemeral and local. I-addresses are permanent and global. The independence of mappings follows directly from this separation.
