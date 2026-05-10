## Question 1 [nelson]

> Does owning a position in the address space mean exclusive authority over that region, or can multiple users share ownership of the same position?

## Ownership Is Exclusive Authority

Owning a position in tumbler-space means **exclusive, hierarchical authority** over that region. Nelson's model has no concept of shared ownership at the same address. The architecture enforces this at every level.

### The Hierarchical Delegation Model

Ownership flows downward through the tree by delegation ("baptism"):

> "The basic principle is that of owned numbers. Numbers are owned by individuals or companies, and subnumbers under them are bestowed on other individuals and companies on whatever basis the owners choose." (4/17)

> "The owner of a given item controls the allocation of the numbers under it." (4/20)

Each level delegates exclusively to the next. A server owner assigns accounts; an account owner assigns documents; a document owner assigns versions. At every stage, **one entity controls** the allocation beneath it:

> "Typically, the user will have no control over the node address he, she or it is assigned; but once assigned a User account, the user will have full control over its subdivision forevermore." (4/29)

### Modification Rights Are Sole

Only the owner may alter content at a position:

> "Every document has an owner, the person who created and stored it (or someone who arranged it to be created and stored, such as a publishing company)... Only the owner has a right to withdraw a document or change it." (2/29)

This is absolute. Nelson provides no mechanism for granting write access to another user. The editing operations (INSERT, DELETE, REARRANGE, COPY-into) all require ownership of the target document.

### What Ownership Does NOT Control

Ownership is exclusive over the position but **not** over what references it. Publication creates an irrevocable openness to incoming links:

> "Each author of a published work is relinquishing the right to control links into that work. This relinquishment must also be part of the publishing contract." (2/43)

And link ownership is determined by the link's home document, not by what it points to:

> "A link need not point anywhere in its home document. Its home document indicates who owns it, and not what it points to." (4/12)

So Alice exclusively owns her document. Bob exclusively owns his links *about* her document. Neither can touch the other's property.

### Collaboration Through Forking, Not Sharing

When someone wants to modify content they don't own, the system's answer is not "share access" but "fork your own version":

> "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate—without damaging the originals. This is done by inclusion links." (2/45)

The CREATENEWVERSION operation creates a new document (at your address, under your ownership) that transcludes from the original. You now own your version exclusively; the original owner still owns theirs exclusively. There is no shared editing.

### Private Document Access ≠ Shared Ownership

Nelson does mention that private documents can be accessed by "the owner and his or her associates" [2/42]. But this is **read access**, not ownership or modification rights. The designees can see the content; they cannot change it.

### Transfer, Not Sharing

Ownership can transfer — Nelson mentions "someone who has bought the document rights" [2/29] — but this transfers sole authority to a new single owner. There is no mechanism described for joint ownership.

### Summary

| Capability | Owner | Others |
|-----------|-------|--------|
| Modify content | Yes (exclusive) | No — fork instead |
| Allocate sub-positions | Yes (exclusive) | No |
| Withdraw document | Yes (with due process) | No |
| Read (if published) | Yes | Yes |
| Link to (if published) | Yes | Yes |
| Read (if private) | Yes | Designees only |

The address space is a tree of exclusive ownership. Every position has exactly one owner. Collaboration happens through the interplay of independently owned documents — transclusion, linking, versioning — not through shared control of any single position.
