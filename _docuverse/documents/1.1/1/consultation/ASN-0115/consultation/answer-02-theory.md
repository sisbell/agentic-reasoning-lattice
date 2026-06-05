## Question 2 [theory]

> Must the delivered content correspond span-for-span to what the spec-set asked about, so that nothing extra is returned and nothing requested is silently omitted?

I don't have file-reading tools available in this session, so I'll answer from the verified curated sources and flag anything that needs the raw pages.

## Answer

**Yes — for content retrieval, the delivered material is exactly what the spec-set designates: nothing extra, nothing requested silently omitted.** This follows from two design facts.

**1. The span-set is built to designate content *exactly*.** A request set is a set of spans, and Nelson is explicit that the span-set mechanism exists precisely to pick out content exactly, excluding everything else:

> "Note: if you want to designate a separated series of items exactly, including nothing else, you do this by a span-set, which is a series of spans." (4/25)

And the content of a span is fully determined by its endpoints — there is no ambiguity about what lies inside:

> "The first point of a span may designate a server, an account, a document or an element; so may the last point. There is no choice as to what lies between; this is implicit in the choice of first and last point." (4/25)

So the request itself has an exact, well-defined extent.

**2. RETRIEVEV returns precisely that extent.** The retrieval operation is defined as returning the material *determined by* the spec-set:

> "RETRIEVEV ... This returns the material (text and links) determined by <spec set>." (4/67)

"Determined by" means the delivered content is a faithful function of the request — the spec-set fixes what comes back. Likewise SHOWRELATIONOF2VERSIONS returns correspondence as exact span pairs, not approximate overlaps:

> "This returns a list of ordered pairs of the spans of the two spec-sets that correspond." (4/70)

This span-for-span fidelity is the same property that makes correspondence and link survivability work: the system tracks content by exact spans/I-addresses, not by fuzzy position.

## Two important qualifications

**Link search is a different model — it is satisfaction-based and paginated, not span-for-span exact.** A link is *returned* if it partially matches the request (the "AND of the ORs"):

> "A link satisfies a search request if one span of each endset satisfies a corresponding part of the request." (4/58)

And results may be delivered in batches rather than all at once (FINDNEXTNLINKSFROMTOTHREE returns "no more than <nlinks>" past a given point, 4/69). So for *link discovery*, the guarantee is "all matching links are findable" — importantly, "THE QUANTITY OF LINKS NOT SATISFYING A REQUEST DOES NOT IN PRINCIPLE IMPEDE SEARCH ON OTHERS" (4/60) — but a single call need not return the complete set in one delivery. This is omission by pagination, not silent omission: the iteration mechanism exists to retrieve the remainder.

**Delivery fidelity is a semantic guarantee, not a transmission guarantee.** Nelson explicitly disclaims reliability of the physical channel:

> "User acknowledges that due to possible unreliability of the software, unreliability and vulnerability of transmission systems, and myriad possibilities for intrusion and malicious mischief by unseen parties throughout the universe, all storage, and transmission of contents and links, and attempts to deliver such material, are at User's risk." (5/18)

So "span-for-span correspondence" is a property of what the operation *is defined to return*, not a promise that the network will never drop bytes.

## Caveat on certainty

The curated sources establish that the spec-set designates content exactly and that RETRIEVEV returns "the material determined by" it. They do **not** contain an explicit sentence stating, in so many words, that delivery is *verified* span-for-span (no partial-fulfillment / resource-exhaustion behavior for RETRIEVEV specifically). If you want the precise wording of the RETRIEVEV command and any surrounding notes about partial delivery or resource limits:

NEED_RAW: 4/61-4/67 (FEBE command definitions, esp. RETRIEVEV and any "Resource Unit"/partial-satisfaction language)
