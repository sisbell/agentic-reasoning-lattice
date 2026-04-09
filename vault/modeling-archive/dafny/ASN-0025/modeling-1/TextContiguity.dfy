include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/Foundation/Foundation.dfy"
include "../../../../proofs/AddressProperties/ForwardAllocation.dfy"
include "../../../../proofs/AddressProperties/PartitionIndependence.dfy"
include "../../../../proofs/AddressProperties/AllocatorDiscipline.dfy"
include "../../../../proofs/AddressProperties/GlobalUniqueness.dfy"
include "../../../../proofs/AddressProperties/HierarchicalParsing.dfy"
include "../../../../proofs/AddressProperties/SubspaceDisjointness.dfy"
include "../../../../proofs/AddressPermanence/AddressPermanence.dfy"

module TextContiguityModule {
  import opened AddressPermanence
  import opened Foundation

  // J1 — TextContiguity (INV, predicate(State))
  // (A d : d in Sigma.D : {ord(q) : q in dom(Sigma.v(d)) /\ q is text} = {1, ..., |text positions in d|})
  ghost predicate TextContiguity(s: State) {
    J1(s)
  }
}
