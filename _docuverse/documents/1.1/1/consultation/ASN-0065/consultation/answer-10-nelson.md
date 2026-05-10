## Question 10 [nelson]

> After rearrangement, if a reader follows a link into the rearranged document, must they arrive at the same content they would have reached before the rearrangement, regardless of its new position within the document?

## Yes — the reader arrives at the same content, regardless of its new position.

This is one of Xanadu's most fundamental architectural guarantees, and it follows directly from the two-address-space design.

### Why rearrangement cannot affect link targets

Links attach to **Istream addresses** (permanent content identity), not to **Vstream addresses** (current positions). REARRANGE is a pure Vstream operation — it changes where bytes appear in the document's current arrangement, but the bytes themselves remain at their permanent Istream addresses. Since links point to Istream, they are completely unaffected.

Nelson states this explicitly:

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." [LM 4/30]

And more broadly:

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes. This has a crucial advantage: it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them." [LM 4/42]

> "Links between bytes can survive deletions, insertions and rearrangements, if anything is left at each end." [LM 4/43]

### The mechanism

The Vstream position of a byte — its location in the document as currently arranged — is explicitly described as irrelevant to the link system:

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." [LM 4/11]

So when a reader follows a link into a rearranged document:

1. The link resolves to the same Istream bytes it always pointed to
2. The system locates those bytes in the document's current Vstream arrangement
3. The reader sees the same content, now at its new position

The reader arrives at the **same words**, even though those words may now be on a different "page" of the document. The link followed the content, not the position.

### The strap metaphor

Nelson's visualization captures this perfectly: a link is a "strap between bytes." If you rearrange the bytes (move paragraphs around), the strap stays attached to the same bytes and stretches to wherever they now sit. The strap doesn't care about position — it cares about identity.
