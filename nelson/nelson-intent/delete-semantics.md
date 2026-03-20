# DELETE Semantics: Vstream Removal, Not Istream Destruction

Source: Literary Machines, 4/9 (page 176), 4/11 (page 178), 2/14-2/15 (pages 94-95), 2/45 (page 125)

## What "DELETE" Means in Xanadu

DELETE in Xanadu does NOT mean what it means in conventional systems. It removes content from a document's Vstream (current arrangement) but does NOT remove it from Istream (permanent storage).

Nelson explicitly distinguishes between:
- **Vstream deletion:** Content becomes "not currently addressable" in that document
- **Istream permanence:** Content remains in Istream forever

The diagram on 4/9 shows "DELETED BYTES" as a valid system state, with the annotation:
> "(not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)"

## User Guarantee

1. **Nothing is ever truly deleted from Xanadu**
   - Deleted bytes remain in Istream
   - Previous versions still contain the deleted content
   - Other documents that transclude the content still show it
   - Links to deleted content still resolve (to Istream)

2. **Historical backtrack is always possible**
   - Any previous arrangement can be reconstructed
   - "The user may go back in time to any previous version"

3. **Modifications never damage originals**
   - Deletion is a modification to Vstream arrangement
   - The Istream content is untouched
   - Other documents' views are unaffected

## What DELETE Affects

| Aspect | Affected by DELETE? |
|--------|---------------------|
| Vstream arrangement | YES - content removed from current view |
| Istream content | NO - bytes remain forever |
| Previous versions | NO - still contain the content |
| Transclusions | NO - other documents still show it |
| Links to content | NO - still resolve to Istream |
| Home document traceability | NO - I-address encodes origin |

## Principle Served

**Non-destruction:** The conventional notion of destructive editing is exactly what Xanadu exists to abolish.

> "Virtually all of computerdom is built around the inadequate convention of making whole copies of each current version... A document is really not just a block of text... it is an ongoing changing file... an evolving braid." (2/14)

> "This users may also republish documents out of old ones indefinitely, making whatever changes seem appropriate--without damaging the originals." (2/45)

## Distinction from Link Deletion

This file addresses **content deletion** (text). Link deletion is a separate administrative operation -- see [link-deletion.md](link-deletion.md).

## Nelson's Words

On deleted bytes state:
> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" (4/9)

On persistence in other documents:
> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." (4/11)

On append-only storage:
> "Instead, suppose we create an append-only storage system. User makes changes, the changes flow into the storage system, filed, as it were, chronologically." (2/14)

On time navigation:
> "The file management system we are talking about automatically keeps track of the changes and the pieces, so that when you ask for a given part of a given version at a given time, it comes to your screen." (2/15)
