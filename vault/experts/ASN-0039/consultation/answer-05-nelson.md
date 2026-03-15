## Question 5 [nelson]

> If two independent acts of baptism occur at the same level of the hierarchy, what guarantees prevent them from producing the same position?

### Nelson's Answer

Ownership partition. The address space is pre-partitioned by ownership, and only the owner of a position can baptize beneath it:

> "The owner of a given item controls the allocation of the numbers under it." (4/20)

> "Whoever owns a specific node, account, document or version may in turn designate (respectively) new nodes, accounts, documents and versions, by forking their integers." (4/17)

Two independent actors can only baptize simultaneously if they own different positions. Since each owner controls only their own subtree, independent baptisms produce addresses in non-overlapping regions of the address space. No coordination is needed because the space is pre-partitioned by ownership.

Nelson designed this explicitly for decentralization:

> "For all these things it had to be assumed that no one would be in charge of the docuverse; that while it was growing continually, there would be no center." (4/16)

The "baptism" principle solves the coordination problem: "whoever owns a specific address can designate new sub-addresses by forking their integers, without coordinating with anyone else." The guarantee against collision is structural — disjoint ownership domains cannot produce overlapping addresses.

The entire docuverse is "all really one big forking document" (4/18). The tree structure ensures that independent forks at different branches never collide.
