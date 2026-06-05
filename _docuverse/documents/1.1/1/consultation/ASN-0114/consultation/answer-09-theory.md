## Question 9 [theory]

> May the returned specification ever describe content that the link does not actually connect at that end, and what guarantee forbids such over- or under-coverage?

No. The returned specification must describe **exactly** the bytes the link connects at that end — never more (over-coverage), never less (under-coverage). The endset *is* the connection; retrieval returns that endset, so there is nothing else for it to describe.

## Why there is no gap to over- or under-cover

A link end is not a pointer to a region that the system then *summarizes*. The endset is itself defined as the set of bytes the link is on:

> "A link may be to or from an arbitrary set of bytes. These may be anywhere in the docuverse." (4/42)

> "The from-set may be an arbitrary collection of spans, pointing anywhere in the docuverse. Similarly, the to-set may be an arbitrary collection of spans pointing anywhere in the docuverse." (4/43)

`RETRIEVEENDSETS` returns precisely these structures:

> "This returns a list of all link end-sets that are in <spec set>." (4/70)

Because the from-set/to-set *are* what the link is "from" and "to," a faithful return cannot describe content the link does not connect — that would mean returning a different endset than the one stored.

## The guarantee that forbids inexactness: exact span-set coverage

Spans are the representation, and Nelson's guarantee is that a span-set can designate a selection **exactly, with nothing extra**:

> "Note: if you want to designate a separated series of items exactly, including nothing else, you do this by a span-set, which is a series of spans." (4/25)

This is the key clause. A single coarse span hangs a whole subtree off the tumbler line ("a zone hanging down from the tumbler line," 4/25), which would *over-cover* if the connected bytes were discontiguous. The span-*set* exists precisely so that discontiguous, exact selections — "these bytes and no others" — are representable. An endset that touches "a broken, discontiguous set of bytes" (4/42) is therefore returned as the corresponding span-set, not as a wider enclosing span.

## The survivability guarantee keeps it exact over time

Editing could otherwise create drift between "what the link claims" and "what it actually touches." Survivability forbids that, because the link tracks the surviving bytes themselves:

> "A Xanadu link is not between points, but between spans of data... it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them." (4/42)

> "Links between bytes can survive deletions, insertions and rearrangements, if anything is left at each end." (4/43)

So after edits the endset shrinks to exactly the bytes that remain — it does not retain ghosts of deleted bytes (no over-coverage) and does not drop surviving attached bytes (no under-coverage).

## Summary

The returned specification may never describe content the link does not connect at that end. The endset is definitional, so retrieval has nothing wider or narrower to report; the **exact span-set representation** ("exactly, including nothing else," 4/25) forbids over- or under-coverage in the representation, and **survivability** (4/42–4/43) preserves that exactness across editing.

---

NEED_RAW: 4/70 — the curated text gives `RETRIEVEENDSETS` as "returns a list of all link end-sets that are in <spec set>" but does not state in Nelson's own words whether retrieval is guaranteed *exact* (vs. merely *covering*). If you want a verbatim Nelson guarantee on exactness of the *returned* spec (rather than the inferential argument above from 4/25 and 4/42), pages 4/58–4/60 and 4/70 should be checked. This bears directly on the project's open "covering vs. exact" (S7) question.
