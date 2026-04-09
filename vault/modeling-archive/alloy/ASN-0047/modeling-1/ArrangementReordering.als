-- K.μ~ ArrangementReordering — POST ensures
-- There exists a bijection π : dom(M(d)) → dom(M'(d)) such that
-- (∀v ∈ dom(M(d)) : M'(d)(π(v)) = M(d)(v))
-- Corollary: ran(M'(d)) = ran(M(d))
-- Precondition: d ∈ E_doc; M(d) non-empty
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

-- Addresses referenced by arrangement of d in state s
fun ran[s: State, d: Doc]: set Addr {
  VPos.(s.arr[d])
}

-- π is a bijection from 'from' onto 'to'
pred isBijection[pi: VPos -> VPos, from: set VPos, to: set VPos] {
  -- total on 'from', undefined elsewhere
  all v: from | one pi[v]
  all v: VPos - from | no pi[v]
  -- surjective onto 'to'
  from.pi = to
  -- injective
  all disj v1, v2: from | pi[v1] != pi[v2]
}

-- K.μ~: reorder arrangement of d via bijection on positions
pred ArrangementReordering[s, s2: State, d: Doc] {
  -- pre: d is an existing document with non-empty arrangement
  d in s.entities
  some s.arr[d]

  -- post: there exists a bijection π such that M'(d)(π(v)) = M(d)(v)
  some pi: VPos -> VPos {
    isBijection[pi, dom[s, d], dom[s2, d]]
    all v: dom[s, d] | s2.arr[d][pi[v]] = s.arr[d][v]
  }

  -- frame: entities unchanged
  s2.entities = s.entities

  -- frame: content unchanged
  s2.content = s.content

  -- frame: provenance unchanged
  s2.prov = s.prov

  -- frame: other documents unchanged
  all d2: Doc - d | s2.arr[d2] = s.arr[d2]
}

-- Corollary: reordering preserves the range (content addresses)
assert ReorderPreservesRange {
  all s, s2: State, d: Doc |
    ArrangementReordering[s, s2, d] implies ran[s2, d] = ran[s, d]
}

-- Domain size is preserved (bijection implies equinumerosity)
assert ReorderPreservesDomainSize {
  all s, s2: State, d: Doc |
    ArrangementReordering[s, s2, d] implies #dom[s2, d] = #dom[s, d]
}

-- Well-formedness preservation
assert ReorderPreservesWF {
  all s, s2: State, d: Doc |
    (wellFormed[s] and ArrangementReordering[s, s2, d]) implies
      wellFormed[s2]
}

-- Frame: entities unchanged
assert FrameEntities {
  all s, s2: State, d: Doc |
    ArrangementReordering[s, s2, d] implies s2.entities = s.entities
}

-- Frame: other documents unchanged
assert FrameOtherDocs {
  all s, s2: State, d: Doc |
    ArrangementReordering[s, s2, d] implies
      (all d2: Doc - d | s2.arr[d2] = s.arr[d2])
}

-- Non-vacuity: find a reordering that actually changes the arrangement
run FindReorder {
  some s, s2: State, d: Doc |
    wellFormed[s] and ArrangementReordering[s, s2, d]
      and s.arr[d] != s2.arr[d]
} for 4 but exactly 2 State, 5 Int

check ReorderPreservesRange for 5 but exactly 2 State, 5 Int
check ReorderPreservesDomainSize for 5 but exactly 2 State, 5 Int
check ReorderPreservesWF for 5 but exactly 2 State, 5 Int
check FrameEntities for 5 but exactly 2 State, 5 Int
check FrameOtherDocs for 5 but exactly 2 State, 5 Int
