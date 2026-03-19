## Question 6 [nelson]

> Must the set of all nodes carry a total ordering that reflects the sequence in which they entered the docuverse?

## No. The tumbler line carries a total ordering, but it reflects tree structure, not temporal sequence.

### What the tumbler line does order

All tumblers — including node addresses — fall on a single totally ordered line. This is a depth-first traversal of the forking tree:

> "In a sense the tumbler line is like the real line, i.e., the line of integers and all the numbers in between. But the tumbler line is a different kind of abstraction from the real line. The real line is the same under all circumstances. The tumbler line is an abstract representation of a particular tree." [LM 4/22]

> "The contents of the tumbler line are determined by the population of entities and relations on the tree it represents. Thus the tumbler line is not definite in the same way as the real line; the tumbler line is a flat mapping of a particular tree, finite but unlimited." [LM 4/22]

So yes, every node has a definite position on a totally ordered line — but that ordering encodes **parentage and sibling position**, not time of arrival.

### Sibling order does reflect creation sequence

Under a given parent, children are numbered sequentially as they are created:

> "One digit can become several by a forking or branching process. This consists of creating successive new digits to the right; we call these 'under' the previous digit." [LM 4/20]

> "For instance, if there is an item 2, it can branch into several more items, each of which is a daughter item. Thus 2.1, 2.2, 2.3, 2.4... are successive items being placed under 2." [LM 4/20]

Node 1.1 was created before node 1.2 under the root. That much is encoded.

### But the total ordering does not reflect global temporal sequence

The depth-first traversal puts all descendants of node 1.1 before node 1.2 on the tumbler line:

```
1, 1.1, 1.1.1, 1.1.2, ..., 1.2, 1.2.1, ...
```

Node 1.2 might have been created years before node 1.1.1, yet 1.1.1 precedes 1.2 on the tumbler line. The ordering reflects the tree, not the calendar.

### Time is explicitly excluded from the tumbler

Nelson is direct about this:

> "Note that 'time' is not included in the tumbler. Time is kept track of separately." [LM 4/18]

Time is metadata maintained alongside the address system, not encoded in it. You can ask "when was this node created?" but the answer comes from a separate mechanism, not from the address itself.

### Why this matters architecturally

The tumbler's job is **permanent addressing in a decentralized system**, not temporal ordering. The design priorities are:

1. **Stability** — existing addresses never change when new nodes arrive
2. **Decentralization** — owners baptize sub-addresses without coordination
3. **Span efficiency** — contiguous subtrees map to contiguous ranges

A global temporal ordering would require either a central sequencer (violating decentralization) or consensus among nodes (violating simplicity). Nelson chose tree-structural ordering instead, which requires only local coordination: the parent assigns the next sibling number.

### Summary

| Scope | Does ordering reflect creation sequence? |
|-------|----------------------------------------|
| Among siblings of one parent | **Yes** — sequential baptism |
| Across different branches | **No** — depth-first tree order, not temporal |
| Globally across all nodes | **No** — time is kept separately |

The nodes carry a total ordering, but it is the depth-first linearization of a forking tree — not a chronicle of when they joined the docuverse.
