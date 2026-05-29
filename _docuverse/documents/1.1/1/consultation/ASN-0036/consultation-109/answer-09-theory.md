## Question 9 [theory]

> Is referential integrity (every V-reference resolves) intended to hold at every observable state including mid-operation, or only at quiescent states between operations — and what is the Literary Machines basis for that intent?

## Answer: Quiescent states, not mid-operation

Nelson's intent — to the extent Literary Machines speaks to it — is that referential integrity holds at **quiescent (between-operations) states**. Mid-operation states are not part of his observable model at all, so the question of whether the invariant holds "mid-operation" doesn't really arise in the text. Here is the basis.

### 1. The protocol/command model makes the operation the unit of observation

Nelson defines the system entirely in terms of the commands it answers:

> "What the Xanadu storage and hypertext system does--and thus is--is defined by the commands to which it responds." (4/61)

The observable interface (FEBE) is the command boundary. A front end issues `INSERT`, `DELETE`, `REARRANGE`, etc., and "the back end responds." There is no notion in Literary Machines of inspecting a document partway through an operation — the operation *is* the atomic interaction. `INSERT`, for instance, is described purely by its before/after effect:

> "This inserts <text set> in document <doc id> at <doc vsa>. The v-stream addresses of any following characters in the document are increased by the length of the inserted text." (4/66)

Nelson states the resulting state (all following V-addresses shifted); he never describes a transient state in which some addresses are shifted and others are not.

### 2. The "canonical order" mandate is explicitly a property of *completed* changes

The strongest direct textual anchor is Nelson on Barus's linking enfilade:

> "His new method would allow linkages to keep up with all changes. It was instantaneous and permanent and could grow indefinitely. **All changes, once made, left the file remaining in canonical order, which was an internal mandate of the system.**" (1/34)

Two phrases matter:
- **"once made"** ties the canonical-order invariant to completed operations — i.e., quiescent states.
- **"instantaneous"** implies changes have no observable duration; there is no mid-operation window to observe. An instantaneous transition goes from one canonical state directly to the next.

"An internal mandate of the system" is the closest Nelson comes to declaring this an invariant rather than an incidental property.

### 3. State transitions leave the system in "canonical operating condition"

The same pattern appears for the distributed case (BEBE):

> "A server's network model, from the null case on up, is at all times unified and operational; whatever information moves between servers is assimilated at once to its overall structure, leaving each server in canonical operating condition with a slightly improved map of what is elsewhere." (4/72)

Note the shape: "at all times unified and operational" describes the *observable* states, and each information-movement is "assimilated at once," **leaving** the server canonical. The integrity property is asserted of the rest-states the transition lands in, not of the interior of the transition.

### 4. Why the V-stream specifically resolves: the I-stream backstop

For V-references the post-operation density guarantee is what makes every V-reference resolve: V-addresses are contiguous (`1..N`, no gaps), and operations transform one dense arrangement into another. Underneath, the deeper reason dangling is impossible is that V-references resolve *through* permanent I-addresses:

> "Native bytes of a document are those actually stored under its control... all other bytes are obtained by front-end or back-end requests to their home locations." (4/11)

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." (4/11)

Because Istream content is never destroyed, the *target* of resolution is always present; the only thing an operation reshapes is the V→I arrangement, atomically.

### Summary

- **Intended scope:** quiescent states between operations.
- **Mid-operation:** outside Nelson's observable model. He frames the system at the command boundary, calls changes "instantaneous," and asserts canonical order "once made." There is no Literary Machines basis for an intent that the invariant hold *during* an operation, nor any text describing a mid-operation observable state.
- **Strongest citations:** 4/61 (system defined by commands), 1/34 ("once made... canonical order... internal mandate"; "instantaneous"), 4/72 ("at all times... leaving each server in canonical operating condition").

One caveat worth flagging for the formalization: Nelson never explicitly discusses operation *atomicity*, partial failure, or concurrent editing of the same document (the session-model gap — there is no locking protocol in Literary Machines). So "holds at quiescent states" is the defensible reading of his intent; treating operations as atomic step-transitions (rather than something with observable intermediate states) is the natural model that intent implies, but Nelson does not formally state an atomicity guarantee. If the formalization needs that guarantee stated as Nelson's explicit intent, that crosses into territory the text doesn't cover.
