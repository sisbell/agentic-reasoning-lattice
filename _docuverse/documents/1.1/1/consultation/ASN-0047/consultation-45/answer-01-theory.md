## Question 1 [theory]

> In Nelson's tumbler design, is a node identity a single top-level component, or may a node address carry multiple components at the top level?

Looking at the curated sources on tumblers, addressing, and forking, the answer is clear.

## Answer

A node identity is **not** required to be a single top-level component. A node address may carry **multiple components** because nodes themselves fork into descendant nodes, and each fork adds another component to the node's address.

## How Tumblers Are Structured

The full Istream address has the form:

```
Node.0.User.0.Document.0.Element
```

The zeros are major dividers; everything between them is one "field." But each field itself contains a series of integers ("digits") separated by minor dividers (periods).

From the curated sources:

> "There are four major fields, each expandable indefinitely, with three major dividers between them. These fields are Server, User, Document and Contents." (4/26)

> "A tumbler address may have at most three zero digits... These are interpreted as the major dividers, and have lexical significance as punctuation." (4/28)

So the Node field is one of four fields — but the field itself is expandable.

## Why Nodes Fork

Forking applies to nodes as much as to anything else in tumbler space:

> "A server node, or station, has ancestors and may have possible descendant nodes. An account, too, and a document, all have possible descendants." (4/19)

> "The entire tumbler works like that: nodes can spin off nodes; accounts can spin off accounts; nodes can spin off accounts; and so on. Thus all numeration in the docuverse is compressed into a single mechanism." (4/19)

The forking rule:

> "One digit can become several by a forking or branching process. This consists of creating successive new digits to the right; we call these 'under' the previous digit." (4/20)

## The Root Node "1" and Its Descendants

The root has a single component:

> "The server address always begins with the digit 1, since all other servers are descended from it. This may seem an unnecessary redundancy, but it permits referring to the entire docuverse by '1' on the first position." (4/28)

But descendant nodes — being "under" their parent — accumulate components. Following the forking rule, a node descended from root 1 might be `1.2`, and a node descended from that might be `1.2.65`, and so on. The tumbler-line sample in the curated arithmetic notes makes this explicit:

> "1, 1.1, 1.1.2, 1.1.2.1, 1.1.2.2, 1.1.3, 1.2, 1.2.1, 1.2.65, 1.2.65.831, 1.3, ..."

## Summary

- A node identity occupies the **first field** of a tumbler address (the part before the first `0` divider).
- Within that field, a node address can carry **one component** (the root `1`) **or many** (e.g., `1.2.65`) depending on how deep in the server-descent tree it sits.
- Multiple components at the node level encode provenance: which ancestor server spawned which descendant.

NEED_RAW: 4/26-4/30 — the curated materials describe the four-field structure, the forking rule, and the root-server convention, but the specific worked examples of multi-component node addresses (vs. multi-component User or Document fields) would be best verified against the original tumbler-design pages.
