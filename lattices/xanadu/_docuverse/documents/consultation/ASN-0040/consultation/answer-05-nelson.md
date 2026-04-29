## Question 5 [nelson]

> If two independent acts of baptism occur at the same level of the hierarchy, what guarantees prevent them from producing the same position?

### Nelson's Answer

The address space is structured as a tree where each position anchors a disjoint subtree:

> "The entire tumbler works like that: nodes can spin off nodes; accounts can spin off accounts; nodes can spin off accounts; and so on. Thus all numeration in the docuverse is compressed into a single mechanism." (4/19)

The tree structure ensures that baptisms under different parent prefixes produce addresses in non-overlapping regions. Within a single parent's namespace, the sequential mechanism prevents collision:

> "For instance, if there is an item 2, it can branch into several more items, each of which is a daughter item. Thus 2.1, 2.2, 2.3, 2.4... are successive items being placed under 2." (4/20)

"Successive" means each baptism produces the next ordinal. Two baptisms under the same parent produce 2.1 then 2.2 — not two copies of 2.1. The mechanism is sequential by construction.

Across different parents, disjointness is structural. Items under 2 (2.1, 2.2, ...) and items under 3 (3.1, 3.2, ...) occupy non-overlapping address ranges because the parent prefixes differ. No coordination between independent subtrees is needed because the address space is pre-partitioned by the tree structure.

Nelson designed for decentralized operation:

> "For all these things it had to be assumed that no one would be in charge of the docuverse; that while it was growing continually, there would be no center." (4/16)

The collision guarantee is structural — disjoint subtrees cannot produce overlapping addresses — not procedural.
