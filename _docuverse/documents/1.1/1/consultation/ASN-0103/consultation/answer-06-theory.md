## Question 6 [theory]

> What ownership or authorship guarantee binds a new document to the account under which it was created?

## Ownership Binding Through the Tumbler Address

The guarantee is **structural**: when a document is created, its ownership by the creating account is encoded directly into the document's permanent tumbler address. Ownership is not metadata attached to the document—it *is* the address.

### The Address Encodes the Owner

Every Istream address has the form:

```
Node.0.User.0.Document.0.Element
```

The **User field** identifies the owning account, and the **Document field** is forked *under* that account by its owner. From `i-space-addresses.md`:

> "There are four major fields, each expandable indefinitely, with three major dividers between them. These fields are Server, User, Document and Contents." (4/26)

Because the document number is baptized beneath the account number, the binding is permanent and unforgeable—you cannot create a document except under an account you own.

### The "Baptism" / Owned-Numbers Principle

The mechanism that binds creation to ownership is what Nelson calls baptism. From `tumblers.md`:

> "The basic principle is that of owned numbers. Numbers are owned by individuals or companies, and subnumbers under them are bestowed on other individuals and companies on whatever basis the owners choose. Whoever owns a specific node, account, document or version may in turn designate (respectively) new nodes, accounts, documents and versions, by forking their integers. We often call this the 'baptism' of new numbers." (4/17)

And from `forking.md`:

> "The owner of a given item controls the allocation of the numbers under it." (4/20)

So a new document at `1.3.27` can only be created by whoever owns account `1.3`. The account-to-document binding is the act of creation itself.

### Ownership Is Absolute

Once bound, ownership confers exclusive control. From `documents.md`:

> "Every document has an owner, the person who created and stored it (or someone who arranged it to be created and stored, such as a publishing company). The rightful copyright holder, or someone who has bought the document rights... Only the owner has a right to withdraw a document or change it." (2/29)

This guarantee extends to links: a link's *home document* determines who owns it, regardless of what it points to. From `documents.md`:

> "A link need not point anywhere in its home document. Its home document indicates who owns it, and not what it points to." (4/12)

### Permanence of the Binding

The account-control guarantee, once granted, lasts forever. From `session-model.md` / `i-space-addresses.md`:

> "Typically, the user will have no control over the node address he, she or it is assigned; but once assigned a User account, the user will have full control over its subdivision forevermore." (4/29)

### Summary

| Guarantee | Source |
|-----------|--------|
| Document number is forked *under* the account that created it | "baptism" of owned numbers, 4/17, 4/20 |
| Owner alone may change or withdraw the document | 2/29 |
| Ownership is encoded in the User field of the address, not removable metadata | 4/26, 4/29 |
| Control over an account's subspace is permanent | 4/29 |

The binding is therefore not a policy layered on top—it is the addressing system itself. A document exists *as* a number forked beneath its owning account, and that parentage is what proves and enforces ownership.
