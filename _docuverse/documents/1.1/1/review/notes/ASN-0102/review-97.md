# Review of ASN-0102

I read the full operation, all five worked examples, and traced the invariant-discharge for the post-state. The mathematical content is sound: the wp(COPY, S3★) reduction is correct, the three-class tiling in X16 genuinely establishes S2/S8a/D-SEQ at the post-state, the J1★/J1'★/P4★/P4a chain through the RR routing closes, and the boundary cases (p=1, p=n_S+1, n_S=0, self-transclusion with displaced source, coalescing) are each exercised against a concrete table. I found no correctness gap and no non-foundation cross-ASN reference.

The findings below are the accretion patterns the `review-mode.anti-bloat` classifier asks me to surface.

## REVISE

### Issue 1: Document-ordering justification in the RR setup
**ASN-0102, "What invariants the completed operation must maintain" (RR introduction)**: "To discharge the boundary obligations that consume this write without re-deriving the same split three times, we factor the routing once."
**Problem**: This sentence justifies *why the document is structured* (factoring to avoid threefold repetition) rather than advancing the argument. It is the "prose justifies document ordering" pattern. The RR lemma's content — the carried/recorded partition of the post-state range — stands on its own; the reader does not need to be told it exists to avoid repetition. The same meta-framing appears at the source-designation section: "the evaluation point matters, and we settle it here once for the whole operation."
**Required**: Drop the organizational justification; state RR (the range partition and its two routes) directly, and pin pre-state resolution without the "once for the whole operation" framing.

### Issue 2: Proof-method asides in X5 and X8
**ASN-0102, X5**: "The claim needs no induction on chain length; one structural fact closes it." — and **X8**: "Here the inference needs the source's V-contiguity to close, so we spell it out."
**Problem**: Both are commentary *about* the proof (what technique is or isn't needed) sitting in front of the proof itself. The reader must skip past the meta-statement to reach the load-bearing step (the single-allocation-event fact in X5; the maximal-merge/V-contiguity argument in X8). "Needs no induction" and "so we spell it out" advance no reasoning.
**Required**: Open X5 directly with the structural fact (each address has one allocation event, fixed by its tumbler; COPY allocates nothing and rewrites no I-coordinate). Open the X8 within-reference case directly with the V-contiguity argument.

## OUT_OF_SCOPE

The four Open Questions (later re-displacement, reference-of-a-reference containment, time-varying views, identity under an unreachable allocator) correctly defer forward-looking territory and are placed in the Open Questions slot — no finding.

VERDICT: REVISE
