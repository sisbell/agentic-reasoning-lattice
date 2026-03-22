## Question 4 [nelson]

> Must the system preserve a record of the original ordering so that the prior arrangement can be recovered, or is rearrangement a one-way transformation of document structure?

The system **must preserve the original ordering**. Rearrangement is not a one-way transformation. This follows from multiple converging guarantees in Literary Machines.

## The Storage Model Requires It

Nelson's storage architecture is explicitly append-only. Changes accumulate; nothing is overwritten:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

> "The true storage of text should be in a system that stores each change and fragment individually, assimilating each change as it arrives, but keeping the former changes; integrating them all by means of an indexing method that allows any previous instant to be reconstructed." [LM 2/15]

The phrase "any previous instant" is key. Not "any previous version" — any previous *instant*. This means every edit, including REARRANGE, produces a recoverable state.

## The I/V Separation Makes It Structural

REARRANGE is a pure Vstream operation. It changes which Istream addresses appear at which Vstream positions. The content bytes are untouched:

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." [LM 4/30]

The prior arrangement is simply a prior V→I mapping. Since Istream content is immutable and the storage system records all changes chronologically, the old mapping is recoverable by reconstructing the state before the REARRANGE was applied.

## Historical Backtrack Is a Design Requirement

Nelson treats recoverability not as a feature but as the fundamental purpose of the storage system:

> "Under many circumstances the writer, or 'text user', needs to reach back to a former condition. This is in the nature of creative work." [LM 2/14]

> "Being able to go back through changes, and perhaps restore an earlier state, is called the problem of historical backtrack." [LM 3/13]

> "The file management system we are talking about automatically keeps track of the changes and the pieces, so that when you ask for a given part of a given version at a given time, it comes to your screen." [LM 2/15]

The "historical trace enfilade" was specifically designed for this purpose:

> "we redesigned Barus's linking enfilade system, designed the historical trace enfilade, and formulated the general theory of enfilades" [LM 1/36]

## The Ongoing Braid Metaphor

Nelson's central metaphor makes one-way transformation architecturally incoherent:

> "A document is really an evolving ONGOING BRAID." [LM 2/14]

> "Think of the process of making editorial changes as re-twisting this braid when its parts are rearranged, added or subtracted... and think then of successive versions of the document, at successive instants of time, as alive in this space-time vortex." [LM 2/15]

A braid accumulates strands. It does not cut them away. REARRANGE adds a new twist to the braid; the prior twist remains in the structure.

## One Nuance: Version Boundaries vs. Continuous History

The FEBE protocol separates *editing within a version* (INSERT, DELETE, REARRANGE) from *creating a new version* (CREATENEWVERSION). The curated sources establish that the storage system records all changes at all times, not merely at version boundaries — Nelson says "successive instants of time," not "successive versions." But the exact granularity of recovery (every keystroke? every command? every save?) is not specified at the FEBE level.

What IS specified is the principle: the system keeps all former changes, and any previous instant can be reconstructed. REARRANGE is a change. Therefore the prior arrangement is kept and recoverable.

NEED_RAW: [4/67] — The REARRANGE command specification may contain additional detail about whether it implicitly creates a recoverable checkpoint. The curated source only gives the mechanical description ("transposes two regions of text").
