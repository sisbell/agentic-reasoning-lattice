# Cone Review — ASN-0034/TumblerAdd (cycle 5)

*2026-04-16 19:59*

### TumblerAdd's Depends citation of ActionPoint omits the "zeros below the action point" postcondition that the dominance proof uses
**Foundation**: `ActionPoint` (this ASN) — Formal Contract postconditions are "`1 ≤ actionPoint(w) ≤ #w`; `wᵢ = 0` for all `i < actionPoint(w)`; `w_{actionPoint(w)} ≥ 1`". The middle conjunct is the "zeros-below-action-point" fact.
**ASN**: `TumblerAdd`, Formal Contract Depends entry for ActionPoint:
> ActionPoint (ActionPoint) — supplies `k = actionPoint(w)` with bounds `1 ≤ k ≤ n` and `wₖ ≥ 1`.

And TumblerAdd's dominance-over-displacement proof (`a ⊕ w ≥ w`):
> For `i < k`, `rᵢ = aᵢ` and `wᵢ = 0` (by definition of action point); if some `aⱼ > 0` for `j < k`, the least such `j` is a divergence point with `rⱼ > wⱼ`, so T1 case (i) gives `r > w`.

**Issue**: The dominance proof load-bears on `wᵢ = 0` for every `i < k` — this is what makes `rⱼ = aⱼ > 0 = wⱼ` at the divergence point, and what allows the equality sub-case to conclude `rᵢ = wᵢ` for `i < k`. That fact is the *second* ActionPoint postcondition ("`wᵢ = 0` for all `i < actionPoint(w)`"). TumblerAdd's Depends cites ActionPoint only for "bounds `1 ≤ k ≤ n` and `wₖ ≥ 1`" — the bounds and the minimum-nonzero-value, not the zeros-below-the-minimum. A formalizer who builds the proof-obligation set from Depends entries will not have "zeros before k" in scope, and the critical step `wᵢ = 0 (by definition of action point)` will be unjustified. The analogous pattern was flagged and fixed for ActionPoint itself in cycle 2; this is the downstream propagation of the same convention, which the current Depends misses for the first of the two ordering postconditions to use it.
**What needs resolving**: TumblerAdd's Depends citation of ActionPoint should be widened to record the `wᵢ = 0 for i < actionPoint(w)` postcondition alongside the bounds and `wₖ ≥ 1`, with a note that the dominance proof uses the zeros-below-k fact to license both the divergence case (`wⱼ = 0 < aⱼ = rⱼ`) and the equality sub-case (`rᵢ = aᵢ = 0 = wᵢ` for `i < k`).
