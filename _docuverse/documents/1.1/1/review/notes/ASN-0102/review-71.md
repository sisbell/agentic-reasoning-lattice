# Review of ASN-0102

The operation's correctness machinery is sound — X1 forces shared reference through S3★, the X16 tiling closes density/disjointness across all `p ∈ [1, n_S+1]`, and the five worked examples genuinely witness distinct claim branches (cross-origin non-merge, self-transclusion snapshot, empty-subspace pin, append, coalescing). The findings below are accretion the `review-mode.anti-bloat` classifier targets: defensive prose that survived the recent PC3/J1'★ reworks.

## REVISE

### Issue 1: PC3 carries defensive projector-distinction meta-prose
**ASN-0102, Precondition PC3**: "The reading runs from the placement obligation to the V-position subspace — a content image forces an `s_C` slot — not from the copied address's `subspace_I` (which is an image-routing fact discharged in the `wp` computation below, over distinct objects: the V-position projector `subspace(v) = v₁` ranges over `dom(M(d))`, the address projector `subspace_I` over `dom(C)`)."
**Problem**: The store-disjointness argument three sentences earlier already establishes `S = s_C` cleanly. This trailing sentence explains what the reading is *not* and distinguishes two projectors the argument never conflates — a misreading the reader was not at risk of making. It also forward-defers to the `wp` computation, which re-derives the same S3★ obligation over the same three position-classes. The reader must skip past it to continue.
**Required**: Cut the "The reading runs from..." sentence. State PC3 as `S = s_C` with the store-disjointness justification; let the `wp` computation carry the S3★ discharge once.

### Issue 2: The `wp` statement repeats the same "not X but Y" pattern
**ASN-0102, wp(COPY, S3★)**: "(using `dom(Σ'.C) = dom(Σ.C)` by X1; the relation is equality, not containment — these are exactly the new mappings S3★ constrains, and they are routed to `dom(Σ.C)` because PC3 fixes their subspace to `s_C`)."
**Problem**: "the relation is equality, not containment" is a defensive clarification of a step that is already unambiguous from the displayed formula. Same accretion shape as Issue 1 — a parenthetical forestalling a misreading rather than advancing the derivation.
**Required**: Reduce to the load-bearing citations (X1, PC3); drop the equality-vs-containment aside.

### Issue 3: J1'★ discharge mixes blame-assignment essay into a proof slot
**ASN-0102, X14, J1'★ branch**: "leaving COPY's recording blameless" ... "the *offending step is that contraction, not COPY*" ... "COPY writes `(a, d)` only with `a` resident at `Σ'`."
**Problem**: The substantive content is correct — a COPY-then-K.μ⁻ stranding makes the *composite* invalid, so COPY's step never grounds a violation. But the argument is delivered as repeated blame-attribution prose ("blameless," "offending step," restated three times across the residence-destroyed paragraph and the closing sentence). The same point is made in the residence-preserved bullet, the residence-destroyed bullet, and the wrap-up. Two of the three restatements can go.
**Required**: State once: COPY records `(a,d)` only with `a ∈ ran_{s_C}(Σ'.M(d))`; any `R_clo`-stranding arises solely from a later K.μ⁻ removing `a`, which invalidates the composite at that step. Remove the duplicated blame restatements.

## OUT_OF_SCOPE

The four Open Questions (re-displacement discoverability, transitive containment when a referencing document is itself a source, time-varying views, identity when the allocating document is unreachable) correctly defer to future ASNs and are already marked as open — no action needed.

VERDICT: REVISE
