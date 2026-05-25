## Question 2 [theory]

> What is the identity relationship between an original link and its edited successor — are they considered the same link or distinct links sharing a lineage?

# Link Identity Under Edits

**Short answer: In Nelson's design, links are immutable once created. There is no concept of "editing" a link in Literary Machines — what survives editing is the link itself, not modifications to it.**

## What Nelson explicitly establishes

**Links have permanent identity through tumbler addresses.** From 4/31:

> "The links designated by a tumbler address are in their permanent order of arrival. A document includes only the links of which it is the home document."

A link created as `N.0.U.0.D.V.0.2.755` is permanently the 755th link of that document. Deleting an earlier link doesn't renumber later ones.

**What "survives editing" means is content-side, not link-side.** The crucial passage at 4/42:

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes. This has a crucial advantage: it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them."

The link is *the same link*, unchanged. What was edited was the content at its endsets, not the link itself.

**No operation modifies a link.** Among Nelson's 17 FEBE commands, `MAKELINK` creates; there is no `EDITLINK` or `MODIFYLINK`. To change a connection, the owner deletes (link enters "not currently addressable, awaiting historical backtrack functions" state per 4/9) and creates a fresh one — which gets the next sequential address and is a distinct link.

## Two distinct scenarios to keep separate

| Scenario | Identity result |
|---|---|
| Bytes at link's endsets are edited (insert/delete/rearrange) | **Same link.** The link "remains on" surviving bytes (4/42–4/43). |
| Owner wants a different connection | **Distinct links.** Delete the old (preserved in Istream); MAKELINK a new one at next position. No formal lineage. |

## Lineage between distinct links

Nelson specifies supersession and counterpart links for **documents/versions** (4/52–4/53), not explicitly for links-as-targets. But since links have tumbler addresses and any tumbler address can be linked to (the link-to-link mechanism, 4/49–4/51), a user could in principle create a supersession-style link pointing from one link's address to another's. This would be a user-asserted claim, not a system-tracked lineage.

## What's not in the curated sources

NEED_RAW: 4/52–4/53 (full metalinks/supersession discussion to confirm whether supersession applies only to documents/versions or also to individual links), 4/65–4/69 (full FEBE command list to confirm no link-modification operation exists).
