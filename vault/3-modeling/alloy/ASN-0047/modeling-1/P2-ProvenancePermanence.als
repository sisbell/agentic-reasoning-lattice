-- P2-ProvenancePermanence.als
-- Property: provenance is permanent — once a provenance record exists,
-- it is never removed in any subsequent state.
-- (A Σ → Σ' :: R ⊆ R')

sig Address {}

sig State {
  R: Address -> Address
}

-- The provenance-permanence predicate (two-state invariant)
pred ProvenancePermanence[s, s2: State] {
  s.R in s2.R
}

-- Elementary transition: record new provenance (K.ρ)
pred RecordProvenance[s, s2: State, a1: Address, a2: Address] {
  -- precondition: pair not already recorded
  a1 -> a2 not in s.R
  -- postcondition: provenance pair is added
  s2.R = s.R + (a1 -> a2)
}

-- Elementary transition: non-provenance operation (entity creation,
-- content addition, mapping change, etc.)
pred NonProvenanceStep[s, s2: State] {
  s2.R = s.R
}

-- A valid elementary transition either records provenance or leaves R unchanged.
-- No transition kind removes provenance records.
pred ValidStep[s, s2: State] {
  (some a1, a2: Address | RecordProvenance[s, s2, a1, a2])
  or NonProvenanceStep[s, s2]
}

-- P2: every valid step preserves provenance permanence
assert P2_ProvenancePermanence {
  all s, s2: State |
    ValidStep[s, s2] implies ProvenancePermanence[s, s2]
}

-- Non-vacuity: find a RecordProvenance step where pre-state already has provenance
run NonVacuity {
  some s, s2: State, a1, a2: Address |
    some s.R and RecordProvenance[s, s2, a1, a2]
} for 4 but exactly 2 State

check P2_ProvenancePermanence for 5 but exactly 2 State
