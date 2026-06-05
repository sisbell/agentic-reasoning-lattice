## Question 2 [theory]

> What guarantee governs whether the endsets a read returns are the original endpoints recorded at the link's creation, or the endpoints as they exist in the current versions?

## Answer

The governing guarantee is **link survivability**, which rests on the fact that endsets attach to **Istream byte-spans (permanent identity), not Vstream positions**. Because of this, the endpoints recorded at creation and the endpoints a read returns are the *same thing* — the Istream addresses never change.

### Why endsets are invariant

A Xanadu link does not record positions; it records spans of permanent content:

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes.
>
> This has a crucial advantage: it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them." (4/42)

The survivability annotation on 4/43 confirms the spans persist through edits:

> "SURVIVABILITY: Links between bytes can survive deletions, insertions and rearrangements, **if anything is left at each end.**" (4/43)

Endsets map to permanent Istream content (`design-intent/three-endset-links.md`, `design-intent/link-survivability.md`). Since "Content at an Istream address never changes" and V-positions "may be constantly changing" (4/11), the *recorded* endpoints are Istream addresses that are immutable by the permanence guarantee. There is therefore no divergence between "original endpoints" and "endpoints in the current version" at the level of what is stored and returned — they are identical.

### The "current version" dimension is a separate mechanism

The idea of endpoints "as they exist in current versions" is not a property of the stored endset but of **refractive following / correspondence**, a navigation behavior layered on top:

> "Links may be refractively followed from a point or span in one version to corresponding places in any other version. Thus a link to one version of a Prismatic Document is a link to all versions." (2/26)

Mapping a recorded endset to a current version's positions is governed by the **correspondence relation** (shared Istream origin), and is what `SHOWRELATIONOF2VERSIONS` exposes — "a list of ordered pairs of the spans of the two spec-sets that correspond" (4/70). Translating to current-version positions is a front-end choice (the front end "may easily be set up to follow the link to the same passage in the most recent version", 2/43), not something RETRIEVEENDSETS does on its own.

### Caveat on the specific operation

For `RETRIEVEENDSETS`, the curated sources give only: "This returns a list of all link end-sets that are in `<spec set>`" (4/70). The sources establish that endsets *are* Istream-based span-sets, but they do **not** explicitly state the address-space representation (raw Istream addresses vs. resolved Vstream positions) that this one command returns in its reply.

NEED_RAW: 4/70 (page-237) — to confirm whether RETRIEVEENDSETS's documented return value specifies I-stream vs V-stream representation of the endsets.

**Summary:** Link survivability (endsets bound to immutable Istream bytes) guarantees that a read returns the original recorded endpoints — they cannot drift, because Istream addresses are permanent. Obtaining "the endpoints as they exist in current versions" instead requires the separate correspondence/refractive-following mechanism, not RETRIEVEENDSETS itself.
