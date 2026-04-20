## Question 1 [nelson]

> What defines the identity of a node — how is each node permanently distinguished from every other node in the docuverse?

## What Defines the Identity of a Node

A node's identity is its **tumbler address** — specifically, its unique position in the first field (the Server/Node field) of the tumbler addressing scheme. Nothing else. No name, no IP address, no description. The number IS the node.

### The Address Is the Identity

Every tumbler address has four major fields:

```
Node.0.User.0.Document.0.Element
```

The first field — the Node field — identifies which server node we are talking about. All nodes descend from digit 1, which represents the entire docuverse:

> "The server address always begins with the digit 1, since all other servers are descended from it. This may seem an unnecessary redundancy, but it permits referring to the entire docuverse by '1' on the first position." [LM 4/28]

So node `1.2` is the second node forked from the original. Node `1.2.3` is the third node forked under node `1.2`. Each position on this tree is unique and permanent.

### Baptism: How Nodes Get Their Numbers

A node's identity is created through **forking**, which I call "baptism":

> "A server node, or station, has ancestors and may have possible descendant nodes." [LM 4/19]

> "The owner of a given item controls the allocation of the numbers under it." [LM 4/20]

> "One digit can become several by a forking or branching process. This consists of creating successive new digits to the right; we call these 'under' the previous digit." [LM 4/20]

Whoever owns node `1.2` can baptize nodes `1.2.1`, `1.2.2`, `1.2.3` beneath it. No coordination with any other node is required. No central registry. The owner designates, and the number is born.

### Permanence: The Number Never Changes

> "New items may be continually inserted in tumbler-space while the other addresses remain valid. This means that any address of any document in an ever-growing network may be specified by a permanent tumbler address." [LM 4/19]

Once a node is baptized as `1.2.3`, it is `1.2.3` forever. The network can grow without limit — new nodes forking from existing nodes — and no existing address is ever disturbed.

### A Node Is a Ghost Element

Here is the subtlety that many people miss. A node is not a stored object. It is a **conceptual position** on the tumbler line:

> "While servers, accounts and documents logically occupy positions on the developing tumbler line, no specific element need be stored in tumbler-space to correspond to them. Hence we may call them ghost elements." [LM 4/23]

> "However, these elements are virtually present in tumbler-space, since links may be made to them which embrace all the contents below them." [LM 4/23]

The node's identity exists in the addressing scheme itself. You can link to node `1.2.3` — meaning all accounts, all documents, everything beneath that address — even though no "node object" is stored anywhere. The identity is the position, not a record.

### The Docuverse Is One Big Forking Tree

> "The entire tumbler works like that: nodes can spin off nodes; accounts can spin off accounts; nodes can spin off accounts; and so on. Thus all numeration in the docuverse is compressed into a single mechanism." [LM 4/19]

> "So the docuverse is all really one big forking document." [LM 4/18]

A node is distinguished from every other node by its unique path through this tree. Node `1.2` and node `1.3` are siblings — both forked under `1`, but permanently distinct. Node `1.2.4` is a descendant of `1.2` and could never be confused with `1.3.4`, even though both end in `.4`, because the ancestry is encoded in the full address.

### What a Node Identity Does NOT Include

The tumbler address says nothing about:
- The node's physical location
- What hardware it runs on
- What content it stores
- When it was created (time is kept track of separately — [LM 4/18])
- Any semantic category or classification

> "Tumblers do not affect the user-level structure of the documents; they only provide a mapping mechanism, and impose no categorization and no structure on the contents of a document." [LM 4/17-4/18]

The identity is purely positional — where this node sits in the ever-growing tree of the docuverse.

### Summary

A node is permanently distinguished by its **tumbler address in the Node field** — a unique, permanent, hierarchical number assigned through baptism by its parent node's owner. It requires no stored object (ghost element), no central coordination, and no metadata. The number is the identity, assigned once, valid forever.
