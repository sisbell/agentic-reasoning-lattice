## Question 8 [theory]

> What identity must the returned end-specification carry — is it permanently tied to the same link and the same position, regardless of when it is requested?

## Short Answer

The returned end-specification carries a **permanent identity at the Istream (content) level, anchored to a link whose address is itself permanent** — but "the same position" needs to be split into two senses. The *identity* of the link and the *bytes* its endsets reach are permanent and survive editing; the *virtual position* (Vstream offset) of those bytes can shift over time. So the endset is permanently tied to the same link and the same content (Istream), but not necessarily to the same V-position.

## Why the link identity is permanent

A link's address is fixed at creation and never reused or reordered:

> "The links designated by a tumbler address are in their permanent order of arrival. A document includes only the links of which it is the home document." (4/31)

Deleting an earlier link does not renumber later ones — link `2.755` is always the 755th link created. The endsets returned belong to a link that has a stable, permanent home address.

## Why the endset content identity is permanent

Endsets attach to *bytes*, not to positions, and bytes carry permanent Istream addresses. This is the survivability guarantee:

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes. This has a crucial advantage: it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them." (4/42)

> "SURVIVABILITY: Links between bytes can survive deletions, insertions and rearrangements, if anything is left at each end." (4/43)

Because endsets map to the Istream-anchored tumbler line, the same content is designated regardless of when you ask:

> "There is a universal address space, the tumbler line... We may visualize a link's endsets as mapping to it." (4/45)

## The caveat about "the same position"

If "position" means the *virtual* (Vstream) location, that is explicitly *not* invariant — editing reshuffles V-positions while the underlying byte identity (and thus the link's attachment) stays fixed:

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." (4/30)

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." (4/11)

So: same link, same bytes — yes, permanently and time-invariantly. Same *V-position* — no, that can change as the document is edited.

The operation that returns these is RETRIEVEENDSETS:

> "This returns a list of all link end-sets that are in <spec set>." (4/70)

## One gap to flag

The curated sources confirm the *identity* guarantees above, but they do **not** explicitly state which address space `RETRIEVEENDSETS` reports its returned endsets in (raw Istream addresses vs. resolved Vstream positions at request time). That distinction matters for the precise wording of "the same position."

NEED_RAW: 4/70 (full RETRIEVEENDSETS definition), 4/58–4/60 (endset return representation in the link-search/retrieval commands)
