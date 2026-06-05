## Question 3 [theory]

> Must an endset be returned in full even when only part of it falls within the queried region, or only the portion that intersects?

The raw page images aren't present in this checkout, so I'll work from the curated sources and flag what isn't covered.

## Answer

This question has two distinct halves that the sources answer differently. **Matching** (does a partially-overlapping endset cause the link to be found?) is explicitly answered. **Return granularity** (is the endset returned whole or clipped to the intersection?) is not explicitly answered for the retrieval command.

### Matching: partial intersection is sufficient

For *whether a link is found*, Nelson is unambiguous — any part of an endset falling in the queried region satisfies the request. The search uses an "all or any part" rule:

> "This returns a list of all links which are (1) in <home set>, (2) from all or any part of <from set>, and (3) to all or any part of <to set> and <three set>." — FINDLINKSFROMTOTHREE (4/69)

And the satisfaction model:

> "A link satisfies a search request if one span of each endset satisfies a corresponding part of the request." (4/58)

So an endset that only partially intersects the queried region still qualifies the link — only *one span* of the endset need fall within the request. This is by design, and connects to survivability: links attach to "an arbitrary collection of bytes (spans)... anywhere in the docuverse" (4/42-4/43), so partial overlap is the normal case.

### Return: the source phrasing favors the full endset, but isn't explicit

The relevant retrieval command is RETRIEVEENDSETS, described as:

> "This returns a list of all link end-sets that are in <spec set>." (4/70)

The phrasing is "link end-sets that are in <spec set>" — i.e., it returns *endsets* (the property of the link) selected by the spec-set, not "the portions of endsets intersecting the spec-set." Read literally, the unit returned is the whole endset. This also fits the semantic purpose of endsets: a from-set or to-set is "an arbitrary collection of spans, pointing anywhere in the docuverse" (4/43), and to follow or comprehend a link you need its complete reach, not a truncated view clipped to your query window. A clipped endset would not let you navigate to the rest of what the link connects.

By contrast, SHOWRELATIONOF2VERSIONS explicitly returns *intersected* pairs — "a list of ordered pairs of the spans of the two spec-sets that correspond" (4/70) — showing Nelson does specify clipping where he means it. RETRIEVEENDSETS uses no such "corresponding spans" language.

### Bottom line

- For **finding/matching** links: only partial intersection is required — "from all or any part of" the endset (4/69), one span satisfying suffices (4/58).
- For **returning** an endset via RETRIEVEENDSETS: the wording ("end-sets that are in <spec set>") and the semantics of links point to returning the **full endset**, not just the intersecting portion. But this is inference from phrasing and purpose, not an explicit statement.

NEED_RAW: 4/69-4/70 (raw pages 236-237) — to confirm whether RETRIEVEENDSETS / RETRIEVEV return the entire endset or only the portion intersecting the spec-set; the curated text does not state the return granularity explicitly.
