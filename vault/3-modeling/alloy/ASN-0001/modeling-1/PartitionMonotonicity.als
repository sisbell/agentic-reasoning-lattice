-- PartitionMonotonicity — Alloy bounded check
--
-- LEMMA: Within any prefix-delimited partition of the address space, the set of
-- allocated addresses is totally ordered by T1, and this order is consistent
-- with the allocation order of any single allocator within that partition.
--
-- Dependencies: T1 (total order on tumblers), T5 (allocs within prefix cone),
-- T9 (per-allocator monotonicity), T10 (prefix disjointness),
-- T10a (same-length sibling prefixes => non-nesting cones => T1-separated cones).

sig Address {}

-- T1: abstract strict total order on addresses (represents tumbler ordering)
one sig Ord {
  lt: Address -> Address
}

-- T1 is irreflexive, transitive, and connected (strict total order)
fact T1_StrictTotalOrder {
  let lt = Ord.lt | {
    no iden & lt
    lt.lt in lt
    all a, b: Address | not (a = b) implies (a -> b in lt or b -> a in lt)
  }
}

-- Allocator: owns a prefix-delimited address region with a monotone allocation sequence
sig Allocator {
  cone: set Address,
  allocs: seq Address
}

-- T10: prefix cones are pairwise disjoint
fact T10 {
  all disj a1, a2: Allocator | no a1.cone & a2.cone
}

-- T10a: prefix cones are T1-separated — no two distinct cones interleave under T1.
-- Follows from same-length sibling prefixes (ASN T10a), which ensures non-nesting and
-- satisfies the Prefix Ordering Extension lemma premise.
fact T10a {
  let lt = Ord.lt |
  all disj a1, a2: Allocator |
    (all x: a1.cone, y: a2.cone | x -> y in lt)
    or
    (all x: a2.cone, y: a1.cone | x -> y in lt)
}

-- T5: all allocated addresses lie within the allocator's prefix cone
fact T5 {
  all a: Allocator | a.allocs.elems in a.cone
}

-- T9: per-allocator monotonicity — each allocator's sequence is strictly T1-increasing
fact T9 {
  let lt = Ord.lt |
  all a: Allocator, i, j: a.allocs.inds |
    i < j implies a.allocs[i] -> a.allocs[j] in lt
}

-- INTRA-ALLOCATOR CONSISTENCY:
-- Within any single allocator's partition, T1 order agrees with allocation order.
-- Forward direction is T9 directly. Backward direction is the contrapositive of T9
-- combined with T1 antisymmetry: if j <= i, then allocs[j] <=_T1 allocs[i], so
-- allocs[i] is not strictly T1-less than allocs[j].
assert PM_IntraConsistency {
  let lt = Ord.lt |
  all a: Allocator, i, j: a.allocs.inds |
    i < j iff a.allocs[i] -> a.allocs[j] in lt
}

-- INTER-ALLOCATOR CONSISTENCY:
-- If cone1 lies entirely T1-below cone2 (guaranteed by T10a), then every allocation
-- in cone1 is T1-less than every allocation in cone2.
-- Proof: allocs[i1] in cone1 (T5), allocs[i2] in cone2 (T5),
-- all of cone1 < all of cone2 (T10a hypothesis) => allocs[i1] < allocs[i2].
assert PM_InterConsistency {
  let lt = Ord.lt |
  all disj a1, a2: Allocator |
    (all x: a1.cone, y: a2.cone | x -> y in lt) implies
    (all i1: a1.allocs.inds, i2: a2.allocs.inds |
      a1.allocs[i1] -> a2.allocs[i2] in lt)
}

-- PARTITION MONOTONICITY (combined):
-- Full claim: allocation order is T1-consistent within each partition (T9),
-- and cross-partition T1 ordering is determined by cone ordering (T10a + T5).
-- Together these imply a globally consistent T1-linearisation of all allocated
-- addresses, compatible with every allocator's internal allocation order.
assert PartitionMonotonicity {
  let lt = Ord.lt | {
    -- Intra-allocator: T1 order is bi-consistent with allocation index order
    all a: Allocator, i, j: a.allocs.inds |
      i < j iff a.allocs[i] -> a.allocs[j] in lt
    -- Inter-allocator: cone T1 ordering lifts to allocation T1 ordering
    all disj a1, a2: Allocator |
      (all x: a1.cone, y: a2.cone | x -> y in lt) implies
      (all i1: a1.allocs.inds, i2: a2.allocs.inds |
        a1.allocs[i1] -> a2.allocs[i2] in lt)
  }
}

-- Non-vacuity: exhibit a valid model with 2 allocators, each making allocations
run NonVacuous {
  #Allocator = 2
  all a: Allocator | some a.allocs.elems
} for 5 but exactly 2 Allocator, 3 seq, 4 Int

check PM_IntraConsistency   for 5 but exactly 2 Allocator, 3 seq, 4 Int
check PM_InterConsistency   for 5 but exactly 2 Allocator, 3 seq, 4 Int
check PartitionMonotonicity for 5 but exactly 2 Allocator, 3 seq, 4 Int
