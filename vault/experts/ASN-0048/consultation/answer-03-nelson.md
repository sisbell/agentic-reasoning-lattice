## Question 3 [nelson]

> Does the previous arrangement of the document — the content and its ordering before the addition — remain permanently retrievable as a prior version?

# Yes — Absolutely and By Design

The permanent retrievability of every prior arrangement is not merely a feature of Xanadu; it is the **foundational storage paradigm**. The entire system is built around the rejection of destructive replacement.

## The Core Guarantee

> "The file management system we are talking about automatically keeps track of the changes and the pieces, so that when you ask for a given part of a given version at a given time, it comes to your screen." [LM 2/15]

> "THE PART YOU WANT COMES WHEN YOU ASK FOR IT." [LM 2/16]

Every prior arrangement — every version, every historical state — remains permanently accessible. You can request "a certain part of a certain version at a certain point in time" and the system reconstructs it.

## Why This Works: I-Space vs V-Space

The mechanism is the separation of **content** (I-space) from **arrangement** (V-space):

- **I-Space** stores content permanently. Bytes at an I-address never change.
- **V-Space** is the document's current arrangement — a mapping from sequential positions to I-space addresses.

When you add content to a document, the new bytes are appended to I-space (getting permanent addresses), and the V-space mapping is updated to include them. But the **previous V-space mapping** — the prior arrangement — is preserved as a version.

> "A document is really an evolving ONGOING BRAID." [LM 2/14]

> "Think of the process of making editorial changes as re-twisting this braid when its parts are rearranged, added or subtracted... and think then of successive versions of the document, at successive instants of time, as alive in this space-time vortex." [LM 2/15]

## Append-Only Storage Makes It Inevitable

Nelson explicitly rejects conventional storage:

> "Virtually all of computerdom is built around the destructive replacement of successive whole copies of each current version." [LM 2/14]

His alternative:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

In an append-only system, nothing is overwritten. Every change is accumulated. The prior state is not "saved" as a separate copy — it simply *persists* because the system never destroys anything. Reconstruction of any prior arrangement is a matter of replaying the appropriate mappings.

## No "Basic" Version — All Are Equal

There is no privileged "current" version that supersedes others:

> "There is thus no 'basic' version of a document set apart from other versions—'alternative' versions—any more than one arrangement of the same materials is a priori better than other arrangements." [LM 2/19]

Nelson calls this **prismatic storage**:

> "We call this system of storage Prismatic because we may think of a given part, or section, as being prismatically refracted when we pass from one version to another. We believe our Prismatic storage can support virtually instantaneous retrieval of any portion of any version (historical or alternative)." [LM 2/19]

## Even "Deletion" Preserves Prior State

The delete operation removes content from the current V-space arrangement only. The I-space content remains:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

## The User Experience

Nelson envisions users navigating through time as naturally as through space:

> "The user of such a system may scroll through an individual document, at successive instants of time, alive in the space-time vortex." [LM 2/15]

> "The user must also be able to find his or her notes, look back through time, and study its previous states." [LM 2/15]

The FEBE protocol provides explicit operations for this. `SHOWRELATIONOF2VERSIONS` returns corresponding span pairs between any two versions [LM 4/70], and `RETRIEVEV` can retrieve content from any specific version [LM 4/67].

## Summary

The previous arrangement is **always** permanently retrievable. This is not a convenience feature — it is a structural consequence of append-only I-space storage combined with versioned V-space mappings. The system was designed from the ground up so that no edit, insertion, deletion, or rearrangement can ever destroy a prior state. Nelson called the complete system a **hyperfile** [LM 2/22] — a storage structure that supports not just content but its full version history and the ability to navigate through time.
