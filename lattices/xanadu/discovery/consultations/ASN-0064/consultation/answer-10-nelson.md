## Question 10 [nelson]

> When the queried region spans content drawn from multiple distinct original sources, must the system independently discover links to each source and merge the results into a single complete set?

## Yes — and the mechanism is the generalized span-set search

Nelson's architecture guarantees that querying a compound region returns links to **all** constituent content, regardless of how many original sources contributed. But the mechanism is not "independently discover and merge" as a multi-step pattern — it falls out naturally from the span-set generalization.

### Why the problem exists

A document's Vstream can include bytes from multiple Istream origins:

> "The virtual byte stream of a document may include bytes from any other document." [LM 4/10]

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

Links attach to **Istream addresses**, not Vstream positions. So a Vstream region spanning three sources maps to three disjoint I-address ranges. Links to each source live at different positions on the tumbler line.

### How the architecture handles it

The FEBE protocol is explicitly generalized for this case:

> "However, the commands for links and connectivity (material shared between documents and versions) are more esoteric, particularly since they have been generalized for the interconnection of broken lists of spans." [LM 4/61]

"Broken lists of spans" is precisely a disjoint span-set crossing multiple sources. The flow:

1. **V-to-I resolution** — The front-end (or middle-end) resolves the Vstream region into its constituent Istream spans. These may be disjoint and span multiple documents.

2. **Span-set construction** — The resulting I-spans form a request set:

   > "A request set is a set of spans, or spanset, presented to the back end in the FEBE protocol... The manipulation of request sets is an important aspect of what front-end functions do." [LM 4/37]

3. **Unified search** — FINDLINKSFROMTOTHREE accepts this span-set as a single argument and returns all matching links:

   > "This returns a list of all links which are (1) in \<home set\>, (2) from all or any part of \<from set\>, and (3) to all or any part of \<to set\> and \<three set\>." [LM 4/69]

4. **Satisfaction across the set** — A link matches if any of its endset spans intersects any span in the request:

   > "A link satisfies a search request if one span of each endset satisfies a corresponding part of the request." [LM 4/58]

### The user-facing guarantee

Nelson states the guarantee in user terms:

> "The reader should be able to ask, for a given document or place in the document, 'What connects here from other documents?' — and be shown all these outside connections without appreciable delay." [LM 2/46]

"A given place in the document" is a Vstream reference. The user points at content; the system finds **all** links, whether the bytes originated natively or were transcluded from one or many sources.

And the efficiency guarantee holds regardless of the span-set's complexity:

> "THE QUANTITY OF LINKS NOT SATISFYING A REQUEST DOES NOT IN PRINCIPLE IMPEDE SEARCH ON OTHERS." [LM 4/60]

### The endset generalization confirms this

Nelson designed endsets to be arbitrary span-sets across the entire docuverse:

> "The from-set may be an arbitrary collection of spans, pointing anywhere in the docuverse. Similarly, the to-set may be an arbitrary collection of spans pointing anywhere in the docuverse." [LM 4/43]

If endsets can be disjoint and cross-document, search arguments can be too. The machinery is symmetric.

### Summary

The semantic answer is **yes**: the system must find links to every original source and return a complete, unified result. But architecturally, this is not a "discover independently then merge" pattern — it is a single span-set search over a disjoint set of I-addresses. The V-to-I resolution (a front-end or middle-end responsibility) produces the disjoint span-set; FINDLINKSFROMTOTHREE searches it as one operation. The "broken lists of spans" generalization [LM 4/61] exists precisely to handle compound content whose identity is scattered across the Istream.
