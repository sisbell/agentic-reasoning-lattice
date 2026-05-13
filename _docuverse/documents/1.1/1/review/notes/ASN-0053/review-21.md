# Review of ASN-0053

## REVISE

### Issue 1: S5 action-point computation is asserted but not fully proven
**ASN-0053, S5 proof, part (b)**: "From (a), the action point is min(k_d, k_{d'}) ≤ k_d ≤ #s (the latter from T12 applied to λ)."
**Problem**: Part (a) of the proof only establishes *positivity* of d ⊕ d' at position min(k_d, k_{d'}). To conclude that the action point *equals* this minimum, the proof must also show that for every i < min(k_d, k_{d'}), (d ⊕ d')_i = 0. This is implicit in the case analysis (e.g., in case k_d > k_{d'}: for i < k_{d'}, TumblerAdd gives r_i = d_i, and i < k_{d'} < k_d makes d_i = 0), but it is never stated. The TA-LC precondition check in the following paragraph depends on actionPoint(d ⊕ d') being exactly min, not merely bounded by it.
**Required**: Add an explicit zero-below-min verification in each of the three cases of (a), and state the action-point identity as the conclusion before (b) consumes it.

### Issue 2: S11c Case 2 has no worked example
**ASN-0053, S11c proof, Case 2**: "start(β) < start(α) < reach(β) < reach(α). We derive the difference by element-chasing... Therefore ⟦α⟧ \ ⟦β⟧ = {t : reach(β) ≤ t < reach(α)}."
**Problem**: Case 1 has a concrete worked example with specific tumblers verifying construction, reach, and denotation. Case 2 — which uses a structurally different construction (γ' anchored at reach(β), not start(α)) and a different argument path (element-chasing rather than direct derivation) — has none. Symmetry is not a substitute for a worked example when the construction shape differs.
**Required**: Add a worked example for Case 2 showing specific level-uniform spans, the construction γ' = (reach(β), reach(α) ⊖ reach(β)), verification of reach(γ') = reach(α), and the denotation equality.

### Issue 3: "Mutually level-compatible" is used in claim conditions but never defined
**ASN-0053, S8 statement**: "Every span-set Σ whose component spans are level-uniform and mutually level-compatible..." Also S10: "mutually level-compatible across both sets" / "across all three sets".
**Problem**: S6 defines level_compat between two tumblers and level-uniform for a single span. "Mutually level-compatible" between an arbitrary collection of spans is not defined. The intended meaning (every pair of starts in the collection is level-compatible) is reachable by inference, but a claim of the form "for every span-set satisfying X" requires X to be a stated predicate.
**Required**: Add a definition before S8: "A span-set Σ = ⟨σ₁, ..., σₙ⟩ is *mutually level-compatible* when level_compat(start(σᵢ), start(σⱼ)) for all 1 ≤ i, j ≤ n." Cite it explicitly in S8 and S10.

### Issue 4: S6 phrasing "for all endpoint pairs" suggests multiple pairs per span
**ASN-0053, S6, paragraph following the definition**: "Level-uniform spans automatically satisfy D0 for all endpoint pairs: since #start = #reach, neither is a proper prefix of the other..."
**Problem**: A span has exactly one endpoint pair (start, reach). "For all endpoint pairs" reads as if a span ranges over a family of pairs. The statement also conflates D0's full precondition list (a < b, divergence(a, b) ≤ #a) with the prefix exclusion alone — the a < b part is from TA-strict, not from level-uniformity.
**Required**: Rephrase to: "The endpoint pair (start(σ), reach(σ)) of a level-uniform span satisfies D0's preconditions: start < reach by TA-strict, and #start = #reach forces divergence to be of type (i) with k ≤ #start, so neither is a proper prefix of the other."

### Issue 5: Interior-point definition's S0 citation is gratuitous
**ASN-0053, Definition (Interior point), preceding S4**: "A position p is interior to span σ when start(σ) < p < reach(σ). By S0, every interior point is in ⟦σ⟧."
**Problem**: Membership p ∈ ⟦σ⟧ follows directly from the definition ⟦σ⟧ = {t ∈ T : start(σ) ≤ t < reach(σ)}: start(σ) < p gives start(σ) ≤ p, and p < reach(σ) is the upper bound. S0 (convexity over a containing interval) is not the operative justification. Citing it suggests interior membership requires the convexity theorem, which it does not.
**Required**: Either remove the "By S0" or replace with "by the definition of ⟦σ⟧".

### Issue 6: S5 proof of part (a) under-specifies the k_d = k_{d'} case
**ASN-0053, S5 proof, part (a)**: "If k_d = k_{d'}, (d ⊕ d')_{k_d} = d_{k_d} + d'_{k_d} > 0."
**Problem**: The strict positivity is asserted but the conjunction "d_{k_d} > 0 ∧ d'_{k_d} > 0 ⟹ d_{k_d} + d'_{k_d} > 0" cites no foundation. On ℕ, this follows from NAT-zero plus NAT-addbound (the sum dominates each operand), but the proof should either invoke these or note the standard fact. A Dijkstra-style audit treats unfounded "> 0" arithmetic as a hand-wave even when the answer is obvious.
**Required**: Add a one-line justification — e.g., "by NAT-addbound (right dominance) at (d_{k_d}, d'_{k_d}) combined with d'_{k_d} > 0" — or cite the relevant foundation fact once for all three cases.

## OUT_OF_SCOPE

None — the ASN's scope is bounded explicitly, and every issue I have is internal to the stated scope.

VERDICT: REVISE
