## Question 4 [theory]

> Did Nelson intend a request with all three parts unconstrained ("match every link") to be a valid query, or must at least one part be constrained for the request to be well-formed?

## Short answer

Nelson never states an explicit prohibition, but his design makes "match every link" a **well-formed and valid query** — it is simply expressed as universal spans (the "1-positions") in each part, not as omitted/empty constraints. The satisfaction model and the system's explicit handling of result avalanches both point to broad, unbounded queries being expected rather than rejected as malformed.

## The reasoning

**1. The satisfaction model is an AND-of-ORs over the request parts.**

The core rule for link search is:

> "A link satisfies a search request if one span of each endset satisfies a corresponding part of the request." (4/58)

A request, per the `links` material, specifies four parts: a **home-set**, **from-set**, **to-set**, and **three-set** (type). For a link to match, at least one span of each of its endsets must fall within the corresponding part of the request. If a request part is the *whole docuverse*, then every link's corresponding endset trivially satisfies it.

**2. "Everything" is expressible as a span, not as an absence.**

The span system is built so that breadth is something you *specify*, not something you *leave out*. A single "1" in the right position designates an entire level — up to the whole docuverse:

> "A digit of 'one' may be used to designate all of a given version, all versions of a given document, all works of a given author, all documents in a given project, all documents on a given server — or the entire docuverse." (4/38)

And from the `spans` material: `0.0.0.1` designates the entire docuverse. So "match every link" is the request whose from-set, to-set, and three-set are each the universal span. That is a constrained, well-formed request — its constraint just happens to be "everything."

This is reinforced by FINDLINKSFROMTOTHREE's documented behavior, where widening a part to the maximum is a normal, supported case:

> "If the home-set is the whole docuverse, all links between these two elements are returned." (4/63)

**3. The system is explicitly designed to survive enormous result sets.**

Nelson treats a flood of matches as an expected operating condition, not an illegal query:

> "THE QUANTITY OF LINKS NOT SATISFYING A REQUEST DOES NOT IN PRINCIPLE IMPEDE SEARCH ON OTHERS." (4/60)

He provides pagination for exactly this — FINDNEXTNLINKSFROMTOTHREE returns "no more than `<nlinks>` items" (4/69) — and, per the `links` material, the "Resource Unit (RU)" exists for when users "ask for the moon and stars simultaneously." A maximally broad query is something the architecture plans to *serve*, not reject.

## The caveat

What Nelson does **not** address is the case of a *literally empty* request part (a part containing no spans at all, as opposed to a part containing the universal span). The satisfaction rule — "one span of each endset satisfies a corresponding part of the request" (4/58) — is ambiguous when a request part has no spans to satisfy. The clean, design-consistent reading is that you never leave a part empty; you express "any" with the universal span. But whether an empty span-set is treated as "match all" or "match none" is an implementation decision Nelson leaves open.

NEED_RAW: 4/58-4/60 — to confirm whether the original text of the link-search request definition explicitly permits or forbids an empty (null) request part, versus requiring a universal span to express "any."
