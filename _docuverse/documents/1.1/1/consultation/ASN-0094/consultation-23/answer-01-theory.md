## Question 1 [theory]

> Was retraction intended to be idempotent in the duplicate-target-Nullify sense (so a second Nullify of an already-retracted address is a no-op), or are repeated retractions of the same target intended to be distinct, recorded audit events?

# Retraction Semantics: Idempotent vs. Audit Events

**The term "Nullify" does not appear in the curated Literary Machines sources I have access to.** This appears to be implementation terminology, not Nelson's own language. Nelson's vocabulary around retraction uses terms like "withdraw," "remove," "supersede," and "peremptory challenge."

That said, Nelson's design intent provides strong philosophical signals, though he does not directly address the specific idempotency-vs-audit question.

## What Nelson Does Say

**1. The presumption is against retraction entirely:**

> "It is in the common interest that a thing once published stay published, as in the world of paper. Other readers and users will come to depend on its accessibility. Consequently its author may not withdraw it except by lengthy due process." [LM 2/43]

**2. Withdrawal is a "lengthy due process" — implying recorded, deliberate events, not casual operations.**

**3. The system preserves all prior states via historical backtrack:**

> "DELETED LINKS (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

**4. Removal by peremptory challenge is framed as a discrete legal-style act:**

> "Consider libelous or uncomplimentary John Doe graffiti defaming specific individuals. If John Doe is not available, the affected individual must be able to effect removal of the materials by peremptory challenge." [LM 2/60]

## What This Implies (Inference, Not Direct Quote)

Nelson's overall design philosophy strongly favors **distinct audit events** over silent no-ops:

- **Historical backtrack is foundational** — the system records what happened and when, not just current state
- **Withdrawal is "due process"** — process implies recording, not idempotent erasure
- **The cash register model** [LM 5/13] shows Nelson's preference for ever-incrementing counters that record activity
- **Append-only storage** [LM 2/14] is the architectural pattern throughout

A second retraction of an already-retracted address being silently dropped would conflict with the "lengthy due process" framing and the audit-preserving character of historical backtrack.

## NEED_RAW

Nelson does not directly address whether retraction operations are idempotent or whether repeat retractions produce distinct audit events. To answer authoritatively, I would need to examine:

- **NEED_RAW: 4/61-4/79** (FEBE protocol command specifications — to see if any retraction-style commands have specified idempotency semantics)
- **NEED_RAW: 5/13-5/21** (Storage Vendor contracts and withdrawal mechanics — for legal-procedural framing)
- **NEED_RAW: 2/43-2/45** (publishing permanence and withdrawal due process — for the full unredacted treatment)
- **NEED_RAW: 6/1-6/6** (appendices — possible additional protocol details)

If "Nullify" is an implementation term that post-dates Literary Machines (e.g., from udanax-green or later spec work), the answer may not exist in Nelson's writings at all and must be derived from the design intent rather than cited from him directly.
