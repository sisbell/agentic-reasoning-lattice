include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/Foundation/Foundation.dfy"

module DeletePre {
  import opened Foundation

  // ASN-0027 A2.pre — DeletePre (PRE, requires)
  // d ∈ Σ.D ∧ 1 ≤ p ∧ p + k − 1 ≤ n_d ∧ k ≥ 1
  predicate DeletePre(s: State, d: DocId, p: nat, k: nat) {
    d in s.docs &&
    d in s.vmap &&
    p >= 1 &&
    k >= 1 &&
    p + k - 1 <= TextCount(s, d)
  }
}
