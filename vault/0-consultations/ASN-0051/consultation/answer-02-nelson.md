## Question 2 [nelson]

> If a linked passage is deleted from a document, what must the system guarantee about the link itself — does it persist, become invalid, or enter some other state?

## Link Persistence After Content Deletion

The system guarantees that the link **persists**. This follows from two architectural properties working together: links attach to Istream (permanent) addresses, and deletion only affects Vstream (current arrangement).

### Links Attach to Bytes, Not Positions

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes. This has a crucial advantage: it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them." [LM 4/42]

The "strap between bytes" metaphor is key. The link grips the bytes themselves — identified by their permanent Istream addresses — not the positions those bytes happen to occupy in a document's current arrangement.

### Deletion Does Not Destroy Bytes

DELETE in Xanadu removes content from Vstream only. The Istream content is untouched:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

The bytes enter a state Nelson describes as "not currently addressable" — they vanish from the document's current view but remain permanently in Istream storage. They also survive in previous versions and in any other documents that transclude them.

### Therefore the Link Survives

Since the link's endset points to Istream addresses, and those addresses are permanent, the link retains valid targets even after Vstream deletion. The survivability guarantee from [LM 4/43] states:

> "SURVIVABILITY: Links between bytes can survive deletions, insertions and rearrangements, **if anything is left at each end.**"

Because Istream is append-only and bytes are never destroyed, "something is left at each end" is always structurally true. The deleted bytes still exist — they are merely removed from the current arrangement.

### What the Reader Experiences

Nelson explicitly addresses the case where a document is updated and a reader follows an old link:

> "When a document is updated, a reader will ordinarily want to see the new version — but the reader may be following a link made to an older version. However, the user's front-end machine may easily be set up to follow the link to the same passage in the most recent version — if it's still there." [LM 2/43]

That final clause — "if it's still there" — acknowledges the case where the linked passage has been deleted from the current version. The link itself remains valid; the front end must decide how to present it. Options include:

1. Show the content in the **previous version** where it still exists (historical backtrack)
2. Show the content at its **Istream home** (permanent address)
3. Show it in **other documents** that transclude it
4. Indicate that the passage was removed from the current version but remains accessible

### Summary

| Aspect | State After Deletion |
|--------|---------------------|
| **The link itself** | Persists — it is a first-class object at its own address |
| **The link's endset targets** | Still valid — point to permanent Istream addresses |
| **The bytes in Istream** | Unchanged — append-only, never destroyed |
| **The bytes in Vstream** | Removed from current version's arrangement |
| **Previous versions** | Still contain the passage |
| **Other transclusions** | Unaffected — still show the content |

The link neither becomes invalid nor enters a degraded state. It continues to function exactly as before, because its targets — Istream bytes — are permanent. What changes is only the current document's Vstream arrangement, which is the one thing the link does *not* depend on.
