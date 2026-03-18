-- J0 — AllocationRequiresPlacement
-- Every freshly allocated I-address appears in some arrangement in the post-state.

sig IAddr {}
sig VAddr {}
sig Doc {}

sig State {
  alloc: set IAddr,                    -- dom(C): allocated I-addresses
  docs: set Doc,                       -- E_doc: existing documents
  arr: Doc -> VAddr -> lone IAddr      -- M: arrangement per document
}

-- Well-formedness: arrangements only for existing docs, arranged addrs allocated
pred wf[s: State] {
  all d: Doc | (some v: VAddr | some s.arr[d][v]) implies d in s.docs
  all d: s.docs, v: VAddr |
    some s.arr[d][v] implies s.arr[d][v] in s.alloc
}

-- All I-addresses appearing in any arrangement of state s
fun placed[s: State]: set IAddr {
  VAddr.(s.docs.(s.arr))
}

-- J0: freshly allocated I-addresses must be placed in some arrangement
pred j0[s, s2: State] {
  (s2.alloc - s.alloc) in placed[s2]
}

-- Monotonic transition between well-formed states
pred step[s, s2: State] {
  wf[s] and wf[s2]
  s.alloc in s2.alloc
  s.docs in s2.docs
}

----------------------------------------------------------------------
-- Check 1: J0 is non-trivial — not implied by monotonic transition
----------------------------------------------------------------------
assert J0NotImplied {
  all s, s2: State | step[s, s2] implies j0[s, s2]
}

check J0NotImplied for 4 but exactly 2 State

----------------------------------------------------------------------
-- Check 2: Fork satisfies J0 (no new allocations, so trivially true)
----------------------------------------------------------------------
pred fork[s, s2: State, src, dst: Doc] {
  -- precondition
  src in s.docs
  some v: VAddr | some s.arr[src][v]
  dst not in s.docs

  -- postcondition: new doc added, no new allocations
  s2.docs = s.docs + dst
  s2.alloc = s.alloc

  -- dst arrangement drawn from src's arranged addresses
  some v: VAddr | some s2.arr[dst][v]
  all v: VAddr | some s2.arr[dst][v] implies
    s2.arr[dst][v] in VAddr.(s.arr[src])

  -- frame: existing docs unchanged
  all d: s.docs, v: VAddr | s2.arr[d][v] = s.arr[d][v]
}

assert ForkSatisfiesJ0 {
  all s, s2: State, src, dst: Doc |
    (wf[s] and fork[s, s2, src, dst]) implies j0[s, s2]
}

check ForkSatisfiesJ0 for 5 but exactly 2 State

----------------------------------------------------------------------
-- Check 3: Allocate-and-place satisfies J0
----------------------------------------------------------------------
pred allocAndPlace[s, s2: State, a: IAddr, d: Doc, v: VAddr] {
  a not in s.alloc
  d in s.docs
  no s.arr[d][v]

  s2.alloc = s.alloc + a
  s2.docs = s.docs
  s2.arr = s.arr + (d -> v -> a)
}

assert AllocPlaceSatisfiesJ0 {
  all s, s2: State, a: IAddr, d: Doc, v: VAddr |
    (wf[s] and allocAndPlace[s, s2, a, d, v]) implies j0[s, s2]
}

check AllocPlaceSatisfiesJ0 for 5 but exactly 2 State

----------------------------------------------------------------------
-- Non-vacuity: a transition where J0 holds with actual new allocation
----------------------------------------------------------------------
run NonVacuity {
  some s, s2: State |
    step[s, s2] and j0[s, s2] and some (s2.alloc - s.alloc)
} for 5 but exactly 2 State
