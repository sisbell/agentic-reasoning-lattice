## Question 10 [nelson]

> Must the system guarantee that no two parties can independently hold ownership of the same position?

Yes — exclusive ownership of each position is a structural invariant of the tumbler addressing system, though Nelson states it as a design property rather than as a separately enumerated guarantee.

## The Structural Argument

The tumbler system is a **tree** with strict ownership at every node. Three properties together enforce exclusivity:

**1. Owned numbers with singular ownership.**

> "The basic principle is that of owned numbers. Numbers are owned by individuals or companies, and subnumbers under them are bestowed on other individuals and companies on whatever basis the owners choose." [LM 4/17]

Nelson consistently uses the singular: "**the** owner of a given item controls the allocation of the numbers under it" [LM 4/20]. Not "an owner" or "owners" — **the** owner.

**2. Baptism as the sole creation mechanism.**

> "Whoever owns a specific node, account, document or version may in turn designate (respectively) new nodes, accounts, documents and versions, by forking their integers. We often call this the 'baptism' of new numbers." [LM 4/17]

New positions are created only by forking from a parent. The parent's owner is the sole authority who can baptize sub-numbers. Two independent parties cannot baptize the same address because doing so would require both to own the parent — which contradicts singular ownership at that level.

**3. The address encodes ownership.**

The I-space tumbler `Node.0.User.0.Document.0.Element` structurally encodes which account owns which document. The User field **is** the owner:

> "Typically, the user will have no control over the node address he, she or it is assigned; but once assigned a User account, the user will have full control over its subdivision forevermore." [LM 4/29]

The account holder has "full control" over subdivision — not shared control with anyone else.

## Why This Must Be Exclusive

Several of Nelson's guarantees depend on exclusive ownership being inviolable:

- **Modification rights**: "Only the owner has a right to withdraw a document or change it" [LM 2/29]. If two parties owned the same position, conflicting modifications would be irreconcilable.

- **Royalty accounting**: "Each published document has a cash register... the remainder becomes the author's profit" [LM 5/12]. The royalty flows to **the** owner. Dual ownership would make royalty disposition ambiguous.

- **Link ownership**: "Its home document indicates who owns it, and not what it points to" [LM 4/12]. Link ownership is determined by address; ambiguous ownership of positions would make link ownership ambiguous.

- **Origin traceability**: "You always know where you are, and can at once ascertain the home document of any specific word or character" [LM 2/40]. This guarantee requires unambiguous ownership at every I-address.

## Ownership Transfer vs. Dual Ownership

Nelson does allow ownership transfer — "the rightful copyright holder, or someone who has bought the document rights" [LM 2/29] — but this is succession, not co-ownership. At any point in time, each position has exactly one owner. The transfer replaces one owner with another; it does not create a second concurrent owner.

## What Nelson Does NOT Address

Nelson does not specify the mechanism that prevents collisions at the network level — that is, how two servers are prevented from independently assigning the same tumbler address to different parties. The tree structure makes this conceptually impossible (each server controls its own sub-tree), but the interserver coordination details are left to BEBE, which Nelson states is "still undergoing definition" [LM 4/70].

The franchise model provides a social backstop: Storage Vendors must "use software furnished by Project Xanadu without modification" [LM 5/14], so the allocation algorithm is centrally controlled even though allocation authority is distributed.

## Summary

Exclusive ownership of each position is not listed among Nelson's explicit "fundamental guarantees" but is a structural invariant of the tumbler tree that every explicit guarantee depends on. The tree-based baptism mechanism makes dual independent ownership of the same position architecturally impossible: you can only create sub-addresses beneath addresses you already exclusively own.
