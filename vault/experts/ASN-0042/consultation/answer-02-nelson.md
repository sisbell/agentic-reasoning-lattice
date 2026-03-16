## Question 2 [nelson]

> Is ownership inherently hierarchical — does owning a position automatically confer ownership of all positions subordinate to it in the address structure?

## Ownership and Hierarchy in Tumbler Space

The short answer: **allocation authority is hierarchical, but ownership of content is not transitive**. Owning a position gives you the right to *create* subordinate positions, but not to *own* what is created under delegated sub-positions.

### What Nelson Specifies

Nelson establishes two distinct concepts that the question conflates:

**1. Baptism authority (hierarchical)**

> "The owner of a given item controls the allocation of the numbers under it." [LM 4/20]

> "Whoever owns a specific node, account, document or version may in turn designate (respectively) new nodes, accounts, documents and versions, by forking their integers. We often call this the 'baptism' of new numbers." [LM 4/17]

This is clearly hierarchical. If you own position X, you can create X.1, X.2, X.3 beneath it. No one else can.

**2. Content ownership (follows creation, not hierarchy)**

> "Every document has an owner, the person who created and stored it (or someone who arranged it to be created and stored, such as a publishing company)... Only the owner has a right to withdraw a document or change it." [LM 2/29]

Ownership follows *who created*, not *where in the tree*. The owner is the creator, not the parent position's owner.

### The Delegation Boundary

Nelson draws this distinction explicitly at the account level:

> "Typically, the user will have no control over the node address he, she or it is assigned; but once assigned a User account, the user will have full control over its subdivision forevermore." [LM 4/29]

This reveals the pattern:
- The **server operator** allocates account positions (baptizes user numbers)
- But once assigned, the **account holder** has "full control over its subdivision forevermore"
- The server operator cannot reach down into the user's domain

The word "forevermore" is significant — delegation is permanent and irrevocable. The parent cannot reclaim allocation authority once delegated.

### The Four-Field Structure Encodes This

The tumbler address `Node.0.User.0.Document.0.Element` has three zero-delimited boundaries, each representing a delegation point:

| Level | Allocated By | Owned By |
|-------|-------------|----------|
| Node | Parent node operator | Node operator |
| Account | Node operator | Account holder |
| Document | Account holder | Account holder (creator) |
| Element | System (append-only) | Document owner |

Each zero-delimiter marks where authority transfers from one party to another. The server operator baptizes accounts but does not own the documents created under those accounts.

### What About the Server's Relationship to User Content?

The enforcement model makes this explicit through the Storage Vendor contract:

> "Storage Vendor agrees to engage in best efforts for the preservation and privacy of all customer material, and not to breach the confidence of any customer, examining customers' stored materials only as required for the orderly maintenance of the system." [LM 5/14-5/15]

The vendor has *custodial obligations*, not ownership rights. The vendor holds the content but may not examine it except for maintenance. This is the opposite of hierarchical ownership — the higher-level entity (vendor) is *constrained* by the lower-level entity's (user's) rights.

### Versions: The Telling Case

When a user creates a new version of someone else's document:

> "This creates a new document with the contents of document \<doc id\>. It returns the id of the new document. The new document's id will indicate its ancestry." [LM 4/66]

The new version lives under the *creating user's* account, not under the original document's position. The address indicates ancestry but ownership follows creation. This confirms that the hierarchy tracks *provenance* (where something came from), not *authority* (who controls it).

### Summary

| Question | Answer |
|----------|--------|
| Does owning X let you create X.1, X.2...? | **Yes** — baptism authority is hierarchical |
| Does owning X mean you own X.1? | **Only if you created X.1 yourself** |
| Can the server operator modify user documents? | **No** — contractually prohibited |
| Can delegation be revoked? | **No** — "full control... forevermore" |
| Does the hierarchy encode ownership? | **No** — it encodes provenance and delegation |

The tumbler hierarchy is a *delegation tree*, not an *ownership tree*. Each level delegates creation authority to the next, but delegation is permanent and the delegatee owns what they create. The address tells you the *lineage* of how something came to exist, not who currently controls it.
