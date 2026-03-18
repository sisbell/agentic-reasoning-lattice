-- K.μ⁻ ArrangementContraction — POST ensures
-- dom(M'(d)) ⊂ dom(M(d)) ∧ (∀v ∈ dom(M'(d)) : M'(d)(v) = M(d)(v))
-- Precondition: d ∈ E_doc
-- Frame: C' = C; E' = E; R' = R; ∀d' ≠ d: M'(d') = M(d')

sig VPos {}
sig Addr {}
sig Doc {}

sig State {
  entities: set Doc,
  content: set Addr,
  prov: set Addr,
  arr: Doc -> VPos -> lone Addr
}

-- Well-formedness: arrangement references existing entities and content
pred wellFormed[s: State] {
  all d: Doc, v: VPos, a: Addr |
    d -> v -> a in s.arr implies (d in s.entities and a in s.content)
}

-- Mapped V-positions for document d in state s
fun dom[s: State, d: Doc]: set VPos {
  (s.arr[d]).Addr
}

-- K.μ⁻: contract arrangement of d by removing one or more mappings
pred ArrangementContraction[s, s2: State, d: Doc] {
  -- pre: d is an existing document entity
  d in s.entities

  -- post: domain strictly shrinks
  dom[s2, d] in dom[s, d]
  some dom[s, d] - dom[s2, d]

  -- post: all surviving mappings preserved
  all v: dom[s2, d] | s2.arr[d][v] = s.arr[d][v]

  -- frame: entities unchanged
  s2.entities = s.entities

  -- frame: content unchanged
  s2.content = s.content

  -- frame: provenance unchanged
  s2.prov = s.prov

  -- frame: other documents unchanged
  all d2: Doc - d | s2.arr[d2] = s.arr[d2]
}

-- Preservation: surviving mappings are unchanged
assert ContractionPreservesMappings {
  all s, s2: State, d: Doc |
    (wellFormed[s] and ArrangementContraction[s, s2, d]) implies
      (all v: VPos | v in dom[s2, d] implies s2.arr[d][v] = s.arr[d][v])
}

-- Shrinkage: domain strictly decreases
assert ContractionStrictlyShrinks {
  all s, s2: State, d: Doc |
    ArrangementContraction[s, s2, d] implies
      #dom[s2, d] < #dom[s, d]
}

-- No new mappings: nothing in post-domain that was not in pre-domain
assert ContractionNoNewMappings {
  all s, s2: State, d: Doc |
    ArrangementContraction[s, s2, d] implies
      no (dom[s2, d] - dom[s, d])
}

-- Well-formedness preservation
assert ContractionPreservesWF {
  all s, s2: State, d: Doc |
    (wellFormed[s] and ArrangementContraction[s, s2, d]) implies
      wellFormed[s2]
}

-- Frame: entities unchanged
assert FrameEntities {
  all s, s2: State, d: Doc |
    ArrangementContraction[s, s2, d] implies s2.entities = s.entities
}

-- Frame: other documents unchanged
assert FrameOtherDocs {
  all s, s2: State, d: Doc |
    ArrangementContraction[s, s2, d] implies
      (all d2: Doc - d | s2.arr[d2] = s.arr[d2])
}

-- Non-vacuity: contraction is satisfiable with pre-existing mappings
run FindContraction {
  some s, s2: State, d: Doc |
    wellFormed[s] and #dom[s, d] > 1 and ArrangementContraction[s, s2, d]
} for 4 but exactly 2 State, 5 Int

check ContractionPreservesMappings for 5 but exactly 2 State, 5 Int
check ContractionStrictlyShrinks for 5 but exactly 2 State, 5 Int
check ContractionNoNewMappings for 5 but exactly 2 State, 5 Int
check ContractionPreservesWF for 5 but exactly 2 State, 5 Int
check FrameEntities for 5 but exactly 2 State, 5 Int
check FrameOtherDocs for 5 but exactly 2 State, 5 Int
