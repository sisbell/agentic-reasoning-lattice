include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/Foundation/Foundation.dfy"

module RearrangePre {
  import opened Foundation

  // Strictly increasing sequence of naturals
  predicate StrictlyIncreasing(cuts: seq<nat>) {
    forall i, j :: 0 <= i < j < |cuts| ==> cuts[i] < cuts[j]
  }

  // ASN-0027 A3.pre — RearrangePre (PRE, requires)
  // d ∈ Σ.D ∧ m ∈ {3, 4} ∧ 1 ≤ c_1 < c_2 < ... < c_m ≤ n_d + 1
  predicate RearrangePre(s: State, d: DocId, cuts: seq<nat>) {
    d in s.docs &&
    d in s.vmap &&
    (|cuts| == 3 || |cuts| == 4) &&
    StrictlyIncreasing(cuts) &&
    cuts[0] >= 1 &&
    cuts[|cuts| - 1] <= TextCount(s, d) + 1
  }
}
