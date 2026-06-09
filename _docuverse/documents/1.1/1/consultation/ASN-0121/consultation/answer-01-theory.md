## Question 1 [theory]

> When a link is requested by four bounding sets at once, what must the system guarantee about how each returned link satisfies all four criteria together rather than any one alone?

## The Four Bounding Sets

When a link is searched by four bounding sets at once, those sets are the **home-set**, **from-set**, **to-set**, and **three-set** (type). The operation is `FINDLINKSFROMTOTHREE`:

> "This returns a list of all links which are (1) in <home set>, (2) from all or any part of <from set>, and (3) to all or any part of <to set> and <three set>." (4/69)

## The Guarantee: "The AND of the ORs"

The system must guarantee that each returned link satisfies **all four criteria jointly**, not just one. Nelson's satisfaction rule:

> "A link satisfies a search request if one span of each endset satisfies a corresponding part of the request." (4/58)

This is a conjunction-of-disjunctions ("the AND of the ORs"):

- **Across the four sets — AND (conjunction):** A link qualifies only if it is in the requested home-set *and* its from-set touches the requested from-set *and* its to-set touches the requested to-set *and* its type touches the requested three-set. Matching any single criterion alone is insufficient.

- **Within each set — OR (disjunction):** Because each endset is itself an arbitrary span-set, satisfaction of that one criterion requires only that *one span* of the link's endset fall within the corresponding requested set ("from all or any part of"). The endset need not match in its entirety.

So the returned link is the intersection of all four constraints, each constraint being individually satisfiable by a partial (single-span) match.

## Why This Matters for Scale

This joint-satisfaction model is what lets search remain tractable in a docuverse saturated with links:

> "THE QUANTITY OF LINKS NOT SATISFYING A REQUEST DOES NOT IN PRINCIPLE IMPEDE SEARCH ON OTHERS." (4/60)

Because every returned link must meet all four bounding sets together, irrelevant links (failing even one criterion) are excluded without slowing the search — the back end subdivides on the conjunction rather than scanning everything.

---

The curated sources cover the four-set satisfaction guarantee directly (4/58, 4/60, 4/69). If you want the surrounding discussion of the request structure (home-set / from-set / to-set / three-set) and the junk-link filtering rationale in full prose, that lives in: NEED_RAW: 4/58-4/60.
