-- J1' — ProvenanceRequiresExtension
-- New provenance (a,d) in R'\R requires a in ran(M'(d))\ran(M(d)).
-- When (a,d) already in R from a prior insertion-deletion cycle,
-- re-introducing a into d's arrangement requires no new K.rho,
-- because J1's requirement is satisfied by existing membership (P2).

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

-- J1': new provenance entries only for newly arranged addresses
pred j1p[s, s2: State] {
  all a: IAddr, d: Doc |
    (a -> d in s2.prov - s.prov) implies
    (a in ranM[s2, d] - ranM[s, d])
}

-- Monotonic transition between well-formed states
pred step[s, s2: State] {
  wf[s] and wf[s2]
  s.docs in s2.docs
  s.prov in s2.prov         -- P2
}

----------------------------------------------------------------------
-- Check 1: J1' is non-trivial — not implied by step + J1 alone
----------------------------------------------------------------------
assert J1PrimeNotImplied {
  all s, s2: State | (step[s, s2] and j1[s, s2]) implies j1p[s, s2]
}

check J1PrimeNotImplied for 4 but exactly 2 State

----------------------------------------------------------------------
-- Check 2: Fork satisfies J1'
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

  -- provenance: exactly prior + new entries for dst
  s2.prov = s.prov +
    {a: IAddr, d: Doc | d = dst and a in ranM[s2, dst]}
}

assert ForkSatisfiesJ1Prime {
  all s, s2: State, src, dst: Doc |
    (wf[s] and fork[s, s2, src, dst]) implies j1p[s, s2]
}

check ForkSatisfiesJ1Prime for 5 but exactly 2 State

----------------------------------------------------------------------
-- Check 3: Extend-and-record satisfies J1'
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

assert ExtendAndRecordSatisfiesJ1Prime {
  all s, s2: State, d: Doc, v: VAddr, a: IAddr |
    (wf[s] and extendAndRecord[s, s2, d, v, a]) implies j1p[s, s2]
}

check ExtendAndRecordSatisfiesJ1Prime for 5 but exactly 2 State

----------------------------------------------------------------------
-- Check 4: Re-insertion with existing provenance needs no new K.rho
----------------------------------------------------------------------
pred reinsert[s, s2: State, d: Doc, v: VAddr, a: IAddr] {
  d in s.docs
  a not in ranM[s, d]           -- a was removed from d
  no s.arr[d][v]
  a -> d in s.prov              -- provenance already exists

  -- re-add to arrangement
  s2.arr = s.arr + (d -> v -> a)
  s2.docs = s.docs

  -- no new provenance needed — P2 preserves existing record
  s2.prov = s.prov
}

-- Re-insertion satisfies J1 (existing provenance covers J1's requirement)
assert ReinsertSatisfiesJ1 {
  all s, s2: State, d: Doc, v: VAddr, a: IAddr |
    (wf[s] and reinsert[s, s2, d, v, a]) implies j1[s, s2]
}

-- Re-insertion satisfies J1' (no new provenance, so J1' trivially holds)
assert ReinsertSatisfiesJ1Prime {
  all s, s2: State, d: Doc, v: VAddr, a: IAddr |
    (wf[s] and reinsert[s, s2, d, v, a]) implies j1p[s, s2]
}

check ReinsertSatisfiesJ1 for 5 but exactly 2 State
check ReinsertSatisfiesJ1Prime for 5 but exactly 2 State

----------------------------------------------------------------------
-- Non-vacuity
----------------------------------------------------------------------
run FindFork {
  some s, s2: State, src, dst: Doc |
    wf[s] and fork[s, s2, src, dst] and
    some ranM[s2, dst]
} for 5 but exactly 2 State

run FindReinsert {
  some s, s2: State, d: Doc, v: VAddr, a: IAddr |
    wf[s] and reinsert[s, s2, d, v, a]
} for 4 but exactly 2 State
