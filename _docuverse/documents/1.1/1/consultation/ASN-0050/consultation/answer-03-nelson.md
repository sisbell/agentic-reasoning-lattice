## Question 3 [nelson]

> Must every prior version of a document — including versions that contained the now-removed content — remain permanently retrievable?

# Yes — Every Prior Version Must Remain Permanently Retrievable

This is one of Xanadu's firmest guarantees, established through multiple interlocking design commitments.

## The Direct Statement

Nelson states the guarantee explicitly:

> "The file management system we are talking about automatically keeps track of the changes and the pieces, so that when you ask for a given part of a given version at a given time, it comes to your screen." [LM 2/15]

> "The user of such a system may scroll through an individual document, at successive instants of time, alive in the space-time vortex." [LM 2/15]

The user can request **any part** of **any version** at **any point in time**, and the system must deliver it.

## Why This Is Architecturally Inevitable

The guarantee is not a policy choice bolted onto the system — it falls out structurally from the I-space/V-space separation.

**I-space is append-only.** Content, once stored, lives at its I-address forever:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

**A version IS a V-space arrangement.** Each version is nothing more than a mapping from V-addresses to I-addresses. Since I-space content is permanent, any prior mapping can be reconstructed. There is no way to make a version "unretrievable" without destroying I-space content — which the architecture forbids.

**Deletion is V-space only.** When content is removed from a document, it disappears from the current arrangement but remains in I-space:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

The phrase "awaiting historical backtrack functions" is telling — the deleted bytes are preserved *specifically so that* prior versions containing them can be reconstructed.

## The Published-Version Obligation

For published documents, the requirement is even stronger. Prior versions must remain not merely reconstructible but actively available, because other users' links depend on them:

> "It is in the common interest that a thing once published stay published, as in the world of paper. Other readers and users will come to depend on its accessibility. Consequently its author may not withdraw it except by lengthy due process." [LM 2/43]

> "However, for corrections and amendments, the author may readily publish a superseding document, but the former version must remain on the network. This is vital because of the links other users may have made to it — which can now reach through from the previous version (to which they were originally attached) into the newer version." [LM 2/43]

The logic chain: others link to version N → you publish version N+1 → version N **must remain** → because links to it are other users' property and cannot be broken by your editorial decisions.

## No "Basic" Version

Nelson explicitly rejects the idea that any version is privileged over others:

> "There is thus no 'basic' version of a document set apart from other versions — 'alternative' versions — any more than one arrangement of the same materials is a priori better than other arrangements." [LM 2/19]

All versions have equal standing. The current version is simply the most recent V-space arrangement; it does not supersede prior versions in terms of existence or retrievability.

## The Braid Metaphor

Nelson's central metaphor reinforces this:

> "A document is really an evolving ONGOING BRAID." [LM 2/14]

> "Think of the process of making editorial changes as re-twisting this braid when its parts are rearranged, added or subtracted... and think then of successive versions of the document, at successive instants of time, as alive in this space-time vortex." [LM 2/15]

A braid does not destroy its earlier strands when new ones are added. The entire history is structural — you can examine any cross-section at any point in time.

## One Qualification: Implementation Status

Nelson acknowledges that XU.87.1 did not fully implement historical backtrack:

> "Being able to go back through changes, and perhaps restore an earlier state, is called the problem of historical backtrack. For simple, linear textual documents this can be done by storing lists of changes and undoing them; and indeed several commercial versioning and backtrack systems are now on the market. But it is rather more difficult to do this for hypertext." [LM 3/13]

The 4/9 annotation — "awaiting historical backtrack functions" — confirms that full version reconstruction was designed-for but not yet built in 87.1. The *architecture* preserves everything needed (append-only I-space, V-space mappings); the *implementation* of reconstruction was still in progress.

## Summary

Every prior version must remain permanently retrievable. This follows from:

1. **Append-only I-space** — content is never destroyed [LM 2/14]
2. **Versions are V-space arrangements** — reconstructible from permanent I-space [LM 4/10-4/11]
3. **Deletion is V-space only** — deleted bytes await historical backtrack [LM 4/9]
4. **Published versions cannot be withdrawn** — others' links depend on them [LM 2/43]
5. **No version is privileged** — all arrangements have equal standing [LM 2/19]
6. **The user guarantee is explicit** — "a given part of a given version at a given time" [LM 2/15]
