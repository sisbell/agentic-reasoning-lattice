## Question 9 [theory]

> Does a description that matches zero links assert that no such link has ever existed, or only that none exists now?

## Short answer

A description that matches zero links asserts only that **none exists now** — that no currently addressable link satisfies the request. It does **not** assert that no such link has ever existed. The search model queries the present state of the docuverse, while deleted or superseded links persist in storage outside that present view.

## Why this is the case

**1. Search returns currently addressable links, not historical ones.**

The link-search operation is a present-tense query. As Nelson specifies it:

> "This returns a list of all links which are (1) in <home set>, (2) from all or any part of <from set>, and (3) to all or any part of <to set> and <three set>." (4/69)

> "A link satisfies a search request if one span of each endset satisfies a corresponding part of the request." (4/58)

Both describe matching against links *as they presently are*. There is no temporal predicate in the request itself, so a zero result is a statement about the current population of addressable links — not about all links that have ever been.

**2. Deleted links leave the addressable set but continue to exist.**

Link deletion does not destroy the link. It moves it into a state Nelson explicitly names as a valid document state:

> "DELETED LINKS (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" (4/9)

The phrase "not currently addressable" is decisive. A deleted link is precisely the case where a description matches zero links *now* even though the link *did* exist. It remains in storage "awaiting historical backtrack functions" and "may remain included in other versions" — so the same description could match it again under a different version or via historical backtrack.

**3. Time is tracked separately, so the default search is over "now."**

> "Note that 'time' is not included in the tumbler. Time is kept track of separately." (4/18)

Because time is not part of the address and not part of the standard request, an ordinary link search resolves against the current arrangement. To ask "did such a link ever exist?" you would have to invoke the separately-maintained historical/backtrack machinery — a different question than the one a zero-match search answers.

## The guarantee, stated precisely

- **Zero matches means:** "No link satisfying this description is currently addressable in the version/state searched."
- **Zero matches does NOT mean:** "No such link has ever existed." A matching link may have been deleted (now "not currently addressable"), or may exist only in a prior version or under historical backtrack.

This mirrors the same Istream/Vstream distinction that governs content: just as a "deleted" byte persists in Istream while vanishing from the current Vstream, a deleted link persists in storage while dropping out of the currently addressable set. Absence from a present-tense search is non-existence *in the view*, not non-existence *in the archive*.

---

NEED_RAW: 4/58-4/60, 4/69 — The curated sources establish each component fact (search returns currently-addressable links; deleted links become "not currently addressable" but persist; time is tracked separately). The synthesis — that a zero-match search is therefore a claim about the present and not about all history — is a logical consequence of these verified facts rather than a verbatim statement by Nelson. If you want a direct textual confirmation that search is explicitly scoped to the present (versus historical) state, the raw link-search pages 4/58-4/60 and the FINDLINKS command definitions on 4/69 are where to look.
