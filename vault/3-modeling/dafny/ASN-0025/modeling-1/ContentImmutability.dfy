include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/Foundation/Foundation.dfy"
include "../../../../proofs/AddressProperties/ForwardAllocation.dfy"
include "../../../../proofs/AddressProperties/PartitionIndependence.dfy"
include "../../../../proofs/AddressProperties/AllocatorDiscipline.dfy"
include "../../../../proofs/AddressProperties/GlobalUniqueness.dfy"
include "../../../../proofs/AddressProperties/HierarchicalParsing.dfy"
include "../../../../proofs/AddressProperties/SubspaceDisjointness.dfy"
include "../../../../proofs/AddressPermanence/AddressPermanence.dfy"

module ContentImmutabilityModule {
  import opened AddressPermanence
  import opened Foundation

  // P1 — ContentImmutability (INV, predicate(State, State))
  // (A a : a ∈ Σ.A : Σ'.ι(a) = Σ.ι(a))
  ghost predicate ContentImmutability(s: State, s': State) {
    forall a :: a in Allocated(s) ==> a in Allocated(s') && s'.iota[a] == s.iota[a]
  }
}
