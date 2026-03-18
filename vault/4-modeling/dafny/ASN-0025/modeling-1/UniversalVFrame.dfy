include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/Foundation/Foundation.dfy"
include "../../../../proofs/AddressProperties/ForwardAllocation.dfy"
include "../../../../proofs/AddressProperties/PartitionIndependence.dfy"
include "../../../../proofs/AddressProperties/AllocatorDiscipline.dfy"
include "../../../../proofs/AddressProperties/GlobalUniqueness.dfy"
include "../../../../proofs/AddressProperties/HierarchicalParsing.dfy"
include "../../../../proofs/AddressProperties/SubspaceDisjointness.dfy"
include "../../../../proofs/AddressPermanence/AddressPermanence.dfy"

module UniversalVFrameModule {
  import opened AddressPermanence
  import opened Foundation

  // UF-V — UniversalVFrame (FRAME, ensures)
  // Applies to every operation targeting document d.
  // (A d' : d' ∈ Σ.D ∧ d' ≠ d : Σ'.v(d') = Σ.v(d'))
  ghost predicate UniversalVFrame(s: State, s': State, d: DocId) {
    forall d' :: d' in s.docs && d' != d && d' in s.vmap ==>
      d' in s'.vmap && s'.vmap[d'] == s.vmap[d']
  }
}
