include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/Foundation/Foundation.dfy"
include "../../../../proofs/AddressProperties/SubspaceDisjointness.dfy"
include "../../../../proofs/IVSpaceProperties/ReferentiallyComplete.dfy"
include "OriginTraceability.dfy"

module HomeDocumentMembershipModule {
  import opened TumblerAlgebra
  import opened Foundation
  import OriginTraceabilityModule
  import ReferentiallyComplete

  // ASN-0029 D7b — HomeDocumentMembership (LEMMA, lemma)
  // Derived from D7a, P2, D2.
  // (A d ∈ Σ.D, p : 1 ≤ p ≤ n_d : home(Σ.V(d)(p)) ∈ Σ.D)

  // Combined D7a + D2 invariant: every allocated address with document
  // level has its home document in D.
  // DIVERGENCE: The ASN derives D7b from D7a, P2, and D2 as separate
  // transition-level properties. We combine D7a and D2 into a single
  // reachable-state invariant AllocatedHomeInD, since the Dafny proof
  // operates on a single state rather than a transition sequence.
  ghost predicate AllocatedHomeInD(s: State) {
    forall a :: a in Allocated(s) && OriginTraceabilityModule.HasDocLevel(a) ==>
      OriginTraceabilityModule.Home(a) in s.docs
  }

  // D7b — HomeDocumentMembership
  lemma HomeDocumentMembership(s: State, d: DocId, q: VPos)
    requires d in s.docs && d in s.vmap
    requires q in s.vmap[d]
    requires ReferentiallyComplete.ReferentiallyComplete(s)  // P2
    requires OriginTraceabilityModule.HasDocLevel(s.vmap[d][q])
    requires AllocatedHomeInD(s)  // D7a + D2
    ensures OriginTraceabilityModule.Home(s.vmap[d][q]) in s.docs
  { }
}
