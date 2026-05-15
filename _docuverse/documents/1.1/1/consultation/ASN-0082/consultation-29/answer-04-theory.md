## Question 4 [theory]

> In Xanadu's design, does DELETE (DELETEVSPAN) consist solely of the V-arrangement contraction, or are there additional phases — link backref updates, version-state changes, allocation bookkeeping — that compose with the arrangement transformation?

# DELETE in Xanadu: Just V-arrangement Contraction

DELETE is conceptually V-arrangement contraction. The phases you name — link backref updates, version-state changes, allocation bookkeeping — don't compose with it as separate steps, because the architecture was designed to make them unnecessary or automatic.

## Link backref updates: none

Links attach to spans of bytes via Istream addresses, not V-positions. The link table is not traversed and rewritten when DELETE runs.

> "A Xanadu link is not between points, but between spans of data... it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them." [LM 4/42]

Survivability is a structural consequence of content-addressed linking. The link still points to the same I-address; that I-address still exists in Istream. Whether the link is currently *satisfiable* on retrieval is a query-time concern, not a write-time bookkeeping phase.

## Allocation bookkeeping: none

Storage is append-only. The bytes you "delete" remain in Istream forever. The diagram on page 4/9 explicitly marks "DELETED BYTES" as a valid state:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

There is no free list, no compaction, no reclamation. The whole point of the model is that destruction is impossible.

## Version state: implicit, not a separate phase

The "ongoing braid" model treats each document as evolving through time [LM 2/14]. DELETE doesn't run a discrete snapshot-creation phase. It changes what bytes the current arrangement maps to. Previous arrangements remain reachable through historical backtrack, and other documents are unaffected:

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

## At the protocol level

The FEBE specification of DELETEVSPAN is one sentence: "This removes the given span from the given document" [LM 4/66]. The brevity reflects the design intent — what would be expensive composing phases in a conventional system (link maintenance, free-list update, snapshot allocation) are absorbed by the underlying invariants:

- Content-addressed linking absorbs link maintenance
- Append-only storage absorbs allocation
- The braid model absorbs versioning

DELETE *is* the arrangement transformation. Nothing else needs to run alongside it.

NEED_RAW: 4/66-4/67 for the full DELETEVSPAN command listing, to confirm whether the FEBE specification documents any return values or side effects beyond the V-arrangement contraction itself.
