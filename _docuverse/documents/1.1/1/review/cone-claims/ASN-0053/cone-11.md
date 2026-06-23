Reading through all four claims (SC, S6, WF, S11c) against the foundation statements, checking every precondition chain, case split, and proof step.

**SC — SpanClassification**

Exhaustiveness argument proceeds by WLOG start(α) ≤ start(β) and a well-formed decision tree: branch on reach(α) vs start(β) gives cases (i), (ii), or sharing; in the sharing branch, compare starts to split case (iii)/(iv) and starts-equal to split (iv)/(v). Since each branch point uses T1 comparability and the branches are mutually exclusive under T1's exactly-one trichotomy, the tree establishes both exhaustiveness and mutual exclusivity simultaneously. The six sub-cases under the WLOG assumption (with the symmetric configurations handled by label exchange) cover all configurations.

Disjoint/overlap correspondence: case (i) — transitivity chains p < reach(α) < start(β) ≤ q; case (ii) — reach(α) = start(β) excluded from ⟦α⟧, included in ⟦β⟧, so no position shared; case (iii) — start(β) ∈ ⟦α⟧ ∩ ⟦β⟧ via non-degeneracy (T12(b) provides start < reach for each well-formed span); case (iv) — ⟦β⟧ ⊆ ⟦α⟧ by chaining start(α) ≤ start(β) ≤ q < reach(β) ≤ reach(α), with ⟦β⟧ nonempty from non-degeneracy; case (v) — ⟦α⟧ = ⟦β⟧. All chains are grounded.

**S6 — LevelConstraint**

TumblerAdd's result-length postcondition #(a ⊕ w) = #w is earned under its four preconditions a ∈ T, w ∈ T, Pos(w), actionPoint(w) ≤ #a. S6's preconditions instantiate these at (a, w) = (s, ℓ), so the identity applies and #reach(σ) = #ℓ; level-uniformity #ℓ = #s closes the chain. The note that Pos(ℓ) is not implied by #s = #ℓ is correctly observed.

**WF — WellFormedSpanFromEndpoints**

Step 1 (divergence(s, r) ≤ #s): s ≠ r from T1 trichotomy disjointness applied to s < r. T1's witness k falls in case (i) or (ii); #s = #r eliminates case (ii) because k = #s + 1 ≤ #r = #s would give #s + 1 ≤ #s, refuted by unfolding ≤ as < ∨ = and deriving #s < #s in both sub-cases, against NAT-order irreflexivity. Case (i) gives k ≤ #s; Divergence uniqueness identifies k = divergence(s, r). ✓

Step 2 (zpd(r, s) defined): Divergence case (i) witness k carries to (r, s) by symmetry; ZPD Relationship-to-Divergence yields zpd(r, s) = k, defined. TumblerSub's positive branch then exports Pos(r ⊖ s) and actionPoint(r ⊖ s) = k. Since k ≤ #s and #(r ⊖ s) = L = #s (sub-case α of TumblerSub, with #r = #s), we have actionPoint(r ⊖ s) ≤ #s. T12's four preconditions are discharged. Level-uniformity: #width(γ) = #s = #start(γ). D1 then delivers reach(γ) = r. ✓

**S11c — DifferenceOverlap**

Case 1 (start(α) < start(β) < reach(α) < reach(β)):

⊆: t ∈ ⟦α⟧ with t ∉ ⟦β⟧. If t ≥ start(β), then start(β) ≤ t < reach(α) < reach(β), placing t ∈ ⟦β⟧ — contradiction. So t < start(β). ✓

⊇: t ∈ [start(α), start(β)) satisfies t < start(β) < reach(α), so t ∈ ⟦α⟧, and t < start(β) excludes ⟦β⟧. ✓

WF applicable to γ = (start(α), start(β) ⊖ start(α)) since start(α) < start(β) and #start(α) = #start(β) from level_compat. ✓

Case 2 (start(β) < start(α) < reach(β) < reach(α)):

The split at reach(β) is correct: for t ∈ ⟦α⟧, t < reach(β) implies start(β) < start(α) ≤ t (transitivity) and t < reach(β), so t ∈ ⟦β⟧; t ≥ reach(β) implies t ∉ ⟦β⟧ (exclusive upper bound). ✓

⊇ direction recovers start(α) ≤ t via start(α) < reach(β) ≤ t by T1 transitivity. ✓

For γ' = (reach(β), reach(α) ⊖ reach(β)): reach(β) ∈ T and reach(α) ∈ T follow from TumblerAdd's carrier postcondition at (start(σ), width(σ)) for each well-formed span σ. Level precondition #reach(β) = #reach(α) follows from S6 applied to each level-uniform span (giving #reach(σ) = #start(σ)) composed with level_compat(start(α), start(β)). WF then delivers γ' well-formed with reach(γ') = reach(α). ✓

Non-emptiness in both cases is correctly grounded: Case 1 via start(α) ∈ ⟦α⟧ \ ⟦β⟧; Case 2 via reach(β) ∈ {t : reach(β) ≤ t < reach(α)} using reach(β) < reach(α). ✓

No ungrounded symbols, missing cases, broken precondition chains, or unsound proof steps were found anywhere in the ASN.

VERDICT: CONVERGED