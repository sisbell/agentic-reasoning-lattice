## Question 9 [theory]

> If part of the spec-set names content that no longer exists or was never established, what must the operation do — refuse entirely, deliver what it can, or signal the gap?

## Short answer

Nelson's architecture points firmly toward **deliver what it can** — not refuse, and not raise an error. A spec-set that names absent content is a *normal, legal state* in Xanadu, not a fault. The operation resolves the portions that exist and the gap is represented implicitly by absence (empty result for that part), with the span's boundaries preserved.

There is no curated passage where Nelson gives explicit per-operation error semantics ("on missing content, do X"). The conclusion below is built from the design principles he *does* state.

## Why "refuse entirely" is wrong

Two design choices make whole-request refusal contrary to Nelson's intent.

**1. Spans address ranges, not stored objects.** A span is defined by its endpoints; what lies between is implicit and may be empty:

> "The first point of a span may designate a server, an account, a document or an element; so may the last point. There is no choice as to what lies between; this is implicit in the choice of first and last point." (4/25)

> "A span that contains nothing today may at a later time contain a million documents." (4/25)

So a span resolving to nothing is explicitly an anticipated condition, not an error. The address remains valid even when unoccupied.

**2. Ghost elements make "nothing stored there" a first-class case.** Addresses can be referenced with nothing behind them:

> "It is possible to link to a node, or an account, even though there is nothing stored in the docuverse corresponding to them." (4/23)

> "Indeed, there is no need for the presence of elements at the addresses specified. Link types may be ghost elements." (4/45)

A system that treated absent content as grounds for refusal would contradict the ghost-element design, where absence is intentional and useful.

## The explicit precedent: partial satisfaction in link search

The one place Nelson states a rule about unsatisfiable parts of a request is link search, and it is unambiguous — gaps don't block the rest:

> "THE QUANTITY OF LINKS NOT SATISFYING A REQUEST DOES NOT IN PRINCIPLE IMPEDE SEARCH ON OTHERS." (4/60)

The satisfaction model returns what matches and silently omits what doesn't:

> "A link satisfies a search request if one span of each endset satisfies a corresponding part of the request." (4/58, per the operations summary)

This is the architectural analogue for retrieval: serve the satisfiable portion, drop the unsatisfiable portion, never fail the whole.

## On "signal the gap"

Nelson's model signals the gap *structurally* rather than through an error code. Because content within a span is implicit in the boundaries (4/25), the caller compares what was requested against what came back — the missing region is self-evident. For retrieval, `RETRIEVEDOCVSPAN` / `RETRIEVEDOCVSPANSET` let a front end establish a document's actual extent, so a front end can detect that part of its spec-set fell outside live content. There is no curated passage describing an explicit "gap marker" returned inline by `RETRIEVEV`.

## Where this exceeds the curated record

The curated sources establish the *principle* (absence is legal; partial satisfaction is the model for search) but do not contain an explicit statement of `RETRIEVEV`'s behavior when its spec-set includes never-established or deleted-and-gone content.

NEED_RAW: 4/66-4/70 (the RETRIEVEV / RETRIEVEDOCVSPAN / FINDDOCSCONTAINING command definitions) to confirm whether Nelson specifies an error return vs. silent partial delivery for content retrieval as he does for link search at 4/58-4/60.
