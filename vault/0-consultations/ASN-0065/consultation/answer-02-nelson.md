## Question 2 [nelson]

> If a link addresses a span of content that is split by a cut point during rearrangement, must the link continue to address exactly the same content bytes, even though they now occupy non-contiguous positions?

## Yes — absolutely and by design.

This is one of the most important architectural consequences of Xanadu's Istream/Vstream separation. A link addresses **bytes by their permanent I-addresses**, not by their current positions in the document's Vstream. When REARRANGE splits the span, the link continues to address exactly the same bytes. The endset simply becomes discontiguous in Vstream terms.

### Three interlocking guarantees make this work:

**1. Links attach to bytes, not positions.**

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes." [LM 4/42]

The "strap" metaphor is precise: the strap is tied to the bytes themselves. Move the bytes around and the strap follows.

**2. Rearrangement changes Vstream, not Istream.**

REARRANGE is a pure Vstream operation — it changes the *arrangement* of content in the document's virtual byte stream, but the underlying I-addresses of every byte remain permanent and unchanged. Since links point to I-addresses, the link is unaffected by the rearrangement.

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." [LM 4/11]

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." [LM 4/30]

**3. Discontiguous endsets are explicitly supported.**

Nelson anticipated exactly this scenario. The result of a rearrangement splitting a linked span is that the endset becomes a discontiguous set of bytes — and this is a first-class concept:

> "We see from above that one end of a link may be on a broken, discontiguous set of bytes. This illustrates the endset: a link may be to or from an arbitrary set of bytes. These may be anywhere in the docuverse." [LM 4/42]

### The survivability guarantee is explicit:

> "Links between bytes can survive deletions, insertions and rearrangements, if anything is left at each end." [LM 4/43]

Note that **rearrangements** are named specifically alongside deletions and insertions. And since rearrangement preserves all bytes (it moves them, doesn't remove them), "anything is left at each end" is trivially satisfied — the link survives with its full original byte set intact.

### What the user sees

After rearrangement, a front end resolving the link's endset would find the same bytes now occupying two non-adjacent regions of the Vstream. The front end could:

- Highlight both regions as the link's extent
- Present them as a single logical selection spanning a gap
- Allow navigation to "the next piece" of the linked content

The system doesn't need to "fix" or "update" the link after rearrangement. The link was always pointing to I-addresses, which never changed. Only the V-to-I mapping changed — and that's the document's concern, not the link's.
