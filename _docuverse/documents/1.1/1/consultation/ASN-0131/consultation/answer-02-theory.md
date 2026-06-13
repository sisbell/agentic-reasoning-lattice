## Question 2 [theory]

> What relationship must each returned endset bear to the region asked about: must every returned endset overlap the region, and must the returned portion be exactly the part of the endset that falls within it?

I've now read the governing passages directly: the link-search satisfaction model on raw page 225 ([LM 4/58]) and the `RETRIEVEENDSETS` definition on raw page 237 ([LM 4/70]). Note one correction to the curated `operations` note along the way: it transcribes `RETRIEVEENDSETS ( <spec set> )`, but the raw page shows the argument is `<linkid set>` — "a list of one or more link i.d.s" — not a region. That distinction matters here.

---

## Answer

**No to both clauses, as stated.** Both halves of the question describe constraints tighter than what Xanadu actually guarantees. The correct relationships are: (1) the matching test is *overlap*, not containment — and only the endset(s) you *bind* to the region need overlap it, not "every" endset; and (2) endsets are returned *whole*, never clipped to the region.

### 1. Matching is overlap, and only the constrained endset(s) must overlap

A link is selected by a search through the "AND of the ORs." The criterion is that **at least one span** of each endset falls within the **corresponding** request part:

> "at least one span of each endset must fall within a corresponding part of the request, for a link to be found by that request." [LM 4/58]

> "a link is found by a request if and only if the AND of the ORs is satisfied-- (some from-span is in the requested from-set) AND (some to-span is in the requested to-set) AND (some 3-span is in the requested three-set)." [LM 4/58]

Two consequences follow, and both cut against the question's first clause:

- **Overlap, not containment.** Because only *one* span need fall within the request, the endset as a whole need not lie inside the region. A from-set can span a whole chapter, intersect your region in one place, and still match. `FINDLINKSFROMTOTHREE` makes this explicit: it returns links "from **all or any part of** `<from set>`" [LM 4/69]. *Any part* matching is enough.

- **Not "every" endset — only the one(s) you constrained.** The test is per-endset against its *corresponding* request part. If you ask "what links touch this span?", you typically place the region in the from-position (or to-position) and leave the others as the whole docuverse. Then only that endset must overlap your region; the link's *other* endsets point wherever the link points. By design, endsets "may point to spans anywhere in the docuverse" [LM 4/45] — a matched link's to-set is generally its destination *elsewhere*, and its type-set is often a ghost element nowhere near your region. So it is simply not true that every returned endset overlaps the region you asked about.

### 2. The returned portion is the *whole* endset, never clipped

`RETRIEVEENDSETS` does not take a region at all — it takes link IDs and hands back the complete endsets:

> "RETRIEVEENDSETS — This important command, given a set of links, returns their endsets... This returns a list of all link end-sets that are in `<linkid set>`." [LM 4/70]

The only optional refinement restricts the *kind* of endset, not its spatial extent:

> "The user may also restrict the kind of endset returned, by an additional argument: RETRIEVEENDSETS ( `<linkid set>`, `<endset spec>` )." [LM 4/70]

`<endset spec>` lets you say "give me only the to-sets" — it does **not** say "give me only the part of the to-set inside region X." There is no clipping operation.

And clipping would defeat the purpose. A link is "between spans of data" [LM 4/42], pointing "to or from an arbitrary set of bytes ... anywhere in the docuverse" [LM 4/42]. You search *from* a region precisely so you can follow the link *out* of it — to its destination and to read its full from-set. If I returned only the slice of each endset that happened to fall inside your search region, the to-set you need to navigate to would usually come back empty, and a from-set straddling the boundary would be misrepresented. The whole endset must come back so the connection remains faithful and followable.

### Summary

| The question asks | Actual guarantee |
|---|---|
| Must *every* returned endset overlap the region? | No. Matching is checked per-endset against its *corresponding* request part. Only the endset(s) you constrain to the region must overlap it; a matched link's other endsets point freely, anywhere in the docuverse. |
| Is overlap (vs. containment) the test? | Overlap — "all or **any part of**" [LM 4/69]; one span "falling within" suffices [LM 4/58]. The whole endset need not be inside. |
| Must the returned portion be exactly the part within the region? | No. Endsets are returned **whole** [LM 4/70]; there is no spatial clipping, only an optional restriction on *which kind* of endset. |

So the precise picture is: a single span's overlap with the *corresponding* request part qualifies a link, and once qualified the endsets come back in full — uncut and pointing wherever they point.
