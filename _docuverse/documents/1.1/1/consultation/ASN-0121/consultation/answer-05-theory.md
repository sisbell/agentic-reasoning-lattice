## Question 5 [theory]

> What completeness guarantee must hold so that every link meeting all four criteria is returned, with none silently omitted?

## The completeness guarantee

The guarantee is what Nelson states on page 4/60: **the presence of non-matching links must never impede the return of matching ones.** A link search request constrains four parts — the home-set, from-set, to-set, and three-set (type) — and the search must return *every* link that satisfies all four, regardless of how many junk links surround them.

### The satisfaction model (what "meeting the criteria" means)

A link qualifies when it satisfies each of the four endset constraints:

> "A link satisfies a search request if one span of each endset satisfies a corresponding part of the request." (4/58)

The request itself specifies the four parts that must be matched:

> "A request specifies: **home-set**: where desired links are to be found; **from-set**: those spans of the docuverse wanted at the first side of the link; **to-set**: those spans of the docuverse wanted at the second side of the link; **three-set**: spans covering the types of link wanted." (from `links.md`, drawing on 4/58–4/60)

### The completeness guarantee itself

The operation must return **all** qualifying links:

> "This returns a list of **all** links which are (1) in <home set>, (2) from all or any part of <from set>, and (3) to all or any part of <to set> and <three set>." (FINDLINKSFROMTOTHREE, 4/69)

And the guarantee that makes "all" achievable at scale — that nothing is silently dropped because of the surrounding volume of irrelevant links:

> "THE QUANTITY OF LINKS NOT SATISFYING A REQUEST DOES NOT IN PRINCIPLE IMPEDE SEARCH ON OTHERS." (4/60)

This is the **junk-link guarantee**: in a docuverse saturated with links, the search mechanism's performance and completeness on the matching subset cannot degrade because of all the non-matching links. As `links.md` puts it: "The quantity of links not satisfying a request does not in principle impede search on others - you can still do link-search and subdivide with constraints that only deal with parts of the system."

### Why this matters

Without this guarantee, a search could return a *partial* result — fast, but silently omitting matches buried among millions of junk links. Nelson's design requires the opposite: filtering is by **address matching on endsets**, not content inspection, so the system can isolate the exact qualifying set. Combined with paginated retrieval (FINDNEXTNLINKSFROMTOTHREE handles "avalanches of material"), every link meeting all four criteria is enumerable and returned, none silently dropped.

**In short:** the required guarantee is that link search is **complete over the four-part constraint** (home, from, to, type) and that this completeness is *invariant to the number of non-satisfying links in the docuverse* (4/58–4/60).
