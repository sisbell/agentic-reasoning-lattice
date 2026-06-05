## Question 5 [theory]

> Must the system guarantee that no endset is returned which fails to touch the region at all?

## Answer

Yes — but the guarantee is scoped to the **constrained** endsets, and it follows directly from Nelson's link-search satisfaction rule (the "AND of the ORs").

### The satisfaction rule

A link is returned only if it *satisfies* the request, and Nelson defines satisfaction per-endset:

> "A link satisfies a search request if one span of each endset satisfies a corresponding part of the request." [LM 4/58]

The curated `links` concept restates this structure as the **AND of the ORs**:

> "For each endset (from-set, to-set, type), at least one span must fall within the corresponding part of the request."

So the logic is: **AND across the endsets, OR across the spans within an endset.** For a link to come back, *each* endset must have at least one of its spans landing in the corresponding requested region.

### What this guarantees

This means the system does guarantee soundness with respect to the region you constrained: **no link is returned whose constrained endset fails to touch the requested region at all.** If you ask for links whose from-set touches region R, every returned link is guaranteed to have at least one from-set span in R. An endset that misses R entirely cannot satisfy "a corresponding part of the request," so the link as a whole fails the AND and is excluded.

### The two caveats

1. **Only constrained endsets are bound.** A request specifies parts for each endset (home-set, from-set, to-set, three-set). If you leave a part unconstrained (effectively "the whole docuverse"), then *any* span trivially satisfies it — so that endset is not guaranteed to touch any particular region. The guarantee applies to the regions you actually specify.

2. **An endset is a span-set, and only one span need touch.** Because an endset may be "a broken, discontiguous set of bytes" [LM 4/42], the rule requires only that *one* span of that endset touch the region. The endset as a whole touches; individual spans within it may lie elsewhere.

### Why precision matters to Nelson

This soundness is paired with a scalability claim about the *opposite* direction — irrelevant links never pollute or impede results:

> "THE QUANTITY OF LINKS NOT SATISFYING A REQUEST DOES NOT IN PRINCIPLE IMPEDE SEARCH ON OTHERS." [LM 4/60]

Together these establish the search contract: links that don't touch the constrained region are neither returned nor allowed to slow the search.

---

So: **for every endset you constrain, the system must return only links whose endset genuinely touches that region** — that is exactly what "one span of each endset satisfies a corresponding part of the request" enforces. It does *not* impose any touching requirement on endsets you leave unconstrained.
