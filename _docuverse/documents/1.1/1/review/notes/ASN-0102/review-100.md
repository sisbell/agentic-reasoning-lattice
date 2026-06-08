# Review of ASN-0102

This is a thorough and largely rigorous note. The tiling argument (X16), the wp reduction of S3★, the per-conjunct discharge of `ExtendedReachableStateInvariants` (X17), and the five boundary-exercising worked examples are exactly the depth the operation requires. Boundary cases (append `p=n_S+1`, empty subspace `n_S=0`, self-transclusion with overlap, coalescing merge) are all explicitly covered. My findings are confined to accretion flagged by the `review-mode.anti-bloat` classifier.

## REVISE

### Issue 1: X2 is a tautological restatement of X1, never consumed
**ASN-0102, "What is preserved" / Claims table**: "X2 (NoFreshAllocation). *A corollary of X1.* COPY consumes no previously-unallocated address: by X1, `dom(Σ'.C) = dom(Σ.C)`, so no address absent from `dom(Σ.C)` becomes present."
**Problem**: X2's content is exactly the `⊆` half of X1's `dom(Σ'.C) = dom(Σ.C)`. It introduces a named claim that adds nothing to X1. Tracing downstream, X3, X5, and X17 cite **X1** ("forced by X1", "COPY allocates nothing (X1)") and the freshness arguments in the examples cite X1 / `dom(Σ'.C)=dom(Σ.C)` directly. X2 is never invoked anywhere — it is a dead restatement. Under the anti-bloat mandate this is noise the reader must step past to confirm it carries no independent obligation.
**Required**: Delete X2 (and its table row), or, if a named "no fresh allocation" handle is genuinely wanted, fold it into X1's statement rather than carrying a separate corollary that duplicates it.

### Issue 2: X17 opening roadmap pre-states the SL-routing plan that the body then states again
**ASN-0102, X17**: opening — "We discharge them below, routing the provenance couplings (J1★/J1'★) through the unconditional write recorded by X14's (SL)." Immediately followed by — "By (SL), COPY's provenance write is *unconditional* … so only J1★/J1'★ require routing."
**Problem**: The roadmap sentence and the SL paragraph assert the same plan (route J1★/J1'★ through SL, J0 vacuous) in different words within the same section. The second statement is where the work begins; the first only previews it.
**Required**: Drop the roadmap clause and let the SL paragraph carry the routing statement once.

## OUT_OF_SCOPE

### Topic 1: Link-discoverability consequence of transclusion
COPY establishes `ran(Σ'.M(d)) = ran(Σ.M(d)) ∪ A`, from which it follows (via ASN-0098's projection/discoverability machinery, e.g. LP16) that links whose coverage includes a copied address become discoverable from `d` — the signature consequence of placement-by-reference. The depth standard names "link discoverability" as the canonical non-trivial wp. I am leaving this OUT_OF_SCOPE because the note's scope explicitly excludes "link semantics," and the wp standard is already satisfied by the non-trivial `wp(COPY, S3★)` computation. Flagging only to record that it was considered, not overlooked.

VERDICT: REVISE
