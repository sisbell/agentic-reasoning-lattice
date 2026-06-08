## Question 6 [theory]

> What permanence guarantee applies to a position once content is inserted there — can a position that has been assigned ever be reused, reassigned, or made to point to different content?

## Permanence of an Assigned Position

The answer depends critically on **which address space** the "position" refers to — and Nelson's two-space model gives opposite answers for each.

### Istream position (Identity Space): permanent, never reused

When content is inserted, it is written to permanent storage and receives an **Istream address** — its identity. This address is immutable: it is never reused, never reassigned, and never made to point to different content.

The foundational tumbler guarantee establishes this:

> "New items may be continually inserted in tumbler-space while the other addresses remain valid. This means that any address of any document in an ever-growing network may be specified by a permanent tumbler address." (4/19)

Insertion of new content never disturbs existing addresses — new items *fork* new addresses rather than overwriting or renumbering old ones:

> "New items may be continually inserted in tumbler-space while the other addresses remain valid." (4/19)

And the content at an I-address is fixed forever. Even "deletion" does not free the address for reuse — the bytes remain in Istream, merely unaddressable in the current view:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" (4/9)

This permanence is precisely what makes links, citations, and transclusions survive editing — they point at Istream addresses that cannot be repurposed:

> "A Xanadu link is not between points, but between spans of data... This has a crucial advantage: it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them." (4/42)

### Vstream position (the position in the current arrangement): ephemeral, *does* get reassigned

If "position" instead means the **Vstream position** — the byte's place in the document as it currently reads — then the opposite holds. V-addresses are not permanent; the *same V-position* points to different content as the document is edited:

> "The v-stream addresses of any following characters in the document are increased by the length of the inserted text." (4/66)

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." (4/11)

So Vstream position 5 may hold one byte today and a different byte after an INSERT or DELETE. The V-address is a slot in a current arrangement, not an identity.

### Summary

| Sense of "position" | Reusable / reassignable? | Can point to different content? |
|---|---|---|
| **Istream address** (where content lives, its identity) | Never | Never — content is immutable |
| **Vstream position** (place in current arrangement) | Yes — edits shift it | Yes — same V-position, different bytes |

The permanence guarantee Nelson promises attaches to **identity (Istream)**, not to arrangement (Vstream). Once content is inserted and given its Istream address, that address is permanent and inviolable; the visible *position* in the document is deliberately fluid so that editing remains possible without destroying the permanent record beneath it. This separation of permanent identity from mutable arrangement is the core of the design.
