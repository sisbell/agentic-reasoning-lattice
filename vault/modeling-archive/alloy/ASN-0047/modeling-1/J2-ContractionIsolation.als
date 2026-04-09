-- J2 — ContractionIsolation
-- K.μ⁻ as elementary transition: C' = C, E' = E, R' = R
-- Contains(Σ') ⊆ Contains(Σ)

sig Address {}
sig Document {}

sig State {
  entities: set Document,
  content: set Address,
  provenance: set Address,
  maps: Document -> set Address
}

-- Contains(Σ) = {(d, a) : d ∈ entities ∧ a ∈ maps[d]}
fun Contains[s: State]: Document -> Address {
  (s.entities) <: (s.maps)
}

-- K.μ⁻: remove one mapping entry from a document
pred ContractMapping[s, s2: State, d: Document, a: Address] {
  -- precondition: d is an entity document, a is in its mappings
  d in s.entities
  a in s.maps[d]

  -- effect: remove the single mapping entry
  s2.maps = s.maps - (d -> a)

  -- frame: C, E, R unchanged
  s2.entities = s.entities
  s2.content = s.content
  s2.provenance = s.provenance
}

-- Frame preservation: C, E, R unchanged by K.μ⁻
assert Frame {
  all s, s2: State, d: Document, a: Address |
    ContractMapping[s, s2, d, a] implies {
      s2.content = s.content
      s2.entities = s.entities
      s2.provenance = s.provenance
    }
}

-- Containment can only shrink under K.μ⁻
assert ContainmentShrinks {
  all s, s2: State, d: Document, a: Address |
    ContractMapping[s, s2, d, a] implies
      Contains[s2] in Contains[s]
}

-- Non-vacuity: find a contraction that actually changes containment
run NonVacuity {
  some s, s2: State, d: Document, a: Address |
    ContractMapping[s, s2, d, a] and
    Contains[s] != Contains[s2]
} for 4 but exactly 2 State

check Frame for 5 but exactly 2 State
check ContainmentShrinks for 5 but exactly 2 State
