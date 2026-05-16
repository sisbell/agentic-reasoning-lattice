-- T8-AllocationPermanence.als
-- ASN-0034 Property T8: Allocation Permanence
-- "The set of allocated addresses is monotonically non-decreasing."

sig Tumbler {}

sig State {
  allocated: set Tumbler
}

-- Case 1 & 2: Read-only operations (T1, T2, T4) and pure arithmetic
-- (plus, minus, inc) preserve the allocated set exactly.
-- Frame: allocated(s') = allocated(s)
pred PreservingOp[s, sPost: State] {
  sPost.allocated = s.allocated
}

-- Case 3: Allocation (T10a) adds a fresh address to the allocated set.
pred AllocateOp[s, sPost: State, a: Tumbler] {
  -- precondition: address is not yet allocated
  a not in s.allocated
  -- postcondition: allocated set grows by exactly one element
  sPost.allocated = s.allocated + a
}

-- Axiom: the system defines no operation that removes an element from
-- the allocated set. This is a design constraint, not a derived property.
-- Encoded: every valid transition is either preserving or allocating.
pred ValidTransition[s, sPost: State] {
  PreservingOp[s, sPost]
  or
  (some a: Tumbler | AllocateOp[s, sPost, a])
}

-- Invariant: for every state transition s -> s', allocated(s) <= allocated(s')
assert AllocationPermanence {
  all s, sPost: State |
    ValidTransition[s, sPost] implies s.allocated in sPost.allocated
}

-- Frame: read-only and pure arithmetic preserve the allocated set exactly
assert FramePreservation {
  all s, sPost: State |
    PreservingOp[s, sPost] implies sPost.allocated = s.allocated
}

-- Non-vacuity: a valid allocation transition exists
run FindAllocate {
  some s, sPost: State, a: Tumbler |
    AllocateOp[s, sPost, a]
} for 4 but exactly 2 State

check AllocationPermanence for 5 but exactly 2 State
check FramePreservation for 5 but exactly 2 State
