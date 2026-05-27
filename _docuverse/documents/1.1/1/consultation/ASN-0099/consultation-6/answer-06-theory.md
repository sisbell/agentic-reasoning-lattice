## Question 6 [theory]

> When a reader queries V-positions that lie outside the document's arrangement domain, was FINDLINKS designed to (a) reject the query, (b) silently project onto the in-domain subset, or (c) leave the handling to a higher protocol layer above the abstract operation?

The FEBE search model is permissive by design — option **(b), silent projection** onto the in-domain subset.

Three principles converge on this:

**1. Spans may refer to empty regions without error.** "A span that contains nothing today may at a later time contain a million documents" [LM 4/25]. The system already accepts under-populated span specifications as well-formed input, so an out-of-domain V-range is not categorically different from an empty in-domain range.

**2. Link search is permissive by construction.** "A link satisfies a search request if one span of each endset satisfies a corresponding part of the request" [LM 4/58]. The phrasing in FINDLINKSFROMTOTHREE — "from all or any part of `<from set>`" [LM 4/69] — is deliberate. Out-of-domain portions contribute nothing; in-domain portions match normally. Nothing in this semantics turns on whether queried positions are currently bound.

**3. FEBE absorbs friction.** "The complications of the protocol are to be handled invisibly by programs in the user's front-end machine, leaving the user free to think about other things" [LM 4/61]. Forcing front ends to validate every span against current document extents before querying would invert the protocol's purpose.

The corollary makes the efficiency story explicit: "THE QUANTITY OF LINKS NOT SATISFYING A REQUEST DOES NOT IN PRINCIPLE IMPEDE SEARCH ON OTHERS" [LM 4/60]. Out-of-domain regions are conceptually identical to "regions with no matching links" — the search proceeds, returns what matches, and remains efficient regardless of how much of the query falls outside the live arrangement.

A front end may of course validate before issuing the call — that's a sensible UX convenience. But it is not a FEBE obligation, and the abstract operation is specified to tolerate well-formed but partially-empty span-sets without rejection.

NEED_RAW: 4/58-4/60 — the curated material captures the search semantics, but if you want me to confirm Nelson nowhere added an explicit "out-of-V-extent rejection" clause around these pages, the raw scan would settle it.
