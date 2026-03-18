include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/Foundation/Foundation.dfy"
include "Reachable.dfy"

module GloballyReachable {
  import opened Foundation
  import Reachable

  // ASN-0030 reachable(a) — GloballyReachable (INV, predicate(Addr, State))
  // reachable(a) ≡ (E d : d ∈ Σ.D : reachable(a, d))
  ghost predicate GloballyReachable(a: IAddr, s: State) {
    exists d :: d in s.docs && d in s.vmap && Reachable.Reachable(a, d, s)
  }
}
