-- PartitionMonotonicity.als
-- Within a prefix-delimited partition the set of allocated addresses is
-- totally ordered by T1, consistent with allocation order for any single
-- allocator.  For sibling sub-partitions with non-nesting prefixes p1 < p2,
-- every address extending p1 precedes every address extending p2 under T1.
--
-- Depends on: T5, T9, T10, T10a, TA5, PrefixOrderingExtension

open util/ordering[Time]

-- ── Time ─────────────────────────────────────────────────────────────────────

sig Time {}

-- ── Tumblers ─────────────────────────────────────────────────────────────────
-- Two-component model: len in {1,2}.  Prefix tumblers have len=1; full
-- addresses have len=2.  Components are non-negative naturals.

sig Tumbler {
  len: Int,
  c1:  Int,
  c2:  Int
} {
  (len = 1 or len = 2)
  c1 >= 0
  c2 >= 0
  len = 1 implies c2 = 0
}

-- Extensional equality (two atoms may encode the same tumbler)
pred tEq[a, b: Tumbler] {
  a.len = b.len and a.c1 = b.c1 and a.c2 = b.c2
}

-- T1 strict ordering: lexicographic with prefix rule.
-- For two-component tumblers the cases are:
--   (i)  first components differ: a.c1 < b.c1
--   (ii) first components equal, a shorter (a is proper prefix of b): a.len < b.len
--   (iii) both length-2, first components equal, second differs: a.c2 < b.c2
pred tLt[a, b: Tumbler] {
  a.c1 < b.c1
  or (a.c1 = b.c1 and a.len < b.len)
  or (a.c1 = b.c1 and a.len = 2 and b.len = 2 and a.c2 < b.c2)
}

-- Prefix relation: p is a prefix of t
pred isPrefix[p, t: Tumbler] {
  p.len =< t.len
  p.c1 = t.c1
  (p.len = 2 implies (t.len = 2 and p.c2 = t.c2))
}

-- Non-nesting: neither p1 is a prefix of p2 nor vice versa
pred nonNesting[p1, p2: Tumbler] {
  not isPrefix[p1, p2]
  not isPrefix[p2, p1]
}

-- ── Allocators ───────────────────────────────────────────────────────────────

sig Allocator {
  ownedPrefix: one Tumbler,
  history:     Time -> lone Tumbler
}

-- All owned prefixes are length-1 tumblers
fact PrefixesAreShort {
  all a: Allocator | a.ownedPrefix.len = 1
}

-- Allocated addresses must extend the owner's prefix and be strictly longer
fact AllocationDiscipline {
  all a: Allocator, t: Time |
    some a.history[t] implies {
      isPrefix[a.ownedPrefix, a.history[t]]
      a.history[t].len > a.ownedPrefix.len
    }
}

-- T10: distinct allocators own non-nesting (disjoint) prefix partitions
fact DisjointPartitions {
  all disj a1, a2: Allocator | nonNesting[a1.ownedPrefix, a2.ownedPrefix]
}

-- T9 / TA5: forward allocation — earlier time yields smaller T1 address
fact ForwardAllocation {
  all a: Allocator, t1, t2: Time |
    (some a.history[t1] and some a.history[t2] and lt[t1, t2])
      implies tLt[a.history[t1], a.history[t2]]
}

-- T10a: no two distinct allocators ever produce the same address
fact DisjointAllocations {
  all disj a1, a2: Allocator, t1, t2: Time |
    (some a1.history[t1] and some a2.history[t2])
      implies not tEq[a1.history[t1], a2.history[t2]]
}

-- ── Assertions ───────────────────────────────────────────────────────────────

-- PM1: Addresses within a single partition are totally ordered by T1.
-- Any two extensionally distinct allocations by the same allocator are
-- comparable under T1.  (Follows from T9 + Time being a total order.)
assert IntraPartitionTotalOrder {
  all a: Allocator, t1, t2: Time |
    (some a.history[t1] and some a.history[t2]
     and not tEq[a.history[t1], a.history[t2]])
      implies (tLt[a.history[t1], a.history[t2]] or tLt[a.history[t2], a.history[t1]])
}

-- PM2: Allocation order is consistent with T1 for any single allocator.
-- If allocation at t1 precedes allocation at t2 in time, the T1 address at
-- t1 is strictly less than the T1 address at t2.  (Direct restatement of T9.)
assert AllocationOrderConsistency {
  all a: Allocator, t1, t2: Time |
    (some a.history[t1] and some a.history[t2] and lt[t1, t2])
      implies tLt[a.history[t1], a.history[t2]]
}

-- PM3: Cross-partition monotonicity.
-- If p1 < p2 under T1 (allocators are non-nesting by DisjointPartitions),
-- then every address from partition p1 precedes every address from partition p2.
-- (PrefixOrderingExtension applied to the allocator structure.)
assert CrossPartitionMonotonicity {
  all a1, a2: Allocator, t1, t2: Time |
    (some a1.history[t1] and some a2.history[t2]
     and tLt[a1.ownedPrefix, a2.ownedPrefix])
      implies tLt[a1.history[t1], a2.history[t2]]
}

-- ── Checks and non-vacuity ───────────────────────────────────────────────────

check IntraPartitionTotalOrder  for 5 but exactly 2 Allocator, exactly 3 Time, 5 Int
check AllocationOrderConsistency for 5 but exactly 2 Allocator, exactly 3 Time, 5 Int
check CrossPartitionMonotonicity for 5 but exactly 2 Allocator, exactly 3 Time, 5 Int

-- Non-vacuity: two allocators each make at least one allocation at the same
-- time step, with their prefixes in T1 order.
run NonVacuity {
  some disj a1, a2: Allocator, t: Time |
    some a1.history[t] and some a2.history[t]
    and tLt[a1.ownedPrefix, a2.ownedPrefix]
} for 5 but exactly 2 Allocator, exactly 3 Time, 5 Int
