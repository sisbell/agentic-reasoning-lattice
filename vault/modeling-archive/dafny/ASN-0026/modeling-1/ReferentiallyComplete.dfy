include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/Foundation/Foundation.dfy"

module ReferentiallyComplete {
  import opened Foundation

  // ASN-0026 P2 — ReferentiallyComplete (INV, predicate(State))
  // [d in Sigma.D /\ 1 <= p <= n_d ==> Sigma.V(d)(p) in dom(Sigma.I)]
  ghost predicate ReferentiallyComplete(s: State) {
    forall d :: d in s.docs && d in s.vmap ==>
      forall q :: q in s.vmap[d] ==> s.vmap[d][q] in Allocated(s)
  }
}
