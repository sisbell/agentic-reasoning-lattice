## Question 8 [theory]

> Does the design require that every fork be attributable to a specific user, and what must that attribution preserve?

# Forking Attribution

**Yes — every fork must be attributable to a specific owner.** This is structural, not metadata. The tumbler address itself encodes the owner.

## The Baptism Principle

> "The basic principle is that of owned numbers. Numbers are owned by individuals or companies, and subnumbers under them are bestowed on other individuals and companies on whatever basis the owners choose. Whoever owns a specific node, account, document or version may in turn designate (respectively) new nodes, accounts, documents and versions, by forking their integers. We often call this the 'baptism' of new numbers." [LM 4/17]

> "The owner of a given item controls the allocation of the numbers under it." [LM 4/20]

This means **forking requires ownership of the parent**. You cannot fork what you do not own. Every fork is therefore traceable to the user who owned the parent and performed the baptism.

## What Attribution Must Preserve

### 1. Owner Identity (Structural)

The tumbler address has four fields: `Node.0.User.0.Document.0.Element` [LM 4/26]. The **User field is part of the address itself** — it cannot be stripped, falsified, or omitted. Attribution is the address.

### 2. Ancestry (The Derivation Chain)

Forking creates parent-child relationships that are permanent and visible:

> "A server node, or station, has ancestors and may have possible descendant nodes. An account, too, and a document, all have possible descendants." [LM 4/19]

For versions specifically, the CREATENEWVERSION operation explicitly preserves lineage:

> "This creates a new document with the contents of document <doc id>. It returns the id of the new document. **The new document's id will indicate its ancestry.**" [LM 4/66]

### 3. Permanence

Once a fork is baptized, the relationship is permanent — no reorganization ever happens:

> "New items may be continually inserted in tumbler-space while the other addresses remain valid." [LM 4/19]

### 4. Ownership Rights and Responsibilities

Attribution carries semantic weight:

> "Every document has an owner, the person who created and stored it... Only the owner has a right to withdraw a document or change it." [LM 2/29]

## The Unified Forking Structure

Nelson treats the entire docuverse as one forking tree:

> "So the docuverse is all really one big forking document." [LM 4/18]

> "The entire tumbler works like that: nodes can spin off nodes; accounts can spin off accounts; nodes can spin off accounts; and so on. Thus all numeration in the docuverse is compressed into a single mechanism." [LM 4/19]

This means servers fork from servers, accounts from servers, documents from accounts, versions from documents, characters from versions — **each level inherits attributability from the level above**.

## Caveat: Anonymous Accounts

The User field is structurally required, but Nelson allows the underlying identity to be pseudonymous:

> "There is no reason that anonymous publication by walk-in and transient users of this system should not be allowed. We may call this 'John Doe publication.'" [LM 2/60]

So attribution preserves *which account* performed the fork, but that account may not be tied to a real-world identity. The structural attribution is non-negotiable; the social identification of the account holder is.

## Summary

| Must Preserve | How |
|---------------|-----|
| Owner identity | User field of tumbler address (structural) |
| Ancestry chain | Address shows derivation path through forking |
| Permanence | Address never changes, relationship is forever |
| Modification rights | Only owner may change or withdraw |
| Royalty destination | Cash register at owner's address |

The design does not just *allow* attribution — it *requires* it as a precondition for the fork to exist. You cannot create an unattributed fork because there is no address structure that omits the User field.
