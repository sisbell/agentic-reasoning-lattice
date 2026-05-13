## Question 2 [theory]

> Does Xanadu's design require that a link's home document be an already-created document (with an owner), or is it permissible for a link to be created under a structurally well-formed document-level prefix that has not been allocated as a document in the system?

# Home Documents Must Be Allocated

A link's home document must be an already-allocated document with an owner. It is **not** permissible to home a link under a merely well-formed but unallocated document-level prefix. The architecture is asymmetric: link *targets* can point to ghost elements, but link *homes* cannot be ghosts.

## Why the home requires an owner

Links are owned objects, and the ownership flows from the home document:

> "A Xanadu link is a connective unit, a package of connecting or marking information. It is owned by a user." [LM 4/41]

> "A link need not point anywhere in its home document. Its home document indicates who owns it, and not what it points to." [LM 4/12]

Documents themselves require owners:

> "Every document has an owner, the person who created and stored it (or someone who arranged it to be created and stored, such as a publishing company)." [LM 2/29]

Sub-addresses within a document — including the `0.2.N` link subspace — are controlled by that document's owner:

> "The owner of a given item controls the allocation of the numbers under it." [LM 4/20]

So a link at `N.0.U.0.D.V.0.2.N` presupposes that `D` has been baptized by `U` and that `U`'s owner has allocated link-instance `N` under version `V`. With no allocated `D`, there is no owner to allocate the `2.x` subspace, and the link would have no determinable owner — contradicting the requirement that every link be owned.

The MAKELINK protocol command reflects this directly:

> "MAKELINK… This creates a link in document `<doc id>` from `<from set>` to `<to set>` connected to `<three set>`. It returns the id of the link made." [LM 4/68]

> "The document must be specified because that determines the actual residence of the link — since a document may contain a link between two other documents." [LM 4/63]

The doc id is the *residence* of the link, not just a pointer.

## The asymmetry with endsets

Ghost elements are explicitly permitted as link *targets* — but Nelson scopes this carefully to nodes, accounts, and type endsets:

> "While servers, accounts and documents logically occupy positions on the developing tumbler line, no specific element need be stored in tumbler-space to correspond to them. Hence we may call them ghost elements." [LM 4/23]

> "It is possible to link to a node, or an account, even though there is nothing stored in the docuverse corresponding to them." [LM 4/23]

> "Indeed, there is no need for the presence of elements at the addresses specified. Link types may be ghost elements." [LM 4/45]

Note what these passages permit: endsets (to-set, type) pointing into ghost regions. Nelson never extends ghost-status to a link's home. The reason is structural: homes carry ownership and allocation authority; targets do not.

## Caveat on "document existence"

There is a subtlety worth being precise about. Nelson notes that in XU.87.1 documents are not stored as separate objects:

> "In the present implementation (XU.87.1), the only entities actually stored in tumbler-space are content bytes and links… What's stored is the contents — bytes and links." [LM 4/23]

So a document being "allocated" does not mean a Document object sits in storage — it means the document address has been baptized by its parent (the user account) and now has an owner. That baptism is what licenses subsequent allocations within it (bytes at `0.1.*`, links at `0.2.*`). Without baptism, the `2.x` subspace is not yet ownable, and no conforming link can reside there.

## Summary

| Question | Answer | Source |
|---|---|---|
| Can a link's **target** be a ghost (unallocated) position? | Yes | LM 4/23, 4/45 |
| Can a link's **home document** be an unallocated prefix? | No — homes determine ownership, which requires an allocated, owned document | LM 4/12, 4/20, 4/41, 4/63 |

The design intent is that every link is traceable to a responsible owner. That guarantee is what permits free linking into others' published work without compromising who is accountable for the link itself. A homeless link — at a prefix no one has baptized — would break that contract.
