## Question 8 [nelson]

> What invariants must hold over the set of all nodes — must their address portions be non-overlapping, contiguous, or satisfy some other structural property?

## Node Address Invariants in the Docuverse

Nelson does not state a single "node invariant" explicitly, but several structural properties are derivable from his tumbler and forking design. Here is what the specification establishes:

### 1. Tree-Structured Non-Overlap (Inherent)

Node addresses form a tree rooted at digit 1. Each node owns a unique subtree of the address space. Non-overlap is not an enforced invariant — it is a structural consequence of the addressing scheme.

> "The server address always begins with the digit 1, since all other servers are descended from it. This may seem an unnecessary redundancy, but it permits referring to the entire docuverse by '1' on the first position." [LM 4/28]

> "A server node, or station, has ancestors and may have possible descendant nodes." [LM 4/19]

> "The owner of a given item controls the allocation of the numbers under it." [LM 4/20]

Because sub-nodes are created by appending digits (1 → 1.1, 1.2, 1.3...; 1.2 → 1.2.1, 1.2.2...), sibling subtrees are structurally disjoint. Content at `1.2.0.U.0.D.0.E` cannot also be at `1.3.0.U.0.D.0.E` — the Node field distinguishes them absolutely.

### 2. Not Contiguous — Sparse Population Is Valid

Nodes need **not** be contiguous among siblings. You may have nodes 1.1 and 1.3 without 1.2 ever existing. Ghost elements explicitly allow this:

> "While servers, accounts and documents logically occupy positions on the developing tumbler line, no specific element need be stored in tumbler-space to correspond to them. Hence we may call them ghost elements." [LM 4/23]

> "A span that contains nothing today may at a later time contain a million documents." [LM 4/25]

The address space is sparse by design. The forking mechanism creates addresses on demand through "baptism" — there is no requirement that all integer positions between existing nodes be populated.

### 3. Subtree Contiguity on the Tumbler Line

While nodes need not be contiguous siblings, each node's **subtree** maps to a contiguous range on the tumbler line (which is a depth-first serialization of the tree):

> "In a sense the tumbler line is like the real line... But the tumbler line is a different kind of abstraction from the real line... The tumbler line is a flat mapping of a particular tree, finite but unlimited." [LM 4/22]

> "A span in the tumbler line, represented by two tumblers, refers to a subtree of the entire docuverse." [LM 4/24]

This is the property that makes spans work for node-level operations. A single span can address "everything on node 1.2" — all accounts, documents, versions, and bytes under that prefix — because the depth-first mapping guarantees the subtree is contiguous on the line.

### 4. Content Partition by Home Node

Every byte in the docuverse has exactly one **home** node, determined by the Node field of its I-address. This partitions all native content across nodes:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

> "There are four major fields, each expandable indefinitely, with three major dividers between them. These fields are Server, User, Document and Contents." [LM 4/26]

Note: this is a partition of *ownership*, not physical presence. BEBE allows content to be cached across nodes:

> "The contents can slosh back and forth dynamically." [LM 4/72]

But the I-address (and therefore the home node) never changes.

### 5. Ownership Delegation (Baptism Invariant)

Only the owner of a node can create sub-nodes beneath it. This is the "baptism" principle:

> "The basic principle is that of owned numbers. Numbers are owned by individuals or companies, and subnumbers under them are bestowed on other individuals and companies on whatever basis the owners choose. Whoever owns a specific node, account, document or version may in turn designate (respectively) new nodes, accounts, documents and versions, by forking their integers." [LM 4/17]

This means the tree can only grow downward from existing owned positions. No node can create a sibling or a parent — only children. This preserves the non-overlap property: since you can only subdivide what you own, you cannot create addresses that collide with another node's subtree.

### 6. Single Root

All nodes descend from 1. There is exactly one root. This is both stated and architecturally necessary for the tumbler line to work as a unified space.

### Summary of Invariants

| Property | Holds? | Source |
|----------|--------|--------|
| Non-overlapping subtrees | Yes (structural) | Tree addressing + forking |
| Contiguous siblings | **No** — sparse allowed | Ghost elements [4/23] |
| Contiguous subtree on tumbler line | Yes | Depth-first mapping [4/22, 4/24] |
| Content partitioned by home node | Yes (by I-address) | Native bytes [4/11, 4/26] |
| Downward-only creation (baptism) | Yes | Ownership delegation [4/17] |
| Single root at 1 | Yes | [4/28] |

### What Nelson Does Not Address

Nelson does not discuss:
- Whether a node can be **retired** or **merged** with another (only vendor shutdown with "orderly transition" is specified [5/16])
- Maximum depth of the node tree
- Whether node addresses can be **reassigned** after abandonment
- Formal constraints on the rate or pattern of node creation

NEED_RAW: [4/17-4/21, 4/28-4/29] — these pages cover forking and the server address field in detail. The curated sources provide good coverage, but the raw pages may contain diagrams or marginal notes about structural constraints on node creation that the text extraction missed.
