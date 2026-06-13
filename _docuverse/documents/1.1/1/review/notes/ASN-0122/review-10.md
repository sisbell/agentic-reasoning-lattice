# Review of ASN-0122

The correspondence relation, the pair/report machinery, and every stability theorem check out. I reran the worked example end to end: `corr` has the three claimed elements; the maximal-pair decomposition is γ₁ (width 2) / γ₂ (width 1); the swap's tie-break on the shared first foot, the single-span window clip (γ₁ collapsing to one in-window pair), and the disjoint-window sharing detector all reproduce the stated results. X-T is correctly premised, and its instantiations are sound — X7(iii) discharges injectivity for the piecewise shift map explicitly (id on L, σ on R, images disjoint by D-DP(a)), and X6 cleanly separates "edit strikes an intermediate after its outgoing copy" (X5 indifference) from "before" (the edit's position map joins the composite). I found no correctness gap, no skipped boundary (empty operands, empty document, self-comparison, multi-document regions, fan-out, cross-document chains all handled), and no scope drift. The findings below are the anti-bloat trims the classifier asks for, plus one precision fix.

## REVISE

### Issue 1: Implementation-cache musing inside an abstract consequence
**ASN-0122, X5 (Locality), "Memorylessness":** "Equally, no auxiliary index may add or veto pairs: the specification pins the result entirely, so any cache or index an implementation keeps must be derived and exactly consistent, on pain of non-conformance."
**Problem**: The memoryless content of X5 is fully carried by the two preceding sentences (the relation consults present arrangements only; a contracted mapping contributes nothing). This sentence is implementation-conformance commentary about caches and indexes — and it pre-empts Open Question 4 ("What consistency contract must a derived correspondence index satisfy for cached reports to remain exact..."), which treats exactly this as open. It is prose to skip past, not reasoning to follow.
**Required**: Delete the sentence; the derived-index consistency question already lives in the Open Questions, and the abstract consequence does not need it.

### Issue 2: Interpretive paragraph restating X4's own corollaries
**ASN-0122, "Windows: Restriction Is Exact" (paragraph following the three corollaries):** "Comparing sub-extents reveals nothing new about content: X4 makes the windowed answer a restriction of the whole-extent answer. That is itself the discovery — correspondence is pointwise... What windows add is resolving power. They make the operation compositional and locally computable... and, as we will see for self-comparison, they are the instrument that switches the forced diagonal off..."
**Problem**: "Compositional and locally computable" restates the Compositionality corollary and X5; "reveals nothing new about content" restates the "No invention, no silent loss" corollary; "That is itself the discovery" is editorializing; "as we will see for self-comparison" is a forward deferral to X8. The one non-redundant point — correspondence is pointwise, so a window has no context to disturb — does not need a paragraph that re-derives the corollaries to carry it.
**Required**: Reduce to the single novel sentence (correspondence is pointwise / context-free; whole-document is the largest window) or remove. Drop the X8 forward pointer.

### Issue 3: Over-attribution in the chain-partition proof
**ASN-0122, X11(a):** "every element has at most one successor and at most one predecessor within the relation, by shift injectivity (TS2) applied per coordinate"
**Problem**: `succ` is a total function, so "at most one successor within the relation" is immediate and needs no lemma — `succ(e)` is one element, in `corr` or not. Only predecessor-uniqueness rests on TS2 (each coordinate's shift-predecessor is unique). Lumping both under "by TS2" mis-states which fact the lemma discharges.
**Required**: Separate the two — successor-uniqueness because `succ` is single-valued; predecessor-uniqueness by TS2 per coordinate (with `#u` equal across the feet by S8-depth, which TS2 requires).

## OUT_OF_SCOPE

None. The Open Questions defer n-way alignment, derived-index consistency, and the arrangement-presence basis appropriately; no excluded operation (version creation, document discovery, deletion comparison, etc.) is specified here.

VERDICT: REVISE
