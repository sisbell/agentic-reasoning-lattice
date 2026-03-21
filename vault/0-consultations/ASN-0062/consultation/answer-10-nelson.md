## Question 10 [nelson]

> Must the completed placement be an all-or-nothing operation — either fully applied with all guarantees holding, or not applied at all — or may it leave the document in a partial state?

## Atomicity of Placement Operations

Nelson never uses the terms "atomic" or "transaction." But the architecture mandates all-or-nothing through a different principle: **canonical order as an internal mandate**.

### The Canonical Order Mandate

From Nelson's description of Barus's enfilade contribution:

> "All changes, once made, left the file remaining in canonical order, which was an internal mandate of the system." [LM 1/34]

The phrase "internal mandate" is significant — this is not a desirable property but a system invariant. After any change, the structure is in canonical order. There is no acknowledged intermediate state where canonical order is violated.

This is reinforced at the network level:

> "A server's network model, from the null case on up, is at all times unified and operational; whatever information moves between servers is assimilated at once to its overall structure, leaving each server in canonical operating condition." [LM 4/72]

"At all times" and "canonical operating condition" leave no room for partial states.

### Why Partial Application Violates the Architecture

A placement (INSERT, COPY, APPEND) modifies the Vstream mapping. Consider what a partial state would mean:

1. **Vstream density violation.** V-addresses are always dense and contiguous from position 1. A partial insertion would either leave a gap (content placed but V-addresses not updated) or create an overlap (V-addresses shifted but content not yet placed). Neither is a valid Vstream state.

2. **Link coherence violation.** Nelson specifies that after INSERT, "the v-stream addresses of any following characters in the document are increased by the length of the inserted text" [LM 4/66]. If only some following addresses were shifted, links referencing the unshifted portion would resolve to wrong content — violating the link survivability guarantee.

3. **Part-pounce integrity.** Nelson guarantees that any part of any version can be materialized on demand: "when you ask for a given part of a given version at a given time, it comes to your screen" [LM 2/15]. A partially-applied placement would produce an incoherent view when pounced upon.

### REARRANGE as Evidence

The REARRANGE operation is especially telling. It "transposes two regions of text" [LM 4/67] — a compound modification (remove region A, remove region B, place B where A was, place A where B was). If this could leave a partial state (one region moved, the other not), the document would contain duplicated or missing content. Nelson describes it as a single FEBE command, implying it completes as a unit.

### What Nelson Specifies vs. What He Leaves to Implementation

**Explicitly specified:** The system is always in canonical order after a change. There is no discussion of partial states, rollback, or recovery from incomplete operations — not because he forgot, but because the architecture doesn't admit them.

**Not specified:** The mechanism by which atomicity is achieved. Whether this is through write-ahead logging, copy-on-write, or some property of enfilade structure is left to the implementor. Nelson designs at the semantic level, not the concurrency-control level.

### My Answer

The completed placement must be all-or-nothing. This follows from the canonical order mandate [LM 1/34], the "at all times unified and operational" requirement [LM 4/72], and the structural properties of the Vstream (dense addressing, link coherence, part-pounce integrity). Nelson does not discuss partial states because his architecture does not admit them — every operation either leaves the system in canonical operating condition or does not happen.
