## Question 2 [nelson]

> When new content is inserted into a document, must the addresses of all previously existing content in that document remain unchanged?

## Answer: It Depends on Which Address Space

Xanadu has **two address spaces**, and the answer is different for each.

### I-Space Addresses: YES — Always Unchanged

Every byte's permanent identity address (its I-space tumbler) is immutable. Insertion, deletion, rearrangement — nothing changes an I-space address. This is the foundational guarantee:

> "New items may be continually inserted in tumbler-space while the other addresses remain valid. This means that any address of any document in an ever-growing network may be specified by a permanent tumbler address." [LM 4/19]

The I-space address encodes where the byte was *born* (server, account, document, element position). That never changes regardless of what happens in any document that references it.

### V-Space Addresses: NO — They Explicitly Shift

V-space addresses (positions in the document's virtual byte stream) change on every edit. Nelson specifies this directly in the INSERT operation:

> "This inserts \<text set\> in document \<doc id\> at \<doc vsa\>. The v-stream addresses of any following characters in the document are increased by the length of the inserted text." [LM 4/66]

And from the V-space description:

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." [LM 4/11]

V-addresses are dense and contiguous (1, 2, 3, ...). When you insert 10 bytes at position 5, everything after position 5 shifts by 10. This is by design — V-space is a *view*, not an identity.

### Why This Works: Links Point to I-Space

The architectural reason for the separation is link survivability:

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." [LM 4/30]

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes. This has a crucial advantage: it means that links can survive editing." [LM 4/42]

Links attach to bytes via their permanent I-space identity, not their ephemeral V-space position. So insertion shifts V-addresses but leaves all links intact.

### Summary

| Address type | Changes on INSERT? | Why? |
|---|---|---|
| **I-space** (permanent identity) | No — immutable forever | Content identity is permanent |
| **V-space** (document position) | Yes — shifts after insertion point | V-space is a mutable view |
| **Tumbler** (docuverse-wide) | No — valid forever | The whole point of tumblers |

The genius of the design is that users work with V-space (intuitive sequential positions) while the system preserves I-space (permanent identity). V-space is disposable; I-space is eternal.
