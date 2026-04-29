## Question 7 [nelson]

> Must node identities be ordered — does the sequence in which nodes enter the docuverse carry permanent meaning in the address space?

# Must Node Identities Be Ordered?

**Yes.** The sequence in which nodes enter the docuverse is permanently encoded in their tumbler addresses and carries lasting structural significance—though not semantic significance.

## The Mechanism: Sequential Forking

Nodes are created by forking under their parent. The root of the docuverse is node 1. When node 1 spawns child nodes, they receive sequential addresses: 1.1, 1.2, 1.3, and so on. This sequence is permanent.

> "One digit can become several by a forking or branching process. This consists of creating successive new digits to the right; we call these 'under' the previous digit." (4/20)

> "For instance, if there is an item 2, it can branch into several more items, each of which is a daughter item. Thus 2.1, 2.2, 2.3, 2.4... are successive items being placed under 2." (4/20)

> "The owner of a given item controls the allocation of the numbers under it." (4/20)

The parent node controls baptism of child nodes. Node 1.3 was necessarily baptized *after* 1.2—the sequential integers reflect creation order among siblings.

## The Ordering Is Permanent

Once a node receives its address, that address never changes and its position relative to all other addresses is fixed forever:

> "New items may be continually inserted in tumbler-space while the other addresses remain valid. This means that any address of any document in an ever-growing network may be specified by a permanent tumbler address." (4/19)

You cannot retroactively insert a node "between" 1.2 and 1.3. However, you *can* create children under 1.2 (e.g., 1.2.1, 1.2.2), which appear between 1.2 and 1.3 on the tumbler line due to depth-first ordering.

## The Tumbler Line: Total Order via Tree Mapping

All tumblers—including node addresses—map to a single ordered line:

> "In a sense the tumbler line is like the real line, i.e., the line of integers and all the numbers in between. But the tumbler line is a different kind of abstraction from the real line. The real line is the same under all circumstances. The tumbler line is an abstract representation of a particular tree." (4/22)

> "The contents of the tumbler line are determined by the population of entities and relations on the tree it represents. Thus the tumbler line is not definite in the same way as the real line; the tumbler line is a flat mapping of a particular tree, finite but unlimited." (4/22)

This means node ordering is not just sibling-sequential—it's a *total order* on all nodes via the depth-first tree walk. Node 1.2.5 comes after 1.2.4 but before 1.3 on the tumbler line.

## What the Ordering Means (and Doesn't Mean)

The ordering carries **operational significance** but **no semantic significance**:

**Operationally significant:**
- Spans work because ordering is stable. You can address "everything on nodes 1.2 through 1.5" as a single span.
- A span containing node 1.2 implicitly contains all of 1.2's descendants (1.2.1, 1.2.2, ...) because they fall within the span on the tumbler line.
- Ghost elements are addressable at node positions even without stored content: "A link to or search of an account or node will find any of the documents under it." (4/23)

**Semantically neutral:**
- The address says nothing about the node's content, purpose, or importance.
- "Tumblers do not affect the user-level structure of the documents; they only provide a mapping mechanism, and impose no categorization and no structure on the contents of a document." (4/17–4/18)
- Time is explicitly excluded: "Note that 'time' is not included in the tumbler. Time is kept track of separately." (4/18)

## The Root Convention

All nodes descend from a single root:

> "The server address always begins with the digit 1, since all other servers are descended from it. This may seem an unnecessary redundancy, but it permits referring to the entire docuverse by '1' on the first position." (4/28)

This means the ordering begins from a universal anchor point. The "1" is not just the first node—it is the address of the entire docuverse, enabling a span starting at "1" to cover everything.

## Summary

Node sequence carries permanent meaning in three ways:

1. **Creation order among siblings** — node 1.3 was baptized after 1.2; this is immutable
2. **Position on the tumbler line** — determines span coverage and range queries
3. **Hierarchical descent** — a node's children fall within its span, enabling hierarchical addressing

But the sequence carries *no* semantic, temporal, or qualitative meaning. It is a coordinate system, not a ranking.
