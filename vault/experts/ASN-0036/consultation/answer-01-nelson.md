## Question 1 [nelson]

> Must every piece of content that has ever been stored remain retrievable even after it no longer appears in any document's current arrangement?

## Yes — with important nuance about mechanism and economics.

Nelson's design requires that content stored in I-space remains retrievable even after removal from every document's current V-space arrangement. This follows from three reinforcing commitments: append-only storage, historical backtrack, and link survivability.

---

### The Append-Only Architecture

The storage model is explicitly non-destructive:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

> "The true storage of text should be in a system that stores each change and fragment individually, assimilating each change as it arrives, but keeping the former changes." [LM 2/15]

Content enters I-space once and stays. No operation removes it. DELETE is a V-space operation only — it changes the current arrangement, not the permanent store.

### DELETE Does Not Destroy

Nelson is explicit about what deletion means. His technical diagram on page 4/9 labels a specific category:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

And further:

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

"Not currently addressable" means absent from the current V-stream — not absent from the system. The bytes are described as "awaiting historical backtrack functions," which presupposes they remain in storage for that purpose.

### Historical Backtrack Requires It

The version history guarantee is meaningless without I-space persistence:

> "The file management system we are talking about automatically keeps track of the changes and the pieces, so that when you ask for a given part of a given version at a given time, it comes to your screen." [LM 2/15]

If the system can reconstruct "a given part of a given version at a given time," the underlying bytes must still exist. You cannot reconstruct a historical state from content that has been destroyed.

### Link Survivability Requires It

Links attach to I-space addresses, not V-space positions:

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes. This has a crucial advantage: it means that links can survive editing." [LM 4/42]

If content vanished from I-space once removed from all current V-streams, links to that content would silently break — violating the survivability guarantee. The "strap between bytes" metaphor only works if the bytes persist.

### The Economic Tension

There is one significant caveat. Nelson's funding model requires ongoing storage rental:

> "ALL SERVICES MUST BE SELF-SUPPORTING. Subsidy between one aspect of the system and another could only work temporarily. This means, for example, that archival storage must be economically self-sustaining." [LM 4/5]

Nelson does **not** specify what happens when storage rental lapses. The curated storage-funding source explicitly notes this gap: Nelson does not address whether there is a grace period, whether the Author's Fund can preserve orphaned content, or how payment obligations interact with the permanence guarantee over centuries.

The technical architecture says "never destroy." The economic architecture says "someone must pay." Nelson leaves the collision unresolved.

### Summary

| Question | Answer | Basis |
|----------|--------|-------|
| Does the architecture permit destroying I-space content? | **No** — append-only by design | [LM 2/14] |
| Can deleted content be retrieved? | **Yes** — through historical backtrack | [LM 2/15, 4/9] |
| Do links to such content still resolve? | **Yes** — links point to I-space | [LM 4/42] |
| Is perpetual storage economically guaranteed? | **Unspecified** — requires ongoing payment | [LM 4/5] |

The design intent is unambiguous: I-space content persists regardless of its presence in any current V-space arrangement. Whether the economic model can sustain this guarantee indefinitely is a question Nelson acknowledged but did not resolve.
