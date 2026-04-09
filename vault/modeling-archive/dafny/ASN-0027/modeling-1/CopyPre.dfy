include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/Foundation/Foundation.dfy"

module CopyPre {
  import opened Foundation

  // ASN-0027 A4.pre — CopyPre (PRE, requires)
  // d_s ∈ Σ.D ∧ d_t ∈ Σ.D ∧ k ≥ 1 ∧ 1 ≤ p_s ∧ p_s + k − 1 ≤ n_{d_s} ∧ 1 ≤ p_t ≤ n_{d_t} + 1
  predicate CopyPre(s: State, ds: DocId, dt: DocId, ps: nat, k: nat, pt: nat) {
    ds in s.docs &&
    ds in s.vmap &&
    dt in s.docs &&
    dt in s.vmap &&
    k >= 1 &&
    ps >= 1 &&
    ps + k - 1 <= TextCount(s, ds) &&
    pt >= 1 &&
    pt <= TextCount(s, dt) + 1
  }
}
