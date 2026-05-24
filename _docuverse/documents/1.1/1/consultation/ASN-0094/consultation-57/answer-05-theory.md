## Question 5 [theory]

> Was Nullify designed to record one retraction event per call (multiset/audit semantics), or to assert the target's nullified status once regardless of call multiplicity (set semantics)?

I need to flag a gap here: **"Nullify" does not appear as a named operation in the curated sources from Literary Machines that I have direct access to.**

The 17 FEBE commands of XU.87.1 documented in my curated sources are: CREATENEWDOCUMENT, CREATENEWVERSION, INSERT, DELETEVSPAN, COPY, APPEND, RETRIEVEV, REARRANGE, MAKELINK, FINDLINKSFROMTOTHREE, FINDNUMOFLINKSFROMTOTHREE, FINDNEXTNLINKSFROMTOTHREE, RETRIEVEDOCVSPAN, RETRIEVEDOCVSPANSET, SHOWRELATIONOF2VERSIONS, FINDDOCSCONTAINING, and RETRIEVEENDSETS. No "Nullify" command is listed.

NEED_RAW: 4/61-4/70 (FEBE command list), 2/43, 2/59-2/60 (withdrawal, peremptory challenge), 4/9, 4/12 (deleted bytes/links state), 5/19-5/20 (Publisher Contract withdrawal terms)

That said, my design principles for related operations point in a clear direction:

**1. Append-only storage suggests audit semantics for events, but set semantics for state.**

From my own writing on storage: I designed the system so changes "flow into the storage system, filed, as it were, chronologically" (2/14). Every change is preserved. But the deletion *state* is binary:

> "DELETED LINKS (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" (4/9)

A link is either in the "currently addressable" state or the "deleted/awaiting historical backtrack" state. It's not in a state that distinguishes "deleted once" from "deleted three times."

**2. The retraction *event* should be recorded; the retracted *status* is unitary.**

This follows from historical backtrack as a fundamental guarantee. You must be able to ask "when was this nullified, and by whom?" — which requires per-event recording. But asking "is this nullified?" returns a single answer.

So if I were specifying Nullify formally, the design intent I would want preserved is:
- **The state assertion is set-semantic** — a target is nullified or it is not; redundant nullifications don't multiply the status
- **The event log is multiset/audit-semantic** — each call generates a retraction record with timestamp and originator, preserved in the historical trace enfilade

The two layers are separable: the *fact of nullification* is a property of the target (set), while the *history of nullification calls* is a sequence of events (multiset). My append-only storage was specifically designed to make this separation natural — state is derived by walking the event history, but state itself is canonical.

Without seeing the specific Nullify specification you're working from, I cannot tell you which layer it was meant to formalize. If it's the state predicate, it should be set-semantic and idempotent. If it's the event recorder, it should be multiset-semantic and audit-preserving.
