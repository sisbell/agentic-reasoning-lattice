## Question 1 [nelson]

> Must every address in the system be comparable to every other — can the system ever encounter two addresses where neither is "before" the other?

## Every Address Is Comparable: The Tumbler Line Is a Total Order

**Yes, every address is comparable to every other.** Nelson designed the tumbler system so that all addresses form a single linear sequence — he consistently calls it "the tumbler line" — and no two addresses can be incomparable.

### The Totality Guarantee

The tumbler system maps a hierarchical tree (servers → accounts → documents → versions → elements) onto a flat linear sequence via depth-first ordering. This traversal inherently produces a total order: for any two nodes in a tree, depth-first traversal visits one before the other.

Nelson states this explicitly:

> "In a sense the tumbler line is like the real line, i.e., the line of integers and all the numbers in between. But the tumbler line is a different kind of abstraction from the real line. The real line is the same under all circumstances. The tumbler line is an abstract representation of a particular tree." [LM 4/22]

The real line is totally ordered. Nelson's comparison is deliberate — the tumbler line shares this property, differing only in that its "population" is determined by the tree it represents rather than being fixed a priori:

> "The contents of the tumbler line are determined by the population of entities and relations on the tree it represents. Thus the tumbler line is not definite in the same way as the real line; the tumbler line is a flat mapping of a particular tree, finite but unlimited." [LM 4/22]

"Finite but unlimited" and "not definite" refer to the *contents* growing over time (new addresses baptized), not to any incomparability between existing addresses. The mapping is always flat — always a line.

### How Comparison Works

Tumblers are sequences of unbounded integers ("digits") separated by minor dividers (periods), with zeros serving as major field dividers. The depth-first ordering gives a concrete comparison algorithm:

1. Compare digit by digit, left to right
2. At the first difference, the smaller digit comes first
3. If one tumbler is a prefix of the other, the shorter one (the parent) comes first

The example sequence from the curated sources illustrates this:

```
1, 1.1, 1.1.2, 1.1.2.1, 1.1.2.2, 1.1.3, 1.2, 1.2.1, 1.2.65, 1.2.65.831, 1.3, ...
```

Every pair here has a definite ordering. No ambiguity, no incomparability.

The zero field-separators integrate into this naturally. A zero at position *n* is simply the digit zero, which is less than any positive digit. So all of User 1's content under Server 1 (`1.0.1.0.…`) comes before any sub-server address (`1.1.…`), because `0 < 1` at the third position.

### Why This Matters: Spans Require Totality

The total ordering is not incidental — it is architecturally load-bearing. Spans are defined as contiguous regions on the tumbler line:

> "A span in the tumbler line, represented by two tumblers, refers to a subtree of the entire docuverse." [LM 4/24]

> "A span may be visualized as a zone hanging down from the tumbler line — what is called in computer parlance a depth-first spanning tree." [LM 4/25]

If two addresses were incomparable, the interval between them would be undefined, and spans would not work. The entire machinery of span-sets, request-sets, and endset-based link search depends on "between address A and address B" always having a definite meaning.

### The Arithmetic Reachability Caveat

Nelson does note one asymmetry in tumbler *arithmetic* (as opposed to tumbler *comparison*):

> "Starting from a given tumbler address, it may only be possible arithmetically to get to some places in the Docuverse — those notationally after that address." [LM 4/25]

This is about **computational reachability via addition of difference tumblers**, not about ordering. You can always *compare* any two addresses, but you cannot always *reach* one from the other through tumbler addition alone. The ordering is total; the arithmetic is not symmetric.

### Summary

The system **never** encounters two addresses where neither is "before" the other. The tumbler line is a total order by construction — it is a depth-first linearization of the docuverse tree. This totality is required by the span mechanism, which is in turn required by the link and search mechanisms. Nelson's repeated use of "the tumbler line" and his comparison to the real line are precise: like the real line, every two points are comparable.
