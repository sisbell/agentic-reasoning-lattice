-- A1-ReachabilityNonMonotone
-- Property: reachability through a document is not monotone across
-- state transitions. A DELETE on document d can remove the V-space
-- mappings that made address a reachable through d.

sig Addr {}
sig Doc {}
sig Pos {}

sig State {
  -- V-space: each document maps positions to addresses
  V: Doc -> Pos -> lone Addr,
  -- set of live documents
  D: set Doc
}

-- reachable(a, d): document d references address a at some position
pred reachable[s: State, a: Addr, d: Doc] {
  some p: Pos | s.V[d][p] = a
}

-- Delete operation: removes a document and its V-space mappings
pred Delete[s, sPost: State, d: Doc] {
  -- precondition: d is a live document
  d in s.D

  -- postcondition: d is removed from live set
  sPost.D = s.D - d

  -- V-space for d is cleared
  no sPost.V[d]

  -- frame: other documents unchanged
  all d2: Doc - d | sPost.V[d2] = s.V[d2]
}

-- Assert the POSITIVE form (monotonicity) and expect a counterexample
assert ReachabilityMonotone {
  all s, sPost: State, a: Addr, d: Doc |
    (reachable[s, a, d] and Delete[s, sPost, d])
      implies reachable[sPost, a, d]
}

check ReachabilityMonotone for 5 but exactly 2 State

-- Non-vacuity: a reachable address exists and Delete can fire
run FindReachableAndDelete {
  some s, sPost: State, a: Addr, d: Doc |
    reachable[s, a, d] and Delete[s, sPost, d]
} for 4 but exactly 2 State
