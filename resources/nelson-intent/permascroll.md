# Permascroll: Append-Only Content Store

Source: Literary Machines 2/13-2/16, 4/10-4/11

## Terminology

**The term "permascroll" does NOT appear in Literary Machines.** Nelson calls this:
- The "hyperfile" (2/22)
- "Append-only storage system" (2/14)
- Content's "home location" (4/11)

## What It Means

The permascroll is global append-only storage where all content permanently resides. It is the physical manifestation of I-space.

- **Append-only**: Content is added, never overwritten or removed
- **Chronological**: Content is "filed, as it were, chronologically" (2/14)
- **Global**: Spans the entire docuverse
- **Permanent**: Every byte ever created has an eternal address here

The permascroll is NOT a document. Documents are views (V-space arrangements) that reference content stored here.

## User Guarantee

- Every byte you create gets a permanent I-address
- That I-address will always return that exact content
- Content is NEVER deleted from the permascroll
- Any previous state of any document can be reconstructed
- "The user may go back in time to any previous version" (2/15)

## Principle Served

Nelson rejects "destructive replacement" — the conventional model where saving overwrites the previous version. Instead:
- The permascroll stores content permanently (I-space)
- Documents arrange references to that content (V-space)
- "Editing" changes the arrangement, not the content
- "Deleting" removes content from the view, not from existence

## What "Deletion" Means

DELETE does NOT remove content from the permascroll. The V-space mapping is removed (content disappears from current view), but I-space content remains. Previous versions still show the content, and links to that I-address still resolve.

> "Safety and backtrack are not separate problems." (2/13)

## Nelson's Words

> "Virtually all of computerdom is built around the destructive replacement of successive whole copies of each current version." (2/14)

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." (2/14)

> "A document is really an evolving ONGOING BRAID." (2/14)

> "The true storage of text should be in a system that stores each change and fragment individually, assimilating each change as it arrives, but keeping the former changes; integrating them all by means of an indexing method that allows any previous instant to be reconstructed." (2/15)

> "The user of such a system may scroll through an individual document, at successive instants of time, alive in the space-time vortex." (2/15)

> "THE PART YOU WANT COMES WHEN YOU ASK FOR IT" (2/16)

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." (4/11)
