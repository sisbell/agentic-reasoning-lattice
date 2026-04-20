## Question 1 [nelson]

> Once content is assigned an address in the system, can any operation — editing, deletion, or reorganization — ever cause that address to refer to different content?

# No operation can cause an I-space address to refer to different content. V-space addresses routinely shift.

The answer depends entirely on which of Xanadu's two address spaces you mean.

## I-Space: Absolutely Not

An I-space address is permanent and immutable. No operation — not editing, not deletion, not reorganization — can ever cause an I-space address to refer to different content than it originally identified.

> "Content at an I-space address **never changes**."

The I-space guarantee from Nelson's design:

- Every byte gets a permanent I-space address at creation
- That address will always return that exact content
- Content is immutable after creation

This is enforced by the append-only storage model:

> "Virtually all of computerdom is built around the destructive replacement of successive whole copies of each current version." [LM 2/14]

Nelson explicitly rejects this. Instead:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

Even **deletion** does not affect I-space:

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

Deleted bytes enter a state described as:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

"Not currently addressable" refers to the V-space view — the bytes are gone from the current arrangement. But they remain in I-space, permanently, at the same address.

## V-Space: Yes, Routinely

V-space addresses shift with every edit. This is by design — they represent the document's **current arrangement**, not content identity.

> "The v-stream addresses of any following characters in the document are increased by the length of the inserted text." [LM 4/66]

After an INSERT at position 3 in a document, what was at V-address 5 is now at V-address 6. The V-address 5 now refers to different content. Nelson acknowledges this explicitly:

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." [LM 4/11]

And:

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." [LM 4/30]

## Why This Matters: Links Point to I-Space

The entire architecture depends on this distinction. Links attach to I-space addresses (content identity), not V-space positions (current arrangement). This is why links survive editing:

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes. This has a crucial advantage: it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them." [LM 4/42]

## Tumbler Addresses: Never Reused

At the tumbler level, the forking mechanism ensures addresses are only ever created, never reassigned:

> "New items may be continually inserted in tumbler-space while the other addresses remain valid. This means that any address of any document in an ever-growing network may be specified by a permanent tumbler address." [LM 4/19]

New addresses are created by subdivision (forking digits to the right). No existing address is ever repurposed. The address space grows monotonically.

## Summary

| Address Space | Can refer to different content? | Mechanism |
|---|---|---|
| **I-Space** | Never | Append-only, immutable |
| **V-Space** | Yes, after any edit | INSERT shifts, DELETE closes gaps |
| **Tumbler (structural)** | Never | Forking only creates, never reuses |

The invariant is: **an I-space address is a permanent name for specific content**. The separation of I-space (identity) from V-space (arrangement) is the architectural foundation that makes permanent addressing, link survivability, version comparison, and origin traceability all possible simultaneously.
