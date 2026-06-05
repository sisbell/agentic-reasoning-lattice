## Question 8 [theory]

> How must the design treat a part of the document that holds no content at all — must its extent still appear in the report, and as what?

## A zero-content part is still a span — defined by its boundaries, not its contents

Yes. In Xanadu's design, a part of a document that holds no content at all must still appear, and it appears **as a span** — designated by its two endpoints, not by any tally of what lies inside it.

The reason is foundational to how spans work. A span is never a *count* of contents; it is a *from-here-to-there* designation whose interior is implicit in its boundaries:

> "A tumbler-span is not a conventional number, and it does not designate the number of bytes contained. It does not designate a number of anything." (4/24)

> "The first point of a span may designate a server, an account, a document or an element; so may the last point. There is no choice as to what lies between; this is implicit in the choice of first and last point." (4/25)

Because the extent is fixed by the choice of first and last point, the span exists and is reportable *regardless of whether anything currently occupies it*. Nelson states this directly:

> "A span that contains nothing today may at a later time contain a million documents." (4/25)

So emptiness does not make the region disappear from a span-based report. The extent is real even when the content is null — what is reported is the boundary pair (or, equivalently, a start address plus a difference tumbler), not the absent material.

### As what, exactly?

- **As a span**, given by its two boundary tumblers (or address + width). The content between is derived, never enumerated (4/25).
- If you must report *exactly* such a region and nothing else, you use a **span-set** — "a series of spans" — which is precisely how Nelson handles designating items "exactly, including nothing else" (4/25).
- Conceptually it is still "a zone hanging down from the tumbler line — what is called in computer parlance a depth-first spanning tree" (4/25), even when that zone is presently unpopulated.

### Caveat on "the report"

I've answered at the level of the span model itself, which governs every span-bearing output (request-sets, version-relation pairs, document extents). If by "the report" you mean a *specific* FEBE operation's return value — e.g., `SHOWRELATIONOF2VERSIONS`, which "returns a list of ordered pairs of the spans of the two spec-sets that correspond" (4/70), and how it represents a region of one version that corresponds to *nothing* in the other — the curated sources don't spell out the empty-correspondence case explicitly.

NEED_RAW: 4/70, 4/24–4/25 (to confirm how an empty/non-corresponding extent is rendered in the SHOWRELATIONOF2VERSIONS pair list specifically)
