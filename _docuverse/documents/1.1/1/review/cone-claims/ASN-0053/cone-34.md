I read the four supporting claims (S0, WF, S6, S2) and the apex S11 as a connected system, tracing every precondition chain across claim boundaries and into ASN-0034.

The mathematics is sound. The dependency graph S0←{T1}, S2←{T12}, S6←{TumblerAdd}, WF←{T12,D1,T1,Divergence,TumblerSub,ZPD,NAT-addcompat,NAT-order}, S11←{T1,S2,WF,S6,TumblerAdd,S0} is acyclic. WF's discharge of D1's five preconditions at (s,r) is complete: the equal-length hypothesis correctly excludes T1 case (ii), placing (s,r) in Divergence case (i) with divergence(s,r)=k≤#s, and the symmetric carry to (r,s) feeds ZPD's Relationship-to-Divergence to certify zpd(r,s) defined, licensing TumblerSub's positive branch. S11's four-point ordering start(α)≤start(β)<reach(β)≤reach(α) is correctly derived (reach-half using reach(α)∈T to test membership in ⟦β⟧), the (L)/(M)/(R) decomposition is exhaustive and disjoint, λ and ρ each discharge WF's three preconditions (carrier via TumblerAdd, order via the case condition, length via level_compat for λ and S6 for ρ), and the tightness contradiction correctly applies S0 to the hypothetical γ. The worked example checks against every postcondition. Hypotheses are tightly used: dropping level-uniformity breaks S6→ρ's length precondition; dropping level_compat breaks λ.

What I found is confined to prose noise — defensive justification and use-site inventory in structural slots, the reviser-drift patterns the brief asks to flag at source.

### S2 wards off an ill-typed comparison nobody proposed
**Class**: OBSERVE
**Foundation**: T12 (SpanWellDefinedness)
**ASN**: S2, *Preconditions*: "The last is a comparison of natural numbers (actionPoint(ℓ) ∈ ℕ), not the type-incoherent comparison of the tumbler s ⊕ ℓ against #s." The proof body carries the same: "not of the end offset s ⊕ ℓ, which is a tumbler."
**Issue**: The well-formedness condition is `actionPoint(ℓ) ≤ #s`, a plain ℕ≤ℕ comparison. The prose invents a rival reading — comparing the tumbler `s ⊕ ℓ` against `#s` — that is obviously ill-typed and that nothing in the definition invites, then explains the precondition is *not* that. This is defensive justification: it explains away a confusion rather than advancing the single-step argument (s ∈ span by T12(b)). The precise reader must skip past it.
**What needs resolving**: State the precondition as `actionPoint(ℓ) ≤ #s` without the contrastive "not the type-incoherent comparison …" gloss in both the proof and the contract.

### S6 Depends inventories why other foundations don't supply the length
**Class**: OBSERVE
**Foundation**: TumblerAdd (result-length identity #(a ⊕ w) = #w)
**ASN**: S6, *Depends* → TumblerAdd: "This is the sole source of the addition result-length: the in-scope foundations supply only the subtraction length (TumblerSub: #(a ⊖ w) = L) and the round-trip identity (D1: a ⊕ (b ⊖ a) = b), neither of which yields #(s ⊕ ℓ) = #ℓ for a general width ℓ."
**Issue**: A dependency slot should state what TumblerAdd exports and where S6 consumes it. This sentence instead surveys two *unused* foundations to argue why they couldn't substitute — a use-site inventory that explains why the axiom is needed rather than what it says. It adds nothing a downstream consumer of S6 can act on.
**What needs resolving**: Trim the "sole source … neither of which yields …" survey; keep the statement that TumblerAdd supplies #(s ⊕ ℓ) = #ℓ under the discharged preconditions.

### S11 Axiom slot re-narrates the entire proof with use-site commentary
**Class**: OBSERVE
**Foundation**: TumblerAdd, T1, S0, S2, WF, S6
**ASN**: S11, *Axiom* field — a multi-hundred-word paragraph reciting the boundary characterization, the S0 bracketing case-split, WF's carrier discharge, and S6's length propagation, including phrases like "this membership is consumed twice. It is needed already in the boundary characterization … and again in the ρ-construction".
**Issue**: The *Axiom* slot is meant to record the exported facts S11 stands on, not to re-tell the proof. As written it is essay content in a structural slot, duplicating the proof body and threading use-site inventory through it ("consumed twice", "needed already in … and again in …"). The duplication is also a drift hazard: any future correction to the proof must be mirrored here or the two silently diverge.
**What needs resolving**: Reduce the *Axiom* field to the bare exported statements relied on (TumblerAdd carrier + result-length, T1 totality/(c), S0 convexity, S2 non-emptiness, WF construction, S6 equal-length consequence); let the proof body carry the use-site narration once.

### S11 boundary start-characterization uses `start(β) ∈ ⟦β⟧` without inline grounding
**Class**: OBSERVE
**Foundation**: T12(b) / S2 (s ∈ span(s,ℓ))
**ASN**: S11, proof: "For the start: start(β) ∈ ⟦β⟧ ⊆ ⟦α⟧ gives start(α) ≤ start(β)"; the *Depends*/*Axiom* note scopes S2's role to "the tightness argument to obtain a witness t ∈ ⟦β⟧."
**Issue**: The start-half of the containment-to-ordering bridge — the load-bearing step that produces `start(α) ≤ start(β)` — depends on `start(β) ∈ ⟦β⟧`, i.e. β's start lying in its own denotation. That fact is S2's postcondition (equivalently T12(b)), and S2 is a declared dependency, but the proof asserts it bare and the dependency note attributes S2 only to tightness. The fact is in scope, so this is traceability, not an ungrounded symbol — but the use-site for S2/T12(b) in the boundary derivation goes unrecorded.
**What needs resolving**: Cite S2 (or T12(b)) at the boundary start-characterization where `start(β) ∈ ⟦β⟧` is invoked, and extend the S2 dependency note to cover this use alongside the tightness witness.

VERDICT: OBSERVE