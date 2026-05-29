## Question 1 [theory]

> Was tumbler baptism designed to occur through a single sequential allocation authority (linear history), or did the design contemplate concurrent/branching allocation from genesis?

The design unambiguously contemplated **concurrent/branching allocation from genesis**, not a single sequential allocation authority. This is the entire point of the tumbler/baptism mechanism.

## The core mechanism: owned numbers, forked independently

Baptism is decentralized by design. Whoever owns a number allocates the sub-numbers beneath it on their own authority, without coordinating with any central allocator:

> "The basic principle is that of owned numbers. Numbers are owned by individuals or companies, and subnumbers under them are bestowed on other individuals and companies on whatever basis the owners choose. Whoever owns a specific node, account, document or version may in turn designate (respectively) new nodes, accounts, documents and versions, by forking their integers. We often call this the 'baptism' of new numbers." (4/17)

> "The owner of a given item controls the allocation of the numbers under it." (4/20)

Allocation is therefore inherently parallel: server 1.2 baptizing account 1.2.3 requires no agreement from server 1.4, and account 1.2.3 spawning documents requires no agreement from anyone above or beside it.

## Branching is the structure, not a later addition

The numeration is forking from the root. Everything is one branching tree, and items spin off daughter items:

> "So the docuverse is all really one big forking document." (4/18)

> "The entire tumbler works like that: nodes can spin off nodes; accounts can spin off accounts; nodes can spin off accounts; and so on. Thus all numeration in the docuverse is compressed into a single mechanism." (4/19)

> "For instance, if there is an item 2, it can branch into several more items, each of which is a daughter item. Thus 2.1, 2.2, 2.3, 2.4... are successive items being placed under 2." (4/20)

## Genesis is a single root, but allocation under it is concurrent

There is one notational origin — the server line always begins with digit 1 — but this is a *root of a tree*, not a linear sequence through a single authority:

> "The server address always begins with the digit 1, since all other servers are descended from it. This may seem an unnecessary redundancy, but it permits referring to the entire docuverse by '1' on the first position." (4/28)

All servers descend from node 1 by forking, and from that point allocation fans out concurrently across independent owners.

## Why this matters: it solves decentralized coordination

The forking design exists precisely *because* a single sequential allocator would not scale to an unpredictably growing, decentralized network. As the curated `forking` source frames it, this "solves the fundamental coordination problem of a decentralized system: how can millions of independent actors create content without a central authority allocating addresses? The answer is delegation through ownership." New items can be inserted anywhere while all existing addresses stay valid:

> "New items may be continually inserted in tumbler-space while the other addresses remain valid. This means that any address of any document in an ever-growing network may be specified by a permanent tumbler address." (4/19)

## One caveat — time is deliberately excluded

Note that "linear history" in the temporal sense is explicitly *not* encoded in the tumbler. Baptism orders things by tree position, not by global creation sequence:

> "Note that 'time' is not included in the tumbler. Time is kept track of separately." (4/18)

So there is no global sequential timeline driving allocation either; ordering is structural (depth-first tree position), and time is tracked separately as metadata.

## Conclusion

Tumbler baptism was designed for **concurrent, branching allocation from genesis**. There is a single notational root (node 1), but allocation authority is distributed: each owner independently forks sub-addresses within their owned subtree without central coordination. A single sequential allocation authority is exactly what the design was built to avoid.
