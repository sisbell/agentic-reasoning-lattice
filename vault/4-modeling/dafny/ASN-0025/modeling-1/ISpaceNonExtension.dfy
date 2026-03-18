include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/Foundation/Foundation.dfy"
include "../../../../proofs/AddressProperties/ForwardAllocation.dfy"
include "../../../../proofs/AddressProperties/PartitionIndependence.dfy"
include "../../../../proofs/AddressProperties/AllocatorDiscipline.dfy"
include "../../../../proofs/AddressProperties/GlobalUniqueness.dfy"
include "../../../../proofs/AddressProperties/HierarchicalParsing.dfy"
include "../../../../proofs/AddressProperties/SubspaceDisjointness.dfy"
include "../../../../proofs/AddressPermanence/AddressPermanence.dfy"

module ISpaceNonExtensionModule {
  import opened AddressPermanence
  import opened Foundation

  // P3 — ISpaceNonExtension (FRAME, ensures)
  // Applies to DELETE, REARRANGE, COPY.
  // Σ'.A = Σ.A ∧ Σ'.ι = Σ.ι
  ghost predicate ISpaceNonExtension(s: State, s': State) {
    Allocated(s') == Allocated(s) && s'.iota == s.iota
  }
}
