## Question 4 [nelson]

> Does a node define an ownership boundary — is the node the authority over the accounts and documents it contains?

# Does a Node Define an Ownership Boundary?

**Short answer: A node defines an *allocation* boundary, not a *content authority* boundary.**

The node owner controls who gets accounts — but once an account is assigned, the account holder has permanent, irrevocable authority over their subtree. The node operator is a custodian, not an owner of the content it hosts.

## Allocation Authority: Yes

The node owner controls the creation of accounts beneath it. This follows from the general baptism principle:

> "The owner of a given item controls the allocation of the numbers under it." (4/20)

> "Whoever owns a specific node, account, document or version may in turn designate (respectively) new nodes, accounts, documents and versions, by forking their integers." (4/17)

The tumbler hierarchy is Node → Account → Document → Element. The node owner baptizes accounts; account owners baptize documents; and so on downward. The node is the root of a local subtree, and its owner decides who enters that subtree.

## Content Authority: No

Once an account is allocated, the account holder owns their entire subtree permanently. The node operator has no authority over the content within:

> "Typically, the user will have no control over the node address he, she or it is assigned; but once assigned a User account, the user will have full control over its subdivision forevermore." (4/29)

That "forevermore" is significant. The grant is irrevocable. And document ownership is absolute:

> "Every document has an owner, the person who created and stored it... Only the owner has a right to withdraw a document or change it." (2/29)

The node operator cannot modify, withdraw, or control documents belonging to account holders on their node.

## The Node Operator as Custodian

The Storage Vendor contract (Chapter 5) makes the custodial role explicit. The node operator must preserve and protect, but may not exercise authority over content:

> "Storage Vendor agrees to engage in best efforts for the preservation and privacy of all customer material, and not to breach the confidence of any customer, examining customers' stored materials only as required for the orderly maintenance of the system; and not to spy for any private persons, corporations or agencies of any government upon the private materials of any customers, nor discuss such private materials with anyone." (5/14-5/15)

And if the vendor goes away, customer content must be migrated, not lost:

> "Upon notice of cancellation, Storage Vendor will arrange for the orderly transition of all customer-stored materials to other Xanadu locations." (5/16)

## The Interoperation Obligation

The node is also not a silo. Vendors must serve content to users on other nodes:

> "Storage Vendor agrees to honor requests for material from customers connected to servers operated by other Xanadu-licensed storage vendors." (5/14)

This means the node boundary is invisible to users. Content flows across nodes transparently.

## Summary

| Role | Controls | Does NOT Control |
|------|----------|-----------------|
| **Node owner** | Which accounts exist on the node (baptism) | Content within those accounts |
| **Account owner** | All documents and sub-accounts beneath them, "forevermore" | Their node address assignment |
| **Document owner** | All content and versions within their document | Links others make to their published work |

The node is an administrative and physical hosting boundary. It is not an authority boundary over content. The deliberate separation — allocation power at the node level, content authority at the account level, custodial obligation binding the operator — prevents the node from becoming a gatekeeper. This serves Nelson's libertarian principle: the infrastructure serves the users, not the other way around.
