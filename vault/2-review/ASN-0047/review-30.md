# Review of ASN-0047

Based on Alloy modeling-1

## SKIP

### Negative tests confirming precondition necessity

The following SAT results on `check` commands are from **intentional negative tests** — assertions that removing a precondition breaks well-formedness. SAT here is the *expected* outcome, confirming the preconditions are load-bearing:

- **NaiveAllocBreaksWF** (ContentAllocatable): Confirms K.α without `IsElement(a) ∧ origin(a) ∈ E_doc` can violate well-formedness. The positive check `AllocPreservesWF` is UNSAT — the precondition works.
- **NaiveRecordProvBreaksWF** (ProvenanceRecordable): Confirms K.ρ without `a ∈ dom(C) ∧ d ∈ E_doc` can violate well-formedness. The positive check `RecordProvPreservesWF` is UNSAT — the precondition works.

### Non-triviality checks

The following SAT results on `check` commands confirm that the coupling constraints are **meaningful** — they are not implied by monotonicity alone. SAT is the expected outcome (the constraint adds real information beyond what follows from well-formedness + monotonicity):

- **J0NotImplied**: J0 is a genuine constraint, not a consequence of monotonic transitions.
- **J1NotImplied**: J1 is a genuine constraint, not a consequence of monotonic transitions.
- **J1PrimeNotImplied**: J1' is a genuine constraint, not implied by step + J1 alone.

### Positive checks — all passed

Every assertion checking the actual ASN property is UNSAT (no counterexample within scope):

- K.α precondition preserves well-formedness (AllocPreservesWF)
- K.ρ precondition preserves well-formedness (RecordProvPreservesWF)
- Fork satisfies J0, J1, J1' (ForkSatisfiesJ0, ForkSatisfiesJ1, ForkSatisfiesJ1Prime)
- Allocate-and-place satisfies J0 (AllocPlaceSatisfiesJ0)
- Extend-and-record satisfies J1, J1' (ExtendAndRecordSatisfiesJ1, ExtendAndRecordSatisfiesJ1Prime)
- Re-insertion with existing provenance satisfies J1 and J1' (ReinsertSatisfiesJ1, ReinsertSatisfiesJ1Prime)

### Non-vacuity runs — all confirmed

All `run` commands return SAT, confirming the models are not vacuously satisfiable: FindAlloc, FindRecordProv, NonVacuity (J0), NonVacuity (J1), FindFork, FindReinsert.

### 28 properties passed bounded check

Σ.E, Σ.R, Σ₀, P0, P1, P8, P2, P3, K.α, K.δ (pre), K.δ, K.μ⁺, K.μ⁻, K.μ~, K.ρ, Arrangement invariants lemma, Valid composite, Permanence lemma, Reachable-state invariants, P4a, J2, J3, J4, P4, P5, P6, P7, P7a — all UNSAT within bounded scope.

VERDICT: CONVERGED
