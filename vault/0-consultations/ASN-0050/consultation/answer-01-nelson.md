## Question 1 [nelson]

> When content is removed from a document's arrangement, does the content itself continue to exist permanently in the system, or can removal ever cause content to cease to exist?

# Content Removal Never Destroys Content

The answer is unambiguous: **removal from a document's arrangement never causes content to cease to exist.** This is one of Xanadu's deepest architectural commitments.

## The Two Address Spaces

Xanadu separates *where content lives permanently* (I-space) from *how a document arranges content right now* (V-space). DELETE operates exclusively on V-space:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

The phrase "not currently addressable" is precise — the bytes are not gone, they are merely unreachable through the current document arrangement.

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

This confirms that deletion is local to one V-space arrangement. Every other document that transcludes the same I-space content is unaffected.

## Append-Only Storage

The storage model is explicitly append-only. Content accumulates; it is never overwritten or removed:

> "Virtually all of computerdom is built around the destructive replacement of successive whole copies of each current version." [LM 2/14]

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

Every byte ever stored has a permanent I-space address that will always return that exact content. This is not a backup mechanism bolted on after the fact — it is the fundamental nature of how storage works.

## Historical Backtrack Depends On It

The guarantee that you can reconstruct any previous state requires that nothing is ever truly destroyed:

> "The file management system we are talking about automatically keeps track of the changes and the pieces, so that when you ask for a given part of a given version at a given time, it comes to your screen." [LM 2/15]

If removal could destroy content, historical backtrack would be impossible. The two guarantees are structurally linked.

## Modifications Never Damage Originals

Nelson states this as a general principle applying to all editing operations:

> "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate — without damaging the originals. This is done by inclusion links." [LM 2/45]

And on derivative documents:

> "The integrity of each document is maintained by keeping the two aspects separate: derivative documents are permanently defined (and stored) in terms of the originals and the changes." [LM 2/37]

## What Deletion Affects vs. What It Does Not

| Aspect | Affected by DELETE? |
|--------|---------------------|
| V-space arrangement (current view) | **YES** — content removed from current arrangement |
| I-space content (permanent storage) | **NO** — bytes remain forever |
| Previous versions | **NO** — still contain the content |
| Transclusions in other documents | **NO** — still show the content |
| Links pointing to that content | **NO** — still resolve via I-space |
| Home document traceability | **NO** — I-address still encodes origin |

## Summary

In Xanadu, "delete" means "remove from this arrangement." It never means "destroy." The content persists in I-space, remains accessible through previous versions, continues to appear in any document that transcludes it, and can always be recovered through historical backtrack. This is by design — Nelson built the system specifically to abolish destructive replacement.
