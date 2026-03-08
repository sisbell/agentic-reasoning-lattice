include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/Foundation/Foundation.dfy"
include "../../../../proofs/AddressProperties/ForwardAllocation.dfy"
include "../../../../proofs/AddressProperties/PartitionIndependence.dfy"
include "../../../../proofs/AddressProperties/AllocatorDiscipline.dfy"
include "../../../../proofs/AddressProperties/GlobalUniqueness.dfy"
include "../../../../proofs/AddressProperties/HierarchicalParsing.dfy"
include "../../../../proofs/AddressProperties/SubspaceDisjointness.dfy"
include "../../../../proofs/AddressPermanence/AddressPermanence.dfy"

module LinkSubspaceFrameModule {
  import opened AddressPermanence
  import opened Foundation

  // Link-subspace frame — LinkSubspaceFrame (FRAME, ensures)
  // Applies to REARRANGE.
  // (A q : q ∈ dom(Σ.v(d)) ∧ q is a link position : Σ'.v(d)(q) = Σ.v(d)(q))
  ghost predicate LinkSubspaceFrame(s: State, s': State, d: DocId) {
    (d in s.vmap && d in s'.vmap) ==>
      forall q :: q in s.vmap[d] && IsLinkPos(q) ==>
        q in s'.vmap[d] && s'.vmap[d][q] == s.vmap[d][q]
  }
}
