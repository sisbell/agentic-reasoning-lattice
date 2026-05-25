## Question 9 [theory]

> How does the design distinguish between a link that has been "edited" and a wholly new link that happens to share endpoints with an existing one?

# How the Design Distinguishes Edited Links from New Links with Shared Endpoints

The distinction is **architectural, not heuristic**: a link's identity is its tumbler address, not its endpoints. Two links pointing at identical content are simply two distinct links — the way two photographs of the same scene are two distinct photographs.

## Each Link Has a Permanent Address

Every link in a document is assigned a unique tumbler address in strict order of arrival. As I wrote in 4/31:

> "The links designated by a tumbler address are in their permanent order of arrival. A document includes only the links of which it is the home document." [LM 4/31]

The addressing scheme is:

- `N.0.U.0.D.V.0.2.1` — the first link of the document
- `N.0.U.0.D.V.0.2.755` — the 755th link to which the document is home

Unlike bytes, links are **not rearrangeable**. Once link `2.5` is created, that slot is its forever. Even if it's deleted, `2.6` doesn't get renumbered. Deleted links enter a "not currently addressable" state, but the address itself is not reused:

> "DELETED LINKS (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

## There Is No "Edit Link" Operation

In XU.87.1, the FEBE protocol provides MAKELINK, the FIND family (FINDLINKSFROMTOTHREE, FINDNUMOFLINKSFROMTOTHREE, FINDNEXTNLINKSFROMTOTHREE), and RETRIEVEENDSETS. There is no operation to modify a link's endsets. Once a link is made, its three endsets are fixed.

This means "editing a link" in the conventional sense does not occur. What can happen:

1. **Content beneath the link is edited.** The link's endsets reference bytes via permanent I-addresses, so insertions, deletions, and rearrangements don't change the link's identity. The link survives unchanged:

   > "Links between bytes can survive deletions, insertions and rearrangements, if anything is left at each end." [LM 4/43]

2. **The owner deletes a link and creates a new one.** The new link gets the next sequential address. The deleted link keeps its original address in the deleted state.

3. **A user creates a new link whose endsets happen to match an existing one.** That new link receives its own address — independent of the original.

## The Practical Consequence

A wholly new link with shared endpoints is simply a different object at a different address, owned (potentially) by a different user, in a different home document. The system never asks "is this the same link as that one?" by comparing endsets — it answers identity questions purely by address.

This follows from Nelson's broader stance that links are first-class objects in the docuverse, not properties of their endpoints. As I noted in 4/41:

> "A Xanadu link is a connective unit, a package of connecting or marking information. It is owned by a user." [LM 4/41]

Two users could legitimately make identical-looking citation links to the same passage; both are valid, both are searchable, and both remain in their respective owners' home documents at their own addresses.

NEED_RAW: The curated sources cover link addressing, FEBE operations, deletion semantics, and survivability — but do not explicitly answer whether endset modification was ever contemplated as a future operation. Pages 4/61-4/79 (FEBE protocol detail) and 4/41-4/60 (link mechanics) would be worth checking if a definitive negative claim is required.
