## Question 4 [nelson]

> Can every collection of content positions be expressed as a finite set of contiguous regions, and must there be exactly one minimal such expression?

## Yes to both — with an important caveat about the second.

### Part 1: Every collection is expressible as a finite span-set

At any moment, the docuverse contains finitely many occupied positions on the tumbler line. Any collection of content positions is therefore a finite subset of a finite totally ordered set.

Nelson explicitly provides the mechanism:

> "Note: if you want to designate a separated series of items exactly, including nothing else, you do this by a span-set, which is a series of spans." [LM 4/25]

In the worst case (every target position separated by non-target content), each position gets its own unit span. This is always possible because:

> "In fact, a tumbler-span may range in possible size from one byte to the whole docuverse." [LM 4/24]

So yes — a finite span-set always suffices.

### Part 2: The minimal expression is unique

The tumbler line is a **total order** — a depth-first linearization of the docuverse tree:

> "In a sense the tumbler line is like the real line, i.e., the line of integers and all the numbers in between. But the tumbler line is a different kind of abstraction from the real line... the tumbler line is a flat mapping of a particular tree, finite but unlimited." [LM 4/22]

Given a target set S of content positions drawn from a finite total order, define two positions p, q in S as *contiguous in S* iff every **content** position between them on the tumbler line is also in S. Ghost elements — addressable positions with no stored content — do not break contiguity, because:

> "While servers, accounts and documents logically occupy positions on the developing tumbler line, no specific element need be stored in tumbler-space to correspond to them." [LM 4/23]

Ghosts carry no content, so including them in a span adds nothing and excludes nothing.

The contiguity relation partitions S into **maximal contiguous components** (runs). Each run yields exactly one span (from its minimum to its maximum element). No span can merge two distinct runs without including a non-target content position between them — which would violate "exactly, including nothing else." Therefore:

- The number of spans equals the number of runs — this is the minimum possible.
- The endpoints of each span are forced (the extremes of each run).
- **The minimal span-set is unique.**

### The caveat: minimality is moment-dependent

Nelson warns:

> "A span that contains nothing today may at a later time contain a million documents." [LM 4/25]

Because new positions can be **forked** into existence between existing ones:

> "One digit can become several by a forking or branching process. This consists of creating successive new digits to the right." [LM 4/20]

A span-set that minimally covers a collection **today** may cease to be minimal — or even correct — **tomorrow**, if new content appears between the endpoints of one of its spans. A single span [A, B] covering target positions A and B might need splitting into [A, A] ∪ [B, B] after a non-target position C is created between them.

The minimal span-set exists and is unique **at any given instant**, but it is not stable across mutations of the address space.

### Summary

| Question | Answer |
|----------|--------|
| Can every collection be expressed as a finite span-set? | **Yes** — unit spans always work as a fallback |
| Is the minimal expression unique? | **Yes** — forced by the total order on the tumbler line |
| Is the minimal expression stable over time? | **No** — forking can split spans |

This has a practical implication for span algebra: canonical forms must either be recomputed after mutations, or the algebra must track the ambient population of the tumbler line at the time of construction.
