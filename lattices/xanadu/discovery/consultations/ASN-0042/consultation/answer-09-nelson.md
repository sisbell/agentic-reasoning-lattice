## Question 9 [nelson]

> Must ownership boundaries align with the natural structural boundaries of the address hierarchy, or can ownership be assigned at arbitrary granularity?

## Ownership Must Align with Structural Boundaries

Nelson's design is explicit: **ownership follows the tree hierarchy of the tumbler address space.** There is no mechanism for assigning ownership at arbitrary granularity independent of structural boundaries.

### The Ownership-Hierarchy Principle

The tumbler system operates on what Nelson calls "owned numbers":

> "The basic principle is that of owned numbers. Numbers are owned by individuals or companies, and subnumbers under them are bestowed on other individuals and companies on whatever basis the owners choose. Whoever owns a specific node, account, document or version may in turn designate (respectively) new nodes, accounts, documents and versions, by forking their integers." [LM 4/17]

> "The owner of a given item controls the allocation of the numbers under it." [LM 4/20]

This creates a strict cascading delegation:

1. **Node owner** → controls account allocation beneath it
2. **Account owner** → controls document allocation beneath it  
3. **Document owner** → controls versions, content, and links beneath it

Each level owns everything structurally subordinate to it.

### The Document Is the Unit of Ownership

Nelson is unambiguous that the **document** is the fundamental ownership unit:

> "Every document has an owner, the person who created and stored it (or someone who arranged it to be created and stored, such as a publishing company)... Only the owner has a right to withdraw a document or change it." [LM 2/29]

> "By this convention, then, everything in the system is part of a document. No free-floating materials exist." [LM 2/29]

You cannot own byte 500 of someone else's document. You cannot own a span within a document independently of owning the document. The document boundary IS the ownership boundary.

### Sub-Document Ownership Through Transclusion, Not Through Arbitrary Assignment

When multiple authors contribute to a compound document, ownership is preserved through I-space origin, not through sub-document ownership grants:

> "Document A can include Document B, even though Document B is owned by someone else." [LM 2/35]

> "Each compound document is like the other documents: it has an owner and receives royalties." [LM 2/33]

The compound document's owner owns the *arrangement* (V-space). The *content* at each byte traces back to its I-space origin — the document where it was natively created. That native document has its own owner. Royalties split accordingly:

> "If a modified document is read, the original owner and the modifier split the royalty in proportion to who wrote what, as determined automatically." [LM 2/45]

This is not arbitrary sub-document ownership assignment. It is structural: the I-address encodes the home document, the home document has an owner, and that owner receives royalties for their bytes wherever they appear.

### Links Follow the Same Rule

Link ownership is also structurally determined:

> "A link need not point anywhere in its home document. Its home document indicates who owns it, and not what it points to." [LM 4/12]

You own links in your document. You do not own links in other people's documents, even if those links point at your content. Ownership is determined by the link's position in the address hierarchy, not by what it references.

### Achieving Fine-Grained Ownership: Create More Documents

If you need finer ownership granularity, the answer is to create more structural units. Nelson provides two mechanisms:

**Sub-accounts:** The User field is "continually subdividable for sub-accounts" [LM 4/29]. You can delegate sub-account ownership, creating new structural boundaries within your account.

**More documents:** Since "everything in the system is part of a document" and documents can be composed through transclusion, you achieve fine-grained ownership by factoring content into separate documents owned by separate parties, then assembling them through windows.

The account holder retains control over subdivision:

> "Typically, the user will have no control over the node address he, she or it is assigned; but once assigned a User account, the user will have full control over its subdivision forevermore." [LM 4/29]

### Summary

Ownership boundaries **must** align with the address hierarchy. Nelson provides no mechanism for cross-cutting ownership that violates structural boundaries. The system achieves flexible ownership not by allowing arbitrary assignment, but by making it trivially easy to create new structural units (documents, sub-accounts) and compose them through transclusion. The document is the atom of ownership; composition through windowing is the molecule.
