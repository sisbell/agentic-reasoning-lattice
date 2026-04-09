include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/Foundation/Foundation.dfy"

module DocumentPermanence {
  import opened Foundation

  // ASN-0029 D2 — DocumentPermanence (INV, predicate(State, State))
  // [d ∈ Σ.D ⟹ d ∈ Σ'.D]
  // Documents, once created, are never removed.
  ghost predicate DocumentPermanence(s: State, s': State) {
    forall d :: d in s.docs ==> d in s'.docs
  }
}
