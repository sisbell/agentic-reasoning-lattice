## Question 5 [theory]

> How must the ordering of the document be preserved across an insertion, so that everything before the insertion point keeps its prior order and everything after it shifts consistently?

The ordering is preserved at the **Vstream (virtual stream) level**: insertion splits the document at the insertion point, leaves the prefix addresses untouched, and shifts every following address by exactly the length of the inserted text — preserving relative order within both segments.

## The INSERT rule

Nelson's FEBE specification states the invariant precisely:

> "This inserts `<text set>` in document `<doc id>` at `<doc vsa>`. The v-stream addresses of any following characters in the document are increased by the length of the inserted text." (4/66)

This gives three guarantees that together preserve ordering:

1. **Prefix unchanged** — Everything before the insertion point keeps its prior V-addresses. No byte before the cut moves.
2. **Suffix shifts uniformly** — Everything after the insertion point has its V-address "increased by the length of the inserted text." Because every following character shifts by the *same* amount, their relative order is preserved.
3. **Density maintained** — The Vstream remains a contiguous sequence with no gaps; the inserted span fills exactly the addresses opened up between prefix and shifted suffix.

## Why this works: identity vs. arrangement

The shifting happens only in the *arrangement* (Vstream), not in *identity* (Istream). The bytes' permanent I-addresses never change — only their position in the current ordering:

> "The digit after the one indicates the byte position in the current ordering of bytes. This is its virtual stream address." (4/30)

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." (4/30)

And from the user/front-end perspective, this V-address reshuffling is invisible to identity:

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." (4/11)

## The consequence for links

Because ordering is preserved through a uniform shift rather than rewriting content, links survive the insertion. Links attach to bytes (I-addresses), not to V-positions:

> "A Xanadu link is not between points, but between spans of data... it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them." (4/42)

The page-4/43 annotation confirms insertion specifically:

> "Links between bytes can survive deletions, insertions and rearrangements, **if anything is left at each end.**" (4/43)

## Summary

The ordering invariant for an insertion at position *p* with inserted length *L*:
- For any byte at V-address *v* where *v < p*: address unchanged.
- For any byte at V-address *v* where *v ≥ p*: new address = *v + L*.
- Relative order within each segment is preserved because the prefix is untouched and the suffix is shifted by a single uniform constant.

Identity (Istream) is invariant throughout; only the V→I arrangement mapping is rewritten.
