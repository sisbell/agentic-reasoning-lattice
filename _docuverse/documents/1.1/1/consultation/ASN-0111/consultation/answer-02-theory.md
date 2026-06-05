## Question 2 [theory]

> What guarantee governs the completeness of a link's endsets when the link is read directly rather than traversed?

## Answer

The relevant guarantee is the one carried by **`RETRIEVEENDSETS`**: when a link is read directly, the system returns the link's endsets *in their entirety* — the complete from-set and to-set, including all of their (possibly discontiguous) spans — rather than just whatever portion happened to satisfy a query.

This is best understood by contrasting the two ways of getting at a link's endsets:

**Traversal / search (partial-match model).** When you *find* a link via `FINDLINKSFROMTOTHREE`, the link is returned if only *one* span of each endset falls within the request. From the operations material:

> "A link satisfies a search request if one span of each endset satisfies a corresponding part of the request." (4/58)

So traversal tells you a link is *relevant*, but the matching is satisfied by a single span per endset — it does not, by itself, hand you the whole endset.

**Direct read (complete-endset model).** When you read the link directly, you ask for its endsets as stored:

> "RETRIEVEENDSETS: This returns a list of all link end-sets that are in <spec set>." (4/70)

The endsets material establishes what "complete" must mean here, because an endset is not a single pointer but an arbitrary collection:

> "The from-set may be an arbitrary collection of spans, pointing anywhere in the docuverse. Similarly, the to-set may be an arbitrary collection of spans pointing anywhere in the docuverse." (4/43)

> "ENDSETS MAY POINT TO SPANS ANYWHERE IN THE DOCUVERSE" (4/45, diagram caption)

So the completeness guarantee governing a *directly read* link is that you receive the full from-set and to-set — every span of each arbitrary, possibly broken/discontiguous collection — not merely the span that matched some search. Reading is complete; traversal is satisfaction-based.

## Caveat

The curated sources give the two halves of this contrast (the `RETRIEVEENDSETS` operation at 4/70 and the "one span of each endset satisfies" satisfaction rule at 4/58, plus the arbitrary-collection nature of endsets at 4/43–4/45). They do **not** contain a single sentence where Nelson explicitly names a "completeness guarantee for directly-read endsets." If you want a verbatim guarantee statement (rather than the synthesis above), it would need confirmation from the raw pages.

NEED_RAW: 4/58, 4/70 (to check for any explicit completeness/exhaustiveness wording around RETRIEVEENDSETS vs. the link-search satisfaction rule)
