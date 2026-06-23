Tracing all six claims against the foundation statements. I'll work through each proof's precondition chains, case analyses, and postcondition derivations systematically before reporting.

---

**WR — WidthRecovery**

D2 requires nine preconditions for (a, b, w) = (s, reach(σ), ℓ). The proof discharges them: s, reach(σ) ∈ T (carrier; TA0), ℓ ∈ T and Pos(ℓ) and actionPoint(ℓ) ≤ #s (σ well-formed), s ⊕ ℓ = reach(σ) (definition), #s ≤ #reach(σ) (from TA0's result-length #(s ⊕ ℓ) = #ℓ = #s, so both sides equal), s < reach(σ) (TA-strict). The fifth precondition divergence(s, reach(σ)) ≤ #s is established by the inline witness argument: T1 witnesses s < reach(σ) with k; equal length #s = #reach(σ) excludes T1 case (ii) via NAT-addcompat (#s < #s+1) and NAT-order irreflexivity; case (i) gives k ≤ #s with sₖ ≠ reach(σ)ₖ; Divergence's case-(i) minimality identifies k = divergence(s, reach(σ)). All D2 preconditions are met. Proof is sound.

**WF — WellFormedSpanFromEndpoints**

D1's preconditions at (s, r): s, r ∈ T (hypotheses), s < r (hypothesis), #s ≤ #r (from #s = #r), and divergence(s, r) ≤ #s. The divergence bound uses the same equal-length T1 case elimination; case (i) gives k = divergence(s, r) ≤ #s. TumblerSub on (r, s): r ≥ s from T1's abbreviations; zpd(r, s) is defined because Divergence case (i) at (s, r) carries to (r, s) by Divergence symmetry, and ZPD's Relationship-to-Divergence equates zpd(r, s) = k; hence the positive branch applies with Pos(r ⊖ s), actionPoint(r ⊖ s) = k ≤ #(r ⊖ s) = max(#r, #s) = #s. T12 is satisfied, D1 gives reach(γ) = r. Level-uniformity: #width(γ) = #(r ⊖ s) = max(#r, #s) = #s = #start(γ). Proof is sound.

**S6 — LevelConstraint**

The claim that #start(σ) = #width(σ) = #reach(σ) follows directly from TumblerAdd's result-length postcondition #(s ⊕ ℓ) = #ℓ (earned under σ's well-formedness preconditions) and the level-uniform hypothesis #ℓ = #s. The distinction between well-formed level-uniform (the identity holds) and merely level-uniform without Pos(ℓ) (no claim on reach) is correctly drawn. Proof is sound.

**S4 — SplitPartition**

For λ: WF preconditions at (s, p) — s ∈ T (σ well-formed), p ∈ T (precondition), s < p (interiority), #s = #p (level_compat) — are met; WF gives λ well-formed with reach(λ) = p. For ρ: reach(σ) ∈ T from TumblerAdd's carrier postcondition; p < reach(σ) from interiority; #p = #reach(σ) from TumblerAdd's result-length identity (#(s ⊕ ℓ) = #ℓ = #s) and level_compat(s, p); WF gives ρ well-formed with reach(ρ) = reach(σ). Parts (a)–(c) follow from T1's total order and WF's postcondition reach(λ) = p = start(ρ). Proof is sound.

**S3 — MergeEquivalence**

Under WLOG start(α) ≤ start(β), the reach(β) = start(α) disjunct is vacuous: reach(β) = start(α) ≤ start(β) < reach(β) (TA-strict at β) gives reach(β) < reach(β) by T1's mixed ≤-< transitivity, contradicting irreflexivity. The union argument covers both cases by T1's dichotomy; Case 2 correctly identifies r = reach(β) when t ≥ reach(α) forces r > reach(α) hence r = max = reach(β). reach(α), reach(β) ∈ T by TumblerAdd; s < r from s = start(α) < reach(α) ≤ r (TA-strict then max bound); #s = #r from S6 at α and β with level_compat; WF gives γ well-formed. Proof is sound.

**S3b — MergeSplitInverse**

The non-emptiness facts (†) from TA-strict ground every interiority step. Case A: r = reach(β) > reach(α) = start(β) by (†); γ = (start(α), reach(β) ⊖ start(α)); p = start(β) interior (start(α) < start(β) via (†) at α and reach(α) = start(β); start(β) < reach(β) = reach(γ) via (†) at β); WR at α recovers p ⊖ start(α) = reach(α) ⊖ start(α) = width(α); WR at β recovers reach(β) ⊖ start(β) = width(β). Case B: s = start(β), r = reach(α), p = start(α) interior; level_compat(start(β), start(α)) = level_compat(start(α), start(β)) by symmetry of #-equality; WR at β recovers start(α) ⊖ start(β) = reach(β) ⊖ start(β) = width(β) using start(α) = reach(β); WR at α recovers reach(α) ⊖ start(α) = width(α). In both cases {λ, ρ} = {α, β} with the stated assignment. The two cases are mutually exclusive (both holding simultaneously would give start(α) < start(β) and start(β) < start(α)). Proof is sound.

---

### S4 Depends entry omits result-length use of TumblerAdd

**Class**: OBSERVE
**Foundation**: TumblerAdd (TumblerAdd, ASN-0034) — postcondition `#(a ⊕ w) = #w`
**ASN**: S4 (SplitPartition), Depends entry for TumblerAdd and proof step for ρ: "(level-uniformity gives #reach = #s = #p)"
**Issue**: S4's Depends entry for TumblerAdd reads: "supplies the carrier postcondition a ⊕ w ∈ T … to place reach(σ) ∈ T." The proof also relies on TumblerAdd's result-length postcondition `#(s ⊕ ℓ) = #ℓ` to establish `#reach(σ) = #ℓ = #s = #p` — the equal-length precondition that WF requires for the ρ invocation. That use appears only as the undocumented parenthetical "(level-uniformity gives #reach = #s = #p)." S3 handles the identical step by explicitly citing S6 in its Depends. S4 cites neither S6 nor the result-length postcondition of TumblerAdd for this purpose.

VERDICT: OBSERVE