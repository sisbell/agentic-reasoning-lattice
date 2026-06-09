## Question 10 [theory]

> When a link is retracted, what must the system guarantee about its absence from any subsequent answer to the same four-set inquiry?

## Link Retraction and the Four-Set Inquiry

The "four-set inquiry" is `FINDLINKSFROMTOTHREE`, which is constrained by four endsets — the home-set plus the from-set, to-set, and three-set (type):

> "This returns a list of all links which are (1) in <home set>, (2) from all or any part of <from set>, and (3) to all or any part of <to set> and <three set>." (4/69)

A link qualifies for inclusion under the satisfaction rule:

> "A link satisfies a search request if one span of each endset satisfies a corresponding part of the request." (4/58)

### What "retraction" means

A link's owner may delete (retract) it — this is the owner's administrative right, distinct from link *survivability* (which concerns edits to the content a link points at). When retracted, the link enters a defined state:

> "DELETED LINKS (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" (4/9)

### The guarantee

The operative phrase is **"not currently addressable."** This scopes the guarantee precisely:

1. **Absence from the current context.** A retracted link must not be returned by any subsequent `FINDLINKSFROMTOTHREE` that is evaluated against the version/document from which it was retracted, no matter how the from/to/three constraints are arranged. Even if its endsets would still satisfy the request, the link no longer satisfies the home-set constraint as a *currently addressable* member of that document. Its absence is total within that context.

2. **The absence is scoped, not destruction.** Nelson's model is non-destructive. The link is removed from current addressability but is *not* erased:
   - It remains in Istream, "awaiting historical backtrack functions" — so a *time-qualified* or *historical* inquiry into a prior state can still surface it.
   - It "may remain included in other versions" — so a four-set inquiry whose home-set covers a version that incorporated the link before retraction can still legitimately return it.

So the precise guarantee is: **once retracted, the link is consistently and completely absent from answers to the same four-set inquiry posed against the current state of its home document — but it is not guaranteed absent from inquiries scoped to prior states or to other versions that captured it.**

3. **Absence is "clean."** The search model guarantees that a retracted (or otherwise non-matching) link's removal does not corrupt results for others:

> "THE QUANTITY OF LINKS NOT SATISFYING A REQUEST DOES NOT IN PRINCIPLE IMPEDE SEARCH ON OTHERS." (4/60)

A retracted link simply drops out of the satisfying set; it neither lingers as a phantom result nor obstructs retrieval of the links that do still satisfy the inquiry.

### Caveat on scope

NEED_RAW: 4/58-4/60, 4/68-4/69 — Nelson specifies the deleted-link *state* ("not currently addressable," 4/9) and the search *satisfaction model* (4/58-4/60), but the curated sources do not contain an explicit verbatim statement tying retraction to a formal idempotency guarantee on repeated `FINDLINKSFROMTOTHREE` results. The conclusion above is the consistent reading of "not currently addressable" applied to the four-set search, not a directly quoted guarantee. If you need Nelson's exact wording on post-deletion search behavior, those pages (4/58-4/60, 4/68-4/69) should be checked against the raw scans.
