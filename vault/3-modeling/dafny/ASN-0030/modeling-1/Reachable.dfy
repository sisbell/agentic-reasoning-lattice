include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/Foundation/Foundation.dfy"

module Reachable {
  import opened Foundation

  // ASN-0030 reachable(a, d) — Reachable (INV, predicate(Addr, DocId, State))
  // reachable(a, d) ≡ (E p : 1 ≤ p ≤ n_d : Σ.V(d)(p) = a)
  ghost predicate Reachable(a: IAddr, d: DocId, s: State)
    requires d in s.vmap
  {
    exists q :: q in s.vmap[d] && s.vmap[d][q] == a
  }
}
