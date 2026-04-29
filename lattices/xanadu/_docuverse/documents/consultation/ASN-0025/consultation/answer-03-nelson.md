## Question 3 [nelson]

> If a user deletes a passage from their document, does the address that once referred to that passage become permanently unusable, or may it be reassigned?

## The Address Is Never Reassigned — But the Answer Depends on Which Address Space

Xanadu has two address spaces, and they behave differently on deletion.

### I-Space Address: Permanently Occupied, Never Reassigned

The I-space (invariant space) address of the deleted passage remains permanently valid and permanently refers to that exact content. The content is not destroyed — it enters the state Nelson labels:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

The bytes still exist at their I-space address. They can be retrieved through historical backtrack or through other documents that transclude them:

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

I-space is append-only. Nothing stored there is ever overwritten or reassigned:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

The I-space address of that passage will refer to that passage for the life of the docuverse. It cannot be given to new content.

### V-Space Address: Positional, Shifts on Editing

The V-space (virtual space) address is a different matter. V-addresses are positional — like array indices, not permanent identifiers. They form a dense, contiguous sequence:

> "The digit after the one indicates the byte position in the current ordering of bytes. This is its virtual stream address." [LM 4/30]

When you delete content, the gap closes. Nelson explicitly states that insertion shifts subsequent addresses:

> "The v-stream addresses of any following characters in the document are increased by the length of the inserted text." [LM 4/66]

Deletion is the inverse: subsequent V-addresses decrease to fill the gap. So the V-address number that once referred to your deleted passage now refers to whatever content follows the deletion point. But this is not "reassignment" — V-addresses were never permanent identifiers. They describe *where content sits right now*, not *what content is*.

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." [LM 4/11]

### Why This Works: Links Point to I-Space

The entire architecture depends on this separation. Links attach to I-space addresses (permanent content identity), not V-space addresses (ephemeral positions):

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." [LM 4/30]

So when a passage is deleted:
- Its **I-space address** remains permanently occupied — the content is still there, still linkable, still retrievable through historical backtrack or transclusion
- Its **V-space position** is reclaimed — subsequent content shifts to fill the gap
- **Links to the passage** still work — they point to I-space, which is unaffected

The principle is absolute: no I-space address is ever reused. The tumbler guarantee applies:

> "New items may be continually inserted in tumbler-space while the other addresses remain valid." [LM 4/19]

"Remain valid" means permanently. An I-space address, once baptized for a piece of content, belongs to that content forever.
