# Review of ASN-0131

I checked the definitions and every introduced claim for rigor before running the anti-bloat pass. The mathematics is sound: RE-NCD's separator-zero argument is correct; RE-ADDR's prefix-antichain reasoning holds; RE-UDIST factors `touch_W` cleanly out of the region-independent pool `Avail(Σ)`; the RE-UDIST-∩ `⊆`/`⊉` split (with both the non-injective and the *injective* split-witness counterexamples) is correct; RE-CWP's weakest precondition reduces correctly to the `Δ`/`I_R` condition; and the worked instance's coverage computations (the width-2 span reaching `{a₂, a₃}`, the clipping-shrinks-to-`{a₂}` illustration) are accurate. The retraction argument's reliance on `coverage(Θ) ∩ dom(Σ.C) = ∅` is genuinely load-bearing (absent it, the emitter `b` re-witnesses the `(3, Θ)` pair), and the note is honest about it being a hypothesis. No correctness defects.

The findings below are the accreted-prose issues the anti-bloat classifier asks for.

## REVISE

### Issue 1: The Θ-disjointness hypothesis and its "b surfaces nothing" consequence are stated three times across two adjacent paragraphs

**ASN-0131, §Stability ("Under retraction")**: The consequence is first given as a standalone two-sided statement —

> "*Under* this hypothesis `coverage(Θ) ∩ dom(Σ.C) = ∅` the emitter `b` surfaces nothing against a content image `I ⊆ dom(Σ.C)`, so a retraction's *net* effect on `RE` is removal only. *Absent* it, `b`'s type-slot `Θ` could meet the content image and surface the fresh pair `(3, Θ)`... the forward direction of the stability result below therefore rests on the hypothesis."

— and then re-derived twice in the very next (deduplication) paragraph:

> "Under the net-removal-only hypothesis `coverage(Θ) ∩ dom(Σ.C) = ∅` — adopted for this result, its sole exception flagged above — that pair fails the touch test against a content image, so `b` surfaces nothing and re-witnesses no pair the answer carries."

> "...`ℓ` leaves `addressable` permanently (just shown) and, under the hypothesis, the emitter `b` surfaces nothing, so neither keeps `(i, e)` alive."

**Problem**: "under the hypothesis, `b` surfaces nothing" is asserted three times in immediate succession. The standalone "*Under*/*Absent*" paragraph pre-announces exactly the conclusion the deduplication paragraph then re-establishes for its own forward-half argument, and the deduplication paragraph states it twice internally. A reader following the dedup argument has to re-absorb the same hypothesis-consequence each time it is invoked — the "two paragraphs say the same thing in different words" pattern.

**Required**: Keep the declaration (earlier paragraph) that `coverage(Θ) ∩ dom(Σ.C) = ∅` is a construction hypothesis routed to Open Question 6, and state the "under hyp ⇒ `b` inert ⇒ net removal; absent ⇒ `b` adds `(3, Θ)`" consequence **once**. Let the deduplication paragraph back-reference that single statement rather than re-deriving "b surfaces nothing" twice.

### Issue 2: Case-bookkeeping framing precedes the substance in the self-retraction paragraph

**ASN-0131, §Stability ("Under self-retraction")**: "One `K.λ` shape falls between the two emission/retraction cases and is covered by neither: ... Being a retraction (`K ~ Θ`) it is not the non-retraction emission case above, and having emitter = target it is not the retraction case below — which withdraws a *pre-existing* `ℓ ≠ b` — so neither argument reaches it; yet it is inert."

**Problem**: The case itself (a self-emit `Nullify` whose to-set targets its own emitter address) is genuine, not excluded by any precondition, and its treatment must stay — but roughly two sentences justify *why this paragraph exists* (which prior cases fail to reach it) before the substantive content arrives ("born-nullified emitter; R-Scope confines the effect to `b`; `addressable` unchanged; image framed"). This is the "defensive justification / exhaustiveness claim" meta-prose pattern.

**Required**: Compress the case-coverage framing to a clause (e.g., "The self-emit `Nullify` — emitter = target — is inert:") and lead with the inertness argument. Keep the case.

## OUT_OF_SCOPE

(none — the note defers FINDLINKSFROMTOTHREE cross-end pairing, multiplicity, rendered answers, the structural intersection-equality condition, non-co-resident link stores, type-against-content matching, and link-subspace regions to Open Questions 1–7, and it cites ASN-0127's image / existence-discovery machinery and ASN-0086's retraction machinery rather than rebuilding them.)

VERDICT: REVISE
