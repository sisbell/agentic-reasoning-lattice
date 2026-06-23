Reading each claim against the foundations, tracing every precondition chain.

---

**S0 — Convexity**

The two-case / four-case unfoldings are complete and reduce correctly to T1(c) or equality substitution. Carrier membership for q follows from the explicit precondition; reach(σ) is implicitly in T by virtue of p ∈ ⟦σ⟧ being a satisfiable T-order statement. The Depends list (T1 only) is correct: the proof uses no other foundation directly. No issues.

**WF — WellFormedSpanFromEndpoints**

D1 preconditions: s, r ∈ T (hypotheses), s < r (hypothesis), #s ≤ #r (from #s = #r), divergence(s, r) ≤ #s (established). The T1 case (ii) elimination is correct: #s = #r forces k = #s + 1 ≤ #s, which NAT-order's ≤-definition splits into #s + 1 < #s and #s + 1 = #s; NAT-addcompat's #s < #s + 1 and NAT-order's transitivity close both sub-cases to #s < #s, contradicting irreflexivity. Divergence symmetry carries the case-(i) witness k to (r, s); ZPD's Relationship-to-Divergence then gives zpd(r, s) = k, defined, licensing TumblerSub's positive branch. Pos(r ⊖ s), actionPoint(r ⊖ s) = k ≤ #s, and #(r ⊖ s) = #s follow from TumblerSub's postconditions. T12 is satisfied; D1 closes reach(γ) = r. Level-uniformity #(r ⊖ s) = #s is immediate since L = #s when #r = #s. Depends list complete.

**S6 — LevelConstraint**

Single application of TumblerAdd's result-length identity #(s ⊕ ℓ) = #ℓ under the span's well-formedness preconditions, composed with #ℓ = #s from level-uniformity. Correct.

**S2 — EmptyDistinction**

Direct application of T12(b): start ∈ span(start, width) for any well-formed span. Correct.

**S11 — DifferenceBound**

reach(α), reach(β) ∈ T established at the outset via TumblerAdd's carrier postcondition. The boundary characterization is sound: start(β) ∈ ⟦β⟧ ⊆ ⟦α⟧ gives start(α) ≤ start(β); the reach half is by contradiction, with reach(α) ∈ T placing it in ⟦β⟧ = {t ∈ T : start(β) ≤ t < reach(β)} (start(β) ≤ reach(α) by weakening, reach(α) < reach(β) by the contradictory assumption), then ⟦β⟧ ⊆ ⟦α⟧ forces reach(α) < reach(α), contradicting T1 irreflexivity. The (L)/(M)/(R) partition is exhaustive and pairwise disjoint by T1 totality. λ is constructed via WF from (start(α), start(β)) — both span starts, hence in T, with level_compat supplying #start(α) = #start(β). ρ is constructed via WF from (reach(β), reach(α)) — carrier membership already established, #reach(β) = #reach(α) from S6 composed with level_compat. The tightness argument: reach(β) ∈ ⟦ρ⟧ and start(α) ∈ ⟦λ⟧ (both by S2 on their respective well-formed spans); the bracket start(α) ≤ t ≤ reach(β) is discharged via weakening (t < reach(β) → t ≤ reach(β)) and by composing start(α) < start(β) with start(β) ≤ t through the abbreviation case-split (exactly the technique S0 itself uses); S0 then forces t ∈ ⟦γ⟧, contradicted by t ∉ ⟦λ⟧ (t ≥ start(β) = reach(λ)) and t ∉ ⟦ρ⟧ (t < reach(β) = start(ρ)). Depends list covers all direct citations.

---

### S11 Axiom slot contains proof-level content
**Class**: OBSERVE
**Foundation**: n/a
**ASN**: S11 formal contract, `*Axiom:*` field
**Issue**: The `Axiom:` slot in S11's formal contract contains a paragraph-length proof sketch — TumblerAdd postcondition instantiation, the boundary-characterization derivation, WF precondition discharge for ρ, and the S0 invocation in the tightness argument. Compare with S0's `Axiom:` slot, which correctly names a single foundation export and distinguishes what T1 exports from what must be derived. S11's slot is a compressed proof narrative placed in a structural position where a reader expects axiomatic content, not derivations.
**What needs resolving**: The proof-level content in the Axiom field should migrate to the proof body or a clearly labeled `*Proof notes:*` field. The Axiom slot, if retained, should name the foundation exports the proof relies on (TumblerAdd's carrier postcondition and result-length identity) without re-executing the derivations.

---

VERDICT: OBSERVE