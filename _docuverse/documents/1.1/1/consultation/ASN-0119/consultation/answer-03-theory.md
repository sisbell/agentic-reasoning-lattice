## Question 3 [theory]

> What must the design guarantee about the content lying between the two moved regions that was itself part of neither?

I don't have file-read access in this session, so I'm answering from the verified curated sources (quotes with page numbers are confirmed against the originals).

## The guarantee for the in-between content

REARRANGE works on four cuts: "the regions are from cut 1 to cut 2, and from cut 3 to cut 4" (4/67). The span lying between cut 2 and cut 3 belongs to neither moved region, yet transposing the two regions necessarily shifts that intervening content's position in the document's virtual stream.

The design must guarantee that this untouched middle content is **preserved in identity and connectivity even though its virtual position changes** — it must not be destroyed, re-created, re-identified, or have its links broken merely because it was displaced as a side-effect.

This follows from three verified guarantees:

**1. REARRANGE is a pure Vstream operation.** It rearranges the *arrangement*, not the content. The intervening bytes keep their permanent Istream (identity) addresses; only their V-positions move. Nelson's general statement on this:

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." (4/11)

**2. Links to the in-between content survive.** Because links attach to bytes (via their permanent addresses), not to positions, any link touching the displaced middle remains attached:

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." (4/30)

> "SURVIVABILITY: Links between bytes can survive deletions, insertions and rearrangements, **if anything is left at each end.**" (4/43)

The phrase "and rearrangements" is the explicit case: a rearrangement must not break the connectivity of content it shifts, including content that was never itself part of either moved region.

**3. The result stays in canonical order.** Nelson's enfilade mandate requires that after any edit the file remains well-ordered:

> "All changes, once made, left the file remaining in canonical order, which was an internal mandate of the system." (1/34)

So the displaced middle must come to rest in a consistent, addressable position — not in some corrupt or ambiguous state.

## In short

The content between the two moved regions must be guaranteed to **retain its permanent content identity (Istream addresses), keep all attached links stably connected, and remain addressable and in canonical order** — its virtual position may shift as a consequence of the transposition, but nothing about its existence, identity, or connectivity may be lost.

---

NEED_RAW: 4/67 (raw page 234) — the curated REARRANGE text defines the four cuts but does not spell out, in Nelson's own words, what happens to the cut-2-to-cut-3 span. If you want a *verbatim* Nelson statement that the in-between content is explicitly addressed (rather than this conclusion derived from the survivability and Vstream/Istream guarantees), that page should be read directly.
