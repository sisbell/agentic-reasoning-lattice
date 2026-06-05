## Question 6 [theory]

> Must the endsets returned by a read identify content by stable identity, so the same link read at different times names the same content?

## Yes — by design, endsets name content by stable identity, not by transient position

This is foundational to Xanadu, not an incidental property. The entire survivability guarantee depends on it. A link's endsets attach to *bytes* (Istream identity), not to *positions* (Vstream arrangement), so the same link read at different times names the same content even though that content's position in any document may have shifted.

### The mechanism

Nelson is explicit that links bind to byte identity, and that this identity is stable across editing:

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes. This has a crucial advantage: it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them." (4/42)

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." (4/30)

The "bytes themselves" are addressed in Istream, the invariant space. Vstream positions are the thing that changes:

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." (4/11)

So endsets cannot be founded on Vstream positions — those are ephemeral. They are founded on the permanent identity of the content. As the curated `endsets` material states the relationship to `i-space-v-space`: "Endsets point to Istream (enables survivability)."

### Why this answers the question directly

If endsets named content by Vstream position, then editing between two reads would silently re-point the link at whatever content now occupies that position — exactly the failure mode Nelson designed against. Instead:

- **Same bytes, even after deletion:** "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" (4/9) — the Istream content the endset names persists.
- **Same bytes, across versions:** "Links may be refractively followed from a point or span in one version to corresponding places in any other version." (2/26) — the endset's identity is what allows correspondence to be computed.

`RETRIEVEENDSETS` "returns a list of all link end-sets that are in <spec set>" (4/70). What it returns is grounded in the stable byte identity the link was created against.

### One distinction worth being precise about

The *content identity* an endset names is stable — that is guaranteed. What may differ between two reads is the *Vstream position* at which those same bytes currently appear (because of intervening edits), since "this order may be continually altered by editorial operations" (4/30). But the bytes named are the same bytes. The invariant is content identity (Istream), and the link "remain[s] stably attached to them."

So: yes — the same link read at different times names the same content. That is precisely what Istream-based endsets buy you, and it is the reason links survive editing at all.

NEED_RAW: 4/70 (to confirm whether the FEBE wire representation of returned endsets is literally expressed in I-addresses or in current V-addresses that resolve to the same bytes — the content-identity guarantee holds either way, but the exact returned address form is not pinned down in the curated sources).
