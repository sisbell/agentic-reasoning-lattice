Reading the foundation statements, then reading the ASN as a system.

**S0 (Convexity).** The proof is a direct application of T1 transitivity on the half-open interval definition. The step `q ≤ r < reach(σ) → q < reach(σ)` is the mixed `≤-<` chain: split on `q < r` (then `<`-transitivity) and `q = r` (then substitution). Both legs close. S0 is sound.

**WF (WellFormedSpanFromEndpoints).** The proof discharges all five preconditions of D1 for `(a,b) = (s,r)`: `s,r ∈ T` from hypotheses; `s < r` from hypothesis; `#s ≤ #r` from `#s = #r`; `divergence(s,r) ≤ #s` by eliminating T1 case (ii) (it would force `#s+1 ≤ #s`, contradicting `#s < #s+1`) and identifying the T1 case-(i) witness with the Divergence uniqueness clause. TumblerSub then gives `r ⊖ s ∈ T`, `Pos(r ⊖ s)` (divergence-point inequality `rⱼ > sⱼ` with padding-free projections since `#r = #s`), and `actionPoint(r ⊖ s) = j ≤ #s` via ActionPoint bounds and the length postcondition. Level-uniformity follows: `#(r ⊖ s) = max(#r,#s) = #s = #start(γ)`. WF is sound.

**S6 (LevelConstraint).** The identity `#reach(σ) = #(s ⊕ ℓ) = #ℓ = #s` chains TumblerAdd's result-length postcondition with the level-uniformity hypothesis. TumblerAdd's preconditions (`s ∈ T`, `ℓ ∈ T`, `Pos(ℓ)`, `actionPoint(ℓ) ≤ #s`) are exactly S6's stated preconditions. S6 is sound.

**S2 (EmptyDistinction).** The proof invokes T12(b) directly: the four well-formedness conditions are S2's preconditions, T12 delivers `s ∈ span(s,ℓ)`, and the set equality `⟦s,ℓ⟧ = span(s,ℓ)` closes the conclusion. S2 is sound.

**S11 (DifferenceBound).** The partition of `⟦α⟧` into three sub-ranges is exhaustive (two nested comparisons under T1 totality) and pairwise disjoint. The WF applications are correctly set up: λ uses `start(α) ∈ T`, `start(β) ∈ T` (primitive starts), `start(α) < start(β)`, and `#start(α) = #start(β)` from `level_compat` directly; ρ uses `reach(β) ∈ T`, `reach(α) ∈ T` from TumblerAdd, `reach(β) < reach(α)`, and `#reach(β) = #reach(α)` derived from S6 + `level_compat`. The tightness argument is sound: `start(α) ∈ ⟦λ⟧ ⊆ ⟦γ⟧`, `reach(β) ∈ ⟦ρ⟧ ⊆ ⟦γ⟧`, S0 convexity places any `t ∈ ⟦β⟧` (non-empty by S2) inside `⟦γ⟧`, yet `t ∉ ⟦λ⟧` (since `t ≥ start(β) = reach(λ)`) and `t ∉ ⟦ρ⟧` (since `t < reach(β) = start(ρ)`). However, the boundary-characterization step has a dependency-ordering gap flagged below.

---

### S11 boundary-characterization contradiction invokes reach(α) ∈ T before establishing it
**Class**: REVISE
**Foundation**: TumblerAdd (carrier postcondition `a ⊕ w ∈ T`)
**ASN**: S11 (DifferenceBound), boundary-characterization paragraph — "suppose for contradiction reach(β) > reach(α). Then start(β) < reach(α) < reach(β), so reach(α) ∈ ⟦β⟧ ⊆ ⟦α⟧"
**Issue**: `⟦β⟧ = {t ∈ T : start(β) ≤ t < reach(β)}`, so the claim `reach(α) ∈ ⟦β⟧` requires `reach(α) ∈ T` in addition to the two order conditions (`start(β) ≤ reach(α)` and `reach(α) < reach(β)`). The proof derives the order conditions in the preceding sentence but says nothing about `reach(α) ∈ T` at this point. TumblerAdd's carrier postcondition `a ⊕ w ∈ T`, applied to α's well-formedness (start(α) ∈ T, width(α) ∈ T, Pos(width(α)), actionPoint(width(α)) ≤ #start(α)), is the only grounding for `reach(α) ∈ T` in scope — but TumblerAdd is only explicitly invoked in the ρ-construction paragraph, which appears later in the proof. The Depends section's description of TumblerAdd names "reach(β) ∈ T and reach(α) ∈ T" only in the context of "discharging WF's carrier preconditions s, r ∈ T"; it does not account for this earlier use. The precondition chain for the membership claim `reach(α) ∈ ⟦β⟧` is broken at the point of use.
**What needs resolving**: The boundary-characterization step must ground `reach(α) ∈ T` before asserting `reach(α) ∈ ⟦β⟧`. TumblerAdd's carrier postcondition, instantiated at `(start(α), width(α))` under α's well-formedness (a precondition of S11), supplies this; the proof should invoke it here — or reorganize so TumblerAdd is applied to both α and β before the boundary characterization is run. The Depends entry for TumblerAdd must be updated to reflect this use.

---

VERDICT: REVISE