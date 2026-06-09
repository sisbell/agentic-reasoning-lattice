## Question 1 [theory]

> When a new link is created, what identity must the system allocate to it, and must that identity be permanent and never reused even after the link's home document changes?

## What identity must be allocated

When MAKELINK is invoked, the system must allocate the link a **permanent tumbler address** in the link subspace of its home document, and return that address as the link's id.

> "This creates a link in document <doc id> from <from set> to <to set> connected to <three set>. It returns the id of the link made." (4/68, from `operations`)

The address falls in the document-local `0.2.N` subspace, assigned by creation order:

```
N.0.U.0.D.V.0.2.1     → first link in document
N.0.U.0.D.V.0.2.755   → 755th link in document
```

> "N.0.U.0.D.V.0.2.1 (the first link of the document, stored in the document's space)" (4/31, from `links`)
> "N.0.U.0.D.V.0.2.755 (the 755th link to which the document is home)" (4/31, from `links`)

## Must it be permanent and never reused

Yes. Link addresses are assigned in **permanent order of arrival** and are never renumbered:

> "The links designated by a tumbler address are in their permanent order of arrival. A document includes only the links of which it is the home document." (4/31, from `links`)

Per the `links` curated source: "Link `2.1` is always the first link created in that document... Deleting link `2.5` doesn't renumber `2.6` through `2.N`." This holds even when a link is deleted — deletion makes it "not currently addressable, awaiting historical backtrack functions" (4/9, from `link-deletion`), but the address itself is never recycled. This is the general tumbler guarantee:

> "New items may be continually inserted in tumbler-space while the other addresses remain valid." (4/19, from `tumblers`)

## On "after the link's home document changes"

I want to flag the premise here: in Nelson's model, **a link's home document does not change** — the home is built into the link's identity, not a mutable attribute. The home document fields (`N.0.U.0.D`) are the leftmost part of the link's own tumbler address, and the home is what determines where the link physically resides and who owns it:

> "The document must be specified because that determines the actual residence of the link--since a document may contain a link between two other documents." (4/63, from `operations`)

> "A link need not point anywhere in its home document. Its home document indicates who owns it, and not what it points to." (4/12, from `documents`)

So the link's permanent identity is inseparable from its home. There is no operation in the curated sources that reassigns a link's home document; the question's hypothetical of an identity surviving a "home document change" does not arise, because the home document is a fixed component of the identity rather than something that can change underneath it.

NEED_RAW: 4/30-4/31 — to confirm whether Nelson anywhere contemplates reassigning a link's home or its sequential link-number subspace beyond what the curated `links` excerpt covers.
