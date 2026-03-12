include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/AddressAllocation/ForwardAllocation.dfy"
include "../../../../proofs/AddressAllocation/PartitionIndependence.dfy"
include "../../../../proofs/AddressAllocation/AllocatorDiscipline.dfy"
include "../../../../proofs/AddressAllocation/GlobalUniqueness.dfy"

module CreationBasedIdentity {
  import opened TumblerAlgebra
  import ForwardAllocation
  import GlobalUniqueness

  // ASN-0026 P4 — CreationBasedIdentity (LEMMA)
  // Distinct allocation acts produce distinct I-addresses.
  // Derived from ASN-0001 GlobalUniqueness.
  lemma CreationBasedIdentity(
    s: ForwardAllocation.AllocState,
    owner: map<ForwardAllocation.AllocatorId, Tumbler>,
    a1: GlobalUniqueness.Allocation,
    a2: GlobalUniqueness.Allocation
  )
    requires GlobalUniqueness.AllStreamsOrdered(s)
    requires GlobalUniqueness.PrefixOwnership(s, owner)
    requires a1.allocator in s.streams
    requires a1.index < |s.streams[a1.allocator]|
    requires a2.allocator in s.streams
    requires a2.index < |s.streams[a2.allocator]|
    requires GlobalUniqueness.DistinctAllocations(a1, a2)
    ensures GlobalUniqueness.AllocAddress(s, a1) != GlobalUniqueness.AllocAddress(s, a2)
  {
    GlobalUniqueness.GlobalUniqueness(s, owner, a1, a2);
  }
}
