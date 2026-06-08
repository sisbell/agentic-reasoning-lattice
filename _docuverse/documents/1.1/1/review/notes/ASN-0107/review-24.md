# Review of ASN-0107

## REVISE

### Issue 1: R3 conflates per-slot survival with whole-link counting

**ASN-0107, R3 (PartialSurvival)**: "A link with a partially-deleted endpoint remains counted while at least one address of the relevant endset's coverage still lies in the resolved request part... The link drops from the count only when all of its slot-`i` coverage has left every consulted arrangement — the empty-intersection boundary."

**Problem**: Both halves of R3 govern whole-link counting (`remains counted` / `drops from the count`) by the status of slot `i` alone. But `sat` is conjunctive across all three slots. A counted link can drop because a *different* slot `j ≠ i` lost its reach, while slot `i` is fully intact — contradicting "drops from the count only when all of its slot-`i` coverage has left." Symmetrically, slot-`i` survival is not sufficient for the link to remain counted. R3 is only correct under a single-slot restriction (the other two parts held fixed) — exactly R1's (P-slot) and R2's (P-slot₂). Unlike R1 and R2, R3 carries no such guard, so as stated it is false in the multi-slot contraction case the surrounding section admits.

**Required**: Add the single-slot precondition to R3 (parallel to P-slot/P-slot₂), or restate R3 as a claim about slot-`i`'s *contribution to satisfaction* rather than about whole-link counting.

### Issue 2: R2's parenthetical imagines an excluded case and forward-defers to R6, which does not treat it

**ASN-0107, R2 (ContentDeletionUnbounded)**: "(Without this restriction a single contraction on `d_q` can change `Q₁`, `Q₂`, and `Q₃` at once whenever `W₁`, `W₂`, `W₃` all draw positions from `d_q`; the multi-slot case is treated by R6, whose weakest precondition is conjunctive over all three slots and so accounts for a link at risk through more than one slot.)"

**Problem**: Two anti-pattern accretions in one parenthetical. (a) It elaborates the very case `(P-slot₂)` excludes ("Without this restriction...") — reviser drift imagining the case the precondition already removes. (b) It forward-defers to R6 with a claim that is not accurate: R6 gives the weakest precondition for *one link's survival*, not a count-level `Δnum_disc` characterisation of the multi-slot contraction. So "the multi-slot case is treated by R6" overstates what R6 delivers and leaves the multi-slot *count* change genuinely untreated while implying it is handled.

**Required**: Delete the parenthetical (the `(P-slot₂)` restriction stands on its own), or replace it with an honest scope note that the multi-slot count Δ is not characterised here.

### Issue 3: R1 / R2 / R6 mutual cross-referencing accretion

**ASN-0107, R1, R2, R6**: R1 closes "the `k = 1` specialisation of R2's `Δ ∈ {−k,…,0}`"; R2 defers to R6 (Issue 2) and repeatedly parenthesises "(the R3 situation)"; R6 closes with "*Specialisation to R1.*"

**Problem**: Three claims at three granularities (per-link wp, minimal-count Δ, general-count bound) are stitched together with reciprocal pointers rather than a clean hierarchy. The cross-references ("k=1 specialisation," "specialises to R1's split," "the R3 situation" appearing twice) are the kind of meta-prose a reader must work around to follow the actual bound. R1's four named preconditions plus its R2-pointer plus R6's R1-pointer is more scaffolding than the result needs.

**Required**: Pick one anchor. If R6 is the weakest-precondition result and R1 is its `k=1` count corollary, derive R1 *from* R6 once and drop the redundant back-pointers; remove the inline "(the R3 situation)" asides in favour of a single statement of when a reaching link is retained.

## OUT_OF_SCOPE

The three Open Questions (independently-anchored multi-document parts; coincidence of discovery and existence counts; count-vs-retrieval cardinality divergence) are correctly deferred and not errors in this ASN. No forbidden-topic claims (FINDLINKS, pagination, MAKELINK, FOLLOWLINK, BEBE) appear in the body.

VERDICT: REVISE
