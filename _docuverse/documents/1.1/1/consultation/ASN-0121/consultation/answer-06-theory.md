## Question 6 [theory]

> What soundness guarantee must hold so that no returned link fails any of the four criteria?

## Soundness Guarantee for Link Search

The guarantee is the **"AND of the ORs"**: every link returned must satisfy *all four* parts of the request simultaneously — and for each part, at least one span of the link's corresponding endset must fall within the requested region.

### The Four Criteria

A link search (`FINDLINKSFROMTOTHREE`) constrains four sets. From the operations extraction:

> "This returns a list of all links which are (1) in <home set>, (2) from all or any part of <from set>, and (3) to all or any part of <to set> and <three set>." (4/69)

These are the four criteria: **home-set**, **from-set**, **to-set**, and **three-set** (type).

### The Satisfaction Rule

The soundness condition is stated in `_docuverse` links/operations material:

> "A link satisfies a search request if one span of each endset satisfies a corresponding part of the request." (4/58)

This is the precise guarantee. Decomposed:

- **Within each criterion (the OR):** the link's endset may be a discontiguous span-set; it satisfies that criterion if *one* of its spans falls in the requested region ("all or any part of"). Only one span needs to match.
- **Across the four criteria (the AND):** the link must satisfy a corresponding part for *each* of the four endsets. Failing even one criterion disqualifies the link.

So for no returned link to fail any of the four criteria, the back end must guarantee that each returned link has, for **every** one of the four request components, at least one endset span satisfying it. The conjunction across all four is what enforces soundness; the disjunction within each is what tolerates discontiguous endsets.

### Why This Matters (Completeness vs. Soundness)

This soundness guarantee is paired with a separate completeness/efficiency guarantee:

> "THE QUANTITY OF LINKS NOT SATISFYING A REQUEST DOES NOT IN PRINCIPLE IMPEDE SEARCH ON OTHERS." (4/60)

Together: soundness ensures no false positives (every returned link meets all four criteria), while the non-impedance property ensures the mass of non-matching links (the "junk-link problem") doesn't degrade the search for matching ones.

### Note on the Request's Home-Set Scope

The home-set criterion governs *where* matching links are sought:

> "If the home-set is the whole docuverse, all links between these two elements are returned." (4/63)

So criterion (1) is satisfied trivially when the home-set spans everything; the soundness obligation then rests on the from/to/three constraints.

---

The four curated sources (`links` concept doc, `operations`, `three-endset-links`, `link-type-system`) cover this fully. The exact phrasing "A link satisfies a search request if one span of each endset satisfies a corresponding part of the request" (4/58) is the soundness guarantee you're asking about.
