## Question 1 [theory]

> Did the "denial as fork" design intend that a principal can always unilaterally produce an owned address as the architectural answer to non-ownership, or was cooperation with sub-delegates an acceptable mode of forking in the multi-tier (node-with-accounts) case?

# Denial as Fork: Unilateral Action Within Owned Space

The design intent is **unilateral forking within already-owned space**, not cooperation across tiers. The "denial as fork" pattern presumes every principal already holds delegated territory in which they have exclusive control; cooperation is required only at the initial boundary of delegation, not for ongoing fork operations.

## The Architectural Answer to Non-Ownership

When a user encounters content they cannot modify, the answer is not negotiation with the owner but creation of a new owned object under their own account:

> "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate--without damaging the originals. This is done by inclusion links." [LM 2/45]

This works because the user already owns the address space where the new document lives. They do not ask Alice for permission to fork her document — they create a new document under their own account that windows hers.

## Exclusive Delegation Once Granted

Nelson is explicit that delegation hands over **full** control, not joint or cooperative control:

> "Typically, the user will have no control over the node address he, she or it is assigned; but once assigned a User account, the user will have full control over its subdivision forevermore." [LM 4/29]

> "The basic principle is that of owned numbers. Numbers are owned by individuals or companies, and subnumbers under them are bestowed on other individuals and companies on whatever basis the owners choose. Whoever owns a specific node, account, document or version may in turn designate (respectively) new nodes, accounts, documents and versions, by forking their integers." [LM 4/17]

> "The owner of a given item controls the allocation of the numbers under it." [LM 4/20]

"Forevermore" rules out a continuing cooperative role for the parent tier. The node assigns an account; from that moment on, the account holder allocates documents, versions, and links beneath that account on their own authority. No further node consent is required.

## Ownership Is Exclusive, Including Against Withdrawal

> "Every document has an owner... Only the owner has a right to withdraw a document or change it." [LM 2/29]

This applies symmetrically up and down the tree. The document owner cannot be forced by the account holder, the account holder cannot be forced by the node, and a non-owner trying to modify Alice's document cannot be helped by Alice's node operator either. The architectural response is: fork under your own account.

## Where Cooperation *Does* Enter

Cooperation is required exactly once per principal: at the boundary where a parent tier delegates space to a child. The node operator assigns an account ("the user will have no control over the node address he... is assigned"); after that the account is the user's exclusively. This bootstrap is not "cooperation as a forking mode" — it is the act of establishing the principal's owned space in the first place. Once established, all subsequent forks within that space are unilateral.

## Summary

| Operation | Mode |
|---|---|
| User forks a new version under their own document | Unilateral |
| User forks a new document under their own account | Unilateral |
| User creates a derivative of someone else's document | Unilateral (forks under own account, windows the original) |
| Node grants a new account to a user | One-time delegation (not a recurring cooperation) |
| Node tries to reach into a delegated account's allocations | Not permitted — "full control... forevermore" [LM 4/29] |

So: yes, a principal can always unilaterally produce an owned address as the architectural answer to non-ownership. Cooperation with sub-delegates is **not** an intended forking mode in the multi-tier case; the multi-tier structure exists to establish exclusive territories, not to require ongoing joint action within them.
