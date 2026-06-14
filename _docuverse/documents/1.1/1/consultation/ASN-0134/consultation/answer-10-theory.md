## Question 10 [theory]

> What is the minimal promise the design demands of any faithful realization, so that a writer's act of claiming space for new content can never silently overwrite space another writer claimed at the same time?

I'll examine the curated sources I have, then verify against the actual tumbler/forking pages since this question hinges precisely on the allocation mechanism.

The question is about **address allocation under concurrency** — what invariant prevents two writers' simultaneous "claims" of new space from colliding. Let me check the two load-bearing pages.

`★ Insight ─────────────────────────────────────`
The question decomposes into: (1) "claiming space for new content" = minting I-addresses on INSERT/APPEND/CREATE; (2) "silently overwrite space another writer claimed at the same time" = a concurrent allocation collision/reassignment. The answer lives in the **owned-numbers ("baptism") + fork-only growth** invariants — but Nelson never frames these *as* a concurrency guarantee, so the safety property is emergent, not stated.
`─────────────────────────────────────────────────`

Let me look at the actual pages for the baptism (4/17) and forking (4/20) mechanisms.
