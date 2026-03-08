include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/Foundation/Foundation.dfy"
include "../../../../proofs/AddressProperties/ForwardAllocation.dfy"
include "../../../../proofs/AddressProperties/PartitionIndependence.dfy"
include "../../../../proofs/AddressProperties/AllocatorDiscipline.dfy"
include "../../../../proofs/AddressProperties/GlobalUniqueness.dfy"
include "../../../../proofs/AddressProperties/HierarchicalParsing.dfy"
include "../../../../proofs/AddressProperties/SubspaceDisjointness.dfy"
include "../../../../proofs/AddressPermanence/AddressPermanence.dfy"

module TransclusionIdentityModule {
  import opened AddressPermanence
  import opened Foundation

  // I-addresses referenced by a set of V-positions in a V-map
  function SpanAddrs(vd: map<VPos, IAddr>, span: set<VPos>): set<IAddr> {
    set q | q in span && q in vd :: vd[q]
  }

  // P5 — TransclusionIdentity (POST, ensures)
  // Applies to COPY. S = (s₁, ..., sₘ) is the I-address sequence of the
  // source span, where sᵢ = Σ.v(d_s)(qᵢ).
  // (A a : a ∈ S : visible(a, d, Σ'))
  ghost predicate TransclusionIdentity(s: State, s': State, d_s: DocId, d: DocId, span: set<VPos>) {
    (d_s in s.vmap && d in s'.vmap) ==>
      forall a :: a in SpanAddrs(s.vmap[d_s], span) ==>
        VisibleInDoc(a, d, s')
  }
}
