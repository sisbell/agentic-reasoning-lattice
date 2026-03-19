## Question 9 [nelson]

> If a user creates content across multiple sessions, must the addresses assigned in each session form a contiguous block, or may they be interleaved with other users' addresses?

## Addresses Are Never Interleaved Between Users

The tumbler hierarchy structurally prevents interleaving. Each user's content lives in its own subtree of the address space, completely isolated from every other user's subtree.

### Why: The Ownership Principle

Tumbler addresses encode a strict hierarchy: `Node.0.User.0.Document.0.Element`. The key mechanism is **baptism** — whoever owns a number controls all sub-numbers beneath it:

> "The owner of a given item controls the allocation of the numbers under it." [LM 4/20]

> "Whoever owns a specific node, account, document or version may in turn designate (respectively) new nodes, accounts, documents and versions, by forking their integers." [LM 4/17]

If Alice is account `1.0.2` and Bob is account `1.0.3`, then:
- Alice's documents are `1.0.2.0.1`, `1.0.2.0.2`, `1.0.2.0.3`...
- Bob's documents are `1.0.3.0.1`, `1.0.3.0.2`, `1.0.3.0.3`...

Bob cannot create anything at an address under `1.0.2` — he doesn't own it. Alice cannot create anything under `1.0.3`. Their address spaces are disjoint by construction.

### Contiguity on the Tumbler Line

Tumblers map to a linear sequence via depth-first tree ordering. All of Alice's content occupies a contiguous range on this line, and all of Bob's content occupies a separate contiguous range:

> "The tumbler line is an abstract representation of a particular tree." [LM 4/22]

Within Alice's subtree, her documents are numbered sequentially. If she creates document 1 in session 1 and document 2 in session 5, they are `Alice.0.1` and `Alice.0.2` — contiguous in her subtree regardless of how many sessions elapsed or what other users did in between.

Within a single document, element addresses are also sequential:

> "The digit after the one indicates the byte position in the current ordering of bytes." [LM 4/30]

### Physical Storage Is a Separate Concern

There is a distinction between **logical addresses** (tumblers) and **physical storage** (the append-only store). Nelson describes content being "filed, as it were, chronologically" [LM 2/14] in the physical store. So physically, bytes from different users' sessions may be interleaved in the append-only stream. But the **I-space addresses** are tree-structured, not chronological. The enfilades bridge this gap — mapping from logical tumbler addresses to physical locations:

> "By various enfilade structures we were able to come up with a design that could conceivably scale up infinitely." [LM 1/36]

### Summary

| Level | Interleaved? | Why |
|-------|-------------|-----|
| Between users | Never | Different subtrees; ownership prevents cross-allocation |
| Between documents (same user) | Never | Documents numbered sequentially under user's account |
| Within a document (across sessions) | Never | Elements numbered sequentially within document |
| Physical storage bytes | May be | Append-only; chronological; but this is invisible to addressing |

The answer is unambiguous: **addresses need not and cannot be interleaved between users.** The tumbler tree structure guarantees that each user's addresses form a contiguous subtree, and the ownership/baptism mechanism makes it impossible for one user to allocate addresses within another user's subtree.
