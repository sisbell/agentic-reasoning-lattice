## Question 5 [theory]

> Should the meaning of "matches these four sets" be defined once as a shared notion of link-matching that both the counting and enumerating operations reference, rather than either operation's behavior being specified by appeal to the other?

## Short answer

Yes. "Matches these four sets" should be defined **once**, as a single satisfaction relation between a link and a request, and the counting operation, the enumerating operation, and the paginating operation should each be specified as a *query over that one relation* — not by appeal to one another. This is not merely tidy formalization; it is how I framed the search model in the first place, and it is the only way the user-facing coherence guarantee between counting and enumerating holds by construction rather than by separate stipulation.

## Where the shared notion already lives in the design

I state the matching criterion as a standalone property of links and requests, before and independent of any particular command:

> "A link satisfies a search request if one span of each endset satisfies a corresponding part of the request." (4/58)

That sentence is the shared notion. It is written about *links and requests*, not about `FINDLINKSFROMTOTHREE` or `FINDNUMOFLINKSFROMTOTHREE`. The four sets it ranges over are the parts of the request — home-set, from-set, to-set, and three-set — with the structure being an **AND across the sets of ORs within each set**: the link's home must lie in the home-set, and each of the link's three endsets must have at least one span landing in its corresponding request set. The enumerating command is then specified by *referring back* to exactly this:

> "This returns a list of all links which are (1) in <home set>, (2) from all or any part of <from set>, and (3) to all or any part of <to set> and <three set>." (4/69)

Notice the phrasing — "all links which are…" That "which are…" clause *is* the satisfaction relation. The command does not redefine matching; it consumes it.

## Why neither operation may be defined by appeal to the other

Three reasons, in order of importance.

**1. The count/enumerate consistency is a user guarantee, and it must be structural.** A user who asks "how many links connect X and Y?" and then "show me the links connecting X and Y" must receive a count equal to the number shown. If you define the count as "the length of what the find returns" (or define find as "the things the count counts"), that coherence becomes a *derived theorem you must keep proving* every time the spec is edited, and you have quietly made one operation conceptually subordinate to the other. If instead both reference one predicate, then by construction:

- count = | { ℓ : matches(ℓ, request) } |
- enumerate = the sequence of { ℓ : matches(ℓ, request) }

and they cannot drift apart, because there is exactly one set in play.

**2. Matching is the primitive; the commands are views.** My governing principle for link search is that satisfaction is the fundamental relation and the rest is consumption of it:

> "THE QUANTITY OF LINKS NOT SATISFYING A REQUEST DOES NOT IN PRINCIPLE IMPEDE SEARCH ON OTHERS." (4/60)

That is a statement about *satisfaction*, not about counting or listing. Search operates on what satisfies; the non-satisfying links are simply outside the relation. Counting asks the cardinality of the satisfying set, enumerating asks for the set, and the relation is prior to both. This mirrors the same Xanadu pattern as the endset design — one symmetrical mechanism underneath, many operations on top — rather than feature-by-feature redefinition.

**3. Pagination forces the issue.** The "next N" command is explicitly a *window onto an ordered total set*:

> "no more than <nlinks> items past that link on that list." (4/69)

"That list" presupposes a single, well-defined, ordered set of *all* the matching links. You cannot sensibly define `FINDNEXT` "by appeal to" the count, and you should not have to define it by appeal to a separate `FINDLINKS` either — all three (find, count, next-N) need the *same* underlying "set of links matching the four sets." Define that once, give it an ordering, and the three commands are: take the set, take its size, take a slice. Specifying any one of them through another would leave the third without a clean foundation.

## How to factor it

Make `matches(link, request)` — equivalently `satisfies` — the single definition, parameterized by the four request sets, with the AND-of-ORs structure from 4/58. Then:

- **Enumerate** = the ordered set `{ ℓ : matches(ℓ, request) }`
- **Count** = its cardinality
- **Paginate** = a contiguous slice of the ordered enumeration

None of the three should mention another. All three should mention `matches`.

## One verification gap

My substantive design-intent answer above does not depend on it, but to confirm that the existing prose for the *counting* command does not already commit the appeal-to-the-other anti-pattern (i.e., to check whether `FINDNUMOFLINKSFROMTOTHREE` is worded as "the number of links matching the request" versus "the number of links `FINDLINKSFROMTOTHREE` would return"), the curated sources give me the count operation only in summary tables ("Count such links" / "Counts matching links"), not in Nelson's verbatim command definition.

NEED_RAW: 4/68–4/69 (the `FINDNUMOFLINKSFROMTOTHREE` command definition, to confirm whether it is specified directly against the satisfaction relation or by appeal to `FINDLINKSFROMTOTHREE`).
