include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/Foundation/Foundation.dfy"
include "../../../../proofs/AddressProperties/ForwardAllocation.dfy"
include "../../../../proofs/AddressProperties/PartitionIndependence.dfy"
include "../../../../proofs/AddressProperties/AllocatorDiscipline.dfy"
include "../../../../proofs/AddressProperties/GlobalUniqueness.dfy"
include "../../../../proofs/AddressProperties/HierarchicalParsing.dfy"
include "../../../../proofs/AddressProperties/SubspaceDisjointness.dfy"
include "../../../../proofs/AddressPermanence/AddressPermanence.dfy"

module LinkContiguityModule {
  import opened AddressPermanence
  import opened Foundation

  // J2 — LinkContiguity (INV, predicate(State))
  // (A d : d in Sigma.D : {ord(q) : q in dom(Sigma.v(d)) /\ q is link} = {1, ..., |link positions in d|})
  ghost predicate LinkContiguity(s: State) {
    J2(s)
  }
}
