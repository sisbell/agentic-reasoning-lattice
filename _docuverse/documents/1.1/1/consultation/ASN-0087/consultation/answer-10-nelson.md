## Question 10 [nelson]

> Does the design require that the system maintain a complete, queryable index from any span of content to all links whose endsets reference that span, and must this index be updated atomically with link creation?

## Yes to the index; implied but not explicitly specified for atomicity.

### The Index Requirement: Clearly Specified

Nelson requires a complete, queryable index from content spans to all referencing links. Multiple passages establish this unambiguously.

**The operation that demands it:**

FINDLINKSFROMTOTHREE returns "a list of all links which are (1) in \<home set\>, (2) from all or any part of \<from set\>, and (3) to all or any part of \<to set\> and \<three set\>" [LM 4/69]. This operation takes arbitrary span-sets as input and returns matching links — which requires an index from content addresses to link endsets.

**The performance guarantee that constrains the implementation:**

> "THE QUANTITY OF LINKS NOT SATISFYING A REQUEST DOES NOT IN PRINCIPLE IMPEDE SEARCH ON OTHERS." [LM 4/60]

This is not aspirational — it is a design constraint. A linear scan of all links would violate it. The system must index links by their endsets such that irrelevant links do not impose cost on queries.

**The user-facing promise that requires it:**

> "The reader should be able to ask, for a given document or place in the document, 'What connects here from other documents?'— and be shown all these outside connections without appreciable delay." [LM 2/46]

"Without appreciable delay" for backlink discovery across the entire docuverse requires indexed access, not scanning.

**The back-end responsibility:**

> "A Xanadu link is a connective unit, a package of connecting or marking information. It is owned by a user. It is put in by a user (or a front end), and thereafter maintained by the back end through the back end's inter-indexing mechanisms." [LM 4/41]

Nelson explicitly names "inter-indexing mechanisms" as the back end's responsibility. The index is not optional infrastructure — it is part of what the back end *is*.

**The data structure designed for it:**

> "His new method would allow linkages to keep up with all changes. It was instantaneous and permanent and could grow indefinitely. All changes, once made, left the file remaining in canonical order, which was an internal mandate of the system." [LM 1/34]

Barus's linking enfilade ("the eye in the pyramid") was specifically designed to make this index efficient and scalable — "efficiently ever-linkable" [LM 1/34].

### Atomicity: Implied but Not Explicitly Specified

Nelson does not use the term "atomic" or discuss transaction semantics. However, two properties he does require strongly imply atomic index updates:

**1. Canonical order after every change:**

> "All changes, once made, left the file remaining in canonical order, which was an internal mandate of the system." [LM 1/34]

"An internal mandate" — not a goal but a requirement. After any change (including MAKELINK), the system must be in canonical operating condition. A link that exists but is not yet indexed would violate this, since FINDLINKSFROMTOTHREE would fail to return it.

**2. Server-level consistency invariant:**

> "A server's network model, from the null case on up, is at all times unified and operational; whatever information moves between servers is assimilated at once to its overall structure, leaving each server in canonical operating condition." [LM 4/72]

"At all times unified and operational" describes an invariant, not an eventual-consistency target.

**What Nelson does NOT specify:**

- Concurrent modification semantics (what happens if two users create links simultaneously)
- Read-after-write guarantees across servers
- Whether "canonical order" permits a brief window of inconsistency during a single operation
- Isolation levels between concurrent FINDLINKS and MAKELINK operations

Nelson's session model section [LM 4/79] acknowledges that "Private documents. (Currently all documents are visible to all users.)" — suggesting XU.87.1 had a single-user simplification that made concurrency moot. He mentions future "barrel-roll shared search model which repeatedly crosses the address space on behalf of all a server's users simultaneously" [LM 4/59], but this addresses search scheduling, not transactional atomicity.

### Summary

| Question | Answer | Strength of evidence |
|----------|--------|---------------------|
| Must the system maintain a complete index from content to links? | **Yes** | Explicit — required by FINDLINKSFROMTOTHREE semantics and the 4/60 performance guarantee |
| Must the index cover all three endsets? | **Yes** | Explicit — search operates on home, from, to, and type simultaneously |
| Must updates be atomic with link creation? | **Strongly implied** | The "canonical order" invariant [1/34] and "at all times unified and operational" [4/72] leave no room for a state where a link exists but is not indexed — but Nelson never discusses the transactional mechanics |

The index is a first-class architectural requirement. Atomicity is a consequence of the consistency invariants Nelson imposes, rather than something he specifies directly as a transactional property.
