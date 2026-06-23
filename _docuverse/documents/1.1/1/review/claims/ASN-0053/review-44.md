## Audit

### S0 (Convexity)

The proof derives the lower and upper bounds by case-splitting on the `≤` abbreviation and reducing every mixed step to T1(c) or substitution of equals. The four-case lower bound and two-case upper bound are fully walked. The Formal Contract explicitly notes that ≤-transitivity is not a T1 export and derives it inline. T1 is the sole dependency, correctly cited. The claim is sound.

### WF (WellFormedSpanFromEndpoints)

D1's five preconditions are discharged in order. The elimination of T1 case (ii) via `#s = #r` is complete: both sub-cases of `#s + 1 ≤ #s` (strict and equality) are driven to `#s < #s` via NAT-addcompat and NAT-order irreflexivity. Case (i) supplies `k ≤ #s` and `sₖ ≠ rₖ`; Divergence's uniqueness clause identifies `k = divergence(s, r)`; ZPD Relationship-to-Divergence is applied to the pair (r, s) via Divergence's symmetry to certify `zpd(r, s) = k` is defined; TumblerSub's positive-branch postconditions (`Pos(r ⊖ s)`, `actionPoint(r ⊖ s) = k`, `#(r ⊖ s) = #s`) discharge T12's preconditions; D1 closes `s ⊕ (r ⊖ s) = r`. Level-uniformity `#(r ⊖ s) = max(#r, #s) = #s` follows directly. All dependencies correctly cited.

### S6 (LevelConstraint)

TumblerAdd's result-length identity `#(a ⊕ w) = #w` is instantiated at `(s, ℓ)` under the well-formedness preconditions, yielding `#reach(σ) = #ℓ`. Level-uniformity closes the chain to `#s`. Preconditions of TumblerAdd are exactly the well-formedness conditions carried in S6's own preconditions. The claim is sound and the dependency on TumblerAdd is the sole requirement.

### S2 (EmptyDistinction)

T12's postcondition (b) (`s ∈ span(s, ℓ)`) is applied directly under S2's preconditions, which are exactly T12's preconditions. The existence of the witness `s ∈ ⟦s, ℓ⟧` establishes non-emptiness. No additional machinery required.

### S11 (DifferenceBound)

**Boundary characterization.** `reach(α), reach(β) ∈ T` are placed at the outset via TumblerAdd's carrier postcondition under each span's well-formedness. `start(β) ∈ ⟦β⟧` is exactly S2's postcondition, which is cited. The reach-bound proof by contradiction correctly uses `reach(α) ∈ T` to test membership in `⟦β⟧`, obtaining `reach(α) < reach(α)` and discharging via T1 irreflexivity.

**Three-way partition.** Totality of T1 splits every `t ∈ ⟦α⟧` into (L)/(M)/(R). Sub-range (M) equals `⟦β⟧` by containment and the complementary exclusions for (L) and (R). `⟦α⟧ \ ⟦β⟧ = (L) ∪ (R)` follows.

**Construction of λ.** WF is applied at `(start(α), start(β))` with `start(α), start(β) ∈ T` (span starts), `start(α) < start(β)` (case hypothesis), and `#start(α) = #start(β)` (level\_compat directly). Yields `reach(λ) = start(β)`. ✓

**Construction of ρ.** WF is applied at `(reach(β), reach(α))`. Carrier membership `reach(β), reach(α) ∈ T` is already in hand from Step 1. Length precondition `#reach(β) = #reach(α)` is discharged through S6: `#reach(σ) = #start(σ)` for each level-uniform span, then level\_compat closes `#reach(β) = #start(β) = #start(α) = #reach(α)`. Yields `reach(ρ) = reach(α)`. ✓

**Tightness.** The contradiction argument correctly identifies `start(α) ∈ ⟦λ⟧ ⊆ ⟦γ⟧` and `reach(β) ∈ ⟦ρ⟧ ⊆ ⟦γ⟧`. The lower half `start(α) ≤ t` is derived by the same mixed `<`-`≤` composition technique S0 uses (case-split on `start(β) ≤ t`). S0 is then applied at `(start(α), t, reach(β))` for span `γ`, all preconditions discharged. `t ∉ ⟦λ⟧` (since `t ≥ start(β) = reach(λ)`) and `t ∉ ⟦ρ⟧` (since `t < reach(β) = start(ρ)`) complete the contradiction. Two-span non-emptiness (both `⟦λ⟧ ≠ ∅` and `⟦ρ⟧ ≠ ∅`) follows from S2 applied to the constructed WF spans.

All dependencies in S11 are correctly cited and all precondition chains are unbroken.

VERDICT: CONVERGED