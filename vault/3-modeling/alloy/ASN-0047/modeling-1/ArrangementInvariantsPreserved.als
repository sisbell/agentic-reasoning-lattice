-- ArrangementInvariantsPreserved — LEMMA
-- Every valid composite transition preserves S2, S3, S8a, S8-depth, S8-fin.
-- Argument: each elementary transition preserves these per-state properties;
-- composition by transitivity gives the composite result.
--
-- S2 (functionality) is structural: arr uses lone multiplicity.
-- S8-fin (finiteness) is trivial in Alloy's bounded universe.
-- S3 (referential integrity) and S8a+S8-depth (V-position structure) are checked.

sig VPos {}
sig Addr {}
sig Doc {}

-- Abstract well-formed V-positions: represents S8a (components > 0) + S8-depth
sig WFVPos in VPos {}

sig State {
  entities: set Doc,
  content: set Addr,
  arr: Doc -> VPos -> lone Addr   -- lone encodes S2 (functionality)
}

-- Only entity-documents carry arrangements
pred wellFormed[s: State] {
  all d: Doc | some s.arr[d] implies d in s.entities
}

-- Mapped V-positions for document d
fun dom[s: State, d: Doc]: set VPos {
  (s.arr[d]).Addr
}

-- I-addresses referenced by arrangement of d
fun ran[s: State, d: Doc]: set Addr {
  VPos.(s.arr[d])
}

-- S3: referential integrity — ran(M(d)) ⊆ dom(C)
pred S3[s: State] {
  all d: Doc | ran[s, d] in s.content
}

-- S8: V-position well-formedness (abstracts S8a + S8-depth; S8-fin is trivial)
pred S8[s: State] {
  all d: Doc | dom[s, d] in WFVPos
}

-- Combined arrangement invariants
pred ArrInv[s: State] {
  wellFormed[s]
  S3[s]
  S8[s]
}

-- === Elementary transitions ===

-- K.α: content allocation — frame: arr unchanged
pred ContentAllocation[s, s2: State, a: Addr] {
  a not in s.content
  s2.content = s.content + a
  s2.entities = s.entities
  all d: Doc | s2.arr[d] = s.arr[d]
}

-- K.δ: entity creation — frame: arr unchanged for all docs
pred EntityCreation[s, s2: State, d: Doc] {
  d not in s.entities
  s2.entities = s.entities + d
  s2.content = s.content
  all d2: Doc | s2.arr[d2] = s.arr[d2]
}

-- K.μ⁺: arrangement extension — disjoint domain extension with preconditions
pred ArrExtension[s, s2: State, d: Doc] {
  d in s.entities
  -- domain strictly extends
  dom[s, d] in dom[s2, d]
  some dom[s2, d] - dom[s, d]
  -- existing mappings preserved
  all v: dom[s, d] | s2.arr[d][v] = s.arr[d][v]
  -- precondition: new addresses in content (establishes S3)
  all v: dom[s2, d] - dom[s, d] | s2.arr[d][v] in s.content
  -- precondition: new positions well-formed (establishes S8a + S8-depth)
  dom[s2, d] - dom[s, d] in WFVPos
  -- frame
  s2.entities = s.entities
  s2.content = s.content
  all d2: Doc - d | s2.arr[d2] = s.arr[d2]
}

-- K.μ⁻: arrangement contraction — restriction of M(d)
pred ArrContraction[s, s2: State, d: Doc] {
  d in s.entities
  -- domain strictly shrinks
  dom[s2, d] in dom[s, d]
  some dom[s, d] - dom[s2, d]
  -- surviving mappings preserved
  all v: dom[s2, d] | s2.arr[d][v] = s.arr[d][v]
  -- frame
  s2.entities = s.entities
  s2.content = s.content
  all d2: Doc - d | s2.arr[d2] = s.arr[d2]
}

-- K.ρ: provenance recording — frame: arr unchanged
pred ProvenanceRecording[s, s2: State] {
  s2.entities = s.entities
  s2.content = s.content
  all d: Doc | s2.arr[d] = s.arr[d]
}

-- === Assertions: each elementary transition preserves ArrInv ===

assert AlphaPreservesArrInv {
  all s, s2: State, a: Addr |
    (ArrInv[s] and ContentAllocation[s, s2, a]) implies ArrInv[s2]
}

assert DeltaPreservesArrInv {
  all s, s2: State, d: Doc |
    (ArrInv[s] and EntityCreation[s, s2, d]) implies ArrInv[s2]
}

assert ExtensionPreservesArrInv {
  all s, s2: State, d: Doc |
    (ArrInv[s] and ArrExtension[s, s2, d]) implies ArrInv[s2]
}

assert ContractionPreservesArrInv {
  all s, s2: State, d: Doc |
    (ArrInv[s] and ArrContraction[s, s2, d]) implies ArrInv[s2]
}

assert RhoPreservesArrInv {
  all s, s2: State |
    (ArrInv[s] and ProvenanceRecording[s, s2]) implies ArrInv[s2]
}

-- Non-vacuity: ArrInv state with non-trivial arrangement admits extension
run FindExtension {
  some s, s2: State, d: Doc |
    ArrInv[s] and some dom[s, d] and ArrExtension[s, s2, d]
} for 4 but exactly 2 State

check AlphaPreservesArrInv for 5 but exactly 2 State
check DeltaPreservesArrInv for 5 but exactly 2 State
check ExtensionPreservesArrInv for 5 but exactly 2 State
check ContractionPreservesArrInv for 5 but exactly 2 State
check RhoPreservesArrInv for 5 but exactly 2 State
