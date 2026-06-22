Reading the five claims against the foundation statements.

**S0 (Convexity):** The four-case lower-bound derivation (distributing `start(σ) ≤ p ∧ p ≤ q` through the abbreviation) and the two-case upper-bound derivation both reduce correctly to T1 postcondition (c) or equality substitution. The Formal Contract correctly notes that ≤-transitivity is not a T1 export and is derived in-place. Sound.

**WF (WellFormedSpanFromEndpoints):** Case-(ii) elimination is clean: `#s = #r` forces `#s + 1 ≤ #s`, which the Axiom-field unfolds into `#s + 1 < #s` and `#s + 1 = #s`; NAT-addcompat's successor inequality chains with transitivity or substitution to `#s < #s`, and NAT-order's irreflexivity closes both sub-cases. Divergence's case-(i) uniqueness identifies the T1 witness `k` with `divergence(s, r) ≤ #s`, discharging D1's fifth precondition. TumblerSub's positive branch is entered via ZPD's Relationship-to-Divergence after carrying the case-(i) structure across the pair swap. ActionPoint's least-element clause identifies `k` as the action point; `k ≤ #s = #(r ⊖ s)` by the length postcondition `max(#r, #s) = #s`. Level-uniformity follows from the same length identity. D1 closes `reach(γ) = r`. Sound.

**S6 (LevelConstraint):** TumblerAdd's result-length identity `#(s ⊕ ℓ) = #ℓ`, earned under the well-formedness preconditions, composed with `#ℓ = #s` from level-uniformity, gives the chain `#start = #width = #reach`. The Depends correctly identifies this as the sole source for the addition result-length, distinct from TumblerSub's length and D1's round-trip. Sound.

**S2 (EmptyDistinction):** T12's postcondition (b), `s ∈ span(s, ℓ)`, is the single step; the well-formedness preconditions S2 assumes are exactly those T12 requires. Sound.

**S11 (DifferenceBound):** Carrier membership `reach(α), reach(β) ∈ T` is placed at the outset from TumblerAdd's carrier postcondition under each span's well-formedness — this is the load-bearing setup for both the boundary-reach test and the ρ-construction. The reach-bound half of the boundary characterization correctly needs `reach(α) ∈ T` to test membership in `⟦β⟧ = {t ∈ T : start(β) ≤ t < reach(β)}`. WF's preconditions for ρ are discharged: carrier membership from the above setup; level-compatibility `#reach(β) = #reach(α)` via S6 (`#reach(σ) = #start(σ)` for each span) composed with `level_compat(start(α), start(β))`. Tightness: S2 supplies `t ∈ ⟦β⟧`; the bracketing `start(α) ≤ t ≤ reach(β)` is discharged by weakening `t < reach(β)` and by the two-case composition of `start(α) < start(β)` with `start(β) ≤ t`, mirroring S0's own technique; S0 then forces `t ∈ ⟦γ⟧ = ⟦λ⟧ ∪ ⟦ρ⟧`, contradicted by `t ∉ ⟦λ⟧` (since `t ≥ start(β) = reach(λ)`) and `t ∉ ⟦ρ⟧` (since `t < reach(β) = start(ρ)`). Sound.

---

### S11 Axiom field carries proof-body material in a structural-axiom slot
**Class**: OBSERVE
**Foundation**: N/A
**ASN**: S11 (DifferenceBound), Formal Contract — Axiom field: "TumblerAdd's carrier postcondition a ⊕ w ∈ T, instantiated at (start(σ), width(σ)) under each span σ ∈ {α, β}'s well-formedness, places reach(α), reach(β) ∈ T at the outset. The boundary characterization … a witness t ∈ ⟦β⟧ is bracketed … WF's carrier preconditions s, r ∈ T are immediate for λ … WF's length preconditions are discharged from S6…"
**Issue**: The Axiom field in NAT-order and NAT-addcompat correctly holds posited clauses — facts primitive at this level of the specification. S11's Axiom field holds seven sentences of derived reasoning: carrier membership derivation, boundary-condition derivation, witness-extraction strategy, and WF precondition discharge for both λ and ρ. These are proof steps, not axioms. The proof body already covers all of them. Placing proof summary in the Axiom slot conflates what is posited with what is proved and means a reader scanning for axiomatic inputs must sift through a proof recapitulation to find them.

VERDICT: OBSERVE