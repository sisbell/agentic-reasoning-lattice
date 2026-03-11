## Question 3 [nelson]

> Can ownership of a document ever transfer from one user to another, or is the creator-owner relationship permanent?

## Ownership Transfer in Xanadu

Nelson explicitly contemplates ownership transfer. The key passage at 2/29 defines the owner broadly:

> "Every document has an owner, the person who created and stored it (or someone who arranged it to be created and stored, such as a publishing company). The rightful copyright holder, or someone who has bought the document rights... Only the owner has a right to withdraw a document or change it." [LM 2/29]

Three categories of owner are recognized here:

1. **The creator** — the person who actually wrote and stored the document
2. **The arranger** — someone who commissioned its creation (e.g., a publishing company)
3. **The purchaser** — "someone who has bought the document rights"

The phrase "bought the document rights" clearly implies ownership can transfer through sale, paralleling traditional copyright assignment.

### The Structural Tension

However, Nelson specifies **no mechanism** for ownership transfer within the system. The tumbler address permanently encodes the User field — the account under which the document was created:

> "There are four major fields, each expandable indefinitely, with three major dividers between them. These fields are Server, User, Document and Contents." [LM 4/26]

> "Typically, the user will have no control over the node address he, she or it is assigned; but once assigned a User account, the user will have full control over its subdivision forevermore." [LM 4/29]

The address `Node.0.User.0.Document.0.Element` always reflects the *original* creator's account. If ownership transfers, the document still resides at the original user's tumbler address. There is no FEBE operation for reassigning document ownership, and changing the address would violate the permanence guarantee.

### My Intent

Ownership transfer is a **legal and contractual** matter, not an addressing matter. The tumbler address records *provenance* (where the document was born), not necessarily current ownership. Just as a painting by Picasso retains its provenance even when sold to a collector, a Xanadu document retains its creation address even when rights transfer.

The enforcement model supports this interpretation — the system operates through contractual trust, not technical enforcement:

> "Because the conceptual structure expects participants to behave in certain ways, these are embraced in the contract offered to users." [LM 4/4]

Royalty routing, modification rights, and withdrawal authority would follow the current rightful owner, tracked through the contractual layer rather than the addressing layer.

### What Is NOT Specified

- No FEBE command for transferring ownership
- No mechanism for updating royalty routing after transfer
- No specification of what documentation or process validates transfer
- No statement on whether sub-accounts or delegation could model transferred rights

NEED_RAW: [2/29-2/31] — The full passage on document ownership may contain additional context about transfer mechanisms that the curated extract condensed.
