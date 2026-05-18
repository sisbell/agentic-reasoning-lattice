## Question 15 [theory]

> Does Literary Machines commit the docuverse to a single-rooted tree (one bootstrap server address from which all node addresses descend), or does the design admit multiple coexisting roots for federated servers each owning a disjoint node-address subtree?

# Single-Rooted Tree, Not Multiple Roots

Literary Machines commits the docuverse to a **single-rooted tree**. All server addresses descend from one bootstrap root (the digit `1`). Federation happens *within* this tree — different Storage Vendors operate disjoint subtrees — but the address space itself has one origin, not many.

## The Decisive Quote

Nelson is explicit at LM 4/28:

> "The server address always begins with the digit 1, since all other servers are descended from it. This may seem an unnecessary redundancy, but it permits referring to the entire docuverse by '1' on the first position." [LM 4/28]

This forecloses the multi-root reading. Every server is, by construction, a descendant of node 1.

## Supporting Evidence

**The whole docuverse is one forking structure** [LM 4/18]:

> "So the docuverse is all really one big forking document."

**Forking is the only growth mechanism** [LM 4/19]:

> "A server node, or station, has ancestors and may have possible descendant nodes."

> "Nodes can spin off nodes; accounts can spin off accounts; nodes can spin off accounts; and so on. Thus all numeration in the docuverse is compressed into a single mechanism." [LM 4/19]

**Mark Miller's design unifies everything under one structure** [LM 4/16]:

> "In one big flash of insight, Mark Miller saw that everything could be named within a common structure, and that an arithmetic could be developed for this structure to be the common internal language throughout the search procedures of the system."

**The network model assumes one address space** [LM 4/72]:

> "Each server contains a continuously valid model or subrepresentation of the entire docuverse and (because of tumbler addressing) a model of the entire network."

A single coherent "model of the entire network" requires that all server addresses live in one comparable space — i.e., share a root.

## How Federation Works Within the Single Tree

Federation is real in Nelson's design, but it is structural, not topological:

- **Vendors own subtrees, not parallel universes.** A Storage Vendor operates some node `1.x` (or a subtree beneath it). They control allocation of `1.x.*` under the "baptism" principle [LM 4/17, 4/20], but `1.x` itself is a descendant of `1`.
- **BEBE melds, it doesn't merge separate spaces.** "The function of BEBE is to meld the contents of separate Xanadu servers into a single unified space" [LM 4/70]. The space is already unified by addressing; BEBE just routes requests.
- **Why `1` is reserved.** Nelson's stated reason — "it permits referring to the entire docuverse by '1' on the first position" [LM 4/28] — only works if every server is reachable from `1`. Multiple disjoint roots would break this convention.

## What Nelson Does Not Address

Nelson does not discuss:
- Who controls baptism of new top-level nodes (`1.2`, `1.3`, ...) — i.e., who plays root operator
- Bootstrapping in a partitioned network
- Migration or splits if a Xanadu-licensed franchise dissolves

These are governance questions the franchise model (Project Xanadu as licensor, [LM 5/14-5/16]) implicitly handles, but Nelson does not specify the mechanics.

NEED_RAW: nothing additional — the curated sources cover the question directly.

## Summary

The design is unambiguous: **one root (`1`), one tree, one tumbler line**. Federated servers are subtrees under that root, each controlling their own allocations under baptism, but all reachable through a single shared address space. Multiple coexisting roots with disjoint node-address subtrees is not Nelson's design — it would defeat the purpose of having a unified tumbler line and the convention that `1` denotes the entire docuverse.
