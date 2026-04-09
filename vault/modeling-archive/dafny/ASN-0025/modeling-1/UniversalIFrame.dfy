include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/Foundation/Foundation.dfy"
include "../../../../proofs/AddressProperties/ForwardAllocation.dfy"
include "../../../../proofs/AddressProperties/PartitionIndependence.dfy"
include "../../../../proofs/AddressProperties/AllocatorDiscipline.dfy"
include "../../../../proofs/AddressProperties/GlobalUniqueness.dfy"
include "../../../../proofs/AddressProperties/HierarchicalParsing.dfy"
include "../../../../proofs/AddressProperties/SubspaceDisjointness.dfy"
include "../../../../proofs/AddressPermanence/AddressPermanence.dfy"

module UniversalIFrameModule {
  import opened AddressPermanence
  import opened Foundation

  // UF — UniversalIFrame (FRAME, ensures)
  // Applies to every operation. Equivalent to P1 restated as a per-operation obligation.
  // (A a : a ∈ Σ.A : Σ'.ι(a) = Σ.ι(a))
  ghost predicate UniversalIFrame(s: State, s': State) {
    forall a :: a in Allocated(s) ==> a in Allocated(s') && s'.iota[a] == s.iota[a]
  }
}
