# Review of ASN-0102

## REVISE

### Issue 1: X8 restates X12's boundary-absorption conditions instead of deferring to it

**ASN-0102, X8 (RunFragmentation)**: "the whole-arrangement maximal merge (M12 of `Σ'.M(d)`) may reduce the count further at the two boundaries where the copied region abuts the surrounding arrangement: it absorbs the leading copied block into the unmoved predecessor iff that predecessor is I-adjacent, and the trailing copied block into the first displaced block iff that block is I-adjacent (X12)."

**Problem**: X12 (BoundaryAbsorption) is the dedicated claim for exactly this content and states the same leading/trailing iff-conditions in full a few paragraphs later. X8 both forward-references X12 *and* re-derives its substance — the "two paragraphs in different sections say the same thing" accretion pattern. X8's job is the block count; the boundary-absorption mechanics belong to X12 alone.

**Required**: In X8, state only that whole-arrangement merge may reduce the count further at the two abutment boundaries (X12) and stop; remove the restated iff-conditions.

### Issue 2: X7 and X16 independently derive the same copied/displaced range-disjointness

**ASN-0102, X7 (NonDestructivePlacement)**: "In last-component terms, the copied region occupies `[p, p+W)` and the displaced image occupies `[p+W, n_S+W]` — the shift carries every displaced slot to a last-component `≥ p+W`, while every copied last-component is `< p+W`, so no copied mapping can land on a surviving displaced one."

**Problem**: X16 (PostStateDensity) re-derives this identical disjointness as part of its full tiling (`[1,p) ∪ [p,p+W) ∪ [p+W,n_S+W]` with "no overlap ... no gap"). The copied-vs-displaced range disjointness is proved twice in different words. X7 needs it as a lemma for non-destruction; X16 owns the complete tiling.

**Required**: Let X16 be the single site for the tiling/disjointness and have X7 cite it ("copied `[v,v+W)` and displaced-image `[v+W,…)` ranges are disjoint by the X16 tiling"), or vice-versa. Do not derive the same interval split in both.

## OUT_OF_SCOPE

### Topic 1: The four Open Questions (later displacement, transitive containment-as-source, time-varying views, unreachable allocator)

**Why out of scope**: These concern subsequent operations acting on copied content and discoverability over time (LP-family territory, ASN-0098) — they are correctly posed as forward questions, not gaps in COPY's contract.

VERDICT: REVISE
