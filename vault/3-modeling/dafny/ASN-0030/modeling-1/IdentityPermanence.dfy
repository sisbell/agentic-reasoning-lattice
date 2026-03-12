include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/Foundation/Foundation.dfy"
include "../../../../proofs/TwoSpace/ISpaceImmutable.dfy"
include "../../../../proofs/TwoSpace/ISpaceMonotone.dfy"

module IdentityPermanence {
  import opened Foundation
  import ISpaceImmutable
  import ISpaceMonotone

  // ASN-0030 A0 — IdentityPermanence (LEMMA, lemma)
  // Conjunction of P0 (ISpaceImmutable) and P1 (ISpaceMonotone) from ASN-0026.
  // For any state transition Σ → Σ':
  //   [a ∈ dom(Σ.I) ⟹ a ∈ dom(Σ'.I) ∧ Σ'.I(a) = Σ.I(a)]
  lemma IdentityPermanence(s: State, s': State)
    requires ISpaceImmutable.ISpaceImmutable(s, s')
    requires ISpaceMonotone.ISpaceMonotone(s, s')
    ensures forall a :: a in Allocated(s) ==>
              a in Allocated(s') && s'.iota[a] == s.iota[a]
  { }
}
