## Question 10 [theory]

> When a link's endpoint spans a portion of a document that is partially edited, must the link still be counted under its original from/to/type description?

## Short answer

Yes—provided at least one byte survives at that endpoint. A link's endsets point to permanent Istream addresses, not to document positions, and Xanadu's search mechanism matches on those addresses. So as long as any of the bytes the link is attached to remain after partial editing, the link is still counted under its original from/to/type description.

## Why

**Links attach to bytes, not positions.** A Xanadu link is a "strap between bytes," and that is precisely what lets it survive editing:

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes. This has a crucial advantage: it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them. This also works for alternative versions in which part of each end has survived." (4/42)

The qualifier "if any of the bytes are left" is the operative condition. Partial editing that removes *some* of the spanned content does not break the link, because the remaining bytes still carry it. The survivability annotation on page 4/43 states this directly:

> "SURVIVABILITY: Links between bytes can survive deletions, insertions and rearrangements, **if anything is left at each end.**" (4/43)

**The from/to/type description is address-based.** The reason the link still counts under its *original* description is that endsets map to fixed positions on the tumbler line (Istream), and search matches on addresses—not on the current Vstream arrangement or on what is stored:

> "What the 'type' designation points to is completely arbitrary. This is because of the way we will be searching for links. The search mechanism does not actually look at what is stored under the 'type' it is searching for; it merely considers the type's address." (4/44–4/45)

Because the surviving bytes retain their permanent I-addresses through editing, the link's from-set, to-set, and type still point where they always did.

**The search-satisfaction rule confirms partial survival is sufficient.** Nelson's link-search model requires only that *one span of each endset* satisfy the request—not that the endset be intact:

> "A link satisfies a search request if one span of each endset satisfies a corresponding part of the request." (4/58)

So if a from-set originally covered a paragraph and editing deletes half of it, the surviving span still satisfies a request constrained to that region. The link continues to be counted.

## The boundary case

The single exception is total deletion of an endpoint. If *all* bytes at one end are removed, nothing remains for the strap to hold, and the link no longer has a surviving span there. Even then, the deletion is a Vstream operation—the bytes persist in Istream "awaiting historical backtrack functions" and "may remain included in other versions," so the link is recoverable in any version where its endpoint content survives. But for the current edited version's search, an endset with nothing left is no longer satisfiable.

## Summary

| Editing outcome at an endpoint | Counted under original from/to/type? |
|---|---|
| Part of the span survives | Yes — link remains attached to surviving bytes (4/42, 4/43) |
| Span rearranged/shifted | Yes — addresses are content-based, not positional (4/44–4/45) |
| Entire span deleted | No surviving span to satisfy search; recoverable only via versions where content remains (4/9) |
