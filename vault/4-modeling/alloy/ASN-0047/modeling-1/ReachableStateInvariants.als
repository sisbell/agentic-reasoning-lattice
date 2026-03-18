-- ReachableStateInvariants -- LEMMA
-- Every state reachable from Sigma_0 by valid composite transitions satisfies
-- P4 (Contains in R), P6, P7, P7a, P8, S2 (structural), S3, S8a/depth/fin.
--
-- Base case: initial state satisfies all invariants vacuously.
-- Inductive step: a two-step composite satisfying J0/J1/J1' at endpoints,
-- with AllInv at s0, produces AllInv at s2.

-- Entity hierarchy (Node <- Acct <- Doc)
sig Node {}
sig Acct { parentNode: one Node }
sig Doc  { parentAcct: one Acct }

-- Content addresses; origin maps each element address to its owning document
sig Addr { origin: one Doc }

-- V-positions; WFVPos is the well-formed subset (abstracts S8a + S8-depth)
sig VPos {}
sig WFVPos in VPos {}

-- System state
sig State {
  E_node: set Node,
  E_acct: set Acct,
  E_doc:  set Doc,
  C:      set Addr,
  arr:    Doc -> VPos -> lone Addr,   -- M: arrangement (S2 = lone multiplicity)
  prov:   Addr -> set Doc             -- R: provenance
}

-- Derived helpers
fun ranM[s: State, d: Doc]: set Addr { VPos.(s.arr[d]) }
fun domM[s: State, d: Doc]: set VPos { (s.arr[d]).Addr }

-- ====== State invariants ======

-- WF: arrangements only for allocated documents
pred WF[s: State] {
  all d: Doc | some s.arr[d] implies d in s.E_doc
}

-- P4: current containment within provenance
pred P4[s: State] {
  all d: s.E_doc, a: ranM[s, d] | (a -> d) in s.prov
}

-- P6: content origin is an allocated document
pred P6[s: State] {
  all a: s.C | a.origin in s.E_doc
}

-- P7: provenance pairs reference allocated content
pred P7[s: State] {
  all a: Addr, d: Doc | (a -> d) in s.prov implies a in s.C
}

-- P7a: every content address has at least one provenance entry
pred P7a[s: State] {
  all a: s.C | some d: Doc | (a -> d) in s.prov
}

-- P8: entity hierarchy closed (non-root entities have allocated parents)
pred P8[s: State] {
  all a: s.E_acct | a.parentNode in s.E_node
  all d: s.E_doc  | d.parentAcct in s.E_acct
}

-- S3: arrangement references only allocated content
pred S3[s: State] {
  all d: Doc | ranM[s, d] in s.C
}

-- S8: V-positions in arrangements are well-formed (abstracts S8a + S8-depth)
pred S8[s: State] {
  all d: Doc | domM[s, d] in WFVPos
}

-- All invariants (S2 is structural via lone; S8-fin is trivial in bounded scope)
pred AllInv[s: State] {
  WF[s]
  P4[s] and P6[s] and P7[s] and P7a[s] and P8[s]
  S3[s] and S8[s]
}

-- ====== Initial state ======

pred IsInitialState[s: State] {
  one s.E_node          -- single bootstrap node
  no s.E_acct
  no s.E_doc
  no s.C
  no s.prov
  all d: Doc | no s.arr[d]
}

-- ====== Elementary transitions ======

-- K.alpha: allocate content at address a (origin must be an allocated document)
pred KAlpha[s, s2: State, a: Addr] {
  a not in s.C
  a.origin in s.E_doc
  s2.C     = s.C + a
  s2.E_node = s.E_node
  s2.E_acct = s.E_acct
  s2.E_doc  = s.E_doc
  all d: Doc | s2.arr[d] = s.arr[d]
  s2.prov  = s.prov
}

-- K.delta for node (no parent required)
pred KDeltaNode[s, s2: State, n: Node] {
  n not in s.E_node
  s2.E_node = s.E_node + n
  s2.E_acct = s.E_acct
  s2.E_doc  = s.E_doc
  s2.C     = s.C
  all d: Doc | s2.arr[d] = s.arr[d]
  s2.prov  = s.prov
}

-- K.delta for account (parent node must be allocated)
pred KDeltaAcct[s, s2: State, a: Acct] {
  a not in s.E_acct
  a.parentNode in s.E_node
  s2.E_acct = s.E_acct + a
  s2.E_node = s.E_node
  s2.E_doc  = s.E_doc
  s2.C     = s.C
  all d: Doc | s2.arr[d] = s.arr[d]
  s2.prov  = s.prov
}

