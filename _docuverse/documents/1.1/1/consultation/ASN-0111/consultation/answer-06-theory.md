## Question 6 [theory]

> Must a link's identity remain stable even as the documents it connects are edited or re-versioned?

# Yes — a link's identity must remain stable across editing and re-versioning

This follows from two distinct but related guarantees in Nelson's design: **link identity** (the link as an addressed object) and **link survivability** (the link's connection to content). Both are designed to persist.

## 1. A link has its own permanent address, fixed in order of arrival

A Xanadu link is a first-class object in tumbler-space with its own permanent address, distinct from the content it connects. Critically, these addresses are assigned in creation order and **never renumbered**:

> "The links designated by a tumbler address are in their permanent order of arrival. A document includes only the links of which it is the home document." (4/31)

Concretely, the link concept notes that link `2.1` is always the first link created in that document and `2.755` is always the 755th — deleting an intermediate link does not renumber the others. The link's identity is therefore stable by construction: editing content cannot shift a link's own address.

Ownership is likewise tied to the home document, not to what the link points at:

> "A link need not point anywhere in its home document. Its home document indicates who owns it, and not what it points to." (4/12)

So even if the documents on *either end* are edited, the link's identity (its home address and ownership) is unaffected.

## 2. The link's connection survives editing because it binds bytes, not positions

Identity stability would be hollow if edits silently broke the link's endpoints. Nelson's span-based ("strap between bytes") model prevents this:

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes. This has a crucial advantage: it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them. This also works for alternative versions in which part of each end has survived." (4/42)

The diagram annotation on 4/43 states it directly:

> "Links between bytes can survive deletions, insertions and rearrangements, if anything is left at each end."

Because endsets point to **Istream** (permanent) addresses rather than **Vstream** positions, editing the arrangement of a document leaves the link's targets intact.

## 3. Re-versioning: links "refractively follow" to corresponding parts

For re-versioning specifically, the link does not merely survive — it reaches through into other versions via correspondence:

> "Links may be refractively followed from a point or span in one version to corresponding places in any other version. Thus a link to one version of a Prismatic Document is a link to all versions." (2/26)

This is why published documents cannot be casually withdrawn: others' links depend on continued accessibility, and a superseding version lets old links "reach through":

> "However, for corrections and amendments, the author may readily publish a superseding document, but the former version must remain on the network. This is vital because of the links other users may have made to it—which can now reach through from the previous version (to which they were originally attached) into the newer version." (2/43)

## Summary

| Aspect | Guarantee | Source |
|--------|-----------|--------|
| Link's own address | Permanent, in order of arrival, never renumbered | 4/31 |
| Link ownership | Fixed by home document, independent of targets | 4/12 |
| Connection through edits | Survives if any byte remains at each end | 4/42–4/43 |
| Connection through versions | Refractively follows to corresponding parts | 2/26, 2/43 |

A link's identity is **invariant** by design. The link is a permanently-addressed, owned object whose identity is decoupled from the volatile content it connects — and whose connection is engineered to survive the very editing and re-versioning the question asks about.
