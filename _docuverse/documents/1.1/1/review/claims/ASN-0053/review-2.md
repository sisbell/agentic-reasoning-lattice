**Foundation audit pass.** The five provided foundations (TA0, D2, TA-strict, T12, D1) are internally consistent; no imported precondition mismatch found across them. D2 correctly discharges all D1 preconditions, and T12 supplies the precondition package (Pos(ℓ), actionPoint(ℓ) ≤ #s) used throughout the ASN.

**S3 (MergeEquivalence).** The WLOG argument is sound: start(α) ≤ start(β) eliminates the reach(β) = start(α) adjacency disjunct via well-formedness (start < reach). Forward and backward set-containment proofs are complete; Case 2 correctly deduces r = reach(β) from t ≥ reach(α) and t < r. Level-uniformity + S6 supply #s = #r for WF; s < r follows from reach(α) > start(α) = s.

**WR (WidthRecovery).** D2's nine preconditions are explicitly discharged in sequence. The divergence-type-(i) argument is reproduced correctly from WF's proof, and the citation to "as in WF's proof" is adequate. TA0 supplies #(s ⊕ ℓ) = #ℓ = #s (level-uniformity closes the second equality), and TA-strict supplies s < reach(σ). Sound.

**S3a (MergeCommutativity).** Trivially correct: A ∪ B = B ∪ A is an instance of logical disjunction commutativity; the proof is complete.

**S4 (SplitPartition).** WF is correctly applied twice (to (s, p) and (p, reach(σ))). For λ: s < p and #s = #p ✓. For ρ: p < reach(σ) and #p = #reach(σ) — the latter from level-uniformity (#s = #ℓ by S6) and TA0 (#(s ⊕ ℓ) = #ℓ = #s). Parts (a), (b), (c) each have closed proofs. D1 is correctly cited for c.

**S6 (LevelConstraint).** Definitional; no proof obligation. The derived fact #reach(σ) = #s is noted inline from TA0 — acceptable as a remark in a definitional claim.

**S3b (MergeSplitInverse).** Case A: the merged span formula, interiority of p, level-compatibility at the split point, and two WR applications are each correct. The final identification λ = α and ρ = β follows cleanly. Case B: the reduction to Case A via S3a is valid — γ's endpoint formula in S3 is symmetric in α and β, so the same span is produced regardless of ordering, and S3a's set-commutativity is consistent with this (span equality follows from S3's uniqueness postulate even if S3a states only set equality; the proof is terse but not wrong). Sound.

**WF (WellFormedSpanFromEndpoints).** Issue below.

---

### WF — TumblerSub and Divergence absent from Depends
**Class**: REVISE
**Foundation**: TumblerSub (ASN-0034), Divergence (ASN-0034) — both cited transitively inside D1 and D2 but not listed in WF's Depends
**ASN**: WF — proof step: *"The width r ⊖ s has a positive component at position k (namely rₖ − sₖ > 0), so it is positive with action point k ≤ #s"*; and: *"the divergence k is of type (i) with k ≤ #s — equal length excludes the prefix case"*
**Issue**: Two steps in WF's proof use ASN-0034 foundations that are not listed in WF's Depends.

(1) **TumblerSub** is required for: the component identity (r ⊖ s)ₖ = rₖ − sₖ that establishes Pos(r ⊖ s); the action-point identification actionPoint(r ⊖ s) = k; and carrier membership r ⊖ s ∈ T. None of these are postconditions of D1 or T12 (WF's only Depends entries). D1's postcondition is only a ⊕ (b ⊖ a) = b; D1's internal use of TumblerSub discharges these facts within D1's own proof but does not re-export them.

(2) **Divergence** is required to discharge D1's precondition divergence(s, r) ≤ #s. WF argues that equal lengths exclude the prefix case, identifying the divergence as type (i) with k ≤ #s. This argument applies Divergence's case classification directly, not via any postcondition of D1 or T12.

**What needs resolving**: TumblerSub (ASN-0034) and Divergence (ASN-0034) must be added to WF's Depends, with citations matching the specific postconditions used: TumblerSub's component formula at the divergence index, its action-point identification, and its carrier-membership guarantee; Divergence's case-(i) criterion (equal lengths → k ≤ min(#a, #b)).

---

VERDICT: REVISE