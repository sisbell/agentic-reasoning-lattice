include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/Foundation/Foundation.dfy"

module ReachableModule {
  import opened Foundation

  // ASN-0027 Σ.reachable — Reachable (INV, predicate(Addr, State))
  // reachable(a, Σ) ≡ refs(a) ≠ ∅
  // refs(a) = {(d, p) : d ∈ Σ.D ∧ 1 ≤ p ≤ n_d ∧ Σ.V(d)(p) = a}
  ghost predicate Reachable(a: IAddr, s: State) {
    exists d, q :: d in s.docs && d in s.vmap && q in s.vmap[d] && s.vmap[d][q] == a
  }
}
