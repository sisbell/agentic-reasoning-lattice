-- T9 ForwardAllocation (ASN-0034)
-- Within a single allocator's sequential stream, addresses are
-- strictly monotonically increasing.

open util/ordering[Step]

sig Tumbler {}

-- T1: strict total order on tumblers
one sig TumblerOrd {
  tlt: Tumbler -> Tumbler
} {
  -- irreflexive
  no t: Tumbler | t -> t in tlt
  -- transitive
  all a, b, c: Tumbler |
    (a -> b in tlt and b -> c in tlt) implies a -> c in tlt
  -- total
  all disj a, b: Tumbler | a -> b in tlt or b -> a in tlt
}

-- Allocation steps in temporal order
sig Step {}

-- Single allocator's sibling stream
one sig Alloc {
  addr: Step -> one Tumbler
} {
  -- TA5(a): inc(v, 0) > v — each step yields a strictly greater address
  all s: Step - last |
    addr[s] -> addr[s.next] in TumblerOrd.tlt
}

-- T9: ForwardAllocation
-- Precondition: same_allocator(a, b) ∧ allocated_before(a, b)
--   (both from same Alloc, s1 before s2 in step order)
-- Postcondition: a < b under tumbler order
assert ForwardAllocation {
  all s1, s2: Step |
    s1 -> s2 in ^next implies
      Alloc.addr[s1] -> Alloc.addr[s2] in TumblerOrd.tlt
}

-- Non-vacuity: find an instance with 3 allocation steps
run NonVacuity {
  #Step >= 3
} for 5 but exactly 1 Alloc, exactly 3 Step

check ForwardAllocation for 5 but exactly 1 Alloc, exactly 4 Step
