Reading the foundation contracts then tracing each claim's proof, precondition chain, and Depends entries.

---

**S0 — Convexity.** The proof is sound. Mixed transitivity (q ≤ r with r < reach gives q < reach) follows by unfolding ≤ ≡ < ∨ = and applying T1(c) in the strict branch and substitution in the equality branch; T1 covers both. No gap.

**WF — WellFormedSpanFromEndpoints.** The proof correctly discharges all five of D1's preconditions. The divergence bound divergence(s, r) ≤ #s is the most load-bearing: T1 case (ii) is excluded by #s = #r (it would force #s < #r), leaving case (i) with k ≤ #s and sₖ ≠ rₖ; the conjunction 1 ≤ k ∧ k ≤ #s ∧ k ≤ #r ∧ sₖ ≠ rₖ ∧ prefix-agreement exactly satisfies Divergence case (i)'s qualifier, whose uniqueness identifies k = divergence(s, r). The actionPoint ≤ #s bound follows. Pos(r ⊖ s) and r ⊖ s ∈ T follow from TumblerSub's conditional postconditions (zpd is defined since s ≠ r). Level-uniformity #(r ⊖ s) = max(#r, #s) = #s closes the chain. Proof is sound.

**S2 — EmptyDistinction.** Proof is sound: TA-strict under Pos(ℓ) and actionPoint(ℓ) ≤ #s gives s ⊕ ℓ > s, so s < reach(σ) and s ≤ s, placing s ∈ ⟦s, ℓ⟧. The T12 citation in Depends carries a description issue handled below.

**S11 — DifferenceBound.** Boundary derivation (start(α) ≤ start(β) from S2 + subset; reach(β) ≤ reach(α) by contradiction via reach(α) ∈ ⟦β⟧ ⊆ ⟦α⟧) is correct. The three-way (L)/(M)/(R) partition is exhaustive by T1 totality. λ is constructed from WF with WF's length precondition #start(α) = #start(β) supplied directly by level_compat. ρ is constructed from WF with #reach(β) = #reach(α) discharged via S6 + level_compat chaining. The tightness argument picks t ∈ ⟦β⟧ (S2), uses start(α) ∈ ⟦λ⟧ ⊆ ⟦γ⟧ and reach(β) ∈ ⟦ρ⟧ ⊆ ⟦γ⟧ under the contradiction assumption, applies S0 with p = start(α) ≤ t ≤ reach(β) = r to get t ∈ ⟦γ⟧, then contradicts t ∉ ⟦λ⟧ (t ≥ start(β) = reach(λ)) ∧ t ∉ ⟦ρ⟧ (t < reach(β) = start(ρ)). Proof is sound.

---

### S6 formal contract — missing preconditions for well-formedness
**Class**: REVISE
**Foundation**: TumblerAdd (TumblerAdd, ASN-0034) — postcondition `a ⊕ w ∈ T` and `#(a ⊕ w) = #w` require `Pos(w)` and `actionPoint(w) ≤ #a`
**ASN**: S6 (LevelConstraint) — Formal Contract has Postconditions and Depends but no Preconditions section; body reads "For a level-uniform span σ = (s, ℓ) — one with level_compat(s, ℓ), i.e. #s = #ℓ — start, width, and reach inhabit a single tumbler length"
**Issue**: The derivation `#reach(σ) = #(s ⊕ ℓ) = #ℓ` requires `s ⊕ ℓ` to be defined and in T, which demands `Pos(ℓ)` and `actionPoint(ℓ) ≤ #s` — the T12 conditions for well-formedness. These are absent from the formal contract. The Depends section acknowledges them in passing ("where Pos(ℓ) and actionPoint(ℓ) ≤ #s hold, so s ⊕ ℓ is defined"), but the claim as stated universally quantifies over level-uniform (s, ℓ) pairs without restricting to well-formed ones. Unlike S0, whose precondition `p ∈ ⟦σ⟧` implicitly filters out non-well-formed spans (an empty denotation makes the antecedent vacuously false), S6 has no such self-protective filter. A downstream consumer can instantiate S6 at a level-uniform but non-well-formed (s, ℓ) — one where `Pos(ℓ)` fails — where reach(σ) is undefined and the length identity does not apply.
**What needs resolving**: S6's formal contract must acquire a Preconditions section stating the well-formedness conditions (`s ∈ T`, `ℓ ∈ T`, `Pos(ℓ)`, `actionPoint(ℓ) ≤ #s`) under which reach(σ) = s ⊕ ℓ is defined and TumblerAdd's postconditions apply.

---

### S2 Depends — T12 citation has the logical direction inverted
**Class**: OBSERVE
**Foundation**: T12 (SpanWellDefinedness, ASN-0034) — postconditions: (a) s ⊕ ℓ ∈ T, (b) s ∈ span(s, ℓ), (c) order-convexity
**ASN**: S2 (EmptyDistinction) — Depends entry: "T12 (SpanWellDefinedness, ASN-0034) — supplies the well-formedness preconditions on (s, ℓ): Pos(ℓ) (i.e. ℓ > 0) and actionPoint(ℓ) ≤ #s, the conditions of Definition (Span) the proof starts from. T12's exported postconditions are s ⊕ ℓ ∈ T, s ∈ span(s, ℓ), and order-convexity; the strict advancement s ⊕ ℓ > s used here is TA-strict's postcondition, not T12's."
**Issue**: T12 is a theorem proved FROM the well-formedness conditions; it does not supply them to S2. Those conditions are S2's own hypotheses. What T12 does export is postcondition (b): s ∈ span(s, ℓ) — which is S2's conclusion. The description says T12 supplies preconditions and explicitly disavows use of T12's postconditions, but T12(b) is the very statement S2 proves. The citation is described as if T12 is a naming convention for the preconditions when it is in fact a theorem whose output coincides with S2's output.

---

### S11 Depends — TumblerAdd cited only for length identity; carrier membership use for ρ undescribed
**Class**: OBSERVE
**Foundation**: TumblerAdd (TumblerAdd, ASN-0034) — postconditions include both `a ⊕ w ∈ T` and `#(a ⊕ w) = #w`
**ASN**: S11 (DifferenceBound) — Depends entry: "TumblerAdd (TumblerAdd, ASN-0034) — supplies the result-length identity #(a ⊕ w) = #w, the exported postcondition of ⊕ that the ρ-construction consumes when discharging WF's length precondition #reach(β) = #reach(α)"
**Issue**: Constructing ρ via WF requires passing reach(β) ∈ T and reach(α) ∈ T as WF's `s ∈ T` / `r ∈ T` preconditions. These follow from TumblerAdd's carrier postcondition `a ⊕ w ∈ T` applied to spans β and α under their well-formedness conditions. TumblerAdd is cited but only the length identity is described; the carrier membership step is not accounted for in the Depends entry or the proof text. The ρ paragraph concludes "With reach(β) < reach(α) already in hand, WF gives a well-formed level-uniform span" without discharging WF's carrier preconditions.

---

VERDICT: REVISE