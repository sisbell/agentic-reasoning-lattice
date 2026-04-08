-- GlobalUniqueness: No two distinct allocation events produce the same address.
--
-- Encodes the proof's axiom structure and checks that global uniqueness
-- follows from T3, T4, T9, T10, T10a/TA5 within bounded scope.
-- The proof partitions all pairs of distinct allocation events into four
-- exhaustive cases based on the relationship between their allocators.

sig Address {}

sig Allocator {
  parent: lone Allocator,
  outputLen: Int,
  level: Int
}

sig Event {
  source: one Allocator,
  result: one Address
}

-- Allocators form an acyclic tree (hierarchy)
fact AllocatorTree {
  no a: Allocator | a in a.^parent
}

-- Output lengths are positive (tumblers have at least one component)
fact PositiveOutputLen {
  all a: Allocator | a.outputLen >= 1
}

-- Levels are non-negative
fact NonNegativeLevel {
  all a: Allocator | a.level >= 0
}

-- T9 (Forward allocation): Within a single allocator's sequential stream,
-- distinct allocation events produce distinct addresses. The strict ordering
-- a < b from allocated_before(a,b) and irreflexivity of < give a != b.
fact T9_ForwardAllocation {
  all disj e1, e2: Event |
    e1.source = e2.source implies e1.result != e2.result
}

-- T10 (Partition independence): Allocators whose prefixes do not nest
-- (neither is an ancestor of the other in the hierarchy) produce disjoint
-- address sets. The proof locates a component k where the prefixes diverge
-- and transfers this to the output addresses via T3.
fact T10_PartitionIndependence {
  all disj e1, e2: Event |
    let a1 = e1.source, a2 = e2.source |
      (a1 != a2 and a1 not in a2.^parent and a2 not in a1.^parent)
        implies e1.result != e2.result
}

-- TA5(d) + T10a (Child extension under allocator discipline): Each child-
-- spawning step uses inc(t, k') with k' >= 1, extending the tumbler by at
-- least one component. Combined with T10a (siblings use inc(.,0) which
-- preserves length by TA5(c)), child allocator outputs are uniformly
-- strictly longer than parent allocator outputs.
fact TA5d_ChildExtension {
  all c: Allocator | some c.parent implies c.outputLen > c.parent.outputLen
}

-- T3 (Canonical representation -- length separation): Tumblers of different
-- lengths are distinct (equal tumblers require equal lengths). If two
-- allocators have different output lengths, their addresses cannot collide.
fact T3_LengthSeparation {
  all disj e1, e2: Event |
    e1.source.outputLen != e2.source.outputLen implies e1.result != e2.result
}

-- T4 (Hierarchical parsing -- level separation): The zero count zeros(t)
-- uniquely determines the hierarchical level. Allocators at different levels
-- produce addresses with different zero counts, hence distinct addresses.
-- (Case 3 of the proof; logically subsumed by TA5d+T3 for nesting allocators,
-- but included to faithfully mirror the proof's case structure.)
fact T4_LevelSeparation {
  all disj e1, e2: Event |
    e1.source.level != e2.source.level implies e1.result != e2.result
}

-- GlobalUniqueness assertion.
-- Case 1 (same allocator):          T9
-- Case 2 (non-nesting prefixes):    T10
-- Case 3 (nesting, different level): T4
-- Case 4 (nesting, same level):     TA5d + T3
assert GlobalUniqueness {
  all disj e1, e2: Event | e1.result != e2.result
}

-- Non-vacuity: the axiom system admits instances with multiple allocation events
run NonVacuity {
  #Event >= 2
} for 5 but 4 Int

check GlobalUniqueness for 5 but 4 Int
