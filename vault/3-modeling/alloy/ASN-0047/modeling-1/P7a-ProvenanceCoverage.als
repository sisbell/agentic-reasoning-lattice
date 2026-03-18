-- P7a — ProvenanceCoverage (LEMMA)
-- (A a ∈ dom(C) :: (E d :: (a, d) ∈ R))
-- Every allocated content address has provenance in some document.
-- Proved by induction: base vacuous (dom(C₀) = ∅), inductive step
-- uses P2 (provenance permanence), J0 (fresh content placed), S3
-- (fresh addresses not in prior maps), J1 (new map entries get provenance).

sig IAddr {}
sig VAddr {}
sig Doc {}

sig State {
  alloc: set IAddr,                    -- dom(C): allocated I-addresses
  docs: set Doc,                       -- E_doc: existing documents
  arr: Doc -> VAddr -> lone IAddr,     -- M: arrangement per document
  prov: IAddr -> set Doc               -- R: provenance relation
}

-- Well-formedness: arrangements only for existing docs,
-- arranged addresses are allocated
pred wf[s: State] {
  all d: Doc | (some v: VAddr | some s.arr[d][v]) implies d in s.docs
  all d: s.docs, v: VAddr |
    some s.arr[d][v] implies s.arr[d][v] in s.alloc
}

-- ran(M(d)): I-addresses appearing in document d's arrangement
fun ranM[s: State, d: Doc]: set IAddr {
  VAddr.(s.arr[d])
}

-- All placed I-addresses across all documents
fun placed[s: State]: set IAddr {
  VAddr.(s.docs.(s.arr))
}

----------------------------------------------------------------------
-- P7a: every allocated I-address has provenance in some document
----------------------------------------------------------------------
pred provenanceCoverage[s: State] {
  all a: s.alloc | some a.(s.prov)
}

----------------------------------------------------------------------
-- Transition: captures the coupling constraints the proof relies on
----------------------------------------------------------------------
pred transition[s, s2: State] {
  wf[s] and wf[s2]

  -- Monotonicity
  s.alloc in s2.alloc
  s.docs in s2.docs

  -- P2: provenance permanence
  s.prov in s2.prov

  -- J0: freshly allocated addresses appear in some arrangement
  (s2.alloc - s.alloc) in placed[s2]

  -- S3: fresh addresses were not in any prior arrangement
  no a: s2.alloc - s.alloc, d: Doc | a in ranM[s, d]

  -- J1: freshly placed addresses get provenance
  all d: s2.docs, a: ranM[s2, d] - ranM[s, d] |
    (a -> d) in s2.prov
}

----------------------------------------------------------------------
-- Base case: empty allocation trivially covered
----------------------------------------------------------------------
pred initialState[s: State] {
  no s.alloc
  no s.prov
  all d: Doc, v: VAddr | no s.arr[d][v]
}

assert P7a_Base {
  all s: State |
    initialState[s] implies provenanceCoverage[s]
}

----------------------------------------------------------------------
-- Inductive step: coverage preserved across transitions
----------------------------------------------------------------------
assert P7a_Inductive {
  all s, s2: State |
    (provenanceCoverage[s] and transition[s, s2])
      implies provenanceCoverage[s2]
}

check P7a_Base for 5 but exactly 1 State
check P7a_Inductive for 5 but exactly 2 State

----------------------------------------------------------------------
-- Non-vacuity: a transition with fresh allocation that maintains coverage
----------------------------------------------------------------------
run NonVacuity {
  some s, s2: State |
    provenanceCoverage[s] and transition[s, s2]
    and some (s2.alloc - s.alloc)
    and some s.alloc
    and some s.prov
} for 5 but exactly 2 State
