-- J3-ReorderingIsolation.als
-- K.μ~ (reorder) as a distinguished composite preserves C, E, R,
-- and therefore containment.

sig Doc {}
sig Addr {}
sig Pos {}

sig State {
  entities: set Doc,
  mapping: Doc -> Pos -> lone Addr,
  content: set Addr,
  provenance: set Addr
}

-- Well-formedness: mapping only references known entities
pred wellFormed[s: State] {
  all d: Doc | some d.(s.mapping) implies d in s.entities
}

-- Range of M(d): the set of addresses appearing in d's mapping
fun ranM[s: State, d: Doc]: set Addr {
  Pos.(d.(s.mapping))
}

-- Containment: {(d, a) : a in ran(M(d))}
fun containment[s: State]: Doc -> Addr {
  { d: Doc, a: Addr | a in ranM[s, d] }
}

-- K.μ~ : reorder entries within a single document's mapping
-- Preserves ran(M(d)); does not touch E, C, R, or other documents
pred Reorder[s, sPost: State, d: Doc] {
  -- precondition
  d in s.entities
  some d.(s.mapping)

  -- E unchanged
  sPost.entities = s.entities

  -- C unchanged
  sPost.content = s.content

  -- R unchanged
  sPost.provenance = s.provenance

  -- range of M(d) preserved (same addresses, possibly different positions)
  ranM[sPost, d] = ranM[s, d]

  -- all other documents' mappings unchanged
  all d2: Doc - d |
    d2.(sPost.mapping) = d2.(s.mapping)
}

-- J3: Reordering preserves E, C, R, and containment
assert ReorderingIsolation {
  all s, sPost: State, d: Doc |
    (wellFormed[s] and Reorder[s, sPost, d]) implies {
      sPost.entities = s.entities
      sPost.content = s.content
      sPost.provenance = s.provenance
      containment[sPost] = containment[s]
    }
}

-- Non-vacuity: find a reorder that actually changes positions
run FindReorder {
  some s, sPost: State, d: Doc |
    wellFormed[s] and Reorder[s, sPost, d] and
    d.(s.mapping) != d.(sPost.mapping)
} for 4 but exactly 2 State, 3 Doc, 3 Addr, 3 Pos

check ReorderingIsolation for 5 but exactly 2 State
