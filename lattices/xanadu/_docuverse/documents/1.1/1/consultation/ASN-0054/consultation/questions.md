# Sub-Questions — Arrangements

**Inquiry:** What structural properties does a document's arrangement have? How do contiguous mappings decompose, and what invariants govern the shape of the arrangement domain?

1. [nelson] Must every document's content occupy a single unbroken sequence of positions, or can a document's address space contain gaps where no content exists?
2. [nelson] When a document maps several consecutive positions to content that originates from different sources, is there a unique way to split that mapping into the fewest contiguous pieces that each reference one original span?
3. [nelson] If two adjacent pieces in a document both reference content from the same original, and that original content was itself contiguous, must those two pieces be merged into one?
4. [nelson] Can a single piece within a document's arrangement map to content of any length, or is there a maximum or minimum size that the design imposes on one contiguous mapping?
5. [nelson] Must the pieces that compose a document's arrangement be non-overlapping — that is, can a single document position ever be claimed by more than one piece simultaneously?
6. [nelson] Does the design require that the pieces of a document's arrangement follow the same order as the document's positions, with no piece's domain preceding another's yet following it in the content sequence?
7. [nelson] If a document is edited so that content is inserted in the middle, what happens to the arrangement's existing pieces — must exactly one piece split into two, or can the restructuring be more complex?
8. [nelson] When content is deleted from a document, must the remaining pieces close the gap so the document's positions stay contiguous, or can the deletion leave a hole in the address space?
9. [nelson] Is an empty document — one with no content at all — represented by an arrangement with zero pieces, or must every document always contain at least one piece?
10. [nelson] When two documents share the same original content, must their arrangements reference that content identically, or can each document's arrangement decompose the shared content into differently sized pieces?
11. [gregory] In a well-formed POOM, can two bottom crums ever have overlapping V-displacement ranges, or does `insertpm` guarantee that V-spans are strictly non-overlapping — and if so, which code path enforces this?
12. [gregory] When `isanextensionnd` coalesces a new entry with an existing bottom crum, does it always extend the V-width and I-width symmetrically — that is, does a single bottom crum always represent a 1:1 mapping where V-width equals I-width in magnitude?
13. [gregory] After a sequence of INSERT, DELETE, and COPY operations, can gaps exist in the V-address domain of a document's text subspace — positions with no POOM entry — or is the V-domain always a single contiguous interval from minimum to maximum?
14. [gregory] Does `slicecbcpm` always produce exactly two pieces when cutting a bottom crum at an interior point, and are both pieces guaranteed to have positive widths, or can degenerate zero-width fragments survive?
15. [gregory] When COPY brings in a multi-span specset where some source spans happen to be I-address-contiguous with existing target POOM entries, does `isanextensionnd` coalesce across the specset boundary — merging the last byte of one copied span with the first byte of the next if they are I-adjacent?
16. [gregory] Is there an ordering invariant on sibling bottom crums within a single POOM loaf — must their V-displacements be sorted left-to-right, or does `incontextlistnd` compensate for arbitrary physical ordering during retrieval?
17. [gregory] After REARRANGE with a 3-cut pivot, can a single pre-existing bottom crum that straddled a cut boundary end up split into two non-contiguous entries in V-space while still referencing a contiguous I-address range — and if so, is there any post-rearrange coalescing pass?
18. [gregory] When DELETE slices a bottom crum that maps to a contiguous I-span, does the surviving fragment preserve exact I-displacement and I-width corresponding to the surviving V-range, or is there any rounding or alignment to tumbler boundaries?
19. [gregory] In the 2D POOM enfilade, does the root's I-displacement track the minimum I-address across all entries via `setwispnd`, and does this minimum ever become stale after DELETE removes the entry that held the minimum?
20. [gregory] When a document contains both text entries (subspace 1.x) and link entries (subspace 0.2.x) in the same POOM tree, are these stored as interleaved siblings in shared loafs sorted by V-displacement, or does the tree naturally partition them into separate subtrees due to the tumbler ordering of `0.2.x < 1.x`?
