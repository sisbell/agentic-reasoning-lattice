## Question 1 [theory]

> Is a link a single permanent identity shared across all versions of the document it is homed in, or does the design intend the version structure to refract/fork a distinct link per version?

**Short answer: a link is a single permanent identity. The version structure does *not* mint a distinct link per version — it *refracts* the one link across versions. And in my vocabulary, refraction is precisely the thing that makes per‑version forking unnecessary.**

People hear "refract" and picture "fork." I meant the opposite. The whole reason I called the storage *Prismatic* is that one thing is seen at corresponding angles in each version — not copied into each.

## Why the link is one identity, not one-per-version

**1. A link grips bytes, not a version-snapshot.** A link is a strap between bytes in the permanent content space. It is not anchored to a position or to a particular version's arrangement, so it does not need re-creating when the arrangement changes:

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes. This has a crucial advantage: it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them. **This also works for alternative versions in which part of each end has survived.**" (4/42)

> "SURVIVABILITY: Links between bytes can survive deletions, insertions and rearrangements, if anything is left at each end." (4/43)

The same strap survives *across versions* — there is no second strap.

**2. Refraction is "one part, seen across versions" — that is the prismatic principle.**

> "We call this system of storage Prismatic because we may think of a given part, or section, as being prismatically refracted when we pass from one version to another." (2/19)

**3. I said it explicitly for links: one link, all versions.**

> "Links may be refractively followed from a point or span in one version to corresponding places in any other version. **Thus a link to one version of a Prismatic Document is a link to all versions.**" (2/26)

**4. A link "reaches through" from the version it was born against — it is not duplicated into the new one.**

> "...the links other users may have made to it—which can now reach through from the previous version (to which they were originally attached) into the newer version." (2/43)

Note the phrasing: the link stays *attached where it was made* and *reaches through*. That is single‑identity-plus-refraction, not fork.

**5. A link has one permanent home and a fixed order of arrival.**

> "The links designated by a tumbler address are in their permanent order of arrival. A document includes only the links of which it is the home document." (4/31)

A link's home determines *ownership*, and a version is only an "accidental extension of the document number" (4/29) — so re-homing the same link into every descendant version would multiply owners of one logical connection, which is not the intent:

> "A link need not point anywhere in its home document. Its home document indicates who owns it, and not what it points to." (4/12)

## On the version field in the link address

The link address carries the version:

> "N.0.U.0.D.V.0.2.1 (the first link of the document, stored in the document's space)" (4/31)
> "N.0.U.0.D.V.0.2.755 (the 755th link to which the document is home)" (4/31)

Read that `V` as the link's **birth/home version** — the single coordinate where the object lives — *not* as evidence that the same link is re-instantiated at `...D.1...`, `...D.2...`, `...D.3...`. Combined with "permanent order of arrival" (and links being non-rearrangeable), the design treats the link as one object at one home coordinate, reaching the rest of the version family by refraction.

## Two senses of "refraction" — both point to one identity

- **Endset/target side** (what the link points *at*): a link aimed into one version reaches the corresponding place in all versions (2/26, 2/43). Not forked.
- **Home side** (where the link *lives* and who owns it): a single permanent home, fixed by order of arrival (4/31, 4/12). Not forked.

Both reinforce the same conclusion: **one link, refracted; never a distinct link per version.**

---

**One caveat on a finer mechanic.** The curated material settles the *identity* question above, but it does not contain a verbatim statement of exactly how a *new* version's link subspace is initialized at `CREATENEWVERSION` (empty, vs. inherited-by-reference) — that detail isn't load-bearing for the single-vs-fork answer, but if you want it pinned down precisely:

NEED_RAW: 4/30–4/31 (link addressing across versions), 4/65–4/66 (CREATENEWVERSION semantics)
