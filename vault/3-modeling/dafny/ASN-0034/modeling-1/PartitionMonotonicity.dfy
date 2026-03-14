include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"

// (Partition monotonicity) — ASN-0034
// Depends on: T5, T9, T10, T10a, TA5, PrefixOrderingExtension
module PartitionMonotonicity {
  import opened TumblerAlgebra

  ghost predicate NonNesting(p1: Tumbler, p2: Tumbler) {
    !IsPrefix(p1, p2) && !IsPrefix(p2, p1)
  }

  ghost predicate AllExtend(stream: seq<Tumbler>, p: Tumbler) {
    forall i :: 0 <= i < |stream| ==> IsPrefix(p, stream[i])
  }

  // T9: allocation produces strictly increasing addresses under T1
  ghost predicate StrictlyIncreasing(stream: seq<Tumbler>) {
    forall i, j :: 0 <= i < j < |stream| ==> LessThan(stream[i], stream[j])
  }

  // PrefixOrderingExtension — helper (separate ASN property, inlined)
  // If p1 < p2 under T1 and neither is a prefix of the other,
  // then every extension of p1 precedes every extension of p2.
  lemma PrefixOrderingExtension(p1: Tumbler, p2: Tumbler, a: Tumbler, b: Tumbler)
    requires LessThan(p1, p2)
    requires NonNesting(p1, p2)
    requires IsPrefix(p1, a)
    requires IsPrefix(p2, b)
    ensures LessThan(a, b)
  {
    var k :| LessThanAt(p1, p2, k);
    LessThanIntro(a, b, k);
  }

  // Part 1: Within a single allocator's strictly increasing stream,
  // any two distinct addresses are comparable under T1.
  lemma IntraPartitionTotalOrder(stream: seq<Tumbler>, i: nat, j: nat)
    requires StrictlyIncreasing(stream)
    requires 0 <= i < |stream| && 0 <= j < |stream| && i != j
    ensures LessThan(stream[i], stream[j]) || LessThan(stream[j], stream[i])
  { }

  // Part 2: Allocation order (stream index) matches T1 order.
  // Direct consequence of T9; stated for traceability.
  lemma AllocationOrderConsistency(stream: seq<Tumbler>, i: nat, j: nat)
    requires StrictlyIncreasing(stream)
    requires 0 <= i < j < |stream|
    ensures LessThan(stream[i], stream[j])
  { }

  // Part 3: Cross-partition monotonicity.
  // For non-nesting prefixes p1 < p2, every address extending p1
  // precedes every address extending p2 under T1.
  lemma CrossPartitionMonotonicity(
    p1: Tumbler, p2: Tumbler,
    stream1: seq<Tumbler>, stream2: seq<Tumbler>
  )
    requires LessThan(p1, p2)
    requires NonNesting(p1, p2)
    requires AllExtend(stream1, p1) && AllExtend(stream2, p2)
    ensures forall i, j :: 0 <= i < |stream1| && 0 <= j < |stream2|
              ==> LessThan(stream1[i], stream2[j])
  {
    forall i, j | 0 <= i < |stream1| && 0 <= j < |stream2|
      ensures LessThan(stream1[i], stream2[j])
    {
      PrefixOrderingExtension(p1, p2, stream1[i], stream2[j]);
    }
  }
}
