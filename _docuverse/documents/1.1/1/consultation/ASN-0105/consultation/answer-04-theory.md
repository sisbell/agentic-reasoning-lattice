## Question 4 [theory]

> Must the returned content show the document's content as it is currently arranged, or as it was originally composed before any rearrangement?

## Answer

Retrieval returns content **as it is currently arranged** (the Vstream / current ordering), not as it was originally composed. The original arrangement is not lost — but it is a *different version*, reached only by explicitly asking for it through historical backtrack.

### Why current arrangement is the default

Xanadu separates two address spaces: **Istream** (permanent, immutable content storage) and **Vstream** (the document's current arrangement of that content). Retrieval operations work in Vstream terms.

The retrieval command operates on virtual-stream addresses, which reflect the *current* ordering:

> "Logical addressing of the byte stream is in the form of virtual spans, or vspans. These are sequences of bytes in the document's virtual byte stream, regardless of their native origin." (4/11)

> "The digit after the one indicates the byte position in the current ordering of bytes. This is its virtual stream address." (4/30)

And critically, that ordering changes as the document is edited:

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." (4/30)

So when you `RETRIEVEV` — "This returns the material (text and links) determined by <spec set>." (4/67) — you get bytes in their *present* Vstream arrangement. REARRANGE changes that arrangement (it "transposes two regions of text," 4/67), and subsequent retrieval reflects the new order.

### The original arrangement survives as a version

Rearrangement does not destroy the prior ordering — the content is permanent in Istream, and the prior arrangement is preserved as an earlier version reachable on request:

> "The file management system we are talking about automatically keeps track of the changes and the pieces, so that when you ask for a given part of a given version at a given time, it comes to your screen." (2/15)

> "The user may thus refer not merely to the present version of the document; he or she may go back in time to any previous version." (2/15)

Nelson is explicit that no arrangement is privileged as "the" canonical one:

> "There is thus no 'basic' version of a document set apart from other versions—'alternative' versions—any more than one arrangement of the same materials is a priori better than other arrangements." (2/19)

### Summary

- **Default retrieval** → current arrangement (Vstream as it stands now).
- **Original composition** → still fully recoverable, but as a distinct prior version via historical backtrack, by specifying "a given part of a given version at a given time."

The current arrangement is what comes back unless you deliberately request an earlier one; the original is never the implicit default, but it is never lost either.
