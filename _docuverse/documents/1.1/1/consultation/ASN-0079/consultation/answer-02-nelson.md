## Question 2 [nelson]

> Must the system guarantee that every link whose endsets reference the queried content is returned, or may it return a partial result?

## The System Guarantees Completeness

Nelson specifies that link search must return **all** matching links, not partial results. The evidence is unambiguous across multiple layers of the specification.

### The Protocol Command Is Explicit

FINDLINKSFROMTOTHREE:

> "This returns a list of **all links** which are (1) in \<home set\>, (2) from all or any part of \<from set\>, and (3) to all or any part of \<to set\> and \<three set\>." [LM 4/69]

The word "all" is the guarantee. The operation does not say "some links," "a sample of links," or "links up to a limit." It returns all links satisfying the criteria.

### The Count Operation Confirms It

FINDNUMOFLINKSFROMTOTHREE exists specifically to count matching links before retrieval. This only makes sense if the system knows the complete set. You cannot count what you haven't found.

### Pagination Handles Volume, Not Incompleteness

FINDNEXTNLINKSFROMTOTHREE provides pagination — "no more than \<nlinks\> items past that link on that list" [LM 4/69]. This handles what Nelson calls "avalanches of material" from link searches. But pagination is a delivery mechanism over a complete result set, not an admission of partial results.

### The Performance Guarantee Reinforces Completeness

> "THE QUANTITY OF LINKS NOT SATISFYING A REQUEST DOES NOT IN PRINCIPLE IMPEDE SEARCH ON OTHERS." [LM 4/60]

This is a performance guarantee that makes completeness practical. Nelson is saying: the system can find all matching links efficiently even in a universe full of non-matching links. If partial results were acceptable, this guarantee would be unnecessary — you'd just stop early.

### The User-Facing Promise

From the user perspective, Nelson is equally explicit:

> "The reader should be able to ask, for a given document or place in the document, 'What connects here from other documents?'— and be shown **all** these outside connections without appreciable delay." [LM 2/46]

Again: "all these outside connections." Not "representative connections" or "nearby connections."

### The Satisfaction Model

The search semantics define precisely what "matching" means:

> "A link satisfies a search request if one span of each endset satisfies a corresponding part of the request." [LM 4/58]

This is a deterministic predicate. Every link in the docuverse either satisfies the request or it does not. The system returns all that satisfy.

### One Acknowledged Practical Limitation

Nelson does acknowledge resource constraints through the Resource Unit concept — when the system "can't fully satisfy a request," the RU works "on your behalf." And separately:

> "It is a truism that 'computer networks are always broken.' Meaning that on the average some nodes are disconnected or not working." [LM 4/75]

These are acknowledged **practical realities** of a distributed system, not semantic relaxations. The architectural intent remains completeness. Network partitions may temporarily prevent access to some links, but the system's subrepresentation model (each server maintaining "a continuously valid model or subrepresentation of the entire docuverse" [LM 4/72]) is designed to minimize such gaps.

### Summary

The guarantee is completeness. Every link whose endsets match the query criteria must be returned. Pagination handles delivery of large result sets. The performance guarantee (4/60) ensures that non-matching links do not degrade search. Network partitions are a practical concern addressed by architectural redundancy, not by weakening the completeness guarantee.

NEED_RAW: [4/58-4/60] — The curated sources cover the key quotes from these pages, but the full discussion of the satisfaction model and the "junk-link problem" may contain additional nuance about edge cases in search completeness.
