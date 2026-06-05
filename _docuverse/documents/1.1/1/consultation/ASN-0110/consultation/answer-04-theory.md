## Question 4 [theory]

> Does the design guarantee that every endset anchored to any part of the region appears in the result, with none omitted?

Yes—completeness is an explicit design intent of the link-search model. The guarantee has two parts.

## 1. "Any part" matching means partial overlap is enough

A link is returned when its endset touches *any* portion of the requested region, not only when it falls wholly inside. From the FINDLINKSFROMTOTHREE specification:

> "This returns a list of all links which are (1) in <home set>, (2) from all or any part of <from set>, and (3) to all or any part of <to set> and <three set>." (4/69)

The phrase "all or any part" is the key: an endset that overlaps the region even partially satisfies the request. And the formal satisfaction rule:

> "A link satisfies a search request if one span of each endset satisfies a corresponding part of the request." (4/58)

So for a single-endset query over a region, any link with at least one span intersecting that region qualifies and is returned.

## 2. Irrelevant links cannot crowd out relevant ones

Nelson states the completeness/scalability invariant directly:

> "THE QUANTITY OF LINKS NOT SATISFYING A REQUEST DOES NOT IN PRINCIPLE IMPEDE SEARCH ON OTHERS." (4/60)

This is precisely the "none omitted" promise: the presence of millions of non-matching links does not prevent the matching ones from being found.

## 3. The result holds through editing

Because endsets attach to spans of bytes (Istream), not positions, matches persist:

> "Links between bytes can survive deletions, insertions and rearrangements, if anything is left at each end." (4/43)

So an endset anchored anywhere in the region remains discoverable as long as any of its bytes survive there.

## Important qualification: completeness ≠ single-call delivery

The guarantee is that every qualifying link is *in the result set*, not that all arrive in one response. Large result sets are paginated, not truncated:

> "FINDNEXTNLINKSFROMTOTHREE ... no more than <nlinks> items past that link on that list." (4/69, per `operations` notes)

Pagination iterates through the complete list; it does not drop members. The `links` source frames this as the system handling "avalanches of material" while still indexing "by all their endsets" for discovery "from any direction."

## Summary

By design, every endset whose spans intersect the queried region appears in the result—partial overlap suffices ("all or any part," 4/69), non-matching links never impede the search (4/60), and matches survive editing (4/43). Omission occurs only if *all* of an endset's bytes at that end are deleted, since then there is nothing left to match.

One caveat on scope: the sources establish this as the *design intent and protocol contract*. Whether a given implementation realizes it perfectly is an implementation question the curated Literary Machines material does not address.
