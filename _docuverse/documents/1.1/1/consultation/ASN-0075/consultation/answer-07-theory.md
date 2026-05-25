## Question 7 [theory]

> What must the design guarantee about the ordering of deleted content when it is returned — must the original sequence be preserved?

# Ordering of Deleted Content When Returned

**Yes — the original sequence must be preserved, but this guarantee is structural. It emerges from how the system handles versions, not from any separate "deletion recovery" mechanism.**

The question implicitly assumes a model where "deleted content" exists as a free-floating set that gets "returned." That isn't how the system works. There is no recovery bin. When content is "deleted," what actually happens is that a new Vstream arrangement is created that excludes those bytes from the current view — but the previous Vstream arrangement, with its full ordering intact, remains permanently accessible.

## What "Deletion" Actually Is

From page 4/9:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

The phrase "awaiting historical backtrack functions" is the key. Recovery happens by accessing previous versions, not through some separate undelete operation. The content's sequence within those previous versions *is* its sequence — it has nowhere else to be.

## The Three Ordering Guarantees

**1. Each version's arrangement is immutable.** From page 2/15:

> "The true storage of text should be in a system that stores each change and fragment individually, assimilating each change as it arrives, but keeping the former changes; integrating them all by means of an indexing method that allows any previous instant to be reconstructed." [LM 2/15]

To reconstruct any previous instant, the system must preserve the ordering as it was at that instant. Without ordering preservation, historical backtrack is meaningless.

**2. Time-indexed retrieval returns content in its original sequence.** Also from 2/15:

> "The file management system we are talking about automatically keeps track of the changes and the pieces, so that when you ask for a given part of a given version at a given time, it comes to your screen." [LM 2/15]

When the system delivers "a given part of a given version," it delivers that part *as it was* — including its position in the document's sequence.

**3. Content persisting in other documents takes those documents' orderings.** From page 4/11:

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

When deleted content is found through a transclusion in another document, it appears in *that* document's sequence — not in its original position. This is correct. Position is meaningful only within a particular arrangement.

## The Deeper Principle

From page 2/19, on prismatic storage:

> "There is thus no 'basic' version of a document set apart from other versions—'alternative' versions—any more than one arrangement of the same materials is a priori better than other arrangements." [LM 2/19]

There is no "true" ordering of content separate from a particular version. Ordering is always per-version. So "preserving the original sequence" means preserving *each version's* sequence — which the system does by preserving the version itself.

## Confirmed by Version Comparison

The SHOWRELATIONOF2VERSIONS operation explicitly returns ordered results. From page 4/70:

> "This returns a list of ordered pairs of the spans of the two spec-sets that correspond." [LM 4/70]

The system tracks ordered correspondence across versions. This works precisely because each version's ordering is permanent.

## What Implementations Must Provide

For a conforming implementation:

- **Per-version Vstream arrangements are immutable once committed.** No backfilling, no retroactive reordering.
- **A request for "version V at time T" must return content in the sequence it had in version V.** Not in I-address order, not in arrival order — in V's Vstream order.
- **When retrieving content that was deleted, the response must specify which version's arrangement is being returned**, because the same bytes can occupy different positions in different versions.
- **A "deleted content" query without a version context is malformed.** There is no canonical ordering for orphaned bytes — only orderings within particular arrangements.

## Summary

The design guarantees the original sequence of deleted content through the version mechanism:

- Each version has a permanent, immutable Vstream arrangement
- Historical backtrack reconstructs any past version completely
- Deleted content is recovered by accessing the version where it existed
- The original sequence is preserved *as the version's sequence*

The ordering question dissolves into the versioning question. Get the versions right, and the ordering follows automatically — because "the original sequence" *is* a property of a particular version, not of the bytes themselves.
