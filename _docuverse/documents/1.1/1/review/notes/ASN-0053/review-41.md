# Review of ASN-0053

I checked every proof, verified all worked examples arithmetically, and probed the boundary cases (empty span-sets, equal starts, containment with coincident boundaries, single-component starts, adjacency-vs-overlap, and the shorter-sequence branches of the uniqueness proof). The ASN holds up.

## REVISE

*(none)*

## What I verified

**Foundation usage is consistent.** WR, WF, S1, S3, S4, S5, S9 all discharge the cited ASN-0034 contracts (D0/D1/D2, TA-LC, TA-assoc, TumblerSub, T12, TA-strict) with their preconditions explicitly checked — notably S5's TA-assoc/TA-LC chain, where `k_d ≤ #s`, `k_{d'} ≤ #d = #s`, and the positivity obligations are each grounded in T12 on the constructed parts rather than waved through.

**Edge cases are covered, not skipped:**
- S1 routes separated/adjacent (`r' ≤ s'`) to empty and overlap/containment/equal to a single span via one membership argument — all five SC cases land correctly, including containment (`γ = β`) and equality (`γ = α`).
- S8 handles `n = 0` (vacuous N1/N2), `n = 1` (seed-then-finalize), equal-start inputs (absorbed by the `start ≤ r` merge branch), and contained spans (`max(r, reach) = r`). The N1-strictness argument correctly derives strictness from the emit condition rather than from the (non-strict) sort.
- S9 exhaustively splits divergence into start-differs (1a/3a), shorter-sequence (1b/3b), and equal-start/reach-differs (2a/2b), with the preamble ruling out the no-divergence configuration via left cancellation.
- S11/S11a–d cover all SC cases including reverse containment (`⟦α⟧ ⊂ ⟦β⟧ ⟹ ∅`), and the two-span tightness in S11 is proved by contradiction against S0, not asserted.

**No hand-waves of consequence.** S3a and S10 reduce to set-union commutativity/associativity plus S9 — these are genuinely one-line facts, not multi-case proofs hiding behind "similarly." Each major theorem carries a concrete worked instance whose arithmetic I recomputed (S3 → `[0,8]`, S8 → `⟨([1,3],[0,6]),([1,10],[0,3])⟩`, S11 → `[0,2]`/`[0,2]`, S11c Case 2 → `[0,4]`); all check.

**Scope and prose.** The level-uniform / level-compatible restriction is applied deliberately and the cross-level failure is both exhibited (WR's `[1,3,5]` instance) and deferred to Open Questions — not a gap. No non-foundation cross-ASN references; ASN-0034 is foundation. The `review-mode.anti-bloat` patterns (forward-reference meta-prose, relocated-finding paragraphs, axiom-rationale sub-prose) are not present at flaggable density — consistent with the prior "trim trailing remarks" revision. The defining-state / operations / invariants content is abstract enough to bind any implementation; no drift.

VERDICT: CONVERGED
