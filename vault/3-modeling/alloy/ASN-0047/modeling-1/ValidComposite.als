-- ValidComposite: a composite transition Sigma -> Sigma' satisfies
-- (1) each elementary step meets its precondition at the intermediate state
-- (2) coupling constraints J0, J1, J1' hold between initial and final states
--
-- Modeled as a two-step composite: s0 -> s1 -> s2, with s1 existentially
-- quantified. Checks: permanence (P0, P1, P2), P4 preservation.

sig Addr {}
sig Doc {}
sig VPos {}

sig State {
  content: set Addr,
  entities: set Doc,
  arr: Doc -> VPos -> lone Addr,
  prov: Addr -> set Doc
}

-- Only entity documents carry arrangements
pred WF[s: State] {
  all d: Doc | some s.arr[d] implies d in s.entities
}

-- S3: referential integrity — arrangement references allocated content
pred S3[s: State] {
  all d: s.entities | ranM[s, d] in s.content
}

fun ranM[s: State, d: Doc]: set Addr { VPos.(s.arr[d]) }
fun domM[s: State, d: Doc]: set VPos { (s.arr[d]).Addr }

-- ====== Elementary transitions ======

-- K.alpha: content allocation
pred KAlpha[s, s2: State, a: Addr] {
  a not in s.content
  s2.content = s.content + a
  s2.entities = s.entities
  all d: Doc | s2.arr[d] = s.arr[d]
  s2.prov = s.prov
}

-- K.delta: entity creation
pred KDelta[s, s2: State, d: Doc] {
  d not in s.entities
  s2.entities = s.entities + d
  no s2.arr[d]
  s2.content = s.content
  all d2: Doc - d | s2.arr[d2] = s.arr[d2]
  s2.prov = s.prov
}

-- K.mu+: arrangement extension
pred KMuPlus[s, s2: State, d: Doc] {
  d in s.entities
  domM[s, d] in domM[s2, d]
  some domM[s2, d] - domM[s, d]
  all v: domM[s, d] | s2.arr[d][v] = s.arr[d][v]
  all v: domM[s2, d] - domM[s, d] | s2.arr[d][v] in s.content
  s2.entities = s.entities
  s2.content = s.content
  all d2: Doc - d | s2.arr[d2] = s.arr[d2]
  s2.prov = s.prov
}

-- K.mu-: arrangement contraction
pred KMuMinus[s, s2: State, d: Doc] {
  d in s.entities
  domM[s2, d] in domM[s, d]
  some domM[s, d] - domM[s2, d]
  all v: domM[s2, d] | s2.arr[d][v] = s.arr[d][v]
  s2.entities = s.entities
  s2.content = s.content
  all d2: Doc - d | s2.arr[d2] = s.arr[d2]
  s2.prov = s.prov
}

-- K.rho: provenance recording
pred KRho[s, s2: State, a: Addr, d: Doc] {
  a in s.content
  d in s.entities
  s2.prov = s.prov + (a -> d)
  s2.content = s.content
  s2.entities = s.entities
  all d2: Doc | s2.arr[d2] = s.arr[d2]
}

-- One elementary step (disjunction of all transition kinds)
pred Step[s, s2: State] {
  (some a: Addr | KAlpha[s, s2, a])
  or (some d: Doc | KDelta[s, s2, d])
  or (some d: Doc | KMuPlus[s, s2, d])
  or (some d: Doc | KMuMinus[s, s2, d])
  or (some a: Addr, d: Doc | KRho[s, s2, a, d])
}

-- ====== Coupling constraints (between initial and final) ======

-- J0: every freshly allocated I-address appears in some arrangement
pred J0[s, s2: State] {
  all a: s2.content - s.content |
    some d: s2.entities, v: VPos | s2.arr[d][v] = a
}

-- J1: fresh arrangement entries have provenance recorded
pred J1[s, s2: State] {
  all d: s2.entities, a: ranM[s2, d] - ranM[s, d] |
    (a -> d) in s2.prov
}

-- J1': fresh provenance requires fresh arrangement entry
pred J1Prime[s, s2: State] {
  all a: Addr, d: s2.entities |
    ((a -> d) in (s2.prov - s.prov))
      implies a in (ranM[s2, d] - ranM[s, d])
}

-- ====== ValidComposite ======

-- Two-step composite with coupling constraints between endpoints
pred ValidComposite[s0, s2: State] {
  WF[s0]
  S3[s0]
  some s1: State - s0 - s2 {
    Step[s0, s1]
    Step[s1, s2]
  }
  J0[s0, s2]
  J1[s0, s2]
  J1Prime[s0, s2]
}

-- ====== Derived properties ======

-- P4: Contains(Sigma) in R — every current containment in provenance
pred P4[s: State] {
  all d: s.entities, a: ranM[s, d] | (a -> d) in s.prov
}

-- ====== Assertions ======

-- P0: content permanence follows from frame conditions
assert CompositeImpliesP0 {
  all disj s0, s2: State |
    ValidComposite[s0, s2] implies s0.content in s2.content
}

-- P1: entity permanence follows from frame conditions
assert CompositeImpliesP1 {
  all disj s0, s2: State |
    ValidComposite[s0, s2] implies s0.entities in s2.entities
}

-- P2: provenance permanence follows from frame conditions
assert CompositeImpliesP2 {
  all disj s0, s2: State |
    ValidComposite[s0, s2] implies s0.prov in s2.prov
}

-- P4 preservation: J1 ensures fresh containments have provenance;
-- P2 preserves pre-existing provenance
assert CompositePreservesP4 {
  all disj s0, s2: State |
    (ValidComposite[s0, s2] and P4[s0]) implies P4[s2]
}

-- Non-vacuity: valid composite with non-trivial state
run FindValidComposite {
  some disj s0, s2: State |
    ValidComposite[s0, s2]
    and some s2.entities
    and some s2.content
} for 4 but exactly 3 State

check CompositeImpliesP0 for 5 but exactly 3 State
check CompositeImpliesP1 for 5 but exactly 3 State
check CompositeImpliesP2 for 5 but exactly 3 State
check CompositePreservesP4 for 5 but exactly 3 State
