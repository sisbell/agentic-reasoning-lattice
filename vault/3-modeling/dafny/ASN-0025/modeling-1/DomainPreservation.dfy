include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/Foundation/Foundation.dfy"
include "../../../../proofs/AddressProperties/ForwardAllocation.dfy"
include "../../../../proofs/AddressProperties/PartitionIndependence.dfy"
include "../../../../proofs/AddressProperties/AllocatorDiscipline.dfy"
include "../../../../proofs/AddressProperties/GlobalUniqueness.dfy"
include "../../../../proofs/AddressProperties/HierarchicalParsing.dfy"
include "../../../../proofs/AddressProperties/SubspaceDisjointness.dfy"
include "../../../../proofs/AddressPermanence/AddressPermanence.dfy"

module DomainPreservationModule {
  import opened AddressPermanence
  import opened Foundation

  // Domain preservation — DomainPreservation (FRAME, ensures)
  // Applies to REARRANGE.
  // dom(Σ'.v(d)) = dom(Σ.v(d))
  ghost predicate DomainPreservation(s: State, s': State, d: DocId) {
    (d in s.vmap && d in s'.vmap) ==>
      s'.vmap[d].Keys == s.vmap[d].Keys
  }
}
