-- K.μ⁺ ArrangementExtension — POST ensures
-- dom(M'(d)) ⊃ dom(M(d)) ∧ (∀v ∈ dom(M(d)) : M'(d)(v) = M(d)(v))
-- Precondition: d ∈ E_doc; new addresses in dom(C)
-- Frame: C' = C; E' = E; ∀d' ≠ d: M'(d') = M(d'); R' = R

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

-- K.μ⁺: extend arrangement of d with one or more new mappings
pred ArrangementExtension[s, s2: State, d: Doc] {
  -- pre: d is an existing document entity
  d in s.entities

  -- post: domain strictly extends
  dom[s, d] in dom[s2, d]
  some dom[s2, d] - dom[s, d]

  -- post: all existing mappings preserved
  all v: dom[s, d] | s2.arr[d][v] = s.arr[d][v]

  -- post: new mappings target allocated content
  all v: dom[s2, d] - dom[s, d] | s2.arr[d][v] in s.content

  -- frame: entities unchanged
  s2.entities = s.entities

  -- frame: content unchanged
  s2.content = s.content

  -- frame: provenance unchanged
  s2.prov = s.prov

  -- frame: other documents unchanged
  all d2: Doc - d | s2.arr[d2] = s.arr[d2]
}

-- Preservation: existing mappings survive unchanged
assert ExtensionPreservesMappings {
  all s, s2: State, d: Doc |
    (wellFormed[s] and ArrangementExtension[s, s2, d]) implies
      (all v: VPos | some s.arr[d][v] implies s2.arr[d][v] = s.arr[d][v])
}

-- Growth: domain strictly increases
assert ExtensionStrictlyGrows {
  all s, s2: State, d: Doc |
    ArrangementExtension[s, s2, d] implies
      #dom[s2, d] > #dom[s, d]
}

-- Well-formedness preservation
assert ExtensionPreservesWF {
  all s, s2: State, d: Doc |
    (wellFormed[s] and ArrangementExtension[s, s2, d]) implies
      wellFormed[s2]
}

-- Frame: entities unchanged
assert FrameEntities {
  all s, s2: State, d: Doc |
    ArrangementExtension[s, s2, d] implies s2.entities = s.entities
}

-- Frame: other documents unchanged
assert FrameOtherDocs {
  all s, s2: State, d: Doc |
    ArrangementExtension[s, s2, d] implies
      (all d2: Doc - d | s2.arr[d2] = s.arr[d2])
}

-- Non-vacuity: ArrangementExtension is satisfiable with pre-existing mappings
run FindExtension {
  some s, s2: State, d: Doc |
    wellFormed[s] and some dom[s, d] and ArrangementExtension[s, s2, d]
} for 4 but exactly 2 State, 5 Int

check ExtensionPreservesMappings for 5 but exactly 2 State, 5 Int
check ExtensionStrictlyGrows for 5 but exactly 2 State, 5 Int
check ExtensionPreservesWF for 5 but exactly 2 State, 5 Int
check FrameEntities for 5 but exactly 2 State, 5 Int
check FrameOtherDocs for 5 but exactly 2 State, 5 Int
