## Question 9 [theory]

> Must endsets belonging to a single link be distinguishable in the result from endsets belonging to different links touching the same region?

# Must endsets of a single link be distinguishable from endsets of other links touching the same region?

**Yes.** This is required by the nature of a link as a unit. A link is not a loose collection of spans — it is "a connective unit, a package of connecting or marking information" (4/41). The three endsets (from-set, to-set, three-set) only have meaning *as a group*: they jointly express that *this* content connects to *that* content under *this* type. If the result couldn't tell you which endsets belonged to which link, the connection itself would be destroyed.

## Why grouping is mandatory

Consider region R touched by two different links:
- Link A: from R → to X (type T1)
- Link B: from Y → to R (type T2)

A search at R encounters endsets {R, X, T1} and {Y, R, T2}. If the result returned these six spans as an undifferentiated pile, you could not reconstruct that A connects R→X while B connects Y→R. The whole point of a link — following it from one end to the other — would be impossible. The link "satisfies a search request if one span of each endset satisfies a corresponding part of the request" (4/58), which presupposes the system evaluates and returns links *as units*, not endsets in isolation.

## The retrieval model enforces this structurally

The operations are organized so the link is the unit of retrieval, not the endset:

- **FINDLINKSFROMTOTHREE** "returns a list of all links which are (1) in `<home set>`, (2) from all or any part of `<from set>`, and (3) to all or any part of `<to set>` and `<three set>`" (4/69) — it returns *links* (which have their own tumbler addresses), already grouped.
- **MAKELINK** "returns the id of the link made" (4/68) — every link is a first-class, individually-addressed object.
- **RETRIEVEENDSETS** then operates on *specified links* — "Returns the from-set and to-set of links." You name which links, and get their endsets back, so the per-link grouping is intrinsic to the call.

Because "links are located [in tumbler-space] as well as data" (4/49) and each has its own address, every endset belongs to an identified, addressable link. The link's identity is what binds its endsets together.

## Two levels of distinguishability

Note the question concerns *inter-link* grouping (which endsets belong to which link). The same link model also requires *intra-link* distinguishability: within one link, the from-set, to-set, and type must remain distinct from one another, because the link "is typically directional. Thus it has a from-set, the bytes the link is 'from,' and a to-set, the bytes the link is 'to.'" (4/42), plus a separate type endset (4/44). Both forms of distinguishability are necessary for the link to retain its meaning.

## Caveat on sourcing

Nelson's curated text does not state this as an explicit single sentence ("results must group endsets by link"). The answer is a direct entailment of (a) the link defined as a unified "package" (4/41), (b) the satisfaction model that operates on whole links (4/58), and (c) the retrieval operations that return and address links individually (4/68–4/70). If you want Nelson's exact wording on how endset results are formatted/labeled in the FEBE reply, that would be in the detailed protocol pages: NEED_RAW: 4/68–4/70.
