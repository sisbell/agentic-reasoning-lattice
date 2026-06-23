## Audit

**S3 (MergeEquivalence)**

The adjacency-disjunct dismissal chains reach(β) ≤ start(β) (from reach(β) = start(α) ≤ start(β) under WLOG) with start(β) < reach(β) (TA-strict at β) to deliver reach(β) < reach(β), which T1 irreflexivity refutes. The mixed ≤-then-< transitivity used here (a ≤ b ∧ b < c → a < c) follows cleanly from T1's ≤ definition and transitivity of <. Sound.

The converse case split (Case 1: t < reach(α); Case 2: t ≥ reach(α)) is exhaustive under T1 trichotomy. Case 2's chain — reach(α) ≤ t < r forces r > reach(α), forcing r = reach(β); overlap/adjacency reach(α) ≥ start(β) then gives start(β) ≤ t < reach(β) — is valid at every step. The forward inclusion (⟦α⟧ ∪ ⟦β⟧ ⊆ {t : s ≤ t < r}) is separately verified. Sound.

WF's preconditions (s, r ∈ T; s < r; #s = #r) are each explicitly discharged: s = start(α) ∈ T directly; r ∈ T via TumblerAdd's carrier postcondition at each well-formed σ; s < r from TA-strict at α giving reach(α) > s together with r ≥ reach(α) (mixed transitivity); #s = #r from S6 applied to both α and β and level_compat(start(α), start(β)). Sound.

The "as S11 does" references in S3 and S4 are stylistic cross-references within the ASN; the full argument is supplied inline in both sites, so no reasoning is deferred.

---

**S4 (SplitPartition)**

WF is invoked twice. For λ = (s, p ⊖ s): preconditions s, p ∈ T; s < p (interiority); #s = #p (level_compat) — all immediate. For ρ = (p, reach(σ) ⊖ p): p ∈ T (given); reach(σ) ∈ T (TumblerAdd's carrier postcondition at (start(σ), width(σ)) under σ's well-formedness); p < reach(σ) (interiority); #p = #reach(σ) — the last step uses TumblerAdd's result-length identity (#(s ⊕ ℓ) = #ℓ = #s, level-uniformity) together with level_compat(s, p). TumblerAdd is in S4's Depends. S6 is not cited but is not needed as an intermediate lemma since the derivation goes directly through TumblerAdd + the level-uniform precondition. Sound.

Parts (a), (b), (c) are each clean. Part (c) reads WF's postcondition directly: reach(λ) = s ⊕ (p ⊖ s) = p; start(ρ) = p by construction. Sound.

---

**WR (WidthRecovery)**

D2 is invoked at (a, b, w) = (s, reach(σ), ℓ). All nine of D2's preconditions are discharged: membership from T12/TA0; a < b from TA-strict; Pos(ℓ) and actionPoint(ℓ) ≤ #s from T12; #s ≤ #reach(σ) (both = #s via TA0); s ⊕ ℓ = reach(σ) by definition; divergence(s, reach(σ)) ≤ #s via the inline argument. The divergence bound proof correctly eliminates T1 case (ii) using #s = #reach(σ) and NAT-addcompat's strict successor inequality, then identifies the case-(i) witness k = divergence(s, reach(σ)) ≤ #s via Divergence's uniqueness clause. Sound.

---

**WF (WellFormedSpanFromEndpoints)**

The case-(ii) elimination is the most elaborate step: #s = #r collapses k = #s + 1 ≤ #r to #s + 1 ≤ #s; NAT-order unfolds ≤ into two sub-cases; NAT-addcompat's successor inequality #s < #s + 1 chains with transitivity (strict sub-case) or substitution (equality sub-case) to reach #s < #s; NAT-order irreflexivity closes both. This is executed carefully and completely. Sound.

TumblerSub's Pos(r ⊖ s) postcondition fires directly from zpd(r, s) being defined — no component-level detour needed. The action-point bound actionPoint(r ⊖ s) = k ≤ #(r ⊖ s) = #s satisfies T12. Level-uniformity of γ follows from #(r ⊖ s) = max(#r, #s) = #s = #start(γ). The D1 precondition divergence(s, r) ≤ #s is discharged before D1 is invoked. Sound.

---

**S6 (LevelConstraint)**

A direct corollary of TumblerAdd's result-length postcondition (#(a ⊕ w) = #w at (s, ℓ)) and the level-uniform hypothesis #ℓ = #s. The commentary on the conditional nature of the length identity (requiring Pos(ℓ) and actionPoint(ℓ) ≤ #s) is correct: without those preconditions, s ⊕ ℓ need not be defined. Sound.

---

**S4a (SplitMergeInverse)**

S3's preconditions are satisfied: λ and ρ are well-formed level-uniform spans (S4 postcondition); level_compat(s, p) is a precondition of S4a; adjacency holds since reach(λ) = p = start(ρ). Under start(λ) = s < p = start(ρ), the WLOG in S3 applies directly. S3 constructs γ with s_m = min(s, p) = s and r_m = max(p, reach(σ)) = reach(σ). WR delivers reach(σ) ⊖ s = ℓ. Hence γ = (s, ℓ) = σ. Sound.

---

No correctness issues found across any claim. Dependency chains are closed, case analyses are exhaustive, precondition discharges are explicit, and the proofs do not defer reasoning with "by similar reasoning."

VERDICT: CONVERGED