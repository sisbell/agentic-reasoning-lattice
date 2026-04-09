include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/Foundation/Foundation.dfy"
include "../../../../proofs/AddressProperties/ForwardAllocation.dfy"
include "../../../../proofs/AddressProperties/PartitionIndependence.dfy"
include "../../../../proofs/AddressProperties/AllocatorDiscipline.dfy"
include "../../../../proofs/AddressProperties/GlobalUniqueness.dfy"
include "../../../../proofs/AddressProperties/HierarchicalParsing.dfy"
include "../../../../proofs/AddressProperties/SubspaceDisjointness.dfy"
include "../../../../proofs/AddressPermanence/AddressPermanence.dfy"

module ISpaceGrowthModule {
  import opened AddressPermanence
  import opened Foundation

  // P0 — ISpaceGrowth (INV, predicate(State, State))
  // Σ.A ⊆ Σ'.A
  ghost predicate ISpaceGrowth(s: State, s': State) {
    Allocated(s) <= Allocated(s')
  }
}
