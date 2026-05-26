## Question 5 [nelson]

> When a link's endset partially overlaps the queried region — covering some but not all of the specified content — must that link appear in the discovery result?

## Yes — partial overlap is sufficient.

Nelson specifies this directly through the FINDLINKSFROMTOTHREE operation:

> "This returns a list of all links which are (1) in \<home set\>, (2) from **all or any part of** \<from set\>, and (3) to **all or any part of** \<to set\> and \<three set\>." [LM 4/69]

The phrase "any part of" is the key. A link whose from-set touches even a single byte within the queried region satisfies condition (2). The same applies to the to-set and three-set.

### The satisfaction model

The general rule from 4/58:

> "A link satisfies a search request if **one span of each endset** satisfies a corresponding part of the request." [LM 4/58]

This is what Nelson calls **the AND of the ORs**:

- **OR across spans within an endset**: A link's endset may be a discontiguous set of spans. At least *one* span must intersect the query region for that endset to be satisfied.
- **AND across endsets**: All three endsets (from, to, type) must independently be satisfied.

So a link with a from-set that partially overlaps the queried from-region, and a to-set that partially overlaps the queried to-region, and a type matching the queried type — that link appears in the result.

### Why this follows from the architecture

Links attach to spans of bytes, not points. A link whose endset covers bytes 50–200 and a query for bytes 100–300 share bytes 100–200. Nelson designed span-based linking precisely so these geometric relationships work naturally:

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes." [LM 4/42]

The "strap" metaphor reinforces this: if you query a region and a strap crosses into that region, you find the strap. You don't need the strap to be entirely within the region.

### Performance guarantee

Nelson also guarantees that non-matching links don't slow things down:

> "THE QUANTITY OF LINKS NOT SATISFYING A REQUEST DOES NOT IN PRINCIPLE IMPEDE SEARCH ON OTHERS." [LM 4/60]

This means the system can efficiently find partially-overlapping links without scanning the universe of non-overlapping ones.

### Summary

A link appears in discovery results whenever its endset **intersects** the queried region — full containment is not required. This is explicitly stated by the "any part of" language in the FINDLINKSFROMTOTHREE specification [LM 4/69] and follows naturally from the span-based, geometrically-addressed link model.
