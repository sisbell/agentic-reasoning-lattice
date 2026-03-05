-- GlobalUniqueness: No two distinct allocations produce the same address.
-- Depends on T9 (Forward Allocation), T10 (Partition Independence),
-- T10a (Allocator Discipline).

open util/ordering[Allocation]

sig Partition {}

-- An allocation event produces an address identified by (partition, offset).
-- T10 (Partition Independence): address subspaces are partitioned by Partition.
-- T10a (Allocator Discipline): one allocator per partition, so allocations
-- within a partition are serialized by the global temporal order.
sig Allocation {
  partition: one Partition,
  offset: one Int
} {
  offset >= 0
}

-- T9: Forward Allocation — within each partition, the allocator's cursor
-- strictly advances. Allocations ordered earlier in time have strictly
-- smaller offsets than later allocations in the same partition.
fact ForwardAllocation {
  all disj a1, a2: Allocation |
    (a1.partition = a2.partition and lt[a1, a2]) implies
      a1.offset < a2.offset
}

-- Two allocations produce the same address iff they agree on partition and offset.
pred sameAddress[a1, a2: Allocation] {
  a1.partition = a2.partition
  a1.offset = a2.offset
}

-- Global Uniqueness: no two distinct allocations produce the same address.
assert GlobalUniqueness {
  all disj a1, a2: Allocation | not sameAddress[a1, a2]
}

-- Non-vacuity: the model admits multiple allocations across multiple partitions.
run NonVacuity {
  #Allocation > 2
  #Partition > 1
  some disj a1, a2: Allocation | a1.partition != a2.partition
} for 5 but 5 Int

check GlobalUniqueness for 5 but 5 Int
