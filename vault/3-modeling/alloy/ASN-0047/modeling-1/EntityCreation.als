-- K.δ EntityCreation — POST ensures
-- E' = E ∪ {e}, e ∉ E, ValidAddress(e), ¬IsElement(e)
-- When IsDocument(e): M'(e) = ∅
-- Frame: C' = C; ∀d': M'(d') = M(d'); R' = R

abstract sig Address {}
sig NodeAddr, AccountAddr, DocumentAddr extends Address {}

sig Datum {}

sig State {
  entities: set Address,
  membership: DocumentAddr -> set Address,
  content: set Datum,
  provenance: set Datum
}

-- Well-formedness: membership scoped to entity documents
pred WellFormed[s: State] {
  all d: DocumentAddr | some s.membership[d] implies d in s.entities
  all d: DocumentAddr | s.membership[d] in s.entities
}

-- EntityCreation: allocate a new entity address
pred EntityCreation[s, s2: State, e: Address] {
  -- pre: e is not yet allocated
  e not in s.entities

  -- post: E' = E ∪ {e}
  s2.entities = s.entities + e

  -- post: new document gets empty membership
  e in DocumentAddr implies no s2.membership[e]

  -- frame: content unchanged
  s2.content = s.content

  -- frame: all memberships unchanged
  all d: DocumentAddr | s2.membership[d] = s.membership[d]

  -- frame: provenance unchanged
  s2.provenance = s.provenance
}

-- EntityCreation preserves well-formedness
assert CreationPreservesWF {
  all s, s2: State, e: Address |
    (WellFormed[s] and EntityCreation[s, s2, e]) implies WellFormed[s2]
}

-- Only e is added to the entity set
assert NoExtraEntities {
  all s, s2: State, e: Address |
    EntityCreation[s, s2, e] implies (s2.entities - s.entities) = e
}

-- New document has empty membership
assert NewDocEmptyMembership {
  all s, s2: State, e: Address |
    (WellFormed[s] and EntityCreation[s, s2, e] and e in DocumentAddr)
      implies no s2.membership[e]
}

-- Frame: content is preserved
assert FrameContent {
  all s, s2: State, e: Address |
    EntityCreation[s, s2, e] implies s2.content = s.content
}

-- Non-vacuity: EntityCreation is satisfiable
run CreateEntity {
  some s, s2: State, e: Address |
    WellFormed[s] and EntityCreation[s, s2, e]
} for 4 but exactly 2 State

check CreationPreservesWF for 5 but exactly 2 State
check NoExtraEntities for 5 but exactly 2 State
check NewDocEmptyMembership for 5 but exactly 2 State
check FrameContent for 5 but exactly 2 State