-- K.delta for document (parent account must be allocated; new doc starts empty)
pred KDeltaDoc[s, s2: State, d: Doc] {
  d not in s.E_doc
  d.parentAcct in s.E_acct
  s2.E_doc  = s.E_doc + d
  no s2.arr[d]
  s2.E_node = s.E_node
  s2.E_acct = s.E_acct
  s2.C     = s.C
  all d2: Doc - d | s2.arr[d2] = s.arr[d2]
  s2.prov  = s.prov
}

-- K.mu+: extend arrangement for document d
pred KMuPlus[s, s2: State, d: Doc] {
  d in s.E_doc
  domM[s, d] in domM[s2, d]
  some domM[s2, d] - domM[s, d]
  all v: domM[s, d]            | s2.arr[d][v] = s.arr[d][v]
  all v: domM[s2, d] - domM[s, d] | s2.arr[d][v] in s.C
  domM[s2, d] - domM[s, d] in WFVPos
  s2.E_node = s.E_node
  s2.E_acct = s.E_acct
  s2.E_doc  = s.E_doc
  s2.C     = s.C
  all d2: Doc - d | s2.arr[d2] = s.arr[d2]
  s2.prov  = s.prov
}

-- K.mu-: contract arrangement for document d
pred KMuMinus[s, s2: State, d: Doc] {
  d in s.E_doc
  domM[s2, d] in domM[s, d]
  some domM[s, d] - domM[s2, d]
  all v: domM[s2, d] | s2.arr[d][v] = s.arr[d][v]
  s2.E_node = s.E_node
  s2.E_acct = s.E_acct
  s2.E_doc  = s.E_doc
  s2.C     = s.C
  all d2: Doc - d | s2.arr[d2] = s.arr[d2]
  s2.prov  = s.prov
}

-- K.rho: record provenance for content a in document d
pred KRho[s, s2: State, a: Addr, d: Doc] {
  a in s.C
  d in s.E_doc
  s2.prov  = s.prov + (a -> d)
  s2.E_node = s.E_node
  s2.E_acct = s.E_acct
  s2.E_doc  = s.E_doc
  s2.C     = s.C
  all d2: Doc | s2.arr[d2] = s.arr[d2]
}

-- Any elementary step
pred Step[s, s2: State] {
  (some a: Addr       | KAlpha[s, s2, a])
  or (some n: Node    | KDeltaNode[s, s2, n])
  or (some a: Acct    | KDeltaAcct[s, s2, a])
  or (some d: Doc     | KDeltaDoc[s, s2, d])
  or (some d: Doc     | KMuPlus[s, s2, d])
  or (some d: Doc     | KMuMinus[s, s2, d])
  or (some a: Addr, d: Doc | KRho[s, s2, a, d])
}

-- ====== Composite-level coupling constraints ======

-- J0: every freshly allocated content address appears in some arrangement
pred J0[s, s2: State] {
  all a: s2.C - s.C |
    some d: s2.E_doc, v: VPos | s2.arr[d][v] = a
}

-- J1: fresh arrangement entries have provenance recorded
pred J1[s, s2: State] {
  all d: s2.E_doc, a: ranM[s2, d] - ranM[s, d] |
    (a -> d) in s2.prov
}

-- J1': fresh provenance implies a fresh arrangement entry
pred J1Prime[s, s2: State] {
  all a: Addr, d: s2.E_doc |
    ((a -> d) in (s2.prov - s.prov))
      implies a in (ranM[s2, d] - ranM[s, d])
}

-- Valid composite: two elementary steps with coupling constraints at endpoints
pred ValidComposite[s0, s2: State] {
  some s1: State - s0 - s2 {
    Step[s0, s1]
    Step[s1, s2]
  }
  J0[s0, s2]
  J1[s0, s2]
  J1Prime[s0, s2]
}

-- ====== Assertions ======

-- Base case: initial state satisfies all invariants (vacuously)
assert BaseCase {
  all s: State | IsInitialState[s] implies AllInv[s]
}

-- Inductive step: valid composite preserves all invariants
assert InductiveStep {
  all disj s0, s2: State |
    (AllInv[s0] and ValidComposite[s0, s2]) implies AllInv[s2]
}

-- Non-vacuity: find a state satisfying AllInv with non-trivial content
run NonVacuity {
  some s: State |
    AllInv[s]
    and some s.E_doc
    and some s.C
    and some a: Addr, d: Doc | (a -> d) in s.prov
} for 4 but exactly 1 State

check BaseCase    for 4 but exactly 1 State
check InductiveStep for 4 but exactly 3 State
