## Question 3 [nelson]

> Can an owner delegate partial rights over a portion of their address space to another party without transferring ownership itself?

## Delegation of Partial Rights in Xanadu

Nelson describes two mechanisms that touch on this question, but neither constitutes a fully specified partial-rights delegation model. The answer is: **partially, through subdivision and bestowment — but not through granular permission delegation over existing space.**

### What Nelson DOES Specify

**1. Baptism: Subdivision and Bestowment**

The primary mechanism is forking — the owner creates sub-addresses and bestows them on others:

> "Numbers are owned by individuals or companies, and subnumbers under them are bestowed on other individuals and companies on whatever basis the owners choose." [LM 4/17]

> "The owner of a given item controls the allocation of the numbers under it." [LM 4/20]

> "Typically, the user will have no control over the node address he, she or it is assigned; but once assigned a User account, the user will have full control over its subdivision forevermore." [LM 4/29]

This is ownership **creation and transfer**, not delegation of partial rights. When you bestow sub-address 1.3.7 on someone, they now **own** 1.3.7 and everything under it. You retain ownership of 1.3 but not of 1.3.7. The phrase "on whatever basis the owners choose" hints at flexibility in the terms of bestowment, but Nelson does not elaborate on what those terms might be.

**2. Designees: Access to Private Documents**

Nelson mentions that private documents can be shared with "associates" or "designees":

> "A private document may be read and linked-to only by the owner and his or her associates." [LM 2/42]

This implies some ability to grant read access without transferring ownership. But the mechanism is unspecified — there are no access control lists, no per-user permission grants, no role definitions.

### What Nelson Does NOT Specify

- **Granular permission delegation** — There is no mechanism for "you may modify bytes 100-200 of my document but not the rest"
- **Read-only vs. modify access** — The model is binary: you own it (full control) or you don't (no modification rights)
- **Revocable delegation** — No mechanism for granting and later revoking partial rights
- **Access control lists** — Only three access levels exist: owner, designees (unspecified mechanism), everyone

### The Ownership Model Is Absolute

Nelson's ownership principle is stark:

> "Every document has an owner... Only the owner has a right to withdraw a document or change it." [LM 2/29]

There is no concept of "co-editors," "collaborators with write access," or "administrators with partial control." If you want someone to modify content, the Xanadu pattern is: they create their **own version** (via `CREATENEWVERSION`) or their own **derivative document** (via transclusion with modifications). They never modify your document — they fork from it.

### The Architectural Consequence

This absoluteness is deliberate. It aligns with Nelson's principle that **writing always succeeds** — if you cannot modify someone else's document, you create a version. Denial is a fork, not an error. The system never needs partial permissions because the response to "you can't edit this" is always "then make your own."

The forking mechanism effectively replaces permission delegation: instead of granting someone partial rights over your space, you subdivide your space and grant them full ownership of the subdivision. The hierarchy of the tumbler address preserves the provenance (1.3.7 is visibly "under" 1.3), but the ownership is complete.

### Summary

| Mechanism | What It Does | Is It Partial Delegation? |
|-----------|-------------|--------------------------|
| Baptism/Forking | Create sub-address, bestow on another | No — ownership transfer, not delegation |
| Designees | Grant access to private docs | Partially — mentioned but unspecified |
| Versioning | Others create their own versions | No — independent ownership, not delegation |

Nelson's design favors **ownership clarity over permission complexity**. Rather than a rich permission model, the system provides absolute ownership plus the ability to subdivide and bestow. The philosophical stance is that literature works through independent ownership and interconnection (via links and transclusion), not through shared control over the same space.

NEED_RAW: [2/29-2/31, 4/17-4/20] — to verify whether Nelson says anything more about the terms of bestowment or the mechanism for designating "associates" that the curated sources may not fully capture.
