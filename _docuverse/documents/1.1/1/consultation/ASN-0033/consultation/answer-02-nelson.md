## Question 2 [nelson]

> What must be true of the global address space when a new node enters the docuverse — must the node receive a unique, permanent portion of that space?

## Yes — absolutely and by design.

The entire tumbler system exists precisely to solve this problem. When a new node enters the docuverse, it must be **baptized** — given a unique, permanent position in the address tree from which all its future addresses will descend.

### The Mechanism: Owned Numbers and Baptism

The tumbler addressing system is built on a principle I call **owned numbers**:

> "The basic principle is that of owned numbers. Numbers are owned by individuals or companies, and subnumbers under them are bestowed on other individuals and companies on whatever basis the owners choose. Whoever owns a specific node, account, document or version may in turn designate (respectively) new nodes, accounts, documents and versions, by forking their integers. We often call this the 'baptism' of new numbers." [LM 4/17]

A new node receives its address from its parent node. If the existing network has node `1.2`, a new descendant node might be baptized as `1.2.3`. That address — `1.2.3` — becomes permanently reserved. Every account, document, version, and byte created under that node will carry `1.2.3` as the prefix of its address.

> "A server node, or station, has ancestors and may have possible descendant nodes. An account, too, and a document, all have possible descendants." [LM 4/19]

> "The entire tumbler works like that: nodes can spin off nodes; accounts can spin off accounts; nodes can spin off accounts; and so on. Thus all numeration in the docuverse is compressed into a single mechanism." [LM 4/19]

### Why Permanence Is Non-Negotiable

The guarantee is explicit:

> "New items may be continually inserted in tumbler-space while the other addresses remain valid. This means that any address of any document in an ever-growing network may be specified by a permanent tumbler address." [LM 4/19]

Once a node is baptized at position `1.2.3`, that position is occupied forever. No future node can take that address. No reorganization can move it. The address encodes the node's place in the genealogy of the network — and that genealogy is permanent.

### The Tree Structure of the Address Space

The node address is the **first field** of every tumbler in the system. The full I-space address has the form:

```
Node.0.User.0.Document.0.Element
```

> "The server address always begins with the digit 1, since all other servers are descended from it. This may seem an unnecessary redundancy, but it permits referring to the entire docuverse by '1' on the first position." [LM 4/28]

So the entire docuverse is rooted at `1`. Every node is a descendant of `1`. The address `1` refers to *everything*. A new node at `1.2.3` gets not just an address but an entire **subtree** — an infinite space of possible accounts, documents, versions, and bytes beneath it.

### The Node Need Not "Exist" as a Stored Object

Here is a subtle but important point. The node address reserves a position in the address space, but the system need not store anything to represent the node itself:

> "While servers, accounts and documents logically occupy positions on the developing tumbler line, no specific element need be stored in tumbler-space to correspond to them. Hence we may call them ghost elements." [LM 4/23]

> "However, these elements are virtually present in tumbler-space, since links may be made to them which embrace all the contents below them." [LM 4/23]

The node is a **conceptual position** — a ghost element. What gets stored is the content beneath it: bytes and links. But the position is real, permanent, and owned.

### No Central Authority Required

This is the beauty of the design. The node's parent baptizes it. No global registry is consulted:

> "Typically, the user will have no control over the node address he, she or it is assigned; but once assigned a User account, the user will have full control over its subdivision forevermore." [LM 4/29]

The parent node simply forks a new digit. Node `1.2` creates `1.2.1`, then `1.2.2`, then `1.2.3` — each a new server with its own permanent subtree. The forking is local, the effect is global.

> "One digit can become several by a forking or branching process. This consists of creating successive new digits to the right; we call these 'under' the previous digit." [LM 4/20]

### So the Docuverse Is One Big Forking Document

> "So the docuverse is all really one big forking document." [LM 4/18]

When a new node enters, it receives a permanent branch of this ever-growing tree. That branch is its portion of the universal address space — unique, permanent, and infinitely subdivisible. The node owns it, can delegate sub-addresses within it, and nothing that happens elsewhere in the tree can ever disturb it.

That is the guarantee. That is what makes the docuverse a single unified space that grows without bound while every address remains valid forever.
