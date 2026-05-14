## Question 5 [theory]

> Was the fork mechanism (denial-as-fork at an ownership boundary) intended to produce content-bearing addresses for node-level principals, or is the node operator's role limited to account allocation with content creation occurring only at account level and below?

The node operator's role is limited to account allocation. Content creation happens only at the account level and below.

## Structural argument

A tumbler address has four fields separated by zero dividers: `Node.0.User.0.Document.0.Element`. Only the Element field holds bytes and links:

> "There are four major fields, each expandable indefinitely, with three major dividers between them. These fields are Server, User, Document and Contents." [LM 4/26]

Nodes and accounts are ghost elements — addressable positions in tumbler-space without stored representation:

> "In the present implementation (XU.87.1), the only entities actually stored in tumbler-space are content bytes and links. While a number on the line may represent a document or an account, that doesn't mean there's an object stored for it. What's stored is the contents—bytes and links." [LM 4/23]

There is no `Node.Element` form. To reach content, you must traverse `Node → User → Document → Element`.

## The division of authority

I'm explicit about where the node operator's role ends and the user's begins:

> "Typically, the user will have no control over the node address he, she or it is assigned; but once assigned a User account, the user will have full control over its subdivision forevermore." [LM 4/29]

The node operator's authority is exactly: hand out user accounts. Once a user has an account, they own its entire subtree — and that's where documents and versions get baptized:

> "The owner of a given item controls the allocation of the numbers under it." [LM 4/20]

## On "denial-as-fork"

That term is from Roger Gregory's BERT mechanism — his implementation of the session layer that I left undesigned. What I did specify is the principle Roger was implementing: writing always succeeds, but not always to the same document.

> "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate—without damaging the originals." [LM 2/45]

When that principle is invoked at an ownership boundary, the result is a new version owned by the writer:

> "This creates a new document with the contents of document <doc id>. It returns the id of the new document. The new document's id will indicate its ancestry." [LM 4/66]

The new document is in the *writer's* user/document subspace, not at the node level. The fork moves down the address — it does not jump to a sibling node.

## Summary

A node operator wearing only the node-operator hat does not create content; they allocate accounts. If a node operator also wants to publish, they hold a user account on their own node like any other user, and their content lives at `their-node.their-account.their-document.elements` — never at a node-level address.

The fork mechanism cannot produce content-bearing addresses for node-level principals because there is no such thing as a node-level content address. The four-field structure forbids it.
