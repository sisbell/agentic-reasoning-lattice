## Question 7 [nelson]

> When two addresses share a common prefix, what relationship must hold between the things they identify — must they belong to the same containing scope?

## Yes — shared prefix means shared containing scope

The tumbler system is explicitly a **tree flattened onto a line**. A common prefix means the two addresses descend from the same node in that tree — they belong to the same containing scope.

Nelson states this directly:

> "One digit can become several by a forking or branching process. This consists of creating successive new digits to the right; we call these 'under' the previous digit." [LM 4/20]

> "The owner of a given item controls the allocation of the numbers under it." [LM 4/20]

> "For instance, if there is an item 2, it can branch into several more items, each of which is a daughter item. Thus 2.1, 2.2, 2.3, 2.4... are successive items being placed under 2." [LM 4/20]

The tumbler line is not an arbitrary number line — it is a specific tree's depth-first linearization:

> "The tumbler line is an abstract representation of a particular tree." [LM 4/22]

> "The contents of the tumbler line are determined by the population of entities and relations on the tree it represents." [LM 4/22]

### What "same scope" means concretely

The four major fields define the containment hierarchy:

```
Node.0.User.0.Document.0.Element
```

If two addresses share prefix `1.2.0.3`, they are under the same user account (`3`) on the same server (`1.2`). If they share `1.2.0.3.0.7`, they are in the same document (`7`). The containment is structural — forking creates daughter items, and ownership flows downward:

> "A server node, or station, has ancestors and may have possible descendant nodes. An account, too, and a document, all have possible descendants." [LM 4/19]

> "The entire tumbler works like that: nodes can spin off nodes; accounts can spin off accounts; nodes can spin off accounts; and so on. Thus all numeration in the docuverse is compressed into a single mechanism." [LM 4/19]

This is why spans work as subtree selectors — a span covering a prefix captures everything beneath it:

> "A span in the tumbler line, represented by two tumblers, refers to a subtree of the entire docuverse." [LM 4/24]

And why ghost elements work — linking to an account address implicitly references all documents under it:

> "A link to or search of an account or node will find any of the documents under it." [LM 4/23]

### The important caveat: scope, not semantics

Shared prefix means shared **administrative scope** (same server, same account, same document), but NOT shared subject matter or semantic relationship:

> "Tumblers do not affect the user-level structure of the documents; they only provide a mapping mechanism, and impose no categorization and no structure on the contents of a document." [LM 4/17–4/18]

Two documents under the same account are owned by the same user. That is the only relationship the prefix guarantees. Nelson is explicit that tumblers are about *where things live* in the ownership tree, not *what they mean*.

### Summary

Shared prefix → same containing scope in the ownership/containment tree. This is not a convention but a structural invariant: the prefix IS the path from the root of the tree to the common ancestor. The relationship is containment and ownership, never semantic categorization.
