## Question 3 [nelson]

> Once a node has entered the docuverse, can it ever be removed, or must the node set grow monotonically?

## Nodes Cannot Be Removed from the Address Space

The node set must grow monotonically. Once a node address is assigned ("baptized"), it is permanently part of tumbler-space. However, the *physical infrastructure* behind a node can change or disappear — what persists is the address, not the machine.

### The Address Is Permanent

Nelson is explicit that tumbler addresses, once assigned, never become invalid:

> "New items may be continually inserted in tumbler-space while the other addresses remain valid. This means that any address of any document in an ever-growing network may be specified by a permanent tumbler address." [LM 4/19]

Since every document, account, and byte address *beneath* a node includes that node's address as a prefix (e.g., `1.3.0.U.0.D.0.E` for anything on node 1.3), removing the node would invalidate every address under it. This would violate the permanence guarantee.

### Ghost Nodes Are Valid Nodes

Nelson directly addresses what happens when a node has no physical representation — it becomes a **ghost element**:

> "While servers, accounts and documents logically occupy positions on the developing tumbler line, no specific element need be stored in tumbler-space to correspond to them. Hence we may call them ghost elements." [LM 4/23]

> "However, these elements are virtually present in tumbler-space, since links may be made to them which embrace all the contents below them." [LM 4/23]

A node whose physical server has been decommissioned still exists as a position on the tumbler line. Links to that node address (or to any address beneath it) remain valid.

### Physical Infrastructure Can Change

Nelson separates the address from the machine. The vendor contract requires orderly transition when a vendor shuts down:

> "Upon notice of cancellation, Storage Vendor will arrange for the orderly transition of all customer-stored materials to other Xanadu locations." [LM 5/16]

Content migrates; the address stays. The BEBE protocol handles this through subrepresentation — other servers hold copies and maps:

> "Each server contains a map and a subset of the whole — a microcosm that shrinks and grows." [LM 4/71]

Nelson also acknowledges that nodes go offline routinely:

> "It is a truism that 'computer networks are always broken.' Meaning that on the average some nodes are disconnected or not working." [LM 4/75]

Temporary unavailability is handled by redundancy and backup copies, not by removing the node from the address space.

### Why This Must Be So

The docuverse is defined as the *occupied tumbler-space* — occupied by conceptual assignment, not physical storage:

> "The docuverse is the occupied tumbler-space — as occupied by conceptually assigned positions, even if nothing represents them in storage." [LM 4/23]

Removing a node would mean un-assigning its position, which contradicts the fundamental nature of the addressing system. The forking mechanism only adds — "nodes can spin off nodes" [LM 4/19] — and there is no corresponding un-fork operation anywhere in the specification.

### Summary

| Aspect | Can it be removed? |
|--------|-------------------|
| Node address in tumbler-space | **No** — permanent |
| Physical server hardware | Yes — content migrates |
| Vendor license | Yes — with orderly transition |
| Content stored at node | Yes — moves to other locations |
| Links pointing to node's address range | **No** — remain valid (may resolve to ghost or backup) |

The node set grows monotonically in addressing terms. A decommissioned node becomes a ghost element — addressable, linkable, but with no physical representation. Its content lives elsewhere; its address endures.
