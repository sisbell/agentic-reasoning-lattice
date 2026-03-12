module GlobalUniquenessModule {

  import opened TumblerAlgebra
  import ForwardAllocation
  import PartitionIndependenceModule
  import AllocatorDisciplineModule

  // ASN-0001 Global uniqueness — GlobalUniqueness (LEMMA, lemma)
  // No two distinct allocations, anywhere in the system, at any time,
  // produce the same address. Derived from T9, T10, T10a.

  // An allocation event: which allocator, which index in its stream
  datatype Allocation = Allocation(allocator: ForwardAllocation.AllocatorId, index: nat)

  // The address produced by an allocation
  function AllocAddress(s: ForwardAllocation.AllocState, alloc: Allocation): Tumbler
    requires alloc.allocator in s.streams
    requires alloc.index < |s.streams[alloc.allocator]|
  {
    s.streams[alloc.allocator][alloc.index]
  }

  // Two allocations are distinct if they differ in allocator or index
  ghost predicate DistinctAllocations(a1: Allocation, a2: Allocation) {
    a1.allocator != a2.allocator || a1.index != a2.index
  }

  // Each allocator's stream is strictly ordered (from T9)
  ghost predicate AllStreamsOrdered(s: ForwardAllocation.AllocState) {
    forall a :: a in s.streams ==> ForwardAllocation.StrictlyOrdered(s.streams[a])
  }

  // Each allocator owns a prefix, and addresses in its stream extend that prefix
  ghost predicate PrefixOwnership(
    s: ForwardAllocation.AllocState,
    owner: map<ForwardAllocation.AllocatorId, Tumbler>
  ) {
    // Every allocator has an ownership prefix
    (forall a :: a in s.streams ==> a in owner) &&
    // Every address in a stream extends its owner's prefix
    (forall a :: a in s.streams ==>
      forall i :: 0 <= i < |s.streams[a]| ==>
        IsPrefix(owner[a], s.streams[a][i])) &&
    // Distinct allocators have non-nesting prefixes (from T10a's tree structure)
    (forall a1, a2 :: a1 in owner && a2 in owner && a1 != a2 ==>
      !IsPrefix(owner[a1], owner[a2]) && !IsPrefix(owner[a2], owner[a1]))
  }

  // DIVERGENCE: The ASN states GlobalUniqueness depends on T9, T10, T10a but
  // does not specify the prefix-ownership structure explicitly. We model the
  // implicit assumption that T10a establishes: each allocator owns a non-nesting
  // prefix, and its addresses extend that prefix. This is the structural
  // precondition that connects T9 (intra-allocator) and T10 (inter-allocator).

  // GlobalUniqueness: no two distinct allocations produce the same address
  lemma GlobalUniqueness(
    s: ForwardAllocation.AllocState,
    owner: map<ForwardAllocation.AllocatorId, Tumbler>,
    a1: Allocation,
    a2: Allocation
  )
    requires AllStreamsOrdered(s)
    requires PrefixOwnership(s, owner)
    requires a1.allocator in s.streams
    requires a1.index < |s.streams[a1.allocator]|
    requires a2.allocator in s.streams
    requires a2.index < |s.streams[a2.allocator]|
    requires DistinctAllocations(a1, a2)
    ensures AllocAddress(s, a1) != AllocAddress(s, a2)
  { }
}
