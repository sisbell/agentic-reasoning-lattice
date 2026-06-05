## Question 5 [theory]

> What must the design promise about not exposing, naming, or hinting at the link's other ends when only one end is requested?

I attempted to open the raw page scans, but the only tools available to me here are the MCP connectors (Gmail/Calendar/Drive) — I don't have file-read access in this session, so I'm working from the verified curated sources.

## Short answer

The curated sources do **not** contain a design promise that one-ended link requests must avoid *exposing, naming, or hinting at* the link's other ends. In fact, Nelson's stated design intent runs the **opposite** way: a link's value is precisely that its other ends are discoverable. So before answering as if such a promise exists, I want to flag the mismatch rather than manufacture a guarantee Nelson didn't make.

## What the sources actually establish

**1. The search model is "one span of each endset," and unconstrained ends are simply unconstrained — not hidden.**

> "A link satisfies a search request if one span of each endset satisfies a corresponding part of the request." (4/58)

A request specifies a home-set, from-set, to-set, and three-set; you may constrain some and leave others open. Leaving an end unconstrained means "match anything there," which is a query-breadth statement, not a confidentiality promise.

**2. Discovery of the other ends is the point, and it is bidirectional.**

> "The reader should be able to ask, for a given document or place in the document, 'What connects here from other documents?'—and be shown all these outside connections without appreciable delay." (2/46)

The system indexes links by all endsets so you can find a link from any side — the design *wants* the far ends reachable.

**3. Retrieving endsets is a distinct, explicit operation.**

`FINDLINKSFROMTOTHREE` returns link identities matching the constraints (4/69); `RETRIEVEENDSETS` "returns a list of all link end-sets that are in <spec set>" (4/70). So a search constrained on one end returns link addresses; the contents of the other endsets come from a separate retrieval step. This is a mechanical separation of operations, not a stated promise to suppress the other ends.

**4. The one-sided link is the only "single end" concept in the sources — and it concerns terminology, not concealment.**

> "Unfortunate terminological problem: since it has only one side, we use the first endset to designate the matter pointed at. To call this 'from' is inane." (4/48)

A one-sided link genuinely has no other end to expose; this is about a link type that points to material without a counterpart, not about withholding ends from a query.

## Flag

The specific guarantee in your question — that the design must promise **not to expose, name, or hint at** a link's other ends when only one end is requested — is not stated in the curated material, and it appears to conflict with Nelson's affirmative bidirectional-discovery intent. If you believe Nelson states such a non-disclosure / minimal-result property in the link-search pages, it would be in passages I can't verify from the curated set:

NEED_RAW: 4/56–4/60 (link search and result semantics), 4/48 (one-sided links), 4/69–4/70 (FINDLINKSFROMTOTHREE, RETRIEVEENDSETS)
