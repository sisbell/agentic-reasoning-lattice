## Question 5 [theory]

> When two users each try to give new content its own permanent identity at the same time, what guarantees that no two pieces of content ever end up sharing one identity?

## The guarantee: identities are never drawn from a shared pool

Two users creating content "at the same time" never collide because in Xanadu **nobody allocates from a common namespace in the first place.** The address space is a tree, every address is *owned*, and only the owner of an address may create sub-addresses beneath it. Two users working simultaneously are minting addresses in *disjoint* regions of that tree — each under their own account — so there is no shared resource to contend for, and therefore no race to lose.

This is the **owned-numbers / baptism** principle:

> "The basic principle is that of owned numbers. Numbers are owned by individuals or companies, and subnumbers under them are bestowed on other individuals and companies on whatever basis the owners choose. Whoever owns a specific node, account, document or version may in turn designate (respectively) new nodes, accounts, documents and versions, by forking their integers. We often call this the 'baptism' of new numbers." (4/17)

> "The owner of a given item controls the allocation of the numbers under it." (4/20)

## Why two users are structurally disjoint

Every piece of content has a tumbler I-address of the form `Node.0.User.0.Document.0.Element`. Two different users sit under different `(Node, User)` prefixes, and each one is sovereign over everything below their account:

> "Typically, the user will have no control over the node address he, she or it is assigned; but once assigned a User account, the user will have full control over its subdivision forevermore." (4/29)

New identities are made by *forking* — appending fresh digits to the right, under an address you already own:

> "One digit can become several by a forking or branching process. This consists of creating successive new digits to the right; we call these 'under' the previous digit." (4/20)

So if Alice (account A) and Bob (account B) each create a document at the same instant, Alice's content is baptized under `…A.0.…` and Bob's under `…B.0.…`. The prefixes differ before either of them touches a single element. Collision is impossible by construction, with zero coordination between them — which is exactly the problem the design exists to solve:

> "The entire tumbler works like that: nodes can spin off nodes; accounts can spin off accounts; nodes can spin off accounts; and so on. Thus all numeration in the docuverse is compressed into a single mechanism." (4/19)

> "So the docuverse is all really one big forking document." (4/18)

## Why "at the same time" is a non-issue: single allocator per subtree

The deeper point is that **uniqueness is structural, not procedural.** There is no lock because there is nothing shared to lock. Trace it up the tree and you find that *every* set of sibling numbers has exactly one authority issuing it:

- **Cross-user / cross-server** — disjoint `(Node, User)` prefixes; the two creators share no allocator at all.
- **Two accounts on one node** — the node is the sole party that hands out account numbers ("the user will have no control over the node address... assigned," 4/29), so it never issues the same one twice.
- **Two documents under one account** — the back end that owns that account mints the id and hands it back: "CREATENEWDOCUMENT... It returns the id of the new document." (4/65), and "The new document's id will indicate its ancestry." (4/66). A single server serializes its own minting.

By induction up the tree, no two siblings ever receive the same digit, so no two full addresses ever coincide. The only place where two simultaneous creators meet a *common* authority is when they're under the same owner — and there a single allocator simply serializes the two requests. Where they're under different owners, there's no meeting point to serialize.

Mark Miller's insight was precisely that one uniform naming structure could carry all of this:

> "In one big flash of insight, Mark Miller saw that everything could be named within a common structure, and that an arithmetic could be developed for this structure to be the common internal language throughout the search procedures of the system." (4/16)

## Identity is by creation-site, not by content

This is why even the hardest case — two users typing the *same bytes* at the same moment — is safe. Identity tracks *where and by whom* content was created, not what it says. Byte-identical text created independently in two accounts lands at two different I-addresses, because each was baptized in its own owned subtree. (Conversely, content that *shares* an I-address is the *same* content — that's what makes transclusion and correspondence work.) The address space never recycles or merges identities:

> "New items may be continually inserted in tumbler-space while the other addresses remain valid. This means that any address of any document in an ever-growing network may be specified by a permanent tumbler address." (4/19)

Once baptized, an address is yours forever and is never reassigned — so uniqueness, once established at creation, is also permanent.

## What I specified vs. what is left to the implementation

Be precise about the boundary here. What *Literary Machines* guarantees is the **principle**: a decentralized, ever-growing system in which addresses are allocated by hierarchical delegation, so that simultaneous creators in different subtrees can never collide and need never coordinate. That is design intent, and it is firm.

What I do *not* spell out in *Literary Machines* is the low-level **mechanism** by which a *single* owner/server serializes two simultaneous `CREATENEWDOCUMENT` calls into its own subtree — there is no discussion of locks, transactions, or "concurrent"/"race" handling, because at that point the duplicate-avoidance is the ordinary job of a single authority issuing distinct numbers, an implementation detail below the level of the proposal. The guarantee holds (one allocator ⇒ no duplicates); the engineering of that allocator is left to the back end. I'd flag any claim about *how* that serialization is implemented as going beyond the text.

---

**In one line:** No two pieces of content ever share an identity because identities are never handed out from a global pool — they are *forked under owned addresses*, and since each region of the address tree has exactly one owner who allocates within it, two simultaneous creators are either in different regions (no shared allocator) or under the same single allocator (which serializes them). Either way, collision is impossible (4/17, 4/19–4/20, 4/29).
