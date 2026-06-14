## Question 9 [theory]

> If someone asks "is everyone done editing?" while another user is mid-edit, what must that answer be taken against — a single frozen view of the store — for the answer to be trustworthy rather than accidental?

## Short answer

It must be taken against **one version of the store at one instant** — a single cross-section of what I called the *space-time vortex*: one *canonical* state of the append-only store, fixed at a single point in time. That is the only referent against which a whole-store question like "is everyone done editing?" has a definite truth value. Asked against the store as a *live, moving* thing, a "yes" gets stitched together across a transition and is true of no actual instant — correct by accident of timing, not because the store was ever quiescent.

Here is why my design forces that, and why the alternative is merely accidental.

## 1. Every read in my model is already indexed to an instant

The unit you may address is *a given version at a given time* — never "the document" as a live moving object:

> "...when you ask for a given part of a given version at a given time, it comes to your screen." (2/14–2/15)

> "THE PART YOU WANT COMES WHEN YOU ASK FOR IT." (2/16)

So the frozen view is not an extra discipline bolted on for queries. It is the *only kind of thing the system lets you ask about*. A question over the whole store is just a question over one version-at-an-instant, taken wide.

## 2. The instant is a first-class, addressable object — the space-time vortex

> "A document is really an evolving ONGOING BRAID." (2/14)

> "...successive versions of the document, at successive instants of time, as alive in this space-time vortex." (2/15)

A "single frozen view of the store" is precisely **one cross-section of that braid** — the store as it stands at one time-coordinate.

## 3. Why such a coherent instant always exists, even mid-edit

Because storage is append-only and every change leaves the file in *canonical order*:

> "...we create an append-only storage system. User makes changes, the changes [flow] into the storage system, filed, as it were, chronologically." (2/14)

> "It was instantaneous and permanent and could grow indefinitely. All changes, once made, left the file remaining in canonical order, which was an internal mandate of the system." (1/34)

Each change is atomic *with respect to canonical order*, so the store is never observed half-changed. The other user's mid-edit, relative to any chosen snapshot, is either already assimilated (a new canonical state) or not yet (the prior canonical state). There is no smeared in-between to read. At the server level I stated the same property: each server is "at all times unified and operational," every change "leaving each server in canonical operating condition" (4/72). There is always a single coherent state to pin the question to.

## 4. The crux: trustworthy vs. accidental

"Is everyone done editing?" quantifies over many parts/users. If you read each part at a *different* moment — letting the store advance under you — you have quantified over a collection of states **that never coexisted**: you might clear user A against the pre-edit state and user B against the post-edit state and report "everyone done" for a configuration that held at no single instant. That is the accidental answer — right only by a fluke of interleaving.

Pinning every part of the evaluation to **one** frozen view forces the parts to coexist. The predicate is then true *of that state* — and that state is a real, canonical, addressable object, not a timing artifact. That coexistence is exactly what converts the answer from accidental to trustworthy. Note also what the snapshot pins: content-state *as of* a time-coordinate, since time is a separate axis from the address — "Time is kept track of separately" (4/18). The frozen view is the address-space state as of one time.

## What I did *not* specify (flag)

I did not, in *Literary Machines*, specify a concurrent-edit session or locking protocol, nor a global "is everyone done editing?" quiescence query. The design-intent reading of the session model is explicit on this: I leave the concurrency mechanics — how a reader obtains an isolated, single-instant view while others write — to the implementor. So the *machinery* of isolation here is an implementation concern (the territory your "Substrate Consistency and Isolation Model" work occupies), consistent with my design but beyond my text.

What I *did* fix — and what your trustworthiness requirement actually rests on — is two things: (a) every read is of a **version-at-an-instant**, and (b) the store is **always in canonical order**. Those two guarantees are what make a single frozen view well-defined in the first place, and therefore what make the answer trustworthy rather than accidental. The implementation must simply ensure the query is evaluated against *one* such view, not re-derived across several.
