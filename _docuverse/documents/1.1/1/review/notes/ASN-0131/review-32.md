# Review of ASN-0131

I worked through the core definition, the soundness/completeness biconditional, the worked instance, union-distributivity, the contraction weakest-precondition (RE-CWP), and the retraction-stability iff (RE-RET). The mathematics is sound throughout — the e₃ field-agreement argument, the `Avail(Σ)` factoring behind RE-UDIST, the D-CWP bridge in RE-CWP, and the R-Scope/R0a/R6a chain behind RE-RET all check out, and the worked instance genuinely exercises every distinctive postcondition. The honest hypothesis-management around `coverage(Θ) ∩ dom(Σ.C) = ∅` (routed to OQ6 rather than silently assumed) is exactly right.

The issues are localized to one paragraph: the insert/delete stability discussion.

## REVISE

### Issue 1: Path-not-taken justification in the insert/delete paragraph

**ASN-0131, "Stability ... Under editing of the queried document"**: "The two are not competing descriptions of one transition" and "(Were the shift instead decomposed into atomic `K.μ` steps, the existing-content motion would live in a domain-preserving `K.μ~` component and route through F-IMG-SWING; we do not take that route.)"

**Problem**: This is meta-prose defending a modeling choice rather than advancing the stability conclusion. The reader following "does RE track insert/delete?" must skip past the reconciliation of two foundation models and an explicit path-not-taken parenthetical to reach the only load-bearing claim — that the image of a fixed region swings, so RE tracks it non-monotonically. The note carries the `review-mode.anti-bloat` classifier precisely for this accretion of justificatory prose around foundation interfaces.

**Required**: State the operative fact directly — insert/delete displace content through the region's fixed positions (I3/D-SHIFT), so the image of a fixed `W` swings and RE tracks it non-monotonically (RE-IDENT keeps each surfaced endset's spans fixed). Drop the "not competing descriptions" reconciliation and the decomposition parenthetical.

### Issue 2: "Freshly inserted content" is not delivered by the cited displacement primitive

**ASN-0131, same paragraph**: "We take insert and delete here as ASN-0082 displacement primitives in their own right, not as `K.μ` composites. The foundation realises them as displacements (I3 PostInsertionShift, D-SHIFT, ASN-0082)" — then: "the positions it vacates take on other content (freshly inserted content, or content displaced in from elsewhere in `d` ...)".

**Problem**: The two halves are internally inconsistent. ASN-0082's I3 models only the make-room shift: I3-V (PostInsertionVacating) removes the gap `[p, shift(p,n))` from the post-state domain, and I3-CS (PostInsertionSubspaceClosure) states that *every* post-state subspace-S position is either preserved-left (`v < p`) or shifted-right (`v = shift(u,n)`) — there is no slot for freshly inserted content. So under the note's own insistence that insert is the displacement *primitive* "not a `K.μ` composite," nothing supplies the "freshly inserted content"; the gap is vacated, not filled. A full INSERT is the I3 displacement *plus* a content-placing extension — i.e. exactly the composite the note disclaims. (The other listed source — "content displaced in from lower positions" — *is* delivered by I3, since a post-state position `q ≥ shift(p,n)` holds `M(d)(u)` with `u` below `q`; the swing conclusion survives on that source alone. Only the fresh-content attribution is unsupported.)

**Required**: Either drop the "not as K.μ composites" framing and acknowledge a full insert is I3-displacement composed with a gap-filling extension, or restrict the cited source to what I3/D-SHIFT actually deliver (content displaced in from adjacent positions), so the attribution matches the foundation primitive named.

## OUT_OF_SCOPE

### Topic 1: Type-slot match against a content region (OQ6) and link-subspace regions (OQ7)
**Why out of scope**: Both are genuinely new territory and the note correctly defers them. The retraction-stability result properly carries `coverage(Θ) ∩ dom(Σ.C) = ∅` as an explicit hypothesis (not a hidden assumption) and names its sole remaining exception; OQ7's note that a link-subspace image adds a retraction-emitter term to RE-RET is the right forward marker. No revision needed for these.

VERDICT: REVISE
