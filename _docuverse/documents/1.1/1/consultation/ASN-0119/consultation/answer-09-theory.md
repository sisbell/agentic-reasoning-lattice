## Question 9 [theory]

> What must the design guarantee about the permanence of content that is displaced but otherwise structurally unchanged?

## The Guarantee: Displacement Changes Arrangement, Never Identity

When content is *displaced but otherwise structurally unchanged* — moved by an INSERT before it, a REARRANGE, or a DELETE elsewhere that shifts its position — the design must guarantee that **only the Vstream (virtual arrangement) changes, while the Istream (permanent content identity) is untouched**. The byte keeps its permanent I-address forever; only its V-address (its ordinal position in the current view) moves.

### Why this matters

Xanadu separates *where content lives* (Istream, permanent) from *where it appears now* (Vstream, ephemeral). Displacement is purely a Vstream event:

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." (4/11)

The permanent address itself is the bedrock guarantee:

> "New items may be continually inserted in tumbler-space while the other addresses remain valid. This means that any address of any document in an ever-growing network may be specified by a permanent tumbler address." (4/19)

### Three concrete obligations the design must keep

**1. The I-address persists through reordering.**

> "The digit after the one indicates the byte position in the current ordering of bytes. This is its virtual stream address... Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." (4/30)

**2. Links attached to displaced content survive.** Because links bind to bytes (via I-addresses), not to positions, displacement cannot break them:

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes. This has a crucial advantage: it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them." (4/42)

The visual annotation on 4/43 is explicit that rearrangement is covered:

> "SURVIVABILITY: Links between bytes can survive deletions, insertions and rearrangements, **if anything is left at each end.**" (4/43)

**3. Correspondence and transclusion are preserved.** Since correspondence and inclusion both derive from shared I-origin — not from position — displaced content remains correctly matched across versions and still resolves for every document that windows it. INSERT shifts following V-addresses but leaves I-addresses (and thus all these relationships) intact:

> "The v-stream addresses of any following characters in the document are increased by the length of the inserted text." (4/66)

### Summary

The design must guarantee that displacement is **non-destructive and identity-preserving**: the content's permanent Istream address is unchanged, its history remains reconstructable, and every link, transclusion, and correspondence anchored to it stays attached. Moving content where it sits in the V-stream must never alter what it *is* or sever what points to it.
