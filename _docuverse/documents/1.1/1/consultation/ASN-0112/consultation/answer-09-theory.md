## Question 9 [theory]

> What invariant ensures the reported origin and extent together describe one continuous, well-formed region rather than a fragmented or empty one?

## The continuity invariant for `RETRIEVEDOCVSPAN`

The operation in question is **RETRIEVEDOCVSPAN**, which "returns a span determining the origin and extent of the V-stream of document `<doc id>`" (operations, 4/68). The invariant that guarantees origin + extent describe *one continuous, well-formed region* comes from two properties Nelson builds into spans and the V-stream.

### 1. A single span's interior is implicit in its two endpoints

A span is represented as **origin + extent** (a start address plus a difference tumbler). Because a span is *defined* by its boundaries, everything between them is fixed — there is no way to express a "hole":

> "The first point of a span may designate a server, an account, a document or an element; so may the last point. There is no choice as to what lies between; this is implicit in the choice of first and last point." (spans, 4/25)

Nelson visualizes this as a connected subtree, not a scattered set:

> "A span may be visualized as a zone hanging down from the tumbler line--what is called in computer parlance a depth-first spanning tree." (spans, 4/25)

The corollary makes the invariant explicit: a *fragmented* selection is **not** a span at all — it must be a span-*set*:

> "Note: if you want to designate a separated series of items exactly, including nothing else, you do this by a span-set, which is a series of spans." (spans, 4/25)

So by construction, a single returned span (origin + extent) is contiguous; discontiguity is only representable by switching to a different type (span-set). That is the well-formedness guarantee.

### 2. The V-stream itself is dense, so the region is non-empty and gap-free

`RETRIEVEDOCVSPAN` reports the V-stream extent specifically, and the V-stream is dense and contiguous by invariant — positions run consecutively from 1 with no gaps (v-space-addresses, 4/11, 4/30). Editing shifts addresses but never punches holes:

> "The v-stream addresses of any following characters in the document are increased by the length of the inserted text." (operations / v-space-addresses, 4/66)

Because the V-stream is a contiguous run from its origin through its extent, the origin+extent pair returned describes the whole document's current arrangement as one unbroken region.

### Summary

The invariant is the **span contiguity rule**: a span is a single subtree whose contents are implicit between its two boundary points, so any *single* span (origin + extent) is necessarily one continuous region — fragmentation requires a span-set instead (4/25). Applied to `RETRIEVEDOCVSPAN`, the additionally dense, gap-free nature of the V-stream (4/30) ensures that region is also well-formed and non-empty for any document with content.

One caveat on "non-empty": at the tumbler level Nelson notes a span "that contains nothing today may at a later time contain a million documents" (4/25) — spans are not *forced* to be occupied. Emptiness is excluded here not by the span abstraction itself but by the V-stream having actual content; an empty document's V-stream extent would be a degenerate (zero-width) case.
