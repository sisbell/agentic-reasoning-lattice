## Question 3 [nelson]

> Must every piece of content in the docuverse belong to exactly one node, or can content exist independent of any node?

## Every piece of content belongs to exactly one node — by address

The tumbler address structure makes this unambiguous. Every I-space address has the form:

```
Node.0.User.0.Document.0.Element
```

> "There are four major fields, each expandable indefinitely, with three major dividers between them. These fields are Server, User, Document and Contents." [LM 4/26]

The Node field is mandatory and always present:

> "The server address always begins with the digit 1, since all other servers are descended from it. This may seem an unnecessary redundancy, but it permits referring to the entire docuverse by '1' on the first position." [LM 4/28]

Since content bytes are the things actually stored in tumbler-space ("In the present implementation (XU.87.1), the only entities actually stored in tumbler-space are content bytes and links" [LM 4/23]), and every tumbler address encodes a node, every piece of content is assigned to exactly one node as part of its permanent identity.

## But physical residence is a different matter

The I-address encodes *origin*, not *current physical location*. Through BEBE, content replicates freely across nodes:

> "The contents can slosh back and forth dynamically." [LM 4/72]

> "Each server contains a map and a subset of the whole — a microcosm that shrinks and grows." [LM 4/71]

Content moves between servers for four reasons (from 4/71):
1. More rapid access to final material
2. More rapid access to needed index material
3. Rebalance in keeping with demand
4. Redundancy and backup

So a byte with I-address `1.3.0.7.0.42.0.1.500` permanently *belongs to* node 1.3, but may physically reside on nodes 1.3, 1.5, and 1.8 simultaneously through replication.

## Content cannot exist independent of a node

Three reasons:

**Structural:** The address format requires a node field. There is no "nodeless" tumbler. The node is as fundamental to the address as the document or element fields.

**Ownership chain:** Forking follows an ownership hierarchy — nodes own accounts, accounts own documents, documents own content. Content without a node has no place in this chain.

> "The owner of a given item controls the allocation of the numbers under it." [LM 4/20]

**Docuverse definition:** The docuverse *is* the occupied tumbler-space, and tumbler-space is rooted at node 1:

> "The docuverse is the occupied tumbler-space — as occupied by conceptually assigned positions, even if nothing represents them in storage." [LM 4/23]

> "So the docuverse is all really one big forking document." [LM 4/18]

## Summary

| Question | Answer |
|----------|--------|
| Must content belong to exactly one node? | **Yes** — by permanent I-address |
| Can content physically reside on multiple nodes? | **Yes** — through BEBE replication |
| Can content exist independent of any node? | **No** — the address structure forbids it |

The node assignment is *identity*, not *location*. It answers "where was this born?" not "where is this stored right now?"
