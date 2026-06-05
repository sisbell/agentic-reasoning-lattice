## Question 3 [theory]

> If content, documents, or links are created or changed between one window request and the next, what must remain stable about the order of links the reader has already seen?

## The invariant: links keep their permanent order of arrival

What must remain stable is the **creation-order numbering of links**. Each link's address is fixed at the moment it is created, and that ordinal position never changes — no matter what content, documents, or links are added, edited, or deleted afterward.

Nelson states this directly:

> "The links designated by a tumbler address are in their permanent order of arrival. A document includes only the links of which it is the home document." (4/31)

The addressing scheme makes this concrete. A link's address ends in its sequential instance number within the document:

> "N.0.U.0.D.V.0.2.1 (the first link of the document, stored in the document's space)" (4/31)
>
> "N.0.U.0.D.V.0.2.755 (the 755th link to which the document is home)" (4/31)

So link `2.1` is *always* the first link created, and `2.755` is *always* the 755th — these are stable identities, not positions in a shifting list.

## Why this matters between window requests

Two consequences flow from "permanent order of arrival":

1. **New links append; they never reorder.** A link created after the reader's last request is added at the next free ordinal (e.g., `2.756`). It cannot displace or renumber `2.1` through `2.755` that the reader has already seen.

2. **Deletion does not renumber.** As the curated `links` source notes, deleting link `2.5` does not renumber `2.6` through `2.N`. The deleted link enters the "not currently addressable" state (see `link-deletion.md`), but the surviving links keep their original addresses.

This contrasts with **bytes**, which can be rearranged in Vstream — their virtual positions shift on every edit. Links are the exception: they are not rearrangeable and hold their arrival-order addresses permanently.

The result is a stable frame of reference for the reader: a link they encountered on one request will carry the same address on the next, so any reference they retained still resolves to the same connection.
