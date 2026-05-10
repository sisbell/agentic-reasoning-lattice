## Question 4 [nelson]

> Must newly assigned addresses always be greater than all previously assigned addresses, or may the system fill in gaps retroactively?

## Addresses Are Inserted, Not Appended

The system explicitly inserts new addresses between existing ones. This is the defining capability of the tumbler addressing scheme — and the reason Nelson chose it.

> "New items may be continually inserted in tumbler-space while the other addresses remain valid."
> — [LM 4/19]

The word is **inserted**, not appended. The forking mechanism creates children beneath any existing address, and those children fall between the parent and its next sibling on the tumbler line.

### How Forking Creates "Retroactive" Addresses

Suppose addresses 2.1 and 2.2 already exist. When 2.1 later acquires a child, the tumbler line becomes:

```
..., 2.1, 2.1.1, 2.2, ...
```

Address 2.1.1 is **newer** than 2.2 in creation time but **smaller** on the tumbler line. The depth-first tree ordering guarantees this:

> "A span may be visualized as a zone hanging down from the tumbler line — what is called in computer parlance a depth-first spanning tree."
> — [LM 4/25]

Every subtree maps to a contiguous range. Children always fall within their parent's range, which necessarily places them before the parent's next sibling.

### Sequential Within a Level, Not Globally

At any single level of the hierarchy, siblings are created sequentially:

> "For instance, if there is an item 2, it can branch into several more items, each of which is a daughter item. Thus 2.1, 2.2, 2.3, 2.4... are successive items being placed under 2."
> — [LM 4/20]

So you create 2.1, then 2.2, then 2.3 — never skipping ahead. But each of those can later spawn children that fill in the space between them on the tumbler line. The owner of any address controls subdivision beneath it:

> "The owner of a given item controls the allocation of the numbers under it."
> — [LM 4/20]

### Spans Anticipate Future Population

Nelson makes the consequence explicit — a range that is empty today may be populated later:

> "A span that contains nothing today may at a later time contain a million documents."
> — [LM 4/25]

A span between two existing addresses is a valid, meaningful range even when empty. Content can be created within it at any future time through forking.

### The Tumbler Line Is Not Fixed

Unlike the real number line, the tumbler line is determined by what has been created so far:

> "The contents of the tumbler line are determined by the population of entities and relations on the tree it represents. Thus the tumbler line is not definite in the same way as the real line; the tumbler line is a flat mapping of a particular tree, finite but unlimited."
> — [LM 4/22]

Every forking operation adds new points to the line, potentially between any existing points.

### Summary

| Level | Ordering rule |
|-------|--------------|
| **Siblings** (same parent) | Sequential — 2.1 before 2.2 before 2.3 |
| **Global tumbler line** | NOT monotonic by creation time — children of 2.1 are inserted before 2.2 regardless of when they're created |
| **Spans** | May be empty now, populated later |

The system does not merely permit filling gaps — **filling gaps is the fundamental growth mechanism**. The entire docuverse grows by forking, and forking always inserts rather than appends. This is why Nelson called it "a superhack" [LM 4/40] — it achieves permanent addressing in an ever-growing space precisely because new addresses slot into the existing structure rather than requiring global renumbering.
