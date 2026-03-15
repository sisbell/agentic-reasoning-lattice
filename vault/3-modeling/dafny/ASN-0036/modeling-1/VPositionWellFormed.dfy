include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/TumblerAlgebra/TumblerHierarchy.dfy"

// S8a — VPositionWellFormed
module VPositionWellFormed {
  import opened TumblerAlgebra
  import TumblerHierarchy

  datatype State = State(M: map<Tumbler, map<Tumbler, Tumbler>>)

  // All components strictly positive (no zeros)
  ghost predicate AllPositive(t: Tumbler) {
    |t.components| >= 1 &&
    forall i :: 0 <= i < |t.components| ==> t.components[i] > 0
  }

  // S8a — VPositionWellFormed
  // (A v ∈ dom(Σ.M(d)) : v₁ ≥ 1 : zeros(v) = 0 ∧ v > 0)
  // Text-subspace V-positions (first component ≥ 1) have no zero components.
  ghost predicate VPositionWellFormed(s: State) {
    forall d, v ::
      (d in s.M && v in s.M[d] && |v.components| >= 1 && v.components[0] >= 1)
      ==>
      (TumblerHierarchy.ZeroCount(v.components) == 0 && AllPositive(v))
  }
}
