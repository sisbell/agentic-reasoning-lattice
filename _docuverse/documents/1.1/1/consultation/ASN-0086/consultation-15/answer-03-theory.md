## Question 3 [theory]

> In Nelson's link/retraction design, does a retraction belong to the same document as the link it retracts, or is the retraction's ownership independent of its target?

I am Ted Nelson. Let me answer this carefully.

## The Answer Depends on What You Mean by "Retraction"

The term "retraction" is not one I use as a distinct link type in the curated material above. The closest concepts I do address are: **link deletion** (administrative removal by the owner), **supersession links** (declaring one document replaces another), and **document withdrawal** (which requires "lengthy due process").

NEED_RAW: 4/52-4/55 — to verify whether "retraction" appears as a specific link type alongside the others I enumerate (Connection, Comment, Counterpart, Supersession, etc.) on those pages.

## What My Principles Establish

That said, the architecture is clear and consistent. **A retraction, if implemented as a link, has its own home document, which determines its ownership — independent of what it points to.**

This follows from the link ownership principle:

> "A link need not point anywhere in its home document. Its home document indicates who owns it, and not what it points to. Conversely, links connecting parts of a document need not reside in that document." `[LM 4/12]`

> "A Xanadu link is a connective unit, a package of connecting or marking information. **It is owned by a user.** It is put in by a user (or a front end), and thereafter maintained by the back end through the back end's inter-indexing mechanisms." `[LM 4/41]`

## Two Distinct Scenarios

**1. The link's owner withdrawing their own link** (link deletion):

The owner of the link's home document — and only that person — may delete it. "DELETED LINKS (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" `[LM 4/9]`

**2. A third party declaring a link or document retracted:**

By the same mechanism that lets an Author link be "used from outside a document to claim that the author is really someone else" `[LM 4/52]`, anyone may create a retraction link at *their own address* pointing at someone else's link or document. That retraction lives in the creator's home document, owned by the creator — entirely independent of the target's owner.

## The Principle Served

This is the deeper point: **claims live where their authors live.** A retraction by the original link's owner is authoritative because the owner controls their link. A retraction by a third party is a *claim* — visible, attributable, rebuttable — but architecturally identical. The system doesn't enforce authority; it makes claims transparent and traceable to their source.

A retraction is never imprisoned inside the document it concerns. That would violate link freedom and the libertarian character of the system: "each user is free to link to anything privately or publicly" `[LM 2/43]`.
