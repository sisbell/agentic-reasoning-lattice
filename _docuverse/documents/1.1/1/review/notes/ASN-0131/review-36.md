# Review of ASN-0131

This is a mature note; all sixteen claims (RE-DEF through RE-CWP) check out on their own terms. I verified the worked instance (image `{a₂}`, the four touch tests, `RE = {(1,e₁)}`), the union-distributivity proof, the `sel = findlinks_V ∩ addressable` identity, and the RE-CWP weakest precondition (including the `R = ∅` collapse to `RE = ∅`). The retraction sole-bearer biconditional and its forward/backward halves are sound under the stated hypotheses. Two issues remain, both in the stability section's supporting prose.

## REVISE

### Issue 1: "both gains and loses" overstates the image's response to a shift

**ASN-0131, "Stability: the answer as the document is edited" (insert/delete paragraph)**: "content the region held is carried off to a displaced position — possibly out of `W` — while the positions it vacates take on content displaced in from an adjacent position (from lower positions under an insert, from higher ones under a delete …). So the fixed region's image *both gains and loses* I-addresses; it swings, non-monotonically".

**Problem**: This is the configuration-dependent below-region case asserted as universal, and the mechanism is misattributed for insert. Take `Σ.M(d): [1,1]↦a₁, [1,2]↦a₂, [1,3]↦a₃`, region `W = {[1,2]}`, and an insertion at `p = [1,2]` of width `1`. By I3 (PostInsertionShift, ASN-0082) the content at `v ≥ p` moves up: `[1,3]↦a₂`, `[1,4]↦a₃`, and `[1,2]` is *vacated* (I3-V) — the note itself stresses the gap-fill is "a separate content-placing step, not part of the primitive." So under the shift primitive `W ∩ dom(Σ'.M(d)) = ∅`: post-image `∅`, pre-image `{a₂}` — **pure loss, no gain**. A gain into a fixed `W` requires content shifting up *from below `W`*, i.e. the insertion point below the region; an insert at or inside the region only carries `W`'s own content upward and out. Correspondingly, "the positions it vacates take on content displaced in from … lower positions under an insert" misnames the actors: the *vacated* gap positions are not backfilled by the shift at all; only positions *above* the gap receive down-shifted content, and that is a gain to the image only when the donor lay below `W`.

**Required**: State the property at the granularity that holds — the shift family is non-monotone *as a class* (an edit may gain, lose, or both, depending on its position relative to the region), in contrast to the weakly-monotone `K.μ⁺`/`K.μ⁻` — and either drop the per-edit "both gains and loses" or restrict it to the insert-below-region / delete-into-region case with the boundary case (region coincident with the insertion gap → pure loss under the primitive) acknowledged. Correct the insert mechanism so the vacated gap is distinguished from the above-gap positions that receive shifted content. (Note also that even the gained *fresh* content of a full insert, being a new K.α allocation, is excluded from a tight endset's coverage by LP19a — so for tight endsets the "gain" need not surface in `RE` at all, which the "RE tracks the swing" framing further glosses.)

### Issue 2: defensive meta-prose around the `Θ` disjointness hypothesis (anti-bloat)

**ASN-0131, "Under retraction" (the `Θ` paragraph)**: "The type-set `Θ` is the slot that same argument does *not* reach — and here we must not overclaim. … Nor does ASN-0086 confine `Θ`'s spans to unit depth, and this is decisive: … so \"exactly as the worked instance seated `θ`\" (whose `e₃` span *was* unit-depth) does not carry over to an arbitrary `Θ`."

**Problem**: The underlying point is correct and worth keeping (a wide type span's coverage can reach content even when its start lies outside content, so `coverage(Θ) ∩ dom(Σ.C) = ∅` is a hypothesis, not a theorem). But it is delivered through reviser-drift framing — "here we must not overclaim," "this is decisive," and most tellingly a *quoted-and-rebutted* phrase ("exactly as the worked instance seated `θ`") that corrects a formulation no longer present in the text. This is essay content explaining why an earlier draft was wrong rather than stating the current fact; the precise reader must work past it to extract the one operative sentence.

A second, smaller instance of the same pattern sits two paragraphs down (retraction backward-half): R0a (FlatLinkDomain) is invoked to get `ℓ ⋠ ℓ'` and then R-Scope (SingleTupleScope) to confine the nullification to `{ℓ}` — but R-Scope's conclusion `{t : ℓ ≼ t} ∩ A_rel^{Σ'} = {ℓ}` already delivers `ℓ ⋠ ℓ'` for every other store element, so the R0a step is redundant for this argument.

**Required**: Reduce the `Θ` passage to the fact and the deferral — e.g. "`coverage(Θ) ∩ dom(Σ.C) = ∅` is a construction hypothesis, not a theorem: `Θ`'s spans may be wide, and a wide span's coverage can include content even when its start lies outside it (Open Question 6)." Drop "must not overclaim," "this is decisive," and the rebuttal of the unstated prior phrasing. In the backward-half, cite R-Scope alone (or R0a alone) for the confinement rather than both.

## OUT_OF_SCOPE

None. The seven Open Questions defer their topics as questions, not claims, and the note makes no specification for any out-of-scope operation; the contrasts with FINDLINKSFROMTOTHREE and the use of `findlinks_V`/ASN-0127 are citations and distinctions, not rebuilds.

VERDICT: REVISE
