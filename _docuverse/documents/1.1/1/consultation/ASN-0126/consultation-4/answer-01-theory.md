## Question 1 [theory]

> Was retraction designed to address a single target per operation, or is retracting several targets in one operation an intended capability?

## Mapping the question

"Retraction" is not Nelson's own term. In *Literary Machines* the operations that retract content are **DELETE** (removing content from a document's current arrangement) and **withdrawal** of a published document. I'll answer for DELETE, since that is the per-operation content-retraction primitive; withdrawal is a separate, document-level act.

## What the DELETE command specifies

The documented FEBE deletion command addresses a **single span** per invocation:

> "**DELETEVSPAN**: 'This removes the given span from the given document.' (4/66)"

Note both the singular phrasing ("the given span") and the command's own name — **VSPAN**, not VSPANSET.

This is a deliberate asymmetry within FEBE. Nelson generalized *other* operations to take multiple, possibly discontiguous regions, but not DELETE:

- **COPY** takes a spec-**set**: "The material determined by `<spec set>` is copied..." (4/67)
- **MAKELINK** endsets are span-**sets**, each "an arbitrary collection of spans, pointing anywhere in the docuverse." (4/43)
- **REARRANGE** operates on multiple cut-defined regions. (4/67)

So where Nelson intended multi-region operation, he said so explicitly (spec-sets, span-sets). The deletion command, as specified, does not carry that generalization — it takes one span.

## Where multi-target selection actually lives

Nelson's design does provide a uniform mechanism for naming several discontiguous targets at once — the **span-set / request-set**:

> "Note: if you want to designate a separated series of items exactly, including nothing else, you do this by a span-set, which is a series of spans." (4/25)

> "A request set is a set of spans, or spanset, presented to the back end in the FEBE protocol... The manipulation of request sets is an important aspect of what front-end functions do." (4/37)

But Nelson locates this machinery in the **front end / request-set layer**, not inside the DELETE primitive itself. The intended way to retract several scattered regions is for the front end to express them as a span-set and drive the (single-span) back-end operation accordingly — not for the back-end retraction command to natively consume multiple targets.

## Answer

On the evidence of the curated specification, **retraction was designed as a single-target (single-span) operation per invocation**. The DELETEVSPAN command takes "the given span" (4/66, singular), in pointed contrast to COPY, MAKELINK, and REARRANGE, which Nelson explicitly generalized to sets/regions. Multi-target retraction is achievable, but as a *front-end / request-set* composition over span-sets (4/25, 4/37), not as a built-in capability of the deletion primitive.

One caveat: a single span at the tumbler level can itself cover a whole subtree (an author, a document, a server with all its contents), so "one span" can still be a very large *contiguous* retraction. Discontiguous multi-region retraction in one shot is what falls to the span-set layer rather than to DELETE.

NEED_RAW: 4/66 — to confirm whether the raw DELETEVSPAN signature admits a span-set argument or strictly a single vspan; the curated quote reads as single-span, but the verbatim command grammar on the page would settle whether multi-span deletion was ever folded into the command itself.
