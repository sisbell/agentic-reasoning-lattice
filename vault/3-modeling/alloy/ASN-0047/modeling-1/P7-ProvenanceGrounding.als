-- P7 — ProvenanceGrounding (LEMMA)
-- (A (a, d) ∈ R :: a ∈ dom(C))
-- Every provenance record references an address with content.

sig Address {}
sig Doc in Address {}
sig Value {}

sig State {
  -- C: content map (address -> value)
  C: Address -> lone Value,
  -- R: provenance relation (address, document)
  R: Address -> set Doc
}

-- The property: all provenance addresses are in dom(C)
pred ProvenanceGrounded[s: State] {
  all a: Address, d: Doc |
    (a -> d) in s.R implies some s.C[a]
}

-- P0: content permanence (dom(C) preserved)
pred ContentPermanence[s, s2: State] {
  all a: Address | some s.C[a] implies s2.C[a] = s.C[a]
}

-- P2: provenance permanence (R preserved)
pred ProvenanceMonotone[s, s2: State] {
  s.R in s2.R
}

-- K.ρ: record provenance with precondition a ∈ dom(C)
pred RecordProvenance[s, s2: State, a: Address, d: Doc] {
  -- precondition: a has content
  some s.C[a]
  -- precondition: pair not already recorded
  (a -> d) not in s.R
  -- postcondition: provenance pair is added
  s2.R = s.R + (a -> d)
  -- frame: content unchanged
  s2.C = s.C
}

-- Non-provenance step: may add content, never removes; R unchanged
pred NonProvenanceStep[s, s2: State] {
  ContentPermanence[s, s2]
  s2.R = s.R
}

-- A valid elementary transition
pred ValidStep[s, s2: State] {
  (some a: Address, d: Doc | RecordProvenance[s, s2, a, d])
  or NonProvenanceStep[s, s2]
}

-- Initial state
pred InitialState[s: State] {
  no s.R
}

-- Base case: empty provenance trivially grounded
assert ProvenanceGroundingBase {
  all s: State |
    InitialState[s] implies ProvenanceGrounded[s]
}

-- Inductive step: if grounded and valid step, grounded in post-state
assert ProvenanceGroundingInductive {
  all s, s2: State |
    (ProvenanceGrounded[s] and ValidStep[s, s2])
      implies ProvenanceGrounded[s2]
}

check ProvenanceGroundingBase for 5 but exactly 1 State
check ProvenanceGroundingInductive for 5 but exactly 2 State

-- Non-vacuity: a step that records provenance where content already exists
run NonVacuity {
  some s, s2: State, a: Address, d: Doc |
    ProvenanceGrounded[s]
    and some s.C
    and some s.R
    and RecordProvenance[s, s2, a, d]
    and ProvenanceGrounded[s2]
} for 4 but exactly 2 State
