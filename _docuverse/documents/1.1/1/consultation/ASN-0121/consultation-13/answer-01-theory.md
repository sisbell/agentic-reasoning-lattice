## Question 1 [theory]

> Was the home-set of FINDLINKSFROMTOTHREE intended to bound residence only by whole-subtree prefixes (node/account/document), or may it carry arbitrary-width spans denoting sub-document residence ranges?

## Answer

The home-set is **architecturally a span-set**, not restricted to whole-subtree prefixes — so it *can* carry arbitrary-width spans, including ones that denote sub-document residence ranges. But Nelson's explicit examples only illustrate the whole-subtree (docuverse/document) cases. Let me lay out what the sources support.

### The home-set is a request span-set, treated symmetrically

In the search-request structure, the home-set is one of the constraining span-sets:

> A request specifies:
> - **home-set**: where desired links are to be found
> *(links concept, drawn from 4/58–4/60)*

And the satisfaction model treats it like any other endset:

> "A link satisfies a search request if one span of each endset satisfies a corresponding part of the request." (4/58)

The operation itself is defined over a `<home set>`:

> "This returns a list of all links which are (1) in `<home set>`, (2) from all or any part of `<from set>`, and (3) to all or any part of `<to set>` and `<three set>`." (4/69)

> "If the home-set is the whole docuverse, all links between these two elements are returned." (4/63)

### Spans can denote sub-document element ranges, not just subtrees

The crucial point is that a tumbler-span is *not* limited to clean subtree prefixes. Nelson explicitly admits the "series of elements" case:

> "A span in the tumbler line, represented by two tumblers, refers to a subtree of the entire docuverse, (or merely to a series of elements of the same type, which is a degenerate case of a subtree). Thus we may have spans of characters, spans of links, spans of documents, spans of versions..." (4/24)

Note "**spans of links**" directly. So the span machinery already contemplates ranges *within* the link population.

### Links have a contiguous, ordered address subspace inside a document

Links reside in their home document's `0.2.N` subspace, numbered by arrival:

> "N.0.U.0.D.V.0.2.1 (the first link of the document...)" / "N.0.U.0.D.V.0.2.755 (the 755th link to which the document is home)" (4/31)

> "The links designated by a tumbler address are in their permanent order of arrival. A document includes only the links of which it is the home document." (4/31)

Because those link instances occupy a sequential, contiguous range, an arbitrary-width span over that range (a "span of links" in the 4/24 degenerate-subtree sense) *would* denote a sub-document residence range — e.g., links by arrival order within one document.

### Conclusion

- **Mechanically/by intent of the span system:** home-set is a general span-set. It is *not* confined to whole-subtree prefixes (node/account/document via the 1-positions). The same `0.2.N` link addressing plus the "spans of links... degenerate case of a subtree" provision (4/24) means a home-set can carry arbitrary-width spans bounding residence to a sub-document range of link instances.
- **The 1-position / whole-subtree forms** ("the whole docuverse," a document, an account, a node) are the *canonical examples* Nelson actually shows (4/63, 4/23), but they are special cases of the span mechanism, not its limit.

### Caveat on "intended"

The curated sources establish the *capability* (home-set is a span-set; spans of links are valid; links have sequential in-document addresses). They do **not** contain a passage where Nelson explicitly says "use a sub-document arrival-order range as the home-set." That specific design intent — as opposed to the general span capability — is not directly stated.

NEED_RAW: 4/58–4/60 (to confirm whether the search-model discussion of the home-set frames residence bounding as subtree-only or as general spans, beyond what the curated summary captures).
