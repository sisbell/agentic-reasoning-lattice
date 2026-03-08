include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/Foundation/Foundation.dfy"
include "../../../../proofs/AddressProperties/ForwardAllocation.dfy"
include "../../../../proofs/AddressProperties/PartitionIndependence.dfy"
include "../../../../proofs/AddressProperties/AllocatorDiscipline.dfy"
include "../../../../proofs/AddressProperties/GlobalUniqueness.dfy"
include "../../../../proofs/AddressProperties/HierarchicalParsing.dfy"
include "../../../../proofs/AddressProperties/SubspaceDisjointness.dfy"
include "../../../../proofs/AddressPermanence/AddressPermanence.dfy"

module DocumentSetGrowthModule {
  import opened AddressPermanence
  import opened Foundation

  // P6 — DocumentSetGrowth (INV, predicate(State, State))
  // Σ.D ⊆ Σ'.D
  ghost predicate DocumentSetGrowth(s: State, s': State) {
    s.docs <= s'.docs
  }
}
