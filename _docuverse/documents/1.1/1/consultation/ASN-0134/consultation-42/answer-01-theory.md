## Question 1 [theory]

> In the owned-numbers design, does an account own and serially allocate its document numbers as a sub-allocator — so two concurrent document creations under one account contend exactly as two content writers under one document do — or are document addresses proposed externally and only checked for uniqueness?

## Verdict

The first horn is correct. An account **owns and serially allocates its document numbers as a sub-allocator** — by baptism/forking. Document addresses are emphatically **not** proposed externally and merely checked for uniqueness. And by design the account→document allocation is structurally *the same mechanism* as the document→byte/link allocation, so two concurrent document creations under one account are the same shape of operation as two element allocations under one document — they meet at the same point: the owned node's allocation frontier.

But I specified the *allocation model*, not the *concurrency-control mechanism*. Whether that contention is resolved by literally the same lock is an implementation matter I left undesigned (see the caveat below).

## Why it's a sub-allocator, not external-proposal-and-check

The whole numeration scheme rests on **owned numbers**: the owner of a number *designates* (creates) the numbers beneath it. The owner is the allocator.

> "The basic principle is that of owned numbers... Whoever owns a specific node, account, document or version may in turn designate (respectively) new nodes, accounts, documents and versions, by forking their integers. We often call this the 'baptism' of new numbers." — 4/17

> "The owner of a given item controls the allocation of the numbers under it." — 4/20

Allocation is **serial / successive**, not value-proposed:

> "One digit can become several by a forking or branching process. This consists of creating successive new digits to the right; we call these 'under' the previous digit." — 4/20

> "For instance, if there is an item 2, it can branch into several more items, each of which is a daughter item. Thus 2.1, 2.2, 2.3, 2.4... are successive items being placed under 2." — 4/20

The decisive operational evidence is that the create operations **return** the assigned id — the caller never proposes it:

> "This creates an empty document. It returns the id of the new document." — CREATENEWDOCUMENT, 4/65

> "This creates a new document with the contents of document <doc id>. It returns the id of the new document. The new document's id will indicate its ancestry." — CREATENEWVERSION, 4/66

There is no "propose-an-address, check-for-collision" command anywhere in the protocol. The owner (here, the account, acting through the back end) hands out the next number under itself.

## Why the contention analogy holds structurally

The unification is explicit and is the point of the design — one allocator pattern at every depth of the tree:

> "Thus all numeration in the docuverse is compressed into a single mechanism." — 4/19

> "So the docuverse is all really one big forking document." — 4/18

The byte/link side of your analogy uses the same successive-baptism pattern under the document, e.g. links:

> "The links designated by a tumbler address are in their permanent order of arrival. A document includes only the links of which it is the home document." — 4/31

So: an account forking documents under itself, and a document forking byte/link element numbers under itself, are the same operation at different tree depths. At the level of the abstract model, two concurrent document creations under one account contend on the account's "next document" frontier exactly as two writers contend on a document's "next element" frontier. (A document number is itself further forkable into versions — "the version, or subdocument number is only an accidental extension of the document number," 4/29 — which is just the same forking one level deeper.)

## The boundary of what I specified

I specified the allocation *model* (owned numbers, serial baptism, single mechanism). I did **not** specify the *concurrency-control* mechanism. The protocol is stateless at the command level, and there is no locking protocol or treatment of simultaneous edits to the same owned node in the spec. The closest I come to concurrency is search, not allocation:

> "In later versions of the storage system, we expect the back end to combine the search models of different users to create a barrel-roll shared search model which repeatedly crosses the address space on behalf of all a server's users simultaneously." — 4/59

So the statement "two concurrent document creations contend *exactly* as two content writers do" is a correct **entailment of the unified forking design** — same allocator shape, same frontier — but it is not something I separately specified. The lock granularity and the contention-resolution protocol are left to the implementor, and an implementation is free to make account-level document allocation cheaper than, or differently serialized from, in-document element allocation without violating anything I wrote.

*(One inference flagged: the "exactly like content writers" contention equivalence is my entailment from the single-mechanism design — 4/18/19, 4/20, 4/31 — not a passage where I discuss allocation concurrency directly. I never address concurrency control of baptism in Literary Machines, so anything stronger than "same structural contention point" is implementation, not spec.)*
