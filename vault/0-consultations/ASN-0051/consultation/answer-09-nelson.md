## Question 9 [nelson]

> When new content is inserted at the exact boundary of a linked passage, must the system have a definite rule about whether the link expands to include the insertion or excludes it?

# Boundary Insertion and Link Endsets

The question answers itself once you understand what links actually attach to.

## Links Attach to Bytes, Not Positions

A link's endset is a set of I-address spans — permanent addresses in the Istream where specific bytes live forever:

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes." [LM 4/42]

The "strap" seizes specific bytes by their permanent identity. It does not seize a region of the document's current arrangement.

## New Content Gets New I-Addresses

When you INSERT, the new bytes are appended to the Istream and receive fresh, never-before-used I-addresses:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

The INSERT operation changes the Vstream arrangement — "The v-stream addresses of any following characters in the document are increased by the length of the inserted text" [LM 4/66] — but creates entirely new Istream content. The linked bytes have not moved, changed, or been touched in any way.

## Therefore: No Ambiguity Exists

The link's endset still references exactly the same I-addresses it always did. The newly inserted bytes have *different* I-addresses. The link does not "know about" the insertion, and there is no mechanism by which it would expand.

This is not an edge case requiring a special rule. It is the natural consequence of the Istream/Vstream separation:

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." [LM 4/11]

V-addresses shift. I-addresses don't. Links point to I-addresses. New content has new I-addresses. The link excludes the insertion — always, automatically, with no rule needed.

## The Strap Metaphor Is Exact

Think of it physically. You strap a set of beads together. Someone slides new beads onto the string next to your strapped group. Your strap hasn't changed — it still holds the same beads. The new beads are *adjacent* in the arrangement but *outside* the strap.

This is precisely the "strap between bytes" model. Survivability means the strap stays on whatever bytes remain:

> "Links between bytes can survive deletions, insertions and rearrangements, if anything is left at each end." [LM 4/43]

Note: survive *insertions*. The link survives because it is unaffected. Insertion creates new bytes elsewhere in Istream; the linked bytes are untouched.

## If You Want the Link to Cover New Content

You would need to explicitly modify the link's endset to include the new I-addresses — or create a new link. The system does not silently expand endsets. That would violate the permanence of I-addresses and the definiteness of endsets.

## Summary

No boundary rule is needed because the architecture makes the answer structural. Links reference I-address spans. Insertions create new I-addresses. The two sets are disjoint by construction. The link excludes the insertion — not by convention, but by the geometry of the address space.
