## Question 7 [theory]

> When a link is retracted, what invariant governs how much the count may decrease, and may it ever decrease by more than one per retraction?

## The Invariant: One Link, One Decrement

A retraction may decrease the count by **exactly one**, and never by more than one per retraction. This follows from three structural facts about how I designed links.

### 1. A link is a single, individually-addressed unit

Each link occupies one position in the docuverse, addressed by its order of arrival in its home document:

> "The links designated by a tumbler address are in their permanent order of arrival. A document includes only the links of which it is the home document." (4/31)

The link count of a document — what `RETRIEVEDOCVSPANSET` reports — is a count of these discrete units. A retraction targets one link by its address. Therefore it can remove at most one from the count.

### 2. A link's reach does not multiply its identity

This is the point most likely to confuse. A single link may touch many scattered places — its endsets are arbitrary span-sets:

> "We see from above that one end of a link may be on a broken, discontiguous set of bytes. This illustrates the endset: a link may be to or from an arbitrary set of bytes." (4/42)

But a link with a discontiguous from-set spanning three passages is still **one** link — one connective unit, one address. Retracting it decrements the count by one regardless of how many spans it embraces. Endset breadth is not link count.

### 3. Retraction does not cascade or renumber

When a link is withdrawn it enters a dormant state — it is not erased and it does not disturb its neighbors:

> "DELETED LINKS (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" (4/9)

Retracting link 2.5 leaves links 2.6 through 2.N exactly where they are — addresses are permanent order-of-arrival, so nothing renumbers. And because links are independent objects, retracting a link that other links *point to* (link-to-link) does not retract those dependent links — they merely point at a now-dormant address. So no single retraction can knock out more than its own one unit.

### Why this matters as a guarantee

Only the owner may withdraw what they own — "Only the owner has a right to withdraw a document or change it" (2/29) — and a link is owned via its home document. Each owner withdraws their own links, one discrete unit at a time. The count is therefore monotonic and well-behaved under retraction: down by one, never more.

---

**A note on scope of my sources.** Nelson's curated text establishes that links are discrete order-of-arrival units (4/31), that retracted links go dormant without renumbering (4/9), and that endsets may span discontiguously without changing link identity (4/42). The specific framing "the count decreases by exactly one per retraction" is my design-intent inference from those facts — Nelson does not state a per-retraction count invariant in those words, nor does he specify any batch-retraction operation. If you need to confirm there is no batch-deletion command that could decrement by more than one, that would live in the protocol pages — NEED_RAW: 4/61-4/70.
