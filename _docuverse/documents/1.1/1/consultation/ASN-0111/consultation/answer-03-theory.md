## Question 3 [theory]

> Must the type a link carries be permanent, or may a link's recorded type change across versions?

## The type a link carries is permanent — to express a different type, you make a different link

A link in my design is an immutable triple of endsets, fixed at the moment of creation. Its type is the third endset (the "three-set"):

> "A link's type is specified by yet another end-set, pointing anywhere in the docuverse. This is symmetrical with the other endsets." [LM 4/44]

Three features of the architecture together make the recorded type permanent:

**1. There is no operation to re-type a link.** A link is created by MAKELINK, which fixes all three endsets and "returns the id of the link made." The FEBE command set has operations to *make* a link, to *find* links, to *retrieve* endsets, and to *delete* a link — but no operation to mutate an existing link's endsets. The content-editing operations (INSERT, DELETEVSPAN, REARRANGE, APPEND, COPY) act on bytes, not on a link's structure. So nothing in the protocol can change a link's type in place. To carry a different type, you delete the old link and make a new one — which is a *different* link.

**2. The type is matched by address, and addresses are permanent.** A type is not stored content that could be edited into something else; it is an address that the search mechanism matches:

> "What the 'type' designation points to is completely arbitrary. This is because of the way we will be searching for links. The search mechanism does not actually look at what is stored under the 'type' it is searching for; it merely considers the type's address." [LM 4/44-4/45]

Even if whatever sits at the type's address is later edited, the type designation does not change — the link still names the same address. The type can even be a ghost element with nothing stored there. The type's *meaning* lives in its address, and addresses do not move.

**3. Links keep their identity permanently.** Links occupy a document's `2.x` subspace in permanent order of arrival:

> "The links designated by a tumbler address are in their permanent order of arrival. A document includes only the links of which it is the home document." [LM 4/31]

A given link's address is stable; deleting one does not renumber the others. The link is one object with one fixed type.

## Across versions

Because a link binds spans (not positions), one link reaches through all versions of a Prismatic Document rather than being re-made per version:

> "Links may be refractively followed from a point or span in one version to corresponding places in any other version. Thus a link to one version of a Prismatic Document is a link to all versions." [LM 2/26]

So a single link presents the *same* type wherever it is followed — there is no per-version "recorded type" that could drift. A later version's author who wants a different type does not re-type the existing link; they author a new link (a new object, at their own home address, in their own order of arrival), and the original link with its original type remains intact. This is consistent with the non-destruction guarantee: modifications never damage the originals.

## Caveat on scope

The curated sources establish the three load-bearing facts above (type is an endset fixed at MAKELINK, matched by permanent address, on a link with a permanent order-of-arrival identity) and contain no operation that edits a link's endsets. The conclusion — "a link's type is immutable; a re-typed link is a different link" — follows from that architecture rather than from a single sentence stating it outright. If you want an explicit statement that the link-editing command set is exhaustive (i.e., that no re-type operation was ever contemplated), that would live in the protocol pages: NEED_RAW: 4/61-4/70.
