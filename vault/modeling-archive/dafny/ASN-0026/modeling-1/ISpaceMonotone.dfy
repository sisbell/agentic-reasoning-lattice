include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/Foundation/Foundation.dfy"

module ISpaceMonotone {
  import opened Foundation

  // ASN-0026 P1 — ISpaceMonotone (INV, predicate(State, State))
  // [a in dom(Sigma.I) ==> a in dom(Sigma'.I)]
  ghost predicate ISpaceMonotone(s: State, s': State) {
    forall a :: a in Allocated(s) ==> a in Allocated(s')
  }
}
