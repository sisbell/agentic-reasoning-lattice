## Question 10 [nelson]

> If multiple users simultaneously create nodes, what must the system guarantee about the consistency and disjointness of the resulting node identities?

## Node Identity: Disjointness and Consistency Under Concurrent Creation

Nelson does not explicitly address the concurrent-creation scenario in Literary Machines. However, the tumbler architecture makes the answer fall out structurally: **disjointness is guaranteed by ownership, not by coordination.**

### The Baptism Mechanism

The core principle is ownership-based delegation:

> "The basic principle is that of owned numbers. Numbers are owned by individuals or companies, and subnumbers under them are bestowed on other individuals and companies on whatever basis the owners choose. Whoever owns a specific node, account, document or version may in turn designate (respectively) new nodes, accounts, documents and versions, by forking their integers. We often call this the 'baptism' of new numbers." [LM 4/17]

> "The owner of a given item controls the allocation of the numbers under it." [LM 4/20]

This means: if Alice owns node `1.2` and Bob owns node `1.3`, Alice creates sub-nodes `1.2.1, 1.2.2, ...` and Bob creates `1.3.1, 1.3.2, ...`. They operate in **structurally disjoint subtrees**. No coordination is needed between them.

### What the System Must Guarantee

**1. Subtree disjointness (architectural, automatic):**
Different owners' subtrees never overlap. Two users creating nodes simultaneously under different parent addresses produce addresses that are guaranteed distinct by the tree structure itself.

**2. Sequential uniqueness within a single owner's scope:**
When a single owner (e.g., a server allocating accounts) must assign successive numbers to concurrent requestors, the system must serialize those assignments. If server `1.2` creates accounts for two simultaneous sign-ups, it must produce `1.2.0.3` and `1.2.0.4`, never `1.2.0.3` twice. This is a local problem — one owner, one counter.

**3. Permanence of assigned addresses:**

> "New items may be continually inserted in tumbler-space while the other addresses remain valid. This means that any address of any document in an ever-growing network may be specified by a permanent tumbler address." [LM 4/19]

Once baptized, an address is permanent. The system must never reassign it.

**4. Canonical condition after every operation:**

> "All changes, once made, left the file remaining in canonical order, which was an internal mandate of the system." [LM 1/34]

> "A server's network model, from the null case on up, is at all times unified and operational; whatever information moves between servers is assimilated at once to its overall structure, leaving each server in canonical operating condition with a slightly improved map of what is elsewhere." [LM 4/72]

After any creation, every server must remain in a valid, queryable state.

### Why Central Coordination Is Not Needed

The architecture eliminates the hard concurrency problem by design. Two servers in different parts of the world can each create thousands of sub-nodes per second without consulting each other, because:

- Server `1.5` creates under `1.5.*`
- Server `1.8` creates under `1.8.*`
- The resulting addresses are structurally guaranteed disjoint

The only point requiring serialization is **within a single owner's allocation counter**, which is local state.

> "The entire tumbler works like that: nodes can spin off nodes; accounts can spin off accounts; nodes can spin off accounts; and so on. Thus all numeration in the docuverse is compressed into a single mechanism." [LM 4/19]

> "So the docuverse is all really one big forking document." [LM 4/18]

### What Nelson Does NOT Specify

Nelson does not address:
- How a single server serializes concurrent allocations internally (implementation detail)
- What happens if two servers claim the same parent address (prevented by the franchise model — servers get assigned disjoint node numbers)
- Consistency protocols for propagating new node existence across the network (BEBE handles this incrementally, but the details are proprietary)

NEED_RAW: [4/70-4/75] — The BEBE protocol pages may contain additional detail about how node creation events propagate between servers, though the curated sources suggest this was still "undergoing definition."

### Summary

The system guarantees:

| Property | Mechanism |
|----------|-----------|
| **Disjointness across owners** | Structural — different subtrees cannot collide |
| **Uniqueness within an owner** | Sequential allocation — local serialization |
| **Permanence** | Once baptized, never reassigned |
| **Canonical state** | Every server remains valid after every operation |

The insight is that Nelson designed away the distributed consensus problem. You don't need agreement on "who gets address X" when every owner has an infinite, exclusive subtree to allocate from.
