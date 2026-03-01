# Tumbler Arithmetic

Source: Literary Machines, 4/19-4/40

## What It Means

Tumblers are a specialized number system for addressing an ever-growing, decentralized tree of content. They are **tree addresses** that happen to be manipulable through arithmetic operations.

A tumbler is "a series of integers" where each integer (called a "digit") has no upper limit. The digits are separated by minor dividers (periods). Tumblers use arbitrary-precision integers ("humbers") because each digit can grow without limit as the network expands.

**Two types:**
- **Address Tumblers** — point to specific locations; permanent
- **Difference Tumblers** — represent spans; always paired with an address

## The Tumbler Line

All tumblers form a linear sequence when sorted (depth-first ordering of the tree):

```
1, 1.1, 1.1.2, 1.1.2.1, 1.1.2.2, 1.1.3, 1.2, 1.2.1, 1.2.65, 1.2.65.831, 1.3, ...
```

Every subtree maps to a contiguous range on the tumbler line. This is why spans work.

## The Width Paradox

A span is NOT a count. A difference tumbler does NOT designate "this many bytes."

> "A tumbler-span is not a conventional number, and it does not designate the number of bytes contained. It does not designate a number of anything." (4/24)

A span designates "from here to there" — a subtree of the docuverse. A span might contain nothing today and a million documents tomorrow.

## User Guarantee

Any address remains valid forever. New items are inserted by forking (creating sub-addresses), not by renumbering.

## Principle Served

Tumblers solve permanent addressing in an infinite, decentralized system: no central authority needed, no coordination between nodes, arithmetic supports efficient span operations, tree structure supports ownership.

## Nelson's Words

> "A tumbler consists of a series of integers. Each integer has no upper limit; since its number base is irrelevant, we call it a 'digit.' The digits of the tumbler are separated by minor dividers, or points." (4/19)

> "New items may be continually inserted in tumbler-space while the other addresses remain valid." (4/19)

> "In a sense the tumbler line is like the real line, i.e., the line of integers and all the numbers in between. But the tumbler line is a different kind of abstraction from the real line. The real line is the same under all circumstances. The tumbler line is an abstract representation of a particular tree." (4/22)

> "The contents of the tumbler line are determined by the population of entities and relations on the tree it represents. Thus the tumbler line is not definite in the same way as the real line; the tumbler line is a flat mapping of a particular tree, finite but unlimited." (4/22)

> "A span may be visualized as a zone hanging down from the tumbler line--what is called in computer parlance a depth-first spanning tree." (4/25)

> "This is a curious, bizarre, powerful, consistent, non-obvious and hard-to-visualize system. It also has a certain quirkiness and charm. Call it a hack, yes; but it is definitely a superhack." (4/40)
