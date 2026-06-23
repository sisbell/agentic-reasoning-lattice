Reading the foundations, then tracing each claim.

**S2 (EmptyDistinction).** T12 postcondition (b) gives s ∈ span(s, ℓ), discharging the non-emptiness claim. The single-step proof is sound.

**S0 (Convexity).** The four-case unfolding for the lower bound and two-case unfolding for the upper bound are correctly derived from T1(c) and the abbreviation a ≤ b ≡ a < b ∨ a = b. The claim that T1 exports no ≤-transitivity is accurate and correctly handled inline.

**S6 (LevelConstraint).** TumblerAdd's result-length identity #(a ⊕ w) = #w, instantiated at (s, ℓ) under the well-formedness conditions, gives #reach(σ) = #ℓ = #s. The level-uniformity assumption is the correct precondition.

**SC (SpanClassification).** The exhaustiveness argument via the WLOG start(α) ≤ start(β) assumption is justified: each case is either symmetric or carries the symmetric rider. The five boundary conditions are mutually exclusive by T1's exactly-one trichotomy. The containment sub-case derives ⟦β⟧ ⊆ ⟦α⟧ via the same four-case/two-case unfolding pattern used in S0 and S11d. The non-degeneracy start(σ) < reach(σ) flows from T12 postcondition (b). No gap in the case taxonomy.

**WF (WellFormedSpanFromEndpoints).** The elimination of T1 case (ii) via the #s = #r hypothesis is sound: unfolding #s + 1 ≤ #s into two sub-cases, then applying NAT-addcompat's successor inequality and NAT-order's transitivity and irreflexivity closes both. Divergence case (i)'s uniqueness correctly identifies the T1 witness k with divergence(s, r), so k ≤ #s discharges D1's precondition. TumblerSub's positive-branch postconditions (Pos(r ⊖ s), actionPoint(r ⊖ s) = k, length = #s) all follow. D1 then delivers reach(γ) = r. Level-uniformity follows from the length identity.

**S11 (DifferenceBound).** Reach membership reach(α), reach(β) ∈ T is correctly bootstrapped from TumblerAdd at the proof's outset, before the boundary argument needs reach(α) ∈ T to test membership in ⟦β⟧. The contradiction argument for reach(β) ≤ reach(α) is sound. The three-range partition (L)/(M)/(R) is exhaustive by T1's totality. Spans λ and ρ are correctly constructed via WF with the level_compat and S6 length conditions discharged. The tightness argument correctly applies S0 with p = start(α) ∈ ⟦λ⟧ ⊆ ⟦γ⟧ and r = reach(β) ∈ ⟦ρ⟧ ⊆ ⟦γ⟧; both S0 preconditions p ≤ t and t ≤ r are derived by the standard case-split.

**S11a (DifferenceSeparated), S11b (DifferenceEqual).** Trivially sound.

**S11c (DifferenceOverlap).** Case 1: the ⊆ direction eliminates t ≥ start(β) by membership in ⟦β⟧ and contradiction with t < reach(α); the ⊇ direction uses T1(c) to chain t < start(β) < reach(α). Case 2: the derivation of start(β) ≤ t from start(β) < start(α) ≤ t via the ≤-case-split is correct. The ⊇ recovery of start(α) ≤ t from start(α) < reach(β) and reach(β) ≤ t is correctly case-split. The γ' construction discharges WF's carrier preconditions via TumblerAdd and WF's length precondition via S6 + level_compat. The worked examples compute correctly.

**S11d (GeneralDifferenceBound).** The five-case table correctly delegates to S11a (cases i/ii), S11c (case iii), S11 (case iv forward), and S11b (case v). The inline derivation for case iv reverse (⟦α⟧ ⊆ ⟦β⟧) uses the same four-case/two-case unfolding pattern established in S0 and SC. All level_compat and well-formedness preconditions are inherited from S11d's precondition. The tightness bound of 2 is correctly attributed to S11 sub-case (c).

No precondition chains are broken. All operators are defined in scope before use. The reach(σ) ∈ T bootstrap is consistently handled before any set membership test on reach values.

VERDICT: CONVERGED