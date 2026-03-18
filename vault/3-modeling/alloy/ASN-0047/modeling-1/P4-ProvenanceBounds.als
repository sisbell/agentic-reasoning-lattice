-- P4 — ProvenanceBounds (LEMMA)
-- Contains(Σ) ⊆ R
-- Every current containment pair is recorded in provenance.

sig Address {}
sig Doc in Address {}

sig State {
  -- M: each document maps to its currently contained addresses
  M: Doc -> set Address,
  -- R: provenance relation (address, document) pairs
  R: Address -> set Doc
}

-- Contains(s) = {(a, d) : d in Doc, a in ran(M(d))}
fun Contains[s: State]: Address -> Doc {
  ~(s.M)
}

-- P2: provenance is monotone (R ⊆ R')
pred ProvenanceMonotone[s, s2: State] {
  s.R in s2.R
}

-- J1: newly introduced containment must appear in R'
-- If a is in M'(d) but not in M(d), then (a, d) in R'
pred J1[s, s2: State] {
  all a: Address, d: Doc |
    (a in s2.M[d] and a not in s.M[d]) implies (a -> d) in s2.R
}

-- Valid transition: provenance monotone + J1
pred Transition[s, s2: State] {
  ProvenanceMonotone[s, s2]
  J1[s, s2]
}

-- Initial state: no documents have content
pred InitialState[s: State] {
  no s.M
  no s.R
}

-- Base case: empty state trivially satisfies Contains ⊆ R
assert ProvenanceBoundsBase {
  all s: State |
    InitialState[s] implies Contains[s] in s.R
}

-- Inductive step: if Contains(s) ⊆ R and transition is valid,
-- then Contains(s') ⊆ R'
assert ProvenanceBoundsInductive {
  all s, s2: State |
    (Contains[s] in s.R and Transition[s, s2])
      implies Contains[s2] in s2.R
}

check ProvenanceBoundsBase for 5 but exactly 1 State
check ProvenanceBoundsInductive for 5 but exactly 2 State

-- Non-vacuity: a transition where new containment is introduced
run NonVacuity {
  some s, s2: State |
    Contains[s] in s.R
    and Transition[s, s2]
    and some s2.M
    and some a: Address, d: Doc |
      a in s2.M[d] and a not in s.M[d]
} for 4 but exactly 2 State
