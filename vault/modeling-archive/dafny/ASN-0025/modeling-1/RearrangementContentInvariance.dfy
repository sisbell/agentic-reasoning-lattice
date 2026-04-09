include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/Foundation/Foundation.dfy"
include "../../../../proofs/AddressProperties/ForwardAllocation.dfy"
include "../../../../proofs/AddressProperties/PartitionIndependence.dfy"
include "../../../../proofs/AddressProperties/AllocatorDiscipline.dfy"
include "../../../../proofs/AddressProperties/GlobalUniqueness.dfy"
include "../../../../proofs/AddressProperties/HierarchicalParsing.dfy"
include "../../../../proofs/AddressProperties/SubspaceDisjointness.dfy"
include "../../../../proofs/AddressPermanence/AddressPermanence.dfy"

module RearrangementContentInvarianceModule {
  import opened AddressPermanence
  import opened Foundation

  // Helper: set of v-positions in a v-map that map to a given address
  function Occurrences(vd: map<VPos, IAddr>, a: IAddr): set<VPos> {
    set q | q in vd && vd[q] == a
  }

  // P4 — RearrangementContentInvariance (POST, ensures)
  // Applies to REARRANGE.
  // (A a : a ∈ Σ.A : #{p ∈ dom(Σ'.v(d)) : Σ'.v(d)(p) = a}
  //                 = #{p ∈ dom(Σ.v(d))  : Σ.v(d)(p)  = a})
  ghost predicate RearrangementContentInvariance(s: State, s': State, d: DocId) {
    (d in s.vmap && d in s'.vmap) ==>
      forall a :: a in Allocated(s) ==>
        |Occurrences(s'.vmap[d], a)| == |Occurrences(s.vmap[d], a)|
  }
}
