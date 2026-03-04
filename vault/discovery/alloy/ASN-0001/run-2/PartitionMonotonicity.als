-- PartitionMonotonicity.als
-- Within any prefix-delimited partition, allocated addresses are
-- totally ordered by lexicographic order (T1), consistent with
-- each allocator's allocation sequence (T9).
--
-- Assumes: T9 (per-allocator monotonicity), T10/T10a (prefix
-- disjointness, sibling prefixes same length / non-nesting).

-- Simplified tumbler: 3 non-negative integer components
sig Tumbler {
  c1: Int,
  c2: Int,
  c3: Int
} {
  c1 >= 0
  c2 >= 0
  c3 >= 0
}

-- Distinct atoms have distinct component triples
fact UniqueTumblers {
  all disj a, b: Tumbler |
    not (a.c1 = b.c1 and a.c2 = b.c2 and a.c3 = b.c3)
}

-- Strict lexicographic less-than (T1)
pred lexLt[a, b: Tumbler] {
  a.c1 < b.c1
  or (a.c1 = b.c1 and a.c2 < b.c2)
  or (a.c1 = b.c1 and a.c2 = b.c2 and a.c3 < b.c3)
}

-- Prefix partition: tumblers sharing first component
pred samePartition[a, b: Tumbler] {
  a.c1 = b.c1
}

-- Allocator with ordered allocation sequence
sig Allocator {
  addrs: set Tumbler,
  precedes: Tumbler -> Tumbler
}

-- precedes is a strict total order on each allocator's addrs
fact AllocOrderProperties {
  all a: Allocator {
    a.precedes in a.addrs -> a.addrs
    no t: a.addrs | t -> t in a.precedes
    all x, y, z: a.addrs |
      (x -> y in a.precedes and y -> z in a.precedes)
        implies x -> z in a.precedes
    all disj x, y: a.addrs |
      x -> y in a.precedes or y -> x in a.precedes
  }
}

-- Each allocator's addresses lie in a single partition
fact AllocatorWithinPartition {
  all a: Allocator | all disj x, y: a.addrs | samePartition[x, y]
}

-- T9 assumption: allocation order implies lexicographic order
fact T9_PerAllocatorMonotonicity {
  all a: Allocator | all disj x, y: a.addrs |
    x -> y in a.precedes implies lexLt[x, y]
}

--------------------------------------------------------------
-- Assertions
--------------------------------------------------------------

-- Lex order is total within any partition
assert LexTotalInPartition {
  all disj a, b: Tumbler |
    samePartition[a, b] implies (lexLt[a, b] or lexLt[b, a])
}

-- Combined: addresses in a partition are totally ordered by lex,
-- consistent with each allocator's sequence
assert PartitionMonotonicity {
  -- All allocated addresses in the same partition are lex-comparable
  (all disj t1, t2: Allocator.addrs |
    samePartition[t1, t2] implies (lexLt[t1, t2] or lexLt[t2, t1]))
  and
  -- Lex order is consistent with each allocator's allocation order
  (all a: Allocator | all disj x, y: a.addrs |
    x -> y in a.precedes implies lexLt[x, y])
}

check LexTotalInPartition for 5 but 4 Int
check PartitionMonotonicity for 5 but 4 Int

-- Non-vacuity: two allocators each with two addresses in the same partition
run NonVacuity {
  #Allocator >= 2
  all a: Allocator | #a.addrs >= 2
  all t: Allocator.addrs | t.c1 = 1
} for 5 but exactly 4 Tumbler, exactly 2 Allocator, 4 Int
