Reading the ASN as a system against the ASN-0034 foundation, I traced every WF/D1/D2/TA-assoc/TA-LC precondition chain through the WF/WR core into the intersection, merge, split, normalization, and difference cones. The proofs are sound: the precondition chains for displacement round-trip (WF→D1), uniqueness (WR→D2), associativity (S5→TA-assoc→TA-LC), and the case splits in SC/S9/S11c/S11d all close, and the level-uniformity length propagation (#start = #width = #reach) is correctly threaded everywhere it is consumed. I found no correctness defect. The items below are observations only.

### D0 listed as a cited property but never invoked
**Class**: OBSERVE
**Foundation**: D0 (DisplacementWellDefined, ASN-0034)
**ASN**: Properties Introduced table — "D0 | Displacement well-definedness: a < b and divergence(a, b) ≤ #a (DisplacementWellDefined, ASN-0034) | cited"
**Issue**: No proof in the ASN actually consumes D0. WF re-derives D0's content (b⊖a ∈ T, Pos, actionPoint = divergence, and the #a>#b mismatch) directly from TumblerSub rather than citing D0; the round-trip is D1, the uniqueness is D2. The table's "cited" annotation for D0 overstates the dependency surface a downstream consumer would read off it.
**What needs resolving**: n/a (OBSERVE).

### reach ∈ T discharged explicitly in S11 but silently assumed in S1/S3/S4/S8
**Class**: OBSERVE
**Foundation**: WF (WellFormedSpanFromEndpoints) — carrier preconditions s, r ∈ T; T12 (SpanWellDefinedness) postcondition (a) s ⊕ ℓ ∈ T
**ASN**: S11's proof opens with a full paragraph establishing reach(α), reach(β) ∈ T via TumblerAdd's carrier postcondition before applying WF to ρ = (reach(β), reach(α) ⊖ reach(β)). By contrast S1 ("γ = (s', r' ⊖ s')" with r' = min(reach(α), reach(β))), S3 ("γ = (s, r ⊖ s)" with r = max(reach(α), reach(β))), and S8's emit step invoke WF on reach-valued endpoints without noting reach ∈ T.
**Issue**: WF's carrier precondition r ∈ T is genuinely required, and r' / r there are computed sums (reaches), not primitive starts. The fact holds — each span is well-formed, so its reach = s ⊕ ℓ ∈ T by T12(a)/TA0 — so there is no soundness gap; but the rigor is inconsistent across the cone. Either the one-line fact belongs in S1/S3/S4/S8 too, or S11's elaborate establishment is heavier than its siblings warrant.
**What needs resolving**: n/a (OBSERVE) — flagging the inconsistency for uniform treatment.

### Defensive type-coherence prose in S2's formal contract
**Class**: OBSERVE
**Foundation**: T12 (SpanWellDefinedness), Span (Span) — actionPoint(ℓ) ≤ #s precondition
**ASN**: S2 formal contract Preconditions: "The last is a comparison of natural numbers (actionPoint(ℓ) ∈ ℕ), not the type-incoherent comparison of the tumbler s ⊕ ℓ against #s." and the body's parallel "This second condition is a comparison of natural numbers … not of the end offset s ⊕ ℓ, which is a tumbler."
**Issue**: This is defensive prose guarding against a type confusion the claim never commits — reviser drift around the precondition rather than a statement of what the precondition says. It explains why a misreading would be wrong instead of advancing the proof.
**What needs resolving**: n/a (OBSERVE).

### "T0(b) not invoked" disclaimers in S7
**Class**: OBSERVE
**Foundation**: T0 (CarrierSetDefinition) comprehension; T0(b) (UnboundedLength)
**ASN**: S7 proof: "(The membership of each extension is what is load-bearing here; the existential UnboundedLength claim T0(b) … is not what we invoke.)" and the Axiom slot's repetition: "The separate UnboundedLength claim T0(b), being purely existential about length, is not invoked here."
**Issue**: Twice the text explains what is *not* used. This is meta-prose explaining a prior finding's resolution (the T0-comprehension-vs-T0(b) distinction) rather than the argument itself; the negative disclaimer is now noise the reader must step past.
**What needs resolving**: n/a (OBSERVE).

### Precondition-necessity essay in S6 body and contract
**Class**: OBSERVE
**Foundation**: TumblerAdd result-length identity #(a ⊕ w) = #w
**ASN**: S6 body: "Drop a precondition — say Pos(ℓ) — and s ⊕ ℓ need not be defined, so the length identity has nothing to stand on." and the contract Preconditions: "They are not implied by level-uniformity: a level-uniform pair with Pos(ℓ) failing has reach(σ) undefined …"
**Issue**: The prose argues *why* the preconditions are needed (counterfactual of dropping Pos(ℓ)) rather than stating the definition. This is the "new prose around an axiom explains why the axiom is needed rather than what it says" pattern.
**What needs resolving**: n/a (OBSERVE).

### Use-site inventory in S11's TumblerAdd dependency slot
**Class**: OBSERVE
**Foundation**: TumblerAdd (ASN-0034)
**ASN**: S11 Depends → TumblerAdd: a paragraph-length inventory — "this membership is consumed twice. It is needed already in the boundary characterization … and again in the ρ-construction …" plus "The proof names both identities in their own right — rather than only through S6's packaged length consequence …"
**Issue**: The dependency slot carries a multi-clause consumption ledger rather than naming the imported postconditions. Use-site inventories in the structural Depends slot degrade scannability.
**What needs resolving**: n/a (OBSERVE).

VERDICT: OBSERVE