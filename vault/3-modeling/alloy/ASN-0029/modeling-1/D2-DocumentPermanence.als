-- D2-DocumentPermanence.als
-- Property D2: documents, once created, are never removed.
--
-- D2: ∀ transitions Σ → Σ' : d ∈ Σ.D ⟹ d ∈ Σ'.D

sig Doc {}

sig State {
  D: set Doc
}

----------------------------------------------------------------------
-- Operations
----------------------------------------------------------------------

-- Create a fresh document
pred CreateDoc[s, s2: State, d: Doc] {
  d not in s.D
  s2.D = s.D + d
}

-- No-op
pred Skip[s, s2: State] {
  s2.D = s.D
}

-- System step: disjunction of all operations
pred Step[s, s2: State] {
  (some d: Doc | CreateDoc[s, s2, d])
  or
  Skip[s, s2]
}

----------------------------------------------------------------------
-- D2 assertion and checks
----------------------------------------------------------------------

assert DocumentPermanence {
  all s, s2: State |
    Step[s, s2] implies s.D in s2.D
}

check DocumentPermanence for 5 but exactly 2 State

-- Non-vacuity: a step that creates a document when docs already exist
run NonVacuity {
  some s, s2: State, d: Doc |
    CreateDoc[s, s2, d] and some s.D
} for 5 but exactly 2 State
