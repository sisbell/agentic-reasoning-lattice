## Question 5 [theory]

> What must happen to a link that spans across both moved regions, or from a moved region into stationary content, after the transposition?

## Short answer

Nothing needs to be done to the link — it survives the transposition automatically. What changes is only its *appearance* in the document's current ordering: a link end that was a single contiguous span before the rearrange may become **discontiguous** (a span-set) afterward, because the bytes it holds onto have moved to new virtual positions.

## Why

REARRANGE is a pure Vstream (arrangement) operation. It transposes regions of the current ordering but does not touch the permanent Istream content:

> "Rearrange transposes two regions of text. With three cuts, the two regions are from cut 1 to cut 2, and from cut 2 to cut 3... With four cuts, the regions are from cut 1 to cut 2, and from cut 3 to cut 4." (4/67)

Because links attach to *bytes* (their permanent I-addresses), not to positions, they ride along with the content wherever it lands:

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." (4/30)

This is the core survivability guarantee, which explicitly names rearrangement:

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes. This has a crucial advantage: it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them." (4/42)

> "SURVIVABILITY: Links between bytes can survive deletions, insertions and rearrangements, **if anything is left at each end.**" (4/43)

## The specific scenarios

- **A link spanning both moved regions:** before the transpose its end was one contiguous range; after the transpose the two regions are no longer adjacent in the Vstream, so that end is now expressed as **two separate spans** (a discontiguous span-set). The link still connects exactly the same bytes.

- **A link from a moved region into stationary content:** the end anchored in the moved region travels to the region's new position; the stationary end stays put. The connection is unchanged.

This discontiguous outcome is exactly what endsets are built to allow:

> "We see from above that one end of a link may be on a broken, discontiguous set of bytes. This illustrates the endset: a link may be to or from an arbitrary set of bytes." (4/42)

So the operative principle: the link "must" do nothing except continue holding its bytes. The system re-expresses the affected endset as a span-set in the new ordering; the link's identity, ownership, and connection are preserved. The only way a transposition could destroy a link is if it left *nothing* at one end — which a rearrange, being non-destructive, never does.
