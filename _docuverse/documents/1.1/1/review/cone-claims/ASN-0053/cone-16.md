I read the four claims in order, tracing every precondition chain, case split, and cited dependency.

---

**SC (SpanClassification)**

The exhaustiveness argument proceeds as a binary tree under the WLOG assumption start(α) ≤ start(β): split reach(α) vs start(β) by T1 trichotomy (three branches), then in the sharing branch split start(α) vs start(β) (two values under WLOG), then split reaches. Every leaf maps to exactly one case. Mutual exclusivity is implicit in the disjoint branches. The WLOG is justified case-by-case: cases (i), (ii), (v) are symmetric by inspection; cases (iii), (iv) carry explicit "or symmetrically" riders.

The disjoint cases (i, ii) are proved by direct chain argument on the half-open denotation. The overlap cases are proved by: case (iii) — exhibiting start(β) as a witness in ⟦α⟧ ∩ ⟦β⟧ (start(β) ∈ T from span definition; T12(b) gives start(β) ∈ ⟦β⟧; Case iii hypothesis places it in ⟦α⟧); case (iv) — deriving ⟦β⟧ ⊆ ⟦α⟧ by four-case analysis on the ≤ abbreviation (never invoking ≤-transitivity as a T1 export), then invoking T12(b) for ⟦β⟧ ≠ ∅; case (v) — ⟦α⟧ = ⟦β⟧ directly from equal boundary points. The Formal Contract correctly notes T1 exports no ≤-transitivity and the proof derives non-strict compositions by case analysis. All paths check out.

**S6 (LevelConstraint)**

Chain: TumblerAdd's result-length postcondition #(s ⊕ ℓ) = #ℓ (earned under the stated well-formedness preconditions) composed with level-uniformity #ℓ = #s gives #reach(σ) = #s. The preconditions of S6 discharge TumblerAdd's preconditions exactly. No gap.

**WF (WellFormedSpanFromEndpoints)**

The critical internal step — discharging D1's precondition divergence(s, r) ≤ #s — proceeds by eliminating T1 case (ii) via the equal-length hypothesis. Case (ii) would require #s + 1 ≤ #s; unfolding ≤ via NAT-order into two sub-cases, each sub-case reaches #s < #s via NAT-addcompat's successor inequality (#s < #s + 1) plus either transitivity (strict sub-case) or substitution (equality sub-case), and NAT-order's irreflexivity closes both. This leaves T1 case (i), giving k ≤ #s with sₖ ≠ rₖ (via NAT-order's exactly-one trichotomy from sₖ < rₖ), whose conjunction matches Divergence case (i)'s unique minimizer, identifying k = divergence(s, r) ≤ #s. TumblerSub's positive branch (zpd(r, s) defined via Divergence symmetry and ZPD's Relationship-to-Divergence) then exports Pos(r ⊖ s) and actionPoint(r ⊖ s) = k ≤ #s as postconditions. Length #(r ⊖ s) = max(#r, #s) = #s from equal-length hypothesis. D1 then applies. Level-uniformity follows from the same length postcondition. All postconditions of WF are derived, not asserted.

**S11c (DifferenceOverlap)**

Case 1: The element-chase is tight. ⊆ direction: t ∈ ⟦α⟧ with t ∉ ⟦β⟧; if t ≥ start(β), then start(β) ≤ t and t < reach(α) < reach(β) gives t ∈ ⟦β⟧ (t ∈ T from ⟦α⟧), contradiction; so t < start(β). ⊇ direction: t < start(β) < reach(α) by T1(c), giving t ∈ ⟦α⟧; t < start(β) excludes t from ⟦β⟧. Witness γ via WF at (start(α), start(β)): s < r by Case 1 hypothesis, #s = #r by level_compat. ✓

Case 2: The proof establishes that within ⟦α⟧, t ∈ ⟦β⟧ iff t < reach(β). The "if" direction derives start(β) ≤ t by case-splitting start(α) ≤ t (in ⟦α⟧) via T1(c) and substitution, both branches yielding start(β) < t hence start(β) ≤ t; combined with t < reach(β), t ∈ ⟦β⟧. The "only if" direction: reach(β) ≤ t places t at or above ⟦β⟧'s exclusive upper bound. The identification {t ∈ ⟦α⟧ : reach(β) ≤ t} = {t : reach(β) ≤ t < reach(α)} is proved by two inclusions: ⊆ drops start(α) ≤ t; ⊇ recovers start(α) ≤ t by case-splitting reach(β) ≤ t using start(α) < reach(β) (Case 2 hypothesis) via T1(c) and substitution. Witness γ' via WF at (reach(β), reach(α)): reach(β), reach(α) ∈ T via TumblerAdd's carrier postcondition on well-formed α, β; reach(β) < reach(α) by Case 2 hypothesis; #reach(β) = #reach(α) via S6 on each span composed with level_compat(start(α), start(β)). ✓

Non-emptiness in both cases is established by exhibiting lower-endpoint membership (start(α) ∈ ⟦α⟧ \ ⟦β⟧ in Case 1 via T12(b) and start(α) < start(β); reach(β) ∈ ⟦α⟧ \ ⟦β⟧ in Case 2 via reach(β) ∈ T already established and reach(β) < reach(α)).

All precondition chains are complete; all cases are walked; all postconditions are derived.

VERDICT: CONVERGED