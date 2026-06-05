## Question 5 [theory]

> When two requested spans overlap, what must the system guarantee about the shared content — is it returned once, twice, or marked as common?

I can't open the page images in this context, so I'll answer from the curated sources and flag where they fall short.

## Short answer

The curated sources **do not explicitly state** whether RETRIEVEV deduplicates overlapping spans within a single request set. What they do establish is the conceptual machinery that bears on it, plus one clear case (link search) where the model is set-based "returned once."

## What the sources do establish

**1. A request set is a set of spans, and manipulating it is front-end work.**

From `spans`:
> "A request set is a set of spans, or spanset, presented to the back end in the FEBE protocol... The manipulation of request sets is an important aspect of what front-end functions do." (4/37)

> "Understanding spans is a key to appropriate software design for handling request-sets." (4/37)

The phrasing "set of spans" and the emphasis that request-set *manipulation* is a front-end responsibility suggests overlap normalization is expected to happen in the front end before/around the call — but Nelson does not state the back-end's dedup contract here.

**2. Span-sets are meant to designate content *exactly*, "including nothing else."**

From `spans`:
> "Note: if you want to designate a separated series of items exactly, including nothing else, you do this by a span-set, which is a series of spans." (4/25)

This "exactly... including nothing else" language points toward a *set* semantics (each designated byte is in the set once), but it addresses what is selected, not whether overlapping input spans cause double-return.

**3. For link search, the model is explicitly set-based — matched once, not per-overlap.**

From `operations` / `links`:
> "A link satisfies a search request if one span of each endset satisfies a corresponding part of the request." (4/58)

> "THE QUANTITY OF LINKS NOT SATISFYING A REQUEST DOES NOT IN PRINCIPLE IMPEDE SEARCH ON OTHERS." (4/60)

A link is returned because it *satisfies* the request (membership), not once per matching span — so for links, overlap does not multiply results.

**4. "Marked as common" is a distinct, explicit operation — but between two versions, not within one request.**

The mechanism for surfacing shared content is correspondence, via SHOWRELATIONOF2VERSIONS:
> "This returns a list of ordered pairs of the spans of the two spec-sets that correspond." (4/70)

This is the only place Nelson explicitly "marks common" content — and it compares two spec-sets, not two overlapping spans inside one retrieval request.

## What is not covered

None of the curated material states the dedup contract for **RETRIEVEV** when two spans in the *same* spec-set overlap. RETRIEVEV is described only as:
> "This returns the material (text and links) determined by <spec set>." (4/67)

"Determined by" is consistent with set semantics (return the union once), but it is not explicit, and the front-end-responsibility framing (4/37) leaves open whether the back end normalizes or trusts the caller to pass disjoint spans.

NEED_RAW: 4/37–4/39 (request-set/spanset manipulation), 4/67 (RETRIEVEV definition and any normalization note), and 4/32–4/36 (spec-set construction) — to confirm whether Nelson specifies union/dedup behavior for overlapping vspans, or leaves it to the front end.
