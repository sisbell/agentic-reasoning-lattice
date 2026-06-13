## Question 7 [theory]

> Must the count reflect the link store exactly as it stands at the instant of inquiry, and what does the design say about a count's validity once subsequent link creation or retraction has occurred?

## Short answer

Nelson specifies a counting operation — `FINDNUMOFLINKSFROMTOTHREE` — but the curated record does **not** contain a verbatim statement on its *temporal* semantics. There is no passage saying a count "must reflect the store exactly at the instant of inquiry," and none addressing what happens to a count after subsequent creation or retraction. So on the literal question the source is silent, and I flag that gap below.

What the design *does* establish forces a clear inference, though: **a count in Xanadu is a measurement of a query at evaluation time, not a stored or durable fact.** It is therefore a snapshot, and the architecture carries no obligation that an old count remain valid once the link store changes. Below is the reasoning, grounded in what Nelson does say.

## A count is the cardinality of a search result — computed, not stored

Counting is defined on top of the link-search satisfaction predicate:

> "A link satisfies a search request if one span of each endset satisfies a corresponding part of the request." (4/58)

A count is thus `|{ links : predicate holds against the current store }|`. Because the predicate is evaluated against the store's *current* state, the number is definitionally state-dependent: a satisfying link created → it rises; a satisfying link retracted → it falls. Nothing in the spec turns that derived number into a fact the system is obliged to preserve.

The one guarantee Nelson *does* attach to this family of operations is about scalability, not durability:

> "THE QUANTITY OF LINKS NOT SATISFYING A REQUEST DOES NOT IN PRINCIPLE IMPEDE SEARCH ON OTHERS." (4/60)

That scopes a count to the *satisfying set of a specific request* — reinforcing that it is a per-request measurement, not a property of "the link store" as a whole.

## Why a count cannot be a durable truth about the store

Several stated design facts make an exact, persistent count incoherent:

**1. Serial arrival ≠ active count.** Link addresses are permanent and never renumbered:

> "The links designated by a tumbler address are in their permanent order of arrival." (4/31)
> "N.0.U.0.D.V.0.2.755 (the 755th link to which the document is home)" (4/31)

So you cannot read a live count off the highest link number. The "755th link" is a permanent address, not a promise that 755 links currently satisfy any request. Deletion confirms the divergence — it does not decrement the numbering:

> "DELETED LINKS (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" (4/9)

A retracted link leaves its address occupied and its content recoverable, while the active-arrangement count drops. "The count" is therefore relative to which frame you mean (current arrangement vs. a version/historical state) — it is not a single number.

**2. There is no global instant to be exact against.** The system is distributed and explicitly assumes partial failure:

> "It is a truism that 'computer networks are always broken.'" (4/75)

Each server answers from a *model*, not from ground truth:

> "Each server contains a continuously valid model or subrepresentation of the entire docuverse and (because of tumbler addressing) a model of the entire network." (4/72)
> "The contents can slosh back and forth dynamically." (4/72)

So even with *no* user edits, the same count question asked twice of the same server can change as its subrepresentation updates and content migrates. A count reflects what a given server's model can currently see and reach — not an exact instantaneous global census.

**3. Permanence in Xanadu attaches to identities and content, never to aggregates.** What the system guarantees as permanent and reconstructable are tumbler addresses, Istream content, and version states. Time itself is held outside the address:

> "Note that 'time' is not included in the tumbler. Time is kept track of separately." (4/18)

A count is none of those permanent objects. It is a derived aggregate over a mutable set, so it inherits none of the permanence guarantees.

## What this means for validity after mutation

Put together: a count answers "how many links satisfy this request, as this server models the store, in this version/time frame, right now." Once subsequent creation or retraction occurs, that number describes a **prior** state. The design provides no mechanism — and asserts no obligation — to keep an old count current; nothing stores it as a fact to be honored later. A returned count is a snapshot that goes stale on mutation, and re-establishing it requires re-asking the query.

This is the same line the architecture draws everywhere else between *what is preserved* (addresses, content, versions — reconstructable on demand) and *what is merely measured* (a query's current answer). The practical consequence is a recompute-on-read discipline for counts, not a cache-as-truth one.

## Genuine gaps (would need raw pages to close)

The strong claims above are inferences from adjacent, verified principles. Nelson's *explicit* wording on count semantics isn't in the curated material:

- **NEED_RAW: 4/58–4/60, 4/69** — the verbatim specification of `FINDNUMOFLINKSFROMTOTHREE` (the curated sources give only a curatorial gloss, "counts matching links," not Nelson's own text). This is where any explicit statement about instantaneous accuracy or staleness would live, if one exists.
- **NEED_RAW: 4/69** — whether `FINDNEXTNLINKSFROMTOTHREE` iterates a *frozen* list or re-evaluates each call. Nelson says it returns "no more than `<nlinks>` items past that link on that list" (4/69), which implies a materialized list but does not state whether that list is held stable against concurrent creation/retraction during pagination — a consistency-during-iteration question parallel to the count-validity one.

If you can pull those pages, that would either surface an explicit Nelson rule or confirm that count-freshness is left to the front/middle end — which is what the surrounding design implies.
