include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/Foundation/Foundation.dfy"
include "../../../../proofs/AddressProperties/ForwardAllocation.dfy"
include "../../../../proofs/AddressProperties/PartitionIndependence.dfy"
include "../../../../proofs/AddressProperties/AllocatorDiscipline.dfy"
include "../../../../proofs/AddressProperties/GlobalUniqueness.dfy"
include "../../../../proofs/AddressProperties/HierarchicalParsing.dfy"
include "../../../../proofs/AddressProperties/SubspaceDisjointness.dfy"
include "../../../../proofs/AddressPermanence/AddressPermanence.dfy"

module CreationBasedIdentityModule {
  import opened AddressPermanence
  import opened TumblerAlgebra
  import ForwardAllocation
  import GlobalUniquenessModule

  // P7 — CreationBasedIdentity (LEMMA)
  // Derived from T9 (ForwardAllocation), T10 (PartitionIndependence),
  // GlobalUniqueness, P3 (ISpaceNonExtension).
  //
  // Each creation event allocates addresses within a single allocator's prefix.
  // Distinct creation events produce disjoint address sets.

  // A creation event: an allocator and the stream indices it allocated
  datatype CreationEvent = CreationEvent(
    allocator: ForwardAllocation.AllocatorId,
    indices: set<nat>
  )

  ghost predicate ValidEvent(e: CreationEvent, s: ForwardAllocation.AllocState) {
    e.allocator in s.streams &&
    forall i :: i in e.indices ==> i < |s.streams[e.allocator]|
  }

  // Distinct events: different allocator or disjoint index sets
  ghost predicate DistinctEvents(e1: CreationEvent, e2: CreationEvent) {
    e1.allocator != e2.allocator || e1.indices !! e2.indices
  }

  // Addresses allocated by an event
  function EventAddresses(e: CreationEvent, s: ForwardAllocation.AllocState): set<Tumbler>
    requires ValidEvent(e, s)
  {
    set i | i in e.indices :: s.streams[e.allocator][i]
  }

  // P7(a): Distinct creation events produce disjoint address sets
  lemma DisjointAllocation(
    e1: CreationEvent,
    e2: CreationEvent,
    s: ForwardAllocation.AllocState,
    owner: map<ForwardAllocation.AllocatorId, Tumbler>
  )
    requires ValidEvent(e1, s) && ValidEvent(e2, s)
    requires DistinctEvents(e1, e2)
    requires GlobalUniquenessModule.AllStreamsOrdered(s)
    requires GlobalUniquenessModule.PrefixOwnership(s, owner)
    ensures EventAddresses(e1, s) !! EventAddresses(e2, s)
  { }

  // P7(b): A shared I-address traces to a single creation event
  lemma SingleOrigin(
    a: Tumbler,
    e1: CreationEvent,
    e2: CreationEvent,
    s: ForwardAllocation.AllocState,
    owner: map<ForwardAllocation.AllocatorId, Tumbler>
  )
    requires ValidEvent(e1, s) && ValidEvent(e2, s)
    requires GlobalUniquenessModule.AllStreamsOrdered(s)
    requires GlobalUniquenessModule.PrefixOwnership(s, owner)
    requires a in EventAddresses(e1, s)
    requires a in EventAddresses(e2, s)
    ensures !DistinctEvents(e1, e2)
  { }

  // Corollary: events under different ownership prefixes produce disjoint addresses
  lemma IndependentCreation(
    e1: CreationEvent,
    e2: CreationEvent,
    s: ForwardAllocation.AllocState,
    owner: map<ForwardAllocation.AllocatorId, Tumbler>
  )
    requires ValidEvent(e1, s) && ValidEvent(e2, s)
    requires e1.allocator in owner && e2.allocator in owner
    requires owner[e1.allocator] != owner[e2.allocator]
    requires GlobalUniquenessModule.AllStreamsOrdered(s)
    requires GlobalUniquenessModule.PrefixOwnership(s, owner)
    ensures EventAddresses(e1, s) !! EventAddresses(e2, s)
  { }

  // Corollary (transclusion preservation): COPY does not allocate new addresses
  // (P3: Σ'.A = Σ.A, Σ'.ι = Σ.ι), so fields() applied to any transcluded
  // byte's I-address returns the originating document. No separate proof needed —
  // this is a direct consequence of ISpaceNonExtension.
}
