## Question 2 [nelson]

> Must every link be a permanent object in the docuverse with its own stable identity, just as documents and content are permanent?

# Are Links Permanent Objects in the Docuverse?

**Yes.** The evidence from Literary Machines is strong and consistent: links are permanent objects with stable identity, treated architecturally on par with content bytes.

## Links Are One of Only Two Stored Object Types

Nelson is explicit that the docuverse stores exactly two kinds of things:

> "In the present implementation (XU.87.1), the only entities actually stored in tumbler-space are content bytes and links." [LM 4/23]

Everything else — servers, accounts, documents — are "ghost elements" that exist only as conceptual positions in the address hierarchy. Links and bytes are the real, stored substance of the docuverse.

## Links Have Permanent Tumbler Addresses

Links occupy the `2.x` subspace within a document and are addressed by creation order. Crucially, this order is permanent:

> "The links designated by a tumbler address are in their permanent order of arrival." [LM 4/31]

This means link `2.1` is always the first link created in that document, link `2.755` is always the 755th. Deleting link `2.5` does not renumber `2.6` through `2.N`. The address is stable and never reused.

This is stronger than the permanence of byte positions. Bytes can be rearranged in V-space (their visual positions shift with editing). Links cannot — they keep their creation-order addresses permanently.

## Link-to-Link Requires Stable Identity

The strongest architectural argument: because links have tumbler addresses, other links can point to them.

> "Because of the universality of tumbler-space, and the fact that links are located there as well as data, it becomes easy for a link to point at another link (or, indeed, to point at several)." [LM 4/49]

> "The to-set of the link need simply point to the actual link address in the tumbler line, with a span of 1 to designate that unit only." [LM 4/49]

If Alice creates a link and Bob creates a link-to-link pointing at Alice's link, Bob's link depends on Alice's link having a stable, resolvable address — exactly the same dependency that makes published documents permanent:

> "It is in the common interest that a thing once published stay published, as in the world of paper. Other readers and users will come to depend on its accessibility." [LM 2/43]

Nelson does not explicitly extend this obligation to links targeted by other links, but the architectural logic is identical: if links can be targets, they must be reliable targets.

## "Deleted" Links Are Not Destroyed

Page 4/9 shows a diagram of a document's technical contents. Both deleted bytes and deleted links receive the **exact same description**:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

> "DELETED LINKS (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

This parallel treatment is telling. "Deleting" a link does not destroy it — it moves the link to a state of being "not currently addressable," just as deleting bytes removes them from V-space but preserves them in I-space. The link awaits historical backtrack (can be recovered from version history) and may persist in other versions of the document.

## The Overall Architecture

Putting it together:

| Property | Content Bytes | Links |
|----------|--------------|-------|
| Actually stored in tumbler-space | Yes [4/23] | Yes [4/23] |
| Permanent address | Yes (I-space) | Yes (creation order) [4/31] |
| Can be target of links | Yes | Yes [4/49] |
| "Deletion" = not currently addressable | Yes [4/9] | Yes [4/9] |
| Recoverable via historical backtrack | Yes [4/9] | Yes [4/9] |
| May persist in other versions | Yes [4/9] | Yes [4/9] |

Links enjoy the same permanence architecture as content. They are stored objects with permanent addresses, can be targets of other links, and are not destroyed by deletion — only rendered "not currently addressable."

## One Nuance

Links CAN be deleted by their owner (the owner of the link's home document). Nelson does not impose the same explicit withdrawal restriction on individual links that he imposes on published documents. But the deletion semantics — "awaiting historical backtrack functions, may remain included in other versions" — make clear that even "deleted" links are preserved in the system, just as "deleted" bytes are.

The system's permanence guarantee — "any address of any document in an ever-growing network may be specified by a permanent tumbler address" [LM 4/19] — applies to link addresses as much as to any other tumbler address. Once a link exists at address `N.0.U.0.D.V.0.2.1`, that address is permanently assigned and never recycled.
