## Question 3 [nelson]

> Is ownership structurally encoded in the address itself, so that inspecting an address reveals its owner, or is ownership a separate association the system maintains?

## Ownership Is Structurally Encoded in the Address

Yes — ownership is encoded directly in the tumbler address. The User field is one of the four major fields of every tumbler:

```
Node.0.User.0.Document.0.Element
```

> "There are four major fields, each expandable indefinitely, with three major dividers between them. These fields are Server, User, Document and Contents." [LM 4/26]

Inspecting any address reveals the account that created it. The User field **is** the owner identifier — not a pointer to a separate ownership record.

## The Baptism Principle

Ownership flows from the address hierarchy itself through "baptism":

> "The basic principle is that of owned numbers. Numbers are owned by individuals or companies, and subnumbers under them are bestowed on other individuals and companies on whatever basis the owners choose. Whoever owns a specific node, account, document or version may in turn designate (respectively) new nodes, accounts, documents and versions, by forking their integers." [LM 4/17]

> "The owner of a given item controls the allocation of the numbers under it." [LM 4/20]

Once you have User account `1.3`, everything under `1.0.3.0.*` is yours. You fork documents beneath your account number. Those documents fork versions. The tree of ownership is the tree of addresses.

> "Typically, the user will have no control over the node address he, she or it is assigned; but once assigned a User account, the user will have full control over its subdivision forevermore." [LM 4/29]

## Links Follow the Same Rule

For links, ownership is determined by the link's home document — which is itself addressed under the creator's account:

> "A link need not point anywhere in its home document. Its home document indicates who owns it, and not what it points to." [LM 4/12]

You can link to anyone's content, but the link lives at **your** address. Inspecting the link's home address reveals who created it.

## No Separate Ownership Metadata

Nelson does not describe a separate ownership table or metadata association. The system doesn't even store explicit "account objects":

> "In the present implementation (XU.87.1), the only entities actually stored in tumbler-space are content bytes and links. While a number on the line may represent a document or an account, that doesn't mean there's an object stored for it." [LM 4/23]

Accounts are "ghost elements" — positions on the tumbler line with no stored object. Ownership is inherent in the address structure, not in a record that could be queried, modified, or corrupted independently.

## One Caveat: Transfer of Rights

Nelson mentions that a document owner may be "the rightful copyright holder, or someone who has bought the document rights" [LM 2/29]. This implies that legal ownership can transfer (as with any property). But the address remains permanent — the User field always reflects the **originating account**, not necessarily the current legal owner. How ownership transfer would be reflected in the system (a metalink? a contractual record?) is not specified.

NEED_RAW: [2/29-2/30] — to check whether Nelson says anything more about ownership transfer mechanics beyond the brief mention of "bought the document rights."

## Summary

Ownership is **structural, not associative**. The tumbler address encodes provenance permanently. There is no separate "owner" field to update, no metadata to strip, no table to corrupt. The address **is** the proof of origin.
