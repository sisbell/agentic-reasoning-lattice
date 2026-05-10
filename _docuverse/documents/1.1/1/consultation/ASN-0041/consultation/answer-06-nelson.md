## Question 6 [nelson]

> Can ownership be transferred from one party to another, and if so, does the original owner retain any residual rights?

## Ownership Transfer in Xanadu

### Transfer Is Acknowledged but Mechanically Unspecified

Nelson acknowledges that ownership can change hands. His definition of "owner" on page 2/29 is notably broad:

> "Every document has an owner, the person who created and stored it (or someone who arranged it to be created and stored, such as a publishing company). The rightful copyright holder, or someone who has bought the document rights... Only the owner has a right to withdraw a document or change it." [LM 2/29]

This definition admits at least three paths to ownership:
1. **Creation** — you made it
2. **Arrangement** — you commissioned it (e.g., a publishing company)
3. **Purchase** — you "bought the document rights"

The phrase "someone who has bought the document rights" explicitly presumes transfer is possible. But Nelson specifies **no in-system mechanism** for executing a transfer — no TRANSFEROWNERSHIP command in the FEBE protocol, no contract provision for reassignment, no tumbler-level operation.

### The Structural Tension

Transfer creates an architectural tension that Nelson does not resolve. The I-space address permanently encodes the originating account:

> "There are four major fields, each expandable indefinitely, with three major dividers between them. These fields are Server, User, Document and Contents." [LM 4/26]

If Alice creates a document, its I-address is `Node.0.Alice.0.Doc.0.Element`. If Bob buys the rights, the address still says "Alice." The permanence guarantee forbids changing it:

> "New items may be continually inserted in tumbler-space while the other addresses remain valid." [LM 4/19]

So after transfer, the system would need to distinguish between **structural origin** (encoded in the address — always Alice) and **current ownership** (now Bob). Nelson does not describe how this distinction is tracked. The curated sources contain no discussion of an ownership registry, transfer ledger, or reassignment metadata.

### Residual Rights: Not Explicitly Addressed

Nelson says nothing about whether the original owner retains any rights after transfer. The curated sources are silent on:

- Moral rights (attribution after transfer)
- Reversion rights (reclaiming ownership under certain conditions)
- Revenue sharing between original creator and new owner
- Whether the original creator retains any control over modifications

However, there is one **structural residual** that cannot be eliminated: origin traceability.

> "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control." [LM 4/11]

Because the I-address permanently encodes the creating account, the system will always show that Alice's account originated the content — even if Bob now owns it. This is not a "right" in the legal sense, but it is a permanent structural fact that no transfer can erase. Whether Nelson intended this as a form of inalienable attribution or simply as an artifact of the addressing scheme is not stated.

### The Publishing Complication

For published documents, transfer is further constrained by permanence obligations:

> "It is in the common interest that a thing once published stay published, as in the world of paper. Other readers and users will come to depend on its accessibility. Consequently its author may not withdraw it except by lengthy due process." [LM 2/43]

A new owner inherits this obligation. The publication contract binds the document, not the person — anyone who owns a published document must keep it published because others' links depend on it.

### Summary

| Question | Answer |
|----------|--------|
| Can ownership be transferred? | Yes — Nelson explicitly mentions "someone who has bought the document rights" |
| Is there a transfer mechanism? | No — no FEBE command, no contract provision, no protocol |
| Does the original owner retain rights? | Not specified |
| Does structural attribution persist? | Yes — I-addresses permanently encode the originating account |
| Does the new owner inherit obligations? | Implied — published documents must stay published regardless of owner |

NEED_RAW: [2/29-2/31, 5/6-5/10] — These pages may contain additional detail on ownership mechanics and the business framework for rights transfer that the curated sources summarize only partially.
