## Question 8 [nelson]

> Is there a guarantee that the sequence of all additions to a document is permanently recoverable — not just the current state, but the full history of how the document grew?

# Yes — with an important nuance about what is guaranteed

Nelson guarantees that **all content is permanently stored** and that **any previous state of a document can be reconstructed**. Together these imply the full growth history is recoverable. But the guarantee is framed as *state reconstruction*, not *operation replay*.

## The explicit guarantee

The strongest statement is on page 2/15:

> "The true storage of text should be in a system that stores each change and fragment individually, assimilating each change as it arrives, but keeping the former changes; integrating them all by means of an indexing method that allows any previous instant to be reconstructed." [LM 2/15]

This commits to three things: each change is stored individually, no former change is discarded, and any previous instant is reconstructable.

The append-only storage model is the foundation:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

Content enters I-space and never leaves. "Deletion" removes content from V-space (the current arrangement) but leaves it intact in I-space:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

## The user-facing promise

Nelson promises the user can navigate backward through the full trajectory:

> "The user of such a system may scroll through an individual document, at successive instants of time, alive in the space-time vortex." [LM 2/15]

> "The file management system we are talking about automatically keeps track of the changes and the pieces, so that when you ask for a given part of a given version at a given time, it comes to your screen." [LM 2/15]

The phrase "at successive instants of time" is key — this is continuous history, not periodic snapshots.

## The mechanism: the historical trace enfilade

Nelson designed a specific data structure for this purpose:

> "we redesigned Barus's linking enfilade system, designed the historical trace enfilade, and formulated the general theory of enfilades" [LM 1/36]

And the underlying enfilade properties ensure that edits preserve canonical order:

> "All changes, once made, left the file remaining in canonical order, which was an internal mandate of the system." [LM 1/34]

## The nuance

Nelson's guarantee is about **reconstructing states** ("give me this part at this time"), not about **replaying operations** ("show me each INSERT and DELETE in order"). The distinction matters:

- **Guaranteed:** Every byte ever added to I-space persists permanently. Any previous arrangement (V-space state) can be reconstructed. You can scroll through time to see the document at any historical instant.

- **Implied but not explicitly specified:** Whether the system records discrete operation events (INSERT at position 5, DELETE span 7-12) as a replayable log, or whether it stores states from which the operations can be inferred.

The append-only, chronological storage strongly implies that the sequence of additions is implicitly preserved — content arrives in order and is never overwritten. But the FEBE protocol specifies operations (INSERT, DELETE, REARRANGE) as commands to the back end without specifying whether those operations themselves are logged as discrete events.

## Summary

The answer is **yes** — the full history of how a document grew is permanently recoverable. This follows from three interlocking guarantees:

1. **I-space is append-only** — every byte persists forever, filed chronologically
2. **Historical backtrack** — any previous instant can be reconstructed
3. **Non-destruction** — "modifications never damage originals" [LM 2/45]

The document is not a thing that is overwritten; it is "an evolving ONGOING BRAID" [LM 2/14] whose entire trajectory through time is preserved. The guarantee is stated in terms of state reconstruction rather than operation logging, but the effect is the same: nothing is lost, and the full sequence of growth is recoverable.
