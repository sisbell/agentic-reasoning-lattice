## Question 9 [nelson]

> If an owner delegates a sub-range of their space, can the delegate further sub-delegate portions of that range to others?

## Yes — Sub-Delegation Is Inherent in the Design

The forking mechanism is **recursive by definition**. Whoever owns a number controls all sub-numbers beneath it, and whoever receives a sub-number becomes its owner with the same power.

### The Core Principle

> "The owner of a given item controls the allocation of the numbers under it."
> — [LM 4/20]

This is the complete rule. There is no qualifier like "only the original owner" or "only one level deep." Ownership of a number confers full authority over its subdivision.

### How It Works

> "Whoever owns a specific node, account, document or version may in turn designate (respectively) new nodes, accounts, documents and versions, by forking their integers. We often call this the 'baptism' of new numbers."
> — [LM 4/17]

So if Server 1 bestows Account 1.3 on Alice, Alice owns 1.3 and can create documents 1.3.1, 1.3.2, etc. She can also sub-delegate: bestow sub-account 1.3.5 on Bob. Bob then owns 1.3.5 and can create 1.3.5.1, 1.3.5.2 — or further delegate 1.3.5.7 to Carol. Carol can then fork beneath 1.3.5.7 indefinitely.

Nelson makes the recursive nature explicit:

> "The entire tumbler works like that: nodes can spin off nodes; accounts can spin off accounts; nodes can spin off accounts; and so on. Thus all numeration in the docuverse is compressed into a single mechanism."
> — [LM 4/19]

The "and so on" is not hand-waving — it's the point. The mechanism repeats at every level:

> "A server node, or station, has ancestors and may have possible descendant nodes. An account, too, and a document, all have possible descendants."
> — [LM 4/19]

### Permanence of Delegated Authority

Once assigned, control is permanent:

> "Typically, the user will have no control over the node address he, she or it is assigned; but once assigned a User account, the user will have full control over its subdivision forevermore."
> — [LM 4/29]

"Forevermore" — not "until the parent revokes it." The delegation is a one-way act. You baptize a sub-number and the new owner takes permanent control of that subtree.

### The Architectural Consequence

> "So the docuverse is all really one big forking document."
> — [LM 4/18]

The entire docuverse is a single recursively-forking tree. Every node in the tree has the same property: its owner can subdivide it, and each subdivision's new owner can subdivide further. There is no distinguished "root level" with special powers — the mechanism is uniform at every depth.

### Summary

Sub-delegation is not merely permitted — it is the **only** delegation mechanism. There is no way to grant someone a number while restricting their ability to fork beneath it. Ownership of a tumbler address means control of its entire subtree, including the right to delegate sub-ranges to others who gain the same recursive authority.
