## Question 6 [theory]

> What must the design guarantee so that a reader paging through windows never receives the same link twice and never silently skips one?

## What the design must guarantee

This is the pagination-correctness problem for link search. When a link query returns more results than fit in one batch, the reader retrieves them in pages via the paginated operation. To page through that "avalanche" without duplicates or gaps, the design must guarantee three things, all of which Nelson's architecture supplies:

### 1. A stable, total, permanent ordering of links

Pagination only has meaning if "the list" of matching links has one fixed order that never shifts between requests. Xanadu gets this from the tumbler addressing of links:

> "The links designated by a tumbler address are in their permanent order of arrival. A document includes only the links of which it is the home document." (4/31, from `links.md`)

Because every link has a permanent tumbler address in creation order, the set of links satisfying a query is a deterministically ordered list, not an unordered bag.

### 2. Cursor-based paging anchored to a *position*, not an offset

The paginated operation does not say "give me results 100–200." It says "give me the links *past this link*":

> **FINDNEXTNLINKSFROMTOTHREE**: Paginated link retrieval — "no more than `<nlinks>` items past that link on that list." (4/69, from `operations.md`)

Anchoring the next page to a specific link (a cursor) rather than a numeric offset is what prevents duplicates and skips. An offset would slide if links were inserted or removed mid-paging; a position-anchor resumes exactly where the previous page ended, regardless of what else changed.

### 3. Addresses are never reused or renumbered

The cursor stays valid only if a link's address is permanent and deletion never re-packs the sequence. Nelson's design guarantees exactly this:

> "Deleting link `2.5` doesn't renumber `2.6` through `2.N`." (from `links.md`, summarizing 4/31)

So the link you paged past keeps its address forever, and the links after it keep theirs. The next page lands precisely on the successor — nothing is counted twice, nothing falls through a gap left by renumbering.

### Why the result set itself stays coherent

The membership of "the list" is also deterministic, fixed by a stable predicate over the stable order:

> "A link satisfies a search request if one span of each endset satisfies a corresponding part of the request." (4/58, from `links.md`)

And large non-matching populations don't perturb the matching subsequence:

> "THE QUANTITY OF LINKS NOT SATISFYING A REQUEST DOES NOT IN PRINCIPLE IMPEDE SEARCH ON OTHERS." (4/60, from `links.md`)

## Summary

The no-duplicate / no-skip property is not a separate feature — it falls out of three guarantees working together: (a) links have a **permanent total order** (permanent order of arrival via tumbler addresses), (b) the paging operation uses a **cursor positioned on the last link returned** ("items past that link"), not a numeric offset, and (c) link addresses are **never reused or renumbered**, so the cursor remains valid and the successor is unambiguous. Each page resumes exactly at the boundary of the last.

---

A note on sourcing: the individual building blocks above are verified quotes (4/31, 4/58, 4/60, 4/69). Nelson does not, in the curated sources, state an explicit "a reader never receives the same link twice and never skips one" guarantee in those words — that conclusion is my synthesis of the permanent-order, cursor-paging, and non-renumbering properties. If you want Nelson's own wording on the pagination operation and its iteration semantics, NEED_RAW: 4/59-4/60, 4/69.
