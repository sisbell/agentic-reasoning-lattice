# Storage

Source: Literary Machines, 2/13-2/22 (pages 93-102)

## Semantic Intent

### What It Means

Xanadu's storage system fundamentally rejects "destructive replacement" - the conventional approach where saving overwrites the previous version. Instead, it uses **append-only storage** where every change is accumulated, never destroying previous states.

A document is not a file that gets overwritten. It is an **evolving structure** - Nelson calls it "an ongoing braid" - where edits are woven in while all previous states remain accessible. The storage system treats a document as a thing that grows through time, not a thing that changes in place.

This is not just version control bolted onto storage. The storage paradigm itself is designed around preservation and reconstruction.

### User Guarantee

**Safety:** You can always go back. Nothing you write is ever lost.

**Historical Backtrack:** You can reconstruct any previous state of your document - not from periodic snapshots, but from the actual sequence of changes.

**Part-Pounce:** When you request a piece of a document, you get it instantly, constructed on demand from fragments, even if the "whole document" doesn't exist as a single stored unit. Nelson: "THE PART YOU WANT COMES WHEN YOU ASK FOR IT."

### Principle Served

**The true structure of text is evolving.** Nelson argues that conventional storage imposes a false model - treating documents as static things that occasionally get replaced wholesale. But writing is actually "an evolving, Protean structure" where pieces are constantly rearranged, added, and reconsidered. The storage system should reflect this reality.

**Safety and backtrack are not separate problems.** Conventional systems treat backup (copying everything) and version history as separate from the storage mechanism. Nelson sees them as unified: if storage itself preserves history, both safety and backtrack emerge naturally.

### How Users Experience It

- Edit freely, knowing nothing is destroyed
- Go back in time to any previous state
- Request any part of any version, constructed on demand
- Scroll through space (the document) or time (its history)
- See successive versions "alive in the space-time vortex"
- Compare what's the same and what's different between versions

### Nelson's Words

On conventional storage vs Xanadu:
> "Virtually all of computerdom is built around the destructive replacement of successive whole copies of each current version." (2/14)

On the true nature of documents:
> "A document is really an evolving ONGOING BRAID." (2/14)

On the storage approach:
> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." (2/14)

On editing as braiding:
> "Think of the process of making editorial changes as re-twisting this braid when its parts are rearranged, added or subtracted." (2/15)

On part-pounce:
> "We call this pounce. You pounce like a cat on a given thing, and it seems to be there, having been constructed while you wait, as it were, in midair." (2/16)

On scrolling through time:
> "The user of such a system may scroll through an individual document, at successive instants of time, alive in the space-time vortex." (2/15)

On time and space viewing:
> "The user may thus refer not merely to the present version of the document; he or she may go back in time to any previous version. The user must also be able to find his or her notes, look back through time, and study its previous states." (2/15)

On what this system is:
> "Let us call such a storage system a hyperfile." (2/22)

### Related Concepts

- **Versions** - The user-facing manifestation of this storage approach
- **I-Space/V-Space** - The address space separation that enables this model
- **Docuverse** - The global space where all this content lives
