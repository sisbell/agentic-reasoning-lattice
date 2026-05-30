## Question 6 [theory]

> Is a node-level operator ever intended to place or modify content directly, or is its role strictly confined to allocating accounts (so the node-level fork-to-content branch is genuinely out of scope)?

Short answer: A node-level operator's role in the ownership hierarchy is to allocate accounts (and sub-nodes), not to place or modify content directly. The node→content branch is genuinely out of scope, though Nelson states this structurally rather than as an explicit prohibition.

## The forking enumeration omits node→document

Nelson's own list of what forks into what is telling:

> "The entire tumbler works like that: nodes can spin off nodes; accounts can spin off accounts; nodes can spin off accounts; and so on. Thus all numeration in the docuverse is compressed into a single mechanism." (4/19)

The enumerated branches are **node→node**, **account→account**, and **node→account**. There is no "node→document." The parallel statement in `prompts`/curated `tumblers` reinforces the level-respecting pattern:

> "Whoever owns a specific node, account, document or version may in turn designate (respectively) new nodes, accounts, documents and versions, by forking their integers. We often call this the 'baptism' of new numbers." (4/17)

Each owner baptizes the next level down: a node baptizes accounts, an account baptizes documents, a document baptizes versions.

## The address structure makes content unreachable at the node level

Content always carries a full four-field I-address (see `i-space-addresses`):

```
Node.0.User.0.Document.0.Element
```

> "There are four major fields, each expandable indefinitely, with three major dividers between them. These fields are Server, User, Document and Contents." (4/26)

The Element (content/bytes) field sits *under* a Document, which sits *under* a User. There is no address form in which content (or a link) hangs directly off a Node without an intervening User and Document. So "node places content directly" has no representable address — content is structurally confined to documents under accounts.

This is corroborated by what is actually stored:

> "In the present implementation (XU.87.1), the only entities actually stored in tumbler-space are content bytes and links. While a number on the line may represent a document or an account, that doesn't mean there's an object stored for it." (4/23)

Bytes and links are the only stored content, and they live at element positions beneath documents.

## The node assigns accounts; the account controls everything below

The division of labor is explicit in the curated `session-model` material:

> "Typically, the user will have no control over the node address he, she or it is assigned; but once assigned a User account, the user will have full control over its subdivision forevermore." (4/29)

The node's relationship to a user is to *assign the account*. From there, document and version creation is the account holder's domain (CREATENEWDOCUMENT, CREATENEWVERSION). Ownership of content is always by account:

> "Every document has an owner, the person who created and stored it." (2/29)

## Operator vs. owner

Note one possible source of confusion: the operator of a node (the Storage Vendor) physically *stores* content on the machine, but that is storage infrastructure, not authorship or ownership. Ownership is encoded in the User field, not the Node field. The Storage Vendor running the hardware does not thereby place content at the node level — the content still belongs to, and is addressed through, an account.

## Conclusion

Confining the node-level operator to account (and sub-node) allocation is faithful to Nelson's design. Treating the node-level fork-to-content branch as out of scope is correct: content placement requires a Node.User.Document.Element address, so it must pass through an account and a document.

One caveat for precision: Nelson never writes an explicit sentence saying "a node may not own content directly." The conclusion rests on (a) the forking enumeration that lists node→node/account→account/node→account but not node→document, and (b) the mandatory four-field content address. Both are verified in the curated sources, but the prohibition itself is inferred from structure rather than stated as a rule.
