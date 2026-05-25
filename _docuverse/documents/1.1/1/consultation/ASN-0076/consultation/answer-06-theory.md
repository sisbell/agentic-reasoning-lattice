## Question 6 [theory]

> Can multiple users independently "edit" the same original link, producing divergent successor links, and what must the system guarantee about each branch?

# Multiple Users "Editing" the Same Link: Divergent Branches

## The Direct Answer

Multiple users cannot directly edit the same link. Links are owned, and ownership is structural. What appears to be "divergent successor links" arises from **document forking** (versioning), not from link editing per se.

## Why Direct Co-Editing Is Forbidden

A link is owned by whoever owns its home document:

> "A link need not point anywhere in its home document. Its home document indicates who owns it, and not what it points to." [LM 4/12]

> "A Xanadu link is a connective unit, a package of connecting or marking information. It is owned by a user." [LM 4/41]

And only owners may modify:

> "Only the owner has a right to withdraw a document or change it." [LM 2/29]

So User B cannot reach into User A's document and alter a link there. Nelson provides no FEBE operation for direct link mutation — MAKELINK creates, link deletion removes (entering the "not currently addressable" state per LM 4/9), but there is no MODIFYLINK. To "edit" a link semantically, the owner must delete and recreate.

## How Divergence Actually Happens

Three mechanisms produce branch-like structures:

**1. Forking via CREATENEWVERSION.** User B can fork User A's document:

> "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate--without damaging the originals. This is done by inclusion links." [LM 2/45]

In the fork, B owns the new document and can delete/recreate links in their branch. A's original link remains untouched in A's document.

**2. Independent parallel linking.** User B creates their own link in their own document, pointing to the same endsets with a different type or different from/to spans. This is not a "successor" — it is an independent assertion.

**3. Link-to-link annotation.** User B creates a link pointing AT User A's link (commentary on the link itself), since links have tumbler addresses and are themselves addressable.

## What the System Must Guarantee Per Branch

For each independently-owned branch:

**Ownership integrity.** The link's home address determines who controls it. No other user can modify or delete it.

**Permanent addressability.** Each link gets a permanent address in its home document:

> "The links designated by a tumbler address are in their permanent order of arrival. A document includes only the links of which it is the home document." [LM 4/31]

Branch L1 at `N.0.U_a.0.D.V.0.2.5` is forever distinct from forked-branch L1' at a different tumbler address under U_b's account.

**Survivability of each branch's link independently.** Editing in branch A does not affect branch B's link:

> "Links between bytes can survive deletions, insertions and rearrangements, if anything is left at each end." [LM 4/43]

**Refractive correspondence across branches.** A link made in one version can be followed to corresponding positions in another:

> "Links may be refractively followed from a point or span in one version to corresponding places in any other version. Thus a link to one version of a Prismatic Document is a link to all versions." [LM 2/26]

**Non-destruction of the original.** The original link persists forever in the original document, even after the owner "deletes" it:

> "DELETED LINKS (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

**Discoverability of all branches.** Any user can find all links pointing into or out of any span across the docuverse — the divergent branches are all visible to anyone searching the endsets, with home addresses revealing their independent owners.

## A Caveat

NEED_RAW: 4/29-4/31, 4/52, 4/65-4/68 — Nelson does not use the phrase "successor link" anywhere I can find in the curated sources. The closest formal mechanisms are CREATENEWVERSION (for documents containing links), the Supersession Link type (which declares "this replaces that" between *documents*, not directly between links), and the Alternative-Version Link type. Whether links have their own first-class supersession semantics independent of document supersession is not explicitly addressed in the curated extractions, and would need verification against pages 4/29-4/31 (link addressing within documents) and 4/52-4/53 (metalinks and supersession).

## Summary

In my design, "editing the same link" is not an operation. Divergence comes from the version system applied to *documents* that *contain* links. Each branch's links are independently owned, independently addressed, independently mutable by their respective owners, and permanently preserved. The original link never disappears — it sits in its home document at its permanent tumbler address, with all forks visible as separate threads in the literature.
