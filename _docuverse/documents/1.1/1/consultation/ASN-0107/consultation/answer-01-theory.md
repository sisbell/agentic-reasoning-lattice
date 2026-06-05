## Question 1 [theory]

> When the system reports how many links match a from/to/type description, what is the unit being counted — distinct links, distinct endpoints, or distinct documents touched?

## Answer: Distinct links

The unit counted is **distinct links** — whole link objects — not endpoints or documents touched.

This follows directly from how Nelson defines link satisfaction. A link is the atomic unit of the search, and each link either satisfies a request or doesn't:

> "A link satisfies a search request if one span of each endset satisfies a corresponding part of the request." (4/58)

The counting operation is the numeric companion to the listing operation. `FINDLINKSFROMTOTHREE` returns the actual links:

> "This returns a list of all links which are (1) in <home set>, (2) from all or any part of <from set>, and (3) to all or any part of <to set> and <three set>." (4/69)

`FINDNUMOFLINKSFROMTOTHREE` simply counts the members of that same list — so its unit is identical to what the list enumerates: links.

### Why not endpoints or documents

The three-endset structure makes the distinction sharp. A single link can have a from-set, to-set, and type-set that each touch *multiple discontiguous spans across multiple documents*:

> "We see from above that one end of a link may be on a broken, discontiguous set of bytes. This illustrates the endset: a link may be to or from an arbitrary set of bytes. These may be anywhere in the docuverse." (4/42)

If the count were of endpoints or documents, one richly-connected link would inflate the number. But the satisfaction rule collapses all that breadth into a single boolean per link ("one span of each endset satisfies..." → the *link* satisfies). A link with a from-set spanning ten documents still counts as **one**.

This is reinforced by the search-scaling guarantee, which treats links as the countable population:

> "THE QUANTITY OF LINKS NOT SATISFYING A REQUEST DOES NOT IN PRINCIPLE IMPEDE SEARCH ON OTHERS." (4/60)

### Summary

`FINDNUMOFLINKSFROMTOTHREE` counts distinct link objects that satisfy the from/to/type constraints. Each link is counted once regardless of how many spans, endpoints, or documents its endsets touch.
