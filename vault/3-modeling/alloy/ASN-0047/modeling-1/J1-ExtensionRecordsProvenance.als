-- J1 — ExtensionRecordsProvenance
-- Every I-address freshly placed in a document's arrangement has provenance recorded.
-- (A Sigma -> Sigma', d in E'_doc, a : a in ran(M'(d)) \ ran(M(d)) : (a, d) in R')

sig IAddr {}
sig VAddr {}
sig Doc {}

sig State {
  docs: set Doc,                       -- E_doc: existing documents
  arr: Doc -> VAddr -> lone IAddr,     -- M: arrangement per document
  prov: IAddr -> set Doc               -- R: provenance relation
}

-- Well-formedness: arrangements only for existing docs
pred wf[s: State] {
  all d: Doc | (some v: VAddr | some s.arr[d][v]) implies d in s.docs
}

-- ran(M(d)): I-addresses appearing in document d's arrangement
fun ranM[s: State, d: Doc]: set IAddr {
  VAddr.(s.arr[d])
}

-- J1: freshly arranged I-addresses must have provenance recorded
pred j1[s, s2: State] {
  all d: s2.docs, a: ranM[s2, d] - ranM[s, d] |
    (a -> d) in s2.prov
}

-- Monotonic transition between well-formed states
pred step[s, s2: State] {
  wf[s] and wf[s2]
  s.docs in s2.docs
  s.prov in s2.prov
}

----------------------------------------------------------------------
-- Check 1: J1 is non-trivial — not implied by monotonic transition
----------------------------------------------------------------------
assert J1NotImplied {
  all s, s2: State | step[s, s2] implies j1[s, s2]
}

check J1NotImplied for 4 but exactly 2 State

----------------------------------------------------------------------
-- Check 2: Fork satisfies J1
----------------------------------------------------------------------
pred fork[s, s2: State, src, dst: Doc] {
  -- precondition
  src in s.docs
  some v: VAddr | some s.arr[src][v]
  dst not in s.docs

  -- K.delta: allocate new doc
  s2.docs = s.docs + dst

  -- K.mu+: dst arrangement drawn from src's arranged addresses
  some v: VAddr | some s2.arr[dst][v]
  all v: VAddr | some s2.arr[dst][v] implies
    s2.arr[dst][v] in ranM[s, src]

  -- K.rho: provenance recorded for every address in dst
  all a: ranM[s2, dst] | (a -> dst) in s2.prov

  -- frame: existing docs' arrangements unchanged
  all d: s.docs, v: VAddr | s2.arr[d][v] = s.arr[d][v]

  -- provenance preserved
  s.prov in s2.prov
}

assert ForkSatisfiesJ1 {
  all s, s2: State, src, dst: Doc |
    (wf[s] and fork[s, s2, src, dst]) implies j1[s, s2]
}

check ForkSatisfiesJ1 for 5 but exactly 2 State

----------------------------------------------------------------------
-- Check 3: Extend-and-record satisfies J1
----------------------------------------------------------------------
pred extendAndRecord[s, s2: State, d: Doc, v: VAddr, a: IAddr] {
  d in s.docs
  a not in ranM[s, d]
  no s.arr[d][v]

  -- extend arrangement with new address
  s2.arr = s.arr + (d -> v -> a)
  s2.docs = s.docs

  -- record provenance for the new address
  s2.prov = s.prov + (a -> d)
}

assert ExtendAndRecordSatisfiesJ1 {
  all s, s2: State, d: Doc, v: VAddr, a: IAddr |
    (wf[s] and extendAndRecord[s, s2, d, v, a]) implies j1[s, s2]
}

check ExtendAndRecordSatisfiesJ1 for 5 but exactly 2 State

----------------------------------------------------------------------
-- Non-vacuity: a transition where J1 holds with actual new placement
----------------------------------------------------------------------
run NonVacuity {
  some s, s2: State |
    step[s, s2] and j1[s, s2] and
    some d: s2.docs | some (ranM[s2, d] - ranM[s, d])
} for 5 but exactly 2 State
