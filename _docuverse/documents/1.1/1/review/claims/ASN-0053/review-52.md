**S0 (Convexity).** The proof correctly composes the bracketing chain start(σ) ≤ p ≤ q ≤ r < reach(σ) by case-splitting on the `≤` abbreviation and reducing each non-strict step to T1 postcondition (c) or substitution of equals. All four cases for the lower bound and both cases for the upper bound are walked. The formal contract correctly notes that the ≤-composition steps are derived, not T1 exports. q ∈ T is discharged from the explicit precondition. No gap.

**WF (WellFormedSpanFromEndpoints).** The proof eliminates T1 case (ii) by unfolding NAT-order's `≤` definition on `#s + 1 ≤ #s`, dispatching both sub-cases (strict and equality) to `#s < #s`, then applying NAT-order's irreflexivity. The Divergence case-(i) uniqueness identification of the T1 witness k with divergence(s,r) is sound: T1's definition already requires `(A i : 1 ≤ i < k : sᵢ = rᵢ)`, which is the same minimality condition restated in Divergence's case-(i) qualifier, so the conjunction is satisfied and uniqueness applies. Divergence's symmetry carries the case-(i) witness to the pair (r,s), ZPD's Relationship-to-Divergence identifies zpd(r,s) = k, and TumblerSub's positive-branch postcondition delivers Pos(r ⊖ s) directly. All five D1 preconditions are discharged. Level-uniformity follows from TumblerSub's length postcondition #(r ⊖ s) = max(#r,#s) = #s. No gap.

**S6 (LevelConstraint).** The proof is a direct application of TumblerAdd's result-length identity #(s ⊕ ℓ) = #ℓ, earned under the well-formedness preconditions that S6 explicitly lists, composed with level-uniformity #ℓ = #s. The note that Pos(ℓ) failure leaves reach(σ) undefined and the identity inapplicable is correctly stated. No gap.

**S2 (EmptyDistinction).** One-step application of T12's postcondition (b): s ∈ span(s,ℓ), read through the set equality ⟦s,ℓ⟧ = span(s,ℓ). The preconditions supplied to T12 are exactly S2's hypotheses. No gap.

**S11 (DifferenceBound).** The proof structure is sound end-to-end.

*Reach carrier memberships* are established at the outset via TumblerAdd's carrier postcondition on each span's well-formedness, and those facts are correctly consumed twice: in the boundary characterization (testing reach(α) ∈ ⟦β⟧ requires reach(α) ∈ T) and in the ρ-construction (WF's s, r ∈ T preconditions).

*Boundary derivation:* start(β) ∈ ⟦β⟧ ⊆ ⟦α⟧ yields start(α) ≤ start(β) < reach(α). The reach(β) ≤ reach(α) argument by contradiction correctly places reach(α) ∈ ⟦β⟧ using start(β) ≤ reach(α) (weakened from strict) and reach(α) < reach(β) (hypothesis), deriving reach(α) < reach(α).

*Three sub-ranges* partition ⟦α⟧ exhaustively and disjointly by the sequenced comparison. Disjointness of (L) and (R) requires start(β) ≤ reach(β), which follows from S2's non-emptiness of β (start(β) < reach(β)), correctly cited.

*λ-construction:* WF's preconditions at (start(α), start(β)) are immediate — both are span starts hence in T, start(α) < start(β) is the sub-case condition, and level_compat supplies #start(α) = #start(β). WF gives reach(λ) = start(β). ✓

*ρ-construction:* WF's carrier preconditions at (reach(β), reach(α)) are the reach memberships already placed. S6 propagates level_compat through #reach(σ) = #start(σ) (TumblerAdd's result-length identity composed with defining #width(σ) = #start(σ)) to give #reach(β) = #reach(α). WF gives reach(ρ) = reach(α). ✓

*Tightness:* start(α) ∈ ⟦λ⟧ (since start(α) < start(β) = reach(λ)) and reach(β) ∈ ⟦ρ⟧ (since reach(β) = start(ρ) < reach(α)). The mixed ≤ composition start(α) ≤ t is correctly derived by case-splitting on start(β) ≤ t and applying T1(c) or substitution of equals, mirroring S0's own technique. S0 is then applied with p = start(α) ∈ ⟦γ⟧, r = reach(β) ∈ ⟦γ⟧, q = t. The conclusion t ∈ ⟦γ⟧ contradicts t ∉ ⟦λ⟧ (since t ≥ start(β) = reach(λ)) and t ∉ ⟦ρ⟧ (since t < reach(β) = start(ρ)). Contradiction is clean. ✓

No correctness issues found in any claim or in the cross-claim dependency chains.

VERDICT: CONVERGED