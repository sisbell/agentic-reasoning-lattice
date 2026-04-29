## Question 1 [nelson]

> When segments of a document's content stream are rearranged by cut points, does every byte of content retain its original identity, or does the act of repositioning create new content?

## Every byte retains its original identity. Rearrangement is purely a Vstream operation.

This is one of the clearest consequences of the Istream/Vstream separation. When you rearrange content, you change the **arrangement** (Vstream mapping), not the **content** (Istream addresses). The bytes themselves are untouched.

### The architectural basis

Content lives permanently in Istream. A document's Vstream is a mapping — an ordered sequence of references to Istream addresses. Rearranging cut-point regions changes which Istream addresses appear at which Vstream positions, but the Istream content is immutable:

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." [LM 4/30]

The REARRANGE operation transposes regions of the virtual byte stream:

> "Rearrange transposes two regions of text. With three cuts, the two regions are from cut 1 to cut 2, and from cut 2 to cut 3... With four cuts, the regions are from cut 1 to cut 2, and from cut 3 to cut 4." [LM 4/67]

This is a pure remapping. The V-addresses shift; the I-addresses do not.

### Why this must be so

Three guarantees depend on content identity surviving rearrangement:

1. **Link survivability.** Links attach to bytes via I-addresses. If rearrangement created new content, links would break on every edit. Instead:

   > "Links between bytes can survive deletions, insertions and rearrangements, if anything is left at each end." [LM 4/43]

2. **Correspondence across versions.** Version comparison works because shared I-addresses identify "the same content." If rearrangement generated new I-addresses, two versions differing only in paragraph order would appear to share nothing — defeating the entire intercomparison facility:

   > "A facility that holds multiple versions of the same material, and allows historical backtrack, is not terribly useful unless it can help you intercompare them in detail — unless it can show you, word for word, what parts of two versions are the same." [LM 2/20]

3. **Transclusion integrity.** If document B transcludes a span from document A, and document A rearranges that span's position, the transclusion must still resolve. It does, because B's reference is to the I-address, which is unaffected by A's Vstream changes:

   > "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

### The analogy

Think of a library and a reading list. Rearranging the reading list changes the order you encounter the books — it does not create new books. The library stacks (Istream) never change. The reading lists (Vstream) can be reordered freely.

### Summary

Repositioning content is an operation on the **view**, not on the **content**. The Istream is append-only — bytes are added, never overwritten, never regenerated. Every editorial operation (insert, delete, rearrange, copy) changes the Vstream mapping while leaving the permanent Istream identity of every byte intact. This is not a design choice that could have gone either way; it is the foundation on which permanence, link survivability, correspondence, and transclusion all rest.
