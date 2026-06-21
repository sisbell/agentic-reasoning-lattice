Reading foundation statements first, then walking each claim carefully.

**T1** exports irreflexivity, trichotomy, transitivity. **TumblerAdd** exports `#(a ⊕ w) = #w` and `a ⊕ w > a`. **TumblerSub** exports `a ⊖ w ∈ T`, length `L`, divergence-point inequality, `Pos`/`Zero` conditional. **D1** exports `a ⊕ (b ⊖ a) = b` under five preconditions. **T12** exports well-formedness (membership, convexity). **TA-strict** exports `a ⊕ w > a` as a re-export. **Divergence** exports two-case partition and symmetry.

---

**S11 (DifferenceBound).** Containment derivation: `start(β) ∈ ⟦β⟧ ⊆ ⟦α⟧` gives `start(α) ≤ start(β)` and `start(β) < reach(α)` — used in the reach contradiction. Contradiction for `reach(β) > reach(α)` is clean: `start(β) < reach(α) < reach(β)` places `reach(α) ∈ ⟦β⟧ ⊆ ⟦α⟧`, yielding `reach(α) < reach(α)`. Three sub-ranges are exhaustive and disjoint by T1 totality. WF calls: λ needs `#start(α) = #start(β)` (from level\_compat directly); ρ needs `#reach(β) = #reach(α)` — derived by S6 applied to α and β plus level\_compat. Tightness: `start(α) ∈ ⟦λ⟧ ⊆ ⟦γ⟧` and `reach(β) ∈ ⟦ρ⟧ ⊆ ⟦γ⟧` (from `reach(β) < reach(α)`, so `reach(β) = start(ρ) ∈ ⟦ρ⟧`), with S0 applied at `p = start(α)`, `q = t`, `r = reach(β)`, where `t ≤ reach(β)` from `t < reach(β)`. Contradiction from `t ∉ ⟦λ⟧ ∪ ⟦ρ⟧`. Precondition chains unbroken.

**SC (SpanClassification).** Five-case split exhaustive under WLOG `start(α) ≤ start(β)` — the case definitions are symmetric or carry explicit "or symmetrically" riders. Mutual exclusivity: (i)/(ii) partition on `reach(α)` vs `start(β)` strict/equal/greater; (iii)/(iv) partition on `reach(α)` vs `reach(β)`; (iv)/(v) partition on whether at least one boundary is strict. Non-degeneracy precondition is invoked for case (v) to confirm `⟦α⟧ ≠ ∅`. Disjoint/overlap alignment: cases (i)/(ii) proved ∅ by element-chase; cases (iii)/(iv)/(v) proved non-empty by exhibiting witnesses. Symmetric configurations handled by the case definitions themselves.

**S11c (DifferenceOverlap).** Case 1 element-chase: `t ≥ start(β)` in `⟦α⟧` forces `t ∈ ⟦β⟧` via `start(β) ≤ t < reach(α) < reach(β)`, contradiction with `t ∉ ⟦β⟧`; hence `t < start(β)`. Converse is immediate. WF call: `start(α) < start(β)` and `#start(α) = #start(β)` from level\_compat. Case 2 partition at `reach(β)`: `t < reach(β)` with `start(β) < start(α) ≤ t` gives `t ∈ ⟦β⟧`; `t ≥ reach(β)` gives `t ∉ ⟦β⟧`. The identification of `{t ∈ ⟦α⟧ : reach(β) ≤ t}` with `{t : reach(β) ≤ t < reach(α)}` recovers the discarded lower guard `start(α) ≤ t` from the Case 2 hypothesis `start(α) < reach(β) ≤ t` via T1 transitivity. WF call for γ': `#reach(β) = #reach(α)` via S6 and level\_compat.

**S11b (DifferenceEqual).** Equal endpoints → equal denotations → `X \ X = ∅`. Trivially sound.

**S11a (DifferenceSeparated).** SC classifies (i)/(ii) as disjoint; `A \ B = A` when `A ∩ B = ∅`. Sound.

**S0 (Convexity).** `p ∈ ⟦σ⟧` and `p ≤ q` give `start(σ) ≤ q` by ≤-transitivity; `q ≤ r` and `r < reach(σ)` give `q < reach(σ)`. Both follow from T1 strict transitivity composed with the ≤ definition. Sound.

**WF (WellFormedSpanFromEndpoints).** D1's five preconditions: `s, r ∈ T`, `s < r`, `#s ≤ #r` from `#s = #r`, and `divergence(s, r) ≤ #s` — established by observing equal length excludes T1 case (ii) (would force `#s + 1 ≤ #s`), leaving T1 case (i) with `k ≤ #s` and `sₖ ≠ rₖ`, which qualifies Divergence case (i); uniqueness identifies `k = divergence(s, r)`. TumblerSub: `r ≥ s` from `s < r`, `s ≠ r` ensures zpd defined → positive branch → `Pos(r ⊖ s)`. Length postcondition `#(r ⊖ s) = max(#r, #s) = #s` closes `actionPoint(r ⊖ s) ≤ #s` and level-uniformity. All precondition chains unbroken.

**S6 (LevelConstraint).** TumblerAdd's `#(a ⊕ w) = #w` instantiated at `(s, ℓ)` with `Pos(ℓ)` and `actionPoint(ℓ) ≤ #s` from well-formedness gives `#reach(σ) = #ℓ = #s`. Sound.

**S2 (EmptyDistinction).** TA-strict gives `s ⊕ ℓ > s` from `Pos(ℓ)` and `actionPoint(ℓ) ≤ #s`. Then `s ≤ s` trivially and `s < s ⊕ ℓ` place `s ∈ ⟦s, ℓ⟧`. Sound.

**S11d (GeneralDifferenceBound).** SC's five cases plus the reverse-containment sub-case are all handled: (i)/(ii) by S11a, (iii) by S11c, (iv) forward by S11, (iv) reverse by inline transitivity derivation (T1 closes `start(β) ≤ start(α) ≤ t` and `t < reach(α) ≤ reach(β)`), (v) by S11b. Maximum 2, achieved only in the S11 case. Coverage is exhaustive and the bound proof is tight.

VERDICT: CONVERGED