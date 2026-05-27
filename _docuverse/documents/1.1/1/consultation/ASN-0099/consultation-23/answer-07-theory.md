## Question 7 [theory]

> Is "without appreciable delay" a quoted phrase from Literary Machines or another Nelson source — and if so, does it carry any timing commitment beyond "the next query after K.λ commitment reflects the link," or is it purely motivational framing for the reader experience?

Yes, "without appreciable delay" is a verbatim phrase from Literary Machines 2/46, in the context of backlink discovery:

> "The reader should be able to ask, for a given document or place in the document, 'What connects here from other documents?'-- and be shown all these outside connections without appreciable delay." [LM 2/46]

**What it commits to:** Interactive responsiveness for the user experience of asking "what links here?" — it's establishing that backlink lookup must feel immediate, not batch-processed or deferred. This pairs with my related design constraint at LM 4/2:

> "Perhaps the most important thing, and certainly the hardest part to believe, is that everything on such a network-- any subset, substructure or grouping-- can come to the user immediately, even as the aggregation grows to tremendous size." [LM 2/57]

And the "soft corridor" performance commitment at LM 4/2 — logarithmic, not linear, slowdown as the docuverse grows.

**What it does NOT commit to:** Any specific transaction-visibility semantics. I never wrote about commit barriers, K.λ semantics, or "next query after commitment reflects the link" — that language is foreign to my specification. My phrase is a *user-experience* guarantee about interactive feel, not a *consistency model* about when writes become visible to subsequent reads.

So treat "without appreciable delay" as:
1. **Binding** on response latency for backlink queries (interactive, not batch)
2. **Binding** on the soft-corridor scaling commitment (it must stay fast as the system grows)
3. **Silent** on commit-visibility ordering — that's implementation territory I left to the back end

If your K.λ commitment model makes the link visible to the next query, that satisfies my intent. If it required a perceptible wait or a separate "refresh" step before backlinks appeared, that would violate 2/46. The phrase polices the *floor* (must feel responsive), not the *ceiling* (doesn't mandate stronger-than-needed consistency).
