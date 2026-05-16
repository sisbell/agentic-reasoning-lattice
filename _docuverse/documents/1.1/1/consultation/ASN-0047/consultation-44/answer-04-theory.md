## Question 4 [theory]

> Does the design contemplate creation of additional root nodes (server nodes) after system initialization, or is the bootstrap node n₀ the unique root node fixed at system creation, with all subsequent entity creation occurring strictly beneath it?

# Answer

The design contemplates both: the bootstrap node is the unique root, AND additional server nodes are created after initialization — but always as descendants beneath the root through forking, never as new roots.

## The Root Is Fixed at "1"

Nelson is explicit that server "1" is the canonical root from which everything else descends:

> "The server address always begins with the digit 1, since all other servers are descended from it. This may seem an unnecessary redundancy, but it permits referring to the entire docuverse by '1' on the first position." [LM 4/28]

> "So the docuverse is all really one big forking document." [LM 4/18]

## New Server Nodes Are Created, But Strictly Beneath Existing Nodes

Server nodes can have descendants — new servers fork from existing servers via the same baptism mechanism that creates accounts, documents, and versions:

> "A server node, or station, has ancestors and may have possible descendant nodes. An account, too, and a document, all have possible descendants." [LM 4/19]

> "The entire tumbler works like that: nodes can spin off nodes; accounts can spin off accounts; nodes can spin off accounts; and so on. Thus all numeration in the docuverse is compressed into a single mechanism." [LM 4/19]

> "Whoever owns a specific node, account, document or version may in turn designate (respectively) new nodes, accounts, documents and versions, by forking their integers. We often call this the 'baptism' of new numbers." [LM 4/17]

## The Architectural Consequence

Because every server has the form `1.x.y.z…` (descended from root "1"), there is exactly one root node. New servers are placed under existing servers by the owner of that parent server — meaning the address space is a single tree with a single root, and growth occurs only by extending branches downward. This is what enables the "1" prefix to address the entire docuverse: there is no second root to disambiguate from.
