## Question 1 [theory]

> Is an account intended to support document creation beneath it the instant it exists — i.e. does account provisioning conceptually carry, as a built-in guarantee, an available document sub-allocator with no separate activation step?

Yes. Account provisioning conceptually carries an immediate, built-in document sub-allocator — there is no separate activation step. The capacity to baptize documents beneath an account is structural: it follows automatically from owning the account's number.

## The baptism principle is intrinsic to ownership

In Xanadu's tumbler model, the right to allocate sub-addresses is not a separate feature granted to an account — it *is* what owning a number means:

> "The basic principle is that of owned numbers. Numbers are owned by individuals or companies, and subnumbers under them are bestowed on other individuals and companies on whatever basis the owners choose. Whoever owns a specific node, account, document or version may in turn designate (respectively) new nodes, accounts, documents and versions, by forking their integers. We often call this the 'baptism' of new numbers." (tumblers, 4/17)

So the moment an account exists as an owned position, its owner already holds the authority to fork documents under it. The sub-allocator is not provisioned separately — it is the same mechanism that defines ownership.

## Forking is uniform and always-available

The forking concept makes clear that subdivision works identically at every level and is never exhausted or gated:

> "The entire tumbler works like that: nodes can spin off nodes; accounts can spin off accounts; nodes can spin off accounts; and so on. Thus all numeration in the docuverse is compressed into a single mechanism." (forking, 4/19)

> "The owner of a given item controls the allocation of the numbers under it." (forking, 4/20)

The user-facing guarantee tied to this is precisely that creation never requires a setup or "finding an address" step:

> "Creating a new document doesn't require 'finding' an unused address - you simply fork a new one under your account... Your addresses belong to you; no one else can create content at addresses under your ownership." (forking, How Users Experience It)

## Accounts can be "ghost elements" — they need no stored object to be allocatable-under

Critically, an account need not have any stored object materialized for documents to be created beneath it. The account's position on the tumbler line is enough:

> "While servers, accounts and documents logically occupy positions on the developing tumbler line, no specific element need be stored in tumbler-space to correspond to them. Hence we may call them ghost elements." (ghost-elements, 4/23)

> "It is possible to link to a node, or an account, even though there is nothing stored in the docuverse corresponding to them. A link to or search of an account or node will find any of the documents under it." (ghost-elements, 4/23)

This is the strongest evidence against any "activation step": the account exists purely as a conceptual position, yet documents can immediately be forked under it and will be found there.

## Control is permanent and immediate from assignment

The session-model curation captures the moment of grant directly:

> "Typically, the user will have no control over the node address he, she or it is assigned; but once assigned a User account, the user will have full control over its subdivision forevermore." (4/29, quoted in session-model)

"Full control over its subdivision forevermore" — from the instant of assignment — is exactly the built-in, no-activation guarantee the question asks about.

## Conclusion

The document sub-allocator is conceptually inseparable from the account itself. Owning an account *is* holding the power to fork documents beneath it; the account's mere existence as a tumbler position (even as a ghost element) suffices. Nelson specifies no enabling, opening, or activation step between "account exists" and "documents can be created under it" — the single baptism mechanism applies uniformly and permanently from the moment of assignment.

One caveat on terminology: Nelson describes this at the level of the *addressing/ownership model* (tumblers, baptism, ghost elements). He does not use the phrase "sub-allocator" or frame it as a provisioned component — that is implementation vocabulary. The conceptual guarantee, however, is unambiguous in the verified sources above.
