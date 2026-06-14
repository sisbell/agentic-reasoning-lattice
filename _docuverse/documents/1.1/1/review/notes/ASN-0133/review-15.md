# Review of ASN-0133

I checked the proofs claim-by-claim. The core machinery holds up under scrutiny: Q0's single-PL-term-vs-metalevel-conjunction split correctly ranges over *domains* not just triggers; Q3's idem=⊤ dedup subtlety (fire ⟹ no audit-slice hit ⟹ deposit ⟹ falsify) is sound; Q-FLIP's `target_of` deposit re-armer genuinely defeats the "no-retraction ⟹ flip-once" folklore; Q5's injection-by-index is right; Q5a's "strictly stronger than H-RF in the open case, equivalent in the closed case" is correctly argued; the H-SFAIR⟹H-FAIR proof correctly scopes to infinite σ and the satisfiability repair (unsatisfiable against withdraw-before-fire environments) is honest. The foundation citations (PD0/PD1/PD2/FP from 0129; I1/I2/I3 from 0128; A_K⊆L_K/R6c from 0086; FrontierUnification from 0126) are used accurately. One precision defect remains, in the load-bearing termination analysis.

## REVISE

### Issue 1: Q6's "three obstructions to reaching a quiescent state" mislabels case (2), which *reaches* one

**ASN-0133, Q6 (non-grow-only regime)**: "Three obstructions to reaching a quiescent state must be distinguished, and only the first is excluded by bounded growth. (1) ... keeps every state non-quiescent ... (2) ... quiescent in the gaps, non-quiescent during each presentation, so reached intermittently. (3) ... yet no state is quiescent: quiescence is not reached..."

**Problem**: Under Q0, quiescence is a *per-state* predicate `quiescent_R(Σ)`. The note's own description of (2) — "quiescent in the gaps ... reached intermittently" — therefore says (2) *does* reach a quiescent state (a Σ with `quiescent_R(Σ) = ⊤`); it only fails to *hold* one. So calling (2) an "obstruction to reaching a quiescent state" is literally false under Q0's definition. Cases (1) and (3) are genuinely "no quiescent state ever occurs"; case (2) is "quiescent states are reached but not held" — two different failure modes lumped under one header. This is exactly the reached/held conflation the note is elsewhere at pains to avoid: the worked composition states the distinction precisely ("possibly unreached, not merely unheld"), and Q6's own thesis sentence is "*Reaching*, not only *holding*." The looseness compounds two clauses later — "only H-SFAIR ... *reaches quiescence* over a non-grow-only domain" uses "reaches" in the terminal sense within the same passage where (2)'s "reached intermittently" used it in the per-state sense.

**Required**: Apply the note's own reached/held vocabulary to the three cases: (1) and (3) obstruct *reaching* (no quiescent state ever occurs); (2) obstructs only *holding* (quiescent states are reached intermittently but are not absorbing against the environment — this is Q8 re-entry, which the note already names for (2)/(3)). Either retitle the group ("obstructions to a *reached-and-held* quiescent state") and re-sort, or fix "reaching a quiescent state" to a single precise sense throughout the passage and reconcile (2)'s "reached intermittently."

## OUT_OF_SCOPE

The note's own deferrals — scheduler construction and its fairness proofs, the `pd_extinct`/SF certificate as a shipped class, a workload/environment model deciding which inputs are bounded — are correctly placed in "What this note doesn't cover" and "Open questions." I have no additional out-of-scope items: H-FAIR-as-hypothesis, the meta-level standing of the bounded-domain-growth bound, and the dangling-pdef-reference case are all named and routed appropriately.

VERDICT: REVISE
