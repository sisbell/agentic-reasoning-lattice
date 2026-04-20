## Question 2 [nelson]

> Between any two adjacent addresses, must there always be room to assign a new address, or can the address space between two points ever be exhausted?

# Between Any Two Addresses, There Is Always Room

The address space between two points can **never** be exhausted. This is fundamental to the design — indeed, it is the entire reason tumblers exist.

## The Forking Mechanism

Tumblers grow by subdivision, not by counting upward into some ceiling. Between address 2 and address 3, I can create 2.1, 2.2, 2.3, and so on indefinitely. Between 2.1 and 2.2, I can create 2.1.1, 2.1.2, 2.1.3. This nesting has no limit:

> "One digit can become several by a forking or branching process. This consists of creating successive new digits to the right; we call these 'under' the previous digit." [LM 4/20]

> "For instance, if there is an item 2, it can branch into several more items, each of which is a daughter item. Thus 2.1, 2.2, 2.3, 2.4... are successive items being placed under 2." [LM 4/20]

And each of those daughters can herself have daughters, without limit.

## The Guarantee

This is stated explicitly as the core addressing invariant:

> "New items may be continually inserted in tumbler-space while the other addresses remain valid. This means that any address of any document in an ever-growing network may be specified by a permanent tumbler address." [LM 4/19]

The word "continually" is doing real work there. It means the process never terminates. There is no state in which you have used up the space between two points.

## Not Like the Integers

People accustomed to conventional numbering think "between 2 and 3 there is nothing." But tumblers are not integers. The tumbler line is a flattening of a tree, and trees grow downward without bound:

> "In a sense the tumbler line is like the real line, i.e., the line of integers and all the numbers in between. But the tumbler line is a different kind of abstraction from the real line. The real line is the same under all circumstances. The tumbler line is an abstract representation of a particular tree." [LM 4/22]

> "The contents of the tumbler line are determined by the population of entities and relations on the tree it represents. Thus the tumbler line is not definite in the same way as the real line; the tumbler line is a flat mapping of a particular tree, finite but unlimited." [LM 4/22]

**Finite but unlimited.** At any moment the tree has finitely many nodes. But it can always grow. A span that today contains nothing may tomorrow contain a million documents:

> "A span that contains nothing today may at a later time contain a million documents." [LM 4/25]

## Why This Matters

If the space between two addresses could be exhausted, the entire system would fail. You would need to renumber, which would break every existing reference. The permanent-address guarantee — the foundation of permanent citation, permanent links, permanent literature — depends absolutely on the inexhaustibility of the address space.

This is what makes tumblers different from file paths, database keys, or URLs. Those systems can run out of names in a given namespace. Tumblers cannot. The owner of any address can always create sub-addresses beneath it, without coordinating with anyone, without risk of collision, and without disturbing any existing address.

> "The owner of a given item controls the allocation of the numbers under it." [LM 4/20]

Each digit in the tumbler is an unbounded integer (a "humber"), and the number of digits is itself unbounded. The address space is infinite in two dimensions: each digit can grow without limit, and the depth of nesting can grow without limit.

> "This is a curious, bizarre, powerful, consistent, non-obvious and hard-to-visualize system. It also has a certain quirkiness and charm. Call it a hack, yes; but it is definitely a superhack." [LM 4/40]
