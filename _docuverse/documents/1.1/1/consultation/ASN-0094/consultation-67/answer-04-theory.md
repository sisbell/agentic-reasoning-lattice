## Question 4 [theory]

> Did the Xanadu design intend duplicate retractions of the same target to produce one logical retraction (set semantics) or accumulate as distinct audit events (multiset semantics)?

# Retraction Semantics in Xanadu Design

**Key finding: Nelson does not directly address the question of duplicate retractions of the same target in the curated material.** The term "retraction" itself does not appear in the verified sources. Nelson discusses related but distinct mechanisms: withdrawal, deletion, peremptory challenge, and supersession. The architectural pattern across these mechanisms is consistent and points toward a layered answer.

## What Nelson Does Specify

**DELETE produces a STATE, not a counter.** The diagram on page 4/9 shows "DELETED BYTES" as a valid document state — content is either "not currently addressable" or it is. There is no notion of being "more deleted":

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" — 4/9

The same model applies to DELETED LINKS (4/9).

**Links and operations are recorded distinctly in append-only storage.** Each operation enters the chronological record:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes [flow] into the storage system, filed, as it were, chronologically." — 2/14

**Links never coalesce based on target.** Each link is a first-class owned object at its own address, even when multiple links point at the same target:

> "The links designated by a tumbler address are in their permanent order of arrival." — 4/31

Supersession links are explicitly designed to permit multiple independent claims about the same target, each owned by its creator (see `_docuverse`-equivalent in concept docs: `concepts/supersession-authority.md`). The Author link analog is explicit:

> "Note that the Author link can also be used from outside a document to claim that the author is really someone else." — 4/52

## The Layered Architectural Pattern

Nelson's design splits cleanly into two layers, and both must be answered:

| Layer | Semantics | Evidence |
|-------|-----------|----------|
| **Audit / event record** | **Multiset** — each operation recorded distinctly | Append-only storage (2/14); links keep "permanent order of arrival" (4/31); multiple supersession/author claims coexist as distinct owned objects (4/52) |
| **Current effect on target state** | **Set** — target is retracted or it isn't | DELETED is a state, not a count (4/9); withdrawal is a status of the document, not a number (2/43) |

This mirrors the Istream/Vstream split that pervades the architecture: history accumulates monotonically (multiset), while the present view is a state (set).

## The Specific Gap

What Nelson does **not** specify in the verified material:

1. Whether identical-target retractions (e.g., two peremptory challenges of the same John Doe document, or two withdrawal-due-process events on the same publication) coalesce
2. Whether the "lengthy due process" for withdrawal (2/43) accumulates challenges as evidence or treats them as deduplicated
3. Whether redundant DELETE on already-deleted Vstream content is a no-op or a distinct audit event

These are exactly the kind of edge cases Nelson tended to leave to implementation — he sets the principles (preservation, ownership, accountability) and leaves operational details to the FEBE/BEBE designers.

## Recommended Reading

NEED_RAW: 2/43-2/45 (raw pages 123-125, withdrawal due process), 2/60 (raw page 140, peremptory challenge mechanics), 4/9 (raw page 176, DELETED state diagram in full context), 4/41-4/52 (raw pages 208-219, link uniqueness and ownership). If Nelson addresses duplicate-operation semantics anywhere, it would be in the withdrawal procedure on 2/43-2/45 or the link-search rules on 4/58-4/60.

## My Reading of Design Intent

Given the consistent architectural pattern, the design intent appears to be: **multiset at the audit layer, set at the effect layer.** Two retractions of the same target should be recorded as two distinct, owned, addressable events (consistent with append-only storage and the way links are treated), but the resulting state of the target is a single "retracted" status. This preserves attribution and accountability for each retracting actor while keeping the target's current state coherent — which matches Nelson's broader pattern of making social claims visible and disputable rather than collapsing them into anonymous system facts.
