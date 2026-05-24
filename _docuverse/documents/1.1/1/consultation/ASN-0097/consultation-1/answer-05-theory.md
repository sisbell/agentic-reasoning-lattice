## Question 5 [theory]

> Was projection of zero-width spans and empty endsets designed as vacuously defined, undefined, or a vanishing operation?

Three different cases need separate answers - the question conflates phenomena I treated differently in my specification.

**Empty endsets — vanishing.** This was designed as a vanishing operation. From 4/43:

> "Links between bytes can survive deletions, insertions and rearrangements, if anything is left at each end." [LM 4/43]

The conditional "if anything is left" is the operative principle. When nothing remains at an end, the link does not survive in that version. The link object itself persists (it has a permanent tumbler address; it remains discoverable in Istream), but it has no semantic effect in the current arrangement.

**Zero-width spans — not designed.** I did not designate these as a first-class case. My specification consistently treats spans as having content:

> "In fact, a tumbler-span may range in possible size from one byte to the whole docuverse on the whole network." [LM 4/24]

> "A tumbler-span is not a conventional number, and it does not designate the number of bytes contained. It does not designate a number of anything." [LM 4/24]

The minimum is one byte, not zero. For link-to-link references, I specified "a span of 1 to designate that unit only" [LM 4/49] — again, the floor is 1.

A span where first equals last is degenerate in my model. I did not specify whether implementations should treat this as vacuously defined, as an error, or as collapse. This is genuinely underspecified.

**Projection across versions — vanishing.** For refractive link following, the behavior is conditional:

> "the user's front-end machine may easily be set up to follow the link to the same passage in the most recent version—if it's still there." [LM 2/43]

"If it's still there" — when correspondence cannot be established, the projection has no result. The link is not deleted; it simply produces nothing in the target version.

**The unifying principle.** Spans and endsets refer to content, not positions. When the content is absent, the reference has no semantic effect. This follows from my deeper commitment that links connect bytes, not positions:

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes." [LM 4/42]

If there are no bytes — empty endset, deleted target, or degenerate zero-width — there is no strap. Whether implementations call this "vacuously defined" or "vanishing" is terminology; the observable result is the same: the operation has no semantic effect, while the link object remains intact in Istream awaiting historical backtrack.

NEED_RAW: 4/47, 4/48, 4/56-4/60 — these pages on link search semantics and the AND-of-ORs satisfaction model may contain additional language about empty satisfaction sets that would tighten this answer, particularly for FINDLINKSFROMTOTHREE behavior when an endset becomes empty.
