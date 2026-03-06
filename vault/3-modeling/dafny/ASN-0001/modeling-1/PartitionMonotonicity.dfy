include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "PrefixOrderingExtension.dfy"

module PartitionMonotonicity {

  import opened TumblerAlgebra
  import PrefixOrderingExtension

  // Helper: neither tumbler is a prefix of the other
  ghost predicate NonNesting(p1: Tumbler, p2: Tumbler) {
    !IsPrefix(p1, p2) && !IsPrefix(p2, p1)
  }

  // Helper: every element in the sequence extends the prefix
  ghost predicate AllExtend(stream: seq<Tumbler>, p: Tumbler) {
    forall i :: 0 <= i < |stream| ==> IsPrefix(p, stream[i])
  }

  // Partition monotonicity — PartitionMonotonicity
  // Within any prefix-delimited partition of the address space, the set of
  // allocated addresses is totally ordered by T1, and this order is consistent
  // with the allocation order of any single allocator within that partition.
  // Derived from T9, T10, T1, T5, T10a.
  lemma PartitionMonotonicity(
    p1: Tumbler, p2: Tumbler,
    stream1: seq<Tumbler>, stream2: seq<Tumbler>
  )
    requires LessThan(p1, p2)
    requires NonNesting(p1, p2)
    requires AllExtend(stream1, p1)
    requires AllExtend(stream2, p2)
    ensures forall i, j :: 0 <= i < |stream1| && 0 <= j < |stream2|
              ==> LessThan(stream1[i], stream2[j])
  { }
}
