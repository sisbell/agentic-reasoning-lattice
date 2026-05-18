## Question 7 [theory]

> What is the design-level discipline for node baptism — is there a single authority that issues node addresses, and what uniqueness guarantee does that authority provide? Should this guarantee be specified at the docuverse model level or treated as out-of-scope?

**Design-level discipline for node baptism**

The baptism principle is universal: "Whoever owns a specific node, account, document or version may in turn designate (respectively) new nodes, accounts, documents and versions, by forking their integers. We often call this the 'baptism' of new numbers" [LM 4/17]. Node addresses are the special case because they require a root.

**The implicit root authority**

The discipline rests on a structural fact: "The server address always begins with the digit 1, since all other servers are descended from it. This may seem an unnecessary redundancy, but it permits referring to the entire docuverse by '1' on the first position" [LM 4/28]. Exactly one ancestor of all nodes — someone must own that root.

In my design, that owner is Project Xanadu, the franchisor. The contractual structure — one of the three structures (conceptual, technical, contractual) I called essential — licenses Storage Vendors who "use software furnished by Project Xanadu without modification" and "honor requests for material from customers connected to servers operated by other Xanadu-licensed storage vendors" [LM 5/14]. Node baptism happens through the franchise: a vendor receives their node digit when they sign the Storage Vendor contract. Beyond the root, the recursive "owned numbers" principle takes over: "The owner of a given item controls the allocation of the numbers under it" [LM 4/20].

**What kind of uniqueness guarantee?**

It is **contractual, not algorithmic**. I did not design a cryptographic uniqueness mechanism. Two vendors cannot collide because exactly one entity allocates from "1", and recursion handles the rest. This is the same kind of guarantee that printers' guilds once provided for shop marks — institutional discipline backed by signed agreements.

**Should this be in the docuverse model?**

It belongs at the model level. The permanence guarantee — that "any address of any document in an ever-growing network may be specified by a permanent tumbler address" [LM 4/19] — collapses without root-level uniqueness. If node digits can collide, every downstream address becomes ambiguous and the entire address space loses meaning.

What is implementation detail is *how* the root authority validates and issues nodes (web form, signed contract, blockchain — I take no position). What is model-level is *that* a single root authority exists, *that* its uniqueness guarantee is contractual rather than mathematical, and *that* the "owned numbers" discipline propagates that uniqueness downward through delegation. The model must commit to this much because the permanence and attribution guarantees rest on it.

NEED_RAW: 4/17-4/22 for the full tumbler discipline text and any explicit statement about who specifically allocates initial node digits versus the general franchise framework; also 5/14-5/16 for the precise Storage Vendor contract language around node assignment.
