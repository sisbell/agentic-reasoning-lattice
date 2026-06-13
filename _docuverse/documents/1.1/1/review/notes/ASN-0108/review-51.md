# Review of ASN-0108

This is a careful, rigorous ASN. The wp analysis in W2 (identity vs. offset cursor) is genuinely non-trivial and correct; the W9a count formula checks out at every regime (m=0, exact multiple, non-divisible, N>m); the W9b per-link multiplicity bound and its non-circular interplay with W5's no-re-delivery are sound; and the edge-case coverage (empty Match, orphaned cursor, exhaustion-by-empty-window, inflow behind vs. ahead of the cursor) is thorough. Two issues remain.

## REVISE

### Issue 1: W0 requires κ injective but not *total*; the least-covered-I-address key is partial on Match

**ASN-0108, "The Enumeration Order" / W0**: "We posit an **ordering key**: a function `κ` assigning to each link address a value in some totally-ordered set `(K, <_K)`" and "the relation `≺` induced by an injective key `κ` … is a strict total order … so `Match(q, Σ)` has a unique listing `a_1 ≺ … ≺ a_m`."

**Problem**: A strict total order and a unique enumeration require κ to be *total* on Match (defined at every matching link), not merely injective. W0 names only injectivity. The gap is not academic, because the **least-covered-I-address key** — which the ASN asserts is a valid κ satisfying W0, W5, and W8 — is not guaranteed total. That key orders a link by "the least I-address that [a fixed designated] slice covers," and the designated slice is "a non-empty selection of slots" — non-empty *as a set of slots*, not guaranteed non-empty *in coverage*. A link with `e₁ = ∅` and `e₂ = ∅` is permitted (L3, ASN-0043, requires only the type slot non-empty; `∅` is a valid endset), and such a link can lie in Match by matching via its type slot (discoverability ranges over *all* slots — ASN-0127 LP12 — and type endsets may reference any address — L4). With a designated `{from, to}` slice its coverage is `∅`, so κ is undefined there; the composite tiebreaker `(endpoint-boundary, a)` inherits the partiality through its first component. This directly contradicts the positing of κ as "a function assigning to each link address a value": the least-covered-I-address key, as described, does not assign a value to every link address. Either the positing or the assertion that this key satisfies W0/W5/W8 must give.

**Required**: State totality of κ on Match as an explicit W0 premise alongside injectivity; and resolve the contradiction for the least-covered-I-address key — either constrain its designated slice to guarantee non-empty coverage on every matching link, or attach the totality caveat where it is claimed to satisfy W0/W5/W8. Note the obvious fix "draw the key from the *matched* slot" is not free: it restores totality but destroys the permanence/state-stability the ASN relies on, since the matched slot varies with state — exactly the fixity tension the ASN already identifies.

### Issue 2: Trailing-gloss restatement (anti-bloat)

**ASN-0108, W11**: the blockquote — "Any two readers issuing the same query with the same cursor and the same `N` against the same state receive the identical batch … The split is a system property — determined by the enumeration order and the window size — not a reader-side choice." — is followed by the gloss "Two readers paging the same search with the same window size traverse the same boundaries, because those boundaries are computed from the order and the size, both of which are properties of the system rather than of the reader."

**Problem**: The gloss restates the blockquote in different words ("determined by the enumeration order and the window size / a system property" ≈ "computed from the order and the size, both of which are properties of the system"; "Any two readers … receive the identical batch" ≈ "Two readers … traverse the same boundaries"). The only new element is the Nelson analogy; the restating clause is skippable. This is the trailing-restatement form of the accretion the note's classifier targets, here in a section outside the recently-tightened W8–W9b region.

**Required**: Keep the Nelson analogy sentence; drop the restating clause ("because those boundaries are computed from the order and the size, both of which are properties of the system rather than of the reader").

## OUT_OF_SCOPE

The major adjacent topics are correctly handled and need no flagging: multi-document enumeration order, eventual-delivery under a non-allocation-monotone key, the cross-call completeness invariant, recoverability of a non-permanent cursor beyond window length, and delivery/progress-count correspondence are all deferred to the Open Questions rather than claimed; count-only, full-set, MAKELINK, FOLLOWLINK, and BEBE are absent as required.

VERDICT: REVISE
