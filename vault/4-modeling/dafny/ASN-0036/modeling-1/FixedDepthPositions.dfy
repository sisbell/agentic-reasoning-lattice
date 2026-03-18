include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"

// S8-depth — FixedDepthPositions
module FixedDepthPositions {
  import opened TumblerAlgebra

  datatype State = State(M: map<Tumbler, map<Tumbler, Tumbler>>)

  // S8-depth — FixedDepthPositions
  // Within a given subspace s of document d, all V-positions share the same
  // tumbler depth:
  // (A d, v₁, v₂ : v₁ ∈ dom(Σ.M(d)) ∧ v₂ ∈ dom(Σ.M(d)) ∧ (v₁)₁ = (v₂)₁
  //   : #v₁ = #v₂)
  ghost predicate FixedDepthPositions(s: State) {
    forall d, v1, v2 ::
      (d in s.M && v1 in s.M[d] && v2 in s.M[d] &&
       |v1.components| >= 1 && |v2.components| >= 1 &&
       v1.components[0] == v2.components[0])
      ==>
      |v1.components| == |v2.components|
  }
}
