## Question 2 [nelson]

> Does ownership of a position automatically extend to all positions subordinate to it in the hierarchy?

## Yes for allocation authority. No for content ownership.

Nelson describes two distinct concepts that the question conflates:

### 1. Baptism Rights (Allocation Authority) — Yes, extends downward

The owner of a position controls the creation of sub-positions beneath it:

> "The owner of a given item controls the allocation of the numbers under it." [LM 4/20]

> "Whoever owns a specific node, account, document or version may in turn designate (respectively) new nodes, accounts, documents and versions, by forking their integers. We often call this the 'baptism' of new numbers." [LM 4/17]

A server operator creates accounts. An account holder creates documents. A document owner creates versions. This authority flows strictly downward through the hierarchy.

### 2. Content Ownership — No, does not extend upward

Once a subordinate position is assigned, its occupant owns it:

> "Typically, the user will have no control over the node address he, she or it is assigned; but once assigned a User account, the user will have full control over its subdivision forevermore." [LM 4/29]

> "Every document has an owner, the person who created and stored it... Only the owner has a right to withdraw a document or change it." [LM 2/29]

The node operator does not own the user's documents. The Storage Vendor contract makes this explicit — vendors are custodians, not owners:

> "Storage Vendor agrees to engage in best efforts for the preservation and privacy of all customer material, and not to breach the confidence of any customer, examining customers' stored materials only as required for the orderly maintenance of the system." [LM 5/14-5/15]

### 3. Addressability — Extends, but is not ownership

A search or link targeting a higher position reaches everything beneath it:

> "A link to or search of an account or node will find any of the documents under it." [LM 4/23]

This is a property of the address space, not an ownership claim. You can find all documents under an account because the tumbler tree structure makes them addressable as a contiguous span — but finding content is not the same as owning it.

### The Delegation Model

The pattern is delegation, not inheritance:

| Level | Controls allocation of... | Owns content of... |
|-------|--------------------------|---------------------|
| Node operator | Accounts under the node | The node itself only |
| Account holder | Documents under the account | Their documents |
| Document owner | Versions under the document | Their document |

Each level grants authority to the level below, then relinquishes control over what's created there. This parallels how DNS delegation works: ICANN controls TLDs, but once `example.com` is assigned, its registrant controls all subdomains.

### One gap

Nelson does not explicitly address what happens if a node operator *revokes* an account, or whether revocation is even possible. The Storage Vendor contract requires "orderly transition of all customer-stored materials to other Xanadu locations" upon cancellation [LM 5/16], suggesting the vendor cannot simply delete a user's content — but the authority relationship between node operator and account holder at the tumbler level is not fully specified.

NEED_RAW: 4/17-4/20 (for any additional detail on ownership delegation vs. inheritance that the curated summaries may have condensed)
