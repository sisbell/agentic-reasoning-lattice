# ASN-0047 Proof Index

*Source: ASN-0047-state-transitions.md (revised 2026-03-17) — Index generated: 2026-03-17*

| ASN Label | Proof Label | Type | Construct | Notes |
|-----------|------------|------|-----------|-------|
| Σ.E | EntitySetValid | INV | predicate(State) | entities: ValidAddress ∧ ¬IsElement; level partition |
| Σ.R | ProvenanceWellTyped | INV | predicate(State) | R ⊆ T_elem × E_doc |
| Σ₀ | IsInitialState | INV | predicate(State) | defines initial state; base case for induction |
| P0 | ContentPermanence | INV | predicate(State, State) | transition; restates S0 (ASN-0036) |
| P1 | EntityPermanence | INV | predicate(State, State) | transition; specialises T8 (ASN-0034) |
| P8 | EntityHierarchy | LEMMA | lemma | derived from EntityCreatable, P1 |
| P2 | ProvenancePermanence | INV | predicate(State, State) | transition |
| P3 | ArrangementMutability | LEMMA | lemma | derived from P0, P1, P2 |
| K.α | ContentAllocation | POST | ensures | C' = C ∪ {a ↦ v}, a fresh |
| K.α (pre) | ContentAllocatable | PRE | requires | IsElement(a) ∧ origin(a) ∈ E_doc |
| K.δ | EntityCreation | POST | ensures | E' = E ∪ {e}, e fresh |
| K.δ (pre) | EntityCreatable | PRE | requires | parent(e) ∈ E when ¬IsNode(e) |
| K.μ⁺ | ArrangementExtension | POST | ensures | dom grows, existing values preserved |
| K.μ⁻ | ArrangementContraction | POST | ensures | dom shrinks, survivors preserved |
| K.μ~ | ArrangementReordering | POST | ensures | composite: K.μ⁻ + K.μ⁺; bijection on V-pos |
| K.ρ | ProvenanceRecording | POST | ensures | R' = R ∪ {(a, d)} |
| K.ρ (pre) | ProvenanceRecordable | PRE | requires | a ∈ dom(C) ∧ d ∈ E_doc |
| Arrangement invariants lemma | ArrangementInvariantsPreserved | LEMMA | lemma | S2/S3/S8a/S8-depth/S8-fin by elementary preservation |
| Valid composite | ValidComposite | INV | predicate(State, State) | transition; elementary PREs + J0/J1/J1' |
| Permanence lemma | PermanenceFromFrames | LEMMA | lemma | P0/P1/P2 from elementary frames |
| Reachable-state invariants | ReachableStateInvariants | LEMMA | lemma | theorem; induction on transitions |
| J0 | AllocationRequiresPlacement | INV | predicate(State, State) | transition; axiom |
| J1 | ExtensionRecordsProvenance | INV | predicate(State, State) | transition; necessitated by wp from P4 |
| J1' | ProvenanceRequiresExtension | INV | predicate(State, State) | transition |
| P4a | HistoricalFidelity | LEMMA | lemma | derived from J1', P2 |
| J2 | ContractionIsolation | LEMMA | lemma | derived from K.μ⁻ frame |
| J3 | ReorderingIsolation | LEMMA | lemma | derived from K.μ~ decomposition |
| J4 | ForkComposite | POST | ensures | compound: K.δ + K.μ⁺ + K.ρ |
| P4 | ProvenanceBounds | LEMMA | lemma | derived from J1, P2; Contains(Σ) ⊆ R |
| P5 | DestructionConfinement | LEMMA | lemma | derived from elementary frames; generalises S9 |
| P6 | ExistentialCoherence | LEMMA | lemma | derived from ContentAllocatable, P0, P1 |
| P7 | ProvenanceGrounding | LEMMA | lemma | derived from ProvenanceRecordable, P0, P2 |
| P7a | ProvenanceCoverage | LEMMA | lemma | derived from J0, J1, P0, P2 |
