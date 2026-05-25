## Question 4 [theory]

> What guarantee does the design make about the permanence of content that has been removed from a document but exists in an ancestor arrangement?

# The Guarantee: Content Removal Is Vstream-Only, Never Istream-Destruction

Xanadu makes a strong, specific guarantee about content that has been "deleted" from a document but exists in an ancestor arrangement: **the content is never destroyed.** Removal is a Vstream operation (changing the current arrangement), not an Istream operation (destroying bytes). The content remains permanently in the ancestor version and remains addressable via historical backtrack.

## The Core Guarantee

Nelson explicitly distinguishes "deleted" from "destroyed." Deleted bytes occupy a recognized state in the system architecture:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

The phrase "awaiting historical backtrack functions" is the key. Deletion makes content *not currently addressable in this version*, but the content persists, ready to be retrieved when the user asks for an older version.

## What Removal Affects (and Doesn't)

Nelson's guarantee is precise about what changes and what doesn't:

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

So when you remove content from your current document:

| Aspect | Affected by removal? |
|--------|---------------------|
| Vstream arrangement (current view) | YES — content disappears from this version |
| Istream content (permanent storage) | NO — bytes remain forever |
| Ancestor versions | NO — they still contain the content |
| Other documents transcluding it | NO — they still show it |
| Links pointing to the content | NO — still resolve to Istream |

## The Append-Only Foundation

This guarantee rests on Xanadu's append-only storage model — a deliberate rejection of conventional "destructive replacement":

> "Virtually all of computerdom is built around the inadequate convention of making whole copies of each current version ... A document is really not just a block of text ... it is an ongoing changing file ... an evolving braid." [LM 2/14]

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

Because storage is append-only, removing content from a current arrangement does not — *cannot* — remove it from the system.

## Historical Backtrack: The User-Facing Promise

The user-facing manifestation of this guarantee is **historical backtrack**: the ability to ask for any previous state and receive it.

> "The file management system we are talking about automatically keeps track of the changes and the pieces, so that when you ask for a given part of a given version at a given time, it comes to your screen." [LM 2/15]

> "THE PART YOU WANT COMES WHEN YOU ASK FOR IT." [LM 2/16]

Nelson frames this as a fundamental need of creative work, not a backup feature:

> "Under many circumstances the writer, or 'text user', needs to reach back to a former condition. This is in the nature of creative work." [LM 2/14]

## No Privileged "Basic" Version

Importantly, the ancestor arrangement is not treated as a backup or historical artifact — it is an equal citizen with the current version. Nelson is explicit:

> "There is thus no 'basic' version of a document set apart from other versions—'alternative' versions—any more than one arrangement of the same materials is a priori better than other arrangements." [LM 2/19]

This means removed content in an ancestor isn't "old" or "stale" — it's just part of a different valid arrangement of the same prismatic document.

## Modifications Never Damage Originals

Nelson generalizes this principle beyond a single document's history: any modification — whether your own edit or someone else's derivative work — preserves what came before.

> "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate--without damaging the originals. This is done by inclusion links." [LM 2/45]

> "This means a whole new pluralistic publishing form. If anything which is already published can be included in anything newly published, any new viewpoint can be freely presented by an easily-made annotated collage. (The old viewpoint is still present too—you can always say, 'Show me what this originally was.')" [LM 2/45]

## Summary

The guarantee can be stated as a conservation law: **content that has ever been part of any version of a document remains permanently retrievable through the ancestor version it lived in.** Removal is non-destructive by architectural necessity, not by policy. The Vstream forgets; the Istream remembers. Anyone can always say "show me what this was originally" — and the system must answer.
