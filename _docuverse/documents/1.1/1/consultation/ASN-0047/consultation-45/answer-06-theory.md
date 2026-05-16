## Question 6 [theory]

> What guarantees does Nelson's design require of the node-identifier namespace — is global uniqueness assumed as a property of the namespace, or established by some protocol?

# Node-Identifier Guarantees: Established by Protocol, Not Assumed

Global uniqueness of node identifiers is **established by protocol**, not assumed as a namespace property. The protocol is hierarchical "baptism" rooted at a single ancestor.

## The Three Mechanisms

**1. A single root.** All server addresses descend from server 1:

> "The server address always begins with the digit 1, since all other servers are descended from it. This may seem an unnecessary redundancy, but it permits referring to the entire docuverse by '1' on the first position." [LM 4/28]

This eliminates the multi-root coordination problem — there is no parallel universe of node 2 to collide with.

**2. Owned numbers with delegated allocation.** Uniqueness is enforced by ownership of subtrees, not by central registration:

> "The basic principle is that of owned numbers. Numbers are owned by individuals or companies, and subnumbers under them are bestowed on other individuals and companies on whatever basis the owners choose. Whoever owns a specific node, account, document or version may in turn designate (respectively) new nodes, accounts, documents and versions, by forking their integers. We often call this the 'baptism' of new numbers." [LM 4/17]

> "The owner of a given item controls the allocation of the numbers under it." [LM 4/20]

**3. Forking as the sole growth mechanism.** New identifiers come into existence only by extending an existing owned address to the right:

> "A server node, or station, has ancestors and may have possible descendant nodes... nodes can spin off nodes; accounts can spin off accounts; nodes can spin off accounts; and so on. Thus all numeration in the docuverse is compressed into a single mechanism." [LM 4/19]

> "One digit can become several by a forking or branching process. This consists of creating successive new digits to the right; we call these 'under' the previous digit." [LM 4/20]

## Why Uniqueness Holds

Uniqueness is **structural**, falling out of the protocol:

- One root means no top-level collisions.
- Each owner controls their own subtree exclusively, so no two parties can baptize the same sub-address.
- New addresses are only created by extension to the right, never by reuse, so existing addresses cannot collide with new ones: *"New items may be continually inserted in tumbler-space while the other addresses remain valid."* [LM 4/19]

This is the same principle as Dewey Decimal subdivision, but with **ownership** enforcing uniqueness at each branch rather than a central cataloger.

## What Nelson Does Not Specify

The franchise contracts (LM 5/14) imply that Project Xanadu, as franchisor, is the implicit owner of server 1 and thus controls allocation of top-level node addresses (1.1, 1.2, 1.3, ...) to licensed Storage Vendors. But Nelson does not explicitly describe a "server-1 allocation protocol" — the franchise model is the substrate that makes the hierarchical baptism work at the top.

NEED_RAW: 4/17, 4/19-4/20 — to verify whether Nelson discusses initial top-of-tree allocation more explicitly than the curated sources capture, and whether the franchise/baptism connection is made explicit.

## Summary

| Property | Source |
|----------|--------|
| Uniqueness | **Established by protocol** (forking baptism + ownership) |
| Coordination cost | None — each owner allocates locally under their subtree |
| Foundational assumption | A single root (server 1) and unforgeable ownership |
| What the namespace alone guarantees | Nothing — without baptism discipline, the tumbler line is just a number system |

The namespace is a passive coordinate system; the protocol is what makes addresses unique. Nelson is explicit that this is by design: *"no central registration required - owners simply 'baptize' new addresses under their own."*
