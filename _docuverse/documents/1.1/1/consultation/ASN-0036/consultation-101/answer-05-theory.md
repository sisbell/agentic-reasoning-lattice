## Question 5 [theory]

> Did the two-stream architecture intend referential integrity (every V-reference resolves) to hold universally at every state, or only at quiescent boundaries between operations — and is mid-operation violation a permitted intermediate condition?

Looking at this question carefully against what's in *Literary Machines*:

## My intent: universal referential integrity at the observable level

The two-stream architecture was designed so that V-references *always* resolve. The mechanism makes mid-operation violation structurally impossible at the user-observable level, because:

1. **Istream is append-only**, never destructive. Content lives at its I-address forever:
   > "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

2. **V→I is a mapping, not a copy.** The Vstream is a view onto permanent content. Editing changes the mapping, not the targets. "Deletion" removes the V-mapping but the I-content persists:
   > "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

3. **Internal volatility is hidden from the front end.** This is the closest I came to addressing your question explicitly:
   > "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." [LM 4/11]

That "constantly changing... front-end is unaware of this" passage is the strongest evidence of design intent: whatever transient states exist internally during reorganization, **the front end must never observe a broken V-reference**. The invariant is presented as universal *from outside*.

4. **At the network level, the same posture is taken**:
   > "Each server contains a continuously valid model or subrepresentation of the entire docuverse... leaving each server in canonical operating condition with a slightly improved map of what is elsewhere." [LM 4/72]

"Continuously valid" and "canonical operating condition" describe an always-on invariant, not a quiescent one.

## What I did *not* specify

I did not formalize transaction boundaries, atomicity guarantees, or operational semantics for intermediate states inside an operation. The FEBE command descriptions (INSERT, DELETE, REARRANGE, COPY at [LM 4/66-4/67]) state pre/post conditions but not mid-operation invariants. Whether the implementation achieves universal integrity via copy-on-write, log-append-then-publish, or some other mechanism is left to the implementor — what's *required* is that no front-end observer ever sees a dangling V-reference.

## Direct answer

**Intent: universal.** Every V-reference should resolve, at every observable state. The append-only + V-as-mapping design makes this achievable without explicit transaction machinery, because the I-targets never disappear — the V-mapping is the only thing that changes, and it changes from one consistent state to another.

**Mid-operation violation is not a permitted observable condition.** Internal storage reorganization may be in flux ("constantly changing"), but [LM 4/11] makes clear the front end must not see this. If your implementation cannot guarantee atomic visibility of V-mapping updates, that's an implementation defect against my intent, not a license.

NEED_RAW: 4/61-4/67 (FEBE command pre/post conditions), 4/72-4/75 (BEBE consistency language around "continuously valid") — to verify whether I said anything more specific about transactional semantics that didn't make it into the curated summaries.
