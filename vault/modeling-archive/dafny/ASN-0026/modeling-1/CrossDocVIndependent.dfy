include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/Foundation/Foundation.dfy"

module CrossDocVIndependent {
  import opened Foundation

  // ASN-0026 P7 — CrossDocVIndependent (INV, predicate(State, State))
  // (A d' : d' in Sigma.D /\ d' =/= target(op) : Sigma'.V(d') = Sigma.V(d'))
  ghost predicate CrossDocVIndependent(s: State, s': State, target: DocId) {
    forall d :: d in s.docs && d != target && d in s.vmap ==>
      d in s'.vmap && s'.vmap[d] == s.vmap[d]
  }
}
