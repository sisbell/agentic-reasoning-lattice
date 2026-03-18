include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/Foundation/Foundation.dfy"
include "../../../../proofs/AddressProperties/ForwardAllocation.dfy"
include "../../../../proofs/AddressProperties/PartitionIndependence.dfy"
include "../../../../proofs/AddressProperties/AllocatorDiscipline.dfy"
include "../../../../proofs/AddressProperties/GlobalUniqueness.dfy"
include "../../../../proofs/AddressProperties/HierarchicalParsing.dfy"
include "../../../../proofs/AddressProperties/SubspaceDisjointness.dfy"
include "../../../../proofs/AddressPermanence/AddressPermanence.dfy"

module VSpaceGroundedModule {
  import opened AddressPermanence
  import opened Foundation

  // J0 — VSpaceGrounded (INV, predicate(State))
  // (A d : d in Sigma.D : rng(Sigma.v(d)) <= Sigma.A)
  ghost predicate VSpaceGrounded(s: State) {
    J0(s)
  }
}
