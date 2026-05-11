## Question 5 [theory]

> Did Nelson intend the link subspace's V-positions to be dense and contiguous (like the text subspace), or sparse/keyed by some other principle that would make D-CTG and D-MIN inapplicable?

# Link Subspace V-Positions: Sparse, Not Dense

Nelson's design treats the link subspace fundamentally differently from the text subspace. **Links are addressed by permanent order of arrival, not by current position**, which makes the subspace sparse rather than dense/contiguous.

## Direct evidence from Nelson

The verified quote from LM 4/31 (in `links.md`):

> "The links designated by a tumbler address are in their permanent order of arrival. A document includes only the links of which it is the home document." [LM 4/31]

The address examples Nelson gives:

> "N.0.U.0.D.V.0.2.1 (the first link of the document, stored in the document's space)" [LM 4/31]
>
> "N.0.U.0.D.V.0.2.755 (the 755th link to which the document is home)" [LM 4/31]

## Contrast with bytes (text subspace)

For bytes Nelson says explicitly:

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." [LM 4/30]

> "The v-stream addresses of any following characters in the document are increased by the length of the inserted text." [LM 4/66]

Bytes are **renumbered** by INSERT/DELETE — addresses 1..N stay dense. Links are **not** — once assigned `0.2.5`, that number is permanent.

## Why this means sparse

Combining two facts from the curated sources:

1. Link deletion is supported. Per LM 4/9: *"DELETED LINKS (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)"*
2. Link addresses are permanent (4/31, above).

So deleting link `0.2.5` from a document that holds `0.2.1..0.2.755` leaves a gap at position 5. The subspace is keyed by arrival ordinal, with holes where deletions occurred.

The `i-space-addresses.md` summary captures this as: *"links are currently not rearrangeable"* — and crucially, the same property that prevents rearrangement (permanence of ordinal) also prevents the renumber-to-close-gap behavior that keeps the byte subspace contiguous.

## Implication for D-CTG and D-MIN

If D-CTG asserts that V-positions form a contiguous range and D-MIN asserts the range starts at 1 with no gaps, **both properties hold for the text subspace but not for the link subspace under Nelson's design**. The link subspace satisfies a weaker invariant: monotonic assignment by creation order, with deletions producing tombstones rather than gaps closing.

## Caveat

Nelson does not use the words "dense" or "sparse" and does not directly state "deletion leaves gaps." The sparseness is an unavoidable consequence of combining (a) permanent arrival-order addressing [4/31] with (b) deletability of links [4/9]. NEED_RAW: 4/31 if you want a single page that nails this down explicitly — the surrounding text on raw page 191 may clarify whether Nelson contemplates gap-closing or treats sparseness as inherent.
