## Question 8 [nelson]

> Must the difference between two addresses within the same level be arithmetically meaningful — for instance, must it tell you how many content units lie between them?

## No. The difference between two tumbler addresses is not a count of anything.

Nelson is explicit and emphatic on this point:

> "A tumbler-span is not a conventional number, and it does not designate the number of bytes contained. It does not designate a number of anything."
> — [LM 4/24]

The difference between two addresses specifies **boundaries**, not **cardinality**. What lies between those boundaries depends on the actual population of the tree — which is dynamic and unpredictable:

> "A span that contains nothing today may at a later time contain a million documents."
> — [LM 4/25]

### Why the arithmetic doesn't yield a count

The tumbler line is not the real number line. It is a depth-first flattening of a tree whose population changes as content is created:

> "The tumbler line is an abstract representation of a particular tree... The contents of the tumbler line are determined by the population of entities and relations on the tree it represents. Thus the tumbler line is not definite in the same way as the real line; the tumbler line is a flat mapping of a particular tree, finite but unlimited."
> — [LM 4/22]

Between any two sibling addresses (say document 3 and document 7 under the same account), the "distance" of 4 tells you nothing about how many items exist there, because:

1. **Forking creates subtrees.** Document 5 might have subdivisions 5.1, 5.2, 5.3... each with further descendants. The span from 3 to 7 encompasses all of them — their count is unknowable from the addresses alone. [LM 4/20]

2. **Ghost elements may occupy positions.** Addresses can be referenced even when nothing is stored there. A span sweeps over occupied and ghost positions alike. [LM 4/23]

3. **The content is implicit in the boundaries, not computable from them:**

> "The first point of a span may designate a server, an account, a document or an element; so may the last point. There is no choice as to what lies between; this is implicit in the choice of first and last point."
> — [LM 4/25]

### The one exception: V-space byte positions

Within a single document version, V-space byte addresses **are** dense sequential integers (1, 2, 3, ... N) with no gaps — by definition, INSERT shifts subsequent addresses and DELETE closes gaps [LM 4/66]. So in V-space, the difference between position 10 and position 20 does correspond to 10 byte positions. But this is a property of V-space's contiguous virtual stream, not of tumbler arithmetic in general. Nelson explicitly notes that V-addresses are ephemeral and "may be continually altered by editorial operations" [LM 4/30].

### What tumbler arithmetic *is* for

Tumbler arithmetic supports **span manipulation** — computing whether one address falls within a span, combining spans, computing difference tumblers for compact representation. It is an addressing calculus, not a counting calculus:

> "In one big flash of insight, Mark Miller saw that everything could be named within a common structure, and that an arithmetic could be developed for this structure to be the common internal language throughout the search procedures of the system."
> — [LM 4/16]

The arithmetic makes addresses **manipulable** (you can compute offsets, test containment, define ranges). It does not make them **cardinal** (you cannot derive population from distance).
