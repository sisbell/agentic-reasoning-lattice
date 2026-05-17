## Question 8 [theory]

> Does the ghost-element doctrine (LM 4/23) treat ghost tumblers as "allocated" in any sense — i.e., does the design distinguish ghost addresses from merely-structurally-valid tumblers that have never been issued by any allocator?

The doctrine treats ghost elements as **conceptually allocated**, but does not sharply distinguish them from merely-structurally-valid tumblers. The distinction is implicit in Nelson's language rather than explicit.

**Ghost elements as allocated positions.** The 4/23 passages frame ghost elements as having undergone conceptual designation:

> "The docuverse is the occupied tumbler-space--as occupied by conceptually assigned positions, even if nothing represents them in storage." (4/23)

> "While servers, accounts and documents logically occupy positions on the developing tumbler line, no specific element need be stored in tumbler-space to correspond to them. Hence we may call them ghost elements." (4/23)

"Conceptually assigned" and "logically occupy" imply some prior act of designation. This pairs with the **baptism principle** from 4/17:

> "Whoever owns a specific node, account, document or version may in turn designate (respectively) new nodes, accounts, documents and versions, by forking their integers. We often call this the 'baptism' of new numbers."

So a ghost document is plausibly a baptized-but-unmaterialized address — owned via the forking chain, just lacking a stored object.

**The implicit asymmetry: occupied vs. unoccupied tumbler-space.** By defining the docuverse as *occupied* tumbler-space, Nelson implies a residual category of structurally-valid-but-unoccupied positions. But this residual category is never named or theorized in the curated material.

**The link-type case complicates the picture.** Link-type endsets weaken any "must be allocated" reading:

> "What the 'type' designation points to is completely arbitrary. This is because of the way we will be searching for links. The search mechanism does not actually look at what is stored under the 'type' it is searching for; it merely considers the type's address." (4/44-4/45)

> "Indeed, there is no need for the presence of elements at the addresses specified. Link types may be ghost elements." (4/45)

If a type address can be "completely arbitrary" and still function (because search matches on address, not content), then types appear to be able to point at unbaptized positions — i.e., merely-structurally-valid tumblers — and still work. Nelson calls these "ghost elements" too, but the conceptual situation is different from a baptized-but-unrepresented document.

**Summary.** The doctrine collapses two cases under one name:
- **Baptized ghosts**: servers/accounts/documents allocated through the forking-ownership chain but lacking stored representation. These "logically occupy" the docuverse.
- **Arbitrary-address ghosts**: link-type targets that need not have been issued by any allocator. These appear to live outside any allocation regime.

The design tolerates both, but does not name the distinction. There is no explicit allocator-state notion (e.g., "issued," "registered," "claimed") attached to a tumbler in the curated material — only the implicit social/contractual fact of whether an owner has baptized that subtree.

NEED_RAW: 4/23 (page 190), 4/44–4/45 (pages 211–212) — to check whether Nelson elsewhere addresses what makes a position "conceptually assigned" versus merely structurally expressible, and whether linking to a never-baptized address (as opposed to a baptized-but-unrepresented one) is treated as a separate case or folded into the same doctrine.
