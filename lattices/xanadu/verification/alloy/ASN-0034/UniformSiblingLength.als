-- ASN-0034 T10a.1: UniformSiblingLength
-- All siblings produced by a single allocator have the same length
-- as its base address.
--
-- inc(t, 0) = t ⊕ δ(1, #t) adds a unit displacement at depth 0.
-- TA5(c) guarantees #inc(t, 0) = #t (length preservation).
-- The property follows by induction over the sibling chain.

sig Tumbler {
  len: Int,
  inc0: lone Tumbler   -- inc(·, 0): next sibling in the chain
}

one sig Allocator {
  base: Tumbler         -- t₀: base address
}

-- TA5(c): inc(t, 0) preserves length
fact IncPreservesLength {
  all t: Tumbler | some t.inc0 implies t.inc0.len = t.len
}

-- The sibling chain is acyclic
fact AcyclicChain {
  no t: Tumbler | t in t.^inc0
}

-- Every tumbler is reachable from the base via inc0
fact AllReachable {
  Tumbler = Allocator.base.*inc0
}

-- T10a.1: (A n >= 0 : #t_n = #t_0)
assert UniformSiblingLength {
  all t: Tumbler | t.len = Allocator.base.len
}

-- Non-vacuity: allocator with at least two siblings beyond the base
run NonVacuity {
  some disj t1, t2: Tumbler - Allocator.base |
    t1 in Allocator.base.^inc0 and t2 in Allocator.base.^inc0
} for 5 but exactly 1 Allocator, 4 Int

check UniformSiblingLength for 5 but exactly 1 Allocator, 4 Int
check UniformSiblingLength for 8 but exactly 1 Allocator, 4 Int
