## Question 8 [theory]

> Was baptism intended as the same mechanism as per-allocator address allocation, or as a distinct registry-level layer sitting above it?

## Answer

Baptism was intended as **the same mechanism** as per-allocator address allocation — not a distinct registry-level layer above it. In Nelson's design, "baptism" is simply the name for the act by which an owner forks new sub-numbers under a number they already own. There is no separate registry sitting above this; the allocation *is* the baptism.

The defining quote ties the term directly to owned-number forking:

> "The basic principle is that of owned numbers. Numbers are owned by individuals or companies, and subnumbers under them are bestowed on other individuals and companies on whatever basis the owners choose. Whoever owns a specific node, account, document or version may in turn designate (respectively) new nodes, accounts, documents and versions, by forking their integers. We often call this the 'baptism' of new numbers." (4/17)

Two further points make clear this is a *single, decentralized* mechanism rather than a layered one:

1. **Allocation authority is purely local to the owner** — there is no central allocator or registry to consult:

   > "The owner of a given item controls the allocation of the numbers under it." (4/20)

2. **All numeration collapses into one uniform operation** across every entity type (servers, accounts, documents, versions):

   > "The entire tumbler works like that: nodes can spin off nodes; accounts can spin off accounts; nodes can spin off accounts; and so on. Thus all numeration in the docuverse is compressed into a single mechanism." (4/19)

The phrase "compressed into a single mechanism" is the strongest statement of intent: Nelson deliberately avoided a separate registry layer. The whole appeal of the scheme is that it solves decentralized address allocation *without* a coordinating authority — each owner baptizes addresses within their own subtree, and those addresses remain permanently valid:

> "New items may be continually inserted in tumbler-space while the other addresses remain valid." (4/19)

So baptism is the per-allocator (per-owner) allocation primitive itself, exercised independently by each owner over their own subtree. It is the mechanism, not a layer above it.
