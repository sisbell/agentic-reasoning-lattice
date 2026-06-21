Reading the ASN end-to-end against the foundation statements before issuing findings.

---

**S0 (Convexity)** — The proof is one line that correctly chains T1's total-order properties to get start(σ) ≤ q < reach(σ). The formal contract's Axiom clause names the two inferential steps explicitly. Sound.

**WF (WellFormedSpanFromEndpoints)** — The proof walks all five of D1's preconditions: s, r ∈ T and s < r are given; #s ≤ #r follows from #s = #r; divergence(s, r) ≤ #s is derived by ruling out T1 case (ii) via the equal-length hypothesis and identifying T1's witness k with divergence(s, r) through Divergence case (i)'s uniqueness (the prefix-agreement clause (A i : 1 ≤ i < k : sᵢ = rᵢ) in T1's definition makes k the first disagreement position, which is exactly Divergence case (i)'s minimality condition). TumblerSub's postconditions correctly source Pos(r ⊖ s), actionPoint identification, and level-uniformity. D1 and TumblerSub citations are clean. Sound.

**S6 (LevelConstraint)** — Definitional for level\_compat and level-uniform. The consequence #reach(σ) = #s is claimed via "the result-length identity (#(s ⊕ ℓ) = #ℓ)" with no Depends section. TumblerAdd is the source of this identity; it appears in D1's internal Depends but is not among the exported foundation statements. S11 relies on S6 for the critical step #reach(β) = #reach(α) needed to apply WF for ρ. Gap noted below.

**S2 (EmptyDistinction)** — The argument is correct: T12(b) gives start(σ) ∈ span(σ), establishing non-emptiness. But the formal contract misattributes roles. Gap noted below.

**S11 (DifferenceBound)** — Boundary characterisation, three-way partition, span constructions for λ and ρ, and tightness argument all follow correctly. The tightness proof picks t = start(β) ∈ ⟦β⟧ (grounded by T12(b)); S0 with p = start(α) ∈ ⟦γ⟧, r = reach(β) ∈ ⟦ρ⟧ ⊆ ⟦γ⟧, q = t gives t ∈ ⟦γ⟧; then t ≥ reach(λ) = start(β) excludes ⟦λ⟧ and t < start(ρ) = reach(β) excludes ⟦ρ⟧ — contradiction. The only unresolved dependency is S6's result-length identity, which propagates from finding 2 below.

---

### S2 Axiom clause credits TA-strict with establishing its own precondition
**Class**: REVISE
**Foundation**: TA-strict (StrictIncrease) — postcondition `a ⊕ w > a`; preconditions include `Pos(w)`
**ASN**: S2 (EmptyDistinction) — Axiom clause `(TA-strict): Every well-formed span has strictly positive length: ℓ > 0` and Depends entry `TA-strict — supplies the axiom ℓ > 0 (strictly positive length for every well-formed span)`
**Issue**: TA-strict's postcondition is `a ⊕ w > a`; `Pos(w)` is its precondition, not its conclusion. The Axiom clause labels TA-strict as the source of `ℓ > 0` (i.e., `Pos(ℓ)`), but that property is a precondition of T12 — the definition of span well-formedness — not something TA-strict establishes. What TA-strict actually contributes to S2 is `s ⊕ ℓ > s` given `Pos(ℓ)` as input. The citation as written has TA-strict proving its own precondition. The proof body then separately credits T12 with strict monotonicity (via T12(b): `s ∈ span(s, ℓ)` implies `s < s ⊕ ℓ`), which is the correct citation for that step. The Axiom and Depends fields swap the roles of the two dependencies.
**What needs resolving**: The Axiom clause must correctly attribute the source of `Pos(ℓ)` (T12's well-formedness precondition, not TA-strict's output) and the source of `s ⊕ ℓ > s` (TA-strict's postcondition, or equivalently T12(b)). The Depends entry for TA-strict must state what it actually exports — `s ⊕ ℓ > s` — not its precondition.

---

### S6 asserts result-length identity without a foundation citation; S11 inherits the gap
**Class**: REVISE
**Foundation**: TumblerAdd (internal to ASN-0034, cited in D1's Depends, not in the exported foundation statements) — result-length identity `#(a ⊕ w) = #w`
**ASN**: S6 (LevelConstraint) — `#reach(σ) = #s by the result-length identity (#(s ⊕ ℓ) = #ℓ)`; S11 (DifferenceBound) — Axiom clause `WF's length precondition #reach(β) = #reach(α) we discharge through S6`
**Issue**: S6 has no Depends section. The identity `#(s ⊕ ℓ) = #ℓ` is sourced from TumblerAdd, which does not appear among the exported foundation statements (T1, T12, TumblerSub, D1, Divergence, TA-strict). The exported foundations give the length of subtraction (TumblerSub: `#(a ⊖ w) = L`) and the round-trip identity (D1: `a ⊕ (b ⊖ a) = b`) but not the addition result-length in general. S11's construction of the right-difference span ρ requires `#reach(β) = #reach(α)`, which the proof discharges through the chain `#reach(σ) = #start(σ)` via S6's result-length identity. Without a grounded source for `#(s ⊕ ℓ) = #ℓ`, S6's consequence is ungrounded and S11's ρ-construction step lacks a complete precondition chain.
**What needs resolving**: S6 must acquire a formal Depends entry naming the source of `#(s ⊕ ℓ) = #ℓ`. Either TumblerAdd must be promoted to an exported foundation statement of ASN-0034 and cited, or the identity must be derived from foundations already in scope. Until the grounding is supplied, S11 must also carry an explicit citation for the result-length identity it consumes through S6.

---

### S0 proof invokes mixed transitivity without walking the case split
**Class**: OBSERVE
**Foundation**: T1 (LexicographicOrder) — postcondition (c) transitivity of `<`; `≤` abbreviation `a ≤ b ≡ a < b ∨ a = b`
**ASN**: S0 (Convexity) — Axiom clause `q ≤ r with r < reach(σ) give q < reach(σ)`
**Issue**: T1(c) gives `<` transitivity; `≤` is an abbreviation, not independently axiomatised as transitive. The step `q ≤ r ∧ r < reach(σ) → q < reach(σ)` requires unfolding `≤` into two sub-cases (q < r and q = r) and applying T1(c) or substitution respectively. The Axiom clause asserts the result as immediate from "≤ is a total order" without walking the sub-cases.

---

VERDICT: REVISE